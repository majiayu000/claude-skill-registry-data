---
name: changelog-page
zh_name: "版本更新日志"
en_name: "Changelog Page"
emoji: "🗒️"
description: "A multi-release changelog page grouped by version: highlights, then breaking, added, changed and fixed items, drawn from tags and commits."
en_description: "A multi-release changelog page grouped by version: highlights, then breaking, added, changed and fixed items, drawn from tags and commits."
category: doc
scenario: engineering
tags: ["changelog", "release notes", "releases", "versions", "whats new", "更新日志"]
triggers:
  - "changelog"
  - "changelog page"
  - "release history"
  - "what changed between versions"
  - "更新日志"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - typography-hierarchy
      - color
      - accessibility-baseline
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Make a changelog page for our last three releases from the git tags and commits: a highlight per version, then breaking, added, changed and fixed items."
---

# Changelog Page

**Intent.** A page users and teammates scan to see what changed in each version. Newest first, user-facing language, no commit noise.

## Ground it

Write only what the sources say. Gather them yourself before writing a word:

- `git tag --sort=-creatordate` for the versions, and `git log --format="%h %cs %s" <previous>..<tag>` for each range;
- an existing `CHANGELOG.md` if there is one (prefer its wording);
- `git show <sha>` for anything unclear. Merge commits, version bumps and test-only changes are left out.

Keep the list of files, commits and refs you read: they go in a **Sources** section at the bottom of the page and in `sources` when you register (`register_open_design_artifact` with kind `html`). If something the document needs isn't in the sources, ask the user, or mark it plainly as an open question. Never invent numbers, dates, names or quotes.

## Structure

1. **Header:** the product name and "Changelog", with a short line on how versions are numbered.
2. **An index** of versions at the top, linking to each section.
3. **One section per version, newest first:** version and date, a one-sentence highlight, then these groups in this order, each only if non-empty: **Breaking**, **Added**, **Changed**, **Fixed**. Each item is one user-facing sentence (rewrite `feat: add X` as "You can now …") with the short commit hash in code.
4. **Sources:** the tag range and where the items came from.

For a single release, the `release-notes-one-pager` skill is a better fit.

## Design

- One readable column (`max-width` 720–780px), body 16–17px with line-height 1.55–1.65, generous space between sections. It must read well on a phone: tables sit in an `overflow-x: auto` wrapper, nothing has a fixed width wider than the screen.
- Style from the active design system (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`); status colours are the only extra colours (green for accepted/done, amber for proposed/in progress, red for rejected/high severity, grey for superseded).
- Headings are short labels; the content does the talking. Code, paths and commands in a monospace face, with `overflow-wrap: anywhere` so long paths wrap on phones.
- Finish with `check_open_design_artifact` and fix every error at desktop and mobile width.
