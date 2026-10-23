---
name: plan
description: 'Use when comparing two implementation options or walking through tradeoffs before committing to one, breaking a change into steps, or planning conversationally for approval.'
argument-hint: '[--parallel] [--team] [--enhanced] [--dry-run] [--no-worktree] [--visual] <what you want to plan>'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Agent
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - AskUserQuestion
  - SendMessage
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(git:*)
  - 'Bash(${CURSOR_PLUGIN_ROOT}/skills/_shared/scripts/prepare-feature-branch.sh:*)'
---

# Plan Skill

Create conversational implementation plan before code. Default output stays in chat; heavier artifact-producing tracks documented in references/planning-tracks.md.

**Core gate: WAIT for explicit confirmation before any code is written.** Accept "yes", "proceed", "approved", or similar affirmative. Until then, read-only analysis only; do not touch code. Unclear draft: ask focused question and re-dispatch rather than guess.

**Questions:** class `checkpoint` (Step 4 confirmation); headless (no question tool or chat turn): emit the plan and stop before any implementation. See `${CURSOR_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## What This Skill Does

1. Parse `--parallel`, `--enhanced`, `--dry-run`, `--no-worktree`, legacy `--worktree`, `--visual`; read request and referenced context; clarify ambiguity before dispatch.
2. Select Path A (single planner), Path C (enhanced standalone), or Path B (team).
3. Step 2.5: validate structure, paths, parallel integrity, merged perspectives.
4. Step 3: relay plan verbatim with validation notes; no summary/commentary above it.
5. Step 4: stop and wait for explicit confirmation.
6. Step 5: optional visual rendering, only after confirmation; then approved implementation handoff.

## When to Use

- Starting a new feature
- Making significant architectural changes
- Working on complex refactoring
- Multiple files/components will be affected
- Requirements are unclear or ambiguous

### Step 1 — Parse flags and the user's request

Parse and strip `--parallel`, `--team`, `--enhanced`, `--dry-run`, `--no-worktree`, legacy `--worktree`, `--visual` from `$ARGUMENTS`. Set `PARALLEL_MODE`, `AGENT_TEAM_MODE`, `ENHANCED_MODE`, `DRY_RUN`, `VISUAL_MODE` to booleans. `WORKTREE_MODE=true` by default; `--no-worktree` makes it false; `--worktree` is silent no-op. Remaining text is request.

| Flag            | Effect                                                                                                                                 |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `--parallel`    | Shapes output only: Batches summary, hierarchical N.N IDs, explicit `Depends on [...]` every step. Not research fan-out.               |
| `--team`        | Coordinated three-persona planning; Claude Code only.                                                                                  |
| `--enhanced`    | Adds security-reviewer and ux-reviewer, widening roster to five. Alone selects standalone Path C; with --team selects enhanced Path B. |
| `--dry-run`     | Prints selected standalone/team roster and exits without spawning. Requires --team or --enhanced.                                      |
| `--no-worktree` | Suppresses Worktree Setup and per-task annotations. Default emits one shared feature path, no children.                                |
| `--worktree`    | Legacy silent no-op.                                                                                                                   |
| `--visual`      | After approval, writes otherwise-inline plan then renders via visual-plan. Dry-run prints intent only.                             |

`--parallel`, `--enhanced`, `--team`, `--no-worktree` compose independently. Enhanced alone works in every bundle; only team combinations need Claude Code.

Validation errors (abort):

- Dry-run without team/enhanced: `--dry-run requires --team or --enhanced (no-op for the single-agent path).`
- Team in Cursor/Codex: `--team requires team tools, which Cursor/Codex bundles do not ship. Use --parallel instead.`
- Enhanced team in Cursor/Codex: `--enhanced --team requires team tools, which Cursor/Codex bundles do not ship. Drop --team to use the standalone 5-persona path.`
- Team without environment flag: `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`

Read request and referenced files. Ambiguous request: ask one focused question before dispatch.

### Step 2 — Dispatch

| AGENT_TEAM_MODE | ENHANCED_MODE | Path                                                                                            |
| --------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| false           | false         | A: single planner via Agent, with request/context and Plan Format confirmation instruction. |
| false           | true          | C: five standalone personas.                                                                    |
| true            | false         | B: three-persona team.                                                                          |
| true            | true          | B enhanced: five-persona team.                                                                  |

Read `${CURSOR_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` when dispatching Path C or after approval for execution; use §§8–9 for planner worktree/batch directives in any mode.
Read `${CURSOR_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` only when `--team` is passed (Path B); prefix `plan-`, flat roster, canonical lifecycle.

Read `${CURSOR_PLUGIN_ROOT}/skills/plan/references/planner-prompts.md` when building Path A prompt or appending parallel directives to any persona prompt.
Read `${CURSOR_PLUGIN_ROOT}/skills/plan/references/personas-and-merge.md` when selecting Path B/C roster, dry-run output, failure policy or merging perspectives.
Read `${CURSOR_PLUGIN_ROOT}/skills/plan/references/enhanced-personas.md` only when `--enhanced` is passed, for security/UX prompts.

Dry-run: print exact selected roster format; no spawning; if visual also print `visual generation would run`; exit. Otherwise dispatch selected roster. Team completes cleanup before validation/relay. Path A planner owns format, worked examples, sizing/phasing and red-flag checks.

### Step 2.5 — Validate the plan before relaying

Read `${CURSOR_PLUGIN_ROOT}/skills/plan/references/plan-validation.md` after planner return/merge; run all four checks. Missing required structure or parallel annotations: re-dispatch with missing-section directive. Missing expected sections/paths/perspectives: append visible validation notes.
With `--team`, re-dispatch only after prior teammates have completed shutdown.

## Step 3 — Relay

Present plan verbatim, including validation notes. Do not shorten or add commentary above it.

## Step 4 — Stop and confirm

Wait; do not touch code until user responds:

- yes/proceed/approved: approved implementation may begin.
- modify/different approach/reorder: re-dispatch with requested change and previous plan as context; discard prior approach when requested.
- no: stop, no implementation.

For standalone enhanced re-dispatch, use a fresh batch of five parallel calls per `references/personas-and-merge.md` (Re-dispatch).
That fresh batch is five parallel `Agent` calls with no `name=`, which is reserved for teammate dispatch.
With `--team`, re-dispatch spawns fresh teammates after prior teammates have shut down; do not message prior teammates.
Unclear response: ask focused clarification.

## Step 5 — Visual rendering (VISUAL_MODE=true only)

Runs only after Step 4 confirmation, last; never substitutes for earlier phases.

- Dry-run: print `visual generation would run`; no writes/invocation.
- Otherwise write confirmed plan verbatim to `docs/prps/plans/<slug>.plan.md`; create directory, resolve absolute path. Slug: lowercase, replace non-[a-z0-9-] with hyphen, collapse/trim, cap 20, fallback untitled.
- Invoke `visual-plan <absolute-plan-path>`; surface its URL, localhost preview or `local files only`; do not derive output directory yourself.

Read `${CURSOR_PLUGIN_ROOT}/skills/_shared/references/visual-mode.md` only when visual requested, for force-write-first terminal decorator contract.

## After approval

Read `${CURSOR_PLUGIN_ROOT}/skills/plan/references/planning-tracks.md` when choosing execution/report/commit handoff or comparing planning tracks. Small parallel features can execute in conversation; rigorous report/validation/archive needs PRP-format file and `/prp-implement --parallel`. `implement-plan` consumes parallel-plan.md. Review via code-review; commit via git-workflow --commit or prp-commit.

Use plan for new features, architecture changes, complex refactors, multi-file work or ambiguous requirements. Internal-only changes can skip enhanced security/UX roster; exposure or user touchpoints justify it.
