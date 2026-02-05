---
name: pagination-standard
description: Frontend-backend pagination standard, defining minimal parameter naming to reduce transmission characters, applicable to all system pagination scenarios.
---

## Pagination Parameter Standard

### Request Parameters

| Param | Full Name | Type | Default | Description |
|-------|-----------|------|---------|-------------|
| `o` | offset | number | 0 | Offset, starting from which record |
| `s` | size | number | 42 | Page size |

### Response Parameters

| Param | Full Name | Type | Description |
|-------|-----------|------|-------------|
| `d` | data | array | Data list |
| `t` | total | number | Total record count |
| `p` | pages | number | Total page count |

## Usage Examples

### Backend Interface

```typescript
interface PageQuery {
  o?: number  // offset, default 0
  s?: number  // size, default 42
}

interface PageResult<T> {
  d: T[]      // data list
  t: number   // total count
  p: number   // total pages
}
```

### Frontend Query Params

```
GET /api/users?o=0&s=42
GET /api/users?o=42&s=42   // page 2
```

### Frontend Pagination Calculation

```typescript
// page number to offset
const offset = (page - 1) * size

// offset to page number
const page = Math.floor(offset / size) + 1

// total pages
const totalPages = Math.ceil(total / size)
```

## Design Philosophy

Single-letter minimal parameter naming reduces network transmission characters. Significantly lowers bandwidth consumption in high-frequency call scenarios.
