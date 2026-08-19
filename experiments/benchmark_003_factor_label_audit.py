#!/usr/bin/env python3
"""Deterministic development audit of the current Benchmark 003 factor labels.

This audit binds one existing public synthetic fixture, the current A-D renderer, and
the published SPEAR/0.2 quick reference and interpretation prompt. It characterizes
whether the current stimuli support the planned representation and contract labels.
It does not change the renderer, choose a repair, establish semantic equivalence, or
replace the required named-human review.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import benchmark_003_equivalence_preflight as preflight


EXPERIMENTS_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENTS_DIR.parent
QUICK_REFERENCE = REPOSITORY_ROOT / "protocol" / "SPEAR_Protocol_Quick_Reference.md"
PUBLISHED_INTERPRETATION_PROMPT = REPOSITORY_ROOT / "protocol" / "SPEAR_LLM_PROMPT.md"

BOUND_SOURCES = {
    "protocol/SPEAR_Protocol_Quick_Reference.md": QUICK_REFERENCE,
    "protocol/SPEAR_LLM_PROMPT.md": PUBLISHED_INTERPRETATION_PROMPT,
    "experiments/benchmark_003_development_fixture.json": preflight.FIXTURE,
    "experiments/benchmark_003_equivalence_preflight.py": Path(preflight.__file__).resolve(),
}
EXPECTED_SOURCE_SHA256 = {
    "protocol/SPEAR_Protocol_Quick_Reference.md":
        "177b03883cd001340e6bb174d1fba72cace86b1d32a6cf76638b5fc9b9b12373",
    "protocol/SPEAR_LLM_PROMPT.md":
        "358ff23dc81861f45707af1a3507cd2a05e1818cae56fb33d8ccf7e867208c75",
    "experiments/benchmark_003_development_fixture.json":
        "36317fdf253e852e6b4602fcd02883c120a4344e1374fea23362473f45a02331",
    "experiments/benchmark_003_equivalence_preflight.py":
        "9bd92da526289a975d300e96297d7e2fd30ea556a1d1d74a22193a2c584a238a",
}

PUBLISHED_FIELDS = (
    "TASK",
    "OBJECTS & TYPES",
    "AUTHORITY",
    "ABSTRACTION",
    "OBJECTIVE",
    "CONSTRAINTS",
    "PRECEDENCE & VOCABULARY",
    "UNCERTAINTY",
    "OUTPUT",
    "EVALUATION & CHECK",
    "INTERACTION / STOP",
    "EXAMPLES",
)

# This mapping is an explicit Researcher-coded classification, not a conformance
# result or an independent construct-validity judgment. Exact-heading means only
# that the published heading appears verbatim; it does not imply full semantics.
FIELD_ASSESSMENT = {
    "TASK": {
        "classification": "exact_heading",
        "observed_sections": ["TASK"],
        "boundary": "Exact heading only; task fidelity is assessed elsewhere.",
    },
    "OBJECTS & TYPES": {
        "classification": "partial_construct",
        "observed_sections": ["ENTITIES", "FACTS"],
        "boundary": "Names, links, attributes, and values appear, but types, units, domains, and interfaces are not declared.",
    },
    "AUTHORITY": {
        "classification": "exact_heading",
        "observed_sections": ["AUTHORITY"],
        "boundary": "Exact heading and allowed/approval/prohibited lists; this does not establish legitimate authority or a human-override procedure.",
    },
    "ABSTRACTION": {
        "classification": "absent",
        "observed_sections": [],
        "boundary": "No PRESERVE, IGNORE, or ASSUME section.",
    },
    "OBJECTIVE": {
        "classification": "absent",
        "observed_sections": [],
        "boundary": "No objective or trade-off section.",
    },
    "CONSTRAINTS": {
        "classification": "partial_construct",
        "observed_sections": ["HARD_GATES"],
        "boundary": "Hard gates appear; the published HARD/SOFT distinction is not instantiated.",
    },
    "PRECEDENCE & VOCABULARY": {
        "classification": "partial_construct",
        "observed_sections": ["FAILURE_OUTPUT", "CANONICAL_LABELS"],
        "boundary": "Canonical labels and one output ordering appear; general rule, exception, source, and tie-break precedence do not.",
    },
    "UNCERTAINTY": {
        "classification": "absent",
        "observed_sections": [],
        "boundary": "No unknown, estimated, disputed, or variable-fact section.",
    },
    "OUTPUT": {
        "classification": "exact_heading",
        "observed_sections": ["OUTPUT"],
        "boundary": "Exact heading and JSON shape; this does not cover every published audience, length, notation, or precision dimension.",
    },
    "EVALUATION & CHECK": {
        "classification": "partial_construct",
        "observed_sections": ["HARD_GATES", "FAILURE_OUTPUT"],
        "boundary": "Mechanical pass/fail logic appears, but no separately declared final independent verification or broader acceptance-test section.",
    },
    "INTERACTION / STOP": {
        "classification": "partial_construct",
        "observed_sections": ["HARD_GATES", "AUTHORITY"],
        "boundary": "Hard gates and approval-required actions are present, but no clarification policy or explicit halt procedure is declared.",
    },
    "EXAMPLES": {
        "classification": "absent",
        "observed_sections": [],
        "boundary": "No positive, negative, or boundary examples.",
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def source_hashes() -> dict[str, str]:
    return {name: sha256_bytes(path.read_bytes()) for name, path in BOUND_SOURCES.items()}


def require_bound_sources() -> dict[str, str]:
    observed = source_hashes()
    if observed != EXPECTED_SOURCE_SHA256:
        changed = {
            name: {"expected": EXPECTED_SOURCE_SHA256.get(name), "observed": observed.get(name)}
            for name in sorted(set(observed) | set(EXPECTED_SOURCE_SHA256))
            if observed.get(name) != EXPECTED_SOURCE_SHA256.get(name)
        }
        raise RuntimeError("bound source changed: " + canonical_json(changed))
    return observed


def fenced_text(markdown: str) -> str:
    match = re.search(r"```text\n(.*?)\n```", markdown, flags=re.DOTALL)
    if match is None:
        raise ValueError("published interpretation prompt text block is missing")
    return match.group(1)


def field_sections(user_prompt: str) -> list[str]:
    return re.findall(r"^([A-Z][A-Z0-9_ &/\-]+):", user_prompt, flags=re.MULTILINE)


def prose_sections(user_prompt: str) -> list[str]:
    return re.findall(r"^([A-Z][A-Za-z -]+):", user_prompt, flags=re.MULTILINE)


def whitespace_word_count(value: str) -> int:
    return len(value.split())


def audit() -> dict[str, Any]:
    hashes = require_bound_sources()
    record = preflight.load_record(preflight.FIXTURE)
    artifacts = preflight.render_all(record)
    preflight_report = preflight.validate_equivalence(artifacts, record)

    published_prompt = fenced_text(PUBLISHED_INTERPRETATION_PROMPT.read_text(encoding="utf-8"))
    field_prompt = artifacts["B"]["user_prompt"]
    prose_prompt = artifacts["A"]["user_prompt"]
    field_headings = field_sections(field_prompt)
    prose_headings = prose_sections(prose_prompt)

    classifications = {
        name: sum(
            item["classification"] == name for item in FIELD_ASSESSMENT.values()
        )
        for name in ("exact_heading", "partial_construct", "absent")
    }
    if tuple(FIELD_ASSESSMENT) != PUBLISHED_FIELDS:
        raise AssertionError("field assessment does not cover the published field order")

    base_system = preflight.FROZEN_BASE_SYSTEM
    current_contract = preflight.FROZEN_INTERPRETATION_CONTRACT
    factor_checks = {
        "representation_factor_system_equal_without_contract":
            artifacts["A"]["system_prompt"] == artifacts["B"]["system_prompt"],
        "representation_factor_system_equal_with_contract":
            artifacts["C"]["system_prompt"] == artifacts["D"]["system_prompt"],
        "contract_factor_user_equal_for_prose":
            artifacts["A"]["user_prompt"] == artifacts["C"]["user_prompt"],
        "contract_factor_user_equal_for_fields":
            artifacts["B"]["user_prompt"] == artifacts["D"]["user_prompt"],
        "contract_preserves_base_system_verbatim": base_system in current_contract,
        "contract_equals_published_spear_0_2_prompt": current_contract == published_prompt,
    }

    return {
        "agenda": "benchmark_003_factor_label_audit",
        "status": "complete_negative_development_characterization",
        "evidence_class": "one_public_synthetic_development_fixture",
        "institute_position": "none",
        "source_sha256": hashes,
        "semantic_record_sha256": preflight_report["semantic_record_sha256"],
        "current_preflight_result": preflight_report["status"],
        "representation_factor": {
            "field_renderer_sections": field_headings,
            "field_renderer_section_count": len(field_headings),
            "prose_renderer_sections": prose_headings,
            "prose_renderer_section_count": len(prose_headings),
            "prose_renderer_is_explicitly_sectioned": bool(prose_headings),
            "published_spear_field_count": len(PUBLISHED_FIELDS),
            "published_spear_fields": list(PUBLISHED_FIELDS),
            "classification_counts": classifications,
            "field_assessment": FIELD_ASSESSMENT,
            "assessment_boundary": (
                "Researcher-coded lexical and construct mapping; not a conformance suite, "
                "semantic-equivalence proof, or independent human construct-validity review."
            ),
        },
        "contract_factor": {
            "base_system_sha256": sha256_text(base_system),
            "current_contract_sha256": sha256_text(current_contract),
            "published_interpretation_prompt_sha256": sha256_text(published_prompt),
            "base_system_word_count": whitespace_word_count(base_system),
            "current_contract_word_count": whitespace_word_count(current_contract),
            "published_interpretation_prompt_word_count": whitespace_word_count(published_prompt),
            "published_numbered_operating_rule_count": len(
                re.findall(r"^\d+\.", published_prompt, flags=re.MULTILINE)
            ),
            "current_contract_numbered_operating_rule_count": len(
                re.findall(r"^\d+\.", current_contract, flags=re.MULTILINE)
            ),
            "published_field_labels_present_verbatim_in_current_contract": [
                field for field in PUBLISHED_FIELDS if field in current_contract
            ],
        },
        "factor_isolation_checks": factor_checks,
        "falsifying_findings": [
            "The prose renderer has seven explicit labeled sections, so 'ordinary prose' is not an unstructured-prose control.",
            "The field renderer has three exact published SPEAR/0.2 headings, five Researcher-mapped partial constructs, and four absent published fields.",
            "The current contract replaces rather than preserves the no-contract base system prompt.",
            "The current contract is not the published SPEAR/0.2 interpretation prompt and reproduces none of its twelve rules as numbered rules; this lexical check does not deny partial semantic overlap.",
        ],
        "derived_researcher_disposition": "REVISE",
        "authority_boundary": (
            "This result chooses no rename, redesign, additive baseline, schema, policy, "
            "fixture extension, registration, model call, publication, or merge."
        ),
        "model_calls": 0,
        "provider_calls": 0,
        "paid_services": 0,
        "exact_spend_usd": "0.00",
    }


def main() -> None:
    print(canonical_json(audit()))


if __name__ == "__main__":
    main()
