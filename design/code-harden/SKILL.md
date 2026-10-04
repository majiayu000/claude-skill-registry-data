---
name: code-harden
version: 1.0.0
description: |
  Produce code that survives senior review. Use this skill whenever the user
  asks for code to be written, improved, refactored, reviewed, or made
  production-ready — components, modules, scripts, APIs, library code,
  infrastructure, anything non-trivial. Trigger even when the user doesn't
  explicitly ask for "good" or "hardened" code; the default for any code task
  longer than ~20 lines should be to run this loop. The skill drafts code,
  runs a strict self-critique pass against a fixed rubric, applies only the
  critiques that name a concrete failure mode, iterates 2-3 times max, and
  outputs the final code plus a decisions changelog. Use for new code AND
  for hardening existing code the user pastes in. Do NOT use for one-line
  typo fixes, doc-only edits, or throwaway prototypes the user explicitly
  flags as scratch work.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# code-harden

You are writing code that has to survive a senior engineer reading every
line. Not code that works. Code that is *defensible*. Every choice must have
a reason you can state in one sentence. Every line that can't be defended
gets cut.

The mechanism is a short self-refinement loop: draft, critique against a
fixed rubric, gate critiques by whether they name a real failure mode,
revise, repeat at most 2-3 times.

## When to run the loop vs. when to just write code

Run the full loop when the code is non-trivial:

- A function or component over ~20 lines
- Anything async, stateful, or touching IO
- Anything with concurrency, cancellation, or lifecycle
- Anything that will be reviewed, shipped, or pasted into a PR
- Anything the user said "make this production-ready" or "harden this" about

Skip the loop, write code once, move on:

- One-line fixes, typos, rename refactors
- Pure functions with obvious behavior (formatters, simple converters)
- Scratch / throwaway / "just trying something" code the user flagged
- Snippets that exist purely to illustrate a concept

When in doubt, run the loop. The overhead is small; the gain is large.

## The loop

```
1. Draft v1.
2. Critique v1 against the rubric. Produce a list of candidates.
3. Gate each candidate through the "is this real?" check.
4. If 0 real critiques: stop. Output v1.
5. Revise into v2 addressing only real critiques.
6. Critique v2. Apply gate. If 0 real critiques: stop. Output v2.
7. Revise into v3 if still finding real critiques. Stop after v3 regardless.
8. Output final code + a changelog of what changed across iterations.
```

Three iterations is the hard ceiling. Past that, you start inventing problems
to fix and the code gets worse, not better. Stop when the critique surface
genuinely collapses, or at v3, whichever is first.

## The rubric

For each draft, walk these categories in order. Skip categories that don't
apply to the code (no point checking a11y on a backend cron job). For each
that does apply, ask the listed questions and write down what you find.

The full rubric lives in `references/rubric.md`. Read that file before
critiquing. The high-level categories:

1. **Correctness** — does it do what it claims under happy path and stated edge cases
2. **Lifecycle & resources** — effects, listeners, timers, handles, connections all have cleanup
3. **Concurrency & async** — cancellation, stale closures, ordering, race conditions
4. **Type safety** (typed languages) — no `any`/`unknown` leaks, discriminated unions where states are exclusive, no loose optionals tied to specific states
5. **Error handling** — every throw point has a defined caller experience; nothing swallowed silently
6. **Edge cases** — empty, single, max, boundary, null, malformed inputs all considered
7. **Determinism & idempotency** — same input gives same output; retry-safe where the operation can retry
8. **Accessibility & UX** (UI code only) — ARIA, keyboard, focus, contrast, motion
9. **Security** (anything touching user input, auth, secrets) — injection, leakage, auth checks, secret handling
10. **Readability** — naming carries meaning, no dead code, no magic numbers without comment, no abstractions that hide more than they explain

Don't apply categories that don't fit. A pure utility function gets graded
on correctness, types, edge cases, readability. A long-lived React component
gets graded on lifecycle, concurrency, a11y, edge cases, types, readability.
Match the rubric to the code.

## The "is this real?" gate

This is the part most self-critique loops get wrong. Without it, you fix
things that don't need fixing and the code drifts into over-engineered slop.

For each candidate critique, answer this question:

> If I left this unchanged, what concrete bad thing would happen?

The critique is **real** if you can name one of:

