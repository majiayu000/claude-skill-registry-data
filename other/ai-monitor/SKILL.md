---
name: ai-monitor
description: Monitor a live AI feature — what to log, the signals that call for a look, a monthly error analysis, a re-evaluation on every prompt or model change, and cost and latency against budget. Use when the feature is launched and the team must know when it gets worse. Not for the first evaluation before launch; see /ai-evaluate.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 8
  artifact: 08-monitor.md
---

# Monitor

Set up how the team will know when the live AI feature in "$ARGUMENTS" gets worse, and run the regular review.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-monitor","workflow":"ai","phase":8,"project":"<project>","event":"skipped","artifact":"08-monitor.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 8 (Monitor) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-monitor","workflow":"ai","phase":8,"project":"<project>","event":"refused","artifact":"08-monitor.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-monitor","workflow":"ai","phase":8,"project":"<project>","event":"started","artifact":"08-monitor.md","note":""}`.

Read `.singularskills/ai/<project>/07-ship.md` for the launch bar, human review and rollout. Read `.singularskills/ai/<project>/06-evaluate.md` for the checks.

If `.singularskills/ai/<project>/08-monitor.md` already exists, keep it as `08-monitor-<date>.md` (today's date as `YYYY-MM-DD`; if that name is taken, add `-2`, `-3` and so on) before you write, and compare against it.

## Process

1. **What to log,** per request: the input, prompt version, model, retrieved sources, output, latency, cost and feedback, with personal data handled as `05-build.md` specifies.

2. **Signals that call for a look:** negative feedback above a rate, handovers to a person above a rate, a check's pass rate below its bar, latency or cost above budget, and any output a hard check blocked. Each with its threshold (`target`) and who looks.

3. **The regular review** (monthly, or as the user sets): a fresh error analysis on a sample of recent outputs, as `/ai-evaluate` runs it, looking for new failure groups. When the user supplies recent outputs or logs now, run it: compute the signals and the sample's notes and groups with a script written to `.singularskills/ai/<project>/`. Scripts read the team's outputs and logs where they keep them and write aggregates under `.singularskills/`; a quote from an output names its row or output ID, and names, emails, phone numbers and account IDs in it are replaced with placeholders.

4. **Re-evaluate on every change:** any prompt version or model change re-runs the checks before it ships; say this is a rule, and who enforces it.

5. **Cost and latency:** actual against budget, `computed` from the logs supplied or `not measured`.

6. **Write the artifact** to `.singularskills/ai/<project>/08-monitor.md` with sections **Logging**, **Signals**, **This review** (or "first review not yet run"), **Change rule**, and **Cost and latency**.

## Output

The monitoring plan and review written to `.singularskills/ai/<project>/08-monitor.md`. Present a summary to the user highlighting:
- The signals and their thresholds
- Any signal over its threshold now
- New failure groups since the last review

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-monitor","workflow":"ai","phase":8,"project":"<project>","event":"finished","artifact":"08-monitor.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-monitor
workflow: ai
phase: 8
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
