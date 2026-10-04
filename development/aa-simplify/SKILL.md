---
name: aa-simplify
description: Use whenever the user wants a critical second-pass focused on cutting code — phrasings like "simplify this", "is this over-engineered?", "did I overdo it?", "what would you remove?", "feels bloated", "any cleanup opportunities?". Reviews recent changes with a bias toward removal — outputs findings for discussion, not direct edits.
---

# Simplify

A critical second-pass on recent code changes, biased toward **removal**. The author just wrote this code and is biased toward keeping it; the reviewer's job is to read it cold and ask what actually survives scrutiny. Treat the iteration history as a _liability_, not credit — early decisions ossify and stop being questioned.

## Scope

If the user already named a comparison target ("simplify this branch", "the last 3 commits", a path, a PR), use it and skip confirmation. Otherwise resolve in order:

- `git diff` + `git diff --staged` (uncommitted work) — the default
- If both are empty: the most recent commit
- If the branch is ahead of trunk and the uncommitted diff is trivial: offer branch-vs-main

If the diff is large or the right target is genuinely ambiguous, ask the user before reading the whole thing.

Done when every hunk in the scoped diff has been run through the diagnostics below.

## The diagnostics

A finding is any question you can't answer "yes, definitely".

### 1. Premature abstraction

For each new function, hook, component, type, or file: **is it used in more than one place right now?** If not, is the second caller genuinely coming — not "might be useful someday"?

### 2. Defensive coding

For each null check, try/catch, optional chain, fallback, or guard: **name a specific scenario where this branch triggers.** If you can't, it's noise — it hides real bugs and inflates surface area.

### 3. Speculative configurability

For each prop, option, or parameter: **does any caller pass a non-default value?** If every caller passes the same thing, the option is dead weight.

### 4. Derived state pretending to be state

For each piece of state synced from another value: **could this be computed at the use-site instead?** (React: a `useState` + `useEffect` pair mirroring props is almost always a `useMemo`, a `key` prop, or inline computation.)

### 5. Wrapper layers

For each new wrapper around a library or utility: **does the wrapper add behavior, or just rename things?** Rename-only wrappers are pure indirection.

### 6. DRY against the grain

For each consolidation of "similar" code: **are the callers solving the same problem, or do they just look alike?** Coupling distinct concerns under one abstraction costs more than the duplication.

### 7. Dead branches and vestigial code

Code paths marked "shouldn't happen", legacy compatibility shims with no caller, commented-out blocks, TODOs with no owner — all candidates for removal.

### 8. Code orphaned by the change

For each replaced or rerouted code path: **does the old path still have a caller?** The diff can make pre-existing code dead — a superseded branch, a helper whose last caller just left. Authors miss this class most.

## The engine

Diagnostics 1, 3, 5, and 8 hinge on callers *outside* the diff — they can never be answered from the diff alone.

**Primary path (RepoPrompt available):** run `context_builder` with `response_type: "review"`. Its discovery pulls in the out-of-diff callers wholesale. Embed the removal bias in the instructions — include all eight diagnostics verbatim in the `<task>`, plus:

> Bias toward removal. Report only cuts — code that should be deleted, inlined, or collapsed. A suggestion to *add* anything (guards, handling, abstraction, tests) is out of scope for this review.

State the confirmed comparison scope in `<context>`. When the oracle's findings come back, verify each against the actual diff before reporting it — the oracle proposes, you confirm. Follow up in the same chat (`ask_oracle`, `new_chat: false`) for anything unclear.

**Fallback (no RepoPrompt tools):** run the diagnostics yourself over the diff, and verify caller counts for 1, 3, 5, and 8 with a search — never answer them from the diff alone.

## Output

Produce a findings list, **don't edit**. Cap at ~10 findings, worst first — ranking is part of the review; a triaged shortlist beats an exhaustive dump. Format each finding:

- **Location** — `file:line` or function name
- **Finding** — what's over-engineered, in one sentence
- **Why it's noise** — which diagnostic question it fails
- **Suggested cut** — concrete change (delete, inline, replace with X)
- **Severity** — `cut` (clearly dead), `consider` (judgment call), `flag` (worth a thought)

Note in each finding whether the cut is behavior-preserving; if it isn't, cap severity at `consider`.

Group by severity, `cut` first. If nothing meaningful is wrong, say so plainly — don't manufacture findings to look thorough. A clean diff is a valid result.

## Example finding

> **Location:** `src/hooks/use-user-display.ts:1-12`
> **Finding:** New hook wraps `user.name || user.email` with `useMemo`, used in one component.
> **Why it's noise:** Premature abstraction (one caller) + unnecessary memoization (string OR, no measurable cost).
> **Suggested cut:** Inline the expression at the call site; delete the hook file.
> **Severity:** `cut`

## When this skill is the wrong fit

This skill is specifically for _reducing surface area_. Redirect when the ask is different:

- General review (bugs, correctness, security) → `aa-second-opinion`
- Commit boundaries (one commit or several) → `aa-commit-clarity`
- Architecture critique / design questions → consult Oracle in `plan` mode

If the ask fits but you have nothing to cut, that's the clean-diff result from Output above.
