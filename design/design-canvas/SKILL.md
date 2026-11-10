---
name: design-canvas
description: "Design it on the canvas / design the page: Claude Design canvas route, design system, render-and-look."
description-budget: 135
version: 1.0.0
triggers:
  - design it on the canvas
  - design the page
  - design canvas
  - canvas redesign
---

# Design canvas

**Size the design work, not the t-shirt.** A large design ask goes to the Claude Design canvas:
produce or iterate a canvas through the Artifact tool's Design type, then review it. Large means a
redesign, a new screen, several layouts to compare, or a design-system record, at any t-shirt. A small
ask (a `staff-ux` flow review inside a plan, a spot check, one component's tweak) stays with the
reviewer agent. A human designer is a PM-gated exception, named as one (brand sign-off). Offering the
PM a "hand it to the designer yourself" fork for a large ask is the defect. Tripwire:
`A-LARGE-DESIGN-ASK-GOES-TO-THE-CANVAS`.

**The bar is a designed canvas, not an artifact.** A ~30-page methodology canvas built from the plain
Artifact type, with no design system and prose in cards, was rejected: "that's an artifact, not a
design canvas." Layout, UI/UX and visuals are the deliverable.

## The repo holds the design; the link is a view

**A link belongs to the login that published it**, and other logins reach it only if its owner shared
it. After a login swap it is out of reach though it still exists, so the repo is the source.

1. **Write the source into the repo first**, under `docs/design/<slug>/project/`, committed in the step
   that produces it. Its `README.md` says the files are canonical, carries steps 2 and 3 as the republish
   recipe, and records the URL as "current published view, <date>, owned by <login>".
2. **Start the canvas:** Artifact `action: "quickstart"`, `intent: "design"` returns the Design type's
   `type_url`; resolve it every time. Publish with that `type_url`, a `title`, no files and
   `auto_open: "after_first_write"`. Attach the repo's design system (§ Design systems) and read every
   page the create result names before writing a board.
3. **Fill it** per the create result, publishing `project/` with `root` set to the design folder.
4. **A link out of reach** (other login, deleted) is republished from the files under the current login.
   Never cite a link as the source of a value.

## The designed-board bar

Each board is a composed screen, not a text page:

- **Layout:** one idea per board, a deliberate grid, the system's tokens for color, type and spacing.
- **Diagrams, charts, stat tiles** carry the claims; prose is cut to captions.
- **Interaction:** real navigation and states across boards, not static cards.
- A board that reads as a document in cards is the defect.

## Design systems

**A repo with a design system keeps it published as a Design System artifact, so a canvas can attach
it.** Build it from the token CSS and token record at `HEAD`, never from memory or an older artifact.
Publishing is private and EM-autonomous; sharing is the gated act. Republish when the token files change
or the link is out of reach, recording the URL in the design-system README as above. Tripwire:
`A-DESIGN-SYSTEM-ARTIFACT-IS-A-VIEW-REPUBLISHED-FROM-THE-REPO`.

Quickstart lists the design systems the account can open; with no default, ask the PM which to attach.
The repo's design-system record names its tokens and points at the CSS that declares their values,
never copying them; a test checks each named token is still declared there.

## Render and look

**The Design type discourages visual verification; do it anyway.** Open `project/*.html` locally in a
browser or take a Playwright screenshot, at several widths, and Read the images. A review that rendered
nothing says so.

**A design-fidelity verify reads the external original**, or records the verify BLOCKED with the
unreachable-original reason. A harvested record or local render is never its proxy. Tripwire:
`A-DESIGN-VERIFY-READS-THE-EXTERNAL-ORIGINAL`.

## Review

- **Reviewers read the committed source**, never the link: `staff-ux` for flow, `senior-front-end` for
  design-system adherence. Neither holds the Artifact tool; the EM applies findings, commits, republishes.
- **People's canvas comments** are harvested, never skimmed: § Harvest. Claude replies or resolves only
  on a thread a person sent to Claude, and cannot open one.

## Harvest before anything executes on it

**A canvas is pulled down to a local record before a plan, brief or dispatch executes on it.** The
record is the source for execution; the link is never read. Token:
`A-CANVAS-IS-HARVESTED-BEFORE-ANYTHING-EXECUTES-ON-IT`. Layout, fields, reason codes and rationale:
`coordinator/docs/wiki/schema-and-validation-contracts/canvas-harvest-record.md`.

1. **When:** a canvas is approved, or a plan, brief or dispatch is about to cite it.
2. **How:** only the canvas's own `project/**` files are required and copied; the type's runtime files
   carry no design. The EM hand-reads nothing. Fire the one reader agent `canvas-harvest reader-dispatch
   --url <artifact url>` emits (it lists, reads `project/**` once, pages every comment), then at once, in
   the same sitting (saved frame files do not last), run `canvas-harvest harvest --url <artifact url>
   --out docs/design/<slug>/harvest --reader --transcript <reader agent transcript>`, resolved per
   `snippets/resolve-coordinator-bin.md`. The op lifts frames and threads to disk; the EM retypes none.
3. **Settle:** fill `harvest/SETTLED.md`, one `[thread:<id>]` item per decision (`[no-threads]` for a
   canvas with none), and commit the record in the same step. Thread files carry commenters' names and
   words verbatim, so a repo whose `docs/design/` is published keeps the record out of the published set.
4. **Cite:** a plan or brief names the record's `harvest/harvest.json` path. Execution reads the record,
   never the link. At execute entry, re-read the canvas and run `canvas-harvest probe`; drift means
   re-harvest and update `SETTLED.md`.
5. **Out of reach:** a canvas owned by the other login (`other-account`) whose committed record is complete
   is admitted with drift unchecked; the dispatch warning names the login to swap back to for a re-probe.
   Any other unreadable canvas is refused with its reason. Republish from the committed files under the
   current login, or cite the committed source without the URL.
6. **Register:** add or update the board's entry in the repo's design registry (`docs/design/registry.yaml`,
   or the repo's `design_registry_path`), with `sources` covering the page and the component dirs it renders.
   A plan touching those files then cites the record or a ratified deviation. Contract:
   `coordinator/docs/wiki/schema-and-validation-contracts/design-registry.md`; token `A-REGISTERED-DESIGN-IS-CITED-NEVER-RE-DERIVED`.

## Boundaries

- **`DesignSync` is not the canvas**: it syncs a local component library to a claude.ai design-system project.
- **The canvas needs an authenticated claude.ai session.** Without one, say so; never substitute a
  designer hand-off. A canvas already cited is not skipped: § Harvest.

## Worked examples (example-stats-repo)

- `docs/design/advanced-stats-canvas/` in example-stats-repo: a redesign canvas whose README carries the
  republish recipe; its `harvest/` holds the frames, the verbatim threads and `SETTLED.md` a plan cites.
- `design-system/cockpit/`: its `tokens.json` copies values and has drifted from Cockpit's `globals.css`,
  the failure the record rule above exists for.
