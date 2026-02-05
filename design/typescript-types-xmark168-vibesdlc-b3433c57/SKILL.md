---
name: typescript-types
description: Define TypeScript types, interfaces, and type utilities. Use when creating type definitions, DTOs, API response types, or component props.
---

This skill guides creation of TypeScript types and interfaces for Next.js applications.

## File Location

- **Types directory**: `src/types/` or `src/types/index.ts`
- **Co-located types**: In same file if only used locally
- **Barrel exports**: Use `index.ts` to re-export all types

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Entity interfaces | PascalCase | `Book`, `User`, `Order` |
| Display/Card types | Entity + Data/Card suffix | `BookCardData`, `UserProfile` |
| API response types | Action + Response | `LoginResponse`, `SearchResult` |
| Props types | ComponentName + Props | `BookCardProps`, `HeaderProps` |
| Enums | PascalCase | `OrderStatus`, `UserRole` |

## Common Patterns

### Entity Types (mirror Prisma models)

```typescript
// src/types/index.ts
export interface Book {
  id: string;
  title: string;
  author: string;
  price: number;
  stock: number;
  coverUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  parentId?: string;
}
```

### Display/Card Types (for UI components)

```typescript
// Subset of entity for display purposes
export interface BookCardData {
  id: string;
  title: string;
  author: string;
  price: number;
  coverUrl?: string;
  rating?: number;
  discountPercent?: number;
}

export interface CategoryWithCount {
  id: string;
  name: string;
  slug: string;
  bookCount: number;
  coverImage?: string;
}
```

### API Response Types

```typescript
// Generic API response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

// Paginated response
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Specific responses
export interface SearchBooksResponse {
  books: BookCardData[];
  total: number;
  query: string;
}
```

### Component Props Types

```typescript
// Props with children
export interface CardProps {
  children: React.ReactNode;
  className?: string;
}

// Props with data
export interface BookCardProps {
  book: BookCardData;
  onAddToCart?: (id: string) => void;
  showRating?: boolean;
}

// Props with handlers
export interface SearchBarProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  onClear?: () => void;
}
```

### Enums and Union Types

```typescript
// Use const objects for better tree-shaking
export const OrderStatus = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled',
} as const;

export type OrderStatus = typeof OrderStatus[keyof typeof OrderStatus];

// Simple union types
export type SortOrder = 'asc' | 'desc';
export type BookSortBy = 'price' | 'title' | 'createdAt' | 'rating';
```

## Conversion Functions

```typescript
// Entity to display type conversion
export function toBookCardData(book: Book): BookCardData {
  return {
    id: book.id,
    title: book.title,
    author: book.author,
    price: book.price,
    coverUrl: book.coverUrl,
  };
}

// Batch conversion
export function toBooksCardData(books: Book[]): BookCardData[] {
  return books.map(toBookCardData);
}
```

## Best Practices

1. **Export all types** from `src/types/index.ts` for easy imports
2. **Use `interface` for objects**, `type` for unions/primitives
3. **Make optional fields explicit** with `?` suffix
4. **Avoid `any`** - use `unknown` if type is truly unknown
5. **Document complex types** with JSDoc comments
6. **Keep types close to usage** if only used in one file
