---
name: tao-dialog-new
description: 'Quy tắc tạo Dialog/Form MỚI cho KetoanApp — 2 pattern từ code thực tế: Full-Screen Nghiệp Vụ (PTDialog.tsx) và Dialog Danh Mục CRUD (KHFormDialog.tsx). Cấu trúc: Header→Body→Footer, 3 mode (View/Create/Edit), DmFormField hoặc Label+Input, validate onBlur, SearchCombobox/TableSearchCombobox FK, view mode div/DmFieldValue. Kế thừa tao-ui-dialog/SKILL.md + b0/Component Catalog.'
argument-hint: 'Mô tả dialog cần tạo. VD: Dialog Loại công trình (ProjectWorkCategory) với fields: code, name, description, isActive'
---

# Tạo Dialog Mới — 2 Pattern Từ Code Thực Tế

> **Nguồn tham khảo:** `PTDialog.tsx` (Phiếu thu Full-Screen) + `KHFormDialog.tsx` (Khách hàng CRUD)
> **Foundation:** `tao-ui-dialog/SKILL.md` (pattern gốc) + `b0/SKILL.md` (Component Catalog)
> **Kiểm tra:** `check-dialog.cjs` (từ `tao-ui-dialog`)
> **KHÔNG tạo master page ở đây.** Master page → `tao-ui-master-page-2/SKILL.md`

---

## 0. Chọn Pattern

| Điều kiện | Pattern | File mẫu |
|-----------|---------|----------|
| Form phức tạp, bảng hạch toán, full-screen, nhiều section | **Full-Screen Nghiệp Vụ** | `PTDialog.tsx` |
| Form đơn giản (≤15 fields), CRUD danh mục, tabs | **Dialog Danh Mục CRUD** | `KHFormDialog.tsx` |

> **Quyết định dựa trên:** có bảng hạch toán không? → Full-Screen. Còn lại → Danh Mục CRUD.

### 0.3 Form Có Tổ Chức / Cá Nhân — 2 Layout Riêng Biệt

> ⚠️ **BẮT BUỘC:** Khi dialog có radio "Tổ chức / Cá nhân", phải thiết kế **CẢ 2 layout riêng biệt** với `orgType` state (`0` = Tổ chức, `1` = Cá nhân).

```tsx
// State
const [orgType, setOrgType] = useState(initialData?.orgType ?? 0)

// Header
<label className='flex items-center gap-1.5 cursor-pointer select-none text-[13px]'>
  <input type='radio' checked={orgType===0} onChange={() => setOrgType(0)}
    className='accent-primary' data-qa='r_to_chuc' /> Tổ chức
</label>
<label className='flex items-center gap-1.5 cursor-pointer select-none text-[13px]'>
  <input type='radio' checked={orgType===1} onChange={() => setOrgType(1)}
    className='accent-primary' data-qa='r_ca_nhan' /> Cá nhân
</label>

// Body — 2 grid khác nhau
{orgType === 0 ? (
  <div className='grid grid-cols-5 gap-x-3 gap-y-3'>
    {/* Fields Tổ chức: Mã, Tên, MST, Người đại diện, Chức danh... */}
  </div>
) : (
  <div className='grid grid-cols-3 gap-x-3 gap-y-3'>
    {/* Fields Cá nhân: Mã, Tên, Ngày sinh, Giới tính, CMND... */}
  </div>
)}
```

**Quy tắc:**
- Fields chung (Mã, Tên, Địa chỉ...) → có trong cả 2 grid
- Fields riêng Tổ chức (MST, Người đại diện, Chức danh...) → chỉ trong grid `orgType === 0`
- Fields riêng Cá nhân (Ngày sinh, Giới tính, CMND...) → chỉ trong grid `orgType === 1`
- **Không tự ý thêm field của chế độ này vào chế độ kia**

### 0.4 Quy Tắc Field Thiếu — Cấm Tự Thêm Vào Type (BẮT BUỘC)

> ⚠️ **TUYỆT ĐỐI CẤM:** Tự ý thêm field vào `types.api.ts` (DTO). Nếu UI cần field mà BE DTO chưa có:

| Tình huống | Hành động đúng | Hành động sai |
|-----------|---------------|--------------|
| UI cần field X, DTO BE chưa có X | **DỪNG** — tạo inbox/yêu cầu BE bổ sung | ❌ Tự thêm `fieldX: string` vào DTO |
| Clone ra nhiều field hơn DTO | **Báo cáo danh sách field thiếu** → chờ BE | ❌ Tự map tất cả vào type |

