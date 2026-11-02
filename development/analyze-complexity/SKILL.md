---
name: analyze-complexity
description: Use when reviewing or choosing code on a hot path or over user data — estimate Big-O and amortized cost, and decide when O(n²) is a bug versus a style point.
---

# Analyze Complexity

Estimates the growth order of code so a review can tell a real performance bug from a style nit. It is
the "measure before optimizing" companion to [engineering-principles.md](../../core/_shared/engineering-principles.md).

## Growth order

`O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)`. A comparison sort cannot beat `Ω(n log n)`.

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null | head -20
grep -rn "for\|while\|sort\|find\|filter\|map" --include="*.ts" --include="*.rs" --include="*.go" --include="*.py" . 2>/dev/null | head -30
```

Find the loop that depends on the size of user data, and name its order: a nested loop over the same
collection is `O(n²)`; a loop that halves its range is `O(log n)`; a loop that sorts then scans is
`O(n log n)`. Watch for a call inside the loop that hides another loop (a `.find` inside a `for`).

## 2. Decide whether it matters

- The input is bounded (a form with five fields, a fixed set of options) → the order is a style point.
- The input is user data or grows unbounded (rows, messages, search results) → the order is a bug when it
  is `O(n²)` or worse, or when a linear scan repeats inside a loop (N+1: a query or scan per element, O(n) → O(n²)).
- The code is on a hot path (per request, per render) → measure before changing; a trace is the evidence.

## 3. Distinguish average from worst and amortized

- **Average vs worst**: quicksort averages `O(n log n)` but is `O(n²)` worst-case on already-sorted input
  without a good pivot; hash lookup is `O(1)` average but `O(n)` worst on a bad hash.
- **Amortized**: a dynamic array's append is `O(1)` amortized even though one in every N doubles and costs
  `O(n)`; the rare cost is spread across the many cheap ones.

## Verify

State the order of the changed code, name the input it grows with, and cite the number (a profile, a
trace, or the data size) that decided bug-vs-style. A second pass confirms no loop hidden inside the loop.

## When to deviate

- Fix a known algorithmic mistake (N+1, quadratic over user data) without a profile — it is a bug, not a
  guess. See [engineering-principles.md](../../core/_shared/engineering-principles.md).
- Bounded input: optimising it is noise; keep the readable version.
