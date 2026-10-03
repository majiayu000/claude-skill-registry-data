---
name: ticket-diagram
layer: method
description: Attach a self-contained Excalidraw status diagram to a GitHub epic — read the epic + its sub-issue tree, render boxes-coloured-by-status with dependency arrows to a committed PNG that (a) renders on the GitHub mobile app and (b) has the editable Excalidraw scene embedded inside it, post it as a sticky comment, and round-trip human edits back in from a comment. Use when asked to "diagram an epic", "draw the ticket tree", "show the epic on mobile", "add a status graph to #NN", or to keep an epic's diagram current as its children change.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Ticket diagram — an editable, mobile-legible status graph per epic

Turn a GitHub epic's sub-issue tree into a picture: **boxes coloured by status, dependency
arrows bound to the boxes**, committed as a **single PNG** that renders in the issue/PR body
on mobile **and** carries the **editable Excalidraw scene embedded inside it** — open that PNG
in Excalidraw and you get the live scene to rearrange and hand back.

This is workstream #2 of the human-readable-tickets epic ([#479](https://github.com/FriendlyInternet/nuxt-crouton/issues/479))
made concrete, tracked under epic [#483](https://github.com/FriendlyInternet/nuxt-crouton/issues/483). It
reuses the **sign-off / revision loop** of #310 (the same loop `ui-proposal` and `schema-review`
use): generate → post on the PR → iterate on feedback → approve.

> **Why Excalidraw + a PNG?** Mermaid is **disqualified**: on the GitHub *mobile* app a
> ```` ```mermaid ```` block shows raw code + a perpetual "Loading" spinner (confirmed on #479).
> A committed PNG renders everywhere, including mobile, with no stall. The scene is **embedded in
> the PNG** (Excalidraw's own "Embed scene" format), so the image is *also* the editable source —
> no separate verbose `.excalidraw` file in the repo.

## Artifacts (what gets committed)

Per diagram, in `writeups/diagrams/`:

- **`<slug>.graph.json`** — the small, **diffable semantic source** (nodes + status + edges).
  This is the human-auditable record; `git blame`/diffs of *what the epic is* live here.
- **`<slug>.png`** — the **render + embedded editable scene** in one file. Shows in the issue
  body on mobile; open it in Excalidraw to edit.

The loose `<slug>.excalidraw` is **not committed** (it's gitignored) — the scene rides inside the
PNG. Pass `--excalidraw` to the generator only if you want a loose copy locally.

## The pipeline (two halves)

```
  YOU (over the GitHub MCP)            the GENERATOR (deterministic, offline)
  ────────────────────────            ──────────────────────────────────────
  read epic + get_sub_issues   ──▶    scripts/ticket-excalidraw.mjs <graph.json>
  build the graph JSON                  → writeups/diagrams/<slug>.graph.json   (semantic source)
                                        → writeups/diagrams/<slug>.png          (render + scene embedded)
```

The split matters: **the agent does the GitHub I/O; the script does the graph→artifacts step**
(no network at render time, byte-stable output → minimal diffs).

## 1 · Read the epic → build the graph JSON

For epic `#NN`: `issue_read` (get) the epic, then `issue_read` (get_sub_issues). For each child
read its **title**, **state** (open/closed), **labels** (`status:*`), and any `Blocked-by: #x, #y`
line in the body. Then build:

```json
{
  "epic": 479,
  "slug": "make-tickets-human-readable",
  "title": "Make tickets human-readable",
  "feedbackUrl": "https://github.com/FriendlyInternet/nuxt-crouton/pull/487",
  "nodes": [{ "id": 454, "title": "Schemas + config", "status": "done" }],
  "edges": [{ "from": 454, "to": 455 }],
  "goal": { "label": "library-catalog.pmcp.dev" }
}
```

- **status** per node — `closed → done` · label `status:in-progress → in_progress` ·
  `status:blocked → blocked` · otherwise `pending`.
- **edges** — `Blocked-by: #x` on child `C` ⇒ edge `{ "from": x, "to": C }` (arrow points from
  blocker to dependent; the generator lays blockers above dependents).
- **goal** (optional) — add it when the epic's acceptance is a concrete artifact (e.g. a preview
  URL). Every terminal node wires into it; it's coloured violet.
- **ref** (optional, per node) — top-line label override (e.g. `"W2"`) for nodes that aren't real
  issues, like an epic's workstreams before it's decomposed. Defaults to `#<id>`.
- **feedbackUrl** (optional) — makes the diagram's footer a clickable **"💬 Comment or send edits"**
  link; pass the **PR URL**. Defaults to the epic issue URL.
- **slug** — kebab-case; drives the filenames. Reuse the same slug every regeneration so the diff
  stays small and the sticky keeps pointing at the same files.

## 2 · Generate

```bash
node scripts/ticket-excalidraw.mjs /tmp/<slug>.graph.json --out-dir writeups/diagrams
```

Writes `<slug>.graph.json` + `<slug>.png` (PNG via the **shared** renderer
`.claude/skills/ui-proposal/render.mjs`, headless Chromium — same as `schema-review`; the scene is
then embedded into the PNG). Then **commit both** with `/commit`, referencing `(#NN)`.

## 3 · Post the sticky comment & iterate (the #310 loop)

