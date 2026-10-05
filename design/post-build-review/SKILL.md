---
name: post-build-review
description: Run a post-implementation review that checks a built change against the intent that was set. Run lint, typecheck, tests, and build; confirm the result matches the chosen design direction and covers its promised states (loading, empty, error, disabled, permission, offline, long content, maximum volume, and partially complete data); check accessibility and responsive behaviour; flag any risky surface; and assemble the handoff evidence a reviewer needs. Read-only — it reviews and reports, it never edits. Invoked automatically by the build skill after implementation, and available manually after a build or a meaningful change, after ui-craft and before opening or finalising a PR, especially when the user asks to verify, review, sign off, sanity-check a built change before handoff, or asks whether a change is ready to ship.
---

# Post-build Review

## Overview

Use this as a small gate after implementation, the read-only mirror of `pre-build-review`.
Its job is to confirm a built change matches the intent that was set, that it runs and is accessible, and to produce the evidence a reviewer needs before handoff.
It reviews and reports; it never edits.

Do not turn this into a redesign.
Check the build against the intent, run the checks, name what is off, and decide whether it is ready to hand off.

## Inputs

Use whatever the change can be checked against, inspected from the repo rather than asked for where possible:

- the diff or the built change
- the chosen direction — a labelled Paper frame, a prototype winner, or a Figma reference — and its decision note when present
- the `pre-build-review` verdict and its `Missing states` list when present
- `CONTEXT.md`, ADRs, and canonical terms
- the UI quality bar: any installed `ui-craft` skill's `references/quality.md` and `references/accessibility.md` (see the suite README for layout); otherwise the project's own design docs
- nearby code and existing components

When the chosen direction or the state list is not written down, reconstruct the expected intent and states and say so; do not block on their absence.

## Workflow

1. Reconstruct in 2 to 4 sentences what the change was meant to do.
2. Run the checks: lint, typecheck, tests, build. Record pass or fail with the output.
3. Where there is a route or a Storybook story, run the build and check for console errors, axe violations, contrast, visible focus, and keyboard reachability. Reuse the already-running dev preview for these checks; never launch a competing server. These checks need a real browser, so never infer them from source: when no browser is available, or no dev preview is running and none can be reused, record each one as `not run` and carry that wording into the verdict.
4. Compare against intent: does the build match the chosen direction (layout, hierarchy, spacing, type, colour roles, material differences only, never pixels), and does it cover the states the plan promised (loading, empty, error, disabled, permission, offline, long content, maximum volume, and partially complete data)?
5. Check craft and the obvious responsive and accessibility misses against the quality bar sources listed in Inputs. Judge craft through six signals: reliability, speed, clarity, efficacy, efficiency, and beauty — and flag where the change optimises one signal by damaging another.
6. Note any change to a risky surface (auth, permissions, API, routing, data). If present, do not approve; flag for an engineer and a security pass.
7. Decide the verdict and assemble the handoff evidence.

## Output

Lead with the verdict, mirroring `pre-build-review`:

- `Pass`: ready to hand off.
- `Pass with notes`: ready to hand off with the listed non-blocking notes.
- `Fail`: return to an earlier stage first.

Then provide only the useful detail:

- `Checks`: commands run and their results.
- `Intent match`: material differences from the chosen direction.
- `State coverage`: states covered and missing.
- `Accessibility and responsive`: concrete findings, listing any check that could not be run as `not run` rather than omitting it.
- `Risky surfaces`: anything touching auth, permissions, API, routing, or data.
- `Handoff evidence`: a ready-to-paste PR block (what changed, design reference, what was tested, reviewer focus, known risks).
- `Next step`: the single next action.

Each finding names the stage that owns it, so a `Fail` returns to the right place: intent to `paper-prototype` or `prototype`, states or scope to `pre-build-review`, domain or terms to `grill-with-docs`, craft to `build` with `ui-craft`.

## Rules

- Read-only: it reviews and reports, it never fixes.
- Run the checks rather than assert them; lead with evidence. A check you could not run is `not run`, never a pass — downstream steps reuse this record as proof.
- Be direct; prefer concrete scenarios to abstract warnings.
- Intent and craft notes are advisory; do not gate on subjective taste.
- Do not invent design direction.
- If the change touches a risky surface, or you cannot personally explain it, escalate rather than approve.
