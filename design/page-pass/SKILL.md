---
name: page-pass
description: "The one skill for taking a page to done: its agent surface and its UI/UX, in one pass. Use when assigned pages or routes to pass, on `/page-pass <route>`, or when a campaign brief says 'do the page pass'. NOT for certification ledger writes (use surface-certification-loop)."
---

# page-pass — take one page to done

**Version 1 (2026-09-27).** Built with Arman and tested on real pages; every
miss found in testing becomes a rule here. **This file plus
[`page-types.md`](./page-types.md) is everything you read up front.** Each rule
below is complete as written. The skill named after a rule holds the step-by-step
procedure — open it only when you are doing that job or the check fails.

## What you do with a page — seven steps, in order

1. **Look first.** Run `pnpm page:look --route <route>` (every route the page
   has, with a real record id): it signs in as the test admin and writes
   desktop 1280×800 and phone 375×812 screenshots in light and dark, plus
   `look.json` — console errors, failed requests, anything under the header,
   charts/images drawn at zero size,
   how much of the first screen holds content, headings, text under 12px,
   emoji, small phone targets. Add `--full` to see below the fold,
   `--signed-out` for what a visitor sees, `--as member` for an ordinary
   (non-admin) person, `--fresh` for a first visit (no remembered organization or
   view prefs), `--org "<name>"` to pick the workspace first, `--views desktop-light,phone-light` to go faster, and
   `--click '[right:]SELECTOR=>TEXT'` (repeatable; chain steps on one load with
   ` >> `) — TEXT matches the START of the text or aria-label ("About Theme" needs `=>About`) to open each menu, dialog and tab and capture it. A slow page needs
   `--settle 12000`. Read every
   screenshot yourself; the numbers are places to look, not verdicts. The dark
   views force the dark class, so a theme control reading "Light" there is the
   tool, not the page. For a
   longer interaction, write a throwaway Playwright script in your own TMPDIR
   modelled on `scripts/page-look.mjs` — never a dev server. Use it the way a person would: click every
   control, open every menu, dialog and tab. **Before you read any rule, write
   down everything that looks wrong or wasteful.** This list is yours; the rules
   must end up covering every line of it.
2. **Name the page's type** from [`page-types.md`](./page-types.md). The type
   says which core rules change and what it adds. Unsure between two types →
   pick the one whose "recognize it" line fits, and say why in your report.
3. **Run the core (below), then your type's additions.** Every rule gets a
   verdict: `pass` · `fixed` (what) · `na` (one-line why) · `deferred-visual`
   (code done; name the exact look still owed) · `arman` (question filed) ·
   `blocked` (what blocks).
