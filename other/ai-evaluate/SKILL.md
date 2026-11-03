---
name: ai-evaluate
description: Evaluate an AI feature on its real outputs — error analysis first (notes on each output, failure groups counted), confirmed by a person, then checks per confirmed group with judges validated against human labels and results per check. Use when the feature is built and the team needs to know how well it works. Not for checking one AI judge; see /ai-judge-check.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 6
  artifact: 06-evaluate.md
---

# Evaluate

Find out how the AI feature in "$ARGUMENTS" actually behaves, from its real outputs, as `references/evaluation.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-evaluate","workflow":"ai","phase":6,"project":"<project>","event":"skipped","artifact":"06-evaluate.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 6 (Evaluate) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-evaluate","workflow":"ai","phase":6,"project":"<project>","event":"refused","artifact":"06-evaluate.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-evaluate","workflow":"ai","phase":6,"project":"<project>","event":"started","artifact":"06-evaluate.md","note":""}`.

Read `.singularskills/ai/<project>/01-define.md` for the success criteria and failure modes and `.singularskills/ai/<project>/05-build.md` for the initial test set. Read `.singularskills/development/<project>/` when it exists, and name what was built; if nothing was built yet, say that this phase needs outputs from the built feature (or a prototype) and ask for them.

If `.singularskills/ai/<project>/06-evaluate.md` already exists, keep it as `06-evaluate-<date>.md` (today's date as `YYYY-MM-DD`; if that name is taken, add `-2`, `-3` and so on) before you write, and compare against it.

## Process

1. **Get the outputs:** ask once, together with any other question, for a file of real outputs (about 100, with the input and an output ID per row), any user feedback, and the team's own notes per output if they have them.

2. **Error analysis, first pass.** Use the team's notes when given. Otherwise read every output and write a one-line note on each: what is wrong, or "fine". Then propose failure groups and count them with a script written to `.singularskills/ai/<project>/` and included beside the result. Scripts read the team's outputs and logs where they keep them and write aggregates under `.singularskills/`; a quote from an output names its row or output ID, and names, emails, phone numbers and account IDs in it are replaced with placeholders.

3. **Stop for confirmation.** Show the proposed groups with their counts and two example rows each, and ask a person who knows the domain to confirm, merge, split or rename them. Under `--skip-checks`, or with no answer, write the groups as **proposed** and build no check from them: list them under Open questions as "groups not yet confirmed by a person".

4. **Turn each confirmed group into a check,** ranked by count and harm: a plain check (a rule code can test) for clear-cut failures, an AI judge with written pass/fail criteria for judgement calls. Fix-now items (a missing instruction, a wrong document) become fixes, not checks. List the new test rows in this artifact under **Test set additions**, for the next build to add to its test set.

5. **Validate every AI judge** with `/ai-judge-check`, against human labels the team supplies on the same outputs: agreement, true-positive rate and true-negative rate, as `references/evaluation.md` shows. Never invent human labels; with none, mark the judge **not validated**.

6. **Report results per check:** pass rate with the sample size, `computed`, or `not measured` when the check has not been run on outputs yet; the comparison with the previous evaluation when one was kept.

7. **Write the artifact** to `.singularskills/ai/<project>/06-evaluate.md` with sections:
   - **Outputs** — source, count, what was built
   - **Notes** — the per-output notes (row IDs, redacted quotes), or where the team's notes are
   - **Failure groups** — confirmed or proposed, with counts
   - **Checks** — per confirmed group: type, criteria, judge validation
   - **Results** — per check
   - **Fixes** — fix-now items and their owners
   - **Test set additions** — new test rows from the confirmed groups
   - **Compared with previous** — when one was kept

## Output

The evaluation written to `.singularskills/ai/<project>/06-evaluate.md`. Present a summary to the user highlighting:
- The top failure groups and whether a person confirmed them
- The pass rate per check, with sample sizes
- Any judge that is not validated

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-evaluate","workflow":"ai","phase":6,"project":"<project>","event":"finished","artifact":"06-evaluate.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-evaluate
workflow: ai
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
