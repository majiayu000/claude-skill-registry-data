---
name: "speckit-retro"
description: "Judge a finished feature as a whole and record a verdict — accepted, accepted-with-open-items, or rejected — from its commits, diff, tasks, requirements and deferred findings, with a source for every claim. Runs after /speckit-review and before /speckit-archive. Use when a feature is done, or when nothing in the repository says whether the last one was any good."
argument-hint: "Optional: the feature directory to judge (defaults to the active feature)."
compatibility: "Node 18+. Writes specs/<feature>/retrospective.md and nothing else."
metadata:
  author: "speckit-demo"
  source: "adapted from BMAD's bmad-retrospective (docs.bmad-method.org/build/finish-an-epic)"
user-invocable: true
disable-model-invocation: false
model: fable
---

## User Input

```text
$ARGUMENTS
```

## Why this exists

`/speckit-harden` judges code mid-flight. `/speckit-learn` mines a *session* for
instincts. `code-reviewer` and `spec-reviewer` judge a *diff*. Nothing read a
finished feature as a whole and said whether it was any good — feature 007
reached seventy-three done tasks and no artifact in this repository recorded a
verdict on it.

BMAD's retrospective is the missing step, and its discipline is the part worth
copying: it reads "the specs, story records, full diff, commits, and tracking
files", and **"every finding carries a source reference: a file, a line, a
commit, a log."** A retrospective assembled from memory is a feeling.

## Phase 1 — gather, do not recall

```bash
node .claude/scripts/retro-evidence.mjs specs/<feature>          # human-readable
node .claude/scripts/retro-evidence.mjs specs/<feature> --json   # machine-readable
node .claude/scripts/retro-evidence.mjs specs/<feature> --since <ref> --jev   # + a suggested verdict to argue with
```

That gives you: artifacts present, tasks open/done, requirements declared and
retired, the `## Spec Delta` and whether its capabilities exist, every commit
that touched the feature, the diff stat and file list, open deferred findings,
and open action items carried in from earlier retrospectives.

Then read what the counts point at — the actual diff, the actual files. The
script reports; it does not judge, and it cannot tell you whether an abstraction
earned its place.

## Phase 2 — look for what no single review could see

A per-diff review cannot see accumulation. These are the four questions:

1. **Patterns that grew a commit at a time.** An abstraction that gained a
   caller per story until nobody would introduce it today. A helper that became
   a second way to do something the codebase already did.
2. **Spec divergence.** Requirements delivered differently from how they were
   written. For each: is the spec now wrong, or is the code? The answer becomes
   a `Modifies` in the `## Spec Delta` before `/speckit-archive` runs.
3. **Runtime behaviour.** Run the thing. `npm test` passing is not the same
   claim as the feature working.
4. **Carryover.** Items the last retrospective left open that this feature was
   expected to address — say plainly whether each was.

Every finding cites `path:line`, a commit hash, or a command and its output. A
finding you cannot source is one you drop.

## Phase 3 — the verdict

One of exactly three, in the frontmatter:

| Verdict | Meaning |
| --- | --- |
| `accepted` | meets its acceptance criteria; nothing outstanding blocks the next feature |
| `accepted-with-open-items` | meets them, with named action items carried forward |
| `rejected` | does not meet them — say which criterion, and what would change that |

A verdict with no stated criterion is an opinion. Name what you judged it
against: the spec's success criteria, the constitution, the acceptance scenarios.

## Phase 4 — write it

Copy `.specify/templates/retrospective-template.md` to
`specs/<feature>/retrospective.md` and fill it in. Open checkboxes under
**Action items** are what `.claude/scripts/retro-evidence.mjs` carries into the next
feature's retrospective, so leave one open only if it is genuinely still owed —
an open item nobody intends to do trains everyone to ignore the list.

Then:

1. `node .claude/scripts/run-state.mjs set --status done --phase retro`
2. Hand off to `/speckit-archive`, which merges the Spec Delta into the living
   capability specs.
3. Commit it to the private specs repository, where the feature folder lives:
   `node .claude/scripts/specs-repo.mjs commit "docs(specs): ST-<n> retrospective" -- <feature>`
   (never `git add specs/` on the motor-fix branch, which ignores `specs/`).

## Boundaries

- It proposes action items; it never assigns them to a person who has not
  agreed, and it never silently fixes what it finds. A fix is a new change with
  its own level (`/speckit-size`) — that separation is the same one the Agent
  Execution Rules draw between the deliverable and a follow-up.
- It never edits code, tests or the spec. A spec correction it identifies goes
  into the `## Spec Delta`, which `/speckit-archive` applies.
- `rejected` is a real option. A retrospective that can only ever accept is
  theatre.
