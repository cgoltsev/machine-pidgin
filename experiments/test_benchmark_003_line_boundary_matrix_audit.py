#!/usr/bin/env python3
"""Regression tests for the Benchmark 003 line-boundary matrix audit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))
import benchmark_003_equivalence_preflight as preflight  # noqa: E402
import benchmark_003_line_boundary_matrix_audit as audit  # noqa: E402


class Benchmark003LineBoundaryMatrixAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.run_audit()

    def case(self, surface: str, boundary: str) -> dict:
        case_id = f"{surface}--{boundary}"
        return next(
            case for case in self.result["cases"] if case["case_id"] == case_id
        )

    def test_matrix_is_complete_and_all_mutations_are_currently_accepted(self) -> None:
        self.assertEqual(self.result["scope"]["boundary_forms"], 11)
        self.assertEqual(self.result["scope"]["source_surfaces"], 4)
        self.assertEqual(self.result["scope"]["mutation_cases"], 44)
        self.assertEqual(self.result["scope"]["render_observations"], 176)
        self.assertEqual(self.result["summary"]["record_validation_accepted"], 44)
        self.assertEqual(self.result["summary"]["record_validation_rejected"], 0)
        self.assertEqual(self.result["summary"]["preflight_pass"], 44)
        self.assertEqual(self.result["summary"]["preflight_rejected"], 0)

    def test_literal_split_line_count_and_representation_asymmetry_are_fixed(self) -> None:
        self.assertEqual(
            self.result["summary"]["reserved_heading_is_split_line"], 144
        )
        self.assertEqual(
            self.result["summary"]["reserved_heading_not_split_line"], 32
        )

        entity_lf = self.case("entity-label", "line-feed")["observations"]
        self.assertTrue(entity_lf["A"]["reserved_heading_is_split_line"])
        self.assertFalse(entity_lf["B"]["reserved_heading_is_split_line"])
        self.assertTrue(entity_lf["C"]["reserved_heading_is_split_line"])
        self.assertFalse(entity_lf["D"]["reserved_heading_is_split_line"])
        self.assertEqual(entity_lf["A"]["lexical_form"], "raw")
        self.assertEqual(entity_lf["B"]["lexical_form"], "json")

        entity_ls = self.case("entity-label", "line-separator")["observations"]
        self.assertTrue(
            all(
                observation["reserved_heading_is_split_line"]
                for observation in entity_ls.values()
            )
        )

        task_ls = self.case("task", "line-separator")
        self.assertEqual(
            task_ls["semantic_record_sha256"],
            "5437bbc8460fefbc3bbe2eca5456800c68243efda59b5fa96335a0f804f26b5a",
        )

    def test_raw_surfaces_expose_every_boundary_in_all_conditions(self) -> None:
        for surface in ("task", "fact-attribute"):
            for boundary in (item["id"] for item in audit.BOUNDARIES):
                with self.subTest(surface=surface, boundary=boundary):
                    observations = self.case(surface, boundary)["observations"]
                    self.assertEqual(set(observations), set(preflight.CONDITIONS))
                    self.assertTrue(
                        all(
                            item["reserved_heading_is_split_line"]
                            for item in observations.values()
                        )
                    )

    def test_shared_renderer_profiles_have_identical_trace_observations(self) -> None:
        for case in self.result["cases"]:
            with self.subTest(case_id=case["case_id"]):
                observations = case["observations"]
                self.assertEqual(observations["A"], observations["C"])
                self.assertEqual(observations["B"], observations["D"])

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
        self.assertRegex(
            self.result["scope"]["runtime"]["unicode_database"],
            r"^\d+\.\d+\.\d+$",
        )


if __name__ == "__main__":
    unittest.main()
