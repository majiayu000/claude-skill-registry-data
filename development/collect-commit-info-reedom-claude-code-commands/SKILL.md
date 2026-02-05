---
name: collect-commit-info
description: Analyze staged files, group by category, and generate conventional commit specs as JSON.
allowed-tools: Read, Bash(${CLAUDE_PLUGIN_ROOT}/skills/collect-commit-info/scripts/collect-info.sh:*), Bash(${CLAUDE_PLUGIN_ROOT}/skills/collect-commit-info/scripts/cleanup.sh:*)
---

This skill analyzes staged git files and returns commit specifications as JSON. It:
1. Collects staged file metadata via script
2. Reads diff content to understand changes
3. Groups files by category (deps, ci, config, source, test, docs)
4. Generates conventional commit messages for each group
5. Returns JSON specs for the caller to execute

## Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--lang` | context | Message language (conversation context → system locale → en) |

## Output Contract

This skill ALWAYS returns JSON. The caller executes git commands based on this output.

**Success:**
```json
{
  "commits": [
    {"message": "type(scope): subject\n\nBody", "files": ["file1", "file2"]}
  ],
  "summary": {"total_commits": 1, "total_files": 2}
}
```

**Error:**
```json
{"error": "description", "error_code": "CODE"}
```

## Workflow

### Step 1: Collect file info

```bash
${CLAUDE_PLUGIN_ROOT}/skills/collect-commit-info/scripts/collect-info.sh --lang <code>
```

Script returns JSON with `temp_dir`, `files` array (with categories), and `paths.diff_content`.

On error JSON → return it immediately and stop.

### Step 2: Read diff content

Read the file at `paths.diff_content` to understand what changed.

### Step 3: Group files by category

Group files from the `files` array. Commit order:
1. `deps` - Dependencies (package.json, lock files)
2. `ci` - CI/CD (.github/*)
3. `config` - Configuration (*.yml, *.toml, rc files)
4. `source` - Source code
5. `test` - Tests (*_test.*, *.test.*, *.spec.*)
6. `docs` - Documentation (*.md, docs/*)

### Step 4: Generate commit messages

For each group, create a conventional commit message:

```
type(scope): imperative subject (max 50 chars)

Optional body explaining what and why.
```

**Type by category:**
| Category | Type |
|----------|------|
| deps | chore |
| ci | ci |
| config | chore |
| source | feat/fix/refactor (analyze diff) |
| test | test |
| docs | docs |

**For source files, analyze diff to determine type:**
- New functionality → `feat`
- Bug fixes, error handling → `fix`
- Restructuring, cleanup → `refactor`

**Scope:** Derive from paths (e.g., `src/auth/*` → `auth`)

**Language:** Use `lang.effective` from script output. If conversation context indicates a preferred language, use that instead.

### Step 5: Cleanup and return

```bash
${CLAUDE_PLUGIN_ROOT}/skills/collect-commit-info/scripts/cleanup.sh <temp_dir>
```

Return the JSON commit specs.
