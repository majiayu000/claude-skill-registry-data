---
name: boardkit-file-format
description: |
  .boardkit file format: ZIP structure, serialization, versioning, migrations.
  Use when working on import/export, persistence, or file format changes.
allowed-tools: Read, Grep, Glob
---

# Boardkit File Format

## Structure

`.boardkit` = ZIP archive containing:

```
my-board.boardkit (ZIP)
├── package.json     → Metadata
└── board.json       → Document content
```

### package.json
```json
{
  "name": "my-board",
  "version": "1.0.0",
  "boardkit": {
    "formatVersion": 2
  }
}
```

### board.json
```json
{
  "version": 2,
  "meta": {
    "title": "My Board",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-02T00:00:00Z"
  },
  "board": {
    "viewport": { "x": 0, "y": 0, "zoom": 1 },
    "widgets": [...],
    "elements": [...],
    "background": { "type": "dots", "color": "#f5f5f5" }
  },
  "modules": {},
  "dataSharing": {
    "permissions": [],
    "links": []
  }
}
```

## Constraints

| Constraint | Value |
|------------|-------|
| Max file size | 50 MB |
| Compression | DEFLATE level 6 |
| Extension | `.boardkit` |
| JSON encoding | UTF-8 |

## Document Versions

| Version | Changes |
|---------|---------|
| v0 | Initial: widgets only |
| v1 | Added: `elements[]`, `background` |
| v2 | Added: `dataSharing` section |

## Migration Functions

```typescript
// packages/core/src/migrations/index.ts
function migrateV0ToV1(doc: V0Document): V1Document {
  return {
    ...doc,
    version: 1,
    board: {
      ...doc.board,
      elements: [],
      background: { type: 'dots', color: '#f5f5f5' }
    }
  }
}
```

## Serialization Rules

1. **Deterministic** - Same input = same output
   - Sort object keys alphabetically
   - No random IDs in output

2. **Atomic writes** (Desktop)
   - Write to temp file first
   - Rename to final path

3. **Transactions** (Web/IndexedDB)
   - Use IDB transactions
   - Rollback on error

## Storage Implementations

### Web (IndexedDB)
```typescript
// packages/platform/src/storage/indexeddb.ts
Database: 'boardkit'
Stores: 'documents', 'history'
Autosave: 500ms debounce
History cap: 100 entries
```

### Desktop (Tauri FS)
```typescript
// apps/desktop/src/composables/usePersistence.ts
Autosave: 1000ms debounce
Atomic writes via temp file
```

## Import Validation

```typescript
// Required checks on import
1. File size < 50MB
2. Valid ZIP structure
3. package.json exists and valid
4. board.json exists and valid JSON
5. Version supported (migrate if needed)
6. Schema validation
```

## Key Files

| Purpose | Path |
|---------|------|
| Document types | `packages/core/src/types/document.ts` |
| Migrations | `packages/core/src/migrations/index.ts` |
| Web import/export | `apps/web/src/utils/boardkitFile.ts` |
| Desktop import/export | `apps/desktop/src/utils/boardkitFile.ts` |
| IndexedDB storage | `packages/platform/src/storage/indexeddb.ts` |
| Migration tests | `packages/core/__tests__/migrations.test.ts` |
