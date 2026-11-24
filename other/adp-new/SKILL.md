---
name: adp-new
description: "Create a brand new Claude Artifact or Sites page on ADP (adp/2): a page, board, tracker, assistant or record page that people and Claude will keep editing. Load it whenever the user asks for a new artifact that will be kept, changed again, commented on or built from catalog parts, before writing any HTML. Covers the starter and assistant templates, taking a theme from the catalog, the first publish, and the one-time editor open that seeds the database."
metadata:
  version: "2.3.0"
---

# New ADP artifact

**Sites host:** read the base ADP skill's `refs/sites.md` first. Use the shared
scaffolds and catalog below, then that guide's native Sites build/publication and
record workflow instead of the Claude-only publish/seeding steps here.

Start on adp/2, not a single index.html: a one-file page cannot give per-file hashes, content as data or part-id comment anchors.

`ADP` below means `python3 -I <adp skill folder>/scripts/adp.py` (the folder of the `adp` skill). `ADP templates` lists the templates `new` can start from: `starter`, `assistant` and `default`.

## 1. Choose a tier

| Start | Command | What you get |
|---|---|---|
| minimal | `ADP new --tier minimal DIR` (the same as `ADP new starter DIR`) | blank page, welcome view, settings view, wearing `theme.default` (the catalog page's look); it takes `kit.dom`, `kit.tokens`, `kit.vocab` and the settings, inbox and namespaces patterns the settings view is built from |
| assistant | `ADP new assistant DIR --theme default --catalog CATALOG` | the starter plus Claude pane, requests, presence, the canvas, and every catalog theme with a switch in the header |
| default | `ADP new --tier default DIR` | the assistant plus 3D and the most useful common kits |
| full | `ADP new --tier full DIR` | not available yet (the published catalog, later): it exits with that message |

Default to the assistant when people and Claude use the page together. Ask the user only if the purpose is unclear. Every page wears a theme, so the commands spell out `--theme default`: that is where you choose another (`--theme glaze`; leaving the flag out also gives `default`). `--theme` takes a theme's short name or entry id and lists the themes when it does not know one; `--layout` takes the entry id in full (`layout.topbar`). Both add their `<link>` tags to index.html. A theme is linked after `styles/page.css` and is tokens only, so it wins over the fallback tokens there: for a palette of your own, set the tokens in page.css and remove the theme's link. The assistant and default pages carry every catalog theme: viewers switch in the header and an editor sets the page's theme in Settings (`look.theme`), so there `--theme` picks the one the page opens with. `ADP kit list CATALOG --kind theme` shows the themes. CATALOG is the catalog url (its fetched index), `-` for the saved catalog, or `~/.adp/catalog/catalog.json`; see `adp-catalog`. A local catalog.json is a build, not the live catalog, and prints a warning: do not publish from it.

## 2. Create the project

1. Run `ADP new assistant DIR --title "<name>" --by <your session name> --theme default --catalog CATALOG` (`--slug`, `--data FILE|DIR` are optional; `--content FILE` only with the starter). It writes the page into DIR (`index.html`, `content.js`, `parts/`, `styles/`; the template's `.txt` suffix is dropped) plus `seed.json` and `seed/`, and prints ONE publish object (`files` already carries the taken kit entries), the `take` list, a `design` note and the ordered `next` steps. Follow `next`.
2. Change the look and copy for the user's content: write `styles/page.css` and the views (`design` says what to keep: the token names, the part markers, the selectors `adp.js` relies on). The starting look is the catalog page's shell; two pages must not ship looking the same. `ADP new starter DIR --content FILE` builds the views from a content file (`## Lead` text, then `## View: <label> (id: <id>)`, under each `### Section <id> - <title>` followed by one fenced html block, used verbatim). The assistant and default templates keep their own Home view (welcome, examples, next steps, about): replace its copy in `content.js` and its views in `parts/app.js`, or hide them, so the page opens on the user's content. `adp.py` parses the object after `window.ADP_CONTENT =` in `content.js` as strict JSON: leave no trailing comma (legal in JS); observed: one made `ADP files` crash with a traceback while `ADP check` still passed.
3. `ADP check DIR` must pass: markers balance, ids valid and unique, every part has `data-part`.

## 3. Publish

- Run the Artifact tool with the `publish` object `new` printed (`file_path`, `root`, `files`, `capabilities`); add a `label` of at most 60 characters and, on the first publish, an `icon`. Re-run `ADP files DIR` for the arguments after you changed files, then compare its `files` map with the one `new` printed. When `files DIR` returns fewer entries, publish with `new`'s map plus the files you added since (for example `parts/journey.js`). It does not repeat `capabilities`: pass them on the first publish only, a republish keeps them. `file_path` and `root` are relative to where you ran the command; pass absolute paths when you are not in that folder.
- Choose the `files` map by tier. Default tier: `installed.json` is a local file that lists the kit entries, and publish only the plain-path entries (the artifact shows 10 files and no `kit/`, yet the page runs with all 83 entries). Minimal tier: no `installed.json` exists and `index.html` loads `kit/*.js` by path, so pass the kit references too. Judge the publish by opening the page, not by the file count: on the default tier compare the My catalog view's "N installed" with the entries in `installed.json`.
- Over 250 files `files` becomes `batches`: publish the page with the first and send the rest to the same url.
- Record the publish result with `ADP ack DIR --result FILE` (or on stdin) after `ADP export DIR --url URL` has run once (road `adp-edit`). On a brand-new page skip it: `ack` answers `no export yet` until then, and the first export takes the live version (`--version V` from the publish result); the next republish of the page starts with that export (road `adp-edit`). `ADP check` prints one warning on every assistant page, `part roots without data-comment-target: page.assist`: the Claude pane is not a place to comment on, so it is expected.

## 4. Seed the database

You run nothing: the page expands `seed.json` and `seed/` into the database itself on its first open by an editor, and a client set to open pages on publish does that at once. Until it is seeded the db has no `manifest/current`, and the edit road cannot hold or record anything. If you need to know, read ArtifactData `get` on collection `manifest`, doc `current`. If it exists, the page is seeded: write nothing, because an unpinned batch onto existing documents is refused (observed: `parts/page.changes` already existed and nothing was written). Only when it is absent and nobody can open the page as an editor, run `ADP seed DIR --by <you> --batches` and write the printed ArtifactData batches yourself (the db rules let an editor write them); the page then does not expand the seed again. Tell the owner in one line which case you found. If you cannot write to the db either, say so.

## Page code

The page's own script reaches the database through the runtime: `ADP.ns('shared').doc('board/main')` and `.collection('cards')` return db handles under `ns/shared/` (the rule that lets everyone who may interact write there); `ADP.ns('users/<id>')` is per person. A handle has `get`, `set`, `update`, `delete` and `onSnapshot`; their shapes are the db capability's (the `artifact-capabilities` skill has its types). `ADP.config.get/on('look.mode')` reads a switch. Both need the page to run under adp.js, which the template already loads.

## Rules

- Part ids never change after publishing; add a new id instead.
- Never build a new part by hand when a catalog entry exists: use `adp-catalog`.
- Hand the user the link and what to do next; do not paste the URL list.
