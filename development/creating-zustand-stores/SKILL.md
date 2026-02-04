---
name: creating-zustand-stores
description: Creating Zustand stores for StickerNest state management. Use when the user asks to create a store, add state management, build a new store, manage global state, persist state, or add new application state. Covers store structure, persist middleware, devtools, selectors, and actions.
---

# Creating Zustand Stores for StickerNest

This skill covers creating Zustand stores following StickerNest's established patterns, including TypeScript types, middleware configuration, selectors, and actions.

## Store Location

All stores are located in `src/state/`. Follow the naming convention `use{Feature}Store.ts`.

---

## Basic Store Template

```typescript
// src/state/useMyFeatureStore.ts

/**
 * StickerNest v2 - My Feature Store (Zustand)
 * Brief description of what this store manages
 */

import { create } from 'zustand';

// ==================
// Types
// ==================

/** Feature item type */
export interface MyItem {
  id: string;
  name: string;
  value: number;
  createdAt: string;
}

// ==================
// Store State
// ==================

export interface MyFeatureState {
  /** List of items */
  items: MyItem[];
  /** Currently selected item ID */
  selectedId: string | null;
  /** Loading state */
  isLoading: boolean;
  /** Error message if any */
  error: string | null;
}

// ==================
// Store Actions
// ==================

export interface MyFeatureActions {
  /** Add a new item */
  addItem: (item: Omit<MyItem, 'id' | 'createdAt'>) => void;
  /** Remove an item by ID */
  removeItem: (id: string) => void;
  /** Update an existing item */
  updateItem: (id: string, updates: Partial<MyItem>) => void;
  /** Select an item */
  selectItem: (id: string | null) => void;
  /** Set loading state */
  setLoading: (loading: boolean) => void;
  /** Set error state */
  setError: (error: string | null) => void;
  /** Reset store to initial state */
  reset: () => void;
}

// ==================
// Initial State
// ==================

const initialState: MyFeatureState = {
  items: [],
  selectedId: null,
  isLoading: false,
  error: null,
};

// ==================
// Store Creation
// ==================

export const useMyFeatureStore = create<MyFeatureState & MyFeatureActions>()(
  (set, get) => ({
    ...initialState,

    addItem: (item) => {
      const newItem: MyItem = {
        ...item,
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
      };
      set((state) => ({
        items: [...state.items, newItem],
      }));
    },

    removeItem: (id) => {
      set((state) => ({
        items: state.items.filter((item) => item.id !== id),
        selectedId: state.selectedId === id ? null : state.selectedId,
      }));
    },

    updateItem: (id, updates) => {
      set((state) => ({
        items: state.items.map((item) =>
          item.id === id ? { ...item, ...updates } : item
        ),
      }));
    },

    selectItem: (id) => {
      set({ selectedId: id });
    },

    setLoading: (isLoading) => {
      set({ isLoading });
    },

    setError: (error) => {
      set({ error });
    },

    reset: () => {
      set(initialState);
    },
  })
);

// ==================
// Selector Hooks
// ==================

export const useMyItems = () => useMyFeatureStore((state) => state.items);
export const useSelectedItemId = () => useMyFeatureStore((state) => state.selectedId);
export const useSelectedItem = () =>
  useMyFeatureStore((state) =>
    state.items.find((item) => item.id === state.selectedId)
  );
export const useMyFeatureLoading = () => useMyFeatureStore((state) => state.isLoading);
export const useMyFeatureError = () => useMyFeatureStore((state) => state.error);
```

---

## Store with Persist Middleware

For stores that should persist data to localStorage:

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useMyFeatureStore = create<MyFeatureState & MyFeatureActions>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Actions...
    }),
    {
      name: 'my-feature-store', // localStorage key
      storage: createJSONStorage(() => localStorage),

      // Optional: Only persist certain fields
      partialize: (state) => ({
        items: state.items,
        // Don't persist: isLoading, error, selectedId
      }),

      // Optional: Version for migrations
      version: 1,

      // Optional: Migration function
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migrate from v0 to v1
          return {
            ...persistedState,
            // Add new fields or transform data
          };
        }
        return persistedState;
      },
    }
  )
);
```

---

## Store with Devtools Middleware

For debugging with Redux DevTools:

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export const useMyFeatureStore = create<MyFeatureState & MyFeatureActions>()(
  devtools(
    (set, get) => ({
      ...initialState,

      addItem: (item) => {
        set(
          (state) => ({
            items: [...state.items, { ...item, id: crypto.randomUUID() }],
          }),
          false, // replace: false (merge)
          'addItem' // Action name for devtools
        );
      },

      // Other actions...
    }),
    {
      name: 'MyFeatureStore', // Store name in devtools
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

---

## Combined Persist + Devtools

```typescript
import { create } from 'zustand';
import { persist, devtools, createJSONStorage } from 'zustand/middleware';

