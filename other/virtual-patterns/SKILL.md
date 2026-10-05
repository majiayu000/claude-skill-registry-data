---
name: TanStack Virtual Patterns
description: >-
  Auto-enforce TanStack Virtual best practices for list virtualization. Activates
  when implementing large lists, infinite scroll, virtualized grids, or performance
  optimization for long lists in React applications.
version: 1.0.0
---

# TanStack Virtual Patterns

This skill enforces TanStack Virtual best practices for efficient rendering of large lists.

## Basic Virtual List

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

interface VirtualListProps<T> {
  items: T[]
  renderItem: (item: T, index: number) => React.ReactNode
  estimateSize?: number
}

export function VirtualList<T>({
  items,
  renderItem,
  estimateSize = 50,
}: VirtualListProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimateSize,
    overscan: 5,
  })

  return (
    <div
      ref={parentRef}
      className="h-[400px] overflow-auto"
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {renderItem(items[virtualItem.index], virtualItem.index)}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Dynamic Size Virtual List

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef, useCallback } from 'react'

export function DynamicVirtualList({ items }: { items: Post[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100, // Estimated height
    measureElement: (element) => element.getBoundingClientRect().height,
  })

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            data-index={virtualItem.index}
            ref={virtualizer.measureElement}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <PostCard post={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Virtual Grid

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

interface VirtualGridProps<T> {
  items: T[]
  columns: number
  renderItem: (item: T, index: number) => React.ReactNode
  rowHeight?: number
}

export function VirtualGrid<T>({
  items,
  columns,
  renderItem,
  rowHeight = 200,
}: VirtualGridProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null)
  const rowCount = Math.ceil(items.length / columns)

  const rowVirtualizer = useVirtualizer({
    count: rowCount,
    getScrollElement: () => parentRef.current,
    estimateSize: () => rowHeight,
    overscan: 2,
  })

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${rowVirtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {rowVirtualizer.getVirtualItems().map((virtualRow) => {
          const startIndex = virtualRow.index * columns
          const rowItems = items.slice(startIndex, startIndex + columns)

          return (
            <div
              key={virtualRow.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
                display: 'grid',
                gridTemplateColumns: `repeat(${columns}, 1fr)`,
                gap: '1rem',
              }}
            >
              {rowItems.map((item, i) => (
                <div key={startIndex + i}>
                  {renderItem(item, startIndex + i)}
                </div>
              ))}
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

## Infinite Scroll with Virtual List

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useInfiniteQuery } from '@tanstack/react-query'
import { useRef, useEffect } from 'react'
import { queryKeys } from '@/lib/query-keys'

export function InfiniteVirtualList() {
  const parentRef = useRef<HTMLDivElement>(null)

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: queryKeys.posts.list({ infinite: true }),
    queryFn: ({ pageParam = 1 }) => postApi.getPosts({ page: pageParam }),
    getNextPageParam: (lastPage) =>
      lastPage.hasMore ? lastPage.nextPage : undefined,
    initialPageParam: 1,
  })

  const allItems = data?.pages.flatMap((page) => page.items) ?? []

  const virtualizer = useVirtualizer({
    count: hasNextPage ? allItems.length + 1 : allItems.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
    overscan: 5,
  })

  const virtualItems = virtualizer.getVirtualItems()

  // Load more when reaching the end
  useEffect(() => {
    const lastItem = virtualItems[virtualItems.length - 1]
    if (!lastItem) return

    if (
      lastItem.index >= allItems.length - 1 &&
      hasNextPage &&
      !isFetchingNextPage
    ) {
      fetchNextPage()
    }
  }, [virtualItems, hasNextPage, isFetchingNextPage, allItems.length, fetchNextPage])

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualItems.map((virtualItem) => {
          const isLoader = virtualItem.index >= allItems.length

          return (
            <div
              key={virtualItem.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualItem.size}px`,
                transform: `translateY(${virtualItem.start}px)`,
              }}
            >
              {isLoader ? (
                <div className="flex items-center justify-center h-full">
                  Loading more...
                </div>
              ) : (
                <PostCard post={allItems[virtualItem.index]} />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

## Horizontal Virtual List

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

export function HorizontalVirtualList({ items }: { items: Image[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    horizontal: true,
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 200,
    overscan: 3,
  })

  return (
    <div ref={parentRef} className="w-full overflow-x-auto">
      <div
        style={{
          width: `${virtualizer.getTotalSize()}px`,
          height: '200px',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              height: '100%',
              width: `${virtualItem.size}px`,
              transform: `translateX(${virtualItem.start}px)`,
            }}
          >
            <img
              src={items[virtualItem.index].url}
              alt={items[virtualItem.index].alt}
              className="h-full w-full object-cover"
            />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Virtual Table (with TanStack Table)

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useReactTable, getCoreRowModel, flexRender } from '@tanstack/react-table'
import { useRef } from 'react'

export function VirtualTable<T>({
  data,
  columns,
}: {
  data: T[]
  columns: ColumnDef<T>[]
}) {
  const parentRef = useRef<HTMLDivElement>(null)

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  const { rows } = table.getRowModel()

  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 10,
  })

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <table className="w-full">
        <thead className="sticky top-0 bg-white z-10">
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
          <tr style={{ height: `${virtualizer.getTotalSize()}px` }}>
            <td colSpan={columns.length} style={{ padding: 0 }}>
              <div style={{ position: 'relative' }}>
                {virtualizer.getVirtualItems().map((virtualRow) => {
                  const row = rows[virtualRow.index]
                  return (
                    <div
                      key={row.id}
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: `${virtualRow.size}px`,
                        transform: `translateY(${virtualRow.start}px)`,
                        display: 'flex',
                      }}
                    >
                      {row.getVisibleCells().map((cell) => (
                        <div key={cell.id} className="flex-1 px-4 py-2">
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </div>
                      ))}
                    </div>
                  )
                })}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
```

## Scroll to Index

```typescript
export function ScrollableVirtualList({ items }: { items: Post[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  const scrollToItem = (index: number) => {
    virtualizer.scrollToIndex(index, { align: 'center', behavior: 'smooth' })
  }

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <button onClick={() => scrollToItem(0)}>First</button>
        <button onClick={() => scrollToItem(Math.floor(items.length / 2))}>
          Middle
        </button>
        <button onClick={() => scrollToItem(items.length - 1)}>Last</button>
      </div>
      <div ref={parentRef} className="h-[400px] overflow-auto">
        {/* Virtual list content */}
      </div>
    </div>
  )
}
```

## Conventions to Enforce

1. **Ref for scroll element** - Always use `useRef` for parent container
2. **Fixed height container** - Parent must have defined height/overflow
3. **Overscan** - Include 3-5 items for smooth scrolling
4. **Absolute positioning** - Use transform for item placement
5. **Stable keys** - Use virtualItem.key, not index
6. **Dynamic sizing** - Use `measureElement` for variable heights
7. **Combine with Query** - Use infinite queries for data loading

## Anti-Patterns to Block

```typescript
// ❌ WRONG: No fixed height container
<div ref={parentRef}>
  {virtualItems.map(...)}
</div>

// ✅ CORRECT: Fixed height with overflow
<div ref={parentRef} className="h-[400px] overflow-auto">
  {virtualItems.map(...)}
</div>

// ❌ WRONG: Using index as key
{virtualItems.map((item, index) => (
  <div key={index}>...</div>
))}

// ✅ CORRECT: Using virtualItem.key
{virtualItems.map((virtualItem) => (
  <div key={virtualItem.key}>...</div>
))}

// ❌ WRONG: No overscan
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
})

// ✅ CORRECT: Include overscan
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
  overscan: 5,
})
```
