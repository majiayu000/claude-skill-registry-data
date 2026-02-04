---
name: electron-fsd
description: This skill should be used when developing Electron applications with Feature-Sliced Design (FSD) architecture and React 19. Triggers on requests to create components, features, entities, widgets, or pages following FSD layer structure. Also applies when setting up Electron main/preload/renderer process code organization.
---

# Electron FSD Development (React 19)

## Overview

This skill provides guidance for developing Electron applications using Feature-Sliced Design (FSD) architecture with React 19. It covers the three-process model (Main, Preload, Renderer) and FSD layer organization for the Renderer process.

## Architecture Patterns

### Electron Process Model

```
┌─────────────────────────────────────────────────────────────┐
│  Main Process (Node.js)                                     │
│  ├─ app/main.ts         - App lifecycle, BrowserWindow      │
│  ├─ app/ipc-handler.ts  - IPC routing to services           │
│  ├─ services/           - Business logic (PdfMergeService)  │
│  └─ workers/            - CPU-intensive tasks               │
├─────────────────────────────────────────────────────────────┤
│  Preload (Isolated)                                         │
│  └─ index.ts            - ContextBridge (window.api)        │
├─────────────────────────────────────────────────────────────┤
│  Renderer (React + FSD)                                     │
│  ├─ shared/             - Common utilities, UI, types       │
│  ├─ entities/           - READ (data display)               │
│  ├─ features/           - CUD (user actions)                │
│  ├─ widgets/            - Feature composition               │
│  └─ pages/              - Route entry points                │
└─────────────────────────────────────────────────────────────┘
```

### FSD Layer Responsibilities

| Layer | Responsibility | IPC Direction | Example |
|-------|----------------|---------------|---------|
| `entities` | Data display only | READ | `document-card.tsx`, `page-thumbnail.tsx` |
| `features` | User actions | CUD | `use-merge-command.ts`, `merge-toolbar.tsx` |
| `widgets` | Feature composition | - | `merge-workspace.tsx` |
| `shared` | Cross-cutting concerns | - | `ipc-client.ts`, types, UI components |

## Component Creation Workflow

### Creating an Entity (READ-only)

To create a new entity for displaying data:

1. Create entity folder: `src/renderer/entities/{entity-name}/`
2. Structure:
```
entities/pdf-document/
├─ ui/
│  └─ document-card.tsx     # Display component
└─ model/
   └─ use-pdf-metadata.ts   # Data fetching hook (READ)
```

3. Entity components must:
   - Only display data (no mutations)
   - Use hooks for data fetching
   - Accept data via props or context

### Creating a Feature (CUD operations)

To create a new feature for user actions:

1. Create feature folder: `src/renderer/features/{feature-name}/`
2. Structure:
```
features/pdf-merge/
├─ ui/
│  ├─ merge-toolbar.tsx      # Action UI
│  └─ merge-file-grid.tsx    # Interactive grid with DnD
└─ model/
   └─ use-merge-command.ts   # IPC command hook
```

3. Feature components must:
   - Handle user interactions
   - Call IPC commands for mutations
   - Compose entities for display

### Creating a Widget (Composition)

To compose features and entities into workspace:

1. Create widget folder: `src/renderer/widgets/{widget-name}/`
2. Structure:
```
widgets/merge-workspace/
└─ merge-workspace.tsx
```

3. Widget implementation:
```typescript
// merge-workspace.tsx
export function MergeWorkspace() {
  const { files, addFiles, removeFile } = useMergeContext();

  return (
    <>
      <MergeToolbar onAddFiles={addFiles} />
      <MergeFileGrid files={files} onRemove={removeFile} />
    </>
  );
}
```

## File Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Folders & files | kebab-case | `pdf-merge-service.ts` |
| React components | PascalCase | `MergeWorkspace` |
| Hooks | camelCase with `use` prefix | `useMergeCommand` |
| Types/interfaces | PascalCase | `MergeRequest` |
| Services | PascalCase + Service | `PdfMergeService` |
| Workers | kebab-case + worker | `merge-worker.ts` |

