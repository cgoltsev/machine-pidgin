#!/usr/bin/env python3
"""Regression tests for the bounded Benchmark 003 factor-label audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "benchmark_003_factor_label_audit.py"
sys.path.insert(0, str(HERE))
import benchmark_003_factor_label_audit as audit_module  # noqa: E402


class FactorLabelAuditTests(unittest.TestCase):
    def test_bound_sources_match_exact_current_bytes(self) -> None:
        self.assertEqual(
            audit_module.source_hashes(),
            audit_module.EXPECTED_SOURCE_SHA256,
        )

    def test_factor_isolation_and_replacement_are_distinguished(self) -> None:
        result = audit_module.audit()
        checks = result["factor_isolation_checks"]
        self.assertTrue(checks["representation_factor_system_equal_without_contract"])
        self.assertTrue(checks["representation_factor_system_equal_with_contract"])
        self.assertTrue(checks["contract_factor_user_equal_for_prose"])
        self.assertTrue(checks["contract_factor_user_equal_for_fields"])
        self.assertFalse(checks["contract_preserves_base_system_verbatim"])
        self.assertFalse(checks["contract_equals_published_spear_0_2_prompt"])

    def test_representation_characterization_is_exact(self) -> None:
        audit = audit_module.audit()
        result = audit["representation_factor"]
        self.assertEqual(result["field_renderer_section_count"], 8)
        self.assertEqual(result["prose_renderer_section_count"], 7)
        self.assertTrue(result["prose_renderer_is_explicitly_sectioned"])
        self.assertEqual(
            result["classification_counts"],
            {"exact_heading": 3, "partial_construct": 5, "absent": 4},
        )
        self.assertEqual(
            {
                field: assessment["classification"]
                for field, assessment in result["field_assessment"].items()
            },
            {
                "TASK": "exact_heading",
                "OBJECTS & TYPES": "partial_construct",
                "AUTHORITY": "exact_heading",
                "ABSTRACTION": "absent",
                "OBJECTIVE": "absent",
                "CONSTRAINTS": "partial_construct",
                "PRECEDENCE & VOCABULARY": "partial_construct",
                "UNCERTAINTY": "absent",
                "OUTPUT": "exact_heading",
                "EVALUATION & CHECK": "partial_construct",
                "INTERACTION / STOP": "partial_construct",
                "EXAMPLES": "absent",
            },
        )
        self.assertEqual(result["published_spear_field_count"], 12)
        self.assertTrue(
            any(
                "three exact published SPEAR/0.2 headings, five Researcher-mapped partial constructs, and four absent published fields"
                in finding
                for finding in audit["falsifying_findings"]
            )
        )

    def test_contract_characterization_is_exact(self) -> None:
        result = audit_module.audit()["contract_factor"]
        self.assertEqual(result["published_numbered_operating_rule_count"], 12)
        self.assertEqual(result["current_contract_numbered_operating_rule_count"], 0)
        self.assertEqual(
            result["published_field_labels_present_verbatim_in_current_contract"],
            [],
        )

    def test_cli_is_deterministic_ascii_json(self) -> None:
        first = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=HERE,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        second = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=HERE,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(first, second)
        first.encode("ascii")
        parsed = json.loads(first)
        self.assertEqual(parsed["derived_researcher_disposition"], "REVISE")
        self.assertEqual(parsed["model_calls"], 0)
        self.assertEqual(parsed["provider_calls"], 0)
        self.assertEqual(parsed["exact_spend_usd"], "0.00")


if __name__ == "__main__":
    unittest.main()
