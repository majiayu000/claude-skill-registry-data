---
name: rot-hunt
description: Trace a recurring bad pattern to the commit that planted it, list every copy, and target the seed instead of the copies. Use when the user asks "why does this pattern keep showing up?", "where did this come from?", wants a repeated hack/workaround/duplication rooted out, or when a review keeps flagging the same shape in different files.
---

# Rot hunt

Agents follow breadcrumbs. The first bad pattern that lands in a tree becomes the exemplar later work copies, then amplifies — a **seed** spreading, not a series of independent mistakes. This skill finds the seed, inventories its copies, and aims the fix at the seed. Patching a copy while the seed stays planted guarantees the next copy.

Sibling of `aa-simplify` (which reads the current diff) — rot-hunt reads *history*. Reach for it when the same smell appears in more than one place.

## Name the pattern

Pin the pattern before searching. Write one line: the shape (a helper name, a workaround idiom, a type, a copy-pasted block, a config hack) and why it's bad. If the user gave only a symptom ("this file feels off"), read the file, pick the candidate pattern, and confirm the one-liner with the user before hunting.

Done when the pattern has a one-line description and at least one **distinctive search token** — a string specific enough that matches are instances, not noise. "No valid candidate" is a legitimate outcome: if reading turns up nothing that meets the bar, report that as the finding and end the hunt there.

## Find the seed

The seed is the *first landed* instance, not the worst one.

1. Search the tree for the token — every hit is a suspected instance:
   `file_search` with `mode: "content"` (fallback: `grep -rn`).
2. For each hit file, find when the pattern arrived:
   `git op=log path=<file>` (fallback: `git log --oneline -- <file>`), then `git log -S"<token>"` to catch the exact introducing commits.
3. The instance with the earliest introducing commit is the seed. Record: file, SHA, author context (human commit or agent run), and the one-line description.

When two instances land in the same commit, the seed is the one the commit message or diff shows was written first / copied from — if that's undecidable, treat the commit itself as the seed.

Done when the seed has a file, a first SHA, and every other hit is either dated after it or explicitly noted as undecidable.

## Inventory the copies

For each remaining hit: file, introducing SHA, and whether it's a **copy** (same shape, plausibly modeled on the seed) or an **independent instance** (same shape, arrived without sight of the seed — rare; note the evidence). "No copies" is a valid result and downgrades the finding from rot to a one-off — hand it back to `aa-simplify` territory.

Done when every search hit is classified seed / copy / independent / false-positive.

## The fork

Name the decision that planted the seed: the commit, plan, or review moment where an alternative existed and the seed won. One sentence — what was chosen, what was available instead. If history shows no real alternative (the seed was forced by a constraint that still holds), say so: that's a `tolerate`.

## Verdict and output

Produce a report, **don't edit**. One table row per pattern hunted:

- **Seed** — file, first SHA, one-line description
- **Copies** — list, or "no copies"
- **Fork** — the decision that planted it, and the alternative
- **Verdict** — `remove` (fix the seed, then the copies follow) or `tolerate` (with the constraint that justifies it)
- **Fix order** — for `remove`: the seed first, copies second, in dependency order. Never the reverse.
- **Rung** — for `remove`: the enforcement rung (see Promote to enforcement)

If the user wants the fix executed, the seed removal is the first work item — hand the ordered list to `tidy-first`/`tdd` or a dispatch, with the seed token as a post-fix search check ("token count reaches zero, or every remaining hit is justified").

## Promote to enforcement

A hunted pattern that isn't enforced regrows. Every `remove` row also gets a **rung**: the hardest rung on the enforcement ladder that fits the pattern.

1. **Impossible** — change the API or type so the pattern no longer compiles.
2. **Lint** — an ESLint rule names the shape (`no-restricted-imports`, `no-restricted-syntax` with an AST selector).
3. **CI check** — a small script greps for the seed token and fails with a message naming the supported path.
4. **Prose** — a line in a skill or AGENTS.md. Picking this rung requires one sentence on why rungs 1–3 don't fit.

The rule ships in the same change as the seed fix, with the cleaned copies as proof it passes. A CI check carries a one-line header naming the seed it guards; delete the check when a later change moves it to rung 1.

Done when every `remove` row has a rung, and every rung-4 row carries its justification.

## When this skill is the wrong fit

- Findings should land on the issue tracker → `rot-hunt-to-issue`
- One-off over-engineering in a fresh diff → `aa-simplify`
- Placement drift (right code, wrong folder) → `improve-codebase-colocation`
- "What did the overnight run do?" → `run-postmortem` (which calls this skill for its rot section)
