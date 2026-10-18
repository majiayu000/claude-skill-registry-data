---
name: design-loop
description: Design an atom or screen in OpenPencil, implement it with a Storybook story, ship it. Use when asked to design, mock up, or add a component or screen, or to link a story to its design.
---

# Design loop (OpenPencil <-> Storybook)

Source of truth for tokens: `web/src/styles/tokens.css`. Design file:
`web/design/hikyo.pen` (JSON, committed). Both MCPs are installed (`open-pencil` is a
user-level MCP, not in the repo; `addon-mcp` is in `main.ts`): `open-pencil`
needs the app running with the file open, `addon-mcp` needs the dev server on
6006.

## 1. Design

`.pen` is read-only in OpenPencil 0.15.0, as in 0.14.0: `openpencil formats` reports
`pen: support: read`, and `save_file` writes a `.fig` zip container even when
handed a `.pen` path. The app is a viewer and inspection surface; edits made
inside it cannot be saved back as JSON. Never call `save_file` onto
`web/design/hikyo.pen`, it would replace the JSON with a binary. Upstream
follow-up: a `.pen` writer (a contribution) would restore the round trip.

So `web/design/hikyo.pen` is edited as JSON. Two routes:

- Write the JSON directly, by hand or by an agent, using the `open-pencil` MCP
  read tools (`get_node`, `node_tree`, `get_jsx`, `find_nodes`) to inspect what
  is already there.
- Or prototype in the app with the write tools (`create_shape` / `set_layout` /
  `set_text` / `rename_node` / `node_to_component`), then export the affected
  node with `get_jsx` or `node_tree` and transcribe the result into the JSON.
  Nothing in the app reaches disk on its own.

Either way:

- `open_file` `web/design/hikyo.pen` to inspect. Never `new_document`.
- Bind every fill, stroke, and radius to a variable, and any size that has a
  token (`$--touch` for the 44 px touch target); raw values where a token
  exists are a review finding.
- Name it `Title/Variant` and give the frame `"reusable": true` in the JSON
  (the Button pilot frames carry that flag; `node_to_component` sets it in the
  app, but that change only lands on disk once transcribed). Screens follow the
  same rule (`Members/Empty`). `design()` rejects anything else: letters,
  digits and single spaces, at least two segments.
- Node names are the only structure. A `.pen` file in OpenPencil 0.14.0 has no
  pages: the reader builds exactly one implicit page named after the first
  frame in `children`. Do not add page wrappers. A `type: "page"` or
  `type: "canvas"` node is read as a plain frame, and a top-level `pages` array
  crashes the reader. Keep `Title/Variant` names and add new frames as siblings
  under `children`.

## 2. Implement
- `get_codegen_prompt`, then `get_jsx` for the node.
- Write the component in `web/src/ui/` (atom) or `web/src/routes/` (screen)
  using the same custom properties.
- Story: `parameters: { design: design('Title/Variant') }` with
  `import { design } from '../../.storybook/design.ts'`.

## 3. Verify
- `pnpm --dir web run design:export` (runs the token check first).
- Open Storybook, compare the Design panel with the rendered story, flip the
  theme toolbar for light and dark.
- The exported image is the design file's default mode, which is Dark, the
  same default as the app. Light is only visible by switching the Mode in the
  app.
- The pencil button in the toolbar opens the node in the app.

## 4. Ship
- Normal PR. The `.pen` diff is reviewed like code.

## Token changes
Edit `tokens.css` and `DESIGN.md`, then `pnpm --dir web run design:seed`.
Never edit variables in the app; the check compares hex for hex and fails the build.
Not mirrored into the design file, so nothing can bind to them: `--ease`,
`--dur`, `--font-ui`, `--font-mono`, and any `color-mix()` token (currently
the `-soft` set).

## Bootstrapping from an existing component
Prefer `clone_node` over the `open-pencil` MCP, which mints fresh ids for the
whole subtree, then rename the clone. Or author the frames in the app
(`create_shape` and friends) and transcribe them back with `get_jsx` /
`node_tree`, since the app cannot write `.pen`.

If you copy node JSON by hand instead, give EVERY node in the pasted subtree a
new `id` and remap any reference inside it to the old ids: the reader registers
nodes by id, so a pasted subtree that keeps the original's ids aliases and
overwrites the original's entries and renders the wrong node. `pnpm --dir web
run design:export` refuses a document with a duplicate id before exporting. `openpencil import` is not usable here: it runs under Node since
`@open-pencil/cli` 0.15.0 (#575), but its `-f` is `fig` or a DOM/CSS `json`
dump, so it cannot produce or extend a `.pen`.

## Troubleshooting
- **App shows as not connected to MCP.** The desktop app attaches to the MCP
  server named in `~/Library/Application Support/OpenPencil/mcp.json`. If a
  stale `openpencil-mcp-http` from an earlier session still owns port 7600, the
  app never attaches. Kill the stale server, delete the stale `mcp.json` and
  `mcp.sock`, relaunch the app.
- **Never leave an `openpencil-mcp-http` running after a test.** Kill dev
  servers by PID only, never by port sweep or name match.
- **The middleware cannot open a repo under a dot-directory.** The app's Tauri fs
  scope uses `**`, which skips dot-directories. When a checkout has a hidden
  ancestor directory, open the file once through the app's own dialog in the
  same session before using the middleware. Checkouts without hidden ancestor
  directories are unaffected.