Post the PNG as a **single sticky comment** on the epic's PR, marked with an HTML anchor, and make
the image a link that opens the scene in Excalidraw:

```markdown
<!-- ticket-diagram:make-tickets-human-readable -->
### 🗺️ Epic diagram — Make tickets human-readable
![epic diagram](https://raw.githubusercontent.com/FriendlyInternet/nuxt-crouton/<branch>/writeups/diagrams/make-tickets-human-readable.png)

**✏️ To edit:** download this PNG and **open it in Excalidraw** — the scene is embedded, so it
opens live; drag boxes (arrows follow), then **export it (Embed scene ON) and attach the PNG to a
comment here**. I'll pull your edits back in.

_Revisions:_
- r1: initial
```

Reference the PNG by its **raw.githubusercontent.com URL on the branch** so it renders on mobile.
The human reviews **on the diff**: they inline-comment, or they edit the scene and **attach the
exported PNG** to a comment. Both are change requests. **Ignore bot/self comments**
(`user.type === 'Bot'`).

**Approval** = a **comment** containing `approve`/`lgtm`. (A 👍 reaction or a label does **not**
resume the pipeline — only `issue_comment` triggers `resume-on-comment.yml`, #572.) On approval,
mark the PR ready / merge per the epic flow.

## 4 · Round-trip a human edit back IN

When a human attaches an edited, scene-embedded PNG (or a `.excalidraw`) to a comment, grab its
URL and run the importer — it decodes the scene, **re-renders the PNG from that scene** (so boxes
they moved stay moved), re-embeds the scene, and writes the committed PNG:

```bash
node scripts/ticket-excalidraw-import.mjs <attachment-url-or-path> --slug <slug> --out-dir writeups/diagrams
```

Commit the PNG and refresh the sticky (append `- rN: <what changed>`). Pair this with
`subscribe_pr_activity`: a comment with an attached PNG → run the importer → commit → done.

## 5 · Keep it current (it's a live view, not a one-shot)

When the epic's children change — a new sub-issue, a child closes, a `Blocked-by` edge changes —
rebuild the graph JSON and regenerate. Same slug ⇒ the PNG updates in place and `graph.json`'s diff
shows exactly what moved semantically. (Regenerating from `graph.json` re-lays-out the boxes; if a
human has hand-arranged the scene, prefer the importer in §4 to preserve their layout.)

## Status palette

| status | colour | meaning |
|---|---|---|
| `done` | 🟩 green | child issue closed |
| `in_progress` | 🟦 blue | `status:in-progress` label |
| `blocked` | 🟥 red | `status:blocked` label |
| `pending` | 🟨 yellow | open, not started |
| goal | 🟪 violet | the epic's concrete acceptance artifact |

## Files

- `scripts/ticket-excalidraw.mjs` — CLI: graph JSON → `.graph.json` + scene-embedded `.png`.
- `scripts/ticket-excalidraw-import.mjs` — CLI: an edited (scene-embedded) PNG / `.excalidraw` →
  re-rendered, re-embedded `.png` (the round-trip IN).
- `scripts/lib/excalidraw.mjs` — pure emitters: `layout()` (layered DAG), `toExcalidraw()` (bound
  arrows + bound text + chrome), `toSvg()`/`toHtml()` (graph render), `sceneToSvg()`/`sceneToHtml()`
  (faithful render of an *edited* scene). No dependencies.
- `scripts/lib/excalidraw-png.mjs` — dependency-free PNG metadata codec: `extractScene()` /
  `embedScene()` (Excalidraw's "Embed scene" tEXt format; Node `zlib` + manual chunk parsing).

## Gotchas

- **The PNG is both the render and the editable source** (scene embedded). Never put a
  client-rendered diagram (Mermaid/widget) in a GitHub body — it must be a committed image so it
  shows on mobile.
- **Editing = open the PNG in Excalidraw**, not a `#url=` deep link — that needed a hosted
  `.excalidraw`, which we no longer commit. (If you want one-tap deep-link editing back, run the
  generator with `--excalidraw`, commit the loose file, and link `https://excalidraw.com/#url=<raw
  url>`.)
- **One-tap mobile editing = the hosted `ticket-editor` Worker** (`workers/ticket-editor`, epic
  #483). Link `…/?slug=<slug>&branch=<branch>&issue=<NN>` — pass **`&issue=<NN>`** so each Save
  posts a **new** comment on issue `NN` with that edit's diagram (a timeline of versions, not just
  silent `nuxt-harness[bot]` commits). Requires the loose `<slug>.excalidraw` committed (generate
  with `--excalidraw`), since the editor reads it.
- **Pin a diagram image you want to stay put to its commit, not the branch.** A
  `raw.githubusercontent.com/<repo>/<branch>/…png` URL re-renders whenever the file is later
  edited (so a "proposal" comment's picture drifts); `…/<commit-sha>/…png` is immutable and frozen.
  Post the proposal/sticky image pinned to the commit that produced it so the timeline reads
  correctly (the editor's per-save comments already do this).
- **Round-trip needs "Embed scene" ON** in Excalidraw's export, or the importer can't find the
  scene (it errors clearly).
- **Reuse the slug** across regenerations, or you'll orphan the old PNG and the sticky image link.
- If the epic has **no sub-issues yet**, diagram its workstreams as `ref`-labelled nodes (e.g.
  `W1`…`W5`).
