---
name: codex
description: Get a second opinion from OpenAI Codex CLI. Use when you want to cross-check your reasoning, validate a plan, or get an independent review.
argument-hint: <task or question for Codex>
user-invocable: true
allowed-tools: Bash(codex *), Read, Grep, Glob
---

# Codex Second Opinion

Delegate a task to OpenAI's Codex CLI for an independent review or second opinion.

## Input

<task>
$ARGUMENTS
</task>

If no task is provided, ask the user what they want Codex to review.

## How to Use

Run Codex in non-interactive mode with read-only sandbox:

```bash
codex exec --full-auto --skip-git-repo-check -s read-only -C "<current working directory>" "<prompt>" 2>/dev/null
```

## Prompt Construction

Build a self-contained prompt for Codex that includes:

1. **Context**: The repo path, what project this is, and what folder/files are relevant
2. **The task**: What you want Codex to do (review, validate, suggest, etc.)
3. **Constraints**: Tell it to only read files, not modify anything

**Keep it unbiased.** Do not include your own conclusions or preferred answer. Present the problem neutrally so Codex forms its own opinion.

**Be specific about files.** Tell Codex exactly which files to read — it has access to the repo but needs direction.

## Example

```bash
codex exec --full-auto --skip-git-repo-check -s read-only -C "/path/to/project" \
  "Review the file at src/config.py. Is the retry logic correct? Read the file and give your assessment. Do NOT modify any files." 2>/dev/null
```

## Troubleshooting

- **Sandbox restrictions**: If Codex output is empty, retry with `dangerouslyDisableSandbox: true` on the Bash call. The `codex` CLI needs network access and may spawn subprocesses that hit sandbox limits.
- **Output truncation**: Codex may run many tool calls (file reads, experiments), producing very large output. Keep prompts focused and ask specific questions rather than open-ended reviews. If output is truncated, the empirical results are still valuable — look for the data in the tool call results even if the final summary is missing.
- **`--skip-git-repo-check`**: Always include this flag to avoid errors in repos with uncommitted changes.

## After Codex Responds

1. Report the Codex response to the user
2. Note where you agree or disagree with Codex's assessment
3. Let the user decide how to proceed
