---
name: nuxt-tables
description: Table components with column builder pattern and XTable. Use when creating data tables, defining columns with custom cells, implementing row actions, or building reusable table configurations.
---

# Nuxt Tables

Data tables with column builder pattern and XTable component.

## Core Concepts

**[tables.md](references/tables.md)** - Column builder, XTable, row actions

## Column Builder Pattern

```typescript
// app/tables/posts.ts
import { h } from 'vue'
import type { TableColumn } from '@tanstack/vue-table'

const statusColumn: TableColumn<Post> = {
  id: 'status',
  accessorKey: 'status',
  header: 'Status',
  cell: ({ row }) => h(UBadge, {
    color: row.getValue('status').color()
  }, () => row.getValue('status').text),
}

export const postsColumnBuilder = createColumnBuilder<Post>({
  ulid: ulidColumn,
  author: authorColumn,
  status: statusColumn,
  dates: datesColumn,
})

// Usage
const columns = postsColumnBuilder.all()
const columns = postsColumnBuilder.build(['ulid', 'status'])
const columns = postsColumnBuilder.except(['dates'])
```

## XTable Usage

```vue
<XTable
  :data="posts"
  :columns="columns"
  :loading="isLoading"
  :fetching="isFetching"
  :row-actions="rowActions"
  row-id="ulid"
  @row-click="handleRowClick"
/>
```

## Row Actions

```typescript
const rowActions = computed(() => (row: Row<Post>) => [
  { label: 'View', to: `/posts/${row.original.ulid}` },
  { label: 'Edit', onSelect: () => openEdit(row.original) },
  { label: 'Delete', onSelect: () => handleDelete(row.original) },
])
```
