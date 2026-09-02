#!/usr/bin/env python3
"""Development-only deterministic renderer and equivalence preflight for Benchmark 003.

This prototype deliberately makes no model calls. It renders conditions A-D from one
canonical semantic record and fails closed when their auditable semantic surfaces differ.
It is a development control, not evidence that arbitrary natural-language paraphrases are
semantically equivalent and not a substitute for blinded human review before freezing.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


FIXTURE = Path(__file__).with_name("benchmark_003_development_fixture.json")
CONDITIONS = {
    "A": ("ordinary_prose", False),
    "B": ("spear_fields", False),
    "C": ("ordinary_prose", True),
    "D": ("spear_fields", True),
}
ROOT_KEYS = {
    "schema_version",
    "id",
    "split",
    "status",
    "task",
    "entities",
    "facts",
    "constraints",
    "authority",
    "canonical_labels",
    "output",
    "expected",
}
ARTIFACT_KEYS = {
    "schema_version",
    "fixture_id",
    "evidence_class",
    "condition",
    "task_representation",
    "interpretation_contract",
    "system_prompt",
    "user_prompt",
    "trace",
    "audit_surface",
    "artifact_sha256",
}
TRACE_KEYS = {
    "target",
    "start",
    "end",
    "text_sha256",
    "category",
    "source_pointer",
    "source_role",
    "lexical_form",
    "source_atom_sha256",
}
AUDIT_SURFACE_KEYS = {
    "task",
    "facts",
    "constraints",
    "authority",
    "entities",
    "canonical_labels",
    "output",
    "expected",
}
FROZEN_BASE_SYSTEM = "Complete the supplied task and return only the requested JSON object."
FROZEN_INTERPRETATION_CONTRACT = (
    "Interpret the supplied fields as a contract: preserve facts, apply every hard gate, "
    "respect authority boundaries, copy canonical vocabulary exactly, and return only the "
    "declared output schema. The contract supplies no task-specific fact or answer."
)
FROZEN_SYSTEM_PROMPTS = {
    False: FROZEN_BASE_SYSTEM,
    True: FROZEN_INTERPRETATION_CONTRACT,
}
FROZEN_SYSTEM_PROMPT_SHA256 = {
    False: "025b87c903682973ae4f374a10eea040b4ea7c3d4add019b41d09a8daac662ba",
    True: "cab85560ca7ce2db4d68315964dfc215c102efccf658f943b0bbfb35cbbcdbe1",
}
# Renderer-facing aliases are intentionally separate from the independent frozen controls.
BASE_SYSTEM = FROZEN_BASE_SYSTEM
INTERPRETATION_CONTRACT = FROZEN_INTERPRETATION_CONTRACT

# Filled from frozen, development-audited prompt skeletons; validation never derives these from
# a renderer. The two profiles are the only structural variants exercised by this narrow fixture.
FROZEN_USER_SKELETON_SHA256: dict[tuple[str, str], str] = {
    (
        "ordinary_prose",
        "base-one-action-per-level",
    ): "60674b397bcd85bfd356251c198a1256b8544ca66650c1f0c0d0991bdfa1a26c",
    (
        "spear_fields",
        "base-one-action-per-level",
    ): "11dac1222bb9127502862c2870585558c6a5b63af018110b3eb65890423eb7c5",
    (
        "ordinary_prose",
        "empty-authority-levels",
    ): "743ed3bef9449df251b05b03c8e6bcd6ef030f2b31af362c285d15de1e3b3d7b",
    (
        "spear_fields",
        "empty-authority-levels",
    ): "6f5935bfd151b86ae5aac4cbef9e4be908747f73fb9139fb7100654040c9800a",
}


class EquivalenceError(ValueError):
    """Raised with all detected preflight defects rather than a partial pass."""

    def __init__(self, issues: Iterable[str]):
        self.issues = tuple(issues)
        super().__init__("equivalence preflight failed:\n- " + "\n- ".join(self.issues))


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _format_scalar(value: Any) -> str:
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    return canonical_json(value)


def _pointer_escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _pointer_unescape(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def _pointer(*tokens: Any) -> str:
    return "/" + "/".join(_pointer_escape(str(token)) for token in tokens)


def _resolve_json_pointer(document: Any, pointer: str) -> Any:
    """Resolve a restricted RFC 6901 JSON Pointer without renderer involvement."""

    _require(isinstance(pointer, str) and pointer.startswith("/"), "invalid source pointer")
    current = document
    for encoded_token in pointer[1:].split("/"):
        token = _pointer_unescape(encoded_token)
        if isinstance(current, dict):
            _require(token in current, f"source pointer does not exist: {pointer}")
            current = current[token]
        elif isinstance(current, list):
            _require(token.isdigit(), f"source pointer list index is invalid: {pointer}")
            index = int(token)
            _require(0 <= index < len(current), f"source pointer is out of range: {pointer}")
            current = current[index]
        else:
            raise ValueError(f"source pointer traverses a scalar: {pointer}")
    return current


def _pointer_key(pointer: str) -> str:
    _require(pointer.startswith("/") and pointer != "/", "pointer has no key token")
    return _pointer_unescape(pointer.rsplit("/", 1)[1])


def _source_category(source_role: str) -> str:
    prefix = source_role.split(".", 1)[0]
    return {
        "task": "facts",
        "entity": "entities",
        "fact": "facts",
        "constraint": "constraints",
        "authority": "authority",
        "canonical_label": "canonical_labels",
        "output": "output_keys",
    }[prefix]


def _expected_atom_text(record: dict[str, Any], spec: dict[str, str]) -> str:
    """Derive one expected lexical atom directly from the canonical source record."""

    pointer = spec["source_pointer"]
    value = _resolve_json_pointer(record, pointer)
    lexical_form = spec["lexical_form"]
    if lexical_form == "raw":
        _require(isinstance(value, str), f"raw source atom is not a string: {pointer}")
        return value
    if lexical_form == "json":
        return canonical_json(value)
    if lexical_form == "pointer_key":
        return _pointer_key(pointer)
    if lexical_form == "operator_prose":
        _require(value in {"equals", "less_than"}, f"unsupported operator atom: {value}")
        return {"equals": "equals", "less_than": "is less than"}[value]
    if lexical_form == "kind_prose":
        _require(value == "all", f"unsupported constraint kind atom: {value}")
        return "every condition"
    if lexical_form == "authority_level_prose":
        return _pointer_key(pointer).replace("_", " ")
    if lexical_form == "label_value_json":
        _require(
            isinstance(value, str) and value in record["canonical_labels"],
            f"label reference does not resolve: {pointer}",
        )
        return canonical_json(record["canonical_labels"][value])
    raise ValueError(f"unknown lexical form: {lexical_form}")


def _source_atom_digest(record: dict[str, Any], spec: dict[str, str]) -> str:
    pointer = spec["source_pointer"]
    payload = {
        "source_pointer": pointer,
        "source_role": spec["source_role"],
        "lexical_form": spec["lexical_form"],
        "source_value": _resolve_json_pointer(record, pointer),
        "expected_text": _expected_atom_text(record, spec),
    }
    return _sha256_text(canonical_json(payload))


def _atom_spec(source_pointer: str, source_role: str, lexical_form: str) -> dict[str, str]:
    return {
        "source_pointer": source_pointer,
        "source_role": source_role,
        "lexical_form": lexical_form,
    }


def _expected_atom_specs(
    record: dict[str, Any], representation: str
) -> list[dict[str, str]]:
    """Traverse source semantics independently to define required atom coverage and order."""

    _require(
        representation in {"ordinary_prose", "spear_fields"},
        "unknown task representation",
    )
    prose = representation == "ordinary_prose"
    specs: list[dict[str, str]] = [
        _atom_spec(_pointer("task"), "task.text", "raw")
    ]
    for entity_index, _ in enumerate(record["entities"]):
        specs.extend(
            [
                _atom_spec(
                    _pointer("entities", entity_index, "id"), "entity.id", "raw"
                ),
                _atom_spec(
                    _pointer("entities", entity_index, "label"),
                    "entity.label",
                    "raw" if prose else "json",
                ),
            ]
        )
    for fact_index, _ in enumerate(record["facts"]):
        base = ("facts", fact_index)
        specs.extend(
            [
                _atom_spec(_pointer(*base, "id"), "fact.id", "raw"),
                _atom_spec(
                    _pointer(*base, "entity_id"), "fact.entity_id", "raw"
                ),
                _atom_spec(
                    _pointer(*base, "attribute"), "fact.attribute", "raw"
                ),
                _atom_spec(_pointer(*base, "value"), "fact.value", "json"),
            ]
        )
    for constraint_index, constraint in enumerate(record["constraints"]):
        base = ("constraints", constraint_index)
        specs.extend(
            [
                _atom_spec(_pointer(*base, "id"), "constraint.id", "raw"),
                _atom_spec(
                    _pointer(*base, "kind"),
                    "constraint.kind",
                    "kind_prose" if prose else "raw",
                ),
                _atom_spec(
                    _pointer(*base, "on_pass_label_id"),
                    "constraint.on_pass_label",
                    "label_value_json",
                ),
                _atom_spec(
                    _pointer(*base, "on_fail_label_id"),
                    "constraint.on_fail_label",
                    "label_value_json",
                ),
            ]
        )
        for condition_index, _ in enumerate(constraint["conditions"]):
            condition_base = (*base, "conditions", condition_index)
            specs.extend(
                [
                    _atom_spec(
                        _pointer(*condition_base, "fact_id"),
                        "constraint.condition.fact_id",
                        "raw",
                    ),
                    _atom_spec(
                        _pointer(*condition_base, "operator"),
                        "constraint.condition.operator",
                        "operator_prose" if prose else "raw",
                    ),
                    _atom_spec(
                        _pointer(*condition_base, "value"),
                        "constraint.condition.value",
                        "json",
                    ),
                    _atom_spec(
                        _pointer(*condition_base, "failure_label_id"),
                        "constraint.condition.failure_label",
                        "label_value_json",
                    ),
                ]
            )
    specs.append(
        _atom_spec(
            _pointer("output", "keys", 1),
            "constraint.failure_output_key",
            "raw",
        )
    )
    for level in ("allowed", "approval_required", "prohibited"):
        level_pointer = _pointer("authority", level)
        specs.append(
            _atom_spec(
                level_pointer,
                "authority.level",
                "authority_level_prose" if prose else "pointer_key",
            )
        )
        for action_index, _ in enumerate(record["authority"][level]):
            specs.append(
                _atom_spec(
                    _pointer("authority", level, action_index),
                    "authority.action",
                    "raw" if prose else "json",
                )
            )
    for label_id in sorted(record["canonical_labels"]):
        label_pointer = _pointer("canonical_labels", label_id)
        specs.extend(
            [
                _atom_spec(label_pointer, "canonical_label.id", "pointer_key"),
                _atom_spec(label_pointer, "canonical_label.value", "json"),
            ]
        )
    for key_index, key in enumerate(record["output"]["keys"]):
        specs.extend(
            [
                _atom_spec(_pointer("output", "keys", key_index), "output.key", "json"),
                _atom_spec(
                    _pointer("output", "types", key), "output.type", "raw"
                ),
            ]
        )
    return specs


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _is_json_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, bool, int, float))


def _matches_output_type(value: Any, declared_type: str) -> bool:
    if declared_type == "string":
        return isinstance(value, str)
    if declared_type == "array[string]":
        return isinstance(value, list) and all(isinstance(item, str) for item in value)
    return False


def _derive_expected(record: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the narrow all-gate fixture without using its expected-answer oracle."""

    facts = {fact["id"]: fact["value"] for fact in record["facts"]}
    labels = record["canonical_labels"]
    constraints = record["constraints"]
    _require(len(constraints) == 1, "prototype evaluator requires exactly one all-gate")
    constraint = constraints[0]
    blocking: list[str] = []
    for condition in constraint["conditions"]:
        observed = facts[condition["fact_id"]]
        target = condition["value"]
        if condition["operator"] == "equals":
            passed = type(observed) is type(target) and observed == target
        else:
            _require(
                isinstance(observed, (int, float)) and not isinstance(observed, bool),
                "less_than requires a numeric observed fact",
            )
            passed = observed < target
        if not passed:
            blocking.append(labels[condition["failure_label_id"]])
    decision_label_id = (
        constraint["on_pass_label_id"] if not blocking else constraint["on_fail_label_id"]
    )
    return {"decision": labels[decision_label_id], "blocking": blocking}


