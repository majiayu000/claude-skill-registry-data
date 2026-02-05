---
name: shadcn-svelte-skill
description: |
  Build accessible, customizable UI components for Svelte/SvelteKit projects using shadcn-svelte CLI, Tailwind CSS v4.1, and TypeScript. Use when creating component-based Svelte applications that need production-ready, styled UI elements with Tailwind v4.1 + Vite.
  Also covers the broader Svelte UI ecosystem including Skeleton UI and Melt UI for library selection guidance.
  Triggers: "add components", "UI components", "build UI", "install component", "create form", "create dialog", "svelte components", "shadcn-svelte", "skeleton ui", "melt ui"
license: Open source (uses MIT from shadcn-svelte)
---

# shadcn-svelte with Tailwind v4.1 + Vite

A comprehensive guide for working with shadcn-svelte, the Svelte port of shadcn/ui. This skill covers component installation, customization, and integration patterns for Svelte and SvelteKit projects using **Tailwind CSS v4.1** with the `@tailwindcss/vite` plugin.

## When to Use

Use shadcn-svelte when:
- Building component-based Svelte/SvelteKit applications
- You need accessible, styled UI elements (buttons, forms, modals, dialogs, etc.)
- You want customizable components that don't lock you into a UI library
- You're using Tailwind CSS v4.1 with Vite for zero-runtime CSS
- You need complex components like data tables, drawers, or navigation menus
- You want TypeScript support with full type safety

**Do NOT use** for lightweight static sites or when you prefer minimal dependencies.

## Svelte Component Library Ecosystem

While this skill focuses on **shadcn-svelte**, here's the broader Svelte UI landscape to help you choose:

### Library Comparison

| Library | Type | Best For | Learning Curve |
|---------|------|----------|----------------|
| **shadcn-svelte** | Copy-paste components | Full customization, TypeScript-first | Medium |
| **Skeleton UI** | Installable package | Rapid development, themes | Low |
| **Melt UI** | Headless primitives | Maximum accessibility control | High |
| **Custom** | Built from scratch | Unique requirements | Varies |

### Skeleton UI

Full-featured component library with built-in theming:

```bash
npm install @skeletonlabs/skeleton @skeletonlabs/tw-plugin
```

```svelte
<script>
  import { AppBar, AppShell } from '@skeletonlabs/skeleton';
</script>

<AppShell>
  <svelte:fragment slot="header">
    <AppBar>My App</AppBar>
  </svelte:fragment>
  <slot />
</AppShell>
```

**Use when:** You want rapid development with pre-built themes and don't need deep customization.

### Melt UI

Headless, accessible primitives—you bring the styling:

```bash
npm install @melt-ui/svelte
```

```svelte
<script>
  import { createDialog, melt } from '@melt-ui/svelte';

  const { trigger, overlay, content, title, close } = createDialog();
</script>

<button use:melt={$trigger}>Open</button>

{#if $open}
  <div use:melt={$overlay} class="fixed inset-0 bg-black/50" />
  <div use:melt={$content} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg">
    <h2 use:melt={$title}>Dialog Title</h2>
    <button use:melt={$close}>Close</button>
  </div>
{/if}
```

**Use when:** You need complete styling control with guaranteed accessibility.

### Quick Add Workflow

For simple component additions across libraries:

```bash
# shadcn-svelte (recommended for this skill)
npx shadcn-svelte@latest add button card dialog

# Skeleton UI
npm install @skeletonlabs/skeleton

# Melt UI
npm install @melt-ui/svelte
```

**For complex multi-component features**, see the `workflows.md` reference document.

## Core Concepts

**shadcn-svelte** is copy-paste component infrastructure, not a traditional npm package. You own the code—components live in your `$lib/components/ui/` directory. This means:

- Full customization without forking
- No version lock-in (upgrade on your schedule)
- TypeScript-first with Svelte 5 reactive variables
- **Tailwind v4.1 with @tailwindcss/vite for zero-runtime styling**
- Built on Bits UI primitives for accessibility
- CSS variables for dynamic theming

## Setup: SvelteKit with Tailwind v4.1

### 1. Create SvelteKit Project

```bash
pnpm dlx sv create my-app
cd my-app
```

### 2. Install Tailwind v4.1 + @tailwindcss/vite

