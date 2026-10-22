---
name: feature-design
description: >-
  Decides how to build an Umbraco feature: extension points, data model, Management API
  surface and frontend components, written to ARCHITECTURE.md, SPEC.md and mockups. Use once
  feature-explore has defined the problem, or on its own to capture a mockup starter for a
  product screen.
user-invocable: true
argument-hint: [area to focus, optional]
---

# feature-design

> 🎯 **Design for change.** Every decision here is judged by one question: when this
> changes, how big is the diff? Pick the Umbraco extension points, seams, and data shapes
> that make the *next* change small and local — not the ones that are merely first to mind.

Decide *how* to build what `feature-explore` defined. Output: which parts of Umbraco you're
extending, the data model (if any), the Management API surface (if any), and the frontend
component shape (if any).

## Where this writes

The same per-feature plan folder `feature-explore` started. Owns two files, plus a `mockups/`
folder when the feature has a UI:

- **`ARCHITECTURE.md`** — the internal structural decisions: which extension point(s), the
  data model, key decisions with their rationale and the rejected alternative. This answers
  "how is it built, and why."
- **`SPEC.md`** — the externally observable contract: the Management API surface and the
  frontend components' expected behavior, in concrete, testable terms. This answers "what must
  it do," and is what `feature-plan` slices into stories — keep it testable, not vague.
- **`mockups/<screen>.html` + `mockups/<screen>.png`** — one static mockup per new or changed
  screen (or user-facing email), and its screenshot. This answers "what will it look like," and
  is what the human approves before any UI code is written. See "Mockup each screen" and
  "Mockup a user-facing email" below.

Outside the plan folder, it also owns the project's shared mockup starters in
`docs/mockups/starters/` (see "Project starters" below), created only when a product surface
is distinct enough to need one.

Read `BRIEF.md` — design must serve it, not redefine it. As with `feature-explore`: if the project
has its own plan-folder convention, fold this content into that shape, but keep the discipline
of touching only these files; that's the point, not the specific file names.

Also updates its own two lines in `README.md` (the index `feature-explore` created) — same
append-only discipline as `DECISION-LOG.md`: never touch a line owned by another phase.

## Scope

- IN: which Umbraco extension point(s) to use (property editor, dashboard, content app,
  section, notification handler, middleware, tree, workspace, etc.), data model & persistence
  (EF Core entities/migrations, or none), Management API surface (controllers, DTOs, routes),
  frontend component boundaries, static mockups of each new or changed screen and of any
  user-facing email the feature sends, build-vs-buy, key tradeoffs, which connected systems a
  change of this kind conventionally touches (see "Connected-pattern check" below).
