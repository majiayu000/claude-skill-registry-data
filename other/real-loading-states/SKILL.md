---
name: real-loading-states
description: "Generic loading UI repair for Pattern Patrol P8. Use when you find 'Loading...' text, unlabeled spinners, meaningless pulses, Suspense fallbacks, or loading placeholders, or when running a P8 patrol."
---

# Real Loading States

Read the Pattern Patrol system, the P8 registry row, repo `CLAUDE.md`, and the
`pattern-patrol` skill first. Their batching, approval, certification, and
release rules remain binding.

## Detect

From the repository root, scan UI source with:

```bash
rg -n -i --glob '*.tsx' --glob '*.jsx' '\bloading\s*(\.\.\.|…)' \
  app components features lib hooks providers utils
```

The word boundary deliberately excludes `Uploading…` and `Downloading…`.
Every match is a candidate until its rendered context is verified.

Also inspect generic visual loaders that the literal grep cannot see:

```bash
rg -n --glob '*.tsx' --glob '*.jsx' '<SuspenseLoader|Loader2|animate-spin|animate-pulse|Skeleton' \
  app components features lib hooks providers utils
```

Review rendered context. A spinner, shimmer, pulse, or skeleton is still a P8
finding when it does not tell the user what part of their work is loading, or
when its shape bears no relationship to the content that will replace it.

## Classify every candidate

Choose exactly one route:

1. **Standing-authority repair** — a contextual canonical loader or
   surface-shaped skeleton is clearly superior, behavior-preserving, and
   bounded; repair it now.
2. **Genuine product decision** — competing legitimate loading experiences
   would materially change interaction, final geometry, progressive disclosure,
   or visual intent; ask Arman about that decision only.
3. **Missing evidence/machinery** — the correct result is clear but the owning
   primitive, final geometry, chunk boundary, or proof harness is unknown;
   investigate or create a focused task. Do not ask Arman to approve making the
   loader professional.
4. **Compliant/false positive** — an existing component-library loader or
   skeleton, a spinner/pulse with contextual status, ARIA-only text, comment,
   fixture, diagnostic, or non-UI string. Record the reason; do not mutate.

An empty repaired set is not completion when a clearly superior bounded repair
is known. If an optional debatable enhancement surrounds an obvious contextual
loader fix, ship the obvious fix and ask only about the enhancement.

## Standing-authority repair

Repair automatically when all conditions hold:

- The state is user-visible and generic, misleading, unlabeled, or visibly
  poorer than the established project standard.
- One canonical contextual loader or skeleton is clearly superior. Prefer
  `@/components/loaders/SuspenseLoader` for compact states and existing
  surface-specific skeleton primitives for content-shaped states.
- The surrounding wrapper, dimensions, theme classes, data/control flow,
  interaction, chunk entry, and desktop/mobile plus light/dark behavior remain
  unchanged. A surface-shaped skeleton may mirror already-established final
  geometry but may not redesign it.
- A deterministic contextual message is available, such as
  `Loading model providers…`. Describe only the user's work; do not expose
  internal services, queues, implementation steps, or sensitive operations.
- The target file has no overlapping uncommitted edits.
- The batch contains at most 15 files.

Use the existing primitive:

```tsx
<SuspenseLoader centered={false} message="Loading model providers…" />
```

Preserve the existing fallback wrapper. Static import of this lightweight,
server-compatible primitive is required; do not add a dynamic boundary or
create another loader. If the primitive lacks a generally useful capability,
extend it compatibly rather than wrapping or copying it locally.

For page, panel, list, tree, editor, preview, or identity content, use a
surface-shaped skeleton automatically when the final content geometry and data
shape are already established and the skeleton can reuse an existing primitive
without changing settled layout. Otherwise record the missing evidence and
create a focused design/proof task.

## Human-decision requirements

Escalate only a decision with multiple legitimate outcomes. State:

- the affected surface and grouped files;
- the competing options and their user-visible tradeoff;
- the safe core repair already completed, if any;
- the exact choice that cannot be inferred from doctrine or established UI;
- the verification plan.

Approval covers only that choice. Do not bundle obvious loader cleanup into the
question.

## Required false-positive review

Exclude only after verifying the rendered context:

- `aria-label`, `ariaLabel`, `title`, and screen-reader-only descriptions;
- comments, docs, fixtures, parser samples, logs, and copied/exported data;
- contextual operation labels such as uploading, downloading, compiling, or
  processing that are not bare loading text;
- an existing `SuspenseLoader`, `LoadingSpinner`, `Skeleton`, `Loader2`,
  spinner ring, shimmer, or pulse paired with contextual status;
- error and empty-state copy that merely contains the word “loading.”

A spinner plus a contextual message is compliant even when the message begins
with “Loading.” A bare animated text pulse is not a component-library loader.

## Verify and certify

After every standing-authority or human-decided batch:

1. Re-run the scoped grep and confirm the repaired bare literals are gone.
2. Run `pnpm type-check` and the relevant repository gates.
3. Apply the Pattern Patrol risk-based matrix: inspect every changed file
   statically, then browser-check one representative surface per distinct
   component/interaction/layout risk class on the other theme and viewport.
   Use the full relevant desktop/mobile and light/dark matrix only for shared
   primitive, interaction, responsive-layout, or theme changes.
4. Spawn a second adversarial agent with: **“assume this broke something; find
   it.”** The certifier repeats the grep and gates, reviews false-positive
   classes, and returns `CERTIFIED` or `REJECTED` with evidence.
5. Fix or fully revert a rejected batch. Ship nothing “mostly.”

After a certified batch, record the transform and exact gates in the P8 report
and registry. Proven classes become reusable recipes. A broader case asks Arman
only when it contains genuine product judgment; missing implementation proof
becomes a focused task, not an approval request.
