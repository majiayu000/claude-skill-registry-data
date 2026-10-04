---
name: think-twice
description: >
  Forces Claude to pause before picking an implementation approach and ask: "Is there a cleverer,
  cheaper way?" Triggers when the request involves generating data or fixtures (lists, datasets,
  sample records), implementing a problem that is likely already solved by a stdlib function,
  package, or public API (validation, parsing, lookups, auth, date/currency/geo data), or any
  implementation expected to exceed ~20 lines. Does NOT trigger when the user has explicitly
  chosen the approach or library, when the task is under ~10 lines, when fixing a bug in existing
  code, or for infra/terraform/k8s and DB queries. Run the checklist before writing code, stop at
  the first question that reveals a cheaper path, and take that path.
---

# Lazy Agent — Work Smarter, Not Harder

> "A great engineer is a lazy engineer. They find the clever shortcut." — Steve Jobs

This skill rewires Claude's default instinct. Instead of charging ahead with the most obvious approach,
Claude must first ask: **"Is there a smarter way to do this?"**

Productive laziness is not about doing less. It's about never doing more than necessary.

---

## When NOT to run this checklist

Skip if the task is trivially small (under ~10 lines, no data, no new dependencies) or if the
user has explicitly described custom logic that no generic library could cover. In those cases,
proceed directly.

Also: never hand-roll cryptography or security primitives. "Use an existing implementation"
means the language stdlib or a widely-audited library — not a custom implementation.

---

## The Lazy Check

Run this before any task that feels heavy — a large block of code, repetitive data, a complex algorithm,
a long implementation. Stop at the first question that reveals a better path.

### 1. Am I solving the right problem?
Before writing a single line, make sure the task is correctly understood.
- What is the user *actually* trying to achieve?
- Am I about to solve a symptom instead of the root cause?
- Would a 2-sentence clarification save 200 lines of code?

**If the answer to any of these is uncertain — ask the user before writing any code.**
One targeted question now saves a full redo later.

### 2. Is there an existing solution?
Someone has almost certainly solved this before.
- **Public API**: Does a service already expose this data or functionality at runtime? Prefer it — no maintenance, always up to date.
- **Package**: Would `npm install` or `pip install` deliver this in 10 lines instead of 200?
- **Open dataset**: Is there a downloadable file (CSV, JSON, SQLite) from a trusted source?
- **Standard library**: Does the language's stdlib already cover this?

### 3. Am I doing too much?
Scope creep is the enemy of efficiency.
- Does the user need *all* of this, or just a slice?
- Am I precomputing everything when I could compute on demand?
- Am I generating 100 cases when 3 examples would prove the point?
- YAGNI: if it's not needed *right now*, don't build it.

### 4. Is my approach the most direct one?
The obvious implementation is rarely the best one.
- Is there a simpler data structure that makes the algorithm trivial?
- Is there a one-liner that replaces 50 lines of logic?
- Am I reaching for complexity when a lookup table would do?
- Can I reframe the problem so the solution becomes obvious?

### 5. Can I do this lazily?
Defer work until it's actually needed.
- Generate on demand instead of precomputing all cases.
- Paginate instead of loading everything.
- Cache results instead of recomputing.
- Render what's visible, not what exists.

### 6. Only then: proceed
If none of the above reveals a shortcut, commit to the implementation — but scope it to the minimum
that solves the problem today.

---

## Decision Checklist

Run this mentally before any significant code block:

```
[ ] Do I fully understand what's being asked, or am I assuming?
[ ] Does an API, package, or dataset already solve this?
[ ] Am I building more than what's needed right now?
[ ] Is there a simpler approach I'm overlooking?
[ ] Can this be computed lazily instead of all at once?
[ ] Would a 10-line solution exist if I reframed the problem?
```

If any box triggers doubt — stop and explore that path before proceeding.

---

## The Mindset

The greedy approach: *see task → start implementing → figure it out as you go.*

The lazy approach: *see task → pause → find the clever path → implement only what's needed.*

The difference is one beat of reflection before execution. That beat is what separates
a solution that costs 50,000 tokens from one that costs 50.

---

## Common Shortcuts

| Instead of... | Consider... |
|---|---|
| Implementing a complex feature from scratch | Checking if a library already does it |
| Hardcoding a large static dataset | Fetching it from an API at runtime |
| Generating all permutations upfront | Computing on demand with memoization |
| Building the full system now | Building only the part that's needed today |
| Writing a clever algorithm | Checking if a simpler data structure makes it trivial |
| Implementing auth, payments, maps from scratch | Using the standard library for that domain |
| Generating many examples to prove a point | Using 2-3 representative cases |
| Preloading everything on startup | Loading lazily when actually needed |

---

## When NOT to be lazy

Productive laziness has limits. Override it when:

- **Correctness requires it**: security-critical code needs the language stdlib or a widely-audited library — never a hand-rolled implementation
- **Latency requires it**: a runtime API call adds unacceptable delay to a hot path
- **Dependencies are restricted**: offline-first or zero-dependency environments
- **The shortcut is overengineered**: adding a library for 5 lines of trivial code

In these cases, proceed — but state why: *"Implementing this directly because X."*

---

## The Rule

**Before committing to any expensive path, spend 30 seconds looking for the cheap one.**

If you find it, take it and explain what you chose.
If you don't, proceed — and know you made the right call.
If you're blocked by ambiguity, ask the user one targeted question and wait for the answer.
