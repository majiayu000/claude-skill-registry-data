---
name: context-initializer
description: Automatically invokes init-explorer agent when project context is empty or unknown.
---

# Context Initializer

This skill detects when Claude Code lacks project context and automatically invokes the init-explorer agent to gather it.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **No project context**: You don't know what this project is about, its tech stack, or its purpose
2. **Missing session history**: `claude-progress.txt` doesn't exist or hasn't been read
3. **Missing architect's digest**: `architects_digest.md` doesn't exist or hasn't been read
4. **User asks context-dependent questions**: The user asks about the project but you have no context
5. **Starting a new task**: Beginning work on a feature without understanding the codebase

## How to Check for Empty Context

Before invoking, verify context is actually missing:

```bash
# Check if session files exist
ls -la claude-progress.txt architects_digest.md 2>/dev/null || echo "Context files missing"
```

## Invocation

When context is empty, invoke the init-explorer agent:

```
Task(subagent_type="init-explorer", prompt="
Gather project context for this codebase.

next_agent: none
task: Explore and document project structure, tech stack, and patterns

After exploration, return a summary of:
1. Project purpose and description
2. Tech stack (languages, frameworks, databases)
3. Key directories and their purpose
4. Testing setup
5. Build/run commands
")
```

## What init-explorer Will Do

The init-explorer agent will:

1. **Orient**: Run `pwd`, `ls -la`, `git log`, `git status`
2. **Read History**: Check `claude-progress.txt` for previous sessions
3. **Read Digest**: Check `architects_digest.md` for task state
4. **Explore**: Use Explore subagent for deep codebase analysis
5. **Create Files**: Initialize `architects_digest.md` if missing
6. **Update Progress**: Log the exploration session

## Expected Output

After init-explorer completes, you will have:

- Understanding of the project's tech stack and purpose
- Knowledge of coding patterns and conventions
- Awareness of test setup and build commands
- Session logged in `claude-progress.txt`
- Task tracking initialized in `architects_digest.md`

## Example Usage

**Scenario**: User asks "How does authentication work in this project?"

**Before**: You have no context about the project.

**Action**: Invoke this skill to run init-explorer.

**After**: You understand the project uses Flask with JWT authentication, tests are in `tests/`, and the auth module is in `src/auth/`.

## Do NOT Invoke When

- You already have project context from earlier in the conversation
- The user explicitly said not to explore
- You're in the middle of a task that already has context
- The init-explorer agent has already run in this session