export const useMyFeatureStore = create<MyFeatureState & MyFeatureActions>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,
        // Actions...
      }),
      {
        name: 'my-feature-store',
        storage: createJSONStorage(() => localStorage),
      }
    ),
    {
      name: 'MyFeatureStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

---

## Common Patterns

### Map-based State (for entities)

```typescript
export interface EntityState {
  entities: Map<string, Entity>;
}

export interface EntityActions {
  addEntity: (entity: Entity) => void;
  removeEntity: (id: string) => void;
  getEntity: (id: string) => Entity | undefined;
}

export const useEntityStore = create<EntityState & EntityActions>()(
  (set, get) => ({
    entities: new Map(),

    addEntity: (entity) => {
      set((state) => ({
        entities: new Map(state.entities).set(entity.id, entity),
      }));
    },

    removeEntity: (id) => {
      set((state) => {
        const newEntities = new Map(state.entities);
        newEntities.delete(id);
        return { entities: newEntities };
      });
    },

    getEntity: (id) => {
      return get().entities.get(id);
    },
  })
);
```

### Nested State Updates

```typescript
export interface NestedState {
  settings: {
    appearance: {
      theme: 'light' | 'dark';
      fontSize: number;
    };
    behavior: {
      autoSave: boolean;
      notifications: boolean;
    };
  };
}

export interface NestedActions {
  setTheme: (theme: 'light' | 'dark') => void;
  setFontSize: (size: number) => void;
  toggleAutoSave: () => void;
}

export const useSettingsStore = create<NestedState & NestedActions>()(
  (set, get) => ({
    settings: {
      appearance: { theme: 'dark', fontSize: 14 },
      behavior: { autoSave: true, notifications: true },
    },

    setTheme: (theme) => {
      set((state) => ({
        settings: {
          ...state.settings,
          appearance: {
            ...state.settings.appearance,
            theme,
          },
        },
      }));
    },

    setFontSize: (fontSize) => {
      set((state) => ({
        settings: {
          ...state.settings,
          appearance: {
            ...state.settings.appearance,
            fontSize,
          },
        },
      }));
    },

    toggleAutoSave: () => {
      set((state) => ({
        settings: {
          ...state.settings,
          behavior: {
            ...state.settings.behavior,
            autoSave: !state.settings.behavior.autoSave,
          },
        },
      }));
    },
  })
);
```

### Async Actions

```typescript
export interface AsyncState {
  data: DataType | null;
  isLoading: boolean;
  error: string | null;
}

export interface AsyncActions {
  fetchData: () => Promise<void>;
  saveData: (data: DataType) => Promise<void>;
}

export const useAsyncStore = create<AsyncState & AsyncActions>()(
  (set, get) => ({
    data: null,
    isLoading: false,
    error: null,

    fetchData: async () => {
      set({ isLoading: true, error: null });
      try {
        const response = await fetch('/api/data');
        const data = await response.json();
        set({ data, isLoading: false });
      } catch (err) {
        set({
          error: err instanceof Error ? err.message : 'Unknown error',
          isLoading: false,
        });
      }
    },

    saveData: async (data) => {
      set({ isLoading: true, error: null });
      try {
        await fetch('/api/data', {
          method: 'POST',
          body: JSON.stringify(data),
        });
        set({ data, isLoading: false });
      } catch (err) {
        set({
          error: err instanceof Error ? err.message : 'Unknown error',
          isLoading: false,
        });
      }
    },
  })
);
```

### Computed Values (Derived State)

```typescript
export interface ComputedState {
  items: Item[];
  filter: string;
}

export interface ComputedActions {
  setFilter: (filter: string) => void;
  addItem: (item: Item) => void;
}

// Selectors for computed values
export const useFilteredItems = () =>
  useComputedStore((state) => {
    const { items, filter } = state;
    if (!filter) return items;
    return items.filter((item) =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  });

export const useItemCount = () =>
  useComputedStore((state) => state.items.length);

export const useHasItems = () =>
  useComputedStore((state) => state.items.length > 0);
```

---

## Subscribing to Store Changes

```typescript
// Subscribe to all changes
const unsubscribe = useMyFeatureStore.subscribe((state) => {
  console.log('State changed:', state);
});

// Subscribe to specific slice
const unsubscribe = useMyFeatureStore.subscribe(
  (state) => state.selectedId,
  (selectedId) => {
    console.log('Selected ID changed:', selectedId);
  }
);

// Don't forget to unsubscribe
unsubscribe();
```

---

## Testing Stores

```typescript
// src/state/useMyFeatureStore.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { useMyFeatureStore } from './useMyFeatureStore';

describe('useMyFeatureStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useMyFeatureStore.getState().reset();
  });

  it('should add item', () => {
    const { addItem } = useMyFeatureStore.getState();

    addItem({ name: 'Test', value: 42 });

    const { items } = useMyFeatureStore.getState();
    expect(items).toHaveLength(1);
    expect(items[0].name).toBe('Test');
    expect(items[0].value).toBe(42);
    expect(items[0].id).toBeDefined();
  });

  it('should remove item', () => {
    const { addItem, removeItem } = useMyFeatureStore.getState();

    addItem({ name: 'Test', value: 42 });
    const { items: itemsAfterAdd } = useMyFeatureStore.getState();
    const itemId = itemsAfterAdd[0].id;

    removeItem(itemId);

    const { items } = useMyFeatureStore.getState();
    expect(items).toHaveLength(0);
  });

  it('should update item', () => {
    const { addItem, updateItem } = useMyFeatureStore.getState();

    addItem({ name: 'Test', value: 42 });
    const { items: itemsAfterAdd } = useMyFeatureStore.getState();
    const itemId = itemsAfterAdd[0].id;

    updateItem(itemId, { value: 100 });

    const { items } = useMyFeatureStore.getState();
    expect(items[0].value).toBe(100);
    expect(items[0].name).toBe('Test'); // Unchanged
  });

  it('should select item', () => {
    const { addItem, selectItem } = useMyFeatureStore.getState();

    addItem({ name: 'Test', value: 42 });
    const { items } = useMyFeatureStore.getState();

    selectItem(items[0].id);

    const { selectedId } = useMyFeatureStore.getState();
    expect(selectedId).toBe(items[0].id);
  });
});
```

---

## Existing Stores Reference

| Store | File | Purpose |
|-------|------|---------|
| `useCanvasStore` | `useCanvasStore.ts` | Canvas state, widgets, selection |
| `useLibraryStore` | `useLibraryStore.ts` | Widget library, search, filters |
| `usePanelsStore` | `usePanelsStore.ts` | Panel visibility and positions |
| `useToolStore` | `useToolStore.ts` | Active tools and defaults |
| `useThemeStore` | `useThemeStore.ts` | Theme settings |
| `useStickerStore` | `useStickerStore.ts` | Sticker/asset management |
| `useApiSettingsStore` | `useApiSettingsStore.ts` | API configuration |
| `useAssetStore` | `useAssetStore.ts` | Asset management |
| `useSelectionStore` | `useSelectionStore.ts` | Selection state |
| `useSlotStore` | `useSlotStore.ts` | Skin slot management |
| `useSkinStore` | `useSkinStore.ts` | Skin management |
| `useCanvasExtendedStore` | `useCanvasExtendedStore.ts` | Extended viewport state |
| `useRuntimeStore` | `useRuntimeStore.ts` | Runtime state |
| `useCanvasRouterStore` | `useCanvasRouterStore.ts` | Canvas routing |
| `entityStore` | `entityStore.ts` | Entity management |

---

## Best Practices

1. **Keep stores focused** - One store per feature/domain
2. **Use TypeScript** - Define interfaces for state and actions
3. **Separate state and actions** - Makes types clearer
4. **Create selector hooks** - For common access patterns
5. **Use persist sparingly** - Only for data that must survive refresh
6. **Include a reset action** - For testing and cleanup
7. **Use devtools in development** - For debugging
8. **Avoid storing derived data** - Compute in selectors instead
