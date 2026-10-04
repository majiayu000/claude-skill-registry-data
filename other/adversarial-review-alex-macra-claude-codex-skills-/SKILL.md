---
name: adversarial-review
description: "Independent second-pass review that tries to break the change: invariants, edge cases, error paths, concurrency, ending in a concrete failing input and a verdict. Use for an adversarial review, red team pass, second opinion, try to break this, or poke holes. Deep security passes belong to security-review."
license: MIT
metadata:
  display-name: "Adversarial Review"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "review red-team quality verification"
---

# Adversarial review

This is the challenge pass that runs *after* a normal review. Your stance is not "does this look fine?" - it is **"this is wrong, and I will find the input that proves it."** If you finish and genuinely couldn't break it after a real attempt, *that* is the signal it's solid.

## Independence discipline

- Do **not** restate or lean on the first review. Re-derive what the change must guarantee, from scratch.
- Don't be anchored by the author's framing or the happy-path test they wrote. Those show it working; your job is to find where it doesn't.
- Assume the diff is guilty until you fail to convict it.

## Attack surface (work through each)

- **Boundary & malformed inputs** - empty, null/undefined, zero, negative, huge, off-by-one, duplicate, out-of-order, Unicode, mixed types, unexpected shapes.
- **Error & failure paths** - what if the call throws, the network drops, the write half-completes, the file is missing, the JSON is malformed? Is the error swallowed? Is state left corrupt?
- **Invariants** - name what must *always* hold (balance never negative, ID unique, list sorted). Then try to construct a sequence of operations that violates it.
- **State, ordering & concurrency** - re-entrancy, double-submit, two writers, retry-after-partial-success, stale cache, events arriving out of order.
- **Security** - any path from untrusted input to a sink (query, shell, filesystem, HTML, deserialization). Trust boundaries crossed without validation; for a dedicated pass use `security-review`.
- **Resource & scale** - unbounded growth, leaks, N+1, quadratic loops, missing pagination, allocations in a hot path.

## Method

1. Identify the **riskiest claim** the change relies on - the assumption that, if false, breaks it.
2. Try to construct concrete inputs or an interleaving that falsifies it. Write the actual values.
3. If you break it, minimize the case to the smallest reproducer.
4. Default to skepticism: when you're unsure whether something holds, **dig** - don't wave it through.

## Output

- **Verdict:** *Confirmed solid* (with the attacks you tried and why they failed) OR *Defects found*.
- Per defect: a **concrete failing scenario** (specific inputs/state to wrong output or crash), a severity from the ladder below, and the **smallest fix** that closes it.
- No vague worries. "This might have issues under load" is not a finding; "with 2 concurrent `submit()` calls, `count` double-increments because the read-modify-write isn't atomic - here's the interleaving" is.

Severity: Blocker (correctness, security, data loss) / Should-fix (compounding design debt) / Nit.

## What this skill is *not*

- Not the first review - that's `architect-review`. This runs after, to stress what it passed.
- Not a rewrite. Find the defect and the minimal fix; don't redesign.