def validate_record(record: dict[str, Any]) -> None:
    """Validate the narrow development schema before rendering anything."""

    _require(set(record) == ROOT_KEYS, "semantic record has missing or unexpected root keys")
    _require(
        record["schema_version"] == "benchmark-003-semantic-record/0.1-development",
        "unsupported semantic-record schema",
    )
    _require(record["split"] == "development", "prototype refuses non-development records")
    _require(
        record["status"] == "exploratory-development-only",
        "record must be explicitly labeled exploratory-development-only",
    )
    _require(isinstance(record["id"], str) and record["id"], "record id must be non-empty")
    _require(isinstance(record["task"], str) and record["task"], "task must be non-empty")

    entities = record["entities"]
    _require(isinstance(entities, list) and entities, "entities must be a non-empty list")
    entity_ids: set[str] = set()
    for entity in entities:
        _require(set(entity) == {"id", "label"}, "entity shape is invalid")
        _require(
            all(isinstance(entity[key], str) and entity[key] for key in ("id", "label")),
            "entity id and label must be non-empty strings",
        )
        _require(entity["id"] not in entity_ids, f"duplicate entity id: {entity['id']}")
        entity_ids.add(entity["id"])

    facts = record["facts"]
    _require(isinstance(facts, list) and facts, "facts must be a non-empty list")
    fact_ids: set[str] = set()
    for fact in facts:
        _require(
            set(fact) == {"id", "entity_id", "attribute", "value"},
            "fact shape is invalid",
        )
        _require(fact["id"] not in fact_ids, f"duplicate fact id: {fact['id']}")
        _require(fact["entity_id"] in entity_ids, f"unknown entity: {fact['entity_id']}")
        _require(
            isinstance(fact["attribute"], str) and fact["attribute"],
            "fact attribute must be non-empty",
        )
        _require(
            _is_json_scalar(fact["value"]),
            "prototype fact values must be JSON scalars",
        )
        canonical_json(fact["value"])
        fact_ids.add(fact["id"])

    labels = record["canonical_labels"]
    _require(
        isinstance(labels, dict) and labels,
        "canonical_labels must be a non-empty object",
    )
    _require(
        all(
            isinstance(key, str) and key and isinstance(value, str) and value
            for key, value in labels.items()
        ),
        "canonical label ids and values must be non-empty strings",
    )
    _require(
        len(labels.values()) == len(set(labels.values())),
        "canonical label values must be unique",
    )

    constraints = record["constraints"]
    _require(isinstance(constraints, list) and constraints, "constraints must be non-empty")
    constraint_ids: set[str] = set()
    for constraint in constraints:
        _require(
            set(constraint)
            == {"id", "kind", "conditions", "on_pass_label_id", "on_fail_label_id"},
            "constraint shape is invalid",
        )
        _require(
            isinstance(constraint["id"], str) and constraint["id"],
            "constraint id must be non-empty",
        )
        _require(constraint["id"] not in constraint_ids, "duplicate constraint id")
        _require(constraint["kind"] == "all", "prototype supports only all-gates")
        _require(
            constraint["on_pass_label_id"] in labels
            and constraint["on_fail_label_id"] in labels,
            "constraint outcome refers to an unknown canonical label",
        )
        _require(
            isinstance(constraint["conditions"], list) and constraint["conditions"],
            "constraint conditions must be non-empty",
        )
        for condition in constraint["conditions"]:
            _require(
                set(condition) == {"fact_id", "operator", "value", "failure_label_id"},
                "gate condition shape is invalid",
            )
            _require(condition["fact_id"] in fact_ids, "gate refers to an unknown fact")
            _require(
                condition["operator"] in {"equals", "less_than"},
                "unsupported gate operator",
            )
            _require(
                _is_json_scalar(condition["value"]),
                "prototype gate values must be JSON scalars",
            )
            if condition["operator"] == "less_than":
                _require(
                    isinstance(condition["value"], (int, float))
                    and not isinstance(condition["value"], bool),
                    "less_than requires a numeric gate value",
                )
            _require(
                condition["failure_label_id"] in labels,
                "gate refers to an unknown failure label",
            )
            canonical_json(condition["value"])
        constraint_ids.add(constraint["id"])

    authority = record["authority"]
    _require(
        set(authority) == {"allowed", "approval_required", "prohibited"},
        "authority shape is invalid",
    )
    for level, actions in authority.items():
        _require(isinstance(actions, list), f"authority.{level} must be a list")
        _require(
            len(actions) == len(set(actions))
            and all(isinstance(action, str) and action for action in actions),
            f"authority.{level} actions must be unique non-empty strings",
        )
    all_authority_actions = [action for actions in authority.values() for action in actions]
    _require(
        len(all_authority_actions) == len(set(all_authority_actions)),
        "authority levels must be mutually exclusive",
    )

    output = record["output"]
    _require(set(output) == {"keys", "types"}, "output shape is invalid")
    _require(
        isinstance(output["keys"], list)
        and output["keys"]
        and len(output["keys"]) == len(set(output["keys"])),
        "output keys must be a unique non-empty list",
    )
    _require(
        all(isinstance(key, str) and key for key in output["keys"]),
        "output keys must be non-empty strings",
    )
    _require(
        isinstance(output["types"], dict)
        and all(isinstance(value, str) and value for value in output["types"].values()),
        "output types must be non-empty strings",
    )
    _require(
        set(output["keys"]) == set(output["types"]),
        "output type map must exactly cover output keys",
    )
    _require(
        isinstance(record["expected"], dict)
        and set(record["expected"]) == set(output["keys"]),
        "expected answer keys must exactly match output keys",
    )
    _require(
        output["keys"] == ["decision", "blocking"]
        and output["types"] == {"decision": "string", "blocking": "array[string]"},
        "prototype output schema must be decision:string and blocking:array[string]",
    )
    for key in output["keys"]:
        _require(
            _matches_output_type(record["expected"][key], output["types"][key]),
            f"expected.{key} does not match its declared output type",
        )
    canonical_json(record["expected"])
    _require(
        record["expected"] == _derive_expected(record),
        "expected answer does not match deterministic all-gate evaluation",
    )


