---
name: project-review
description: Review pending changes (working tree diff, a branch, or a PR) for correctness and for THIS repository's own invariants, listed in the Invariants section below. Use when asked to review changes, a diff, a branch or a PR in this repo, and before committing anything non-trivial.
---

# Project review

Review the target for correctness first, then for this repo's invariants. If the user
passed arguments, treat them as the target (a PR number, branch, or path); otherwise
review the working-tree changes (`git diff`, `git diff --staged`, and untracked files
from `git status`).

> **Seed file.** The "Invariants" and "Known deliberate gaps" sections below start empty
> on purpose. Fill them in with this repo's real rules (see `AGENTS-SETUP.md` for where
> they come from). While any `<fill>` marker remains, say so at the top of the report and
> run the generic passes only — never invent invariants.

## Ground rules

- Read enough surrounding code to judge each change in context; never review a hunk alone.
- Report findings ranked by severity, each with `file:line`, a one-sentence claim and the
  concrete failure scenario. Verify a finding is real before reporting it; drop what you
  cannot substantiate.
- Findings are the deliverable. Report them; do not fix them unless asked.
- If the diff is clean, say so plainly. Do not invent nitpicks.
- Say what you did NOT check (no tests run, no running app, file not read).

## 1. Correctness pass

Bugs, broken edge cases, error-handling gaps, type or contract mismatches, security issues
(secrets, injection, auth), and regressions to existing behaviour. Run what the diff
touches (tests, linter, type-check) rather than assuming; quote the command and output.

## 2. Generic invariants (apply to every repo)

1. **Hand-synced mirrors** — if the diff changes one side of a pair the repo keeps in sync
   by hand (API shapes vs client types, docs vs code, a generated file vs its source), the
   other side must change in the same diff.
2. **Generated files are not hand-edited** — a diff touching generated output without its
   source is a finding.
3. **Published/versioned artefacts are immutable** — a diff editing one in place instead of
   adding a new version is a finding.
4. **Secrets and personal data** — none in the diff, none in logs, none in test fixtures.
5. **Docs staleness** — if the diff changes commands, env vars, ports, routes or counts,
   the README and agent-guidance docs change in the same diff.
6. **Tests** — a changed behaviour without a test that would fail without the change is a
   finding; a test that cannot fail is a finding.

## 3. Invariants (this repo) — <fill>

List the repo's own rules, one per line, each checkable from the diff. Example shape:

| # | Invariant | Where it lives | A violation looks like |
|---|-----------|----------------|------------------------|
| 1 | <fill: e.g. "API shapes in A and B change together"> | <fill: files> | <fill: diff touches A only> |

## 4. Known deliberate gaps — <fill>

Things the repo knowingly does not have yet (CI, a test suite, an eval set). These are not
findings unless the diff claims otherwise. Delete an entry the day it ships.

## Report format

```
Review of <target> — <N> findings (<critical>/<high>/<medium>/<low>)
Not checked: <what you did not run or read>
1. [severity] file:line — claim
   Scenario: <concrete input/state -> wrong outcome>
```
