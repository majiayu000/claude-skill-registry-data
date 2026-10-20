---
name: iru-build-docs
description: Build a repository's existing Antora documentation site, setting it up first (via `iru-setup-antora`) if it doesn't exist yet. Invoke as `/iru-build-docs`. Does no code exploration and makes no content edits to any existing page — it only ensures the toolchain/module exist and runs the Antora build, unlike `iru-update-docs`, which edits pages to reflect codebase changes. Use whenever the user just wants the docs site built/verified (e.g. to check it compiles, or to get the built HTML output) instead of updating its content.
model: haiku
---

# Build Docs

Build a repository's Antora documentation site as-is. This skill never edits page content, `nav.adoc`, or
`antora.yml` beyond what bootstrapping requires — if the docs need to be updated to reflect code changes, that's
`iru-update-docs`, not this skill.

## Step 1 — Locate the documentation module

Find `antora.yml` file(s) in the repository (`find . -name antora.yml -not -path '*/node_modules/*'`).

- **None found**: there is no documentation module yet to build. Ask the user whether Antora documentation
  should be set up now (via the `iru-setup-antora` skill) before continuing — don't assume either way.
  - **User agrees**: run the `iru-setup-antora` skill (via the Agent tool, or directly via Skill if already in this
    context) to scaffold the module. If it reports it stopped short (e.g. Node.js isn't installed), relay that
    blocker to the user and stop — there's nothing to build yet.
  - **User declines**: stop this skill entirely — there is nothing for it to build.
- **One or more found**: continue to Step 2 for each one.

## Step 2 — Locate the playbook and toolchain

For the docs module found in Step 1, locate its Antora playbook file (commonly `antora-playbook.yml` or
`site.yml`, usually next to `antora.yml` or at the docs module root) — don't assume a fixed name, check
`docs/package.json` scripts or the repository's CI config (e.g. `.github/workflows/docs.yml`) if it isn't
obvious.

Check Node.js is usable (`node -v` / `npm -v`). If either fails, stop and point the user at `iru-setup-antora`'s
Step 1 install instructions rather than attempting to install Node.js yourself.

## Step 3 — Install dependencies and build

From the docs module's directory:

```bash
npm ci
npx antora <playbook-file>
```

Use `npm ci` when a lockfile is present (matching CI); fall back to `npm install` only if there's no lockfile
yet.

- **Build succeeds**: the static site lands at the module's build output directory (e.g. `docs/build/site`).
  Note the path to its `index.html`.
- **Build fails**: read the Antora/Asciidoctor error (broken `xref:`, bad YAML, malformed AsciiDoc table,
  invalid Mermaid/MathJax syntax) and report it verbatim to the user along with the offending file — do not fix
  page content yourself; that's `iru-update-docs`'s job, not this skill's.

## Step 4 — Report

State whether the module already existed or was just set up via `iru-setup-antora`, whether the build succeeded or
failed, and the path to the built `index.html` (or the build error) — nothing else.
