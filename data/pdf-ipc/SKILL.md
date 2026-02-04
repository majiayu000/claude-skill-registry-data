---
name: pdf-ipc
description: This skill should be used when implementing IPC (Inter-Process Communication) channels for PDF operations in Electron. Triggers on requests to create PDF merge, edit, or convert functionality, implement preload APIs, or set up Main-Renderer communication for file operations.
---

# PDF IPC Communication

## Overview

This skill provides guidance for implementing IPC communication between Electron's Main and Renderer processes for PDF operations. It covers channel naming conventions, type definitions, service patterns, and worker integration.

## IPC Channel Naming Pattern

```
scope.action:detail
```

| Part | Description | Examples |
|------|-------------|----------|
| scope | Domain area | `pdf`, `file`, `dialog`, `app` |
| action | Operation type | `merge`, `edit`, `convert`, `meta` |
| detail | Specific event | `start`, `progress`, `complete`, `apply` |

### Channel Examples

| Channel | Direction | Description |
|---------|-----------|-------------|
| `pdf.merge:start` | R → M | Start merge operation |
| `pdf.merge:progress` | M → R | Real-time progress event |
| `pdf.merge:complete` | M → R | Completion notification |
| `pdf.edit:apply` | R → M | Apply edit operations |
| `file.convert.tiff` | R → M | TIFF to PDF conversion |
| `file.meta.get-pdf-info` | R → M | Get PDF metadata |
| `dialog.show-open` | R → M | Open file dialog |
| `dialog.show-save` | R → M | Save file dialog |

## Type Definitions

All IPC types should be defined in `src/main/types/ipc-schema.ts` and shared across Main, Preload, and Renderer.

### Core Types

```typescript
// src/main/types/ipc-schema.ts

export interface MergeRequest {
  files: MergeFileItem[];
  outputPath?: string;
}

export interface MergeFileItem {
  path: string;
  pages?: number[];  // Specific pages to merge
}

export interface MergeResult {
  outputPath: string;
  totalPages: number;
}

export interface MergeProgress {
  current: number;
  total: number;
  percentage: number;
}

export interface EditPageRequest {
  filePath: string;
  operations: PageOperation[];
}

export interface PageOperation {
  type: 'delete' | 'reorder';
  pageIndices: number[];
  newOrder?: number[];  // For reorder operation
}

export interface ConvertTiffRequest {
  tiffPath: string;
  outputDir?: string;
}

export interface ConvertResult {
  outputPdfPath: string;
  pageCount: number;
}
```

## Implementation Patterns

### Preload Script (ContextBridge)

```typescript
// src/preload/index.ts
import { contextBridge, ipcRenderer } from 'electron';
import type {
  MergeRequest,
  MergeProgress,
  MergeResult,
  EditPageRequest,
  ConvertTiffRequest,
  ConvertResult
} from '../main/types/ipc-schema';

contextBridge.exposeInMainWorld('api', {
  // Commands (Renderer → Main)
  mergePdf: (request: MergeRequest) =>
    ipcRenderer.invoke('pdf.merge:start', request),

  editPdf: (request: EditPageRequest) =>
    ipcRenderer.invoke('pdf.edit:apply', request),

  convertTiff: (request: ConvertTiffRequest) =>
    ipcRenderer.invoke('file.convert.tiff', request),

  getPdfInfo: (filePath: string) =>
    ipcRenderer.invoke('file.meta.get-pdf-info', filePath),

  // Dialogs
  showOpenDialog: (options?: { filters?: Electron.FileFilter[] }) =>
    ipcRenderer.invoke('dialog.show-open', options),

  showSaveDialog: (options?: { defaultPath?: string }) =>
    ipcRenderer.invoke('dialog.show-save', options),

  // Events (Main → Renderer)
  onMergeProgress: (callback: (progress: MergeProgress) => void) => {
    const handler = (_: Electron.IpcRendererEvent, data: MergeProgress) => callback(data);
    ipcRenderer.on('pdf.merge:progress', handler);
    return () => ipcRenderer.removeListener('pdf.merge:progress', handler);
  },

  onMergeComplete: (callback: (result: MergeResult) => void) => {
    const handler = (_: Electron.IpcRendererEvent, data: MergeResult) => callback(data);
    ipcRenderer.on('pdf.merge:complete', handler);
    return () => ipcRenderer.removeListener('pdf.merge:complete', handler);
  },
});
```

