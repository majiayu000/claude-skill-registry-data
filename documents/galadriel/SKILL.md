---
name: galadriel
description: Use when the user runs /galadriel [folder]. Renders a folder of plan concepts (markdown, default docs/plans/) into one local HTML page — a left selector grouped by lifecycle (shaping/active/done), the chosen concept's preview in the main area, and a progress dashboard along the bottom. Edits are directed in chat; while the standing server is up it watches every registered project's plans folder in the background and re-renders on its own within a few seconds of any concept file changing, so no manual re-render is owed. The one change the page makes itself is deleting a concept, which moves it to the plans folder's .trash/ and needs the standing server. The Mirror shows what was, is, and may yet be — done, in-flight, pending.
purpose: Renders a local dashboard mirroring a folder of plan concepts and their step progress.
user_invocable: true
stage: plan
---

# Galadriel

A local HTML mirror of your plan concepts. Each concept is one markdown file in a
plans folder; the page shows them all behind a left selector, renders the chosen
one, and tracks its step progress in a dashboard below. To manipulate a concept
(reorder, reword, add, cut steps) the user tells you in chat; you edit the file and
re-render. The page makes exactly one change of its own — deleting a concept, which
moves the file to `.trash/` rather than unlinking it, and only while the standing
server is up.

## Concept file format

One `.md` file per concept under the plans folder (default `docs/plans/`):

```markdown
# Concept title

Intro prose — the overview. Everything before the first step or heading.

## Steps
- [x] A finished step <!-- sha: a1b2c3d, e4f5a6b -->
- [~] The step in flight   (or - [>])
- [ ] A step still pending
```

Lifecycle is **derived**, never typed: no steps → *shaping (draft)*; some steps,
not all done → *active*; every step done → *done*.

A step may name the commits that landed it with a trailing
`<!-- sha: <sha>[, <sha>...] -->` marker. The renderer runs `git show` for each
sha against the project repo (resolved from the plans folder, or passed as the
third argument) and tucks the patch behind a per-step **diff** toggle in the page.
The marker is stripped from the displayed label; a bad sha shows a plain
"diff unavailable" note rather than failing the render.

A concept may name a mockup with a `<!-- preview: <file.html> -->` marker (path
relative to the plans folder). The renderer inlines that HTML into a read-only,
sandboxed `<iframe>` in the main area above the steps — a UI preview to eye, not
to edit. You generate the mockup HTML in chat (per the Visual Review convention) and
drop it beside the concept; a missing file shows a "preview unavailable" note.

## Workflow

### 1. Resolve the plans folder

The argument names it; absent, default to `docs/plans/` in the current project.

- If the folder is missing, create it with one starter concept (`docs/plans/example.md`)
  bearing the format above, and tell the user plainly that you seeded it.
- If it exists but holds no `.md`, render anyway — the page shows "No concepts".

### 2. Render

**The dashboard is not a Henneth artifact.** Henneth holds *static* previews —
wireframes, diagrams, screenshots. This page is a small application: it keeps view
state in `localStorage`, polls its own URL to live-reload, and has drag-resizable
panes. It gets its own home, one per project, so two repos never overwrite each
other's mirror:

```bash
PROJ=<project>
DEST=~/.claude/galadriel/$PROJ/plan-dashboard.html
mkdir -p "$(dirname "$DEST")"
~/.claude/hooks/galadriel-render.py <plans-folder> "$DEST"
printf '%s' <plans-folder> > ~/.claude/galadriel/$PROJ/source
```

`<project>` is the plans folder's repository name — the basename of
`git -C <plans-folder> rev-parse --show-toplevel`, or of the folder's parent when
it is not a repo. Keep it **stable**: the path is what an open tab holds across
re-renders, and a changing name orphans the tab.

**The `source` marker is not optional.** It records which plans folder this
mirror was rendered from, and the server resolves every delete through it
(`galadriel-server.py`, `concept_path`). Without it the page still renders and
still shows its delete controls, but every delete answers 404 — a failure that
looks like a bug rather than a missing file. Write it on every render.

The renderer parses every `.md`, derives lifecycle, and writes one self-contained
HTML file — no external assets, no build step.

### 3. Boot or reuse the standing server

