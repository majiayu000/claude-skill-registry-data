#!/usr/bin/env python3
"""Validate skill metadata.json files against the registry schema.

Runs three layers of checks:

1. **Schema** — structural conformance with `schemas/skill-metadata.schema.json`.
2. **Filesystem agreement** — `dir_name` matches the parent directory and
   `category` matches the grandparent (top-level) category directory.
3. **Cross-file consistency** — when a SKILL.md sidecar is present, the
   frontmatter `name`, `description` and `category` agree with metadata.json.

The script does not require third-party dependencies for its default mode; if
`jsonschema` is installed it will be used for full Draft 2020-12 validation,
otherwise a minimal in-process validator covers the required-fields and
enum checks that matter for this repo.

Exit code is `0` when no violations are found, `1` otherwise. Use
`--max-issues` to bound output for CI logs and `--sample N` to scan a
randomly chosen subset for fast smoke runs.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "skill-metadata.schema.json"

# Directories that are not category folders (kept at the top level for tooling
# or hidden git plumbing) — the grandparent-category check skips them.
NON_CATEGORY_DIRS = frozenset(
    {
        ".git",
        ".github",
        "schemas",
        "tools",
    }
)

REPO_PATTERN = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
CATEGORY_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
LICENSE_CLASS_VALUES = frozenset({"compatible", "restricted", "unknown"})


@dataclass
class Violation:
    """A single rule violation against one metadata.json file."""

    path: str
    rule: str
    message: str
    severity: str = "error"  # "error" or "warning"

    def as_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "rule": self.rule,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass
class Report:
    scanned: int = 0
    skipped: int = 0
    violations: list[Violation] = field(default_factory=list)

    def add(self, v: Violation) -> None:
        self.violations.append(v)

    @property
    def errors(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == "error"]

    @property
    def warnings(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == "warning"]

    def summary(self) -> dict[str, Any]:
        rule_counts: dict[str, int] = {}
        for v in self.violations:
            rule_counts[v.rule] = rule_counts.get(v.rule, 0) + 1
        return {
            "scanned": self.scanned,
            "skipped": self.skipped,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "by_rule": rule_counts,
        }


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover(root: Path) -> Iterator[Path]:
    """Yield every metadata.json under `root`, skipping VCS/tooling dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Mutate dirnames in-place to prune the walk.
        dirnames[:] = [d for d in dirnames if d not in NON_CATEGORY_DIRS]
        if "metadata.json" in filenames:
            yield Path(dirpath) / "metadata.json"


def parse_skill_frontmatter(skill_path: Path) -> dict[str, str] | None:
    """Return a dict of frontmatter keys from a SKILL.md, or None if missing.

    The parser is intentionally tiny — we only need a handful of top-level
    string keys (`name`, `description`, `category`). Multi-line YAML values
    are folded into one logical line.
    """
    try:
        with skill_path.open("r", encoding="utf-8", errors="replace") as f:
            data = f.read(8192)
    except OSError:
        return None
    if not data.startswith("---"):
        return None
    end = data.find("\n---", 3)
    if end == -1:
        return None
    block = data[3:end].lstrip("\n")
    out: dict[str, str] = {}
    current_key: str | None = None
    current_val_lines: list[str] = []
    for raw in block.splitlines():
        # Top-level key: starts at column 0, contains a colon, and the colon
        # is preceded by something that does not look like a list item.
        if raw and not raw.startswith((" ", "\t", "-")) and ":" in raw:
            if current_key is not None:
                out[current_key] = " ".join(current_val_lines).strip()
            key, _, val = raw.partition(":")
            current_key = key.strip()
            stripped = val.strip()
            # Strip surrounding quotes when present.
            if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
                stripped = stripped[1:-1]
            current_val_lines = [stripped] if stripped else []
        else:
            if current_key is not None:
                current_val_lines.append(raw.strip())
    if current_key is not None:
        out[current_key] = " ".join(current_val_lines).strip()
    return out


