---
name: plan
description: Use when comparing two implementation options or walking through tradeoffs
  before committing to one, breaking a change into steps, or planning conversationally
  for approval.
---

# Plan Skill

> **OpenCode V2 compatibility:** `--team` is unsupported. If it is supplied, abort before setup or dispatch and ask the caller to rerun without it. This target uses native standalone `subagent` calls only.

Create conversational implementation plan before code. Default output stays in chat; heavier artifact-producing tracks documented in references/planning-tracks.md.

**Core gate: WAIT for explicit confirmation before any code is written.** Accept "yes", "proceed", "approved", or similar affirmative. Until then, read-only analysis only; do not touch code. Unclear draft: ask focused question and re-dispatch rather than guess.

**Questions:** class `checkpoint` (Step 4 confirmation); headless (no question tool or chat turn): emit the plan and stop before any implementation. See `~/.config/opencode/shared/references/question-policy.md`.

## What This Skill Does

1. Parse `--parallel`, `--enhanced`, `--dry-run`, `--no-worktree`, `--worktree`,
   and `--visual`, then read the request and referenced files.
2. Dispatch one planner by default, three standalone planning perspectives when
   the user explicitly asks for a multi-perspective plan, or five perspectives
   when `--enhanced` is present.
3. Validate and merge every returned perspective into one plan.
4. Wait for explicit user confirmation before any implementation.

## Flags

| Flag | Effect |
| --- | --- |
| `--parallel` | Shape the plan for dependency-batched parallel implementation. |
| `--enhanced` | Use five standalone perspectives: architecture, risk, testing, security, and UX. |
| `--dry-run` | Print the selected multi-perspective roster and stop without dispatching. |
| `--worktree` | Legacy no-op; shared worktree annotations are enabled by default. |
| `--no-worktree` | Omit shared worktree annotations. |
| `--visual` | Force-write the confirmed plan and render it with `visual-plan`. |

`--parallel` changes the output shape, independently of whether one, three, or
five planning perspectives are dispatched. `--enhanced` selects five
perspectives. An explicit natural-language request for a multi-perspective plan
selects three perspectives when `--enhanced` is absent.

## When to Use

- Starting a new feature
- Making significant architectural changes
- Working on complex refactoring
- Multiple files/components will be affected
- Requirements are unclear or ambiguous

### Step 1 — Parse flags and the user's request

Strip the supported flags from `$ARGUMENTS`. Set `PARALLEL_MODE`,
`ENHANCED_MODE`, `DRY_RUN`, `VISUAL_MODE`, and `WORKTREE_MODE` explicitly.
Default `WORKTREE_MODE=true`; `--no-worktree` sets it false and `--worktree` is
a legacy no-op. Set `PERSPECTIVE_COUNT=5` when `ENHANCED_MODE=true`, otherwise
set it to `3` only when the remaining request explicitly asks for a
multi-perspective plan; default it to `1`.

Read the stripped request and any referenced files. Ask one focused question
before dispatch if the request is ambiguous. `--dry-run` with
`PERSPECTIVE_COUNT=1` aborts because the single-agent path has no roster to
preview.

### Step 2 — Dispatch

- `PERSPECTIVE_COUNT=1`: one foreground `planner` call.
- `PERSPECTIVE_COUNT=3`: `architect` (`planner`), `risk-analyst`
  (`codebase-research-analyst`), and `test-strategist`
  (`test-strategy-planner`) in one parallel foreground batch.
- `PERSPECTIVE_COUNT=5`: the same three plus `security-reviewer` and
  `ux-reviewer` (both `research-specialist`) in one parallel foreground batch.

Every call uses the native shape below, with a complete role-specific prompt and
no `sessionID` for a new child:

```text
subagent(agent="<configured-agent>", description="<perspective>",
         prompt="<complete planning prompt>", background=false)
```

Do not set `model`; each configured agent supplies or inherits its model. Include
the original request, referenced context, role focus, confirmation instruction,
and the parallel/worktree directives selected by the flags.

When `DRY_RUN=true`, print the selected three- or five-persona roster and stop
without calling `subagent`.

For a single planner, relay the validated report. For three or five perspectives,
merge architecture, risks, testing, and optional security/UX slices without
dropping a role. A terminal lifecycle state alone is insufficient: require each
candidate report and validate any declared artifact. For contentless completion,
record `sessionID`, inspect edits/artifacts, preserve work, retry at most once,
then report the missing perspective. Follow
`~/.config/opencode/shared/references/standalone-dispatch.md`.

### Step 2.5 — Validate the plan before relaying

Read `~/.config/opencode/skills/plan/references/plan-validation.md` after planner return/merge; run all four checks. Missing required structure or parallel annotations: re-dispatch with missing-section directive. Missing expected sections/paths/perspectives: append visible validation notes.



## Step 3 — Relay

Present plan verbatim, including validation notes. Do not shorten or add commentary above it.

## Step 4 — Stop and confirm

Wait; do not touch code until user responds:

- yes/proceed/approved: approved implementation may begin.
- modify/different approach/reorder: re-dispatch with requested change and previous plan as context; discard prior approach when requested.
- no: stop, no implementation.

For standalone enhanced re-dispatch, use a fresh batch of five parallel calls per `references/personas-and-merge.md` (Re-dispatch).
That fresh batch is five parallel native `subagent` calls with no `description` plus the role-specific `prompt`, which is reserved for sub-agent dispatch.


Unclear response: ask focused clarification.

## Step 5 — Visual rendering (VISUAL_MODE=true only)

Runs only after Step 4 confirmation, last; never substitutes for earlier phases.

- Dry-run: print `visual generation would run`; no writes/invocation.
- Otherwise write confirmed plan verbatim to `docs/prps/plans/<slug>.plan.md`; create directory, resolve absolute path. Slug: lowercase, replace non-[a-z0-9-] with hyphen, collapse/trim, cap 20, fallback untitled.
- Invoke `visual-plan <absolute-plan-path>`; surface its URL, localhost preview or `local files only`; do not derive output directory yourself.

Read `~/.config/opencode/shared/references/visual-mode.md` only when visual requested, for force-write-first terminal decorator contract.

## After approval

Read `~/.config/opencode/skills/plan/references/planning-tracks.md` when choosing execution/report/commit handoff or comparing planning tracks. Small parallel features can execute in conversation; rigorous report/validation/archive needs PRP-format file and `/prp-implement --parallel`. `implement-plan` consumes parallel-plan.md. Review via code-review; commit via git-workflow --commit or prp-commit.

Use plan for new features, architecture changes, complex refactors, multi-file work or ambiguous requirements. Internal-only changes can skip enhanced security/UX roster; exposure or user touchpoints justify it.
