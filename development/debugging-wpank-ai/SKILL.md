---
name: debugging
model: standard
category: testing
description: Systematic debugging approaches — scientific method applied to code, structured techniques, common bug categories, git bisect, time-boxing, prevention strategies, and anti-patterns. Use when investigating bugs, diagnosing failures, or establishing debugging practices.
version: 1.0
---

# Debugging Methodology

A systematic, scientific approach to finding and fixing bugs — replacing guesswork with method.

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." — Brian Kernighan


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install debugging
```


---

## Debugging Philosophy

Debugging is not guessing. It is applied science.

1. **Observe** — gather evidence: error messages, logs, stack traces, screenshots, reproduction steps
2. **Hypothesize** — form a specific, testable explanation for the behavior
3. **Test** — design an experiment that confirms or disproves the hypothesis
4. **Conclude** — accept or reject the hypothesis based on evidence, then iterate

Every debugging session should follow this loop. If you catch yourself making random changes and re-running, stop — you've left the scientific method.

---

## Systematic Methods

Choose the method that matches the situation:

| Method | When to Use | How It Works |
|--------|-------------|-------------|
| **Binary search** | Large codebase, unknown origin | Bisect code or commits to narrow location by half each step |
| **Hypothesis testing** | Known symptoms, multiple possible causes | Form specific hypothesis, design targeted test, verify or refute |
| **Minimal reproduction** | Complex bugs, intermittent failures | Strip away code, config, and data until smallest case reproduces |
| **Trace analysis** | Flow-based bugs, wrong output | Follow data or execution path step by step from input to output |
| **Rubber duck** | Stuck, unclear thinking, no progress | Explain the problem aloud — forces clarity and often reveals the answer |
| **Divide and conquer** | Multi-component issues, integration bugs | Isolate each component, test independently, find which misbehaves |

### Combining Methods

Most real bugs require combining methods. A typical pattern:

1. Start with **trace analysis** to understand the flow
2. Use **hypothesis testing** to narrow the cause
3. Apply **binary search** (on code or commits) to pinpoint the location
4. Build a **minimal reproduction** to confirm and share

---

## Debugging Workflow

Follow these six steps in order. Do not skip ahead.

### Step 1: Reproduce

Can you make the bug happen reliably? Write down the exact steps.

- What input triggers it?
- What environment (OS, browser, Node version)?
- Is it deterministic or intermittent?
- What is the expected behavior vs actual behavior?

**If you cannot reproduce it, you cannot confirm you have fixed it.**

### Step 2: Isolate

Narrow the scope. Which component, file, function, or line?

- Use binary search: comment out half the code, does it still fail?
- Use divide and conquer: test each component independently
- Check recent changes: `git log --oneline -20` and `git diff`

### Step 3: Diagnose

Understand the root cause, not just the symptom.

- Ask "why?" repeatedly until you reach the actual defect
- Distinguish between the symptom (what you see) and the cause (why it happens)
- Verify your diagnosis by predicting what will happen if you change a specific thing

### Step 4: Fix

Make the smallest change that addresses the root cause.

- Fix the cause, not the symptom
- Avoid side effects — don't "fix" by restructuring unrelated code
- If the fix is complex, break it into smaller, verifiable steps

### Step 5: Verify

Confirm the fix resolves the original reproduction case.

- Run the exact reproduction steps from Step 1
- Check for regressions — did the fix break anything else?
- Test edge cases related to the bug

### Step 6: Prevent

Add safeguards so this class of bug cannot recur.

- Write a regression test that reproduces the original bug
- Improve types, add assertions, or add validation
- Update monitoring or alerts if the bug was caught late
- Document the fix if the root cause was non-obvious

---

## Debugging Toolkit

| Tool | Purpose | When to Reach for It |
|------|---------|---------------------|
| **Debugger** | Set breakpoints, step through execution, inspect state | Logic errors, unexpected control flow |
| **Logging** | Add strategic log statements at key points | Flow tracing, production issues, async bugs |
| **Profiler** | Measure CPU, memory, and timing | Performance regressions, slow endpoints |
| **Network inspector** | Inspect HTTP requests, responses, headers, timing | API integration bugs, auth failures, CORS |
| **Memory analyzer** | Heap snapshots, allocation tracking, leak detection | Memory leaks, growing memory usage |

### Effective Logging

- Include the **module and function name** as a prefix: `[OrderService.processPayment]`
- Log **inputs** on entry and **outputs/status** on exit
- Use **structured data** (objects), not string concatenation
- Remove debug logging before committing (or use a debug log level)

---

## Common Bug Categories

Recognize the pattern to find the fix faster:

| Category | Typical Symptoms | First Things to Check |
|----------|-----------------|----------------------|
| **Null reference** | "Cannot read property of undefined/null" | Input validation, optional chaining, API response shape |
| **Off-by-one** | Missing first/last item, extra iteration, boundary failure | Loop bounds, array indices, fence-post conditions |
| **Race condition** | Intermittent failures, order-dependent, works in debugger | Shared mutable state, missing locks/awaits, event ordering |
| **Memory leak** | Growing memory over time, eventual OOM or slowdown | Event listeners not removed, closures holding references, cache without eviction |
| **State management** | UI out of sync, stale data, phantom updates | Mutation vs immutability, missing re-renders, stale closures |
| **Encoding** | Garbled text, wrong characters, hash mismatches | UTF-8 vs Latin-1, URL encoding, base64 padding |
| **Timezone** | Times off by hours, wrong dates near midnight | UTC vs local, DST transitions, serialization format |
| **Async ordering** | Operations complete in unexpected order | Missing await, unhandled promise, callback timing |
| **Configuration** | Works locally, fails in staging/production | Environment variables, feature flags, config file differences |
| **Dependency version** | Broke after update, works with old version | Lock file changes, breaking API changes, peer dependency conflicts |

---

## Git Bisect Guide

When you know a bug was introduced between two commits, `git bisect` finds the exact breaking commit using binary search.

```bash
# 1. Start bisect
git bisect start

