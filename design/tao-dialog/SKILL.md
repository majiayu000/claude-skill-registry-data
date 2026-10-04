---
name: tao-dialog
description: 'Tạo Dialog hoặc sửa Dialog, áp dụng component dùng chung và logic từ tao-dialog-new. Đầu vào: mô tả dialog bằng tiếng Việt (các field) hoặc ảnh (Claude model). Tự động đặt tên file theo quy tắc dat-ten. Đảm bảo form reset data mỗi lần đóng/mở dialog. Hỗ trợ cả 2 pattern: Danh Mục CRUD (DmFormField) và Nghiệp Vụ Full-Screen (Label+Input).'
argument-hint: 'Mô tả dialog hoặc ảnh. VD: "Dialog Loại công trình gồm các field: Mã, Tên, Mô tả, Trạng thái" hoặc "Tạo dialog Nhân viên từ ảnh chụp MISA"'
---

# Tạo Dialog / Sửa Dialog — SASUCO InvoiceEasy

> **Kế thừa:** `tao-dialog-new/SKILL.md` (pattern + cấu trúc) + `tao-ui-giao-dien-new/SKILL.md` (component catalog + className chuẩn)
> **Đặt tên file:** `dat-ten/SKILL.md`
> **Xác định phạm vi:** `xac-dinh-pham-vi/SKILL.md`

---

## 0. Workflow Tổng Quan

```
Đầu vào (text / ảnh)
  ↓
Bước 1: Phân tích đầu vào → trích xuất fields, tên đối tượng, loại dialog
  ↓
Bước 2: Sinh shortName + tên file theo dat-ten
  ↓
Bước 3: Xác định phạm vi (tạo mới hay sửa) bằng xac-dinh-pham-vi
  ↓
Bước 4: Chọn Pattern (A: Danh Mục CRUD / B: Nghiệp Vụ)
  ↓
Bước 5: Tạo/Sửa types (.types.api.ts + .types.ui.ts)
  ↓
Bước 6: Tạo/Sửa API Service (nếu chưa có)
  ↓
Bước 7: Tạo/Sửa Hook dialog (use{SN}.dlg.form.ts)
  ↓
Bước 8: Tạo/Sửa Dialog component ({SN}Dialog.tsx)
  ↓
Bước 9: Barrel export (index.ts)
  ↓
Bước 10: Checklist kiểm tra
```

---

## 0. Font Chữ Toàn Cục — TUYỆT ĐỐI Không Ghi Đè

**Global font:** `Inter` (ưu tiên 1) → `InterVariable` → `"Noto Sans"` → `"Open Sans"` → `sans-serif`

> ⚠️ **QUAN TRỌNG:** Font được khai báo tập trung trong `src/styles/globals.css` trên `body` và `html`. **KHÔNG BAO GIỜ** set `font-family` riêng cho bất kỳ element nào trong dialog (`input`, `button`, `label`, `select`, `textarea`, `table`). Tất cả element kế thừa font từ `body`.

**Nguyên nhân font đôi khi khác:**
1. Tailwind v4 dùng `@theme` CSS thay vì `tailwind.config.js` — nếu `--font-sans` không được khai báo trong `@theme inline`, Tailwind fallback về `ui-sans-serif` (Segoe UI trên Windows) thay vì Inter.
2. `font-family` bị set cục bộ trên một component nào đó ghi đè global.

**Quy tắc:**
- ❌ **CẤM:** `className='font-sans'`, `style={{ fontFamily: '...' }}`, hoặc bất kỳ CSS `font-family` nào trên dialog element
- ✅ **ĐÚNG:** Không set `font-family` — để element tự kế thừa từ `body`
- ✅ Nếu component bắt buộc cần font vì bị reset (vd: `button`, `input` trong một số browser): dùng `font-family: inherit`

---

## 1. Phân Tích Đầu Vào

### 1.1 Đầu vào dạng text (tiếng Việt)

Người dùng mô tả dialog bằng tiếng Việt. Agent phải trích xuất:

| Từ mô tả | Trích xuất |
|----------|-----------|
| "Dialog Loại công trình" | Tên đối tượng: `Loại công trình` → `ProjectWorkCategory` |
| "gồm các field: Mã, Tên, Mô tả" | Fields: `code`, `name`, `description` |
| "có tab Thông tin chung, Liên hệ" | Tabs: `tab-chung`, `tab-lien-he` |
| "chọn Nhóm khách hàng từ dropdown" | FK field: `customerGroupId` → `SearchCombobox` |
| "có bảng hạch toán" | Pattern B (Nghiệp Vụ) |
| "trạng thái active/inactive" | Field: `isActive` (boolean) |
| "ngày sinh, giới tính" | Fields: `birthDate` (date), `gender` (enum) |
| "Tổ chức / Cá nhân" | Radio orgType: `organizationType` field |

**Quy tắc dịch tên tiếng Việt → tên field tiếng Anh:**

