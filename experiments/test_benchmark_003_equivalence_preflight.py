#!/usr/bin/env python3
"""Mutation tests for the Benchmark 003 development equivalence preflight."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).parent))
import benchmark_003_equivalence_preflight as preflight  # noqa: E402


class Benchmark003EquivalencePreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = preflight.load_record()

    def render_with_a_mutation(self, mutate) -> dict:
        mutated = copy.deepcopy(self.record)
        mutate(mutated)
        artifacts = preflight.render_all(self.record)
        artifacts["A"] = preflight.render_condition(mutated, "A")
        return artifacts

    def assert_fails_closed(self, artifacts: dict, category: str) -> None:
        with self.assertRaises(preflight.EquivalenceError) as caught:
            preflight.validate_equivalence(artifacts, self.record)
        self.assertIn(category, str(caught.exception))

    def assert_buggy_renderer_atoms_fail_closed(
        self,
        replacements: dict[tuple[str, str], str],
        renderer_name: str = "_render_fields",
    ) -> None:
        """Corrupt exact traced spans while keeping trace and artifact hashes fresh."""

        original_renderer = getattr(preflight, renderer_name)
        matched: set[tuple[str, str]] = set()

        def buggy_renderer(record: dict) -> tuple[str, list[dict]]:
            prompt, trace = original_renderer(record)
            rewritten_trace = copy.deepcopy(trace)
            parts: list[str] = []
            cursor = 0
            output_length = 0
            for item in rewritten_trace:
                old_start, old_end = item["start"], item["end"]
                prefix = prompt[cursor:old_start]
                parts.append(prefix)
                output_length += len(prefix)
                key = (item["source_pointer"], item["source_role"])
                old_text = prompt[old_start:old_end]
                new_text = replacements.get(key, old_text)
                if key in replacements:
                    matched.add(key)
                item["start"] = output_length
                item["end"] = output_length + len(new_text)
                item["text_sha256"] = preflight._sha256_text(new_text)
                parts.append(new_text)
                output_length += len(new_text)
                cursor = old_end
            parts.append(prompt[cursor:])
            return "".join(parts), rewritten_trace

        with mock.patch.object(preflight, renderer_name, buggy_renderer):
            artifacts = preflight.render_all(self.record)
            with self.assertRaises(preflight.EquivalenceError) as caught:
                preflight.validate_equivalence(artifacts, self.record)
            message = str(caught.exception)
            self.assertIn("source-bound atom text differs", message)
            self.assertNotIn("artifact integrity hash differs", message)
            self.assertNotIn("text hash differs", message)
            self.assertNotIn("canonical source render", message)
        self.assertEqual(matched, set(replacements))

    def assert_buggy_renderer_glue_fails_closed(
        self,
        renderer_name: str,
        mutate_glue,
    ) -> None:
        """Change only untraced glue while refreshing offsets and artifact hashes."""

        original_renderer = getattr(preflight, renderer_name)

        def buggy_renderer(record: dict) -> tuple[str, list[dict]]:
            prompt, trace = original_renderer(record)
            return mutate_glue(prompt, copy.deepcopy(trace))

        with mock.patch.object(preflight, renderer_name, buggy_renderer):
            artifacts = preflight.render_all(self.record)
            with self.assertRaises(preflight.EquivalenceError) as caught:
                preflight.validate_equivalence(artifacts, self.record)
        message = str(caught.exception)
        self.assertIn("static user-prompt skeleton differs", message)
        self.assertNotIn("source-bound atom text differs", message)
        self.assertNotIn("text hash differs", message)
        self.assertNotIn("artifact integrity hash differs", message)
        self.assertNotIn("canonical source render", message)

    def replace_untraced_range(
        self,
        prompt: str,
        trace: list[dict],
        start: int,
        end: int,
        replacement: str,
    ) -> tuple[str, list[dict]]:
        for item in trace:
            self.assertTrue(item["end"] <= start or item["start"] >= end)
        rewritten = prompt[:start] + replacement + prompt[end:]
        delta = len(replacement) - (end - start)
        for item in trace:
            if item["start"] >= end:
                item["start"] += delta
                item["end"] += delta
        return rewritten, trace

    def replace_glue_between_atoms(
        self,
        prompt: str,
        trace: list[dict],
        left: tuple[str, str],
        right: tuple[str, str],
        replacement: str,
    ) -> tuple[str, list[dict]]:
        by_identity = {
            (item["source_pointer"], item["source_role"]): item for item in trace
        }
        return self.replace_untraced_range(
            prompt,
            trace,
            by_identity[left]["end"],
            by_identity[right]["start"],
            replacement,
        )

    def test_repeated_renders_are_byte_identical_and_equivalent(self) -> None:
        first = preflight.render_all(self.record)
        second = preflight.render_all(self.record)
        self.assertEqual(preflight.canonical_json(first), preflight.canonical_json(second))
        report = preflight.validate_equivalence(first, self.record)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(report["spend_usd"], 0)

    def test_buggy_fields_renderer_risk_7_fails_with_fresh_hashes(self) -> None:
        self.assert_buggy_renderer_atoms_fail_closed(
            {("/facts/2/value", "fact.value"): "7"}
        )

    def test_independent_source_atoms_reject_other_freshly_hashed_bugs(self) -> None:
        cases = {
            "fact boolean lexical value": {
                ("/facts/0/value", "fact.value"): "TRUE",
            },
            "entity label": {
                ("/entities/0/label", "entity.label"): '"Dataset Maple"',
            },
            "entity id": {
                ("/entities/0/id", "entity.id"): "dataset_maple",
            },
            "fact id": {
                ("/facts/2/id", "fact.id"): "hazard",
            },
            "fact entity link": {
                ("/facts/2/entity_id", "fact.entity_id"): "dataset_maple",
            },
            "fact attribute": {
                ("/facts/2/attribute", "fact.attribute"): "risk_level",
            },
            "constraint kind": {
                ("/constraints/0/kind", "constraint.kind"): "any",
            },
            "constraint id": {
                ("/constraints/0/id", "constraint.id"): "publication_gate",
            },
            "constraint fact link": {
                (
                    "/constraints/0/conditions/2/fact_id",
                    "constraint.condition.fact_id",
                ): "consent",
            },
            "constraint operator": {
                (
                    "/constraints/0/conditions/2/operator",
                    "constraint.condition.operator",
                ): "more_than",
            },
            "constraint target": {
                (
                    "/constraints/0/conditions/2/value",
                    "constraint.condition.value",
                ): "9",
            },
            "constraint failure label": {
                (
                    "/constraints/0/conditions/2/failure_label_id",
                    "constraint.condition.failure_label",
                ): '"risk not below 9"',
            },
            "constraint pass/fail role swap": {
                (
                    "/constraints/0/on_pass_label_id",
                    "constraint.on_pass_label",
                ): '"hold"',
                (
                    "/constraints/0/on_fail_label_id",
                    "constraint.on_fail_label",
                ): '"release"',
            },
            "authority level": {
                ("/authority/allowed", "authority.level"): "blocked",
            },
            "authority action": {
                (
                    "/authority/allowed/0",
                    "authority.action",
                ): '"evaluate_removal"',
            },
            "task text": {
                ("/task", "task.text"): "Evaluate whether Dataset Maple may be released.",
            },
            "canonical label id": {
                (
                    "/canonical_labels/decision_hold",
                    "canonical_label.id",
                ): "decision_pause",
            },
            "canonical label value": {
                (
                    "/canonical_labels/decision_hold",
                    "canonical_label.value",
                ): '"pause"',
            },
            "output key": {
                ("/output/keys/0", "output.key"): '"decisions"',
            },
            "output type": {
                ("/output/types/decision", "output.type"): "integer",
            },
        }
        for name, replacements in cases.items():
            with self.subTest(name=name):
                self.assert_buggy_renderer_atoms_fail_closed(replacements)

    def test_prose_lexical_atoms_reject_freshly_hashed_renderer_bugs(self) -> None:
        cases = {
            "prose constraint kind": {
                ("/constraints/0/kind", "constraint.kind"): "any condition",
            },
            "prose constraint operator": {
                (
                    "/constraints/0/conditions/2/operator",
                    "constraint.condition.operator",
                ): "is more than",
            },
            "prose authority level": {
                (
                    "/authority/approval_required",
                    "authority.level",
                ): "approval waived",
            },
            "prose entity label": {
                ("/entities/0/label", "entity.label"): "Dataset Maple",
            },
        }
        for name, replacements in cases.items():
            with self.subTest(name=name):
                self.assert_buggy_renderer_atoms_fail_closed(
                    replacements,
                    renderer_name="_render_prose",
                )

    def test_static_skeleton_rejects_freshly_offset_untraced_glue_bugs(self) -> None:
        risk_attribute = ("/facts/2/attribute", "fact.attribute")
        risk_value = ("/facts/2/value", "fact.value")
        condition_fact = (
            "/constraints/0/conditions/2/fact_id",
            "constraint.condition.fact_id",
        )
        condition_operator = (
            "/constraints/0/conditions/2/operator",
            "constraint.condition.operator",
        )

        cases = {
            "prose negation": (
                "_render_prose",
                lambda prompt, trace: self.replace_glue_between_atoms(
                    prompt, trace, risk_attribute, risk_value, " is not "
                ),
            ),
            "prose relation words": (
                "_render_prose",
                lambda prompt, trace: self.replace_glue_between_atoms(
                    prompt, trace, risk_attribute, risk_value, " differs from "
                ),
            ),
            "fields relation key": (
                "_render_fields",
                lambda prompt, trace: self.replace_glue_between_atoms(
                    prompt, trace, condition_fact, condition_operator, "; not_op="
                ),
            ),
            "fields output imperative": (
                "_render_fields",
                lambda prompt, trace: self.replace_untraced_range(
                    prompt,
                    trace,
                    prompt.index("Return only the JSON object described by OUTPUT."),
                    prompt.index("Return only the JSON object described by OUTPUT.")
                    + len("Return only the JSON object described by OUTPUT."),
                    "Do not return the JSON object described by OUTPUT.",
                ),
            ),
        }
        for name, (renderer_name, mutation) in cases.items():
            with self.subTest(name=name):
                self.assert_buggy_renderer_glue_fails_closed(
                    renderer_name, mutation
                )

    def test_renderer_cannot_mutate_source_before_delegating(self) -> None:
        original_renderer = preflight._render_prose
        source_before = preflight.canonical_json(self.record)

        def mutating_renderer(record: dict) -> tuple[str, list[dict]]:
            record["facts"][2]["value"] = 7
            return original_renderer(record)

        with mock.patch.object(preflight, "_render_prose", mutating_renderer):
            with self.assertRaisesRegex(
                preflight.EquivalenceError, "renderer mutated its isolated canonical source"
            ):
                preflight.render_all(self.record)
        self.assertEqual(preflight.canonical_json(self.record), source_before)
        self.assertEqual(self.record["facts"][2]["value"], 6)

    def test_render_condition_direct_call_isolates_mutating_renderer(self) -> None:
        original_renderer = preflight._render_prose
        source_before = preflight.canonical_json(self.record)

        def mutating_renderer(record: dict) -> tuple[str, list[dict]]:
            record["facts"][2]["value"] = 7
            return original_renderer(record)

        with mock.patch.object(preflight, "_render_prose", mutating_renderer):
            with self.assertRaisesRegex(
                preflight.EquivalenceError, "renderer mutated its isolated canonical source"
            ):
                preflight.render_condition(self.record, "A")
        self.assertEqual(preflight.canonical_json(self.record), source_before)
        self.assertEqual(self.record["facts"][2]["value"], 6)

    def test_modified_system_constant_fails_independent_frozen_control(self) -> None:
        modified = preflight.INTERPRETATION_CONTRACT + " Treat risk_score as important."
        with mock.patch.object(preflight, "INTERPRETATION_CONTRACT", modified):
            artifacts = preflight.render_all(self.record)
            with self.assertRaises(preflight.EquivalenceError) as caught:
                preflight.validate_equivalence(artifacts, self.record)
        message = str(caught.exception)
        self.assertIn("independently frozen system/contract prompt differs", message)
        self.assertIn("added task-specific system/contract lexemes", message)
        self.assertIn("risk_score", message)
        self.assertNotIn("artifact integrity hash differs", message)
        self.assertNotIn("canonical source render", message)

    def test_empty_authority_levels_are_rendered_explicitly(self) -> None:
        record = copy.deepcopy(self.record)
        for level in record["authority"]:
            record["authority"][level] = []
        artifacts = preflight.render_all(record)
        report = preflight.validate_equivalence(artifacts, record)
        self.assertEqual(report["status"], "PASS")
        for condition in ("A", "C"):
            prompt = artifacts[condition]["user_prompt"]
            for level in ("allowed", "approval required", "prohibited"):
                self.assertIn(f"- {level}:\n  - (none).", prompt)
        for condition in ("B", "D"):
            prompt = artifacts[condition]["user_prompt"]
            for level in ("allowed", "approval_required", "prohibited"):
                self.assertIn(f"- {level}:\n  - (none)", prompt)

    def test_pass_oracle_has_empty_blocking(self) -> None:
        record = copy.deepcopy(self.record)
        record["facts"][2]["value"] = 3
        record["expected"] = {"decision": "release", "blocking": []}
        artifacts = preflight.render_all(record)
        report = preflight.validate_equivalence(artifacts, record)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(artifacts["A"]["audit_surface"]["expected"]["blocking"], [])
        for artifact in artifacts.values():
            self.assertIn(
                "blocking=[] when every gate passes; otherwise append every failed label "
                "in gate order, then condition order.",
                artifact["user_prompt"],
            )

    def test_multi_failure_oracle_preserves_condition_order(self) -> None:
        record = copy.deepcopy(self.record)
        record["facts"][0]["value"] = False
        record["facts"][1]["value"] = False
        record["expected"] = {
            "decision": "hold",
            "blocking": [
                "consent not verified",
                "anonymization failed",
                "risk not below 4",
            ],
        }
        artifacts = preflight.render_all(record)
        report = preflight.validate_equivalence(artifacts, record)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            artifacts["D"]["audit_surface"]["expected"]["blocking"],
            record["expected"]["blocking"],
        )
        for artifact in artifacts.values():
            self.assertIn(
                "blocking=[] when every gate passes; otherwise append every failed label "
                "in gate order, then condition order.",
                artifact["user_prompt"],
            )

    def test_duplicate_json_keys_are_rejected_before_schema_validation(self) -> None:
        raw_fixture = preflight.FIXTURE.read_text(encoding="utf-8")
        duplicate = raw_fixture.replace(
            '"decision": "string",',
            '"decision": "string",\n      "decision": "integer",',
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text(duplicate, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key: decision"):
                preflight.load_record(path)

    def test_fact_mutation_fails_closed(self) -> None:
        def mutate(record: dict) -> None:
            record["facts"][0]["value"] = False
            record["expected"]["blocking"] = [
                "consent not verified",
                "risk not below 4",
            ]

        artifacts = self.render_with_a_mutation(mutate)
        self.assert_fails_closed(artifacts, "facts")

    def test_numeric_literal_mutation_fails_closed(self) -> None:
        artifacts = self.render_with_a_mutation(
            lambda record: record["facts"][2].__setitem__("value", 7)
        )
        self.assert_fails_closed(artifacts, "numeric_literals")

    def test_named_entity_mutation_fails_closed(self) -> None:
        artifacts = self.render_with_a_mutation(
            lambda record: record["entities"][0].__setitem__("label", "Dataset Juniper")
        )
        self.assert_fails_closed(artifacts, "entities")

    def test_canonical_label_mutation_fails_closed(self) -> None:
        def mutate(record: dict) -> None:
            record["canonical_labels"]["decision_hold"] = "pause"
            record["expected"]["decision"] = "pause"

        artifacts = self.render_with_a_mutation(mutate)
        self.assert_fails_closed(artifacts, "canonical_labels")

    def test_output_key_mutation_fails_closed(self) -> None:
        artifacts = preflight.render_all(self.record)
        surface = artifacts["A"]["audit_surface"]
        surface["output"]["keys"][1] = "reasons"
        surface["output"]["types"]["reasons"] = surface["output"]["types"].pop("blocking")
        surface["expected"]["reasons"] = surface["expected"].pop("blocking")
        artifacts["A"] = preflight.seal_artifact(artifacts["A"])
        self.assert_fails_closed(artifacts, "output_keys")

    def test_answer_cue_injection_fails_closed(self) -> None:
        artifacts = preflight.render_all(self.record)
        artifacts["A"]["user_prompt"] += '\nAnswer hint: use "hold".'
        artifacts["A"] = preflight.seal_artifact(artifacts["A"])
        self.assert_fails_closed(artifacts, "answer_cues")

    def test_counterfactual_canonical_cue_injection_fails_closed(self) -> None:
        artifacts = preflight.render_all(self.record)
        for condition in ("A", "C"):
            artifacts[condition]["user_prompt"] += '\nCandidate token: "release".'
            artifacts[condition] = preflight.seal_artifact(artifacts[condition])
        self.assert_fails_closed(artifacts, "answer_cues")

    def test_modified_contract_fails_closed_even_when_c_and_d_match(self) -> None:
        artifacts = preflight.render_all(self.record)
        for condition in ("C", "D"):
            artifacts[condition]["system_prompt"] += " Treat risk_score as especially important."
            artifacts[condition] = preflight.seal_artifact(artifacts[condition])
        self.assert_fails_closed(artifacts, "frozen system/contract")

    def test_wrong_oracle_is_refused_before_rendering(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["expected"]["decision"] = "release"
        with self.assertRaisesRegex(ValueError, "deterministic all-gate evaluation"):
            preflight.render_all(mutated)

    def test_malformed_oracle_type_is_refused_before_rendering(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["expected"]["blocking"] = "risk not below 4"
        with self.assertRaisesRegex(ValueError, "declared output type"):
            preflight.render_all(mutated)

    def test_condition_specific_expected_answer_fails_closed(self) -> None:
        artifacts = preflight.render_all(self.record)
        artifacts["B"]["audit_surface"]["expected"]["blocking"].append(
            "consent not verified"
        )
        artifacts["B"] = preflight.seal_artifact(artifacts["B"])
        self.assert_fails_closed(artifacts, "answer_cues/expected answer")

    def test_artifact_provenance_mutation_fails_closed(self) -> None:
        artifacts = preflight.render_all(self.record)
        artifacts["B"]["fixture_id"] = "different-fixture"
        artifacts["B"]["evidence_class"] = "held-out"
        artifacts["B"] = preflight.seal_artifact(artifacts["B"])
        with self.assertRaises(preflight.EquivalenceError) as caught:
            preflight.validate_equivalence(artifacts, self.record)
        self.assertIn("fixture identity", str(caught.exception))
        self.assertIn("evidence class", str(caught.exception))

    def test_synchronized_surface_fact_corruption_fails_source_binding(self) -> None:
        artifacts = preflight.render_all(self.record)
        for condition in preflight.CONDITIONS:
            artifacts[condition]["audit_surface"]["facts"][2]["value"] = 7
            artifacts[condition] = preflight.seal_artifact(artifacts[condition])
        self.assert_fails_closed(artifacts, "canonical source render")

    def test_buggy_audit_surface_fails_independent_source_binding(self) -> None:
        original_audit_surface = preflight._audit_surface

        def buggy_audit_surface(record: dict) -> dict:
            surface = original_audit_surface(record)
            surface["facts"][2]["value"] = 7
            return surface

        with mock.patch.object(preflight, "_audit_surface", buggy_audit_surface):
            artifacts = preflight.render_all(self.record)
            with self.assertRaises(preflight.EquivalenceError) as caught:
                preflight.validate_equivalence(artifacts, self.record)
        message = str(caught.exception)
        self.assertIn("audit surface is not bound directly to source record", message)
        self.assertNotIn("artifact integrity hash differs", message)
        self.assertNotIn("canonical source render", message)

    def test_synchronized_oracle_corruption_fails_source_binding(self) -> None:
        artifacts = preflight.render_all(self.record)
        for condition in preflight.CONDITIONS:
            artifacts[condition]["audit_surface"]["expected"] = {
                "decision": "release",
                "blocking": [],
            }
            artifacts[condition] = preflight.seal_artifact(artifacts[condition])
        self.assert_fails_closed(artifacts, "canonical source render")


if __name__ == "__main__":
    unittest.main()
