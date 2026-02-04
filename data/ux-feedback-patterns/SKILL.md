---
name: ux-feedback-patterns
description: Loading states, progress indicators, status colors, toasts, and DebugScope instrumentation for TMNL
triggers:
  - loading
  - progress
  - toast
  - notification
  - status
  - feedback
  - debug
---

# UX Feedback Patterns

TMNL provides rich feedback mechanisms for asynchronous operations, state changes, and developer instrumentation. This skill documents patterns for loading states, status indicators, toasts, and debug instrumentation.

## Overview

Feedback in TMNL follows these principles:
- **Immediate acknowledgment** - User actions trigger instant visual response
- **Progressive disclosure** - Show detail on demand, not by default
- **Semantic color coding** - Consistent meaning across the system
- **Debug-friendly** - All components support optional instrumentation via DebugScope

## Canonical Sources

### Primary Files
- `/src/lib/overlays/visual/hooks/useToast.ts` - Toast notification system
- `/src/lib/overlays/visual/renderers/ToastRenderer.tsx` - Toast UI implementation
- `/src/lib/debug/DebugScope.tsx` - Component instrumentation
- `/src/lib/overlays/schemas/visual.ts` - Toast/overlay config schemas
- `/src/lib/overlays/visual/constants.ts` - Animation timing constants

### Key Type Definitions
- `/src/lib/overlays/visual/hooks/useToast.ts` - `ToastVariant`, `ToastPosition`, `ToastOpenOptions`
- `/src/lib/debug/DebugScope.tsx` - `DebugScopeConfig`, `DebugScopeContextValue`
- `/src/lib/overlays/schemas/visual.ts` - `ToastConfig`, `OverlayAnimationState`

## Patterns

### 1. Toast Notifications

**Pattern**: Non-blocking status messages with variant-based styling and auto-dismiss.

**Canonical Implementation**: `/src/lib/overlays/visual/hooks/useToast.ts`

```typescript
export type ToastVariant = "info" | "success" | "warning" | "error"
export type ToastPosition =
  | "top-left" | "top-center" | "top-right"
  | "bottom-left" | "bottom-center" | "bottom-right"

export interface ToastOpenOptions {
  id?: string
  variant?: ToastVariant          // Defaults to "info"
  position?: ToastPosition        // Defaults to "bottom-right"
  duration?: number               // Auto-dismiss ms (0 = manual only)
  dismissible?: boolean           // Show close button
  zIndexOffset?: number
}
```

**Variant Styling** (from `/src/lib/overlays/visual/renderers/ToastRenderer.tsx`):
```typescript
const VARIANT_STYLES: Record<string, React.CSSProperties> = {
  info: { borderLeft: "4px solid var(--tmnl-info, #3b82f6)" },      // Blue
  success: { borderLeft: "4px solid var(--tmnl-success, #22c55e)" }, // Green
  warning: { borderLeft: "4px solid var(--tmnl-warning, #f59e0b)" }, // Amber
  error: { borderLeft: "4px solid var(--tmnl-error, #ef4444)" },    // Red
}
```

**Usage Example**:
```tsx
import { useToast } from '@/lib/overlays'

function MyComponent() {
  const toast = useToast()

  const handleSave = async () => {
    try {
      await saveData()
      toast.success("Changes saved successfully")
    } catch (error) {
      toast.error("Failed to save changes", {
        duration: 0, // Errors don't auto-dismiss
        position: "top-center",
      })
    }
  }

  const handleInfo = () => {
    toast.info("Processing...", {
      duration: 3000,
      dismissible: false, // No close button
    })
  }
}
```

**Auto-Dismiss Behavior**:
```typescript
// From useToast.ts
const open = (options: ToastOpenOptions, content: ReactNode) => {
  const config: ToastConfig = {
    duration: options.duration ?? 5000, // Default 5s
    // ...
  }

  const id = ctx.open("toast", { config, content })

  // Auto-dismiss after duration + animation time
  if (config.duration > 0) {
    const totalDuration = config.duration + getAnimationDuration("toast")
    setTimeout(() => ctx.close(id), totalDuration)
  }

  return id
}

// Errors don't auto-dismiss
const error = (message: ReactNode, options?) =>
  open({ ...options, variant: "error", duration: 0 }, message)
```

