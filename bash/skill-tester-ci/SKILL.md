---
name: skill-tester-ci
description: "Validates all CI skills in this repo. Checks Agent Skills spec compliance, gh-aw workflow compilation, permission correctness, and structural conventions. Use when CI skills have been added or modified and you want to verify they compile and conform before committing."
---

# Skill Tester CI

Validates all CI skills (`*-ci`) in this repo. Runs spec validation, compiles gh-aw workflows, and checks CI-specific conventions.

## When to Use

- After adding or modifying a CI skill
- After upgrading `gh-aw` to a new version (API changes may break workflows)
- Before committing CI skill changes
- Before submitting the plugin for Anthropic review

## Prerequisites

- `gh-aw` CLI installed (`gh extension install github/gh-aw`)
- `python3` with `pyyaml` installed
- `quick_validate.py` available at `.claude/skills/skill-creator/scripts/`

## Checks

### 1. Anthropic Spec Validation

Run `quick_validate.py` on every CI skill:

```bash
for d in skills/*-ci/; do
  python3 .claude/skills/skill-creator/scripts/quick_validate.py "$d"
done
```

### 2. Workflow Example Compilation

Extract workflow blocks from each CI skill's `references/workflow-example.md` and compile with `gh aw compile`:

```bash
# Extract markdown code blocks with frontmatter
# Copy to temp .github/workflows/
# Run: gh aw compile
```

**Pass criteria:** Zero compilation errors. Warnings are reported but don't fail.

### 3. Permission Checks

CI workflows in strict mode must NOT use write permissions directly. Verify:

- No `issues: write` (use `safe-outputs: add-comment` instead)
- No `pull-requests: write` (use `safe-outputs: create-pull-request-review-comment` instead)
- No `contents: write` unless the workflow creates files (eval-creator create mode)
- Required read permissions present for declared toolsets

### 4. Structural Checks

| Check | Rule | Severity |
|-------|------|----------|
| Has `references/workflow-example.md` | Required for all CI skills | Error |
| Workflow example has frontmatter block | At least one `` ```markdown `` block with `---` | Error |
| Name matches folder | Frontmatter `name` == directory name | Error |
| Description mentions gh-aw | CI skills should reference gh-aw | Warning |
| Has corresponding interactive skill | `foo-ci` should have a `foo` counterpart | Warning |

### 5. Cross-Workflow Validation

For workflows that use `call-workflow`:
- Verify the target workflow exists and has `workflow_call` in its `on:` section
- Verify the target's inputs match what the caller provides

## Output Format

```markdown
## CI Skill Test Results

**Date:** YYYY-MM-DD
**gh-aw version:** vX.Y.Z
**Skills tested:** N
**Passed:** N
**Compile errors:** N
**Spec failures:** N

### Compilation Results
- [skill-name]: ✓ compiled (N KB) | ✗ error: [message]

### Spec Results
- [skill-name]: ✓ valid | ✗ [error]

### Permission Issues
- [skill-name]: [issue]
```

## Running

Invoke manually:
```
/skill-tester-ci
```

Or run the script directly:
```bash
bash skills/skill-tester-ci/scripts/run-tests.sh
```

## What This Skill Does NOT Do

- Does not test interactive skills (use `skill-tester` for those)
- Does not execute workflows against real repos — only compiles them
- Does not modify skills — reports findings only
- Does not test workflow runtime behavior — compilation validates structure and permissions only
