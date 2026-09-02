#!/usr/bin/env python3
"""Offline tests for the Benchmark 003 two-stage human-review bundle."""

from __future__ import annotations

import copy
import os
import stat
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))
import benchmark_003_build_review_packet as review  # noqa: E402


NONCE = bytes(range(32)).hex()
OTHER_NONCE = bytes(range(32, 64)).hex()


class Benchmark003ReviewBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = review.source_manifest()
        cls.phase1, cls.reveal = review.build_bundle(NONCE, manifest=cls.manifest)

    def reseal(self, value: dict, digest_key: str) -> dict:
        return review._seal(value, digest_key)

    def valid_phase1_response(self) -> dict:
        judgment = {"verdict": "PASS", "rationale": "No defect observed in this item."}
        profile_judgment = {
            **judgment,
            "semantic_extraction": {
                field: f"Independent synthetic extraction for {field}."
                for field in review.SEMANTIC_EXTRACTION_FIELDS
            },
            "mutation_probe_judgments": {
                item["probe_id"]: copy.deepcopy(judgment)
                for item in review.MUTATION_PROBES
            },
        }
        return {
            "schema_version": review.PHASE1_RESPONSE_SCHEMA_VERSION,
            "phase1_packet_sha256": self.phase1["phase1_packet_sha256"],
            "reviewer": {
                "name": "Synthetic Test Reviewer",
                "qualifications": "Test fixture only",
                "conflicts": "None declared for this synthetic test",
                "prior_exposure": "No exposure in this synthetic test",
                "independence_statement": "Independent synthetic validation record",
                "public_attribution_consent": False,
            },
            "profile_judgments": {
                item["profile_id"]: copy.deepcopy(profile_judgment)
                for item in self.phase1["profiles"]
            },
            "cross_profile_judgments": {
                item: copy.deepcopy(judgment)
                for item in review.CROSS_PROFILE_ITEMS
            },
        }

    def valid_phase2_response(self, phase1_response: dict) -> dict:
        phase1_result = review.validate_phase1_response(self.phase1, phase1_response)
        judgment = {"verdict": "PASS", "rationale": "Resolved for synthetic test."}
        return {
            "schema_version": review.PHASE2_RESPONSE_SCHEMA_VERSION,
            "phase1_packet_sha256": self.phase1["phase1_packet_sha256"],
            "phase1_response_sha256": phase1_result["phase1_response_sha256"],
            "reveal_sha256": self.reveal["reveal_sha256"],
            "known_issue_dispositions": {
                issue_id: copy.deepcopy(judgment)
                for issue_id in review.KNOWN_ISSUE_IDS
            },
            "overall_verdict": "PASS",
            "rationale": "All synthetic test judgments are complete.",
            "authorizes_fixture_extension": False,
        }

    def test_same_inputs_and_nonce_are_byte_identical(self) -> None:
        phase1, reveal = review.build_bundle(NONCE, manifest=self.manifest)
        self.assertEqual(review.canonical_bytes(phase1), review.canonical_bytes(self.phase1))
        self.assertEqual(review.canonical_bytes(reveal), review.canonical_bytes(self.reveal))

    def test_different_nonce_changes_packet_and_allocation(self) -> None:
        phase1, reveal = review.build_bundle(OTHER_NONCE, manifest=self.manifest)
        self.assertNotEqual(
            phase1["phase1_packet_sha256"], self.phase1["phase1_packet_sha256"]
        )
        self.assertNotEqual(phase1["allocation_commitment"], self.phase1["allocation_commitment"])
        self.assertNotEqual(reveal["mapping"], self.reveal["mapping"])

    def test_obviously_weak_nonce_fails_closed(self) -> None:
        with self.assertRaisesRegex(review.ReviewBundleError, "low-diversity"):
            review.build_bundle("00" * 32, manifest=self.manifest)

    def test_private_nonce_and_reveal_writes_are_exclusive_and_mode_0600(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            private_dir = Path(directory)
            os.chmod(private_dir, 0o700)
            nonce_path = private_dir / "nonce.hex"
            generated = review._generate_nonce_file(nonce_path)
            self.assertEqual(review._read_nonce_file(nonce_path), generated)
            self.assertEqual(stat.S_IMODE(nonce_path.stat().st_mode), 0o600)
            with self.assertRaisesRegex(review.ReviewBundleError, "overwrite"):
                review._generate_nonce_file(nonce_path)

            reveal_path = private_dir / "reveal.json"
            review._write_json_exclusive(
                reveal_path,
                self.reveal,
                mode=0o600,
                private_parent=True,
            )
            self.assertEqual(stat.S_IMODE(reveal_path.stat().st_mode), 0o600)
            with self.assertRaisesRegex(review.ReviewBundleError, "overwrite"):
                review._write_json_exclusive(
                    reveal_path,
                    self.reveal,
                    mode=0o600,
                    private_parent=True,
                )

    def test_packets_verify_and_cover_four_profiles(self) -> None:
        review.verify_phase1(self.phase1)
        review.verify_reveal(self.phase1, self.reveal)
        self.assertEqual(len(self.phase1["profiles"]), 4)
        self.assertEqual(set(self.reveal["mapping"].values()), {"A", "B", "C", "D"})

    def test_phase1_structurally_omits_reveal_and_oracle_keys(self) -> None:
        leaked = review._walk_keys(self.phase1) & review.FORBIDDEN_PHASE1_KEYS
        self.assertEqual(leaked, set())
        self.assertNotIn("expected", self.phase1["source_without_oracle"])

    def test_phase1_contains_no_prior_automated_result(self) -> None:
        serialized = review.canonical_json(self.phase1)
        self.assertNotIn("preflight_result", serialized)
        self.assertNotIn("known_issues", serialized)
        self.assertEqual(self.phase1["status"], "draft-not-reviewed")

    def test_phase1_exposes_no_unsalted_oracle_bearing_digest(self) -> None:
        record, _, result = review._current_semantic_evidence()
        context = review._source_context(self.manifest, record, result)
        forbidden = {
            result["semantic_record_sha256"],
            self.manifest["files"][
                "experiments/benchmark_003_development_fixture.json"
            ],
            review.sha256_bytes(review.canonical_bytes(context)),
        }
        serialized = review.canonical_json(self.phase1)
        self.assertTrue(all(value not in serialized for value in forbidden))

    def test_unknown_phase1_or_nested_profile_field_fails_closed(self) -> None:
        for location in ("top", "profile"):
            with self.subTest(location=location):
                tampered = copy.deepcopy(self.phase1)
                if location == "top":
                    tampered["answer_oracle_under_unchecked_name"] = "hold"
                else:
                    tampered["profiles"][0]["opaque_profile_A"] = True
                tampered = self.reseal(tampered, "phase1_packet_sha256")
                with self.assertRaisesRegex(
                    review.ReviewBundleError, "missing or unexpected fields"
                ):
                    review.verify_phase1(tampered, expected_manifest=self.manifest)

    def test_mutable_phase1_response_requirements_fail_closed(self) -> None:
        tampered = copy.deepcopy(self.phase1)
        tampered["response_schema"]["required_profile_ids"] = []
        tampered["response_schema"]["required_cross_profile_items"] = []
        tampered["response_schema"]["required_reviewer_fields"] = [
            "public_attribution_consent"
        ]
        tampered = self.reseal(tampered, "phase1_packet_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "fixed requirements"):
            review.verify_phase1(tampered, expected_manifest=self.manifest)

    def test_tampered_prompt_fails_even_when_packet_is_resealed(self) -> None:
        tampered = copy.deepcopy(self.phase1)
        tampered["profiles"][0]["user_prompt"] += "\nTAMPERED"
        tampered = self.reseal(tampered, "phase1_packet_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "user_prompt hash differs"):
            review.verify_phase1(tampered)

    def test_tampered_source_fails_even_when_packet_is_resealed(self) -> None:
        tampered = copy.deepcopy(self.phase1)
        tampered["source_without_oracle"]["task"] += " TAMPERED"
        tampered["source_without_oracle_sha256"] = review.sha256_bytes(
            review.canonical_bytes(tampered["source_without_oracle"])
        )
        tampered = self.reseal(tampered, "phase1_packet_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "canonical source"):
            review.verify_phase1(tampered, expected_manifest=self.manifest)

    def test_bool_int_alias_cannot_bypass_source_binding(self) -> None:
        tampered_phase1 = copy.deepcopy(self.phase1)
        self.assertIs(tampered_phase1["source_without_oracle"]["facts"][0]["value"], True)
        tampered_phase1["source_without_oracle"]["facts"][0]["value"] = 1
        tampered_phase1 = self.reseal(tampered_phase1, "phase1_packet_sha256")
        tampered_reveal = copy.deepcopy(self.reveal)
        tampered_reveal["phase1_packet_sha256"] = tampered_phase1[
            "phase1_packet_sha256"
        ]
        tampered_reveal = self.reseal(tampered_reveal, "reveal_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "canonical source"):
            review.verify_reveal(tampered_phase1, tampered_reveal)

    def test_boolean_zero_accounting_alias_fails_closed(self) -> None:
        tampered_phase1 = copy.deepcopy(self.phase1)
        tampered_phase1["model_calls"] = False
        tampered_phase1["provider_calls"] = False
        tampered_phase1["spend_usd"] = False
        tampered_phase1 = self.reseal(tampered_phase1, "phase1_packet_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "integer zero"):
            review.verify_phase1(tampered_phase1)

    def test_manifest_byte_change_fails_commit_binding(self) -> None:
        changed_manifest = copy.deepcopy(self.manifest)
        path = next(iter(changed_manifest["files"]))
        changed_manifest["files"][path] = "f" * 64
        with self.assertRaisesRegex(review.ReviewBundleError, "recorded commit"):
            review.build_bundle(NONCE, manifest=changed_manifest)

    def test_noncommit_manifest_head_fails_closed(self) -> None:
        changed_manifest = copy.deepcopy(self.manifest)
        changed_manifest["git_head_at_build"] = "f" * 40
        with self.assertRaisesRegex(review.ReviewBundleError, "resolvable commit"):
            review.build_bundle(NONCE, manifest=changed_manifest)

    def test_working_tree_bytes_must_match_manifest(self) -> None:
        original_sha256_file = review.sha256_file
        first_bound_path = review.BOUND_PATHS[0]

        def altered_hash(path: Path) -> str:
            if path == first_bound_path:
                return "0" * 64
            return original_sha256_file(path)

        with mock.patch.object(review, "sha256_file", side_effect=altered_hash):
            with self.assertRaisesRegex(review.ReviewBundleError, "working-tree bytes"):
                review.build_bundle(NONCE, manifest=self.manifest)

    def test_wrong_nonce_cannot_open_resealed_reveal(self) -> None:
        tampered = copy.deepcopy(self.reveal)
        tampered["nonce_hex"] = OTHER_NONCE
        tampered = self.reseal(tampered, "reveal_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "source context commitment"):
            review.verify_reveal(self.phase1, tampered)

    def test_wrong_mapping_cannot_open_resealed_reveal(self) -> None:
        tampered = copy.deepcopy(self.reveal)
        keys = list(tampered["mapping"])
        tampered["mapping"][keys[0]], tampered["mapping"][keys[1]] = (
            tampered["mapping"][keys[1]],
            tampered["mapping"][keys[0]],
        )
        tampered = self.reseal(tampered, "reveal_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "deterministic allocation"):
            review.verify_reveal(self.phase1, tampered)

    def test_prompt_payload_swap_cannot_hide_behind_valid_mapping(self) -> None:
        tampered_phase1 = copy.deepcopy(self.phase1)
        first, second = tampered_phase1["profiles"][:2]
        for field in (
            "system_prompt",
            "system_prompt_sha256",
            "user_prompt",
            "user_prompt_sha256",
        ):
            first[field], second[field] = second[field], first[field]
        tampered_phase1 = self.reseal(tampered_phase1, "phase1_packet_sha256")
        tampered_reveal = copy.deepcopy(self.reveal)
        tampered_reveal["phase1_packet_sha256"] = tampered_phase1[
            "phase1_packet_sha256"
        ]
        tampered_reveal = self.reseal(tampered_reveal, "reveal_sha256")
        with self.assertRaisesRegex(review.ReviewBundleError, "revealed condition"):
            review.verify_reveal(tampered_phase1, tampered_reveal)

    def test_resealed_reveal_core_tampering_fails_closed(self) -> None:
        mutations = {
            "source_context": lambda value: value["source_context"].__setitem__(
                "fixture_id", "tampered"
            ),
            "factor_metadata": lambda value: next(
                iter(value["factor_metadata"].values())
            ).__setitem__("artifact_sha256", "0" * 64),
            "expected_oracle": lambda value: value["expected_oracle"].__setitem__(
                "decision", "tampered"
            ),
            "preflight_result": lambda value: value["preflight_result"].__setitem__(
                "status", "tampered"
            ),
            "known_issue": lambda value: value["known_issues"][0].__setitem__(
                "status", "tampered"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(field=label):
                tampered = copy.deepcopy(self.reveal)
                mutate(tampered)
                tampered = self.reseal(tampered, "reveal_sha256")
                with self.assertRaises(review.ReviewBundleError):
                    review.verify_reveal(
                        self.phase1, tampered, expected_manifest=self.manifest
                    )

    def test_reveal_contains_all_known_issue_dossiers(self) -> None:
        issues = {item["issue_id"]: item for item in self.reveal["known_issues"]}
        self.assertEqual(set(issues), set(review.KNOWN_ISSUE_IDS))
        injection = issues["raw-string-structural-injection-false-pass"]
        self.assertEqual(
            [item["preflight_status"] for item in injection["evidence"]],
            ["PASS", "PASS", "PASS", "PASS"],
        )
        self.assertTrue(
            any(item["fields_contains_json_escaped_marker"] for item in injection["evidence"])
        )

    def test_reveal_preserves_schema_and_error_contract_gaps(self) -> None:
        issue = next(
            item
            for item in self.reveal["known_issues"]
            if item["issue_id"] == "schema-and-error-contract-gaps"
        )
        evidence = issue["evidence"]
        self.assertEqual(evidence["empty_fact_id_validation_result"], "NO_EXCEPTION")
        self.assertEqual(evidence["non_object_artifact_exception"], "AttributeError")
        self.assertEqual(evidence["non_object_audit_surface_exception"], "TypeError")

    def test_common_baseline_replacement_is_explicit(self) -> None:
        issue = next(
            item
            for item in self.reveal["known_issues"]
            if item["issue_id"] == "common-system-baseline-replaced"
        )
        self.assertFalse(issue["evidence"]["contract_contains_common_baseline"])

    def test_complete_phase1_response_can_derive_pass(self) -> None:
        result = review.validate_phase1_response(
            self.phase1, self.valid_phase1_response()
        )
        self.assertEqual(result["disposition"], "PASS")
        self.assertEqual(len(result["phase1_response_sha256"]), 64)

    def test_any_uncertainty_derives_revise(self) -> None:
        response = self.valid_phase1_response()
        first_profile = next(iter(response["profile_judgments"]))
        response["profile_judgments"][first_profile]["verdict"] = "UNCERTAIN"
        response["profile_judgments"][first_profile][
            "rationale"
        ] = "The evidence is insufficient."
        result = review.validate_phase1_response(self.phase1, response)
        self.assertEqual(result["disposition"], "REVISE")

    def test_missing_reviewer_disclosure_fails_closed(self) -> None:
        response = self.valid_phase1_response()
        response["reviewer"].pop("conflicts")
        with self.assertRaisesRegex(review.ReviewBundleError, "disclosure fields"):
            review.validate_phase1_response(self.phase1, response)

    def test_missing_profile_judgment_fails_closed(self) -> None:
        response = self.valid_phase1_response()
        response["profile_judgments"].pop(next(iter(response["profile_judgments"])))
        with self.assertRaisesRegex(review.ReviewBundleError, "every opaque profile"):
            review.validate_phase1_response(self.phase1, response)

    def test_missing_semantic_extraction_or_mutation_judgment_fails_closed(self) -> None:
        profile_id = self.phase1["profiles"][0]["profile_id"]
        response = self.valid_phase1_response()
        response["profile_judgments"][profile_id]["semantic_extraction"].pop("facts")
        with self.assertRaisesRegex(review.ReviewBundleError, "semantic extraction"):
            review.validate_phase1_response(self.phase1, response)

        response = self.valid_phase1_response()
        response["profile_judgments"][profile_id]["mutation_probe_judgments"].pop(
            review.MUTATION_PROBES[0]["probe_id"]
        )
        with self.assertRaisesRegex(review.ReviewBundleError, "mutation judgments"):
            review.validate_phase1_response(self.phase1, response)

    def test_phase2_requires_every_known_issue(self) -> None:
        phase1_response = self.valid_phase1_response()
        phase2_response = self.valid_phase2_response(phase1_response)
        phase2_response["known_issue_dispositions"].pop(review.KNOWN_ISSUE_IDS[0])
        with self.assertRaisesRegex(review.ReviewBundleError, "every known issue"):
            review.validate_phase2_response(
                self.phase1,
                self.reveal,
                phase1_response,
                phase2_response,
            )

    def test_phase2_nonpass_derives_revise(self) -> None:
        phase1_response = self.valid_phase1_response()
        phase2_response = self.valid_phase2_response(phase1_response)
        phase2_response["known_issue_dispositions"][review.KNOWN_ISSUE_IDS[0]] = {
            "verdict": "REVISE",
            "rationale": "The issue remains unresolved.",
        }
        result = review.validate_phase2_response(
            self.phase1,
            self.reveal,
            phase1_response,
            phase2_response,
        )
        self.assertEqual(result["disposition"], "REVISE")

    def test_current_unresolved_dossiers_force_revise(self) -> None:
        phase1_response = self.valid_phase1_response()
        phase2_response = self.valid_phase2_response(phase1_response)
        self.assertTrue(
            any(
                item["status"] != review.RESOLVED_ISSUE_STATUS
                for item in self.reveal["known_issues"]
            )
        )
        result = review.validate_phase2_response(
            self.phase1,
            self.reveal,
            phase1_response,
            phase2_response,
        )
        self.assertEqual(result["disposition"], "REVISE")

    def test_phase2_cannot_authorize_fixture_extension(self) -> None:
        phase1_response = self.valid_phase1_response()
        phase2_response = self.valid_phase2_response(phase1_response)
        phase2_response["authorizes_fixture_extension"] = True
        with self.assertRaisesRegex(review.ReviewBundleError, "may not authorize"):
            review.validate_phase2_response(
                self.phase1,
                self.reveal,
                phase1_response,
                phase2_response,
            )

    def test_phase2_response_binds_exact_reveal(self) -> None:
        phase1_response = self.valid_phase1_response()
        phase2_response = self.valid_phase2_response(phase1_response)
        phase2_response["reveal_sha256"] = "0" * 64
        with self.assertRaisesRegex(review.ReviewBundleError, "wrong reveal"):
            review.validate_phase2_response(
                self.phase1,
                self.reveal,
                phase1_response,
                phase2_response,
            )

    def test_bundle_records_zero_calls_and_spend(self) -> None:
        for document in (self.phase1, self.reveal):
            self.assertEqual(document["model_calls"], 0)
            self.assertEqual(document["provider_calls"], 0)
            self.assertEqual(document["spend_usd"], 0.0)


if __name__ == "__main__":
    unittest.main()
