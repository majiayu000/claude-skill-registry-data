---
name: mkdraft
description: Creates a timestamped markdown draft file for iterating on long-form content like PR descriptions, release notes, or issue descriptions
---

# Create Draft

Use this skill when you need to create and iterate on long-form content that will eventually be used with other commands or tools.

## When to Use

Use this skill when:
- Writing PR descriptions, issue descriptions, or release notes
- Creating content that may need multiple rounds of feedback or iteration
- Writing anything longer than a few lines that might benefit from being refined before final use
- The final content will be passed to a command that accepts file input (e.g., `gh pr create --body-file`)

This approach is better than generating large content directly because it:
- Gives the user a dedicated file to review and edit
- Allows for iterative improvements without rewriting everything
- Keeps drafts organized by date for future reference

## How the Skill Works

1. The skill runs the mkdraft command to reserve a timestamped filename
2. The command outputs a filename in format `drafts.local/YYYY-MM-DD_NNN.md`
3. Draft content is written to that file
4. The file can be reviewed, edited, and refined iteratively
5. Once ready, the file path can be used with other commands

## Implementation Details

The mkdraft command:
- Takes **no arguments** - invoke as `mkdraft` directly
- **IMPORTANT**: The command is already in your $PATH. Just run `mkdraft` from anywhere - do NOT cd to the skill directory
- Manages numbered drafts automatically within each day
- Handles file existence checking to avoid overwrites
- Persists state in `drafts.local/state.json`
- Draft numbering resets daily (increments within a day, resets next day)

## Example Workflow

When writing a PR description:
1. Use this skill to get a reserved draft filename
2. Write the PR description content to that file
3. User can review and optionally edit the draft
4. Pass the file to `gh pr create --body-file <draft-file>`

Or for release notes, issue descriptions, or any other long-form content that needs iteration.
