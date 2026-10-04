---
name: models
description: "Skill for the Models area of iVista-Client-Application. 39 symbols across 10 files."
---

# Models

39 symbols | 10 files | Cohesion: 79%

## When to Use

- Working with code in `V3SClient/`
- Understanding how FilesPlayer, PlaybackHLS, RtspPlayer work
- Modifying models-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/models/RtspPlayer.cs` | GetPipelineDescription, SetState, ExtractResourceToTempFile, CreatePipeline, Monitor (+19) |
| `V3SClient/models/PlaybackHLS.cs` | ReConnect, InitPipeline, PlaybackHLS |
| `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | Dispose, InitPipeline |
| `V3SClient/models/FilesPlayer.cs` | ReConnect, FilesPlayer |
| `V3SClient/models/MetaAIResult.cs` | MetaAIResult, OnPropertyChanged |
| `V3SClient/models/PlateFolderItem.cs` | PlateFolderItem, OnPropertyChanged |
| `V3SClient/UI/Views/VLiveStream.xaml.cs` | InitialPipeline |
| `V3SClient/ucs/ViewCamera.xaml.cs` | InitPipeline |
| `V3SClient/models/NamingSegment.cs` | NamingFieldDefinition |
| `V3SClient/viewModels/VMDocumentConfig.cs` | InitializeAvailableFields |

## Entry Points

Start here when exploring this area:

- **`FilesPlayer`** (Class) — `V3SClient/models/FilesPlayer.cs:16`
- **`PlaybackHLS`** (Class) — `V3SClient/models/PlaybackHLS.cs:12`
- **`RtspPlayer`** (Class) — `V3SClient/models/RtspPlayer.cs:38`
- **`MetaAIResult`** (Class) — `V3SClient/models/MetaAIResult.cs:9`
- **`NamingFieldDefinition`** (Class) — `V3SClient/models/NamingSegment.cs:79`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `FilesPlayer` | Class | `V3SClient/models/FilesPlayer.cs` | 16 |
| `PlaybackHLS` | Class | `V3SClient/models/PlaybackHLS.cs` | 12 |
| `RtspPlayer` | Class | `V3SClient/models/RtspPlayer.cs` | 38 |
| `MetaAIResult` | Class | `V3SClient/models/MetaAIResult.cs` | 9 |
| `NamingFieldDefinition` | Class | `V3SClient/models/NamingSegment.cs` | 79 |
| `PlateFolderItem` | Class | `V3SClient/models/PlateFolderItem.cs` | 9 |
| `InitPipeline` | Method | `V3SClient/models/RtspPlayer.cs` | 611 |
| `Dispose` | Method | `V3SClient/models/RtspPlayer.cs` | 788 |
| `Dispose` | Method | `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | 735 |
| `SetRate` | Method | `V3SClient/models/RtspPlayer.cs` | 973 |
| `SpeedDown` | Method | `V3SClient/models/RtspPlayer.cs` | 985 |
| `SpeedUp` | Method | `V3SClient/models/RtspPlayer.cs` | 994 |
| `InitPipeline` | Method | `V3SClient/models/PlaybackHLS.cs` | 42 |
| `QueryPositionPlaying` | Method | `V3SClient/models/RtspPlayer.cs` | 378 |
| `InitPipeline` | Method | `V3SClient/ucs/ViewCamera.xaml.cs` | 232 |
| `InitPipeline` | Method | `V3SClient/ucs/ViewCameraPlayback.xaml.cs` | 176 |
| `ParseSeiNalH265` | Method | `V3SClient/models/RtspPlayer.cs` | 100 |
| `Send2Draw` | Method | `V3SClient/models/RtspPlayer.cs` | 355 |
| `GetPipelineDescription` | Method | `V3SClient/models/RtspPlayer.cs` | 340 |
| `SetState` | Method | `V3SClient/models/RtspPlayer.cs` | 369 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `CoreWebView2_WebMessageReceived → LogException` | cross_community | 8 |
| `CoreWebView2_WebMessageReceived → SetState` | cross_community | 8 |
| `PlaybackHLS → LogException` | cross_community | 7 |
| `PlaybackHLS → SetState` | cross_community | 7 |
| `CoreWebView2_WebMessageReceived → ReleaseDraw` | cross_community | 7 |
| `PlaybackHLS → ReleaseDraw` | cross_community | 6 |
| `PlaybackHLS → PlayerInfo` | cross_community | 6 |
| `InitPipeline → LogException` | cross_community | 6 |
| `InitPipeline → SetState` | cross_community | 6 |
| `InitPipeline → LogException` | cross_community | 6 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Libs | 3 calls |
| V3SClient | 3 calls |
| Views | 2 calls |
| Ucs | 1 calls |

## How to Explore

1. `context({name: "FilesPlayer"})` — see callers and callees
2. `query({search_query: "models"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
