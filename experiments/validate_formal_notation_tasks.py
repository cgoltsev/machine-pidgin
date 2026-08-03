#!/usr/bin/env python3
"""Static integrity checks for Benchmark 002 before any model call."""

from __future__ import annotations

import json
from pathlib import Path

TASKS = Path(__file__).with_name("formal_notation_tasks.json")
REQUIRED = {"id", "split", "category", "notation_expected_to_help", "vernacular", "formal", "expected"}
EXPECTED_LITERAL_MIN_LENGTH = 4

# The task corpus is frozen because its SHA-256 hash is part of the published raw
# record. Keep the two known development/held-out asymmetries visible here so a
# future prompt edit or newly introduced cue fails validation instead of silently
# changing the intervention.
KNOWN_OUTPUT_LITERAL_ASYMMETRIES = {
    ("dev-math-04-stop-gate", "rollback not ready", "vernacular_only"),
    ("test-math-14-workflow", "open the vote", "formal_only"),
}


def expected_string_leaves(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from expected_string_leaves(child)
    elif isinstance(value, list):
        for child in value:
            yield from expected_string_leaves(child)
    elif isinstance(value, str) and len(value.strip()) >= EXPECTED_LITERAL_MIN_LENGTH:
        yield value.strip()


def output_contract(prompt: str) -> str:
    return prompt[prompt.rfind("Return") :]


def output_literal_asymmetries(rows):
    findings = set()
    for row in rows:
        vernacular_contract = output_contract(row["vernacular"]).casefold()
        formal_contract = output_contract(row["formal"]).casefold()
        for literal in set(expected_string_leaves(row["expected"])):
            in_vernacular = literal.casefold() in vernacular_contract
            in_formal = literal.casefold() in formal_contract
            if in_vernacular != in_formal:
                side = "vernacular_only" if in_vernacular else "formal_only"
                findings.add((row["id"], literal, side))
    return findings


def main() -> None:
    rows = json.loads(TASKS.read_text())
    assert len(rows) == 28, f"expected 28 tasks, got {len(rows)}"
    assert len({row["id"] for row in rows}) == len(rows), "duplicate task id"
    assert sum(row["split"] == "development" for row in rows) == 8
    assert sum(row["split"] == "held_out" for row in rows) == 20
    assert sum(not row["notation_expected_to_help"] for row in rows if row["split"] == "held_out") == 2
    for row in rows:
        assert set(row) == REQUIRED, f"unexpected fields in {row['id']}"
        assert row["split"] in {"development", "held_out"}
        assert row["vernacular"] != row["formal"]
        assert isinstance(row["expected"], dict) and row["expected"]
        json.dumps(row["expected"], allow_nan=False)
        assert "Return" in row["vernacular"] and "Return" in row["formal"]
    asymmetries = output_literal_asymmetries(rows)
    unexpected = asymmetries - KNOWN_OUTPUT_LITERAL_ASYMMETRIES
    missing = KNOWN_OUTPUT_LITERAL_ASYMMETRIES - asymmetries
    assert not unexpected, f"new asymmetric expected literal in output contract: {sorted(unexpected)}"
    assert not missing, f"documented output-literal asymmetry changed: {sorted(missing)}"
    print(
        f"validated {len(rows)} tasks: 8 development, 20 held-out, "
        "2 held-out negative controls; 2 documented historical output-literal asymmetries"
    )


if __name__ == "__main__":
    main()
