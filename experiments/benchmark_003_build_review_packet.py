#!/usr/bin/env python3
"""Build and validate the two-stage Benchmark 003 human-review bundle.

This tool is development-method instrumentation. It makes no model or provider calls,
spends nothing, and cannot establish prompt equivalence or authorize fixture extension.
Phase 1 is condition-label-masked and oracle-withheld, not treatment-blind: the prompt
content and public source may make the experimental factors inferable.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import hmac
import json
import os
import secrets
import stat
import subprocess
from pathlib import Path
from typing import Any, Callable

import benchmark_003_equivalence_preflight as preflight


EXPERIMENTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENTS_DIR.parent
PROTOCOL = EXPERIMENTS_DIR / "BENCHMARK_003_HUMAN_REVIEW_PROTOCOL.md"
BOUND_PATHS = (
    EXPERIMENTS_DIR / "benchmark_003_development_fixture.json",
    EXPERIMENTS_DIR / "BENCHMARK_003_PREREGISTRATION_DRAFT.md",
    EXPERIMENTS_DIR / "benchmark_003_equivalence_preflight.py",
    EXPERIMENTS_DIR / "test_benchmark_003_equivalence_preflight.py",
    REPO_ROOT / "protocol" / "SPEAR_Protocol_Quick_Reference.md",
    REPO_ROOT / "protocol" / "SPEAR_LLM_PROMPT.md",
    PROTOCOL,
    Path(__file__).resolve(),
    EXPERIMENTS_DIR / "test_benchmark_003_build_review_packet.py",
)
VERDICTS = {"PASS", "REVISE", "UNCERTAIN"}
RESOLVED_ISSUE_STATUS = "resolved-and-reverified"
PHASE1_SCHEMA_VERSION = "benchmark-003-human-review-phase1/0.2-development"
REVEAL_SCHEMA_VERSION = "benchmark-003-human-review-reveal/0.2-development"
PHASE1_RESPONSE_SCHEMA_VERSION = "benchmark-003-human-review-response/0.2"
PHASE2_RESPONSE_SCHEMA_VERSION = "benchmark-003-human-review-phase2-response/0.2"
REVIEWER_FIELDS = (
    "name",
    "qualifications",
    "conflicts",
    "prior_exposure",
    "independence_statement",
    "public_attribution_consent",
)
CROSS_PROFILE_ITEMS = (
    "semantic_equivalence",
    "factor_isolation",
    "answer_cue_balance",
    "mutation_oracle_adequacy",
)
SEMANTIC_EXTRACTION_FIELDS = (
    "task",
    "facts",
    "hard_gates",
    "ordering",
    "authority",
    "canonical_labels",
    "output_contract",
    "answer_cues",
)
MUTATION_PROBES = (
    {
        "probe_id": "task-text-reserved-heading",
        "source_pointer": "/task",
        "mutation": "append newline + HARD_GATES heading + '- injected'",
        "review_question": (
            "Would this source value remain data in every profile, or could it become "
            "prompt structure or an instruction?"
        ),
    },
    {
        "probe_id": "entity-label-reserved-heading",
        "source_pointer": "/entities/0/label",
        "mutation": "append newline + HARD_GATES heading + '- injected'",
        "review_question": (
            "Would raw versus JSON-escaped rendering change the pragmatic instruction?"
        ),
    },
    {
        "probe_id": "fact-attribute-reserved-heading",
        "source_pointer": "/facts/0/attribute",
        "mutation": "append newline + HARD_GATES heading + '- injected'",
        "review_question": (
            "Would this source value remain a fact attribute in every profile?"
        ),
    },
    {
        "probe_id": "authority-action-reserved-heading",
        "source_pointer": "/authority/allowed/0",
        "mutation": "append newline + HARD_GATES heading + '- injected'",
        "review_question": (
            "Would raw versus JSON-escaped rendering alter the authority boundary?"
        ),
    },
)
KNOWN_ISSUE_IDS = (
    "common-system-baseline-replaced",
    "spear-construct-mismatch",
    "raw-string-structural-injection-false-pass",
    "schema-and-error-contract-gaps",
)
FORBIDDEN_PHASE1_KEYS = {
    "expected",
    "condition",
    "task_representation",
    "interpretation_contract",
    "trace",
    "audit_surface",
    "mapping",
    "nonce_hex",
    "known_issues",
    "preflight_result",
    "semantic_record_sha256",
    "source_context_sha256",
    "bound_source_files",
}

PHASE1_TOP_LEVEL_KEYS = {
    "schema_version",
    "status",
    "evidence_class",
    "masking",
    "fixture_scope",
    "bound_source_paths",
    "source_without_oracle",
    "source_without_oracle_sha256",
    "source_context_commitment",
    "reveal_core_commitment",
    "allocation_commitment",
    "profiles",
    "mutation_probes",
    "review_instructions",
    "response_schema",
    "model_calls",
    "provider_calls",
    "spend_usd",
    "phase1_packet_sha256",
}
PROFILE_KEYS = {
    "profile_id",
    "system_prompt",
    "system_prompt_sha256",
    "user_prompt",
    "user_prompt_sha256",
}
REVEAL_CORE_KEYS = {
    "schema_version",
    "status",
    "source_context",
    "source_context_commitment",
    "nonce_hex",
    "allocation_commitment",
    "mapping",
    "factor_metadata",
    "expected_oracle",
    "preflight_result",
    "known_issues",
    "phase2_response_requirements",
    "model_calls",
    "provider_calls",
    "spend_usd",
}
REVEAL_TOP_LEVEL_KEYS = REVEAL_CORE_KEYS | {
    "phase1_packet_sha256",
    "reveal_core_commitment",
    "reveal_sha256",
}


class ReviewBundleError(ValueError):
    """Raised when a packet, response, or reveal fails closed."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def _canonical_equal(left: Any, right: Any) -> bool:
    return canonical_bytes(left) == canonical_bytes(right)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _worktree_is_clean() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return not result.stdout.strip()