**Animation Timing** (from `/src/lib/overlays/visual/constants.ts`):
```typescript
export const getAnimationDuration = (type: VisualOverlayType): number => {
  switch (type) {
    case "toast": return 200       // Fast slide/fade
    case "drawer": return 300      // Medium slide
    case "modal": return 250       // Medium fade
    // ...
  }
}

export const getAnimationEasing = (type: VisualOverlayType): string => {
  switch (type) {
    case "toast": return "ease-out"
    case "drawer": return "ease-in-out"
    // ...
  }
}
```

### 2. Status Color System

**Pattern**: Semantic color tokens with consistent meaning across components.

**Color Token Definitions**:
```typescript
// Design token pattern (from various *-theme.ts files)
const TMNL_STATUS_COLORS = {
  // Information states
  info: "#3b82f6",      // Blue - neutral information
  success: "#22c55e",   // Green - successful completion
  warning: "#f59e0b",   // Amber - caution, non-critical
  error: "#ef4444",     // Red - critical error, failure

  // Extended states
  processing: "#8b5cf6", // Purple - in-progress operations
  pending: "#6b7280",    // Gray - awaiting action
  neutral: "#9ca3af",    // Light gray - default/inactive
}
```

**CSS Variable Pattern**:
```tsx
// Use CSS variables with fallbacks
<div
  style={{
    borderLeft: "4px solid var(--tmnl-success, #22c55e)"
  }}
/>

// Or via className (if theme provider sets variables)
<span className="text-[var(--tmnl-error,#ef4444)]">
  Error message
</span>
```

**When to Use Each Color**:
| Color | Use Case | Examples |
|-------|----------|----------|
| `info` | Neutral information, tips | "Settings saved to localStorage" |
| `success` | Successful operations | "File uploaded", "Test passed" |
| `warning` | Caution, non-blocking | "Unsaved changes", "Approaching limit" |
| `error` | Failures, critical issues | "Network error", "Validation failed" |
| `processing` | In-progress operations | "Uploading...", "Compiling..." |
| `pending` | Awaiting user action | "Awaiting confirmation" |

### 3. Loading States

**Pattern**: Differentiate between blocking and non-blocking loading with appropriate indicators.

**Non-Blocking Loading** (show inline, allow interaction):
```tsx
function SearchBar() {
  const [isSearching, setIsSearching] = useState(false)
  const [results, setResults] = useState([])

  const handleSearch = async (query: string) => {
    setIsSearching(true)
    try {
      const data = await search(query)
      setResults(data)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div>
      <input type="text" onChange={(e) => handleSearch(e.target.value)} />
      {isSearching && (
        <span className="text-[var(--tmnl-processing,#8b5cf6)]">
          Searching...
        </span>
      )}
      <ResultsList results={results} />
    </div>
  )
}
```

**Blocking Loading** (prevent interaction):
```tsx
function DataLoader() {
  const [isLoading, setIsLoading] = useState(true)
  const [data, setData] = useState(null)

  useEffect(() => {
    fetchData().then((d) => {
      setData(d)
      setIsLoading(false)
    })
  }, [])

  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center min-h-screen"
        role="status"
        aria-live="polite"
      >
        <div className="text-[var(--tmnl-processing,#8b5cf6)]">
          Loading...
        </div>
      </div>
    )
  }

  return <DataView data={data} />
}
```

**Progress Indicators**:
```tsx
// Determinate progress (known total)
<div className="relative h-1 bg-neutral-800 rounded">
  <div
    className="absolute h-full bg-[var(--tmnl-info,#3b82f6)] rounded transition-all"
    style={{ width: `${(loaded / total) * 100}%` }}
    role="progressbar"
    aria-valuenow={loaded}
    aria-valuemin={0}
    aria-valuemax={total}
  />
</div>

// Indeterminate progress (unknown total)
<div className="animate-pulse text-[var(--tmnl-processing,#8b5cf6)]">
  Processing...
</div>
```

### 4. DebugScope Instrumentation

**Pattern**: Opt-in component instrumentation with lifecycle logging and dependency tracking.

**Canonical Implementation**: `/src/lib/debug/DebugScope.tsx`

```typescript
export interface DebugScopeConfig {
  name: string               // Component/scope name for log prefixing
  debug?: boolean            // Enable debug mode
  logLifecycle?: boolean     // Log mount/unmount events
  logDeps?: boolean          // Log dependency changes
  metadata?: Record<string, unknown> // Custom metadata
}

export interface DebugScopeContextValue {
  enabled: boolean
  name: string
  log: (message: string, data?: Record<string, unknown>) => void
  error: (message: string, data?: Record<string, unknown>) => void
  warn: (message: string, data?: Record<string, unknown>) => void
  child: (name: string) => DebugScopeContextValue
}
```

