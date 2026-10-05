---
name: TanStack Table Patterns
description: >-
  Auto-enforce TanStack Table best practices for headless data tables. Activates
  when creating tables, implementing sorting, filtering, pagination, or building
  data grids in React applications.
version: 1.0.0
---

# TanStack Table Patterns

This skill enforces TanStack Table best practices for headless, type-safe data tables.

## Basic Table Setup

```typescript
import {
  createColumnHelper,
  useReactTable,
  getCoreRowModel,
  flexRender,
} from '@tanstack/react-table'
import type { Post } from '@/features/posts/types'

const columnHelper = createColumnHelper<Post>()

const columns = [
  columnHelper.accessor('title', {
    header: 'Title',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('author.name', {
    header: 'Author',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('createdAt', {
    header: 'Created',
    cell: (info) => new Date(info.getValue()).toLocaleDateString(),
  }),
  columnHelper.display({
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => <PostActions post={row.original} />,
  }),
]

export function PostsTable({ data }: { data: Post[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id}>
                {header.isPlaceholder
                  ? null
                  : flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

## Sorting

```typescript
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  type SortingState,
} from '@tanstack/react-table'
import { useState } from 'react'

export function SortableTable({ data }: { data: Post[] }) {
  const [sorting, setSorting] = useState<SortingState>([])

  const columns = [
    columnHelper.accessor('title', {
      header: ({ column }) => (
        <button
          onClick={() => column.toggleSorting()}
          className="flex items-center gap-1"
        >
          Title
          {column.getIsSorted() === 'asc' ? ' ↑' : column.getIsSorted() === 'desc' ? ' ↓' : ''}
        </button>
      ),
      cell: (info) => info.getValue(),
    }),
    // More columns...
  ]

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  return (/* table JSX */)
}
```

## Filtering

### Global Filter
```typescript
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  type ColumnFiltersState,
} from '@tanstack/react-table'

export function FilterableTable({ data }: { data: Post[] }) {
  const [globalFilter, setGlobalFilter] = useState('')

  const table = useReactTable({
    data,
    columns,
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  })

  return (
    <div>
      <input
        type="search"
        placeholder="Search all columns..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
      />
      {/* table JSX */}
    </div>
  )
}
```

### Column Filters
```typescript
import { useState } from 'react'
import type { ColumnFiltersState } from '@tanstack/react-table'

export function ColumnFilterTable({ data }: { data: Post[] }) {
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

  const columns = [
    columnHelper.accessor('status', {
      header: 'Status',
      cell: (info) => info.getValue(),
      filterFn: 'equals',
    }),
    // More columns...
  ]

  const table = useReactTable({
    data,
    columns,
    state: { columnFilters },
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  })

  return (
    <div>
      <select
        onChange={(e) =>
          table.getColumn('status')?.setFilterValue(e.target.value || undefined)
        }
      >
        <option value="">All statuses</option>
        <option value="draft">Draft</option>
        <option value="published">Published</option>
      </select>
      {/* table JSX */}
    </div>
  )
}
```

## Pagination

### Client-Side Pagination
```typescript
import {
  useReactTable,
  getCoreRowModel,
  getPaginationRowModel,
} from '@tanstack/react-table'

