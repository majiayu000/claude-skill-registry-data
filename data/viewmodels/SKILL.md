---
name: viewmodels
description: "Skill for the ViewModels area of iVista-Client-Application. 99 symbols across 29 files."
---

# ViewModels

99 symbols | 29 files | Cohesion: 76%

## When to Use

- Working with code in `V3SClient/`
- Understanding how LatestFrameSnapshot, CapturedSnapshot, ProcessingJobStatusItem work
- Modifying viewmodels-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/viewModels/VMQLBSXDK.cs` | Instance_OnProcessingStatusChanged, Instance_OnProcessingUpdated, RefreshData, RefreshProcessingJobs, RefreshRecentCaptures (+27) |
| `V3SClient/viewModels/VMDocumentConfig.cs` | VMDocumentConfig, SaveConfig, TestConnection, InitializeCommands, UpdatePreviews (+4) |
| `V3SClient/viewModels/VMDocumentDashboard.cs` | VMDocumentDashboard, ProcessingRecordModel, OnProcessingUpdated, TryLoadJobData, AddDateParameters (+2) |
| `V3SClient/Services/DatabaseHelper.cs` | GetVisibleProcessingJobCount, GetVisibleProcessingJobs, UpdatePlateFolder, UpdateProcessedFilePath, GetActiveProcessingJobCount (+1) |
| `V3SClient/viewModels/VMAIEvent.cs` | VMAIEvent, FilterAndUpdateEvents, MatchPatternList, LoadEvents, UpdatePagedEvents (+1) |
| `V3SClient/viewModels/VMMetaAIResult.cs` | VMMetaAIResult, Add, Add, AddInternal |
| `V3SClient/models/CapturedSnapshot.cs` | CapturedSnapshot, FromFrame, OnPropertyChanged |
| `V3SClient/libs/ToastManager.cs` | ShowToast, PositionToast, RepositionToasts |
| `V3SClient/models/NamingSegment.cs` | NamingSegment, CharReplacementRule, NamingRule |
| `V3SClient/Services/RtspStreamService.cs` | LatestFrameSnapshot, TryGetLatestFrameSnapshot |

## Entry Points

Start here when exploring this area:

- **`LatestFrameSnapshot`** (Class) — `V3SClient/Services/RtspStreamService.cs:11`
- **`CapturedSnapshot`** (Class) — `V3SClient/models/CapturedSnapshot.cs:8`
- **`ProcessingJobStatusItem`** (Class) — `V3SClient/models/ProcessingJobStatusItem.cs:5`
- **`VMPSearchAndFilter`** (Class) — `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs:126`
- **`ItemEditField`** (Class) — `V3SClient/libs/ItemEditField.cs:13`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `LatestFrameSnapshot` | Class | `V3SClient/Services/RtspStreamService.cs` | 11 |
| `CapturedSnapshot` | Class | `V3SClient/models/CapturedSnapshot.cs` | 8 |
| `ProcessingJobStatusItem` | Class | `V3SClient/models/ProcessingJobStatusItem.cs` | 5 |
| `VMPSearchAndFilter` | Class | `V3SClient/UI/Pages/PSearchAndFilter.xaml.cs` | 126 |
| `ItemEditField` | Class | `V3SClient/libs/ItemEditField.cs` | 13 |
| `ObservableDictionary` | Class | `V3SClient/libs/ObservableDictionary.cs` | 14 |
| `VMItemEditWindow` | Class | `V3SClient/ucs/Settings/viewmodels/VMItemEditWindow.cs` | 15 |
| `VMSystemConfig` | Class | `V3SClient/ucs/Settings/viewmodels/VMSystemConfig.cs` | 12 |
| `LoginViewModel_v3` | Class | `V3SClient/viewModels/LoginViewModel_v3.cs` | 9 |
| `ShellViewModel_v3` | Class | `V3SClient/viewModels/ShellViewModel_v3.cs` | 7 |
| `VMBase` | Class | `V3SClient/viewModels/VMBase.cs` | 11 |
| `VMDocumentConfig` | Class | `V3SClient/viewModels/VMDocumentConfig.cs` | 15 |
| `VMDocumentDashboard` | Class | `V3SClient/viewModels/VMDocumentDashboard.cs` | 36 |
| `VMMetaAIResult` | Class | `V3SClient/viewModels/VMMetaAIResult.cs` | 16 |
| `VMViewSearchCustom` | Class | `V3SClient/viewModels/VMViewSearchCustom.cs` | 9 |
| `PaginationButtonItem` | Class | `V3SClient/viewModels/VMQLBSXDK.cs` | 23 |
| `VMQLBSXDK` | Class | `V3SClient/viewModels/VMQLBSXDK.cs` | 31 |
| `NamingSegment` | Class | `V3SClient/models/NamingSegment.cs` | 7 |
| `CharReplacementRule` | Class | `V3SClient/models/NamingSegment.cs` | 54 |
| `NamingRule` | Class | `V3SClient/models/NamingSegment.cs` | 87 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Add → OnPropertyChanged` | cross_community | 5 |
| `Add → OnPropertyChanged` | cross_community | 5 |
| `Instance_OnProcessingStatusChanged → LogError` | cross_community | 5 |
| `InitializeRealTimeAsync → GetBrush` | cross_community | 5 |
| `InitializeRealTimeAsync → GetIcon` | cross_community | 5 |
| `SaveConfig → Dispose` | cross_community | 5 |
| `SaveConfig → LogWarn` | cross_community | 5 |
| `Instance_OnProcessingUpdated → LogError` | cross_community | 5 |
| `Instance_OnProcessingUpdated → PlateFolderItem` | cross_community | 5 |
| `Instance_OnProcessingUpdated → ResolvePlateColor` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ucs | 15 calls |
| Services | 12 calls |
| Libs | 4 calls |
| V3SClient | 1 calls |
| Views | 1 calls |

## How to Explore

1. `context({name: "LatestFrameSnapshot"})` — see callers and callees
2. `query({search_query: "viewmodels"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
