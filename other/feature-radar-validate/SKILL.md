---
name: feature-radar-validate
description: |
  Validate SKILL.md frontmatter and .feature-radar/ files against format rules. Runs
  validate.sh, reports errors/warnings, and auto-fixes issues. MUST use this skill after
  editing any SKILL.md or .feature-radar/ file, even if the user doesn't ask — catches format
  bugs like the Agent Skills spec's 1024-char description limit before they break the skill.
  Use when the user asks to validate, lint, or verify skills or .feature-radar/ files, after
  editing either, or before committing changes that touch skills/ or .feature-radar/.
---

# Validate Feature Radar

Run `skills/feature-radar-validate/scripts/validate.sh` from the project root to check SKILL.md frontmatter and `.feature-radar/` SPEC compliance, then fix any issues found.

## Why This Matters

The `description` field in SKILL.md has a 1024-character limit in the Agent Skills spec (agentskills.io/specification, checked 2026-09-29). Agents that enforce the spec may reject a longer description; Claude Code instead truncates the skill listing at 1,536 characters, cutting off trigger text. Similarly, `.feature-radar/` files must follow SPEC.md naming and metadata conventions or downstream tools can't parse them. This skill catches these issues before they cause problems.

## Workflow

### Step 1: Run Validation

```bash
bash skills/feature-radar-validate/scripts/validate.sh
```

Read the full output. Note the exit code:
- **Exit 0**: all checks passed (may still have warnings)
- **Exit 1**: errors found — must be fixed

### Step 2: Report Results

Present the results clearly:

```
── Feature Radar: Validate ──

Errors:   {n}
Warnings: {n}

{List each error/warning with file path and issue}
```

If everything passes, say so and stop. No further action needed.

### Step 3: Auto-Fix (if errors or warnings found)

For each issue, apply the appropriate fix:

| Issue | Fix Strategy |
|-------|-------------|
| `description` > 1024 chars | Trim to fit — cut the least essential trigger phrases or examples first, keep the core "what it does" and "Use when" intact. Show before/after char count. |
| `description` missing "Use when" | Add a "Use when:" section based on the skill's purpose |
| `name` not kebab-case | Rename to kebab-case |
| `name` missing | Derive from directory name |
| `name` > 64 chars | Propose a shorter name and ask user to confirm — the name is how the skill is invoked |
| `name` does not match directory | Set `name` to the directory name; if the `name` is the intended one, ask user before renaming the directory (other skills reference it by path) |
| Body > 500 lines | Flag for user — this requires judgment about what to extract into reference files |
| Filename not `{nn}-{slug}.md` | Rename file to correct format |
| Missing `**Status**:` / `**Impact**:` / `**Effort**:` | Add field with a placeholder value, ask user to confirm |
| `base.md` count mismatch | Update the Tracking Summary table counts |

After fixing, re-run `bash skills/feature-radar-validate/scripts/validate.sh` to confirm all errors are resolved.

### Step 4: Completion Summary

```
── Feature Radar: Validate Complete ──

Files fixed:   ~ {path} ({what changed})
Errors fixed:  {n}
Warnings fixed: {n}
Remaining:     {n} (need user input)
```

## Proactive Triggering

When you notice yourself editing `skills/*/SKILL.md` or `.feature-radar/**/*.md`, run validation afterward without being asked. A quick `bash skills/feature-radar-validate/scripts/validate.sh` check takes seconds and prevents silent breakage.
