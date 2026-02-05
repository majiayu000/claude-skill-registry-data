---
name: collect-commits-and-files
description: Collect changed files from git diff and explicit paths, categorize by type, output manifest.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/skills/collect-commits-and-files/scripts/collect-info.sh:*), Bash(${CLAUDE_PLUGIN_ROOT}/skills/collect-commits-and-files/scripts/cleanup.sh:*)
---

Skill for collecting files to review: runs git diff against target branch, merges explicit files, categorizes by type.

## Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--against` | origin/main | Target branch for diff comparison |
| `--files` | (none) | Comma-separated explicit file paths |

## Workflow

### 1. Collect File Info

Run:
```bash
${CLAUDE_PLUGIN_ROOT}/skills/collect-commits-and-files/scripts/collect-info.sh --against <branch> --files <paths>
```

Returns JSON manifest:
```json
{
  "temp_dir": "<git-root>/.tmp/quick-refactor-XXXXXX",
  "repo_root": "/path/to/repo",
  "against_branch": "origin/main",
  "paths": {
    "diff_dir": "<temp_dir>/diff",
    "files_dir": "<temp_dir>/files",
    "reviews_dir": "<temp_dir>/reviews"
  },
  "summary": {
    "total_files": 10,
    "source": 6,
    "test": 2,
    "config": 1,
    "docs": 1
  },
  "project_rules": ["/path/to/CLAUDE.md", "/path/to/.kiro/steering.md"]
}
```

### 2. Handle Errors

If script returns error, report to caller:
```json
{"error": "No files to review", "error_code": "NO_FILES"}
```

Error codes:
- `NOT_GIT_REPO`: Not in a git repository
- `BRANCH_NOT_FOUND`: Target branch does not exist
- `NO_FILES`: No files found to review
- `NO_EXISTING_FILES`: All files are deleted

### 3. Temp Directory Structure

The script creates temp directory at `<git-root>/.tmp/` (falls back to system temp):

```
<git-root>/.tmp/
├── .gitignore              # Contains `*` to ignore all temp files
└── quick-refactor-XXXXXX/
    ├── diff/               # Individual file diffs
    │   └── <md5hash>.diff
    ├── files/              # File paths by category (JSON arrays)
    │   ├── source.json     # ["path/to/file1.ts", "path/to/file2.ts"]
    │   ├── test.json
    │   ├── config.json
    │   └── docs.json
    └── reviews/            # Empty, for review agent outputs
```

### 4. Cleanup

After processing is complete, run:
```bash
${CLAUDE_PLUGIN_ROOT}/skills/collect-commits-and-files/scripts/cleanup.sh <temp_dir>
```

## File Categories

| Category | Description | Example patterns |
|----------|-------------|------------------|
| source | Source code files | `*.ts`, `*.py`, `*.go` |
| test | Test files | `*_test.go`, `*.spec.ts`, `tests/` |
| config | Configuration | `*.yaml`, `.eslintrc`, `.github/` |
| docs | Documentation | `*.md`, `docs/` |

## Return Value

Return the manifest JSON directly. Orchestrator uses this to:
1. Read file lists from `paths.files_dir`
2. Route to appropriate review agents based on `summary` counts
3. Store review outputs in `paths.reviews_dir`
4. Clean up `temp_dir` on completion
