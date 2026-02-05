---
name: react-ui-component
description: Create production-ready React UI components using shadcn/ui and Tailwind CSS. Use when creating shared components, building forms, dialogs, tables, or any UI elements. Automatically installs missing shadcn/ui components and places components in the proper directory structure (app/components/).
---

# React UI Component Builder

Build production-ready React UI components using shadcn/ui and Tailwind CSS with proper project structure.

## Quick Start

When creating a new component:

1. Identify required shadcn/ui components
2. Install missing shadcn/ui components using the script
3. Create component in proper directory
4. Use Tailwind CSS for styling
5. Follow project structure patterns

## Component Creation Workflow

### Step 1: Determine Component Type

Choose the appropriate shadcn/ui components based on the requirement:

- **Forms**: Use `input`, `label`, `button`, `select`, `checkbox`, `textarea`
- **Dialogs/Modals**: Use `dialog`, `sheet`, or `drawer`
- **Data Display**: Use `table`, `card`, `badge`, `tabs`
- **Interactive**: Use `dropdown-menu`, `tooltip`, `toggle`
- **Layout**: Use `separator`, `scroll-area`, `sidebar`

### Step 2: Install Missing shadcn/ui Components

Before creating the component, install any required shadcn/ui components:

```bash
bash scripts/add_shadcn_component.sh <component-names>
```

Example:
```bash
bash scripts/add_shadcn_component.sh dialog input label button
```

Common component combinations:
- Form: `input label button select`
- Dialog with form: `dialog input label button`
- Data table: `table badge dropdown-menu`
- Settings panel: `card input label select button`

### Step 3: Choose Component Structure

Based on complexity, use one of these patterns:

**Simple Component** (no Panda CSS styles needed):
```
app/components/ComponentName.tsx
```

**Component with Panda CSS** (if matching existing patterns):
```
app/components/ComponentName/
├── ComponentName.tsx
├── ComponentName.style.ts
└── index.ts
```

**Complex Component** (with sub-components):
```
app/components/ComponentName/
├── ComponentName.tsx
├── ComponentName.style.ts
├── components/
│   ├── SubComponent.tsx
│   └── index.ts
└── index.ts
```

For detailed structure guidelines, see [references/component-structure.md](references/component-structure.md).

### Step 4: Write Component Code

**Use "use client" directive when the component needs:**
- React hooks (useState, useEffect, etc.)
- Event handlers
- Browser APIs

**Use Tailwind CSS for styling** (preferred for new components).

Example patterns are available in [references/shadcn-patterns.md](references/shadcn-patterns.md).

### Step 5: Export Component

Always export from `index.ts` for clean imports:

```tsx
// app/components/MyComponent/index.ts
export { MyComponent } from './MyComponent'
```

## Common Component Patterns

### Form Dialog Component

```tsx
"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function CreateItemDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create New</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Item</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" placeholder="Enter name" />
          </div>
          <Button type="submit">Create</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

### Data Table Component

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

interface DataItem {
  id: string
  name: string
  status: string
}

export function DataTable({ data }: { data: DataItem[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Status</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={item.id}>
            <TableCell>{item.name}</TableCell>
            <TableCell>
              <Badge>{item.status}</Badge>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### Form Component with Validation

```tsx
"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

export function UserForm() {
  const [email, setEmail] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter email"
          required
        />
      </div>
      <Button type="submit">Submit</Button>
    </form>
  )
}
```

## Important Guidelines

1. **Always use shadcn/ui components** - Do not create custom button, input, dialog components from scratch
2. **Use Tailwind CSS for styling** - Apply utility classes directly in JSX
3. **Place components in app/components/** - UI primitives go in `app/components/ui/`, custom components in `app/components/`
4. **Add "use client" only when needed** - Keep components as Server Components by default
5. **Use TypeScript** - Always define prop types
6. **Export from index.ts** - Use barrel exports for cleaner imports

## Path Aliases

Use these import aliases:
```tsx
import { Button } from "@/components/ui/button"  // shadcn/ui components
import { api } from "@/lib/apis/api"              // API utilities
import { css } from "@/styles/css"                // Panda CSS (when needed)
```

## Additional Resources

- **Common Patterns**: See [references/shadcn-patterns.md](references/shadcn-patterns.md) for form, dialog, table, and interactive component examples
- **Component Structure**: See [references/component-structure.md](references/component-structure.md) for detailed organization patterns
- **Script**: Use `scripts/add_shadcn_component.sh` to install shadcn/ui components

## Checklist for New Components

- [ ] Identified required shadcn/ui components
- [ ] Installed missing shadcn/ui components using script
- [ ] Created component in `app/components/` directory
- [ ] Added "use client" directive if using hooks/event handlers
- [ ] Used Tailwind CSS for styling
- [ ] Defined TypeScript types for props
- [ ] Exported component from index.ts
- [ ] Tested component renders correctly
