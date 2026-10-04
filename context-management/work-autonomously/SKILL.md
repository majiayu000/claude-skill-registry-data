---
name: work-autonomously
description: Shared rules for unattended execution — only load when explicitly referenced by another command or skill. Never auto-trigger based on user prompts.
---

# Autonomous Conventions

Rules for commands and skills that run without user input (e.g., `/ops:get-to-work`, `/ops:batch-execute`). The goal is to keep moving and defer human judgment to a structured follow-up review.

## Core Rules

1. **Never stop for user input.** Record questions and move on.
2. **Never delete files.** Record intended deletions in the follow-up file.
3. **Never push to remote.** Only local branches and commits.
4. **When uncertain, make a sensible choice and move on.** Record your reasoning and alternatives in the follow-up file so the user can review. Only skip when the wrong choice could have truly bad consequences (data loss, security, breaking external contracts). Getting work done with transparent doubts beats a slightly lower chance of mistakes.

## Follow-Up File

Create a follow-up `.md` file in the project's plans directory (`.plans/` or `plans/`, whichever the project uses) at the start of the process. It captures everything that needs human review afterward.

### Required sections

```markdown
## Controversial Decisions
Items where the agent made a judgment call the user should review.

## Skipped Items
Opportunities identified but not acted on, with reasons.

## User Input Needed
Questions that blocked progress on specific items.

## Files to Delete
Files that should be removed (agent does not delete files autonomously).

## Implementation Issues
Problems encountered during execution.

## Borderline Insights
Findings that might warrant persisting to the project's knowledge system (e.g., MEMORY.md, CLAUDE.md, or equivalent) but the agent wasn't confident enough to add directly. User should review and decide whether to keep or discard.

## Suggested Follow-Up Work
Potential new work items that emerged during execution but the agent wasn't confident enough to add directly (e.g., to a backlog, TODO list, or issue tracker). User should review and decide whether to act on or discard.
```

Not every section will be used by every command — include the ones that are relevant.

## Resolving Follow-Up Items

After all work is complete, go through follow-up items with the user:

1. Use the **AskUserQuestion** tool with concrete options derived from the context (e.g., "Keep as-is", "Revert this commit", "Modify to X") plus an "Other (I'll specify)" option.
2. Don't ask open-ended questions when you can present sensible choices.
3. Document each resolved item in the related plan file.
4. Once all items are resolved and integrated into their plan files, delete the follow-up file.

## Bash Command Rules

Respect the bash command allowlist rules from CLAUDE.md so the process doesn't get interrupted for user confirmations.

### Temporary files

If your project CLAUDE.md says to create temp files instead of running inline Python/Node in Bash, then delete them afterward: during autonomous execution, do NOT delete temp files — `rm` may require user confirmation and will interrupt the unattended run. Instead, add the file path to the **Files to Delete** section in the follow-up file. The user will clean them up during follow-up review.