**Three Usage Patterns**:

**1. Content Pattern** (render-nothing instrumentation):
```tsx
function Screensaver({ debug, isActive, timeRemaining }) {
  return (
    <>
      <DebugScope
        debug={debug}
        name="Screensaver"
        watch={{ isActive, timeRemaining }}
      />
      {isActive && <AsciiScene />}
    </>
  )
}
```

**2. Hook Pattern** (imperative logging):
```tsx
function DataGrid({ debug, data }) {
  const scope = useDebugScope({
    debug,
    name: "DataGrid",
    deps: [data],
    depLabels: ["data"],
  })

  const handleCellClick = (cell) => {
    scope.log("Cell clicked", { cell })
  }

  return <Grid onCellClick={handleCellClick} />
}
```

**3. Provider Pattern** (scope subtree):
```tsx
<DebugScopeProvider debug={true} name="OverlaySystem">
  <DrawerRenderer />
  <ModalRenderer />
  <ToastRenderer />
</DebugScopeProvider>
```

**Lifecycle Logging Output**:
```
[Screensaver] MOUNT { isActive: false, timeRemaining: 60000 }
[Screensaver] WATCH CHANGED { isActive: { from: false, to: true } }
[Screensaver] UNMOUNT { duration: "3245.67ms" }
```

**Dependency Change Tracking**:
```typescript
// From DebugScope.tsx
const diffDeps = (
  prev: unknown[] | undefined,
  next: unknown[],
  labels?: string[]
): Array<{ index: number; label: string; from: unknown; to: unknown }> => {
  if (!prev) return []

  const changes = []
  for (let i = 0; i < Math.max(prev.length, next.length); i++) {
    if (!Object.is(prev[i], next[i])) {
      changes.push({
        index: i,
        label: labels?.[i] ?? `dep[${i}]`,
        from: prev[i],
        to: next[i],
      })
    }
  }
  return changes
}
```

### 5. Animation State Feedback

**Pattern**: Visual feedback for overlay entrance/exit animations.

**Animation States** (from `/src/lib/overlays/schemas/visual.ts`):
```typescript
export const OverlayAnimationState = Schema.Literal(
  "entering",   // Animation in-progress (entering viewport)
  "visible",    // Fully visible, interactive
  "exiting",    // Animation in-progress (leaving viewport)
  "exited",     // Fully removed from DOM
)
```

**Transition Handler Pattern** (from `ToastRenderer.tsx`):
```tsx
useEffect(() => {
  if (!overlay) return

  if (overlay.animationState === "entering") {
    const timer = setTimeout(() => {
      ctx.setAnimationState(id, "visible")
    }, getAnimationDuration("toast"))
    return () => clearTimeout(timer)
  }

  if (overlay.animationState === "exiting") {
    const timer = setTimeout(() => {
      ctx.setAnimationState(id, "exited")
    }, getAnimationDuration("toast"))
    return () => clearTimeout(timer)
  }
}, [overlay?.animationState])
```

**CSS Transition Pattern**:
```typescript
const toastContainerStyles = (visible: boolean): React.CSSProperties => ({
  opacity: visible ? 1 : 0,
  transform: visible ? "translateY(0)" : "translateY(-20px)",
  transition: `
    opacity ${getAnimationDuration("toast")}ms ${getAnimationEasing("toast")},
    transform ${getAnimationDuration("toast")}ms ${getAnimationEasing("toast")}
  `,
  pointerEvents: visible ? "auto" : "none", // Block interaction during exit
})
```

### 6. Stream Progress Feedback

**Pattern**: Progressive status updates for streaming operations.

