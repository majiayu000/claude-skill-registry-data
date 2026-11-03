---
name: sales-discovery
description: Write up a discovery call from the seller's notes or transcript — the buyer's pains in their own words, the metrics they gave, their decision criteria and process, and the buying committee — leaving unknown whatever the buyer did not say. Use when a seller has held a discovery call and needs the buyer's picture written down. Not for researching buyers in general; see /marketing-customer-research.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 2
  artifact: 02-discovery.md
---

# Discovery

Write down what the buyer in "$ARGUMENTS" actually said, and only that.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-discovery","workflow":"sales","phase":2,"project":"<project>","event":"skipped","artifact":"02-discovery.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Discovery) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-discovery","workflow":"sales","phase":2,"project":"<project>","event":"refused","artifact":"02-discovery.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"sales-discovery","workflow":"sales","phase":2,"project":"<project>","event":"started","artifact":"02-discovery.md","note":""}`.

Read `.singularskills/sales/<project>/01-qualify.md` for the qualification and its unknowns.

## Process

1. **Get the call record:** notes or a transcript of a discovery call that has happened, from the user. Ask once if none was given. **With neither, write nothing:** say that this phase records a call that has happened, and to plan the call with `/sales-call-prep`, append the `finished` line of Prerequisites to `.singularskills/log.jsonl` with `"note":"no call record; nothing written"`, so the run is not left open, then stop. Phases 3 to 5 depend on this file, so it must never be written from guesses.

2. **If `02-discovery.md` already exists** (a later call), keep it as `02-discovery-<date>.md` (today's date as `YYYY-MM-DD`; if that name is taken, add `-2`, `-3` and so on), then write the new file: the overall picture updated, with what changed marked, and a dated section for this call.

3. **The buyer's pains,** in their words: quote them, with who said it. Do not paraphrase a pain into something the buyer did not say.

4. **Metrics they gave:** numbers the buyer stated (hours, costs, volumes, targets), with who gave them; these feed the value case in phase 3.

5. **Decision criteria and process,** as stated: what they will judge on, the steps, the people and the dates. Label each **known** (said on the call), **assumed** or **unknown**.

6. **The buying committee:** each person mentioned, their role, what they care about, their stance, and **identified** or **engaged**. Name contacts only as the user supplied them, with their role; no personal details beyond what the deal needs.

7. **Gaps for the next call:** the MEDDPICC elements still unknown, as open questions to ask, one at a time, following up on the buyer's words, as `references/qualification.md` describes.

8. **Write the artifact** to `.singularskills/sales/<project>/02-discovery.md` with sections **Calls** (date, attendees), **Pains**, **Metrics**, **Decision criteria and process**, **Buying committee** and **Gaps**.

## Output

The discovery record written to `.singularskills/sales/<project>/02-discovery.md`, or, with no call record, nothing written and the reason. Present a summary to the user highlighting:
- The buyer's top pain, in their words
- The metrics they gave
- The gaps to close on the next call

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-discovery","workflow":"sales","phase":2,"project":"<project>","event":"finished","artifact":"02-discovery.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: sales-discovery
workflow: sales
phase: 2
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
