---
name: msb-docs
description: "The documentation site and the README's pictures: how a page is written (the four page kinds by section, the voice, the table shapes for commands, config keys and troubleshooting), docs/content Markdown with title/section/order/description front matter, docs/build.py's deliberate Markdown subset and template.html, the SEO and agent outputs (canonical, Open Graph, JSON-LD, sitemap.xml, llms.txt, a .md copy per page), what --check refuses including an msbctl subcommand with no Commands-page section, and scripts/screenshots (make.sh driving real msbctl in tmux against an invented HOME, render.py drawing the SVG). Use when editing or adding a page, when --check fails on a link, anchor or missing section, or when a screen a screenshot shows has changed."
---

# Docs

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- `docs/` — the documentation site (GitHub Pages, `.github/workflows/docs.yml`). Pages are Markdown in `docs/content/` with `title`/`section`/`order` front matter; `docs/build.py` is a stdlib-only converter for a deliberate Markdown subset (extend it rather than adding a generator), plus `template.html` and `assets/` (terminal theme, light/dark/auto, client-side search over an index it writes as a script so the site works off `file://`). `CHANGELOG.md` is rendered as a page, never copied; the logo comes from the repo-level `assets/`. The same build writes the SEO/agent outputs (canonical, Open Graph, JSON-LD, `sitemap.xml`, `llms.txt`, `llms-full.txt`, a `.md` copy of each page), all derived from the pages and `--site-url`, so a new page needs only its front matter — including the `description`, which `--check` requires. `--check` (run by `check.sh`) fails on a broken internal link or anchor and on any `msbctl` subcommand without a `### \`msbctl <name>\`` section on the Commands page. **A user-visible change updates the relevant page in the same PR**, like its changelog line.
- `assets/` — the logo: `msb-manager-mark-dotmatrix-dark.svg` (for dark grounds, also readable on light; the README's header) and `msb-manager-icon.svg`.
- `scripts/screenshots/` — `make.sh` regenerates `docs/assets/screenshots/*.svg` (used by the README): the real `msbctl`/`msb-picker` in a fixed-size tmux against an invented HOME (`world.py`), a fake `bin/msb` and a `bin/msbctl` wrapper that skips only the `/dev/kvm` preflight; `render.py` turns the captured grid into an SVG terminal (fixed cells, box lines drawn as strokes, docs palette). Needs tmux and fzf. Re-run it when a screen it shows changes; never hand-edit the SVGs or put real names, hosts or tokens in `world.py`.

## Writing the pages

The site borrows its shape from [Diátaxis](https://diataxis.fr/) and keeps its own voice. A page is one kind, set by its `section`, and doesn't drift into another; when it starts to, split it and link.

| Section | Kind | A page here |
| --- | --- | --- |
| Start here | tutorial | one path, in order, from nothing to a working sandbox; no options the reader doesn't need yet |
| Guides | how-to | one task, named for the task ("Folders & ports", not "Advanced"). Opens with a sentence on *when* you need it. Commands first, then the why of each step |
| Concepts | explanation | why it works this way, and what it does not protect. No steps |
| Reference | reference | complete and terse: every command, flag, key, type and default, in tables. Behaviour in a sentence; the why is linked, not repeated |

Voice, which is what the docs are for:

- **Say why, and say what fails.** "It's deliberately not `set -e`", "It's a missing egress rule until proven otherwise." A failure the page predicts saves a debugging session. Never trade this away for brevity.
- **Second person, plain verbs, short paragraphs.** One condition per sentence. When a paragraph needs three "unless"es, it wants a list or a table.
- **No dating.** Behaviour is stated as it is, never as a change ("now", "no longer", "used to", "current msb-manager"); that's the changelog's job. An upgrade step names its condition instead: "a sandbox created before the filtered agent existed needs one rebuild".
- **Define before relying.** A term with a specific meaning (placeholder, policy pin, registry entry, rule group, feature) is defined where it's first used or is in `glossary.md`; add the row when you add the term.
- **No filler and no marketing.** No "In this section we will", no "simply", no adjectives doing a claim's job. Say what's not covered as plainly as what is.
- **Specific over general.** Exact paths, values, defaults, limits and error strings; a reader searching for an error message should land on the heading that quotes it.

Shapes that repeat:

- **Commands** (`commands.md`): `### \`msbctl <name>\``, a `text` synopsis, behaviour in prose, then an `| Option | Meaning |` table (and `| Action | Does |` for verbs with sub-actions). Options come from the argparse parser; check them against `msbctl <name> --help`, never from memory.
- **Configuration** (`configuration.md`): `| Key | Type | Default | Meaning |`, with types from the "Value types" table; validation the code enforces goes in that table or the row, never guessed.
- **Troubleshooting**: the heading is the symptom as the user sees it, the error string where there is one. Then the cause in one bold sentence, then the fix as commands.
- **Callouts**: `> **Note:**`, `> **Tip:**`, `> **Warning:**` only; a warning is for what loses data or opens the network.

