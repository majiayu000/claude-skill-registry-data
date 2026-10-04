---
name: feature-pipeline
description: >-
  Multi-agent exploration-to-PR pipeline for safely exploring, fixing, and
  shipping a feature or CLI. Use when the user says: "explore X", "test and
  ship X", "run the pipeline on X", "run /feature-pipeline on X", "let's
  properly investigate X", "stress-test X and file issues", or "take X
  through the full pipeline." Also triggers on: "find what's broken in X",
  "test X end-to-end", "do a sandbox review of X", "file issues for X and
  fix them." Do NOT use for single-file bug fixes or one-off edits — the
  overhead is only justified when exploration, planning approval, and CI
  watching all matter. Manages state via scripts/state.sh (jq required).
  Five phases: LIGHTER explores → ORCHESTRATOR drafts PR → HEAVIER plans
  (user approves first) → ORCHESTRATOR commits → HEAVIER sandbox review →
  LIGHTER iterates CI → LIGHTER drift check + summary. Four mandatory stop
  hooks (M1–M4) gate each phase transition.
version: 2.0.0
argument-hint: "<feature-or-cli-to-explore>"
---

# feature-pipeline

A five-phase exploration-to-PR pipeline. The currently active agent acts as
**ORCHESTRATOR** — it coordinates two sub-agents (LIGHTER and HEAVIER) and
holds pipeline state. Sub-agents do all the work; the ORCHESTRATOR should
produce no more than 50% of total pipeline output.

```
Phase 1 ── LIGHTER explores → files GitHub issues           [STOP M1]
Phase 2 ── ORCHESTRATOR drafts PR + HEAVIER plans
           → user approves → ORCHESTRATOR commits           [STOP M2]
Phase 3 ── HEAVIER RED/GREEN sandbox review → PR comment    [STOP M3]
Phase 4 ── LIGHTER iterates on comment + watches CI         [STOP M4]
Phase 5 ── LIGHTER drift check → user summary
```

When sub-agent spawning is unavailable, write a Handover and pause. The
pipeline is only valuable if the right model tier does the right work.

---

## Setup — State File

Before Phase 1, initialise pipeline state (requires `jq`):

```bash
bash .claude/skills/feature-pipeline/scripts/state.sh init "{{feature}}"
```

This writes `.fp-state.json` with all fields at their defaults. Use `state.sh
set <key> <value>` and `state.sh push <key> <value>` throughout phases to
track progress. `state.sh show` at any point gives the full snapshot.

---

## Terminology

| Label | Meaning |
|-------|---------|
| **ORCHESTRATOR** | The currently active agent. Coordinates, drafts the PR, gates approval, commits, and holds state. Never explores, plans, implements, or reviews directly. |
| **LIGHTER** | One capability tier below ORCHESTRATOR. Faster and cheaper — suited to exploration and CI watch. If ORCHESTRATOR is already at base tier, LIGHTER = same tier. |
| **HEAVIER** | One capability tier above ORCHESTRATOR. Deeper reasoning — suited to planning and adversarial review. If ORCHESTRATOR is at apex, HEAVIER = same tier. |

### Harness compatibility

| Harness | Spawn mechanism |
|---------|-----------------|
| Claude Code | `Agent` tool (`subagent_type`, `model`) |
| Cursor | Background agents / `@agent` — pass brief as system prompt |
| Codex CLI | `codex run --agent --instructions "..."` |
| Windsurf Cascade | Cascade sub-tasks — delegate via task handoff |
| Other / unknown | Trigger Handover Protocol (see below) |

---

## Phase 1 — Feature Exploration (LIGHTER)

The goal is a complete picture of what's broken before anyone writes a fix.
LIGHTER approaches `{{feature}}` as a first-time user, exercising every
interesting edge so issues get filed while observations are fresh.

Spawn LIGHTER with this brief:

> You are a developer sandbox-testing `{{feature}}` for the first time. Invoke
> it in at least five distinct ways: happy path, edge cases, invalid inputs,
> flag combos, piped output. Note every footgun, unintuitive behaviour, unclear
> error, or doc gap. File one GitHub issue per distinct finding:
> - Title: `[{{feature}}] <short description>`
> - Labels: `exploration`, `needs-triage`
> - Body: steps to reproduce / expected / actual / severity (low | medium | high)
>
> End with a severity table of all issues filed.

