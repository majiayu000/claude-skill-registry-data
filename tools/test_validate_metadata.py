"""Tests for tools/validate_metadata.py.

Run with `python3 -m unittest tools.test_validate_metadata`.

The tests construct a tiny synthetic registry inside a temporary directory
so they neither depend on nor mutate the real archive.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_metadata as vm  # noqa: E402


def write_skill(
    root: Path,
    category: str,
    dir_name: str,
    *,
    metadata: dict | None = None,
    skill_md_frontmatter: dict | None = None,
    skill_md_body: str = "# body\n",
    write_skill_md: bool = True,
) -> Path:
    """Create a `category/dir_name/{metadata.json,SKILL.md}` skill on disk."""
    skill_dir = root / category / dir_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "name": dir_name,
        "category": category,
        "dir_name": dir_name,
        "description": f"description for {dir_name}",
        "repo": "owner/example",
    }
    if metadata is not None:
        meta.update(metadata)

    with (skill_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    if write_skill_md:
        fm = {
            "name": meta["name"],
            "description": meta.get("description", ""),
            "category": meta["category"],
        }
        if skill_md_frontmatter is not None:
            fm.update(skill_md_frontmatter)
        lines = ["---"]
        for key, value in fm.items():
            lines.append(f"{key}: {value}")
        lines.append("---")
        text = "\n".join(lines) + "\n" + skill_md_body
        with (skill_dir / "SKILL.md").open("w", encoding="utf-8") as f:
            f.write(text)

    return skill_dir


class FixtureCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="skill-registry-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestFrontmatterParser(FixtureCase):
    def test_parses_simple_frontmatter(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        fm = vm.parse_skill_frontmatter(self.tmp / "core" / "alpha" / "SKILL.md")
        self.assertIsNotNone(fm)
        assert fm is not None
        self.assertEqual(fm["name"], "alpha")
        self.assertEqual(fm["category"], "core")

    def test_quoted_values_are_stripped(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "beta",
            skill_md_frontmatter={"description": '"a quoted description"'},
        )
        fm = vm.parse_skill_frontmatter(self.tmp / "core" / "beta" / "SKILL.md")
        assert fm is not None
        self.assertEqual(fm["description"], "a quoted description")

    def test_returns_none_when_no_frontmatter(self) -> None:
        skill_dir = self.tmp / "core" / "noyaml"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("just plain text\n", encoding="utf-8")
        self.assertIsNone(vm.parse_skill_frontmatter(skill_dir / "SKILL.md"))


class TestSchemaValidation(FixtureCase):
    def test_clean_skill_passes(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        report = vm.Report()
        validator = vm.build_validator()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, validator, report)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_missing_required_field_is_error(self) -> None:
        write_skill(self.tmp, "core", "alpha", metadata={"name": ""})
        report = vm.Report()
        validator = vm.build_validator()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, validator, report)
        self.assertTrue(any(v.rule.startswith("schema/") for v in report.errors))

    def test_bad_repo_pattern_is_error(self) -> None:
        write_skill(self.tmp, "core", "alpha", metadata={"repo": "not-a-repo"})
        report = vm.Report()
        # Use the minimal validator path so this test does not depend on
        # whether jsonschema is installed in CI.
        validator = None
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, validator, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("schema/repo-pattern", rules)

    def test_bad_license_class_is_error(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"license_class": "weird"},
        )
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("schema/license-class-enum", rules)

    def test_negative_stars_is_error(self) -> None:
        write_skill(self.tmp, "core", "alpha", metadata={"stars": -1})
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("schema/stars", rules)

    def test_corrupt_json_is_error(self) -> None:
        skill_dir = self.tmp / "core" / "broken"
        skill_dir.mkdir(parents=True)
        (skill_dir / "metadata.json").write_text("{not json", encoding="utf-8")
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        self.assertTrue(any(v.rule == "schema/json-parse" for v in report.errors))


class TestFilesystemAgreement(FixtureCase):
    def test_dir_name_mismatch_is_flagged(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"dir_name": "different"},
        )
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("fs/dir-name", rules)

    def test_category_mismatch_is_flagged(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"category": "elsewhere"},
        )
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("fs/category", rules)


class TestCrossFileChecks(FixtureCase):
    def test_missing_skill_md_is_error(self) -> None:
        skill_dir = self.tmp / "core" / "alpha"
        skill_dir.mkdir(parents=True)
        meta = {
            "name": "alpha",
            "category": "core",
            "dir_name": "alpha",
            "description": "x",
        }
        with (skill_dir / "metadata.json").open("w", encoding="utf-8") as f:
            json.dump(meta, f)
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.errors}
        self.assertIn("cross/missing-skill-md", rules)

    def test_description_only_in_skill_md_is_warning(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"description": ""},
            skill_md_frontmatter={"description": "rich description"},
        )
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        rules = {v.rule for v in report.warnings}
        self.assertIn("cross/description-missing-in-metadata", rules)
        self.assertEqual(report.errors, [])

    def test_name_mismatch_is_warning_not_error(self) -> None:
        write_skill(
            self.tmp,
            "core",
            "alpha",
            metadata={"name": "alpha-suffix"},
            skill_md_frontmatter={"name": "alpha"},
        )
        report = vm.Report()
        for meta_path in vm.discover(self.tmp):
            vm.validate_one(meta_path, self.tmp, None, report)
        warning_rules = {v.rule for v in report.warnings}
        self.assertIn("cross/name-mismatch", warning_rules)
        self.assertEqual(report.errors, [])


class TestSampling(unittest.TestCase):
    def test_sample_returns_all_when_n_is_large(self) -> None:
        files = [Path(f"x{i}") for i in range(5)]
        self.assertEqual(vm.select_files(files, 100, seed=1), files)

    def test_sample_is_deterministic_for_same_seed(self) -> None:
        files = [Path(f"x{i}") for i in range(20)]
        a = vm.select_files(files, 5, seed=42)
        b = vm.select_files(files, 5, seed=42)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 5)


class TestPathFiltering(FixtureCase):
    def test_paths_argument_only_validates_listed_files(self) -> None:
        write_skill(self.tmp, "core", "alpha")
        write_skill(
            self.tmp,
            "core",
            "broken",
            metadata={"name": ""},  # would be an error under full scan
        )
        rc = vm.main(
            [
                "--root",
                str(self.tmp),
                "--paths",
                "core/alpha/metadata.json",
            ]
        )
        # Only the clean file was validated, so exit code is 0.
        self.assertEqual(rc, 0)

    def test_paths_outside_root_are_rejected(self) -> None:
        rc = vm.main(
            [
                "--root",
                str(self.tmp),
                "--paths",
                "/etc/passwd",
            ]
        )
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