**Example**: DataManager search with throughput metrics:
```tsx
import { useAtomValue } from '@effect-atom/atom-react'
import { dataManagerAtoms } from '@/lib/data-manager'

function SearchStatus() {
  const status = useAtomValue(dataManagerAtoms.status)
  const throughput = useAtomValue(dataManagerAtoms.throughput)

  const statusColors = {
    idle: "var(--tmnl-neutral, #9ca3af)",
    streaming: "var(--tmnl-processing, #8b5cf6)",
    complete: "var(--tmnl-success, #22c55e)",
    error: "var(--tmnl-error, #ef4444)",
  }

  return (
    <div className="flex items-center gap-2">
      <div
        className="w-2 h-2 rounded-full animate-pulse"
        style={{ backgroundColor: statusColors[status] }}
      />
      <span style={{ fontSize: 'var(--tmnl-text-xs, 12px)' }}>
        {status === 'streaming' && `${throughput.chunks} chunks/s`}
        {status === 'complete' && `${throughput.items} items in ${throughput.ms}ms`}
        {status === 'error' && 'Search failed'}
      </span>
    </div>
  )
}
```

## Examples

### Example 1: Multi-Stage Operation with Toast Feedback

```tsx
import { useToast } from '@/lib/overlays'

function FileUploader() {
  const toast = useToast()
  const [progress, setProgress] = useState(0)

  const handleUpload = async (file: File) => {
    // Stage 1: Validation
    const validationId = toast.info("Validating file...", {
      dismissible: false,
      duration: 0,
    })

    if (!validateFile(file)) {
      toast.close(validationId)
      toast.error("Invalid file type")
      return
    }

    toast.close(validationId)

    // Stage 2: Upload
    const uploadId = toast.info(
      <div>
        Uploading... {progress}%
        <div className="mt-2 h-1 bg-neutral-800 rounded">
          <div
            className="h-full bg-[var(--tmnl-info,#3b82f6)] rounded transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>,
      { dismissible: false, duration: 0 }
    )

    try {
      await uploadWithProgress(file, setProgress)
      toast.close(uploadId)
      toast.success("File uploaded successfully")
    } catch (error) {
      toast.close(uploadId)
      toast.error(`Upload failed: ${error.message}`)
    }
  }
}
```

### Example 2: DebugScope with Custom Metadata

```tsx
import { DebugScope } from '@/lib/debug'

function DataTable({ debug, rows, columns }) {
  const [sortBy, setSortBy] = useState(null)
  const [filter, setFilter] = useState("")

  return (
    <>
      <DebugScope
        debug={debug}
        name="DataTable"
        watch={{
          rowCount: rows.length,
          columnCount: columns.length,
          sortBy,
          filterActive: !!filter,
        }}
        metadata={{
          version: "2.0",
          component: "DataTable",
        }}
      />
      <table>{/* ... */}</table>
    </>
  )
}

// Console output (when debug=true):
// [DataTable] MOUNT { rowCount: 50, columnCount: 5, sortBy: null, filterActive: false, version: "2.0", component: "DataTable" }
// [DataTable] WATCH CHANGED { sortBy: { from: null, to: "name" } }
```

### Example 3: Status Badge Component

```tsx
type Status = "idle" | "processing" | "success" | "error" | "warning"

interface StatusBadgeProps {
  status: Status
  label?: string
}

const STATUS_CONFIG: Record<Status, { color: string; label: string }> = {
  idle: { color: "var(--tmnl-neutral, #9ca3af)", label: "Idle" },
  processing: { color: "var(--tmnl-processing, #8b5cf6)", label: "Processing" },
  success: { color: "var(--tmnl-success, #22c55e)", label: "Success" },
  error: { color: "var(--tmnl-error, #ef4444)", label: "Error" },
  warning: { color: "var(--tmnl-warning, #f59e0b)", label: "Warning" },
}

function StatusBadge({ status, label }: StatusBadgeProps) {
  const config = STATUS_CONFIG[status]

  return (
    <div
      className="inline-flex items-center gap-1.5 px-2 py-1 rounded"
      style={{
        backgroundColor: `${config.color}20`, // 20% opacity
        borderLeft: `3px solid ${config.color}`,
      }}
    >
      <div
        className="w-1.5 h-1.5 rounded-full"
        style={{
          backgroundColor: config.color,
          animation: status === 'processing' ? 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite' : 'none',
        }}
      />
      <span
        className="font-mono uppercase tracking-wider"
        style={{
          fontSize: 'var(--tmnl-text-xs, 12px)',
          color: config.color,
        }}
      >
        {label ?? config.label}
      </span>
    </div>
  )
}
```

## Anti-Patterns

### DON'T: Use Alerts for Non-Critical Feedback

```tsx
// WRONG - Blocks user interaction
alert("Settings saved")

// CORRECT - Use toast
toast.success("Settings saved")
```

