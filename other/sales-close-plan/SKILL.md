---
name: sales-close-plan
description: Plan how a deal closes — a mutual action plan worked back from the buyer's go-live date with an owner on each side for every step, legal, security and procurement in parallel, the risks to the date, and a give-get list for negotiation within policy. Use when a proposal is out and the seller needs the steps to signature agreed. Not for legal negotiation strategy; see /legal-negotiation-prep.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 5
  artifact: 05-close.md
---

# Close plan

Plan, with the buyer, the steps from proposal to go-live for "$ARGUMENTS", as `references/qualification.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-close-plan","workflow":"sales","phase":5,"project":"<project>","event":"skipped","artifact":"05-close.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (Close plan) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-close-plan","workflow":"sales","phase":5,"project":"<project>","event":"refused","artifact":"05-close.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"sales-close-plan","workflow":"sales","phase":5,"project":"<project>","event":"started","artifact":"05-close.md","note":""}`.

Read `.singularskills/sales/<project>/04-proposal.md` for the options, price and next steps. Read `.singularskills/sales/<project>/02-discovery.md` for the decision process and committee.

## Process

1. **Start from the buyer's go-live date** (the date they need the outcome), not the seller's quarter. If the buyer has not given one, it is **unknown** and the first step is to agree it.

2. **Work back to today:** every step to signature and go-live (decision meeting, security review, legal review, procurement, signature, kickoff), each with an owner on the buyer's side, an owner on the seller's side, and a date.

3. **Run the paper process in parallel:** legal, security and procurement start as soon as the buyer is likely to proceed, not after the commercial decision. Link `/legal-contract-review` for the contract.

4. **Name the risks to the date:** a missing economic buyer, a champion who is only identified, an unknown step, and what to do about each.

5. **The give-get list:** what the seller may give in negotiation (within the policy from `04-proposal.md`) and what it asks for in return; anything beyond policy is marked **for approval**. Link `/legal-negotiation-prep` for the legal side.

6. **Agree it with the buyer:** the plan is a draft until the buyer has seen and accepted it; say so, and mark which steps the buyer has confirmed.

7. **Honest selling.** No false urgency, no fake scarcity, no misrepresentation of the product or a competitor, and no commitment (discount, term, date, feature) beyond the policy the user stated; anything beyond it is marked **for approval**, with who approves.

8. **Write the artifact** to `.singularskills/sales/<project>/05-close.md` with sections **Go-live date**, **Mutual action plan** (a table: step, buyer owner, seller owner, date, confirmed), **Paper process**, **Risks** and **Give-get**.

## Output

The close plan written to `.singularskills/sales/<project>/05-close.md`. Present a summary to the user highlighting:
- The go-live date and whether the buyer confirmed it
- The steps on the critical path
- The biggest risk to the date

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-close-plan","workflow":"sales","phase":5,"project":"<project>","event":"finished","artifact":"05-close.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: sales-close-plan
workflow: sales
phase: 5
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
