---
name: shared-context
description: 'Creates verified shared.md research context through plan-workflow. Use when gathering codebase context, preparing shared context for parallel-plan, or researching without generating a plan.'
argument-hint: '[--team] [feature-name] [--dry-run]'
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
  - Bash(mkdir:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/plan-workflow/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

## MANDATORY FORCED MODE - READ FIRST

This skill is a thin alias. It ALWAYS runs canonical `plan-workflow` with
`--research-only --no-checkpoint` (stop after `shared.md` + validation, print
summary, no interactive checkpoint), regardless of `$ARGUMENTS`.

**Flag policy (unambiguous):**

- Supported: the feature name, `--team`, `--dry-run`.
- Redundant — silently ignored because already forced: `--research-only`, `--no-checkpoint`.
- Every other flag (including `--plan-only`, `--no-worktree`, `--worktree`, `--visual`, `--optimized`, and any unknown `-`/`--` token) → abort with the usage error below. Do not read the canonical skill or write anything.

## SCOPE LIMITATION - READ FIRST

**THIS SKILL ONLY CREATES RESEARCH CONTEXT FILES. IT NEVER PLANS OR IMPLEMENTS.**

- DO NOT run the parallel-plan skill
- DO NOT run the implement-plan skill
- DO NOT execute implementation tasks
- DO NOT modify application source files

**Outputs**:

- `${PLANS_DIR}/[feature-name]/research-architecture.md`
- `${PLANS_DIR}/[feature-name]/research-patterns.md`
- `${PLANS_DIR}/[feature-name]/research-integration.md`
- `${PLANS_DIR}/[feature-name]/research-docs.md`
- `${PLANS_DIR}/[feature-name]/shared.md`

After creating the shared context files and displaying the summary, **STOP COMPLETELY**.

---

# Shared Context (alias)

## Arguments

**Target**: `$ARGUMENTS`

- **--team**: Optional. (Claude Code only) Deploy researchers as teammates. Default is standalone parallel sub-agents via the `Agent` tool. Cursor and Codex bundles lack team tools — do not pass `--team` there.
- **--dry-run**: Show orchestration plan without creating files. Writes nothing.
- **feature-name**: Required. Directory name under `${PLANS_DIR}` (kebab-case).

If any unsupported flag is present (see Flag policy above), abort with a usage error and STOP:

```
Usage: /shared-context [--team] [feature-name] [--dry-run]
This alias always runs plan-workflow --research-only --no-checkpoint.
Unsupported flag: <flag>
```

If no feature name provided, abort with the same usage plus examples:

```
/shared-context user-authentication
/shared-context payment-integration --dry-run
/shared-context --team payment-integration
```

## Execution

Build the **effective `$ARGUMENTS`** for canonical `plan-workflow`:

```
<feature-name> --research-only --no-checkpoint [--team] [--dry-run]
```

(`--team` / `--dry-run` only if the user passed them; user-supplied redundant `--research-only` / `--no-checkpoint` are dropped, not duplicated.)

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-workflow/SKILL.md`.
2. Execute as orchestrator with the effective `$ARGUMENTS` above substituted for `$ARGUMENTS`, so the canonical parser itself sets `RESEARCH_ONLY=true` and `NO_CHECKPOINT=true` (those variables are explanatory only — never invocation syntax).
3. On completion print the research summary and STOP. Never plan or implement.

## Summary

```markdown
# Shared Context Created

## Location

${feature_dir}/shared.md

## Research Files

- ${feature_dir}/research-architecture.md
- ${feature_dir}/research-patterns.md
- ${feature_dir}/research-integration.md
- ${feature_dir}/research-docs.md

## Next Step (User Triggered)

/parallel-plan [feature-name]
```

**STOP**: Do not execute parallel-plan. Do not write any more files. Do not modify any code. This skill is complete.
