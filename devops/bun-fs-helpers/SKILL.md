---
name: bun-fs-helpers
description: Pure Bun-native filesystem utilities from @sidequest/core/fs. Use when you need command-injection-safe filesystem operations, prefer Bun over node:fs, or want token-efficient fs helpers. All functions use Bun.spawn, Bun.file(), or Bun.write() - no node:fs dependencies.
---

# Bun Filesystem Helpers

Pure Bun-native filesystem utilities from `@sidequest/core/fs` - zero node:fs dependencies, command-injection safe.

## When to Use

- **Writing new code** - Always prefer these over node:fs
- **Command injection concerns** - All shell commands use array args (safe)
- **Token efficiency** - Smaller imports, faster operations
- **Bun-first projects** - Leverages Bun's native APIs

## Available Functions

### File Existence

```typescript
import { pathExists, pathExistsSync } from "@sidequest/core/fs";

// Async
if (await pathExists("/path/to/file")) { }

// Sync
if (pathExistsSync("/path/to/file")) { }
```

**Implementation**: Uses `Bun.file().exists()` (async) or `test -e` command (sync)

### Reading Files

```typescript
import { readTextFile, readTextFileSync, readJsonFile, readJsonFileSync } from "@sidequest/core/fs";

// Async text
const content = await readTextFile("/path/to/file.txt");

// Sync text
const content = readTextFileSync("/path/to/file.txt");

// Async JSON
const data = await readJsonFile<MyType>("/path/to/data.json");

// Sync JSON
const data = readJsonFileSync<MyType>("/path/to/data.json");
```

**Implementation**: Uses `Bun.file().text()` (async) or `cat` command (sync)

### Writing Files

```typescript
import { writeTextFile, writeTextFileSync, writeJsonFile, writeJsonFileSync } from "@sidequest/core/fs";

// Async text
await writeTextFile("/path/to/file.txt", "content");

// Sync text
writeTextFileSync("/path/to/file.txt", "content");

// Async JSON
await writeJsonFile("/path/to/data.json", { foo: "bar" }, 2);

// Sync JSON
writeJsonFileSync("/path/to/data.json", { foo: "bar" }, 2);
```

**Implementation**: Uses `Bun.write()` (async) or `printf` via shell (sync)

### Directory Operations

```typescript
import { ensureDir, ensureDirSync, readDir, readDirAsync } from "@sidequest/core/fs";

// Create directory (recursive)
await ensureDir("/path/to/nested/dir");
ensureDirSync("/path/to/nested/dir");

// List directory contents
const files = readDir("/path/to/dir");  // Sync
const files = await readDirAsync("/path/to/dir");  // Async
```

**Implementation**: Uses `mkdir -p` command, `ls -1` command

### File Operations

```typescript
import { copyFile, moveFile, rename, unlink, unlinkSync } from "@sidequest/core/fs";

// Copy file
await copyFile("/source.txt", "/dest.txt");

// Move file (copy + delete)
await moveFile("/source.txt", "/dest.txt");

// Rename/move atomically
await rename("/old-path.txt", "/new-path.txt");

// Delete file
await unlink("/path/to/file.txt");
unlinkSync("/path/to/file.txt");
```

**Implementation**: Uses `Bun.write()` for copy, `mv` command for rename, `rm` command for delete

### File Stats

```typescript
import { stat } from "@sidequest/core/fs";

const stats = await stat("/path/to/file.txt");
console.log(stats.size);      // File size in bytes
console.log(stats.mtimeMs);   // Last modified timestamp
```

**Implementation**: Uses `Bun.file().size` and `Bun.file().lastModified`

**Use case**: TOCTOU protection - check file before AND after operations

### Hashing

```typescript
import { sha256, sha256File, fastHash } from "@sidequest/core/fs";

// Hash string
const hash = sha256("content");  // Hex string (64 chars)

// Hash file
const hash = await sha256File("/path/to/file.pdf");

// Fast non-cryptographic hash (cache keys)
const hash = fastHash("content");  // bigint or number
```

