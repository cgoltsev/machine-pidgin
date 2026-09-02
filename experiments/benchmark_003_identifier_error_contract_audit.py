#!/usr/bin/env python3
"""Characterize Benchmark 003 identifier and malformed-input handling.

This development-only audit applies a fixed mutation matrix to the one public
Benchmark 003 synthetic fixture.  It records whether identifier/reference
mutations fail at record validation and whether malformed containers are
reported through a deliberate validation exception or leak an incidental
Python ``TypeError``/``AttributeError``.

The audit does not choose or implement an identifier schema or public error
contract.  It makes no model/provider calls, uses no held-out or participant
data, spends nothing, and grants no authority to extend the fixture set.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

import benchmark_003_equivalence_preflight as preflight


Mutation = Callable[[Any], Any]


def _set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> Any:
    current = value
    for token in path[:-1]:
        current = current[token]
    current[path[-1]] = replacement
    return value


def _replace_references(
    record: dict[str, Any], path: tuple[Any, ...], replacement: Any
) -> dict[str, Any]:
    """Replace one identifier and the fixture references that depend on it."""

    current: Any = record
    for token in path[:-1]:
        current = current[token]

    if path == ("canonical_labels", "blocker_risk"):
        old_value = path[-1]
        label_value = current.pop(old_value)
        current[replacement] = label_value
    else:
        old_value = current[path[-1]]
        current[path[-1]] = replacement

    if path == ("entities", 0, "id"):
        for fact in record["facts"]:
            if fact["entity_id"] == old_value:
                fact["entity_id"] = replacement
    elif path == ("facts", 0, "id"):
        for constraint in record["constraints"]:
            for condition in constraint["conditions"]:
                if condition["fact_id"] == old_value:
                    condition["fact_id"] = replacement
    elif path == ("canonical_labels", "blocker_risk"):
        for constraint in record["constraints"]:
            if constraint["on_pass_label_id"] == old_value:
                constraint["on_pass_label_id"] = replacement
            if constraint["on_fail_label_id"] == old_value:
                constraint["on_fail_label_id"] = replacement
            for condition in constraint["conditions"]:
                if condition["failure_label_id"] == old_value:
                    condition["failure_label_id"] = replacement
    else:
        raise ValueError(f"unsupported paired-identifier path: {path!r}")
    return record


def _replace_output_key(record: dict[str, Any], replacement: Any) -> dict[str, Any]:
    old_value = record["output"]["keys"][0]
    record["output"]["keys"][0] = replacement
    record["output"]["types"][replacement] = record["output"]["types"].pop(
        old_value
    )
    record["expected"][replacement] = record["expected"].pop(old_value)
    return record


IDENTIFIER_CASES: tuple[dict[str, Any], ...] = (
    {
        "case_id": "record-id-empty",
        "surface": "/id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(record, ("id",), ""),
    },
    {
        "case_id": "record-id-integer",
        "surface": "/id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(record, ("id",), 0),
    },
    {
        "case_id": "entity-id-empty-with-references",
        "surface": "/entities/0/id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _replace_references(
            record, ("entities", 0, "id"), ""
        ),
    },
    {
        "case_id": "entity-id-integer-with-references",
        "surface": "/entities/0/id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _replace_references(
            record, ("entities", 0, "id"), 0
        ),
    },
    {
        "case_id": "fact-id-empty-with-references",
        "surface": "/facts/0/id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _replace_references(
            record, ("facts", 0, "id"), ""
        ),
    },
    {
        "case_id": "fact-id-integer-with-references",
        "surface": "/facts/0/id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _replace_references(
            record, ("facts", 0, "id"), 0
        ),
    },
    {
        "case_id": "constraint-id-empty",
        "surface": "/constraints/0/id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "id"), ""
        ),
    },
    {
        "case_id": "constraint-id-integer",
        "surface": "/constraints/0/id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "id"), 0
        ),
    },
    {
        "case_id": "canonical-label-id-empty-with-references",
        "surface": "/canonical_labels/blocker_risk",
        "invalid_value": "empty-string",
        "mutation": lambda record: _replace_references(
            record, ("canonical_labels", "blocker_risk"), ""
        ),
    },
    {
        "case_id": "canonical-label-id-integer-with-references",
        "surface": "/canonical_labels/blocker_risk",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _replace_references(
            record, ("canonical_labels", "blocker_risk"), 0
        ),
    },
    {
        "case_id": "output-key-empty-with-dependent-maps",
        "surface": "/output/keys/0",
        "invalid_value": "empty-string",
        "mutation": lambda record: _replace_output_key(record, ""),
    },
    {
        "case_id": "output-key-integer-with-dependent-maps",
        "surface": "/output/keys/0",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _replace_output_key(record, 0),
    },
    {
        "case_id": "fact-entity-reference-empty",
        "surface": "/facts/0/entity_id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record, ("facts", 0, "entity_id"), ""
        ),
    },
    {
        "case_id": "fact-entity-reference-integer",
        "surface": "/facts/0/entity_id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record, ("facts", 0, "entity_id"), 0
        ),
    },
    {
        "case_id": "condition-fact-reference-empty",
        "surface": "/constraints/0/conditions/0/fact_id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "conditions", 0, "fact_id"), ""
        ),
    },
    {
        "case_id": "condition-fact-reference-integer",
        "surface": "/constraints/0/conditions/0/fact_id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "conditions", 0, "fact_id"), 0
        ),
    },
    {
        "case_id": "condition-failure-label-reference-empty",
        "surface": "/constraints/0/conditions/0/failure_label_id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record,
            ("constraints", 0, "conditions", 0, "failure_label_id"),
            "",
        ),
    },
    {
        "case_id": "condition-failure-label-reference-integer",
        "surface": "/constraints/0/conditions/0/failure_label_id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record,
            ("constraints", 0, "conditions", 0, "failure_label_id"),
            0,
        ),
    },
    {
        "case_id": "constraint-pass-label-reference-empty",
        "surface": "/constraints/0/on_pass_label_id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "on_pass_label_id"), ""
        ),
    },
    {
        "case_id": "constraint-pass-label-reference-integer",
        "surface": "/constraints/0/on_pass_label_id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "on_pass_label_id"), 0
        ),
    },
    {
        "case_id": "constraint-fail-label-reference-empty",
        "surface": "/constraints/0/on_fail_label_id",
        "invalid_value": "empty-string",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "on_fail_label_id"), ""
        ),
    },
    {
        "case_id": "constraint-fail-label-reference-integer",
        "surface": "/constraints/0/on_fail_label_id",
        "invalid_value": "integer-zero",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "on_fail_label_id"), 0
        ),
    },
)


RECORD_CONTAINER_CASES: tuple[dict[str, Any], ...] = (
    {
        "case_id": "record-root-null",
        "entrypoint": "validate_record",
        "surface": "/",
        "mutation": lambda _record: None,
    },
    {
        "case_id": "entity-item-null",
        "entrypoint": "validate_record",
        "surface": "/entities/0",
        "mutation": lambda record: _set_path(record, ("entities", 0), None),
    },
    {
        "case_id": "fact-item-null",
        "entrypoint": "validate_record",
        "surface": "/facts/0",
        "mutation": lambda record: _set_path(record, ("facts", 0), None),
    },
    {
        "case_id": "constraint-item-null",
        "entrypoint": "validate_record",
        "surface": "/constraints/0",
        "mutation": lambda record: _set_path(record, ("constraints", 0), None),
    },
    {
        "case_id": "condition-item-null",
        "entrypoint": "validate_record",
        "surface": "/constraints/0/conditions/0",
        "mutation": lambda record: _set_path(
            record, ("constraints", 0, "conditions", 0), None
        ),
    },
    {
        "case_id": "authority-null",
        "entrypoint": "validate_record",
        "surface": "/authority",
        "mutation": lambda record: _set_path(record, ("authority",), None),
    },
    {
        "case_id": "canonical-labels-null",
        "entrypoint": "validate_record",
        "surface": "/canonical_labels",
        "mutation": lambda record: _set_path(
            record, ("canonical_labels",), None
        ),
    },
    {
        "case_id": "output-null",
        "entrypoint": "validate_record",
        "surface": "/output",
        "mutation": lambda record: _set_path(record, ("output",), None),
    },
)


ARTIFACT_CONTAINER_CASES: tuple[dict[str, Any], ...] = (
    {
        "case_id": "artifacts-root-null",
        "entrypoint": "validate_equivalence",
        "surface": "/",
        "mutation": lambda _artifacts: None,
    },
    {
        "case_id": "condition-artifact-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A",
        "mutation": lambda artifacts: _set_path(artifacts, ("A",), None),
    },
    {
        "case_id": "condition-artifact-list",
        "entrypoint": "validate_equivalence",
        "surface": "/A",
        "mutation": lambda artifacts: _set_path(artifacts, ("A",), []),
    },
    {
        "case_id": "audit-surface-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A/audit_surface",
        "mutation": lambda artifacts: _set_path(
            artifacts, ("A", "audit_surface"), None
        ),
    },
    {
        "case_id": "audit-surface-list",
        "entrypoint": "validate_equivalence",
        "surface": "/A/audit_surface",
        "mutation": lambda artifacts: _set_path(
            artifacts, ("A", "audit_surface"), []
        ),
    },
    {
        "case_id": "trace-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A/trace",
        "mutation": lambda artifacts: _set_path(artifacts, ("A", "trace"), None),
    },
    {
        "case_id": "trace-item-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A/trace/0",
        "mutation": lambda artifacts: _set_path(
            artifacts, ("A", "trace", 0), None
        ),
    },
    {
        "case_id": "system-prompt-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A/system_prompt",
        "mutation": lambda artifacts: _set_path(
            artifacts, ("A", "system_prompt"), None
        ),
    },
    {
        "case_id": "user-prompt-null",
        "entrypoint": "validate_equivalence",
        "surface": "/A/user_prompt",
        "mutation": lambda artifacts: _set_path(
            artifacts, ("A", "user_prompt"), None
        ),
    },
)


def _classify_call(call: Callable[[], Any]) -> dict[str, Any]:
    try:
        call()
    except preflight.EquivalenceError:
        return {
            "status": "REJECTED",
            "exception_class": "EquivalenceError",
            "interface": "aggregate-equivalence-error",
        }
    except ValueError as error:
        return {
            "status": "REJECTED",
            "exception_class": type(error).__name__,
            "interface": "record-value-error",
        }
    except (TypeError, AttributeError) as error:
        return {
            "status": "REJECTED",
            "exception_class": type(error).__name__,
            "interface": "incidental-python-exception",
        }
    except Exception as error:  # pragma: no cover - fail visible on new behavior
        return {
            "status": "REJECTED",
            "exception_class": type(error).__name__,
            "interface": "unexpected-exception",
        }
    return {
        "status": "ACCEPTED",
        "exception_class": None,
        "interface": "no-exception",
    }


def _identifier_result(
    base_record: dict[str, Any], case: dict[str, Any]
) -> dict[str, Any]:
    mutated = case["mutation"](copy.deepcopy(base_record))
    record_result = _classify_call(lambda: preflight.validate_record(mutated))
    render_result = {"status": "NOT_RUN", "exception_class": None, "interface": None}
    equivalence_result = {
        "status": "NOT_RUN",
        "exception_class": None,
        "interface": None,
    }
    artifacts: dict[str, dict[str, Any]] | None = None
    if record_result["status"] == "ACCEPTED":
        try:
            artifacts = preflight.render_all(mutated)
        except Exception as error:
            render_result = _classify_call(
                lambda error=error: (_ for _ in ()).throw(error)
            )
        else:
            render_result = {
                "status": "ACCEPTED",
                "exception_class": None,
                "interface": "no-exception",
            }
    if artifacts is not None:
        equivalence_result = _classify_call(
            lambda: preflight.validate_equivalence(artifacts, mutated)
        )
    return {
        "case_id": case["case_id"],
        "surface": case["surface"],
        "invalid_value": case["invalid_value"],
        "record_validation": record_result,
        "render_all": render_result,
        "validate_equivalence": equivalence_result,
    }


def _container_result(
    base_record: dict[str, Any], case: dict[str, Any]
) -> dict[str, Any]:
    if case["entrypoint"] == "validate_record":
        value = case["mutation"](copy.deepcopy(base_record))
        result = _classify_call(lambda: preflight.validate_record(value))
    else:
        artifacts = case["mutation"](preflight.render_all(base_record))
        result = _classify_call(
            lambda: preflight.validate_equivalence(artifacts, base_record)
        )
    return {
        "case_id": case["case_id"],
        "entrypoint": case["entrypoint"],
        "surface": case["surface"],
        "result": result,
    }


def _fixture_label(fixture: Path) -> str:
    try:
        return str(fixture.resolve().relative_to(preflight.FIXTURE.parent.parent))
    except ValueError:
        return str(fixture.resolve())


def run_audit(fixture: Path = preflight.FIXTURE) -> dict[str, Any]:
    base_record = preflight.load_record(fixture)
    base_before = preflight.canonical_json(base_record)
    base_sha256 = preflight._sha256_text(base_before)

    identifier_cases = [
        _identifier_result(base_record, case) for case in IDENTIFIER_CASES
    ]
    container_cases = [
        _container_result(base_record, case)
        for case in (*RECORD_CONTAINER_CASES, *ARTIFACT_CONTAINER_CASES)
    ]
    if preflight.canonical_json(base_record) != base_before:
        raise RuntimeError("audit mutated the caller-owned base record")

    record_identifier_accepts = [
        case
        for case in identifier_cases
        if case["record_validation"]["status"] == "ACCEPTED"
    ]
    deliberate_identifier_rejections = [
        case
        for case in identifier_cases
        if case["record_validation"]["interface"]
        in {"record-value-error", "aggregate-equivalence-error"}
    ]
    incidental_identifier_errors = [
        case
        for case in identifier_cases
        if case["record_validation"]["interface"]
        == "incidental-python-exception"
    ]
    unexpected_identifier_errors = [
        case
        for case in identifier_cases
        if case["record_validation"]["interface"] == "unexpected-exception"
    ]
    incidental_container_errors = [
        case
        for case in container_cases
        if case["result"]["interface"] == "incidental-python-exception"
    ]
    deliberate_container_errors = [
        case
        for case in container_cases
        if case["result"]["interface"]
        in {"record-value-error", "aggregate-equivalence-error"}
    ]
    accepted_container_cases = [
        case
        for case in container_cases
        if case["result"]["interface"] == "no-exception"
    ]
    unexpected_container_errors = [
        case
        for case in container_cases
        if case["result"]["interface"] == "unexpected-exception"
    ]

    return {
        "schema_version": (
            "benchmark-003-identifier-error-contract-audit/0.1-development"
        ),
        "evidence_class": "exploratory-development-characterization",
        "benchmark": "003",
        "question": (
            "Do all declared identifier/reference mutations fail at record validation, "
            "and do malformed JSON-like containers fail through a deliberate validation "
            "exception rather than an incidental Python exception?"
        ),
        "hypothesis": (
            "Every empty or non-string identifier/reference case will be rejected by "
            "validate_record, and every malformed-container case will avoid raw "
            "TypeError or AttributeError."
        ),
        "falsification_criterion": (
            "The hypothesis is falsified if any identifier/reference mutation is "
            "accepted or raises an incidental/unexpected exception at record validation, "
            "or if any malformed-container case raises TypeError or AttributeError "
            "instead of a deliberate validation exception."
        ),
        "scope": {
            "fixture": _fixture_label(fixture),
            "base_semantic_record_sha256": base_sha256,
            "runtime": {"python": sys.version.split()[0]},
            "identifier_reference_cases": len(identifier_cases),
            "malformed_container_cases": len(container_cases),
            "record_validation_entrypoint": "validate_record",
            "artifact_validation_entrypoint": "validate_equivalence",
        },
        "summary": {
            "identifier_cases_with_deliberate_record_rejection": (
                len(deliberate_identifier_rejections)
            ),
            "identifier_cases_accepted_at_record_validation": len(
                record_identifier_accepts
            ),
            "identifier_cases_with_incidental_record_exception": len(
                incidental_identifier_errors
            ),
            "identifier_cases_with_unexpected_record_exception": len(
                unexpected_identifier_errors
            ),
            "accepted_identifier_case_ids": [
                case["case_id"] for case in record_identifier_accepts
            ],
            "container_cases_with_deliberate_validation_exception": (
                len(deliberate_container_errors)
            ),
            "container_cases_with_incidental_python_exception": len(
                incidental_container_errors
            ),
            "container_cases_accepted": len(accepted_container_cases),
            "container_cases_with_unexpected_exception": len(
                unexpected_container_errors
            ),
            "incidental_exception_case_ids": [
                case["case_id"] for case in incidental_container_errors
            ],
        },
        "identifier_cases": identifier_cases,
        "malformed_container_cases": container_cases,
        "accounting": {
            "model_calls": 0,
            "provider_calls": 0,
            "paid_services": 0,
            "spend_usd": 0.0,
        },
        "limitations": [
            "One public synthetic development fixture and a fixed mutation matrix only.",
            "The matrix characterizes current Python validator behavior; it is not a general fuzzer or security-impact test.",
            "An incidental exception class does not by itself establish exploitability or deployment impact.",
            "The audit does not choose identifier syntax or the public exception hierarchy.",
            "No held-out, validation, model-behavior, participant, performance, or human-review evidence is produced.",
            "A named human must decide the schema and error contract before any repair or fixture extension.",
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
