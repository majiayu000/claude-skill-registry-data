---
name: ai-approach
description: Assess the approaches for an AI feature — prompt only, retrieval over the team's content, tool use or a multi-step agent — and pick the simplest that meets its criteria, with the data and tools it needs and how to choose the model. Use when an AI feature is defined and the team must decide how to build it. Not for comparing models on test results; see /ai-model-compare.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 2
  artifact: 02-approach.md
---

# Approach

Pick how the AI feature for "$ARGUMENTS" will work: the simplest approach that can meet its criteria.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-approach","workflow":"ai","phase":2,"project":"<project>","event":"skipped","artifact":"02-approach.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Approach) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-approach","workflow":"ai","phase":2,"project":"<project>","event":"refused","artifact":"02-approach.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-approach","workflow":"ai","phase":2,"project":"<project>","event":"started","artifact":"02-approach.md","note":""}`.

Read `.singularskills/ai/<project>/01-define.md` for the job, success criteria, failure modes and budgets.

## Process

1. **Lay out the approaches,** simplest first:
   - **Prompt only** — the model answers from the request and the prompt
   - **Retrieval** — the model answers from the team's content, retrieved per request
   - **Tool use** — the model calls functions to look things up or act
   - **Agent** — the model plans and takes several steps on its own

2. **Test each against `01-define.md`:** which success criteria and failure modes each can meet, and its latency and cost against the budgets. Pick the simplest that meets them, and say why each simpler one was not enough.

3. **List what it needs:** the content to retrieve (where it lives, how fresh, who owns it), the tools and their permissions (least privilege: only what the job needs), and the data the feature sees, including any personal data.

4. **Set the model criteria:** quality on this task, cost, latency, context length, and data handling (where data is processed and retained). Name models only from the team's shortlist, and ask for one if there is none; do not recommend a model from memory.

5. **Note the risks of the chosen approach:** an agent or tool use can act on the world; retrieval can carry injected instructions; each needs a defence in phase 3.

6. **Write the artifact** to `.singularskills/ai/<project>/02-approach.md` with sections:
   - **Options** — each approach against the criteria and budgets
   - **Chosen approach** — and why the simpler ones were not enough
   - **Content, tools and data**
   - **Model criteria** — and the team's shortlist
   - **Risks**

## Output

The approach written to `.singularskills/ai/<project>/02-approach.md`. Present a summary to the user highlighting:
- The chosen approach and why
- The content, tools and data it needs
- The risks phase 3 must defend against

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-approach","workflow":"ai","phase":2,"project":"<project>","event":"finished","artifact":"02-approach.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-approach
workflow: ai
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
