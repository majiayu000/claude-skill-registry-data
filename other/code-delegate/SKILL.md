---
name: code-delegate
description: Solve one hard task with a manager call and fresh-context workers that coordinate through files on disk. Use when a task is too large for one pass, when one pass keeps failing, or when the user asks for a manager, an orchestrator, or parallel attempts.
---

Run the task as a manager that owns a task list, delegating single-step tasks to fresh-context worker subagents that coordinate through a ledger directory on disk.

## When to Use

Use this skill when:

- The task is too large for one context: many files, a long deliverable, or coupled goals.
- One pass failed twice on the same approach.
- The user asks for a manager, an orchestrator, a plan-and-delegate loop, or several independent attempts.

Do not use this skill when:

- One file, one function, or one command answers the request.
- The task is a question you can answer directly.
- The work is a short tool loop you can finish in this turn.

The loop costs about 3x the tokens of one pass. Use it for hard tasks only.

## Ledger

Create one run directory under `tmp/` per task. Keep every file in it small.

| File | Owner | Content |
| --- | --- | --- |
| `task.md` | Manager | The request, verbatim |
| `plan.md` | Manager | 3-6 sentence strategy, capped at 4k characters |
| `tasks.md` | Manager | One line per task, `- [todo]` or `- [done]` |
| `notes.md` | Worker | Findings, ruled-out ideas, and partial results, capped at 8k characters |
| `solution.<ext>` | Worker | The current artifact |
| `verify.log` | Worker | The last check output |

Workers never talk to each other. Each worker reads the ledger and one task.

## Process

### Step 1 - Plan

- Write `task.md` with the request, verbatim.
- Write `plan.md` with a 3-6 sentence approach.
- Write 3-6 seed tasks in `tasks.md`.

### Step 2 - Brainstorm

- Start one worker before any artifact exists.
- Ask it for the core difficulty, several genuinely different approaches, and the pitfall of each.
- Require it to rewrite `notes.md` with the result and produce no artifact.

### Step 3 - Delegation Loop

Repeat until the budget is spent or the task is done:

1. **Pick one task**: Read the ledger, merge duplicates in `tasks.md`, mark finished items `[done]`, and name the single next task.
2. **Run one worker**: Give it `plan.md`, `notes.md`, the current artifact, and that one task.
3. **Read the report**: The worker must rewrite `notes.md`, report `solved` or `continue`, and list the remaining steps.
4. **Check the artifact**: Run the test, build, or check that proves the task (read `code-check` for command detection when needed). Treat a failing result as ground truth.
5. **Decide**: Mark the task `[done]` only when the check passes; otherwise name the next task.

### Step 4 - Close

- When the budget expires or the same task repeats, run one final worker call that merges the ledger into the definitive artifact.

### Step 5 - Report

Report to the user:

- **Result**: The final artifact or changes produced.
- **Verification**: Checks run and their outcomes.
- **Remaining Items**: Anything left unproven or incomplete.

## Worker Contract

Give every worker this output template. The manager parses it, so require the exact headings:

```markdown
### RESULT

<the full updated artifact, or "none" for a brainstorm task>

### NOTES

<the complete notes file, rewritten. Fold in what still matters and delete what is superseded, disproven, or obvious. This replaces the file. Under 800 words.>

### NEXT

<bullet list of remaining steps, or "none">

### STATUS

<solved|continue>
```

Notes replace, never append. A growing notes file is the failure this skill exists to avoid.

## Subagent Invocation

Use the harness's built-in subagent tool so each worker runs in a fresh, isolated context:

| Harness | One worker |
| --- | --- |
| lofi | `await lofi.subagent({ prompt })` from `exec` |
| Claude Code | `Agent` tool (`description`, `prompt`, `subagent_type: "general-purpose"`) |
| Codex | `spawn_agent` (`message: "<prompt>"`, `fork_context: false`), `wait_agent` (`ids: [id]`), `close_agent` (`id`) |
| agy | `invoke_subagent` (`TypeName: "self"`, `Role`, `Prompt`, `Workspace: "inherit"`) |

- Pass the full worker contract, the ledger files, and the single task in the prompt; the worker starts with nothing else.
- Run independent workers in parallel only when they do not write the same file.

## Convergence Rules

- **Round budget**: 10 worker calls by default. Stop and close when it is spent.
- **No progress**: Stop when the next task repeats the last one. A repeated task means the ledger is not moving.
- **Cut off**: When a worker hits the token limit, keep its `NOTES` and summarize the partial attempt in the next task. Do not restart from zero.
- **Stuck approach**: After two failed rounds on one approach, make the next task "try a different approach from the notes".
- **Independent attempt**: When the plan looks wrong, start one worker with the raw task and no notes. Compare its artifact with the ledger artifact.
- **No trust without a check**: A worker's claim is not proof. Run the check yourself, or require the worker to paste the command and its output into `verify.log`.

## Guardrails

- Keep every ledger file under its cap. Truncate the plan and the notes, never the artifact.
- Do not let a worker edit `tasks.md` or `plan.md`. Only the manager writes those.
- Do not mark a task `[done]` or accept a `solved` status while a check fails.
- Do not spawn CLI processes (`<agent> -p` or `<agent> exec`) as subagents; use the harness's native subagent tool.
- Do not use this loop for a task you can finish in this turn.
