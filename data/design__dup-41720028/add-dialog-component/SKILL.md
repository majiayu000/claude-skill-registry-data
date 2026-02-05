---
name: add-dialog-component
description: Create React dialog components with forms for the dealflow-network project using Radix UI, tRPC mutations, and proper state management. Use when adding create/edit dialogs, modals, or form-based UI components.
---

# Add Dialog Component

Create form dialogs following project patterns.

## Quick Start

When adding a dialog, I will:
1. Create component in `client/src/components/`
2. Use Radix UI Dialog primitive
3. Add form state with useState
4. Integrate tRPC mutation
5. Handle loading, success, and error states

## Template: Create Dialog

```tsx
// client/src/components/CreateItemDialog.tsx

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

interface CreateItemDialogProps {
  trigger?: React.ReactNode;
  onSuccess?: (item: { id: number; name: string }) => void;
}

export function CreateItemDialog({ trigger, onSuccess }: CreateItemDialogProps) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const utils = trpc.useUtils();

  const createMutation = trpc.items.create.useMutation({
    onSuccess: (item) => {
      utils.items.list.invalidate();
      toast.success("Item created successfully");
      setOpen(false);
      resetForm();
      onSuccess?.(item);
    },
    onError: (error) => {
      toast.error(`Failed to create item: ${error.message}`);
    },
  });

  const resetForm = () => {
    setName("");
    setDescription("");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Name is required");
      return;
    }
    createMutation.mutate({ name: name.trim(), description });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {trigger || <Button>Create Item</Button>}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Item</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name *</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter item name"
              disabled={createMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Input
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter description (optional)"
              disabled={createMutation.isPending}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={createMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={createMutation.isPending}>
              {createMutation.isPending ? "Creating..." : "Create"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## Template: Edit Dialog

```tsx
// client/src/components/EditItemDialog.tsx

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";
import type { Item } from "@shared/types";

interface EditItemDialogProps {
  item: Item | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export function EditItemDialog({
  item,
  open,
  onOpenChange,
  onSuccess,
}: EditItemDialogProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const utils = trpc.useUtils();

  // Populate form when item changes
  useEffect(() => {
    if (item) {
      setName(item.name);
      setDescription(item.description ?? "");
    }
  }, [item]);

  const updateMutation = trpc.items.update.useMutation({
    onSuccess: () => {
      utils.items.list.invalidate();
      utils.items.get.invalidate({ id: item?.id });
      toast.success("Item updated successfully");
      onOpenChange(false);
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(`Failed to update: ${error.message}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!item) return;
    if (!name.trim()) {
      toast.error("Name is required");
      return;
    }
    updateMutation.mutate({
      id: item.id,
      name: name.trim(),
      description,
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Item</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="edit-name">Name *</Label>
            <Input
              id="edit-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={updateMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-description">Description</Label>
            <Input
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={updateMutation.isPending}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={updateMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={updateMutation.isPending}>
              {updateMutation.isPending ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## Template: Confirmation Dialog

```tsx
// client/src/components/DeleteConfirmDialog.tsx

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

interface DeleteConfirmDialogProps {
  itemId: number | null;
  itemName: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export function DeleteConfirmDialog({
  itemId,
  itemName,
  open,
  onOpenChange,
  onSuccess,
}: DeleteConfirmDialogProps) {
  const utils = trpc.useUtils();

  const deleteMutation = trpc.items.delete.useMutation({
    onSuccess: () => {
      utils.items.list.invalidate();
      toast.success("Item deleted");
      onOpenChange(false);
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(`Failed to delete: ${error.message}`);
    },
  });

  const handleConfirm = () => {
    if (itemId) {
      deleteMutation.mutate({ id: itemId });
    }
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Item</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{itemName}"? This action cannot be
            undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={deleteMutation.isPending}>
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={handleConfirm}
            disabled={deleteMutation.isPending}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            {deleteMutation.isPending ? "Deleting..." : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

## Usage in Page Component

```tsx
// In a page component
import { CreateItemDialog } from "@/components/CreateItemDialog";
import { EditItemDialog } from "@/components/EditItemDialog";
import { DeleteConfirmDialog } from "@/components/DeleteConfirmDialog";

function ItemsPage() {
  const [editItem, setEditItem] = useState<Item | null>(null);
  const [deleteItem, setDeleteItem] = useState<{ id: number; name: string } | null>(null);

  return (
    <div>
      <CreateItemDialog />

      <EditItemDialog
        item={editItem}
        open={!!editItem}
        onOpenChange={(open) => !open && setEditItem(null)}
      />

      <DeleteConfirmDialog
        itemId={deleteItem?.id ?? null}
        itemName={deleteItem?.name ?? ""}
        open={!!deleteItem}
        onOpenChange={(open) => !open && setDeleteItem(null)}
      />
    </div>
  );
}
```

## Available UI Components

Import from `@/components/ui/`:
- `Dialog`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogTrigger`
- `AlertDialog`, `AlertDialogAction`, `AlertDialogCancel`, `AlertDialogContent`
- `Button` (variants: default, outline, destructive, ghost)
- `Input`, `Label`, `Textarea`
- `Select`, `SelectContent`, `SelectItem`, `SelectTrigger`, `SelectValue`
- `Checkbox`, `Switch`

## Checklist

- [ ] Form state managed with useState
- [ ] Form populated from props (for edit dialogs)
- [ ] Input validation before mutation
- [ ] Loading state on submit button
- [ ] Inputs disabled during mutation
- [ ] Cache invalidation on success
- [ ] Toast notifications for success/error
- [ ] Form reset on close/success
- [ ] Cancel button available
