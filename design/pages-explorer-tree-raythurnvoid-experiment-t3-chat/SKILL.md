---
name: pages-explorer-tree
description: Complete implementation guide for the DocsSidebar v2 (React Complex Tree + Convex + Liveblocks + AI).
---

# Overview

Complete implementation guide for the React Complex Tree sidebar with Convex, Liveblocks, and AI features.

# DocsSidebar v2 - Complete Implementation Guide

## Overview

The DocsSidebar v2 component is a sophisticated Notion-like file explorer for an AI-powered document management system. It integrates React Complex Tree with Convex (backend), Liveblocks (real-time collaboration), shadcn/ui (UI components), and AI features for document generation and enhancement.

## Architecture Stack

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│  React Complex Tree + shadcn/ui + Tailwind CSS          │
├─────────────────────────────────────────────────────────┤
│                  State Management                       │
│              DocsSearchContext                          │
├─────────────────────────────────────────────────────────┤
│                 Real-time Collaboration                 │
│         Liveblocks (Yjs + TipTap Editor)                │
├─────────────────────────────────────────────────────────┤
│                   Data Persistence                      │
│          Convex (Database + HTTP Actions)               │
├─────────────────────────────────────────────────────────┤
│                    AI Integration                       │
│        Novel Editor + Contextual AI Prompts             │
└─────────────────────────────────────────────────────────┘
```

## Core Implementation Files

### 1. Main Component (`../../../packages/app/src/components/docs-sidebar-v2.tsx`)

The main sidebar component with the following structure:

```typescript
export function DocsSidebar(props: DocsSidebar_Props) {
  return (
    <SidebarProvider>
      <DocsSearchContextProvider>
        <Sidebar>
          <DocsSidebarContent>
            <SidebarHeader /> // Search, controls, multi-selection
            <SidebarContent>
              <TreeArea /> // React Complex Tree implementation
            </SidebarContent>
          </DocsSidebarContent>
        </Sidebar>
      </DocsSearchContextProvider>
    </SidebarProvider>
  );
}
```

### 2. Data Store (`../../../packages/app/src/stores/docs-store.ts`)

Manages document data:

```typescript
// Document data structure
interface DocData {
	id: string;
	title: string;
	type: "folder" | "document" | "placeholder";
	content?: string; // HTML content for TipTap editor
}

// Custom data provider
class PagesSidebarTreeDataProvider implements TreeDataProvider<DocData> {
	// Handles all tree operations with automatic sorting
	// Manages placeholder items for empty folders
	// Notifies listeners of tree changes
}
```

### 3. Convex Backend (`../../../packages/app/convex/ai_docs_temp.ts`)

Backend integration for persistence and AI:

```typescript
// Database schema
const schema = defineSchema({
	docs_yjs: defineTable({
		roomId: v.string(),
		content: v.bytes(), // Yjs document state
		orgId: v.string(),
		projectId: v.string(),
		docId: v.string(),
	}).index("by_room_id", ["roomId"]),
});

// HTTP actions
export const ai_docs_temp_liveblocks_auth; // JWT auth for Liveblocks
export const ai_docs_temp_contextual_prompt; // AI generation endpoint
export const ai_docs_temp_liveblocks_webhook; // Persistence webhook

// Mutations
export const ai_docs_temp_upsert_yjs_document; // Save document changes
```

## React Complex Tree Integration Details

### Configuration

The UncontrolledTreeEnvironment is configured with specific patterns for Notion-like behavior:

```typescript
<UncontrolledTreeEnvironment
  // Data management
  dataProvider={dataProvider} // Stable instance via useMemo
  getItemTitle={(item) => item.data.title}

  // Interaction modes
  defaultInteractionMode={InteractionMode.ClickArrowToExpand}
  // Arrow expands/collapses, title click selects only (VSCode-like)

  // Drag & drop configuration
  canDragAndDrop={true}
  canDropOnFolder={true}
  canDropOnNonFolder={true} // All items can receive drops
  canReorderItems={true}
  canDropBelowOpenFolders={false}

  // Custom filtering for search
  shouldRenderChildren={handleShouldRenderChildren}

  // Selection handling
  onPrimaryAction={handlePrimaryAction}
  onSelectItems={handleSelectItems}

  // Custom rendering
  renderItem={(props) => <TreeItem {...props} />}
  renderItemArrow={(props) => <TreeItemArrow {...props} />}
  renderRenameInput={(props) => <PagesSidebarTreeRenameInput {...props} />}
/>
```

### Custom Data Provider Implementation

The PagesSidebarTreeDataProvider extends TreeDataProvider with critical features:

1. **Automatic Alphabetical Sorting**: All children arrays are sorted on every change
2. **Placeholder System**: Empty folders automatically get "No files inside" placeholder
3. **Real-time Updates**: Uses listener pattern to notify tree of changes
4. **CRUD Operations**: Create, rename, move with proper parent-child relationship management

```typescript
class PagesSidebarTreeDataProvider implements TreeDataProvider<DocData> {
	private data: Record<TreeItemIndex, TreeItem<DocData>>;
	private treeChangeListeners: ((changedItemIds: TreeItemIndex[]) => void)[] = [];

