---
name: grok-first
description: "Use when Claude Code should delegate implementation, fixes, exploration, and approved git mechanics to Grok Build CLI while Claude specifies, decides, reviews, and verifies."
version: 1.2.0
author: Carlos Ziegler
license: MIT
metadata:
  tags: [claude-code, grok, grok-build, delegation, coding-agent]
---

# Grok First

## Hard Gate

Use this skill for hands-on delegation only when the active harness is **Claude
Code** and `command grok` is available. Before the first delegation in a batch,
run:

```bash
command -v grok
grok --version
```

If Grok is unavailable, unauthenticated, or its version check fails, report the
blocker or continue the work directly in Claude Code. Do not guess a fallback
binary or authentication method.

Every other harness — Grok itself, Codex, ChatGPT, Pi, or another routed agent
— works directly and must not invoke Grok CLI for hands-on self-delegation.
This prevents recursive delegation and invisible work. There is no equivalent
of Codex's `ANTHROPIC_BASE_URL` router gate verified for Grok; do not invent one.

An independent, repository-provided review workflow may always be used after a
frozen change set. This skill does **not** claim that Grok provides a built-in
`autoreview` command.

## Ownership and Route

Claude Code thinks, specifies, decides, and verifies. Grok types, explores, and
executes a frozen work order.

Delegate to Grok by default when the prompt is a clear work order:

- implementation from a frozen specification; refactors; mechanical migrations
- bug fixes with a known reproduction, or diagnosis followed by a bounded fix
- CI, lint, type, and test failures; focused test writing or coverage fills
- dependency updates, scripts, and tooling
- read-heavy repository exploration when raw reading greatly outweighs the
  resulting answer
- git mechanics — rebase, merge-conflict resolution, and the repository's land
  workflow — are **mandatory Grok delegations**, never direct Claude execution,
  once Claude has made the land decision and every required pre-land gate passes

For an approved land operation, send **one self-contained order** covering:
rebase → resolve → push → confirm a CI run attached to the exact head SHA →
wait for **successful/green** CI → land. If that exact-head run fails, is
cancelled, or never attaches, stop and report; do not land. Do not bounce this
sequence back to Claude mid-flight. Claude retains the decision to land and must
review the outcome.

When waiting for CI, precheck that the PR is mergeable, confirm a run attached
to the exact head SHA before polling, report every terminal state, bound the
wait, and prefer a repository watcher script when one exists.

Keep in Claude Code:

- architecture, API and UX decisions, naming, and any task where writing the
  specification is the work
- tiny obvious edits (roughly fewer than 20 changed lines)
- session-only tools such as MCP, browser/computer use, password managers, and
  account tooling
- releases, publishing, version bumps, credentials, and secrets
- the decision to land, pre-land gates, final review, and closeout evidence

Mixed task: Claude first decides the design and freezes a specification, then
Grok builds it. Heuristic: if the prompt already reads like a work order,
delegate; if writing it requires decisions, stay in Claude.

New work orders always use a **fresh** Grok session. Do not resume a long-lived
session for unrelated work: stale sessions can reinterpret a new order as
configuration or no-op. Portfolio or multi-repository work goes to the active
session's designated maintainer/orchestrator skill when one exists. Otherwise
Claude Code orchestrates the portfolio directly but delegates only separate,
self-contained, per-repository Grok work orders; never ask one Grok worker to
coordinate uncontrolled cross-repository work.

## Repository Instructions

Before writing the work order, identify the repository's canonical instruction
files and include their relevant constraints. Never create or modify `CLAUDE.md`,
`AGENTS.md`, or other agent instruction files unless the user explicitly asks.
If the repository designates one canonical file, point Grok to that file rather
than duplicating its contents loosely.

## Invoke

Grok starts with no reliable Claude Code conversation context. Use a temporary
prompt file, an explicit session ID, a fixed working directory, and per-worker
result/log paths. Never put a multi-line work order in shell history.

```bash
REPO="/absolute/path/to/repository"
WORKER="feature-short-name"
SID="$(uuidgen | tr '[:upper:]' '[:lower:]')"
PROMPT="$(mktemp -t grok-first-prompt.XXXXXX)"
OUT="/tmp/grok-first-${WORKER}-${SID}.json"
LOG="/tmp/grok-first-${WORKER}-${SID}.log"
MAX_TURNS=30  # Set deliberately for this work order; reaching it is incomplete.

cleanup() { rm -f "$PROMPT"; }
trap cleanup EXIT HUP INT TERM

cat >"$PROMPT" <<'EOF'
Work only in <REPO>.

Goal: <observable outcome>
Scope: <paths/modules to inspect or change>
Repository instructions: <canonical instruction file and relevant rules>
Constraints: <rules; do not touch X>
Non-goals: <explicit exclusions>
Proof: run <exact command(s)>.

Finish this work order only. If a constraint prevents an honest solution, STOP
and report the exact blocker and numbers; do not work around the constraint.
Do not start adjacent work or the next PR.

Final report: files changed; commands run and their results; test output or
failure details; remaining risks; blockers; and whether the work is ready for
Claude Code review.
EOF

command grok --no-auto-update \
  --cwd "$REPO" \
  --session-id "$SID" \
  --no-memory \
  --verbatim \
  --model grok-4.6 \
  --reasoning-effort xhigh \
  --max-turns "$MAX_TURNS" \
  --always-approve \
  --output-format json \
  --prompt-file "$PROMPT" >"$OUT" 2>"$LOG"
```

- `command grok` bypasses aliases.
- `--prompt-file` avoids fragile quoting; `--verbatim` sends the work order
  exactly as written; `--no-memory` keeps the fresh-session contract honest.
