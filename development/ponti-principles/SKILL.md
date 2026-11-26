---
name: ponti-principles
description: "Use when writing, reviewing or refactoring Charles's code: the engineering laws for architecture, code shape, data and secrets, tests and dependencies."
license: MIT
compatibility: Any repo. TypeScript, React Native and Swift are covered in depth; the laws carry to other stacks.
metadata:
  author: ponti-studios
  version: "2.0.0"
  category: Engineering
  tags: [principles, standing-rules, review, engineering, code-style]
---

# Ponti principles

How Charles wants code written, in one place. Twenty-six laws, ordered inside each section by how often he
has had to _correct_ an agent into them — the top of a section is what agents most reliably get wrong.

**The laws are code craft, not work management.** Branches, PRs, merges, deploys, tickets and voice are not
laws here: they are detail in the references below, and operationally they live in `linear-tickets` and
`switchyard-fleet-ops` (lives in the switchyard repo at `docs/skills/switchyard-fleet-ops`). Design has its own depth in [product-and-design.md](references/product-and-design.md).

Load this before writing code and before reviewing a file or a diff. Where a law conflicts with a framework
default or your own habit, the law wins. A law is not always his literal words: one that began as an
inference from how he reviews is marked _(inferred)_ in the reference behind it, and his next correction
overrules both.

## Precedence

1. What Charles says in the moment wins. Record a durable preference in the canonical source when the user asks to retain it.
2. A repo's own written rules (`AGENTS.md`, `CLAUDE.md`, a repo-local skill) beat this skill where they
   conflict. They usually add to it.
3. This skill fills every gap the repo leaves open.
4. Charles is the product manager and architect. Never invent product behavior, navigation or
   architecture and present it as decided ([workflow.md](references/workflow.md), "Decision authority").

## The laws

### Before you write code

1. **Plan first, in the open.** State what must be built, in what order, and how each step can be tested.
   Go deep on the latest docs before using a framework's features. If the task is big, the plan is the
   first deliverable.

2. **YAGNI.** The smallest thing that works. One-liners where they read well, nothing built for later, no
   options nobody asked for.

3. **Check blast radius.** If a change alters an existing default, endpoint behaviour, or consumer, flag it
   before handoff — don't let it ride along silently.

### Architecture

4. **The API owns server-side business logic.** No screen or client reaches a database directly. On
   device, the same rule takes the local form: decisions that must be right live in the native package
   and screens only draw the state they are given ([swift.md](references/swift.md)). One owner per decision,
   never shared between screen and server.

5. **Simplify toward the goal.** If the stack is heavier than what the user wants to accomplish, say so and
   cut. Squash proliferating files into a few canonical ones. One function where one suffices.

6. **Shared code lives together.** Platforms that share code share a repo. Extract reusable units (hooks,
   input groups, shared UI package imported like a library) instead of duplicating per app.

7. **One pattern, applied everywhere.** Merge duplicates; reuse the existing way rather than adding a
   parallel one. Two ways to do the same thing is a defect.

8. **Isolate state for performance.** Form edits must never re-render the world. Treat visible input delay
   as an architecture bug.

9. **One standard shape for repeated surfaces.** List endpoints: bounded limit, opaque keyset cursor,
   deterministic ordering — plus route tests for cursor boundaries, an empty page, and a row inserted
   between pages.

10. **Schema-first for anything read from outside the program.** Validate at the boundary; no hand-rolled
    guards scattered through the body. Not for a one-line comparison or matching an error message — a
    schema adds noise there ([typescript-react-native.md](references/typescript-react-native.md)).

11. **Offline behaviour is a design constraint**, stated upfront, not discovered later. Sync claims
    require a ground-truth check (e.g. airplane-mode test verified against the server), never an
    assumption. Serving cost is the same kind of constraint (law 22).

### Data, secrets, trust

12. **Secrets are a designed plan**, explained before implementation — not values pasted into places.

13. **Never print, log or commit a secret.** Not in a report, not in a test, not "temporarily". Rotate
    anything that leaked into a log or a diff.

14. **Nothing about a person is stored that they cannot see, delete and switch off.** Memory-like
    features are off by default with a brief undo. Telemetry is content-free (closed enums and numbers,
    never a free string or a transcript): on by default for TestFlight, off for the App Store until it is
    switched on, and shown in full before it is sent ([data-and-trust.md](references/data-and-trust.md)).

### Code, review, dependencies

15. **Short domain names.** Name what a thing is, not how it is stored. Units in numeric names. One word per
    concept.

16. **No nested or multi-way ternaries.** A lookup table, early returns, or an exhaustive `switch`. One
    short two-way ternary is fine — the lint rule draws the same line.

17. **Tooling enforces style, not comments asking nicely.** Types, lint and formatter are the enforcement;
    a convention nobody checks is a preference.

