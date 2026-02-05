---
name: composable-svelte-code
description: Code editing, syntax highlighting, and visual programming for Composable Svelte. Use when implementing code editors, syntax highlighting, or node-based visual programming. Covers CodeEditor (CodeMirror), CodeHighlight (Prism), and NodeCanvas (SvelteFlow) from @composable-svelte/code package.
---

# Composable Svelte Code Package

Code editing, syntax highlighting, and visual programming components.

---

## PACKAGE OVERVIEW

**Package**: `@composable-svelte/code`

**Purpose**: Rich interactive components for code editing and visual programming.

**Technology Stack**:
- **CodeMirror 6**: Modern code editor with extensible architecture
- **Prism.js**: Lightweight syntax highlighter
- **SvelteFlow**: Node-based visual programming canvas

**Core Components**:
- `CodeEditor` - Full-featured code editor (CodeMirror)
- `CodeHighlight` - Read-only syntax highlighting (Prism)
- `NodeCanvas` - Visual node editor (SvelteFlow)

**State Management**:
All components follow Composable Architecture patterns with dedicated reducers and type-safe actions.

---

## CODE EDITOR (CodeMirror)

**Purpose**: Full-featured code editor with syntax highlighting, autocomplete, and language support.

### Quick Start

```typescript
import { createStore } from '@composable-svelte/core';
import { CodeEditor, codeEditorReducer, createInitialState } from '@composable-svelte/code';

// Create editor store
const store = createStore({
  initialState: createInitialState({
    value: '// Write code here',
    language: 'typescript',
    theme: 'dark',
    showLineNumbers: true
  }),
  reducer: codeEditorReducer,
  dependencies: {
    onSave: async (value) => {
      await fetch('/api/save', { method: 'POST', body: value });
    },
    formatter: async (code, language) => {
      // Use prettier or similar
      return formatCode(code, language);
    }
  }
});

// Render editor
<CodeEditor {store} showToolbar={true} />
```

### Props

- `store: Store<CodeEditorState, CodeEditorAction>` - Editor store (required)
- `showToolbar: boolean` - Show toolbar with controls (default: true)

### State Interface

```typescript
interface CodeEditorState {
  // Content
  value: string;                    // Current code
  language: SupportedLanguage;      // Active language

  // Cursor & Selection
  cursorPosition: { line: number; column: number } | null;
  selection: EditorSelection | null;

  // UI State
  theme: 'light' | 'dark' | 'auto';
  showLineNumbers: boolean;
  readOnly: boolean;

  // Features
  enableAutocomplete: boolean;
  enableLinting: boolean;
  tabSize: number;

  // Editor Status
  hasUnsavedChanges: boolean;
  lastSavedValue: string | null;
  isFocused: boolean;

  // History
  canUndo: boolean;
  canRedo: boolean;

  // Errors
  error: string | null;
  saveError: string | null;
  formatError: string | null;
}
```

### Supported Languages

TypeScript, JavaScript, Svelte, HTML, CSS, JSON, Markdown, Bash, SQL, Python, Rust

### Actions

```typescript
type CodeEditorAction =
  // Content
  | { type: 'valueChanged'; value: string; cursorPosition?: {...} }
  | { type: 'languageChanged'; language: SupportedLanguage }

  // Editing
  | { type: 'undo' }
  | { type: 'redo' }
  | { type: 'insertText'; text: string; position?: {...} }
  | { type: 'selectAll' }

  // Configuration
  | { type: 'themeChanged'; theme: 'light' | 'dark' | 'auto' }
  | { type: 'toggleLineNumbers' }
  | { type: 'setReadOnly'; readOnly: boolean }

  // Save/Format
  | { type: 'save' }
  | { type: 'format' };
```

### Dependencies

```typescript
interface CodeEditorDependencies {
  // Save handler
  onSave?: (value: string) => Promise<void>;

  // Format handler
  formatter?: (code: string, language: SupportedLanguage) => Promise<string>;
}
```

### Complete Example

