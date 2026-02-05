---
name: maintaining-code-quality
description: Maintaining code quality and standards in StickerNest. Use when refactoring code, checking file sizes, splitting large files, reviewing code structure, or when files exceed length limits. Covers file length limits, refactoring patterns, code organization, and the "check existing code first" principle.
---

# Maintaining Code Quality

This skill defines StickerNest's code quality standards, including file length limits, refactoring triggers, and the critical "check existing code first" principle.

## The Golden Rule: Check Existing Code First

**BEFORE writing any new code, ALWAYS:**

1. **Search for existing implementations**
   ```bash
   # Search for similar functionality
   grep -r "similar keyword" src/
   ```

2. **Check for existing utilities**
   - `src/utils/` - Utility functions
   - `src/hooks/` - Custom hooks
   - `src/components/` - Reusable components

3. **Follow existing patterns**
   - Find a similar feature
   - Match its structure and conventions
   - Reuse its helpers and utilities

4. **Ask yourself:**
   - Does this already exist somewhere?
   - Can I extend an existing solution?
   - Is there a pattern I should follow?

**Why?** Duplicate code leads to inconsistencies, bugs, and maintenance burden. StickerNest has many utilities that solve common problems.

## File Length Limits

| File Type | Ideal | Warning | Refactor Required |
|-----------|-------|---------|-------------------|
| Component (.tsx) | < 300 | 300-500 | > 500 |
| Store (.ts) | < 400 | 400-600 | > 600 |
| Utility (.ts) | < 200 | 200-300 | > 300 |
| Hook (.ts) | < 150 | 150-250 | > 250 |
| Types (.ts) | < 200 | 200-400 | > 400 |
| Test (.test.ts) | < 500 | 500-800 | > 800 |

### Current Large Files (Need Attention)

Based on codebase analysis, these files exceed limits:

```
1924 lines - src/runtime/WidgetSandboxHost.ts     ⚠️ CRITICAL
1808 lines - src/components/.../StyleGalleryPanel.tsx  ⚠️ CRITICAL
1586 lines - src/runtime/WidgetAPI.ts             ⚠️ CRITICAL
1548 lines - src/widgets/.../LiveChatWidget.ts    ⚠️ CRITICAL
1471 lines - src/services/enhancedAIGenerator.ts  ⚠️ CRITICAL
1403 lines - src/state/useCanvasStore.ts          ⚠️ CRITICAL
```

## When to Refactor

### Immediate Refactoring Triggers

1. **File exceeds line limit** (see table above)
2. **Function > 50 lines** - Extract helper functions
3. **Component > 200 lines JSX** - Split into sub-components
4. **> 5 useState hooks** - Consider useReducer or custom hook
5. **> 3 levels of nesting** - Extract to separate functions
6. **Duplicate code** - Extract to shared utility

### Refactoring Signals

```typescript
// 🚩 Too many imports (> 15)
import { a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p } from '...';
// → Split into focused modules

// 🚩 God component (does too much)
function MyComponent() {
  // 500+ lines of mixed concerns
}
// → Split into container + presentational components

// 🚩 Prop drilling (> 3 levels)
<A data={data}><B data={data}><C data={data}><D data={data} /></C></B></A>
// → Use context or Zustand store

// 🚩 Complex conditionals
if (a && (b || c) && (!d || (e && f))) { ... }
// → Extract to named boolean or function
```

## Refactoring Patterns

### Extracting Components

```typescript
// BEFORE: Monolithic component
function BigComponent() {
  return (
    <div>
      {/* 50 lines of header */}
      {/* 100 lines of content */}
      {/* 50 lines of footer */}
    </div>
  );
}

// AFTER: Composed components
function BigComponent() {
  return (
    <div>
      <Header />
      <Content />
      <Footer />
    </div>
  );
}

// Each in its own file if > 100 lines
// src/components/BigComponent/
//   index.tsx
//   Header.tsx
//   Content.tsx
//   Footer.tsx
```

### Extracting Hooks

```typescript
// BEFORE: Logic in component
function MyComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  // ... 200 more lines
}

// AFTER: Custom hook
function useDataFetch() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}

function MyComponent() {
  const { data, loading, error } = useDataFetch();
  // ... cleaner component
}
```

### Extracting Store Slices