### IPC Handler (Main Process)

```typescript
// src/main/app/ipc-handler.ts
import { ipcMain, dialog, BrowserWindow } from 'electron';
import { PdfMergeService } from '../services/pdf-merge-service';
import { PdfEditService } from '../services/pdf-edit-service';
import { FileConverterService } from '../services/file-converter-service';

export function setupIpcHandlers(mainWindow: BrowserWindow) {
  const mergeService = new PdfMergeService();
  const editService = new PdfEditService();
  const converterService = new FileConverterService();

  // PDF Merge
  ipcMain.handle('pdf.merge:start', async (_, request) => {
    return mergeService.merge(request, (progress) => {
      mainWindow.webContents.send('pdf.merge:progress', progress);
    });
  });

  // PDF Edit
  ipcMain.handle('pdf.edit:apply', async (_, request) => {
    return editService.applyOperations(request);
  });

  // File Convert
  ipcMain.handle('file.convert.tiff', async (_, request) => {
    return converterService.convertTiff(request);
  });

  // Dialogs
  ipcMain.handle('dialog.show-open', async (_, options) => {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openFile', 'multiSelections'],
      filters: options?.filters ?? [{ name: 'PDF Files', extensions: ['pdf'] }],
    });
    return result.filePaths;
  });

  ipcMain.handle('dialog.show-save', async (_, options) => {
    const result = await dialog.showSaveDialog(mainWindow, {
      defaultPath: options?.defaultPath,
    });
    return result.filePath;
  });
}
```

### Renderer IPC Client

```typescript
// src/renderer/shared/lib/ipc-client.ts
import type {
  MergeRequest,
  MergeProgress,
  MergeResult,
  EditPageRequest,
  ConvertTiffRequest,
  ConvertResult
} from '@/main/types/ipc-schema';

export const ipcClient = {
  merge: {
    start: (request: MergeRequest) => window.api.mergePdf(request),
    onProgress: (cb: (p: MergeProgress) => void) => window.api.onMergeProgress(cb),
    onComplete: (cb: (r: MergeResult) => void) => window.api.onMergeComplete(cb),
  },
  edit: {
    apply: (request: EditPageRequest) => window.api.editPdf(request),
  },
  convert: {
    tiff: (request: ConvertTiffRequest) => window.api.convertTiff(request),
  },
  dialog: {
    open: window.api.showOpenDialog,
    save: window.api.showSaveDialog,
  },
};
```

## Service Pattern

### Service Class Structure

```typescript
// src/main/services/pdf-merge-service.ts
import type { MergeRequest, MergeResult, MergeProgress } from '../types/ipc-schema';

export class PdfMergeService {
  async merge(
    request: MergeRequest,
    onProgress: (progress: MergeProgress) => void
  ): Promise<MergeResult> {
    const { files, outputPath } = request;
    const total = files.length;

    for (let i = 0; i < files.length; i++) {
      // Process file...
      onProgress({
        current: i + 1,
        total,
        percentage: Math.round(((i + 1) / total) * 100),
      });
    }

    return {
      outputPath: outputPath ?? '/path/to/output.pdf',
      totalPages: 0, // Calculate actual pages
    };
  }
}
```

### Worker Integration

For CPU-intensive operations, delegate to workers:

```typescript
// src/main/workers/merge-worker.ts
import { parentPort, workerData } from 'worker_threads';
import { PDFDocument } from 'pdf-lib';

async function processMerge() {
  const { files } = workerData;
  // PDF merge logic with pdf-lib
  parentPort?.postMessage({ type: 'complete', result: {} });
}

processMerge();
```

## Resources

### references/
- `ipc-channels.md` - Complete IPC channel reference
- `type-definitions.md` - All IPC type definitions

To delete unused example files in `scripts/` and `assets/` directories as this skill focuses on IPC patterns.