```typescript
<script lang="ts">
import { createStore, Effect } from '@composable-svelte/core';
import { CodeEditor, codeEditorReducer, createInitialState } from '@composable-svelte/code';
import { formatCode } from './my-formatter'; // Your formatter

// Create store with dependencies
const editorStore = createStore({
  initialState: createInitialState({
    value: `function hello() {\n  console.log('Hello, World!');\n}`,
    language: 'typescript',
    theme: 'dark',
    showLineNumbers: true,
    enableAutocomplete: true,
    tabSize: 2
  }),
  reducer: codeEditorReducer,
  dependencies: {
    // Handle save
    onSave: async (value: string) => {
      console.log('Saving code:', value);
      await fetch('/api/code/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: value })
      });
    },

    // Handle format
    formatter: async (code: string, language: string) => {
      return formatCode(code, language);
    }
  }
});
</script>

<div class="editor-container">
  <CodeEditor store={editorStore} showToolbar={true} />

  <!-- Status bar -->
  <div class="status-bar">
    {#if $editorStore.hasUnsavedChanges}
      <span class="status-warning">Unsaved changes</span>
    {/if}
    {#if $editorStore.cursorPosition}
      <span>Ln {$editorStore.cursorPosition.line}, Col {$editorStore.cursorPosition.column}</span>
    {/if}
    <span>{$editorStore.language}</span>
  </div>
</div>
```

### Toolbar Features

When `showToolbar={true}`:
- Language selector dropdown
- Line numbers toggle
- Theme toggle (light/dark)
- Format button
- Save button (shows "Save *" when unsaved changes)

### Keyboard Shortcuts

CodeMirror provides standard keyboard shortcuts:
- `Ctrl/Cmd + S`: Save
- `Ctrl/Cmd + Z`: Undo
- `Ctrl/Cmd + Shift + Z`: Redo
- `Ctrl/Cmd + /`: Toggle comment
- `Ctrl/Cmd + D`: Delete line
- `Ctrl/Cmd + A`: Select all

---

## CODE HIGHLIGHT (Prism.js)

**Purpose**: Read-only syntax highlighting for displaying code snippets.

### Quick Start

```typescript
import { CodeHighlight } from '@composable-svelte/code';

<CodeHighlight
  code={`const greeting = "Hello, World!";`}
  language="javascript"
  theme="dark"
  showLineNumbers={true}
/>
```

### Props

- `code: string` - Code to highlight (required)
- `language: string` - Language (e.g., 'javascript', 'typescript', 'python')
- `theme: 'light' | 'dark'` - Color theme (default: 'dark')
- `showLineNumbers: boolean` - Show line numbers (default: false)
- `highlightLines: number[]` - Lines to highlight (optional)
- `class: string` - Custom CSS class (optional)

### Supported Languages

JavaScript, TypeScript, Python, Rust, Go, Java, C, C++, C#, PHP, Ruby, SQL, HTML, CSS, JSON, YAML, Markdown, Bash, Svelte, and more.

### Examples

```typescript
<!-- Basic highlighting -->
<CodeHighlight
  code={`function add(a, b) {\n  return a + b;\n}`}
  language="javascript"
/>

<!-- With line numbers -->
<CodeHighlight
  code={pythonCode}
  language="python"
  showLineNumbers={true}
/>

<!-- Highlight specific lines -->
<CodeHighlight
  code={tsCode}
  language="typescript"
  highlightLines={[3, 5, 7]}
/>

<!-- Custom theme -->
<CodeHighlight
  code={rustCode}
  language="rust"
  theme="light"
/>
```

### When to Use CodeEditor vs CodeHighlight

**Use CodeEditor**:
- User needs to edit code
- Autocomplete required
- Linting/error checking needed
- Save functionality required

**Use CodeHighlight**:
- Display-only code snippets
- Documentation/tutorials
- Code examples in blog posts
- Faster rendering for many snippets

---

## NODE CANVAS (SvelteFlow)

**Purpose**: Visual node-based programming canvas (node editor, flow diagrams).

### Quick Start