| Tiếng Việt | Tên field | Loại |
|-----------|----------|------|
| Mã | `code` | string |
| Tên | `name` | string |
| Mô tả / Ghi chú / Diễn giải | `description` / `note` / `explanation` | string |
| Địa chỉ | `address` | string |
| Điện thoại | `phone` / `phoneNumber` | string |
| Email | `email` | string |
| Mã số thuế / MST | `taxCode` | string |
| Ngày sinh | `birthDate` / `dateOfBirth` | date |
| Ngày cấp | `issuedDate` | date |
| Giới tính | `gender` | enum (0: Nam, 1: Nữ, 2: Khác) |
| Trạng thái | `isActive` | boolean |
| Số tiền | `amount` / `totalAmount` | number |
| Số lượng | `quantity` | number |
| Đơn giá | `unitPrice` | number |
| Đơn vị tính | `unitId` / `unitName` | FK |
| Nhóm | `groupId` / `groupName` | FK |
| Loại | `typeId` / `typeName` | FK / enum |
| Người đại diện | `representativeName` | string |
| Chức danh | `position` / `title` | string |
| CMND/CCCD | `identityNumber` | string |
| Nơi cấp | `issuedPlace` | string |
| Số tài khoản | `accountNumber` | string |
| Ngân hàng | `bankName` / `bankId` | string / FK |
| Tỉnh/Thành phố | `provinceId` | FK |
| Quận/Huyện | `districtId` | FK |
| Xã/Phường | `wardId` | FK |

### 1.2 Đầu vào dạng ảnh (Claude model)

Khi người dùng cung cấp ảnh chụp màn hình dialog:

1. Dùng `view_image` để đọc ảnh
2. Phân tích:
   - Tiêu đề dialog → tên đối tượng
   - Các field trong form → tên + loại (text, select, date, checkbox...)
   - Layout: grid hay flex 2 cột, có tab không, có sidebar không
   - Các nút footer: Lưu, Hủy, Lưu & Thêm...
   - Có bảng hạch toán không
   - Có radio Tổ chức/Cá nhân không
3. Nếu ảnh từ MISA hoặc web khác → tham khảo thêm `clone-web-playwright/SKILL.md` và `ve-theo-template/SKILL.md`

### 1.3 Quy Tắc Hiển Thị FK Từ Danh Mục — TableSearchCombobox (BẮT BUỘC)

> ⚠️ **Khi một field tham chiếu đến entity trong danh mục khác, PHẢI dùng `TableSearchCombobox` hiển thị ít nhất Mã + Tên.**

**Nguyên tắc:** Mọi field FK trỏ đến danh mục (khách hàng, nhân viên, kho, đơn vị tính, ngân hàng, tài khoản ngân hàng, hàng hóa, nhóm khách hàng, nhà cung cấp...) → dùng `TableSearchCombobox` với columns `[{ field: 'code', title: 'Mã ...' }, { field: 'name', title: 'Tên ...' }]`.

**Bảng ánh xạ danh mục → TableSearchCombobox columns:**

| Field tiếng Việt | Danh mục tham chiếu | Cột hiển thị mặc định | Cột bổ sung (nếu cần) | API Service |
|---|---|---|---|---|
| Khách hàng | AccountObject | `Mã khách hàng` (code), `Tên khách hàng` (name) | `MST` (taxCode) | `KHApiService` |
| Nhà cung cấp | Supplier | `Mã NCC` (code), `Tên NCC` (name) | `MST` (taxCode) | `NCCApiService` |
| Nhân viên | Employee | `Mã NV` (code), `Tên NV` (name) | `SĐT` (phone) | `NVApiService` |
| Kho / Kho hàng | Warehouse | `Mã kho` (code), `Tên kho` (name) | `Địa chỉ` (address) | `WarehouseApiService` |
| Đơn vị tính | Unit | `Mã ĐVT` (code), `Tên ĐVT` (name) | — | `UnitApiService` |
| Ngân hàng | Bank | `Mã NH` (code), `Tên NH` (name) | — | `BankApiService` |
| Tài khoản ngân hàng | BankAccount | `Số TK` (accountNumber), `Tên TK` (name) | `Ngân hàng` (bankName) | `BankAccountApiService` |
| Loại hàng hóa | GoodsType | `Mã loại` (code), `Tên loại` (name) | — | `GoodsTypeApiService` |
| Hàng hóa / Vật tư | Goods | `Mã HH` (code), `Tên HH` (name) | `ĐVT` (unitName) | `GoodsApiService` |
| Nhóm khách hàng | CustomerGroup | `Mã nhóm` (code), `Tên nhóm` (name) | — | `CustomerGroupApiService` |
| Đối tượng tập hợp CP | CostObject | `Mã ĐT` (code), `Tên ĐT` (name) | — | `CostObjectApiService` |
| Tài khoản ngầm định | DefaultAccount | `Mã TK` (code), `Tên TK` (name) | — | `DefaultAccountApiService` |
| Loại tiền / Tiền tệ | Currency | `Mã tiền` (code), `Tên tiền` (name) | — | `CurrencyApiService` |
| Loại công trình | ProjectWorkCategory | `Mã loại` (code), `Tên loại` (name) | — | `PWCApiService` |
| Điều khoản thanh toán | PaymentTerm | `Mã ĐK` (code), `Tên ĐK` (name) | `Số ngày` (days) | `PTApiService` |
| TK kế toán (hệ thống) | Account | `Số TK` (accountNumber), `Tên TK` (name) | — | (SearchCombobox do quá nhiều bản ghi) |

