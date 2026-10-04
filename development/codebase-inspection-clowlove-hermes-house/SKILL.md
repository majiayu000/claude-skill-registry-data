---
name: codebase-inspection
description: "Inspect codebases w/ pygount: LOC, languages, ratios. Also: remote GitHub repo analysis via gh CLI API."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository, GitHub, Deep Analysis, Repo Review]
    related_skills: [github-repo-management]
triggers:
  - "分析这个仓库"
  - "深度分析"
  - "repo analysis"
  - "what is this repo"
  - "代码行数"
  - "LOC"
  - "language breakdown"
  - "代码分析"
prerequisites:
  commands: [pygount]
---

# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

## When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions

## Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## 1. Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

## 2. Common Folder Exclusions

Adjust based on the project type:

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Filter by Specific Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## 4. Detailed File-by-File Output

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## 5. Output Formats

```bash
# Summary table (default recommendation)
pygount --format=summary .

# JSON output for programmatic use
pygount --format=json .

# Pipe-friendly: Language, file count, code, docs, empty, string
pygount --format=summary . 2>/dev/null
```

## 6. Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

## 7. Remote GitHub Repo Analysis (no clone needed)

Use `gh api` to inspect a repo without cloning it — useful for quick assessment, comparison, or deciding whether to invest time in a deeper look.

```bash
# Repo overview (stars, forks, language, license, description)
gh repo view owner/repo --json name,description,stargazerCount,forkCount,primaryLanguage,createdAt,updatedAt,licenseInfo,homepageUrl

# List top-level files and directories
gh api repos/owner/repo/contents --jq '.[] | {name, type, size}'

# List files in a subdirectory
gh api repos/owner/repo/contents/path/to/dir --jq '.[] | {name, type, size}'

# Read a specific file (returns base64-encoded content)
gh api repos/owner/repo/contents/README.md --jq '.content' | base64 -d

# Read the first N lines of any file
gh api repos/owner/repo/contents/path/to/file.md --jq '.content' | base64 -d | head -100

# Count files by extension in a directory
gh api repos/owner/repo/contents/src --jq '[.[] | .name | split(".")[-1]] | group_by(.) | map({ext: .[0], count: length})'

# Check contributors
gh api repos/owner/repo/contributors --jq '.[] | {login, contributions}'

# Check recent commits
gh api repos/owner/repo/commits --jq '.[] | {sha: .sha[:8], message: .commit.message[:80], date: .commit.author.date}'
```

### Deep Analysis Pattern (for user reports)

When the user asks to "deeply analyze" a GitHub repo:

1. **Overview**: `gh repo view` for metadata (stars, forks, language, license, dates)
2. **Structure**: `gh api repos/.../contents` for top-level directory layout
3. **README**: Read README.md for project purpose and usage
4. **Key files**: Read package.json, setup.py, Cargo.toml, or equivalent for dependencies/tech stack
5. **Scripts/CI**: Check `.github/workflows/`, `scripts/`, `Makefile` for build/test patterns
6. **Specific deep dives**: Read representative source files from key directories

Report format: Overview → Architecture → Tech Stack → Key Features → Strengths/Weaknesses → Comparison (if relevant).

## Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.
