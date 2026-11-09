---
name: progressive-enhancement
description: Use when a page must paint before its JavaScript runs.
version: 1.0.0
author: TimeLine
license: MIT
platforms: [macos]
metadata:
    hermes:
        tags: [astro, solid, hydration, no-js, audit, cdp]
---

# Progressive Enhancement

The site is a static archive behind a service worker, so a reader with a cold cache, a blocked
script or a browser that never runs one must still see the archive. Every surface therefore has two
jobs: paint itself from the build, then hydrate for interaction. A surface that renders its content
only after hydration has one job, and it is the wrong one.

The rule is one sentence: the first paint is the server's, and JavaScript only makes it interactive.

## The first paint is the server's

A page reads its content at build time from the content collections and renders it into HTML. That
is what the service worker caches and what a script-free reader sees.

- **Props carry the data; the island never fetches it.** `Source/pages/Workspace/index.astro` reads
  the collections and hands `Stages`, `Columns` and `Tiles` to the islands as plain objects. What a
  person is doing right now - which stage is selected, which record is open, which tiles were
  published - lives in `Source/Script/Workspace/Store.ts`, which every island on the page reads. An
  island that fetched its own content would render an empty frame first.
- **`client:visible` over `client:load`.** A `client:load` island competes with the first paint for
  the main thread; `client:visible` lets the canvas paint and boots when the island is on screen.
  The workspace fills the viewport, so it hydrates immediately in practice - the directive only
  changes who wins the first frame.
- **`client:only` never sits on a content surface.** It renders nothing at build time, so the page
  ships an empty box and a script fills it. The audit fails on it outright.
- **One visible `<h1>` per page, on every surface.** It is the page's own name and the only heading
  a screen reader can outline the document from, so it is the server's to draw. The workspace's is
  the drawer's title (`My Files`): the composition draws no heading above the frame, and the title
  keeps its 13px semibold face because the level is the document's, not a type step.
- **Interaction may be absent without scripts.** A button that does nothing is acceptable; a row, a
  tile or a heading that is missing is not. That distinction is the whole scope of this skill.

## A visible island needs a rendered frame

`client:visible` observes the island's children with an `IntersectionObserver`, and the observation
only delivers while the page is being rendered. Two conditions break it, both of which look like a
broken component rather than a broken environment:

- **A background tab is never rendered.** A target created with `background: true` - the polite way
  to open a tab in someone's own browser - receives no rendering updates, so the observer stays
  silent and the island never hydrates. Bring the tab to the front (`Page.bringToFront`) before
  measuring for this reason. A real reader's tab is in front, so this is an audit-environment rule,
  not a product defect.
- **An observer target with no box never intersects.** Astro styles `astro-island` as
  `display: contents`, which is why the directive observes children rather than the island itself. A
  child that is itself `display: contents`, `display: none` or zero-height keeps the island dormant.

A `client:visible` island that stays static is diagnosed by reading the `ssr` attribute: the runtime
removes it on hydration, so `document.querySelector("astro-island[ssr]")` still matching means the
directive never fired. Report that as `js=static` and say the parity comparison measured two static
renders - a parity that holds between two static pages proves nothing about hydration.

## The audit

It is two passes over every built route, and it is run by hand: launch a headless browser on a
throwaway profile, point it at a copy of `Target/` served on loopback, and load each route twice
over CDP - once with `Emulation.setScriptExecutionDisabled`, once normally.

- **The script-free pass is the measurement.** `Runtime.evaluate` still answers while page script
  execution is disabled - the switch stops the document's own scripts, not the debugger's - so the
  pass reports what the first paint actually shows, with layout. "Visible" is a layout fact: a node
  inside `display: none` or a zero-height wrapper is present in the markup and absent from the page.
- **Parity is the rule that catches the defect.** For every selector a route profile names, the
  script-free render must show at least as much as the hydrated one. Content that appears only in
  the second pass fails with `content waits for hydration`.
- **The read is a snapshot, not the build directory.** `astro build` empties `Target/` before it
  writes, so a run that starts mid-build sees an empty tree and reports every route as serving no
  document - a total failure that looks exactly like the defect this exists to catch. The audit
  waits for the newest mtime under `Target/` to be older than 1.5s, copies the tree aside, checks
  that every copied document is complete and that the route set matches the live one, and serves the
  copy. A build that starts after the copy cannot take the pages away from the browser.
- **Every route gets the generic contract, profile or not.** A non-empty `<title>`, at least 40
  characters of prose under `<main>`, exactly one visible `<h1>`, no island unless the profile
  allows one, no `client:only` island, and server-rendered content inside every island. A route with
  no profile is reported as `generic`, so a new page cannot pass by being unknown.
- **A failing route is named, never dropped.** Write the report as one line per route, pass or fail.
  A route missing from the report is indistinguishable from a route that passed, and the second is
  the claim the audit exists to make.

The browser binary is configuration, never a constant: the first installed candidate will do -
Chrome, Chromium, Brave, a Playwright cache - so a clone on another machine needs no edit.

## One store, two islands

A page that draws a rail and a body mounts two islands, and both read
`Source/Script/Workspace/Store.ts`. A signal inside each component would make them two workspaces
that happen to look alike: press a band in the rail and the seam beside it would still name the old
stage, and neither would be wrong about a value the other never had.

- **State lives in the store; data arrives as props.** The store owns the selected stage, the live
  column, the view, the open record, the published tile set and the session slot. The stages, the
  columns and the tiles stay with the page, which derives them at build time; a second copy in the
  store would be a second source of truth.
- **`Adopt` is what makes one store safe to mount twice.** The first island to render seeds a field
  and a later island fills only what is still empty, so the order two islands hydrate in cannot
  change what is on screen - and hydration never resets a server-rendered view to empty.
