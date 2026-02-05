---
name: file-history
description: Use when looking for past work on specific FILES, understanding why code was written, or when user references "what we did before" on a file/feature. Uses file-history tracking for accurate results. PREFER THIS over episodic-memory for file-specific queries.
---

# File History Context

**Use this for FILE-SPECIFIC history queries. For general semantic search across all conversations, use episodic-memory instead.**

## When to Use This Skill

**USE file-history when:**
- Looking for sessions that edited a specific file
- Understanding why code was written a certain way
- User says "what did we do with [filename]"
- User asks about past changes to a component/module
- Refactoring and need to understand original intent
- Code seems unusual and you want the backstory

**DON'T use this when:**
- General conceptual questions across all projects → use episodic-memory
- No specific file/feature in mind → use episodic-memory
- Looking for patterns across unrelated conversations → use episodic-memory

## How to Use

Dispatch the `history-context` agent:

```
Task tool:
  description: "Find history for [file/feature]"
  prompt: "Find context for [specific file or feature]. Focus on [decisions/implementation/rationale]."
  subagent_type: "history-context"
```

**Example prompts:**
- "Find context for src/components/AuthForm.tsx"
- "What sessions worked on the caching implementation?"
- "Get history for the payment processing feature"

## What You Get Back

The agent will return:
- Summary of what was done and why
- Key decisions and rationale
- Implementation notes
- **Full session IDs** (UUIDs) for reference
- Session file paths for direct access

## Why This Works Better Than episodic-memory for Files

| Aspect | file-history | episodic-memory |
|--------|--------------|-----------------|
| Accuracy | Uses Claude's file-history tracking | Semantic search (fuzzy) |
| Speed | Indexed, instant | Searches full conversations |
| File mapping | Knows exactly which sessions edited which files | Guesses from content |
| Git dependency | None | None |
| Project scope | Per-project | Cross-project |

## Technical Details

Uses `~/.claude/commands/claude-history.py` which:
1. Scans `~/.claude/file-history/` to build file→session index
2. Cross-references with `~/.claude/projects/` for session metadata
3. Reads and synthesizes conversation content
4. Returns structured context with full session IDs