## React 19 Component Patterns

### No forwardRef (React 19)

```typescript
// ❌ React 18 (forwardRef)
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

// ✅ React 19 (ref as regular prop)
interface InputProps {
  ref?: React.Ref<HTMLInputElement>;
  placeholder?: string;
}
function Input({ ref, ...props }: InputProps) {
  return <input ref={ref} {...props} />;
}
```

### Context as Provider (React 19)

```typescript
// ❌ React 18
<ThemeContext.Provider value={theme}>
  {children}
</ThemeContext.Provider>

// ✅ React 19
<ThemeContext value={theme}>
  {children}
</ThemeContext>
```

### use() Hook for Promise/Context

```typescript
// ✅ React 19: use() for Promise (requires Suspense)
import { use, Suspense } from 'react';

function FileList({ filesPromise }: { filesPromise: Promise<PdfFile[]> }) {
  const files = use(filesPromise);
  return files.map(f => <FileCard key={f.id} file={f} />);
}

// Usage with Suspense
<Suspense fallback={<Loading />}>
  <FileList filesPromise={fetchFiles()} />
</Suspense>

// ✅ React 19: use() for Context (conditional allowed)
function ConditionalTheme({ show }: { show: boolean }) {
  if (show) {
    const theme = use(ThemeContext);
    return <div className={theme}>Themed</div>;
  }
  return null;
}
```

### useActionState for Forms

```typescript
// ✅ React 19: Form action with state
import { useActionState } from 'react';

function MergeForm() {
  const [state, submitAction, isPending] = useActionState(
    async (prev, formData) => {
      const files = formData.getAll('files');
      const result = await window.api.merge(files);
      return result;
    },
    null
  );

  return (
    <form action={submitAction}>
      <input type="file" name="files" multiple disabled={isPending} />
      <button disabled={isPending}>
        {isPending ? 'Merging...' : 'Merge PDFs'}
      </button>
    </form>
  );
}
```

### useOptimistic for Optimistic UI

```typescript
// ✅ React 19: Optimistic updates
import { useOptimistic } from 'react';

function FileList({ files }: { files: PdfFile[] }) {
  const [optimisticFiles, addOptimistic] = useOptimistic(
    files,
    (state, newFile: PdfFile) => [...state, { ...newFile, pending: true }]
  );

  async function handleAdd(file: File) {
    const tempFile = { id: 'temp', name: file.name, pending: true };
    addOptimistic(tempFile);
    await window.api.addFile(file);
  }

  return (
    <div>
      {optimisticFiles.map(f => (
        <FileCard key={f.id} file={f} opacity={f.pending ? 0.5 : 1} />
      ))}
    </div>
  );
}
```

### ref Callback Cleanup

```typescript
// ✅ React 19: ref cleanup function
function AutoFocusInput() {
  return (
    <input
      ref={(el) => {
        if (el) el.focus();
        return () => {
          // cleanup when element removed
          console.log('Input unmounted');
        };
      }}
    />
  );
}
```

## Type Definition Rules

### No Inline Object Types

```typescript
// ❌ Avoid
function process(data: { id: string; name: string }) {}

// ✅ Preferred
interface ProcessData { id: string; name: string }
function process(data: ProcessData) {}
```

### Constants with ValueOf Pattern

```typescript
// Define constants
export const MERGE_STATUS = {
  IDLE: 'idle',
  PENDING: 'pending',
  COMPLETE: 'complete',
} as const;

// Create union type
type ValueOf<T> = T[keyof T];
type MergeStatus = ValueOf<typeof MERGE_STATUS>;

// Usage
const status: MergeStatus = MERGE_STATUS.PENDING;
```

## Resources

### references/
- `fsd-layers.md` - Detailed FSD layer documentation
- `electron-patterns.md` - Electron-specific patterns

To delete unused example files in `scripts/` and `assets/` directories as this skill focuses on architectural guidance.
