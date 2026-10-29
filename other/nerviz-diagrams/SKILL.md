---
name: nerviz-diagrams
description: Renders diagrams of this repository's own .claude/ harness — the layers, the skill and agent classes with their write territories, the /new-feature pipeline — from .claude/schemas/extensions.json and the files on disk, as .drawio, .excalidraw, static and animated SVG under docs/diagrams/, plus PNG and video for the site. Meta-repository only; never a use case or domain diagram, which are Mermaid inside the spec.
argument-hint: "[empty for every view | <view name> to compose or refresh one]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Bash(java:*), Bash(node:*), Bash(ls:*)
model: sonnet
---

# Nerviz Diagrams

Draws the harness from its own data, so a diagram cannot say what the pipeline stopped
saying. Code extracts the facts, you compose a view that cites them, code validates and
renders. A diagram a model drew from memory is wrong the first commit the pipeline changes.

## Target

$ARGUMENTS

Empty: every view under `docs/diagrams/`. A name: only that view, created when absent.

**Class:** media

## Why this is a manual skill

Form 2: rendering writes files the person decides to commit and runs per release or when a
piece is added, never every session. Axis 2 is the manual trigger (`disable-model-invocation`,
so it never competes with the Mermaid of `use-case-design`), and axis 9 a write territory no
class has: `docs/diagrams/**`. The closest rejected form was an `ArchHook.java` mode, which
`export` would ship as dead code into every generated project. Record:
`@.claude/decisions/0190-nerviz-diagrams-skill-derived-from-data.md`.

## Procedure

Run every command from the repository root. No network at run time; `npm ci` in step 5 is the
only download, and nothing is ever `npx`-ed from an unpinned package.

1. **Facts.** `java .claude/skills/nerviz-diagrams/scripts/Diagrams.java facts` writes
   `docs/diagrams/facts.json` (gitignored): `layer:*`, `class:*`, `agentclass:*`, `skill:*`,
   `agent:*`, `step:*`, each with a stable id. Read it to learn what you may cite.
2. **Compose.** Write or adjust `docs/diagrams/<view>/view.json` per
   `references/view.schema.json` and `references/visual-identity.md`. Every entity node is
   `{"fact":"<id>"}` or a selector `{"from":"<path into facts>"}` (`step:*`, or
   `class:design.members`). Free text lives only in `title`, `caption` and a group's caption
   label. `steps` gives the animation order. Kinds: `layers`, `classes`, `territory`, `pipeline`.
3. **Validate.** `java .claude/skills/nerviz-diagrams/scripts/Diagrams.java validate`.
   Every fact id and selector must resolve against facts extracted now.
4. **Render.** `java .claude/skills/nerviz-diagrams/scripts/Diagrams.java render` writes
   `<view>.drawio`, `<view>.excalidraw`, `<view>.svg` and `<view>.animated.svg` beside the view.
5. **Export (optional).** Once per machine, copy the skill's `package.json` and
   `package-lock.json` into `"${XDG_CACHE_HOME:-$HOME/.cache}/nerviz-diagrams"` and run
   `npm ci --prefix "${XDG_CACHE_HOME:-$HOME/.cache}/nerviz-diagrams" --no-update-notifier --no-audit --no-fund`.
   Then `node .claude/skills/nerviz-diagrams/scripts/export.mjs <view> [--video]` writes
   `docs/diagrams/<view>/dist/<view>.png` (and `.webm` with `--video`) and a
   `<file>.source-sha256` holding the SHA-256 of the SVG it came from.
6. **Check.** `java .claude/skills/nerviz-diagrams/scripts/Diagrams.java check` — what CI runs.

Never hand-edit a rendered file: edit `view.json` and render again. Never write under
`docs/use-cases/`.

## Failure modes

**Node absent.** Steps 1-4 and 6 are Java and still work; only step 5 needs Node.

**Playwright browser missing.** Video is opt-in. `export.mjs` stops and names the download
command (`playwright install chromium`); tell the person, never run it unasked.

**A `### Step` heading of `new-feature/SKILL.md` no longer matches the extractor.** `facts`,
`validate` and `check` exit 2 naming the line, so CI goes red by name. Fix the regex `STEP` or
`CONS` in `scripts/Diagrams.java` in the same change that reworded the heading.

**Unresolved fact id.** A piece was renamed or removed: `validate` names the view, the JSON
path and nearby ids. Update the view.

**Stale render.** `check` lists each file that differs from a fresh render, or a `dist/` file
whose `.source-sha256` is not its SVG's hash. Run `render` (and `export.mjs` for `dist/`).

## Contract

**Class:** media — the territory is `skill_classes.media` in `@.claude/schemas/extensions.json`:
`docs/diagrams/**`, nothing else. `ArchHook.java guard` enforces it.

**Reads** `.claude/schemas/extensions.json`, the `### Step` headings of
`.claude/skills/new-feature/SKILL.md`, the `.claude/` tree on disk, `.claude/settings.json`,
`.mcp.json` when present, and this skill's `references/`.

**Writes** `docs/diagrams/**` only.

**Never writes** any other path, and declares no `.mcp.json` server. The person's own
Excalidraw connector may refine a copy ad hoc, never a rendered file.

**Stays out of the generated project** — listed in `export.skills.exclude`.