@dataclass(frozen=True)
class _RenderedAtom:
    text: str
    source_pointer: str
    source_role: str
    lexical_form: str


def _rendered_atom(
    text: str, source_pointer: str, source_role: str, lexical_form: str
) -> _RenderedAtom:
    return _RenderedAtom(text, source_pointer, source_role, lexical_form)


class _TraceBuilder:
    """Build prompt text while tracing the exact span of each source-bound atom."""

    def __init__(self, target: str, source_record: dict[str, Any]):
        self.target = target
        self.source_record = source_record
        self._parts: list[str] = []
        self.trace: list[dict[str, Any]] = []
        self._length = 0

    def line(self, *parts: str | _RenderedAtom) -> None:
        rendered_line: list[str] = []
        line_length = 0
        for part in parts:
            if isinstance(part, str):
                rendered_line.append(part)
                line_length += len(part)
                continue
            _require(isinstance(part, _RenderedAtom), "invalid rendered prompt part")
            start = self._length + line_length
            rendered_line.append(part.text)
            line_length += len(part.text)
            spec = _atom_spec(part.source_pointer, part.source_role, part.lexical_form)
            self.trace.append(
                {
                    "target": self.target,
                    "start": start,
                    "end": start + len(part.text),
                    "text_sha256": _sha256_text(part.text),
                    "category": _source_category(part.source_role),
                    **spec,
                    "source_atom_sha256": _source_atom_digest(
                        self.source_record, spec
                    ),
                }
            )
        text = "".join(rendered_line)
        self._parts.append(text + "\n")
        self._length += len(text) + 1

    def build(self) -> str:
        return "".join(self._parts).removesuffix("\n")


