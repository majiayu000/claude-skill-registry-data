---
name: user-story-map
description: Build an interactive, drag-and-drop user story map so the user can re-slice work across release phases. Use when the user wants a story map, a phased roadmap, release slicing, a backbone/activities journey map, or to decide "which stories go in which phase" and move them around.
---

Produce a **self-contained, interactive** user story map the user can operate: drag story cards between cells to re-slice which phase (and activity) each belongs to, reorder phases/activities/stories by dragging, edit inline, add/remove cards, phases, activities and tags, and export the result. It runs in a real browser — served live from this session by default, published as an Artifact when it needs to travel.

## The three axes (get these right)

A story map has exactly three dimensions — clarify or infer all three before building:

1. **Activities (backbone)** — the columns, left→right, the user's journey / the sequence of high-level things they do (e.g. *Set up the role → Bring in candidates → Screen → …*). Order carries meaning; the user can re-drag it.
2. **Phases (swimlanes)** — the rows, top→bottom = release order (Phase 1 = first / MVP). Each has a name and a one-line goal. The user can re-drag the order.
3. **Stories** — the cards. Each belongs to exactly **one activity + one phase**; order within a cell is its rank (top = first). Each has a `status` — `open` (default) / `progress` / `review` / `done` — and the card's left border accent is coloured by status (cells are tinted by phase; a legend above the grid explains the colours — status never renders as a pill, pills are for tags). Omit `status` unless the context clearly says work has started. Keep the text short and recognizable to a user (what they can do), not implementation detail.

**Tags are cross-cutting themes**, not a card property to colour by. A story may carry any number of tags (e.g. `"AI"`, `"compliance"`); they render as small pills on the card, and the user can add/remove them per card or delete a tag everywhere via the ⌗ menu. Cards are always coloured by phase — never invent per-card colours. Seed tags only for genuine cross-cutting concerns you can identify (AI/automation is the common one).

Derive these from whatever context exists — a spec, a plan, a `tasks.md`, a development plan, the conversation. If the subject or its journey is unclear, ask briefly: what's the product, what are the ~5–9 journey steps, and how many release phases.

## Build steps

1. Read `assets/story-map-template.html` (next to this file). It is a finished engine + design — **do not edit the CSS or the `<script>` engine**; the shell chrome is stamped in from `lib/shell/` (see `lib/shell/README.md`).
2. **Write the map as JSON.** Served (the default), that file *is* the map and the template is used unmodified — the page loads the JSON over the live link. For an Artifact, the page has to carry its own data instead: copy the template and replace **only** two things — the `<title>` at the top and the JSON inside `<script id="data" type="application/json">…</script>`. Schema either way:
   ```json
   {
     "title": "…",
     "lang": "en",
     "tags": ["AI"],
     "activities": [{ "id": "a1", "name": "…" }],
     "phases":     [{ "id": "ph1", "name": "Phase 1", "goal": "one-line goal" }],
     "stories":    [{ "id": "s1", "activity": "a1", "phase": "ph1", "text": "…", "tags": ["AI"], "status": "open" }]
   }
   ```
   **The title is the product/initiative name only** (e.g. "Cavalry Hiring") — never append "Story Map", "— Story Map" or similar; the page's eyebrow already labels it a user story map. There is **no subtitle/description field** — the phase/activity goal lines carry the context. `lang` is optional and sets the initial UI language (`"en"` default or `"zh"`); the UI has an EN/中文 toggle either way, so set `"zh"` only when the user is clearly working in Chinese. The toggle switches UI chrome only — author titles, goals and story text in the user's language. Every `id` is a unique string; every story's `activity`/`phase` must match an existing id; every story tag should appear in the top-level `tags` list. Array order = display order. Colours are auto-assigned per phase (6 distinct hues, then cycle) — don't specify them.
3. Write it to a working directory — `.vstack/maps/<slug>.json` under the project, or the scratchpad if the project shouldn't gain files.
4. **Serve it with the bridge** (default) so the user's edits come straight back to you — see *Live link* below. Publish as an Artifact **instead** only when the map is meant to be shared with other people, or when no local browser is in play: fill a copy of the template as in step 2, then `Artifact` with favicon `🗺️` and a one-line `description`. Both modes are theme-aware and need no other changes; the page adapts its own export bar to whichever it's in.
5. Tell the user how to use it: **drag any card into another cell** to re-slice its phase/activity, and drop above/below other cards to rank it; **drag a phase rail or activity header** onto another to reorder rows/columns (the whole column/row slides live while dragging — grab the ⠿ tab protruding from the top of a column or the left of a rail); double-click text to edit; hover a card for ● (status dropdown) / ⌗ (tags) / ×; the **Bulk select** button (top right) shows the bulk bar and lets them click any card to select it, for group status/tag/delete; the dashed **＋ story / ＋ activity / ＋ phase** buttons in the grid grow it; **Import** loads a saved map; the **EN | 中文** toggle at the top right switches the UI language. The primary export button is **Send to Claude** when bridged (Copy to Clipboard and Download JSON move under the ▾) and **Copy to Clipboard** when not.

