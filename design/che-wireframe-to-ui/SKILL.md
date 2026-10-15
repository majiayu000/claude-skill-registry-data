---
name: "che-wireframe-to-ui"
description: "End-to-end UI generation: ingest a wireframe (.excalidraw / PNG) plus design references (images / links), derive a design system (tokens.json + DESIGN.md), then produce the screens in OpenPencil for a developer to implement. Trigger: /che-wireframe-to-ui."
---

# Che — Wireframe → UI (Orchestrator)

Turns a designer's wireframe plus visual references into a developer-ready design system and screens.
This skill **orchestrates**; it does not re-implement the design engine (`che-social-ui-designer` MODE B/C).

## 1. Inputs (at least one wireframe is mandatory)

| Input | Form | Used for |
|---|---|---|
| Wireframe | `.excalidraw` file | structure (IR) — deterministic parse |
| Wireframe | PNG / JPG image | structure — read via vision, then normalised to the same IR |
| Reference | image(s) | palette / typography / mood |
| Reference | URL(s) | palette / typography / mood |

Ask via `AskUserQuestion` which inputs are present before starting.

## 2. Pipeline (stop on the first failure)

1. **Structure** — `che designer ingest wireframe <file.excalidraw> --out ir.json`, then `che designer ir validate ir.json`.
   - For a PNG/JPG wireframe: read it with vision, emit the same IR shape (`domains/ux/templates/wireframe-ir.schema.json`), then `che designer ir validate`.
2. **Theme** — from the references, propose a palette (and fonts) and write `proposed.json` (`{"colors": {"primary": "#RRGGBB", ...}}`).
   - `che designer init <wt> <session_id> --sub-product <slug>` once, if the design tree does not exist.
   - `che designer ingest theme <wt> --sub-product <slug> --colors proposed.json`.
3. **Handoff contract** — `che designer tokens render <wt>`, then `che designer validate <wt>/design/DESIGN.md`.
4. **Screens** — delegate to the `che-social-ui-designer` skill (MODE B for feature screens, MODE C for the component set), consuming `design/DESIGN.md` + `design/tokens/tokens.json`.

## 3. Gates

- The `che-social-ui-designer` SPEC approval gate still applies before any pixel is drawn.
- WCAG 2.2 AA contrast is checked on the proposed palette before stage 4.
- The IR is the only structure contract; every source adapter emits the same shape (`skills/che-social-ui-designer/references/DESIGN_BACKEND_CONTRACT.md`).

## 4. Outputs

- `design/tokens/tokens.json` — single source of truth for the design system.
- `design/DESIGN.md` — Stitch handoff contract for the developer.
- OpenPencil screens + dev-spec — produced by `che-social-ui-designer`.

## 5. Boundaries

- Ingest is deterministic and stdlib-only for `.excalidraw`; vision (PNG/links) only proposes, the CLI validates.
- Never write design artifacts outside the bound worktree's `design/` tree.
