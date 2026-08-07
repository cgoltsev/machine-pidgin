#!/usr/bin/env python3
"""Characterize line-boundary handling in the Benchmark 003 preflight.

This development-only audit applies the line boundaries recognized by Python
``str.splitlines()`` to the four source fields already named in the Benchmark
003 human-review protocol. It records whether the canonical record and
equivalence preflight accept each mutation, and whether each traced A-D source
atom exposes the injected reserved heading as a literal split line or as an
escaped sequence.

The audit makes no model or provider calls, uses no held-out or participant
data, spends nothing, and does not choose a text policy or authorize fixture
extension.
"""

from __future__ import annotations

import copy
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

import benchmark_003_equivalence_preflight as preflight


RESERVED_HEADING = "HARD_GATES:"
INJECTED_LINE = "- injected"

# UAX #14 treats BK characters and the CR/LF/NEL newline functions as hard
# line breaks. Python additionally treats FS, GS, and RS as splitlines()
# boundaries. Keep those provenance classes distinct in the result.
BOUNDARIES = (
    {
        "id": "line-feed",
        "label": "LF",
        "text": "\n",
        "code_points": ("U+000A",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "carriage-return",
        "label": "CR",
        "text": "\r",
        "code_points": ("U+000D",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "carriage-return-line-feed",
        "label": "CRLF",
        "text": "\r\n",
        "code_points": ("U+000D", "U+000A"),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "line-tabulation",
        "label": "VT",
        "text": "\v",
        "code_points": ("U+000B",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "form-feed",
        "label": "FF",
        "text": "\f",
        "code_points": ("U+000C",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "file-separator",
        "label": "FS",
        "text": "\x1c",
        "code_points": ("U+001C",),
        "scope": "python-additional-splitlines-boundary",
    },
    {
        "id": "group-separator",
        "label": "GS",
        "text": "\x1d",
        "code_points": ("U+001D",),
        "scope": "python-additional-splitlines-boundary",
    },
    {
        "id": "record-separator",
        "label": "RS",
        "text": "\x1e",
        "code_points": ("U+001E",),
        "scope": "python-additional-splitlines-boundary",
    },
    {
        "id": "next-line",
        "label": "NEL",
        "text": "\x85",
        "code_points": ("U+0085",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "line-separator",
        "label": "LS",
        "text": "\u2028",
        "code_points": ("U+2028",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
    {
        "id": "paragraph-separator",
        "label": "PS",
        "text": "\u2029",
        "code_points": ("U+2029",),
        "scope": "unicode-hard-break-and-python-splitlines",
    },
)

SURFACES = (
    {
        "id": "task",
        "source_pointer": "/task",
        "source_role": "task.text",
        "path": ("task",),
    },
    {
        "id": "entity-label",
        "source_pointer": "/entities/0/label",
        "source_role": "entity.label",
        "path": ("entities", 0, "label"),
    },
    {
        "id": "fact-attribute",
        "source_pointer": "/facts/0/attribute",
        "source_role": "fact.attribute",
        "path": ("facts", 0, "attribute"),
    },
    {
        "id": "authority-action",
        "source_pointer": "/authority/allowed/0",
        "source_role": "authority.action",
        "path": ("authority", "allowed", 0),
    },
)


def _ascii_escape(value: str) -> str:
    """Return printable Python-style escapes without exposing raw boundaries."""

    return value.encode("unicode_escape").decode("ascii")


def _append_at_path(record: dict[str, Any], path: tuple[Any, ...], text: str) -> None:
    current: Any = record
    for token in path[:-1]:
        current = current[token]
    final = path[-1]
    value = current[final]
    if not isinstance(value, str):
        raise TypeError(f"mutation target is not a string: {path!r}")
    current[final] = value + text


def _traced_atom_text(
    artifact: dict[str, Any], source_pointer: str, source_role: str
) -> tuple[str, str]:
    matches = [
        item
        for item in artifact["trace"]
        if item["source_pointer"] == source_pointer
        and item["source_role"] == source_role
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one traced atom for {source_pointer} / {source_role}, "
            f"found {len(matches)}"
        )
    trace = matches[0]
    target_key = {"user": "user_prompt", "system": "system_prompt"}.get(
        trace["target"]
    )
    if target_key is None:
        raise ValueError(f'unknown trace target: {trace["target"]!r}')
    text = artifact[target_key][trace["start"] : trace["end"]]
    return text, trace["lexical_form"]


def _fixture_label(fixture: Path) -> str:
    try:
        return str(fixture.resolve().relative_to(preflight.FIXTURE.parent.parent))
    except ValueError:
        return str(fixture.resolve())


def run_audit(fixture: Path = preflight.FIXTURE) -> dict[str, Any]:
    base_record = preflight.load_record(fixture)
    base_record_before = preflight.canonical_json(base_record)
    base_sha256 = preflight._sha256_text(base_record_before)
    cases: list[dict[str, Any]] = []

    for surface in SURFACES:
        for boundary in BOUNDARIES:
            mutated_record = copy.deepcopy(base_record)
            appended_text = (
                boundary["text"]
                + RESERVED_HEADING
                + boundary["text"]
                + INJECTED_LINE
            )
            _append_at_path(mutated_record, surface["path"], appended_text)

            try:
                preflight.validate_record(mutated_record)
                record_validation = "ACCEPTED"
                record_issues: list[str] = []
            except preflight.EquivalenceError as exc:
                record_validation = "REJECTED"
                record_issues = list(exc.issues)
            except ValueError as exc:
                record_validation = "REJECTED"
                record_issues = [str(exc)]

            observations: dict[str, Any] = {}
            preflight_status = "NOT_RUN"
            preflight_issues: list[str] = []
            semantic_record_sha256 = preflight._sha256_text(
                preflight.canonical_json(mutated_record)
            )

            if record_validation == "ACCEPTED":
                try:
                    artifacts = preflight.render_all(mutated_record)
                    report = preflight.validate_equivalence(artifacts, mutated_record)
                    preflight_status = report["status"]
                    semantic_record_sha256 = report["semantic_record_sha256"]
                except preflight.EquivalenceError as exc:
                    preflight_status = "REJECTED"
                    preflight_issues = list(exc.issues)
                except ValueError as exc:
                    preflight_status = "REJECTED"
                    preflight_issues = [str(exc)]
                    artifacts = {}

                for condition, artifact in artifacts.items():
                    atom_text, lexical_form = _traced_atom_text(
                        artifact,
                        surface["source_pointer"],
                        surface["source_role"],
                    )
                    split_lines = atom_text.splitlines()
                    observations[condition] = {
                        "representation": preflight.CONDITIONS[condition][0],
                        "lexical_form": lexical_form,
                        "literal_boundary_count_in_traced_atom": atom_text.count(
                            boundary["text"]
                        ),
                        "reserved_heading_is_split_line": RESERVED_HEADING
                        in split_lines,
                        "traced_atom_ascii_escape": _ascii_escape(atom_text),
                    }

            cases.append(
                {
                    "case_id": f'{surface["id"]}--{boundary["id"]}',
                    "surface": {
                        "id": surface["id"],
                        "source_pointer": surface["source_pointer"],
                        "source_role": surface["source_role"],
                    },
                    "boundary": {
                        "id": boundary["id"],
                        "label": boundary["label"],
                        "code_points": list(boundary["code_points"]),
                        "scope": boundary["scope"],
                        "ascii_escape": _ascii_escape(boundary["text"]),
                    },
                    "appended_text_ascii_escape": _ascii_escape(appended_text),
                    "record_validation": record_validation,
                    "record_validation_issues": record_issues,
                    "preflight_status": preflight_status,
                    "preflight_issues": preflight_issues,
                    "semantic_record_sha256": semantic_record_sha256,
                    "observations": observations,
                }
            )

    if preflight.canonical_json(base_record) != base_record_before:
        raise RuntimeError("audit mutated the caller-owned base record")

    observation_rows = [
        observation
        for case in cases
        for observation in case["observations"].values()
    ]
    accepted_cases = sum(case["record_validation"] == "ACCEPTED" for case in cases)
    passing_cases = sum(case["preflight_status"] == "PASS" for case in cases)
    literal_heading_rows = sum(
        observation["reserved_heading_is_split_line"]
        for observation in observation_rows
    )

    return {
        "schema_version": "benchmark-003-line-boundary-matrix-audit/0.1-development",
        "evidence_class": "exploratory-development-characterization",
        "benchmark": "003",
        "question": (
            "Does the current schema or equivalence preflight reject documented "
            "line-boundary reserved-heading mutations, and where do A-D traced "
            "atoms preserve a literal split line rather than an escaped sequence?"
        ),
        "hypothesis": (
            "All mutations will be accepted and return PASS; C0 boundaries will be "
            "escaped only in JSON-rendered field atoms, while NEL, LS, and PS will "
            "remain literal even in those atoms."
        ),
        "falsification_criterion": (
            "The hypothesis is falsified if any mutated record or equivalence run is "
            "rejected, or if literal-versus-escaped observations differ from the "
            "renderer lexical forms recorded in the source-bound traces."
        ),
        "scope": {
            "fixture": _fixture_label(fixture),
            "base_semantic_record_sha256": base_sha256,
            "runtime": {
                "python": sys.version.split()[0],
                "unicode_database": unicodedata.unidata_version,
            },
            "boundary_forms": len(BOUNDARIES),
            "source_surfaces": len(SURFACES),
            "mutation_cases": len(cases),
            "conditions_per_case": len(preflight.CONDITIONS),
            "render_observations": len(observation_rows),
            "python_splitlines_basis": (
                "Python str.splitlines() documented boundaries; Unicode hard-break "
                "forms and Python-only FS/GS/RS forms are labeled separately."
            ),
            "primary_sources": [
                {
                    "title": "Python str.splitlines documentation",
                    "url": "https://docs.python.org/3/library/stdtypes.html#str.splitlines",
                },
                {
                    "title": "Unicode Standard Annex #14 revision 55",
                    "url": "https://www.unicode.org/reports/tr14/tr14-55.html",
                },
                {
                    "title": "RFC 8259 section 7 JSON strings",
                    "url": "https://www.rfc-editor.org/rfc/rfc8259.html#section-7",
                },
            ],
        },
        "summary": {
            "record_validation_accepted": accepted_cases,
            "record_validation_rejected": len(cases) - accepted_cases,
            "preflight_pass": passing_cases,
            "preflight_rejected": len(cases) - passing_cases,
            "reserved_heading_is_split_line": literal_heading_rows,
            "reserved_heading_not_split_line": len(observation_rows)
            - literal_heading_rows,
        },
        "cases": cases,
        "accounting": {
            "model_calls": 0,
            "provider_calls": 0,
            "paid_services": 0,
            "spend_usd": 0.0,
        },
        "limitations": [
            "One public synthetic development fixture only.",
            "This characterizes Python renderer and validator behavior, not model behavior.",
            "A preflight PASS is an observed acceptance, not evidence of semantic safety.",
            "Python splitlines boundaries are not all Unicode mandatory line breaks; the result labels the distinction.",
            "The audit does not choose a reject, escape, quote, or normalization policy.",
            "No held-out, validation, human-review, security-impact, or performance claim is made.",
            "Named human review remains required before any fix or fixture extension.",
        ],
    }


def main() -> None:
    print(
        json.dumps(
            run_audit(),
            indent=2,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