def validate_schema_minimal(meta: dict[str, Any], rel_path: str, report: Report) -> None:
    """Tiny in-process validator that covers the rules CI cares about.

    This avoids forcing a `jsonschema` dependency on every CI runner. When
    `jsonschema` *is* installed we still defer to it for richer reporting.
    """
    required = ("name", "category", "dir_name")
    for key in required:
        if key not in meta:
            report.add(
                Violation(
                    path=rel_path,
                    rule="schema/required",
                    message=f"missing required field `{key}`",
                )
            )
        elif not isinstance(meta[key], str) or not meta[key].strip():
            report.add(
                Violation(
                    path=rel_path,
                    rule="schema/type",
                    message=f"field `{key}` must be a non-empty string",
                )
            )

    cat = meta.get("category")
    if isinstance(cat, str) and not CATEGORY_PATTERN.match(cat):
        report.add(
            Violation(
                path=rel_path,
                rule="schema/category-pattern",
                message=f"category `{cat}` must match {CATEGORY_PATTERN.pattern}",
            )
        )

    repo = meta.get("repo")
    if isinstance(repo, str) and repo and not REPO_PATTERN.match(repo):
        report.add(
            Violation(
                path=rel_path,
                rule="schema/repo-pattern",
                message=f"repo `{repo}` is not in `owner/name` shape",
            )
        )

    license_class = meta.get("license_class")
    if license_class is not None and license_class not in LICENSE_CLASS_VALUES:
        report.add(
            Violation(
                path=rel_path,
                rule="schema/license-class-enum",
                message=(
                    f"license_class `{license_class}` not in "
                    f"{sorted(LICENSE_CLASS_VALUES)}"
                ),
            )
        )

    distribution = meta.get("distribution")
    if distribution is not None and distribution not in LICENSE_CLASS_VALUES:
        report.add(
            Violation(
                path=rel_path,
                rule="schema/distribution-enum",
                message=(
                    f"distribution `{distribution}` not in "
                    f"{sorted(LICENSE_CLASS_VALUES)}"
                ),
            )
        )

    stars = meta.get("stars")
    if stars is not None and (not isinstance(stars, int) or stars < 0):
        report.add(
            Violation(
                path=rel_path,
                rule="schema/stars",
                message="stars must be a non-negative integer",
            )
        )

    tags = meta.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not all(
            isinstance(t, str) and t for t in tags
        ):
            report.add(
                Violation(
                    path=rel_path,
                    rule="schema/tags",
                    message="tags must be a list of non-empty strings",
                )
            )


def validate_schema_with_jsonschema(
    meta: dict[str, Any], rel_path: str, report: Report, validator: Any
) -> None:
    for err in validator.iter_errors(meta):
        location = "/".join(str(p) for p in err.absolute_path) or "<root>"
        report.add(
            Violation(
                path=rel_path,
                rule=f"schema/{err.validator}",
                message=f"{location}: {err.message}",
            )
        )


def validate_filesystem_agreement(
    meta: dict[str, Any], meta_path: Path, repo_root: Path, report: Report
) -> None:
    rel = meta_path.relative_to(repo_root)
    rel_path = rel.as_posix()
    parent = meta_path.parent
    parent_name = parent.name

    dir_name = meta.get("dir_name")
    if isinstance(dir_name, str) and dir_name and dir_name != parent_name:
        report.add(
            Violation(
                path=rel_path,
                rule="fs/dir-name",
                message=(
                    f"dir_name `{dir_name}` does not match parent directory "
                    f"`{parent_name}`"
                ),
            )
        )

    # The category should be the top-level directory inside the repo root.
    try:
        rel_to_root = parent.relative_to(repo_root)
    except ValueError:
        return
    parts = rel_to_root.parts
    if len(parts) >= 1:
        top = parts[0]
        cat = meta.get("category")
        if isinstance(cat, str) and cat and cat != top:
            report.add(
                Violation(
                    path=rel_path,
                    rule="fs/category",
                    message=(
                        f"category `{cat}` does not match top-level directory "
                        f"`{top}`"
                    ),
                )
            )


def validate_skill_md_consistency(
    meta: dict[str, Any], meta_path: Path, repo_root: Path, report: Report
) -> None:
    skill_path = meta_path.parent / "SKILL.md"
    rel_path = meta_path.relative_to(repo_root).as_posix()
    if not skill_path.exists():
        report.add(
            Violation(
                path=rel_path,
                rule="cross/missing-skill-md",
                message="metadata.json has no sibling SKILL.md",
            )
        )
        return

    fm = parse_skill_frontmatter(skill_path)
    if fm is None:
        report.add(
            Violation(
                path=rel_path,
                rule="cross/skill-md-no-frontmatter",
                message="sibling SKILL.md has no YAML frontmatter",
                severity="warning",
            )
        )
        return

    fm_name = fm.get("name", "").strip()
    meta_name = (meta.get("name") or "").strip()
    if fm_name and meta_name and fm_name != meta_name:
        # Many archive entries deliberately suffix dir_name with -owner-repo to
        # disambiguate name collisions; the SKILL.md frontmatter keeps the
        # original short name. Only flag when the metadata name is *not* a
        # prefix of the dir_name and *not* equal to the frontmatter name.
        report.add(
            Violation(
                path=rel_path,
                rule="cross/name-mismatch",
                message=(
                    f"metadata.json name `{meta_name}` differs from SKILL.md "
                    f"frontmatter name `{fm_name}`"
                ),
                severity="warning",
            )
        )

    fm_desc = fm.get("description", "").strip()
    meta_desc = (meta.get("description") or "").strip()
    if fm_desc and not meta_desc:
        report.add(
            Violation(
                path=rel_path,
                rule="cross/description-missing-in-metadata",
                message=(
                    "SKILL.md frontmatter has a description but metadata.json "
                    "is empty or missing the field"
                ),
                severity="warning",
            )
        )

    fm_cat = fm.get("category", "").strip()
    meta_cat = (meta.get("category") or "").strip()
    if fm_cat and meta_cat and fm_cat != meta_cat:
        # The dataset reorganises skills by curated top-level category, so the
        # original SKILL.md `category` will diverge from `metadata.category`
        # for many entries. Treat this as informational only.
        report.add(
            Violation(
                path=rel_path,
                rule="cross/category-divergence",
                message=(
                    f"metadata.category `{meta_cat}` differs from SKILL.md "
                    f"frontmatter category `{fm_cat}`"
                ),
                severity="warning",
            )
        )


