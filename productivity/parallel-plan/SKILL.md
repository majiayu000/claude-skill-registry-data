---
name: parallel-plan
description: 'Creates parallel-plan.md from existing shared.md through plan-workflow. Use when planning from shared context, organizing dependency batches, or validating parallel implementation tasks.'
argument-hint: '[--team] [--no-worktree] [--visual] [feature-name] [--dry-run]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - SendMessage
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/plan-workflow/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/**/*.sh:*)'
---

## MANDATORY FORCED MODE - READ FIRST

This skill is a thin alias. It ALWAYS runs canonical `plan-workflow` with
`--plan-only --no-checkpoint` (use existing `shared.md`, no interactive
checkpoint), regardless of `$ARGUMENTS`.

**Flag policy (unambiguous):**

- Supported: the feature name, `--team`, `--dry-run`, `--no-worktree`, `--visual`.
- Silent no-op (legacy): `--worktree`.
- Redundant — silently ignored because already forced: `--plan-only`, `--no-checkpoint`.
- Every other flag (including `--research-only`, `--optimized`, and any unknown `-`/`--` token) → abort with the usage error below. Do not read the canonical skill or write anything.

## SCOPE LIMITATION - READ FIRST

**THIS SKILL ONLY CREATES PLANNING ARTIFACTS. IT NEVER IMPLEMENTS.**

- DO NOT execute any implementation tasks
- DO NOT modify application code
- DO NOT run the implement-plan skill
- DO NOT proceed beyond creating planning artifacts

**Outputs**:

- `${PLANS_DIR}/[feature-name]/analysis-context.md`
- `${PLANS_DIR}/[feature-name]/analysis-code.md`
- `${PLANS_DIR}/[feature-name]/analysis-tasks.md`
- `${PLANS_DIR}/[feature-name]/parallel-plan.md`

After creating planning artifacts and displaying the summary, **STOP COMPLETELY**.

---

# Parallel Plan (alias)

## Workflow Integration

```text
shared-context (step 1) -> parallel-plan (this skill) -> implement-plan (step 3)
```

This skill requires `${feature_dir}/shared.md` and ends after producing
analysis artifacts and `parallel-plan.md`. The user manually runs
`/implement-plan` when ready.

**If shared.md doesn't exist**: canonical `plan-workflow/scripts/check-prerequisites.sh`
fails fast in plan-only mode. Stop and tell the user to run
`/shared-context [feature-name]` first. Do NOT fall back to research.

## Arguments

**Target**: `$ARGUMENTS`

- **--team**: Optional. (Claude Code only) Deploy analysis and validation stages as teammates. Default is standalone parallel sub-agents via the `Agent` tool. Cursor and Codex bundles lack team tools — do not pass `--team` there.
- **--worktree**: Optional. (legacy — now default; safe to omit) Worktree annotations are emitted by default. Accepted as a silent no-op.
- **--no-worktree**: Optional. Opt out of worktree annotations. The plan will not contain a `## Worktree Setup` section.
- **--visual**: Optional. Render the finished plan as an Agent-Native visual artifact (MDX) via `ycc:visual-plan`; local-files by default, hosted link requires `--share`.
- **--dry-run**: Show what would be created without making changes. Writes nothing.
- **feature-name**: Required. Matches directory name in `${PLANS_DIR}`.

If any unsupported flag is present (see Flag policy above), abort with a usage error and STOP:

```
Usage: /parallel-plan [--team] [--no-worktree] [--visual] [feature-name] [--dry-run]
This alias always runs plan-workflow --plan-only --no-checkpoint.
Unsupported flag: <flag>
```

If no feature name provided, abort with the same usage plus examples:

```
/parallel-plan user-authentication
/parallel-plan payment-integration --dry-run
/parallel-plan --team payment-integration
/parallel-plan --no-worktree user-authentication
/parallel-plan --visual user-authentication
```

## Execution

Build the **effective `$ARGUMENTS`** for canonical `plan-workflow`:

```
<feature-name> --plan-only --no-checkpoint [--team] [--dry-run] [--no-worktree] [--visual]
```

(optional flags only if the user passed them; `--worktree` maps to nothing —
it is a legacy no-op; user-supplied redundant `--plan-only` / `--no-checkpoint`
are dropped, not duplicated.)

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-workflow/SKILL.md`.
2. Execute as orchestrator with the effective `$ARGUMENTS` above substituted for `$ARGUMENTS`, so the canonical parser itself sets `PLAN_ONLY=true` and `NO_CHECKPOINT=true` (those variables are explanatory only — never invocation syntax).
3. On completion print the plan summary and STOP. Never implement.

## Summary

```markdown
# Parallel Plan Created

## Location

${feature_dir}/parallel-plan.md

## Analysis Files Generated

- ${feature_dir}/analysis-context.md
- ${feature_dir}/analysis-code.md
- ${feature_dir}/analysis-tasks.md

## Next Steps (FOR USER - NOT FOR THIS SKILL)

**THIS SKILL IS NOW COMPLETE. DO NOT PROCEED.**

/implement-plan [feature-name]
```

**STOP**: Do not execute implement-plan. Do not write any more files. Do not modify any code. This skill is complete.
