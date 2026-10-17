---
name: my-html-artifact-flavour
description: >-
  House style for every HTML page or artifact the user asks for: reports,
  runbooks, checklists, dashboards, explainers. IBM Plex type, role colour
  tokens in light and dark, offline fonts, copy boxes and an interactive
  checklist pattern. Use whenever you write or restyle an HTML page.
---

# my-html-artifact-flavour

One look for every HTML page: IBM Plex Sans, Serif and Mono, calm green-grey role tokens in
Light and Dark, quiet bordered controls, disclosures that animate once, and copy boxes for
anything literal. Pages work offline from one file.

## With the artifact-design skill

When `artifact-design` also loads, keep its page contract and use this skill's look in place of
its default design. The flavour already meets the contract: a `<title>` of two to four words
(`pageTitle` or `--title`), colour tokens on `:root`, dark tokens under `:root[data-theme="dark"]`
and under `prefers-color-scheme: dark` guarded by `:root:not([data-theme="light"])`, an explicit
`body` background, and a 16px gutter with no horizontal scroll at phone width. A page built here
can be published with the Artifact tool as it is: it loads nothing from the network.

## 1. Pick the route

- **Checklist**: a person walks items and marks each one (UAT, runbook, migration, audit,
  acceptance list). Use [`patterns/checklist/`](patterns/checklist/schema.md): write content
  JSON, render, verify. Start from `patterns/checklist/example-content.json`.
- **Any other page** (report, explainer, dashboard, comparison): write a body fragment with the
  foundation components in [`foundation/components.md`](foundation/components.md), then wrap it:

```sh
python3 <skill-dir>/page.py body.html page.html --title "Build health report" [--css extra.css]
```

`page.py` adds the CSP, embedded fonts and OFL licences, `flavour.css`, `flavour.js`, and a top
bar with the theme switch (and Expand all / Collapse all when the body has disclosures). Extra
CSS uses the tokens; a new colour is a new token in both themes.

Done when the route is chosen and the content source (JSON or body fragment) exists.

## 2. Write the content

Apply `write-simply` to all visible text when it is installed
(`~/.agents/skills/write-simply/SKILL.md`). Give each step a bold lead-in; split multiple
actions into lettered substeps; put a warning before the step it affects. Put literal commands
in copy boxes (`command` in checklist JSON, `<pre data-copy>` in a body), with undo commands in
undo boxes. Mark items that change something. Keep at most one diagram, and only when it
explains a sequence or a state change.

Done when every literal command is in a copy box and every change has its undo beside it.

## 3. Render

```sh
python3 <skill-dir>/patterns/checklist/render.py render content.json page.html [--origin https://host] [--storage prefix] [--forbid-host text]
python3 <skill-dir>/patterns/checklist/render.py extract earlier.html content.json
```

`--storage` keeps saved results apart (default `html-flavour`, which also shares the theme choice
between flavour pages). Both scripts use only the Python standard library.

## 4. Check

For a checklist, run the verifier (it needs `jsdom`: `--repo` with a checkout that has it, or
`--jsdom <dir>`, or a global install):

```sh
node <skill-dir>/patterns/checklist/verify.mjs page.html --repo <checkout> [--origin https://host] [--expected-count n] [--forbid-host text] [--example other.html] [--language-report report.json]
```

For every page, inspect the local `file://` page with agent-browser in a dedicated session:

- 1280 and 390 px wide, each in System, Light and Dark, after fonts load;
- no horizontal page overflow (`document.documentElement.scrollWidth <= innerWidth`);
- body and muted text, chips, tags, links and the diagram readable in both themes
  (`page.py` and the verifier print token contrast; every pair is at least 4.5:1);
- an open disclosure, a copy box (its height follows the content), and a lightbox if present;
- zero network requests; then close the session.

Done when the verifier has no FAIL (a WARN about the title is acceptable for content you must
not rename), all six views were inspected, and the browser session is closed.

## Files

- `foundation/flavour.css`, `foundation/flavour.js`: tokens, components and behaviours; the
  single source for every pattern. `foundation/components.md` documents them.
- `foundation/example-body.html` → `foundation/example.html`: every component on one page.
- `fonts/`: IBM Plex WOFF2 (latin; Sans 400/600, Serif 400, Mono 400), checksums in
  `manifest.json`, SIL Open Font Licence texts. Embedded at build time.
- `flavour.py`: shared build helpers (fonts, CSP, contrast); `page.py`: the body wrapper.
- `patterns/checklist/`: `template.html`, `render.py`, `schema.md`, `example-content.json`,
  `example-shot.png`, `example.html`, `verify.mjs`.

Layers build on a pattern by installed path (`~/.agents/skills/my-html-artifact-flavour/…`):
they pass a pattern extension and their own checks, and keep this skill's files unchanged.
Planned patterns: report and audit checklist.