```bash
pnpm i -D tailwindcss @tailwindcss/vite
pnpm dlx shadcn-svelte@latest init
```

### 3. Configure Vite with Tailwind Plugin

Edit `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import { sveltekit } from '@sveltejs/kit/vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
})
```

### 4. Update CSS Entry Point

Edit `src/app.css` (remove old @tailwind directives):

```css
@import "tailwindcss";

/* Your custom CSS here */
@layer utilities {
  .btn-custom {
    @apply px-4 py-2 rounded-lg font-semibold transition-colors;
  }
}
```

No separate `tailwind.config.js` needed—Tailwind v4.1 scans content automatically. If you need custom configuration:

```javascript
// tailwind.config.js (optional)
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f9fafb',
          // ...
        },
      },
    },
  },
  plugins: [],
}
```

### 5. Ensure CSS is Imported in Layout

Edit `src/routes/+layout.svelte`:

```svelte
<script>
  import '../app.css'
</script>

<slot />
```

The `init` command:
- Sets up @tailwindcss/vite plugin in vite.config.ts
- Creates `src/app.css` with `@import "tailwindcss"`
- Creates the `cn()` utility function for class merging
- Configures path aliases

### Add Components

```bash
# Add individual components
pnpm dlx shadcn-svelte@latest add button

# Add multiple at once
pnpm dlx shadcn-svelte@latest add card alert dialog

# Add all components
pnpm dlx shadcn-svelte@latest add --all

# View all available components
pnpm dlx shadcn-svelte@latest list
```

Components install to: `src/lib/components/ui/[component-name]/`

## Common Workflows

### Basic Component Usage

```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<Button variant="default">Click me</Button>
<Button variant="outline">Outlined</Button>
<Button variant="destructive">Delete</Button>
<Button disabled>Disabled</Button>
```

### Form with Validation

```bash
pnpm dlx shadcn-svelte@latest add form input label
```

```svelte
<script lang="ts">
  import { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { z } from "zod";
  import * as Form from "$lib/components/ui/form";
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";

  const schema = z.object({
    email: z.string().email(),
    name: z.string().min(2),
  });

  const form = superForm(data.form, {
    validators: zodClient(schema),
  });

  const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance>
  <Form.Field {form} name="email">
    <Form.Control let:attrs>
      <Form.Label>Email</Form.Label>
      <Input {...attrs} type="email" bind:value={$formData.email} />
    </Form.Control>
    <Form.FieldErrors />
  </Form.Field>

  <Button type="submit">Submit</Button>
</form>
```

### Data Table with TanStack Table v8

**For production data tables**, use TanStack Table v8 (not svelte-headless-table) for advanced features like sorting, filtering, pagination, and row selection.

#### Installation

```bash
# Add table components and helpers
pnpm dlx shadcn-svelte@latest add table data-table button dropdown-menu checkbox input

# Install TanStack Table core
pnpm add @tanstack/table-core
```

#### Project Structure for Data Tables

```
routes/your-route/
  columns.ts                          # Column definitions
  data-table.svelte                   # Main table component
  data-table-actions.svelte           # Row action menus
  data-table-checkbox.svelte          # Selection checkboxes
  data-table-[field]-button.svelte    # Sortable headers
  +page.svelte                        # Page using the table
```

#### Basic Data Table Setup

**Step 1: Define Columns** (`columns.ts`)

```ts
import type { ColumnDef } from "@tanstack/table-core";
import { renderComponent, renderSnippet } from "$lib/components/ui/data-table/index.js";
import { createRawSnippet } from "svelte";

export type Payment = {
  id: string;
  amount: number;
  status: "pending" | "processing" | "success" | "failed";
  email: string;
};

export const columns: ColumnDef<Payment>[] = [
  // Simple text column
  {
    accessorKey: "status",
    header: "Status",
  },
  
  // Formatted cell with snippet
  {
    accessorKey: "amount",
    header: () => {
      const snippet = createRawSnippet(() => ({
        render: () => `<div class="text-end">Amount</div>`,
      }));
      return renderSnippet(snippet);
    },
    cell: ({ row }) => {
      const snippet = createRawSnippet<[{ value: number }]>((getValue) => {
        const { value } = getValue();
        const formatted = new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: "USD",
        }).format(value);
        return {
          render: () => `<div class="text-end font-medium">${formatted}</div>`,
        };
      });
      return renderSnippet(snippet, { value: row.original.amount });
    },
  },
  
  // Component-based cell (for complex UI like action menus)
  {
    id: "actions",
    cell: ({ row }) => renderComponent(DataTableActions, { payment: row.original }),
  },
];
```

