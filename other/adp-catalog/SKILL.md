---
name: adp-catalog
description: "Find, use and add components, themes, layouts and guides from the ADP catalog (the shared library of reusable artifact parts). Load it whenever an artifact needs a component, theme, layout or pattern that may already exist, when the user says take, reuse, catalog, kit or theme, or when a new reusable piece should be added. Covers search, taking entries by reference with the files map, and the catalog rules. Also load it when the user wants their own, a separate or a private copy of the catalog."
metadata:
  version: "2.3.0"
---

# ADP catalog

The catalog is a published artifact whose files are kit entries, listed in its `catalog.json` (schema `kit-catalog/2`, generated from the header of each entry's main file). Claude catalogs support native references: the server copies their files into your artifact. Sites catalogs use authenticated HTTPS reads, hash verification and native destination publication (see below).

`ADP` means `python3 -I <adp skill folder>/scripts/adp.py`. CATALOG is the catalog url (its fetched index is the live one), `-` for the saved catalog, or a local `catalog.json` (the shipped build is `~/.adp/catalog/catalog.json` after setup: not the live catalog).

## Save and fetch the user's catalog (My Own Kit)

For Claude catalogs, the user's whole catalog lives on disk in `~/.adp/catalog/`: get it first. Sites catalogs use `~/.adp/catalogs/<hostname>/` and can fetch only the selected entries using the Sites workflow below. Setup already put the shipped copy there, so `ADP catalog URL` then only lists what differs. `ADP catalog URL` saves the url in `~/.adp/config.json` and prints the Artifact `read` of its `catalog.json` into `~/.adp/catalog/`. Make that read, then run the command again: it prints `fetched: true`, the build date, the entry count and, for every file the index lists that is not on disk yet, `read` calls with `paths` (at most 256 each, `out_dir` `~/.adp/catalog/`). Make them all, run the command once more, and it prints `complete: true`. `take`, `kit` and `suggest` read from that folder (an older `~/.adp/catalogs/<id>/` copy still counts); `adp.py` stays offline, it only prints the calls. `ver` is empty until the catalog's owner sets one, so compare the build date. `ADP catalog` alone shows the saved one. Never assume a catalog.

## Your own published catalog

When the user wants their own, a separate or a private catalog: after setup the shipped catalog is already in `~/.adp/catalog`, so nothing needs downloading to start.

Publish it from `~/.adp/catalog` with `python3 -I <adp skill folder>/scripts/publish_catalog.py`. `welcome --out DIR` makes the first page: publish it as a new artifact, with the capabilities it lists, to get the link. `plan --url <that link> --out DIR` writes the packed publish, with that link stamped in: publish its `publish.json` once, into that artifact, then hand off: the page applies the proposals itself and reloads. Then run `ADP catalog <its link>`. The steps are in the repo's `docs/RELEASING.md`, "Publish the catalog".

Then ask the user whether to add the extra kits: entries kept outside the base catalog, one seed pack each in the repo's `extras/` folder (https://github.com/fblgit/artifacts-done-properly/tree/main/extras); list them by id. For each one the user picks, download `https://raw.githubusercontent.com/fblgit/artifacts-done-properly/main/extras/<id>.json` and write its docs as one ArtifactData batch (the repo's `docs/kit-json.md`, "Push"). The page applies them while an editor has it open and adds them to its index.

- Never have the user clone a catalog artifact: a clone carries the original's `catalog.json` link and none of its db, so its start prompt and Take it references point at the original.

- Never download the whole catalog to publish a copy of it.
- Never publish a files map of hundreds of references: an upload takes at most about 250 files, and a catalog copy by reference has no bootstrap.
- A published catalog changes by proposal, not by a publish over it.
- The owner shares it (view) from the Share menu; you cannot.

## Find

- `ADP suggest CATALOG --for "free words" [--n 3] [--kind K]`: ranked by overlap with tags, name, summary, id, provides and about (the `why` field says which matched), no model call. `--n` counts per kind (viz, theme, pattern...), so it can print more than N lines; `takes` is how many files the entry brings.
- `ADP kit list [CATALOG] [--kind K] [--tag T]`: one JSON line per entry. The kind is the id prefix (`viz`, `theme`, `layout`, `kit`, `pattern`, `runtime`, `template`, `guide`).
- `ADP kit show ID [CATALOG]`: name, summary, about, tags, files, requires, provides, and what the entry's header says (status, version, config, db, source, changed); `about` and those fields are read from the main file in the local kit.
- `ADP kit describe ID [CATALOG]`: the mount signature: needs, provides, requires, file paths, the sample path.

## Connect the selected Sites catalog

For a Codex/Sites catalog, use the Sites skill to publish and connect that exact Site. Keep its returned project ID, published origin, MCP endpoint and local artifact namespace together; a namespace such as `catalog` is not a Site address. Never reuse another Site's connected tools just because their names are also `adp_read`, `adp_query` and `adp_write`.

