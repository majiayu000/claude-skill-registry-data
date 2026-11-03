---
name: ai-build
description: Write the build spec for an AI feature — components, prompt files, retrieval pipeline or tool definitions, configuration, logging, and an initial test set from the failure modes — ready for the development workflow to implement. Use when the prompt and experience are designed and the feature needs building. Not for writing the code itself; see /development-plan.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 5
  artifact: 05-build.md
---

# Build

Turn the designs for "$ARGUMENTS" into a build spec the development workflow can implement. This skill writes the spec; it does not write the feature's code.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-build","workflow":"ai","phase":5,"project":"<project>","event":"skipped","artifact":"05-build.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (Build) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-build","workflow":"ai","phase":5,"project":"<project>","event":"refused","artifact":"05-build.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-build","workflow":"ai","phase":5,"project":"<project>","event":"started","artifact":"05-build.md","note":""}`.

Read `.singularskills/ai/<project>/03-prompt.md` for the prompt and context design and `.singularskills/ai/<project>/04-experience.md` for the user-facing behaviour. Read `.singularskills/ai/<project>/01-define.md` and `02-approach.md` for the criteria, budgets and approach.

## Process

1. **List the components:** where the feature sits in the product, the request path from user input to model to output, and each part (prompt assembly, retrieval, tools, output checks, fallback, feedback capture).

2. **Specify the prompt files:** each prompt as a versioned file, with its variables, taken from `03-prompt.md`.

3. **Specify retrieval or tools** for the chosen approach: for retrieval, the content sources, chunking, ranking and the "nothing found" path; for tools, each tool's name, inputs, outputs, permissions and whether it needs user confirmation.

4. **Specify configuration:** model, parameters, timeouts against the latency budget, and spending limits against the cost budget.

5. **Specify logging:** per request, the input, the prompt version, retrieved sources, the output, latency, cost and any feedback, with personal data handled (stored only where the product already stores it, or redacted).

6. **Write the initial test set** from the failure modes in `01-define.md`: for each, five or more test inputs and what passes. Phase 6 grows it from real outputs.

7. **Write the artifact** to `.singularskills/ai/<project>/05-build.md` with sections **Components**, **Prompt files**, **Retrieval or tools**, **Configuration**, **Logging** and **Initial test set**, and end it with **Hand-off**: the next steps for the user.

## Output

The build spec written to `.singularskills/ai/<project>/05-build.md`. Present a summary to the user highlighting:
- The components to build
- The initial test set size per failure mode
- **Next:** run `/development-plan <project>` with the same project name to turn this spec into an implementation plan, then `/development-build <project>` to build it. Come back to phase 6 with real outputs from the built feature.

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-build","workflow":"ai","phase":5,"project":"<project>","event":"finished","artifact":"05-build.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-build
workflow: ai
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