**Lý do:** BE và FE phải thống nhất DTO. FE tự thêm field vào type nhưng BE không có → API lỗi hoặc mất dữ liệu.

### 0.5 Chọn Layout Trong Pattern A: Grid vs Flex 2 Cột

Pattern A (Danh Mục CRUD) có **2 kiểu layout** bên trong body:

| Layout | Dùng khi | File mẫu |
|--------|---------|----------|
| **grid-cols-5 (DmFormField)** | Form đều các field, không có sidebar, field xếp theo grid | `KHFormDialog.tsx` |
| **flex gap-6 2 cột (Label+Input)** | Form có 2 cột rõ rệt: trái form chính (Mã, Tên, Đơn vị, Chức danh...) + phải sidebar (Ngày sinh, CMND, Nơi cấp...) | `NVFormDialog.tsx` |

> **Quy tắc chọn layout:** Nếu clone từ MISA thấy layout chia 2 cột trái-phải rõ rệt → dùng flex. Nếu field xếp đều thành lưới → dùng grid-cols-5.

**Layout flex 2 cột:**
```tsx
<div className='flex gap-6'>
  {/* Cột trái: form chính */}
  <div className='flex-1 space-y-3'>
    {/* Label + Input / DmGroupInput */}
  </div>
  {/* Cột phải: sidebar */}
  <div className='w-[300px] flex-shrink-0 space-y-3'>
    {/* Ngày sinh, giới tính, CMND, ngày cấp, nơi cấp... */}
  </div>
</div>
```

> ⚠️ **Bài học từ Nhân viên:** Không phải mọi danh mục CRUD đều dùng `grid-cols-5`. Phải xem clone MISA để xác định layout chính xác. Dùng sai layout → dialog không giống bản gốc, thiếu field.

---

## 1. Pattern A — Dialog Danh Mục CRUD (KHFormDialog.tsx)

> **Dùng khi:** Form danh mục (Khách hàng, Nhà cung cấp, Nhân viên, Hàng hóa, Loại công trình...)
> **Đặc điểm:** `maxWidth='920px'`, DmFormField, DmDialogFooter, Tabs bên dưới form

### 1.1 Import

```tsx
import { useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'
import { Tabs, TabsList, TabsContent } from '@/shared/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { X } from 'lucide-react'
import { ValidationErrorDialog } from '@/shared/components/common'
import {
  DmFormField, DmFormInput, DmFormTextarea,
  DmFieldValue, DmTabFieldValue, DmGroupInput, DmDialogFooter,
} from '@/modules/KetoanApp/components'
import DmTabTrigger from '@/modules/KetoanApp/components/DMTabTrigger'
```

### 1.2 Props Interface

```tsx
interface Props {
  open: boolean
  onOpenChange: (v: boolean) => void
  initialData?: XxxDto | null         // undefined = create, có giá trị = edit
  viewOnly?: boolean                   // true = view mode
  onSuccess?: () => void
}
```

### 1.3 3 Mode Logic

```tsx
export function XxxDialog({ open, onOpenChange, initialData, viewOnly, onSuccess }: Props) {
  const isView = viewOnly === true
  const isCreate = !initialData
  const editMode = !!initialData && !isView
  const isReadonly = isView

  const {
    formData, setFormData, updateField, handleBlur, clearErrors, autoFillCode,
    errors, submitting, mode,
    serverError, serverErrorOpen, setServerErrorOpen,
    handleSubmit,
  } = useXxxDialogForm(editMode ? initialData : null)

  const f = formData as Record<string, unknown>

  // Init khi mở dialog
  useEffect(() => {
    if (!open) { clearErrors(); return }
    // Reset về initialData mới khi dialog mở lại với record khác
    if (editMode && initialData) {
      setFormData(buildFormState(initialData))
    } else if (mode === 'create') {
      setFormData(INITIAL_FORM as Record<string, unknown>)
      autoFillCode()
    }
  }, [open, initialData?.id]) // dùng id để detect record thay đổi khi chuyển giữa các record

  // Submit logic
  const doSubmit = async () => {
    const ok = await handleSubmit()
    if (!ok) return
    onSuccess?.()
    onOpenChange(false)
  }
```

### 1.4 Dialog Wrapper

