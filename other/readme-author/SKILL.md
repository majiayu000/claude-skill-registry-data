---
name: readme-author
description: Use when creating, writing, or substantially improving a README (this project or any project) — distills the best precepts from the matiassingers/awesome-readme exemplars into a structured, scannable, high-signal README. Triggers on "write/improve the README", "make a README", README review.
---

# README Author

Goal: **write a README that earns the user's trust in the first screen and never wastes their
time.** A great README is judged like a product landing page: a newcomer must grasp *what this
is, why they'd want it, and how to start* within seconds — then find depth on demand. These
precepts are distilled from the curated exemplars and articles in
[matiassingers/awesome-readme](https://github.com/matiassingers/awesome-readme).

## First, ground it in the project

Don't invent. Read before writing: the code's entry points and public API, `go.mod`/manifest,
existing docs (`PROGRESS.md`, `docs/`, `CLAUDE.md`), `LICENSE`, CI config, and any current
README. The README must match what the project *actually* does and how it's *actually* run.
For this repo, prefer real `mise run …` commands and the real module path over invented ones.

## The precepts (what the best READMEs share)

1. **Above-the-fold clarity.** Project name, a one-line description of what it does and for whom,
   and (where it fits) a logo/banner — all visible before any scrolling. A reader decides to
   stay or leave here.
2. **Show, don't tell.** A GIF/screenshot/asciinema of the tool in action, or a short
   copy-pasteable example with its output, beats paragraphs. Visual proof of functionality is
   the single most-cited strength of the exemplars.
3. **Badges that inform, not decorate.** Build status, version/release, coverage, license,
   go.dev/docs — a tight row near the top. Don't add a badge you can't keep green.
4. **A table of contents** once the README is long enough to scroll (collapsible for very long
   ones), with "back to top" links. Navigation is a feature.
5. **The standard backbone, in what→why→how→where order:** brief description → (demo) →
   features → install → usage/quick-start → configuration → examples → how it works/architecture
   → contributing → license. Include only the sections the project needs; omit empty ones.
6. **Conciseness with depth on demand.** Keep the main flow short; push long output, advanced
   options, FAQs, and benchmarks into `<details>` expandable blocks. Respect the reader's time.
7. **Copy-pasteable, correct commands.** Every install/usage snippet must run as written
   (verify them). Pin the language/tool version. Show expected output where it helps.
8. **Friendly, precise tone.** Welcoming to newcomers, a little personality is fine, never at the
   cost of accuracy. Define jargon or link it.
9. **Point to the deeper docs**, don't inline everything: link API reference, `ARCHITECTURE.md`,
   changelog, live demo, chat/Discussions. The README is the map, not the whole territory.
10. **Credit and license.** Acknowledge contributors/prior art (for a port, name and link the
    original and its license), and state the license clearly — both the badge and a `## License`
    line. Honor copyleft/attribution obligations.

## Avoid (why people won't use your project)

- No description / unclear what it does or who it's for.
- No runnable install or usage; commands that don't work or assume hidden setup.
- A wall of text with no headings, no visuals, no TOC.
- Stale badges, dead links, screenshots of an old UI, invented features.
- Burying the one thing the reader needs under autobiography.

## Process

1. **(RDD mindset)** If the project/feature is new, consider writing the README *first* to
   clarify the vision, then reconcile with the code.
2. **Draft the backbone** from the template below; fill only the sections that apply.
3. **Lead with the hook** — nail the one-liner and the demo/quick-start before anything else.
4. **Make it scannable** — short paragraphs, lists, headings, expandable blocks for depth.
5. **Verify every command** actually runs (in this repo, via `mise run …`); fix or remove what
   doesn't.
6. **Trim** — cut anything that doesn't help the reader decide or start. Add a TOC if it scrolls.
7. **Check links, badges, and license/attribution** are correct and live.

## Template skeleton

```markdown
<!-- optional: centered logo/banner -->
# Project Name

> One sentence: what it does and for whom.

[![build](…)](…) [![coverage](…)](…) [![version](…)](…) [![license](…)](…)

<!-- demo: GIF / screenshot / asciinema, or a 3-line example + output -->

## Table of contents   <!-- once it scrolls -->

## Features
- Bullets of concrete capabilities (benefit-first).

## Install
\`\`\`bash
# copy-pasteable, version-pinned
\`\`\`

## Usage / Quick start
\`\`\`bash
# smallest real example
\`\`\`
<!-- expected output -->

## Configuration   <!-- if any; flags/env/options table -->

## How it works / Architecture   <!-- brief; link ARCHITECTURE.md for depth -->

<details><summary>Advanced / benchmarks / FAQ</summary>
… depth on demand …
</details>

## Contributing   <!-- how to build/test; link CONTRIBUTING.md -->

## Credits / Acknowledgements   <!-- prior art, original project + its license for a port -->

## License
State the license (and attribution obligations).
```

## Notes & sources

- Match the host project's tooling and conventions (here: `mise run …`, module
  `github.com/oioio-space/unpixel`, GPL-3.0, the bishopfox/unredacter attribution).
- Precepts distilled from [awesome-readme](https://github.com/matiassingers/awesome-readme) and
  its referenced articles: *Art of README*, *Readme Driven Development*, *Top ten reasons why I
  won't use your open source project*, and *ARCHITECTURE.md*.
