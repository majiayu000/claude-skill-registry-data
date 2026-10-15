---
name: ralph-prompt-generator
description: >-
  Generate auto-compact-resilient Ralph Wiggum loop prompts for Claude Code, with a PRD and progress file for large features. Triggers: ralph, ralph wiggum, ralph loop, loop until done, autonomous loop, keep going until complete.
---

# Ralph Wiggum Prompt Generator

Generate production-ready Ralph Wiggum loop prompts that survive Claude Code's auto-compact behavior.

## Quick Reference

**Small tasks** (single concern, <30 min): Generate prompt only  
**Large features** (multiple stories, hours of work): Generate PRD + prompt

## Core Principle: Auto-Compact Resilience

Claude Code auto-compacts at ~78% context. The standard Ralph Wiggum approach loses state. The solution: external state files that persist across compaction.

### State Files

1. **`prd.json`** - Tracks user stories with `passes: true/false`
2. **`progress.txt`** - Learnings and blockers from each iteration  
3. **Git history** - Commits serve as persistent memory

The prompt instructs Claude to **always read these files first** on each iteration.

## Workflow

### Step 1: Analyze the Request

Ask yourself:
- Is this a single, well-defined task? → Small task
- Does it have multiple components or stories? → Large feature
- Will it take more than ~30 minutes? → Large feature
- Could Claude lose track if context compacts mid-work? → Large feature

### Step 2: Generate Output

**For small tasks**: Generate a self-contained Ralph loop prompt.

**For large features**:
1. Generate a `prd.json` with prioritized user stories
2. Generate a `progress.txt` template
3. Generate the Ralph loop prompt that references these files

## Small Task Prompt Template

```
/ralph-loop "[TASK_DESCRIPTION]

## Context
[BRIEF_CONTEXT_ABOUT_CODEBASE_OR_PROBLEM]

## Success Criteria
- [CRITERION_1]
- [CRITERION_2]
- [CRITERION_3]

## Verification
Run: [VERIFICATION_COMMAND]

Output <promise>DONE</promise> when ALL criteria pass." --max-iterations [N] --completion-promise "DONE"
```

**Guidelines:**
- `--max-iterations`: 10-20 for small tasks, 30-50 for medium
- Always include verification command (test, lint, build, etc.)
- Success criteria must be objectively verifiable

## Large Feature: State Files

Generate both files in the project root, from the templates:

- `prd.json`: copy `assets/prd-template.json`. Fields: `featureName`, `branchName`, `description`, `userStories[]` with `id`, `title`, `description`, `priority`, `dependsOn`, `acceptanceCriteria`, `verificationCommand`, `passes` (false until verified).
- `progress.txt`: copy `assets/progress-template.txt` (codebase patterns, completed stories, blockers, session notes, error patterns).

**Story sizing rule**: Each story must be completable within one context window. If it's too big, split it.

## Large Feature Prompt Template

Use `assets/large-feature-prompt.txt` verbatim (replace `[N]`). It makes the loop read state files first, implement the next eligible story, verify, update `prd.json` and `progress.txt`, commit, and output `<promise>COMPLETE</promise>` or `<promise>BLOCKED</promise>`.

**Iteration guidelines:**
- 50-100 for multi-story features
- Plan ~5-10 iterations per story
- Always set `--max-iterations` as safety net

## Examples

Worked small-task and large-feature examples: [references/examples.md](references/examples.md). Edge cases (multi-phase, error-analysis, TDD, migration, overnight batch, auto-compact recovery, debugging): [references/advanced-patterns.md](references/advanced-patterns.md).

## Anti-Patterns to Avoid

1. **No verification command**: Always include one. No verification = loop runs forever.
2. **Vague success criteria**: "Make it work" → bad. "All tests pass" → good.
3. **Stories too large**: If story could take 30+ min, split it.
4. **Missing state files for large tasks**: Always generate PRD for multi-story work.
5. **Forgetting --max-iterations**: Always set a safety limit.

## Customization Options

When generating prompts, ask user about:
- Preferred iteration limit
- Verification commands (test framework, linter, etc.)
- Whether to include auto-commit behavior
- Specific coding standards or patterns to follow
