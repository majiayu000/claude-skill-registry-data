---
description: >-
  Review code from the current (or clearly-restored) session for DRY
  opportunities. Apply the obvious wins immediately; surface only the
  ambiguous calls for the user to decide. Invoke as: /dry [optional focus guidance]
---

You are reviewing code written in this session (or in a prior session whose work
this session is clearly continuing) for DRY violations. The scope is _just the
work that was done_ — not the whole codebase.

The output of this skill is **edits, not a report**. Apply the obvious wins
yourself and only ask the user about the genuinely ambiguous calls.

## When to use

- After implementing a feature in the current session and before / during
  housekeeping.
- When resuming a summarized session that has a clear concrete deliverable in
  flight (e.g. a flow task), the scope is the deliverable's diff.
- Skip if the session has no concrete recent code work (research-only,
  planning-only, conversation-only).

## Step 1: Determine the diff scope

Pick the right scope, in this order:

1. **Uncommitted changes**: `git diff HEAD` and untracked files via
   `git status --short`. If non-empty, that's the scope.
2. **Commits made in this session**: `git log --oneline @{u}..HEAD` (commits
   ahead of upstream on the current branch). If non-empty, that's the scope.
3. **Restored session with concrete prior work**: if the session summary
   references specific files modified in named commits on the current branch,
   use the SHA range from the summary (`git diff <start-sha>..HEAD`). Confirm
   with the user before assuming.
4. **Nothing matches**: tell the user there's nothing to review and stop.

Run `git diff <range> --stat` first to confirm the scope and surface the file
count.

## Step 2: Read the changed files

Read every file in scope fully. For test files, read them too — duplicated
assertion patterns or fixture builders are fair game.

If the user provided focus guidance ("focus on the streaming changes"), narrow
accordingly but still glance at the rest.

## Step 3: Triage each candidate into one of three buckets

For every duplication you spot, check whether it's **real** (the code already
says the same thing twice) vs **speculative** (the code _might_ need to be the
same later). Only real duplication counts.

Triage dimensions:

- **Callsite count**: 2 callsites is the threshold for considering an
  extraction; 3+ makes it a clear win. 2 is borderline — extract only if the
  rule itself is non-trivial or coupled (e.g. provider-namespacing, a magic
  string with semantic meaning).
- **Coupling**: do the duplicates need to change together? If yes, dedupe
  protects against drift. If no (they happen to look alike now), don't dedupe —
  premature abstraction.
- **Abstraction cost**: a 1-line predicate or a Sass `%placeholder` is cheap; a
  new component with props is expensive. Match the cost to the win.
- **Distance**: same file = local extraction. Cross-file in the same slice =
  small helper. Cross-slice = check if it belongs in `shared/`.

Sort each candidate into one of:

### OBVIOUS — apply silently in Step 4

A clear win on every dimension: real coupled rule, ≥2 callsites, cheap
extraction, no naming or placement ambiguity. Examples:

- A magic string with semantic meaning duplicated in 2+ places in the same file
  → extract a 1-line predicate or constant.
- A 4+ line CSS rule block repeated in 2+ classes in the same module → extract a
  Sass `%placeholder`.
- A literal expression repeated 3+ times → extract a const.

### AMBIGUOUS — surface to the user in Step 5

The duplication is real, but at least one dimension is genuinely unclear and a
code reviewer might reasonably prefer either choice. Examples:

- Borderline cost/value: 2 callsites with a moderately expensive extraction.
- Naming or placement uncertain: should the helper live in this file, the
  slice's `lib`, or `shared`?
- Semantic ambiguity: the duplicates _look_ identical but might be expressing
  different intent that future edits would diverge.
- A new shared component would replace the duplication but with non-trivial prop
  API design.

### NON-ISSUE — do not mention

Reject these as **non-issues**, even if the code looks repetitive:

- **Belt-and-suspenders patterns** (e.g. `.done()` in both success and
  `.finally()`): intentional, not duplication.
- **Same shape, different semantics** (e.g. one helper returns last value,
  another returns all): merging hides intent.
- **Boilerplate the framework requires** (e.g. `'use client'`, `import` lines,
  mock setup blocks).
- **Test fixtures across files** with different scenarios — duplication there
  documents intent.
- **Visual similarity without rule similarity** — e.g. two CSS classes with the
  same color but for unrelated UI concepts.

## Step 4: Apply OBVIOUS fixes immediately

Make the edits surgically — one DRY fix per logical change, minimal surrounding
churn. Do not bundle unrelated cleanups. Do not rename things that aren't part
of the dedupe.

If there are no OBVIOUS items, skip this step.

## Step 5: Surface AMBIGUOUS items for discussion

For each ambiguous candidate, give the user:

- The exact files and line ranges.
- The shared code (verbatim or near-verbatim).
- The candidate extraction (1–5 lines of code).
- A one-sentence statement of _why it's ambiguous_ — what dimension is unclear
  and what choices the user has.

Do **not** rank these or recommend one. The point of surfacing them is that you
don't know.

If there are no AMBIGUOUS items, skip this step.

## Step 6: Report

Tell the user, briefly:

- What was applied (one bullet per OBVIOUS fix, with file:line references).
- What's pending discussion (the AMBIGUOUS list, if any).

Do not list non-issues — keep the report tight.

Once done, commit the applied fixes.

## Anti-patterns to avoid

- **Don't propose extractions you wouldn't make in a code review.** If a 2-line
  repetition is genuinely fine, treat it as a non-issue and skip silently.
- **Don't invent abstractions.** New helpers must replace existing duplication,
  not anticipate future duplication.
- **Don't widen scope.** If a file in the diff calls a duplicate that exists
  _elsewhere_ in the codebase (outside the diff), mention it once but don't fix
  it — that's a separate task.
- **Don't reorder, rename, or "while you're at it" cleanups.** DRY only.
- **Don't ask permission for OBVIOUS fixes.** That's the whole point of triaging
  — if it's obvious, just do it.
