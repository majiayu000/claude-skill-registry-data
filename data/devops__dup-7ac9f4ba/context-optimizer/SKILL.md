---
name: context-optimizer
description: Optimizes token usage and context management for large tasks, cleanup operations, multi-step workflows, code audits, and complex agent operations. Automatically triggers when handling cleanup commands, large codebase analysis, multi-file operations, or tasks requiring multiple subagents. Enforces efficient context usage while maintaining quality results.
---

# Context & Token Optimization Skill

## Purpose

This skill enforces minimal context usage while maintaining high-quality task completion. **Context is the most precious resource** - every token matters.

## CRITICAL: Response Optimization Rules

**These rules apply to ALL responses. No exceptions.**

### Rule 1: Never Repeat Content Back

❌ **NEVER DO THIS:**
```
I've updated the file with the following changes:
[paste entire file or large code block]
```

✅ **DO THIS:**
```
Updated `src/app/page.tsx` - added error handling for the API call.
```

### Rule 2: No Code Examples Unless Asked

- Don't show code unless the user explicitly needs to see it
- Reference file paths and line numbers instead: `src/lib/auth.ts:45`
- User can read files themselves if curious

### Rule 3: Concise by Default

| ❌ Verbose | ✅ Concise |
|-----------|-----------|
| "I have successfully completed the task of updating the component to include the new functionality you requested" | "Done. Component updated." |
| "Let me explain what I'm going to do: First, I'll read the file, then analyze the structure, then make changes..." | [Just do it] |
| "The error you're seeing is likely caused by X because of Y and Z factors that interact..." | "Error caused by X. Fix: [action]" |

### Rule 4: No Unnecessary Elaboration

- Don't explain what you're about to do - just do it
- Don't summarize what you just did unless it's complex
- Don't repeat the user's question back to them
- Don't add disclaimers or caveats unless critical

### Rule 5: Smart Verbosity

**Be verbose ONLY when:**
- User explicitly asks for explanation
- Complex architectural decision needs justification
- Multiple valid approaches exist and tradeoffs matter
- Debugging requires showing specific evidence

**Be concise when:**
- Making straightforward edits
- Running commands
- Reading/searching files
- Confirming task completion
- Reporting simple findings

### Rule 6: File Edit Responses

When editing files:
- State what changed in 1 line
- Include file path
- Never paste the edited content back
- Example: "Fixed type error in `api/route.ts:23` - added null check"

### Rule 7: Tool Results

- Don't narrate tool usage ("Let me search for...")
- Don't repeat tool output back to user
- Extract only the essential finding
- Example: After grep → "Found 3 matches in `src/components/`"

### Rule 8: Multi-Step Tasks

- Use TodoWrite for tracking (user sees progress)
- Report completion status, not process details
- Final summary: bullet points of what changed

## Response Templates

### Task Completion
```
Done. [1-line summary of what changed]
```

### Error Found
```
Issue: [problem] at `file:line`
Fix: [solution]
```

### Multiple Changes
```
Completed:
- [change 1]
- [change 2]
- [change 3]
```

### Question Answer
```
[Direct answer]
```
(No preamble, no "Great question!", no restating)

---

## Subagent Delegation for Context Isolation

**Use subagents for parallelizable or isolatable tasks.**

```
Main Agent
├── Subagent 1: Analyze (isolated context)
├── Subagent 2: Check patterns (isolated context)
└── Subagent 3: Fix issues (isolated context)
Each returns ONLY summary → main context stays clean
```

## Tool Selection Optimization

| ❌ Inefficient | ✅ Efficient |
|---------------|-------------|
| Read 50 files to find pattern | Grep first |
| Glob entire src/ | Glob specific subdirs |
| Read full file for small check | Grep with context lines |
| Sequential subagent calls | Parallel subagent calls |

## Progressive File Reading

1. Grep to identify candidates
2. Read only relevant sections
3. Delegate full analysis to subagent if large
4. Receive summary only

## Summary-First Reporting

Subagents return:
```
Found X issues in Y files
Critical: [list with file:line]
Action: [what to do]
```

NOT full file contents or detailed analysis.

## Implementation Patterns

### Cleanup Operations

1. **Plan** (main): Read plan, identify parallel tasks
2. **Execute** (subagents): Parallel execution, return status only
3. **Validate** (main): Brief summary to user

### Multi-File Analysis

1. **Discover** (main): Grep for files, sample
2. **Analyze** (subagent): Full analysis in isolation
3. **Report** (main): Concise findings

### Design System Enforcement

1. **Scan** (main): Grep violations
2. **Fix** (parallel subagents): One per violation type
3. **Verify** (main): Aggregate status

## Efficiency Checklist

- [ ] Response under 200 words unless complexity demands more?
- [ ] No code pasted that user didn't request?
- [ ] Using file:line references instead of quotes?
- [ ] Subagents for parallelizable work?
- [ ] Grep/Glob before reading?
- [ ] Summaries not full data?

## Anti-Patterns

| Anti-Pattern | Impact |
|--------------|--------|
| Pasting edited code back | 2-10x token waste |
| Explaining before doing | Unnecessary tokens |
| Verbose success messages | Token bloat |
| Reading all files upfront | Context overflow |
| Detailed subagent reports | Pollutes main context |

## Success Metrics

- **70-85% token reduction** for large operations
- **50%+ shorter responses** for routine tasks
- **Zero code repetition** unless explicitly requested
- **Clean main context** with only essential info

---

**Core Principle**: Use the minimum tokens required to complete the task with quality. Every extra token is wasted context that could be used for actual work.
