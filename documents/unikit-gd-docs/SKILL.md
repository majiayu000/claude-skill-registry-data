---
name: unikit-gd-docs
description: >-
  Render the GAME-DESIGN document (the GDD) into a human-readable form — read-only
  Markdown chapters under docs/design/ (index, systems, flows, content, economy, glossary),
  with facts resolved inline from GD-IDS.yaml and drafts flagged 🚧. Optional --web also
  renders an HTML site from the unikit-docs template (falls back to Markdown-only if the
  template is absent). Use to export or publish the design for people to read, e.g. "render
  the GDD", "export the game design to docs", "generate readable design docs", "publish
  the GDD", "make a design doc site". Read-only — it never edits the GDD or registry, only
  renders it. This renders the game DESIGN — for the project's CODE documentation (README,
  docs/*, modules, architecture) use /unikit-docs.
argument-hint: "[--web]  (renders docs/design/*.md from the GDD workspace; --web also emits HTML)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(date *)
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Human-Readable GDD Renderer (workspace → docs/design/)

Render the design workspace (`.unikit/gamedesign/`) into a **human-readable GDD** under
`docs/design/` — the export end of the module, the conceptual mirror of `unikit-gd-recon`:
where recon turns *code → readable design facts*, this turns *design → a readable GDD*.
Both are **read-only at the edge**.

This skill is a **leaf renderer**: it **reads** the GDD (the authored docs + the `GD-IDS`
registry), **resolves the facts inline**, and **writes** only into `docs/design/`. It has
**no `Skill` tool** — it renders, it never authors and never dispatches. The source of
truth stays the workspace; `docs/design/` is a generated, throwaway view (re-render any
time).

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md` and apply
it (fall back to English if missing). The rendered chapters are **prose for humans** — write
them in the project's artifact language (`gd-principles` → "Language": GDD prose is `ru` by
default). **IDs, keywords, canonical terms, and formulas stay English** verbatim — they are
the registry's vocabulary, never translated. Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — for the **ID conventions**
   (so resolved facts print with correct ids), the facts-registry model, and the one-way
   boundary (this renderer reads design, never code).
2. **`.unikit/gamedesign/GAME.md`** + **`GD-IDS.yaml`** — the render source. **Schema
   guard:** `GD-IDS.yaml` MUST be `version: 2`; on `version: 1` **STOP** with the upgrade
   message (the pre-v2 layout renders differently — do not silently misrender).
3. The per-artifact docs under `.unikit/gamedesign/`: `systems/SYS-*.md`, `flows/FLOW-*.md`,
   `content-types/CT-*.md`. Read each at render time for its prose; take **numbers, ids,
   status, and relationships from `GD-IDS` (the truth)**, not the doc body, when they differ.

**No GDD yet** — if `GAME.md` does not exist, there is nothing to render: **STOP** and route
to `/unikit-gd-spec` (author the master GDD) or `/unikit-gd-recon` (reconstruct one from
code first). Never invent content to fill a chapter.

**One-way boundary:** this skill reads only the design workspace — **never** `.unikit/code/`,
project source, or build artifacts. It is a render of the *design*, not of the code.

## Pipeline — RESOLVE → RENDER → (optional) WEB

### Step 1 — Ensure the output directory

```
Bash: mkdir -p docs/design
```

`docs/design/` is this skill's **owned subtree** (the ownership split with `unikit-docs`,
which owns the non-design `docs/*.md`, is below). Never write a design chapter outside it.

### Step 2 — Resolve the facts

Read `GD-IDS.yaml` once and build the resolution maps the chapters need: `systems` (by
`category`), `flows` (by `mode`), `content_types` (+ their `content` units), `events`,
`resources` / `tracks` / `knobs`, `entities` / `formulas` / `terms`, plus the `depends_on`
/ `belongs_to` / `goals.targets` edges. **Resolve inline** — a chapter prints the actual
name, number, status, and relationship, not a bare id with a "see the registry" pointer (a
reader of `docs/design/` never opens `GD-IDS`). A `deprecated` entry is rendered struck or
under a "Deprecated" subhead, never silently dropped (the registry never deletes).

### Step 3 — Render the chapters (Variant B — by axis)

Write these six Markdown chapters into `docs/design/`. Every chapter opens with a **nav
header** (links to the other chapters) and closes with a **"См. также / See also"** block
(artifact-language label) cross-linking the related chapters. **Drafts are included, never
hidden:** a `not-started` / `skeleton` artifact is rendered with a **🚧 draft banner** so a
reader knows it is provisional — a half-finished GDD honestly shown beats a polished one
that silently omits the unfinished half.

| Chapter | Renders |
|---------|---------|
| `index.md` | The cover: premise/theme, core fantasy, pillars + anti-pillars, loop stack, player needs (SDT), win/lose intent, monetization stance, non-goals, reference games — from `GAME.md`'s authored sections. Plus a **status overview** (counts by `doc_status`) and a **clickable TOC** built from the `## System Map [gen]` / `## Flow Map [gen]` / `## Funnel [gen]` / `## Content Map [gen]` rows, each linking into the chapter below. |
| `systems.md` | **All** systems grouped by `category` (Core / Gameplay / Progression / Economy / UI / Narrative / Meta). Per system: name, tier, `doc_status`, `implemented_version` (if set), `implements` pillars, `depends_on`, and the fantasy + core-rules summary from its `SYS-*.md`. 🚧 on drafts. |
| `flows.md` | **All** flows grouped by wiring `mode` (linear / conditional / emergent). Per flow: the `GOAL` steps + their `targets`, pacing summary, `depends_on` systems, and the **derived "realized"** state (from the depended systems' `implemented_version` — never a written field). 🚧 on drafts. |
| `content.md` | **All** content types. Per type: the typed `CT.fields` schema (name : type, with `ref<>` links resolved to the target's name), the `scale` (`bulk` → count+spec; `curated` → the unit rows), and `belongs_to` system. 🚧 on drafts. |
| `economy.md` | The cross-boundary facts: `resources` (RES, by `kind`), `tracks` (TRACK), `knobs` (KNOB, with current/range), and `formulas` (FORM, with expression + range) — as tables. |
| `glossary.md` | The canonical vocabulary (`terms`: canonical → translation, forbidden aliases) and a **master ID index** (every PIL / SYS / FLOW / CT / CU / RES / TRACK / KNOB / ENT / FORM id → its name + owning doc), so any id seen anywhere resolves. |

### Step 4 — `--web` (optional; default is Markdown-only)

The MVP is Markdown chapters; **`--web` is opt-in**. When `--web` is passed:

1. Read the template at **`{{skills_dir}}/unikit-docs/templates/html-template.html`** (a
   non-`.md` asset, used verbatim — the same template `unikit-docs` renders its site with).
2. **Template missing or unreadable** → skip HTML, keep the Markdown chapters, and emit
   exactly: `WARN [--web] unikit-docs html-template not found; rendered Markdown only.`
   (`/unikit-docs` may not be installed — degrade gracefully, never fail).
3. Template present → render each chapter to `docs/design/<chapter>.html` using the
   template, fix `.md` links to `.html` **within `docs/design/`**, and build a sidebar with
   `class="active"` on the current page. The HTML lands **inside `docs/design/`** (this
   skill's owned subtree) — it never writes into `unikit-docs`'s top-level `docs-html/`.

### Step 5 — Report

List the chapters written (and the `--web` outcome). Note that `docs/design/` is a
generated view — re-run after any authoring change to refresh it. **Do not** offer to edit
the GDD here (route authoring to the owner skills).

**Next steps** (do not auto-invoke):

- 🌐 Render the HTML site — /unikit-gd-docs --web

## Ownership Boundaries

- **Owns:** `docs/design/**` — the rendered design chapters (and their `.html` under
  `--web`). Nothing else.
- **Reads (read-only):** `.unikit/gamedesign/` (`GAME.md`, `GD-IDS.yaml`, systems, flows,
  content types), the gd-principles core, and `unikit-docs`'s html-template (for `--web`).
- **The `docs/` split with `unikit-docs`.** `unikit-docs` owns the **non-design**
  `docs/*.md` (top-level) + `README.md` + `docs-html/`; this skill owns **`docs/design/**`**.
  The two never relink each other's pages: `unikit-docs`'s `--web` glob is top-level
  (`docs/*.md`) and does not descend into `docs/design/`. Keep this boundary — never write a
  non-design page, never touch `README.md` or `docs/*.md`.
- **Never:** edit the GDD or `GD-IDS.yaml` (read-only render); call any skill (no `Skill`
  tool — it is a leaf); read the code workspace or project source; invent content to fill a
  chapter; drop a draft or a `deprecated` entry to look more complete.

## Quick Reference

```
/unikit-gd-docs            → render docs/design/{index,systems,flows,content,economy,glossary}.md from the GDD
/unikit-gd-docs --web      → the same, plus an HTML site from the unikit-docs template (MD-only + WARN if absent)
/unikit-gd-docs  (no GDD)  → STOP → route to /unikit-gd-spec (author) or /unikit-gd-recon (reconstruct from code)
```
