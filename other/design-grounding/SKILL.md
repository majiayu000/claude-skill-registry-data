---
name: design-grounding
description: >
  How a read-only agent inventories an existing product before anything is drawn: its screens,
  components, flows and data, per stack, and how to capture a screenshot that is missing.
  Writes the `grounding/` files the design workflow reads.
when_to_use: >
  A grounding agent in `/create-design` or `/design-system` needs to describe what the product
  already has. Not for drawing boards (see `designing-on-canvas`).
allowed-tools: Read, Write, Glob, Grep, Bash
---

# design-grounding

## When it applies

A design is being made for a product that already has code. Ground it in what exists: read
only, no product edits. Environments and test credentials are in `.claude/rules/verification.md`
sections 1 and 3, and the route list and capture command are in `.claude/rules/design.md`.

## Inventory

Find each by reading code, not by guessing from names.

- **screens**: one row per reachable screen and state, with route and screenshot path.
  React Router: route table (`createBrowserRouter`, `<Route path>`). Next: `app/**/page.*` or
  `pages/**`. React Native: navigator screens (`Stack.Screen`, `Tab.Screen`, expo-router
  `app/`). Flutter: `MaterialApp` routes, `GoRoute`, `Navigator.push`. Server-rendered
  (Rails, Phoenix, Laravel): routes file plus its templates.
- **components**: each component's props and where it is used. React/React Native: exported
  components and their prop types; Flutter: widget constructors; templates: partials and their
  locals. Record the library path so boards can `x-import` it.
- **flows**: how screens connect, from navigation calls, links and redirects; name each flow
  by the user goal.
- **data**: the fields the backend actually returns for each screen, from the API handler,
  serializer or schema, not from the types the client wishes it had.

## Capture

Capture every in-scope screen fresh, at each viewport `design.md` lists, with the capture
command in `design.md`, and write it to the screenshots path named there, replacing any earlier
file. A stored screenshot may predate the code or have been captured wrong, and the as-is board
is judged against it. Browser capture steps are in the `playwright-automation` skill; the
capture and state-reaching approach is in `verify-design-comparison/SKILL.md`'s Capture
section. Do not restate either.

The viewport must be the page's real layout width, not a window size:

- Set it in the browser context, for example Playwright's `viewport: { width, height }`, or
  device emulation. Do not use headless Chrome's `--window-size` flag. Below about 500 px it
  lays the page out wider than asked and crops the image, so a 390 px capture of a centred
  column comes out shifted right and clipped.
- Before saving, read `window.innerWidth` in the page. If it is not the viewport width, the
  capture is wrong: fix the method and capture again; do not keep the image.

A right width is not enough: after saving, look at the image. One that shows anything the page
does not render is a capture error too: a repeated nav or card (a second copy of the top of the
page further down), a blank or black band, content cut off or shifted. The source decides what
the page renders; a screenshot that disagrees with it is wrong, not the board. Capture it again
in a fresh browser context (a new context and page, wait for the network to go idle, then
screenshot the viewport) and look again. If the recapture is still wrong, delete the file: never
keep it, and never commit it. Record the screen's screenshot as unavailable in `screens.md`
with the reason ("capture error: <what the image showed>"). A note that a screenshot is "worth
recapturing" is never the outcome: recapture it.

If the screen cannot be reached (environment not listed in `verification.md`, credentials
unavailable), keep any earlier screenshot only if you say how old it is, otherwise record
`screenshot_match: false` and the reason rather than inventing an image.

## Output

Write under `grounding/`: `screens.md`, `components.md`, `flows.md`, `data.md` and
`standards.md` (the design rules from `design.md` that apply). Cite the file and line for each
claim; mark anything unread as unknown.
