---
name: kumo-query-module
description: Expert assistant for Kumo's Query Module (src/features/query). Use when working with SQL Editor, Monaco editor integration, query execution, result grids, tabs management, AI features, or any query-related components. Provides architecture patterns, component APIs, hooks, utilities, and examples.
---

# Kumo Query Module Expert

Comprehensive guide for developing and extending Kumo's Query Module (`src/features/query`) - the SQL Editor and query execution system.

## When to Use This Skill

Use this skill when:
- Working on the **SQL Editor** (`SQLEditor.tsx`)
- Adding features to **Monaco Editor** integration
- Modifying **query execution** logic
- Working with **ResultGrid** or result display
- Managing **editor tabs** system
- Implementing **AI-powered features** (natural language to SQL, query optimization)
- Building **toolbar components** or editor controls
- Handling **datetime/timezone** display
- Working with **export/copy** functionality
- Implementing **auto-refresh** or **split editor** features

## Quick Start

### Module Structure

```
src/features/query/
├── SQLEditor.tsx              # Main SQL editor component (800+ lines)
├── ResultGrid.tsx             # Query results display with inline editing
├── NaturalLanguageToSQL.tsx   # AI: Convert natural language to SQL
├── AIResultsPanel.tsx         # AI analysis results display
├── ExplainVisualizer.tsx      # EXPLAIN query visualization
├── QueryHistoryPanel.tsx      # Query history sidebar
├── SavedQueriesPanel.tsx      # Saved queries sidebar
├── QuerySnippetsPanel.tsx     # SQL snippets sidebar
├── QueryResultsCompare.tsx    # Compare query results (split view)
│
├── components/
│   ├── EditorToolbar/         # Toolbar buttons and controls
│   │   ├── index.tsx          # Main toolbar component
│   │   ├── RunButton.tsx      # Execute query button
│   │   ├── FormatButtons.tsx  # Format/minify SQL buttons
│   │   ├── AIMenuButton.tsx   # AI features dropdown
│   │   ├── AutoRefreshToggle.tsx  # Auto-refresh control
│   │   ├── UtilityButtons.tsx # Misc utility buttons
│   │   └── ToolbarRightButtons.tsx  # Right-aligned buttons
│   │
│   ├── EditorTabBar/          # Tab management
│   │   ├── index.tsx          # Tab bar component
│   │   ├── EditorTab.tsx      # Single tab component
│   │   ├── TabColorPicker.tsx # Tab color selector
│   │   └── NewTabButton.tsx   # Add new tab button
│   │
│   ├── RightPanelSidebar/     # History/Saved/Snippets panels
│   │   └── index.tsx          # Sidebar toggle component
│   │
│   ├── DateTimeDisplay.tsx    # Timezone-aware datetime rendering
│   ├── ResultTable.tsx        # Virtual scrolling results table
│   ├── ResultGridHeader.tsx   # Result grid toolbar
│   ├── NonSelectResult.tsx    # INSERT/UPDATE/DELETE results
│   ├── ContextMenu.tsx        # Right-click context menu
│   ├── ContextMenuLogic.tsx   # Context menu state logic
│   ├── PivotPanel.tsx         # Pivot table & charts
│   ├── PivotFullScreenOverlay.tsx  # Fullscreen pivot view
│   ├── ToastNotification.tsx  # Toast messages
│   │
│   ├── TableColumns.tsx       # Result grid column definitions (hook)
│   ├── CopyFunctions.tsx      # Copy to clipboard functions (hook)
│   ├── ExportFunctions.tsx    # Export CSV/JSON/Excel (hook)
│   ├── QueryGenerator.tsx     # Generate UPDATE/INSERT/DELETE (hook)
│   ├── PivotFunctions.tsx     # Pivot table logic (hook)
│   ├── EditModeFunctions.tsx  # Inline edit mode logic (hook)
│   ├── DatabaseResolution.tsx # Resolve database/table from SQL (hook)
│   └── QueryUtils.tsx         # Utility functions
│
└── utils/
    ├── sqlUtils.ts            # SQL parsing, formatting, validation
    └── tabUtils.ts            # Tab state management

```

