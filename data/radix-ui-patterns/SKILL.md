---
name: radix-ui-patterns
description: Radix UI primitive components for accessible UI. Use when building accessible interactive components.
---

# Radix UI Patterns Skill

This skill covers Radix UI primitives for building accessible, unstyled components.

## When to Use

Use this skill when:
- Building accessible UI components
- Need keyboard navigation
- Implementing dialogs, dropdowns, tooltips
- Creating design system primitives

## Core Principle

**ACCESSIBILITY FIRST** - Radix handles focus management, keyboard navigation, and ARIA attributes. You handle styling.

## Installation

```bash
# Install individual primitives
npm install @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-popover
npm install @radix-ui/react-tooltip
npm install @radix-ui/react-tabs
npm install @radix-ui/react-accordion
npm install @radix-ui/react-select
npm install @radix-ui/react-checkbox
npm install @radix-ui/react-switch
npm install @radix-ui/react-slider
```

## Dialog Pattern

```typescript
'use client';

import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
}

export function Modal({
  open,
  onOpenChange,
  title,
  description,
  children,
}: ModalProps): React.ReactElement {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] bg-white rounded-lg p-6 w-full max-w-md shadow-xl data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          <Dialog.Title className="text-lg font-semibold">
            {title}
          </Dialog.Title>
          {description && (
            <Dialog.Description className="mt-2 text-sm text-gray-500">
              {description}
            </Dialog.Description>
          )}
          <div className="mt-4">{children}</div>
          <Dialog.Close className="absolute right-4 top-4 rounded-sm opacity-70 hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2">
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Usage
function App(): React.ReactElement {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button onClick={() => setOpen(true)}>Open Modal</button>
      <Modal
        open={open}
        onOpenChange={setOpen}
        title="Confirm Action"
        description="Are you sure you want to proceed?"
      >
        <div className="flex gap-2 justify-end">
          <button onClick={() => setOpen(false)}>Cancel</button>
          <button onClick={() => { /* action */ setOpen(false); }}>
            Confirm
          </button>
        </div>
      </Modal>
    </>
  );
}
```

## Dropdown Menu Pattern

```typescript
'use client';

import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { Check, ChevronRight } from 'lucide-react';

interface MenuItem {
  label: string;
  onSelect: () => void;
  disabled?: boolean;
  icon?: React.ReactNode;
}

interface MenuProps {
  trigger: React.ReactNode;
  items: MenuItem[];
}

export function Menu({ trigger, items }: MenuProps): React.ReactElement {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        {trigger}
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="min-w-[200px] bg-white rounded-md shadow-lg border p-1 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[side=bottom]:slide-in-from-top-2"
          sideOffset={5}
        >
          {items.map((item, index) => (
            <DropdownMenu.Item
              key={index}
              disabled={item.disabled}
              onSelect={item.onSelect}
              className="flex items-center gap-2 px-2 py-1.5 text-sm rounded cursor-pointer outline-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:opacity-50 data-[disabled]:pointer-events-none"
            >
              {item.icon}
              {item.label}
            </DropdownMenu.Item>
          ))}
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}

// With sub-menus and checkboxes
function AdvancedMenu(): React.ReactElement {
  const [showBookmarks, setShowBookmarks] = useState(true);

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button>Options</button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content className="menu-content">
          <DropdownMenu.CheckboxItem
            checked={showBookmarks}
            onCheckedChange={setShowBookmarks}
            className="menu-item"
          >
            <DropdownMenu.ItemIndicator>
              <Check className="h-4 w-4" />
            </DropdownMenu.ItemIndicator>
            Show Bookmarks
          </DropdownMenu.CheckboxItem>

          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />

          <DropdownMenu.Sub>
            <DropdownMenu.SubTrigger className="menu-item">
              More Options
              <ChevronRight className="ml-auto h-4 w-4" />
            </DropdownMenu.SubTrigger>
            <DropdownMenu.Portal>
              <DropdownMenu.SubContent className="menu-content">
                <DropdownMenu.Item className="menu-item">
                  Option 1
                </DropdownMenu.Item>
                <DropdownMenu.Item className="menu-item">
                  Option 2
                </DropdownMenu.Item>
              </DropdownMenu.SubContent>
            </DropdownMenu.Portal>
          </DropdownMenu.Sub>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

## Tabs Pattern

```typescript
'use client';

import * as Tabs from '@radix-ui/react-tabs';

interface TabItem {
  value: string;
  label: string;
  content: React.ReactNode;
}

