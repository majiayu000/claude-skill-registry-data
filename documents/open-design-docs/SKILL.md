---
name: open-design-docs
description: Turn a folder of Markdown documents (ADRs, RFCs, runbooks, notes) into designed HTML pages, one per file, all in one style, and keep them in step when the Markdown changes — use whenever the user wants several Markdown files (a docs folder, ADRs, RFCs, runbooks, meeting notes) turned into HTML pages, or wants HTML versions of existing docs refreshed after edits
---

<!-- generated:open-design-agent-kit -->

Turn existing Markdown documents into designed HTML pages with Open Design, one page per file.

Request: the rest of the user's message (if there is none, ask the user: "Which Markdown files should become pages, and in what style?")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Find the files

Resolve the folder or glob in the request with your own file tools (for example `docs/adr/*.md`). List what you found.

- More than 20 files: tell the user how many there are and ask whether to do all of them or a subset. Don't start until they answer.
- No files: say so and stop.

## 2. Pick one template for the set

All pages in a set share one template, so they read as one collection. Choose by what the files are, or use the style the user named:

| Files | Skill |
|---|---|
| Architecture decisions | `od:prototype:adr` |
| Proposals, design docs | `od:prototype:rfc` |
| Incident write-ups | `od:prototype:postmortem` |
| Runbooks | `od:prototype:eng-runbook` |
| Release notes or changelogs | `od:prototype:changelog-page` |
| Long-form notes, essays, anything else | `od:prototype:doc-kami-parchment` |

Derive a `collectionId` from the folder name (for example `docs-adr`) and a readable `collectionName`.

## 3. On a re-run, only redo what changed

If pages from an earlier run exist (look for artifacts in that collection, or call `get_open_design_artifact` on each), compare: a page whose `staleSources` lists its Markdown file is out of date and gets regenerated; a page that isn't stale is skipped; a file with no page yet gets one. Tell the user what you'll regenerate and what you'll skip.

## 4. Build each page

For each file, in order:

1. Call `read_open_design_source` with the file. Use only what it returns: never add facts the Markdown doesn't have.
2. Call `prepare_open_design_brief` with the chosen skill, a brief naming the file, `collectionId`, `collectionName`, and `screenRole` set to the file's name.
3. Write the page, keeping the document's own headings, structure and status (for ADRs and RFCs, its status goes in the `data-od-status` banner). Link to sibling pages in the set where the Markdown links to the sibling `.md` file.
4. Call `register_open_design_artifact` with the same collection values and `sources: ["<the .md path>"]`, so a later run can tell when the Markdown changed.

Check the first page with `check_open_design_artifact` and fix its errors before doing the rest, so mistakes aren't copied into every page. Check the others at the end.

## 5. Report

List each page with its source file, and anything skipped or still flagged. In VS Code, mention the Collections view, where the whole set opens with Prev/Next.
