---
name: next
description: "\\\"What should I work on next?\\\" — two modes. Fast mode (default): one-shot recommendation from docs + git state, ≤15 lines, no interview. Deep mode (`/next deep` or when user asks to explore priorities): multi-round interview to surface the best move."
---

# Clade for Codex

This workflow runs **directly in Codex**. Do not launch the `claude` CLI or
delegate the workflow to Clade's MCP bridge.

Codex compatibility rules:

- Plugin skills are namespaced. Invoke this workflow explicitly as
  `$clade:next`; a bare `$name` does not select the installed Clade plugin.
- Read the nearest `AGENTS.md` files for repository instructions. If a project
  has only `CLAUDE.md`, treat it as legacy project guidance and read it too.
- Store new Clade working state under `.clade/` (or `~/.clade/` for personal
  state). Existing legacy Claude state may be read for migration, but do not
  create new vendor-specific state.
- A `/skill-name` reference means the corresponding Codex
  `$clade:skill-name` plugin skill, or the same workflow invoked naturally when
  explicit skill invocation is not available.
- Use Codex web, file, shell, image, and subagent capabilities when the source
  workflow names a vendor-specific tool. If a capability is unavailable, use
  the documented fallback instead of spawning another agent CLI.
- Paths such as `<plugin-root>/...` are relative to the installed Clade plugin
  containing this `SKILL.md`; resolve that root before invoking a helper.

## Canonical Clade workflow

You help the user pick the best next move. Two modes, picked automatically unless the user forces one.


## Weigh findings by whether the layer runs

Before ranking anything, read `docs/layers.json`. It declares which surfaces of
this repository are actually run and how much a finding in each one is worth:

- **load-bearing** — a defect here is a defect. Rank normally.
- **dormant** — builds and passes CI but is not run. Report findings, and rank
  them *below* any load-bearing finding. Do not propose deleting the layer and
  do not present its gaps as debt; new work there is opt-in.
- **generated** — never edit directly. The finding belongs in the source surface
  plus its regen script, not in the copy.

This exists because an audit of this repository spent most of its effort on the
orchestrator, a layer the owner had switched off months earlier. Nothing in the
tree said so, so the effort looked well spent right up until it was reported.

---

## Mode selection

**Fast mode** (default for drive-by asks like "下一步做什么"):
- User invoked with no arg, OR with `fast` / `quick`, OR it's a short single-line question with no context about priorities being unclear.
- One-shot: read docs + git state, recommend top pick + runner-up, stop. No interview.
- Target output: ≤15 lines.

**Deep mode** (full multi-round interview):
- User invoked with `deep`, OR they explicitly say they're stuck / unsure / want to explore.
- Runs the Framing Check → Round 1 → Round 2 → Round 3 → Synthesis flow below.

If in doubt, start in fast mode and offer deep mode at the end: `Want to go deeper? /next deep` — the user can always escalate, but forcing them through 3 rounds for a casual ask wastes their time.

All estimates use **AI-agent speed**, not human programmer speed (see Time Scale Reference below).

---

## Time Scale Reference (Codex speed)

| Human estimate | Codex equivalent |
|---|---|
| "a few hours" | 5–15 min (one focused session) |
| "half a day" | 20–40 min |
| "1 day" | 1–2 hours of agent time |
| "1 week" | 3–6 hours across sessions |
| "2+ weeks" | multi-session /loop, needs phasing |

When the user mentions effort, translate it: "you said 'a day of work' — that's probably one 30-min /loop run."

## Task Type Reference

**Execution task**: Requirements are clear, outcome is known. Just run it.
**Discovery task**: Requirements are fuzzy or outcome is uncertain. Run a 10–20 min spike first to reduce unknowns before committing to a full implementation.

Always distinguish these. A discovery task disguised as an execution task is the #1 cause of stalled autonomous runs.

---

---

## Fast mode — one-shot recommendation

Use when the user fired `/next` casually or with `fast`. Do all of this silently, then output.

1. Read `TODO.md`, `PROGRESS.md`, `GOALS.md` if present (≤1 Read each; skip missing).
2. `git log --oneline -10` and `git status -sb` for momentum signal.
3. Pick **top 1** (and optional runner-up) using this priority order:
   - In-progress / half-done items from PROGRESS.md that block other work
   - Stalled items the user last referenced but never closed
   - Highest-signal TODO item that fits a single 20-min agent run

Output template (≤15 lines, no headers beyond these):