## Core Architecture

### 1. SQLEditor Component

**Main component** (`SQLEditor.tsx`) - Central orchestrator for the query module.

**Key Responsibilities**:
- Monaco Editor integration
- Multi-tab management
- Query execution workflow
- State management (40+ state variables!)
- Toolbar coordination
- Results display
- Split editor mode
- Auto-refresh
- AI features integration

**State Structure**:
```typescript
const [sql, setSql] = useState<string>('');                    // Current SQL
const [results, setResults] = useState<QueryResult[] | null>(); // Query results
const [tabs, setTabs] = useState<EditorTab[]>();               // All tabs
const [activeEditorTab, setActiveEditorTab] = useState(0);     // Active tab index
const [selectedTimezone, setSelectedTimezone] = useState('default');
const [splitEnabled, setSplitEnabled] = useState(false);       // Split editor
const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(false);
// ... 30+ more state variables
```

**Key Features**:
- **Monaco Editor** with syntax highlighting, autocomplete, validation
- **Tab system** with color coding, pinning, persistence (localStorage)
- **Split editor** for comparing queries side-by-side
- **Auto-refresh** with countdown timer
- **AI integration** (explain, optimize, analyze, natural language to SQL)
- **Timezone support** for datetime display
- **Format on paste** (auto-format pasted SQL)
- **Dark mode** support

### 2. Query Execution Flow

```
User clicks Run → handleExecuteQuery()
    ↓
getQueryAtCursor() → Extract SQL at cursor position
    ↓
executeQueryMutation.mutate() → Send to backend API
    ↓
Backend executes query → Returns QueryResult[]
    ↓
setResults() → Update state
    ↓
ResultGrid renders → Display results with inline editing
```

**Key API**: `useExecuteQuery` hook from `hooks/useQuery.ts`

### 3. Monaco Editor Integration

**Setup**:
```typescript
import Editor from '@monaco-editor/react';

<Editor
  height="260px"
  language="sql"
  theme={isDarkMode ? 'vs-dark' : 'vs'}
  value={sql}
  onChange={(value) => setSql(value || '')}
  onMount={handleEditorMount}
  options={{
    minimap: { enabled: false },
    fontSize: 14,
    lineNumbers: 'on',
    automaticLayout: true,
    formatOnPaste: formatOnPaste,
    // ... more options
  }}
/>
```

**Custom Features**:
- **SQL syntax validation** (`validateSQL()` in `sqlUtils.ts`)
- **Auto-complete** (value hints from database)
- **Format SQL** (`formatSQL()` using `sql-formatter`)
- **Minify SQL** (`minifySQL()` - remove comments/whitespace)
- **Query at cursor** (`getQueryAtCursor()` - execute specific query)

### 4. Tab Management

**EditorTab Type**:
```typescript
type EditorTab = {
  id: string;              // Unique tab ID
  name: string;            // Tab display name
  sql: string;             // SQL content
  results: QueryResult[] | null;
  error: string | null;
  isRunning: boolean;
  isPinned?: boolean;      // Prevent tab close
  color?: string;          // Tab color (#hex)
  executionTime?: number;  // Last execution time
  rowsAffected?: number;   // Rows affected
};
```

**Persistence**: Tabs saved to `localStorage` (excluding runtime state)

**Key Functions** (from `tabUtils.ts`):
- `loadSavedTabs()` - Load tabs from localStorage on mount
- `saveTabs()` - Save tabs to localStorage (auto on change)
- `createNewTab()` - Create new tab with default SQL
- `duplicateTab()` - Duplicate existing tab
- `generateTabId()` - Generate unique tab identifier

### 5. ResultGrid Component

**Purpose**: Display query results with advanced features:
- Virtual scrolling (TanStack Virtual)
- Inline editing
- Sorting
- Export (CSV, JSON, Excel)
- Copy (cell, column, row, all)
- Pivot tables & charts
- Context menu
- Timezone-aware datetime display

