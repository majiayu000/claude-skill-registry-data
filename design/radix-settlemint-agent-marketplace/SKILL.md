---
name: radix
description: Radix UI primitives for accessible React components. Covers dialogs, dropdowns, popovers, and form controls. Triggers on radix, Dialog, Popover, DropdownMenu.
triggers: ["radix", "@radix-ui", "Dialog", "Popover", "DropdownMenu", "Select", "Tooltip", "Tabs"]
---

<objective>
Build accessible UI components using Radix UI primitives. Radix provides unstyled, accessible components that you style with Tailwind/CSS.
</objective>

<mcp_first>
**CRITICAL: Fetch Radix UI documentation before implementing.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_context7__query-docs" })
```

```typescript
// Radix primitives
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/radix-ui/primitives",
  topic: "Dialog Trigger Content"
})

// Form controls
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/radix-ui/primitives",
  topic: "Select Checkbox RadioGroup"
})

// Accessibility
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/radix-ui/primitives",
  topic: "accessibility aria keyboard"
})
```
</mcp_first>

<quick_start>
**Dialog:**

```tsx
import * as Dialog from "@radix-ui/react-dialog";

function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button>Open Dialog</button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg">
          <Dialog.Title>Dialog Title</Dialog.Title>
          <Dialog.Description>Dialog description.</Dialog.Description>
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

**Dropdown Menu:**

```tsx
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";

function MyDropdown() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button>Options</button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content className="bg-white rounded-md shadow-lg p-1">
          <DropdownMenu.Item className="px-2 py-1 cursor-pointer hover:bg-gray-100">
            Edit
          </DropdownMenu.Item>
          <DropdownMenu.Item className="px-2 py-1 cursor-pointer hover:bg-gray-100">
            Delete
          </DropdownMenu.Item>
          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />
          <DropdownMenu.Item className="px-2 py-1 cursor-pointer hover:bg-gray-100">
            Settings
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

**Select:**

```tsx
import * as Select from "@radix-ui/react-select";

function MySelect() {
  return (
    <Select.Root>
      <Select.Trigger className="border px-3 py-2 rounded">
        <Select.Value placeholder="Select option" />
        <Select.Icon />
      </Select.Trigger>
      <Select.Portal>
        <Select.Content className="bg-white border rounded shadow-lg">
          <Select.Viewport>
            <Select.Item value="1" className="px-3 py-2 hover:bg-gray-100">
              <Select.ItemText>Option 1</Select.ItemText>
            </Select.Item>
            <Select.Item value="2" className="px-3 py-2 hover:bg-gray-100">
              <Select.ItemText>Option 2</Select.ItemText>
            </Select.Item>
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```
</quick_start>

<common_components>
| Component | Use Case |
|-----------|----------|
| `Dialog` | Modals, confirmations |
| `AlertDialog` | Destructive action confirmations |
| `DropdownMenu` | Context menus, action menus |
| `Select` | Form select inputs |
| `Popover` | Floating content, tooltips |
| `Tooltip` | Hover hints |
| `Tabs` | Tabbed interfaces |
| `Accordion` | Collapsible sections |
| `Checkbox` | Boolean inputs |
| `RadioGroup` | Single selection |
| `Switch` | Toggle inputs |
| `Slider` | Range inputs |
</common_components>

<patterns>
**Controlled state:**

```tsx
const [open, setOpen] = useState(false);

<Dialog.Root open={open} onOpenChange={setOpen}>
  {/* ... */}
</Dialog.Root>
```

**asChild pattern:**

```tsx
// Radix renders YOUR button, not its own
<Dialog.Trigger asChild>
  <Button variant="primary">Open</Button>
</Dialog.Trigger>
```

**Portal for proper stacking:**

```tsx
<Dialog.Portal>
  <Dialog.Overlay />
  <Dialog.Content>
    {/* Content renders outside parent DOM */}
  </Dialog.Content>
</Dialog.Portal>
```

**Forwarding refs:**

```tsx
const MyTrigger = forwardRef((props, ref) => (
  <button ref={ref} {...props}>
    Custom Trigger
  </button>
));

<Dialog.Trigger asChild>
  <MyTrigger />
</Dialog.Trigger>
```
</patterns>

<constraints>
**Required:**
- Use `asChild` to compose with your own components
- Use `Portal` for overlays/dropdowns
- Provide accessible labels (Title, Description)
- Handle keyboard navigation (built-in)

**Accessibility:**
- Always include `Title` for dialogs
- Use `Description` for additional context
- Test with keyboard navigation
- Test with screen readers
</constraints>

<success_criteria>
- [ ] Context7 docs fetched for current API
- [ ] Uses `asChild` for custom triggers
- [ ] Portal used for floating content
- [ ] Accessible labels provided
- [ ] Styled with Tailwind (not inline)
</success_criteria>
