---
name: repo-workflows
description: Git-history-derived workflows, co-change patterns, and iteration rhythms for ProAnimate. Auto-applied when planning multi-file changes.
version: 1.0.0
source: local-git-analysis
analyzed_commits: 200
user-invocable: false
---

# ProAnimate Repository Workflows

Patterns extracted from the last 200 commits (2026-03-17 to 2026-03-19).

## Commit Conventions

**Format**: `type(scope): description`

| Type | Usage | Frequency |
|------|-------|-----------|
| `feat` | New features | ~20% of commits |
| `fix` | Bug fixes | ~2% |
| `Add` | New files/features (informal) | ~18% |
| `Fix` | Bug fixes (informal) | ~18% |
| `Move` | Reorganizing tabs/panels | ~6% |
| `Remove` | Cleanup | ~5% |
| `Replace` | Swapping implementations | ~4.5% |
| `Revert`/`Restore` | Undoing changes | ~4% |

**Scopes** (when conventional): `mobile`, `core`, `timeline`, `api`, `server`

**Note**: About half of commits use conventional format (`feat(scope):`), the other half use imperative verbs (`Add`, `Fix`, `Move`). Both are acceptable.

## File Co-Change Patterns

These files almost always change together. If you touch one, check the others.

### Adding a Panel (3-file rule)
1. `src/types/editor.ts` — add tab ID to union type
2. `src/constants/tabGroups.ts` — register in TAB_GROUPS array
3. `src/components/layout/LeftPanel/LeftPanel.tsx` — add lazy import + PanelContent case

**Evidence**: 100% of panel-addition commits touch all 3 files.

### Moving/Reorganizing Tabs
1. `src/constants/tabGroups.ts` — move sub-tab between groups
2. Sometimes `src/types/editor.ts` — if TabGroupId changes
3. Sometimes `src/components/layout/LeftPanel/LeftPanel.tsx` — if GROUP_ICONS needs update

### Whiteboard Feature Changes (5-file cluster)
1. `src/components/panels/WhiteboardPanel.tsx` (32 changes — most changed file)
2. `src/components/canvas/WhiteboardDrawingOverlay.tsx` (21 changes)
3. `src/components/canvas/WhiteboardLayer.tsx` (16 changes)
4. `src/stores/useWhiteboardStore.ts` (13 changes)
5. `src/services/whiteboardAnimation.ts` (13 changes)

### Right Panel Properties
- `src/components/layout/RightPanel/RightPanel.tsx` co-changes with any panel that has properties
- Whiteboard properties panels (Drawing, Text, Stroke) change together

## Iteration Rhythms

### Revert-Heavy Areas
The whiteboard and drawing tools have a high revert rate (~10 reverts in 200 commits). This indicates:
- **UI preferences are subjective** — always confirm visual changes with the user before committing
- **Keep reverts cheap** — make small, atomic commits for visual/UX changes
- Common revert patterns: draw style presets, color picker layouts, cursor icons, brush settings

### Mobile Sprint Pattern
Mobile features (`feat(mobile):`) come in rapid sequential commits (30 commits in 1 day). Each commit is atomic:
1. Infrastructure first (auth, stores, API client)
2. Renderers and engines next (DynamicRenderer, TypographyRenderer)
3. Screens last (browse, editor, projects, export)
4. Polish/fix passes after (`fix(mobile):`)

### Panel Consolidation Pattern
Recurring pattern of merging panels:
- `Merge Style Effects into Mixed Media panel`
- `Merge Camera into Cinema Studio`
- `Consolidate SVG Art, Components, Motion AI, and Animations into single Assets tab`

**Lesson**: Before adding a new panel, check if it should merge into an existing one.

## High-Churn Files (Touch With Care)

| File | Changes | Risk |
|------|---------|------|
| `WhiteboardPanel.tsx` | 32 | Highly iterated, revert-prone |
| `RightPanel.tsx` | 32 | Many panels feed into it |
| `WhiteboardDrawingOverlay.tsx` | 21 | Complex interaction logic |
| `VideoCanvas.tsx` | 20 | Core rendering surface |
| `WhiteboardLayer.tsx` | 16 | Rendering pipeline |
| `tabGroups.ts` | 14 | Tab organization (merge conflicts) |
| `editor.ts` (types) | 13 | Type unions grow frequently |

## Architecture Hotspots

### Left Panel System
- `LeftPanel.tsx` renders all panels through `PanelContent` switch
- Tab groups defined in `tabGroups.ts` drive navigation
- Large groups (>threshold) show card grid; small groups go direct to panel
- `DrillDownHeader` provides prev/next navigation within groups

### Layout Hierarchy
```
EditorLayout
├── TopMenuBar
├── LeftPanel (collapsible, 300px)
│   ├── MainGroupHeader / DrillDownHeader
│   └── PanelContent (lazy-loaded)
├── Center (flex-1)
│   ├── VideoCanvas / BRViewport / RigEditor3DViewport
│   └── Timeline / BRTimeline / Rig3DTimeline
└── RightPanel (context-sensitive properties)
```

### Collapse Toggle Pattern
Toggle buttons for collapsible panels must be **siblings** of the panel in the flex layout, never children. Placing a toggle inside an `overflow-hidden` collapsible container causes it to be clipped when collapsed.
