---
name: spec
description: Turn a natural-language feature request into specs/<feature>/spec.md, with acceptance criteria written in EARS notation wherever a criterion is testable. Use this at the start of any new feature, before any plan or code exists.
user-invocable: true
---

Given a natural-language description of a feature (from the user's message or `$ARGUMENTS`):

1. Pick a short kebab-case feature slug (e.g. `newsletter-signup`) and create
   `specs/<slug>/spec.md` from `specs/_TEMPLATE/spec.md`.
2. Write:
   - **Summary** — one paragraph, what and why.
   - **Acceptance criteria** — one EARS line per testable behavior, numbered `EARS-1`,
     `EARS-2`, ... Use the 6 patterns (Ubiquitous / Event-driven / State-driven /
     Optional feature / Unwanted behaviour / Complex) — never a vague "should work" line.
   - **Out of scope** — explicitly list what this spec does NOT cover, to stop scope creep
     later in `/implement`.
   - **Critical flows** — name any flow that involves money, personal data, or auth; these
     become `critical: true` tasks later and require Playwright coverage (SPEC.md §8).
3. Do not write plan.md or tasks.md — that is `/plan`'s job, after this spec is approved.
4. Stop and present the spec for human approval (GATE humano). Do not proceed to `/plan`
   in the same turn unless explicitly told to.

If the request is ambiguous, ask instead of guessing — an ambiguous EARS line is worse than
no EARS line.