```tsx
  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent maxWidth='920px' className='max-h-[90vh] flex flex-col gap-0 p-0 overflow-hidden'>

          {/* ── Header ── */}
          <DialogHeader className='flex-none px-5 py-3 border-b border-[#B7BCC3]'>
            <div className='flex items-center gap-2'>
              <DialogTitle className='text-[20px] font-bold text-gray-900 shrink-0'>
                {isCreate ? 'Thêm mới' : isView ? 'Xem chi tiết' : 'Chỉnh sửa'} {tên đối tượng}
              </DialogTitle>

              {/* Optional: radio/checkbox controls in header */}
              {/* <label><input type='radio' ... /> Tổ chức</label> */}

              <Button variant='ghost' size='sm'
                className='ml-auto h-7 w-7 p-0 text-gray-400 hover:text-gray-600 rounded-[8px]'
                onClick={() => onOpenChange(false)} data-qa='btn_dong_dialog'>
                <X className='h-4 w-4' />
              </Button>
            </div>
          </DialogHeader>
```

### 1.5 Body — Grid Form

```tsx
          {/* ── Body ── */}
          <div className='flex-1 min-h-0 overflow-y-auto px-5 py-4'>
            <form id='xxx-form' onSubmit={(e) => { e.preventDefault(); doSubmit() }}>

              {/* Grid form: 5 cột mặc định */}
              <div className='grid grid-cols-5 gap-x-3 gap-y-3'>

                <DmFormField label='Mã' required error={errors.code} tooltip='Tự động tạo nếu để trống'>
                  {isReadonly ? <DmFieldValue value={f.code as string} />
                    : <DmFormInput data-qa='i_code'
                        value={(f.code as string) ?? ''}
                        onChange={(e) => updateField('code', e.target.value)}
                        onBlur={() => handleBlur('code')} />}
                </DmFormField>

                <DmFormField label='Tên' required className='col-span-3' error={errors.name}>
                  {isReadonly ? <DmFieldValue value={f.name as string} />
                    : <DmFormInput data-qa='i_name'
                        value={(f.name as string) ?? ''}
                        onChange={(e) => updateField('name', e.target.value)}
                        onBlur={() => handleBlur('name')} />}
                </DmFormField>

                <DmFormField label='Nhóm' className='col-span-2'>
                  {isReadonly ? <DmFieldValue value={f.groupName as string} />
                    : <DmGroupInput withChevron
                        value={(f.groupName as string) ?? ''}
                        onChange={(v) => updateField('groupName', v)}
                        placeholder='Chọn nhóm'
                        dataQa='i_group' />}
                </DmFormField>

                <DmFormField label='Địa chỉ' className='col-span-3'>
                  {isReadonly ? <DmFieldValue value={f.address as string} />
                    : <DmFormTextarea data-qa='i_address' rows={2}
                        value={(f.address as string) ?? ''}
                        onChange={(e) => updateField('address', e.target.value)} />}
                </DmFormField>

              </div>
            </form>

            {/* ── Tabs (nếu có) ── */}
            <div className='mt-4 rounded-[8px] overflow-hidden'>
              <Tabs defaultValue='tab-1' className='gap-0'>
                <TabsList className='w-full justify-start h-auto bg-transparent border-b border-[#B7BCC3] p-0 gap-1 overflow-x-auto rounded-none'>
                  <DmTabTrigger value='tab-1'>Tab 1</DmTabTrigger>
                  <DmTabTrigger value='tab-2'>Tab 2</DmTabTrigger>
                </TabsList>
                <TabsContent value='tab-1' className='m-0 p-4 h-[280px] overflow-y-auto border border-[#B7BCC3]'>
                  {/* Tab content — dùng DmTabFieldValue / DmFormInput */}
                </TabsContent>
              </Tabs>
            </div>
          </div>
```

### 1.6 Footer — DmDialogFooter (mặc định: Hủy + Lưu)

> ⚠️ **QUY TẮC MẶC ĐỊNH:** Footer chỉ gồm **[Hủy] [Lưu]**. Nút **"Lưu & Thêm"** chỉ thêm khi user yêu cầu riêng.

```tsx
          <DmDialogFooter
            isView={isView}
            submitting={submitting}
            onClose={() => onOpenChange(false)}
            onSave={() => doSubmit()}
          />
```

**Khi user yêu cầu "Lưu & Thêm":**

```tsx
          <DmDialogFooter
            isView={isView}
            isCreate={isCreate}
            submitting={submitting}
            onClose={() => onOpenChange(false)}
            onSave={() => doSubmit(false)}
            onSaveAndAdd={() => doSubmitAndNew()}
          />
```

### 1.7 Error Dialog

