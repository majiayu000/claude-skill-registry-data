---
name: spec
description: Interview the user, inspect the repository, write a feature specification and implementation plan, then hand implementation to a fresh session. Use when the user asks to define or plan a feature before implementation or invokes the spec workflow, for example "plan a new feature with me", "write a spec", "spec this feature".
license: MIT
compatibility: "Claude Code"
argument-hint: "[feature description]"
---

# Spec

1. Interview the user one question at a time about behavior, UX, edge cases, constraints, and trade-offs, starting from the feature description when one was given. Do not ask what the repository already answers.
2. Inspect relevant code before locking decisions.
3. Write the specification to the repository's documented specification location as `<YYYY-MM-DD-feature>-spec.md`; if none is documented, propose `docs/specs/` and confirm. Never write it into the planning location: a spec there is read as the active plan. Start it with frontmatter `status: draft`, `owner` and `last-verified: <today>`, then cover goals, non-goals, flows, technical design, decisions with rejected alternatives (one line each), contracts, failure handling, acceptance criteria, tests, and unresolved decisions.
4. Write the implementation plan to the repository's documented plan location as `<YYYY-MM-DD-feature>.md`. Start it with the goal, the decisions, and a `Status: in progress | done` line; write every step as a `- [ ]` checkbox with What, Where, How, Test, `Done when` (its acceptance criterion), complexity (S/M/L), and a deployable invariant; end with `## Open questions` and a `Next action:` line. plan-status and session-retro read these.
5. Check the spec and plan against each other: show a coverage table (each acceptance criterion → its step IDs, each step → its criterion; a gap either way is a hit), scan for vague words ("fast", "robust", "intuitive"), placeholders (TODO, ???) and scope reduction ("v1", "for now", "stub", "placeholder", "future enhancement": a step delivering less than a decision says), and read the project's decision records and `AGENTS.md` invariants for conflicts. Put every hit under `## Open questions` before the hand-off.
6. Offer to add the plan's steps to the project backlog: find or create its files as audit-to-backlog's Establish scope does (the `Backlog:` line, the path question before creating them, the git-ignored warning) and write each step as an item in the `developer-os:audit-to-backlog` format, with the `FEAT-` prefix, the next free `FEAT` number, and severity P2 unless the user names another of P0–P3, filed under that severity's section; complexity becomes `Size`, the step's `Done when` stays `Done when`, its Test becomes a runnable `Check` (`Manual: …` when no command can check it), `Where` is the step's Where, `Problem` and `Fix` are one line each (what is missing, what the step builds), and `Evidence` is the spec path and section (`docs/specs/<file>#<section>`), since new work has no `file:line` yet. Add `Session N: <ID>, …` lines of 5–7 items each for them under `## Implementation sessions`, so `implement-backlog` can execute them. Then replace each step in the plan with a plain line linking its ID (`- FEAT-03: <title>`, no checkbox), so the work is counted once, in the backlog.
7. Stop and hand implementation to a fresh session: when the steps moved to the backlog, a prompt that invokes `developer-os:implement-backlog`, which runs a convergence check against the acceptance criteria when the spec's last `FEAT-` item closes; otherwise "continue from <plan path>".

## Stop point

Stop after the specification and plan are written and the backlog offer is answered. Return both paths and the step 7 handoff prompt for a fresh session.

## Never

- Implement any part of the feature.
- Overwrite an existing plan or specification.
- Add items to the backlog without the user's yes.
