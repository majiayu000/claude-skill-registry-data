---
name: api-service-conventions
description: 'Quy tắc viết API Service (`**/services/*.ts`) trong JDX-Gamers Website (JGameApp) — static class methods, apiCall(), buildJGameUrl(). Dùng khi: tạo hoặc sửa file `*ApiService.ts`, viết class gọi API/mock backend.'
---

# API Service Conventions — JGameApp

## Cấu Trúc Chuẩn

```typescript
import { apiCall, buildJGameUrl, buildJGameUrlWithParams, type ApiResponse } from '../../../../shared/services/api'

export class {ShortName}ApiService {
  private static readonly BASE_PATH = '/api/{endpoint}'

  static async getList(params: {...}): Promise<ApiResponse<...>> {
    const url = buildJGameUrl(`${this.BASE_PATH}`, params)
    return apiCall<...>({ url, method: 'GET' })
  }

  static async create(data: CreateRequest): Promise<ApiResponse<...>> {
    return apiCall<...>({
      url: buildJGameUrl(this.BASE_PATH),
      method: 'POST',
      body: data,
    })
  }
}
```

> Import từ `shared/services/api` là relative path (số `../` phụ thuộc độ sâu file, vd `../../../../shared/services/api`
> từ `features/Public/xxx/services/`) — module JGameApp không dùng alias `@/shared/`.

## Quy Tắc Bắt Buộc

- **Static class methods** — không dùng instance, không dùng hooks gọi API
- Luôn dùng `apiCall()` — không dùng `fetch()`, `axios`, hay `XMLHttpRequest` trực tiếp
- Luôn dùng `buildJGameUrl()` / `buildJGameUrlWithParams()` để build URL — không hardcode URL
- BASE_PATH là `private static readonly` — không truyền URL qua tham số hàm
- Hiện chưa có backend thật cho JGameApp — nhiều service thực chất gọi qua lớp mock (`mockGate`), xem
  `Website/.claude/system-architect/mock-gate-va-api.md`. Vẫn viết theo đúng shape `ApiService` này để dễ chuyển
  sang backend thật sau này.

## Phân Loại URL Builder

| Hàm | Dùng khi |
|-----|---------|
| `buildJGameUrl(path, params?)` | Query string params (GET list, filter) |
| `buildJGameUrlWithParams(path, pathVars)` | Path variables (GET by ID: `/api/items/:id`) |

## Response Pattern

```typescript
// Hook gọi service:
const result = await FooApiService.getList(params)
if (result.success) {
  setData(result.data)
} else {
  // Xử lý lỗi: toast/inline error tuỳ ngữ cảnh — JGameApp hiện chưa có skill riêng cho việc này (xem quy-tac-code)
}
```