def _skeleton_profile(record: dict[str, Any]) -> str:
    authority_counts = tuple(
        len(record["authority"][level])
        for level in ("allowed", "approval_required", "prohibited")
    )
    if authority_counts == (1, 1, 1):
        return "base-one-action-per-level"
    if authority_counts == (0, 0, 0):
        return "empty-authority-levels"
    raise ValueError(
        "no independently frozen prompt skeleton for authority counts "
        f"{authority_counts}"
    )


def _skeleton_placeholder(trace: dict[str, Any]) -> str:
    identity = {
        "source_pointer": trace["source_pointer"],
        "source_role": trace["source_role"],
        "lexical_form": trace["lexical_form"],
    }
    return "{{SOURCE_ATOM:" + canonical_json(identity) + "}}"


def _user_prompt_skeleton(prompt: str, trace: list[dict[str, Any]]) -> str:
    """Replace exact atom spans with stable identities, preserving every glue byte."""

    parts: list[str] = []
    cursor = 0
    for item in trace:
        start, end = item["start"], item["end"]
        _require(
            isinstance(start, int)
            and isinstance(end, int)
            and 0 <= cursor <= start < end <= len(prompt),
            "cannot skeletonize invalid or overlapping atom spans",
        )
        parts.append(prompt[cursor:start])
        parts.append(_skeleton_placeholder(item))
        cursor = end
    parts.append(prompt[cursor:])
    return "".join(parts)


