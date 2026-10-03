---
name: plan-change
description: Use when the user says "plan a change", "/plan-change", "plan a feature", "let's design X", "let's discuss this change", "kick off feature/refactor/initiative Y", or wants Claude to drive a discussion that produces both an ADR (architecture decision record) and a Gherkin spec (.feature file) for a piece of work about to start - new feature, refactor, behaviour change, or significant bug fix. Discovers the repo's ADR and specs conventions, holds an interactive discussion to extract scope + architecture + scenarios + edge cases, then writes both files cross-linked together. Composes /write-adr and /write-spec into the natural "I'm starting something" workhorse. Usually arrived at via /start-feature; can be called directly when intent is clear.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Bash(fd:*), Read, Edit, Write, Grep, Glob, Skill
---

# plan-change - drive the discussion that produces the ADR + spec

A piece of work worth doing usually has two documents worth writing before code:

- An **ADR** for the architectural choices the change requires (new
  table, new service boundary, new dependency, new transport, new
  pattern, or a non-trivial refactor of an existing one).
- A **Gherkin spec** for the *behaviour* - what the user does, what the
  system does back, what counts as success, what the edge cases are.

`plan-change` is the "I'm starting something" workhorse. It drives an
interactive discussion to fill out both documents at the same time, then
writes them cross-linked. It composes the same logic as `/write-adr` and
`/write-spec` - you can use either of those standalone if you only need
one half.

Usually `/plan-change` is reached via `/start-feature` (which sorts new
vs existing first, and runs `/backfill-feature` if the feature has no
ADR yet). Call it directly when you already know it's the right tool.

## When to use which skill

| Situation | Right skill |
| --- | --- |
| Not sure yet what kind of work this is | `/start-feature` (entry router) |
| Pure architectural decision (DB choice, library swap, topology) - no new user-facing behaviour | `/write-adr` |
| New user-visible feature, but no architectural decision (a new filter on an existing screen) | `/write-spec` |
| New feature **with** architectural implications (new service, new data model, new external dependency) | `/plan-change` (this one) |
| Refactor that changes architecture or contracts | `/plan-change` |
| Bug fix that's actually a design change in disguise | `/plan-change` |
| Iterating on a feature already shipped - adding a scenario to an existing spec | `/write-spec`, against the existing file |
| Touching a feature that has no ADR yet | `/backfill-feature` first, then `/plan-change` |

If the user invokes `/plan-change` but only one document is actually
called for, write only that one and explain - don't pad an ADR with a
trivial decision just because the skill name says "plan".

## Phase 0 - Discover conventions

Find existing ADRs in `docs/adr/` (or `docs/architecture/decisions/`, etc.) and `.feature` files in `specs/` (or `features/`, `tests/features/`). See `/write-adr` and `/write-spec` skills for full discovery if installed.

Read 2-3 existing examples of each to extract style. Defaults when nothing exists:

- **ADR**: `docs/adr/YYYYMMDD-title.md` (date-prefixed, MADR v3 format - avoids merge collisions when parallel PRs each add an ADR). If the repo already uses sequential `NNNN-title.md`, match it but flag the collision risk to the user.
- **Spec**: `specs/feature-name.feature`, full `As a … I want … So that …` narrative.

## Phase 1 - Open the discussion

Ask the user to describe the feature in their own words, then sharpen through 3-5 follow-up turns. Anchor questions:

1. **What's being decided?** New service, table, dependency, pattern, or a choice between options?
2. **What's the forcing function?** Deadline, outage, vendor migration, customer requirement. Without one, flag that they may be too early.
3. **What alternatives were considered?** "We considered X but rejected it because Y" is the heart of the ADR.
4. **Who's the user?** Customer, admin, internal, service?
5. **Golden path step-by-step?** Concrete actions, inputs, and what counts as success.
6. **Edge cases?** Empty, missing, already-done, concurrent, permission boundary, rate limit, network failure.
7. **What's NOT in scope?** Often more useful than what is.

