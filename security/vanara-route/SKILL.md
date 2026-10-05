---
name: vanara-route
description: Given a task, find the best-fit installed Vanara agent and run it. Reads the installed agent roster, scores each by how well its stated purpose matches the task, delegates to the strongest match, and — when nothing fits — records the gap so you can request the missing agent. Use when you are not sure which specialist should handle a job, or you want the toolkit to pick for you.
type: skill
version: 1.0.1
updated: 2026-07-27
---

# vanara-route — the dispatcher

You are routing a task to the **best-capable installed agent**, then handing off to it.
Claude Code already auto-selects agents from their descriptions; this skill adds two things
on top: an *explicit* "pick the strongest specialist for this exact task" step you can invoke
on demand, and a **gap-capture** path for when the toolkit has nothing that fits.

## When to use

- The user asks "which agent should handle X?" or "use the right agent for this."
- A task spans several specialties and you want the single best owner (or a short list).
- You suspect no installed agent covers the task and want that recorded, not silently dropped.

## The routing procedure

1. **Enumerate the roster.** Run `node .claude/skills/vanara-route/scripts/roster.mjs` (or read
   `.claude/agents/*.md` directly) to list every installed agent with its `name` and
   `description` — the path is from your project root, where Claude Code runs. The description
   is the agent's own statement of when it should be used — treat it as the primary signal.

2. **Score each candidate against the task.** For every agent, judge fit on:
   - **Domain match** — does the task fall in this agent's stated domain? (a Terraform change
     → `iac-author`; a failing test → `test-author`; a slow query → `database-administrator`).
   - **Verb match** — does the agent *do* what the task needs (review vs. write vs. audit vs.
     plan)? A read-only reviewer is the wrong pick for "implement".
   - **Proactivity cues** — descriptions that say "Use PROACTIVELY when …" are strong matches
     for exactly those triggers.
   Assign each a confidence: **strong / partial / none**.

3. **Act on the best match.**
   - **One strong match** → delegate the task to that agent (invoke it via the Task tool) and
     return its result. Say which agent you chose and why in one line.
   - **Several strong matches** (e.g. review + security on the same diff) → run them in the
     order the work implies, or present the short list and let the user pick.
   - **Only partial matches** → name the closest agent, state plainly that it is an approximate
     fit, and ask before running it.
   - **No match** → do **not** improvise a fake specialist. Record the gap (next section).

4. **Never fabricate a specialist.** If the roster has no agent for the job, routing has
   failed on purpose — that failure is a signal, not something to paper over.

## Recording a gap (when nothing fits)

When no installed agent covers the task, append one line to the local gap log so it is not
lost. Do this with the helper (it is append-only and creates the file if needed):

```bash
node .claude/skills/vanara-route/scripts/log-gap.mjs "one-line capability that was missing"
```

This writes to `~/.vanara/gaps.jsonl` **on the user's machine only** — nothing is sent
anywhere. Then tell the user, in one sentence, that they can submit the request with
`vanara request` (which prepares an email to the Vanara team; the user sends it, or not).
See [references/gap-reporting.md](references/gap-reporting.md) for the privacy model.

## Edge cases and failure modes

- **Empty roster** (nothing installed yet): tell the user to `npx vanara install <name>` or
  `vanara list` first; there is nothing to route to.
- **Over-eager matching:** a vaguely-related description is a *partial* match, not a strong
  one. Prefer asking over running the wrong specialist on a real task.
- **Ambiguous verbs:** "fix the auth bug" implies reproduce → test → patch → review, which is
  an *orchestration* job — prefer an orchestrator pack if one is installed over a single agent.
- **Secrets:** never write task contents, code, credentials, or customer data into the gap
  log — only a short, generic description of the missing capability.
- **Do not loop:** route once. If the chosen agent itself can't finish, report that back to
  the user rather than re-routing endlessly.

## Example

> **Task:** "our Terraform plan keeps showing drift on the prod VPC — figure out why."
>
> Roster scan → `iac-author` (writes/refactors IaC) is a *partial* verb match (this is
> diagnosis, not authoring); no dedicated drift-diagnosis agent exists. Route names
> `iac-author` as the closest fit, flags it as approximate, and logs the gap
> *"Terraform drift diagnosis / state reconciliation"* so it can be requested.

See [references/matching-heuristics.md](references/matching-heuristics.md) for the full scoring
rubric and worked examples.

## Worked micro-example

```text
$ task: "our checkout p99 doubled since Tuesday"

ROUTE SCORING (installed items):
  debugger              0.86  ← symptom is a regression, not a design ask
  perf-optimizer        0.79     (would optimize; can't explain "since Tuesday")
  sql-index-tuning      0.61     (plausible cause, wrong entry point)
  incident-responder    0.44     (no user-facing outage declared)

DECISION: debugger — a dated regression wants hypothesis-driven bisection
first; perf work without the culprit is guessing with a profiler.
HANDOFF: debugger gets the task + the "since Tuesday" anchor + last deploys.
```

Routing is a ranked decision with reasons, and the runner-up matters: if
debugger's bisection lands in a query plan, sql-index-tuning is next, and the
route log already says why.
