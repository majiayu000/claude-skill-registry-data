---
name: factory
description: Use this skill whenever the user wants to run multiple side projects in parallel via an AI org chart. Also trigger when the user says "/factory", "ship multiple side projects in a day", "hire an AI company", "run my side-project portfolio", or "scale beyond one harness". Takes a company goal + monthly budget + 3-5 side-project ideas + stack defaults + day-plan start time, then installs Paperclip, creates a company with budget cap, hires a 3-5 agent org chart (CEO + CTO + 2 engineers + marketer for 5 projects), wires per-agent budgets and heartbeats, drops in a 12-hour day-plan calendar with explicit human-attention windows. Companion to /autopilot — assumes the reader has shipped at least one /autopilot run before. Human-in-the-loop at the four daily attention windows (9am standup / 1pm checkpoint / 5pm gate review / 9pm daily review).
---

# Factory — Run Multiple Side Projects In Parallel

Hire an AI org chart that ships your side-project portfolio on a Saturday. One company. 3-5 agents. 5-piece setup. Companion to [/autopilot](../autopilot) — assumes the reader has shipped at least one autopilot run before.

Ship With AI artifact #25 · post-LtM methodology · companion to [How To Build A Factory From Your Agent Harnesses](https://shipwithai.substack.com/).

## When to run

Invoke when the user:

- Types `/factory` or `/factory "<company goal>"`
- Asks to "run multiple side projects in parallel," "hire an AI company," "scale beyond one harness," "run my portfolio"
- Has at least one shipped `/autopilot` run and wants to scale to 3-5 projects in parallel

Do NOT invoke when the user wants to:

- Ship a single side project (use [/autopilot](../autopilot) instead — factory is overkill for one project)
- Run an autonomous overnight session on a single project (use [night-shift](../night-shift) instead)
- Plan a feature inside an already-shipped project (use [collect-feedback](../collect-feedback))
- Coordinate a team of HUMANS (this skill is for AI agents under one human supervisor)

## Input surface

- `/factory` → operate on the user's current portfolio root directory
- `/factory "<company goal>"` → operate on cwd with the goal pre-filled

If `cwd` is not the user's portfolio root (e.g. they're inside one project), warn and ask whether to step up to the portfolio root before proceeding.

## Process

### Phase 1 — Discovery (silent, ~15 seconds)

Read, in order:

1. `git status` and `pwd` — confirm we're in a portfolio root, not a single-project subdir
2. Check for an existing `~/.paperclip/` install — if Paperclip is already running, note the existing companies and warn before creating another
3. Check `CLAUDE.md` for existing `## Lessons` section in the portfolio root
4. Check for existing per-project `idea.md` / `user.md` / `stack.md` — note overwrite risk
5. Verify the user has run `/autopilot` at least once before (look for any `.archon/workflows/` or any `done.md` files in subdirs); if not, recommend they install autopilot first

Do not print anything user-facing during this phase.

### Phase 2 — Interview (exactly five questions)

Ask these five questions, in this order, and wait for the user to answer each before proceeding. Do **not** ask follow-up questions. Five questions is the budget.

**Q1.** What's the company goal? (One sentence. The arch goal that all 3-5 side projects ladder up to.)

> Example: "Ship 5 micro-SaaS prototypes to first-users by end of May to find which one has retention."

**Q2.** What's your monthly budget across the whole company? (In USD. Paperclip enforces atomically — agents stop at cap.)

> Example: "$50/month."

**Q3.** What are the 3 to 5 side-project ideas? (One line each. Just the title or one-sentence description.)

> Example: "1. Bedtime story generator. 2. Receipt OCR for freelancers. 3. CSV-to-chart Slack bot. 4. Gym log with photo proof. 5. Side-project deadline tracker."

**Q4.** What's your stack default for the portfolio? (Language, framework, deploy target. One line each.)

> Example: "TypeScript, Next.js 14 app router, Vercel."

**Q5.** What time does your factory day start? (HH:MM in your local timezone. Used to schedule the four daily attention windows: standup, checkpoint, gate review, daily review.)

> Example: "09:00 GMT+2."

All other calibration comes from Phase 1 discovery. Do not ask follow-ups.

### Phase 3 — Scaffold (silent, ~60 seconds)

1. If Paperclip is not installed: run `bash ${SKILL_DIR}/scripts/install-paperclip.sh`.
2. Create the company via `POST /api/companies` with `name` (derived from Q1), `issuePrefix` (3-letter slug), `budgetMonthlyCents` (Q2 × 100). Capture the returned `companyId`.
3. For 5 projects: hire CEO + CTO + Engineer × 2 + Marketer. For 3 projects: hire CEO + Engineer × 2 + Marketer (skip CTO). For 4 projects: hire CEO + CTO + Engineer × 2 (skip Marketer).
4. Per-agent budget split:
   - CEO: 10% of company budget
   - CTO: 30% of company budget
   - Engineer × 2: 20% each
   - Marketer: 20% (or absorbed into CEO if 3-project)
5. Wire reports-to:
   - CTO reports to CEO
   - Engineers report to CTO (or CEO if no CTO)
   - Marketer reports to CEO