```tsx
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

### 1.8 DmFormField Pattern

```tsx
// Pattern cố định cho MỌI field trong grid:
<DmFormField label='Nhãn' required error={errors.fieldName} tooltip='Giải thích' className='col-span-X'>
  {isReadonly
    ? <DmFieldValue value={value} />
    : <DmFormInput data-qa='i_field'
        value={value}
        onChange={(e) => updateField('field', e.target.value)}
        onBlur={() => handleBlur('field')} />}
</DmFormField>
```

| Component | Dùng khi |
|-----------|---------|
| `DmFormInput` | Text ngắn (code, name, phone, email...) |
| `DmFormTextarea` | Text dài (address, description) + `rows={2}` |
| `DmGroupInput withChevron` | FK chọn từ danh sách (nhóm KH, nhân viên...) |
| `DmFieldValue` | View mode — hiển thị text thuần |
| `DmTabFieldValue` | View mode trong tab — `label='...' value={...}` |
| `Select` | Enum cố định (giới tính, trạng thái...) |

### 1.9 Quy Tắc Tabs Trong Dialog

| Quy tắc | Pattern | Lý do |
|---------|---------|-------|
| **Tất cả TabsContent cùng chiều cao** | `h-[280px] overflow-y-auto` | Không bị nhảy layout khi đổi tab |
| **Border ở TabsContent** | `border border-[#B7BCC3]` | Phân biệt nội dung với tab header |
| **Tab mặc định khớp MISA** | `defaultValue` = tab đầu tiên bên MISA | Giữ UX nhất quán |
| **Tên tab giữ nguyên từ MISA** | Không tự ý đổi tên tab | Tránh sai lệch nghiệp vụ |
| **Mỗi tab có fields khác nhau** | Không tự phân phối fields giữa các tab | Tab Tiền lương ≠ Tab Liên hệ |
| **Click từng tab khi clone** | Dùng nhiều selector (MISA không dùng role=tab) | `button:has-text()` hoặc `.ms-tabs-btn` |
| **Đối chiếu với BE DTO** | Field MISA có mà BE chưa có → tạo inbox BE | Tránh submit field không tồn tại |

> ⚠️ **KHÔNG để TabsContent không có chiều cao cố định** — sẽ gây nhảy layout.
> ⚠️ **KHÔNG tự ý phân phối fields giữa các tab** — mỗi tab có nội dung khác nhau theo MISA. Ví dụ: Tab "Tiền lương" chỉ chứa fields lương (không có phone, email, địa chỉ).
> ⚠️ **KHÔNG tự ý thêm/bớt tab** so với MISA.

**Ví dụ phân phối fields cho Nhân viên (NVFormDialog.tsx):**
```
Tab "Thông tin tiền lương": MST, Lương thỏa thuận, Hệ số lương, Lương đóng BH, Loại HĐ, Số người phụ thuộc
Tab "Tài khoản ngân hàng": DmBankAccountsTab
Tab "Thông tin liên hệ": Điện thoại, Di động, Email, Người liên hệ, Địa chỉ, Ghi chú
```

---

## 2. Pattern B — Full-Screen Nghiệp Vụ (PTDialog.tsx)

> **Dùng khi:** Chứng từ kế toán (Phiếu thu, Phiếu chi, Hóa đơn...), form có bảng hạch toán, nhiều section.

### 2.1 Import

```tsx
import { useEffect, useRef, useState } from 'react'
import { Dialog, DialogContent } from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { Label } from '@/shared/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { Loader2, X, Plus, Trash2, AlertCircle } from 'lucide-react'
import { DatePicker } from '@/shared/components/common'
import { SearchCombobox } from '@/shared/components/common'
import { TableSearchCombobox } from '@/shared/components/common'
import { ValidationErrorDialog, ConfirmDialog } from '@/shared/components/common'
import { cn } from '@/shared/components/ui/utils'
import { formatCurrency, formatNumber } from '@/shared/utils'
```

### 2.2 Props Interface

```tsx
interface PTDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  editingId?: string | null     // null/undefined = create
  defaultMode?: 'view' | 'edit' | 'create'
  onSuccess: () => void
}
```

### 2.3 Dialog Wrapper (Full-Screen)

```tsx
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent
    maxWidth='none'
    className='w-[100vw] max-w-[100vw] h-[100vh] max-h-[100vh] p-0 gap-0
      rounded-none shadow-[0_5px_20px_rgba(0,0,0,0.1)] border-0
      flex flex-col bg-white overflow-hidden [&>button:first-child]:hidden'
  >
    {/* Header + Body + Footer */}
  </DialogContent>
</Dialog>
```

### 2.4 Header (Title + Select + Tổng tiền + Nút X)

```tsx
<div className='flex items-center justify-between px-5 py-3.5 bg-white flex-shrink-0 border-b border-[#B7BCC3]'>
  <div className='flex items-center gap-3'>
    <span className='font-semibold text-black text-base'>Tiêu đề {formData.refNo}</span>
    {isReadOnly ? (
      <span className='text-sm text-black'>Loại chứng từ</span>
    ) : (
      <Select value={String(formData.refType)} onValueChange={...}>
        <SelectTrigger className='w-[200px] h-8 text-sm border-[#B7BCC3] rounded-lg bg-white' data-qa='sel_ref_type'>
          <SelectValue placeholder='Loại chứng từ' />
        </SelectTrigger>
        <SelectContent>...</SelectContent>
      </Select>
    )}
  </div>
  <div className='flex items-center gap-4'>
    <div className='text-right'>
      <div className='text-[11px] text-black leading-tight'>Tổng tiền</div>
      <div className='font-bold text-base text-black'>{formatCurrency(totalAmount)}</div>
    </div>
    <Button variant='ghost' size='sm' data-qa='btn_dong_dialog'
      className='h-7 w-7 p-0 text-black hover:text-black hover:bg-gray-100' onClick={handleClose}>
      <X className='h-4 w-4' />
    </Button>
  </div>
</div>
```

### 2.5 Body (2 Cột Layout: Main + Sidebar)

```tsx
<div className='flex-1 min-h-0 overflow-y-auto bg-[#f4f5f7]'>
  <div className='p-5 space-y-4'>
    <div className='flex gap-6'>
      {/* Cột trái: Form chính */}
      <div className='flex-1 space-y-3'>
        {/* grid grid-cols-2 gap-4 cho các row 2 field */}
        {/* space-y-1 cho field full-width */}
      </div>
      {/* Cột phải: Sidebar (Ngày + Số CT) */}
      <div className='w-[250px] flex-shrink-0 space-y-3'>
        {/* DatePicker + Input số CT */}
      </div>
    </div>
  </div>
</div>
```

### 2.6 Form Field Pattern (Label + Input)

```tsx
<div className='space-y-1'>
  <Label className='text-[13px] font-semibold text-black'>
    Tên field <span className='text-red-500'>*</span>
  </Label>
  {isReadOnly ? (
    <div className='text-[13px] text-black'>{value || '-'}</div>
  ) : (
    <div className='space-y-0.5'>
      <Input data-qa='i_field' value={value}
        onChange={e => setField('field', e.target.value)}
        onBlur={() => handleBlur('field')}
        placeholder='...'
        className={cn(
          'h-[30px] text-[13px] rounded-lg bg-white',
          touched.field && errors.field ? 'border-destructive' : 'border-[#B7BCC3]',
        )} />
      {touched.field && errors.field && (
        <p className='text-xs text-destructive flex items-center gap-1'>
          <AlertCircle className='h-3 w-3' />{errors.field}</p>)}
    </div>
  )}
</div>
```

### 2.7 Footer (3 Mode — mặc định: Hủy + Lưu)

> ⚠️ **QUY TẮC MẶC ĐỊNH:** Footer chỉ gồm **[Hủy] [Lưu]**. Nút **"Lưu & Thêm"** chỉ thêm khi user yêu cầu riêng.

```tsx
<div className='flex items-center justify-between px-5 py-2.5 bg-white flex-shrink-0 border-t border-[#B7BCC3]'>
  <span className='text-xs text-black truncate max-w-[50%]'>Tên đơn vị</span>
  <div className='flex gap-2'>
    {/* View mode */}
    {isReadOnly ? (
      <>
        {!formData.isPosted && <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_ghi_so'>Ghi sổ</Button>}
        {formData.isPosted && <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_bo_ghi_va_sua'>Bỏ ghi và sửa</Button>}
        <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_dong'>Đóng</Button>
      </>
    ) : (
      <>
        <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy' disabled={submitting}>Hủy</Button>
        <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_luu' onClick={handleSubmit}>Lưu</Button>
      </>
    )}
  </div>
</div>
```

### 2.8 Bảng Hạch Toán Inline

Xem chi tiết tại `b0/SKILL.md` → Section B (Bảng Hạch Toán Trong Dialog). Pattern:

```tsx
<div className='bg-white rounded-lg shadow-sm overflow-hidden'>
  <div className='border-b border-[#B7BCC3] px-3'>
    <button className='py-2.5 text-base font-normal text-primary border-b-2 border-primary -mb-[1px] px-1' data-qa='tab_hach_toan'>
      Hạch toán
    </button>
  </div>
  <div className='p-0'>
    <div className='overflow-x-auto border border-[#B7BCC3]'>
      <table className='w-full text-[13px] border-collapse'>
        <thead><tr className='bg-[#ededf1]'>{/* Các <th> */}</tr></thead>
        <tbody>
          {lines.map((line, i) => (
            <tr key={i} className='hover:bg-gray-50/50 border-b border-[#B7BCC3] last:border-b-0'>
              {/* <td> với Input/SearchCombobox inline */}
            </tr>
          ))}
          {/* Sum row: <tr className='bg-[#f2f2f4] font-medium'> */}
        </tbody>
      </table>
    </div>
    {/* Nút Thêm dòng / Xóa hết dòng */}
  </div>
</div>
```

---

## 3. Component Mapping — Chọn Đúng Component Cho Từng Field

| Loại field | Pattern A (Danh Mục) | Pattern B (Nghiệp Vụ) |
|-----------|---------------------|----------------------|
| Text ngắn (code, name) | `DmFormInput` | `Input` + `Label` |
| Text dài (address, desc) | `DmFormTextarea rows={2}` | `Input` (full-width) |
| FK đơn (chọn 1) | `DmGroupInput withChevron` (nếu không có API) / **`TableSearchCombobox` + ApiService** (nếu có API riêng) | `SearchCombobox` / `TableSearchCombobox` |
| FK nhiều cột | (không dùng) | `TableSearchCombobox` + columns |
| Enum | `Select` | `Select` |
| Ngày tháng | `DmFormInput type='date'` | `DatePicker` |
| Số tiền | `DmFormInput type='number'` | `Input type='text' inputMode='numeric' text-right` |
| Checkbox | `<input type='checkbox'>` | `<input type='checkbox'>` |
| Radio | `<input type='radio'>` | — |
| Mã số thuế | `DmTaxCodeInput` | — |
| View mode display | `DmFieldValue` / `DmTabFieldValue` | `<div className='text-[13px] text-black'>` |
| Footer | `DmDialogFooter` | Custom footer |

### 3.1 SearchCombobox / TableSearchCombobox — Luôn Có initialLabel Khi Sửa / Nhân Bản (BẮT BUỘC)

> ⚠️ **Lỗi phổ biến:** Khi sửa/nhân bản, `SearchCombobox` có `value` (ID) nhưng chưa load options → không hiển thị label, hiển thị placeholder. User phải click mở dropdown mới thấy giá trị đã chọn.

**Quy tắc:** Mọi `SearchCombobox` / `TableSearchCombobox` trong dialog PHẢI có `initialLabel` và PHẢI preload tên hiển thị khi dialog mở ở chế độ sửa hoặc nhân bản.

### 3.1.1 Quy Tắc `value` Phải Khớp Với `loadOptions` (BẮT BUỘC)

> ⚠️ **Lỗi nghiêm trọng:** API response (DTO) thường **KHÔNG trả về FK ID** mà chỉ trả về code/name. Khi edit, `value` của TableSearchCombobox bị rỗng → không chọn được item trong dropdown → submit sẽ gửi `bankAccountID: ''` → **mất dữ liệu FK**.

**Kiểm tra trước khi code:**
1. Xác định `value` của TableSearchCombobox là gì? (VD: `bankId`, `accountObjectId`)
2. Xác định `loadOptions` trả về `value` từ đâu? (VD: `b.id`, `kh.id`)
3. Kiểm tra API response (DTO) có chứa field đó không?
4. Nếu **KHÔNG có** → **PHẢI thêm `useEffect` resolve FK ID khi mở dialog Edit**

**Pattern resolve FK ID khi Edit (BẮT BUỘC nếu DTO thiếu FK ID):**

```tsx
// ── Edit mode: resolve FK ID từ code/name (vì API response không trả về FK ID) ──
useEffect(() => {
  if (!open || mode !== 'edit') return
  if (formData.objectCode && !formData.accountObjectId) {
    XxxApiService.list({ pageIndex: 1, pageSize: 1, keyword: formData.objectCode })
      .then(r => {
        if (r.success && r.data?.items?.length) {
          const match = r.data.items.find(x => x.code === formData.objectCode)
          if (match) {
            onFieldChange('accountObjectId', match.id)
            onFieldChange('objectName', match.name)
          }
        }
      })
      .catch(() => {})
  }
}, [open, mode, formData.objectCode, formData.accountObjectId])
```

**Ví dụ cụ thể các trường hợp phổ biến:**

| Dialog | Combobox | `value` | DTO có field? | Cần resolve? |
|--------|----------|---------|--------------|-------------|
| TK Ngân hàng | TK ngân hàng | `bankId` | `OpeningAccountEntryBankResponse` → ❌ Không có | ✅ Có |
| Công nợ KH | Khách hàng | `accountObjectId` | `OpeningAccountEntryCustomerResponse` → ❌ Không có | ✅ Có |
| Công nợ NCC | Nhà cung cấp | `accountObjectId` | `OpeningAccountEntryVendorResponse` → ❌ Không có | ✅ Có |
| Nhập số dư | TK kế toán | `accountNumber` | `OpeningAccountEntryOtherResponse` → ✅ Có `accountNumber` | ❌ Không |
| Danh mục CRUD | Nhóm KH | `customerGroupId` | `CustomerDto` → ✅ Có `customerGroupId` | ❌ Không |

### 3.1.2 Pattern Preload Label (khi DTO đã có FK ID nhưng thiếu tên hiển thị)

**Pattern trong Dialog:**

```tsx
const effectiveData = isClone ? cloneFrom : initialData

// Preload tên FK để hiển thị initialLabel khi sửa / nhân bản
useEffect(() => {
  if (!open || !effectiveData?.foreignKeyId) return
  let cancelled = false
  ;(async () => {
    try {
      const res = await XxxApiService.getById(effectiveData!.foreignKeyId!)
      if (cancelled || !res.success || !res.data) return
      updateField('_foreignKeyName', res.data.name) // Lưu tên vào formData với prefix _
    } catch { /* ignore */ }
  })()
  return () => { cancelled = true }
}, [open, effectiveData?.foreignKeyId, updateField])

// Trong JSX:
<SearchCombobox
  value={(f.foreignKeyId as string) ?? ''}
  onChange={(v: string) => updateField('foreignKeyId', v || null)}
  loadOptions={loadXxxOptions}
  placeholder='Chọn...'
  dataQa='sel_xxx'
  initialLabel={(f._foreignKeyName as string) ?? ''}   // ← BẮT BUỘC
/>
```

**Nếu API trả về sẵn tên trong DTO** (vd: `AccountObjectDto.customerGroup`, `AccountObjectDto.salesPersonName`), dùng trực tiếp không cần preload:

```tsx
<SearchCombobox
  value={(f.customerGroupId as string) ?? ''}
  initialLabel={f.customerGroup as string}   // ← DTO đã có sẵn tên
  ...
/>
```

**Quy ước đặt tên field preload:** Dùng prefix `_` + tên field + `Name` (vd: `_parentName`, `_fromAccountName`, `_orgLevelName`) để phân biệt với field từ DTO.

---

## 4. Quy Ước Chung (Cả 2 Pattern)

| Quy ước | Pattern A (Danh Mục) | Pattern B (Nghiệp Vụ) |
|---------|---------------------|----------------------|
| **maxWidth** | `'920px'` | `'none'` (100vw) |
| **Body bg** | white | `bg-[#f4f5f7]` |
| **Header border** | `border-b border-[#B7BCC3]` | `border-b border-[#B7BCC3]` |
| **Footer border** | DmDialogFooter tự có | `border-t border-[#B7BCC3]` |
| **Input height** | DmFormInput mặc định (`h-8`) | `h-[30px]` |
| **Input border** | DmFormInput mặc định | `border-[#B7BCC3]` |
| **Input error** | DmFormField `error={errors.x}` | `border-destructive` + inline msg |
| **Input rounding** | `rounded-[8px]` | `rounded-lg` |
| **Font size** | `text-[13px]` | `text-[13px]` |
| **Label style** | DmFormField auto | `text-[13px] font-semibold text-black` |
| **Required** | `required` prop | `<span className='text-red-500'>*</span>` |
| **View mode** | `DmFieldValue` / `DmTabFieldValue` | `<div>` thay `<Input>` |
| **Validate** | onBlur (DmFormInput) | onBlur + `touched` check |
| **data-qa prefix** | `i_`=input, `sel_`=select, `chk_`=checkbox, `r_`=radio | `i_`=input, `sel_`=select, `dt_`=date, `btn_`=button |
| **Close button** | `h-7 w-7 text-gray-400 rounded-[8px]` | `h-7 w-7 text-black` |
| **Grid layout** | `grid grid-cols-5 gap-x-3 gap-y-3` | `flex gap-6` (2 cột) |
| **Column span** | `className='col-span-3'`, `col-span-2` | `w-[250px]` sidebar |
| **Tabs** | Có (trong body, dưới form) | Có (tab Hạch toán trong section) |
| **Error dialog** | `ValidationErrorDialog` | `ValidationErrorDialog` |
| **Submit modes** | `doSubmit(false)` Lưu / `doSubmit(true)` Lưu & Thêm mới | `handleSubmit` Lưu / `handleSubmitAndNew` Lưu & Thêm mới |

---

## 5. Cấu Trúc File (Từ `cau-truc-du-an`)

```
features/{nhom}/{ten-feature}/
├── types/
│   ├── {SN}.types.api.ts       ← Enums + DTO từ BE
│   └── {SN}.types.ui.ts        ← FormState, initial values, errors type
├── services/
│   └── {SN}ApiService.ts       ← CRUD API (getById, create, update, delete)
├── hooks/
│   ├── use{SN}.page.list.ts    ← Nếu có master page
│   └── use{SN}.dlg.form.ts    ← Hook dialog (submit, delete, init)
├── dialogs/
│   └── {SN}Dialog.tsx          ← Dialog component ← ĐÂY LÀ FILE CHÍNH
├── pages/
│   └── {SN}Page.tsx            ← Master page (nếu có)
└── index.ts                    ← Barrel exports
```

### 5.1 Hook Initialization Pattern — Reset State Khi Mở Lại Dialog

> ⚠️ **BẮT BUỘC:** Hook phải reset `formData` khi `initialData` thay đổi. Dialog thường không unmount (chỉ ẩn/hiện), nên `useState(initial)` chỉ chạy 1 lần.

```tsx
export function useXxxDialogForm(initialData: XxxDto | null) {
  // ✅ Dùng lazy initializer + useEffect reset
  const buildInitial = (data: XxxDto | null): XxxFormState =>
    data ? { code: data.code, name: data.name, ... } : { ...INITIAL_FORM }

  const [formData, setFormData] = useState<XxxFormState>(() => buildInitial(initialData))

  // Reset khi initialData thay đổi (dialog đóng → mở với record khác)
  useEffect(() => {
    setFormData(buildInitial(initialData))
    clearErrors()
  }, [initialData])

  // ...
}
```

| Pattern | Dùng khi | Mô tả |
|---------|---------|-------|
| **Hook nhận `initialData`** | Dialog đơn giản, 1 hook riêng | Hook tự reset trong `useEffect` khi `initialData` thay đổi |
| **Hook nhận `editMode ? initialData : null`** | Dialog dùng chung hook | Component gọi `setFormData` trong `useEffect([open, initialData?.id])` |

> **Nguyên nhân lỗi:** `const [formData] = useState(buildInitial(initialData))` — `useState` chỉ dùng giá trị khởi tạo 1 lần. Khi dialog đóng rồi mở lại với `initialData` mới, `useState` không chạy lại → form vẫn giữ data cũ.
> **Fix:** Luôn có `useEffect` reset form khi dependency thay đổi (`initialData` hoặc `[open, initialData?.id]`).

---

## 6. Checklist Trước Commit

- [ ] Chọn đúng pattern (A: Danh Mục / B: Nghiệp Vụ)
- [ ] `maxWidth` đúng (`'920px'` hoặc `'none'`)
- [ ] 3 mode hoạt động: View / Create / Edit
- [ ] `isReadonly` flag cho tất cả fields
- [ ] Validate onBlur + inline error message
- [ ] `ValidationErrorDialog` cho lỗi server
- [ ] `data-qa` đầy đủ (btn_, i_, sel_, dt_, chk_, r_)
- [ ] View mode hiển thị `<div>` / `DmFieldValue` (không dùng disabled input)
- [ ] Input số: `type='text' inputMode='numeric'` (Pattern B)
- [ ] Footer đúng pattern (DmDialogFooter hoặc custom)
- [ ] Nút X close custom (ẩn mặc định Radix)
- [ ] Hook không gọi API trực tiếp từ dialog
- [ ] Types đủ fields từ DTO BE
- [ ] Barrel `index.ts` export dialog
- [ ] Compile không lỗi, TypeScript check pass
- [ ] ⚠️ **Reset state khi đóng/mở lại dialog:** `useEffect` theo `[open, initialData?.id]` — form phải theo giá trị mới, không giữ giá trị cũ

---

## Script Kiểm Tra

```bash
node .claude/skills/tao-ui-dialog/check-dialog.cjs src/modules/.../dialogs/XxxDialog.tsx
```