Read the user's initial description, identify the biggest gaps, ask 2-3 questions. Iterate.

## Phase 2 - Decide what to write

After 2-4 turns of discussion, you should know:

- Is there at least one **architectural** decision worth capturing?
  (Multiple options were considered, the choice has lasting
  consequences, the team needs to remember why.)
- Is there at least one **behavioural** flow worth specifying?
  (User-visible, non-trivial, multiple scenarios, edge cases that matter.)

State the plan back to the user:

```
Plan:
  - Writing ADR <id>: "<title>"  (location: docs/adr/, id format matches repo - e.g. 20260608 or 0042)
  - Writing spec: <feature-name>.feature  (location: specs/)
  - The ADR will reference the spec for the behavioural contract;
    the spec will reference the ADR for the architectural rationale.
```

If only one document is justified, write only that one and explain
why the other isn't needed.

If neither is justified - the conversation revealed it's a tiny change
or already specified elsewhere - say so. Don't write something just
because the skill was invoked.

## Phase 3 - Draft both

Write the ADR using the convention you found in Phase 0 (or default to
MADR v3 with frontmatter if the repo has no existing ADRs). The
`/write-adr` skill, if installed, carries the full template reference.

Write the `.feature` file using the convention from Phase 0. The
`/write-spec` skill, if installed, carries the full Gherkin syntax
reference.

### Cross-linking

Link from the ADR's Context section to the spec, and from the spec's leading comment back to the ADR:

```markdown
## Context and Problem Statement

…See [specs/order-cancellation.feature](../../specs/order-cancellation.feature)
for the behavioural contract this decision supports.
```

The spec uses a `# See docs/adr/0042-order-cancellation.md ...` comment above its `Feature:` line. Match the repo's relative-path convention (some use absolute repo-root paths, some relative).

## Phase 4 - Review with the user

Show both drafts. Ask:

- "Does the ADR capture the *real* reason for the architectural choice?"
- "Are the alternatives in the ADR the ones you actually considered, or
  did I invent any?"
- "Does the spec's golden path match how a user would actually flow
  through this?"
- "Are the edge cases in the spec the ones you'd want to catch in
  regression?"
- "Is there anything in either document that contradicts the other?"

Iterate. Two or three drafts is normal.

## Phase 5 - Write the files

When the user signs off:

```bash
mkdir -p <adr-dir> <specs-dir>
```

Write both files with the `Write` tool. Then commit each separately so
the history shows what was decided when:

```bash
git add <adr-dir>/<adr-file>
git commit -m "ADR <id>: <title>"  # e.g. "ADR 20260608: ..." or "ADR-0042: ..."

git add <specs-dir>/<spec-file>.feature
git commit -m "spec: <feature title>"
```

Match the repo's commit message convention (`git log --oneline -20`).

## Phase 6 - Suggest next steps

After both files land, point the user at natural next moves: `/review-spec` to check overlap before building, then start implementation (ADR defines the *shape*, spec defines the *behaviour*), and `/review-feature` once code exists to check it against the spec.

## Operating rules

- **Have the discussion. Don't skip to writing.** A 5-turn discussion produces documents the team will actually use; a one-shot draft from the user's first sentence produces fan fiction.
- **Don't decide the decision for the user.** Present the trade-offs; let them choose. If asked for an opinion, give one with reasons, but the call is theirs.
- **Don't pad.** If only one option was viable, say so rather than inventing strawman alternatives. If only one document (or neither) is justified, say so and write only what's needed - the skill doesn't owe you an output.
- **Match local style.** Read 2-3 existing examples of each document type before drafting.
- **Cross-link both ways.** ADR to spec, spec to ADR. Without cross-links, the two documents drift.

## Composing with other skills

- **Before:** `/start-feature` is the usual entry. `/backfill-feature` runs first if the feature you're modifying has no ADR yet.
- **After both documents land:** `/review-spec` checks for overlap / conflict against the rest of the corpus.
- **Once code exists:** `/review-feature` audits implementation against the spec written here. `/drive-change` runs the full audit suite.