6. For each Engineer, run `/autopilot` inside the assigned side-project subdirectory to scaffold idea.md / user.md / stack.md / done.md and the Archon workflow.
7. Write `day-plan.md` to the portfolio root with the four attention windows scheduled relative to Q5.
8. Print the org chart (curl GET `/api/companies/$ID/org`) for user review. Wait for explicit `go` before proceeding to Phase 4.

### Phase 4 — Run (Paperclip orchestrates)

On the user's exact reply of `go`:

1. Print: "Starting the factory. The CEO will run the 9am standup automatically. You'll triage at the four attention windows."
2. Trigger the first standup: `npx paperclipai heartbeat run --agent-id $CEO_ID`.
3. The CEO wakes, reads the company goal, creates one ticket per side project, assigns each to an Engineer.
4. Engineers wake on assignment, each fires an `archon workflow run ship-side-project "<task from idea.md>"` inside their assigned project directory.
5. Heartbeats trigger at 13:00 (checkpoint) and 17:00 (gate review). The CEO drafts triage notes for the human at each pulse.
6. The skill is done once Paperclip's audit log shows the daily review entry at 21:00 (or whatever is 12 hours past Q5 start).

Do **not** auto-approve any DEPLOY gate on the user's behalf. Even if the agent thinks the artifact is fine.

Do **not** modify the org chart mid-day. Reports-to is the constant.

### Phase 5 — Reflection (silent, ~30 seconds)

After the day's audit log is closed:

1. Read the audit log for the company: which projects shipped, which paused at budget cap, which got killed at SCOPE.
2. Compute mortality table: shipped / paused / killed counts.
3. Append one new rule to the portfolio-root `CLAUDE.md` under `## Lessons`. The rule should be portfolio-shaped (cross-project), not project-shaped — that's the difference between this and `/autopilot`'s reflection.
4. Print the mortality table and the new rule.

## Output templates

### company.json (POST /api/companies body)

```json
{
  "name": "{from Q1, slug-cased}",
  "issuePrefix": "{3-letter prefix}",
  "budgetMonthlyCents": {Q2 × 100}
}
```

### org-chart.json (5-agent default)

See `assets/org-chart-5.json` for the canonical 5-agent config. The skill substitutes `{COMPANY_ID}`, `{CEO_ID}`, `{CTO_ID}`, model strings, and per-agent budget splits at scaffold time.

### day-plan.md (12-hour calendar overlay)

```markdown
# Day Plan — {today as YYYY-MM-DD}

Total human attention budget: ~90 minutes spread across 12 hours.

- **{Q5 + 0h} — Standup.** Each agent reports {what shipped / what's blocked / what's next}. Triage: kill, continue, escalate. ~15 minutes.
- **{Q5 + 4h} — Checkpoint.** Scan audit log + budget burn rate. Reassign blocked tickets. ~15 minutes.
- **{Q5 + 8h} — Gate review.** Approve DEPLOY transitions across active projects. ~30 minutes.
- **{Q5 + 12h} — Daily review.** Read audit log. Compute mortality (shipped / paused / killed). ~30 minutes.

Between windows: agents work async. You don't watch.
```

### CLAUDE.md ## Lessons section (appended by Phase 5)

```markdown
## Lessons (added {today as YYYY-MM-DD})

- {one portfolio-shaped rule extracted from this run's mortality pattern —
   phrased as a positive directive for the next factory run, not a complaint
   about this one}
```

## Anti-patterns to avoid

1. **No more than five questions in Phase 2.** Five is the budget.
2. **No more than five agents.** Five is the supervisor ceiling for one human. Six burns budget without shipping more.
3. **No skipping per-agent budget caps.** Cap every agent before the first heartbeat. Within four hours, an uncapped engineer in a tool-use loop will burn more than your monthly company budget.
4. **No letting CTO assign tickets to itself.** Lock reporting lines: CTO reviews engineering work, does not replace it.
5. **No running the factory without /autopilot already installed in each side-project subdirectory.** The factory orchestrates harnesses; the harnesses do the work. Install /autopilot in each project subdir before the first heartbeat.
6. **No auto-approving DEPLOY gates.** Even if the engineer thinks the artifact is fine. Live URLs are visible. Confirm first.
7. **No skipping the standup.** The 9am triage is the highest-leverage block of the day. Without it, blocked tickets stay blocked all morning.

## What "done" looks like

The skill completed successfully when:

- A Paperclip company exists with the user's goal + monthly budget cap
- 3-5 agents are hired, reporting lines wired, per-agent budgets capped
- Every Engineer's assigned project subdirectory has `/autopilot` scaffolded inside it
- A `day-plan.md` exists in the portfolio root with four scheduled attention windows
- The factory has run at least one full day cycle (standup → async → checkpoint → async → gate → async → daily review)
- A new rule has been appended to portfolio-root `CLAUDE.md ## Lessons`

The user should now be able to:

- Re-run the factory next Saturday with the same company + the same org chart, just new tickets
- Watch session N+1 ship more than session N (because CLAUDE.md grows portfolio-shaped lessons)
- Trust the budget caps to prevent any single agent from burning the month's spend in a day

## Start here

Begin with Phase 1 (silent discovery). Output nothing user-facing until Phase 2 (the five questions).
