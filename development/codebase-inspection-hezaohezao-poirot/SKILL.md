---
name: codebase-inspection
description: "Inspect codebases: LOC, languages, ratios via pygount."
allowed-tools:
  - bash
  - read_file
  - list_dir
enabled: true
related-skills: [github-repo-management]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# Codebase Inspection

Analyze repositories for lines of code, language breakdown, file counts, and
code-vs-comment ratios using `pygount`.

## When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions

## Prerequisites

```bash
pip install pygount
```

## 1. Basic Summary (Most Common)

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build
directories, otherwise pygount will crawl them and take a very long time.

## 2. Common Folder Exclusions

```bash
# Python project
--folders-to-skip=".git,__pycache__,venv,.venv,.tox,.eggs,*.egg-info,.pytest_cache,.mypy_cache,.ruff_cache"

# Node.js project
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,coverage"

# General (safe default)
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,*.egg-info,.pytest_cache,.mypy_cache"
```

## 3. Detailed Per-File Output

```bash
pygount --format=summary \
  --folders-to-skip=".git,node_modules,.venv,__pycache__" \
  --names-to-skip="*.pyc,*.pyo,*.so,*.dylib" \
  /path/to/repo
```

## 4. Language Breakdown Only

```bash
pygount --format=summary /path/to/repo 2>/dev/null | grep -E "^\s+\w" | sort -t$'\t' -k2 -rn
```

## 5. JSON Output (for further processing)

```bash
pygount --format=json \
  --folders-to-skip=".git,node_modules,.venv,__pycache__" \
  /path/to/repo > codebase_stats.json

python3 -c "
import json
with open('codebase_stats.json') as f:
    data = json.load(f)
# Aggregate by language
from collections import defaultdict
by_lang = defaultdict(lambda: {'code': 0, 'files': 0})
for entry in data:
    lang = entry.get('language', 'unknown')
    by_lang[lang]['code'] += entry.get('code', 0)
    by_lang[lang]['files'] += 1
for lang, stats in sorted(by_lang.items(), key=lambda x: -x[1]['code']):
    print(f'{lang:20s} {stats[\"code\"]:8d} lines  {stats[\"files\"]:4d} files')
"
```

## 6. Quick LOC Count (without pygount)

If pygount isn't available, use `find` + `wc`:

```bash
# Count lines in all Python files (excluding venvs)
find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/__pycache__/*" | xargs wc -l | tail -1

# Count by language
echo "Python: $(find . -name '*.py' -not -path '*/.venv/*' | xargs wc -l 2>/dev/null | tail -1)"
echo "JavaScript: $(find . -name '*.js' -not -path '*/node_modules/*' | xargs wc -l 2>/dev/null | tail -1)"
echo "TypeScript: $(find . -name '*.ts' -not -path '*/node_modules/*' | xargs wc -l 2>/dev/null | tail -1)"
```

## 7. File Count by Type

```bash
# Count files by extension
find . -type f -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.venv/*" | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

## Pitfalls

- **Always exclude dependency dirs**: `node_modules`, `venv`, `.venv`,
  `__pycache__`, `dist`, `build` — otherwise pygount hangs or counts millions
  of irrelevant lines.
- **Binary files**: pygount skips them, but `find + wc` doesn't. Use
  `--names-to-skip` for pygount, or filter with `grep -I` for find.
- **Generated files**: `*.min.js`, `*_pb2.py`, auto-generated code inflates
  counts. Exclude with `--names-to-skip`.
- **Encoding**: pygount may fail on non-UTF-8 files. Use `--encoding=utf-8`
  or `--encoding=chardet` for mixed-encoding repos.