**Quy tắc bắt buộc:**
1. **Mặc định hiển thị 2 cột: Mã + Tên.** Tên cột tiếng Việt phản ánh đúng nghiệp vụ (VD: "Mã khách hàng" chứ không phải "Mã" chung chung).
2. **Có thể thêm cột thứ 3 nếu user yêu cầu** (VD: MST cho Khách hàng/NCC, SĐT cho Nhân viên, Địa chỉ cho Kho).
3. **Nếu danh mục chưa có API list/search → tạo inbox yêu cầu BE.** Sau đó dùng tạm `DmGroupInput withChevron` và ghi chú `// TODO: CHỜ API — thay bằng TableSearchCombobox`.
4. **Column definitions phải có `width` cụ thể** (VD: `width: 100` cho Mã, `width: 220` cho Tên).
5. **`displayField` là `'name'`** và `onChange` phải set cả id + code + name.

**Pattern code mẫu:**

```tsx
// Column definitions
const xxxColumns: TableComboboxColumn[] = [
  { field: 'code', title: 'Mã khách hàng', width: 100 },
  { field: 'name', title: 'Tên khách hàng', width: 220 },
]

// loadOptions function
const loadXxx = async (keyword: string): Promise<TableComboboxRow[]> => {
  const r = await XxxApiService.list({ pageIndex: 1, pageSize: 30, keyword })
  if (r.success && r.data?.items) {
    return r.data.items.map(x => ({ id: x.id ?? '', code: x.code ?? '', name: x.name ?? '', ...x }))
  }
  return []
}

// Trong JSX
<TableSearchCombobox
  value={formData.customerId}
  initialLabel={formData.customerName}
  displayField='name'
  onChange={(id, rowData) => {
    updateField('customerId', id)
    updateField('customerCode', rowData.code ?? '')
    updateField('customerName', rowData.name ?? '')
  }}
  loadOptions={loadKhachHang}
  columns={khColumns}
  placeholder='Chọn khách hàng...'
  dataQa='sel_khach_hang'
  debounceMs={800}
/>
```

> ⚠️ **Nếu dialog có nhiều FK cùng loại (VD: nhiều dòng chọn khách hàng trong bảng hạch toán), mỗi dòng dùng riêng `TableSearchCombobox` hoặc dùng chung `loadOptions` nhưng state riêng.**

---

## 2. Sinh ShortName & Tên File

> **Quy tắc đầy đủ:** xem `dat-ten/SKILL.md`

### 2.1 Từ tên tiếng Việt → shortName

| Tên đối tượng | Tên tiếng Anh | shortName |
|--------------|---------------|-----------|
| Loại công trình | ProjectWorkCategory | `PWC` |
| Nhóm khách hàng | CustomerGroup | `CG` |
| Điều khoản thanh toán | PaymentTerm | `PT` |
| Loại hàng hóa | GoodsType | `GT` |
| Đơn vị tính | Unit | `U` → giữ nguyên `Unit` (≤2 từ) |
| Kho | Warehouse | `Warehouse` |
| Nhân viên | Employee | `E` → `NV` (theo convention VN) |
| Khách hàng | Customer / AccountObject | `KH` |
| Nhà cung cấp | Supplier | `NCC` |
| Phiếu thu | ReceiptVoucher | `PT` |
| Phiếu chi | PaymentVoucher | `PC` |

> ⚠️ **Ưu tiên shortName theo convention dự án.** Nếu đối tượng đã có shortName trong codebase → dùng lại. Dùng `grep_search` để kiểm tra.

### 2.2 Danh sách file cần tạo

```
features/{nhom}/{ten-feature}/
├── types/
│   └── {SN}.types.api.ts       ← Enums + DTO từ BE
│   └── {SN}.types.ui.ts        ← FormState, initial values, errors type
├── services/
│   └── {SN}ApiService.ts       ← CRUD API
├── hooks/
│   └── use{SN}.dlg.form.ts    ← Hook dialog (submit, validate, init, reset)
├── dialogs/
│   └── {SN}Dialog.tsx          ← Dialog component
└── index.ts                    ← Barrel exports
```

**Tên thư mục feature:** `kebab-case`, phản ánh nghiệp vụ. VD: `loai-cong-trinh`, `nhom-khach-hang`.

---

## 3. Xác Định Phạm Vi — Tạo Mới Hay Sửa

> Dùng `xac-dinh-pham-vi/SKILL.md` để tìm file hiện có.

### 3.1 Tạo mới (không có file cũ)

- Tìm feature trong index: `grep_search` với từ khóa tên đối tượng
- Nếu không thấy → **tạo mới hoàn toàn** → hỏi user xác nhận portal + nhóm feature

### 3.2 Sửa dialog hiện có

- Tìm thấy dialog trong index → đọc file hiện có
- Phân tích diff: cần thêm/xóa/sửa field gì
- **Không sửa những phần không liên quan**
- Nếu thêm field mới → kiểm tra DTO BE đã có chưa, nếu chưa → tạo inbox BE

---

## 4. Chọn Pattern

> Chi tiết pattern: `tao-dialog-new/SKILL.md`

| Điều kiện | Pattern | File mẫu |
|-----------|---------|----------|
| Form phức tạp, bảng hạch toán, full-screen, nhiều section | **B: Full-Screen Nghiệp Vụ** | `PTDialog.tsx` |
| Form đơn giản (≤15 fields), CRUD danh mục, tabs | **A: Dialog Danh Mục CRUD** | `KHFormDialog.tsx` |

