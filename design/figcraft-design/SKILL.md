---
name: figcraft-design
category: design
description: Use for every design task when FigCraft is installed - the design system and every screen are drawn as editable FigCraft layers (frames, auto layout, components, variants, styles, variables) in the task's own .figcraft file from get_design_file; Foundations page, one page per flow, frame naming, batch-and-verify loop, saving, and the short notes document the human reviews beside it
---
# FigCraft Design

## Overview

When `get_design_file` says `figcraft_installed: true`, the design IS a FigCraft file — the way a product designer works in a design tool, not an HTML page. The human sees each page of that file rendered on the task and opens it in FigCraft for detail; developers get the notes document and the exact values in it. Everything is editable layers: frames with auto layout, text, vectors, components with variants, instances, paint and text styles, colour variables with Light and Dark modes. Never paste a screenshot as an image, never draw a screen as one flat picture.

**Core principle:** One file per task, built from the design system's components; every screen a real auto-layout frame a designer could keep working in; verify every frame by looking at it.

## The file

1. `get_design_file` (no arguments in your own task's run). It returns `task_file` — the ONLY file you write — and, when the project or repository already has a design system file, it has already copied it there (`seeded_from`), so the Foundations page, styles, variables and components are in the file you open.
2. Open it with the figcraft MCP `open_file` (path `task_file`). When `task_file_exists` is false, start a new document instead and `save_file` it to exactly `task_file` before anything else, so a crash never loses the work.
3. Name the document `<Project or repository> — <feature>` (screen design) or `<Project or repository> — Design system` (design system).
4. `save_file` to `task_file` after every page you finish and once more before the run ends. A file that was not saved does not exist for the human.
5. Never write `project_design_system_file` or `repository_design_system_file`: the system replaces them with this task's file when the human approves a design-system task.

Discover commands with `list_commands` and a filter (`autoLayout`, `component`, `style`, `variable`, `text`, `export`) — never unfiltered. `run_command` runs one; `batch` runs many as one undo step, chaining ids with `as` / `$ref`. Prefer `batch` with 20–60 commands. Always pass explicit `ids` / `parent`; never rely on the selection or the current page.

## Pages

| Page | What it holds |
|---|---|
| `00 · Foundations` | The design system: `Colors` (every token as a swatch with name, value, Light and Dark), `Typography` (the scale set in real copy, each line naming its style), `Spacing & radius`, `Icons` (the set the code uses, imported from the repository's SVGs), brand imagery (logo, mascot, illustrations), and `Components` — every component as a main component or component set with its variants and states. |
| `01 · <Flow>` … | One page per flow of the task (`01 · Auth & Onboarding`, `02 · Invoices`). Screens in rows, one row per flow or variant, a Bold 32 label above each row. |
| `Review` (design review only) | The approved frame and the built screenshot side by side per state, each difference a numbered callout. |

A design-system task builds or revises `00 · Foundations` and nothing else. A screen-design task adds its flow pages and only ADDS to Foundations a component it proposes (in a `Proposed` section, named in the notes) — it never changes an existing one.

## Foundations — the design system as a file

- Colour **variables** in a `Theme` collection with `Light` and `Dark` modes, named by role exactly as the tokens you propose (`primary`, `on-primary`, `surface`, `text-secondary`); every fill on every screen is bound to a variable, never a raw hex.
- **Text styles** `Type/<role>` (`Type/Headline L`) and **paint styles** `Color/<role>`; apply them with `style.apply`.
- **Components** for every recurring element — status bar, navigation bar, page header, buttons (each style × state as variants: default, pressed, disabled, loading), inputs (empty, filled, focus, error), cards, list rows, chips, sheets, dialogs, snackbars, empty state. Auto layout inside every component, so text overrides resize it. Component properties for text and booleans where the code has props.
- The values come from the code (design-system-authoring) and from `propose_design_system`'s tokens — the file and the proposal say the same thing. Contrast-check every text/background pair you draw.

## Screens

- Device frames at real size: iPhone 393 × 852 (mobile), 768 × 1024 tablet, 1440 × 900 web. A long scrolling screen is one taller frame named `… — full scroll`, never cut.
- Frame name `<Area> / <Screen> — <state>` (`Invoices / List — empty`), variant in the name when there are several (`Invoices / List — A · default`). Every state of every screen is its own frame (rule every-state-designed): default, loading, empty, error, dark, and the control states that change the layout.
- Build from **instances** of the Foundations components (`instance.create {component, parent, x, y}`) and override their text; draw locally only what the design system lacks, and name it as a proposed addition.
- Auto layout for real structure — lists, rows, cards, buttons, sections — with gap and padding from the spacing tokens, so the frame behaves when copy changes. Name layers by meaning (`Header`, `Invoice row`, `Primary CTA`), never `Frame 12`.
- Real copy in the product's language (rule real-content-no-lorem); real imagery from the repository's assets (`file.placeImage`), icons imported as SVG from the repository (`file.import`, resized with `transform.scale`, recoloured on the child vector), not redrawn.
- Variants (design-variants) are rows on the same page, A above B, the same screens in the same columns.
- Prototype connections for the main path of a flow when the task is a flow (`On click → Navigate to`).

## Verify

After each batch, `screenshot {ids: [frameId]}` the frames it built — never a whole page of other work — and fix what you see: clipped text, overlaps, an instance that lost its override, a fill not bound to a variable, a raw hex, misaligned edges, anything visual-craft's detail pass fails. `inspect_document` / `get_node` with the frame id tells you sizes, fills and overrides. Ids a batch returns without `as` can be off by one — always use `as` / `$ref` and verify. Two fix rounds at most; what is still open goes into the notes.

## The notes document

The file is the design; the task still carries ONE short HTML document (sanitizer-safe-html) under the usual title — `design: <feature>`, `design system: <name> v<N>`, `design review: <screen>` — because the human comments on it, developers get it as text, and attaching it is what sends the task to review. It holds:

- one line saying the design is the FigCraft file on this task (the task view renders its pages and opens it in FigCraft), with the document name;
- per screen: the frames (by exact frame name), each variant's idea, what it costs, the one you recommend and why;
- the decisions on palette, type, imagery and layout and their reasons (visual-craft, avoid-ai-default-looks);
- tokens and components proposed, by name and value;
- the ASCII wireframe of each screen (they survive the text rendition developers get);
- for a design system: the token table per repository (today in code · design system · layer or drift) and the lint warnings left;
- the self-check result.

No HTML mockup of the screens and no loopback server: the pages of the file are what the human reviews. Revisions (`need_revision`) change the SAME file and the SAME notes document; resolve the annotations in one `resolve_document_annotations` call.

## Other ArtCraft servers

`vectorcraft` draws what FigCraft should import as finished vectors — an icon the set lacks, a logo mark, a spot illustration — export SVG into the design files folder and `file.import` it. `photocraft` prepares raster imagery — crop, mask, retouch a product photo or a mockup — export PNG/WebP and `file.placeImage` it. Both write only inside the design files folder (the folder `task_file` is in).

## Common Mistakes

| Mistake | Fix |
|---|---|
| A screen as one image or one flat group | Frames, auto layout, instances, text layers |
| Raw hex on a fill | Bind to the `Theme` variable |
| Editing a Foundations component in a screen task | Add a proposed component; never change an approved one |
| Forgetting `save_file` | Save after each page and before the run ends |
| Writing outside `task_file` | Only `task_file`; the system promotes it on approval |
| Re-drawing icons | Import the repository's SVGs |
