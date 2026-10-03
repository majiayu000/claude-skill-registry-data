---
name: verify-flow-as-built
description: >
  Checks that a designed screen-to-screen journey — an interaction diagram or a
  named list of steps — actually runs that way in the build, with the data
  changes it specifies. Walks each journey end to end, derives the as-built
  navigation and API edges from the code, and renders a page comparing designed
  and as-built flow side by side, with a pass/fail wiring matrix per step.
when_to_use: >
  The PRD carries an interaction diagram (screen-to-screen edges, e.g. Mermaid)
  or a list of screen-to-screen journeys the feature is meant to support.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Verify Flow As-Built

## When it applies

The PRD carries an interaction diagram or a list of screen-to-screen journeys — the shape a
user is meant to move through the build, screen by screen, with the data each step is meant to
change. This check does not apply to a PRD that describes only single screens with no
between-screen journey.

## Inputs

| Input | Where it usually comes from | Required or optional | Default |
|-------|------------------------------|------------------------|---------|
| Designed flow | The PRD's interaction diagram (a Mermaid graph, or equivalent), or a named list of journeys (each an ordered list of screens/steps) | Required | None — without a designed flow there is nothing to compare against |
| Source root | `stack.md` / `CLAUDE.md` (where the app's routes, navigation calls and API handlers live) | Required | The project root |
| How to run a journey | The project's own docs (`CLAUDE.md`, `stack.md`, existing suites) — how to start the build and drive it through a screen | Required | The stack-hint table in the verification contract (`functional-verification.md`, "The four stack hint rows"), used only when the project's own docs are silent |
| Data store to read before/after each step | `verification.md` (which store, and whether reading — or writing — it is authorised) | Optional | None — a journey with no stated data store is walked for navigation only, and its statement omits the data-change clause |

## Criteria

One row per designed journey — never one row per step, and never one row spanning every
journey. ID: `FL-<journey slug>` (the journey's own name, slugified; stable across runs so a
resumed loop keeps a settled verdict attached to its journey). Statement: "Journey `<name>` runs
`<A → B → …>` as designed, with the data changes it specifies." Cites: the diagram's path (or
the source naming the journey list) and the journey's name — never a task ID. Evidence: "walk
transcript with each step's screen, route, API call and data before and after, plus the as-built
edges of its screens." Derivation: `check:verify-flow-as-built`. Tier 1: `locator`.

## Capture

For each journey in the slice:

1. **Derive the as-built edges first.** Before walking anything, read the code for the screens
   the journey names: its navigation calls (route pushes, link targets, redirects) and the API
   calls each screen makes. This is what the journey is actually wired to do, independent of
   what the design says it should do.
2. **Walk the journey end to end**, in one running instance (per the contract's exercise
   discipline — bring the system up once for the slice, do not restart between journeys or
   steps). At each step, record: the screen reached, the route taken, the API call made (if
   any), and — where a data store is named in Inputs and `verification.md` authorises reading
   it (O9) — the relevant data **before** the step and **after** it. Reading is the default;
   writing only where the data-permission column for that environment allows it, and never past
   what the journey itself requires.
3. **Write the transcript as text**, under `<evidenceDir>/verify-flow-as-built/`, one file per
   journey. Each row is a step: screen → route → API call → data before → data after. Below the
   steps, list the as-built edges derived in step 1, and call out any edge that is extra
   (wired but not in the design) or missing (in the design but not wired).
4. **Claim it with a locator copied verbatim from the transcript** — a literal string the
   transcript actually contains (a route, a screen name, an API path as written in the file),
   never a description of what the transcript ought to show. The tier-1 check is a literal
   substring match against the transcript's own bytes; a locator that paraphrases rather than
   quotes will fail that check even when the walk itself succeeded.
5. A journey whose walk cannot proceed — the environment cannot reach the first screen, the
   build fails on the way — is claimed with `artifact: null` (or the partial transcript) and a
   stated reason, same as any other capture that comes up short. Capture never edits source,
   rebuilds, or restarts to work around a broken step.
6. **Any script this Capture step needs** — walking the journey, extracting edges, reading
   data before and after — is written at run time under
   `<evidenceDir>/verify-flow-as-built/scratch/`, never into the source tree. This skill ships
   no such script; write the one the journeys in front of you need.

## Rubric

- `met` — every step reaches its designed target, in order, with the data change the journey
  specifies (where a data store applies).
- `not_met` — naming the first failing step, or a wrong/extra/missing edge against the design —
  handed to Debug as a gap.
- `not_met` with reason `not built: <screen>` — a designed screen the journey needs does not
  exist in the build at all. **Never `unbuilt`** for a check row: the criterion still resolves
  through the ordinary `not_met` path so the run keeps debugging every other journey rather than
  ending the loop over one absent screen.
- `not_verifiable` — the environment named for this journey is not one `verification.md`
  authorises, or nothing in the project's own docs gives a way to run it.

Any defect found while walking a journey that no criterion here covers — a broken link off the
journey's own path, a screen that errors on an unrelated input — is not silently dropped and is
not turned into a new criterion of its own. Add it to this file's `verdicts.json` entry under an
`uncovered` key, and record it separately:

```bash
node -e 'require("./.claude/lib/discovered").record(
  ".trd-state/<feature>", {
    kind: "bug",
    foundBy: "verify-flow-as-built",
    phase: <N>,
    summary: "one line, what it is",
    file: "path/to/file",
    evidence: "how you know"
  })'
```

Write one `verdicts.json` entry per journey criterion judged this run (page status, one-sentence
verdict, notes, and the `uncovered` list, if any); entries for journeys not judged this run are
kept, not deleted.

## Page

Written to `<pagesDir>/verify-flow-as-built/index.html`: light and dark, responsive at phone
width, images (if any) lazy-loaded. Any script the page assembly needs is written at run time
under `<evidenceDir>/verify-flow-as-built/scratch/`, never into the source tree.

- **Both diagrams, side by side**: the designed flow and the as-built flow, each screen-to-screen
  edge drawn. Use Mermaid when the design itself carries no diagramming notation of its own (the
  PRD's own diagram, when it has one, is redrawn as given). Call out the differences between the
  two — an edge present in one and not the other — rather than leaving the reader to spot them.
- **A wiring matrix**: journey × step, one cell per (journey, step) pair, each cell pass or fail,
  showing that step's before/after data where the journey has any.
- **Uncovered defects**: every entry recorded under a journey's `uncovered` key, listed plainly
  and not folded into the pass/fail matrix.
- Cross-cutting problems that recur across journeys are stated once, not once per journey.
- Each card carries its criterion ID (`FL-<journey slug>`) as its visible label, so an owner's
  comment can name it.
- A line under the title states the iteration and whether the loop is still running or has
  exited, and with which outcome.

## Safety

Only environments `.claude/rules/verification.md` authorises (O9); an environment it does not
list is not authorised, and a criterion needing it resolves `not_verifiable` rather than to a
guessed endpoint. Read-only unless that file's data-permission column grants writes for the
environment in use, and never more than the journey itself requires. Never write a credential
value into the transcript, the manifest, `verdicts.json`, the page, or any agent return — record
where a credential lives, never its value (O8). Do not spawn a copy of yourself (constitution:
same-type self-delegation is forbidden) — a large journey set is split across Exercise slices by
the orchestrator, not by this skill spawning its own copies.