> ⚠️ **Quy tắc bảng editable trong dialog:** Nếu dialog có bảng dữ liệu dạng editable (thêm/xóa/sửa dòng) → **BẮT BUỘC load skill `tao-bang-data/SKILL.md`** và dùng component `EditableDataTable` từ `@/modules/KetoanApp/components`. Với các cell cần custom behavior (TableSearchCombobox, disabled có điều kiện...), dùng `render` prop trên `EditableColumnDef`. Không tự viết `<table>` thủ công khi đã có `EditableDataTable`.

### 4.1 Trong Pattern A: Chọn Layout

| Layout | Dùng khi |
|--------|---------|
| `grid grid-cols-5 gap-x-3 gap-y-3` (DmFormField) | Form đều các field, không có sidebar |
| `flex gap-6` 2 cột (Label+Input) | Layout 2 cột trái-phải rõ rệt (Mã+Tên+Đơn vị \| Ngày sinh+Giới tính+CMND) |

---

## 5. Tạo Types

### 5.1 `{SN}.types.api.ts` — Enums + DTO

```tsx
// Enum (nếu có)
export enum XxxStatus {
  Active = 1,
  Inactive = 0,
}

// DTO từ BE
export interface XxxDto {
  id?: string
  code?: string
  name?: string
  description?: string
  isActive?: boolean
  // ... các field khác từ BE
}
```

> ⚠️ **TUYỆT ĐỐI CẤM tự thêm field vào DTO.** Nếu UI cần field mà BE chưa có → tạo inbox/yêu cầu BE bổ sung.

### 5.2 `{SN}.types.ui.ts` — Form State

```tsx
import type { XxxDto } from './{SN}.types.api'

export interface XxxFormState {
  code: string
  name: string
  description: string
  isActive: boolean
  // ... tất cả field UI
}

export const INITIAL_XXX_FORM: XxxFormState = {
  code: '',
  name: '',
  description: '',
  isActive: true,
}

export interface XxxFormErrors {
  code?: string
  name?: string
  description?: string
  // ...
}
```

---

## 6. Tạo API Service

> Pattern đầy đủ: `tao-apiservice/SKILL.md`

```tsx
// {SN}ApiService.ts
import { apiCall, buildApiUrl, ApiResponse, PagingInfo } from '@/shared/services/api'
import type { XxxDto } from '../types/{SN}.types.api'

const BASE_PATH = '/api/xxx/v1/xxx'

export const XxxApiService = {
  async list(params: { pageIndex: number; pageSize: number; keyword?: string }): Promise<ApiResponse<PagingInfo<XxxDto>>> {
    return apiCall(buildApiUrl(BASE_PATH, params))
  },
  async getById(id: string): Promise<ApiResponse<XxxDto>> {
    return apiCall(buildApiUrl(`${BASE_PATH}/${id}`))
  },
  async create(data: Partial<XxxDto>): Promise<ApiResponse<XxxDto>> {
    return apiCall(buildApiUrl(BASE_PATH), { method: 'POST', body: JSON.stringify(data) })
  },
  async update(id: string, data: Partial<XxxDto>): Promise<ApiResponse<XxxDto>> {
    return apiCall(buildApiUrl(`${BASE_PATH}/${id}`), { method: 'PUT', body: JSON.stringify(data) })
  },
  async delete(id: string): Promise<ApiResponse<void>> {
    return apiCall(buildApiUrl(`${BASE_PATH}/${id}`), { method: 'DELETE' })
  },
}
```

---

## 7. Tạo Hook Dialog

> ⚠️ **BẮT BUỘC:** Hook phải reset `formData` mỗi lần dialog mở. Đây là yêu cầu cốt lõi của skill này.

### 7.1 Pattern Hook Chuẩn (Có Reset)