**Step 2: Create Table Component** (`data-table.svelte`)

```svelte
<script lang="ts" generics="TData, TValue">
  import {
    type ColumnDef,
    type PaginationState,
    type SortingState,
    getCoreRowModel,
    getPaginationRowModel,
    getSortedRowModel,
  } from "@tanstack/table-core";
  import { createSvelteTable, FlexRender } from "$lib/components/ui/data-table/index.js";
  import * as Table from "$lib/components/ui/table/index.js";
  import { Button } from "$lib/components/ui/button/index.js";

  type DataTableProps<TData, TValue> = {
    data: TData[];
    columns: ColumnDef<TData, TValue>[];
  };

  let { data, columns }: DataTableProps<TData, TValue> = $props();

  // State management with Svelte 5 runes
  let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });
  let sorting = $state<SortingState>([]);

  const table = createSvelteTable({
    get data() { return data; },
    columns,
    state: {
      get pagination() { return pagination; },
      get sorting() { return sorting; },
    },
    onPaginationChange: (updater) => {
      pagination = typeof updater === "function" ? updater(pagination) : updater;
    },
    onSortingChange: (updater) => {
      sorting = typeof updater === "function" ? updater(sorting) : updater;
    },
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });
</script>

<div class="w-full">
  <div class="rounded-md border">
    <Table.Root>
      <Table.Header>
        {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
          <Table.Row>
            {#each headerGroup.headers as header (header.id)}
              <Table.Head>
                {#if !header.isPlaceholder}
                  <FlexRender
                    content={header.column.columnDef.header}
                    context={header.getContext()}
                  />
                {/if}
              </Table.Head>
            {/each}
          </Table.Row>
        {/each}
      </Table.Header>
      <Table.Body>
        {#each table.getRowModel().rows as row (row.id)}
          <Table.Row>
            {#each row.getVisibleCells() as cell (cell.id)}
              <Table.Cell>
                <FlexRender
                  content={cell.column.columnDef.cell}
                  context={cell.getContext()}
                />
              </Table.Cell>
            {/each}
          </Table.Row>
        {:else}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
              No results.
            </Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
    </Table.Root>
  </div>

  <!-- Pagination controls -->
  <div class="flex items-center justify-end space-x-2 pt-4">
    <Button
      variant="outline"
      size="sm"
      onclick={() => table.previousPage()}
      disabled={!table.getCanPreviousPage()}
    >
      Previous
    </Button>
    <Button
      variant="outline"
      size="sm"
      onclick={() => table.nextPage()}
      disabled={!table.getCanNextPage()}
    >
      Next
    </Button>
  </div>
</div>
```

**Step 3: Use in Page** (`+page.svelte`)

```svelte
<script lang="ts">
  import DataTable from "./data-table.svelte";
  import { columns } from "./columns.js";
  
  let { data } = $props();
</script>

<DataTable data={data.payments} {columns} />
```

#### Adding Sorting to Columns

Create sortable header button component (`data-table-email-button.svelte`):

```svelte
<script lang="ts">
  import type { ComponentProps } from "svelte";
  import ArrowUpDownIcon from "@lucide/svelte/icons/arrow-up-down";
  import { Button } from "$lib/components/ui/button/index.js";
  
  let { variant = "ghost", ...restProps }: ComponentProps<typeof Button> = $props();
</script>

<Button {variant} {...restProps}>
  Email
  <ArrowUpDownIcon class="ms-2" />
</Button>
```

Update column definition:

```ts
{
  accessorKey: "email",
  header: ({ column }) => renderComponent(DataTableEmailButton, {
    onclick: column.getToggleSortingHandler(),
  }),
}
```

#### Adding Filtering

Add to `data-table.svelte`:

