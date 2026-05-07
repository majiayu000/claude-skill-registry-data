#!/usr/bin/env python3
"""Compute coverage and quality statistics for the skill registry archive.

Outputs a small set of high-signal numbers that the README and the upstream
core repo both need:

* Total skills, total categories.
* Top categories by count.
* Field-coverage percentages (description, repo, source, stars, tags,
  license metadata).
* License-class distribution.
* Number of `metadata.json` ↔ `SKILL.md` mismatches and orphan files.

Two output formats are supported: a human-readable table (default) and a
Markdown block suitable for embedding in `README.md`. A `--json` mode is
also available for downstream tooling.

The walker reuses the discovery logic from `validate_metadata.py` so the
two tools agree on what counts as a skill.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent

# Mirror the validator's prune list so the two tools stay in sync.
NON_CATEGORY_DIRS = frozenset({".git", ".github", "schemas", "tools"})

# Fields whose presence (and non-empty value) we want to report on.
TRACKED_FIELDS: tuple[str, ...] = (
    "description",
    "repo",
    "source",
    "source_url",
    "stars",
    "tags",
    "license",
    "license_class",
    "distribution",
    "github_branch",
    "github_path",
    "downloaded_at",
    "author",
)


def is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    if isinstance(value, int):
        return True
    return bool(value)


def discover(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in NON_CATEGORY_DIRS]
        if "metadata.json" in filenames:
            out.append(Path(dirpath) / "metadata.json")
    return out


def collect(root: Path) -> dict[str, Any]:
    files = discover(root)
    total = len(files)
    categories: Counter[str] = Counter()
    field_counts: Counter[str] = Counter()
    license_classes: Counter[str] = Counter()
    distribution_classes: Counter[str] = Counter()
    parse_errors = 0
    missing_skill_md = 0
    orphan_skill_md = 0
    repo_owners: Counter[str] = Counter()

    for meta_path in files:
        try:
            with meta_path.open("r", encoding="utf-8") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError):
            parse_errors += 1
            continue
        if not isinstance(meta, dict):
            parse_errors += 1
            continue

        cat = meta.get("category")
        if isinstance(cat, str) and cat:
            categories[cat] += 1
        for key in TRACKED_FIELDS:
            if is_non_empty(meta.get(key)):
                field_counts[key] += 1

        lc = meta.get("license_class")
        if isinstance(lc, str) and lc:
            license_classes[lc] += 1
        else:
            license_classes["unset"] += 1

        dist = meta.get("distribution")
        if isinstance(dist, str) and dist:
            distribution_classes[dist] += 1
        else:
            distribution_classes["unset"] += 1

        repo_field = meta.get("repo")
        if isinstance(repo_field, str) and "/" in repo_field:
            repo_owners[repo_field.split("/", 1)[0]] += 1

        if not (meta_path.parent / "SKILL.md").exists():
            missing_skill_md += 1

    # Walk again to find SKILL.md files with no metadata.json sibling.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in NON_CATEGORY_DIRS]
        if "SKILL.md" in filenames and "metadata.json" not in filenames:
            orphan_skill_md += 1

    return {
        "total": total,
        "parse_errors": parse_errors,
        "missing_skill_md": missing_skill_md,
        "orphan_skill_md": orphan_skill_md,
        "categories": dict(categories),
        "field_counts": {k: field_counts.get(k, 0) for k in TRACKED_FIELDS},
        "license_classes": dict(license_classes),
        "distribution_classes": dict(distribution_classes),
        "top_repo_owners": dict(repo_owners.most_common(15)),
    }


def pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "n/a"
    return f"{100.0 * numerator / denominator:.1f}%"


def render_text(stats: dict[str, Any], top_categories: int) -> str:
    total = stats["total"]
    out: list[str] = []
    out.append(f"Total skills:              {total}")
    out.append(f"Distinct categories:       {len(stats['categories'])}")
    out.append(f"metadata.json parse errors: {stats['parse_errors']}")
    out.append(f"metadata.json without sibling SKILL.md: {stats['missing_skill_md']}")
    out.append(f"SKILL.md without sibling metadata.json: {stats['orphan_skill_md']}")
    out.append("")
    out.append("Field coverage:")
    for key in TRACKED_FIELDS:
        count = stats["field_counts"][key]
        out.append(f"  {key:18s} {count:>7d}  ({pct(count, total)})")
    out.append("")
    cats = sorted(stats["categories"].items(), key=lambda kv: (-kv[1], kv[0]))
    out.append(f"Top {top_categories} categories:")
    for name, count in cats[:top_categories]:
        out.append(f"  {name:35s} {count:>7d}  ({pct(count, total)})")
    out.append("")
    out.append("License class distribution:")
    for key, count in sorted(
        stats["license_classes"].items(), key=lambda kv: (-kv[1], kv[0])
    ):
        out.append(f"  {key:18s} {count:>7d}  ({pct(count, total)})")
    out.append("")
    out.append("Top contributing owners (by repo field):")
    for owner, count in stats["top_repo_owners"].items():
        out.append(f"  {owner:35s} {count:>7d}")
    return "\n".join(out)


def render_markdown(stats: dict[str, Any], top_categories: int) -> str:
    total = stats["total"]
    lines: list[str] = []
    lines.append("## Registry stats")
    lines.append("")
    lines.append(f"- **Total skills**: {total}")
    lines.append(f"- **Distinct categories**: {len(stats['categories'])}")
    lines.append(f"- **metadata.json parse errors**: {stats['parse_errors']}")
    lines.append(
        f"- **metadata.json without sibling SKILL.md**: {stats['missing_skill_md']}"
    )
    lines.append(
        f"- **SKILL.md without sibling metadata.json**: {stats['orphan_skill_md']}"
    )
    lines.append("")
    lines.append("### Field coverage")
    lines.append("")
    lines.append("| Field | Filled | Coverage |")
    lines.append("|---|---:|---:|")
    for key in TRACKED_FIELDS:
        count = stats["field_counts"][key]
        lines.append(f"| `{key}` | {count} | {pct(count, total)} |")
    lines.append("")
    lines.append(f"### Top {top_categories} categories")
    lines.append("")
    lines.append("| Category | Skills | Share |")
    lines.append("|---|---:|---:|")
    cats = sorted(stats["categories"].items(), key=lambda kv: (-kv[1], kv[0]))
    for name, count in cats[:top_categories]:
        lines.append(f"| `{name}` | {count} | {pct(count, total)} |")
    lines.append("")
    lines.append("### License class distribution")
    lines.append("")
    lines.append("| Class | Skills | Share |")
    lines.append("|---|---:|---:|")
    for key, count in sorted(
        stats["license_classes"].items(), key=lambda kv: (-kv[1], kv[0])
    ):
        lines.append(f"| `{key}` | {count} | {pct(count, total)} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to scan.",
    )
    parser.add_argument(
        "--top-categories",
        type=int,
        default=20,
        help="Number of categories to show in the top-categories table.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
    )
    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Optional path to write the rendered output to. Useful for "
            "embedding generated stats into README via CI."
        ),
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    stats = collect(root)

    if args.format == "json":
        rendered = json.dumps(stats, indent=2, sort_keys=True) + "\n"
    elif args.format == "markdown":
        rendered = render_markdown(stats, args.top_categories)
    else:
        rendered = render_text(stats, args.top_categories) + "\n"

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        sys.stdout.write(rendered)

    return 0


if __name__ == "__main__":
    sys.exit(main())
