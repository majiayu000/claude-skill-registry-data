---
name: sales-proposal
description: Draft the proposal for a deal — the buyer's situation, scope, outcomes tied to their metrics, two or three options priced from the seller's policy, assumptions, terms to confirm with legal, and next steps — with anything beyond policy marked for approval. Use when the buyer has asked for a proposal or pricing. Not for setting list prices or packaging; see /marketing-pricing-strategy.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 4
  artifact: 04-proposal.md
---

# Proposal

Draft the proposal for "$ARGUMENTS": the buyer's situation, what they get, what it costs, and what happens next.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-proposal","workflow":"sales","phase":4,"project":"<project>","event":"skipped","artifact":"04-proposal.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Proposal) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-proposal","workflow":"sales","phase":4,"project":"<project>","event":"refused","artifact":"04-proposal.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"sales-proposal","workflow":"sales","phase":4,"project":"<project>","event":"started","artifact":"04-proposal.md","note":""}`.

Read `.singularskills/sales/<project>/02-discovery.md` for the buyer's situation and `.singularskills/sales/<project>/03-solution.md` for the value case and fit.

## Process

1. **Get the pricing policy:** list prices, the discount the seller may give without approval, who approves more, and standard terms. Ask once if not given; read the seller's own marketing project in `.singularskills/marketing/*/` (marketing projects are named after the seller's product or company, not the buyer: with exactly one folder there, use it; with several, ask once which is the seller's) for pricing work when it exists. Never invent a price.

2. **Open with the buyer's situation,** in their words from `02-discovery.md`, so the buyer recognises their problem.

3. **Scope and outcomes:** what is included, what is not, and the outcomes tied to the buyer's metrics, using the value case from `03-solution.md` with its label (computed or illustration).

4. **Options:** two or three where useful (for example, a smaller start and the full scope), each priced from the policy. A discount or term the buyer asked for beyond the policy is not offered: it is marked **for approval**, with who approves, and the proposal shows the price within policy.

5. **Assumptions and terms:** what the price assumes, and terms to confirm with legal (`/legal-contract-review` for the contract itself).

6. **Next steps** with dates, which become the start of the close plan.

7. **Honest selling.** No false urgency, no fake scarcity, no misrepresentation of the product or a competitor, and no commitment (discount, term, date, feature) beyond the policy the user stated; anything beyond it is marked **for approval**, with who approves.

8. **Write the artifact** to `.singularskills/sales/<project>/04-proposal.md` with the proposal draft and, after it, an internal section **For approval** listing anything beyond policy.

## Output

The proposal written to `.singularskills/sales/<project>/04-proposal.md`. Present a summary to the user highlighting:
- The options and their prices
- Anything marked for approval, and who approves
- The next steps proposed to the buyer

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-proposal","workflow":"sales","phase":4,"project":"<project>","event":"finished","artifact":"04-proposal.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: sales-proposal
workflow: sales
phase: 4
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