```svelte
<script lang="ts" generics="TData, TValue">
  import {
    type ColumnFiltersState,
    getFilteredRowModel,
  } from "@tanstack/table-core";
  import { Input } from "$lib/components/ui/input/index.js";
  
  let columnFilters = $state<ColumnFiltersState>([]);
  
  const table = createSvelteTable({
    // ... existing config
    state: {
      get columnFilters() { return columnFilters; },
    },
    onColumnFiltersChange: (updater) => {
      columnFilters = typeof updater === "function" ? updater(columnFilters) : updater;
    },
    getFilteredRowModel: getFilteredRowModel(),
  });
</script>

<!-- Add above table -->
<div class="flex items-center py-4">
  <Input
    placeholder="Filter emails..."
    value={(table.getColumn("email")?.getFilterValue() as string) ?? ""}
    oninput={(e) => table.getColumn("email")?.setFilterValue(e.currentTarget.value)}
    onchange={(e) => table.getColumn("email")?.setFilterValue(e.currentTarget.value)}
    class="max-w-sm"
  />
</div>
```

#### Adding Row Selection

Create checkbox component (`data-table-checkbox.svelte`):

```svelte
<script lang="ts">
  import type { ComponentProps } from "svelte";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
  
  let {
    checked = false,
    onCheckedChange = (v) => (checked = v),
    ...restProps
  }: ComponentProps<typeof Checkbox> = $props();
</script>

<Checkbox bind:checked={() => checked, onCheckedChange} {...restProps} />
```

Add select column to `columns.ts`:

```ts
{
  id: "select",
  header: ({ table }) => renderComponent(DataTableCheckbox, {
    checked: table.getIsAllPageRowsSelected(),
    indeterminate: table.getIsSomePageRowsSelected() && !table.getIsAllPageRowsSelected(),
    onCheckedChange: (value) => table.toggleAllPageRowsSelected(!!value),
    "aria-label": "Select all",
  }),
  cell: ({ row }) => renderComponent(DataTableCheckbox, {
    checked: row.getIsSelected(),
    onCheckedChange: (value) => row.toggleSelected(!!value),
    "aria-label": "Select row",
  }),
  enableSorting: false,
  enableHiding: false,
}
```

Add to `data-table.svelte`:

```svelte
<script lang="ts" generics="TData, TValue">
  import { type RowSelectionState } from "@tanstack/table-core";
  
  let rowSelection = $state<RowSelectionState>({});
  
  const table = createSvelteTable({
    // ... existing config
    state: {
      get rowSelection() { return rowSelection; },
    },
    onRowSelectionChange: (updater) => {
      rowSelection = typeof updater === "function" ? updater(rowSelection) : updater;
    },
  });
</script>

<!-- Show selection count -->
<div class="text-muted-foreground flex-1 text-sm">
  {table.getFilteredSelectedRowModel().rows.length} of{" "}
  {table.getFilteredRowModel().rows.length} row(s) selected.
</div>
```

#### Row Actions Pattern

Create actions component (`data-table-actions.svelte`):

```svelte
<script lang="ts">
  import EllipsisIcon from "@lucide/svelte/icons/ellipsis";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
  
  let { id }: { id: string } = $props();
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger>
    {#snippet child({ props })}
      <Button {...props} variant="ghost" size="icon" class="relative size-8 p-0">
        <span class="sr-only">Open menu</span>
        <EllipsisIcon />
      </Button>
    {/snippet}
  </DropdownMenu.Trigger>
  <DropdownMenu.Content>
    <DropdownMenu.Label>Actions</DropdownMenu.Label>
    <DropdownMenu.Item onclick={() => navigator.clipboard.writeText(id)}>
      Copy ID
    </DropdownMenu.Item>
    <DropdownMenu.Separator />
    <DropdownMenu.Item>View details</DropdownMenu.Item>
    <DropdownMenu.Item>Edit</DropdownMenu.Item>
  </DropdownMenu.Content>
</DropdownMenu.Root>
```

#### Styling Data Tables with Tailwind v4.1

**Define CSS Variables for Table States** in `src/app.css`:

