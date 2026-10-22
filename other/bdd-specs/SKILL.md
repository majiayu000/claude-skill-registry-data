---
name: bdd-specs
description: >-
  Writes behavior-driven executable specs (Feature > Scenario > Specification, one assertion
  per test) from a feature's STORIES.md and PLAN.md, in C# or Lit/TypeScript, using the
  project's existing test framework. Use when stories are final and it's time to write the
  tests, or when asked to spec out, write tests first, or do BDD/TDD.

---

# BDD specs

Specs are written before the `builder` subagent implements a task — see "Open question"
below if your team wants to relax that. The spec is the design artifact: it encodes the
intended behavior from the stories, is marked pending until the code exists, and is
`feature-build`'s definition of done for the task.

This skill states the discipline once and applies it to whichever layer(s) a feature actually
touches — backend (C#), frontend (Lit + TypeScript), or both. The shape (Feature > Scenario >
Specification, one assertion, happy-then-sad, pending by default, a real-entry-point spec) is
identical either way; only the syntax it's expressed in differs. Don't duplicate this
discipline into a second, stack-specific skill — extend the relevant reference file instead.

## *🎯 Why: Design for Change*

One assertion per Specification means a failing spec names exactly what broke. Segregating
happy path from sad path means you can change one behavior without re-reading the whole
suite. The spec suite is the change-budget for the codebase — treat generating it as
seriously as generating the code it will gate.

## Gate: require the design and the stories first

Read the feature's plan folder.

1. **`SPEC.md`** — if it's missing, still a stub, or full of `TODO`, **stop**. Tell the
   user: "No design yet — run `feature-design` first, so specs are grounded in real extension
   points and API shapes instead of invented ones."
2. **`STORIES.md`** — if it's missing, empty, or full of placeholder text, **stop**.
   Tell the user: "No stories yet — run `feature-plan` first, so specs come from real
   acceptance criteria instead of invented ones."

Do not draft design or stories yourself under this skill — that's `feature-design`'s and
`user-stories`'s job. If both gates pass, proceed.

## Which layer(s) does this feature touch?

Check `SPEC.md`'s "Management API surface" and "Frontend components" sections, and read
only the reference file(s) that layer needs:

- **Management API surface isn't "none"** → read `references/backend-csharp.md`.
- **Frontend components isn't "none"** → read `references/frontend-lit.md`.
- Both present → read both, and generate both as separate spec files in their respective
  projects. A story that spans both layers gets a spec in each — don't try to force one file
  to cover both.

## Hard rules (apply to every spec, either layer)

1. **Happy path first, and exhaustive.** Cover every success outcome the story implies
   before any failure case.
2. **Sad path is segregated** into its own scenario grouping, never interleaved with
   happy-path specs.
3. **Exactly one assertion per test.** No multiple assertion calls in one test, no looped
   assertions across a collection — assert on the collection shape instead (a single-item or
   count check), or split into one test per element being checked.
4. **At least one spec per feature exercises the real entry point** — for a backend story, a
   Management API controller action through an in-memory test server, or a service resolved
   from DI exactly as Umbraco's Composer would wire it up; for a frontend story, the actual
   custom element rendered and driven through its public attributes/properties/events, not an
   internal method called directly. Fakes/mocks are fine for collaborators the spec doesn't
   own; the entry point itself must be real.
5. **Match the project's existing test conventions** before inventing new ones — reuse its
   builders, fakes/mocks, and fixtures rather than writing ad hoc setup per spec.
6. **New specs are pending by default**, marked so the runner reports them as skipped, not
   failed, until a `builder` task makes them pass: `[Ignore("Pending")]` in NUnit,
   `[Fact(Skip = "Pending")]` in xUnit, `it.skip` in Mocha. A spec left active against code
   that doesn't exist yet fails the whole suite, and the next task can't tell its own failures
   from these.
7. Never invent acceptance criteria. If a story is underspecified, stop and send the user
   back to `user-stories` to tighten it.

Before reporting, reread every spec you wrote against rules 3 and 6: one assertion each, and
each one marked pending. These two slip most often.

## *Examples and per-stack mechanics*

- **`references/backend-csharp.md`** — test framework detection, the shape mapped onto
  NUnit (or xUnit), a full worked example, file/naming convention.
- **`references/frontend-lit.md`** — test framework detection, the shape mapped onto native
  `describe`/`it` blocks, a full worked example, file/naming convention.

## Open question: before or alongside implementation?

This skill assumes specs are written and pending before `feature-build` dispatches the
`builder` for the matching task — strict TDD. Writing tests alongside the implementation
instead, with the same one-assertion/happy-then-sad rigor applied after the fact, is equally
legitimate. Confirm which stance a project wants once, early (e.g. in its `CLAUDE.md`), rather
than letting it drift task by task.
