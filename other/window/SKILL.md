---
name: window
description: "Skill for the Window area of iVista-Client-Application. 70 symbols across 10 files."
---

# Window

70 symbols | 10 files | Cohesion: 89%

## When to Use

- Working with code in `V3SClient/`
- Understanding how AIAssignmentViewItem, UserItem, CameraItem work
- Modifying window-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/window/ROIConfigWindow.xaml.cs` | ROIConfigWindow_Loaded, LoadAIServices, LoadSnapshot, SetComboByTag, CboTemplate_SelectionChanged (+8) |
| `V3SClient/window/ClientProfileEditWindow.xaml.cs` | LoadData, FilterUsers, FilterCameras, TxtSearchUser_TextChanged, TxtSearchCamera_TextChanged (+6) |
| `V3SClient/window/AIConfigWindow.xaml.cs` | AIConfigWindow_Loaded, LoadCameraInfo, LoadServices, UpdateAvailableServices, LoadData (+5) |
| `V3SClient/libs/ApiManager.cs` | GetCameraAIConfigsAsync, AssignCameraToAIAsync, RemoveAIAssignmentAsync, GetCameraDetailAsync, GetAccountsAsync (+4) |
| `V3SClient/window/LoginWindow.xaml.cs` | LoginButton_Click, LoadClientInfo, SaveLoginInfo, DeleteLoginInfo, EncodeBase64 (+4) |
| `V3SClient/window/ImageViewerWindow.xaml.cs` | SetImage, FitImage_Click, FitImage, ZoomIn_Click, ZoomOut_Click (+2) |
| `V3SClient/window/ROIManagementWindow.xaml.cs` | ROIManagementWindow_Loaded, LoadData, BtnAdd_Click, BtnRefresh_Click, BtnEdit_Click (+1) |
| `V3SClient/window/CameraEditWindow.xaml.cs` | PopulateFields, cboCameraType_SelectionChanged, UpdateFieldVisibility |
| `V3SClient/libs/GlobalUserInfo.cs` | SetLoginTime |
| `V3SClient/UI/Pages/PObjectDetail.xaml.cs` | ViewOriginalImage_Click |

## Entry Points

Start here when exploring this area:

- **`AIAssignmentViewItem`** (Class) — `V3SClient/window/AIConfigWindow.xaml.cs:206`
- **`UserItem`** (Class) — `V3SClient/window/ClientProfileEditWindow.xaml.cs:234`
- **`CameraItem`** (Class) — `V3SClient/window/ClientProfileEditWindow.xaml.cs:250`
- **`ClientDisplayItem`** (Class) — `V3SClient/window/LoginWindow.xaml.cs:369`
- **`PointViewModel`** (Class) — `V3SClient/window/ROIConfigWindow.xaml.cs:491`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `AIAssignmentViewItem` | Class | `V3SClient/window/AIConfigWindow.xaml.cs` | 206 |
| `UserItem` | Class | `V3SClient/window/ClientProfileEditWindow.xaml.cs` | 234 |
| `CameraItem` | Class | `V3SClient/window/ClientProfileEditWindow.xaml.cs` | 250 |
| `ClientDisplayItem` | Class | `V3SClient/window/LoginWindow.xaml.cs` | 369 |
| `PointViewModel` | Class | `V3SClient/window/ROIConfigWindow.xaml.cs` | 491 |
| `ClientProfileEditWindow` | Class | `V3SClient/window/ClientProfileEditWindow.xaml.cs` | 14 |
| `GetCameraAIConfigsAsync` | Method | `V3SClient/libs/ApiManager.cs` | 595 |
| `AssignCameraToAIAsync` | Method | `V3SClient/libs/ApiManager.cs` | 613 |
| `RemoveAIAssignmentAsync` | Method | `V3SClient/libs/ApiManager.cs` | 647 |
| `GetCameraDetailAsync` | Method | `V3SClient/libs/ApiManager.cs` | 728 |
| `GetAccountsAsync` | Method | `V3SClient/libs/ApiManager.cs` | 249 |
| `GetRoisAsync` | Method | `V3SClient/libs/ApiManager.cs` | 384 |
| `DeleteRoiAsync` | Method | `V3SClient/libs/ApiManager.cs` | 415 |
| `GetAIServicesAsync` | Method | `V3SClient/libs/ApiManager.cs` | 460 |
| `GetCameraSnapshotAsync` | Method | `V3SClient/libs/ApiManager.cs` | 563 |
| `SetLoginTime` | Method | `V3SClient/libs/GlobalUserInfo.cs` | 130 |
| `SetImage` | Method | `V3SClient/window/ImageViewerWindow.xaml.cs` | 29 |
| `AIConfigWindow_Loaded` | Method | `V3SClient/window/AIConfigWindow.xaml.cs` | 37 |
| `LoadCameraInfo` | Method | `V3SClient/window/AIConfigWindow.xaml.cs` | 44 |
| `LoadServices` | Method | `V3SClient/window/AIConfigWindow.xaml.cs` | 60 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `ExecuteAdd → LogDebug` | cross_community | 5 |
| `ExecuteAdd → LogInfo` | cross_community | 5 |
| `ExecuteAdd → LogWarn` | cross_community | 5 |
| `ExecuteEdit → LogDebug` | cross_community | 5 |
| `ExecuteEdit → LogInfo` | cross_community | 5 |
| `ExecuteEdit → LogWarn` | cross_community | 5 |
| `OnEditItem → UpdateFieldVisibility` | cross_community | 4 |
| `ExecuteAdd → GetAccountsAsync` | cross_community | 4 |
| `ExecuteAdd → FilterUsers` | cross_community | 4 |
| `ExecuteEdit → GetAccountsAsync` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Libs | 6 calls |
| Views | 2 calls |
| Services | 2 calls |
| V3SClient | 2 calls |

## How to Explore

1. `context({name: "AIAssignmentViewItem"})` — see callers and callees
2. `query({search_query: "window"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
