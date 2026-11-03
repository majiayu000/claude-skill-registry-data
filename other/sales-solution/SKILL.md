---
name: sales-solution
description: Build the value case and proof plan for a deal — value tied to the buyer's own metrics and computed only from their numbers, what each stakeholder needs to see, and the fit gaps stated honestly. Use when discovery is done and the seller must show the buyer why this is worth it. Not for the team's general demo talking points; see /marketing-sales-enablement.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 3
  artifact: 03-solution.md
---

# Solution

Show the buyer in "$ARGUMENTS" why the solution is worth it, in their own numbers, and what each person needs to see.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-solution","workflow":"sales","phase":3,"project":"<project>","event":"skipped","artifact":"03-solution.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Solution) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-solution","workflow":"sales","phase":3,"project":"<project>","event":"refused","artifact":"03-solution.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"sales-solution","workflow":"sales","phase":3,"project":"<project>","event":"started","artifact":"03-solution.md","note":""}`.

Read `.singularskills/sales/<project>/02-discovery.md` for the pains, metrics, criteria and committee.

## Process

1. **Map pains to capabilities:** for each pain in `02-discovery.md`, what in the product addresses it, and how well (fully, partly, not at all).

2. **Build the value case** from the metrics the buyer gave: the saving or return, computed with a script written to `.singularskills/sales/<project>/` and included beside the result, with every input and its source, and a range where an input is uncertain. Scripts read the user's files where they keep them and write results under `.singularskills/`; contact details (emails, phone numbers) never go into any file there. Without the buyer's numbers, a figure is an **illustration** and says so; never present it as the buyer's result.

3. **Plan the proof per stakeholder:** what each person in the committee needs to see or try (a demo of a workflow, a pilot, a reference customer, a security document), tied to their criteria.

4. **State the fit gaps honestly:** what the product does not do for this buyer, and the workaround or the answer, if any.

5. **Honest selling.** No false urgency, no fake scarcity, no misrepresentation of the product or a competitor, and no commitment (discount, term, date, feature) beyond the policy the user stated; anything beyond it is marked **for approval**, with who approves.

6. **Write the artifact** to `.singularskills/sales/<project>/03-solution.md` with sections **Pains to capabilities**, **Value case**, **Proof plan**, **Fit gaps**.

## Output

The solution written to `.singularskills/sales/<project>/03-solution.md`. Present a summary to the user highlighting:
- The value case and whether it is computed or an illustration
- The proof each key stakeholder needs
- The fit gaps

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-solution","workflow":"sales","phase":3,"project":"<project>","event":"finished","artifact":"03-solution.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: sales-solution
workflow: sales
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