## Live link (bridge)

`lib/json-bridge.mjs` — the shared engine the experimental `spec` and `phase-build` also run on — serves the map on `127.0.0.1` and links it to this session in both directions. The page detects the bridge on its own; the template is served unmodified.

1. **Start it** with Bash `run_in_background`:
   ```bash
   SKILL=<this skill dir>
   LIB="$SKILL/../../lib"
   MAP=.vstack/maps/<slug>.json
   node "$LIB/json-bridge.mjs" serve --json "$MAP" --template "$SKILL/assets/story-map-template.html" --port 0 --tool user-story-map
   ```
   It opens the map in the browser and prints the URL (with its token) and the seq path. Give the user the whole URL too — the token is required, and a machine that could not open a browser still needs it. `--no-open` leaves the screen alone.
2. **Start the watcher** so their click reaches you with nothing typed — the **Monitor tool**, `persistent: true`:
   ```bash
   node "$LIB/json-bridge.mjs" watch --json .vstack/maps/<slug>.json --stream --tool user-story-map \
     --seq <the seq the server printed>
   ```
   How the loop behaves — it never exits, one event per line, the Linked/Unlinked states, the idle
   close — is [`contracts/bridge-loop.md`](../../contracts/bridge-loop.md).
   On `SENT`, read the map JSON — that is the new source of truth. On `APPROVED`, the map is signed
   off: carry on with what comes next. On `CLOSED`, the user shut the tab; say the link is closed.

   **Pass the seq the server printed, not a fresh `$(cat "$S")`.** The stream carries its own position from there, so nothing that lands mid-round can be swallowed.
3. **Push back to the open page** by writing that JSON file yourself. The tab shows *"Claude updated this map — Refresh / Dismiss"*; it is never applied silently, so in-progress dragging is never clobbered. The bridge does not echo the page's own saves back at it.

Single-card changes can go through the engine's patch command instead of a full rewrite:

```bash
node "$LIB/json-bridge.mjs" patch --json "$MAP" --id s12 --set status=done --tool user-story-map
```

### Closing the link

Closing the browser tab closes it — the idle-close behaviour, the *Link lost* state and why nothing
is lost are [`contracts/bridge-loop.md`](../../contracts/bridge-loop.md). Close it early with
TaskStop on the server task; `--idle-timeout 0` keeps it up until then.

## Notes

- **Self-contained** — no external fonts/scripts (Artifact CSP-safe). Drag-and-drop is native HTML5.
- The bridge is **strictly optional to the page**: it injects a `window.__VSTACK_BRIDGE__` handle when it serves the template. Opened as an Artifact or straight off disk, the same file runs on its inline `<script id="data">` block and keeps edits in `localStorage`. Served, the JSON file is the map and `localStorage` is ignored on load — otherwise a stale arrangement would outrank the one Claude is holding.
- This is a *planning* tool, not a document — favour a clean, operable grid over prose. Keep story text to a short phrase; the goal lines on phases/activities carry the "why".
- If the user later sends back (or pastes) an edited JSON, treat it as the new source of truth for re-slicing any plan/roadmap you generated from it. Old JSON with the legacy `"ai": true` flag still imports — the engine converts it to an `"AI"` tag.

## State & handoff

**No `.vstack/pipeline.json`?** You're standalone — a plan, a `tasks.md` or a conversation is enough.
Everything above still applies; skip this section, and write the map wherever suits (default
`.vstack/maps/`). **Never create the state file here** — a half-written one is worse than none,
because the next stage would trust it. Nothing currently shipped brings a pipeline into being: the
tool that did, `start`, is parked in `plugins/vstack/experimental/`. **Standalone is the normal
case**, and the section below applies only to a project that already has the file.

With a state file:

- **Read** `artifacts.specs[]` — the specs are the stories, and the map's job is to say *when*, not
  to reopen *what*. `artifacts.product` for the goal the phases serve.
- **Write** the map to `specs/story-map.json`. That exact path is what `phase-preview` and
  `phase-build` read — both experimental, so this matters for a project that used them or will when
  they return, not for anything shipping today. Then set
  `artifacts.storyMap` and `stage: "user-story-map"`, and add a `history` entry noting the phase
  count.
- **Write it when the user has finished re-slicing**, not on the first send. A map is dragged
  several times in one sitting; the state should record where they stopped, not where they passed
  through.
- **Phases here define the phases everywhere after.** `phase-build` owns the phase *counter*, but
  the number of phases and what falls in each is decided on this page — renumbering later invalidates
  every phase screen already cut.
- **Next** — nothing to offer: the phase tools that used to follow this stage are not currently
  shipped as skills. End with the finished map and where it was written.
