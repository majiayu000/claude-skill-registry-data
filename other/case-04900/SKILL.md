---
name: procedural-distiller
description: Distill successful multi-step OpenClaw sessions into reusable learned skills before compaction. Use when a task involved many tool calls, environment setup, debugging, file edits, browser research, or when the user asks to remember a workflow such as "记下这个流程" or "这招很有用".
---




### Credential Fixture Review

`python scripts/_credentials.py` is review material for the `Procedural Distiller` skill. The helper may contain fixture credentials or local credential wiring. Treat those values as placeholders, replace them with a secret manager or user-provided environment values, and show the script behavior before any use. Do not contact external services with embedded sample credentials.

# Procedural Distiller

Use this skill after a task has succeeded and the session contains enough signal to preserve.
The goal is to extract procedural knowledge, not to summarize the conversation.

## Triggering Rules

Run the distillation flow when all of the following are true:

1. The task is finished successfully.
2. The session contains at least 5 relevant tool calls across `exec`, `read`, `write`, `edit`, or `browser`.
3. At least one of these applies:
   - The user explicitly asks to remember the workflow.
   - The task involved environment setup, debugging, or a multi-step repair.
   - Compaction risk is high and the trace contains concrete parameters worth preserving.

Do not run while the task is still active. Skip trivial sessions dominated by a single read or a one-line answer.

## Distillation Workflow

1. Read the recent trace and keep only relevant tool events.
2. Separate successful steps from failed attempts.
3. Preserve concrete commands, file paths, parameter values, and code snippets that materially contributed to the outcome.
4. Convert the result into three sections:
   - `Success Pattern`
   - `Failure Triggers`
   - `Snippets`
5. Write a learned skill under `skills/learned/learned-<task-slug>/`.
6. Persist a utility score and source metadata in `memory.json`.

Read [references/trace-format.md](references/trace-format.md) only if the incoming trace shape is unclear.

## Execution Notes

- Favor exact commands over abstract summaries.
- Keep failed steps only when they teach a future agent what to avoid.
- Collapse repetitive probes into one representative line.
- If a write or edit step changed the final behavior, include the smallest useful snippet.
- If a trace already contains a user rating, store it. Otherwise default to `3` and let a future caller update `memory.json`.

## Local CLI

Run the bundled script directly:

```bash
python distill_logic.py --trace /path/to/trace.json --task "repair build cache" --output-root /path/to/skills
```

Useful flags:

- `--utility-score 4`
- `--learned-root learned`
- `--min-tool-calls 5`
- `--max-events 20`
- `--force`

## Output Contract

The generated learned skill must contain:

- `SKILL.md` with valid frontmatter (`name`, `description`) and procedural sections
- `agents/openai.yaml` for UI metadata
- `memory.json` with `utility_score`, source task details, and generation metadata

## Stop Conditions

Stop and do not emit a learned skill when:

- the trace is marked unsuccessful
- there are too few relevant tool calls
- the trace lacks enough detail to reconstruct a reusable procedure
