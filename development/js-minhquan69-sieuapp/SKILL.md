---
name: js
description: "Skill for the Js area of iVista-Client-Application. 65 symbols across 2 files."
---

# Js

65 symbols | 2 files | Cohesion: 90%

## When to Use

- Working with code in `V3SClient/`
- Understanding how closeTrajectoryImagePreview, openTrajectoryImagePreview, collapseTimeline work
- Modifying js-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/map_assets/js/module_live.js` | normalizeLatLng, toLngLatArray, getFOVWedge, updateFOVSource, initPathLayers (+30) |
| `V3SClient/map_assets/js/module_trajectory.js` | closeTrajectoryImagePreview, openTrajectoryImagePreview, collapseTimeline, setStatus, setSummary (+25) |

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `closeTrajectoryImagePreview` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 65 |
| `openTrajectoryImagePreview` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 73 |
| `collapseTimeline` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 107 |
| `setStatus` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 165 |
| `setSummary` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 172 |
| `hasTrajectoryPopupData` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 178 |
| `stripHtml` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 183 |
| `buildTrajectoryPopupContent` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 189 |
| `renderTimeline` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 254 |
| `initTrajLayer` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 287 |
| `computeDistanceMeters` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 303 |
| `rebuildPlaybackDistanceCache` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 318 |
| `setPlaybackButtons` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 331 |
| `getTrajectoryMode` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 346 |
| `applyPlaybackMarkerVisual` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 350 |
| `ensurePlaybackMarker` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 372 |
| `refreshPlaybackMarkerVisual` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 388 |
| `stopPlayback` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 403 |
| `movePlaybackTo` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 485 |
| `updatePlaybackByDistance` | Function | `V3SClient/map_assets/js/module_trajectory.js` | 499 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `DrawTrajectory → SetPlaybackFocusButton` | cross_community | 7 |
| `DrawTrajectory → FocusPlaybackNow` | cross_community | 7 |
| `ResetPlayback → SetPlaybackFocusButton` | cross_community | 6 |
| `ResetPlayback → FocusPlaybackNow` | cross_community | 6 |
| `UpdatePositions → GetLocalKey` | cross_community | 6 |
| `StartPlayback → SetPlaybackFocusButton` | cross_community | 6 |
| `StartPlayback → FocusPlaybackNow` | cross_community | 6 |
| `StartPlayback → GetTrajectoryMode` | intra_community | 5 |
| `DrawTrajectory → SetPlaybackButtons` | intra_community | 4 |
| `ResetPlayback → SetPlaybackButtons` | intra_community | 3 |

## How to Explore

1. `context({name: "closeTrajectoryImagePreview"})` — see callers and callees
2. `query({search_query: "js"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