```css
@import "tailwindcss";

@layer theme {
  :root {
    /* Table colors */
    --color-table-bg: 0 0% 100%;
    --color-table-row-hover: 0 0% 96.1%;
    --color-table-row-selected: 210 40% 96%;
    --color-table-border: 0 0% 89.8%;
    --color-table-text: 0 0% 3.6%;
    --color-table-header-bg: 0 0% 94.1%;
  }

  .dark {
    --color-table-bg: 0 0% 14.9%;
    --color-table-row-hover: 0 0% 22%;
    --color-table-row-selected: 210 100% 35%;
    --color-table-border: 0 0% 22%;
    --color-table-text: 0 0% 98%;
    --color-table-header-bg: 0 0% 22%;
  }
}

@layer utilities {
  .table-cell {
    @apply px-4 py-3 text-sm;
  }

  .table-row-hover {
    @apply hover:bg-[hsl(var(--color-table-row-hover))] transition-colors;
  }

  .table-row-selected {
    @apply bg-[hsl(var(--color-table-row-selected))] border-l-4 border-l-primary;
  }

  .table-header {
    @apply bg-[hsl(var(--color-table-header-bg))] font-semibold text-xs uppercase tracking-wide;
  }
}
```

**Apply Row States** in your table component:

```svelte
<Table.Body>
  {#each table.getRowModel().rows as row (row.id)}
    {@const rowSelected = row.getIsSelected()}
    <Table.Row
      class={cn(
        "table-row-hover",
        rowSelected && "table-row-selected"
      )}
      data-state={rowSelected && "selected"}
    >
      {#each row.getVisibleCells() as cell (cell.id)}
        <Table.Cell class="table-cell">
          <FlexRender
            content={cell.column.columnDef.cell}
            context={cell.getContext()}
          />
        </Table.Cell>
      {/each}
    </Table.Row>
  {/each}
</Table.Body>
```

#### Key Patterns for TanStack Tables

1. **Svelte 5 State Management**: Always use `$state` and `get` accessors
2. **State Updater Pattern**: All handlers follow `(updater) => state = typeof updater === "function" ? updater(state) : updater`
3. **Cell Rendering**:
   - Simple HTML: `createRawSnippet` → `renderSnippet`
   - Components: `renderComponent` for interactive UI
   - Plain text: Direct string or number
4. **Row Models**: Add the appropriate row model for each feature (pagination, sorting, filtering)

#### Common Pitfalls

- Forgetting `get` accessors in `createSvelteTable` state config
- Not binding both `oninput` and `onchange` for filter inputs
- Missing row models (e.g., `getFilteredRowModel` for filtering)
- Using wrong import path for data-table helpers

**For comprehensive DataTable reference including:**
- Advanced sorting and filtering patterns
- Column visibility controls
- Responsive table layouts
- Performance optimization (virtual scrolling, debouncing)
- Complete working examples with all features

**See:** `shadcn-datatable.md` and `datatable-tanstack-svelte5.md` reference documents

### Modal/Dialog

```bash
pnpm dlx shadcn-svelte@latest add dialog button
```

```svelte
<script lang="ts">
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";

  let open = false;
</script>

<Dialog.Root bind:open>
  <Dialog.Trigger asChild let:builder>
    <Button builders={[builder]}>Open Dialog</Button>
  </Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Dialog Title</Dialog.Title>
      <Dialog.Description>This is a dialog.</Dialog.Description>
    </Dialog.Header>
    <p>Your content here</p>
    <Dialog.Footer>
      <Button on:click={() => (open = false)}>Close</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>
```

### Drawer (Mobile-Friendly Sidebar)

```bash
pnpm dlx shadcn-svelte@latest add drawer button
```

```svelte
<script lang="ts">
  import * as Drawer from "$lib/components/ui/drawer";
  import { Button } from "$lib/components/ui/button";

  let open = false;
</script>

<Drawer.Root bind:open>
  <Drawer.Trigger asChild let:builder>
    <Button builders={[builder]} variant="outline">Open Drawer</Button>
  </Drawer.Trigger>
  <Drawer.Content>
    <Drawer.Header>
      <Drawer.Title>Navigation</Drawer.Title>
    </Drawer.Header>
    <nav class="flex flex-col gap-2 p-4">
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
    <Drawer.Footer>
      <Drawer.Close asChild let:builder>
        <Button builders={[builder]} variant="outline">Close</Button>
      </Drawer.Close>
    </Drawer.Footer>
  </Drawer.Content>
</Drawer.Root>
```