18. **Delete before adding; kill dead things completely.** No unused code, params, options, exports, files
    or dependencies, no compatibility shims inside an app. When an idea, app, skill or test dies, remove all
    of it — including related artefacts and leftover dot folders. A "stupid test" gets deleted, not
    defended.

19. **Account for existing failures.** Diagnose failures encountered during the task. Fix those within the authorized scope and report unrelated failures with evidence.

20. **Decomposition ships with tests.** Breaking a file apart and writing its test file are one
    instruction. Coverage is a consequence of the specified cases, not a target: a test that only
    constructs a type or asserts a private detail is deleted, not kept to move a number.

21. **Mock before you integrate.** Mock external providers (MSW-style) against a set of realistic scenarios
    before calling the real thing.

22. **Price before you pick.** Model and tool choices get a cost comparison first. Hosting and serving costs
    are part of the design.

23. **Latest tooling, gold-standard scaffolding.** New apps are set up as the reference example: current
    versions, lint/format tooling (oxlint/oxfmt/ruff as appropriate), modern platform floors (@Observable,
    current iOS/macOS unless the repo states a deliberate minimum). Volatile values (tool counts, version numbers that change) never get hardcoded into
    durable text; metadata stays short but discoverable.

24. **Keep disposable output out of the repo.** Retain intentional fixtures, templates and generated distribution resources when the repository requires them; keep their source and regeneration procedure clear. Present code properly formatted.

### Rigour

25. **Prove with evidence.** Logs and measurements before rebuilds; run it, test it, read it back. "Done"
    means verified — never claim a state you did not check.

26. **Verify the contract before claiming absence.** A claim that something is missing, broken, unsupported or
    fixed carries the live check behind it — schema confirmed, filters widened, a control probe, a read-back —
    or it is reported as unverified ([verify-before-asserting.md](references/verify-before-asserting.md)).

## How to run a review

1. Read the file, diff or PR in full before judging it.
2. Find the repo's own checks (type check, lint, format, tests) from its docs or manifests. Use those.
3. Open only the references the change touches (table below). Check each law and each rule.
4. Report only real violations: file, line, the rule it breaks, the fix. No padding, no praise filler.
5. For a refactor, preserve behavior except for changes explicitly included in the requested outcome. Validate each coherent change.
6. Say what was run and what was not (not run on a device, not run live, not run at all).

## Which reference to open

| Touching                                                            | Open                                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Any code                                                            | [code.md](references/code.md)                                       |
| TypeScript, React, React Native, Expo                               | [typescript-react-native.md](references/typescript-react-native.md) |
| Swift, SwiftUI, native modules, watchOS                             | [swift.md](references/swift.md)                                     |
| Screens, copy, motion, errors, PRDs, design files                   | [product-and-design.md](references/product-and-design.md)           |
| Secrets, user data, telemetry, auth, databases, APIs                | [data-and-trust.md](references/data-and-trust.md)                   |
| Branches, commits, PRs, merges, deploys, tickets, debugging, checks | [workflow.md](references/workflow.md)                               |
| Claims that something is missing, broken, unsupported or fixed    | [verify-before-asserting.md](references/verify-before-asserting.md) |
| Reports, summaries and how to talk to Charles                       | [communication.md](references/communication.md)                     |

## Final checklist

- [ ] Untrusted data goes through a schema; no hand-rolled guards
- [ ] No nested or multi-way ternaries; no clever one-liner that hides logic
- [ ] Names are short domain nouns; units in numeric names; one word per concept
- [ ] No unused code, params, options, exports, files or dependencies
- [ ] No inline styles; the repo formatter, linter and type check are clean
- [ ] Existing pattern reused; no duplicated helper
- [ ] Nothing about the person is stored that they cannot see, delete and switch off
- [ ] No secret, key or user content in the repo, build, log or telemetry
- [ ] Full checks ran for every affected package; skipped checks are named
- [ ] The report says plainly what changed, why, and what is unverified

## References

- [code.md](references/code.md) — the day-to-day code rules: names, shape, error handling, deletion.
- [typescript-react-native.md](references/typescript-react-native.md) — TS/React/Expo specifics.
- [swift.md](references/swift.md) — Swift, SwiftUI and native module specifics.
- [product-and-design.md](references/product-and-design.md) — product framing, screens, copy, motion, PRDs, design laws.
- [data-and-trust.md](references/data-and-trust.md) — secrets, personal data, telemetry, auth, databases, APIs.
- [workflow.md](references/workflow.md) — scope, branches, commits, tickets, PRs, merges, deploys, checks.
- [verify-before-asserting.md](references/verify-before-asserting.md) — proving absence, breakage and fix claims against the live surface.
- [communication.md](references/communication.md) — how to talk to Charles, reports and summaries.