- OUT: the problem/why (`feature-explore` — read it, don't redo it), task breakdown
  (`feature-plan`), actual code (`feature-build`).

## Preflight

If the request is only to capture a project mockup starter, skip this preflight: no plan
folder or `BRIEF.md` is needed. Read the project's `CLAUDE.md` for the Umbraco version, then
go straight to "Project starters".

1. Resolve which feature this run is for. If more than one plan folder exists, prefer a match
   between the current branch/worktree name and a folder name (see `CLAUDE.md`'s "Finding the
   current feature's plan folder" rule) — this is the normal case once `feature-build` has
   started. If nothing matches, fall back to the one plan folder present, or ask if more than
   one is ambiguous.
2. Read `BRIEF.md` in the resolved folder. If it's still `TODO` or missing, surface that and
   offer to bounce back to `feature-explore` — designing against an undefined problem is wasted
   work.
3. Read the project's `CLAUDE.md` for existing architectural conventions (folder structure,
   namespace rules, extension patterns already in use) — a new feature should extend the
   grain of the codebase, not fight it.

## Connected-pattern check

Some changes belong to a *kind* the codebase already has conventions for — a new property on
a content/model type, a new CRUD method on a repository, a new entity type — and that kind
conventionally fans out to systems well outside the file being changed: version history/audit
trail, Deploy import/export connectors, search indexing, cache refreshers, before/after
notification events, permission checks. Missing one of these doesn't fail a build or a test —
it ships a feature that quietly doesn't round-trip through Deploy, or doesn't show up in
version history, and nobody notices until a user does.

Before drafting `ARCHITECTURE.md`, decide if this feature is that kind of addition. If it is:

1. **Check docs first.** If `CLAUDE.md` or another skill already states what a change of this
   kind must touch, that's ground truth — skip straight to step 3. For Deploy and uSync,
   `umbraco-env-sync`'s "Keep sync in step" table is that statement.
2. **Otherwise, sample sibling implementations.** Find two or three existing siblings of the
   same kind (properties on similar models, similar entity types, similar CRUD methods) and
   read what each one currently wires up. If they agree, that's the pattern. If they disagree,
   note the split in `ARCHITECTURE.md` and ask which behavior this feature should follow rather
   than picking one.
3. For each system the pattern touches, decide: does this feature need the same treatment?
   Carry the ones that apply into `ARCHITECTURE.md`'s decisions and `SPEC.md`'s scope so
   `feature-plan` slices them into real tasks. Explicitly note the ones that don't apply and why,
   so it reads as a deliberate cut, not an oversight.

This is a different altitude than `reviewer`'s sibling-comparison step: reviewer catches a
missed cross-cutting concern on the *same class* after the code is written; this catches a
missed *subsystem* before a single task is planned. Skipping this step doesn't fail review —
it just means the gap ships, because nothing else in the pipeline looks for it.

## Backoffice UX check (features with a UI)

If `SPEC.md`'s "Frontend components" section isn't "none," invoke `umbraco-backoffice-ux` and apply
it before finalizing the design:

1. **Pick each component by its convention**, not the plainest control that works. Above all,
   anything that chooses an entity is a picker, not a select box. A select chosen over a picker
   gets a line in `ARCHITECTURE.md` saying why.
2. **Walk the five moments** (first run, mistake, wait, finish, return) for each screen. Each
   one that applies becomes one ordinary line in `SPEC.md`, same as any other observable
   behaviour, that `feature-plan` slices into a task like anything else. One that doesn't apply is
   noted as a deliberate skip.
3. **List every place each component will appear**, so the mockups and the spec cover all of
   them.

### Mockup each screen

A screen described in words can't be judged until it's built. "A summary box and a by-model
table, styled like the Usage dashboard" reads fine in `SPEC.md` and still ships with the wrong
box layout, a column nobody needs, and a chart people misread — each one found only once the
code exists, and each one a fix-and-rebuild round trip. A picture gets the same feedback in
minutes, before a task is planned.

Every new or visibly changed screen gets a mockup; none is optional. If the session is too
long to finish them, stop and say which screens are left, so the user can re-run this phase
in a fresh session. Never hand off with a screen described but not drawn.

For each screen the feature adds or visibly changes:

1. **Match the sibling screen first.** Following `umbraco-backoffice-ux`'s "Match what's already
   there", open the nearest existing screen of the same kind and write down its layout rules
   before drawing anything. A new screen that looks like a stranger next to its neighbours is
   the most common UI fix, and the cheapest to prevent.
2. **Start from a project starter if one fits, otherwise the matching pattern in
   `templates/mockups/`.** Check the project's `docs/mockups/starters/` first (see "Project
   starters" below). Otherwise, almost every backoffice screen is one of a handful of
   patterns, and each has a starter:

   | Pattern | Starter | Covers |
   |---|---|---|
   | Dashboard | `dashboard.html` | Dashboard tabs, summary boxes, chart box, box with an edge-to-edge table |
   | Collection (list) view | `collection.html` | Toolbar (create, filter, view switch), table with status tags and selection, bulk action bar, pagination; content cards and empty state as alternatives |
   | Media card view | `collection-media.html` | Grid of folder, image and file cards, selection, bulk action bar |
   | Editor (workspace) | `editor.html` | Header (back, icon, name, "..." actions menu, view tabs), count badges on a view tab and a content tab, property groups, a picker property, footer with save actions, toast; `editor.html#save-options` shows the save options menu |
   | Sidebar modal (picker) | `modal-sidebar.html` | Slide-in panel for choosing from a list, small/medium/large widths |
   | Sidebar modal (form) | `modal-form.html` | Slide-in panel for create/edit forms — property rows inside a `uui-box` group, same as `editor.html`'s groups |
   | Dialog modal | `modal-dialog.html` | Centred confirm box, positive or danger action |

   Every starter carries the backoffice chrome: the header with **section tabs** and the
   sidebar with the **tree**, so those are set on whichever starter the screen uses — mark the
   new section tab or tree item active. Copy `_mockup.css` and `_mockup.js` into `mockups/`
   once, copy the starter to `mockups/<screen>.html`, and replace what's between its "Replace
   from here" and "Replace to here" comments. Delete the parts the screen doesn't use. Open
   menus (`.popover-menu`) sit in a `.popover-anchor` beside their trigger; a page that needs
   a second open state uses the `on-target` class and is shot at `<screen>.html#<id>`.

   A few more patterns build from these: a **property editor** is one `.property` row in
   `editor.html`; an editor's **Info view** is the editor's main area as a two-column grid
   (`1fr 350px`, 24px gap) with stacked boxes left and a "General" box right; a **search or
   filter bar** above a box is the collection toolbar without its create button. Property
   rows always sit inside a `uui-box` group, never loose on the page or modal background —
   `modal-form.html` is `modal-sidebar.html`'s shell with that content instead of a picker
   list; reach for it whenever the modal's job is to create or edit something, not choose
   from a list. A property row stacks (label, then description, then the editor, full width)
   or sits side by side (a fixed label column next to the editor) purely by how wide the row
   itself renders, not by which starter or modal size it's in — `_mockup.css` already does
   this with a container query, the same way the real `umb-property-layout` component does,
   so it's never something to add by hand per screen. A property row that looks wrong is
   almost always a sign something else broke its width (an unexpected `max-width`, a modal
   narrower than intended), not a layout to override directly.

   A property with a validation problem — a duplicate alias, a value that fails a rule — gets
   the real mistake-moment treatment, not an invented one: inside the `uui-label`, right after
   its text, a small red `!` badge (`<span class="invalid-badge"><uui-badge color="danger"
   attention>!</uui-badge></span>` — the span is required, since `uui-badge` positions itself
   absolutely by default and needs a small relatively-positioned box to land in rather than
   the corner of the page), and a `<div class="validation-message">` as the last thing in the
   editor column, holding the one-line error. `_mockup.css` styles both already. Show it on
   the one field with the problem, not every field, matching the real
   `umb-form-validation-message` component. A screen that fits none of them starts from the
   closest starter, and the mockup notes which.

   The starters load the real UUI elements, theme and Umbraco's own backoffice icons from the
   CDN (`<uui-icon name="icon-*">` uses the same icon names the code will), and
   `_mockup.css` recreates the `umb-*` layout elements with values copied from the backoffice
   source. So the mockup is built from the same parts the code will be, with no separate
   design system to keep in sync. Set `UMBRACO_VERSION` at the top of `_mockup.js` to the
   Umbraco major the project targets (from `CLAUDE.md`; the newest one when it targets more
   than one). It picks the look: 18 has UUI's rounder corners, 17 the squarer 3px ones and
   pink highlight. Umbraco 17.6+ and 18 use UUI 2 (the default); 17.5 and older use UUI 1
   (see the note in `_mockup.js`). Static HTML only: no build step, no data fetching, no charting
   library (a rough inline SVG of the right chart type is enough).
3. **For a component that already exists and runs in the product, copy its real source —
   don't invent it.** A chat bubble from the product's own chat package, a bespoke chart, any
   custom control that isn't plain UUI: read its actual CSS/markup (the same discipline
   "Project starters" below uses for the backoffice chrome) and copy its real colours,
   spacing and shape. A plausible-looking guess is exactly the kind of difference a human
   catches by eye and sends back as a fix-and-rebuild round trip, instead of being resolved in
   the one minutes-long look that was the point of mocking it up.