# 2. Mark the current (broken) commit as bad
git bisect bad

# 3. Mark a known good commit
git bisect good abc1234

# 4. Git checks out a middle commit — test it, then tell git:
git bisect good   # if this commit works fine
git bisect bad    # if this commit has the bug

# 5. Repeat until git identifies the first bad commit
#    Output: "<commit-hash> is the first bad commit"

# 6. Examine the breaking commit
git show <commit-hash>

# 7. End the bisect session
git bisect reset
```

### Automated Bisect

If you have a test script that exits 0 for good and non-zero for bad:

```bash
git bisect start
git bisect bad HEAD
git bisect good abc1234
git bisect run ./test-for-bug.sh
```

Git runs the script at each step automatically and reports the first bad commit.

---

## Questions to Ask When Stuck

Use this checklist when you've been stuck for more than 15 minutes. Answer each question explicitly:

- [ ] **What changed recently?** — new deploy, dependency update, config change, data migration?
- [ ] **Can I reproduce it?** — reliably, intermittently, or not at all?
- [ ] **What are the exact error conditions?** — specific input, user, environment, time of day?
- [ ] **What does the data look like?** — inspect actual values, not what you assume they are
- [ ] **What do the logs say?** — read them carefully, including timestamps and context
- [ ] **Does it happen in other environments?** — local, staging, production, different OS/browser?
- [ ] **What is the expected behavior?** — can I articulate exactly what should happen?
- [ ] **Have I seen this pattern before?** — check the common bug categories table above
- [ ] **Am I looking at the right layer?** — frontend vs backend, app vs infrastructure, code vs config?
- [ ] **What assumptions am I making?** — list them explicitly, then verify each one

---

## Time-Boxing

If you've spent more than 30 minutes without progress: step back and re-read the error from scratch, explain the problem aloud (rubber duck method), take a 10-minute break, try a completely different hypothesis, ask for help, or reduce scope by building the smallest reproduction from scratch.

---

## Prevention

After fixing a bug, invest time to prevent its recurrence:

| Action | How It Helps |
|--------|-------------|
| **Add a regression test** | Ensures this exact bug cannot return undetected |
| **Improve types** | Catches null, undefined, and shape mismatches at compile time |
| **Add runtime assertions** | Fails fast with a clear message instead of silent corruption |
| **Document the fix** | Helps future developers understand the "why" behind the code |
| **Review related code** | The same mistake pattern may exist in similar locations |
| **Update monitoring** | Add alerts or dashboards so the symptom is caught earlier next time |

---

## Anti-Patterns

Behaviors that waste time and make bugs harder to find:

| Anti-Pattern | Why It Fails | Do This Instead |
|--------------|-------------|-----------------|
| **Random changes** | Introduces new bugs, obscures original cause | Follow the scientific method — one variable at a time |
| **Fixing symptoms** | The root cause remains and will resurface | Ask "why?" until you reach the actual defect |
| **Debugging in production** | Risk to users, limited tooling, high stress | Reproduce locally or in staging first |
| **Not reproducing first** | You cannot confirm a fix for a bug you cannot trigger | Invest the time to build a reliable reproduction |
| **Ignoring error messages** | The answer is often in the message you skipped | Read the full error, including stack trace and context |
| **Assuming your code is correct** | Confirmation bias hides obvious mistakes | Re-read your code as if someone else wrote it |
| **Changing multiple things at once** | You cannot tell which change fixed (or broke) it | Make one change, test, then move to the next |
| **Debugging while fatigued** | Tired debugging creates more bugs than it fixes | Take a break, come back with fresh eyes |

---

## NEVER Do

1. **NEVER push a fix you cannot explain** — if you don't know why it works, it doesn't work
2. **NEVER debug without version control** — always be able to revert to a known-good state
3. **NEVER ignore a failing test** — a skipped test is a hidden bug waiting to resurface
4. **NEVER assume the bug is in someone else's code first** — check your own code before blaming libraries or frameworks
5. **NEVER debug while fatigued** — tired debugging creates more bugs than it fixes
6. **NEVER delete error handling to "simplify"** — error handling is where bugs reveal themselves
7. **NEVER skip the reproduction step** — a fix without a reproduction is a guess, not a solution
8. **NEVER make random changes hoping something works** — follow the scientific method; one variable at a time
