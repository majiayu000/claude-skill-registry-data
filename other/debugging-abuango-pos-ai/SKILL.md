---
name: debugging
description: Systematic debugging and troubleshooting playbook. Use when diagnosing bugs, investigating errors, tracing issues, or when user mentions "debug", "troubleshoot", "investigate", "error", "bug", "broken", "not working", or "trace issue".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Debugging Skill

You are systematically debugging an issue. Follow this structured approach — never brute-force retry the same thing. Every step narrows the search space.

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

## Process

### Step 1: Reproduce

Before anything else, confirm the bug exists and is reproducible.

1. **Get the error** — Exact error message, stack trace, or unexpected behavior description
2. **Get the context** — When did it start? What changed recently? Which environment?
3. **Reproduce locally** — Run the failing command/test/request and capture the full output
4. **If not reproducible** — Check environment differences, data differences, timing/race conditions

Output: "I can reproduce this: {exact steps and output}"
— OR —
"Cannot reproduce. Need: {what additional info is required}"

### Step 2: Isolate

Narrow down where the bug lives.

1. **Check recent changes** — `git log --oneline -20`, `git diff` for uncommitted work
2. **Trace the execution path** — Follow the request/data from entry point to failure
3. **Binary search** — If the codebase is large, bisect: does the bug exist in module A or B?
4. **Check boundaries** — Is the bug in our code, a dependency, the database, or the infrastructure?

Key questions:
- Does it fail with the simplest possible input?
- Does it fail in a different environment?
- Does reverting the last change fix it?
- Is it data-dependent?

Output: "The bug is in {file}:{line_range} because {evidence}"

### Step 3: Diagnose

Understand the root cause, not just the symptom.

1. **Read the code** — Read the actual implementation, don't assume
2. **Check assumptions** — What does the code assume about inputs, state, ordering?
3. **Look for common patterns**:
   - **Null/undefined access** — Missing null checks, optional chaining needed
   - **Race condition** — Async operations completing in unexpected order
   - **State mutation** — Shared state modified unexpectedly
   - **Type mismatch** — String vs number, date formats, encoding
   - **Off-by-one** — Array bounds, pagination, date ranges
   - **Missing migration** — Database schema doesn't match model
   - **Cache stale** — OPcache, view cache, query cache serving old data
   - **Environment mismatch** — .env values, Docker config, service URLs
   - **Dependency version** — Breaking change in updated package

Output: "Root cause: {explanation of why the bug occurs}"

### Step 4: Fix

Apply the minimal correct fix.

1. **Fix the root cause** — Not the symptom
2. **Keep the fix minimal** — Don't refactor unrelated code while debugging
3. **Consider edge cases** — Does the fix handle related scenarios?
4. **Check for the same bug elsewhere** — Grep for similar patterns in the codebase

### Step 5: Verify

Confirm the fix works and doesn't break anything.

1. **Reproduce the original bug** — Confirm it no longer occurs
2. **Run related tests** — Not just the failing test, but adjacent tests
3. **Check the happy path** — Make sure normal operation still works
4. **Test edge cases** — Empty input, large input, concurrent access

## Anti-Patterns (DO NOT)

- **Don't retry the same command** hoping for a different result
- **Don't add random print statements** without a hypothesis
- **Don't fix the symptom** and ignore the root cause
- **Don't make multiple changes at once** — change one thing, test, repeat
- **Don't assume** — read the actual code and actual error

## Debug Output Format

```markdown
# Debug Report: {Brief Description}

**Status:** FIXED | NEEDS_INFO | ESCALATE
**Time spent:** {duration}

## Symptom
{What the user reported / what failed}

## Root Cause
{Why it happened — the actual technical explanation}

## Fix Applied
{What was changed and why}
- File: {path} — {what changed}

## Verification
- [x] Original bug no longer reproduces
- [x] Related tests pass
- [x] No regressions in adjacent functionality

## Prevention
{How to prevent this class of bug in the future — test, lint rule, type check, etc.}
```

## Framework-Specific Debug Guides

### Laravel/PHP
- Check `storage/logs/laravel.log` for stack traces
- `php artisan tinker` to test in isolation
- `php artisan route:list` to verify route registration
- OPcache: restart container if code changes aren't picked up

### Next.js/React
- Check browser console + network tab
- `npm run build` catches type errors that `dev` mode misses
- Server vs client component errors have different stack traces
- Check `.next/` cache — `rm -rf .next` if stale

### Docker
- `docker compose logs {service}` for container output
- `docker compose exec {service} sh` to inspect container state
- Check port mappings, volume mounts, environment variables
- Container restart picks up code changes when OPcache is active

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
