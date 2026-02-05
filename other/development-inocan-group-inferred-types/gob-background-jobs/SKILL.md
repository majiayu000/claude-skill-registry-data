---
name: gob-background-jobs
description: Use when user requests "parallel" commands, running multiple builds/tests simultaneously, or long-running tasks. Use `gob add` instead of parallel Bash tool calls - gob provides job management, output capture, and proper process control.
---

# Managing Background Jobs with `gob`

## Overview

`gob` (Background Job Manager) runs tasks asynchronously while keeping context free. Essential for builds, tests, dev servers, and any long-running commands.

**When to use**:
- User explicitly asks for "parallel" or "simultaneous" commands → use `gob add` for each
- Long-running command that would block context → use `gob add`
- Multiple independent commands to run at once → use `gob add` for each

**Why gob over parallel Bash tool calls**: `gob` provides job IDs, output capture, status monitoring, and proper process control. Parallel Bash calls just fire and forget.

## CRITICAL: Parallel Command Requests

When user says "run X and Y in parallel" or "run two parallel builds":

```bash
# ✅ CORRECT: Use gob add for each command
gob add pnpm build
gob add pnpm build

# Then await results
gob await-any
gob await-any

# ❌ WRONG: Do NOT use parallel Bash tool calls
# Bash(pnpm build) + Bash(pnpm build) in same message
```

**Why this matters**: Parallel Bash tool calls work but provide no job management. `gob` gives you job IDs, status checks, output streaming, and the ability to stop/restart jobs.

## Core Concepts

### The Problem Without `gob`

```bash
# ❌ BLOCKS: Claude Code waits for this to finish
npm run build
npm test
npm run lint

# Total time: Sequential, slow, context locked
```

### The Solution With `gob`

```bash
# ✅ DISPATCHES: Returns immediately with job IDs
gob add npm run build    # Job #1
gob add npm test         # Job #2
gob add npm run lint     # Job #3

# Continue working while jobs run...
# Then collect results when ready
```

**Key insight**: `gob add` starts a job and returns immediately. You never wait. You work. You collect results later.

## Sequential Execution

Use sequential execution when:

- A command must complete before the next one starts
- Result of one command needed for the next
- Order matters
- Examples: `build` → `test`, `compile` → `verify`, database migrations → seed data

### Pattern: Sequential with Await

```bash
# Dispatch first command
JOB_ID=$(gob add make build)

# Wait for it (blocks here, but only here)
gob await $JOB_ID

# If it passed, dispatch next
JOB_ID_2=$(gob add npm test)
gob await $JOB_ID_2

# Result known, proceed
```

### Process

1. **Dispatch**: `gob add <command>` → returns job ID immediately
2. **Await**: `gob await <job_id>` → streams output, returns exit code
3. **Check result**: If exit code is 0, continue. If non-zero, handle error
4. **Next command**: Only run next command if previous succeeded

### Key Points

- **One await per command**: Always explicitly wait for sequential commands
- **Check exit codes**: Know if a command succeeded or failed
- **Error handling**: Stop on first failure or continue gracefully
- **Clear naming**: Use descriptive job names in comments

## Parallel Execution

Use parallel execution when:

- Commands are independent (don't depend on each other's output)
- Running them together is faster than sequential
- Examples: lint + typecheck, test suite 1 + test suite 2, API build + UI build

### Pattern 1: Start All, Await All

Good when you have a few known parallel tasks:

```bash
# Dispatch all jobs
gob add npm run lint
gob add npm run typecheck
gob add npm test

# Collect results (order doesn't matter)
gob await-any
gob await-any
gob await-any
```

**How it works**:

1. `gob add` three times → all three start in parallel
2. `gob await-any` → waits for whichever finishes first, returns result
3. Call `await-any` three times total to wait for all three jobs

### Pattern 2: Specific Job Await

Good when you need specific jobs' results:

```bash
# Dispatch parallel jobs
LINT_JOB=$(gob add npm run lint)
TYPE_JOB=$(gob add npm run typecheck)
TEST_JOB=$(gob add npm test)

# Wait for specific jobs
gob await $LINT_JOB
gob await $TYPE_JOB
gob await $TEST_JOB

# Check all passed before proceeding
```

### Pattern 3: Parallel Build Steps

```bash
# Dispatch parallel compilation tasks
gob add npm run build:frontend
gob add npm run build:backend
gob add npm run build:types

# Wait for all to complete
gob await-any
gob await-any
gob await-any

# All complete, package everything
gob add npm run package
```

### Key Points

- **Independence**: Jobs truly don't depend on each other
- **Dispatch first**: Start all jobs before awaiting any
- **await-any**: Call once per job when using this pattern
- **gob list**: Check job status anytime with `gob list`
- **Latency**: Parallel jobs reduce total time significantly

## Common Patterns

### Pattern: Long Test Run

```bash
# Start expensive test suite
TEST_JOB=$(gob add npm run test:integration)

# Implement feature or write docs
# (Tests run in background)

# Check if done:
gob list   # See status

# Wait for completion:
gob await $TEST_JOB
```

## Job Management

### View Job Status

```bash
gob list
```

### Get Job Output

```bash
# Wait for job and stream output
gob await <job_id>

# Returns exit code (0 = success, non-zero = failure)
```

### Stop a Job

```bash
# Graceful stop (allows cleanup)
gob stop <job_id>

# Force kill (immediate termination)
gob stop --force <job_id>
```

### Restart a Job

```bash
# Stop and restart a specific job
gob restart <job_id>
```

### Remove a Job

```bash
# Remove a stopped job from list
gob remove <job_id>
```

### Real-Time Monitoring

```bash
# Watch jobs as they run
watch gob list

# Or check once
gob list
```

## Best Practices

### ✅ DO

- **Use `gob add` for all long-running commands** (builds, tests, servers)
- **Dispatch all parallel jobs before awaiting any** (maximizes concurrency)
- **Check exit codes** after sequential operations
- **Use descriptive comments** to explain job purpose
- **Clean up stopped jobs** periodically with `gob remove`
- **Monitor with `gob list`** if uncertain about job status
- **Use `--prompt-only`** with CLI tools (smaller output)

### ❌ DON'T

- **Don't use `npm run build &`** - Use `gob add npm run build` instead
- **Don't use `command &`** - `gob` handles backgrounding
- **Don't forget to await sequential commands** - Result matters
- **Don't mix bash backgrounding with gob** - Creates confusion
- **Don't await the same job twice** - Job completes once
- **Don't ignore exit codes** - Errors need handling
- **Don't let job list grow unbounded** - Remove completed jobs

### Conditional Parallel Execution

```bash
# Phase 1: Build must complete first
gob add npm run build
gob await-any

# Phase 2: Run quality checks in parallel (only if build succeeded)
gob add npm run lint
gob add npm run typecheck
gob add npm test

# Phase 3: Wait for all quality checks
gob await-any
gob await-any
gob await-any

# Phase 4: Package only if all checks pass
gob add npm run package
```
