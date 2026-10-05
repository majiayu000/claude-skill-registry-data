---
name: release-notes-writer
description: Generates professional release notes from git history, pull requests, and issues with conventional commit parsing and audience-specific formatting. Use when.
---

# Release Notes Writer

Specialized skill for generating clear, well-structured release notes from repository history. This skill parses conventional commits, categorizes pull requests, highlights breaking changes, and formats the output for different audiences (end users, developers, internal stakeholders). It produces both human-readable release notes and machine-parseable changelogs, and includes automation scripts that can be integrated into CI/CD pipelines for fully automated release documentation.

## When to Use This Skill

Use this skill for:

- Generating release notes for a new version from git history and merged PRs
- Creating changelogs that follow the Keep a Changelog format
- Parsing conventional commits to automatically categorize changes
- Highlighting breaking changes and migration instructions for consumers
- Producing audience-specific release notes (user-facing versus internal/developer)
- Automating release note generation as part of a CI/CD pipeline
- Summarizing changes across multiple repositories for a platform release
- Formatting release notes for GitHub Releases, GitLab Releases, or documentation sites

**Trigger phrases**: "release notes", "changelog", "version notes", "what changed", "write release notes", "generate changelog", "release summary", "breaking changes", "version history", "release documentation"

## What This Skill Does

This skill follows a structured methodology to produce release notes:

1. **History Collection**: Gathers all commits, merged pull requests, and linked issues between two git references (tags, branches, or SHAs).

2. **Conventional Commit Parsing**: Parses commit messages following the Conventional Commits specification to extract type (feat, fix, chore, etc.), scope, description, breaking change markers, and issue references.

3. **PR Categorization**: Groups pull requests by label, conventional commit type, or directory path into user-meaningful categories (Features, Bug Fixes, Performance, Documentation, Internal).

4. **Breaking Change Detection**: Identifies breaking changes from commit footers (`BREAKING CHANGE:`), PR labels (`breaking-change`), and major version bumps in dependency updates.

5. **Audience Filtering**: Separates user-facing changes from internal changes. End users see features and bug fixes; developers see API changes and deprecations; internal stakeholders see all changes with contributor attribution.

6. **Output Generation**: Produces formatted release notes in Markdown (for GitHub/GitLab Releases), plain text (for email), or structured data (JSON/YAML for further processing).

## Instructions

### Step 1: Collect Change History

Gather all changes between two references (typically the previous release tag and the current HEAD or new tag).

