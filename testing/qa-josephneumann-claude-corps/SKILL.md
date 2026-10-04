---
name: qa
description: "Use when you need acceptance-first release confidence: validate acceptance criteria, regressions, and browser workflows before calling work ready"
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_click, mcp__playwright__browser_fill_form, mcp__playwright__browser_type, mcp__playwright__browser_press_key, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_resize, mcp__playwright__browser_console_messages, mcp__playwright__browser_close, mcp__playwright__browser_run_code, mcp__playwright__browser_navigate_back, mcp__playwright__browser_evaluate
---

# /qa $ARGUMENTS

Acceptance-first validation. Your job is to answer: "Is this actually ready?" with evidence, not vibes.

This is not deep code review. `/multi-review` owns architectural and reviewer-style findings. `/qa` owns acceptance criteria, regressions, browser workflow confidence, and release readiness.

## Arguments

- `$ARGUMENTS` = task ID, plan path, or empty
- Optional `--url <URL>` to force a browser target
- Optional `--public-only` to skip authenticated flows

Argument handling:
- If `$ARGUMENTS` looks like a task ID and Linear MCP is available, call `get_issue(id=<task-id>, includeRelations=true)` and use the task description plus relations as the primary acceptance-criteria source
- If `$ARGUMENTS` looks like a task ID but Linear MCP is not available, say so explicitly and fall back to the latest plan plus current diff
- If `$ARGUMENTS` is a readable file path, read it directly
- If `$ARGUMENTS` is empty, use the latest plan in `docs/plans/`, then current diff as fallback
- If a task ID is provided and `get_issue` fails, stop and report the lookup failure rather than silently inventing acceptance criteria

## Verification Discipline

Use `/verify` standards throughout:
- no success claims without fresh evidence
- no "should work"
- if a check was not run, say so explicitly

## Phase 1: Build the QA Scope

Collect acceptance criteria in this order:

1. Explicit task lookup from `$ARGUMENTS` via `get_issue` when Linear MCP is available
2. Explicit plan or spec file named in `$ARGUMENTS`
3. Latest plan in `docs/plans/`
4. Current diff and changed files

Summarize:
- what is under test
- what is out of scope
- which risks matter most for this change

If a task ID was provided but could not be resolved because Linear is unavailable, say that clearly before falling back.

If you cannot find any concrete acceptance criteria, say so and derive a provisional checklist from the diff. Label it as inferred.

## Phase 2: Run Deterministic Checks

Run the project's relevant test or verification commands first.

Examples:
```bash
uv run pytest
pnpm test
make run-checks
```

Then capture:
- command run
- exit code
- what it proves
- what it does not prove

If a required check fails, mark the run `Blocked` and continue only far enough to clarify blast radius.

## Phase 3: Infer Regression Surface

Map changed files to impacted workflows:
- forms
- navigation
- auth
- CRUD
- data display
- overlays
- shared utilities or global wrappers

When UI-visible files changed, read `docs/browser-testing-protocol.md` and follow it. Reuse its workflow inference, cache clearing, auth handling, and responsive checks instead of inventing a second protocol.

## Phase 4: Browser Validation

If browser testing is applicable:

1. Confirm Playwright MCP is available
2. Confirm a target URL via `--url`, detected localhost server, or user answer
3. Run only the workflows affected by the change
4. Check console errors after major interactions
5. Verify persistence after reload when the workflow mutates data

If Playwright is unavailable or no server is running:
- do not fake confidence
- emit a manual workflow checklist instead
- mark the final verdict `Needs manual verification` unless deterministic checks already prove there is no UI surface

If auth is required and `--public-only` is set, skip protected flows and call that out explicitly.

## Phase 5: Final Verdict

Use exactly one of these outcomes:
- **Pass** — acceptance criteria covered, checks green, no unresolved blocker
- **Blocked** — failing tests, broken workflow, or clear regression
- **Needs manual verification** — some important check could not be executed

## Required Output

Structure the report as:

```markdown
## QA Summary

### Scope Under Test
- ...

### Checks Run
| Check | Result | Evidence |
|-------|--------|----------|
| ... | Pass/Fail/Skipped | ... |

### Browser Workflows
| Workflow | Result | Notes |
|----------|--------|-------|
| ... | Pass/Fail/Manual | ... |

### Regressions and Gaps
- ...

### Final Verdict
Pass / Blocked / Needs manual verification

### Manual Follow-Ups
- ...
```

## Rules

- Be strict about evidence
- Prefer targeted verification over exhaustive busywork
- Distinguish "not tested" from "passed"
- Do not silently downgrade risk
- Do not rewrite code or fix issues inside `/qa`
