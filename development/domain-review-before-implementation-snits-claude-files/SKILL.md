---
name: domain-review-before-implementation
description: BEFORE dispatching any implementation agent or starting to code - if you're about to write "Task(subagent_type=..., prompt=...)" for implementation, or about to implement a plan yourself, STOP and review first. The prompt you're about to send IS a brief - review it for design flaws before the agent implements garbage.
---

# Domain Review Before Implementation

## The Trigger

**Use this skill when you're about to:**
- Dispatch a `Task()` for implementation work
- Start coding from a plan or task description
- Send a prompt to a subagent that will write code

**The prompt you write IS the brief.** If you're about to send an implementation agent a task, that task description needs review first.

**Ask yourself:** "Am I about to have code written (by me or an agent)?" If yes → domain review first.

## Overview

**Core principle:** Task briefs contain design flaws. Domain experts catch them before implementation, not code reviewers after.

**Real-world data:** Phase 4A Task 16 (RiverGraph serialization) - "straightforward" brief reviewed by domain expert found 8 issues (3 critical type safety bugs, 3 important design gaps, 2 minor improvements). Cost: 5 minutes review. Savings: hours of debugging and refactoring.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT DOMAIN REVIEW FIRST
```

If you have a written brief, as a separate file or within a larger plan, dispatch domain expert before any implementation. No exceptions.

**Not for:**
- "Simple additions" (simple briefs hide complex issues)
- "Just following the steps" (steps may be flawed)
- "Time pressure" (exactly when you need review most)
- Don't rationalize. Review means review.

## When to Use

**MANDATORY for:**
- Any task with a written brief, spec, or implementation plan
- All tasks in subagent-driven-development workflow
- Tasks you're about to implement (even if they seem simple)

**Especially critical when:**
- Brief includes code examples (may have anti-patterns)
- Specialized domain (serialization, networking, security, concurrency, data modeling)
- You recognize the pattern (familiarity breeds assumptions)
- Time pressure (exactly when you need to catch issues early)

## The Pattern

### BEFORE This Skill

```
Read brief → Implement → Code review finds issues → Refactor
Cost: Implementation time + refactoring time + context switching
```

### AFTER This Skill

```
Read brief → Domain experts review brief → Fix brief → Implement with corrections
Cost: 5 minutes review
Savings: Hours of rework
```

## Implementation

### Step 1: Dispatch Domain Expert

**If you have Task tool available:**

Use Task tool to dispatch domain-appropriate expert agents.

- If reviewing an implementation plan, dispatch multiple agents focused on different aspects (examples: alogrithmic correctness, architecture, api, tasks properly sized, ...)
- If reviewing a design, dispatch multiple agents focused on different aspects (examples: conceptual correctness, ui/ux, architecture, api, ...)
- If reviewing a task brief dispatch domain-appropriate expert agents to validate the prompt.

Dispatch the agents with a prompt similar to this format:

```
Task(subagent_type="general-purpose", prompt=f"""
**Role:** You are a [domain] expert specializing in [specific area].

**Task:** Review this task brief for technical correctness and design flaws.

**Brief location:** [path to brief]

**Review focus:**
1. [Domain-specific concerns - e.g., serialization format, data types, security, industry standards]
2. Edge cases and error handling
3. Performance implications
4. Best practices compliance
5. Integration considerations
6. Coherence with overall plan
7. Task complexity and whether it should be decomposed.

**Provide:**
1. List of issues (Critical/Important/Minor)
2. For each: what's wrong and recommended fix
3. Things done well
4. Overall: "Ready to implement" or "Needs revision"

**Note:** Review the BRIEF/DESIGN, not code. Focus on flaws that cause problems during implementation.
""")
```

**If Task tool not available:**

STOP and ask your human partner: "I need to have a domain expert review this brief before implementing. How should I dispatch a consulting agent in this environment?"

Don't skip review because tool isn't obvious. Escalate to get the right mechanism.

### Step 2: Address Issues

- Fix all Critical issues in brief before implementing
- Fix Important issues (or document why skipping)
- Note Minor issues for cleanup

### Step 3: Implement with Corrections

Now dispatch implementation agent with corrected brief.

### Step 4: Code Review After Implementation

Use code-reviewer to catch implementation gaps.

## Domain Expert Examples

**Serialization tasks:** "Data serialization expert specializing in format design, type safety, and versioning"

**Security tasks:** "Application security specialist focusing on OWASP Top 10, attack vectors, and secure design patterns"

**Networking tasks:** "Distributed systems expert specializing in protocols, error handling, and network reliability"

**Database tasks:** "Database architect specializing in schema design, indexing strategies, and query optimization"

**Algorithm tasks:** "Algorithm specialist focusing on complexity analysis, edge cases, and correctness proofs"

**Concurrency tasks:** "Concurrency expert specializing in race conditions, deadlocks, and synchronization patterns"

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Brief is simple/straightforward" | Task 16 "straightforward serialization" had 8 issues. Simple briefs hide complex issues. |
| "Brief has TDD steps already" | TDD tests the implementation, not the design. Flawed design → passing tests for wrong behavior. |
| "Not security-critical" | Technical correctness matters everywhere. Type safety bugs, data loss, performance issues affect all code. |
| "I know this pattern" | Familiarity causes assumptions. Expert finds issues you overlook because "I've done this before." |
| "Domain review is overkill" | 5 minutes review vs hours debugging. Math favors review. |
| "Subagent overhead not worth it" | Agent dispatch: 30 seconds. Finding 8 bugs later: hours. Review always wins. |
| "I can see issues myself" | Then fix them in the brief BEFORE implementing. Domain expert systematically finds what you miss. |
| "We already reviewed the plan, so we don't need a review for this task brief" | More focused review on the task prompt routinely finds issues missed when reviewing the full plan. |

## Red Flags - You're Rationalizing

If you think ANY of these thoughts, STOP and dispatch domain expert:

- "Brief is well-specified, just implement it"
- "This is a standard pattern"
- "The examples look good"
- "We're in a hurry"
- "Domain review for this is overkill"
- "I'll catch issues during implementation"

**All of these mean: Dispatch domain expert first. No exceptions.**

## Integration with Workflows

### With subagent-driven-development

**CRITICAL:** If you're using subagent-driven-development, you MUST add domain review as mandatory step.

**Original workflow (from that skill):**
```
For each task:
  1. READ the task from plan
  2. Dispatch implementation subagent
  3. Code review
  4. Fix code review issues
