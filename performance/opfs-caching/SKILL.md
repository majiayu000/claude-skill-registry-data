---
name: opfs-caching
description: OPFS (Origin Private File System) for offline audio caching. Use when implementing offline storage, audio file caching, or prefetching content. Triggers on mentions of OPFS, offline storage, audio caching, prefetch, or offline-first.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# OPFS for Offline Audio Caching

## Why OPFS?

OPFS (Origin Private File System) is **3-4x faster** than IndexedDB for binary files like audio.

| Feature | OPFS | IndexedDB |
|---------|------|-----------|
| Speed | 3-4x faster | Baseline |
| File operations | Native | Blob wrappers |
| Streaming | Supported | Not ideal |
| Browser support | All modern (2023+) | Universal |

## Browser Support

- Chrome 86+
- Edge 86+
- Firefox 111+
- Safari 15.2+
- **Requires HTTPS** (secure context)

## Basic Usage

### Get OPFS Root

```typescript
const root = await navigator.storage.getDirectory();
```

### Create Directory Structure

```typescript
async function setupCacheDirectories(): Promise<void> {
  const root = await navigator.storage.getDirectory();

  // Create subdirectories
  await root.getDirectoryHandle('tracks', { create: true });
  await root.getDirectoryHandle('messages', { create: true });
  await root.getDirectoryHandle('schedules', { create: true });
}
```

### Store Audio File

```typescript
async function cacheTrack(trackId: string, blob: Blob): Promise<void> {
  const root = await navigator.storage.getDirectory();
  const tracksDir = await root.getDirectoryHandle('tracks');
  const fileHandle = await tracksDir.getFileHandle(
    `${trackId}.mp3`,
    { create: true }
  );

  // Method 1: createWritable (async, main thread)
  const writable = await fileHandle.createWritable();
  await writable.write(blob);
  await writable.close();
}
```

### Read Audio File

```typescript
async function getCachedTrack(trackId: string): Promise<ArrayBuffer | null> {
  try {
    const root = await navigator.storage.getDirectory();
    const tracksDir = await root.getDirectoryHandle('tracks');
    const fileHandle = await tracksDir.getFileHandle(`${trackId}.mp3`);
    const file = await fileHandle.getFile();
    return await file.arrayBuffer();
  } catch {
    return null; // Not cached
  }
}
```

## Web Worker for Performance

For large files, use **sync operations in a Web Worker** (faster):

### Worker File (cache-worker.ts)

```typescript
// This runs in Web Worker context where createSyncAccessHandle is available

self.onmessage = async (event: MessageEvent) => {
  const { type, payload } = event.data;

  switch (type) {
    case 'WRITE_FILE': {
      const { directory, filename, data } = payload;

      const root = await navigator.storage.getDirectory();
      const dir = await root.getDirectoryHandle(directory);
      const fileHandle = await dir.getFileHandle(filename, { create: true });

      // Sync access is much faster for large files
      const accessHandle = await fileHandle.createSyncAccessHandle();

      const buffer = new Uint8Array(data);
      accessHandle.write(buffer, { at: 0 });
      accessHandle.flush();
      accessHandle.close();

      self.postMessage({ type: 'WRITE_COMPLETE', success: true });
      break;
    }

    case 'READ_FILE': {
      const { directory, filename } = payload;

      const root = await navigator.storage.getDirectory();
      const dir = await root.getDirectoryHandle(directory);
      const fileHandle = await dir.getFileHandle(filename);

      const accessHandle = await fileHandle.createSyncAccessHandle();
      const size = accessHandle.getSize();
      const buffer = new Uint8Array(size);
      accessHandle.read(buffer, { at: 0 });
      accessHandle.close();

      // Transfer ownership for performance
      self.postMessage(
        { type: 'READ_COMPLETE', data: buffer.buffer },
        [buffer.buffer]
      );
      break;
    }
  }
};
```

### Using the Worker

```typescript
class OPFSCache {
  private worker: Worker;

  constructor() {
    this.worker = new Worker(
      new URL('./cache-worker.ts', import.meta.url),
      { type: 'module' }
    );
  }

  async writeFile(directory: string, filename: string, data: ArrayBuffer): Promise<void> {
    return new Promise((resolve, reject) => {
      this.worker.onmessage = (event) => {
        if (event.data.type === 'WRITE_COMPLETE') {
          resolve();
        }
      };
      this.worker.onerror = reject;

      this.worker.postMessage(
        { type: 'WRITE_FILE', payload: { directory, filename, data } },
        [data] // Transfer ownership
      );
    });
  }
}
```

## Prefetch Manager

Cache content based on schedule:

```typescript
interface PrefetchConfig {
  lookAheadHours: number;       // How far ahead to cache (4)
  maxCacheSize: number;         // Max bytes (500MB)
  networkThreshold: 'wifi' | 'any';
}

class PrefetchManager {
  private cache: OPFSCache;
  private config: PrefetchConfig;

  async prefetchSchedule(schedule: ScheduleEntry[]): Promise<void> {
    const now = Date.now();
    const lookAhead = this.config.lookAheadHours * 60 * 60 * 1000;
    const cutoff = now + lookAhead;

    // Filter to upcoming tracks
    const upcoming = schedule
      .filter(entry => {
        const entryTime = entry.scheduledTime.getTime();
        return entryTime > now && entryTime < cutoff;
      })
      .sort((a, b) => a.scheduledTime.getTime() - b.scheduledTime.getTime());

    // Check storage quota
    const { usage, quota } = await navigator.storage.estimate();
    const available = (quota ?? 0) - (usage ?? 0);

    for (const entry of upcoming) {
      if (await this.cache.has(entry.trackId)) continue;

      // Check we have space
      if (entry.fileSize > available * 0.8) {
        await this.evictOldest(entry.fileSize);
      }

      await this.downloadAndCache(entry);
    }
  }

  private async evictOldest(neededBytes: number): Promise<void> {
    // Remove oldest cached tracks until we have space
    const cached = await this.cache.getAllMetadata();
    const sorted = cached.sort((a, b) => a.cachedAt - b.cachedAt);

    let freed = 0;
    for (const entry of sorted) {
      if (freed >= neededBytes) break;

      await this.cache.delete(entry.id);
      freed += entry.size;
    }
  }
}
```

## Storage Quota

Check available storage:

```typescript
async function checkStorageQuota(): Promise<{
  used: number;
  quota: number;
  percent: number;
}> {
  const estimate = await navigator.storage.estimate();
  const used = estimate.usage ?? 0;
  const quota = estimate.quota ?? 0;

  return {
    used,
    quota,
    percent: quota > 0 ? (used / quota) * 100 : 0
  };
}
```

## Cleanup

Remove old cached files:

```typescript
async function evictExpired(maxAge: number = 24 * 60 * 60 * 1000): Promise<void> {
  const root = await navigator.storage.getDirectory();
  const tracksDir = await root.getDirectoryHandle('tracks');
  const now = Date.now();

  for await (const [name, handle] of tracksDir.entries()) {
    if (handle.kind === 'file') {
      const file = await (handle as FileSystemFileHandle).getFile();
      if (now - file.lastModified > maxAge) {
        await tracksDir.removeEntry(name);
      }
    }
  }
}
```

## Best Practices

1. **Use Web Workers** for sync operations (faster for large files)
2. **Transfer ArrayBuffers** to avoid copying
3. **Check quota before writing**
4. **Evict old content** based on schedule
5. **Handle errors gracefully** (file not found, quota exceeded)
6. **Keep metadata index** in IndexedDB for fast lookups