4. **Fix what you found** — the cause, not the symptom. Never remove, rename or
   hide a feature, or a designed look another page relies on, to make a rule pass. Database changes are part of the job
   (functions, grants, `client_callable_door` rows, per CLAUDE.md; new tables only
   via `platform.create_entity_table`). Pick ONE path: through the Supabase MCP
   with NO migration file, or a file you write and apply with `pnpm db:apply`
   (ledgered). Never both — an MCP-applied change with a file left beside it
   reads as unapplied drift. A
   DROP/CREATE of a function loses its grants and its `client_callable_door` row:
   restore both in the same transaction. A shared-link fix often reaches past the
   page into the shared execution stack (org gate, bindings, the server's guest
   path) — follow it there. If the fix belongs in a shared component
   or package, first list every page that uses it (search its imports in every
   repo). A behavior or bug fix that leaves the look unchanged: fix it and prove it
   live on a few of those pages. A change to how it LOOKS: ask Arman first, one
   simple question with the full page list and before/after links (law:
   `common-docs/policies/no-dead-ends.md`); if it suits your page
   and not the others, make it an option for your page, never the new default. Run that
   component's tests (`npx jest <its dir>`; menus: `npx jest features/context-menu-v3`,
   which runs the heading check). If it belongs on the server (a read wrongly gated,
   a 4xx/5xx the page can't fix), fix it in `../aidream` under that repo's
   CLAUDE.md, same commit rules, and name both commits in your report.
5. **Prove it live.** Every fix seen working on the real page; every main
   action carried through to its real saved result **as the page's real
   audience** (signed out for a shared link or promotional page — a guest run,
   not an admin run), then re-checked (console
   and Error Inspector clean after, not just on load).
6. **Look again as a stranger — the final look.** Needs your changes live: push
   (or have your coordinator push), then wait for the release with
   `until pnpm -s page:look --route <r> --views desktop-light --commit <sha> --out /tmp/<you>/w; do sleep 120; done`
   (exit 3 = not live yet). On the live result, run
   `page:look --full` (and `--signed-out` where visitors come) and review it as
   a demanding customer who never saw your work: list every flaw you can still
   see, rule or no rule. Look at EVERY mode and state the page has (each
   view/edit mode, each tab, empty/loading/error, the phone path to each — in light AND dark; a third-party stylesheet once made one view's text near-black on dark), not
   just its default screen: a notes pass once graded its Read view and missed a
   stock third-party Write view with no app menu. Fix them, or report each as open. Blind reviewers
   grade the page after you; a flaw they find that your final look missed
   counts against the pass.
7. **Record it.** One Change Log line in the owning feature's `FEATURE.md` (no
   FEATURE.md for this route? the nearest one that owns its code) in the same
   commit (`page-pass <date>: type <x>, posture <x> after <product>, fixed …`),
   then the report below.

**If the live site or database is down** (504s on several pages, `db.matrxserver.com`
reads timing out), stop the live steps, write `INCIDENT: <time, what failed>` in
your report, keep doing static work, and resume the live steps when it answers —
an outage is never a page finding and never yours to chase.

**You decide; you never interview.** Product questions only — does a feature
exist, should a surface move in the hierarchy, a size or policy outside what
this file allows — go to Arman through `ask-arman`; keep working on everything
else. Posture skills that say "interview first" mean a person live in the
session, never you.

## Where you work — pick your lane once

| | **Local lane** (a Mac session) | **Cloud lane** (a cloud container) |
|---|---|---|
| Server | none needed to look; `pnpm preview:start` (the ONE shared server, `http://<session>.localhost:3001`) only when you must see an unreleased change | **none** — a container cannot run a dev server and a type check together |
| Look and prove | `TMPDIR=/tmp/pl-<you> pnpm page:look --route <route> --commit <sha>` against `https://aimatrx.com` (admin routes are served from `https://manage.aimatrx.com` — check the commit there) after the release carrying your commit (about hourly; exit 3 = not live yet — work on something else) | same |
| Agent surface proof | `TMPDIR=/tmp/pp-<you> pnpm surface:probe --surface <name> --route <route> --commit <sha> --out <file>` (a window/dialog surface: add `--open 'SELECTOR=>TEXT'` so it is opened before the read) (+ `--agent '<request>'` for write targets) | same |
| A view you cannot see | `deferred-visual` with the exact step | same |

**Both lanes:**
- **A hot shared file holds someone else's uncommitted hunks** (the surface
  registry, `route-to-surface.ts`)? Commit only your hunks through a private
  index, then re-sync the real index for those paths:
  ```
  git diff -- <file> > /tmp/<you>.patch   # edit it down to your hunks only
  GIT_INDEX_FILE=/tmp/<you>.idx git read-tree HEAD
  GIT_INDEX_FILE=/tmp/<you>.idx git apply --cached /tmp/<you>.patch
  GIT_INDEX_FILE=/tmp/<you>.idx git commit -m "page-pass(<route>): …"
  git reset -q -- <file>                  # index only; the worktree keeps their hunks
  ```
- Admin routes redirect to `manage.aimatrx.com` by themselves; pass `--base
  https://manage.aimatrx.com` only if a look lands on the wrong host.
- A page that needs an organization or record opens with it in the URL
  (`/hr/settings/employer?org=<slug>`, `/crm/<id>`): pass that full route to
  `page:look` and the probe.
