---
name: views
description: "Skill for the Views area of iVista-Client-Application. 146 symbols across 32 files."
---

# Views

146 symbols | 32 files | Cohesion: 81%

## When to Use

- Working with code in `V3SClient/`
- Understanding how AIConfigView, CamInfoView, CameraGroupView work
- Modifying views-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/UI/Views/VLiveStream.xaml.cs` | Node_Selectd_Camera_Changed, ShowCameras, Dispose, UpdateSelectedCameras, RemoveCameraFromCell (+25) |
| `V3SClient/UI/Views/VPlayback.xaml.cs` | PlaybackControl, PlayAllCam, PauseAllCam, SetRatePlayers, Page_Loaded (+17) |
| `V3SClient/UI/Views/VPlaybackHLS.xaml.cs` | PauseAllCam, SeekBackwardPlayers, SeekForwardPlayers, Page_Loaded, CamGroupList_CollectionChanged (+16) |
| `V3SClient/UI/Views/VLivePosition.xaml.cs` | VLivePosition_Unloaded, VLivePosition, PositionPoint, InitializeWebViewAsync, LoadMapAsync (+15) |
| `V3SClient/UI/Views/VWebConfigView.xaml.cs` | NavigateTo, InitializeWebView, UpdatePreInjectionScript, WebView_NavigationCompleted, InjectAuthToken |
| `V3SClient/models/RtspPlayer.cs` | Playing, Pause, Seek, SeekForward, SeekBackward |
| `V3SClient/UI/Views/CameraFloatingWindow.xaml.cs` | StopCamera, BtnClose_Click, ForceClose, OnClosing, ShowCamera |
| `V3SClient/libs/GlobalClass.cs` | FindRowsAndCols, LoadImage |
| `V3SClient/libs/GlobalUserInfo.cs` | SetAllowSelectingForAllCams, SetAllowSelectingRecursive |
| `V3SClient/UI/Views/VConfig.xaml.cs` | LoadInitialWebConfig, MenuButton_Click |

## Entry Points

Start here when exploring this area:

- **`AIConfigView`** (Class) — `V3SClient/ucs/Settings/views/AIConfigView.xaml.cs:6`
- **`CamInfoView`** (Class) — `V3SClient/ucs/Settings/views/CamInfoView.xaml.cs:23`
- **`CameraGroupView`** (Class) — `V3SClient/ucs/Settings/views/CameraGroupView.xaml.cs:23`
- **`ClientInfoView`** (Class) — `V3SClient/ucs/Settings/views/ClientInfoView.xaml.cs:22`
- **`GroupTalkView`** (Class) — `V3SClient/ucs/Settings/views/GroupTalkView.xaml.cs:22`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `AIConfigView` | Class | `V3SClient/ucs/Settings/views/AIConfigView.xaml.cs` | 6 |
| `CamInfoView` | Class | `V3SClient/ucs/Settings/views/CamInfoView.xaml.cs` | 23 |
| `CameraGroupView` | Class | `V3SClient/ucs/Settings/views/CameraGroupView.xaml.cs` | 23 |
| `ClientInfoView` | Class | `V3SClient/ucs/Settings/views/ClientInfoView.xaml.cs` | 22 |
| `GroupTalkView` | Class | `V3SClient/ucs/Settings/views/GroupTalkView.xaml.cs` | 22 |
| `ROIManagementView` | Class | `V3SClient/ucs/Settings/views/ROIManagementView.xaml.cs` | 6 |
| `SystemConfigView` | Class | `V3SClient/ucs/Settings/views/SystemConfigView.xaml.cs` | 6 |
| `VLivePosition` | Class | `V3SClient/UI/Views/VLivePosition.xaml.cs` | 22 |
| `PositionPoint` | Class | `V3SClient/UI/Views/VLivePosition.xaml.cs` | 35 |
| `Camera` | Class | `V3SClient/models/Camera.cs` | 11 |
| `VPlayback` | Class | `V3SClient/UI/Views/VPlayback.xaml.cs` | 38 |
| `VPlaybackHLS` | Class | `V3SClient/UI/Views/VPlaybackHLS.xaml.cs` | 38 |
| `IClosableView` | Interface | `V3SClient/libs/interfaces/IClosableView.cs` | 8 |
| `Dispose` | Method | `V3SClient/UI/Views/VLiveStream.xaml.cs` | 401 |
| `ShowCamerasPreset` | Method | `V3SClient/UI/Views/VLiveStream.xaml.cs` | 431 |
| `ShowCamerasCustom` | Method | `V3SClient/UI/Views/VLiveStream.xaml.cs` | 911 |
| `FindRowsAndCols` | Method | `V3SClient/libs/GlobalClass.cs` | 59 |
| `SetAllowSelectingForAllCams` | Method | `V3SClient/libs/GlobalUserInfo.cs` | 70 |
| `NavigateTo` | Method | `V3SClient/UI/Views/VWebConfigView.xaml.cs` | 145 |
| `Cleanup` | Method | `V3SClient/ucs/Settings/views/AIConfigView.xaml.cs` | 17 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `CoreWebView2_WebMessageReceived → LogException` | cross_community | 8 |
| `CoreWebView2_WebMessageReceived → SetState` | cross_community | 8 |
| `PlaybackHLS → LogException` | cross_community | 7 |
| `PlaybackHLS → SetState` | cross_community | 7 |
| `CoreWebView2_WebMessageReceived → ReleaseDraw` | cross_community | 7 |
| `ApplyImageSyncConfig → LogDebug` | cross_community | 6 |
| `MenuLayout_Click → UpdateCamInfoNodeStreamMode` | cross_community | 6 |
| `PlaybackHLS → MapVideoPositionToRealTimeOffset` | cross_community | 6 |
| `PlaybackHLS → ReleaseDraw` | cross_community | 6 |
| `PlaybackHLS → PlayerInfo` | cross_community | 6 |

## Connected Areas

| Area | Connections |
|------|-------------|
| V3SClient | 8 calls |
| Ucs | 8 calls |
| Services | 6 calls |
| Models | 6 calls |
| Libs | 4 calls |

## How to Explore

1. `context({name: "AIConfigView"})` — see callers and callees
2. `query({search_query: "views"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
