---
name: tich-hop-api-ui
description: 'Quy trình tích hợp API Service vào UI. Dùng khi: tạo types/hooks kết nối API→UI; hook fetch danh sách / form submit; validate client-side trước API; xử lý response; toàn bộ logic ở hooks, UI chỉ render.'
---

# Tích Hợp API → UI

## LUẬT BẤT DI BẤT DỊCH

```
Page/Dialog/Component → props + callbacks ONLY (KHÔNG ApiService, try/catch, toast)
  Hook (logic)        → useState, validate, gọi service, xử lý response
    ApiService        → apiCall(), buildApiUrl()
```
> ❌ Lỗi #1: gọi `SomeApiService.create(...)` trực tiếp trong component → phải chuyển vào hook.

## Cấu Trúc & Thứ Tự Tạo

Cấu trúc thư mục: xem `cau-truc-du-an`. Thứ tự bắt buộc: **types → services → hooks → components → dialogs → pages → routes**.

---

## 1. Types

- `*.types.api.ts` — 1:1 BE DTO (xem `tao-apiservice`)
- `*.types.ui.ts` — `FormState`, `FormErrors`, `FilterState`
- ❌ KHÔNG dùng request DTO làm form state — tạo `FormState` riêng.

```ts
export interface FeatureFormState { name: string; code: string }
export type FeatureFormErrors = Partial<Record<keyof FeatureFormState, string | null>>
```

---

## 2. Hook Fetch Danh Sách

```ts
export function useFeatureFetchData() {
  const [items, setItems] = useState<Doc[]>([])
  const [paging, setPaging] = useState<PagingInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const r = await FeatureApi.getAll({ search, page, pageSize })
      if (r.success && r.data) { setItems(r.data.items); setPaging(r.data) }
    } catch { /* apiCall tự log */ }
    finally { setLoading(false) }
  }, [search, page, pageSize])

  useEffect(() => { fetchData() }, [fetchData]) // KHÔNG useEffect([],...)

  return { items, paging, loading, search, page, pageSize,
           setSearch, setPage, refetch: fetchData }
}
```
> ⚠️ `useCallback` + `useEffect([fetchData])`, reset page về 1 khi filter đổi.

---

## 3. Hook Form/Submit + Flow

```
BLUR   → validate 1 field, set touched
SUBMIT → validateAll() FAIL → showValidationErrorsToast → RETURN
       → upload (nếu có) FAIL → setServerError → RETURN
       → ApiService.create/update()
           success     → toast.success → onClose → onSuccess
           !success    → setServerError → setServerErrorOpen
           catch       → toast.error('Không thể kết nối...')
       → finally: setSubmitting(false)
```

```ts
export function useFeatureForm({ initialData, onSuccess, onClose }: Props) {
  const buildInitial = (data: typeof initialData) => data ?? { name: '', code: '' }
  const [formData, setFormData] = useState(() => buildInitial(initialData))
  const [errors, setErrors] = useState<FeatureFormErrors>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [submitting, setSubmitting] = useState(false)
  const [serverError, setServerError] = useState<unknown>(null)
  const [serverErrorOpen, setServerErrorOpen] = useState(false)

  // ⚠️ Reset form khi initialData thay đổi (dialog đóng → mở với record khác)
  useEffect(() => {
    setFormData(buildInitial(initialData))
    setErrors({})
    setTouched({})
  }, [initialData])

  const handleBlur = (f: string) => {
    setTouched(p => ({ ...p, [f]: true }))
    // validate field đơn → setErrors
  }
  const validateAll = (): boolean => {
    const errs = validateAllFields({ /* fields */ })
    setTouched(Object.keys(formData).reduce((a,k) => ({...a,[k]:true}), {}))
    setErrors(errs)
    if (hasAnyError(errs)) { showValidationErrorsToast(getAllErrorMessages(errs)); return false }
    return true
  }
  const handleSubmit = async () => {
    if (!validateAll()) return
    setSubmitting(true)
    try {
      const r = await FeatureApi.create(formData)
      if (r.success) { toast.success('Thành công'); onClose(); onSuccess() }
      else { setServerError(r); setServerErrorOpen(true) }
    } catch { toast.error('Không thể kết nối đến máy chủ') }
    finally { setSubmitting(false) }
  }
  return { formData, setFormData, errors, touched, submitting,
           serverError, serverErrorOpen, setServerErrorOpen, handleBlur, handleSubmit }
}
```
> ⚠️ Validate ALL fields cùng lúc, không return sớm. `showValidationErrorsToast` (không `toast.error`).
> ⚠️ Hook phải reset form khi `initialData` thay đổi — dùng `useEffect([initialData])` để set lại `formData`, `errors`, `touched`.

---

## 4. Kết Nối UI

**Page** — chỉ kết nối hook:
```tsx
const { items, paging, loading, setSearch, refetch } = useFeatureFetchData()
// <Dialog open={...} onSuccess={refetch} />
```

**Dialog** — nhận `onSuccess`+`onClose`, giao hook:
```tsx
const { formData, errors, touched, submitting, serverError, serverErrorOpen,
        setServerErrorOpen, handleBlur, handleSubmit } = useFeatureForm({ onSuccess, onClose })
// <ValidationErrorDialog open={serverErrorOpen} error={serverError} title="Lỗi từ máy chủ" ... />
```

**Input error:**
```tsx
<input onBlur={() => handleBlur('name')}
  className={cn(touched.name && errors.name && 'border-destructive',
                touched.name && !errors.name && 'border-success')} />
{touched.name && errors.name && <p className='text-xs text-destructive'>{errors.name}</p>}
```

---

## 5. Xử Lý Lỗi

| Lỗi | Hook | UI |
|-----|------|----|
| Client validation | `validateAll()` → false | Inline error + `showValidationErrorsToast` |
| Server (400/401/403/500) | `result.success===false` | `ValidationErrorDialog` |
| Network | `catch` | `toast.error('Không thể kết nối...')` |

> ❌ `toast.error` cho lỗi server. ❌ `ValidationErrorDialog` cho lỗi client.

---

## 6. Upload File

Xem chi tiết `cdn-upload`. Tóm tắt: preview = `FileReader` (không upload ngay), upload tuần tự trong hook submit, dừng ngay nếu fail, truyền cả `url`+`fileId`.

```ts
if (file) {
  const up = await MediaApi.upload(file)
  if (!up.success) { setServerError(up); return }
  payload.url = up.data.url; payload.fileId = up.data.fileId
}
```

---

## 7. Barrel Export

```ts
// types/index.ts, hooks/index.ts, services/index.ts → named export
// pages/ → KHÔNG index.ts (router import trực tiếp)
```

---

## Checklist

| Mục | Check |
|-----|-------|
| Types: 1:1 BE DTO, FormState riêng, barrel | ☐ |
| Fetch: `useCallback`, `useEffect([fetchData])`, reset page khi filter | ☐ |
| Submit: validateAll 1 lần, showValidationErrorsToast, server→ValidationErrorDialog | ☐ |
| UI: không ApiService/try-catch/toast/logic, ValidationErrorDialog mount trong dialog | ☐ |
| **PAGE_FEATURES: `PAGE_ID` + `PAGE_FEATURES` (bắt buộc, khớp navItem.id)** | ☐ |
| Clean: 1 hook 1 việc, JSDoc tiếng Việt, kebab-case folder, đọc BE docs trước | ☐ |