```tsx
// use{SN}.dlg.form.ts
import { useState, useEffect, useCallback } from 'react'
import { validateAllFields, hasAnyError } from '@/shared/utils/ValidationUtils'
import { showValidationErrorsToast } from '@/shared/utils/ValidationToastHelper'
import { XxxApiService } from '../services/{SN}ApiService'
import type { XxxDto } from '../types/{SN}.types.api'
import type { XxxFormState, XxxFormErrors } from '../types/{SN}.types.ui'
import { INITIAL_XXX_FORM } from '../types/{SN}.types.ui'

export function useXxxDialogForm(initialData: XxxDto | null, onSuccess?: () => void) {
  const mode = initialData ? 'edit' as const : 'create' as const

  // ── State ──
  const buildInitial = (data: XxxDto | null): XxxFormState => {
    if (!data) return { ...INITIAL_XXX_FORM }
    return {
      code: data.code ?? '',
      name: data.name ?? '',
      description: data.description ?? '',
      isActive: data.isActive ?? true,
    }
  }

  const [formData, setFormData] = useState<XxxFormState>(() => buildInitial(initialData))
  const [errors, setErrors] = useState<XxxFormErrors>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [submitting, setSubmitting] = useState(false)
  const [serverError, setServerError] = useState<string[] | null>(null)
  const [serverErrorOpen, setServerErrorOpen] = useState(false)

  // ── ⚠️ RESET KHI initialData THAY ĐỔI (BẮT BUỘC) ──
  useEffect(() => {
    setFormData(buildInitial(initialData))
    setErrors({})
    setTouched({})
    setServerError(null)
    setServerErrorOpen(false)
    setSubmitting(false)
  }, [initialData])

  // ── Update field ──
  const updateField = useCallback((field: string, value: unknown) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Xóa lỗi khi user sửa
    setErrors(prev => { const next = { ...prev }; delete next[field as keyof XxxFormErrors]; return next })
  }, [])

  // ── Blur handler ──
  const handleBlur = useCallback((field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }))
    // Validate field đơn
    const value = formData[field as keyof XxxFormState]
    if (field === 'code' && !String(value ?? '').trim()) {
      setErrors(prev => ({ ...prev, code: 'Mã không được để trống' }))
    } else if (field === 'name' && !String(value ?? '').trim()) {
      setErrors(prev => ({ ...prev, name: 'Tên không được để trống' }))
    }
  }, [formData])

  // ── Clear errors ──
  const clearErrors = useCallback(() => {
    setErrors({})
    setTouched({})
    setServerError(null)
    setServerErrorOpen(false)
  }, [])

  // ── Auto fill code ──
  const autoFillCode = useCallback(async () => {
    // Gọi API preview code nếu có
    try {
      const r = await XxxApiService.previewCode?.()
      if (r?.success && r.data) {
        setFormData(prev => ({ ...prev, code: r.data! }))
      }
    } catch { /* ignore */ }
  }, [])

  // ── Validate tất cả fields ──
  const validateAll = useCallback((): boolean => {
    const allErrors: XxxFormErrors = {}
    if (!formData.code?.trim()) allErrors.code = 'Mã không được để trống'
    if (!formData.name?.trim()) allErrors.name = 'Tên không được để trống'
    // ... thêm validate khác

    setErrors(allErrors)
    // Đánh dấu tất cả field đã touched
    const allTouched: Record<string, boolean> = {}
    Object.keys(formData).forEach(k => { allTouched[k] = true })
    setTouched(allTouched)

    if (hasAnyError(allErrors)) {
      showValidationErrorsToast(allErrors)
      return false
    }
    return true
  }, [formData])

  // ── Submit ──
  const handleSubmit = useCallback(async (): Promise<boolean> => {
    if (!validateAll()) return false

    setSubmitting(true)
    setServerError(null)
    try {
      const payload: Partial<XxxDto> = {
        code: formData.code || undefined,
        name: formData.name,
        description: formData.description || undefined,
        isActive: formData.isActive,
      }

      let result
      if (mode === 'edit' && initialData?.id) {
        result = await XxxApiService.update(initialData.id, payload)
      } else {
        result = await XxxApiService.create(payload)
      }

      if (result.success) {
        onSuccess?.()
        return true
      } else {
        setServerError([result.message ?? 'Có lỗi xảy ra'])
        setServerErrorOpen(true)
        return false
      }
    } catch (e: any) {
      setServerError([e?.message ?? 'Có lỗi xảy ra'])
      setServerErrorOpen(true)
      return false
    } finally {
      setSubmitting(false)
    }
  }, [formData, mode, initialData, onSuccess, validateAll])

  return {
    formData, setFormData, updateField, handleBlur, clearErrors, autoFillCode,
    errors, touched, submitting, mode,
    serverError, serverErrorOpen, setServerErrorOpen,
    handleSubmit, validateAll,
  }
}
```

### 7.2 Pattern Reset Khi Có `open` Prop (Khuyến nghị)

Khi dialog không unmount (chỉ ẩn/hiện), `useEffect([initialData])` có thể không chạy nếu `initialData` cùng tham chiếu. Pattern an toàn hơn:

```tsx
// Hook nhận thêm `open`
export function useXxxDialogForm(initialData: XxxDto | null, onSuccess?: () => void, open?: boolean) {
  // ...

  // Reset khi dialog mở HOẶC initialData thay đổi
  useEffect(() => {
    if (open === false) return        // <-- QUAN TRỌNG: không reset khi đóng
    setFormData(buildInitial(initialData))
    setErrors({})
    setTouched({})
    setServerError(null)
    setServerErrorOpen(false)
    setSubmitting(false)
  }, [initialData, open])
}
```

**Gọi từ component:**
```tsx
const hookData = useXxxDialogForm(editMode ? initialData : null, onSuccess, open)
```

---

## 8. Tạo Dialog Component

### 8.0 Quy Tắc Mặc Định Khi Tạo Dialog

> ⚠️ **Các quy tắc sau áp dụng cho MỌI dialog được tạo ra từ skill này.**

