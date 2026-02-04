---
name: commit-messager
description: Write clear and concise commit messages that accurately describe the changes made in the codebase
allowed-tools: Bash(git branch:*), Bash(git diff:*)
---

## Tools
- Current git diff (staged): !`git diff --cached`
- Current branch: !`git branch --show-current`

## Your Task
Your role as a front-end developer.
Put the $ARGUMENTS [context] as additional context to write clear and concise commit message when provided.
Only output the commit message as code canvas so I can copy them, don't execute git commit message command.

## Custom Instructions
1. Analyze the staged changes in the codebase
2. Commit message must follow these rules:
  - Start with a type (feat/fix/docs/chore/refactor) according your judgement of the changes.
  - Write clear, concise, and developer-friendly commit messages under 160 characters that accurately describe the code changes in the current staged files only.
  - Use present tense and imperative mood. Explain what and why, not how.
  - Add task number with "#" character based on current branch name at the end of the commit message title. eg: <prefix>: <commit-message> #<task-id>
  - Add a few bullet points explaining the detailed change if the commit message title isn't enough to explain the changes.
    Keep in mind that bullet points aren't necessary when the commit message title is already clear and self-explanatory describing the changes.
    DON'T WRITE UNNECESSARY POINT. The explanation for each point must be unique one each other; there should be no repetition of information or context.
3. DON'T ADD YOUR SIGNATURE at the end of the commit message.tical logic code changes, add minimum 2 and maximum 5 detailed bullet points explaining the change. The explanation for each point must be different from one another; there should be no repetition of information.