## Component Organization

### Project Structure

```
src/
├── lib/
│   ├── components/
│   │   ├── ui/              (shadcn-svelte components)
│   │   │   ├── button/
│   │   │   ├── card/
│   │   │   ├── dialog/
│   │   │   └── [...]
│   │   └── custom/          (your custom components)
│   │       └── header.svelte
│   └── utils/
│       └── cn.ts            (class utility from init)
└── routes/
```

### Import Patterns

```svelte
// Named imports (preferred for tree-shaking)
import { Button } from "$lib/components/ui/button";
import { Dialog, DialogTrigger, DialogContent } from "$lib/components/ui/dialog";

// Namespace imports
import * as Button from "$lib/components/ui/button";
import * as Dialog from "$lib/components/ui/dialog";
```

## Customization

### Theme via CSS Variables (Tailwind v4.1)

Edit `src/app.css` to define theme colors as CSS variables. Tailwind v4.1 auto-scans these:

```css
@import "tailwindcss";

@layer theme {
  :root {
    --color-background: 0 0% 100%;
    --color-foreground: 0 0% 3.6%;
    --color-primary: 0 0% 9%;
    --color-primary-foreground: 0 0% 100%;
    --color-secondary: 0 0% 96.1%;
    --color-secondary-foreground: 0 0% 9%;
    --color-destructive: 0 84% 60%;
    --color-muted: 0 0% 96.1%;
    --color-muted-foreground: 0 0% 45.1%;
    --color-border: 0 0% 89.8%;
  }

  .dark {
    --color-background: 0 0% 3.6%;
    --color-foreground: 0 0% 98%;
    --color-primary: 0 0% 98%;
    --color-primary-foreground: 0 0% 9%;
    --color-secondary: 0 0% 14.9%;
    --color-secondary-foreground: 0 0% 98%;
    --color-destructive: 0 84% 60%;
    --color-muted: 0 0% 14.9%;
    --color-muted-foreground: 0 0% 63.9%;
    --color-border: 0 0% 14.9%;
  }
}

@layer utilities {
  .btn-custom {
    @apply px-4 py-2 rounded-lg font-semibold transition-colors;
  }
}
```

Reference in `tailwind.config.js` (if needed):

```javascript
export default {
  theme: {
    colors: {
      background: 'hsl(var(--color-background))',
      foreground: 'hsl(var(--color-foreground))',
      primary: 'hsl(var(--color-primary))',
      'primary-foreground': 'hsl(var(--color-primary-foreground))',
      // ... map CSS variables to theme
    },
    extend: {
      spacing: {
        gutter: '1rem',
      },
    },
  },
}
```

### Override Component Styles

Modify components in `src/lib/components/ui/[name]/` directly. Tailwind v4.1 automatically applies classes:

```svelte
<!-- src/lib/components/ui/button/button.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";

  interface Props {
    variant?: "default" | "outline" | "ghost";
    size?: "sm" | "md" | "lg";
    class?: string;
  }

  let { variant = "default", size = "md", class: className }: Props = $props();

  const baseClasses = cn(
    "inline-flex items-center justify-center font-semibold transition-colors",
    {
      "bg-primary text-primary-foreground hover:bg-primary/90": variant === "default",
      "border border-border bg-background hover:bg-muted": variant === "outline",
      "hover:bg-muted": variant === "ghost",
    },
    {
      "h-8 px-3 text-xs": size === "sm",
      "h-10 px-4 text-sm": size === "md",
      "h-12 px-6 text-base": size === "lg",
    },
    className
  );
</script>

<button class={baseClasses}>
  <slot />
</button>
```

### Tailwind v4.1 Content Scanning

No manual `content` paths needed—Tailwind v4.1 auto-scans your SvelteKit project:

```javascript
// tailwind.config.js (minimal, Vite handles scanning)
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f9fafb',
          600: '#1f2937',
        },
      },
    },
  },
}
```

For custom `@source` directive in CSS:

```css
@import "tailwindcss";

@source "../src/lib/components";
```

## Key Dependencies

Automatically installed with `init` and Tailwind v4.1:

