---
name: ops-alert-audit
description: Audit a service's alerts from an export — firings and actionable ratio per alert over the period, computed — and decide for each whether to keep, tune, demote to a ticket or delete, flagging pages with no runbook and pages per shift over the target. Use when on-call is noisy and the team wants fewer, better alerts. Not for designing alerting from scratch; see /ops-alerting.
metadata:
  argument-hint: "<alerts file> [project]"
---

# Alert audit

Find out which alerts in "$ARGUMENTS" earn their place, as `references/slos-and-alerting.md` describes.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The export: one row per alert firing with the alert name, the time it fired, whether it was acknowledged, and what action was taken (or none), over a period of about 90 days if available. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ops/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, ask for a project name. Read `.singularskills/ops/<project>/04-runbooks.md` and `05-on-call.md` when they exist.

Append this line to `.singularskills/log.jsonl` before you write the audit (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ops-alert-audit","workflow":"ops","phase":null,"project":"<project>","event":"started","artifact":"alerts/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the topic, never a person.

## Process

1. **Compute per alert** with a script written to `.singularskills/ops/<project>/` and included beside the result: firings, the share that led to an action (the actionable ratio), firings outside working hours, and time to acknowledge. Scripts read the user's files where they keep them and write results under `.singularskills/`.

2. **Compute the load:** pages per on-call shift, against the target of no more than 2–3 actionable pages per 12-hour shift (`target`).

3. **Decide each alert:**
   - **keep** — actionable ratio of 80% or more, and it pages for a user-facing symptom
   - **tune** — real but noisy: change the threshold, the window or move it to a burn-rate alert
   - **demote** — never urgent: make it a ticket
   - **delete** — not acted on in the period
   with the reason and the numbers behind it.

4. **Flag pages with no runbook,** and alerts named by a resource ("CPU high") instead of what users see.

5. **Write the audit** to `.singularskills/ops/<project>/alerts/<date>-<slug>.md` with sections **Period**, **Per alert** (a table: alert, firings, actionable ratio, after hours, decision, reason), **Load**, **Missing runbooks** and **Changes**.

## Output

The audit written to `.singularskills/ops/<project>/alerts/<date>-<slug>.md`. Present the pages per shift against the target, then the alerts to delete or demote.

After you have written the audit, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"ops-alert-audit","workflow":"ops","phase":null,"project":"<project>","event":"finished","artifact":"alerts/<date>-<slug>.md","note":""}`.

The audit opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: ops-alert-audit
workflow: ops
phase: null
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

The audit ends with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what a reviewer must settle>
```
