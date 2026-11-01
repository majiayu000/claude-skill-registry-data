---
name: prose-pass
description: Judge added comments, JSDoc, changelog entries, and PR bodies on information content and cut what a reader can derive. Use before presenting a diff, committing, or writing a PR body.
---

A pass over the prose in a diff — comments, JSDoc, changelog entries, PR body —
deleting text a reader does not need. Scope is the diff: prose the change added
or touched, not every comment in the files it happens to open.

Run it **before** presenting work, not after someone asks for it. When done,
return control to the calling workflow rather than stopping to present.

Invoked with `args="changelogs"` (from `update-changelogs`, or the `pr` changelog
phase), run the Changelogs section only and skip the rest.

## The bar

**The desired default is no comment.** A comment must justify its existence;
accuracy is not a justification.

The bar is **"obvious and logical"**, not "true and useful". A comment stating a
real hazard still goes if a competent reader derives it from the adjacent lines.
What survives is what the code cannot carry: a constraint, an invariant, a
non-obvious failure mode, or why a test is shaped the way it is — in the shortest
form that carries it.

Every judgment here is about **information content, never about style**. No
phrasing is banned; nothing survives on phrasing either.

Deleting a comment is cheap to undo — one line restored on request. A trivial
rename nearly so. Anything larger is not, and is out of scope for this pass; a
dropped JSDoc block can also break lint, so verify the result still lints.

## Prefer a trivial rename to a comment

If a comment exists only because an identifier is vague, and a **trivial rename**
removes the need for it, rename and delete the comment. Trivial means a local, a
parameter, or a private field that this diff already touches, renamed within the
one file — nothing exported, nothing that ripples across call sites.

Stop there. **Do not introduce structural refactors to eliminate prose**, even
when the result would clearly read better:

```ts
// Check whether the remote peer restarted.
if (currentId !== previousId) {
```

A `remotePeerRestarted()` helper would carry that sentence in its name, but
extracting it is a behavior-adjacent change with its own review surface. Keep the
comment, leave the structure alone, and propose the refactor separately if it is
worth doing.

This pass runs before every commit and PR, so it has to be predictable: its diff
is comments removed, occasionally one identifier renamed — never a refactor
nobody asked for.

## AI smell openers

Comments beginning with phrases such as `Ensure`, `Handle`, `Now`, `First`,
`Then`, `We need to`, `This allows`, `This ensures`, `Note that`, or `Important`
often introduce a restatement of the next line. **Treat the opener as a signal to
inspect the comment, not as a deletion rule.**

Delete it when the remaining sentence merely narrates the code. Keep it when the
sentence carries information the code cannot express: a constraint, an invariant,
a compatibility requirement, or a non-obvious failure mode. For example:

```ts
// Note that N must stay a power of two.
```

stays if nothing in the type system or the surrounding code makes that constraint
apparent.

When the verdict is delete, delete — rewriting a restatement into a shorter
restatement is not the fix.

## Delete on sight

- **Restatements of the next line.** If the identifier, the following statement,
  or the `it(...)` title already says it, cut it. This includes a comment
  describing a newly introduced variable immediately above its declaration.
  (Function JSDoc is lint-required — see below.)
- **TDD scaffolding.** `// FAILING REPRO.` and the paragraph under it describe a
  bug that no longer exists once the fix lands.
- **Per-test preambles** that restate the title or re-argue the fix. The test
  title is the claim; the source comment is the reasoning.
- **Narration of test steps** when the mock's name already says it
  (`// The second enqueue is the write that fails.`).

## Comments above a log call

A comment above a `logger.error`/`logger.warn` is usually the log message
restated, or a defense of logging rather than throwing. Both go. Keep it when it
carries what the log line cannot:

```ts
// Expected during shutdown; warn so we don't page.
```

Same test as the openers — narration out, information in. Separately, an empty
`catch {}` may need an annotation because lint requires one; keep that minimal.

## Tests

Keep mock and setup mechanics that would otherwise baffle: which prepared
statement the failure targets, why a shared mock makes the expected call count 2,
why a cache is primed before the assertion. Shape rationale stays too — why the
test needs two kernels, why the assertion runs inside the crank.

## Say it once

State a rationale once, at the code it justifies — not in both a source comment
and its test, and not duplicated across sibling files.

At the second site, **delete it and add nothing.** No cross-file pointer, no
"same reasoning as `<name>`" — a reader who needs the argument finds it, and one
who doesn't pays for the line. A pointer is warranted only when the second site
is genuinely hard to understand without it; that is rare, and the burden is on
the pointer.

## JSDoc

This repo lints JSDoc: `ocap/require-jsdoc` is an error on functions, methods,
and classes, and `jsdoc/require-param-description` and
`jsdoc/require-returns-description` are errors wherever those tags appear. Tests
and some JS and config globs are exempt — check `oxlint.config.ts` rather than
assuming. **Do not delete a required block or its description** — make the prose
minimal instead. Keep the `- ` before each `@param` description, and the
sentence casing and terminal period the existing blocks use:

```ts
/**
 * Roll back the crank.
 *
 * @param err - The error the rollback threw, if it threw.
 */
```

Trim `@param` text to a bare noun phrase, not a clause about how the argument
gets used.

## Changelogs

State the change and its why once, then stop. See
[`docs/contributing/updating-changelogs.md`](../../../docs/contributing/updating-changelogs.md)
for format and categories; this section is only about length.

Default to **one line per user-visible change**.

Ask of every line: **Would a consumer notice this change, care about it, or need to act differently because of it?**
If not, cut it. That test is what rules out describing how the fix works
internally, which mechanism was chosen over which alternative, what was
verified, or a "known gap" / follow-up bullet.

## PR bodies

A PR body has a different reader — a reviewer, who does want the narrative and
how the change was tested. The `pr` skill requires both, so **the changelog test
above does not apply here.** Apply only "say it once": the description, the
change summary, and the testing note each make their point once, and none
repeats a rationale that is already in a code comment.

## Checklist

1. Judge every comment the diff adds or touches on information content. The
   openers above are a hint about where to look, not the filter.
2. Delete any whose information is in the identifier, the next line, or the test
   title. If it lives in another file, delete it here too — unless this site is
   genuinely hard to follow without it.
3. For each survivor, ask whether a trivial rename removes the need for it. If
   so, rename and delete the comment, then re-run lint. Do not restructure code
   to remove a comment.
4. Re-read what is left asking **"is this obvious?"** — this is the pass that
   gets skipped.
5. Apply the Changelogs and PR bodies sections to those artifacts.
6. Return control to the calling workflow.
