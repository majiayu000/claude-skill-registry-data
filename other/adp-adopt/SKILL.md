---
name: adp-adopt
description: "Put an existing claude.ai Artifact on ADP: add part ids and hashes, declare the db, seed the records, or move a single-file page to the multi-file adp/2 layout. Load it when the user wants an artifact they already have to be split into parts, changed by records, built from catalog parts, commented on, or converted to ADP or adp/2, before touching its source."
metadata:
  version: "2.3.0"
---

# Adopt an existing artifact

Why: a page without part ids has no stable anchors, and its history lives only in versions. Adoption adds the part ids and the db without changing how the page looks or behaves.

`ADP` means `python3 -I <adp skill folder>/scripts/adp.py`. Read the artifact's latest version first (Artifact `read`), save it into a folder, and tell the owner what you are about to do. The read returns the page inside the Artifact tool's document skeleton (`<!doctype html><html><head>...</head><body>` ... `</body></html>`). Save only what sits between `<body>` and `</body>` (it starts at `<title>`): the publish wraps the file again, and a file that carries its own doctype, head and body ends up nested inside the wrapper.

## Step A: markers on the existing page

1. Wrap every view and its main sections in markers `<!-- part:view.section -->` ... `<!-- /part:view.section -->` (ids lowercase kebab, dot-separated, never changed later; styles and shared scripts become parts such as `page.style`, `page.script`, and each carries its own `data-part="<id>"`, which `ADP check` requires; their missing `data-comment-target` only warns). Add `data-part="<id>"` and `data-comment-target` to each rendered root. A page with no views is one part per block (title, list, form...).
2. `ADP check PAGE|DIR` takes a single page or a folder: it must pass. `ADP manifest PAGE|DIR` prints the part hashes.
3. Publish with a `label` and `capabilities` that keep what the page already declares (Artifact `list` with scope `files` prints the stored declaration; a non-empty `capabilities` replaces it, so restate every capability in it) and add the ADP rule `{path: "", read: "view", write: "admin"}` to the `db` rules, so only editors write the record. A page that declared nothing gets just that `db` rule: ADP's record lives there, and data the page keeps in the browser (localStorage) stays where it is, not migrated. Add one more rule per collection the page itself writes, at the access its writers have now (for example `{path: "books", read: "view", write: "interact"}`), or they lose write access. Add `user: {}` only if the page uses it.
4. Seed the database: `ADP seed DIR --by <you> --data FILE|DIR` writes `seed.json` and `seed/` for the page to expand on its first open by an editor (it expands whenever `manifest/current` is absent, so a page that already has its own rows still seeds); `--batches` prints ArtifactData batches instead, only when nobody can open the page as an editor. Tell the owner in one line.

Step A alone gives the page part ids and comment anchors; Step B is optional and needs a parity proof.

## Step B: move to the multi-file layout

1. Start a reference project with `ADP new starter REF --catalog CATALOG` and copy its shell, `adp.js` and `content.js` structure: a thin `index.html`, `adp.js`, `content.js`, `styles/*`, `parts/*`.
2. Move the page's own copy and views into those files; use `ADP new starter DIR --content FILE` to build views from a content file, then `--data` for records.
3. Prove parity: render old and new in a headless browser and compare every element's computed style and box in every view and state, at the widths and themes in use. No parity proof, no publish.
4. `ADP check DIR`, publish with `ADP files DIR`, then `ADP export` and `ADP record` (road `adp-edit`).
5. A page not seeded in Step A expands its seed on its first open by an editor (a client set to open pages on publish does that at once).

## Rules

- Never rename a published part id.
- Do not change the page's look while adopting; restyling is a separate change under `adp-edit`.