interface TabsGroupProps {
  defaultValue: string;
  items: TabItem[];
}

export function TabsGroup({ defaultValue, items }: TabsGroupProps): React.ReactElement {
  return (
    <Tabs.Root defaultValue={defaultValue}>
      <Tabs.List className="flex border-b">
        {items.map((item) => (
          <Tabs.Trigger
            key={item.value}
            value={item.value}
            className="px-4 py-2 text-sm border-b-2 border-transparent data-[state=active]:border-blue-500 data-[state=active]:text-blue-600 hover:text-gray-700"
          >
            {item.label}
          </Tabs.Trigger>
        ))}
      </Tabs.List>

      {items.map((item) => (
        <Tabs.Content
          key={item.value}
          value={item.value}
          className="p-4 focus:outline-none"
        >
          {item.content}
        </Tabs.Content>
      ))}
    </Tabs.Root>
  );
}
```

## Select Pattern

```typescript
'use client';

import * as Select from '@radix-ui/react-select';
import { Check, ChevronDown, ChevronUp } from 'lucide-react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectFieldProps {
  value: string;
  onValueChange: (value: string) => void;
  options: SelectOption[];
  placeholder?: string;
}

export function SelectField({
  value,
  onValueChange,
  options,
  placeholder = 'Select...',
}: SelectFieldProps): React.ReactElement {
  return (
    <Select.Root value={value} onValueChange={onValueChange}>
      <Select.Trigger className="inline-flex items-center justify-between gap-2 px-3 py-2 text-sm bg-white border rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <Select.Value placeholder={placeholder} />
        <Select.Icon>
          <ChevronDown className="h-4 w-4" />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content className="bg-white rounded-md shadow-lg border overflow-hidden">
          <Select.ScrollUpButton className="flex items-center justify-center h-6">
            <ChevronUp className="h-4 w-4" />
          </Select.ScrollUpButton>

          <Select.Viewport className="p-1">
            {options.map((option) => (
              <Select.Item
                key={option.value}
                value={option.value}
                className="relative flex items-center px-8 py-2 text-sm rounded cursor-pointer outline-none hover:bg-gray-100 focus:bg-gray-100 data-[state=checked]:text-blue-600"
              >
                <Select.ItemIndicator className="absolute left-2">
                  <Check className="h-4 w-4" />
                </Select.ItemIndicator>
                <Select.ItemText>{option.label}</Select.ItemText>
              </Select.Item>
            ))}
          </Select.Viewport>

          <Select.ScrollDownButton className="flex items-center justify-center h-6">
            <ChevronDown className="h-4 w-4" />
          </Select.ScrollDownButton>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```

## Tooltip Pattern

```typescript
'use client';

import * as Tooltip from '@radix-ui/react-tooltip';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
}

export function TooltipWrapper({
  content,
  children,
  side = 'top',
}: TooltipProps): React.ReactElement {
  return (
    <Tooltip.Provider delayDuration={300}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          {children}
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content
            side={side}
            className="px-3 py-1.5 text-sm bg-gray-900 text-white rounded shadow-lg animate-in fade-in-0 zoom-in-95"
            sideOffset={5}
          >
            {content}
            <Tooltip.Arrow className="fill-gray-900" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
```

## Accessibility Features

Radix primitives automatically provide:

- **Keyboard navigation** - Tab, Arrow keys, Enter, Escape
- **Focus management** - Traps focus in modals, returns focus on close
- **ARIA attributes** - Proper roles, states, and properties
- **Screen reader announcements** - Live regions for dynamic content

## Data Attributes for Styling

```css
/* Style based on state */
[data-state="open"] {
  /* Open state styles */
}

[data-state="closed"] {
  /* Closed state styles */
}

[data-state="active"] {
  /* Active state styles */
}

[data-state="checked"] {
  /* Checked state styles */
}

[data-disabled] {
  /* Disabled state styles */
}

[data-highlighted] {
  /* Keyboard highlighted styles */
}
```

## Best Practices

1. **Use `asChild`** - Pass your own trigger elements
2. **Portal content** - Render overlays outside DOM tree
3. **Use data attributes** - Style based on component state
4. **Add animations** - Use `data-[state=open]` for enter/exit animations
5. **Provide sr-only labels** - For icon-only buttons

## Notes

- Radix is unstyled by design
- Use with Tailwind CSS or CSS-in-JS
- shadcn/ui is built on Radix primitives
- All primitives are individually installable
