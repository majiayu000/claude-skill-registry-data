---
name: review
description: 'Review a file, directory, or PR diff in beginner-friendly mode — structured feedback with "why" explanations Arguments: <file-path|directory|PR#>.'
---

# Beginner-Friendly Code Review

Review code with educational explanations. Target: $ARGUMENTS

## Instructions

1. Read the primary skill:
   - `${CLAUDE_PLUGIN_ROOT}/skills/codemap-review/SKILL.md` — review methodology and output format

2. Parse `$ARGUMENTS` to determine what to review:
   - If it's a file path → pass the file path to the agent
   - If it's a directory → pass the directory path to the agent
   - If it's a PR number (e.g., `#15` or `15`) → pass the PR number to the agent
   - If no argument → ask user what to review

3. Launch the **code-reviewer** agent with a prompt describing the target and any additional context from the user's message.

The agent applies 5-dimension analysis (Security, Correctness, Readability, Patterns, Beginner Pitfalls), generates educational findings, and uses codemap-explain/codemap-diagram skills when needed.