def _git_commit_exists(commit: str) -> bool:
    if not isinstance(commit, str) or len(commit) not in {40, 64}:
        return False
    try:
        bytes.fromhex(commit)
    except ValueError:
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def _git_file_sha256(commit: str, relative_path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return sha256_bytes(result.stdout)


def source_manifest(*, git_head_override: str | None = None) -> dict[str, Any]:
    missing = [str(path) for path in BOUND_PATHS if not path.is_file()]
    if missing:
        raise ReviewBundleError("missing bound source files: " + ", ".join(missing))
    return {
        "schema_version": "benchmark-003-review-source-manifest/0.1-development",
        "git_head_at_build": git_head_override or _git_head(),
        "files": {
            path.relative_to(REPO_ROOT).as_posix(): sha256_file(path)
            for path in BOUND_PATHS
        },
    }


def _validate_source_manifest(manifest: Any) -> None:
    _require_exact_keys(
        manifest,
        {"schema_version", "git_head_at_build", "files"},
        "source manifest",
    )
    if manifest["schema_version"] != "benchmark-003-review-source-manifest/0.1-development":
        raise ReviewBundleError("source manifest schema version differs")
    commit = manifest["git_head_at_build"]
    if not _git_commit_exists(commit):
        raise ReviewBundleError("source manifest git head is not a resolvable commit")
    expected_paths = {
        path.relative_to(REPO_ROOT).as_posix() for path in BOUND_PATHS
    }
    files = manifest["files"]
    if not isinstance(files, dict) or set(files) != expected_paths:
        raise ReviewBundleError("source manifest file set differs")
    for relative_path, supplied_hash in files.items():
        if not _is_sha256(supplied_hash):
            raise ReviewBundleError("source manifest contains an invalid file hash")
        try:
            committed_hash = _git_file_sha256(commit, relative_path)
        except subprocess.CalledProcessError as error:
            raise ReviewBundleError(
                f"bound source is absent from recorded commit: {relative_path}"
            ) from error
        if committed_hash != supplied_hash:
            raise ReviewBundleError(
                f"bound source bytes differ from recorded commit: {relative_path}"
            )
        working_tree_hash = sha256_file(REPO_ROOT / relative_path)
        if working_tree_hash != supplied_hash:
            raise ReviewBundleError(
                f"bound working-tree bytes differ from source manifest: {relative_path}"
            )


def _seal(document: dict[str, Any], digest_key: str) -> dict[str, Any]:
    sealed = copy.deepcopy(document)
    sealed.pop(digest_key, None)
    sealed[digest_key] = sha256_bytes(canonical_bytes(sealed))
    return sealed


def _verify_seal(document: dict[str, Any], digest_key: str) -> None:
    if not isinstance(document, dict):
        raise ReviewBundleError("sealed document must be an object")
    supplied = document.get(digest_key)
    unsealed = copy.deepcopy(document)
    unsealed.pop(digest_key, None)
    if supplied != sha256_bytes(canonical_bytes(unsealed)):
        raise ReviewBundleError(f"{digest_key} does not match document content")


def _parse_nonce(nonce_hex: str) -> bytes:
    try:
        nonce = bytes.fromhex(nonce_hex)
    except ValueError as error:
        raise ReviewBundleError("coordinator nonce must be hexadecimal") from error
    if len(nonce) < 32:
        raise ReviewBundleError("coordinator nonce must contain at least 32 bytes")
    if len(set(nonce)) < 16:
        raise ReviewBundleError(
            "coordinator nonce is obviously low-diversity; use generated random bytes"
        )
    return nonce


def _hiding_commitment(nonce: bytes, domain: str, value: Any) -> str:
    """Commit to potentially low-entropy data without exposing an offline oracle."""

    message = domain.encode("utf-8") + b"\0" + canonical_bytes(value)
    return hmac.new(nonce, message, hashlib.sha256).hexdigest()


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        bytes.fromhex(value)
    except ValueError:
        return False
    return True


def _allocation(
    nonce: bytes,
    source_context_commitment: str,
) -> tuple[list[str], dict[str, str]]:
    def token(purpose: str, condition: str) -> bytes:
        message = (
            f"{source_context_commitment}|{purpose}|{condition}"
        ).encode("utf-8")
        return hmac.new(nonce, message, hashlib.sha256).digest()

    ordered_conditions = sorted(preflight.CONDITIONS, key=lambda item: token("order", item))
    mapping: dict[str, str] = {}
    ordered_profiles: list[str] = []
    for condition in ordered_conditions:
        profile_id = "profile-" + token("label", condition).hex()[:12]
        if profile_id in mapping:
            raise ReviewBundleError("opaque profile collision")
        mapping[profile_id] = condition
        ordered_profiles.append(profile_id)
    return ordered_profiles, mapping


def _allocation_commitment(
    nonce: bytes,
    source_context_commitment: str,
    mapping: dict[str, str],
) -> str:
    payload = {
        "source_context_commitment": source_context_commitment,
        "mapping": mapping,
    }
    return _hiding_commitment(nonce, "benchmark-003-allocation-v2", payload)


def _phase1_response_schema(profile_ids: list[str]) -> dict[str, Any]:
    return {
        "schema_version": PHASE1_RESPONSE_SCHEMA_VERSION,
        "required_reviewer_fields": list(REVIEWER_FIELDS),
        "required_profile_ids": profile_ids,
        "required_cross_profile_items": list(CROSS_PROFILE_ITEMS),
        "required_semantic_extraction_fields": list(SEMANTIC_EXTRACTION_FIELDS),
        "required_mutation_probe_ids": [item["probe_id"] for item in MUTATION_PROBES],
        "judgment_shape": {
            "verdict": ["PASS", "REVISE", "UNCERTAIN"],
            "rationale": "non-empty string",
        },
        "disposition_rule": (
            "PASS only when every profile, per-profile mutation-probe, and "
            "cross-profile verdict is PASS; otherwise REVISE"
        ),
    }


def _phase1_review_instructions() -> list[str]:
    return [
        "Do not inspect the repository, prior reports, or coordinator reveal until the "
        "Phase 1 response is complete and its canonical SHA-256 is recorded.",
        "Judge only the supplied prompts and source-without-oracle. Record uncertainty "
        "rather than inferring a missing fact.",
        "Independently extract every required semantic field for each profile and record "
        "an observation for every supplied mutation probe.",
        "The task answer may be derivable from the supplied facts; only the stored "
        "expected-output object and prior automated verdict are withheld.",
        "This packet cannot authorize fixture extension, corpus freezing, registration, "
        "publication, or model calls.",
    ]


def _phase2_response_requirements() -> dict[str, Any]:
    return {
        "schema_version": PHASE2_RESPONSE_SCHEMA_VERSION,
        "required_fields": [
            "schema_version",
            "phase1_packet_sha256",
            "phase1_response_sha256",
            "reveal_sha256",
            "known_issue_dispositions",
            "overall_verdict",
            "rationale",
            "authorizes_fixture_extension",
        ],
        "required_known_issue_ids": list(KNOWN_ISSUE_IDS),
        "judgment_verdicts": ["PASS", "REVISE", "UNCERTAIN"],
        "authorizes_fixture_extension_must_equal": False,
        "disposition_rule": (
            "Any non-PASS or unresolved item yields REVISE; this development review "
            "never itself authorizes fixture extension"
        ),
    }


def _source_context(
    manifest: dict[str, Any],
    record: dict[str, Any],
    preflight_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_manifest": copy.deepcopy(manifest),
        "semantic_record_sha256": preflight_result["semantic_record_sha256"],
        "fixture_id": record["id"],
    }


def _reveal_core(
    nonce: bytes,
    source_context: dict[str, Any],
    source_context_commitment: str,
    allocation_commitment: str,
    mapping: dict[str, str],
    artifacts: dict[str, dict[str, Any]],
    record: dict[str, Any],
    preflight_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": REVEAL_SCHEMA_VERSION,
        "status": "coordinator-held-until-phase1-sealed",
        "source_context": copy.deepcopy(source_context),
        "source_context_commitment": source_context_commitment,
        "nonce_hex": nonce.hex(),
        "allocation_commitment": allocation_commitment,
        "mapping": copy.deepcopy(mapping),
        "factor_metadata": {
            profile_id: {
                "condition_label": condition,
                "task_representation": preflight.CONDITIONS[condition][0],
                "interpretation_contract": preflight.CONDITIONS[condition][1],
                "artifact_sha256": artifacts[condition]["artifact_sha256"],
            }
            for profile_id, condition in mapping.items()
        },
        "expected_oracle": copy.deepcopy(record["expected"]),
        "preflight_result": copy.deepcopy(preflight_result),
        "known_issues": _known_issue_dossiers(record),
        "phase2_response_requirements": _phase2_response_requirements(),
        "model_calls": 0,
        "provider_calls": 0,
        "spend_usd": 0.0,
    }


def build_bundle(
    nonce_hex: str,
    *,
    manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a public Phase 1 packet and coordinator-only reveal."""

    nonce = _parse_nonce(nonce_hex)
    record = preflight.load_record()
    artifacts = preflight.render_all(record)
    preflight_result = preflight.validate_equivalence(artifacts, record)
    manifest = copy.deepcopy(manifest if manifest is not None else source_manifest())
    _validate_source_manifest(manifest)
    context = _source_context(manifest, record, preflight_result)
    context_commitment = _hiding_commitment(
        nonce, "benchmark-003-source-context-v2", context
    )
    profile_ids, mapping = _allocation(nonce, context_commitment)
    allocation_commitment = _allocation_commitment(
        nonce, context_commitment, mapping
    )

    profiles: list[dict[str, Any]] = []
    for profile_id in profile_ids:
        artifact = artifacts[mapping[profile_id]]
        profiles.append(
            {
                "profile_id": profile_id,
                "system_prompt": artifact["system_prompt"],
                "system_prompt_sha256": sha256_text(artifact["system_prompt"]),
                "user_prompt": artifact["user_prompt"],
                "user_prompt_sha256": sha256_text(artifact["user_prompt"]),
            }
        )

    source_without_oracle = copy.deepcopy(record)
    source_without_oracle.pop("expected")
    reveal_core = _reveal_core(
        nonce,
        context,
        context_commitment,
        allocation_commitment,
        mapping,
        artifacts,
        record,
        preflight_result,
    )
    reveal_core_commitment = _hiding_commitment(
        nonce, "benchmark-003-reveal-core-v2", reveal_core
    )
    phase1 = _seal(
        {
            "schema_version": PHASE1_SCHEMA_VERSION,
            "status": "draft-not-reviewed",
            "evidence_class": "research-method-tooling-synthetic-development-only",
            "masking": "condition-label-masked-and-oracle-withheld-not-treatment-blind",
            "fixture_scope": "one existing public synthetic development fixture",
            "bound_source_paths": sorted(manifest["files"]),
            "source_without_oracle": source_without_oracle,
            "source_without_oracle_sha256": sha256_bytes(
                canonical_bytes(source_without_oracle)
            ),
            "source_context_commitment": context_commitment,
            "reveal_core_commitment": reveal_core_commitment,
            "allocation_commitment": allocation_commitment,
            "profiles": profiles,
            "mutation_probes": copy.deepcopy(list(MUTATION_PROBES)),
            "review_instructions": _phase1_review_instructions(),
            "response_schema": _phase1_response_schema(profile_ids),
            "model_calls": 0,
            "provider_calls": 0,
            "spend_usd": 0.0,
        },
        "phase1_packet_sha256",
    )

    reveal = _seal(
        {
            **reveal_core,
            "phase1_packet_sha256": phase1["phase1_packet_sha256"],
            "reveal_core_commitment": reveal_core_commitment,
        },
        "reveal_sha256",
    )
    verify_phase1(phase1, expected_manifest=manifest)
    verify_reveal(phase1, reveal, expected_manifest=manifest)
    return phase1, reveal


def _accepted_mutation(
    base_record: dict[str, Any],
    name: str,
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    record = copy.deepcopy(base_record)
    mutate(record)
    artifacts = preflight.render_all(record)
    result = preflight.validate_equivalence(artifacts, record)
    marker = "\nHARD_GATES:\n- injected"
    return {
        "name": name,
        "preflight_status": result["status"],
        "prose_contains_literal_marker": marker in artifacts["A"]["user_prompt"],
        "fields_contains_literal_marker": marker in artifacts["B"]["user_prompt"],
        "fields_contains_json_escaped_marker": "\\nHARD_GATES:\\n- injected"
        in artifacts["B"]["user_prompt"],
    }


def _exception_name(call: Callable[[], Any]) -> str:
    try:
        call()
    except Exception as error:  # The exception type is the audit result.
        return type(error).__name__
    return "NO_EXCEPTION"


def _known_issue_dossiers(record: dict[str, Any]) -> list[dict[str, Any]]:
    marker = "\nHARD_GATES:\n- injected"
    mutations = [
        _accepted_mutation(
            record,
            "task-text-reserved-heading",
            lambda candidate: candidate.__setitem__("task", candidate["task"] + marker),
        ),
        _accepted_mutation(
            record,
            "entity-label-reserved-heading",
            lambda candidate: candidate["entities"][0].__setitem__(
                "label", candidate["entities"][0]["label"] + marker
            ),
        ),
        _accepted_mutation(
            record,
            "fact-attribute-reserved-heading",
            lambda candidate: candidate["facts"][0].__setitem__(
                "attribute", candidate["facts"][0]["attribute"] + marker
            ),
        ),
        _accepted_mutation(
            record,
            "authority-action-reserved-heading",
            lambda candidate: candidate["authority"]["allowed"].__setitem__(
                0, candidate["authority"]["allowed"][0] + marker
            ),
        ),
    ]

    empty_fact_id = copy.deepcopy(record)
    old_id = empty_fact_id["facts"][0]["id"]
    empty_fact_id["facts"][0]["id"] = ""
    for constraint in empty_fact_id["constraints"]:
        for condition in constraint["conditions"]:
            if condition["fact_id"] == old_id:
                condition["fact_id"] = ""
    empty_fact_id_error = _exception_name(
        lambda: preflight.validate_record(empty_fact_id)
    )

    def malformed_artifact() -> None:
        artifacts = preflight.render_all(record)
        artifacts["A"] = []  # type: ignore[assignment]
        preflight.validate_equivalence(artifacts, record)

    def malformed_surface() -> None:
        artifacts = preflight.render_all(record)
        artifacts["A"]["audit_surface"] = []
        preflight.validate_equivalence(artifacts, record)

    return [
        {
            "issue_id": KNOWN_ISSUE_IDS[0],
            "status": "unresolved-requires-human-methodological-decision",
            "evidence": {
                "base_system": preflight.FROZEN_BASE_SYSTEM,
                "contract_system": preflight.FROZEN_INTERPRETATION_CONTRACT,
                "contract_contains_common_baseline": preflight.FROZEN_BASE_SYSTEM
                in preflight.FROZEN_INTERPRETATION_CONTRACT,
            },
            "required_disposition": (
                "Decide whether to make the contract additive over one common baseline and "
                "invalidate/re-audit affected frozen hashes."
            ),
        },
        {
            "issue_id": KNOWN_ISSUE_IDS[1],
            "status": "unresolved-requires-human-construct-validity-decision",
            "evidence": {
                "published_spear_sources": {
                    "protocol/SPEAR_Protocol_Quick_Reference.md": sha256_file(
                        REPO_ROOT / "protocol" / "SPEAR_Protocol_Quick_Reference.md"
                    ),
                    "protocol/SPEAR_LLM_PROMPT.md": sha256_file(
                        REPO_ROOT / "protocol" / "SPEAR_LLM_PROMPT.md"
                    ),
                },
                "published_core_headings": [
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
                ],
                "semantic_record_root_keys": sorted(record),
                "explicitly_unrepresented_core_headings": [
                    "ABSTRACTION",
                    "OBJECTIVE",
                    "UNCERTAINTY",
                    "EVALUATION & CHECK",
                    "INTERACTION / STOP",
                    "EXAMPLES",
                ],
                "implemented_representation_tags": sorted(
                    {value[0] for value in preflight.CONDITIONS.values()}
                ),
                "researcher_audit": (
                    "The ordinary-prose template remains highly fielded; the bespoke field "
                    "template and compact contract do not instantiate published SPEAR/0.2."
                ),
            },
            "required_disposition": (
                "Choose and justify rename-to-templates or redesign-to-SPEAR/0.2 before freeze."
            ),
        },
        {
            "issue_id": KNOWN_ISSUE_IDS[2],
            "status": "reproduced-negative-development-result",
            "evidence": mutations,
            "required_disposition": (
                "Treat the current PASS as fixture-specific; reject extension until raw-string "
                "grammar boundaries fail closed and are human reviewed."
            ),
        },
        {
            "issue_id": KNOWN_ISSUE_IDS[3],
            "status": "reproduced-negative-development-result",
            "evidence": {
                "empty_fact_id_validation_result": empty_fact_id_error,
                "non_object_artifact_exception": _exception_name(malformed_artifact),
                "non_object_audit_surface_exception": _exception_name(malformed_surface),
            },
            "required_disposition": (
                "Require non-empty typed identifiers and normalize malformed-input failures "
                "to the documented aggregate error interface before fixture extension."
            ),
        },
    ]


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def _require_exact_keys(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ReviewBundleError(f"{label} has missing or unexpected fields")


def _validate_source_without_oracle_shape(value: Any) -> None:
    root_keys = set(preflight.ROOT_KEYS) - {"expected"}
    _require_exact_keys(value, root_keys, "source_without_oracle")
    if not isinstance(value["entities"], list):
        raise ReviewBundleError("source_without_oracle.entities must be a list")
    for item in value["entities"]:
        _require_exact_keys(item, {"id", "label"}, "source entity")
    if not isinstance(value["facts"], list):
        raise ReviewBundleError("source_without_oracle.facts must be a list")
    for item in value["facts"]:
        _require_exact_keys(
            item, {"id", "entity_id", "attribute", "value"}, "source fact"
        )
    if not isinstance(value["constraints"], list):
        raise ReviewBundleError("source_without_oracle.constraints must be a list")
    for item in value["constraints"]:
        _require_exact_keys(
            item,
            {"id", "kind", "conditions", "on_pass_label_id", "on_fail_label_id"},
            "source constraint",
        )
        if not isinstance(item["conditions"], list):
            raise ReviewBundleError("source constraint conditions must be a list")
        for condition in item["conditions"]:
            _require_exact_keys(
                condition,
                {"fact_id", "operator", "value", "failure_label_id"},
                "source condition",
            )
    _require_exact_keys(
        value["authority"],
        {"allowed", "approval_required", "prohibited"},
        "source authority",
    )
    if not isinstance(value["canonical_labels"], dict):
        raise ReviewBundleError("source canonical_labels must be an object")
    _require_exact_keys(value["output"], {"keys", "types"}, "source output")
    output_keys = value["output"]["keys"]
    output_types = value["output"]["types"]
    if (
        not isinstance(output_keys, list)
        or not all(isinstance(item, str) for item in output_keys)
        or not isinstance(output_types, dict)
        or set(output_types) != set(output_keys)
    ):
        raise ReviewBundleError("source output keys and types differ")


def _current_semantic_evidence() -> tuple[
    dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]
]:
    record = preflight.load_record()
    artifacts = preflight.render_all(record)
    result = preflight.validate_equivalence(artifacts, record)
    return record, artifacts, result


def _require_zero_accounting(document: dict[str, Any], label: str) -> None:
    if type(document.get("model_calls")) is not int or document["model_calls"] != 0:
        raise ReviewBundleError(f"{label} model_calls must be integer zero")
    if type(document.get("provider_calls")) is not int or document["provider_calls"] != 0:
        raise ReviewBundleError(f"{label} provider_calls must be integer zero")
    if type(document.get("spend_usd")) is not float or document["spend_usd"] != 0.0:
        raise ReviewBundleError(f"{label} spend_usd must be floating-point zero")


def verify_phase1(
    phase1: dict[str, Any],
    *,
    expected_manifest: dict[str, Any] | None = None,
) -> None:
    _require_exact_keys(phase1, PHASE1_TOP_LEVEL_KEYS, "Phase 1 packet")
    _verify_seal(phase1, "phase1_packet_sha256")
    if phase1.get("schema_version") != PHASE1_SCHEMA_VERSION:
        raise ReviewBundleError("Phase 1 schema version differs")
    if phase1.get("status") != "draft-not-reviewed":
        raise ReviewBundleError("Phase 1 must remain draft-not-reviewed")
    fixed_fields = {
        "evidence_class": "research-method-tooling-synthetic-development-only",
        "masking": "condition-label-masked-and-oracle-withheld-not-treatment-blind",
        "fixture_scope": "one existing public synthetic development fixture",
        "review_instructions": _phase1_review_instructions(),
        "mutation_probes": list(MUTATION_PROBES),
    }
    for key, expected in fixed_fields.items():
        if not _canonical_equal(phase1.get(key), expected):
            raise ReviewBundleError(f"Phase 1 {key} differs from the fixed protocol")
    _require_zero_accounting(phase1, "Phase 1")
    leaked_keys = _walk_keys(phase1) & FORBIDDEN_PHASE1_KEYS
    if leaked_keys:
        raise ReviewBundleError(
            "Phase 1 contains forbidden structural keys: " + ", ".join(sorted(leaked_keys))
        )
    record, artifacts, preflight_result = _current_semantic_evidence()
    source_without_oracle = copy.deepcopy(record)
    source_without_oracle.pop("expected")
    _validate_source_without_oracle_shape(phase1.get("source_without_oracle"))
    if not _canonical_equal(phase1["source_without_oracle"], source_without_oracle):
        raise ReviewBundleError("Phase 1 source differs from the current canonical source")
    expected_source_hash = sha256_bytes(canonical_bytes(source_without_oracle))
    supplied_source_hash = sha256_bytes(
        canonical_bytes(phase1["source_without_oracle"])
    )
    if (
        phase1.get("source_without_oracle_sha256") != supplied_source_hash
        or supplied_source_hash != expected_source_hash
    ):
        raise ReviewBundleError("Phase 1 redacted source hash differs")
    expected_paths = sorted(
        path.relative_to(REPO_ROOT).as_posix() for path in BOUND_PATHS
    )
    if phase1.get("bound_source_paths") != expected_paths:
        raise ReviewBundleError("Phase 1 bound source path list differs")
    for key in (
        "source_context_commitment",
        "reveal_core_commitment",
        "allocation_commitment",
        "phase1_packet_sha256",
    ):
        if not _is_sha256(phase1.get(key)):
            raise ReviewBundleError(f"Phase 1 {key} is not a SHA-256 value")

    profiles = phase1.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != 4:
        raise ReviewBundleError("Phase 1 must contain exactly four opaque profiles")
    profile_ids: set[str] = set()
    observed_prompts: set[tuple[str, str]] = set()
    for profile in profiles:
        _require_exact_keys(profile, PROFILE_KEYS, "Phase 1 profile")
        profile_id = profile.get("profile_id")
        if not isinstance(profile_id, str) or not profile_id.startswith("profile-"):
            raise ReviewBundleError("Phase 1 profile id is invalid")
        if profile_id in profile_ids:
            raise ReviewBundleError("Phase 1 profile ids must be unique")
        profile_ids.add(profile_id)
        for field in ("system_prompt", "user_prompt"):
            prompt = profile.get(field)
            if not isinstance(prompt, str) or not prompt:
                raise ReviewBundleError(f"Phase 1 {field} must be non-empty text")
            if profile.get(field + "_sha256") != sha256_text(prompt):
                raise ReviewBundleError(f"Phase 1 {field} hash differs")
        observed_prompts.add((profile["system_prompt"], profile["user_prompt"]))
    expected_prompts = {
        (artifact["system_prompt"], artifact["user_prompt"])
        for artifact in artifacts.values()
    }
    if observed_prompts != expected_prompts:
        raise ReviewBundleError("Phase 1 profiles differ from the current rendered prompts")
    ordered_profile_ids = [item["profile_id"] for item in profiles]
    if not _canonical_equal(
        phase1.get("response_schema"), _phase1_response_schema(ordered_profile_ids)
    ):
        raise ReviewBundleError("Phase 1 response schema differs from fixed requirements")

    # The public phase must not expose a reusable digest over oracle-bearing source.
    manifest_for_check = expected_manifest or source_manifest()
    full_context = _source_context(manifest_for_check, record, preflight_result)
    forbidden_raw_digests = {
        preflight_result["semantic_record_sha256"],
        manifest_for_check["files"][
            "experiments/benchmark_003_development_fixture.json"
        ],
        sha256_bytes(canonical_bytes(full_context)),
    }
    serialized = canonical_json(phase1)
    if any(digest in serialized for digest in forbidden_raw_digests):
        raise ReviewBundleError("Phase 1 exposes an oracle-bearing raw digest")


def verify_reveal(
    phase1: dict[str, Any],
    reveal: dict[str, Any],
    *,
    expected_manifest: dict[str, Any] | None = None,
) -> None:
    verify_phase1(phase1, expected_manifest=expected_manifest)
    _require_exact_keys(reveal, REVEAL_TOP_LEVEL_KEYS, "coordinator reveal")
    _verify_seal(reveal, "reveal_sha256")
    _require_zero_accounting(reveal, "reveal")
    if reveal.get("schema_version") != REVEAL_SCHEMA_VERSION:
        raise ReviewBundleError("reveal schema version differs")
    if reveal.get("phase1_packet_sha256") != phase1.get("phase1_packet_sha256"):
        raise ReviewBundleError("reveal is not bound to the Phase 1 packet")
    nonce = _parse_nonce(reveal.get("nonce_hex", ""))
    mapping = reveal.get("mapping")
    if not isinstance(mapping, dict) or set(mapping.values()) != set(preflight.CONDITIONS):
        raise ReviewBundleError("reveal mapping must open exactly A, B, C, and D")
    profile_ids = {item["profile_id"] for item in phase1["profiles"]}
    if set(mapping) != profile_ids:
        raise ReviewBundleError("reveal mapping does not cover Phase 1 profiles")

    record, artifacts, preflight_result = _current_semantic_evidence()
    actual_manifest = reveal.get("source_context", {}).get("source_manifest")
    _validate_source_manifest(actual_manifest)
    manifest = copy.deepcopy(
        expected_manifest
        if expected_manifest is not None
        else source_manifest(git_head_override=actual_manifest["git_head_at_build"])
    )
    _validate_source_manifest(manifest)
    if not _canonical_equal(actual_manifest, manifest):
        raise ReviewBundleError("reveal source manifest differs from bound source bytes")
    expected_context = _source_context(manifest, record, preflight_result)
    if not _canonical_equal(reveal.get("source_context"), expected_context):
        raise ReviewBundleError("reveal source context differs from current evidence")
    context_commitment = _hiding_commitment(
        nonce, "benchmark-003-source-context-v2", expected_context
    )
    if (
        reveal.get("source_context_commitment") != context_commitment
        or phase1.get("source_context_commitment") != context_commitment
    ):
        raise ReviewBundleError("reveal does not open the source context commitment")

    expected_profile_ids, expected_mapping = _allocation(nonce, context_commitment)
    if mapping != expected_mapping:
        raise ReviewBundleError("reveal mapping differs from deterministic allocation")
    if [item["profile_id"] for item in phase1["profiles"]] != expected_profile_ids:
        raise ReviewBundleError("Phase 1 profile order differs from deterministic allocation")
    profiles_by_id = {item["profile_id"]: item for item in phase1["profiles"]}
    for profile_id, condition in expected_mapping.items():
        profile = profiles_by_id[profile_id]
        artifact = artifacts[condition]
        if (
            profile["system_prompt"] != artifact["system_prompt"]
            or profile["user_prompt"] != artifact["user_prompt"]
        ):
            raise ReviewBundleError(
                "Phase 1 prompt payload differs from its revealed condition mapping"
            )
    expected_commitment = _allocation_commitment(
        nonce, context_commitment, expected_mapping
    )
    if (
        expected_commitment != phase1.get("allocation_commitment")
        or reveal.get("allocation_commitment") != expected_commitment
    ):
        raise ReviewBundleError("reveal does not open the allocation commitment")

    expected_core = _reveal_core(
        nonce,
        expected_context,
        context_commitment,
        expected_commitment,
        expected_mapping,
        artifacts,
        record,
        preflight_result,
    )
    actual_core = {key: copy.deepcopy(reveal[key]) for key in REVEAL_CORE_KEYS}
    if not _canonical_equal(actual_core, expected_core):
        raise ReviewBundleError("reveal core differs from independently recomputed evidence")
    reveal_core_commitment = _hiding_commitment(
        nonce, "benchmark-003-reveal-core-v2", expected_core
    )
    if (
        reveal.get("reveal_core_commitment") != reveal_core_commitment
        or phase1.get("reveal_core_commitment") != reveal_core_commitment
    ):
        raise ReviewBundleError("reveal does not open the reveal-core commitment")


def _validate_judgment(value: Any, label: str) -> str:
    if not isinstance(value, dict) or set(value) != {"verdict", "rationale"}:
        raise ReviewBundleError(f"{label} judgment shape is invalid")
    verdict = value["verdict"]
    rationale = value["rationale"]
    if verdict not in VERDICTS:
        raise ReviewBundleError(f"{label} verdict is invalid")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ReviewBundleError(f"{label} rationale must be non-empty")
    return verdict


def validate_phase1_response(
    phase1: dict[str, Any], response: dict[str, Any]
) -> dict[str, str]:
    verify_phase1(phase1)
    required = {
        "schema_version",
        "phase1_packet_sha256",
        "reviewer",
        "profile_judgments",
        "cross_profile_judgments",
    }
    if not isinstance(response, dict) or set(response) != required:
        raise ReviewBundleError("Phase 1 response has missing or unexpected fields")
    if response["schema_version"] != PHASE1_RESPONSE_SCHEMA_VERSION:
        raise ReviewBundleError("Phase 1 response schema version differs")
    if response["phase1_packet_sha256"] != phase1["phase1_packet_sha256"]:
        raise ReviewBundleError("Phase 1 response is bound to the wrong packet")
    reviewer = response["reviewer"]
    reviewer_fields = set(REVIEWER_FIELDS)
    if not isinstance(reviewer, dict) or set(reviewer) != reviewer_fields:
        raise ReviewBundleError("reviewer disclosure fields are incomplete")
    for field in reviewer_fields - {"public_attribution_consent"}:
        if not isinstance(reviewer[field], str) or not reviewer[field].strip():
            raise ReviewBundleError(f"reviewer.{field} must be non-empty text")
    if not isinstance(reviewer["public_attribution_consent"], bool):
        raise ReviewBundleError("public attribution consent must be boolean")

    required_profiles = {item["profile_id"] for item in phase1["profiles"]}
    profile_judgments = response["profile_judgments"]
    if not isinstance(profile_judgments, dict) or set(profile_judgments) != required_profiles:
        raise ReviewBundleError("profile judgments do not cover every opaque profile")
    verdicts: list[str] = []
    mutation_probe_ids = {item["probe_id"] for item in MUTATION_PROBES}
    for profile_id, value in profile_judgments.items():
        _require_exact_keys(
            value,
            {"verdict", "rationale", "semantic_extraction", "mutation_probe_judgments"},
            f"profile {profile_id} judgment",
        )
        verdicts.append(
            _validate_judgment(
                {"verdict": value["verdict"], "rationale": value["rationale"]},
                f"profile {profile_id}",
            )
        )
        extraction = value["semantic_extraction"]
        _require_exact_keys(
            extraction,
            set(SEMANTIC_EXTRACTION_FIELDS),
            f"profile {profile_id} semantic extraction",
        )
        for field in SEMANTIC_EXTRACTION_FIELDS:
            if not isinstance(extraction[field], str) or not extraction[field].strip():
                raise ReviewBundleError(
                    f"profile {profile_id} semantic_extraction.{field} must be non-empty"
                )
        mutation_judgments = value["mutation_probe_judgments"]
        if (
            not isinstance(mutation_judgments, dict)
            or set(mutation_judgments) != mutation_probe_ids
        ):
            raise ReviewBundleError(
                f"profile {profile_id} mutation judgments are incomplete"
            )
        verdicts.extend(
            _validate_judgment(item, f"profile {profile_id} mutation {probe_id}")
            for probe_id, item in mutation_judgments.items()
        )

    required_cross = set(CROSS_PROFILE_ITEMS)
    cross_judgments = response["cross_profile_judgments"]
    if not isinstance(cross_judgments, dict) or set(cross_judgments) != required_cross:
        raise ReviewBundleError("cross-profile judgments are incomplete")
    verdicts.extend(
        _validate_judgment(value, f"cross-profile {key}")
        for key, value in cross_judgments.items()
    )
    disposition = "PASS" if all(verdict == "PASS" for verdict in verdicts) else "REVISE"
    return {
        "disposition": disposition,
        "phase1_response_sha256": sha256_bytes(canonical_bytes(response)),
    }


def validate_phase2_response(
    phase1: dict[str, Any],
    reveal: dict[str, Any],
    phase1_response: dict[str, Any],
    phase2_response: dict[str, Any],
) -> dict[str, str]:
    verify_reveal(phase1, reveal)
    phase1_result = validate_phase1_response(phase1, phase1_response)
    required = set(_phase2_response_requirements()["required_fields"])
    if not isinstance(phase2_response, dict) or set(phase2_response) != required:
        raise ReviewBundleError("Phase 2 response has missing or unexpected fields")
    if phase2_response["schema_version"] != PHASE2_RESPONSE_SCHEMA_VERSION:
        raise ReviewBundleError("Phase 2 response schema version differs")
    if phase2_response["phase1_packet_sha256"] != phase1["phase1_packet_sha256"]:
        raise ReviewBundleError("Phase 2 response is bound to the wrong Phase 1 packet")
    if phase2_response["phase1_response_sha256"] != phase1_result[
        "phase1_response_sha256"
    ]:
        raise ReviewBundleError("Phase 2 response is bound to the wrong Phase 1 response")
    if phase2_response["reveal_sha256"] != reveal["reveal_sha256"]:
        raise ReviewBundleError("Phase 2 response is bound to the wrong reveal")
    if phase2_response["authorizes_fixture_extension"] is not False:
        raise ReviewBundleError("this review may not authorize fixture extension")
    if phase2_response["overall_verdict"] not in VERDICTS:
        raise ReviewBundleError("Phase 2 overall verdict is invalid")
    if not isinstance(phase2_response["rationale"], str) or not phase2_response[
        "rationale"
    ].strip():
        raise ReviewBundleError("Phase 2 rationale must be non-empty")
    dispositions = phase2_response["known_issue_dispositions"]
    if not isinstance(dispositions, dict) or set(dispositions) != set(KNOWN_ISSUE_IDS):
        raise ReviewBundleError("Phase 2 must disposition every known issue")
    issue_verdicts = [
        _validate_judgment(value, f"known issue {key}")
        for key, value in dispositions.items()
    ]
    reveal_issues_resolved = all(
        item.get("status") == RESOLVED_ISSUE_STATUS
        for item in reveal["known_issues"]
    )
    all_pass = (
        phase1_result["disposition"] == "PASS"
        and phase2_response["overall_verdict"] == "PASS"
        and all(verdict == "PASS" for verdict in issue_verdicts)
        and reveal_issues_resolved
    )
    return {"disposition": "PASS" if all_pass else "REVISE"}


def _resolved_target(path: Path) -> Path:
    if not path.name or path.name in {".", ".."}:
        raise ReviewBundleError("output path must name a file")
    try:
        parent = path.parent.resolve(strict=True)
    except FileNotFoundError as error:
        raise ReviewBundleError("output parent directory must already exist") from error
    if not parent.is_dir():
        raise ReviewBundleError("output parent must be a directory")
    return parent / path.name


def _require_private_parent(path: Path) -> None:
    parent_stat = path.parent.stat()
    if parent_stat.st_uid != os.getuid():
        raise ReviewBundleError("private output directory must be owned by the current user")
    if stat.S_IMODE(parent_stat.st_mode) & 0o077:
        raise ReviewBundleError(
            "private output directory must deny all group and other permissions"
        )


def _write_bytes_exclusive(
    path: Path,
    data: bytes,
    *,
    mode: int,
    private_parent: bool,
) -> Path:
    target = _resolved_target(path)
    if private_parent:
        _require_private_parent(target)
    if target.exists() or target.is_symlink():
        raise ReviewBundleError(f"refusing to overwrite existing file: {target}")
    temporary = target.parent / f".{target.name}.tmp-{secrets.token_hex(16)}"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    file_descriptor: int | None = None
    try:
        file_descriptor = os.open(temporary, flags, mode)
        os.fchmod(file_descriptor, mode)
        offset = 0
        while offset < len(data):
            offset += os.write(file_descriptor, data[offset:])
        os.fsync(file_descriptor)
        os.close(file_descriptor)
        file_descriptor = None
        try:
            os.link(temporary, target, follow_symlinks=False)
        except FileExistsError as error:
            raise ReviewBundleError(f"refusing to overwrite existing file: {target}") from error
        directory_fd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        temporary.unlink(missing_ok=True)
    return target


def _write_json_exclusive(
    path: Path, value: Any, *, mode: int, private_parent: bool
) -> Path:
    data = (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    return _write_bytes_exclusive(
        path, data, mode=mode, private_parent=private_parent
    )


def _ensure_outside_public(path: Path, label: str) -> Path:
    target = _resolved_target(path)
    if target == REPO_ROOT or REPO_ROOT in target.parents:
        raise ReviewBundleError(f"{label} must be outside the public repository")
    return target


def _read_nonce_file(path: Path) -> str:
    target = _ensure_outside_public(path, "coordinator nonce file")
    _require_private_parent(target)
    if path.is_symlink() or not target.is_file():
        raise ReviewBundleError("coordinator nonce file must be a regular non-symlink file")
    file_stat = target.stat()
    if file_stat.st_uid != os.getuid() or stat.S_IMODE(file_stat.st_mode) & 0o077:
        raise ReviewBundleError(
            "coordinator nonce file must be user-owned and deny group/other permissions"
        )
    try:
        nonce_hex = target.read_text(encoding="ascii").strip()
    except (OSError, UnicodeError) as error:
        raise ReviewBundleError("coordinator nonce file is not readable ASCII") from error
    _parse_nonce(nonce_hex)
    return nonce_hex


def _generate_nonce_file(path: Path) -> str:
    target = _ensure_outside_public(path, "generated coordinator nonce file")
    nonce_hex = secrets.token_hex(32)
    _write_bytes_exclusive(
        target,
        (nonce_hex + "\n").encode("ascii"),
        mode=0o600,
        private_parent=True,
    )
    return nonce_hex


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    nonce_group = parser.add_mutually_exclusive_group(required=True)
    nonce_group.add_argument(
        "--nonce-file",
        type=Path,
        help="user-owned 0600 file containing a secret random 32+ byte hex nonce",
    )
    nonce_group.add_argument(
        "--generate-nonce-file",
        type=Path,
        help="atomically create a new 0600 nonce file with 32 random bytes",
    )
    parser.add_argument("--phase1-out", required=True, type=Path)
    parser.add_argument("--reveal-out", required=True, type=Path)
    args = parser.parse_args()
    if not _worktree_is_clean():
        raise ReviewBundleError("refusing live packet build from a dirty worktree")
    reveal_path = _ensure_outside_public(
        args.reveal_out, "coordinator reveal"
    )
    _require_private_parent(reveal_path)
    phase1_path = _resolved_target(args.phase1_out)
    for destination in (phase1_path, reveal_path):
        if destination.exists() or destination.is_symlink():
            raise ReviewBundleError(
                f"refusing to overwrite existing file: {destination}"
            )
    nonce_hex = (
        _generate_nonce_file(args.generate_nonce_file)
        if args.generate_nonce_file is not None
        else _read_nonce_file(args.nonce_file)
    )
    phase1, reveal = build_bundle(nonce_hex)
    _write_json_exclusive(reveal_path, reveal, mode=0o600, private_parent=True)
    _write_json_exclusive(phase1_path, phase1, mode=0o644, private_parent=False)
    print(
        json.dumps(
            {
                "status": "READY_FOR_HUMAN_REVIEW_NOT_REVIEWED",
                "phase1_packet_sha256": phase1["phase1_packet_sha256"],
                "reveal_sha256": reveal["reveal_sha256"],
                "model_calls": 0,
                "provider_calls": 0,
                "spend_usd": 0.0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
