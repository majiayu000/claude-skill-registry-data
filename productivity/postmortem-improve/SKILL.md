---
name: postmortem-improve
description: >
  Run a postmortem → improve loop for LibrAgent multi-agent work so the harness
  organization gets better over time. Capture evidence-backed failures and friction,
  write a durable postmortem, then route each actionable to the right bundled skill
  (teamwork, org, org-restructure, boost, recruit, agent-init, delegation-eval-loop,
  schedule/loop). Use after incidents, repeated handoff failures, mission completion
  retros, stuck KANBAN/Blocked items, or when the user asks for continuous improvement,
  after-action review, postmortem, or org learning. Not for one-off task execution,
  initial team bootstrap (use teamwork), or first-time org create (use org).
---

# Postmortem → Improve

Close the loop: **observe failure → write truth → change the system**.

This skill owns the learning cycle. Specialist skills own the mutations.
Do not invent a parallel org model — improve the existing teamwork/org constitution.

## Not This Skill

| Skill | Use for |
| --- | --- |
| **teamwork** | First-time scaffold / choose substrate |
| **org** | Create org, spawn/resume org members |
| **org-restructure** | Apply role/constitution structural changes |
| **delegation-eval-loop** | Grade one child sprint (not fleet learning) |
| **boost** / **recruit** | Tune or create assistant configs only |
| **schedule** / **loop** | Recurring wake-ups (cadence only) |

## Core Rules

1. **Evidence before narrative.** Prefer coordination files, tool errors, session status, and diffs over memory.
2. **One postmortem, many actions.** Split findings into discrete, routed improvements — no mega-patch.
3. **Route, don't reinvent.** Each action maps to exactly one specialist skill (see routing table).
4. **Durable artifacts.** Write under the teamwork artifact directory (`@teamwork/...`), not chat-only conclusions.
5. **Refresh honesty.** `agents.md` / role-skill edits apply on a **later** execution step — say so after applying.
6. **Bounded ambition.** Prefer 1–3 high-leverage actions per cycle. Park the rest in backlog.

## When to Run

Trigger when any of these are true:

- A mission, sprint, or org objective finished (success or failure)
- The same failure class repeats (≥2 times): wrong owner, missing tool, stale handoff, eval soft-accept
- `coordination/KANBAN.md` has lingering **Blocked** or thrashing In Progress
- User asks for postmortem, retro, after-action, continuous improvement, or "learn from this"

If no teamwork artifact directory exists yet, stop and use **teamwork** first.

## Workflow

### 1. Anchor on the teamwork SSOT

1. Confirm artifact path via existing `.libragent/teamwork.json` / `@teamwork/`.
2. Read, in order: `MISSION.md` → `ROLES.md` → `agents.md` → `coordination/KANBAN.md` → `HANDOFF.md` → `RISKS.md` → `DECISIONS.md`.
3. If substrate is org: confirm `executionSubstrate.mode: "org"` and prefer the **org root** session for coordination writes.

### 2. Gather evidence (short)

Collect only what supports root-cause claims:

- Failed acceptance criteria / eval rejects
- Session terminals: cancelled, timeout, circuit-break, empty final text
- Ownership gaps (unowned KANBAN items, wrong role writes)
- Tool/config mismatches (missing MCP, bloated tools) via `agent__listAgents` / `tool__listServers` when relevant
- Optional: session trace excerpts — do not dump entire traces into the postmortem

### 3. Write the postmortem

Create:

```text
@teamwork/coordination/POSTMORTEMS/YYYY-MM-DD-<slug>.md
```

Use the template in [postmortem-template.md](references/postmortem-template.md).

Also append a one-line index entry to `@teamwork/coordination/LESSONS.md` (create if missing):

```markdown
- YYYY-MM-DD — <slug> — <one-line lesson> — actions: N open
```

### 4. Classify and route improvements

For each actionable, pick **one** route from [improvement-routing.md](references/improvement-routing.md).

| Action type | Route to |
| --- | --- |
| Role add/layoff/merge, constitution edit | **org-restructure** |
| Missing coordination files / role skills / framework mismatch | **teamwork** (tighten scaffold) then **org-restructure** if org exists |
| Assistant tool add/remove vs role | **boost** |
| New specialist config needed | **recruit** |
| Workspace `agents.md` / guide drift (non-org) | **agent-init** |
| Weak acceptance criteria / soft "done" | **delegation-eval-loop** (update brief/eval habit) |
| Recurring retro cadence | **schedule** (global) or **loop** (in-session) |

Write each action as a KANBAN item under **Backlog** or **In Progress** with owner + target skill name.

### 5. Apply (execute the routes)

1. Record intent in `coordination/DECISIONS.md` (what changes and why).
2. Invoke the specialist skill(s) for the top 1–3 actions **now**.
3. Leave lower-priority actions as KANBAN backlog with clear owners.
4. Update `LESSONS.md` action counts; move finished items to Done.

### 6. Verify the learning stuck

Before declaring the cycle complete:

- [ ] Postmortem file exists and links evidence
- [ ] At least one durable change landed (constitution, role skill, config, or eval contract) **or** an explicit deferred KANBAN item with owner
- [ ] Org/team members are told refresh applies next step when constitution changed
- [ ] No duplicate "learning" left only in chat

## Cadence (optional)

For long-lived orgs, propose a lightweight recurring review:

- Weekly: scan Blocked + LESSONS.md open actions → run this skill if new friction
- After each major mission: mandatory postmortem even on success (capture near-misses)

Use **schedule** for org-wide cadence; **loop** only for a reminder inside the current conversation.

## Guardrails

- Do not rewrite history to protect a role — blame systems (contracts, tools, handoffs).
- Do not dissolve the org or recreate `agent__createOrg` as "improvement".
- Do not apply every idea — prefer reversible, measurable changes.
- Do not mix boost (existing configs) with recruit (new configs) in one vague patch.
- Do not skip writing `POSTMORTEMS/` because "we already talked about it".

## References

- [Postmortem template](references/postmortem-template.md)
- [Improvement routing matrix](references/improvement-routing.md)
