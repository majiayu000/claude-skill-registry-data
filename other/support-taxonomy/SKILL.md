---
name: support-taxonomy
description: Design the ticket taxonomy — a two-level category tree, tags, and P1 to P4 priority definitions an agent can apply — and test it against real tickets. Use when the user needs to decide how support tickets are categorised, tagged and prioritised before building help content or reports. Not for mapping where customers contact support; see /support-journey-map.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: support
  phase: 2
  artifact: 02-taxonomy.md
---

# Taxonomy

Design how tickets are categorised, tagged and prioritised for "$ARGUMENTS", so every ticket lands in one place and reports mean something.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"support-taxonomy","workflow":"support","phase":2,"project":"<project>","event":"skipped","artifact":"02-taxonomy.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Taxonomy) of the Support Operations Cycle workflow (`support`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `support` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"support-taxonomy","workflow":"support","phase":2,"project":"<project>","event":"refused","artifact":"02-taxonomy.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"support-taxonomy","workflow":"support","phase":2,"project":"<project>","event":"started","artifact":"02-taxonomy.md","note":""}`.

Read `.singularskills/support/<project>/01-map.md` for the channels, journey moments and contact reasons.

## Process

1. **Draft the category tree** from the contact reasons in `01-map.md`:
   - At most about twelve top-level categories, each with a one-line definition, what belongs in it, what does not, and an example ticket.
   - A second level only where it changes who handles the ticket or what the answer is.
   - One "Other" category, used only when nothing fits.

2. **Define the tags**, kept separate from the categories: product area, plan or tier, channel, and any the user needs for reporting. A tag describes the ticket; it never repeats the category.

3. **Write the priority definitions** P1 to P4 as tests a new agent can apply without asking anyone. For example, P1: "the customer cannot use the product at all, or is losing money or data now, and has no workaround". For each priority give two example tickets and the most common mistake.

4. **Test the tree against real tickets** if the user gave an export (ask once if they have not, with any other question): classify a sample of at least 50 tickets, or all of them if there are fewer, against the draft. Do the counting with a script written to `.singularskills/support/<project>/`. Scripts read the export where the user keeps it and write only aggregates (counts, times, shares and `acct-` identifiers): no ticket text, names, emails, phone numbers or raw account IDs go into any file under `.singularskills/`. Report how many fell into each category and into "Other". Revise the tree and reclassify until fewer than 10% are "Other", or say why the remaining ones cannot be placed. Without an export, say the tree is untested.

5. **Protect personal data:** example tickets are paraphrased, with names, emails, phone numbers and account or order numbers replaced by placeholders (`<customer>`, `<email>`, `<account-1>`).

6. **Write the artifact** to `.singularskills/support/<project>/02-taxonomy.md` with sections:
   - **Categories** — the tree, with definitions and examples
   - **Tags** — each tag and its allowed values
   - **Priorities** — P1 to P4 tests, examples and common mistakes
   - **Test results** — the classification counts (`computed`, with the script) or "untested"
   - **Key takeaways** — what the Knowledge and Responses phases should start from

## Output

The taxonomy written to `.singularskills/support/<project>/02-taxonomy.md`. Present a summary to the user highlighting:
- The top-level categories
- The P1 definition
- The share of sample tickets in "Other", or that the tree is untested
- The three categories with the most tickets

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"support-taxonomy","workflow":"support","phase":2,"project":"<project>","event":"finished","artifact":"02-taxonomy.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: support-taxonomy
workflow: support
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
