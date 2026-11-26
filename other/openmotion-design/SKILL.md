---
name: openmotion-design
description: >-
  Create, revise, version, annotate, import and export HTML Design Studio projects
  (interactive web/app prototypes, 16:9 slide decks with speaker notes, print-ready documents,
  website clones, data-backed live artifacts and WebGL2 experiences) through openmotion_design_catalog,
  openmotion_design_project, openmotion_design_edit and openmotion_design_comments.
  OpenMotion runs no internal design agent: external Agents author and iterate over MCP while Design Studio previews, annotates and exports.
---

# OpenMotion Design Studio

Author and iterate HTML design deliverables through the four Design Studio MCP tools so the user can inspect responsive views (Desktop, Tablet, Mobile), annotate elements, compare versions, export (ZIP, Open Design package, standalone HTML, PDF, PNG, PPTX) and open projects in local editors.

## Scenarios

| Scenario | Deliver | Guide |
| --- | --- | --- |
| `prototype` | Responsive interactive HTML (`index.html`) | [scenarios](references/scenarios.md#prototype) |
| `deck` | Single-file 1920×1080 HTML slide deck with OD deck host protocol & speaker notes | [scenarios](references/scenarios.md#slide-deck) |
| `document` | Print-ready semantic HTML (`@media print`) exportable to PDF | [scenarios](references/scenarios.md#document) |
| `web-clone` | Functional responsive HTML rebuild from observed references | [scenarios](references/scenarios.md#website-clone) |
| `live-artifact` | `data.json`-driven dashboard with escaped rendering | [scenarios](references/scenarios.md#live-artifact) |
| `webgl` | Real-time WebGL2 canvas with DPR cap and resize/visibility lifecycle | [scenarios](references/scenarios.md#webgl) |

For editable motion films and timeline graphics (`motion-design`, `hyperframes`), use the OpenMotion video production skills instead. For standalone image, video or audio assets, use `openmotion-media`.

## Core workflow

1. **Discover resources:** call `openmotion_design_catalog` (`list_scenarios`, `list_templates`, `list_design_systems`, `list_skills`, `get_craft`) to load the scenario guide, starter template or design system (`DESIGN.md` and `tokens.css`). See [design systems](references/systems.md).
2. **Create or inspect the project:** call `openmotion_design_project` (`action="create"` with `scenario`, optional `templateId` / `designSystemId` and stable `requestId`; or `action="get"` for an existing `projectId` to read its `revision` and file list).
3. **Read before editing:** read existing files with `openmotion_design_edit` (`action="read_file"`, paging with `offset` when `nextOffset` is non-null).
4. **Write atomically with revision protection:** save complete files via `openmotion_design_edit` (`action="write"`, passing `expectedRevision`, `requestId`, `files` and a short `summary`). Every write creates an immutable `vN` version snapshot. To embed a pinned image from the OpenMotion asset library, call `openmotion_design_edit` (`action="import_asset"`, passing `assetId`, `versionId`, `expectedRevision` and `requestId`) to copy the binary into `assets/` and reference the returned project-relative path in HTML.
5. **Present in Design Studio:** call `openmotion_design_project` (`action="open"`) and share the returned `editorUrl` / `previewUrl` so the user can review and annotate.

## Reference guides

- [Scenarios and deck protocol](references/scenarios.md)
- [Iterating from user annotations](references/iterate.md)
- [Export and Open Design round-trip import](references/export.md)
- [Using design systems and craft guides](references/systems.md)
- [Shared material policy](../openmotion-production/references/materials.md) (when generating image or media assets for a design)
- [Shared edit workflow](../openmotion-production/references/edit.md) (for Motion Studio video edits outside Design Studio)