**Git Log Collection Script** (`scripts/collect-changes.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

FROM_REF="${1:?Usage: collect-changes.sh <from_ref> <to_ref>}"
TO_REF="${2:-HEAD}"
OUTPUT="${3:-changes.json}"

echo "Collecting changes from $FROM_REF to $TO_REF"

# Collect commits with structured output
git log "${FROM_REF}..${TO_REF}" \
  --pretty=format:'{%n  "hash": "%H",%n  "short_hash": "%h",%n  "author": "%an",%n  "email": "%ae",%n  "date": "%aI",%n  "subject": "%s",%n  "body": "%b"%n},' \
  > /tmp/commits_raw.txt

# Wrap in JSON array (remove trailing comma, add brackets)
echo "[" > "$OUTPUT"
sed '$ s/,$//' /tmp/commits_raw.txt >> "$OUTPUT"
echo "]" >> "$OUTPUT"

COMMIT_COUNT=$(git rev-list --count "${FROM_REF}..${TO_REF}")
echo "Collected $COMMIT_COUNT commits -> $OUTPUT"

# Collect merge commits (PRs) separately
echo ""
echo "Merge commits (PRs):"
git log "${FROM_REF}..${TO_REF}" --merges --oneline
```

**GitHub PR Collection** (using `gh` CLI):

```bash
#!/usr/bin/env bash
set -euo pipefail

FROM_DATE="${1:?Usage: collect-prs.sh <from_date> <to_date>}"
TO_DATE="${2:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
OUTPUT="${3:-prs.json}"

echo "Collecting merged PRs from $FROM_DATE to $TO_DATE"

gh pr list \
  --state merged \
  --search "merged:${FROM_DATE}..${TO_DATE}" \
  --json number,title,labels,author,body,mergedAt,headRefName \
  --limit 500 \
  > "$OUTPUT"

PR_COUNT=$(jq length "$OUTPUT")
echo "Collected $PR_COUNT merged PRs -> $OUTPUT"
```

### Step 2: Parse Conventional Commits

Conventional Commits follow the pattern: `type(scope): description`

**Python Parser** (`scripts/parse_commits.py`):

```python
"""Parse conventional commits into structured release note data."""
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


CONVENTIONAL_PATTERN = re.compile(
    r"^(?P<type>\w+)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s*"
    r"(?P<description>.+)$"
)

BREAKING_CHANGE_PATTERN = re.compile(
    r"^BREAKING[ -]CHANGE:\s*(?P<description>.+)",
    re.MULTILINE,
)

ISSUE_REF_PATTERN = re.compile(
    r"(?:closes?|fixes?|resolves?)\s+#(\d+)",
    re.IGNORECASE,
)

# Map conventional commit types to release note categories
TYPE_CATEGORY_MAP = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "docs": "Documentation",
    "refactor": "Internal Changes",
    "test": "Internal Changes",
    "chore": "Internal Changes",
    "build": "Build System",
    "ci": "CI/CD",
    "style": "Internal Changes",
    "revert": "Reverts",
}


@dataclass
class ParsedCommit:
    hash: str
    short_hash: str
    author: str
    date: str
    type: str = "other"
    scope: Optional[str] = None
    description: str = ""
    body: str = ""
    breaking: bool = False
    breaking_description: str = ""
    category: str = "Other"
    issues: list = field(default_factory=list)
    is_conventional: bool = False


def parse_commit(commit: dict) -> ParsedCommit:
    """Parse a single commit into structured data."""
    subject = commit.get("subject", "")
    body = commit.get("body", "")

    parsed = ParsedCommit(
        hash=commit["hash"],
        short_hash=commit["short_hash"],
        author=commit["author"],
        date=commit["date"],
        body=body,
    )

    match = CONVENTIONAL_PATTERN.match(subject)
    if match:
        parsed.is_conventional = True
        parsed.type = match.group("type")
        parsed.scope = match.group("scope")
        parsed.description = match.group("description")
        parsed.breaking = match.group("breaking") is not None
        parsed.category = TYPE_CATEGORY_MAP.get(parsed.type, "Other")
    else:
        parsed.description = subject

    # Check body for breaking change footer
    breaking_match = BREAKING_CHANGE_PATTERN.search(body)
    if breaking_match:
        parsed.breaking = True
        parsed.breaking_description = breaking_match.group("description").strip()

    # Extract issue references
    parsed.issues = ISSUE_REF_PATTERN.findall(subject + " " + body)

    return parsed


def parse_all(input_path: str) -> list[ParsedCommit]:
    """Parse all commits from a JSON file."""
    with open(input_path) as f:
        commits = json.load(f)

    return [parse_commit(c) for c in commits]


def group_by_category(commits: list[ParsedCommit]) -> dict[str, list[ParsedCommit]]:
    """Group parsed commits by their release note category."""
    groups: dict[str, list[ParsedCommit]] = {}
    for commit in commits:
        groups.setdefault(commit.category, []).append(commit)
    return groups


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "changes.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "parsed_commits.json"

    commits = parse_all(input_file)
    grouped = group_by_category(commits)

    output = {
        "total_commits": len(commits),
        "conventional_commits": sum(1 for c in commits if c.is_conventional),
        "breaking_changes": [asdict(c) for c in commits if c.breaking],
        "categories": {
            cat: [asdict(c) for c in items]
            for cat, items in grouped.items()
        },
    }

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Parsed {len(commits)} commits ({output['conventional_commits']} conventional)")
    print(f"Breaking changes: {len(output['breaking_changes'])}")
    print(f"Categories: {', '.join(grouped.keys())}")
    print(f"Output: {output_file}")
```

### Step 3: Categorize Pull Requests

When conventional commits are not used consistently, fall back to PR labels and file paths for categorization.

**PR Categorization Script** (`scripts/categorize_prs.py`):

```python
"""Categorize pull requests by labels, title patterns, and file paths."""
import json
import re
import sys
from typing import Optional


# Label-to-category mapping (checked first)
LABEL_CATEGORY_MAP = {
    "feature": "Features",
    "enhancement": "Features",
    "bug": "Bug Fixes",
    "bugfix": "Bug Fixes",
    "fix": "Bug Fixes",
    "performance": "Performance",
    "perf": "Performance",
    "documentation": "Documentation",
    "docs": "Documentation",
    "security": "Security",
    "breaking-change": "Breaking Changes",
    "breaking": "Breaking Changes",
    "dependencies": "Dependencies",
    "deps": "Dependencies",
    "internal": "Internal Changes",
    "chore": "Internal Changes",
    "ci": "CI/CD",
}

# File path patterns for fallback categorization
PATH_CATEGORY_MAP = [
    (r"^docs/", "Documentation"),
    (r"^\.github/", "CI/CD"),
    (r"^\.gitlab-ci", "CI/CD"),
    (r"^Jenkinsfile", "CI/CD"),
    (r"^tests?/", "Internal Changes"),
    (r"^benchmark", "Performance"),
]

# Title patterns for fallback categorization
TITLE_CATEGORY_MAP = [
    (r"^feat(\(.+\))?:", "Features"),
    (r"^fix(\(.+\))?:", "Bug Fixes"),
    (r"^perf(\(.+\))?:", "Performance"),
    (r"^docs(\(.+\))?:", "Documentation"),
    (r"^chore(\(.+\))?:", "Internal Changes"),
    (r"^ci(\(.+\))?:", "CI/CD"),
    (r"^refactor(\(.+\))?:", "Internal Changes"),
]


def categorize_pr(pr: dict) -> str:
    """Determine the category for a single PR."""
    labels = [label.get("name", "").lower() for label in pr.get("labels", [])]

    # Check labels first (highest priority)
    for label in labels:
        if label in LABEL_CATEGORY_MAP:
            return LABEL_CATEGORY_MAP[label]

    # Check title patterns
    title = pr.get("title", "")
    for pattern, category in TITLE_CATEGORY_MAP:
        if re.match(pattern, title, re.IGNORECASE):
            return category

    # Default category
    return "Other"


def is_breaking(pr: dict) -> bool:
    """Check if a PR contains breaking changes."""
    labels = [label.get("name", "").lower() for label in pr.get("labels", [])]
    if "breaking-change" in labels or "breaking" in labels:
        return True

    title = pr.get("title", "")
    if "!" in title.split(":")[0] if ":" in title else False:
        return True

    body = pr.get("body", "") or ""
    if "BREAKING CHANGE" in body:
        return True

    return False


def categorize_all(input_path: str, output_path: str):
    """Categorize all PRs and write grouped output."""
    with open(input_path) as f:
        prs = json.load(f)

    categorized = {}
    breaking = []

    for pr in prs:
        category = categorize_pr(pr)
        entry = {
            "number": pr["number"],
            "title": pr["title"],
            "author": pr.get("author", {}).get("login", "unknown"),
            "merged_at": pr.get("mergedAt", ""),
            "category": category,
            "breaking": is_breaking(pr),
        }

        categorized.setdefault(category, []).append(entry)
        if entry["breaking"]:
            breaking.append(entry)

    output = {
        "total_prs": len(prs),
        "breaking_changes": breaking,
        "categories": categorized,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Categorized {len(prs)} PRs")
    for cat, items in categorized.items():
        print(f"  {cat}: {len(items)}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "prs.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "categorized_prs.json"
    categorize_all(input_file, output_file)
```

### Step 4: Generate Formatted Release Notes

**Release Notes Generator** (`scripts/generate_release_notes.py`):

```python
"""Generate formatted release notes from categorized changes."""
import json
import sys
from datetime import datetime, timezone
from typing import Optional


# Category display order (user-facing categories first)
CATEGORY_ORDER = [
    "Breaking Changes",
    "Features",
    "Bug Fixes",
    "Performance",
    "Security",
    "Documentation",
    "Dependencies",
    "CI/CD",
    "Build System",
    "Internal Changes",
    "Reverts",
    "Other",
]


def generate_markdown(
    parsed_data: dict,
    version: str,
    date: Optional[str] = None,
    repo_url: Optional[str] = None,
    audience: str = "all",
) -> str:
    """Generate Markdown release notes.

    Args:
        parsed_data: Output from parse_commits.py or categorize_prs.py.
        version: Version string (e.g., "v2.5.0").
        date: Release date (defaults to today).
        repo_url: Repository URL for linking commits and PRs.
        audience: "user" (features/fixes only), "developer" (all technical),
                  or "all" (everything).
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# {version}")
    lines.append("")
    lines.append(f"**Release Date**: {date}")
    lines.append("")

    # Breaking changes section (always first if present)
    breaking = parsed_data.get("breaking_changes", [])
    if breaking:
        lines.append("## Breaking Changes")
        lines.append("")
        for change in breaking:
            desc = change.get("description", change.get("title", ""))
            breaking_detail = change.get("breaking_description", "")
            if "number" in change:
                if repo_url:
                    lines.append(f"- {desc} ([#{change['number']}]({repo_url}/pull/{change['number']}))")
                else:
                    lines.append(f"- {desc} (#{change['number']})")
            else:
                short_hash = change.get("short_hash", "")
                if repo_url and short_hash:
                    lines.append(f"- {desc} ([{short_hash}]({repo_url}/commit/{change.get('hash', '')}))")
                else:
                    lines.append(f"- {desc}")
            if breaking_detail:
                lines.append(f"  - Migration: {breaking_detail}")
        lines.append("")

    # Filter categories by audience
    user_categories = {"Features", "Bug Fixes", "Performance", "Security"}
    developer_categories = user_categories | {"Documentation", "Dependencies", "CI/CD", "Build System", "Reverts"}
    all_categories = developer_categories | {"Internal Changes", "Other"}

    if audience == "user":
        visible_categories = user_categories
    elif audience == "developer":
        visible_categories = developer_categories
    else:
        visible_categories = all_categories

    # Render each category
    categories = parsed_data.get("categories", {})
    for category in CATEGORY_ORDER:
        if category == "Breaking Changes":
            continue  # Already rendered above
        if category not in categories:
            continue
        if category not in visible_categories:
            continue

        items = categories[category]
        if not items:
            continue

        lines.append(f"## {category}")
        lines.append("")

        for item in items:
            desc = item.get("description", item.get("title", ""))
            scope = item.get("scope")
            author = item.get("author", "")

            prefix = f"**{scope}**: " if scope else ""

            if "number" in item:
                # PR-based entry
                ref = f"#{item['number']}"
                if repo_url:
                    ref = f"[#{item['number']}]({repo_url}/pull/{item['number']})"
                attribution = f" (@{author})" if author else ""
                lines.append(f"- {prefix}{desc} ({ref}){attribution}")
            else:
                # Commit-based entry
                short_hash = item.get("short_hash", "")
                if repo_url and short_hash:
                    ref = f"[{short_hash}]({repo_url}/commit/{item.get('hash', '')})"
                else:
                    ref = short_hash
                attribution = f" (@{author})" if author else ""
                lines.append(f"- {prefix}{desc} ({ref}){attribution}")

        lines.append("")

    # Summary statistics
    total = parsed_data.get("total_commits", parsed_data.get("total_prs", 0))
    lines.append("---")
    lines.append("")
    lines.append(f"**Full Changelog**: {total} changes from {len(categories)} categories")
    if repo_url:
        lines.append(f"**Compare**: [{repo_url}/compare/...{version}]({repo_url}/compare/...{version})")
    lines.append("")

    return "\n".join(lines)


def generate_keepachangelog(
    parsed_data: dict,
    version: str,
    date: Optional[str] = None,
) -> str:
    """Generate a CHANGELOG.md entry in Keep a Changelog format.

    See: https://keepachangelog.com/
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Map internal categories to Keep a Changelog categories
    keepachangelog_map = {
        "Features": "Added",
        "Bug Fixes": "Fixed",
        "Performance": "Changed",
        "Security": "Security",
        "Documentation": "Changed",
        "Dependencies": "Changed",
        "Internal Changes": "Changed",
        "Reverts": "Removed",
        "Breaking Changes": "Changed",
    }

    # Regroup by Keep a Changelog categories
    regrouped: dict[str, list] = {}
    categories = parsed_data.get("categories", {})
    for category, items in categories.items():
        kac_category = keepachangelog_map.get(category, "Changed")
        regrouped.setdefault(kac_category, []).extend(items)

    kac_order = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]

    lines = []
    lines.append(f"## [{version}] - {date}")
    lines.append("")

    for kac_cat in kac_order:
        if kac_cat not in regrouped:
            continue
        items = regrouped[kac_cat]
        if not items:
            continue

        lines.append(f"### {kac_cat}")
        lines.append("")
        for item in items:
            desc = item.get("description", item.get("title", ""))
            lines.append(f"- {desc}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "parsed_commits.json"
    version = sys.argv[2] if len(sys.argv) > 2 else "v0.0.0"
    audience = sys.argv[3] if len(sys.argv) > 3 else "all"
    repo_url = sys.argv[4] if len(sys.argv) > 4 else None

    with open(input_file) as f:
        data = json.load(f)

    notes = generate_markdown(data, version, repo_url=repo_url, audience=audience)
    print(notes)

    # Also generate Keep a Changelog format
    kac = generate_keepachangelog(data, version)
    kac_path = "CHANGELOG_entry.md"
    with open(kac_path, "w") as f:
        f.write(kac)
    print(f"\nKeep a Changelog entry written to {kac_path}", file=sys.stderr)
```

### Step 5: Automate Release Note Generation in CI/CD

**GitHub Actions Workflow** (`.github/workflows/release-notes.yml`):

```yaml
name: Generate Release Notes

on:
  release:
    types: [created]
  workflow_dispatch:
    inputs:
      tag:
        description: "Release tag (e.g., v2.5.0)"
        required: true
        type: string
      previous_tag:
        description: "Previous tag for comparison (auto-detected if empty)"
        required: false
        type: string

jobs:
  generate-notes:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Determine version range
        id: range
        run: |
          TAG="${{ inputs.tag || github.event.release.tag_name }}"
          echo "tag=$TAG" >> "$GITHUB_OUTPUT"

          if [ -n "${{ inputs.previous_tag }}" ]; then
            PREV="${{ inputs.previous_tag }}"
          else
            # Find the previous tag automatically
            PREV=$(git tag --sort=-creatordate | grep -A1 "^${TAG}$" | tail -1)
            if [ -z "$PREV" ] || [ "$PREV" = "$TAG" ]; then
              # Fall back to the tag before this one by date
              PREV=$(git tag --sort=-creatordate | sed -n '2p')
            fi
          fi

          echo "previous_tag=$PREV" >> "$GITHUB_OUTPUT"
          echo "Generating notes for $PREV..$TAG"

      - name: Collect commits
        run: |
          bash scripts/collect-changes.sh \
            "${{ steps.range.outputs.previous_tag }}" \
            "${{ steps.range.outputs.tag }}"

      - name: Collect PRs
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PREV_DATE=$(git log -1 --format=%aI "${{ steps.range.outputs.previous_tag }}")
          TAG_DATE=$(git log -1 --format=%aI "${{ steps.range.outputs.tag }}")
          bash scripts/collect-prs.sh "$PREV_DATE" "$TAG_DATE"

      - name: Parse and categorize
        run: |
          python scripts/parse_commits.py changes.json parsed_commits.json
          python scripts/categorize_prs.py prs.json categorized_prs.json

      - name: Generate release notes
        id: notes
        run: |
          REPO_URL="${{ github.server_url }}/${{ github.repository }}"
          python scripts/generate_release_notes.py \
            parsed_commits.json \
            "${{ steps.range.outputs.tag }}" \
            "all" \
            "$REPO_URL" \
            > release_notes.md

          echo "Generated release notes:"
          cat release_notes.md

      - name: Update GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release edit "${{ steps.range.outputs.tag }}" \
            --notes-file release_notes.md

      - name: Update CHANGELOG.md
        run: |
          if [ -f CHANGELOG.md ]; then
            # Insert new entry after the header
            python -c "
          import sys
          with open('CHANGELOG.md') as f:
              content = f.read()
          with open('CHANGELOG_entry.md') as f:
              entry = f.read()
          # Insert after the first '# Changelog' line
          marker = '# Changelog'
          if marker in content:
              idx = content.index(marker) + len(marker)
              # Find end of that line
              newline_idx = content.index('\n', idx)
              content = content[:newline_idx+1] + '\n' + entry + content[newline_idx+1:]
          else:
              content = '# Changelog\n\n' + entry + content
          with open('CHANGELOG.md', 'w') as f:
              f.write(content)
          "
            echo "CHANGELOG.md updated"
          fi
```

**GitLab CI Release Notes Job**:

```yaml
generate-release-notes:
  stage: release
  image: python:3.12-slim
  before_script:
    - apt-get update && apt-get install -y git jq
    - pip install --quiet requests
  script:
    - |
      PREV_TAG=$(git tag --sort=-creatordate | sed -n '2p')
      CURRENT_TAG=$CI_COMMIT_TAG
      echo "Generating notes for $PREV_TAG..$CURRENT_TAG"

      bash scripts/collect-changes.sh "$PREV_TAG" "$CURRENT_TAG"
      python scripts/parse_commits.py changes.json parsed_commits.json
      python scripts/generate_release_notes.py parsed_commits.json "$CURRENT_TAG" all > release_notes.md

      # Update GitLab Release description via API
      ENCODED_TAG=$(echo "$CURRENT_TAG" | jq -sRr @uri)
      curl --request PUT \
        --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        --header "Content-Type: application/json" \
        --data "{\"description\": $(jq -Rs . release_notes.md)}" \
        "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/releases/${ENCODED_TAG}"
  rules:
    - if: $CI_COMMIT_TAG
```

### Step 6: Handle Audience-Specific Formatting

Different audiences need different levels of detail:

**User-Facing Release Notes** (for product announcements, in-app changelogs):

```markdown
# What's New in v2.5.0

## New Features

- **Dashboard**: Added a real-time activity feed showing team member actions as they happen
- **Export**: PDF export now supports custom page layouts and company branding
- **Search**: Full-text search across all project documents with highlighted results

## Improvements

- File upload speed improved by 40% for documents over 10 MB
- Mobile navigation now remembers your last visited section
- Reduced initial page load time by 200ms through optimized asset loading

## Bug Fixes

- Fixed an issue where notifications were not delivered for shared documents
- Corrected timezone display for users in UTC-negative regions
- Resolved a crash that occurred when uploading files with special characters in the filename

## Important Notes

This release requires all users to re-authenticate once after upgrading.
The legacy CSV import format is deprecated and will be removed in v3.0.
```

**Developer Release Notes** (for API consumers, library users):

```markdown
# v2.5.0

## Breaking Changes

- `GET /api/v1/users` now returns paginated results by default (limit: 50). Pass `?limit=0` to retrieve all results. ([#342](https://github.com/org/app/pull/342))
- The `UserPreferences` type now uses `Record<string, unknown>` instead of `any` for the `settings` field. ([#358](https://github.com/org/app/pull/358))

## Features

- **api**: Added `POST /api/v1/documents/search` endpoint with full-text search support ([#345](https://github.com/org/app/pull/345))
- **sdk**: New `DocumentClient.search()` method wrapping the search endpoint ([#347](https://github.com/org/app/pull/347))
- **webhooks**: Added `document.searched` event type ([#350](https://github.com/org/app/pull/350))

## Bug Fixes

- **api**: Fixed race condition in concurrent document updates ([#355](https://github.com/org/app/pull/355))
- **sdk**: Corrected retry logic for 429 responses to respect `Retry-After` header ([#360](https://github.com/org/app/pull/360))

## Migration Guide

### Pagination Change

If your integration fetches all users in a single request, update your code:

Before:
    response = client.get("/api/v1/users")
    all_users = response.json()

After:
    all_users = []
    page = 1
    while True:
        response = client.get(f"/api/v1/users?page={page}&limit=100")
        data = response.json()
        all_users.extend(data["items"])
        if not data["has_next"]:
            break
        page += 1
```

### Step 7: End-to-End Automation Script

**Complete Release Notes Pipeline** (`scripts/release-notes-pipeline.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Usage: release-notes-pipeline.sh <version> [previous_version] [audience]}"
PREV_VERSION="${2:-}"
AUDIENCE="${3:-all}"
REPO_URL="${REPO_URL:-$(git remote get-url origin | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')}"

echo "=== Release Notes Pipeline ==="
echo "Version:  $VERSION"
echo "Audience: $AUDIENCE"
echo "Repo:     $REPO_URL"

# Auto-detect previous version if not specified
if [ -z "$PREV_VERSION" ]; then
  PREV_VERSION=$(git tag --sort=-version:refname | grep -v "^${VERSION}$" | head -1)
  if [ -z "$PREV_VERSION" ]; then
    echo "ERROR: Could not detect previous version. Specify it explicitly."
    exit 1
  fi
fi
echo "Previous: $PREV_VERSION"
echo ""

# Step 1: Collect data
echo "--- Collecting changes ---"
bash scripts/collect-changes.sh "$PREV_VERSION" "$VERSION"

# Step 2: Parse commits
echo ""
echo "--- Parsing commits ---"
python scripts/parse_commits.py changes.json parsed_commits.json

# Step 3: Generate release notes
echo ""
echo "--- Generating release notes ---"
python scripts/generate_release_notes.py \
  parsed_commits.json \
  "$VERSION" \
  "$AUDIENCE" \
  "$REPO_URL" \
  > "release_notes_${VERSION}.md"

echo ""
echo "Release notes written to: release_notes_${VERSION}.md"
echo ""
echo "--- Preview ---"
head -40 "release_notes_${VERSION}.md"
```

## Best Practices

- **Enforce conventional commits**: Use a commit-msg hook (commitlint, commitizen) to ensure all commits follow the conventional format. This makes automated release note generation reliable rather than a best-effort guess.

- **Write user-meaningful PR titles**: The PR title is often the primary source for release note entries. Write titles as complete sentences describing the user-visible change, not as internal shorthand. "Add real-time activity feed to dashboard" is useful; "JIRA-1234 dashboard work" is not.

- **Label PRs consistently**: Define a clear set of labels (feature, bug, breaking-change, internal) and require at least one category label on every PR. This enables accurate categorization even without conventional commits.

- **Separate user-facing from internal changes**: Not every merged PR belongs in user-facing release notes. Internal refactoring, CI changes, and test improvements are valuable to track but should not appear in product announcements.

- **Highlight breaking changes prominently**: Breaking changes should always appear first in release notes, with clear migration instructions. Users who scan release notes need to see breaking changes immediately, not buried in a list of features.

- **Include contributor attribution**: Crediting authors in release notes encourages community contribution and helps users know who to contact about specific changes.

- **Version your release notes tooling**: The scripts that generate release notes are as important as the application code. Keep them in version control, test them against historical releases, and update them when your commit conventions evolve.

- **Generate notes before publishing**: Generate a draft of the release notes before tagging the release. This gives you a chance to review, edit, and add context that automated tools cannot provide (such as "why" a feature was built).

## Common Pitfalls

- **Relying solely on commit messages**: Commit messages often lack context. If your team writes terse commits ("fix bug", "wip", "address review"), the generated release notes will be useless. Supplement commit data with PR titles and descriptions.

- **Including merge commit noise**: Merge commits ("Merge branch 'main' into feature-x") add clutter. Filter them out unless they carry meaningful information (such as "Merge pull request #123: Add search feature").

- **Forgetting to handle non-conventional commits**: Even teams that use conventional commits will have occasional non-conforming commits. Your parser must handle these gracefully (categorize as "Other") rather than crashing or producing garbled output.

- **Generating notes for the wrong range**: The most common error is comparing against the wrong base reference. Always verify that the "previous version" tag is correct before generating notes. An incorrect range produces either too many or too few entries.

- **Not escaping special characters**: Commit messages and PR titles may contain Markdown special characters (backticks, brackets, asterisks). Ensure your generator escapes these properly to avoid broken formatting in the rendered output.

- **Publishing unedited automated notes**: Automated generation is a starting point, not a finished product. Always review generated notes for accuracy, clarity, and completeness before publishing. Add context, reword unclear entries, and remove irrelevant items.

- **Mixing audience concerns**: A single release note document that includes both "Added export to PDF" and "Refactored internal caching layer" confuses every audience. Either produce separate documents per audience or clearly section them with headings.

- **Ignoring dependency updates**: Dependabot and Renovate PRs can flood release notes with noise. Group dependency updates into a single "Dependencies" section with a summary count rather than listing each individual bump.

- **Not linking to issues and PRs**: Release notes without links to the underlying PRs or issues force readers to search for context manually. Always include references that allow drilling down into details.

- **Inconsistent formatting across releases**: Each release should follow the same structure. If v2.4.0 used one format and v2.5.0 uses another, consumers cannot reliably parse your changelog. Use the same tooling and templates for every release.
