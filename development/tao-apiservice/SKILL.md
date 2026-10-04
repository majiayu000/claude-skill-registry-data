---
name: tao-apiservice
description: 'Quy tắc tạo API Service từ backend docs trong SASUCO. Dùng khi: viết class ApiService từ tài liệu API backend, import apiCall/buildApiUrl/buildApiUrlWithParams/ApiResponse/PagingInfo, tránh deprecated buildApiHeaders/handleApiError/ApiLogger, định nghĩa enums và interfaces đầy đủ theo docs, cấu trúc BASE_PATH/static methods, phân biệt Admin vs Business portal.'
---

# Tạo API Service từ Backend Docs — SASUCO

## ⚠️ Trước Khi Code

1. **Đọc tài liệu backend API** (trong `docs/backend/` hoặc prompt)
2. **Kiểm tra `/shared/services/api/`** để xác nhận functions tồn tại
3. Tài liệu có interface/enum nào → phải implement đủ, không bỏ sót
4. **Nếu phát hiện sai lệch tài liệu ↔ code thực tế → BÁO CÁO, không tự ý code**

---

## 🔴 Nguyên Tắc Mapping Types 1:1 với BE DTO (BẮT BUỘC)

> **Tên field trong interface FE phải GIỐNG HỆT tên field trong DTO của BE.**
> Không được đổi tên, không được viết tắt, không được sáng tạo tên mới.

### ✅ ĐÚNG — Copy chính xác tên từ BE docs

```typescript
// BE DTO (C#): class InvoiceDocument { string invoiceNumber; DateTime issuedDate; }
interface InvoiceDocument {
  invoiceNumber: string   // ✅ giữ nguyên tên BE
  issuedDate: string      // ✅ giữ nguyên tên BE
}
```

### ❌ SAI — Đổi tên theo ý FE

```typescript
interface InvoiceDocument {
  number: string          // ❌ BE trả về invoiceNumber, không phải number
  date: string            // ❌ BE trả về issuedDate, không phải date
}
```

---

## 🔴 Mapping Dữ Liệu Phân Trang (BẮT BUỘC)

`PagingInfo<T>` trong shared có cấu trúc cố định:

```typescript
interface PagingInfo<T> {
  items: T[]        // ← tên field items
  total: number     // ← tổng bản ghi
  page: number      // ← trang hiện tại (1-based)
  limit: number     // ← số bản ghi mỗi trang
  totalPages: number
}
```

### Quy tắc chọn type cho response phân trang:

| BE thực tế trả về | FE dùng |
|-------------------|---------|
| `{ items, total, page, limit, totalPages }` | `PagingInfo<T>` ✅ |
| `{ data, totalCount, currentPage, pageSize }` | Tự tạo interface 1:1 theo BE ❌ KHÔNG dùng `PagingInfo<T>` |
| Bất kỳ cấu trúc khác | Tự tạo interface 1:1 theo BE |

> **KHÔNG được giả định BE trả về `PagingInfo<T>` nếu chưa đọc docs.**
> Nếu BE trả về `pageNumber` thì interface phải có `pageNumber`, không phải `page`.

### Ví dụ BE trả cấu trúc KHÁC PagingInfo:

```typescript
// BE docs: { data: T[], totalCount: number, pageNumber: number, pageSize: number }
// ❌ SAI: dùng PagingInfo<T> vì tên field không khớp
// ✅ ĐÚNG: tạo interface riêng
interface CustomerListResponse {
  data: CustomerDocument[]   // ← đúng tên BE
  totalCount: number         // ← đúng tên BE
  pageNumber: number         // ← đúng tên BE
  pageSize: number           // ← đúng tên BE
}
```

---

---

## Import — BẮT BUỘC

```typescript
import {
  apiCall,                  // ✅ Auto: logging, headers, errors, token
  buildApiUrl,              // ✅ Build URL từ path
  buildApiUrlWithParams,    // ✅ Build URL có query params
  type ApiResponse,         // ✅ Response type chuẩn
  type PagingInfo,          // ✅ Paging type (nếu có pagination)
} from '../../../../../shared/services/api'
```

## Import — CẤM (deprecated)

```typescript
// ❌ CẤM dùng:
import { buildApiHeaders, handleApiError } from '...'
// ❌ CẤM manual try-catch — apiCall tự xử lý
// ℹ️ Không cần import ApiLogger trong static methods của ApiService
//    → apiCall tự xử lý logging nội bộ
//    → Nếu cần log trong hook hoặc component → dùng ApiLogger (xem skill quy-tac-code)
```

