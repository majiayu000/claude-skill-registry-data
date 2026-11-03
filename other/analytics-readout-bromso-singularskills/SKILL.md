---
name: analytics-readout
description: Write the decision readout — the answer to each question in one line, the recommendation, the confidence and why, what would change it, and what to watch — for the decision-maker named at the start. Use when the analysis is done and someone has to decide. Not for the sprint or project status report; see /project-management-status-report.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: analytics
  phase: 6
  artifact: 06-readout.md
---

# Readout

Turn the analysis for "$ARGUMENTS" into a memo the decision-maker can act on in five minutes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"analytics-readout","workflow":"analytics","phase":6,"project":"<project>","event":"skipped","artifact":"06-readout.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 6 (Readout) of the Decision Analytics Cycle workflow (`analytics`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `analytics` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"analytics-readout","workflow":"analytics","phase":6,"project":"<project>","event":"refused","artifact":"06-readout.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"analytics-readout","workflow":"analytics","phase":6,"project":"<project>","event":"started","artifact":"06-readout.md","note":""}`.

Read `.singularskills/analytics/<project>/04-analysis.md` for the answers and their limits. Read `.singularskills/analytics/<project>/01-questions.md` for the decisions, their decision-makers and deadlines. Read `.singularskills/analytics/<project>/02-metrics.md` and `.singularskills/analytics/<project>/03-data.md` when they exist.

## Process

1. **Write for the decision-maker** named in `01-questions.md`, in their terms, one memo per decision.

2. **Lead with the recommendation:** the option you recommend and the one-sentence reason.

3. **Give the answers:** each question's answer in one line, with its uncertainty, taken from `04-analysis.md` without changing a number.

4. **Rate the confidence** as high, medium or low, with why: the size of the effect against its uncertainty, the data caveats from `03-data.md` and `04-analysis.md`, and whether the answer is observational.

5. **Say what would change the recommendation:** the result, the data or the event that would make you recommend otherwise.

6. **Say what to watch** after the decision: the metrics (by their `02-metrics.md` names) and the threshold that would mean the decision is not working.

7. **Write the artifact** to `.singularskills/analytics/<project>/06-readout.md` with sections, per decision:
   - **Recommendation**
   - **Answers**
   - **Confidence**
   - **What would change this**
   - **What to watch**

## Output

The readout written to `.singularskills/analytics/<project>/06-readout.md`. Present the recommendation and confidence for each decision, and what to watch.

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"analytics-readout","workflow":"analytics","phase":6,"project":"<project>","event":"finished","artifact":"06-readout.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: analytics-readout
workflow: analytics
phase: 6
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
