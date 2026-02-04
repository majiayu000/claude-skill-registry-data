---
name: frontend-patterns
description: >
  CRITICAL: Use this skill when creating/debugging React UI components, Radix UI, forms, modals, or drag & drop.

  AUTO-ACTIVATE when user mentions (FR/EN):
  - select, Select, SelectValue, SelectItem, Radix
  - modal, modale, dialog, Dialog, DialogContent
  - form, formulaire, validation, Zod, React Hook Form, shadcn
  - drag, drop, DnD, @dnd-kit, sortable, réordonner
  - UI bug, composant, component, affiche ID, shows ID, undefined
  - Button, Input, Label, Checkbox, Switch, Badge, Card
  - créer composant, create component, nouveau composant

  This skill contains TESTED patterns for Radix UI Select (ID vs Name), Modal CRUD templates,
  Drag & Drop with @dnd-kit, Form validation with Zod + shadcn/ui Form.
---

# Frontend Patterns - Mathildanesth UI Components

**Stack**: React 18, Next.js 15, Radix UI, Zustand, @dnd-kit, shadcn/ui
**Purpose**: Reusable patterns to avoid recurring UI bugs

---

## 🎯 Problems Solved

### ❌ Bugs Without This Guide
```tsx
// ❌ BUG 1: Select displays IDs instead of names
<SelectValue placeholder="Select site" />
// Shows: "site-123-abc" instead of "Clinique Mathilde"

// ❌ BUG 2: Modal doesn't reset state after close
const [isOpen, setIsOpen] = useState(false);
// Open, close, reopen → old content still visible

// ❌ BUG 3: Inconsistent form validation
if (!name || name === '') { ... }  // Repeated 15 times
```

---

## ✅ PATTERN 1: Radix UI Select (ID vs Name)

### The Problem
**Symptom**: Select shows technical ID ("site-123") instead of display name ("Clinique Mathilde")

**Root Cause**: `SelectValue` with only `placeholder` doesn't handle displaying value when `value` is ID.

### ✅ Correct Pattern (Tested & Validated)

```tsx
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';

interface Site {
  id: string;
  name: string;
}

// ✅ COMPLETE PATTERN
<Select value={selectedSiteId} onValueChange={setSelectedSiteId}>
  <SelectTrigger>
    <SelectValue>
      {selectedSiteId
        ? sites.find(s => s.id === selectedSiteId)?.name || 'Site selected'
        : 'Select a site'}
    </SelectValue>
  </SelectTrigger>
  <SelectContent>
    {sites.map(site => (
      <SelectItem key={site.id} value={site.id}>
        {site.name}
      </SelectItem>
    ))}
  </SelectContent>
</Select>
```

**Files**: `src/app/admin/views/SitesView.tsx:1234, 1328, 1542, 1651, 893`

---

## ✅ PATTERN 2: Modal CRUD Templates

### General Pattern: State & Handlers

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useState } from 'react';

// ✅ Separate states for create and edit
const [createDialogOpen, setCreateDialogOpen] = useState(false);
const [editDialogOpen, setEditDialogOpen] = useState(false);
const [editingItem, setEditingItem] = useState<Item | null>(null);

// Form states
const [newItemName, setNewItemName] = useState('');
const [newItemDescription, setNewItemDescription] = useState('');

// ✅ Reset states on close
const handleCloseCreate = () => {
  setCreateDialogOpen(false);
  setNewItemName('');
  setNewItemDescription('');
};

const handleCloseEdit = () => {
  setEditDialogOpen(false);
  setEditingItem(null);
  setNewItemName('');
  setNewItemDescription('');
};
```

### Template: Create Modal

```tsx
{/* ✅ CREATE MODAL */}
<Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
  <DialogContent className="sm:max-w-[500px]">
    <DialogHeader>
      <DialogTitle>Create new item</DialogTitle>
    </DialogHeader>
    <div className="space-y-4 py-4">
      <div>
        <Label htmlFor="item-name">Name *</Label>
        <Input
          id="item-name"
          value={newItemName}
          onChange={(e) => setNewItemName(e.target.value)}
          placeholder="Enter name..."
          required
        />
      </div>
    </div>

    <div className="flex justify-end gap-2">
      <Button variant="outline" onClick={handleCloseCreate}>
        Cancel
      </Button>
      <Button onClick={handleCreateItem} disabled={!newItemName.trim()}>
        Create
      </Button>
    </div>
  </DialogContent>
</Dialog>
```

**Handler**:
```tsx
const handleCreateItem = async () => {
  try {
    const response = await fetch('/api/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newItemName, description: newItemDescription })
    });

    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.error || 'Failed'}`);
      return;
    }

    const newItem = await response.json();
    setItems(prev => [...prev, newItem]);  // ✅ Update local state
    handleCloseCreate();  // ✅ Close and reset
  } catch (error) {
    console.error('Error:', error);
    alert('Network error');
  }
};
```

**Files**: `src/app/admin/views/SitesView.tsx:1200-1700`

---

## ✅ PATTERN 3: Drag & Drop (@dnd-kit)

### Installation
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

### Pattern: Sortable List

```tsx
import {
  DndContext,
  closestCenter,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  verticalListSortingStrategy,
  useSortable
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

function SortableList() {
  const [items, setItems] = useState([...]);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5  // ✅ Avoids conflicts with click
      }
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    setItems((items) => {
      const oldIndex = items.findIndex(i => i.id === active.id);
      const newIndex = items.findIndex(i => i.id === over.id);
      return arrayMove(items, oldIndex, newIndex);
    });
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext items={items.map(i => i.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-2">
          {items.map(item => (
            <SortableItem key={item.id} item={item} />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
}

function SortableItem({ item }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1
  };

  return (
    <div ref={setNodeRef} style={style} className="p-4 bg-white border rounded-lg">
      <button {...attributes} {...listeners} className="cursor-grab">
        <GripVertical className="w-4 h-4" />
      </button>
      <span>{item.name}</span>
    </div>
  );
}
```

**Files**: `src/app/admin/views/SitesView.tsx:650-750`, `src/modules/planning/components/DraggablePlanningGrid.tsx`

---

## ✅ PATTERN 4: Form Validation (Zod + shadcn/ui)

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';

// ✅ Define schema
const itemSchema = z.object({
  name: z.string().min(1, 'Name required').max(100),
  email: z.string().email('Invalid email').optional().or(z.literal('')),
  category: z.enum(['STANDARD', 'PREMIUM'], { errorMap: () => ({ message: 'Invalid' }) }),
});

type FormData = z.infer<typeof itemSchema>;

function ItemForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(itemSchema),
    defaultValues: { name: '', category: 'STANDARD' }
  });

  const onSubmit = async (data: FormData) => {
    await fetch('/api/items', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    form.reset();
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name *</FormLabel>
              <FormControl>
                <Input placeholder="Enter name..." {...field} />
              </FormControl>
              <FormMessage />  {/* ✅ Auto error display */}
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Creating...' : 'Create'}
        </Button>
      </form>
    </Form>
  );
}
```

---

## 📚 Progressive Resources

For complete templates and variants:
- **`resources/select-pattern.md`** - Variants + edge cases
- **`resources/modal-crud-templates.md`** - Complete Create/Edit/Delete modals
- **`resources/dnd-patterns.md`** - Advanced @dnd-kit patterns
- **`resources/form-validation.md`** - Zod schemas + validation patterns

---

**Files**: `src/components/ui/`, `src/app/admin/views/SitesView.tsx`
**Last Update**: 27 October 2025