- **`pnpm page:checks <your files or dirs>`** runs every check this skill names
  (six at a time, ~3 min) and prints CLEAN / FINDINGS / ERROR per check for
  YOUR files only; red on other files is not yours. The per-area check lists
  below say what each covers.
- Type check: `pnpm type-check` (TypeScript 7, whole repo, ~30 s; the machine-wide
  queue folds your call into any other waiting one). Never a focused tsconfig and
  never a direct compiler call — both bypass the queue and cannot be shared.
  Errors in files you didn't touch are not yours; list them.
- **Every commit parses.** Before each commit run `pnpm -s check:parse` (~20s, whole tree; red outside your files is not yours) — a quote inside a string once broke a manifest on main between two commits. Committing early never means committing unparsed.
- **Commit right after each coherent edit, before running checks** — a sync sweeps the shared
  checkout every ~30 minutes and commits any dirty file under its own message,
  so a file left uncommitted loses your authorship and message.
  It can still win the race by seconds. If it swept your edit, that is fine:
  name its commit as yours in the report and move on — never rewrite it.
- **Never delete code to clear a check.** A flow a guard flags is fixed, not removed; deleting needs Arman's written word (unfinished-work alarm). Check `git log` first: a worker once deleted a login flow another lane had hardened 16 minutes earlier.
- **Prove a test fails on a scratch copy, never by breaking the real file** —
  the sync sweep can commit the broken version in the seconds it sits there.
  Copy the file (or its old version from git) into your TMPDIR and point the
  test at it.
- zsh does not split a variable holding several paths: use an array
  (`F=(a.ts b.tsx); git add -- $F`) or list the paths literally.
- Commit by path per page (push unless your coordinator says it pushes): `git add <files>` → `git commit --only -m "page-pass(<route>): …" -- <files>` → push.
  One shared checkout on `main`: no branches, no worktrees, no tree-wide git,
  never format a file you didn't create, never run `release.sh`. After a
  pull, re-run `pnpm install --frozen-lockfile` if the lockfile changed.
- Test data you create is obviously named (`PP test — …`) and listed in your report.

**Content a person authored is not the page.** An app's own layout, a
document's text, a user's template body are judged by their author; the rules
here judge our chrome around them (header, menus, run controls, states, agent
surface). Say which parts you judged as authored content.

## The core — seven areas, every page

### 1 · Agents can work on the page
- **Registered:** a surface manifest in `features/surfaces/manifests/` whose
  values describe THIS page (a record's sub-views — run, code, settings — may share the
  record's family surface when every value is true on each; a sub-view with data
  of its own gets a child surface) (a list page never borrows its parent's
  one-record surface — give it its own), label = the page's human name, route mapped in `route-to-surface.ts`, DB mirror synced.
- **Sees everything:** every piece of data the page loads and a person could
  point at is a declared value, emitted by one pure scope module from state the
  page already rendered (`getScope` never fetches). Not loaded yet → omit the
  key; loaded and empty → `[]`/`0`/`""`; a failed load reports its status
  (a `load_error`-style value the agent can see), never counts, rows or a
  value that contradicts what the person sees.
  Keep existing value names (stored bindings use them).
- **Sees what its jobs need up front — the context budget.** An agent that
  lacks what it needs fails or spends more tokens looking it up, so send it —
  up to 10,000 chars per page in total, spent by the page's shape: a focused
  record ~10,000; a record with its comments/folders ~7,000 + the rest shared;
  a list page's condensed visible list ~4,000; a broad page (SEO, dashboards)
  only a ~2,000-3,000 overview and a guide for discovery. Pack it as ONE XML
  bundle with `packages/chat/src/surfaces/runtime/context-bundle.ts` — never raw JSON rows.
  The bundle is what the agent reads up front; the page's individual values
  stay declared too (bindings and write twins use their names) at the default
  size. Worked bundles: `features/research/browse/surface.ts` (list),
  `features/flashcards/components/home/deckSurface.ts` (list); older manifests
  that inline raw arrays are not examples to copy. Over budget
  needs Arman's approval. Procedure: `surface-write-targets` Step 4.
