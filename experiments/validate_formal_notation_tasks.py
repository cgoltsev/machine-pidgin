#!/usr/bin/env python3
"""Static integrity checks for Benchmark 002 before any model call."""

from __future__ import annotations

import json
from pathlib import Path

TASKS = Path(__file__).with_name("formal_notation_tasks.json")
REQUIRED = {"id", "split", "category", "notation_expected_to_help", "vernacular", "formal", "expected"}


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
    print(f"validated {len(rows)} tasks: 8 development, 20 held-out, 2 held-out negative controls")


if __name__ == "__main__":
    main()
