---
name: boardkit-architecture
description: |
  Boardkit monorepo architecture: package boundaries, module system, registries, stores.
  Use when planning refactors, adding features, or understanding system boundaries.
allowed-tools: Read, Grep, Glob
---

# Boardkit Architecture

## Package Structure

```
packages/
├── core/          @boardkit/core
│   ├── src/types/           → Document, Module, Action, DataContract
│   ├── src/stores/          → boardStore, toolStore (Pinia)
│   ├── src/actions/         → coreActions, ActionRegistry
│   ├── src/modules/         → ModuleRegistry, defineModule
│   └── src/migrations/      → Document migrations (v0→v1→v2)
│
├── ui/            @boardkit/ui
│   ├── src/components/      → 28 reusable components
│   ├── DESIGN_SYSTEM.md     → Complete DS spec
│   └── uno.config.ts        → UnoCSS tokens
│
├── platform/      @boardkit/platform
│   └── src/storage/         → IndexedDB adapter, Tauri FS adapter
│
└── app-common/    @boardkit/app-common
    ├── src/modules/         → Shared modules (Text, Todo, TaskRadar, FocusLens)
    └── src/composables/     → Shared composables

apps/
├── web/           → PWA (Vite + Vue 3)
└── desktop/       → Tauri macOS app
```

## Boundaries (STRICT)

| Package | Can import | Cannot import |
|---------|------------|---------------|
| core | Nothing | ui, platform, apps |
| ui | core (types only) | platform, apps |
| platform | core (types only) | ui, apps |
| app-common | core, ui | platform, apps |
| apps | Everything | Each other |

## Registries (Singletons)

```typescript
// ModuleRegistry - widget definitions
ModuleRegistry.register(todoModule)
ModuleRegistry.get('todo') // → ModuleDefinition

// ActionRegistry - user actions
ActionRegistry.register({ id: 'duplicate', ... })
ActionRegistry.execute('duplicate')

// DataContractRegistry - data sharing contracts
DataContractRegistry.register('boardkit.todo.v1', schema)

// DataBus - runtime pub/sub
DataBus.publish('boardkit.todo.v1', data)
DataBus.subscribe('boardkit.todo.v1', callback)
```

## Stores (Pinia)

```typescript
// boardStore - document state
boardStore.widgets        // Widget[]
boardStore.elements       // CanvasElement[]
boardStore.selectedIds    // Set<string>
boardStore.viewport       // { x, y, zoom }
boardStore.isDirty        // boolean
boardStore.addWidget(module, position)
boardStore.updateWidgetState(id, state)

// toolStore - tool state
toolStore.activeTool      // 'select' | 'hand' | 'rectangle' | ...
toolStore.isDrawing       // boolean
toolStore.setTool(tool)
```

## Document Schema (v2)

```typescript
interface BoardkitDocument {
  version: 2
  meta: { title, createdAt, updatedAt }
  board: {
    viewport: { x, y, zoom }
    widgets: Widget[]
    elements: CanvasElement[]
    background: BoardBackground
  }
  modules: Record<string, unknown>
  dataSharing?: { permissions[], links[] }
}
```

## Module System

```typescript
const myModule = defineModule<MyState>({
  id: 'my-module',
  displayName: 'My Module',
  icon: 'box',
  category: 'productivity',
  defaultWidth: 300,
  defaultHeight: 200,
  minWidth: 200,
  minHeight: 150,
  defaultState: () => ({ items: [] }),
  serialize: (state) => state,
  deserialize: (data) => data as MyState,
  component: () => import('./MyWidget.vue')
})
```

## Key Files

| Purpose | Path |
|---------|------|
| Document types | `packages/core/src/types/document.ts` |
| Module types | `packages/core/src/types/module.ts` |
| Action types | `packages/core/src/types/action.ts` |
| Board store | `packages/core/src/stores/boardStore.ts` |
| Migrations | `packages/core/src/migrations/index.ts` |
| Tests | `packages/core/__tests__/` |
