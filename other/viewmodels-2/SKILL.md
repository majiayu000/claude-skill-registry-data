---
name: viewmodels-2
description: "Skill for the Viewmodels area of iVista-Client-Application. 50 symbols across 15 files."
---

# Viewmodels

50 symbols | 15 files | Cohesion: 76%

## When to Use

- Working with code in `V3SClient/`
- Understanding how CameraGroupInfo, CameraGroupModel, GroupSelection work
- Modifying viewmodels-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/ucs/Settings/viewmodels/VMPageableBase.cs` | CanGoNext, UpdatePagedItems, FilteredItems, VMPageableBase, EditSelectedItem (+5) |
| `V3SClient/libs/ApiManager.cs` | GetCameraGroupsAsync, CameraGroupInfo, DeleteCameraGroupAsync, GetAllCamerasAsync, DeleteCameraAsync (+3) |
| `V3SClient/ucs/Settings/viewmodels/VMCamInfo.cs` | LoadGroups, OnROIConfig, OnAIConfig, OnAddCamera, OnEditItem (+3) |
| `V3SClient/ucs/Settings/viewmodels/VMCameraGroup.cs` | LoadData, OnEditItem, OnAddItem, OnDeleteItem, VMCameraGroup |
| `V3SClient/ucs/Settings/viewmodels/VMClientInfo.cs` | VMClientInfo, LoadData, OnDeleteItem, ExecuteAdd, ExecuteEdit |
| `V3SClient/ucs/Settings/viewmodels/VMGroupTalkInfo.cs` | LoadData, OnEditItem, OnAddItem, VMGroupTalkInfo |
| `V3SClient/window/CameraEditWindow.xaml.cs` | GroupSelection, LoadGroups |
| `V3SClient/ucs/Settings/models/CameraGroupModel.cs` | CameraGroupModel |
| `V3SClient/UI/Converters/PermissionVisibilityConverter.cs` | Convert |
| `V3SClient/libs/GlobalUserInfo.cs` | HasPermission |

## Entry Points

Start here when exploring this area:

- **`CameraGroupInfo`** (Class) — `V3SClient/libs/ApiManager.cs:541`
- **`CameraGroupModel`** (Class) — `V3SClient/ucs/Settings/models/CameraGroupModel.cs:9`
- **`GroupSelection`** (Class) — `V3SClient/window/CameraEditWindow.xaml.cs:19`
- **`CamInfoModel`** (Class) — `V3SClient/ucs/Settings/models/CamInfoModel.cs:9`
- **`VMCamInfo`** (Class) — `V3SClient/ucs/Settings/viewmodels/VMCamInfo.cs:18`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `CameraGroupInfo` | Class | `V3SClient/libs/ApiManager.cs` | 541 |
| `CameraGroupModel` | Class | `V3SClient/ucs/Settings/models/CameraGroupModel.cs` | 9 |
| `GroupSelection` | Class | `V3SClient/window/CameraEditWindow.xaml.cs` | 19 |
| `CamInfoModel` | Class | `V3SClient/ucs/Settings/models/CamInfoModel.cs` | 9 |
| `VMCamInfo` | Class | `V3SClient/ucs/Settings/viewmodels/VMCamInfo.cs` | 18 |
| `VMClientInfo` | Class | `V3SClient/ucs/Settings/viewmodels/VMClientInfo.cs` | 20 |
| `VMPageableBase` | Class | `V3SClient/ucs/Settings/viewmodels/VMPageableBase.cs` | 12 |
| `VMPageableDynamicGridMain` | Class | `V3SClient/ucs/Settings/viewmodels/VMPageableDynamicGridMain.cs` | 13 |
| `VMPageableDynamicGridSub` | Class | `V3SClient/ucs/Settings/viewmodels/VMPageableDynamicGridSub.cs` | 12 |
| `ClientInfoModel` | Class | `V3SClient/ucs/Settings/models/ClientInfoModel.cs` | 8 |
| `IDynamicGridViewModel` | Interface | `V3SClient/libs/interfaces/IDynamicGridViewModel.cs` | 9 |
| `GetCameraGroupsAsync` | Method | `V3SClient/libs/ApiManager.cs` | 478 |
| `Convert` | Method | `V3SClient/UI/Converters/PermissionVisibilityConverter.cs` | 14 |
| `DeleteCameraGroupAsync` | Method | `V3SClient/libs/ApiManager.cs` | 528 |
| `HasPermission` | Method | `V3SClient/libs/GlobalUserInfo.cs` | 135 |
| `GetAllCamerasAsync` | Method | `V3SClient/libs/ApiManager.cs` | 661 |
| `DeleteCameraAsync` | Method | `V3SClient/libs/ApiManager.cs` | 715 |
| `GetCameraDependenciesAsync` | Method | `V3SClient/libs/ApiManager.cs` | 746 |
| `GetClientProfilesAsync` | Method | `V3SClient/libs/ApiManager.cs` | 203 |
| `DeleteClientProfileAsync` | Method | `V3SClient/libs/ApiManager.cs` | 302 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `ExecuteAdd → LogDebug` | cross_community | 5 |
| `ExecuteAdd → LogInfo` | cross_community | 5 |
| `ExecuteAdd → LogWarn` | cross_community | 5 |
| `ExecuteEdit → LogDebug` | cross_community | 5 |
| `ExecuteEdit → LogInfo` | cross_community | 5 |
| `ExecuteEdit → LogWarn` | cross_community | 5 |
| `OnDeleteItem → FilteredItems` | cross_community | 4 |
| `OnEditItem → GetMediaServersAsync` | cross_community | 4 |
| `OnEditItem → GetCameraGroupsAsync` | cross_community | 4 |
| `OnEditItem → GroupSelection` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| ViewModels | 2 calls |
| Views | 1 calls |
| Services | 1 calls |
| Libs | 1 calls |
| V3SClient | 1 calls |

## How to Explore

1. `context({name: "CameraGroupInfo"})` — see callers and callees
2. `query({search_query: "viewmodels"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
