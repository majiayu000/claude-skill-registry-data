---
name: gallery-ui
description: >-
  React component patterns, CSS Modules styling, design tokens, virtualization,
  and UX constitution for the Driftara Gallery renderer. Use for src/ UI work,
  styling, FilterPanel/GalleryGrid/ImageViewer, or design:check—not electron/db
  unless coordinated with gallery-electron-ts.
---

# Gallery UI

## When to apply

- Renderer changes under **`src/`** (components, styles, hooks used by UI)
- Styling, CSS Modules, design-token usage
- Gallery grid, viewer, filters, layout shell

## Out of scope

- **`electron/`** DB, IPC, main process — defer to **`gallery-electron-ts`**
- Backend `/ui/` — defer to **`backend-frontend-ui`**
- Editing **`src/tokens.json`** — defer to **image-scoring-ui** **`design-tokens`** skill

## Read first

1. [docs/design/UX_UI_CONSTITUTION.md](../../../docs/design/UX_UI_CONSTITUTION.md) — gallery binding
2. [image-scoring-ui UX_UI_CONSTITUTION.md](https://github.com/synthet/image-scoring-ui/blob/main/docs/UX_UI_CONSTITUTION.md) — shared articles
3. [docs/design/FRONTEND_UX_SPEC.md](../../../docs/design/FRONTEND_UX_SPEC.md) — typography, spacing, layout
4. [image-scoring-ui DESIGN_SYSTEM.md](https://github.com/synthet/image-scoring-ui/blob/main/docs/DESIGN_SYSTEM.md)

## Design tokens

| Need | Source |
|------|--------|
| Shared colors | `src/styles/tokens.css` → `@synthet/image-scoring-design/tokens.css` |
| Layout/spacing only | `src/styles/tokens.local.css` |
| Stage names | `src/constants/pipelineLabels.ts` |
| Embedding icon | `EmbeddingSpaceIcon`, `EMBEDDING_SPACE_LABELS` from package |
| Photo labels | `LABEL_COLORS` from package or `var(--label-*)` |

**Rules:** CSS Modules for new UI; `var(--color-*)` not hex; `npm run design:check` before done.

## Component architecture

```
App.tsx                          ← Root: state, filters, image selection
├── MainLayout                   ← 3-panel layout (header, sidebar, content)
│   ├── header                   ← Current folder name + item count
│   ├── sidebar
│   │   ├── FilterPanel          ← Rating slider, color label filter
│   │   ├── Keyword/Sort selects
│   │   └── FolderTree
│   └── content
│       ├── GalleryGrid          ← Virtualized image/stack grid
│       └── ImageViewer          ← Full-screen viewer overlay
```

## Styling conventions

- **CSS Modules** for component styles (e.g. `GalleryGrid.module.css`, `toggle.module.css`)
- **Global tokens:** `tokens.css` + `tokens.local.css` loaded from `main.tsx`
- **Legacy inline styles** still exist in some components — migrate token colors when editing; do not expand inline styling for new features
- **Focus:** `2px solid var(--color-accent)` with offset (see FRONTEND_UX_SPEC)
- **Text on images:** gradient overlays OK; use semantic tokens elsewhere

## GalleryGrid (`src/components/Gallery/GalleryGrid.tsx`)

Uses `react-virtuoso`'s `VirtuosoGrid`:

```tsx
<VirtuosoGrid
    style={{ height: '100%' }}
    totalCount={displayData.length}
    overscan={400}
    endReached={handleEndReached}
    components={{ List: ItemContainer, Item: ItemWrapper }}
    itemContent={itemContent}
/>
```

- Fixed item size: 180×240px cards
- Dual mode: images vs stacks
- Label borders: package `LABEL_COLORS` / `--label-*`, not status colors
- Images: `media://` protocol (main process)
- **Detection overlays** (`bird_bbox` / `BirdBoxOverlay`): center an
  `aspect-ratio: img_w / img_h` wrapper inside `.imageArea` so fractional boxes
  align under `object-fit: contain` letterboxing — do **not** position against
  the full cell.

## FilterPanel

`FilterState` in `FilterPanel.tsx`:

```typescript
interface FilterState {
    minRating?: number;
    colorLabel?: string;
    keyword?: string;
    sortBy?: string;
    order?: 'ASC' | 'DESC';
}
```

New filter: extend `FilterState`, UI in `FilterPanel`, then `electron/db.ts` query options.

## ImageViewer

Full-screen overlay: prev/next, metadata, in-viewer edits, Escape to close.

## Commands

```bash
npm run design:check
npm run typecheck
npm run lint        # known pre-existing issues; avoid new errors
```

## Deliverable format

Summary, files touched, `design:check` and `tsc` results (or why not run).