```

**REQUIRED modification - add domain review FIRST:**
```
For each task:
  1. READ the task from plan
  2. DISPATCH DOMAIN EXPERT to review task brief  ← MANDATORY
  3. ADDRESS domain expert issues                 ← MANDATORY
  4. Dispatch implementation subagent
  5. Code review
  6. Fix code review issues
```

**Why both reviews:**
- Domain review: Catches design flaws in the BRIEF (wrong approach, anti-patterns, security issues)
- Code review: Catches implementation gaps in the CODE (missed requirements, bugs, style issues)

Skipping domain review = implementing flawed designs. Code review can't fix architectural problems.

### With executing-plans

Add domain review as first step before parallel execution:

```
1. Load plan
2. For each task: Dispatch domain expert, collect issues
3. Review all domain feedback with human
4. Execute tasks in parallel with corrections applied
```

## Why This Works

**Prevention vs remediation:**
- Domain review: 5 min, catches design flaws
- Implementation: 30 min with flawed brief
- Debugging: 2+ hours finding root cause
- Refactoring: 1+ hour fixing architecture

**Cost comparison:**
- With review: 5 + 30 = 35 minutes
- Without review: 30 + 120 + 60 = 210 minutes

**6× time savings** for 5 minutes of review.

## Real-World Example

**Task:** "Implement RiverGraph serialization using NumPy npz format"

**Without domain review:**
- Implement using code from brief
- Tests pass ✓
- MyPy fails (numpy scalars vs Python types)
- Runtime errors (ID arrays not numpy arrays)
- Missing validation (corrupted files accepted)
- Refactor for 2+ hours

**With domain review (actual Phase 4A data):**
- 5 min domain review finds 8 issues
- Fix in brief before implementing
- Implementation takes 30 min
- Tests pass ✓
- MyPy passes ✓
- Code review finds 1 minor issue
- Fix in 5 min
- Done

## The Bottom Line

**Task briefs lie.** Not maliciously - they're written without complete knowledge. Authors don't know every edge case, anti-pattern, or domain best practice.

**Domain experts find the lies before they become bugs.**

5 minutes. Every task. No exceptions.