- A production failure scenario (will crash, leak, deadlock, return wrong result)
- A review-time rejection (a senior reviewer will block the PR over this)
- A maintenance trap (a future reader will misread this and break it)
- A correctness gap (the spec or stated behavior isn't actually met)

The critique is **speculative** (drop it) if the answer is any of:

- "It could be more abstract / reusable / generic" — premature, drop
- "Performance might matter someday" — no measurement, drop
- "Style preference" — drop
- "Defensive guard against a state that can't happen" — drop
- "Could add a feature" — that's scope creep, not a critique, drop
- "Would be nice to have" — drop

Apply the gate strictly. If you can't articulate a concrete bad outcome in
one sentence, the critique is speculative. Cut it.

The full gate logic with worked examples lives in
`references/gate-examples.md`. Read it when you find yourself wavering on
whether a critique is real.

## What "stop" looks like

You stop when one of these is true:

1. **The critique pass turned up zero real critiques.** Code is defensible.
2. **The remaining critiques are all fork-choices.** A fork-choice is a
   place where two senior engineers would disagree about the right call (e.g.
   "use Context vs prop-drilling here"). These aren't critiques; they're
   alternatives. Note them in the changelog as "fork: chose X because Y" and
   move on. Do not iterate to chase them.
3. **You've hit iteration 3.** Stop. Output what you have. If you found real
   critiques on v3 that you didn't address, list them in the changelog as
   "known limitations" so the user can decide whether to fix manually.

If you find yourself on iteration 2 or 3 and the only "critiques" you're
generating are speculative, that's a stop signal. The gate is telling you
the code is done.

## Output format

After the final iteration, output **two things** in this order:

### 1. The final code

Just the code. Clean. No commentary inline. If it's a file, write it as a
file. If it's a snippet, output as a code block.

### 2. The decisions changelog

A markdown section titled `## Decisions` containing:

- **v1 → v2**: bullet list of what changed and why (each item: "Changed X because Y would have happened")
- **v2 → v3**: same, if applicable
- **Forks taken**: places where multiple choices were reasonable, with the
  one you picked and the one-sentence reason
- **Known limitations**: anything you didn't fix, with why (out of scope,
  needs user input, would require a bigger refactor)

The changelog is the load-bearing part of this skill. It's what the user
walks into a code review with. They don't have to reverse-engineer your
reasoning; they can read it. When a reviewer asks "why X," the user has the
answer ready.

Keep changelog entries short. One sentence per change. No fluff.

## Examples of the gate in action

**Code:** A React `useEffect` subscribes to a WebSocket without a cleanup
return.

- Critique candidate: "Missing cleanup will leak the connection on unmount."
- Real? Yes. Concrete failure: memory leak + duplicate listeners on remount.
- Action: fix.

**Code:** A `map` over 5 array elements without `useMemo`.

- Critique candidate: "Could memoize for performance."
- Real? No. 5 elements, no measurement, premature.
- Action: drop.

**Code:** A function takes `data: any` and returns `any`.

- Critique candidate: "`any` defeats type safety."
- Real? Yes. Concrete failure: review-time rejection, runtime bugs at call sites.
- Action: fix.

**Code:** A small utility that splits a string by comma.

- Critique candidate: "Could handle quoted commas like a CSV parser."
- Real? Depends. If the spec said "split CSV", yes (correctness gap). If the
  spec said "split a simple comma-separated list", no (scope creep).
- Action: check the spec. If ambiguous, ask the user.

**Code:** A class with public fields where private would be safer.

- Critique candidate: "Should be private."
- Real? Only if external code mutating them would cause a bug. If yes, fix
  and explain in changelog. If no (just preference), drop.

More worked examples in `references/gate-examples.md`.

## Language-specific notes

The rubric is the same shape across languages, but the specifics vary:

- **TypeScript / JavaScript**: discriminated unions, strict null checks, no
  `any`, lifecycle in React/Vue, AbortController for cancellation
- **Python**: context managers for resources, `async`/`await` discipline,
  type hints with `mypy`-strict-friendly types, no bare `except`
- **Rust**: ownership/borrow correctness, `Result` propagation discipline,
  no `unwrap` outside of `main` or tests
- **Go**: error wrapping, context cancellation, goroutine leak prevention,
  `defer` for cleanup
- **Java/Kotlin**: try-with-resources, nullability, exception type discipline
- **Swift**: optional handling, `[weak self]` in closures, actor isolation
  for concurrent code

Detailed per-language rubric extensions live in `references/by-language.md`.
Read the relevant section before critiquing if the code is in a language
you're not actively writing daily.

## What this skill does NOT do

- It does not add features. If the user said "build X with feature Y", the
  loop hardens Y; it doesn't add Z.
- It does not turn small problems into big ones. A 30-line utility comes out
  a 30-line utility, not a 200-line "framework."
- It does not generate tests unless the user asked for tests. (If you want a
  test-generating skill, that's a different skill.)
- It does not chase 100% defensibility. The goal is "no real critiques left,"
  not "no critiques imaginable." Speculative critiques exist forever; the
  gate's job is to ignore them.

## Workflow when a user pastes existing code to harden

If the user pastes code and says "harden this" or similar:

1. Read the code carefully.
2. Treat the user's paste as v0.
3. Run the rubric. Generate candidate critiques.
4. Apply the gate.
5. If 0 real critiques: tell the user "this is already defensible" and stop.
   Do not invent issues to look thorough.
6. If real critiques exist: produce v1 that addresses them. Run the loop
   from there.

When telling a user their code is already good, do it directly. Don't pad.
"Read this carefully. Nothing real to fix. Here's why:" followed by a brief
defense of the major choices.

## Workflow when generating new code

When the user asks for new code:

1. Read the request. Identify the spec. Note ambiguities.
2. If the spec has critical ambiguities (multiple reasonable interpretations
   that lead to materially different code), ask the user one sharp question
   before writing. Don't ask trivia.
3. Draft v1.
4. Run the loop.
5. Output as specified above.

## A note on speed vs. quality

Three iterations of a 100-line file is the right cost for code that matters.
Three iterations of a 1000-line file is too much; break into parts and
harden each. Three iterations of a 10-line file is too much; just write it
right the first time.

Use judgment. The loop is a tool, not a ritual.
