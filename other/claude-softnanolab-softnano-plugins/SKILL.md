---
name: claude
description: Get a second opinion from Claude Code. Use from Codex when you want to cross-check your reasoning, validate a plan, or get an independent review from Claude.
argument-hint: <task or question for Claude>
user-invocable: true
allowed-tools: Bash(claude *), Read, Grep, Glob
---

# Claude Second Opinion

Delegate a task to Claude Code for an independent review or second opinion.

## Input

<task>
$ARGUMENTS
</task>

If no task is provided, ask the user what they want Claude to review.

## How to Use

Run Claude in non-interactive print mode from the current working directory. Prefer a read-only tool set:

```bash
claude -p \
  --permission-mode dontAsk \
  --allowedTools Read,Grep,Glob,LS \
  --add-dir "<current working directory>" \
  "<prompt>"
```

If the Claude CLI is not installed or is not authenticated, report that blocker and include the command output.

## Prompt Construction

Build a self-contained prompt for Claude that includes:

1. **Context**: The repo path, what project this is, and what folder/files are relevant
2. **The task**: What you want Claude to do (review, validate, suggest, etc.)
3. **Constraints**: Tell it to only read files, not modify anything

**Keep it unbiased.** Do not include your own conclusions or preferred answer. Present the problem neutrally so Claude forms its own opinion.

**Be specific about files.** Tell Claude exactly which files to read — it has access to the repo but needs direction.

## Example

```bash
claude -p \
  --permission-mode dontAsk \
  --allowedTools Read,Grep,Glob,LS \
  --add-dir "/path/to/project" \
  "Review the file at src/config.py. Is the retry logic correct? Read the file and give your assessment. Do NOT modify any files."
```

## Troubleshooting

- **Authentication**: If Claude exits with an auth error, ask the user to run `claude auth` or configure the required Claude credentials before retrying.
- **Tool restrictions**: If Claude cannot read the requested files, retry with a narrower prompt and the same read-only tools. Do not remove read-only restrictions unless the user explicitly approves.
- **Output truncation**: Claude may produce a long review. Keep prompts focused and ask specific questions rather than open-ended reviews.
- **Session state**: Use `-p` for a fresh non-interactive answer. Do not use `--continue` or `--resume` unless the user specifically asks to continue an existing Claude session.

## After Claude Responds

1. Report the Claude response to the user
2. Note where you agree or disagree with Claude's assessment
3. Let the user decide how to proceed