**Architecture**:
```
ResultGrid (main)
  ├── ResultGridHeader (toolbar)
  ├── ResultTable (virtualized table)
  ├── PivotPanel (pivot/chart preview)
  ├── PivotFullScreenOverlay (fullscreen pivot)
  ├── ContextMenu (right-click menu)
  └── ToastNotification (feedback messages)
```

**See**: [components.md](components.md) for detailed component API

## Common Development Tasks

### Task 1: Add a New Toolbar Button

**Location**: `src/features/query/components/EditorToolbar/`

**Steps**:
1. Create new component file (e.g., `MyButton.tsx`)
2. Implement button with handler
3. Import and add to `EditorToolbar/index.tsx`

**Example**:
```typescript
// MyButton.tsx
import { Sparkles } from 'lucide-react';

interface MyButtonProps {
  onAction: () => void;
  disabled?: boolean;
}

export const MyButton: React.FC<MyButtonProps> = ({ onAction, disabled }) => {
  return (
    <button
      onClick={onAction}
      disabled={disabled}
      className="px-3 py-1.5 text-sm rounded hover:bg-gray-100 dark:hover:bg-gray-800"
      title="My Custom Action"
    >
      <Sparkles className="w-4 h-4" />
    </button>
  );
};

// EditorToolbar/index.tsx
import { MyButton } from './MyButton';

export const EditorToolbar = ({ ... }) => {
  const handleMyAction = () => {
    // Your logic here
  };

  return (
    <div className="toolbar">
      {/* ... other buttons ... */}
      <MyButton onAction={handleMyAction} />
    </div>
  );
};
```

### Task 2: Add New SQL Utility Function

**Location**: `src/features/query/utils/sqlUtils.ts`

**Example**: Add a function to extract table names from SQL

```typescript
// sqlUtils.ts

/**
 * Extract table names from SQL query
 */
export const extractTableNames = (sql: string): string[] => {
  const tables: string[] = [];
  const upperSql = sql.toUpperCase();

  // Match FROM and JOIN clauses
  const fromRegex = /FROM\s+`?(\w+)`?/gi;
  const joinRegex = /JOIN\s+`?(\w+)`?/gi;

  let match;
  while ((match = fromRegex.exec(sql)) !== null) {
    tables.push(match[1]);
  }
  while ((match = joinRegex.exec(sql)) !== null) {
    tables.push(match[1]);
  }

  return [...new Set(tables)]; // Remove duplicates
};
```

### Task 3: Add New AI Feature

**Location**: `src/features/query/SQLEditor.tsx` and AI components

**Steps**:
1. Add new AI result type to `aiResultType` state
2. Create handler function
3. Add menu item to `AIMenuButton.tsx`
4. Handle response in `AIResultsPanel.tsx`

**Example**: Add "Suggest Indexes" feature

```typescript
// SQLEditor.tsx

// 1. Add to type (if needed)
type AIFeature = 'explain' | 'optimize' | 'analyze' | 'schema' | 'suggest-indexes';

// 2. Create handler
const handleSuggestIndexes = async () => {
  if (!connectionId) return;

  setIsAIProcessing(true);
  setAiResultType('suggest-indexes');

  try {
    const response = await aiApi.suggestIndexes(connectionId, currentDatabase, sql);
    setAiResultContent(response.suggestions);
  } catch (error) {
    setAiResultContent('Failed to generate index suggestions.');
  } finally {
    setIsAIProcessing(false);
  }
};

// 3. Add menu item in AIMenuButton.tsx
<button onClick={handleSuggestIndexes}>
  <Database className="w-4 h-4" />
  Suggest Indexes
</button>

// 4. Handle display in AIResultsPanel.tsx
{aiResultType === 'suggest-indexes' && (
  <div className="suggestions">
    <h3>Index Suggestions</h3>
    <pre>{aiResultContent}</pre>
  </div>
)}
```

### Task 4: Modify Datetime Display

**Location**: `src/features/query/components/DateTimeDisplay.tsx`

**Use Case**: Change datetime format or add new timezone logic

**Current Logic**:
- DATE columns → `YYYY-MM-DD`
- DATETIME/TIMESTAMP columns → `YYYY-MM-DD HH:MM:SS`
- Timezone conversion support

