---
name: hook-conventions
description: 'Quy tắc viết custom hook (`**/hooks/*.ts`) trong JDX-Gamers Website (JGameApp) — page hook, dialog hook, data hook, reset state khi dialog mở lại, useEffect dependencies. Dùng khi: tạo hoặc sửa file `use*.ts` chứa business logic của 1 feature.'
---

# Hook Conventions — JGameApp

## Nguyên Tắc

- Hook là **nơi duy nhất** chứa business logic trong một feature
- Hook **không** render JSX, **không** import component
- Page/Dialog/Component chỉ gọi hook — không tự quản lý state

## Phân Loại Hook

| Loại | File pattern | Trách nhiệm |
|------|-------------|-------------|
| Page hook | `use{SN}.page.{action}.ts` | Quản lý state trang: data, loading, filter, pagination, dialogs open/close |
| Dialog hook | `use{SN}.dlg.{action}.ts` | Form state, validation, submit, loading |
| Data hook | `use{SN}Data.ts` | Gọi API, quản lý data cache, refresh |

## Pattern Chuẩn — Page Hook

```typescript
export function use{SN}PageMain() {
  // 1. State
  const [data, setData] = useState<...[]>([])
  const [loading, setLoading] = useState(false)
  const [filterParams, setFilterParams] = useState<FilterType>(defaultFilter)

  // 2. Fetch data
  const fetchData = useCallback(async () => {
    setLoading(true)
    const result = await {SN}ApiService.getList(filterParams)
    if (result.success) setData(result.data ?? [])
    else showValidationErrorDialog(result)
    setLoading(false)
  }, [filterParams])

  useEffect(() => { fetchData() }, [fetchData])

  // 3. Return
  return { data, loading, filterParams, setFilterParams, refreshData: fetchData }
}
```

## Quy Tắc useEffect

- Luôn khai báo đầy đủ dependencies array
- Không bỏ qua eslint dependency warnings
- Hàm bên trong useEffect hoặc dùng `useCallback` nếu là dependency

## Quy Tắc Dialog Hook — Reset State (BẮT BUỘC)

> ⚠️ **Dialog KHÔNG unmount khi đóng** (chỉ ẩn/hiện bằng `open` prop) → `useState(initialValue)` chỉ chạy 1 lần. Khi dialog mở lại với `initialData` mới, state vẫn giữ giá trị cũ.

```typescript
// ❌ SAI — formData không reset khi initialData thay đổi
export function useXxxDialogForm(initialData: XxxDto | null) {
  const [formData, setFormData] = useState(initialData ?? INITIAL_FORM)
}

// ✅ ĐÚNG — useEffect reset khi initialData thay đổi
export function useXxxDialogForm(initialData: XxxDto | null) {
  const buildInitial = (data: XxxDto | null) => data ? mapDto(data) : { ...INITIAL_FORM }
  const [formData, setFormData] = useState(() => buildInitial(initialData))

  useEffect(() => {
    setFormData(buildInitial(initialData))
    setErrors({})
    setTouched({})
  }, [initialData])
}
```

> **Pattern thay thế:** Nếu component dùng `useEffect([open, initialData?.id])` để gọi `setFormData`, thì hook không cần `useEffect` riêng. Nhưng luôn phải có 1 trong 2.

## Quy Tắc Loading State

- `loading` = true **trước** khi gọi API, false **sau** khi nhận response (cả success và error)
- `saving` cho form submit, phân biệt với `loading` cho fetch
- Truyền `disabled={saving}` cho submit button khi đang gửi

> Skill `tich-hop-api-ui` và `filter-phan-trang` đã được archive vào `_archived-sasuco/` (viết cho quy ước KetoanApp,
> dùng `PagingUtils`/`ValidationErrorDialog` không tồn tại trong JGameApp) — tham khảo pattern thực tế trong code
> JGameApp (VD: `features/Public/playtime/hooks/useMarketplaceHome.page.fetchData.ts`) thay vì đọc 2 skill đó.