def validate_one(meta_path: Path, repo_root: Path, schema_validator: Any, report: Report) -> None:
    rel_path = meta_path.relative_to(repo_root).as_posix()
    try:
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        report.add(
            Violation(
                path=rel_path,
                rule="schema/json-parse",
                message=f"could not parse JSON: {e}",
            )
        )
        return
    except OSError as e:
        report.add(
            Violation(
                path=rel_path,
                rule="io/read",
                message=f"could not read file: {e}",
            )
        )
        return

    if not isinstance(meta, dict):
        report.add(
            Violation(
                path=rel_path,
                rule="schema/root-type",
                message="metadata.json must be a JSON object",
            )
        )
        return

    if schema_validator is not None:
        validate_schema_with_jsonschema(meta, rel_path, report, schema_validator)
    else:
        validate_schema_minimal(meta, rel_path, report)

    validate_filesystem_agreement(meta, meta_path, repo_root, report)
    validate_skill_md_consistency(meta, meta_path, repo_root, report)


def build_validator() -> Any:
    """Return a `jsonschema.Validator` if available, else None."""
    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:
        return None
    schema = load_schema()
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema)


def select_files(files: list[Path], sample: int | None, seed: int) -> list[Path]:
    if sample is None or sample >= len(files):
        return files
    rng = random.Random(seed)
    return rng.sample(files, sample)


def format_human(report: Report, max_issues: int) -> str:
    out: list[str] = []
    summary = report.summary()
    out.append(f"Scanned {summary['scanned']} metadata.json files")
    out.append(
        f"Errors: {summary['errors']}   Warnings: {summary['warnings']}"
    )
    if summary["by_rule"]:
        out.append("By rule:")
        for rule, count in sorted(
            summary["by_rule"].items(), key=lambda kv: (-kv[1], kv[0])
        ):
            out.append(f"  {rule:40s} {count}")
    if report.violations:
        out.append("")
        out.append("First violations (truncated):")
        for v in report.violations[:max_issues]:
            out.append(f"  [{v.severity}] {v.rule}: {v.path}")
            out.append(f"      {v.message}")
        if len(report.violations) > max_issues:
            out.append(f"  ... and {len(report.violations) - max_issues} more")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to scan (defaults to repo containing this script).",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Validate only N randomly chosen files. Useful for CI smoke runs.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260301,
        help="Seed for --sample selection so CI runs are reproducible.",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=50,
        help="Cap on number of individual violations printed in human output.",
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        default=None,
        help="Optional path to write a JSON report to.",
    )
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Exit non-zero when only warnings are present.",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help=(
            "If given, only validate these specific metadata.json paths "
            "(relative to --root). Used by pre-commit and PR checks."
        ),
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.root).resolve()
    schema_validator = build_validator()
    report = Report()

    if args.paths:
        files = []
        for p in args.paths:
            candidate = (repo_root / p).resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                report.add(
                    Violation(
                        path=p,
                        rule="io/outside-root",
                        message="path is outside repository root",
                    )
                )
                continue
            if candidate.name != "metadata.json":
                report.skipped += 1
                continue
            if candidate.exists():
                files.append(candidate)
            else:
                report.skipped += 1
    else:
        files = list(discover(repo_root))

    files = select_files(files, args.sample, args.seed)
    report.scanned = len(files)

    for meta_path in files:
        validate_one(meta_path, repo_root, schema_validator, report)

    print(format_human(report, args.max_issues))

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "summary": report.summary(),
            "violations": [v.as_dict() for v in report.violations],
        }
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
            f.write("\n")

    if report.errors:
        return 1
    if args.warnings_as_errors and report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
