---
name: ops-alerting
description: Design alerting for a service — multiwindow, multi-burn-rate alerts on each SLO, symptom alerts only where no SLO covers a user-facing failure, page or ticket for every alert, and a runbook named for every page, written in the service's monitoring syntax. Use when a team pages too often, too late, or on the wrong things. Not for security event alerting; see /security-monitoring-strategy.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ops
  phase: 3
  artifact: 03-alerting.md
  stack-aware: true
---

# Alerting

Alert on what hurts users of "$ARGUMENTS", fast enough to matter and rarely enough to be trusted, as `references/slos-and-alerting.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ops-alerting","workflow":"ops","phase":3,"project":"<project>","event":"skipped","artifact":"03-alerting.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Alerting) of the Reliability Cycle workflow (`ops`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ops` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ops-alerting","workflow":"ops","phase":3,"project":"<project>","event":"refused","artifact":"03-alerting.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ops-alerting","workflow":"ops","phase":3,"project":"<project>","event":"started","artifact":"03-alerting.md","note":""}`.

Read `.singularskills/ops/<project>/02-slos.md` for the SLOs and budgets. Read `.singularskills/ops/<project>/01-inventory.md` for the **Tooling** section and the alerts that exist today, when it exists.

## Process

1. **Burn-rate alerts on each SLO.** Start from the multiwindow, multi-burn-rate thresholds: 14.4× over 1 hour and 5 minutes (**page**), 6× over 6 hours and 30 minutes (**page**), 1× over 3 days and 6 hours (**ticket**). Compute each alert's error-rate threshold for the SLO's **own** target (burn rate × (1 − target)); if that is 100% or more the alert can never fire, so say so and use a lower burn rate or a longer window for it and the budget consumed when it fires (burn rate × long window ÷ SLO window), with a script written to `.singularskills/ops/<project>/` and included beside the result. Scripts read the user's files where they keep them and write results under `.singularskills/`.

2. **Symptom alerts only where no SLO covers a user-facing failure** (a queue backing up, a certificate about to expire); no alerts on CPU, memory or disk alone.

3. **Page or ticket for every alert,** with the reason: a page means a person must act now.

4. **Name every alert by what users see** ("Checkout failing for 2% of users"), and give every page the name of the runbook phase 4 writes for it.

5. **Write the rules** in the monitoring query language recorded under **Tooling** in `01-inventory.md` (PromQL, Datadog, CloudWatch). With the tool unknown, write each rule as a plain condition and mark it **rule to fill in**; never invent a syntax.

6. **Existing alerts:** with an export of today's alerts, audit them as `/ops-alert-audit` does (actionable ratio, keep, tune, demote or delete); without one, list the alerts named in `01-inventory.md` and what replaces each.

7. **Never touch live systems.** Do not run any command against a live system, and never say a command, alert or runbook was tested or verified; you write them for people to apply.

8. **Write the artifact** to `.singularskills/ops/<project>/03-alerting.md` with sections **Burn-rate alerts** (a table: SLO, burn rate, windows, severity, threshold, budget consumed, runbook), **Symptom alerts**, **Rules**, **Existing alerts** and **Pages per shift** (the expected load against the target of no more than 2–3 actionable pages per 12-hour shift).


## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The alerting written to `.singularskills/ops/<project>/03-alerting.md`. Present a summary to the user highlighting:
- The pages and the tickets
- The runbooks phase 4 must write
- Existing alerts to delete or demote

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ops-alerting","workflow":"ops","phase":3,"project":"<project>","event":"finished","artifact":"03-alerting.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ops-alerting
workflow: ops
phase: 3
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