```typescript
// BEFORE: Massive store
// useCanvasStore.ts - 1400 lines

// AFTER: Sliced stores
// useCanvasStore.ts - Main canvas state
// useSelectionStore.ts - Selection logic
// useViewportStore.ts - Viewport/zoom/pan
// useHistoryStore.ts - Undo/redo
// useGridStore.ts - Grid/snap settings

// Or use Zustand slices pattern:
const createSelectionSlice = (set, get) => ({
  selectedIds: new Set(),
  select: (id) => set({ selectedIds: new Set([id]) }),
  // ...
});
```

### Extracting Utilities

```typescript
// BEFORE: Inline logic
function Component() {
  const formatted = value
    .replace(/[^a-z]/gi, '')
    .toLowerCase()
    .substring(0, 50);
}

// AFTER: Utility function
// src/utils/formatters.ts
export function sanitizeInput(value: string, maxLength = 50): string {
  return value
    .replace(/[^a-z]/gi, '')
    .toLowerCase()
    .substring(0, maxLength);
}

// Component
import { sanitizeInput } from '@/utils/formatters';
const formatted = sanitizeInput(value);
```

## File Organization

### Component Structure

```
src/components/MyFeature/
├── index.tsx           # Main export
├── MyFeature.tsx       # Main component (< 300 lines)
├── MyFeatureHeader.tsx # Sub-component
├── MyFeatureList.tsx   # Sub-component
├── useMyFeature.ts     # Custom hooks
├── MyFeature.types.ts  # Types (if > 50 lines)
├── MyFeature.utils.ts  # Utilities
└── MyFeature.test.tsx  # Tests
```

### Module Structure

```
src/features/canvas/
├── index.ts            # Public API
├── components/         # UI components
├── hooks/              # Feature hooks
├── store/              # Zustand store(s)
├── utils/              # Utilities
├── types.ts            # Types
└── constants.ts        # Constants
```

## Code Review Checklist

### Before Submitting

- [ ] **Checked for existing code** that does similar things
- [ ] **File lengths** within limits
- [ ] **No duplicate code** - extracted to utilities
- [ ] **Follows existing patterns** in codebase
- [ ] **Imports are reasonable** (< 15 per file)
- [ ] **No commented-out code** (delete it)
- [ ] **No console.log** (except error handling)

### For New Files

- [ ] **Placed in correct directory**
- [ ] **Named consistently** with conventions
- [ ] **Has TypeScript types** (no `any` unless necessary)
- [ ] **Exports are intentional** (don't export everything)

### For Refactoring

- [ ] **Behavior unchanged** (same inputs → same outputs)
- [ ] **Tests still pass**
- [ ] **No new TypeScript errors**
- [ ] **Imports updated** across codebase

## Naming Conventions

```typescript
// Components: PascalCase
MyComponent.tsx
WidgetCard.tsx

// Hooks: camelCase with 'use' prefix
useCanvasStore.ts
useWidgetDrag.ts

// Utilities: camelCase
formatDate.ts
validateInput.ts

// Types: PascalCase
types.ts → interface WidgetInstance { }
types.ts → type CanvasMode = 'edit' | 'view';

// Constants: SCREAMING_SNAKE_CASE
const MAX_WIDGETS = 100;
const API_ENDPOINT = '/api/v1';
```

## Anti-Patterns to Avoid

```typescript
// ❌ God objects
const everythingStore = { /* 1000+ properties */ };

// ❌ Prop drilling
<A><B><C><D><E prop={value} /></D></C></B></A>

// ❌ Inline styles everywhere
<div style={{ color: 'red', padding: 20, margin: 10, ... }}>

// ❌ Magic numbers
if (widgets.length > 47) { /* why 47? */ }

// ❌ Nested ternaries
const result = a ? b ? c : d : e ? f : g;

// ❌ any types
function process(data: any): any { }

// ❌ Mutation
state.items.push(newItem); // ❌
set({ items: [...get().items, newItem] }); // ✅
```

## Quick Commands

```bash
# Find large files
find src -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -n | tail -20

# Find files with too many imports
grep -l "^import" src/**/*.{ts,tsx} | xargs -I{} sh -c 'echo "$(grep "^import" {} | wc -l) {}"' | sort -n | tail -10

# Find potential duplicates (similar function names)
grep -rh "function\|const.*=.*=>" src/ | sort | uniq -c | sort -n | tail -20
```