	async onChangeItemChildren(itemId: TreeItemIndex, newChildren: TreeItemIndex[]): Promise<void> {
		// Sort children alphabetically
		const sortedChildren = this.sortChildren(newChildren);

		// Update data
		this.data[itemId] = {
			...this.data[itemId],
			children: sortedChildren,
		};

		// Notify listeners
		this.notifyTreeChange([itemId]);
	}

	createNewItem(parentId: string, title: string, type: "document" | "folder"): string {
		const newId = `${type}-${Date.now()}`;

		// Create item with placeholder if it's a folder
		this.data[newId] = {
			index: newId,
			isFolder: true, // All items are foldable
			children: [`${newId}-placeholder`],
			data: { id: newId, title, type },
			canMove: true,
			canRename: true,
		};

		// Update parent's children
		this.updateParentChildren(parentId, newId);

		return newId;
	}
}
```

## Advanced Features Implementation

### 1. Drag & Drop to Root Area

By default, React Complex Tree doesn't support dropping items directly onto the root area (empty space). We implemented a custom solution:

```typescript
function TreeArea() {
  const rootElement = useRef<HTMLDivElement>(null);
  const [isDraggingOverRootArea, setIsDraggingOverRootArea] = useState(false);

  const handleDropOnRootArea = async (e: React.DragEvent<HTMLDivElement>) => {
    if (e.target !== rootElement.current) return;

    // Get dragging items from react-complex-tree's internal context
    const draggingItems = treeRef.current?.dragAndDropContext.draggingItems;
    if (!draggingItems) return;

    // Use the tree's live state as source of truth
    const currentItems = treeRef.current?.treeEnvironmentContext.items || {};

    // Follow same pattern as library's internal drop handling
    const promises: Promise<void>[] = [];

    // Step 1: Remove items from old parents
    for (const item of draggingItems) {
      const parent = Object.values(currentItems).find(
        p => p?.children?.includes(item.index)
      );

      if (parent && parent.index !== ROOT_TREE_ID) {
        promises.push(
          dataProvider.onChangeItemChildren(
            parent.index,
            parent.children.filter(c => c !== item.index)
          )
        );
      }
    }

    // Step 2: Add items to root
    const itemIds = draggingItems.map(item => item.index);
    promises.push(
      dataProvider.onChangeItemChildren(ROOT_TREE_ID, [
        ...currentItems[ROOT_TREE_ID].children.filter(i => !itemIds.includes(i)),
        ...itemIds
      ])
    );

    await Promise.all(promises);
  };

  return (
    <div
      ref={rootElement}
      className={cn(
        "DocsSidebar-tree-area",
        isDraggingOverRootArea && "DocsSidebar-tree-area-drag-over"
      )}
      onDragOver={handleDragOverRootArea}
      onDrop={handleDropOnRootArea}
    >
      <UncontrolledTreeEnvironment>
        <Tree />
      </UncontrolledTreeEnvironment>
    </div>
  );
}
```

### 2. Archive System

Archive functionality with visual indicators and bulk operations:

```typescript
// Context state
const [archivedItems, setArchivedItems] = useState<Set<string>>(new Set());
const [showArchived, setShowArchived] = useState(false);

// In TreeItem component
if (isArchived && !showArchived) {
  return null; // Hide archived items
}

// Visual indicators
className={cn(
  isArchived && "line-through opacity-60"
)}

// Bulk operations for multi-selection
const handleArchiveAll = () => {
  const newArchivedSet = new Set(archivedItems);
  selectedItemIds.forEach(id => newArchivedSet.add(id));
  setArchivedItems(newArchivedSet);
  treeRef.current?.selectItems([]); // Clear selection
};
```

### 3. Search Implementation

Real-time search with hierarchical filtering:

```typescript
const handleShouldRenderChildren: TypedUncontrolledTreeEnvironmentProps["shouldRenderChildren"] = (item, context) => {
	// Default expansion check
	const defaultShouldRender = item.isFolder && context.isExpanded;
	if (!defaultShouldRender) return false;

	// Placeholder items always render if expanded
	if (item.data.type === "placeholder") return true;

	// Search filtering
	if (searchQuery.trim() && item.children) {
		const hasVisibleChildren = item.children.some((childId) => {
			const child = dataProvider.getAllData()[childId];
			return child?.data.title.toLowerCase().includes(searchQuery.toLowerCase());
		});
		return hasVisibleChildren;
	}

	return defaultShouldRender;
};
```

### 4. Multi-Selection Features

Selection counter with batch operations:

```typescript
// Track selection
const [multiSelectionCount, setMultiSelectionCount] = useState(0);
const [selectedItemIds, setSelectedItemIds] = useState<string[]>([]);

