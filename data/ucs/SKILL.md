---
name: ucs
description: "Skill for the Ucs area of iVista-Client-Application. 142 symbols across 23 files."
---

# Ucs

142 symbols | 23 files | Cohesion: 87%

## When to Use

- Working with code in `V3SClient/`
- Understanding how ViewCamera, FlexibleTimePicker, PlaybackSegment work
- Modifying ucs-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/ucs/ViewCamera.xaml.cs` | ViewCamera, OnPropertyChanged, ForwardMetaAI, SetTextCenterButton, SetSegments (+22) |
| `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | PlaybackSegment, GetPlayerState, ConnectedCamera, btnLive_MouseDown, btnPlayCamera_Click (+21) |
| `V3SClient/ucs/TimelineControl.xaml.cs` | LaneData, TimelineControl_SizeChanged, SetTimeRange, Clear, BtnExpand_Changed (+15) |
| `V3SClient/ucs/ViewCamGroupWithOrganization.xaml.cs` | TreeViewItem_DoubleClick, GetVisibleCamsFromArea, GetVisibleCamsFromUnit, Camera_CheckedChanged, GetCheckedCamsRecursive (+6) |
| `V3SClient/ucs/UCTrajectoryMap.xaml.cs` | UCTrajectoryMap_Loaded, InitializeWebViewAsync, CoreWebView2_WebMessageReceived, ConfigureOfflineMap, ShowTrajectory (+5) |
| `V3SClient/ucs/FlexibleTimePicker.xaml.cs` | FlexibleTimePicker, OnPropertyChanged, UpdateUI, RenderCalendar, Day_Click (+4) |
| `V3SClient/ucs/LineChart.xaml.cs` | SetAxisXLimits, timer_Tick, SetVal, MeasureModel, LineChart (+1) |
| `V3SClient/ucs/ViewCamGroupList.xaml.cs` | TreeViewItem_DoubleClick, GetVisibleCameras, Camera_CheckedChanged, GetCheckedCamerasRecursive, FilterTree (+1) |
| `V3SClient/ucs/VehicleCaptureResultControl.xaml.cs` | GetScrollStep, PreviousImages_Click, NextImages_Click, ImageScrollViewer_ScrollChanged, UpdateNavigationButtons |
| `V3SClient/ucs/ucImageViewer.xaml.cs` | LoadImage, btnActualSize_Click, ResetToActualSize |

## Entry Points

Start here when exploring this area:

- **`ViewCamera`** (Class) — `V3SClient/ucs/ViewCamera.xaml.cs:38`
- **`FlexibleTimePicker`** (Class) — `V3SClient/ucs/FlexibleTimePicker.xaml.cs:11`
- **`PlaybackSegment`** (Class) — `V3SClient/ucs/ViewCameraPlayback.xaml.cs:152`
- **`ViewCameraPlayback`** (Class) — `V3SClient/ucs/ViewCameraPlayback.xaml.cs:35`
- **`MeasureModel`** (Class) — `V3SClient/ucs/LineChart.xaml.cs:167`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ViewCamera` | Class | `V3SClient/ucs/ViewCamera.xaml.cs` | 38 |
| `FlexibleTimePicker` | Class | `V3SClient/ucs/FlexibleTimePicker.xaml.cs` | 11 |
| `PlaybackSegment` | Class | `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | 152 |
| `ViewCameraPlayback` | Class | `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | 35 |
| `MeasureModel` | Class | `V3SClient/ucs/LineChart.xaml.cs` | 167 |
| `LineChart` | Class | `V3SClient/ucs/LineChart.xaml.cs` | 26 |
| `UCTrajectoryMap` | Class | `V3SClient/ucs/UCTrajectoryMap.xaml.cs` | 15 |
| `PositionPoint` | Class | `V3SClient/ucs/UCTrajectoryMap.xaml.cs` | 21 |
| `SetTimeRange` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 63 |
| `Clear` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 72 |
| `AddCameraLane` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 131 |
| `AddVideoSegments` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 214 |
| `AddEventMarker` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 220 |
| `UpdatePlayhead` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 253 |
| `ClearSelection` | Method | `V3SClient/ucs/TimelineControl.xaml.cs` | 533 |
| `OnPropertyChanged` | Method | `V3SClient/ucs/ViewCamera.xaml.cs` | 221 |
| `SetTextCenterButton` | Method | `V3SClient/ucs/ViewCamera.xaml.cs` | 475 |
| `SetSegments` | Method | `V3SClient/ucs/ViewCamera.xaml.cs` | 689 |
| `GetRecordStatus` | Method | `V3SClient/Services/DatabaseHelper.cs` | 230 |
| `LogError` | Method | `V3SClient/libs/LoggerManager.cs` | 72 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PlaybackHLS → LogException` | cross_community | 7 |
| `PlaybackHLS → SetState` | cross_community | 7 |
| `PlaybackHLS → MapVideoPositionToRealTimeOffset` | cross_community | 6 |
| `PlaybackHLS → ReleaseDraw` | cross_community | 6 |
| `PlaybackHLS → PlayerInfo` | cross_community | 6 |
| `Playback → TimeToX` | cross_community | 6 |
| `ShowCamera → GetEndpointToken` | cross_community | 6 |
| `ShowCamera → GeneralLog` | cross_community | 6 |
| `ShowCamera → InitDraw` | cross_community | 6 |
| `ShowCamera → PlayerInfo` | cross_community | 6 |

## Connected Areas

| Area | Connections |
|------|-------------|
| V3SClient | 4 calls |
| Models | 3 calls |
| ViewModels | 2 calls |
| Libs | 2 calls |

## How to Explore

1. `context({name: "ViewCamera"})` — see callers and callees
2. `query({search_query: "ucs"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
