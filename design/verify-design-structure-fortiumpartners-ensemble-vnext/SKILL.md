---
name: verify-design-structure
description: >
  Checks that the components a design board names actually appear at that board's route in the
  running build. Walks React's fiber tree in Playwright, collects each rendered component's
  name, and compares it with the board's `components` in design-map.json. React and
  react-native-web only; on any other stack, and for a parts board, it runs no walk and reports
  "not verifiable here".
when_to_use: >
  The feature is built from a design made by /create-design (it has a design-map.json).
  Selected once per feature by the TRD's Verification Artifacts section, for every such design.
  Real-component boards on React or react-native-web are walked; a parts board, or a build on
  any other stack, gets its row reported "not verifiable here" rather than being left out, so
  the skipped check is visible in the report.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# verify-design-structure

## When it applies

A design made by `/create-design` has **real-component boards**: boards in `design-map.json`
whose `components` list names the product's own components. This check answers "are those
components rendered at the board's route," not "does it look right" (that is
`verify-design-comparison`) and not "does the journey work" (`verify-flow-as-built`). It works
on React and react-native-web; a Vue, Svelte, Angular, Flutter or native build is "not
verifiable here" (Rubric).

**It is never silent.** A design with only parts boards, or one built on a stack other than
React or react-native-web, still gets its rows (Criteria), each reported "not verifiable here"
with the reason. Skipping the walk is correct for those boards (AC-F12.5); leaving them out of
the report is not, because an absent row reads the same as a check that never ran.

## Inputs

| Input | Where it usually comes from | Required / optional | Default |
|---|---|---|---|
| Design map | `docs/ui/<slug>/design-map.json` | required | — |
| Boards in scope | boards whose status is `approved`, `building` or `shipped`, real-component boards (a non-empty `components` list) and parts boards (an empty one) alike | required | — |
| Build stack | the UI stack the build renders with (`.claude/rules/stack.md`, or the board's `platform`): React, react-native-web, or something else | required | — |
| Route per board | the board's `route` in `design-map.json` | required | — |
| Capture method and commands | how to open the route in a browser against the running build, with the exact command; a development build is preferred, since a production build minifies names | required | — |
| Namespace prefix | the prefix `/create-design` put on component names (`Ns.Name`), stripped before comparing | optional | everything up to and including the first `.` |

## Criteria

One row per **board in scope**, never per component. Which row a board gets:

- A **real board** (a non-empty `components` list) on React or react-native-web: the row in the
  table below, walked per Capture.
- A **parts board** (an empty `components` list): row `ST-<board id>`, statement "Board
  `<board id>` is a parts board: the structure check does not run", Tier 1 `locator`. It is not
  walked; the exerciser claims it with `artifact: null` and the reason "parts board: no
  components to walk; verify-design-comparison carries the weight", and the Judge resolves it
  `not_verifiable` (AC-F12.5).
- **Any board on a stack other than React or react-native-web**: its `ST-<board id>` row is
  not walked; claimed with `artifact: null` and the reason "stack is `<stack>`, not React or
  react-native-web", and resolved `not_verifiable`.
- **No board in scope** (for example every board is still `draft`): one row,
  `ST-<design slug>`, statement "Design `<design slug>` has no board the structure check can
  walk", claimed with `artifact: null` and a reason naming why (no board `approved`, `building`
  or `shipped`; and the stack, when it is not React or react-native-web), resolved
  `not_verifiable`. The check is never silent: a selected skill always leaves at least one row.

| Column | Value |
|---|---|
| ID | `ST-<board id>` (stable across runs, so a resumed run keeps its verdict) |
| Functional statement | "Route `<route>` renders the components board `<board id>` names" |
| Cites | `design-map.json` and the board id |
| Evidence that would prove it | the fiber-walk transcript for the route and a screenshot of the route, per Capture |
| Derivation | `check:verify-design-structure` |
| Tier 1 | `locator` — a component name copied verbatim from the walk transcript |
| Parts | blank |

## Capture

For each board in the slice (never narrow to a subset of your own slice). A parts board, a
board on a stack other than React or react-native-web, and the `ST-<design slug>` row are not
walked: claim each with `artifact: null` and the reason Criteria gives, and skip the steps
below for it.

1. **Open the route** in Playwright against the running build, using the capture command given.
   Playwright resolves from the product first, then the global install; if neither is found,
   report that and stop (Rubric).
2. **Walk the fiber tree.** From the page's DOM, find host nodes carrying a `__reactFiber$*`
   key, follow each fiber up through its parents, and collect each component's `displayName` or
   function name. Write the sorted, de-duplicated names to the transcript.
3. **Compare** with the board's `components` after removing the namespace prefix from each. List
   each board component as found or missing, and note how many collected names are one or two
   characters long.
4. **Write the transcript as text** to `<evidenceDir>/verify-design-structure/<board id>.txt`
   and take a screenshot of the route to `<evidenceDir>/verify-design-structure/<board id>.png`
   (the contract's screenshot rule for any criterion that names a screen).
5. **Claim it with a locator copied verbatim from the transcript**: a component name the
   transcript contains. A route that cannot be reached is claimed with `artifact: null` and a
   stated reason.
6. **Any script this step needs** is written at run time under
   `<evidenceDir>/verify-design-structure/scratch/`, never into the source tree. This skill
   ships no such script.

**Capture only: no source edits, rebuilds or restarts.** A repair belongs to Debug, after the
Judge. **Never spawn a copy of yourself** (constitution: same-type self-delegation is
forbidden); a slice too large for one instance is reported, not delegated around.

## Rubric

- `met` — every component the board names was found at the route.
- `not_met` — naming each missing component; handed to Debug as a gap.
- `not_met` with reason `not built: <route>` — the route does not exist in the build.
- `not_verifiable` ("not verifiable here") — any of: the board is a parts board (an empty
  `components` list; the design comparison carries the weight); no board is in scope (the
  `ST-<design slug>` row); the stack is not React or
  react-native-web; no `__reactFiber$*` key is present on host nodes; Playwright is not
  installed; the names are minified (no board component found and most collected names one or
  two characters long), in which case the reason names minification and not a missing component;
  or the environment is not one `verification.md` authorises.

Write one `verdicts.json` entry per board judged this run (page status, one-sentence verdict,
notes); entries for boards not judged this run are kept.

## Page

Written to `<pagesDir>/verify-design-structure/index.html`: light and dark, responsive at phone
width. One card per row, labelled with its criterion ID (`ST-<board id>`, or `ST-<design slug>`),
showing the route, a found/missing table for the board's components, and the screenshot. Rows
judged `not_verifiable` (parts boards, a non-React stack) show the reason in place of the table. A line under the title states the iteration and whether the
loop is still running or has exited, and with which outcome.

## Safety

Only environments `.claude/rules/verification.md` authorises; an unlisted environment resolves
`not_verifiable`, never a guessed endpoint. Read-only: opening a route is the whole exercise.
Never write a credential value into the transcript, `verdicts.json`, the page or any return;
record where a credential lives, never its value. Do not spawn a copy of yourself.