// Selection counter UI
{multiSelectionCount > 1 && (
  <div className="DocsSidebar-selection-counter">
    <span>{multiSelectionCount} items selected</span>
    <IconButton onClick={handleArchiveAll} tooltip="Archive all">
      <Archive />
    </IconButton>
    <IconButton onClick={handleClearSelection} tooltip="Clear">
      <X />
    </IconButton>
  </div>
)}
```

## Liveblocks Integration

Real-time collaboration setup:

```typescript
// Room ID pattern: orgId:projectId:docId
const roomId = `${orgId}:${projectId}:${selectedDocId}`;

// JWT Authentication
const authEndpoint = `${CONVEX_URL}/api/ai-docs-temp/liveblocks-auth`;

// Webhook for persistence
const webhook = `${CONVEX_URL}/api/ai-docs-temp/liveblocks-webhook`;

// TipTap editor with Liveblocks
<LiveblocksRoomProvider roomId={roomId}>
  <TipTapEditor
    extensions={[LiveblocksYjsExtension]}
    initialContent={documentContent}
  />
</LiveblocksRoomProvider>
```

## AI Features Integration

### 1. Contextual AI Prompts

The editor supports multiple AI operations:

```typescript
const AI_OPERATIONS = {
  continue: "Continue writing from the current position",
  improve: "Improve the selected text",
  shorter: "Make the text shorter",
  longer: "Make the text longer",
  fix: "Fix grammar and spelling",
  zap: "Custom command-based generation"
};

// AI resolver in editor
ai: {
  name: "Claude",
  resolveContextualPrompt: async ({ prompt, context, previous }) => {
    const response = await fetch(`${CONVEX_URL}/api/ai-docs-temp/contextual-prompt`, {
      method: "POST",
      body: JSON.stringify({ prompt, context, previous })
    });
    return response.json();
  }
}
```

### 2. Document Generation

AI can generate new documents or sections based on prompts, with the generated content immediately synced via Liveblocks to all users.

## Styling System

### CSS Architecture (`docs-sidebar-v2.css`)

```css
/* Grid layout for tree items with action buttons */
.DocsSidebar-tree-item-content {
	display: grid;
	grid-template-columns: 1fr auto;
	grid-template-rows: 32px 32px;
}

/* Dynamic indentation using CSS variables */
.DocsSidebar-tree-item-main-row {
	padding-left: calc(var(--DocsSidebar-tree-item-content-depth) * 16px);
}

/* Action buttons on second row */
.DocsSidebar-tree-item-actions {
	grid-column: 1 / -1;
	grid-row: 2;
	padding-left: calc(var(--DocsSidebar-tree-item-content-depth) * 16px + 32px);
}
```

### Tailwind Integration

Uses `cn()` utility for conditional classes:

```typescript
className={cn(
  "base-classes",
  isSelected && "selected-classes",
  isDraggingOver && "drag-over-classes",
  isArchived && "archived-classes"
)}
```

## Critical Implementation Rules

### ⚠️ NEVER Violate These Patterns

1. **Hook Usage in renderItem**

   ```typescript
   // ❌ WRONG - Will crash
   renderItem={({ item }) => {
     const id = useId(); // CRASH!
   }}

   // ✅ CORRECT - Extract to component
   function TreeItem(props) {
     const id = useId(); // Safe
     return <li>...</li>;
   }
   renderItem={(props) => <TreeItem {...props} />}
   ```

2. **Data Provider Stability**

   ```typescript
   // ❌ WRONG - Recreates every render
   const dataProvider = new PagesSidebarTreeDataProvider(data);

   // ✅ CORRECT - Stable instance
   const dataProvider = useMemo(() => {
   	const provider = new PagesSidebarTreeDataProvider(data);
   	dataProviderRef.current = provider;
   	return provider;
   }, []); // Empty deps
   ```

3. **Selection Management**

   ```typescript
   // ❌ WRONG - Custom click handlers
   <button onClick={() => setSelectedId(item.id)}>

   // ✅ CORRECT - Use library callbacks
   onSelectItems={(items) => handleSelection(items)}
   ```

## Performance Optimizations

1. **Memoized Computations**: Expensive operations cached with useMemo
2. **Stable References**: Data provider and handlers have stable identities
3. **Efficient Filtering**: Uses shouldRenderChildren for structural filtering
4. **Lazy Loading**: TipTap editor loaded dynamically
5. **Batch Updates**: Multiple tree operations batched together

## Testing Considerations

When modifying the sidebar:

1. **Test drag & drop** to root area and between folders
2. **Verify search** filters correctly with nested items
3. **Check archive** functionality with multi-selection
4. **Ensure placeholders** appear/disappear correctly
5. **Validate sorting** maintains alphabetical order
6. **Test real-time sync** with multiple users
7. **Verify AI features** generate and insert content properly

## Extension Points

The architecture supports future enhancements:

1. **Custom node types**: Add new document types via DocData.type
2. **Additional AI operations**: Extend contextual prompts
3. **New actions**: Add buttons to TreeItem component
4. **Enhanced search**: Implement content-based search
5. **Permissions**: Add access control to tree operations
6. **Version history**: Track document changes over time

This implementation provides a production-ready, enterprise-grade document management system with sophisticated file organization, real-time collaboration, and AI assistance capabilities.
