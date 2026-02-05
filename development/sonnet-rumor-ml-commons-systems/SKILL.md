---
name: sonnet
description: Override default model selection for specific subagents to use Sonnet instead of Opus. Use ONLY when the user explicitly requests to use Sonnet model for Plan, code-reviewer, code-simplifier, or Resolve Conflicts agents. Do not use this skill proactively - it requires explicit user instruction.
---

# Sonnet Model Override

## Overview

Use Sonnet model for specific subagents that normally run with Opus. This provides faster execution with lower cost while maintaining high quality for most tasks.

## When to Use This Skill

**IMPORTANT**: Only use this skill when the user explicitly requests to use Sonnet. Examples:

- "Use Sonnet for the code review"
- "Run the plan agent with Sonnet"
- "Use Sonnet model for this"

Do NOT use this skill proactively or by default.

## Supported Subagents

This skill applies to the following subagents only:

1. **Plan** - Planning and exploration agent
2. **pr-review-toolkit:code-reviewer** - Code review agent
3. **pr-review-toolkit:code-simplifier** - Code simplification agent
4. **Resolve Conflicts** - Merge conflict resolution agent

## Usage

When invoking any of the supported subagents, add the `model` parameter set to `"sonnet"`:

### Examples

**Plan agent with Sonnet:**

```
Task(
  subagent_type="Plan",
  model="sonnet",
  prompt="Plan the implementation of the new feature",
  description="Plan new feature"
)
```

**Code reviewer with Sonnet:**

```
Task(
  subagent_type="pr-review-toolkit:code-reviewer",
  model="sonnet",
  prompt="Review the recent changes for code quality issues",
  description="Review code changes"
)
```

**Code simplifier with Sonnet:**

```
Task(
  subagent_type="pr-review-toolkit:code-simplifier",
  model="sonnet",
  prompt="Simplify the code while preserving functionality",
  description="Simplify code"
)
```

**Resolve Conflicts with Sonnet:**

```
Task(
  subagent_type="Resolve Conflicts",
  model="sonnet",
  prompt="Resolve the merge conflicts in the current branch",
  description="Resolve merge conflicts"
)
```

## Important Notes

- The `model` parameter accepts: `"sonnet"`, `"opus"`, or `"haiku"`
- Only add this parameter when explicitly requested by the user
- Sonnet provides a good balance of speed, cost, and quality for most tasks
- For particularly complex tasks, Opus may still be preferable (but only use if user requests it)