- `--session-id` gives deterministic recovery. Never use `--continue` or an
  argument-less `--resume` when workers can run in parallel.
- `--output-format json` writes one machine-readable result. Inspect the result
  file deliberately; do not flood Claude's context by blindly dumping logs.
- `--no-auto-update` suppresses background update checks in documented headless
  scripting use.
- Pin `grok-4.6` and extra-high reasoning (`xhigh`) unless the work order
  intentionally selects a different locally available model.
- Make `MAX_TURNS` task-specific. Hitting the maximum is incomplete evidence,
  not success.
- `--always-approve` is only for an explicit, trusted repository and a scoped
  prompt. Prefer an isolated worktree for write tasks. Never use it for
  untrusted prompts, unknown directories, secrets, publishing, or destructive
  operations outside an explicitly approved land order.

For a long operation, launch the complete setup-and-Grok command as **one**
Claude Code Bash tool call with `run_in_background: true`. Each worker gets its
own tracked background call, unique `SID`, `OUT`, and `LOG`. Never fork multiple
workers from a shared shell launcher: that makes them invisible orphan processes.

## Follow-up and Recovery

A correction to the same bounded work order may resume its explicit session ID:

```bash
FOLLOWUP="$(mktemp -t grok-first-followup.XXXXXX)"
cat >"$FOLLOWUP" <<'EOF'
Fix only <specific issue>. Do not broaden scope. Re-run <exact verification>.
Report changed files, command output, and any remaining blocker.
EOF

command grok --no-auto-update \
  --cwd "$REPO" \
  --resume "$SID" \
  --no-memory \
  --verbatim \
  --always-approve \
  --output-format json \
  --prompt-file "$FOLLOWUP" >"$OUT" 2>"$LOG"
rm -f "$FOLLOWUP"
```

Monitor the tracked background command for completion. Do not treat a quiet log
as proof of a hang: Grok's documented logging does not promise a reasoning
heartbeat. Instead, set a task-specific wall-clock deadline before launch. At
the deadline, inspect whether the tracked worker/process is still active: if it
is, report a liveness incident, cancel that tracked worker, and resume the exact
`SID` with a narrowly scoped continuation prompt. Do not kill merely because
stdout or stderr has been quiet. If the active harness cannot inspect/cancel a
tracked job, do not claim watchdog coverage; timebox the delegation and return
control to Claude for an explicit recovery decision. After two unsuccessful
correction rounds, Claude takes over directly rather than looping.

## Prompt Contract

Every work order contains:

- **Goal:** observable desired outcome.
- **Scope:** repository path and exact relevant paths/modules.
- **Repository rules:** canonical instruction file and constraints that apply.
- **Constraints and non-goals:** including files that must not change.
- **Proof:** exact test, typecheck, lint, CI, or manual verification command.
- **Report shape:** changed files, real command results, risks, and blockers.
- **Stop condition:** complete only this order; do not begin adjacent work.

Every hard prohibition needs a sanctioned escape hatch. Pair “do not change X”
with “if X blocks an honest solution, stop and report why; do not work around
it.” A stop-report is a successful coordination result, not a failed worker.

For a multi-PR series, reuse the same frozen skeleton, cite landed precedents
and their idioms, carry newly discovered traps into the next order, and end
every order with an explicit instruction not to begin the next PR.

## Parallel Workers, One Repository

Parallelize only independent tasks. For concurrent write work, use one fresh
worktree and distinctive branch per worker, based on `origin/main`; Grok's
verified `--worktree <name>` and `--worktree-ref origin/main` can create the
isolation. Give every worker its own tracked background launch, worktree,
branch, `SID`, prompt, output, and log.

Use one shared frozen specification plus a target-specific header per worker.
Landing serializes on the repository's land-workflow lock: if a worker finds a
held lock, it backs off, waits, and retries the failed step. It never recovers a
lock it did not create or repeatedly chases `main` while sibling PRs land.

For a sequential PR series, reuse one worktree but rebranch from current
`origin/main` for each next PR.

## Coordinator Verification

Grok's report is evidence, not authority. After every worker run, Claude Code
must:

1. Inspect `git status --short` and the full diff; judge it as a contributor PR.
2. Check every changed file against the work order and canonical repository
   instructions.
3. Run focused proof itself or inspect the real command output. A model claim is
   advisory, not verification.
4. For a landed PR, verify against merged `origin/main`, not the worker report:
   read the actual public surface and naming; inspect squash history; diff-stat
   forbidden guard/budget/baseline files; and scrutinize test-helper edits that
   could hide an incomplete migration.
5. Run an independent frozen-change review before any ship or land. Use the
   repository's documented review workflow when it has one; otherwise Claude
   Code performs a fresh review pass distinct from the worker's report. This is
   mandatory even though Grok has no verified built-in `autoreview` command.
6. Iterate with the exact session ID only when a focused correction is justified;
   after two failures, take over directly.

## Completion Checklist

- [ ] Claude Code passed the hard gate and used an explicit repository path.
- [ ] The work order was self-contained, frozen, and included proof plus a stop condition.
- [ ] The worker used a fresh explicit session ID, `--no-memory`, and unique output/log paths.
- [ ] Parallel write workers used separate worktrees and branches.
- [ ] Any push/land operation was explicitly approved, attached to the exact head
  SHA, and reached successful/green CI before land.
- [ ] Claude inspected the complete diff and real verification evidence.
- [ ] A landed change was checked on merged `origin/main` and passed a mandatory
  independent frozen-change review plus any required repository closeout review.

## Economics

Win by moving generation and read-heavy exploration to Grok while Claude spends
tokens on the work order, actual changed surfaces, and verification. Do not
ping-pong trivia through delegation or reprocess Grok's narrative when the diff
and proof already answer the question.