One server serves every project's mirror, exactly as one Henneth window serves
every artifact. Whichever session runs `/galadriel` first boots it; the rest reuse
it.

**Reuse before booting.** Read `~/.claude/galadriel/.galadriel-port`. If it names a
port that answers a quick GET to `http://localhost:<port>/index.json`, the server
is already up — print the URL and launch nothing. A lockfile alone proves nothing:
a killed server leaves its port file behind.

**Otherwise boot it in the background**, detached so it outlives the turn. The
port is fixed at **10002** (override with `GALADRIEL_PORT`) so the URL never
drifts across restarts:

```bash
~/.claude/hooks/galadriel-server.py ~/.claude/galadriel "${GALADRIEL_PORT:-10002}"
```

It records its own port in `.galadriel-port` on boot. If the port is already
held by something other than a dead Galadriel server, the bind fails and the
process exits at once — report that plainly rather than silently retrying on a
different port.

**Then surface two URLs** — `http://localhost:<port>/` for the index of every
project, and `http://localhost:<port>/<project>/plan-dashboard.html` for the one
just rendered.

**Say what the page can do**, in a line, the first time a mirror is served in a
session. A user who is not told will not find it: the affordances are a `◀` and a
`☐`, and nothing on screen explains either. Name the three — the sidebar collapses
with `◀`; the panes drag-resize; and `☐` enters selection mode, where checked
concepts can be moved to `.trash/`. Without that line the delete feature is
present and invisible.

**Why a server at all, when the page opens from disk.** Reading needs none: over
`file://` the selector, preview, dashboard, collapse and resize all work. Two
things need HTTP. Auto-reload — the page polls its own URL and refreshes when the
bytes change (`galadriel-render.py:538`); over `file://` that fetch is refused and
the call swallows its own failure, so the page is whole but will not refresh
itself. And **deleting** — `DELETE` is an HTTP verb, so from disk the selection
controls are removed outright rather than offering a button that cannot work.

If the port will not bind or Python is absent, render anyway and print the
`file://` path, saying plainly that deleting is unavailable until a server stands.

### 3b. Deleting a concept

The `☐` button beside the sidebar toggle enters selection mode: each concept gains
a checkbox, and a **Delete selected (N)** bar appears. Confirming moves each chosen
`.md` into `<plans-folder>/.trash/` and re-renders.

**Nothing is unlinked.** Restoring a plan is moving its file back out of `.trash/`;
emptying the trash is yours to do by hand. The renderer never sees it, because
`collect()` globs the top level only.

Since `.trash/` sits inside the repo's plans folder, add it to `.gitignore` when a
project first uses the feature:

```
docs/plans/.trash/
```

A delete that fails is reported in the page and its concepts stay selected — it
does not reload into a view that looks as though everything worked.

### 4. The edit loop

Every edit but deleting happens in chat. When the user asks to change a concept — "swap steps 3 and
4", "mark the decorator done", "cut the last step", "add an overview" — edit the
concept's `.md` file directly. **No manual re-render is owed while the standing
server is up** — it watches every registered project's plans folder in the
background (`galadriel-server.py`'s `watch_forever`, polling every
`WATCH_INTERVAL_S` seconds) and re-renders on its own the moment a concept file
changes, whoever changed it. The path does not change, so the open tab stays
valid; served, it refreshes itself within a few seconds of the re-render. Cutting
a concept entirely is the one edit the page does itself — see *Deleting a
concept* above. The sidebar collapses via the `◀` beside the brand, and that
state persists; it needs nothing from you.

This is how "manipulate before you start" works: shape the draft concept by chat
until it reads true, then begin the work — ticking `- [ ]` to `- [~]` to `- [x]` as
each step lands; the mirror catches up on its own. When a step's commit lands,
stamp its sha into the step's `<!-- sha: ... -->` marker so the page can show
that step's diff behind its toggle.

## Notes

- **Defers authoring to you and the user.** The skill renders; it does not invent
  plan content. `/rumil` is the authoring half — it translates a product spec into
  a concept file in exactly this format, and writes it straight into the plans
  folder. Any other planning skill works too, so long as its output matches the
  concept format above.
- **Per-project by default.** `docs/plans/` lives with the repo and travels with it.
  Point the argument elsewhere for a one-off folder.
