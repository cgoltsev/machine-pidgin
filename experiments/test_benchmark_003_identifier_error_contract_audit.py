#!/usr/bin/env python3
"""Regression tests for the Benchmark 003 identifier/error-contract audit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))
import benchmark_003_equivalence_preflight as preflight  # noqa: E402
import benchmark_003_identifier_error_contract_audit as audit  # noqa: E402


class Benchmark003IdentifierErrorContractAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.run_audit()

    def identifier_case(self, case_id: str) -> dict:
        return next(
            case
            for case in self.result["identifier_cases"]
            if case["case_id"] == case_id
        )

    def container_case(self, case_id: str) -> dict:
        return next(
            case
            for case in self.result["malformed_container_cases"]
            if case["case_id"] == case_id
        )

    def test_identifier_matrix_is_complete_and_preserves_false_accepts(self) -> None:
        expected_case_ids = {
            "record-id-empty",
            "record-id-integer",
            "entity-id-empty-with-references",
            "entity-id-integer-with-references",
            "fact-id-empty-with-references",
            "fact-id-integer-with-references",
            "constraint-id-empty",
            "constraint-id-integer",
            "canonical-label-id-empty-with-references",
            "canonical-label-id-integer-with-references",
            "output-key-empty-with-dependent-maps",
            "output-key-integer-with-dependent-maps",
            "fact-entity-reference-empty",
            "fact-entity-reference-integer",
            "condition-fact-reference-empty",
            "condition-fact-reference-integer",
            "condition-failure-label-reference-empty",
            "condition-failure-label-reference-integer",
            "constraint-pass-label-reference-empty",
            "constraint-pass-label-reference-integer",
            "constraint-fail-label-reference-empty",
            "constraint-fail-label-reference-integer",
        }
        observed_case_ids = {
            case["case_id"] for case in self.result["identifier_cases"]
        }
        self.assertEqual(len(observed_case_ids), len(self.result["identifier_cases"]))
        self.assertEqual(observed_case_ids, expected_case_ids)
        self.assertEqual(self.result["scope"]["identifier_reference_cases"], 22)
        self.assertEqual(
            self.result["summary"][
                "identifier_cases_with_deliberate_record_rejection"
            ],
            20,
        )
        self.assertEqual(
            self.result["summary"][
                "identifier_cases_accepted_at_record_validation"
            ],
            2,
        )
        self.assertEqual(
            self.result["summary"][
                "identifier_cases_with_incidental_record_exception"
            ],
            0,
        )
        self.assertEqual(
            self.result["summary"][
                "identifier_cases_with_unexpected_record_exception"
            ],
            0,
        )
        self.assertEqual(
            self.result["summary"]["accepted_identifier_case_ids"],
            [
                "fact-id-empty-with-references",
                "fact-id-integer-with-references",
            ],
        )
        for case in self.result["identifier_cases"]:
            with self.subTest(case_id=case["case_id"]):
                expected = (
                    "ACCEPTED"
                    if case["case_id"]
                    in {
                        "fact-id-empty-with-references",
                        "fact-id-integer-with-references",
                    }
                    else "REJECTED"
                )
                self.assertEqual(case["record_validation"]["status"], expected)
                if expected == "REJECTED":
                    self.assertEqual(
                        case["record_validation"]["interface"],
                        "record-value-error",
                    )

    def test_fact_identifier_failures_remain_stage_specific(self) -> None:
        empty_id = self.identifier_case("fact-id-empty-with-references")
        self.assertEqual(empty_id["record_validation"]["status"], "ACCEPTED")
        self.assertEqual(empty_id["render_all"]["status"], "ACCEPTED")
        self.assertEqual(
            empty_id["validate_equivalence"]["exception_class"],
            "EquivalenceError",
        )

        integer_id = self.identifier_case("fact-id-integer-with-references")
        self.assertEqual(integer_id["record_validation"]["status"], "ACCEPTED")
        self.assertEqual(integer_id["render_all"]["exception_class"], "TypeError")
        self.assertEqual(
            integer_id["render_all"]["interface"],
            "incidental-python-exception",
        )
        self.assertEqual(integer_id["validate_equivalence"]["status"], "NOT_RUN")

    def test_malformed_container_matrix_records_raw_exception_surface(self) -> None:
        self.assertEqual(self.result["scope"]["malformed_container_cases"], 17)
        self.assertEqual(
            self.result["summary"][
                "container_cases_with_incidental_python_exception"
            ],
            14,
        )
        self.assertEqual(
            self.result["summary"][
                "container_cases_with_deliberate_validation_exception"
            ],
            3,
        )
        self.assertEqual(self.result["summary"]["container_cases_accepted"], 0)
        self.assertEqual(
            self.result["summary"]["container_cases_with_unexpected_exception"],
            0,
        )

        expected_interfaces = {
            "record-root-null": "incidental-python-exception",
            "entity-item-null": "incidental-python-exception",
            "fact-item-null": "incidental-python-exception",
            "constraint-item-null": "incidental-python-exception",
            "condition-item-null": "incidental-python-exception",
            "authority-null": "incidental-python-exception",
            "canonical-labels-null": "record-value-error",
            "output-null": "incidental-python-exception",
            "artifacts-root-null": "incidental-python-exception",
            "condition-artifact-null": "incidental-python-exception",
            "condition-artifact-list": "incidental-python-exception",
            "audit-surface-null": "incidental-python-exception",
            "audit-surface-list": "incidental-python-exception",
            "trace-null": "aggregate-equivalence-error",
            "trace-item-null": "aggregate-equivalence-error",
            "system-prompt-null": "incidental-python-exception",
            "user-prompt-null": "incidental-python-exception",
        }
        observed_interfaces = {
            case["case_id"]: case["result"]["interface"]
            for case in self.result["malformed_container_cases"]
        }
        self.assertEqual(observed_interfaces, expected_interfaces)

    def test_deliberate_rejections_are_not_reclassified_as_raw(self) -> None:
        self.assertEqual(
            self.container_case("canonical-labels-null")["result"]["interface"],
            "record-value-error",
        )
        for case_id in ("trace-null", "trace-item-null"):
            with self.subTest(case_id=case_id):
                self.assertEqual(
                    self.container_case(case_id)["result"]["interface"],
                    "aggregate-equivalence-error",
                )

    def test_result_is_deterministic_and_records_zero_calls_and_spend(self) -> None:
        repeated = audit.run_audit()
        self.assertEqual(
            preflight.canonical_json(self.result),
            preflight.canonical_json(repeated),
        )
        self.assertEqual(
            self.result["accounting"],
            {
                "model_calls": 0,
                "provider_calls": 0,
                "paid_services": 0,
                "spend_usd": 0.0,
            },
        )
        self.assertRegex(self.result["scope"]["runtime"]["python"], r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
