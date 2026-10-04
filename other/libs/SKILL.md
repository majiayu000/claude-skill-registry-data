---
name: libs
description: "Skill for the Libs area of iVista-Client-Application. 170 symbols across 41 files."
---

# Libs

170 symbols | 41 files | Cohesion: 81%

## When to Use

- Working with code in `V3SClient/`
- Understanding how BaseColumnDefinition, TextColumnDefinition, CheckBoxColumnDefinition work
- Modifying libs-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/libs/ApiManager.cs` | SetBackendToken, LoginAsync, GetMyAuthorizedProfilesAsync, GetMeAsync, GetDiscoveredEndpoints (+21) |
| `V3SClient/libs/Counter.cs` | GetFreeRAMInPercent, GetNetworkSentBytes, GetNetworkReceivedBytes, GetGpuData, GetOnboardGPUUtilization (+18) |
| `V3SClient/libs/CustomColumnDefinition.cs` | TextColumnDefinition, CheckBoxColumnDefinition, ComboBoxColumnDefinition, DateColumnDefinition, ButtonColumnDefinition (+16) |
| `V3SClient/libs/RedisPubSubManager.cs` | Publish, CmdControl, SetMaster, Configure, Connect (+2) |
| `V3SClient/libs/NodeDefines.cs` | CamInfoNode, CamData_PropertyChanged, OnPropertyChanged, UnitNode, AreaNode (+1) |
| `V3SClient/libs/MetaAIResultStorage.cs` | EnsureTodayFilePath, SaveData, StartAutoSave, StopAutoSave, ResetDataIfNewDay (+1) |
| `V3SClient/libs/SmartDownloadManager.cs` | DownloadTask, OnPropertyChanged, StartSmartDownloadAsync, DownloadSessionAsync, DownloadFileStreamedAsync |
| `V3SClient/libs/CommandStruct.cs` | CommandBase, ControlCmd, ToString, TalkStatusEvent, DeviceStatusEvent |
| `V3SClient/libs/WebSocketManager.cs` | ConnectAsync, ReceiveLoop, HandleWSMessage, DisconnectAsync, Dispose |
| `V3SClient/ucs/SystemMonitor.xaml.cs` | timer_Tick, SetUpdateSpeed, Grid_RightClick, GetNextRange |

## Entry Points

Start here when exploring this area:

- **`BaseColumnDefinition`** (Class) — `V3SClient/libs/BaseColumnDefinition.cs:9`
- **`TextColumnDefinition`** (Class) — `V3SClient/libs/CustomColumnDefinition.cs:19`
- **`CheckBoxColumnDefinition`** (Class) — `V3SClient/libs/CustomColumnDefinition.cs:38`
- **`ComboBoxColumnDefinition`** (Class) — `V3SClient/libs/CustomColumnDefinition.cs:57`
- **`DateColumnDefinition`** (Class) — `V3SClient/libs/CustomColumnDefinition.cs:86`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `BaseColumnDefinition` | Class | `V3SClient/libs/BaseColumnDefinition.cs` | 9 |
| `TextColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 19 |
| `CheckBoxColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 38 |
| `ComboBoxColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 57 |
| `DateColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 86 |
| `ButtonColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 109 |
| `ImageColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 140 |
| `MultiButtonColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 170 |
| `TwoImageButtonColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 219 |
| `MultiActionButtonColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 297 |
| `ClientListColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 345 |
| `ClientListWrapPanelColumnDefinition` | Class | `V3SClient/libs/CustomColumnDefinition.cs` | 424 |
| `PlaybackSearchResult` | Class | `V3SClient/libs/ApiManager.cs` | 1486 |
| `DownloadTask` | Class | `V3SClient/libs/SmartDownloadManager.cs` | 18 |
| `CommandBase` | Class | `V3SClient/libs/CommandStruct.cs` | 17 |
| `ControlCmd` | Class | `V3SClient/libs/CommandStruct.cs` | 57 |
| `TalkStatusEvent` | Class | `V3SClient/libs/CommandStruct.cs` | 75 |
| `DeviceStatusEvent` | Class | `V3SClient/libs/CommandStruct.cs` | 92 |
| `CamInfoNode` | Class | `V3SClient/libs/NodeDefines.cs` | 10 |
| `UnitNode` | Class | `V3SClient/libs/NodeDefines.cs` | 139 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `InitPipeline → LogException` | cross_community | 6 |
| `InitPipeline → SetState` | cross_community | 6 |
| `InitPipeline → LogException` | cross_community | 6 |
| `InitPipeline → SetState` | cross_community | 6 |
| `SelectdPage → GetValueSafely` | cross_community | 6 |
| `ShowCamera → GetEndpointToken` | cross_community | 6 |
| `ShowCamera → GeneralLog` | cross_community | 6 |
| `ApplyImageSyncConfig → LogWarn` | cross_community | 5 |
| `OnStartup → OnPropertyChanged` | cross_community | 5 |
| `OnStartup → AsyncRelayCommand` | intra_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| V3SClient | 21 calls |
| Services | 11 calls |
| Views | 10 calls |
| Ucs | 4 calls |
| ViewModels | 2 calls |
| Models | 2 calls |
| Viewmodels | 2 calls |
| Window | 1 calls |

## How to Explore

1. `context({name: "BaseColumnDefinition"})` — see callers and callees
2. `query({search_query: "libs"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
