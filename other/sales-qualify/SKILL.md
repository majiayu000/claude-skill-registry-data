---
name: sales-qualify
description: Assess whether a deal is worth pursuing — ICP fit, every MEDDPICC element marked known, assumed or unknown, people identified or engaged, the risk of no decision — and recommend pursue, nurture or drop. Use when a seller has a new opportunity and must decide how much effort it deserves. Not for defining the ideal customer profile itself; see /sales-icp.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 1
  artifact: 01-qualify.md
---

# Qualify

Decide whether the deal in "$ARGUMENTS" deserves effort, and what is still unknown, as `references/qualification.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-qualify","workflow":"sales","phase":1,"project":"<project>","event":"skipped","artifact":"01-qualify.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Qualify) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Deal Cycle workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-qualify","workflow":"sales","phase":1,"project":"<project>","event":"started","artifact":"01-qualify.md","note":""}`.

None — this is the first phase.

## Process

1. **Find the ideal customer profile:** the newest file in any `.singularskills/sales/*/icp/` folder (usually `playbook/icp/`) when one exists; else the customer research in the seller's own marketing project in `.singularskills/marketing/*/` (marketing projects are named after the seller's product or company, not the buyer: with exactly one folder there, use it; with several, ask once which is the seller's); else ask the user, once, who their best customers are.

2. **Gather what is known** from the user's notes, emails, CRM record or the conversation, and ask once, together, for anything missing: who the buyer is, how the deal started, who they have spoken to, and what the buyer has said they want.

3. **Check fit** against the profile: each criterion met, not met or unknown.

4. **Qualify with MEDDPICC:** metrics, economic buyer, decision criteria, decision process, paper process, identified pain, champion, competition. Label each element **known** (with its source), **assumed** (with why) or **unknown**. Never fill a gap with a guess presented as fact.

5. **Map the people** the user named: role, what they care about, stance, and whether each is **identified** or **engaged**.

6. **Name the risk of no decision:** what the buyer does if they do nothing, and what that costs them, as known, assumed or unknown.

7. **Recommend** pursue, nurture or drop, with the reasons, and the unknowns that would change the recommendation.

8. **Write the artifact** to `.singularskills/sales/<project>/01-qualify.md` with sections **Fit**, **MEDDPICC**, **People**, **No decision**, **Recommendation** and **Unknowns to close**. If it already exists (a re-qualification after discovery), keep the previous file as `01-qualify-<date>.md` (today's date as `YYYY-MM-DD`; if that name is taken, add `-2`, `-3` and so on) before you write, and mark what changed.

## Output

The qualification written to `.singularskills/sales/<project>/01-qualify.md`. Present a summary to the user highlighting:
- The recommendation and why
- The MEDDPICC elements still unknown
- Whether the economic buyer and a champion are engaged or only identified

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-qualify","workflow":"sales","phase":1,"project":"<project>","event":"finished","artifact":"01-qualify.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: sales-qualify
workflow: sales
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