**Example**: Add milliseconds to datetime display

```typescript
// DateTimeDisplay.tsx

const formatDateInTimezone = (date: Date, timezone?: string, showMs = false): string => {
  // ... existing code ...

  const milliseconds = String(date.getMilliseconds()).padStart(3, '0');

  if (showMs) {
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
  }

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};
```

### Task 5: Add New Export Format

**Location**: `src/features/query/components/ExportFunctions.tsx`

**Example**: Add XML export

```typescript
// ExportFunctions.tsx

const exportToXML = useCallback(async () => {
  const dataToExport = /* ... get data ... */;

  // Build XML
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<rows>\n';
  dataToExport.forEach((row) => {
    xml += '  <row>\n';
    Object.entries(row).forEach(([key, value]) => {
      xml += `    <${key}>${value}</${key}>\n`;
    });
    xml += '  </row>\n';
  });
  xml += '</rows>';

  // Download
  const blob = new Blob([xml], { type: 'application/xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `query-results.xml`;
  a.click();
  URL.revokeObjectURL(url);
}, [rows, selectedTimezone]);

return {
  exportToCSV,
  exportToJSON,
  exportToExcel,
  exportToXML,  // Add to return
};
```

## Key Utilities

### SQL Utilities (`utils/sqlUtils.ts`)

```typescript
// Get query at cursor position
const query = getQueryAtCursor(editorRef.current);

// Get query with line range
const { query, startLine, endLine } = getQueryAtCursorWithRange(editorRef.current);

// Format SQL
const formatted = formatSQL(sql);  // Uses sql-formatter

// Minify SQL
const minified = minifySQL(sql);   // Remove comments/whitespace

// Validate SQL
validateSQL(editorRef.current, sql);  // Sets Monaco markers
```

### Tab Utilities (`utils/tabUtils.ts`)

```typescript
// Load tabs from localStorage
const tabs = loadSavedTabs();

// Save tabs to localStorage
saveTabs(tabs);

// Create new tab
const newTab = createNewTab(existingTabs, 'SELECT * FROM users;', 'Users Query');

// Duplicate tab
const duplicatedTab = duplicateTab(originalTab, existingTabs);

// Generate unique ID
const id = generateTabId();  // 'tab_1234567890_abcd'
```

## Hooks Used

**From `hooks/useQuery.ts`**:
- `useExecuteQuery()` - Execute single query
- `useExecuteMultipleQueries()` - Execute multiple queries
- `useCancelQuery()` - Cancel running query

**From `hooks/useConnections.ts`**:
- `useConnection(id)` - Get connection details

**From `hooks/useSavedQueries.ts`**:
- `useCreateSavedQuery()` - Save query to library

**Custom Hooks in Components**:
- `useResultTableColumns()` - Generate result grid columns
- `useCopyFunctions()` - Copy operations
- `useExportFunctions()` - Export operations
- `useQueryGenerator()` - Generate UPDATE/INSERT/DELETE
- `usePivotFunctions()` - Pivot table logic
- `useEditModeFunctions()` - Inline edit mode
- `useDatabaseResolution()` - Resolve DB/table from SQL
- `useContextMenuLogic()` - Context menu state

## Best Practices

### 1. State Management

**DO**:
```typescript
// Use refs for frequently changing callbacks
const onEditCellRef = useRef(onEditCell);
useEffect(() => { onEditCellRef.current = onEditCell; }, [onEditCell]);

// Keep deps minimal in useMemo/useCallback
const columns = useMemo(() => {
  // ...
}, [columnInfo, editable]);  // Only essential deps
```

**DON'T**:
```typescript
// Don't recreate functions on every render
const handleClick = () => {  // ❌ New function every render
  doSomething();
};

// Use useCallback instead
const handleClick = useCallback(() => {  // ✅
  doSomething();
}, []);
```

### 2. Monaco Editor

**DO**:
```typescript
// Store editor reference
const editorRef = useRef<any>(null);

const handleEditorMount = (editor: any) => {
  editorRef.current = editor;
  // Set up editor features
  validateSQL(editor, sql);
};
```

