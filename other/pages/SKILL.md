---
name: pages
description: "Skill for the Pages area of iVista-Client-Application. 46 symbols across 9 files."
---

# Pages

46 symbols | 9 files | Cohesion: 89%

## When to Use

- Working with code in `V3SClient/`
- Understanding how LeftMenu, VAISearchArgs, SetBottomContent work
- Modifying pages-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/UI/Pages/VAISearchPage.xaml.cs` | EnableSelectionRecursive, EnableSelectionRecursive, EnableSelectionRecursive, Loaded_Handler, CamGroupList_CollectionChanged (+12) |
| `V3SClient/UI/Pages/LeftMenu.xaml.cs` | SetBottomContent, Org_Nodes_Camera_Selected_Changed, Org_Forward_Camera_Selected_Changed, FindCameraInGroupRecursive, Forward_Camera_Selected_Changed (+3) |
| `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | SetStatus, ClearStatus, AppendStatus, UpdateSelectedCameraCount, VAISearchArgs (+1) |
| `V3SClient/libs/ApiManager.cs` | GetPlateTrajectoryAsync, GetPersonTrajectoryAsync, GetTrajectoryAsync, GetAssetAccessUrlAsync |
| `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs` | ConfigureComboBox, Configure_ComboxContent_1, Configure_ComboxContent_2 |
| `V3SClient/UI/Pages/ViewSearchCustom.xaml.cs` | ConfigureComboBox, Configure_ComboxContent_1, Configure_ComboxContent_2 |
| `V3SClient/UI/Pages/ViewSearch.xaml.cs` | btnExportFiles_MouseLeftButtonDown, GetTargetFolder |
| `V3SClient/UI/Pages/PObjectDetail.xaml.cs` | DisplayImages, LoadImage |
| `V3SClient/libs/GlobalClass.cs` | GetAllKeyPairsMp4Tmp |

## Entry Points

Start here when exploring this area:

- **`LeftMenu`** (Class) — `V3SClient/UI/Pages/LeftMenu.xaml.cs:30`
- **`VAISearchArgs`** (Class) — `V3SClient/UI/Pages/ViewVAISearch.xaml.cs:17`
- **`SetBottomContent`** (Method) — `V3SClient/UI/Pages/LeftMenu.xaml.cs:218`
- **`ActivateCameraSelection`** (Method) — `V3SClient/UI/Pages/VAISearchPage.xaml.cs:219`
- **`SetStatus`** (Method) — `V3SClient/UI/Pages/ViewVAISearch.xaml.cs:137`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `LeftMenu` | Class | `V3SClient/UI/Pages/LeftMenu.xaml.cs` | 30 |
| `VAISearchArgs` | Class | `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | 17 |
| `SetBottomContent` | Method | `V3SClient/UI/Pages/LeftMenu.xaml.cs` | 218 |
| `ActivateCameraSelection` | Method | `V3SClient/UI/Pages/VAISearchPage.xaml.cs` | 219 |
| `SetStatus` | Method | `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | 137 |
| `ClearStatus` | Method | `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | 161 |
| `GetPlateTrajectoryAsync` | Method | `V3SClient/libs/ApiManager.cs` | 841 |
| `GetPersonTrajectoryAsync` | Method | `V3SClient/libs/ApiManager.cs` | 846 |
| `AppendStatus` | Method | `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | 143 |
| `GetAssetAccessUrlAsync` | Method | `V3SClient/libs/ApiManager.cs` | 890 |
| `OnPropertyChanged` | Method | `V3SClient/UI/Pages/LeftMenu.xaml.cs` | 33 |
| `ConfigureComboBox` | Method | `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs` | 77 |
| `Configure_ComboxContent_1` | Method | `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs` | 87 |
| `Configure_ComboxContent_2` | Method | `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs` | 99 |
| `GetAllKeyPairsMp4Tmp` | Method | `V3SClient/libs/GlobalClass.cs` | 115 |
| `ConfigureComboBox` | Method | `V3SClient/UI/Pages/ViewSearchCustom.xaml.cs` | 45 |
| `Configure_ComboxContent_1` | Method | `V3SClient/UI/Pages/ViewSearchCustom.xaml.cs` | 55 |
| `Configure_ComboxContent_2` | Method | `V3SClient/UI/Pages/ViewSearchCustom.xaml.cs` | 68 |
| `DisplayImages` | Method | `V3SClient/UI/Pages/PObjectDetail.xaml.cs` | 28 |
| `UpdateSelectedCameraCount` | Method | `V3SClient/UI/Pages/ViewVAISearch.xaml.cs` | 42 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `SelectdPage → UpdateCommanderVisibility` | cross_community | 4 |
| `ViewVAISearch_SearchRequested → GetTrajectoryAsync` | intra_community | 3 |
| `Loaded_Handler → EnableSelectionRecursive` | intra_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Services | 2 calls |
| V3SClient | 1 calls |
| Views | 1 calls |
| Libs | 1 calls |

## How to Explore

1. `context({name: "LeftMenu"})` — see callers and callees
2. `query({search_query: "pages"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