```typescript
import { createStore } from '@composable-svelte/core';
import { NodeCanvas, nodeCanvasReducer, createInitialNodeCanvasState } from '@composable-svelte/code';

// Create node canvas store
const canvasStore = createStore({
  initialState: createInitialNodeCanvasState({
    nodes: [
      {
        id: '1',
        type: 'input',
        position: { x: 100, y: 100 },
        data: { label: 'Input Node' }
      },
      {
        id: '2',
        type: 'default',
        position: { x: 300, y: 100 },
        data: { label: 'Process Node' }
      }
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2' }
    ]
  }),
  reducer: nodeCanvasReducer,
  dependencies: {}
});

<NodeCanvas
  store={canvasStore}
  nodeTypes={customNodeTypes}
  onNodeClick={(node) => console.log('Clicked:', node)}
/>
```

### Props

- `store: Store<NodeCanvasState, NodeCanvasAction>` - Canvas store (required)
- `nodeTypes: Record<string, ComponentType>` - Custom node components (optional)
- `edgeTypes: Record<string, ComponentType>` - Custom edge components (optional)
- `onNodeClick: (node: Node) => void` - Node click handler (optional)
- `onEdgeClick: (edge: Edge) => void` - Edge click handler (optional)
- `class: string` - Custom CSS class (optional)

### State Interface

```typescript
interface NodeCanvasState {
  // Nodes
  nodes: Node[];
  selectedNodes: string[];  // Node IDs

  // Edges
  edges: Edge[];
  selectedEdges: string[];  // Edge IDs

  // Viewport
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };

  // Interaction
  isDragging: boolean;
  isPanning: boolean;

  // Error handling
  error: string | null;
}

interface Node {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: any;
}

interface Edge {
  id: string;
  source: string;  // Node ID
  target: string;  // Node ID
  type?: string;
  data?: any;
}
```

### Actions

```typescript
type NodeCanvasAction =
  // Nodes
  | { type: 'addNode'; node: Node }
  | { type: 'removeNode'; nodeId: string }
  | { type: 'updateNode'; nodeId: string; data: Partial<Node> }
  | { type: 'moveNode'; nodeId: string; position: { x: number; y: number } }
  | { type: 'selectNode'; nodeId: string }
  | { type: 'deselectNode'; nodeId: string }
  | { type: 'clearNodeSelection' }

  // Edges
  | { type: 'addEdge'; edge: Edge }
  | { type: 'removeEdge'; edgeId: string }
  | { type: 'updateEdge'; edgeId: string; data: Partial<Edge> }

  // Viewport
  | { type: 'setViewport'; viewport: Partial<Viewport> }
  | { type: 'zoomIn' }
  | { type: 'zoomOut' }
  | { type: 'fitView' }

  // Error
  | { type: 'errorOccurred'; error: string }
  | { type: 'errorCleared' };
```

### Use Cases

- Visual programming tools
- Flow diagrams
- Workflow builders
- Data pipelines
- State machines
- Architecture diagrams

### Complete Example

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { NodeCanvas, nodeCanvasReducer, createInitialNodeCanvasState } from '@composable-svelte/code';

// Custom node component
import CustomNode from './CustomNode.svelte';

const canvasStore = createStore({
  initialState: createInitialNodeCanvasState({
    nodes: [
      {
        id: '1',
        type: 'input',
        position: { x: 100, y: 100 },
        data: { label: 'Start', value: 0 }
      },
      {
        id: '2',
        type: 'process',
        position: { x: 300, y: 100 },
        data: { label: 'Add 10', operation: 'add', value: 10 }
      },
      {
        id: '3',
        type: 'output',
        position: { x: 500, y: 100 },
        data: { label: 'Result' }
      }
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2' },
      { id: 'e2-3', source: '2', target: '3' }
    ]
  }),
  reducer: nodeCanvasReducer,
  dependencies: {}
});

// Handle node clicks
function handleNodeClick(node: Node) {
  console.log('Node clicked:', node);
  canvasStore.dispatch({ type: 'selectNode', nodeId: node.id });
}

// Handle edge clicks
function handleEdgeClick(edge: Edge) {
  console.log('Edge clicked:', edge);
}
</script>

<div class="canvas-container">
  <NodeCanvas
    store={canvasStore}
    nodeTypes={{ custom: CustomNode }}
    onNodeClick={handleNodeClick}
    onEdgeClick={handleEdgeClick}
  />

  <!-- Controls -->
  <div class="canvas-controls">
    <button onclick={() => canvasStore.dispatch({ type: 'zoomIn' })}>
      Zoom In
    </button>
    <button onclick={() => canvasStore.dispatch({ type: 'zoomOut' })}>
      Zoom Out
    </button>
    <button onclick={() => canvasStore.dispatch({ type: 'fitView' })}>
      Fit View
    </button>
  </div>
