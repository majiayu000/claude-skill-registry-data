---
name: ai-prompt-design
description: Design the prompt and context for an AI feature — system prompt, how context is assembled per request, examples, output format, refusal and uncertainty behaviour, and defences against prompt injection — versioned like code. Use when the approach is chosen and the team needs the instructions the model will run on. Not for reviewing an existing prompt; see /ai-prompt-review.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 3
  artifact: 03-prompt.md
---

# Prompt and context

Design what the model in "$ARGUMENTS" is told and what it is given, as `references/prompt-and-context.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-prompt-design","workflow":"ai","phase":3,"project":"<project>","event":"skipped","artifact":"03-prompt.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Prompt and context) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-prompt-design","workflow":"ai","phase":3,"project":"<project>","event":"refused","artifact":"03-prompt.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ai-prompt-design","workflow":"ai","phase":3,"project":"<project>","event":"started","artifact":"03-prompt.md","note":""}`.

Read `.singularskills/ai/<project>/01-define.md` for the job and failure modes and `.singularskills/ai/<project>/02-approach.md` for the chosen approach, content and tools.

## Process

1. **Draft the system prompt:** the job, the audience, what a good answer contains, the output format, and what to do when the answer is not in the context or the request is out of scope.

2. **Design the context per request:** what is retrieved or looked up, how much, in what order, and how each piece is delimited. Keep untrusted input (the user's message, retrieved documents, tool results) in clearly marked blocks that the prompt says are data, never instructions.

3. **Add examples:** two or three good outputs for typical inputs, and one for a request the feature should decline.

4. **Define refusal and uncertainty:** when the model says it does not know, asks a question, or hands over to a person, and the exact wording pattern.

5. **Defend against prompt injection:** both direct (the user's message) and indirect, through **retrieved** documents or tool results the user may never see. For each tool: least privilege, and confirmation before any action with side effects. Add output checks for things the feature must never produce.

6. **Map the prompt to the failure modes** in `01-define.md`: for each, the instruction, example or check that addresses it, or "evaluation will tell".

7. **Version it:** name the prompt version, and state that every change is reviewed and re-evaluated before it ships.

8. **Write the artifact** to `.singularskills/ai/<project>/03-prompt.md` with sections:
   - **System prompt** — the full draft, with its version
   - **Context assembly** — per request, with the untrusted blocks marked
   - **Examples**
   - **Refusal and uncertainty**
   - **Injection defences**
   - **Failure-mode coverage**

## Output

The prompt design written to `.singularskills/ai/<project>/03-prompt.md`. Present a summary to the user highlighting:
- The prompt version and its key instructions
- How untrusted input is kept apart from instructions
- The failure modes left for evaluation to catch

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-prompt-design","workflow":"ai","phase":3,"project":"<project>","event":"finished","artifact":"03-prompt.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ai-prompt-design
workflow: ai
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
