---
name: plan-backlog
description: Turn a product's context and PRD into a backlog — epics, stories as vertical slices, consolidated, prioritised and grouped into waves that never touch the same files. Use when the user says "armá el backlog", "generá las historias", "stories", "épicas", "consolidá el backlog", "priorizá", "planificá las waves", "backlog", when project-new reaches gate 5, or after a new feature intake. Also re-plans an existing backlog without renumbering finished stories.
---

# Backlog — epics, stories, waves

Inputs: `docs/context/*`, `docs/prd.md`, and the code if it exists. Output: `backlog/epics.md`
and `backlog/stories/<ID>-<slug>.md` in the format of `backlog/README.md`. Status is never
written: a story is done when a commit on `main` carries the trailer `Story: <ID>`.

## 1. Epics

3–7 epics that map to the PRD's in-scope capabilities, each with: id (short uppercase word,
e.g. `AUTH`), goal in one sentence, the PRD line it serves, and what is explicitly outside it.
Anything in the PRD's "out" list never becomes a story.

## 2. Stories

- **Vertical slices**: each story delivers something a user or operator can observe end to end
  (API + UI + test), sized to one focused session. Split anything bigger; merge anything that
  can't be observed alone.
- Id `EPIC-NNN`, never reused. File name `<ID>-<slug>.md`.
- Front matter (`+++` TOML): `id`, `epic`, `title`, `wave`, `depends_on`, `touches` (the paths
  it will change — directories are fine), `dimensions` (what it can break, from
  `${CLAUDE_PLUGIN_ROOT}/references/dimensions.md`: a screen implies at least `ux`, `ui`, `i18n`,
  `a11y`; an endpoint implies `api`, `contract`, `auth`), and `invariants` (the `INV-nnn` from
  `docs/context/domain.md` the story must keep; listing any means declaring `integrity`, and
  touching a critical area from `.keelokit/critical.toml` means both). No `status`. Optional
  `origin` when the story comes from somewhere other than the first plan:
  `"bugbash:<date> <finding id>"` or `"feature:<date>"` (a later feature intake).
- Body sections, in order:
  1. **Context** — why, with references to `docs/context` / PRD sections, and a
     **Does NOT do** list.
  2. **User story** — As a <user>, I want <capability>, so that <outcome>.
  3. **Acceptance criteria** — Gherkin, one `Scenario: [S1] …` per behaviour (ids are how tests
     trace back: `AUTH-003.S1`). Cover, per declared dimension, the uncomfortable cases: empty,
     error, loading, no permission, another role, expired session, other locale, 320 px, twice in
     a row, two at once. The invariants go in the front matter, not as scenarios: each one gets
     the test its class calls for (`${CLAUDE_PLUGIN_ROOT}/references/invariants.md`).
  4. **Testable units** — table: unit · test type (unit / integration / e2e) · file.
  5. **Definition of done** — `pnpm verify` green, every scenario covered by a test titled with
     its id, `Story: <ID>` trailer on the completing commit, addendum if the result differs.
- A story that needs an unknown fact gets the `[GAP-nnn]` reference and depends on answering it
  (record the gap in `docs/context/gaps.md`); never fill the hole with a guess.

## 3. Consolidate (always, and when re-planning)

- Merge duplicates and overlapping stories; keep the lower id.
- Stories already done (`Story:` trailer on main) are never edited, renumbered or deleted;
  changes to done work become new stories.
- Every PRD in-scope line is covered by at least one story; every story traces to one.

## 4. Prioritise and wave

1. Order: what unblocks the most first (foundations, then the core user journey), then PRD
   priority, then risk (unknowns early).
2. Waves: a story goes in the earliest wave where all `depends_on` are in earlier waves **and**
   its `touches` don't overlap any other story in the same wave (same file, or one path inside
   another) **and** it shares no critical area with another story of the wave. Overlap → next
   wave; `python3 .keelokit/bin/doctor.py` fails on both. This is what lets several agents build in parallel
   safely, and what keeps critical work (money, notices, limits, orchestrators) one story at a
   time.
3. Critical areas: when the plan creates code where a bug moves money, repeats a side effect,
   breaks a limit or leaks data, propose an area for `.keelokit/critical.toml` (name, why,
   paths) to the user, and point its stories at it. Shared orchestrators that many stories call
   are good candidates: serialising them is cheap, a collision in them is not.
4. Write `backlog/epics.md`: the epics table, then one table per wave
   (`Story · Title · Depends on · Touches`), then a short "collisions resolved" note for stories
   moved to a later wave because of overlap.

## 5. Check

Run `python3 .keelokit/bin/doctor.py` and fix every backlog error (ids, file names, unknown
dependencies, stray `status`). Refresh the dashboard (`/keelokit:project-dashboard`): it shows the
stories by wave and by epic. Then show the user in the chat: epics, stories per wave, the first
ready stories, and any story blocked by a gap — and ask them to approve the order. Talking to the
user in Spanish, waves are **olas de desarrollo**; say once what one is (stories that don't touch
the same files, so they can be built at the same time).