- **One instance per page, one per render on the server.** The module is evaluated once in the
  browser, so every island that imports it reads the same value. A build renders every route in one
  process, so `store()` hands each render its own instance; a singleton there would carry one page's
  selection into the next page's HTML.
- **A session read happens on mount, never during render.** The server's HTML and the first client
  render are then the same anonymous slot, so hydration has nothing to disagree with. A failed read
  keeps that slot, and the session layer states the failure once.

The check for this is three passes of the built workspace page, each in its own tab - anonymous, a
session element that is not JSON, and a readable session - read per pass:

- two islands on the page, both hydrated (a pass that never hydrates reports it instead of measuring
  a static render);
- a press on a rail band that moves the seam beside it, which is the cross-island proof: the rail
  island dispatches and the body island renders, so a store that is not shared leaves the seam
  naming the stage it opened on;
- a seam that is `locked` and names no stage while there is no identity, and offers the verb once
  the session names one;
- exactly one warning for a session element that cannot be read, and none for a page that embeds
  none;
- a publish that lands one more filled tile once an identity exists - skipped, not failed, when the
  archive holds no drawer rows, because a fresh clone is a normal state.

The session element is spliced into the served HTML rather than injected in the browser: it has to
be in the document before any island script runs, or the read races hydration. The press check is
falsifiable by construction - it requires the seam to name a stage it did not name before the press.

## Adding a route

A new page is audited the moment it builds, and its expectations are written down before the page is
read: the route, how many islands it may mount, a minimum visible count per selector it must show,
and any group of alternatives where one has to hold.

The workspace's profile is the shape: two islands; at least one `.rail`, one `.drawer` and four
`section.drawer-column`; and, as the one alternative, at least one `main ol` or one `main p`. The
alternative is how an empty archive passes: the page shows rows when there is content and a note
when there is none, and both are complete first paints. The island count caps hydration boundaries
and defaults to none, so a page that grows an island without a reason fails. A dynamic route names
its variable segment with `:`, so `/Bookmark/:Id/` covers every built post.

A profile names what the design promises, never the markup a page happens to use:

- **Elements with a meaning** - `main section`, `main ol`, `main article`, `main a[href]`.
- **The parts the composition makes contractual** - `.rail`, `.drawer`, `.drawer-column`,
  `.swimlane`, `.spectrometer__cell`, `.status__value`, `.security__mark`, `.provenance__band`.
  These are the names `Documentation/Reference/Design-Composition.md` gives its own parts.
- **The empty state a page renders when the archive holds nothing** - `.drawer__empty`.

**A selector is a claim about the DOM, never about the source.** The audit runs
`document.querySelector` inside the page, so it is immune to the minifier - but it is not immune to
a redesign, and the two look the same when a route fails. A profile pinned to `.roster__row` or
`article.sheet` fails the day the surface is redrawn, and a redraw is not a no-script regression:
when six of nine routes fail while each still renders its text with zero islands, the content
contract held and the selector profile went stale. Assert what the design guarantees, and let a
per-route profile name only classes the composition spec makes contractual. A grep over `Target/` is
the weaker check in both directions: `@playform/compress` strips attribute quotes, so `class="foo"`
matches nothing on a page full of `class=foo`. The heading is the clearest case: the rules name
`h1`, never `h1.board__title`, because the class belongs to the component that draws the page while
"one visible heading" is the contract a screen reader depends on.

Expectations are structural selectors, not counts of records: a count that depends on the archive
would make the audit fail on a fresh clone, which is a normal state.

## Proving the audit bites

An audit that cannot fail is decoration. Build two pages that satisfy the structural rules and break
them at render time - one draws a rail band from a script and carries an island with no
server-rendered content, the other has lost its heading and its prose - and require the audit to
fail on both before trusting a clean run.

Both fixtures must fail, and on the rules they were built to break: hydration parity, an empty
island and a lost heading. A fixture that passes means a rule stopped catching the defect it exists
for, and the fixture's report is where the gap shows. Build the fixtures from the current rules
rather than keeping them beside them: a fixture archived next to the rules drifts the moment a rule
changes, and then the control tests the fixture instead of the audit. Run the negative control after
changing the rules.

A build that is still writing is not a verdict: the audit waits for the tree to settle and then
measures a copy, so a run that overlaps `astro build` reports what the finished build renders. A
page that genuinely lost its content fails the generic contract - the `<main>` text floor and the
one-visible-heading rule - before any profile is consulted, so the two failures cannot be confused
for one another.

## Claim → test

| Claim                                        | Test                                                                                                                 |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Every built route renders without scripts    | the two-pass audit reports one `PASS` line per route                                                                 |
| The workspace island hydrates                | the audit's `/Workspace/` line ends in `js=hydrated`                                                                 |
| A route's content is not hydration-only      | the route line carries no `content waits for hydration` failure                                                      |
| Every route shows one visible heading        | every `PASS` line carries `h1=1`                                                                                     |
| A route mounts an island only where expected | the `/Workspace/` line carries `islands=2` and every other route `islands=0`, except the post's `islands=1`          |
| The audit catches the defect it exists for   | both negative-control fixtures fail on hydration parity, an empty island and a lost heading                          |
| The audit reads a settled build              | run `pnpm run build` in the background and audit while it runs: one `PASS` line per route                            |
| The island boots after the canvas paints     | the built HTML carries `<astro-island ... client=visible>`; `grep -c 'client=load' Target/Workspace/index.html` is 0 |
| Two islands read one store                   | the readable-session pass reports the pressed stage in the seam                                                      |
| A failed session read is one warning         | the audit's malformed pass reports exactly one warning and `state=static`                                            |
| An empty session slot hydrates cleanly       | the audit's anonymous pass reports no error, `state=static` and a `locked` seam                                      |
