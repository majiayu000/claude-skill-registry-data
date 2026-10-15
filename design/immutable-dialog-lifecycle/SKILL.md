---
name: immutable-dialog-lifecycle
description: Prevent dialog content flicker, identity changes, and stale exit callbacks by creating an immutable instance for every opening and destroying it only after its closing transition completes. Use when React dialogs, modals, sheets, popovers, or animated overlays reuse shared state, change copy while closing, briefly switch the selected item, or need reliable open/close lifecycle ownership.
---

# Immutable Dialog Lifecycle

## Principle

Treat every opening as a new dialog instance, not another render of one shared container.

Create an immutable descriptor containing everything needed during that instance's lifetime:

- a unique instance id;
- dialog type;
- target identity or snapshot;
- title and description;
- any render-critical labels or options.

Keep visibility separate from content identity. Closing sets `open` to `false`, but retains the descriptor while the exit transition renders. Destroy that exact instance only after the transition completes.

This prevents closing UI from reading a cleared selection, a default file type, or data belonging to the next dialog.

## Bad Pattern

This shared-state pattern clears the content when closing. The dialog can still be visible during its exit animation, so fallback or newly selected content flashes before unmounting.

```tsx
type DialogState =
  | { type: "rename"; item: Item; }
  | { type: "delete"; item: Item; }
  | null;

const [dialog, setDialog] = useState<DialogState>(null);

const closeDialog = () => {
  setDialog(null);
};

return (
  <Dialog open={dialog !== null} onOpenChange={(open) => !open && closeDialog()}>
    <DialogTitle>
      {dialog?.type === "delete" ? `Delete ${dialog.item.name}` : "Rename"}
    </DialogTitle>
  </Dialog>
);
```

Retained-state patches such as `current ?? previous ?? defaultValue` only hide the symptom. They create multiple sources of truth and still allow the wrong snapshot to win during races.

## Good Pattern

Give each opening a stable descriptor and key. Close without mutating it, then destroy only the instance whose exit actually completed.

```tsx
type DialogDescriptor = Readonly<{
  id: number;
  type: "rename" | "delete";
  itemId: string;
  title: string;
  description: string;
}>;

const nextId = useRef(0);
const [instance, setInstance] = useState<DialogDescriptor | null>(null);
const [open, setOpen] = useState(false);

const createDialog = (type: DialogDescriptor["type"], item: Item) => {
  nextId.current += 1;

  setInstance({
    id: nextId.current,
    type,
    itemId: item.id,
    title: type === "delete" ? `Delete ${item.name}?` : "Rename",
    description: type === "delete" ? `This permanently deletes ${item.name}.` : "",
  });
  setOpen(true);
};

const closeDialog = () => {
  setOpen(false);
};

const destroyDialog = (id: number) => {
  setInstance((current) => (current?.id === id ? null : current));
};

return instance
  ? (
    <Dialog
      key={instance.id}
      open={open}
      onOpenChange={setOpen}
      onOpenChangeComplete={(nextOpen) => {
        if (!nextOpen) destroyDialog(instance.id);
      }}
    >
      <DialogTitle>{instance.title}</DialogTitle>
      <DialogDescription>{instance.description}</DialogDescription>
      <button onClick={closeDialog}>Cancel</button>
    </Dialog>
  )
  : null;
```

Use the component library's real exit-completion callback (`onOpenChangeComplete`, `onExitComplete`, or equivalent). Do not guess the animation duration with `setTimeout`.

The id check matters when a new dialog opens before an older exit callback finishes: the stale callback may destroy only its own instance, never the current one.

## Ownership Rules

- Snapshot render-critical content when opening; do not derive it from a mutable global selection during exit.
- Keep `open` as visibility state and the descriptor as instance identity.
- Keep pending submission state scoped to the instance when it affects rendered content or disabled controls.
- Use `key={instance.id}` when local component state must reset for every opening.
- Let dismissal begin the exit; let exit completion perform destruction.
- Prefer one reusable lifecycle hook over separate retained-state fixes in Rename, Create, and Delete dialogs.

## Verification

Test the lifecycle, not only the final hidden state:

1. Open for item A and record its id and copy.
2. Close it and assert item A's unchanged copy remains during the ending phase.
3. Complete the exit and assert the instance is destroyed.
4. Reopen for item B and assert it has a new id and fresh snapshot.
5. Fire item A's stale exit callback and assert item B remains mounted.

The invariant is: closing changes visibility, never identity or content; exit completion destroys only the instance that exited.