</div>

<style>
  .canvas-container {
    width: 100%;
    height: 600px;
    position: relative;
  }

  .canvas-controls {
    position: absolute;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 8px;
  }
</style>
```

---

## COMPONENT SELECTION GUIDE

**When to use each component**:

**CodeEditor**:
- User edits code
- Autocomplete needed
- Syntax checking required
- Save functionality required

**CodeHighlight**:
- Display-only code
- Documentation examples
- Fast rendering for many snippets

**NodeCanvas**:
- Visual programming
- Workflow editors
- Diagram builders
- Data pipeline visualization

---

## CROSS-REFERENCES

**Related Skills**:
- **composable-svelte-core**: Store, reducer, Effect system, TestStore
- **composable-svelte-media**: Audio/video playback (AudioPlayer, VideoEmbed, VoiceInput)
- **composable-svelte-chat**: Real-time communication (StreamingChat)
- **composable-svelte-components**: UI components (Button, Input, etc.)
- **composable-svelte-testing**: TestStore for testing reducers

**When to Use Each Package**:
- **code**: Code editors, syntax highlighting, visual programming
- **media**: Audio players, video embeds, voice input
- **chat**: Real-time chat, streaming responses
- **graphics**: 3D scenes, WebGPU/WebGL rendering
- **charts**: 2D data visualization
- **maps**: Geospatial data

---

## PERFORMANCE CONSIDERATIONS

**CodeEditor**:
- Heavy component (CodeMirror bundle ~300KB)
- Use CodeHighlight for display-only snippets
- Lazy load for better initial page load

**NodeCanvas**:
- Heavy component (SvelteFlow bundle ~200KB)
- Limit number of nodes for performance (< 1000 recommended)
- Use virtualization for large graphs
- Disable animations for large graphs

---

## TESTING PATTERNS

### CodeEditor Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { codeEditorReducer, createInitialState } from '@composable-svelte/code';

const store = new TestStore({
  initialState: createInitialState({ value: '' }),
  reducer: codeEditorReducer,
  dependencies: {
    onSave: vi.fn(),
    formatter: vi.fn((code) => Promise.resolve(code))
  }
});

// Test value change
await store.send({
  type: 'valueChanged',
  value: 'console.log("test");'
}, (state) => {
  expect(state.value).toBe('console.log("test");');
  expect(state.hasUnsavedChanges).toBe(true);
});

// Test save
await store.send({ type: 'save' });
await store.receive({ type: 'saved', value: 'console.log("test");' }, (state) => {
  expect(state.hasUnsavedChanges).toBe(false);
  expect(state.lastSavedValue).toBe('console.log("test");');
});
```

### NodeCanvas Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { nodeCanvasReducer, createInitialNodeCanvasState } from '@composable-svelte/code';

const store = new TestStore({
  initialState: createInitialNodeCanvasState({
    nodes: [],
    edges: []
  }),
  reducer: nodeCanvasReducer,
  dependencies: {}
});

// Test add node
await store.send({
  type: 'addNode',
  node: {
    id: '1',
    type: 'input',
    position: { x: 100, y: 100 },
    data: { label: 'Test' }
  }
}, (state) => {
  expect(state.nodes.length).toBe(1);
  expect(state.nodes[0].id).toBe('1');
});

// Test add edge
await store.send({
  type: 'addEdge',
  edge: { id: 'e1-2', source: '1', target: '2' }
}, (state) => {
  expect(state.edges.length).toBe(1);
});
```

---

## TROUBLESHOOTING

**CodeEditor not rendering**:
- Check CodeMirror peer dependency installed
- Verify store created with `codeEditorReducer`
- Ensure container has height set

**NodeCanvas performance issues**:
- Limit number of nodes (< 1000 recommended)
- Use simpler custom node components
- Disable animations for large graphs

**CodeHighlight language not recognized**:
- Check language name matches Prism.js language keys
- Ensure Prism.js language pack is loaded
- Verify syntax highlighting CSS is included
