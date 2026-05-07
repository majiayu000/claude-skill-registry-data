"""Tests for tools/repo_stats.py.

Run with `python3 -m unittest tools.test_repo_stats`.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_stats as rs  # noqa: E402

from test_validate_metadata import write_skill  # noqa: E402


class StatsCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="skill-registry-stats-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestCollect(StatsCase):
    def test_counts_skills_and_categories(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        write_skill(self.tmp, "core", "beta")
        write_skill(self.tmp, "design", "gamma")
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["categories"], {"core": 2, "design": 1})

    def test_field_coverage_is_computed(self) -> None:
        write_skill(self.tmp, "core", "alpha")  # has description
        write_skill(self.tmp, "core", "beta", metadata={"description": ""})
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["field_counts"]["description"], 1)
        self.assertEqual(stats["field_counts"]["repo"], 2)

    def test_license_distribution(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"license_class": "compatible", "distribution": "compatible"},
        )
        write_skill(
            self.tmp,
            "core",
            "beta",
            metadata={"license_class": "restricted", "distribution": "restricted"},
        )
        write_skill(self.tmp, "core", "no-license")  # no license_class field
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["license_classes"]["compatible"], 1)
        self.assertEqual(stats["license_classes"]["restricted"], 1)
        self.assertEqual(stats["license_classes"]["unset"], 1)

    def test_orphan_skill_md_detected(self) -> None:
        # SKILL.md without metadata.json sibling.
        orphan_dir = self.tmp / "core" / "orphan"
        orphan_dir.mkdir(parents=True)
        (orphan_dir / "SKILL.md").write_text("---\nname: orphan\n---\n", encoding="utf-8")
        write_skill(self.tmp, "core", "alpha")
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["orphan_skill_md"], 1)
        self.assertEqual(stats["total"], 1)

    def test_top_repo_owners(self) -> None:
        write_skill(self.tmp, "core", "alpha", metadata={"repo": "alice/one"})
        write_skill(self.tmp, "core", "beta", metadata={"repo": "alice/two"})
        write_skill(self.tmp, "core", "gamma", metadata={"repo": "bob/one"})
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["top_repo_owners"]["alice"], 2)
        self.assertEqual(stats["top_repo_owners"]["bob"], 1)

    def test_corrupt_metadata_counted_as_parse_error(self) -> None:
        skill_dir = self.tmp / "core" / "broken"
        skill_dir.mkdir(parents=True)
        (skill_dir / "metadata.json").write_text("{not json", encoding="utf-8")
        write_skill(self.tmp, "core", "alpha")
        stats = rs.collect(self.tmp)
        self.assertEqual(stats["parse_errors"], 1)
        self.assertEqual(stats["total"], 2)


class TestRendering(StatsCase):
    def test_text_render_includes_total_line(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        stats = rs.collect(self.tmp)
        text = rs.render_text(stats, top_categories=5)
        self.assertIn("Total skills:", text)
        self.assertIn("Field coverage:", text)

    def test_markdown_render_has_table_headers(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        stats = rs.collect(self.tmp)
        md = rs.render_markdown(stats, top_categories=5)
        self.assertIn("| Field | Filled | Coverage |", md)
        self.assertIn("| Category | Skills | Share |", md)

    def test_pct_handles_zero_denominator(self) -> None:
        self.assertEqual(rs.pct(0, 0), "n/a")
        self.assertEqual(rs.pct(1, 4), "25.0%")


if __name__ == "__main__":
    unittest.main()
