---
name: ai-experience
description: Design how an AI feature behaves for its users — saying it is AI, showing sources and uncertainty, letting users correct or undo it, falling back to a person or a non-AI path, collecting feedback, and handling slow or failed responses. Use when the team must decide what users see when the AI is right, unsure or wrong. Not for designing a UI component; see /design-define-component.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 4
  artifact: 04-experience.md
---

# Experience

Design what users of the AI feature in "$ARGUMENTS" see and can do when it is right, unsure, wrong, slow or down.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-experience","workflow":"ai","phase":4,"project":"<project>","event":"skipped","artifact":"04-experience.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Experience) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-experience","workflow":"ai","phase":4,"project":"<project>","event":"refused","artifact":"04-experience.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-experience","workflow":"ai","phase":4,"project":"<project>","event":"started","artifact":"04-experience.md","note":""}`.

Read `.singularskills/ai/<project>/01-define.md` for the job and failure modes and `.singularskills/ai/<project>/02-approach.md` for what the feature can do. Read `.singularskills/ai/<project>/03-prompt.md` for the refusal and uncertainty rules when it exists.

## Process

1. **Disclosure:** where and how users learn they are dealing with AI, in the product's own words.

2. **Sources:** how the feature shows where an answer came from, so users can check it.

3. **Uncertainty:** what users see when the model is unsure: a hedge, a clarifying question, or a handover, matching the refusal and uncertainty rules in `03-prompt.md` when it exists, or setting them for phase 3 to follow.

4. **Correction and undo:** how users fix a wrong answer, edit an output before using it, or undo an action the feature took.

5. **Fallback:** the path to a person or a non-AI route, when it is offered, and what it keeps of the conversation.

6. **Feedback:** how users say an output was good or bad, and what is captured with it (the output ID, never more personal data than needed); this feeds phase 6 and phase 8.

7. **Slow and down:** what users see while waiting, after the latency budget is exceeded, and when the model is unavailable.

8. **Write the artifact** to `.singularskills/ai/<project>/04-experience.md` with one section per item above.

## Output

The experience design written to `.singularskills/ai/<project>/04-experience.md`. Present a summary to the user highlighting:
- How users can check and correct an answer
- The fallback when the AI is unsure or down
- The feedback that will feed evaluation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-experience","workflow":"ai","phase":4,"project":"<project>","event":"finished","artifact":"04-experience.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-experience
workflow: ai
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
