---
name: ai-ship
description: Set the launch decision for an AI feature — the bar each check must meet, where human review stays, the rollout and kill switch, the compliance work that applies — and decide launch, hold or fix against the evaluation. Use when the feature has been evaluated and the team must decide whether it can go live. Not for monitoring it after launch; see /ai-monitor.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 7
  artifact: 07-ship.md
---

# Ship

Decide whether the AI feature in "$ARGUMENTS" is ready, and how it goes live safely.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-ship","workflow":"ai","phase":7,"project":"<project>","event":"skipped","artifact":"07-ship.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 7 (Ship) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-ship","workflow":"ai","phase":7,"project":"<project>","event":"refused","artifact":"07-ship.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-ship","workflow":"ai","phase":7,"project":"<project>","event":"started","artifact":"07-ship.md","note":""}`.

Read `.singularskills/ai/<project>/06-evaluate.md` for the checks, results and judge validation. Read `.singularskills/ai/<project>/01-define.md` for the failure modes and their harm. Read `.singularskills/compliance/<project>/` when it exists, for compliance work already done.

## Process

1. **Set the launch bar** per check: the pass rate it must reach, higher for failure modes with worse harm, each labelled `target`. A check built on a proposed group, or measured by a judge that is not validated, cannot count towards the bar.

2. **Decide where human review stays:** every output type whose check is below its bar, or whose failure would cause harm, keeps a person reviewing before users see it. Review is removed only where the evaluation shows the feature passes.

3. **Plan the rollout:** internal users first, then a small share of real users, then everyone, with the evidence needed to move between stages, and the **kill switch**: who can turn the feature off, how fast, and what users see then.

4. **Check the compliance work** that applies: `/compliance-eu-ai-act` for AI used in the EU, `/compliance-nist-ai-rmf` and `/compliance-iso42001` for risk-management frameworks. Name which apply and whether they are done; this skill does not assess them.

5. **Decide.** With no confirmed check, the decision is **hold**: a launch needs evidence, and groups that are only proposed give none. Otherwise: **launch** (every check meets its bar, review and rollout set), **hold** (a bar missed, evidence missing, or compliance open), or **fix** (a failure group needs a change first). For **fix**, name the phase to re-run: 3 for a prompt change, 5 for a build change, then 6.

6. **Write the artifact** to `.singularskills/ai/<project>/07-ship.md` with sections **Launch bar**, **Human review**, **Rollout and kill switch**, **Compliance**, and **Decision** (with the evidence behind it).

## Output

The launch decision written to `.singularskills/ai/<project>/07-ship.md`. Present the decision first, then the checks that decided it, where human review stays, and the first rollout stage.

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-ship","workflow":"ai","phase":7,"project":"<project>","event":"finished","artifact":"07-ship.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-ship
workflow: ai
phase: 7
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