### DON'T: Show Loading State for <100ms Operations

```tsx
// WRONG - Flicker on fast operations
const [isLoading, setIsLoading] = useState(false)
setIsLoading(true)
const result = await fastOperation() // 50ms
setIsLoading(false)

// CORRECT - Debounce loading state
const [isLoading, setIsLoading] = useState(false)
const showLoader = useDebounce(isLoading, 150) // Only show if >150ms

const handleFetch = async () => {
  setIsLoading(true)
  try {
    await fetchData()
  } finally {
    setIsLoading(false)
  }
}

// In JSX
{showLoader && <LoadingSpinner />}
```

### DON'T: Auto-Dismiss Error Toasts

```tsx
// WRONG - User might miss critical error
toast.error("Payment failed", { duration: 5000 })

// CORRECT - Errors stay until dismissed
toast.error("Payment failed", { duration: 0 })

// Or use the error() shortcut (already sets duration: 0)
toast.error("Payment failed")
```

### DON'T: Log to DebugScope in Production

```tsx
// WRONG - Always logs, even in production
<DebugScope debug={true} name="MyComponent" />

// CORRECT - Controlled via prop or env var
<DebugScope
  debug={process.env.NODE_ENV === 'development'}
  name="MyComponent"
/>

// Or via feature flag
<DebugScope
  debug={featureFlags.enableDebugLogs}
  name="MyComponent"
/>
```

### DON'T: Use Console.log for User-Facing Feedback

```tsx
// WRONG - User doesn't see console
console.log("File saved")

// CORRECT - Use toast
toast.success("File saved")

// Debug logs are still fine for development
const scope = useDebugScope({ debug: true, name: "FileManager" })
scope.log("File saved to disk", { path })
```

### DON'T: Hardcode Status Colors

```tsx
// WRONG - Inconsistent with design system
<div style={{ color: "#00ff00" }}>Success</div>

// CORRECT - Use CSS variables with fallbacks
<div style={{ color: "var(--tmnl-success, #22c55e)" }}>Success</div>

// Or design tokens
import { TMNL_STATUS_COLORS } from '@/lib/tokens'
<div style={{ color: TMNL_STATUS_COLORS.success }}>Success</div>
```

## Testing Feedback Patterns

### Manual Testing Checklist

1. **Toast Notifications**:
   - [ ] Toasts appear at correct position
   - [ ] Variants have distinct visual styling
   - [ ] Auto-dismiss works for info/success/warning
   - [ ] Errors don't auto-dismiss
   - [ ] Multiple toasts stack correctly
   - [ ] Close button works when dismissible
   - [ ] Animation timing feels natural (200ms)

2. **Loading States**:
   - [ ] Loading indicator appears after debounce delay
   - [ ] No flicker on fast operations (<100ms)
   - [ ] User can't interact with blocked content
   - [ ] Loading state clears on error

3. **Status Colors**:
   - [ ] Colors are consistent across components
   - [ ] Sufficient contrast for accessibility
   - [ ] Color meaning is clear without text labels

4. **DebugScope**:
   - [ ] No logs in production when debug=false
   - [ ] Mount/unmount logs show correct timing
   - [ ] Dependency changes are tracked accurately
   - [ ] Nested scopes show parent.child hierarchy

### Debug Mode Testing

```tsx
// Enable debug mode for feedback system
<DebugScopeProvider debug={true} name="FeedbackSystem">
  <ToastRenderer />
  <LoadingOverlay />
</DebugScopeProvider>

// Check console for lifecycle events:
// [FeedbackSystem.ToastRenderer] MOUNT
// [FeedbackSystem.ToastRenderer] WATCH CHANGED { isVisible: { from: false, to: true } }
// [FeedbackSystem.ToastRenderer] UNMOUNT { duration: "250.34ms" }
```

## Related Skills

- `ux-interaction-patterns` - Modifier keys, keybindings, hover states
- `ux-accessibility-patterns` - ARIA, focus management for feedback
- `ux-overlay-patterns` - Modal/toast z-index, animation states

## References

- Toast Implementation: `/src/lib/overlays/visual/hooks/useToast.ts`
- DebugScope: `/src/lib/debug/DebugScope.tsx`
- Animation Constants: `/src/lib/overlays/visual/constants.ts`
- Status Colors: Various `*-theme.ts` files in `/src/lib/*/theme/`
