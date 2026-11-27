---
name: agnos-meta-website
description: "AGNOS maintainer skill. Builds the AGNOS presentation website, a guided tour of the demo's Performance Center for CIOs, in English and French, from the Markdown text and the images of its assets, with the demo Performance Center page. USE FOR: regenerating the site after AGNOS, its demo or the site's text evolves. It writes a folder only: committing and publishing it stay with the maintainer."
argument-hint: "build --demo <demo repository> --out <folder> [--demo-page <PERF-CENTER.html>]"
---

<!-- FTR-WEB-001; RQ-WEB-001, RQ-WEB-002, RQ-WEB-003, RQ-WEB-016 / ADR-WEB-001 (DEC-WEB-001 to DEC-WEB-003, DEC-WEB-006) -->
# AGNOS Presentation Website

`<skill-folder>` is the folder holding this file. Run from any folder; the script uses Python's standard library only.

## Build

`python -I <skill-folder>/scripts/build_site.py build --demo <demo repository> --out <folder> [--demo-page <page>]`

| Argument | Meaning |
|---|---|
| `--demo <folder>` | The demo repository (`agnos-lightweight-process.demo`, built by `agnos-meta-demo`): its Performance Center is generated when no page is given <!-- TASK-WEB-017: no measure since RQ-WEB-005 was deprecated --> |
| `--out <folder>` | Where the site is written, typically the working copy of `spashx/agnos.site`: `index.html`, `screens/` and `demo/` are replaced there, nothing else is touched |
| `--demo-page <file>` | A `PERF-CENTER.html` already generated, copied into `demo/` with its `PERF-CENTER.json` and `PERF-CENTER.data.js` |

Without `--demo-page`, the build runs this repository's `agnos-perf-center` on the demo's `service` and `client` with
`--history` and `--call-graph`; the functions are left out when the call-graph packages are not installed
(`agnos-perf-center`'s `requirements-callgraph.txt`).

- Exit `0`: the site is written; show the summary line.
- Exit `1`: nothing is written; each error names its file and its field. Correct the content, never the checks.
- The build never commits nor pushes: publishing the folder stays with the maintainer.

## Changing the site

Everything the reader sees comes from `assets/`:

| Path | Content |
|---|---|
| `assets/content/en.md`, `assets/content/fr.md` | The text, one `##` section per page element and one `###` field per text, the same in both files; the header comment of each file gives the format |
| `assets/screens/*.png` | The images the content links to; replace a file by one of the same name. The page frames each one at the capture ratio 16:9 (the design-system token `web.ratio-shot`): `build` refuses an image whose ratio differs by more than 0.5% or whose width is under 1920 px, naming the file and its size. Accepted sizes: 1920x1080, 3840x2160 <!-- RQ-WEB-019 --> |
| `assets/template.html` | The page's layout, without text |
| `assets/site.json` | The names of the external links the site uses; their addresses come from the repository's `assets/links.json`, declared once: `{{v:link.<name>}}` in the template, `{{link.<name>}}` in the content; `link.demo` is the build's own. An unlisted or undeclared link fails the build <!-- RQ-WEB-020, RQ-DOC-007 / DEC-WEB-008, DEC-DOC-001 --> |

To change a word, edit the Markdown and build again. To add a field, add it to both languages and give it an element in
the template: the build refuses a field one language lacks or the template does not use.