def _numeric_refs(value: Any, path: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    if isinstance(value, bool):
        return refs
    if isinstance(value, (int, float)):
        refs.append(("numeric_literals", path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            refs.extend(_numeric_refs(item, f"{path}.{index}"))
    elif isinstance(value, dict):
        for key in sorted(value):
            refs.extend(_numeric_refs(value[key], f"{path}.{key}"))
    return refs


def _operator_prose(operator: str) -> str:
    return {"equals": "equals", "less_than": "is less than"}[operator]


def _kind_prose(kind: str) -> str:
    return {"all": "every condition"}[kind]


def _render_prose(record: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    builder = _TraceBuilder("user", record)
    labels = record["canonical_labels"]

    builder.line(
        _rendered_atom(record["task"], _pointer("task"), "task.text", "raw")
    )
    builder.line()
    builder.line("Named entities:")
    for entity_index, entity in enumerate(record["entities"]):
        builder.line(
            "- ",
            _rendered_atom(
                entity["id"],
                _pointer("entities", entity_index, "id"),
                "entity.id",
                "raw",
            ),
            " names ",
            _rendered_atom(
                entity["label"],
                _pointer("entities", entity_index, "label"),
                "entity.label",
                "raw",
            ),
            ".",
        )
    builder.line()
    builder.line("Task facts:")
    for fact_index, fact in enumerate(record["facts"]):
        builder.line(
            "- Fact ",
            _rendered_atom(
                fact["id"],
                _pointer("facts", fact_index, "id"),
                "fact.id",
                "raw",
            ),
            " links to entity ",
            _rendered_atom(
                fact["entity_id"],
                _pointer("facts", fact_index, "entity_id"),
                "fact.entity_id",
                "raw",
            ),
            "; ",
            _rendered_atom(
                fact["attribute"],
                _pointer("facts", fact_index, "attribute"),
                "fact.attribute",
                "raw",
            ),
            " is ",
            _rendered_atom(
                _format_scalar(fact["value"]),
                _pointer("facts", fact_index, "value"),
                "fact.value",
                "json",
            ),
            ".",
        )
    builder.line()
    builder.line("Hard gates:")
    for constraint_index, constraint in enumerate(record["constraints"]):
        pass_label = labels[constraint["on_pass_label_id"]]
        fail_label = labels[constraint["on_fail_label_id"]]
        constraint_base = ("constraints", constraint_index)
        builder.line(
            "- Gate ",
            _rendered_atom(
                constraint["id"],
                _pointer(*constraint_base, "id"),
                "constraint.id",
                "raw",
            ),
            " requires ",
            _rendered_atom(
                _kind_prose(constraint["kind"]),
                _pointer(*constraint_base, "kind"),
                "constraint.kind",
                "kind_prose",
            ),
            " to pass; return ",
            _rendered_atom(
                _format_scalar(pass_label),
                _pointer(*constraint_base, "on_pass_label_id"),
                "constraint.on_pass_label",
                "label_value_json",
            ),
            " if it passes and ",
            _rendered_atom(
                _format_scalar(fail_label),
                _pointer(*constraint_base, "on_fail_label_id"),
                "constraint.on_fail_label",
                "label_value_json",
            ),
            " otherwise.",
        )
        for index, condition in enumerate(constraint["conditions"]):
            failure_label = labels[condition["failure_label_id"]]
            condition_base = (*constraint_base, "conditions", index)
            builder.line(
                "  - Fact ",
                _rendered_atom(
                    condition["fact_id"],
                    _pointer(*condition_base, "fact_id"),
                    "constraint.condition.fact_id",
                    "raw",
                ),
                " ",
                _rendered_atom(
                    _operator_prose(condition["operator"]),
                    _pointer(*condition_base, "operator"),
                    "constraint.condition.operator",
                    "operator_prose",
                ),
                " ",
                _rendered_atom(
                    _format_scalar(condition["value"]),
                    _pointer(*condition_base, "value"),
                    "constraint.condition.value",
                    "json",
                ),
                "; if it fails, append exactly ",
                _rendered_atom(
                    _format_scalar(failure_label),
                    _pointer(*condition_base, "failure_label_id"),
                    "constraint.condition.failure_label",
                    "label_value_json",
                ),
                " to blocking.",
            )
    builder.line()
    builder.line(
        "Failure-output rule: ",
        _rendered_atom(
            record["output"]["keys"][1],
            _pointer("output", "keys", 1),
            "constraint.failure_output_key",
            "raw",
        ),
        "=[] when every gate passes; otherwise append every failed label in gate order, "
        "then condition order.",
    )
    builder.line()
    builder.line("Authority boundaries:")
    for level in ("allowed", "approval_required", "prohibited"):
        builder.line(
            "- ",
            _rendered_atom(
                level.replace("_", " "),
                _pointer("authority", level),
                "authority.level",
                "authority_level_prose",
            ),
            ":",
        )
        if not record["authority"][level]:
            builder.line("  - (none).")
        for action_index, action in enumerate(record["authority"][level]):
            builder.line(
                "  - ",
                _rendered_atom(
                    action,
                    _pointer("authority", level, action_index),
                    "authority.action",
                    "raw",
                ),
                ".",
            )
    builder.line()
    builder.line("Canonical labels:")
    for label_id in sorted(labels):
        label_pointer = _pointer("canonical_labels", label_id)
        builder.line(
            "- ",
            _rendered_atom(
                label_id, label_pointer, "canonical_label.id", "pointer_key"
            ),
            " means exactly ",
            _rendered_atom(
                _format_scalar(labels[label_id]),
                label_pointer,
                "canonical_label.value",
                "json",
            ),
            ".",
        )
    builder.line()
    builder.line("Output contract:")
    for key_index, key in enumerate(record["output"]["keys"]):
        builder.line(
            "- ",
            _rendered_atom(
                _format_scalar(key),
                _pointer("output", "keys", key_index),
                "output.key",
                "json",
            ),
            " (",
            _rendered_atom(
                record["output"]["types"][key],
                _pointer("output", "types", key),
                "output.type",
                "raw",
            ),
            ").",
        )
    builder.line("Return one JSON object with exactly the listed keys in order.")
    return builder.build(), builder.trace


def _render_fields(record: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    builder = _TraceBuilder("user", record)
    labels = record["canonical_labels"]

    builder.line(
        "TASK: ",
        _rendered_atom(record["task"], _pointer("task"), "task.text", "raw"),
    )
    builder.line("ENTITIES:")
    for entity_index, entity in enumerate(record["entities"]):
        builder.line(
            "- ",
            _rendered_atom(
                entity["id"],
                _pointer("entities", entity_index, "id"),
                "entity.id",
                "raw",
            ),
            ": label=",
            _rendered_atom(
                _format_scalar(entity["label"]),
                _pointer("entities", entity_index, "label"),
                "entity.label",
                "json",
            ),
        )
    builder.line("FACTS:")
    for fact_index, fact in enumerate(record["facts"]):
        builder.line(
            "- ",
            _rendered_atom(
                fact["id"],
                _pointer("facts", fact_index, "id"),
                "fact.id",
                "raw",
            ),
            ": entity=",
            _rendered_atom(
                fact["entity_id"],
                _pointer("facts", fact_index, "entity_id"),
                "fact.entity_id",
                "raw",
            ),
            "; attribute=",
            _rendered_atom(
                fact["attribute"],
                _pointer("facts", fact_index, "attribute"),
                "fact.attribute",
                "raw",
            ),
            "; value=",
            _rendered_atom(
                _format_scalar(fact["value"]),
                _pointer("facts", fact_index, "value"),
                "fact.value",
                "json",
            ),
        )
    builder.line("HARD_GATES:")
    for constraint_index, constraint in enumerate(record["constraints"]):
        constraint_base = ("constraints", constraint_index)
        builder.line(
            "- ",
            _rendered_atom(
                constraint["id"],
                _pointer(*constraint_base, "id"),
                "constraint.id",
                "raw",
            ),
            ": kind=",
            _rendered_atom(
                constraint["kind"],
                _pointer(*constraint_base, "kind"),
                "constraint.kind",
                "raw",
            ),
            "; on_pass=",
            _rendered_atom(
                _format_scalar(labels[constraint["on_pass_label_id"]]),
                _pointer(*constraint_base, "on_pass_label_id"),
                "constraint.on_pass_label",
                "label_value_json",
            ),
            "; on_fail=",
            _rendered_atom(
                _format_scalar(labels[constraint["on_fail_label_id"]]),
                _pointer(*constraint_base, "on_fail_label_id"),
                "constraint.on_fail_label",
                "label_value_json",
            ),
        )
        for index, condition in enumerate(constraint["conditions"]):
            condition_base = (*constraint_base, "conditions", index)
            builder.line(
                "  - fact=",
                _rendered_atom(
                    condition["fact_id"],
                    _pointer(*condition_base, "fact_id"),
                    "constraint.condition.fact_id",
                    "raw",
                ),
                "; op=",
                _rendered_atom(
                    condition["operator"],
                    _pointer(*condition_base, "operator"),
                    "constraint.condition.operator",
                    "raw",
                ),
                "; value=",
                _rendered_atom(
                    _format_scalar(condition["value"]),
                    _pointer(*condition_base, "value"),
                    "constraint.condition.value",
                    "json",
                ),
                "; on_failure=",
                _rendered_atom(
                    _format_scalar(labels[condition["failure_label_id"]]),
                    _pointer(*condition_base, "failure_label_id"),
                    "constraint.condition.failure_label",
                    "label_value_json",
                ),
            )
    builder.line(
        "FAILURE_OUTPUT: ",
        _rendered_atom(
            record["output"]["keys"][1],
            _pointer("output", "keys", 1),
            "constraint.failure_output_key",
            "raw",
        ),
        "=[] when every gate passes; otherwise append every failed label in gate order, "
        "then condition order.",
    )
    builder.line("AUTHORITY:")
    for level in ("allowed", "approval_required", "prohibited"):
        builder.line(
            "- ",
            _rendered_atom(
                level,
                _pointer("authority", level),
                "authority.level",
                "pointer_key",
            ),
            ":",
        )
        if not record["authority"][level]:
            builder.line("  - (none)")
        for action_index, action in enumerate(record["authority"][level]):
            builder.line(
                "  - ",
                _rendered_atom(
                    _format_scalar(action),
                    _pointer("authority", level, action_index),
                    "authority.action",
                    "json",
                ),
            )
    builder.line("CANONICAL_LABELS:")
    for label_id in sorted(labels):
        label_pointer = _pointer("canonical_labels", label_id)
        builder.line(
            "- ",
            _rendered_atom(
                label_id, label_pointer, "canonical_label.id", "pointer_key"
            ),
            ": ",
            _rendered_atom(
                _format_scalar(labels[label_id]),
                label_pointer,
                "canonical_label.value",
                "json",
            ),
        )
    builder.line("OUTPUT:")
    for key_index, key in enumerate(record["output"]["keys"]):
        builder.line(
            "- key=",
            _rendered_atom(
                _format_scalar(key),
                _pointer("output", "keys", key_index),
                "output.key",
                "json",
            ),
            "; type=",
            _rendered_atom(
                record["output"]["types"][key],
                _pointer("output", "types", key),
                "output.type",
                "raw",
            ),
        )
    builder.line("Return only the JSON object described by OUTPUT.")
    return builder.build(), builder.trace


def _audit_surface(record: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(
        {
            "task": record["task"],
            "facts": record["facts"],
            "constraints": record["constraints"],
            "authority": record["authority"],
            "entities": record["entities"],
            "canonical_labels": record["canonical_labels"],
            "output": record["output"],
            "expected": record["expected"],
        }
    )


def seal_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with an integrity hash over every other artifact field."""

    sealed = copy.deepcopy(artifact)
    sealed.pop("artifact_sha256", None)
    sealed["artifact_sha256"] = _sha256_text(canonical_json(sealed))
    return sealed


def _render_condition_isolated(
    record: dict[str, Any], condition: str
) -> dict[str, Any]:
    """Render one already isolated record; callers must enforce source immutability."""

    _require(condition in CONDITIONS, f"unknown condition: {condition}")
    representation, has_contract = CONDITIONS[condition]
    if representation == "ordinary_prose":
        user_prompt, trace = _render_prose(record)
    else:
        user_prompt, trace = _render_fields(record)
    artifact = {
        "schema_version": "benchmark-003-render/0.1-development",
        "fixture_id": record["id"],
        "evidence_class": "exploratory-development-only",
        "condition": condition,
        "task_representation": representation,
        "interpretation_contract": has_contract,
        "system_prompt": INTERPRETATION_CONTRACT if has_contract else BASE_SYSTEM,
        "user_prompt": user_prompt,
        "trace": trace,
        "audit_surface": _audit_surface(record),
    }
    return seal_artifact(artifact)


def render_condition(record: dict[str, Any], condition: str) -> dict[str, Any]:
    """Safely render one condition without exposing caller-owned source to a renderer."""

    validate_record(record)
    caller_before = canonical_json(record)
    isolated_record = copy.deepcopy(record)
    isolated_before = canonical_json(isolated_record)
    artifact = _render_condition_isolated(isolated_record, condition)
    if canonical_json(isolated_record) != isolated_before:
        raise EquivalenceError(
            [f"{condition}: renderer mutated its isolated canonical source"]
        )
    if canonical_json(record) != caller_before:
        raise EquivalenceError(["renderer mutated the caller-owned canonical source"])
    return artifact


def render_all(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    validate_record(record)
    caller_before = canonical_json(record)
    source_snapshot = copy.deepcopy(record)
    snapshot_json = canonical_json(source_snapshot)
    artifacts: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        isolated_record = copy.deepcopy(source_snapshot)
        artifacts[condition] = render_condition(isolated_record, condition)
        if canonical_json(isolated_record) != snapshot_json:
            raise EquivalenceError(
                [f"{condition}: renderer mutated its isolated canonical source"]
            )
        if canonical_json(record) != caller_before:
            raise EquivalenceError(["renderer mutated the caller-owned canonical source"])
    return artifacts


def _projection(surface: dict[str, Any], category: str) -> Any:
    if category == "facts":
        return {
            "task": surface["task"],
            "facts": surface["facts"],
        }
    if category == "constraints":
        return surface["constraints"]
    if category == "authority":
        return surface["authority"]
    if category == "numeric_literals":
        values: dict[str, Any] = {}
        for fact_index, fact in enumerate(surface["facts"]):
            for _, path in _numeric_refs(fact["value"], f"facts.{fact_index}.value"):
                values[path] = fact["value"]
        for constraint in surface["constraints"]:
            for index, condition in enumerate(constraint["conditions"]):
                base = f"constraints.{constraint['id']}.conditions.{index}.value"
                for _, path in _numeric_refs(condition["value"], base):
                    values[path] = condition["value"]
        return values
    if category == "entities":
        return {entity["id"]: entity["label"] for entity in surface["entities"]}
    if category == "canonical_labels":
        return surface["canonical_labels"]
    if category == "output_keys":
        return surface["output"]
    raise KeyError(category)


def _primitive_leaves(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return [leaf for key in sorted(value) for leaf in _primitive_leaves(value[key])]
    if isinstance(value, list):
        return [leaf for item in value for leaf in _primitive_leaves(item)]
    return [value]


def _lexeme_count(text: str, value: Any) -> int:
    if isinstance(value, bool):
        token = "true" if value else "false"
    elif isinstance(value, (int, float)):
        if isinstance(value, float):
            _require(math.isfinite(value), "non-finite answer cue")
        token = canonical_json(value)
    elif isinstance(value, str):
        token = value
    elif value is None:
        token = "null"
    else:
        raise TypeError(f"unsupported expected scalar: {type(value).__name__}")
    if not token:
        return 0
    return len(re.findall(rf"(?<![\w]){re.escape(token)}(?![\w])", text))


def _answer_cue_counts(artifact: dict[str, Any]) -> dict[str, int]:
    text = artifact["system_prompt"] + "\n" + artifact["user_prompt"]
    surface = artifact["audit_surface"]
    cue_values = list(surface["canonical_labels"].values())
    cue_values.extend(_primitive_leaves(surface["expected"]))
    counts: dict[str, int] = {}
    for value in cue_values:
        typed_value = f"{type(value).__name__}:{canonical_json(value)}"
        counts[typed_value] = _lexeme_count(text, value)
    return counts


def _string_inventory(value: Any) -> set[str]:
    """Collect string leaves and object keys, including semantic IDs and attributes."""

    strings: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key:
                strings.add(key)
            strings.update(_string_inventory(child))
    elif isinstance(value, list):
        for child in value:
            strings.update(_string_inventory(child))
    elif isinstance(value, str) and value:
        strings.add(value)
    return strings


def _unexpected_system_lexemes(
    system_prompt: str,
    frozen_system_prompt: str,
    source_record: dict[str, Any],
) -> list[tuple[str, int, int]]:
    """Find source lexeme counts added beyond immutable generic-prompt collisions."""

    leaks: list[tuple[str, int, int]] = []
    sensitive_source = {
        key: source_record[key] for key in AUDIT_SURFACE_KEYS
    }
    for value in sorted(_string_inventory(sensitive_source)):
        observed = _lexeme_count(system_prompt, value)
        frozen_baseline = _lexeme_count(frozen_system_prompt, value)
        if observed > frozen_baseline:
            leaks.append((value, observed, frozen_baseline))
    return leaks


def validate_equivalence(
    artifacts: dict[str, dict[str, Any]], source_record: dict[str, Any]
) -> dict[str, Any]:
    """Bind artifacts to their source, then compare semantics and cue counts A-D."""

    issues: list[str] = []
    source_snapshot = copy.deepcopy(source_record)
    validate_record(source_snapshot)
    source_record = source_snapshot
    if set(artifacts) != set(CONDITIONS):
        raise EquivalenceError(["condition set must be exactly A, B, C, and D"])
    canonical_renders = render_all(source_record)

    if artifacts["A"].get("user_prompt") != artifacts["C"].get("user_prompt"):
        issues.append("factor isolation failed: A and C prose task prompts differ")
    if artifacts["B"].get("user_prompt") != artifacts["D"].get("user_prompt"):
        issues.append("factor isolation failed: B and D field task prompts differ")
    if artifacts["A"].get("system_prompt") != artifacts["B"].get("system_prompt"):
        issues.append("factor isolation failed: A and B no-contract system prompts differ")
    if artifacts["C"].get("system_prompt") != artifacts["D"].get("system_prompt"):
        issues.append("factor isolation failed: C and D contract system prompts differ")

    for condition in CONDITIONS:
        artifact = artifacts[condition]
        if canonical_json(artifact) != canonical_json(canonical_renders[condition]):
            issues.append(f"{condition}: artifact is not bound to the canonical source render")
        expected_representation, expected_contract = CONDITIONS[condition]
        if set(artifact) != ARTIFACT_KEYS:
            issues.append(f"{condition}: artifact has missing or unexpected fields")
        if artifact.get("schema_version") != "benchmark-003-render/0.1-development":
            issues.append(f"{condition}: artifact schema version differs")
        if artifact.get("evidence_class") != "exploratory-development-only":
            issues.append(f"{condition}: artifact evidence class differs")
        if artifact.get("fixture_id") != artifacts["A"].get("fixture_id"):
            issues.append(f"{condition}: fixture identity differs from A")
        if artifact.get("fixture_id") != source_record["id"]:
            issues.append(f"{condition}: fixture identity is not bound to source record")
        if artifact.get("condition") != condition:
            issues.append(f"{condition}: artifact condition tag differs")
        if artifact.get("task_representation") != expected_representation:
            issues.append(f"{condition}: task representation tag differs")
        if artifact.get("interpretation_contract") is not expected_contract:
            issues.append(f"{condition}: interpretation-contract tag differs")
        expected_system = FROZEN_SYSTEM_PROMPTS[expected_contract]
        if artifact.get("system_prompt") != expected_system:
            issues.append(f"{condition}: independently frozen system/contract prompt differs")
        if not isinstance(artifact.get("system_prompt"), str) or _sha256_text(
            artifact.get("system_prompt", "")
        ) != FROZEN_SYSTEM_PROMPT_SHA256[expected_contract]:
            issues.append(f"{condition}: frozen system/contract hash differs")
        supplied_hash = artifact.get("artifact_sha256")
        unsealed = copy.deepcopy(artifact)
        unsealed.pop("artifact_sha256", None)
        if supplied_hash != _sha256_text(canonical_json(unsealed)):
            issues.append(f"{condition}: artifact integrity hash differs")

        expected_specs = _expected_atom_specs(source_record, expected_representation)
        expected_identities = [
            (
                spec["source_pointer"],
                spec["source_role"],
                spec["lexical_form"],
            )
            for spec in expected_specs
        ]
        observed_identities: list[tuple[str, str, str]] = []
        trace_items = artifact.get("trace")
        if not isinstance(trace_items, list):
            issues.append(f"{condition}: source-bound trace must be a list")
            trace_items = []
        prior_end = -1
        for trace_index, trace in enumerate(trace_items):
            if not isinstance(trace, dict):
                issues.append(f"{condition}: trace {trace_index} is not an object")
                continue
            if set(trace) != TRACE_KEYS:
                issues.append(
                    f"{condition}: trace {trace_index} has missing or unexpected fields"
                )
            target = trace.get("target")
            if target != "user":
                issues.append(
                    f"{condition}: source-bound trace {trace_index} must target user prompt"
                )
                continue
            prompt = artifact.get("user_prompt")
            if not isinstance(prompt, str):
                issues.append(f"{condition}: user prompt is not text")
                continue
            start, end = trace.get("start"), trace.get("end")
            if (
                not isinstance(start, int)
                or isinstance(start, bool)
                or not isinstance(end, int)
                or isinstance(end, bool)
                or not (0 <= start < end <= len(prompt))
            ):
                issues.append(f"{condition}: source-bound trace {trace_index} span is invalid")
                continue
            if start < prior_end:
                issues.append(
                    f"{condition}: source-bound trace spans overlap or are out of order"
                )
            prior_end = end
            actual_text = prompt[start:end]
            if _sha256_text(actual_text) != trace.get("text_sha256"):
                issues.append(
                    f"{condition}: source-bound trace {trace_index} text hash differs"
                )

            source_pointer = trace.get("source_pointer")
            source_role = trace.get("source_role")
            lexical_form = trace.get("lexical_form")
            if not all(
                isinstance(value, str) and value
                for value in (source_pointer, source_role, lexical_form)
            ):
                issues.append(
                    f"{condition}: source-bound trace {trace_index} identity is invalid"
                )
                continue
            spec = _atom_spec(source_pointer, source_role, lexical_form)
            observed_identities.append((source_pointer, source_role, lexical_form))
            try:
                expected_category = _source_category(source_role)
                expected_text = _expected_atom_text(source_record, spec)
                expected_digest = _source_atom_digest(source_record, spec)
            except (KeyError, TypeError, ValueError) as error:
                issues.append(
                    f"{condition}: source-bound trace {trace_index} cannot resolve: {error}"
                )
                continue
            if trace.get("category") != expected_category:
                issues.append(
                    f"{condition}: source-bound trace {trace_index} category differs"
                )
            if trace.get("source_atom_sha256") != expected_digest:
                issues.append(
                    f"{condition}: source-bound atom digest differs for "
                    f"{source_role} at {source_pointer}"
                )
            if actual_text != expected_text:
                issues.append(
                    f"{condition}: source-bound atom text differs for "
                    f"{source_role} at {source_pointer} "
                    f"(expected={canonical_json(expected_text)}, "
                    f"observed={canonical_json(actual_text)})"
                )

        if observed_identities != expected_identities:
            mismatch_index = next(
                (
                    index
                    for index, pair in enumerate(
                        zip(observed_identities, expected_identities)
                    )
                    if pair[0] != pair[1]
                ),
                min(len(observed_identities), len(expected_identities)),
            )
            issues.append(
                f"{condition}: source-bound atom coverage/order differs at index "
                f"{mismatch_index} (observed={len(observed_identities)}, "
                f"expected={len(expected_identities)})"
            )

        try:
            profile = _skeleton_profile(source_record)
            skeleton = _user_prompt_skeleton(artifact["user_prompt"], trace_items)
            skeleton_hash = _sha256_text(skeleton)
            expected_skeleton_hash = FROZEN_USER_SKELETON_SHA256[
                (expected_representation, profile)
            ]
        except (KeyError, TypeError, ValueError) as error:
            issues.append(
                f"{condition}: static user-prompt skeleton cannot be checked: {error}"
            )
        else:
            if skeleton_hash != expected_skeleton_hash:
                issues.append(
                    f"{condition}: static user-prompt skeleton differs "
                    f"(profile={profile}, observed_sha256={skeleton_hash})"
                )

        surface = artifact.get("audit_surface")
        if not isinstance(surface, dict) or set(surface) != AUDIT_SURFACE_KEYS:
            issues.append(f"{condition}: audit surface has missing or unexpected fields")
            continue
        expected_source_surface = {
            key: source_record[key] for key in AUDIT_SURFACE_KEYS
        }
        if canonical_json(surface) != canonical_json(expected_source_surface):
            issues.append(
                f"{condition}: audit surface is not bound directly to source record"
            )
        leaked = _unexpected_system_lexemes(
            artifact["system_prompt"], expected_system, source_record
        )
        if leaked:
            issues.append(
                f"{condition}: added task-specific system/contract lexemes detected: "
                + ", ".join(
                    f"{canonical_json(value)}:{observed}>{baseline}"
                    for value, observed, baseline in leaked
                )
            )

    baseline = artifacts["A"]
    for category in (
        "facts",
        "numeric_literals",
        "entities",
        "constraints",
        "authority",
        "canonical_labels",
        "output_keys",
    ):
        expected = canonical_json(_projection(baseline["audit_surface"], category))
        for condition in ("B", "C", "D"):
            observed = canonical_json(_projection(artifacts[condition]["audit_surface"], category))
            if observed != expected:
                issues.append(f"{category} differ between A and {condition}")

    expected_cues = canonical_json(_answer_cue_counts(baseline))
    expected_answer = canonical_json(baseline["audit_surface"]["expected"])
    for condition in ("B", "C", "D"):
        observed_answer = canonical_json(artifacts[condition]["audit_surface"]["expected"])
        if observed_answer != expected_answer:
            issues.append(f"answer_cues/expected answer differ between A and {condition}")
        observed_cues = canonical_json(_answer_cue_counts(artifacts[condition]))
        if observed_cues != expected_cues:
            issues.append(f"answer_cues differ between A and {condition}")

    if issues:
        raise EquivalenceError(issues)

    return {
        "benchmark": "003",
        "status": "PASS",
        "evidence_class": "exploratory-development-only",
        "fixture_id": baseline["fixture_id"],
        "semantic_record_sha256": _sha256_text(canonical_json(source_record)),
        "conditions": list(CONDITIONS),
        "compared_categories": [
            "facts",
            "numeric_literals",
            "entities",
            "constraints",
            "authority",
            "canonical_labels",
            "output_keys",
            "answer_cues",
            "source_bound_atoms",
        ],
        "deterministic_renderer": True,
        "factor_isolation": True,
        "model_calls": 0,
        "spend_usd": 0,
        "answer_cue_counts": {
            condition: _answer_cue_counts(artifacts[condition]) for condition in CONDITIONS
        },
        "artifact_sha256": {
            condition: artifacts[condition]["artifact_sha256"] for condition in CONDITIONS
        },
        "source_bound_atom_counts": {
            condition: len(artifacts[condition]["trace"]) for condition in CONDITIONS
        },
        "user_prompt_skeleton_sha256": {
            condition: _sha256_text(
                _user_prompt_skeleton(
                    artifacts[condition]["user_prompt"], artifacts[condition]["trace"]
                )
            )
            for condition in CONDITIONS
        },
        "limitations": [
            "Development fixture only; no held-out evidence or outcome claim.",
            "The preflight binds controlled source atoms to exact rendered spans and checks "
            "static prompt glue, semantic surfaces, exact scalar cues, and task-specific "
            "system leakage; it "
            "cannot prove arbitrary paraphrase equivalence or detect every pragmatic cue.",
            "System lexeme checks compare source-derived counts to the independently frozen "
            "generic prompt baseline; the frozen exact hash remains authoritative when a "
            "source string collides with generic contract vocabulary.",
            "Static user-prompt skeletons cover only the frozen development-audited base and "
            "all-empty-authority profiles; other structures fail closed pending a new "
            "human-reviewed hash.",
            "Blinded human equivalence review remains required before corpus freezing or "
            "registration.",
        ],
    }


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_record(path: Path = FIXTURE) -> dict[str, Any]:
    record = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_json_keys,
    )
    validate_record(record)
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument(
        "--print-renders",
        action="store_true",
        help="include full development render artifacts in stdout JSON",
    )
    args = parser.parse_args()

    record = load_record(args.fixture)
    first = render_all(record)
    second = render_all(record)
    if canonical_json(first) != canonical_json(second):
        raise EquivalenceError(["repeated renders are not byte-identical"])
    report = validate_equivalence(first, record)
    if args.print_renders:
        report["development_renders"] = first
    print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True))


if __name__ == "__main__":
    main()