**Implementation**: Uses `Bun.CryptoHasher` (SHA256) or `Bun.hash` (xxHash64)

### Deep Equality

```typescript
import { deepEquals } from "@sidequest/core/fs";

const equal = deepEquals(obj1, obj2);           // Loose mode
const equal = deepEquals(obj1, obj2, true);     // Strict mode
```

**Implementation**: Uses `Bun.deepEquals()`

## Security Guarantees

✅ **Command injection safe** - All shell commands use array arguments:
```typescript
// Safe - array args prevent injection
Bun.spawnSync(["mkdir", "-p", userInput]);

// Never - string interpolation allows injection
Bun.spawnSync(`mkdir -p ${userInput}`);  // ❌ DON'T DO THIS
```

✅ **TOCTOU protection** - Use `stat()` before AND after file operations to detect tampering

## Migration from node:fs

```typescript
// Before (node:fs)
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";

existsSync("/path");
mkdirSync("/path", { recursive: true });
readFileSync("/path", "utf8");
writeFileSync("/path", "content", "utf8");

// After (@sidequest/core/fs)
import { pathExistsSync, ensureDirSync, readTextFileSync, writeTextFileSync } from "@sidequest/core/fs";

pathExistsSync("/path");
ensureDirSync("/path");
readTextFileSync("/path");
writeTextFileSync("/path", "content");
```

## Performance Characteristics

| Operation | Speed | Notes |
|-----------|-------|-------|
| `pathExists` | ~1ms | Bun.file().exists() |
| `pathExistsSync` | ~2ms | test -e command |
| `readTextFile` | ~5-50ms | Depends on file size |
| `writeTextFile` | ~5-20ms | Bun.write() is fast |
| `ensureDir` | ~10ms | mkdir -p command |
| `readDir` | ~5-15ms | ls -1 command |
| `sha256File` | ~50-500ms | Depends on file size |
| `fastHash` | <1ms | xxHash64 is very fast |

## Common Patterns

### Atomic File Updates

```typescript
import { pathExistsSync, writeTextFileSync, rename } from "@sidequest/core/fs";

// Write to temp file, then atomically rename
const tempPath = `${targetPath}.tmp`;
writeTextFileSync(tempPath, newContent);
await rename(tempPath, targetPath);  // POSIX guarantees atomicity
```

### Safe File Modification with TOCTOU Protection

```typescript
import { stat, readTextFileSync, writeTextFileSync } from "@sidequest/core/fs";

// Get pre-modification stats
const preStat = await stat(filePath);

// Read and modify
const content = readTextFileSync(filePath);
const modified = transform(content);

// Verify file unchanged before writing
const postStat = await stat(filePath);
if (postStat.mtimeMs !== preStat.mtimeMs) {
  throw new Error("File was modified during read (TOCTOU attack detected)");
}

writeTextFileSync(filePath, modified);
```

### Idempotent Processing with Content Hashing

```typescript
import { sha256File, pathExistsSync } from "@sidequest/core/fs";

const hash = await sha256File(sourceFile);
const processedMarker = `.processed/${hash}`;

if (pathExistsSync(processedMarker)) {
  console.log("Already processed - skipping");
  return;
}

// Process file...
writeTextFileSync(processedMarker, new Date().toISOString());
```

## Implementation Details

All functions are exported from `core/src/fs/index.ts` and use:
- `Bun.file()` - File existence, reading, size, timestamps
- `Bun.write()` - Writing files
- `Bun.spawn()` / `Bun.spawnSync()` - Shell commands with array args
- `Bun.CryptoHasher` - SHA256 hashing
- `Bun.hash` - Fast non-cryptographic hashing (xxHash64)
- `Bun.deepEquals()` - Deep equality checks
- `Bun.Glob` - Recursive file scanning (used elsewhere, not exported from fs)

**Zero node:fs dependencies in production code.**

## References

- Core package source: `core/src/fs/index.ts`
- Test coverage: 423 tests passing
- Used by: para-obsidian inbox processing, registry, PDF processor