**DON'T**:
```typescript
// Don't access editor directly without ref ❌
```

### 3. Tab Persistence

**DO**:
```typescript
// Auto-save tabs on change
useEffect(() => {
  saveTabs(tabs);
}, [tabs]);

// Load on mount
const [tabs, setTabs] = useState(() => loadSavedTabs());
```

### 4. Error Handling

**DO**:
```typescript
try {
  const result = await executeQuery();
  setResults(result);
} catch (error) {
  setError(error.message);
  // Show toast notification
  setToast({ message: error.message, type: 'error' });
}
```

### 5. Performance

**DO**:
```typescript
// Use virtual scrolling for large result sets
import { useVirtualizer } from '@tanstack/react-virtual';

// Lazy load components
const ExplainVisualizer = lazy(() => import('./ExplainVisualizer'));

// Debounce expensive operations
import { useDebounce } from 'use-debounce';
const [debouncedSearch] = useDebounce(search, 300);
```

## Common Patterns

### Pattern 1: Custom Hook for Feature Logic

```typescript
// Good: Extract complex logic into custom hook
export function useMyFeature({ sql, connectionId }: Props) {
  const [state, setState] = useState();

  const doSomething = useCallback(() => {
    // Logic here
  }, [sql, connectionId]);

  useEffect(() => {
    // Side effects
  }, [connectionId]);

  return { state, doSomething };
}

// Usage
const { state, doSomething } = useMyFeature({ sql, connectionId });
```

### Pattern 2: Portal Rendering for Dropdowns

```typescript
// Render dropdown at document root to avoid z-index issues
{showDropdown && ReactDOM.createPortal(
  <div style={{ position: 'absolute', left: pos.x, top: pos.y }}>
    <Dropdown />
  </div>,
  document.body
)}
```

### Pattern 3: Keyboard Shortcuts

```typescript
// Use Monaco editor's keyboard API
editor.addAction({
  id: 'execute-query',
  label: 'Execute Query',
  keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
  run: () => handleExecuteQuery(),
});
```

## Troubleshooting

### Issue: Monaco editor not syntax highlighting

**Solution**: Check language mode is set to 'sql'
```typescript
<Editor language="sql" />  // Not 'mysql' or 'postgres'
```

### Issue: Tabs not persisting

**Solution**: Check localStorage quota and error handling
```typescript
try {
  localStorage.setItem('sqlEditorTabs', JSON.stringify(tabs));
} catch (e) {
  console.error('Failed to save tabs:', e);  // Quota exceeded?
}
```

### Issue: Query at cursor returns null

**Solution**: Ensure editor is mounted and has content
```typescript
if (!editorRef.current) return;
const model = editorRef.current.getModel();
if (!model) return;
```

### Issue: Datetime showing wrong timezone

**Solution**: Check `selectedTimezone` state and `DateTimeDisplay` props
```typescript
<DateTimeDisplay value={value} timezone={selectedTimezone} columnType={field.type} />
```

## Further Reading

- [components.md](components.md) - Detailed component API reference
- [hooks.md](hooks.md) - Custom hooks documentation
- [examples.md](examples.md) - Real-world examples and recipes

## Quick Reference

**Main Files**:
- `SQLEditor.tsx` - Main component (800+ lines)
- `ResultGrid.tsx` - Query results display
- `utils/sqlUtils.ts` - SQL utilities
- `utils/tabUtils.ts` - Tab management
- `components/DateTimeDisplay.tsx` - Datetime rendering

**Key State**:
- `sql` - Current SQL content
- `tabs` - All editor tabs
- `activeEditorTab` - Active tab index
- `results` - Query results
- `selectedTimezone` - Timezone for datetime display

**Key Hooks**:
- `useExecuteQuery()` - Execute query
- `useResultTableColumns()` - Result grid columns
- `useExportFunctions()` - Export data

**Utilities**:
- `getQueryAtCursor()` - Get query at cursor
- `formatSQL()` - Format SQL
- `validateSQL()` - Validate and set markers