export function PaginatedTable({ data }: { data: Post[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: { pageSize: 10 },
    },
  })

  return (
    <div>
      {/* table JSX */}
      <div className="pagination">
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of{' '}
          {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
        <select
          value={table.getState().pagination.pageSize}
          onChange={(e) => table.setPageSize(Number(e.target.value))}
        >
          {[10, 20, 50].map((size) => (
            <option key={size} value={size}>
              Show {size}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
```

### Server-Side Pagination
```typescript
import { useQuery } from '@tanstack/react-query'
import { Route } from '@tanstack/react-router'

export function ServerPaginatedTable() {
  const { page, pageSize } = Route.useSearch()
  const navigate = Route.useNavigate()

  const { data, isLoading } = useQuery({
    queryKey: queryKeys.posts.list({ page, pageSize }),
    queryFn: () => postApi.getPosts({ page, pageSize }),
  })

  const table = useReactTable({
    data: data?.items ?? [],
    columns,
    pageCount: data?.pageCount ?? -1,
    state: {
      pagination: { pageIndex: page - 1, pageSize },
    },
    onPaginationChange: (updater) => {
      const newState =
        typeof updater === 'function'
          ? updater({ pageIndex: page - 1, pageSize })
          : updater
      navigate({
        search: (prev) => ({
          ...prev,
          page: newState.pageIndex + 1,
          pageSize: newState.pageSize,
        }),
      })
    },
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
  })

  if (isLoading) return <Skeleton />

  return (/* table with pagination controls */)
}
```

## Row Selection

```typescript
import {
  useReactTable,
  getCoreRowModel,
  type RowSelectionState,
} from '@tanstack/react-table'

export function SelectableTable({ data, onSelectionChange }: Props) {
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({})

  const columns = [
    columnHelper.display({
      id: 'select',
      header: ({ table }) => (
        <input
          type="checkbox"
          checked={table.getIsAllRowsSelected()}
          onChange={table.getToggleAllRowsSelectedHandler()}
        />
      ),
      cell: ({ row }) => (
        <input
          type="checkbox"
          checked={row.getIsSelected()}
          onChange={row.getToggleSelectedHandler()}
        />
      ),
    }),
    // Other columns...
  ]

  const table = useReactTable({
    data,
    columns,
    state: { rowSelection },
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    enableRowSelection: true,
  })

  // Get selected rows
  const selectedRows = table.getSelectedRowModel().rows.map((row) => row.original)

  return (
    <div>
      <span>{selectedRows.length} selected</span>
      {/* table JSX */}
    </div>
  )
}
```

## Column Visibility

```typescript
import { useState } from 'react'
import type { VisibilityState } from '@tanstack/react-table'

export function ColumnVisibilityTable({ data }: { data: Post[] }) {
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})

  const table = useReactTable({
    data,
    columns,
    state: { columnVisibility },
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <div>
      <div className="column-toggles">
        {table.getAllLeafColumns().map((column) => (
          <label key={column.id}>
            <input
              type="checkbox"
              checked={column.getIsVisible()}
              onChange={column.getToggleVisibilityHandler()}
            />
            {column.id}
          </label>
        ))}
      </div>
      {/* table JSX */}
    </div>
  )
}
```

## Complete Feature Table

```typescript
import {
  createColumnHelper,
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  type SortingState,
  type ColumnFiltersState,
} from '@tanstack/react-table'
import { useState } from 'react'

export function FullFeaturedTable<T>({
  data,
  columns,
}: {
  data: T[]
  columns: ColumnDef<T>[]
}) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [globalFilter, setGlobalFilter] = useState('')

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })

  return (
    <div className="table-container">
      {/* Search */}
      <input
        type="search"
        placeholder="Search..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
      />

      {/* Table */}
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="pagination">
        <button onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
        </span>
        <button onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
          Next
        </button>
      </div>
    </div>
  )
}
```

## Conventions to Enforce

1. **Column helper** - Use `createColumnHelper<T>()` for type safety
2. **FlexRender** - Always use `flexRender()` for headers and cells
3. **Stable columns** - Define columns outside component or memoize
4. **Server pagination** - Use `manualPagination: true` with API
5. **URL state** - Sync table state with router search params
6. **Accessibility** - Include proper table semantics and roles

## Anti-Patterns to Block

```typescript
// ❌ WRONG: Columns inside component without memo
function Table() {
  const columns = [/* columns recreated every render */]
}

// ✅ CORRECT: Columns outside or memoized
const columns = [/* stable reference */]
function Table() {
  const table = useReactTable({ columns, ... })
}

// ❌ WRONG: Not using flexRender
<td>{cell.getValue()}</td>

// ✅ CORRECT: Use flexRender
<td>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>

// ❌ WRONG: Hardcoded pagination
const [page, setPage] = useState(1)

// ✅ CORRECT: URL-synced pagination
const { page } = Route.useSearch()
```
