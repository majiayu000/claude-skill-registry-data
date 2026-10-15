---
name: using-sequential-thinking
description: Use for complex multi-step reasoning where you need to think out loud, revise, branch.
---

# Using Sequential Thinking

## What this is

An MCP server that gives you a structured scratchpad for **complex reasoning**. Each call records one thought; you can number them, mark revisions, branch, and decide when to stop. Output is deeper and more auditable than inline prose reasoning.

## When to use

- Designing an architecture or making a non-trivial design decision (database schema, API boundary, caching strategy)
- Choosing between 2-4 algorithm/approach alternatives with non-obvious trade-offs
- Tracing a tricky bug's causal chain when the surface symptom doesn't match the root cause
- Planning a multi-stage implementation where later steps depend on earlier conclusions
- Any time you catch yourself wanting to say "wait, let me reconsider..." mid-answer

## When NOT to use

- Simple questions with obvious answers ("what's the syntax for a Python list comprehension")
- Direct factual lookups (use `context7` or `deepwiki` instead)
- User asks for a quick answer or is impatient
- Tasks with 1-2 trivial steps — overhead exceeds value
- You already have a clear path and just need to execute (use a TodoList or just do it)

The MCP can easily consume 10+ thoughts. Don't use it on questions that deserve 1 sentence. **Don't bring a SAT solver to "1+1"**.

## Tool

`mcp__sequential-thinking__sequentialthinking`

Required parameters:
- `thought` — the current step's content (string, free-form)
- `thoughtNumber` — current step number (starts at 1)
- `totalThoughts` — your current estimate of how many you'll need
- `nextThoughtNeeded` — `true` to continue, `false` when done

Optional parameters:
- `isRevision: true` + `revisesThought: N` — this thought revises an earlier one
- `branchFromThought: N` + `branchId: "alt-approach"` — explore an alternative branch
- `needsMoreThoughts: true` — you've reached `totalThoughts` but need more

## How it differs from inline reasoning

Inline reasoning in your reply is **linear and committed**. Sequential thinking lets you:

- **Revise**: thought 7 marks thought 3 as wrong without erasing it — the trace stays auditable
- **Branch**: explore "what if we used Redis instead" without abandoning the SQL line
- **Adjust scope**: bump `totalThoughts` from 5 to 12 when you realize the problem is bigger
- **Stop early**: drop from 10 to 4 when the answer crystallizes

This produces more rigorous answers for hard problems and is more honest about uncertainty.

## Workflow

1. **Frame the problem** in thought 1. State what you're trying to decide / understand.
2. **Estimate `totalThoughts`** — 3-5 for moderate problems, 8-15 for complex. It's an estimate; you can adjust.
3. **One step per thought**. Don't cram 5 ideas into one `thought` string.
4. **When you contradict yourself**, set `isRevision: true` and `revisesThought` to the wrong step. Don't pretend you didn't change your mind.
5. **When you want to compare alternatives**, branch with `branchFromThought` and `branchId`. Compare branches in a later thought.
6. **End with a synthesis thought**: hypothesis + verification + conclusion. Set `nextThoughtNeeded: false` on this one.

## Example shape (don't execute — just illustrative)

```
{thoughtNumber: 1, totalThoughts: 6, thought: "Problem: pick auth strategy for a multi-tenant SaaS. Constraints: SSO required, low latency, ≤2 weeks to ship."}
{thoughtNumber: 2, totalThoughts: 6, thought: "Option A: Auth0 — fastest to ship, vendor lock-in, ~$240/mo at our tier."}
{thoughtNumber: 3, totalThoughts: 6, thought: "Option B: Keycloak self-hosted — no per-seat cost, ops burden, JWT customization easier."}
{thoughtNumber: 4, totalThoughts: 6, thought: "Revising 2: Auth0's tier is actually $130/mo at our seat count — I had the wrong tier.", isRevision: true, revisesThought: 2}
{thoughtNumber: 5, totalThoughts: 6, thought: "2-week deadline kills Keycloak — ops setup alone is a week."}
{thoughtNumber: 6, totalThoughts: 6, thought: "Conclusion: Auth0. Re-evaluate at 12 months if cost grows.", nextThoughtNeeded: false}
```

## Combining with other tools

- **Before `Write`/`Edit`**: think through a design, then write the code
- **With `context7`/`deepwiki`**: gather facts from MCPs, then reason through them in sequential-thinking
- **After failed debugging**: when ad-hoc debugging stalls, switch to structured thinking to find the root cause

## Anti-patterns

- Setting `totalThoughts: 20` for a simple question — overshoots, wastes your context budget
- Cramming multiple ideas into one `thought` — defeats the purpose; one step per call
- Never revising — if you never used `isRevision`, you're probably not thinking critically enough on hard problems
- Using it as a fancy bullet list — if your "thoughts" are just an outline, write the outline directly

## Red flags

- You're about to answer a complex design question off the cuff in 2 paragraphs
- You catch yourself reversing position mid-paragraph in your draft reply — start over with sequential-thinking
- The user explicitly says "think hard" / "really think this through" — they want structured reasoning

## One-liner reminder

Hard reasoning gets the structured tool; quick questions stay inline.