After LIGHTER reports: `state.sh push issueNumbers <N>` for each issue,
`state.sh set phase 2`.

If spawning fails, write a [Handover](#handover-protocol) with `role: LIGHTER`,
`task: Phase 1 exploration`, `context: {{feature}}` — do not explore yourself.

**→ STOP HOOK M1** — print the banner, wait for user input before Phase 2.

---

## Phase 2 — Plan & Draft PR (ORCHESTRATOR + HEAVIER)

ORCHESTRATOR does these steps directly — this is its core authoring work:

1. Read Phase 1 issues → write a one-paragraph **Problem Statement**.
2. Create branch `fix/{{feature}}-findings-<slug>`.
3. Open a **draft** PR:
   - Title: `fix({{feature}}): address exploration findings`
   - Labels: `draft`, `needs-plan`
   - Body: Problem Statement + `Closes #N` links + `## Plan` placeholder.
4. `state.sh set branch <name>` and `state.sh set prUrl <url>`.

Then spawn HEAVIER with the issue bodies, PR URL, and relevant source excerpts.
HEAVIER produces a **numbered implementation plan**:

```
1. <file/area>  —  <change>  —  <rationale>  [⚠ breaking | ⚠ test-only | ⚠ schema]
2. …
```

Present the plan to the user. Zero implementation commits until explicit
approval — because an unreviewed plan means unreviewed code, and that defeats
the purpose of the HEAVIER planning tier. Accept corrections ("change step 3
to …", "skip step 2"). Update PR body `## Plan` with the approved plan.
`state.sh set planApproved true`.

After approval, ORCHESTRATOR implements step by step:
- One atomic commit per plan step: `<type>(<scope>): <desc>`
- Remove `needs-plan`, add `in-progress`
- Push

Programmatic-First rule applies: registry mutations via `gaia dev` commands —
never hand-edit `registry/nodes/`.

If HEAVIER spawning fails, write a [Handover](#handover-protocol) with
`role: HEAVIER`, `task: Phase 2 planning` — do not plan yourself.

**→ STOP HOOK M2** — print the banner, wait for user input before Phase 3.

---

## Phase 3 — Sandbox Review (HEAVIER)

Spawn a fresh HEAVIER in `isolation: worktree` with the PR branch checked out.
Worktree isolation prevents a broken review from dirtying the working branch.

Brief:

> Read the full diff (`git diff origin/main...HEAD`). For each changed public
> surface or behaviour: write a RED test (must fail before the fix — verify by
> temporarily reverting, running, re-applying) and a GREEN test (must pass with
> fix). Run `gaia dev validate` for schema changes; `gaia dev docs --check` for
> doc changes. Post this review comment to the PR:
>
> ```markdown
> ## Sandbox Review
>
> ### RED tests
> | Description | Result | Notes |
> |-------------|--------|-------|
>
> ### GREEN tests
> | Description | Result | Notes |
> |-------------|--------|-------|
>
> ### Issues found
> - [ ] <description> — `<file>:<line>`
>
> ### Verdict: APPROVE / REQUEST CHANGES
> ```

After comment is posted: `state.sh set reviewCommentUrl <url>`.

If spawning fails, write a [Handover](#handover-protocol) with
`role: HEAVIER`, `task: Phase 3 sandbox review` — do not review yourself.

**→ STOP HOOK M3** — print the banner, wait for user input before Phase 4.

---

## Phase 4 — Iterate & Watch CI (LIGHTER)

Spawn LIGHTER (same agent as Phase 1 if context is intact, else fresh) with
the PR context and the Phase 3 review comment URL. Reusing the Phase 1 agent
when possible avoids re-establishing feature context.

Brief:

> Read the review comment. For each `[ ] issue`: fix, commit
> (`fix(<scope>): <desc> (per review)`), push. Subscribe to CI events. On
> each failure: read logs, diagnose root cause, push targeted fix. Do not
> exit until all required checks pass. On CI green: remove `draft` status,
> swap `in-progress` → `ready-for-review`. If the same check fails 3× with
> no new diagnosis, escalate to ORCHESTRATOR with the exact log excerpt.

`ciRound` in state tracks CI attempts — LIGHTER should increment it via
`state.sh set ciRound <N>` before each push. This makes the 3× escalation
threshold auditable.

If spawning fails, write a [Handover](#handover-protocol) with `role: LIGHTER`,
`task: Phase 4 CI watch` — do not watch CI yourself.

**→ STOP HOOK M4** — print the banner, wait for user input before Phase 5.

---

## Phase 5 — Drift Check & Summary (LIGHTER)

Spawn LIGHTER for the final hygiene pass.

Brief:

> `git fetch origin main` → `gaia dev diff`. If unexpected drift: print a
> warning table (skill ID / field / main value / branch value) and pause —
> do not auto-fix drift, because silent registry mutations are the main
> source of hard-to-audit regressions. If clean: send the user the final
> summary (feature explored, issues filed with links, PR URL + title, CI
> status, commit list, what was fixed). All agents exit.

Exception: if spawning is unavailable here, ORCHESTRATOR may run the drift
check and summary itself — Phase 5 is lightweight and terminal.

---

## Stop Hooks

Stop hooks are mandatory pauses. They exist because each phase handoff is a
natural review point where the user may want to change course before work
compounds. ORCHESTRATOR prints the banner and ends the turn — it does not
auto-advance.

| Hook | After | Review | User options |
|------|-------|--------|--------------|
| **M1** | LIGHTER files last issue + severity table | Issue list, severity | `continue` → Phase 2 · `stop` · `add: <notes>` |
| **M2** | ORCHESTRATOR pushes implementation commits | PR diff, commit list | `continue` → Phase 3 · `stop` · `amend: <notes>` |
| **M3** | HEAVIER posts review comment | Verdict, `[ ]` items | `continue` → Phase 4 · `stop` · `override: <notes>` |
| **M4** | LIGHTER reports CI green + PR ready | Final PR state | `continue` → Phase 5 · `stop` |

**Banner format:**
```
╔══ STOP HOOK M<N> ════════════════════════════════════════════════════════════╗
║  <one-line summary of what just completed>                                   ║
║  Review above, then reply: continue · stop · <feedback>                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Handover Protocol

When sub-agent spawning is unavailable, write a handover and pause — never
do the sub-agent's work yourself. Handing off preserves model-tier separation,
which is the whole point of the pipeline.

**Storage:** `./feature-pipeline-handover-{{feature}}.md` on disk; PR comment
if filesystem is unavailable.

```markdown
## Feature Pipeline Handover — Phase <N>

**Feature**: {{feature}}
**Timestamp**: <ISO 8601>
**PR**: <URL or "not yet created">
**Branch**: <name or "not yet created">

### Role needed
LIGHTER | HEAVIER

### Task
<paste the exact Phase brief from this skill — do not paraphrase>

### State snapshot
<contents of .fp-state.json — or paste from state.sh show>

### Resume steps
1. Read this document.
2. Complete the Task above as the specified role.
3. Update .fp-state.json (or the PR comment) when done.
4. Write a Phase <N+1> handover or post a completion note and notify ORCHESTRATOR.
```

After writing, print:
```
⚠  Sub-agent spawning unavailable.
   Handover written → <path or "PR comment">
   Assign task to a <LIGHTER | HEAVIER> agent, then reply 'continue'.
```

Then end the turn.

---

## Key Rules (condensed)

- **One PR per run** — all Phase 1 issues close in a single PR.
- **No commits before plan approval** — HEAVIER's plan gates all implementation.
- **No force-pushes** — commits append only; rebase only on explicit user request.
- **Drift → warn, never auto-fix** — Phase 5 surfaces drift as a table and pauses.
- **CI loop has no exit until green** — or 3× same failure triggers escalation.
- **Phase order is strict** — Phase N+1 does not start until Phase N stop hook is cleared.

---

## Invocation

```
/feature-pipeline <feature>
```

If `<feature>` is omitted, ask: "Which feature or CLI should I explore?"

**Examples:** `gaia scan` · `packages/cli-npm` · `the --canon flag` · `gaia skills install`

---

## Phase banner (sub-agents)

Sub-agents print at phase end:
```
── Phase <N> complete ─────────────────────────────────────────────────────────
```
ORCHESTRATOR prints stop-hook banners separately. Neither should be suppressed.