---

## Template Cơ Bản

```typescript
/**
 * {Feature} API Service - {Portal} Portal
 * @see /docs/backend/{Feature}API.md
 */
import {
  apiCall, buildApiUrl, buildApiUrlWithParams,
  type ApiResponse, type PagingInfo,
} from '../../../../../shared/services/api'

// ===== ENUMS & TYPES (export từ service file) =====
export enum {Feature}Status { Active = 1, Inactive = 0 }
export interface {Feature}Document { id: number; /* ... */ }
export interface Create{Feature}Request { /* ... */ }
export interface {Feature}ListParams { page?: number; pageSize?: number; search?: string }

// ===== SERVICE =====
export class {Feature}ApiService {
  private static readonly BASE_PATH = '/api/{portal}/{feature}'

  /** Lấy danh sách */
  static async getAll(params?: {Feature}ListParams): Promise<ApiResponse<PagingInfo<{Feature}Document>>> {
    const queryParams: Record<string, unknown> = {}
    if (params?.search) queryParams.search = params.search
    if (params?.page) queryParams.page = params.page
    if (params?.pageSize) queryParams.pageSize = params.pageSize
    const url = buildApiUrlWithParams(this.BASE_PATH, queryParams)
    const response = await apiCall(url, { method: 'GET' })
    return response.json()
  }

  /** Lấy chi tiết */
  static async getById(id: number): Promise<ApiResponse<{Feature}Document>> {
    const url = buildApiUrl(`${this.BASE_PATH}/${id}`)
    const response = await apiCall(url, { method: 'GET' })
    return response.json()
  }

  /** Tạo mới */
  static async create(data: Create{Feature}Request): Promise<ApiResponse<{Feature}Document>> {
    const url = buildApiUrl(this.BASE_PATH)
    const response = await apiCall(url, { method: 'POST', body: JSON.stringify(data) })
    return response.json()
  }

  /** Cập nhật */
  static async update(id: number, data: Update{Feature}Request): Promise<ApiResponse<{Feature}Document>> {
    const url = buildApiUrl(`${this.BASE_PATH}/${id}`)
    const response = await apiCall(url, { method: 'PUT', body: JSON.stringify(data) })
    return response.json()
  }

  /** Xóa */
  static async delete(id: number): Promise<ApiResponse<void>> {
    const url = buildApiUrl(`${this.BASE_PATH}/${id}`)
    const response = await apiCall(url, { method: 'DELETE' })
    return response.json()
  }
}
```

---

## Tổ Chức Types

```
services/
  └── {Feature}ApiService[Admin].ts    ← Enums + API types + Service class
types/
  └── {feature}.types.ts               ← Re-export API types + UI-only types
```

**Trong `types/{feature}.types.ts`:**
```typescript
// Re-export từ service
export { {Feature}Status, type {Feature}Document } from '../services/{Feature}ApiService'

// UI-only types (KHÔNG export từ service)
export interface {Feature}FormData { /* ... */ }
export const {FEATURE}_STATUS_NAMES: Record<number, string> = { 1: 'Hoạt động', 0: 'Tạm dừng' }
```

---

## Naming

| Loại | Business | Admin |
|------|---------|-------|
| Service class | `{Feature}ApiService` | `{Feature}ApiServiceAdmin` |
| Interface | `{Feature}Document` | — |
| Request | `Create{Feature}Request`, `Update{Feature}Request` | — |
| Params | `{Feature}ListParams` | — |

---

## Lưu Ý Quan Trọng

- Backend docs thường viết cho cả Admin + Customer
- **Chỉ tạo endpoints phù hợp với portal đang phát triển**
- Admin: thường có CRUD đầy đủ
- Business/Customer: thường chỉ xem/sửa của mình

---

## Checklist

- [ ] Import đúng: `apiCall`, `buildApiUrl`, `buildApiUrlWithParams`, `ApiResponse`, `PagingInfo`
- [ ] KHÔNG import: `buildApiHeaders`, `handleApiError`, `ApiLogger`
- [ ] Có JSDoc cho class và mỗi method
- [ ] Có `BASE_PATH` constant
- [ ] Không có `try-catch`, không có manual logging
- [ ] **Tên field trong tất cả interfaces khớp 1:1 với tên DTO của BE (không đổi tên)**
- [ ] **Dùng `PagingInfo<T>` CHỈ KHI BE thực sự trả `items/total/page/limit/totalPages` — kiểm tra docs trước**
- [ ] 0 TypeScript errors

---