```
→ Top pick: {task}
  Type: {Execution | Discovery (needs spike)}
  Why: {one clause, referencing what you saw in docs/git}
  Done when: {observable criterion}
  Estimate: {one agent-session equivalent}

→ Runner-up: {task} — {when to pick this instead}

Parking lot: {1–3 items noted but not urgent, one line each} (omit if none)

Want to go deeper? /next deep
```

Then STOP. Don't ask a question. Don't run rounds. If the user agrees, they'll say so; if they want alternatives, they'll escalate with `/next deep` or name a different pick.

Skip Framing / Round 1 / Round 2 / Round 3 / Final Synthesis sections below — those belong to deep mode only.

---

## Deep mode — multi-round interview

Runs only when the user invoked `/next deep`, or fast-mode judgment said "this isn't a drive-by — they actually want to think."

### Setup — Read Context First

Before asking anything, read the project docs silently:
1. `GOALS.md` — vision, phases, north star
2. `PROGRESS.md` — what worked, what broke, current momentum
3. `TODO.md` — backlog (prioritization, in-progress, stalled items)
4. `BRAINSTORM.md` — unprocessed inbox

Build a mental model:
- What phase is this project in? (exploration, active build, stabilization, scaling?)
- What's the planning horizon implied by the backlog?
- What looks stalled, blocked, or abandoned?
- Which items are fuzzy problems vs. clear tasks?
- Which items could run in parallel (no shared state)?

**If any file is missing, that itself is a signal.**

---

## Pre-Round: Framing Check

Before scanning the backlog, do a framing check. Ask **1–2 questions** to validate the problem space — NOT to score tasks, but to check if the backlog itself is tracking the right things.

Ask one or two of these (pick the most relevant):
- "Looking at the TODO list — are there items you listed weeks ago that you're no longer sure are worth doing? What's changed?"
- "Is there a gap between what's in the TODO and what the project actually needs right now? What's NOT on the list?"
- "What would 'done enough to ship / hand off / stop worrying' look like for the most important open item?"

Wait for the user's answers. This often surfaces the real priority before Round 1 even starts.

---

## Round 1 — Wide Scan

Ask 4–5 targeted questions, one per angle. Present as a numbered list; ask the user to answer all before you continue.

Cover BOTH immediate and longer-horizon angles.

**Angles (pick the most relevant given context):**
- **Pain (immediate)**: What's the most broken/slow/frustrating right now? (What actually hurts, not what's in the TODO)
- **Momentum**: What's half-done or "almost there" and blocking other things?
- **Phase horizon**: Where does the project need to be in 2–4 weeks? Is the current backlog tracking toward that, or is there a gap?
- **Discovery opportunity**: Are there items in the TODO where you don't yet know HOW to do them? (vs. items you know exactly how to implement)
- **Risk horizon**: What technical debt or deferred decision will cause the most pain in 2–4 weeks if left unaddressed?
- **Parallelism opportunity**: Are there independent workstreams that could run simultaneously in separate worktrees?
- **Energy**: What are you most excited to work on — even if it's not the "right" priority?

Rules:
- Each question MUST reference something specific from the project docs ("I see X is still open — is that still live?")
- At least one question should probe a longer horizon (weeks, not just today)
- At least one question should probe task clarity (discovery vs. execution)
- Short, sharp, specific — one sentence each

---

## Round 2 — Dig Deeper

Pick 2–3 most interesting threads from Round 1 — ones with tension, uncertainty, or outsized impact.

For each thread, ask a follow-up that challenges assumptions or surfaces hidden constraints:

**Follow-up angles:**
- **Root cause**: "You mentioned X is blocking — what's actually causing that? Code problem, design problem, or missing clarity?"
- **Discovery check**: "When you say X needs to be done — do you know *how* to implement it, or is the approach still unclear? Should we run a 15-min spike first to map it out?"
- **Unknown unknowns**: "What could a quick 15-min exploration reveal that might change how we approach X? Is there something we should learn before committing to it?"
- **Scope reality**: "What's the MVP of X — the part that a single agent run could complete and still be valuable? What's the rest?"
- **Dependency trap**: "If you start X, what needs to be true first? DB schema? Another module? An API key you don't have?"
- **Sequencing vs. parallelism**: "Could X and Y run simultaneously in two worktrees? Or does Y depend on X's output?"
- **Unlock effect**: "Once X ships, what does it unblock? Is there a cascade of value, or is it standalone?"
- **The avoided thing**: "You didn't mention Y (from TODO/PROGRESS) — intentional? Still relevant or quietly stale?"
- **Horizon mismatch**: "Your immediate answer was about today, but your phase goal needs Z by week 4 — is there a gap we're not addressing?"

