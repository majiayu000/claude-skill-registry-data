---
name: walkthrough
description: Interactive walkthrough of code changes with diagrams and step-by-step explanations
argument-hint: "[focus-area]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Code Walkthrough Skill

Provide a comprehensive walkthrough of code changes with narrative explanation, ASCII diagrams, and step-by-step code analysis.

## Configuration

**Focus Area (Optional):** $ARGUMENTS

If provided, filter the walkthrough to changes related to the focus area (e.g., "authentication", "src/api/", "payment processing").

## Step 1: Verify Git Repository

First, verify we're in a git repository:

```bash
git rev-parse --git-dir 2>&1
```

If this fails, respond with:
```
Error: This directory is not a git repository.
The walkthrough skill requires git to analyze code changes.

To use this skill:
1. Navigate to a git repository, or
2. Initialize git with: git init
```

Then stop execution.

## Step 2: Detect Branch Context

Determine the current branch and what to compare against:

```bash
# Get current branch
git branch --show-current

# Check if main exists
git rev-parse --verify main 2>/dev/null

# Check if master exists
git rev-parse --verify master 2>/dev/null
```

**Decision Logic:**
- If on `main` → analyze uncommitted changes only (staged + unstaged)
- If on `master` → analyze uncommitted changes only (staged + unstaged)
- If on feature branch AND `main` exists → compare feature branch to `main`
- If on feature branch AND `master` exists (no main) → compare feature branch to `master`
- If on feature branch but no main/master → compare to the default branch or ask user

## Step 3: Gather Changes

Based on the branch context:

**For uncommitted changes (on main/master):**
```bash
# Get both staged and unstaged changes
git diff HEAD
```

**For feature branches:**
```bash
# Get all changes since branching from main/master
git diff main...HEAD  # or master...HEAD
```

Also get the list of changed files:
```bash
git diff --name-status main...HEAD  # or appropriate comparison
```

## Step 4: Filter by Focus Area (If Provided)

If `$ARGUMENTS` is provided, filter the diff and file list to only include relevant changes:

- Use grep to filter files matching the focus area
- Read only the relevant portions of the diff
- Mention at the start: "Focusing walkthrough on: [focus area]"

## Step 5: Analyze Changes (Read the Code)

For each changed file:
1. Read the current version of the file
2. Understand the context and purpose
3. Note the specific changes made
4. Identify patterns: new features, bug fixes, refactoring, etc.

## Step 6: Ask Deepening Questions (Only If Needed)

**Important:** Only ask questions if something is truly unclear or ambiguous.

Examples of when to ask:
- Large architectural changes without clear purpose
- Multiple possible interpretations of the changes
- Unclear data flow or business logic

Use the AskUserQuestion tool sparingly. Most of the time, infer intent from the code.

## Step 7: Create the Story

Write a narrative explanation of what these changes accomplish:

### Story Format:

```
## Code Changes Story

[Brief overview: what was changed and why]

### Context
[What problem is being solved or what feature is being added]

### Changes Overview
[High-level summary of what files were modified and the nature of changes]

### Key Modifications
[Bullet points of the most important changes:
- Component X was updated to...
- Function Y now handles...
- New module Z was added to...]

### Data Flow
[How data moves through the system with these changes]

### Impact
[What parts of the system are affected]
```

## Step 8: Create ASCII Diagram

Generate an ASCII art diagram showing the architecture, data flow, or component relationships affected by these changes.

### Diagram Guidelines:

- Use simple ASCII characters: `+`, `-`, `|`, `*`, `>`, `<`, `^`, `v`
- Show components as boxes
- Show data flow with arrows
- Label each element clearly
- Keep it readable and properly aligned
- Maximum width: 80 characters

### Example Diagram Format:

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         v
┌─────────────────┐     ┌──────────────┐
│  Controller     │────>│   Service    │
│  (Modified)     │     │  (New)       │
└─────────────────┘     └──────┬───────┘
                                │
                                v
                        ┌──────────────┐
                        │  Database    │
                        └──────────────┘
```

Or use simpler ASCII:

```
User Request
     |
     v
Controller (Modified) ---> Service (New)
                                |
                                v
                            Database
```

Choose the style that best represents the changes.

## Step 9: Step-by-Step Code Explanation

Walk through each changed file and explain the code changes:

### Format:

```
## Step-by-Step Code Walkthrough

### File: path/to/file.ts

**Change Type:** [Added/Modified/Deleted]

**Purpose:** [What this file does in the context of the changes]

**Key Changes:**

1. **Lines X-Y:** [Function/block name]
   ```typescript
   [relevant code snippet]
   ```

   Explanation: [What this code does and why it changed]

   Data flow: [If applicable, how data moves through this code]

2. **Lines A-B:** [Next significant change]
   [continue pattern...]

**Integration:** [How this file integrates with other changed files]

---

### File: path/to/next-file.ts
[Continue same pattern...]
```

### Code Snippet Guidelines:

- Show only the most relevant changed portions (5-15 lines)
- Include enough context to understand the change
- Use proper syntax highlighting in code blocks
- Explain the "why" not just the "what"
- Highlight the data flow and transformations

## Step 10: Summary

End with a concise summary:

```
## Walkthrough Summary

**Files Changed:** [count]
**Change Type:** [Feature/Bugfix/Refactor/etc.]
**Complexity:** [Low/Medium/High]

**Key Takeaways:**
- [Main point 1]
- [Main point 2]
- [Main point 3]

**Testing Recommendations:**
- [What should be tested based on these changes]
```

## Output Order

Present the walkthrough in this order:
1. Branch context message
2. Story
3. ASCII Diagram
4. Step-by-Step Code Explanation
5. Summary

## Style Guidelines

- Be clear and concise
- Use technical language but explain complex concepts
- Focus on understanding the "why" behind changes
- Highlight important patterns and architectural decisions
- Keep ASCII diagrams simple and readable
- Use code references with line numbers when relevant
