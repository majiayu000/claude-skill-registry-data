---
name: design-verification
description: Use when a built page must be proven to match a design, not merely to compile.
version: 1.0.0
author: TimeLine
license: MIT
platforms: [macos]
metadata:
    hermes:
        tags: [design, verification, cdp, geometry, figma, scss]
---

# Design Verification

A green `astro build` proves a page compiled. It does not prove the composition is the composition.
This skill is the check between those two facts: serve the build, drive it in a real browser, and
compare the measured geometry against numbers that were read from the design file.

The authority is `Documentation/Reference/Design-Composition.md`. The check is the manual one
described below: serve a snapshot of the build, read the route in a real browser, and compare the
measured boxes against the numbers the spec states. It is ad-hoc verification, not a test suite, and
a run that cannot read a number says so rather than passing.

## When to use

- A component was built or restyled against a design and the result must be proven, not eyeballed.
- A layout "looks wrong" and the stylesheet looks right - which is the signature of a rule that
  never reached the page.
- A design reference was inferred from a screenshot and has to be replaced with measured values.

## The two facts a screenshot cannot give you

**A stylesheet that is not imported does nothing.** `.workspace` rendering as `display: block` with
a correct `display: flex` rule in a correct `.scss` file means the sheet was never imported by the
component. The build succeeds, the class names match, and the layout is a column. Check the import
before checking the rule.

**A probe reads a cached page.** Chromium keeps the document across a rebuild, so a probe run after
a build can report the previous geometry with no error. Cache-bust the URL (`?v=$(date +%s)`) or the
result describes the page that used to exist.

## Running it

The check is four steps in this order, and the order is what makes the readings trustworthy.

**Snapshot the build.** `astro build` empties the output directory before it writes, so a probe that
serves the live tree while another agent's build runs sees zero routes and reports each as "the
route served no document" - a total failure that is in the observer, not the page. Copy `Target/`
aside once the newest mtime under it has been quiet for 1.5s, re-read that mtime after the copy, and
throw the copy away and wait again if the tree moved; a tree still being written after 180s is a
blocker rather than a snapshot of whatever was on disk. What the snapshot guarantees is narrower
than coordination with the builder: it is a quiet-time heuristic, so a build that starts in the
instant between the quiet check and the copy is still possible - the re-read is what catches it, and
the run retries or blocks rather than measuring a half-written tree.

**Serve the copy, not the live tree.** Serve the snapshot on loopback (`PORT`, default `4411`) and
point the browser at that origin, or probe a server that is already running instead.

**Probe `/Workspace/`.** With a Chromium on `CDP_URL` (default `http://127.0.0.1:9222`), open the
route, cache-bust it (`?v=$(date +%s)`), and read the box of every part an invariant names -
`getBoundingClientRect` per part is enough. The cache-bust is not optional: Chromium keeps the
document across a rebuild, so a probe run after a build can report the previous geometry with no
error.

**Read one line per invariant.** A measurement that does not match the number below is a failure. A
selector that no longer matches anything is reported as `ABSENT` with the selector named, never as a
pass - a deleted component is a page defect, and filing it in the precondition class is filing it
where the reader is told not to look. A missing precondition is the only thing that is not the
page's fault: no build, no browser, or a route that served no document is stated as such, with the
step that fixes it.

## The invariants

The frame, in the page's own coordinates: the rail is `224 × 360` and level with the drawer; the
drawer starts at `240` (the rail plus the ground showing through); the seam is `40` tall directly
under it; the canvas is `900` tall directly under that. The drum draws thirteen bands and its ladder
reads `8, 10, 12, 16, 22, 28, 44, 28, 22, 16, 12, 10, 8` from edge to centre and back.

The composition then grows downward. Three bands follow the canvas on its own 20px rhythm, in the
order a reader meets them - the swimlanes, the spectrometer, the status footer - and the rail's
security cluster is bottom-aligned in the rail column, so its last mark sits on the footer's
baseline. The lane air is measured against the canvas's own gap rather than against a literal, so
the invariant survives a change to either. The footer's four values are asserted as words, because a
status band that reports itself only in colour is the failure RFC-0048 exists to prevent.

Those are the numbers that a screenshot cannot distinguish and a stylesheet can silently lose.

The seam is also measured for its state, because `/Workspace` is public and the build's own state is
the anonymous one (RFC-0054): the publish control must read `locked` with `aria-disabled="true"`,
and its note must state the reason a drop cannot cross - a published record carries an author. A
page whose seam silently offered the verb would pass every geometric invariant and still be wrong,
which is why the state is asserted beside the frame.

## The showcase pages

Five pages that are not the workspace are the showcase surfaces (RFC-0053), and they are the same
check at another width. Serve the same snapshot, probe `/`, `/Bookmark`, `/List`, `/Voted` and
`/Activity` at 1440 wide, and read what a showcase page can be wrong about: the rail is 224 wide,
sits at the page's left edge and stays in view while the page is read; the hero takes the one extra
type step (48px); the page holds three boxes, each bleeding to the page's own edge with the tile's
24px corner on the side that is still inside the page, in the canvas's own three greys; the rail is
a table of contents whose every band resolves to a section that exists; and no record is drawn at
all - no canvas, no drawer, no seam.

The last one is the point of the whole check. A showcase page that grew a tile would still look
right, and would have become a data surface - the state RFC-0053 exists to keep it out of.

**`/Showcase` is the sixth page that is not the workspace, and it is probed for its own claim.** It
demonstrates the layout primitive with six dispersed boxes rather than three, so the three-box,
three-grey invariants describe a surface it is not. Probe it the same way and read what the spread
claims: consecutive boxes sit at different horizontal offsets, the vertical gap exceeds the canvas's
own 20px rhythm, and the page ends on a three-column pillar band. A spread whose boxes lined up
would still pass a "no record is drawn" check and would have lost the only thing it demonstrates.

The route inventory is the tree's own: `find Target -name index.html` lists every page the build
emitted, and a route that appears there and in none of the three probes is unverified rather than
passing. A count written into this file is a claim about the route set and goes stale the moment a
page is added.

## Extending it

An invariant is one line in the list above: a label, the box it reads, and either a literal or a
relationship to another measurement on the same page. Add a measurement to the probe when an
invariant needs something the page does not already expose - the band heights were added that way,
after a reading came back empty and was reported as a failure the page had not committed.

A new invariant must be a fact from the design file. An invariant invented from the implementation
proves the implementation agrees with itself.

## Claim → test

| Claim                                   | Test                                                                                                |
| --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| The workspace matches the frame         | the probe's readings match every number above, one line per invariant                               |
| An absent element fails, and is named   | delete `class=bento` from a copy of the build: the report reads `ABSENT  .bento is not in the page` |
| A snapshot refuses an unsettled tree    | probe a tree that never stops being written: the copy is refused and nothing is served              |
| A probe reads a settled build           | probe while `pnpm run build` runs: the frame reads, not "served no document"                        |
| Every emitted route is probed           | `find Target -name index.html` lists only routes one of the three probes covers                     |
| The seam states its state, not a title  | the workspace probe reads `locked/true` and the reason, not a record name                           |
| No record is drawn on a showcase page   | the showcase probe finds no canvas, drawer or seam on any of the five routes                        |
| A missing precondition is not a failure | with no browser on `CDP_URL`, the report names the browser as missing, not the page                 |
