---
name: thatch-refine-shared-lib
description: Type-specific requirements for refining a plan that touches a library's API surface, in any repo, including personal ones. Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. Use whenever exported API, published packages, or downstream consumers are involved; API hygiene governs even solo projects.
---

You are refining a plan for a **shared-lib** change: work that touches an
API other code consumes and keeps working against. This applies to any
library with external callers, including a personal one. The governing
value is API hygiene: you are writing for consumers you cannot see and
cannot call back. Load `thatch-plan-refinement` for the core loop and
apply the deltas below; where they disagree, these win.

## What this type owes

- **Flexible on input, strict on output.** Accept broad input types and
  normalize them; return precise, well-defined types and never leak
  internal representations. Callers write code against your output
  shapes; widen what you accept, pin down what you emit.
- **Keep special cases out of the API.** No caller-specific knobs, no
  one-off escape hatches, no parameters that exist for exactly one
  consumer. A special case is a design smell: handle it inside the
  implementation or reject it at the boundary.
- **Do not foreclose caller options.** Prefer returning data over making
  decisions callers might want to make differently. Every shortcut the
  library takes on the caller's behalf is a wall they hit later.
- **Keep the surface small.** Every export is a permanent maintenance
  promise. The best API change is often the one that exports nothing new.

## How this changes the loop

- **Deep mode is the default** for anything that adds, changes, or
  removes an export. The abstraction gets locked in at ship time; after
  release, changing it costs every consumer. This is the last cheap
  moment to get the shape right.
- **Alternatives works harder here.** "No better alternative found" must
  be argued harder than the core skill's paragraph: enumerate the
  plausible alternative shapes and say why the plan's shape wins for
  callers, not just for the implementation.
- **Backward compatibility findings are blockers by default.** A breaking
  change without a deprecation path is a blocker, not a should-fix.

## Lens weights

- **Hidden problems reframes entirely.** Every consumer is a stranger;
  you cannot grep your callers. Enumerate the contract the plan changes
  and reason about the population of consumers you cannot see, including
  the ones using the API in ways you never intended.
- **Pattern and reuse applies to your own API first.** Consistency with
  the library's existing API conventions is its own requirement: a
  second method that disagrees with the first in naming or shape is a
  finding even when both are internally fine.

## Extra plan sections

- **API surface diff.** Exactly what is exported, added, changed, or
  removed, in a list a reviewer can check one line at a time.
- **Semver impact and deprecation path.** The version bump this deserves,
  what is deprecated, and how callers migrate.
- **External documentation.** The docs and examples this change requires,
  written for the reader: what the behavior is, when to use it, what it
  does not do. "I'll document it later" is a finding.
- **Caller migration notes.** For breaking or behavior-changing exports,
  the note that goes in the changelog.

## Docs bar

Reader-facing documentation is a plan deliverable, not a follow-up. Draft
it under the writing skills' contracts: define terms on first use,
behavior stated precisely enough that a caller needs no source dive.
