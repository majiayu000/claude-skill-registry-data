---
name: v3sclient
description: "Skill for the V3SClient area of iVista-Client-Application. 27 symbols across 9 files."
---

# V3SClient

27 symbols | 9 files | Cohesion: 59%

## When to Use

- Working with code in `V3SClient/`
- Understanding how StartCameraMonitor, UpdateCameraStatusById, SetCameraWarningById work
- Modifying v3sclient-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/MainWindow.xaml.cs` | StartCameraMonitor, runInspector, HandleWSMessage, UpdateCameraStatusById, UpdateStatusInGroupsRecursive (+10) |
| `V3SClient/libs/Utils.cs` | GetFfmpegPath, IsRtspUrlValid, CloseAndResetApp |
| `V3SClient/libs/ApiManager.cs` | UpdateDeviceTalkStatusAsync, GetDeviceStatusBatchAsync |
| `V3SClient/libs/GlobalUserInfo.cs` | UpdateCameraStatus, UpdateStatusRecursive |
| `V3SClient/UI/Views/VLiveStream.xaml.cs` | SetCameraWarningById |
| `V3SClient/libs/LoggerManager.cs` | LogException |
| `V3SClient/libs/MediaHelper.cs` | IsMp4FileValidUseFfprobe |
| `V3SClient/libs/RedisPubSubManager.cs` | Unsubscribe |
| `V3SClient/UI/Views/EMap.xaml.cs` | UpdateActiveCameras |

## Entry Points

Start here when exploring this area:

- **`StartCameraMonitor`** (Method) — `V3SClient/MainWindow.xaml.cs:151`
- **`UpdateCameraStatusById`** (Method) — `V3SClient/MainWindow.xaml.cs:294`
- **`SetCameraWarningById`** (Method) — `V3SClient/UI/Views/VLiveStream.xaml.cs:295`
- **`UpdateDeviceTalkStatusAsync`** (Method) — `V3SClient/libs/ApiManager.cs:1540`
- **`GetDeviceStatusBatchAsync`** (Method) — `V3SClient/libs/ApiManager.cs:1556`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `StartCameraMonitor` | Method | `V3SClient/MainWindow.xaml.cs` | 151 |
| `UpdateCameraStatusById` | Method | `V3SClient/MainWindow.xaml.cs` | 294 |
| `SetCameraWarningById` | Method | `V3SClient/UI/Views/VLiveStream.xaml.cs` | 295 |
| `UpdateDeviceTalkStatusAsync` | Method | `V3SClient/libs/ApiManager.cs` | 1540 |
| `GetDeviceStatusBatchAsync` | Method | `V3SClient/libs/ApiManager.cs` | 1556 |
| `UpdateCameraStatus` | Method | `V3SClient/libs/GlobalUserInfo.cs` | 100 |
| `LogException` | Method | `V3SClient/libs/LoggerManager.cs` | 89 |
| `IsMp4FileValidUseFfprobe` | Method | `V3SClient/libs/MediaHelper.cs` | 105 |
| `Unsubscribe` | Method | `V3SClient/libs/RedisPubSubManager.cs` | 148 |
| `GetFfmpegPath` | Method | `V3SClient/libs/Utils.cs` | 282 |
| `IsRtspUrlValid` | Method | `V3SClient/libs/Utils.cs` | 294 |
| `UpdateActiveCameras` | Method | `V3SClient/UI/Views/EMap.xaml.cs` | 38 |
| `CloseAndResetApp` | Method | `V3SClient/libs/Utils.cs` | 22 |
| `runInspector` | Method | `V3SClient/MainWindow.xaml.cs` | 197 |
| `HandleWSMessage` | Method | `V3SClient/MainWindow.xaml.cs` | 240 |
| `UpdateStatusInGroupsRecursive` | Method | `V3SClient/MainWindow.xaml.cs` | 318 |
| `UpdateCameraPTTStatus` | Method | `V3SClient/MainWindow.xaml.cs` | 337 |
| `Window_Loaded` | Method | `V3SClient/MainWindow.xaml.cs` | 643 |
| `InitializeRealTimeAsync` | Method | `V3SClient/MainWindow.xaml.cs` | 652 |
| `btnNativeConfig_Click` | Method | `V3SClient/MainWindow.xaml.cs` | 719 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `CoreWebView2_WebMessageReceived → LogException` | cross_community | 8 |
| `PlaybackHLS → LogException` | cross_community | 7 |
| `InitPipeline → LogException` | cross_community | 6 |
| `InitPipeline → LogException` | cross_community | 6 |
| `BtnEMap_Click → PositionPoint` | cross_community | 6 |
| `SelectdPage → PositionPoint` | cross_community | 6 |
| `SelectdPage → GetValueSafely` | cross_community | 6 |
| `Monitor → LogException` | cross_community | 5 |
| `InitPipeline → LogException` | cross_community | 5 |
| `InitializeRealTimeAsync → GetBrush` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| ViewModels | 1 calls |
| Ucs | 1 calls |
| Services | 1 calls |
| Views | 1 calls |
| Libs | 1 calls |

## How to Explore

1. `context({name: "StartCameraMonitor"})` — see callers and callees
2. `query({search_query: "v3sclient"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
