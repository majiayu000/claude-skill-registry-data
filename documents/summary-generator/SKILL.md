---
name: summary-generator
description: Generates session summaries and resume prompts for multi-session work. Use when completing features, before context limits (~50% capacity), or when user says "summary", "wrap up", "save progress", "end session". Creates markdown in docs/summaries/ with completed work, files modified, and restart instructions.
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git status:*), Write
---

# Session Summary Generator

## Overview

This skill creates comprehensive session summaries for complex multi-session work, enabling seamless resumption of tasks. It generates a markdown file in `docs/summaries/` with a standardized format.

## When to Use

Trigger this skill when:
- User explicitly requests a summary ("generate summary", "wrap up", "save progress")
- Completing a significant feature or refactor
- Conversation context is reaching limits (~50% before auto-compact)
- Before starting a new chat session
- When collaborating with team members on the same feature

### Auto-Suggest Triggers

Proactively suggest generating a summary when:
- Multiple files have been modified in the session
- A feature implementation is complete
- The conversation has been long (many exchanges)
- User mentions ending their work session

## Output Location

Session summaries are stored in: `docs/summaries/YYYY-MM-DD_feature-name.md`

## Instructions

### Step 1: Analyze Current Work

Run these commands to understand what was done:

```bash
git status
git diff --stat
git log --oneline -10
```

Review the conversation history to identify:
- What was accomplished
- Key decisions made
- Files created or modified
- Any remaining tasks

### Step 2: Generate Summary File

Create the summary using the template in [TEMPLATE.md](TEMPLATE.md).

Key sections to include:
1. **Overview**: Brief description of session focus
2. **Completed Work**: Bullet points of accomplishments
3. **Key Files Modified**: Table of files and changes
4. **Design Patterns Used**: Important architectural decisions
5. **Remaining Tasks**: What's left to do
6. **Resume Prompt**: Copy-paste instructions for next session

### Step 3: Create Resume Prompt

The resume prompt should include:
- Context reference to the summary file
- Specific file paths to review first
- Current status and immediate next steps
- Any blockers or decisions that need user input

## Example Usage

When user says: "Let's wrap up for today"

Response:
1. Analyze git changes and conversation history
2. Create `docs/summaries/2025-12-30_enrollment-improvements.md`
3. Provide the resume prompt for the next session
4. Suggest: "When context gets long, consider starting a new chat with the resume prompt"

## Tips

- Keep summaries focused on a single feature or area
- Include exact file paths for easy navigation
- Note any environmental setup needed (database migrations, etc.)
- Flag any blocking issues or decisions made
- Reference the CLAUDE.md file patterns when applicable