- **An agent sees the choices of anything it can set** — a stage, rating or
  role target ships its options as a value (`<field>_options`: id + label), and
  a write the agent makes shows where the person looks (the tile that lists it).
- **Every person-action has an agent twin — count them.** List every create /
  edit / archive control on the page (New deal, Add file, a toggle) and the
  write target that does the same job; put that mapping in your report. A
  control with no target is a gap you close or explain.
- **Can change what makes sense:** every record type the page lists gets
  `create_/update_/delete_<plural>` over lists (one set per type, built with
  `collectionWriteHandlers`), plus `<record>_draft` when the page has a
  "New ___" dialog, and `draft` targets for authored fields on editors. All
  `ask`. Handlers save through the page's own save function, validate the whole
  value before the approval card, and return what landed with ids. Never
  targets for ids/ownership, credentials, billing, permissions, or derived
  numbers (scores, counts).
- **Told how:** the intro names which target does which job; a page with more
  than one record type or rules the descriptions can't hold gets a guide.
- **Right-click menu:** one menu per pane, delegated per row (a `MatrxDataTable`
  does it with `contextMenu={{ resolveRowContext }}` +
  `createTableRowMenuDescriptor` — worked: `lib/entity-list/components/EntityListTable.tsx`;
  `EntityListPage` lists get it for free), wrapper carries
  `sourceFeature` + `surfaceName` + `getApplicationScope`; the runtime
  provider goes AROUND the menu. A page showing a real record passes that
  record's own `contentSource` (and `entity` when it can be attached or
  shared); `{type:"raw"}` only when there is no primary text. Items are short
  verbs with no subtext — the one exception is a disabled item, whose
  `description` says why it is off and where it works. The menu's last entry
  (this page's label) is added by the platform from `surfaceName`; if it reads
  "This page" or another page's label, the surface mapping is wrong.
- **Agents menu:** every AI job the page already runs appears once in the top
  Agents menu; nothing is added to the visible page to announce it, and no AI
  feature is invented to fill it. A mandate opens in place.
- **Agent feedback read first:** `pnpm surface:feedback --surface <name>` prints
  SQL — run it through the Supabase MCP; fix what agents reported or say why not.
- **Proven with a real agent:** the probe reads the page (every visible value
  supplied, nothing undeclared, no `INERT MENU` / `VALUE MAPPING GAP`); with
  write targets, `--agent '<a real request>'` creates two, updates one,
  archives one, gets one refused before the card — and a read-only SQL check
  shows created rows complete, matching one made by hand.
- Checks: `pnpm check:surface-drift` · `check:surface-routes` ·
  `check:surface-impact <name>` · `check:context-menu` · `check:menu-naming` ·
  `check:agent-disclosure`.
- Procedures: `surface-write-targets` (Steps 0-4: targets, handlers, inline
  tiers, guide, live agent test) · `surface-authoring/references/campaign-worker.md`
  §2 "Rules that bite" and §3 sync · `context-menu-v3` · `agent-disclosure`.

### 2 · It actually works
- Every button, link and menu item does something real — no dead controls,
  no toast stubs, no disabled-looking controls that work or working-looking
  ones that don't.
- **A write is proven by the saved row, never by the absence of an error.**
  For every save/create/delete the page offers, follow the call to the
  database function it reaches and confirm that function accepts it (a
  generic upsert may refuse the kind you send); then, live, save a
  `PP test —` value and read the row back with SQL, and restore it. A button
  that "works" and saves nothing is the worst dead control.
- **Read the field that exists.** Reading a property the type does not have
  (`request.errorMessage` when the field is `request.error`) makes every failure
  silent — let the type check catch it (no casts), and show the real reason.
- **An empty read is not a success.** A lookup that returns no row where one
  must exist (access refused, wrong id) is an error the person and the agent
  see — never a silent return that leaves the page "still loading" forever.
- **A control is never enabled while what it needs is loading** only to
  refuse on press — it shows a pending state, or waits and then acts.
- **A server render never waits on the database without a limit.** Every read
  a page's server render (and `generateMetadata`) makes has a timeout and a
  fallback — metadata falls back to the generic title, the page to an honest
  error — so a slow database is never a platform 504.
- **An error affordance appears only in an error state** — an error menu, red
  icon or retry never renders beside a healthy "Saved" (`ErrorAlchemyMenu` goes
  inside the error branch; it reads the error box it sits in).
- **A vague error has a real cause — find it.** "Couldn't load …" is a symptom:
  read the recorded failure (`errors` MCP tool, or `ops.system_error` via the
  Supabase MCP) and fix the cause.
- Every load ends: data, an honest empty state, or a visible error with a
  retry after a bounded wait. Never an endless skeleton or spinner.
- Loading says what is loading: `SuspenseLoader` with a `message` for compact
  states; a `Skeleton` from `@ai-matrx/design-system` shaped like the content
  for content areas. Never plain "Loading…" or a bare pulsing box.
- Errors surface; nothing is swallowed. AI work streams into the live-run
  window, never a spinner.
- Every record the page names (a person, agent, document, a count over our
  records) opens — open, new tab, peek or window. Every detected problem
  carries its one-click fix.
- **What a person typed is never lost** — on every page, window and dialog:
  closing, navigating or a refresh keeps the draft (or asks first). Any
  non-empty text counts — a minimum length before saving a draft loses short reports.
  Unsaved edits in a form are guarded against in-app navigation too (header
  Back, links, browser Back): use `lib/navigation/useUnsavedChangesGuard.ts`,
  never a page-local `beforeunload`, and give edit mode a Discard.
- **A custom editing field keeps everything a plain field gives** — replacing a
  textarea/input with a rich or chip editor must keep: undo/redo for every
  change (inserts and auto-formatting included), plain-text paste, the caret
  never landing inside a non-editable piece, Home/End/Enter at the edges, and
  the standard field toolbar (voice and the page-agent door). Test each one
  live by typing — every one of these failed on first build.
- **A Stop / Cancel / Undo is proven by the server's state, not the client's.** Stopping a run means the server stops generating (reopen it: no finished answer), not that the screen hid it; after a stop the screen says "Stopped" and offers the next step.
- **A control's saved value must change what it claims to change.** Prove it
  by the effect (switch the model off → it is gone from the picker), never by
  the saved row alone: a settings switch once wrote a list nothing read.
- **Catalog text written for engineers never reaches a person** ("Fires
  when…", "Audience:", spec tags) — fix it at the source; a display filter is
  only the stopgap while the source rewrite lands.
- **An empty value is still a supplied value**: a context inspector or a check
  that treats `null` as "missing" raises a false alarm.
- **Desktop keeps every action visible; only the phone folds.** Folding into a "More"/tools menu is a phone fix — applying it at every width hid features and Arman had it reverted (2026-09-27). On desktop, fit actions into fewer rows, never behind a menu.
- **A control the device cannot run is absent** (screen capture on a phone),
  never a button that fails.
- **The screen shows what was saved.** After a save the view re-reads (or
  applies the returned row) — never the pre-save copy. **Saving an untouched
  form changes nothing:** a save writes only the fields the person changed, and
  every field round-trips exactly (a toggle labelled
  "Private" never writes another visibility; a blank type is never saved as a
  default).
- **A count on a button equals what it opens** ("Review 81 due" opens 81, not 29).
- **An automatic AI job re-runs only when its inputs meaningfully change** —
  never on page open, a view switch, or an empty record it created itself.
- **Numbers are plausible.** Sanity-check every computed figure against the
  rows behind it (a study time of 57 days, a count that disagrees with its
  list, a 0 shown beside content that exists are defects).
  A count or total built from a plain list read stops silently at 1000 rows —
  read it with `readAllRows` or count on the server (an admin "in DB" count read
  1 where the database held 31). Colour carries meaning only when it varies:
  a green badge on nearly every row is noise.
- **Any change that loosens a gate is reviewed before it ships** — dropping an
  organization requirement, a new grant or door, a row-security or auth
  exemption: dispatch an independent reviewer (standard lane) to trace every
  call path to the end (the org-free `/browse` declaration broke every Microsoft
  browse five calls down). Say so in your report.
- **First ask whether it needs an organization at all.** A person's own
  records (their connections, their settings, their history) never do — if the
  server demands one for them, fix the server declaration, don't hold the page.
  A page re-runs its loads when the header organization changes.
- **A request that needs an organization is held, never failed.** With no
  organization selected, the page shows the person's memberships inline and
  proceeds once one is chosen (`lib/organization/organization-gate.ts`); an
  automatic AI job waits for its organization rather than failing on load —
  never an error box, and never an internal key (`app.some_mandate`,
  `execution_error`) on screen. A page opening in an error state before the
  person did anything is a first-look failure.
- **Edit rights follow the person's access** (`iam.has_access_for`), never
  "created_by = me" alone.
- **Nothing that decides what a person may do is writable by that person.**
  When the page reads a plan, grant, quota, usage, role or approval, confirm
  the browser cannot write it: `select has_table_privilege('authenticated',
  '<schema.table>', 'UPDATE')` (and INSERT/DELETE) must be false. If it is
  true, the fix is `client_read_only = true` on its `platform.entity_types`
  row, then `iam.apply_table_grants(<schema>, <table>, <its rls_variant>)`,
  proven by a refused write as the test user (the D355 pattern).
- Reads and writes go straight to the database through the feature's service;
  a list treated as complete uses `readAllRows`.
- A browser component never imports a value from server-only code (a loader
  using the server database client, `next/headers`, `"server-only"`) — share
  constants from a plain module. The type check cannot see this; the build breaks.
- Checks: `pnpm check:dead-ends` · `check:unwired` · `check:static-loader` ·
  `check:client-server-only`.
- Procedures: `real-loading-states` · `no-dead-ends`.

### 3 · The first screen is right
- **The title stands alone.** One title, in the page header, with no
  description or subtitle under it and no second title or hero in the body.
  No welcome text, no "this page lets you…". Help is one short sentence next
  to the thing it helps with, or a tooltip. **The same holds for every section
  and card:** a heading, not a heading plus an explanatory sentence.
- **Empty is compact.** A thin record never shows a wall of "—" rows or a stack
  of empty cards: empty fields collapse into one "Add …" affordance, and an
  empty section is one line with its create action, not a full card.
- **Nothing sits under the header.** The header is glass over the page. Content
  that must stay visible — buttons, toolbars, card grids, banners — starts
  below it with `pt-[var(--shell-header-h)]` (never a hand-typed `pt-12`), and
  at rest nothing interactive or readable sits inside the glass or its fade.
  Content that scrolls freely may pass behind it while scrolling.
- **No wasted space.** At 1280×800 the real work (the table, the editor, the
  list) is on screen without scrolling and uses the width. No empty bands, no
  oversized headings, no cards holding one label and an icon, no tiles that
  show one small number, no box inside a box, no narrow centered column
  unless it is long reading text.
- **The floating assistant never covers content.** The element that actually
  scrolls the page's last content reserves bottom space for the fixed chat
  composer / assist dock, so the final item scrolls fully above it at desktop
  and phone widths (check each content mode).
- `(core)` routes: header via `<PageHeader>`; body `h-full overflow-hidden`;
  never `h-screen`, `100vh`, `h-page`; no fake title bar in the body.
- Density: **sharp** by default — clean, compact, generous only where it helps
  reading (Linear, Stripe); **dense** for all-day power pages — tables, tight
  rows, many columns (Airtable, Datadog). Name the posture and the real product
  you matched in the Change Log line; open `ui-sharp` / `ui-dense` only if unsure.
- Checks: `pnpm check:page-headers` · `check:scroll-chain:strict` · live look at
  the top edge on desktop and phone.
- Procedures: `core-route-headers` · `.claude/ui-skills/shared/application-ui-copy-and-hierarchy.md` · `ui-sharp` / `ui-dense`.

### 4 · It works on a phone
- Every desktop action exists on a phone (header actions → bottom sheet);
  functionality is gated with `useIsMobile()`, never just hidden with CSS.
- Finger-sized: the page's section roots and every `DialogContent` carry
  `matrx-touch-targets` (44px on touch, desktop stays compact — but a control's
  own `h-*`/`min-h-*` class overrides the floor, so check the rendered size); a checkbox,
  radio or switch gets `matrx-tap-area` on its label.
- Nothing hover-only — including a tooltip that carries real information (a
  limit, a reason): on touch it opens on tap (a popover), or the text is shown.
  A control revealed with `opacity-0 group-hover:opacity-100` also carries
  `pointer-coarse:opacity-100`.
- A plain `<Dialog>` becomes a bottom sheet by itself; hand-roll a Drawer only
  for a drag handle or a genuinely different layout.
- `dvh` never `vh`; `pb-safe` on anything fixed to the bottom; one scroll area;
  no tabs as phone navigation; tables reflow; popups capped with internal
  scroll; fields authored `text-base`, never an inline font size under 16px.
- Long-press opens the same menu as right-click.
- Checks: `pnpm check:phone-layout` · live look at 375×812, tapping everything.
- Procedure: `ios-mobile-first`.

### 5 · It looks like one product
- **Only our standard parts.** Buttons, icon buttons (TapButtons from
  `@ai-matrx/tap-target/buttons`), inputs, pickers, dialogs, tables and lists
  come from the design system. A hand-styled `<button>` or one-off control
  that does what a standard one does is a finding — replace it.
- Tables: `MatrxDataTable`, sort and filter on every column. Lists:
  `EntityListPage` with saved view preferences and an archive control wherever
  records can be archived. Pickers over a growable list offer
  `Create "what you typed"`.
- Dialogs open through their typed opener (`useOpenX()`), never
  `dispatch(openOverlay(...))`. No browser `confirm/alert/prompt`; `toast`
  only from `@/lib/toast`. With a layer open, the page behind stays usable.
- Lucide icons only; no emoji; no Sparkles for AI; `INTELLIGENCE_ICON` only
  for Intelligence, `AGENT_ICON` for Agents.
- Text a person reads is 12px or larger; 10px only for small all-caps section
  labels and keyboard hints. Machine labels (`some_key`) are humanized.
- **Show what a person recognizes, never an internal key** — ours or the
  data's (import paths like `Biology::Cells`, slugs, codes). A value is shown
  as its display form (proper case, platform named, a link when it is a
  link), never its normalized/dedupe key, slug, raw id or JSON. A person never
  types JSON: structured input gets real fields (an address is address
  fields, a state is a state picker, a fixed set is a select).
- **One name per thing.** The header, tab title, buttons, placeholders, empty
  and error states use the same noun (a "deck" is never also a "set").
- **Nothing internal reaches a person.** No test/fixture product names, no
  engineering notes ("no read path…", ticket codes), no placeholder copy. An
  unbuilt part is absent, or a Coming Soon entry.
- Semantic color tokens only; right in light AND dark.
- **A link is a link.** Navigation is an `<a>`/`Link` (new tab, copy, crawl),
  never a button calling `router.push`. **A status is never shaped like a
  button** — a state ("Premium is on") is a badge or a line of text, not a
  full-width filled pill where an action would be.
- **One door per action.** No button that repeats navigation the header or
  section nav already gives (a Back beside the section tabs). One create button per page (not a header "+", a
  toolbar button AND a create card); one org/scope control (the header's
  switcher — a page never adds a second organization picker).
- A destructive or expensive click says what it will cost before it happens.
  A person's records are archived (restorable), never permanently deleted from
  a page — Arman's standing rule, never a question; if the feature's reads do
  not yet hide archived rows, adding that filter to every read is part of the fix; a destructive option is never pre-checked; a one-click trash with
  no confirm is a defect.
- **Color means something.** Success color only for success, alarm color
  only for a real alarm (a zero is never green; a routine control is never
  red).
- **Charts are readable and honest:** axes and units visible and not clipped,
  a scale a person can read, they render on a phone, and a line never smooths
  across periods with no data (mark empty periods; points carry their count).
- **One fact, once.** The same list or number never appears twice on a page.
- **A section's scope is its title.** A section that covers only part of what
  the page covers (one study mode of many) says so, or is widened to match.
- Tab title leads with the specific word (on a record page, the record's
  name); follow the `route-metadata-favicons` helper's order for a record's
  sub-views. The route has a favicon entry.
- Checks: `pnpm check:ui-primitives` · `check:one-table-law` ·
  `check:archived-items-law` · `check:picker-add` · `check:canonical-pickers` ·
  `check:browser-dialogs` · `check:blocking-dialogs` · `check:popover-sizing` ·
  `check:reserved-icons` · `check:new-tab-icon` · `check:theme-color-literals` ·
  `check:route-metadata:strict` · `check:favicon-letters` ·
  `node .claude/skills/light-dark-integrity/scripts/detect-light-dark.mjs <paths> --strict`.
- Procedures: `efficient-tap-button-migration` · `canonical-table-usage` ·
  `picker-custom-entry` · `overlay-system` · `no-emojis-in-ui` ·
  `light-dark-integrity` · `route-metadata-favicons` · `compact-nav-menus`.

### 6 · Copy and AI are everywhere
- Nothing is shown that can't be copied — field, row, record, page — through
  the canonical `CopyButtons` menu (the Alchemy copy menu; Copy and Copy
  for AI live inside it).
- Every box a person writes in is `ProTextarea` / `ProInput` with the
  microphone and the page's agents (`surfaceName` + `getApplicationScope`
  passed). A bare textarea needs a comment saying why.
- A field that expects a syntax (formula, pattern, cron, JSON, filter) offers
  "Help with this…".
- A friction point gets an assist chip before anyone invents a manual button.
- Checks: `pnpm check:copy-everywhere`.
- Procedures: `agent-copy` · `components/official/ProTextarea.tsx` docstring.

### 7 · Proof and record
- Live proof for this page: desktop light, desktop dark, phone light, phone
  dark, the right-click menu, the probe output — with the URL and commit.
- `FEATURE.md` Change Log line in the same commit; manifest `readiness`
  honest (`partial` with a note naming what is unproven; `verified` only when
  everything is); anything Arman should see → `agent-review-queue` row;
  unrelated defects → `FOUND_DEFECTS.md`.

## Running it as a loop (coordinator)

The tested loop: a worker per page (`loop/worker-brief.md`), then a blind judge
per page who has never seen the worker's report (`loop/judge-brief.md`). The
coordinator sends the judge's findings back as the next iteration, gives each
shared defect one owner, and turns every miss into a rule here.

## Shared defects — report, don't skip, don't collide

A defect you see on your page that lives in a shared piece (the shell header,
the org picker, the list shell, a shared section, the right-click menu) is
never "not mine". If it is small and nobody else is on that file, fix it at the
source (step 4's second-page proof applies). Otherwise put it in your report
under `SHARED:` with file, symptom and evidence; the coordinator gives each
shared defect exactly one owner so parallel workers never edit it twice.

When YOU change a shared piece (or a sibling route's code that renders into
another page), look at every page that renders it, not just yours — a top bar
added for the public route once doubled the title on the signed-in run page.

When the page hosts content it does not own (a person's agent app, an
embedded document), its quality limits are still yours to report: give the
content the full width and the restored input through the host contract; what
only the content's author can change goes in the report as `CONTENT-OWNED:`.

## Report — one per page

```
<route> — type <x>, posture <x> after <product>, commit <sha>
My first look (step 1): <every problem I wrote down> → each: fixed / covered by rule / not fixed (why)
Core 1-7 and type additions: <n> <verdict> — <what>
Proof: <lane, URL, screenshots / probe file>
Test rows created: <table, ids>
PERSON→AGENT MAP: <each create/edit/archive control → its write target, or why none>
SHARED: <shared-component defects seen: file, symptom, evidence>
Left open: <exact remaining work, or none>
```

Checks no script runs yet: [`candidate-checks.md`](./candidate-checks.md).

**A problem from your first look that no rule covered goes in its own line:**
`RULE GAP: <problem>`. Those lines are how this skill improves.