1. Read that Site with `include_mcp_connection: true`. Use its returned plugin ID unchanged. Sites publication provisions the plugin; do not create a fixture-specific replacement or a proxy to another Site.
2. If the plugin's tools are absent and installation is unconfirmed, offer the returned plugin through Plugin Management. Installed does not mean tools are available in this chat. Sites documents trying a new chat for an already-installed plugin; report this connection blocker explicitly rather than claiming setup succeeded.
3. Through the selected Site's own tools, call `adp_session`, then `adp_read` for its artifact namespace and `manifest/current`. Configure membership only with the authenticated Site-scoped identity and the owner's authorization. Do not borrow an identity from another Site or substitute a static-file access token.
4. A native record read with its revision is the agent connection receipt. Browser initialization, a successful deployment, or reading `catalog.json` does not prove that connection. Saved guidance and ADP records require native revision guards; source publication uses the Sites lifecycle. Keep both receipts.

## Take from a Sites catalog

An HTTPS `*.chatgpt.site` catalog uses authenticated HTTP reads, not Claude server-side artifact references. The shell stays offline; the agent supplies the authorized Site session without putting credentials in commands, saved plans or replies.

1. Run `ADP catalog <Sites URL>` and execute its `fetch` plan, saving the exact live `catalog.json` bytes to `out_file`.
2. Run `ADP take <Sites URL> ID ...`. It resolves dependencies and prints the selected HTTPS reads. Execute them and save the exact response bytes at each `out_file`; do not substitute repository copies.
3. Run `ADP take <Sites URL> ID ... --materialize DIR`. It verifies every full SHA-256 before copying. It refuses missing/mismatched files and conflicting destination files. Retain the returned source/index/file hashes as provenance.
4. Merge those files into the destination artifact using the normal edit protocol. `ADP files DIR` produces the native publication payload. Load script/style dependencies in order; publish with the destination's own tool and verify the destination hashes and rendered result.

## Take by reference (Claude catalog)

1. Run `ADP take CATALOG ID ...`. Dependencies (`requires`) come first. It prints the `catalog` used, the `entries` taken and a `files` map to pass to the Artifact tool unchanged:
   `"kit/themes/glaze.css": {"artifact": "<catalog url>", "path": "kit/themes/glaze.css"}`
   An entry you name that owns a sample also brings its sample bundle (`kit/samples/<folder>.json`, by reference), and `samples` names only that entry's own `path#key`; dependencies bring none.
2. A `warning` in the output means CATALOG was a local `catalog.json`, not the live catalog: do not publish from it. Local catalogs need `--url URL` to name the catalog artifact; `--config C.json` is accepted too.
3. Publish with that `files` map (merge it into the page's own `files`), then `ADP check DIR`.
4. A taken file is served, not loaded: in the page's `index.html` add a `<link rel="stylesheet">` for each taken `.css` and a `<script src>` for each taken `.js`, in the order of `entries` (requires first), the scripts before `parts/app.js`; the globals an entry `provides` (for example `Kit.timeline`) exist only after its script loaded. Stylesheets: the entries' own in `entries` order, then the page's `styles/page.css`, then the theme last (a theme is tokens only, so it wins over the starter's placeholder tokens and leaves the page's rules alone). A theme also needs its web fonts: `take` prints them as `fonts` (`{id: url}`); add `<link rel="stylesheet" href="<url>">` for each before `styles/page.css`, or its families fall back to system fonts. `ADP new --theme`/`--layout` writes these tags for you. Switching a page's theme later means replacing both its theme link and its font link (`docs/themes.md` in the repo). `ADP check` does not verify the loading.
5. Besides what its tier already takes (adp-new, section 1), `ADP new` takes only the theme and a layout for you: `--theme NAME` (`default` when left out), `--layout ID` and `--catalog CATALOG` put them (and what they require) into its publish object and its index.html. Any other entry: `ADP take`, merge its `files`, add the tags of step 4.

## Rules

- Templates and files an artifact does not serve are kept with a `.txt` suffix; HTML cannot be copied server-side. Read such a file and write it to your project without the `.txt`.
- Never copy a kit file by retyping it; take it.
- `adp.py` has no sha256 check command; `scripts/adp_catalog.py` (next to `adp.py`; run `python3 -I <adp skill folder>/scripts/adp_catalog.py [catalog dir]`) verifies sizes and hashes of the local catalog build only, and also checks the headers.

## Add or update entries

No `adp.py` command adds an entry. An entry is files under `catalog/kit/`, the main one with a header comment (id, kind, group, status, version, updated, summary, tags, requires, files and the rest: the format is the repo's `docs/catalog-header.md`; a theme also `@fonts`, the url in its json). `python3 -I <adp skill folder>/scripts/adp_catalog.py build` writes the entry's record into `catalog.json` from that header, and `python3 -I <adp skill folder>/scripts/adp_catalog.py` must pass. The catalog artifact is planned by `python3 -I <adp skill folder>/scripts/publish_catalog.py` (the steps are in the repo's `docs/RELEASING.md`, "Publish the catalog"). Never publish over, test on or republish a catalog others use: ask the user first, and try anything on a scratch artifact.

An entry kept outside the base catalog is one seed pack in the repo's `extras/`, written by `publish_catalog.py kit pack ID`: one inbox proposal with the entry's own files (sample and preview included) and its index record. Push its docs unchanged as one ArtifactData batch; the catalog applies it and lists it by itself (`docs/kit-json.md`).
