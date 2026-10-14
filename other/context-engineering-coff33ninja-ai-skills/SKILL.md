---
name: context-engineering
description: Token-aware context management — selects what context to include, when to load reference files, how to use progressive disclosure. Prevents context bloat while ensuring the right information is available.
---

# Context Engineering

## Problem it solves

Without intentional context management, agents waste tokens and miss critical information:
- Loading entire files when only a few lines are needed
- Keeping irrelevant context in the window, crowding out useful information
- Missing important reference files because they weren't loaded
- Context overload degrading model performance
- Re-reading the same files multiple times instead of caching key information

## Protocol

### 1. Assess the task scope

Before loading any context, determine:
- **What kind of task?** (implement, debug, review, research, document)
- **What files are needed?** (be specific: which file, which function)
- **What is the minimum context to start?** (start lean, add as needed)

Use progressive disclosure: load only what you need now, not everything you might need.

### 2. Context prioritization

Rank context by importance:

| Priority | What | When |
|----------|------|------|
| P0 | Current file being edited | Always |
| P1 | Direct dependencies / imports of current file | Always |
| P2 | Similar files (same pattern/convention) | When implementing similar feature |
| P3 | Tests for current file | When implementing or debugging |
| P4 | Config files, package manifests | When adding dependencies |
| P5 | Documentation, README, ADRs | When understanding architecture |
| P6 | Historical context (git log, past PRs) | When debugging regressions |

Load P0-P1 immediately. Add P2+ only when needed for the current step.

### 3. Progressive disclosure pattern

```
Step 1: Load P0-P1 context
     ↓
Step 2: If unclear, load P2-P3
     ↓
Step 3: If still unclear, load P4-P5
     ↓
Step 4: As a last resort, load P6
```

If you're at Step 4, consider whether you have enough context or need to ask the user.

### 4. Token budget management

Be aware of context window limits:
- **Small reads over large reads**: Read specific functions/sections, not entire files
- **Use search tools efficiently**: Search for what you need, don't dump the file
- **Summarize after reading**: Condense what you've read into a summary to retain key facts
- **Drop irrelevant context**: Once a file is no longer needed, stop referencing it

### 5. Reference file linking

When multiple files are related:
- Note file names and key line numbers for quick re-access
- Group related reads together (read all files for one step at once)
- Avoid re-reading files you've already processed — retain the key information

## Detection triggers

Activate when:
- Starting a new task that requires context
- Loading project files for the first time
- Context window is getting full and performance is degrading
- About to read a large file — ask "do I need all of this or just a section?"
- User provides a multi-step request with multiple files involved

## When NOT to use

- Trivial single-file changes
- User explicitly provides all necessary context in their message
- Working in a familiar codebase where context is already known

## Cross-references

- **skill-loader** — Use together. skill-loader handles which skills to load; context engineering handles which project files to load.

- **dont-kill-tokens** — Token efficiency is the goal. Context engineering provides the strategy; dont-kill-tokens enforces the discipline.

- **anti-tool-sprawl** — Tool sprawl wastes context. Context engineering helps select the right tools for the current task.

- **follow-existing-patterns** — Reading existing patterns is a context engineering decision. Load 2-3 examples, not all of them.

- **incremental-implementation** — Each slice needs only the context for that slice. Start with minimal context and add as slices progress.

- **debugging-and-error-recovery** — Progressive disclosure is critical in debugging. Start with the error message, then add context as needed.