| Package | Purpose |
|---------|---------|
| `@tailwindcss/vite` | Vite plugin for zero-runtime CSS with v4.1 |
| `tailwindcss` | Tailwind CSS framework (v4.1+) |
| `clsx` / `tailwind-merge` | Class utility functions via `cn()` |
| `@lucide/svelte` | Icon library (650+ icons) |
| `bits-ui` | Headless UI primitives (accessibility) |
| `sveltekit` | Full-stack framework |
| `vite` | Build tool (handles CSS imports) |

**Not needed in v4.1:**
- PostCSS
- Autoprefixer
- `tailwind.config.ts` for basic projects

## Advanced Topics

### Dark Mode

Use `mode-watcher` for automatic dark mode switching:

```bash
pnpm i mode-watcher
```

```svelte
<script lang="ts">
  import { modeWatcher } from "mode-watcher";
</script>

<div use:modeWatcher>
  <!-- Your app content -->
</div>
```

### Icons with Lucide

```bash
pnpm dlx shadcn-svelte@latest add button
```

```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Heart } from "@lucide/svelte";
</script>

<Button>
  <Heart class="w-4 h-4 mr-2" />
  Save
</Button>
```

### Creating Custom Components

Copy shadcn component structure as template:

```svelte
<!-- src/lib/components/custom/my-card.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";
  
  interface Props {
    title: string;
    class?: string;
  }

  let { title, class: className, children }: Props & { children?: any } = $props();
</script>

<div class={cn("rounded-lg border p-4", className)}>
  <h3>{title}</h3>
  {#if children}
    <slot />
  {/if}
</div>
```

### Building Component Registries

To create a custom registry for sharing components:

```json
// registry.json
{
  "$schema": "https://shadcn-svelte.com/schema/registry.json",
  "name": "my-components",
  "homepage": "https://my-components.com",
  "items": [
    {
      "name": "custom-card",
      "type": "registry:component",
      "title": "Custom Card",
      "description": "Extended card component",
      "files": [
        {
          "path": "./src/lib/custom-card.svelte",
          "type": "registry:component"
        }
      ]
    }
  ]
}
```

Build registry: `pnpm run registry:build`

## Troubleshooting

### Component Not Found

Verify install location: `src/lib/components/ui/[component]/`
```bash
pnpm dlx shadcn-svelte@latest list    # Check installed components
pnpm dlx shadcn-svelte@latest add button --overwrite  # Reinstall
```

### Styling Issues

1. Ensure Tailwind CSS is configured in `tailwind.config.ts`
2. Check that CSS variables are defined in `src/app.css`
3. Verify component imports use correct path aliases

### TypeScript Errors

Update TypeScript settings in `svelte.config.js`:
```javascript
const config: Config = {
  kit: {
    alias: {
      "$lib": "./src/lib",
      "$components": "./src/lib/components",
    },
  },
};
```

## Command and Hook

### `/shadcn` Command

Interactive assistant for shadcn-svelte component development:

```bash
/shadcn              # Show help and available topics
/shadcn add          # Component installation guidance
/shadcn form         # Form patterns with superforms
/shadcn table        # DataTable with TanStack Table v8
/shadcn dialog       # Modal/drawer/sheet patterns
/shadcn theme        # CSS variables and customization
/shadcn debug        # Troubleshooting common issues
/shadcn button       # Specific component guidance
```

### Development Hook

A hook is available that triggers when editing files in `$lib/components/ui/`:

**Install hook script:**
```bash
# Script location: ~/.claude/hooks/shadcn-component-reminder.sh
chmod +x ~/.claude/hooks/shadcn-component-reminder.sh
```

**Add to ~/.claude/settings.json:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/shadcn-component-reminder.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The hook provides contextual reminders about shadcn patterns when editing component files.

## Resources

- **Official Docs**: https://www.shadcn-svelte.com/docs
- **Component Gallery**: https://www.shadcn-svelte.com/docs/components
- **CLI Reference**: https://www.shadcn-svelte.com/docs/cli
- **Bits UI Docs**: https://bits-ui.com (underlying primitives)
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Lucide Icons**: https://lucide.dev

## Summary

shadcn-svelte provides production-grade UI components that you control. Start with `init`, add components via CLI, customize in-place, and build accessible applications with TypeScript and Tailwind. The copy-paste model means you own your UI layer—no library lock-in.
