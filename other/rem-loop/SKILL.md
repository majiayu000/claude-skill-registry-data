---
name: rem-loop
description: 'Autonomous agentic loop patterns for multi-iteration work — PR Loop (branch → implement → CI → auto-fix → repeat with SHARED_TASK_NOTES.md context bridge) and De-Sloppify (two-pass - implementation agent then dedicated cleanup agent). Use when a task requires many iterations against CI feedback, when you want a post-implementation cleanup pass without negative constraints, or when you need to bridge context between loop iterations. Distinct from the built-in /loop (which schedules recurring prompts on an interval) — rem-loop provides the PATTERNS for building autonomous development loops. Use for "autonomous loop", "keep running until CI passes", "pr loop", "loop until green", "agentic loop", "cleanup pass", "de-sloppify", "two-agent pattern", "context bridge", "SHARED_TASK_NOTES".'
user-invocable: true
allowed-tools: Bash, Read, Write, Agent, AskUserQuestion
argument-hint: '''[pattern to use: "pr-loop" or "de-sloppify", or describe task]'''
---

# Autonomous Loop Patterns

Two production-tested patterns for running Claude Code autonomously across multiple iterations. These are operational blueprints, not magic — they work because they solve the two hard problems of autonomous loops: context loss between iterations and quality degradation from constraint accumulation.

---

## Pattern 1: PR Loop

**When to use**: multi-session feature work that needs to run CI gates, auto-fix failures, and continue without you watching it. Works best for tasks where the acceptance criterion is "CI passes" and the work requires multiple fix cycles.

**The core problem it solves**: context is lost between Claude sessions. Without a bridge, each iteration starts cold and re-discovers the same state. `SHARED_TASK_NOTES.md` is the solution.

### How It Works

```
branch → implement → commit → run CI → 
  if CI passes: done
  if CI fails: read failures → read SHARED_TASK_NOTES.md → fix → commit → run CI → repeat
```

### SHARED_TASK_NOTES.md Structure

Create this file at repo root at the start of the loop. Claude reads it at the top of every iteration and writes to it at the end. It bridges the context gap.

```markdown
# Task: [feature name]

## Goal
[one-paragraph description of what done looks like]

## Acceptance Criteria
- [ ] CI passes (yarn build + tests)
- [ ] [specific criterion 2]
- [ ] [specific criterion 3]

## Progress Log
<!-- Claude appends here each iteration -->
- [YYYY-MM-DD HH:MM] Iteration 1: [what was done, what failed]
- [YYYY-MM-DD HH:MM] Iteration 2: [what was fixed, what's still failing]

## Known Issues
<!-- Claude writes blockers here so next iteration doesn't re-discover them -->

## Files Changed
<!-- Running list so each iteration knows what's in play -->
```

### Setup Prompt Template

Tell Claude:
```
Read SHARED_TASK_NOTES.md. Implement the next iteration toward the goal. 
Run: [CI command — e.g. yarn build && yarn test]
If CI fails, fix failures and commit. 
Before stopping, update SHARED_TASK_NOTES.md Progress Log with what you did and what remains.
Stop when all Acceptance Criteria are checked.
```

Pair this with the `ralph-loop` plugin (already installed) for Stop-hook-based iteration, or run iterations manually.

### Guard Rails

- Set `--max-iterations N` so a stuck loop doesn't run forever
- Use `SHARED_TASK_NOTES.md` to surface blockers that require human input: Claude writes "BLOCKED: [reason]" and stops
- Review the Progress Log after each iteration to catch loops going in circles

---

## Pattern 2: De-Sloppify

**When to use**: after completing an implementation, when you want a cleanup pass — removing dead code, normalizing patterns, tightening types — WITHOUT constraining the implementation agent's creative freedom during the first pass.

**The core insight**: "two focused agents outperform one constrained agent." If you tell the implementation agent "implement this AND keep it clean AND don't add dead code AND normalize patterns," you get mediocre work on all dimensions. If you separate the passes, each agent has one job and does it well.

### How It Works

```
Pass 1 (Implementation Agent): implement without cleanup constraints
  → commit checkpoint
Pass 2 (Cleanup Agent): dedicated cleanup with no new feature work
  → cleanup commit
```

### Pass 1 Prompt

Tell Claude:
```
Implement [feature]. Focus entirely on correctness and completeness. 
Do not worry about dead code, style consistency, or cleanup — those happen in a second pass.
When done, commit with message "feat: [feature] — pre-cleanup checkpoint".
```

### Pass 2 Prompt (new Claude session or new conversation turn)

Tell Claude:
```
Review the changes from the last commit. Your ONLY job is cleanup — no new features, no behavior changes.
Clean up:
- Dead code introduced during implementation
- Inconsistent naming vs. the rest of the codebase
- Type widening that can be tightened
- Imports that are unused
- Comments that describe what the code does (remove) vs. why (keep)
Run: [typecheck + lint command]
Commit with message "chore: cleanup [feature] post-implementation".
```

### When NOT to Use De-Sloppify

- Simple 1-2 file changes where cleanup is obvious inline
- Highly interdependent changes where pass separation would require re-reading all context anyway
- When the "cleanup" would require understanding business logic (that's still Pass 1 territory)

---

## Choosing Between Patterns

| Situation | Pattern |
|---|---|
| Multi-day feature, CI-driven acceptance, context loss is a risk | PR Loop |
| Single session, implementation done, want a quality pass | De-Sloppify |
| Both — multi-day feature where quality matters | PR Loop for iterations, De-Sloppify as final pass before PR |

---

## Anti-Patterns

**The unbounded loop**: no max-iterations, no BLOCKED escape hatch, no human checkpoint. Claude silently makes the same mistake 20 times.

**The unchecked SHARED_TASK_NOTES.md**: notes grow stale and contradict each other. Set a convention: Claude prunes resolved items each iteration.

**De-Sloppify with behavior changes**: if Pass 2 starts "fixing" behavior it noticed while cleaning, you've lost the separation. Cleanup agent should commit only non-behavior-changing diffs. Check with `git diff --stat` before Pass 2 commits.

**Negative constraints in Pass 1**: "implement this but don't add dead code" is a constraint that degrades Pass 1 quality. Trust the separation.
