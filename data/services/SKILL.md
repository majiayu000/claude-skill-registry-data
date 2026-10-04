---
name: services
description: "Skill for the Services area of iVista-Client-Application. 153 symbols across 21 files."
---

# Services

153 symbols | 21 files | Cohesion: 74%

## When to Use

- Working with code in `V3SClient/`
- Understanding how ProcessingTask, UnifiedResult, ClassificationResult work
- Modifying services-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/Services/DatabaseHelper.cs` | InsertRecord, RegisterJob, RegisterJobAsset, MarkJobProcessing, MarkJobRetryPending (+21) |
| `V3SClient/Services/FileWatcherService.cs` | Start, ScanExistingFiles, ExtractPdfAndEnqueuePages, ScanExistingSubdirectories, OnFileOrDirCreated (+16) |
| `V3SClient/Services/LLMClient.cs` | UnifiedResult, ClassificationResult, ImageToDataUrl, ExtractJsonFromText, CallApiAsync (+8) |
| `V3SClient/Services/OutputFolderMonitorService.cs` | Stop, OnFileSystemEvent, ResolveTopLevelOutputFolder, Dispose, CancelAndDispose (+7) |
| `V3SClient/Services/ProcessingPipeline.cs` | ProcessSingleTaskAsync, ProcessFolderTaskAsync, IsAllowedByMode, RejectTask, GetFriendlyError (+6) |
| `V3SClient/Services/DocumentProcessingManager.cs` | RaiseProcessingUpdated, TryQueueManualRetry, Initialize, Start, Stop (+6) |
| `V3SClient/Services/ImageSyncService.cs` | ImageSyncState, ImageSyncResult, LoadState, NormalizeSince, WriteState (+5) |
| `V3SClient/Services/RtspStreamService.cs` | ResolveBundledFfmpegPath, StartPreview, StopPreview, ReadPreviewFrames, PublishFrame (+4) |
| `V3SClient/viewModels/VMQLBSXDK.cs` | SetServiceRunningAsync, ReloadProcessingServices, Dispose, StartDocumentCamera, RestartDocumentCamera (+3) |
| `V3SClient/Services/InputCaptureMonitorService.cs` | Start, OnChanged, GetRecentCaptures, MergeCurrentCaptures, Dispose (+2) |

## Entry Points

Start here when exploring this area:

- **`ProcessingTask`** (Class) — `V3SClient/Services/ProcessingQueue.cs:24`
- **`UnifiedResult`** (Class) — `V3SClient/Services/LLMClient.cs:28`
- **`ClassificationResult`** (Class) — `V3SClient/Services/LLMClient.cs:55`
- **`LLMConfig`** (Class) — `V3SClient/Services/LLMClient.cs:15`
- **`ImageSyncState`** (Class) — `V3SClient/Services/ImageSyncService.cs:15`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ProcessingTask` | Class | `V3SClient/Services/ProcessingQueue.cs` | 24 |
| `UnifiedResult` | Class | `V3SClient/Services/LLMClient.cs` | 28 |
| `ClassificationResult` | Class | `V3SClient/Services/LLMClient.cs` | 55 |
| `LLMConfig` | Class | `V3SClient/Services/LLMClient.cs` | 15 |
| `ImageSyncState` | Class | `V3SClient/Services/ImageSyncService.cs` | 15 |
| `ImageSyncResult` | Class | `V3SClient/Services/ImageSyncService.cs` | 33 |
| `PlateImageItem` | Class | `V3SClient/models/PlateImageItem.cs` | 7 |
| `ProcessingStatusChangedEventArgs` | Class | `V3SClient/Services/DocumentProcessingManager.cs` | 11 |
| `PlateRecognitionData` | Class | `V3SClient/Services/ProcessingQueue.cs` | 12 |
| `FileWatcherService` | Class | `V3SClient/Services/FileWatcherService.cs` | 12 |
| `PdfPageImageExtractionService` | Class | `V3SClient/Services/PdfPageImageExtractionService.cs` | 12 |
| `RtspStreamService` | Class | `V3SClient/Services/RtspStreamService.cs` | 18 |
| `InsertRecord` | Method | `V3SClient/Services/DatabaseHelper.cs` | 193 |
| `RegisterJob` | Method | `V3SClient/Services/DatabaseHelper.cs` | 323 |
| `RegisterJobAsset` | Method | `V3SClient/Services/DatabaseHelper.cs` | 382 |
| `MarkJobProcessing` | Method | `V3SClient/Services/DatabaseHelper.cs` | 410 |
| `MarkJobRetryPending` | Method | `V3SClient/Services/DatabaseHelper.cs` | 415 |
| `MarkJobFailed` | Method | `V3SClient/Services/DatabaseHelper.cs` | 420 |
| `MarkJobRejected` | Method | `V3SClient/Services/DatabaseHelper.cs` | 425 |
| `MarkJobIgnored` | Method | `V3SClient/Services/DatabaseHelper.cs` | 430 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `ApplyImageSyncConfig → LogDebug` | cross_community | 6 |
| `ApplyImageSyncConfig → SafeOutputPath` | cross_community | 6 |
| `Start → NormalizePath` | cross_community | 6 |
| `Start → UpdateJobStatus` | cross_community | 6 |
| `OnFileOrDirCreated → NormalizePath` | cross_community | 5 |
| `Initialize → NormalizePath` | cross_community | 5 |
| `ApplyImageSyncConfig → LogWarn` | cross_community | 5 |
| `ApplyImageSyncConfig → ImageSyncState` | cross_community | 5 |
| `Start → NormalizePath` | cross_community | 5 |
| `Start → ResolveRoleFromFileName` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ucs | 24 calls |
| Libs | 14 calls |
| Views | 4 calls |
| V3SClient | 1 calls |

## How to Explore

1. `context({name: "ProcessingTask"})` — see callers and callees
2. `query({search_query: "services"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