4. **Use realistic fake data.** Real-looking names and real magnitudes, one long value that
   might wrap, one row in a warning or error state. Placeholder text hides the questions that
   matter — whether a range reads better as one number, whether a column earns its space,
   whether a first-time viewer understands what a chart is showing.
5. **Mock the five moments that apply.** The empty state and error state are their own small
   variants (a second section in the same file, or `<screen>-empty.html`), not something left
   for the builder to invent.
6. **Screenshot and show it.** Serve the folder locally (the pages load ES modules, so
   `file://` won't work), wait for `html[data-mockup-ready]` so UUI, icons and any toast have
   finished loading, then check the console for warnings before screenshotting — a missing
   icon name (`No backoffice icon named icon-*`) is the common one, and it's free to catch
   since the loader already prints it. Screenshot each mockup at a backoffice-sized viewport
   (1440×900), save it beside the HTML as `<screen>.png`, and show it to the human with the
   two or three choices you're least sure of named underneath. Revise the HTML on feedback
   and re-shoot; the screenshot in the folder is always the current one.

#### Project starters

Some products have their own surface that most of their features land on: Umbraco.AI's
Copilot sidebar, Automate's flow editor. The general starters can't draw these, and mocking a
Copilot feature on a generic editor page hides the questions that matter (does it fit a
narrow sidebar, how does it sit among flow nodes). A project starter captures that surface
once so every later feature reuses it.

A starter gets made one of two ways:

- **On first need:** while mocking a feature's screen, the surface passes the test below and
  no starter exists yet.
- **On request:** someone asks for one ahead of time, usually because they know several
  upcoming features will land on that surface. Apply the first test only; the second is the
  requester's call, since they know what's coming. If the surface can be drawn from a general
  starter, say which one and don't save a project starter. Show the finished starter's
  screenshot for approval, then leave it uncommitted and tell the user, since there's no
  build to commit it with (committing follows `git-workflow`).

**On first need, capture one only when both are true:**

1. **It can't be drawn from a general starter.** The surface's own layout or chrome differs
   (a docked panel over the backoffice, a canvas of connected nodes, a chat thread), not just
   the content between the "Replace from here" comments. A dashboard with unusual boxes is
   still a dashboard: use `dashboard.html`.
2. **Features keep landing on it.** It's a host surface the product's features are built
   into, not one screen of this feature. If it's a one-off, draw it inside this feature's own
   mockup and don't save a starter.

When both are true and no starter exists yet:

- **It's a drawing of the surface, not the surface.** Like the general starters, it's static
  HTML and CSS plus UUI elements, built to look like the real thing. Never load the product's
  own components, bundles or libraries into it (a flow editor's React canvas, the Copilot's
  chat element, the package's built JS): they need the running app, they break outside it, and
  they make the starter as hard to change as the product. Draw a flow node as a styled box and
  a connector as an inline SVG line; draw a chat thread as stacked message boxes.
- Build it the same way the general starters were built: read the product's own source for
  that surface and copy its layout, spacing and colours into an HTML page that uses
  `_mockup.css` and `_mockup.js`, with a "Replace from here" / "Replace to here" region where
  feature content goes. Screenshot the real surface, if a running site is available, and
  compare.
- Save it to `docs/mockups/starters/<surface>.html` with a copy of `_mockup.css` and
  `_mockup.js` beside it, so it previews on its own.
- Start the file with a comment naming the source files it copies and the commit it was
  copied from (`git rev-parse HEAD`).

When reusing a project starter, first check whether its source files have changed since that
commit (`git log --oneline <commit>..HEAD -- <source files>`). If they have, refresh the
starter before copying it, and update the commit in its comment.

Fidelity is "close enough to judge the layout and the content choices," not pixel-perfect:
real components, real spacing tokens, real data shapes. Final colour tweaks and dark-mode
polish still happen on the built screen.

`SPEC.md`'s "Frontend components" section shows each mockup's screenshot inline at full size
(GitHub fits it to the page; a thumbnail is too small to judge layout) with a link to its
HTML source underneath. The text under a screenshot covers only what the picture can't show
(see `plain-writing`'s "Let pictures carry what they show"): what happens on click, save and
failure, rules and permissions, where the data comes from, and the states not pictured. It
doesn't walk through the layout, labels or columns the reader can already see. The mockup is part of the contract: the builder matches its layout
and content, and `feature-build`'s smoke step compares the built screen against it. A deliberate change from the mockup during the build
is a decision, logged in `DECISION-LOG.md` and reflected back into the mockup by re-running
this phase.

## Mockup a user-facing email

If the feature sends an email (a notification, a digest, anything a real person reads in their
inbox), it needs the same mockup discipline as a screen, whether or not the feature has any
backoffice UI of its own — a described email reads fine in `ARCHITECTURE.md` and still ships
with a subject line that's too long or a layout that breaks in Outlook, found only once it's
built.

Start from `templates/mockups/email-notification.html` (check the project's own
`docs/mockups/starters/` first, same as a screen) and replace what's between its "Replace from
here"/"Replace to here" comments, including the subject line — it's as reviewable as the layout.
Real Umbraco notification emails, and most transactional email generally, are plain
inline-styled HTML with literal hex colors, not CSS custom properties or a `<style>` block on
the email body itself: mail clients strip both. This file never loads this folder's
`_mockup.css`/`_mockup.js`/UUI harness — that's for backoffice screens, and would be actively
wrong here. Open it directly in a browser or an email client preview; no local server needed.

Same rules as a screen otherwise: realistic copy, not placeholder text; the real send and
failure behaviour goes in `SPEC.md`'s prose, not the mockup; screenshot it and show the human
before moving on.

## Skills to pull in

- Extension-point idioms, DI registration patterns → `umbraco-extensibility`.
- Umbraco's documented way to use an extension point, setting, or API → `umbraco-docs`, for
  the project's major.
- How the CMS itself implements something (a base class, an extension point's real contract,
  a built-in sibling) → `umbraco-cms-source`, read at the project's release tag.
- Async naming, visibility (internal by default), public-API compatibility → `umbraco-package-conventions`.
- A new service's result shape for routine failures → `umbraco-package-conventions`.
- Persistence needed → `ef-core-data`.
- A new NuGet or npm dependency → `umbraco-dependencies`, so whether the CMS already
  decides its version, and whether it ships to sites, is known before it's chosen.
- Reading content on front-end requests, caching, or large lists → `umbraco-performance`,
  so where data is read from and what clears each cache is decided now.
- Background jobs or scheduled work → `umbraco-extensibility`, so work meant to happen once
  happens once on a site with several servers.
- A new or changed entity in a project that supports Umbraco Deploy or uSync, or adding that
  support → `umbraco-env-sync`, so how the entity moves between environments is decided
  now, and its "Keep sync in step" changes reach `SPEC.md`'s scope.
- Backoffice UI needed → `umbraco-backoffice-ux` for how screens should look and behave, the official
  Umbraco Backoffice Skills plugin for the specific extension point (dashboard, property
  editor, tree, etc.), plus `umbraco-backoffice-conventions` for package-level frontend
  structure.
- Writing `ARCHITECTURE.md` and `SPEC.md` → `plain-writing`.
- Anything touching auth, the Management API, an endpoint outside it, a stored secret,
  rendering external or AI-generated content in the backoffice, or a design that would
  expose a secret to the client → `umbraco-security`, now, not at review time.

## Assume, then show

Not every topic below needs a spoken question. Before asking:

1. **Check whether it's a checkable fact** — the codebase's existing conventions, how a
   sibling feature is built, what an extension point actually supports — and go find it
   instead of asking. Find it in the real source (the CMS's own via `umbraco-cms-source`) or Umbraco's docs
   (`umbraco-docs`). When the design says it mirrors a sibling's
   method signature, type or settings pattern, open that sibling's file and copy from it, not
   from a `CLAUDE.md` summary or memory. A detail recalled from a summary can be wrong in ways
   nothing catches until a builder compiles against it, several tasks later.
2. **If it's a judgment call and a wrong guess is cheap to correct once it's written down**
   (component boundaries, a non-functional target, which pattern to reach for), write it as
   `> ASSUMPTION: ...` under the relevant section of `ARCHITECTURE.md`/`SPEC.md` instead of
   asking, and let the human correct it when they read the design. Correcting a written-down
   guess costs them a sentence; answering a live question costs them a context switch.
3. **Ask directly only when a wrong guess is expensive to undo here** — which extension point
   to hang the feature off (hard to walk back once built against), the data model/migration
   shape, which CMS version(s) to support, or an auth/trust boundary crossing into the
   public-facing site. Everything else defaults to assume-and-show.

This doesn't relax "stop, don't guess" — that rule is about a phase's *required input* being
missing (no `BRIEF.md` to read). This is about which of *this* phase's own questions you put
to the human versus answer yourself and show your work.

## Interview

Up to ~10 questions, adaptive, batched (4 at a time) — only what's left after the filter
above:

1. Which Umbraco extension point(s) does this hang off? (property editor, dashboard,
   content app, notification handler, middleware, custom section, tree...)
2. Does it need its own persistence, or does it read/write existing Umbraco data
   (content, media, members)?
3. If persistence: core entities, relationships, and — SQL Server only, or SQL Server *and*
   SQLite (most packages need both, since sites run either)?
4. Does this need a Management API surface of its own, or is it purely a backoffice UI
   against existing APIs?
5. Component boundaries — what's a service, what's a repository, what's UI-only?
6. Which CMS major version(s) does this need to run on? Any API used only in one?
7. Auth & trust boundaries — is this backoffice-only, or does anything cross into the
   public-facing site?
8. Hardest technical risk, and the fallback if the assumed extension point doesn't behave as
   expected?
9. What are we explicitly **not** building for now (YAGNI)?
10. Non-functionals that bite: content-tree or data scale, request latency, cold-start on a
    busy site, accessibility of a new screen? Each answer becomes a target in `SPEC.md`.

## Produce

Write every file this phase produces following `plain-writing`: a person reads it before the
next phase runs, so it should be quick to read without leaving anything out.

When revising an existing `ARCHITECTURE.md`/`SPEC.md`, rewrite the affected sections to
reflect the current approach only — don't leave the old approach in place alongside a note
about what changed. These files are a snapshot of the current design, not a changelog. Past
approaches and why they were rejected belong in `DECISION-LOG.md`.

`ARCHITECTURE.md`:

```md
# Architecture

## Extension points
<which Umbraco extension point(s), and why this one over an alternative>

## Data model & persistence
<entities, relationships, SQL Server + SQLite considerations, or "none — reads/writes
existing Umbraco data via <service>">

## Connected systems
<other systems this kind of change conventionally touches — version history, Deploy
connectors, search indexing, notification events, etc. — and whether each applies here and
why, or "none — not this kind of change">

## Key decisions
<each decision, its rationale, and the alternative rejected>
```

`SPEC.md`:

```md
# Spec

## Management API surface
<routes, request/response shapes, and the observable behavior each one guarantees — or
"none">

## Frontend components
<component boundaries, which package/library they live in, and what each must observably
do/render/emit — or "none">

### <Screen name>

![<Screen name> mockup](./mockups/<screen>.png)

[Mockup source](./mockups/<screen>.html)

<behaviour the screenshot can't show: what happens on each action, rules, data source,
states not pictured>

<one block like this per mocked-up screen>

## Non-functional targets
<one line per target the feature must meet (scale, speed on a hot path, accessibility of a
new screen), each a number or a condition a test or reviewer can check. Every figure that
`BRIEF.md` or the human didn't give (a time, a limit, a count) is `> ASSUMPTION: ...` until
they agree to it. "none — <why>" when nothing applies.>
```

Update the `ARCHITECTURE.md` and `SPEC.md` lines in `README.md`: check each box and replace
`<pending>` with one plain-English line for what each file now says.

Append dated entries to `DECISION-LOG.md` for each architectural call made here. If a call is
a standing, project-wide decision rather than one scoped to this feature (the CMS major
version(s) targeted, the database provider(s) supported, a pattern every future feature must
follow), write it to `.claude/memory/` instead (type: `decision`) — see
`.claude/memory/README.md` for the format.

## Hand off

If any screen or email described in `SPEC.md`/`ARCHITECTURE.md` is still missing its mockup,
this phase is not finished. Stop here instead of handing off: say which are left, per "Mockup
each screen" and "Mockup a user-facing email" above, so the human can re-run this phase in a
fresh session. A design with a screen or email described but not drawn is not a smaller version
of this phase's output — it's an unfinished one, and noting the gap is not a substitute for
closing it.

Otherwise, note any `TODO` in `ARCHITECTURE.md`/`SPEC.md`, any screen mockup the human hasn't
approved yet, and any project starter created or refreshed in `docs/mockups/starters/`, then:
`Suggested next: feature-plan.`