| # | Quy tắc | Mô tả |
|---|---------|-------|
| 1 | **Không thêm `placeholder`** | Mặc định KHÔNG thêm `placeholder` cho input, select, datepicker, textarea. Chỉ thêm `placeholder` khi user yêu cầu cụ thể. |
| 2 | **Label `font-bold`** | Tất cả label trong dialog (DmFormField, Label, DmTabFieldValue) đều dùng `font-bold`. Đối với Pattern A: `DmFormField` tự xử lý. Đối với Pattern B: `className='text-[13px] font-bold text-black'`. |
| 3 | **Border `#AEB3BA`** | Tất cả input, select, datepicker, textarea dùng `border-[#AEB3BA]`. |
| 4 | **Không `border-b` ở header** | Header dialog KHÔNG có `border-b`. Chỉ `border-t` ở footer dialog dùng `border-[#AEB3BA]`. |
| 5 | **Font `text-[13px]` đồng bộ page** | Font chữ trong dialog đồng bộ với page bên ngoài: `text-[13px]` cho label, input, select, datepicker, textarea, view mode. Pattern A: `DmFormField`/`DmFormInput` tự xử lý. Pattern B: thêm `text-[13px]` vào `Label` và `Input`. View mode: `<div className='text-[13px] text-black'>`. |
| 6 | **FK danh mục → `TableSearchCombobox`** | Mọi field FK trỏ đến danh mục khác (Khách hàng, NCC, Nhân viên, Kho, ĐVT, Ngân hàng, TK ngân hàng, Hàng hóa, Nhóm KH, ĐT THCP...) **PHẢI** dùng `TableSearchCombobox` hiển thị ít nhất **Mã + Tên** (code + name). Nếu danh mục chưa có API → tạo inbox BE, dùng tạm `DmGroupInput`. Xem chi tiết → [Section 1.3](#13-quy-tắc-hiển-thị-fk-từ-danh-mục--tablesearchcombobox-bắt-buộc). |

### 8.1 Pattern A — Dialog Danh Mục CRUD

```tsx
// {SN}Dialog.tsx
import { useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'
import { X } from 'lucide-react'
import { ValidationErrorDialog } from '@/shared/components/common'
import {
  DmFormField, DmFormInput, DmFormTextarea,
  DmFieldValue, DmDialogFooter,
} from '@/modules/KetoanApp/components'
import { useXxxDialogForm } from '../hooks/use{SN}.dlg.form'
import type { XxxDto } from '../types/{SN}.types.api'

interface Props {
  open: boolean
  onOpenChange: (v: boolean) => void
  initialData?: XxxDto | null
  viewOnly?: boolean
  onSuccess?: () => void
}

export function XxxDialog({ open, onOpenChange, initialData, viewOnly, onSuccess }: Props) {
  const isView = viewOnly === true
  const isCreate = !initialData
  const editMode = !!initialData && !isView
  const isReadonly = isView

  const {
    formData, updateField, handleBlur, clearErrors, autoFillCode,
    errors, submitting, mode,
    serverError, serverErrorOpen, setServerErrorOpen,
    handleSubmit,
  } = useXxxDialogForm(editMode ? initialData : null, onSuccess)

  const f = formData as Record<string, unknown>

  // Init khi mở dialog
  useEffect(() => {
    if (!open) { clearErrors(); return }
    if (mode === 'create') autoFillCode()
  }, [open, clearErrors, autoFillCode, mode])

  const doSubmit = async () => {
    const ok = await handleSubmit()
    if (!ok) return
    onOpenChange(false)
  }

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent maxWidth='920px' className='max-h-[90vh] flex flex-col gap-0 p-0 overflow-hidden'>

          {/* ── Header ── */}
          <DialogHeader className='flex-none px-5 py-3'>
            <div className='flex items-center gap-2'>
              <DialogTitle className='text-[20px] font-bold text-gray-900 shrink-0'>
                {isCreate ? 'Thêm mới' : isView ? 'Xem chi tiết' : 'Chỉnh sửa'} {tên đối tượng}
              </DialogTitle>
              <Button variant='ghost' size='sm'
                className='ml-auto h-7 w-7 p-0 text-gray-400 hover:text-gray-600 rounded-[8px]'
                onClick={() => onOpenChange(false)} data-qa='btn_dong_dialog'>
                <X className='h-4 w-4' />
              </Button>
            </div>
          </DialogHeader>

          {/* ── Body ── */}
          <div className='flex-1 min-h-0 overflow-y-auto px-5 py-4'>
            <form id='xxx-form' onSubmit={(e) => { e.preventDefault(); doSubmit() }}>
              <div className='grid grid-cols-5 gap-x-3 gap-y-3'>

                <DmFormField label='Mã' required error={errors.code} tooltip='Tự động tạo nếu để trống'>
                  {isReadonly
                    ? <DmFieldValue value={f.code as string} />
                    : <DmFormInput data-qa='i_code'
                        value={(f.code as string) ?? ''}
                        onChange={(e) => updateField('code', e.target.value)}
                        onBlur={() => handleBlur('code')}
                        placeholder='' />}
                </DmFormField>

                <DmFormField label='Tên' required className='col-span-4' error={errors.name}>
                  {isReadonly
                    ? <DmFieldValue value={f.name as string} />
                    : <DmFormInput data-qa='i_name'
                        value={(f.name as string) ?? ''}
                        onChange={(e) => updateField('name', e.target.value)}
                        onBlur={() => handleBlur('name')} />}
                </DmFormField>

                <DmFormField label='Mô tả' className='col-span-5'>
                  {isReadonly
                    ? <DmFieldValue value={f.description as string} />
                    : <DmFormTextarea data-qa='i_description' rows={2}
                        value={(f.description as string) ?? ''}
                        onChange={(e) => updateField('description', e.target.value)} />}
                </DmFormField>

              </div>
            </form>
          </div>

          {/* ── Footer ── */}
          <DmDialogFooter
            isView={isView}
            submitting={submitting}
            onClose={() => onOpenChange(false)}
            onSave={() => doSubmit()}
          />

          <ValidationErrorDialog
            open={serverErrorOpen}
            onOpenChange={setServerErrorOpen}
            errors={serverError}
          />
        </DialogContent>
      </Dialog>
    </>
  )
}
```

### 8.2 Pattern B — Full-Screen Nghiệp Vụ

Xem chi tiết trong `tao-dialog-new/SKILL.md` Section 2. Cấu trúc chính:

```tsx
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent maxWidth='none'
    className='w-[100vw] max-w-[100vw] h-[100vh] max-h-[100vh] p-0 gap-0
      rounded-none shadow-[0_5px_20px_rgba(0,0,0,0.1)] border-0
      flex flex-col bg-white overflow-hidden [&>button:first-child]:hidden'>
    {/* Header: title + select + tổng tiền + nút X */}
    {/* Body: flex gap-6 (main + sidebar) + bảng hạch toán */}
    {/* Footer: Hủy + Lưu (btn-secondary + btn-primary) */}
  </DialogContent>
</Dialog>
```

---

## 9. Barrel Export

```tsx
// index.ts
export { XxxDialog } from './dialogs/{SN}Dialog'
export { useXxxDialogForm } from './hooks/use{SN}.dlg.form'
export { XxxApiService } from './services/{SN}ApiService'
export type { XxxDto } from './types/{SN}.types.api'
export type { XxxFormState, XxxFormErrors } from './types/{SN}.types.ui'
```

---

## 10. Xử Lý Ảnh Đầu Vào (Claude Model)

Khi nhận ảnh chụp màn hình dialog:

1. **`view_image`** để đọc ảnh
2. **Phân tích layout:**
   - Tiêu đề → tên đối tượng
   - Các field → tên + loại (text, select, date, checkbox)
   - Grid layout → Pattern A grid-cols-5 hay flex 2 cột
   - Tabs → nội dung từng tab
   - Footer → các nút
   - Có bảng hạch toán → Pattern B
3. **Đối chiếu với convention:**
   - Field MISA có mà BE chưa có → render UI, gửi qua formData, tạo inbox BE
   - Không tự ý thêm/bớt field so với ảnh
   - Giữ nguyên thứ tự field như trong ảnh
   - Giữ nguyên tên tab như trong ảnh
4. **Sinh code** theo pattern tương ứng

---

## 11. Reset Form Khi Đóng/Mở Lại (BẮT BUỘC)

> ⚠️ **Đây là yêu cầu cốt lõi của skill `tao-dialog`.** Mọi dialog tạo ra PHẢI reset đúng cách.

| Tình huống | Hành vi đúng | Cách implement |
|-----------|-------------|---------------|
| Đóng dialog → mở lại với record khác | Form reset về giá trị từ `initialData` mới | `useEffect([initialData])` trong hook |
| Đóng dialog → mở lại để tạo mới | Form trắng, `autoFillCode()` chạy lại | `useEffect([open])` với `if (!open) return` |
| Chuyển từ edit record A → edit record B (không đóng dialog) | Form cập nhật theo record B | `useEffect([initialData?.id])` |
| Đóng dialog → mở lại View cùng record | Form hiển thị đúng `initialData` | `useEffect([open, initialData?.id])` |

### Pattern An Toàn Nhất (Khuyến nghị)

```tsx
// Trong hook:
useEffect(() => {
  if (open === false) return        // Không reset khi đóng
  setFormData(buildInitial(initialData))
  setErrors({})
  setTouched({})
  setServerError(null)
  setServerErrorOpen(false)
  setSubmitting(false)
}, [initialData, open])             // Cả 2 dependency

// Trong component:
const hookData = useXxxDialogForm(
  editMode ? initialData : null,
  onSuccess,
  open,                             // Truyền open vào hook
)
```

---

## 12. Checklist Trước Commit

- [ ] Đã xác định đúng portal + nhóm feature (`xac-dinh-pham-vi`)
- [ ] Chọn đúng pattern (A: Danh Mục / B: Nghiệp Vụ)
- [ ] Sinh đúng shortName + tên file (`dat-ten`)
- [ ] Types: DTO khớp BE, không tự thêm field
- [ ] API Service: đúng `BASE_PATH`, CRUD đầy đủ
- [ ] Hook: có `useEffect` reset khi `initialData` hoặc `open` thay đổi
- [ ] **Label `font-bold`:** tất cả label trong dialog dùng `font-bold` (Pattern B: `font-bold text-black`; Pattern A: DmFormField tự xử lý)
- [ ] **Không thêm `placeholder`** mặc định cho input/select/datepicker/textarea
- [ ] **Border `#AEB3BA`:** input, select, datepicker, textarea dùng `border-[#AEB3BA]`
- [ ] **Không `border-b` ở header:** header dialog không có `border-b`, chỉ `border-t` ở footer dùng `border-[#AEB3BA]`
- [ ] **Font `text-[13px]` đồng bộ page:** label, input, select, datepicker, textarea, view mode dùng `text-[13px]` (Pattern B: `Label` và `Input` thêm `text-[13px]`)
- [ ] Dialog: `maxWidth` đúng, 3 mode (View/Create/Edit)
- [ ] `isReadonly` flag cho tất cả fields
- [ ] Validate onBlur + inline error message
- [ ] `ValidationErrorDialog` cho lỗi server
- [ ] `data-qa` đầy đủ (`btn_`, `i_`, `sel_`, `dt_`, `chk_`, `r_`, `tab_`)
- [ ] View mode hiển thị `<div>` / `DmFieldValue` (không dùng disabled input)
- [ ] Input số: `type='text' inputMode='numeric'` (Pattern B)
- [ ] Footer đúng: mặc định [Hủy] [Lưu], "Lưu & Thêm" chỉ khi user yêu cầu
- [ ] Nút X close custom (ẩn mặc định Radix)
- [ ] `SearchCombobox` / `TableSearchCombobox` có `initialLabel` khi sửa
- [ ] ⚠️ **FK ID resolve:** nếu combobox `value` là ID nhưng DTO không có → thêm `useEffect` resolve FK ID (xem `tao-dialog-new` 3.1.1)
- [ ] ⚠️ **FK danh mục dùng `TableSearchCombobox`:** mọi field FK trỏ đến danh mục phải hiển thị dạng `TableSearchCombobox` với ít nhất Mã + Tên. Nếu danh mục chưa có API → tạo inbox BE, dùng tạm `DmGroupInput`. (xem Section 1.3)
- [ ] Barrel `index.ts` export dialog
- [ ] ⚠️ **Reset state khi đóng/mở lại dialog:** form phải theo giá trị mới, không giữ giá trị cũ
- [ ] Compile không lỗi, TypeScript check pass

---

## 13. Kế Thừa & Liên Kết Skill

| Khi cần | Load skill |
|---------|-----------|
| Xác định file cần sửa | `xac-dinh-pham-vi/SKILL.md` |
| Pattern dialog chi tiết | `tao-dialog-new/SKILL.md` |
| Component catalog + className | `tao-ui-giao-dien-new/SKILL.md` |
| Quy tắc UI nền tảng | `tao-ui-giao-dien/SKILL.md` |
| Đặt tên file | `dat-ten/SKILL.md` |
| Tạo API Service | `tao-apiservice/SKILL.md` |
| Validate input | `validate-input/SKILL.md` |
| Cấu trúc thư mục | `cau-truc-du-an/SKILL.md` |
| Quy tắc code TS/React | `quy-tac-code/SKILL.md` |
| Filter + phân trang (nếu có master page) | `filter-phan-trang/SKILL.md` |
| Thêm nút "+" tạo nhanh FK | `them-nhanh-fk/SKILL.md` |
| DatePicker / ngày tháng | `date-input/SKILL.md` |
| **Tạo bảng dữ liệu editable trong dialog** | `tao-bang-data/SKILL.md` |
| Clone web bằng Playwright | `clone-web-playwright/SKILL.md` |
| Vẽ theo ảnh template | `ve-theo-template/SKILL.md` |
| Checklist sau code | `checklist-sau-code/SKILL.md` |

---

## 14. Ví Dụ Cụ Thể

### Ví dụ 1: "Tạo dialog Loại công trình gồm field Mã, Tên, Mô tả"

1. **Phân tích:** Tên = "Loại công trình" → `ProjectWorkCategory`, shortName = `PWC`
2. **Pattern:** A (Danh Mục CRUD, 3 fields)
3. **Files:**
   - `features/danh-muc/loai-cong-trinh/types/PWC.types.api.ts`
   - `features/danh-muc/loai-cong-trinh/types/PWC.types.ui.ts`
   - `features/danh-muc/loai-cong-trinh/services/PWCApiService.ts`
   - `features/danh-muc/loai-cong-trinh/hooks/usePWC.dlg.form.ts`
   - `features/danh-muc/loai-cong-trinh/dialogs/PWCDialog.tsx`
   - `features/danh-muc/loai-cong-trinh/index.ts`
4. **Layout:** `grid-cols-5`, Mã (1 cột) + Tên (3 cột) + Mô tả (5 cột)

### Ví dụ 2: "Sửa dialog Nhân viên, thêm field Số điện thoại"

1. **Xác định phạm vi:** `grep_search` tìm `NVFormDialog.tsx`
2. **Đọc file hiện có:** dialog + hook + types
3. **Kiểm tra DTO:** `phone` đã có trong `EmployeeDto` chưa?
   - Có → thêm field vào form
   - Chưa → tạo inbox BE → chờ → mới thêm
4. **Sửa files:**
   - `NV.types.ui.ts`: thêm `phone: string` vào `EmployeeFormState`
   - `useNV.dlg.form.ts`: thêm validate cho `phone`
   - `NVFormDialog.tsx`: thêm `<DmFormField label='Điện thoại'>`
5. **KHÔNG sửa:** các field khác, layout khác không liên quan

### Ví dụ 3: "Tạo dialog từ ảnh chụp MISA"

1. `view_image` → phân tích ảnh
2. Trích xuất: tên dialog, danh sách field, tabs, layout
3. Đối chiếu convention → chọn pattern
4. Sinh code như ví dụ 1
5. Field MISA có mà BE chưa có → tạo inbox BE