Ask 2–3 follow-ups. NOT all of the above — only the ones relevant to what the user said.

---

## Round 3 — Prioritization Challenge

Narrow to the top 2 candidates. Stress-test the front-runner:

- "You're leaning toward X — but why not Y? What does Y lack?"
- "If the next agent run can only do ONE thing, which survives the cut?"
- "What's the atomic version of X — completable in a single 20-min session with clear value?"
- "Is X an execution task (you know how) or a discovery task (you need to explore first)? If discovery — what's the spike?"
- "If X gets 80% done and the agent stops — is partial progress useful, or just noise?"
- "What's the confidence level on the estimate? 1 = wild guess, 5 = done similar before"

---

## Final Synthesis

After 3 rounds, synthesize into a structured plan optimized for Codex autonomous runs:

```
## Next Steps Plan

**Top pick**: [task name]
Type: [Execution | Discovery → spike first]
Why: [1–2 sentences from the conversation]
Risk: [main risk or open question]
Done when: [concrete, observable acceptance criteria]
Agent estimate: [e.g. "one 20-min session" / "2–3 sessions" / "needs /loop"]
Confidence: [1–5, with reason]
Parallelizable: [yes/no — if yes, which subtasks split into worktrees?]

IF Discovery task:
  Spike first: [10–20 min agent run to answer: "X?" before committing]
  Spike done when: [what the spike produces — a design doc, proof of concept, list of constraints]

**Runner-up**: [task name]
When to choose this instead: [condition — e.g. "if top pick blocked by X"]
Agent estimate: [same format]

**Sequencing**:
→ Do [A] first (it unblocks B), then [B] can run independently.
OR
→ [A] and [B] are independent — run in parallel worktrees.
OR
→ Spike [A] first (15 min), then decide between [B] and [C] based on findings.

**Parking lot** (surfaced but not urgent):
- [item] — [why it surfaced, why not now]
```

Then ask: "Want me to write this into TODO.md and BRAINSTORM.md?"

If yes:
- Add top pick + runner-up to `TODO.md` at appropriate priority with checkbox and agent-time estimate in brackets:
  `- [ ] Task name [~20 min agent run, confidence 4/5]`
- If discovery task, add the spike as a separate preceding item:
  `- [ ] Spike: explore X approach [~15 min, unblocks task above]`
- Add parking lot items to `BRAINSTORM.md` tagged `[next-session YYYY-MM-DD]`
- Match the tone/format of existing entries in each file

---

## Conversation Rules

- **One round at a time** — wait for answers before proceeding
- **Reference specifics** — every question must show you read the docs
- **Framing before scoring** — don't rank tasks before validating the problem is worth solving
- **Challenge, don't validate** — if user says "I should do X", ask "why X over Y?"
- **Surface the unspoken** — the best insight is usually what the user *didn't* mention
- **Distinguish discovery from execution** — fuzzy tasks need a spike, not a timeline
- **Use AI-speed framing** — say "one session" not "a few hours", "/loop run" not "a week of work"
- **Think in parallel** — always ask "can any of this run simultaneously?" before settling on sequential plans
- **If no project docs exist** — use `git log` + file structure to infer context, then ask what the project is for before starting


---

## Completion Status

- ✅ **DONE** — task completed successfully
- ⚠ **DONE_WITH_CONCERNS** — completed but with caveats to note
- ❌ **BLOCKED** — cannot proceed; write details to `.clade/blockers.md`
- ❓ **NEEDS_CONTEXT** — missing information; use AskUserQuestion

**3-strike rule:** If the same approach fails 3 times, switch to BLOCKED — do not retry indefinitely.

## Delivery completion

If this workflow changes files or external state:

- Inspect the real final state before responding, including `git status` for a
  repository task.
- Never report `DONE` while task-owned changes are uncommitted. Use or continue
  `$clade:delivery` and create a repository-compliant checkpoint or preserve
  the work when committing is unavailable.
- When the user request or trusted repository policy makes publication,
  deployment, or live verification part of the task, do not silently downgrade
  the result to local-only work.
- If a required delivery transition lacks authority, credentials, a destination,
  or reachable external state, report `BLOCKED` or `NEEDS_CONTEXT` rather than
  appending a "not committed/pushed/deployed" caveat after `DONE`.
