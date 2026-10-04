---
name: tao-ui-giao-dien-new
description: 'FOUNDATION — Quy tắc UI nền tảng cho MỌI loại giao diện KetoanApp, cập nhật từ code thực tế (PTDialog.tsx + KHFormDialog.tsx): buttons (btn-primary/btn-secondary/btn-danger), DmFormField/DmFormInput/DmFieldValue, SearchCombobox/TableSearchCombobox, format utilities, data-qa, validate onBlur, className chuẩn (h-[30px]/rounded-lg/border-[#AEB3BA]/text-[13px]), 2 pattern dialog (Danh Mục CRUD + Nghiệp Vụ). Kế thừa tao-ui-giao-dien/SKILL.md. Luôn load kèm tao-dialog-new/SKILL.md khi tạo dialog.'
---

# Quy Tắc UI Nền Tảng (New) — SASUCO KetoanApp

> **FOUNDATION SKILL** — Áp dụng cho MỌI loại UI trong KetoanApp.
> Nguồn tham khảo: `PTDialog.tsx` (Full-Screen Nghiệp Vụ) + `KHFormDialog.tsx` (Danh Mục CRUD).
> Kế thừa: `tao-ui-giao-dien/SKILL.md` (nền tảng gốc).

---

## 1. Component Catalog — Có Gì Dùng Nấy

### 1.1 Shared Components (`@/shared/components`)

| Component | Import | Dùng trong |
|-----------|--------|-----------|
| `Dialog`, `DialogContent` | `@/shared/components/ui/dialog` | Cả 2 pattern |
| `DialogHeader`, `DialogTitle` | `@/shared/components/ui/dialog` | Pattern Danh Mục |
| `Tabs`, `TabsList`, `TabsContent` | `@/shared/components/ui/tabs` | Pattern Danh Mục |
| `Input` | `@/shared/components/ui/input` | Pattern Nghiệp Vụ |
| `Label` | `@/shared/components/ui/label` | Pattern Nghiệp Vụ |
| `Button` | `@/shared/components/ui/button` | Cả 2 |
| `Select` | `@/shared/components/ui/select` | Cả 2 |
| `DatePicker` | `@/shared/components/common` | Pattern Nghiệp Vụ |
| `SearchCombobox` | `@/shared/components/common` | Pattern Nghiệp Vụ |
| `TableSearchCombobox` | `@/shared/components/common` | Pattern Nghiệp Vụ |
| `ConfirmDialog` | `@/shared/components/common` | Cả 2 |
| `ValidationErrorDialog` | `@/shared/components/common` | Cả 2 |
| `BulkActionBar` | `@/shared/components/common` | Master Page |
| `TableSettingsPanel` | `@/shared/components/table-settings` | Master Page |

### 1.2 KetoanApp Components (`@/modules/KetoanApp/components`)

| Component | Dùng trong | Mô tả |
|-----------|-----------|-------|
| `DmFormField` | Pattern Danh Mục | Wrapper: label + required + error + tooltip |
| `DmFormInput` | Pattern Danh Mục | Input text chuẩn (h-8, rounded-[8px]) |
| `DmFormTextarea` | Pattern Danh Mục | Textarea (rows={2}) |
| `DmFieldValue` | Pattern Danh Mục | Hiển thị text view mode |
| `DmTabFieldValue` | Pattern Danh Mục | Hiển thị label+value view mode trong tab |
| `DmGroupInput` | Pattern Danh Mục | FK tạm (chưa có API) — nếu có API riêng → dùng `TableSearchCombobox` |
| `DmDialogFooter` | Pattern Danh Mục | Footer dialog: Hủy+Lưu+Lưu&Thêm mới |
| `DmTaxCodeInput` | Pattern Danh Mục | Input MST + auto-fill |
| `DmTabTrigger` | Pattern Danh Mục | Tab trigger trong TabsList |
| `DmPageHeader` | Master Page | Header trang |
| `DmSearchToolbar` | Master Page | Thanh tìm kiếm |
| `DmTable`, `DmTablePagination` | Master Page | Bảng + phân trang |
| `DmRowActions` | Master Page | Row actions (tự sinh data-qa) |
| `DmValidatedInput` | Pattern Danh Mục | Input email/phone/website với validate realtime + border đổi màu |

### 1.3 Shared Hooks

| Hook | Source | Dùng ở |
|------|--------|--------|
| `useTableSettings` | `@/shared/hooks/useTableSettings` | Master Page |
| `useTableLayout` | `@/shared/hooks` | Master Page |
| `useDmRowActions` | `@/shared/hooks` | Master Page |
| `useExcelExport` | `@/shared/hooks` | Master Page |
| `useBulkSelection` | `@/shared/hooks` | Master Page |

### 1.4 Utilities

| Utility | Source |
|---------|--------|
| `cn()` | `@/shared/components/ui/utils` |
| `formatCurrency()`, `formatNumber()` | `@/shared/utils` |
| `formatDate()`, `formatDateTime()` | `@/shared/utils` |

---

## 2. Buttons

| Class | Dùng cho |
|-------|---------|
| `.btn-primary` | Thêm mới, Lưu, Xác nhận, Ghi sổ |
| `.btn-secondary` | Hủy, Đóng, Làm mới |
| `.btn-danger` | Xóa (phải kèm ConfirmDialog) |

### Kích thước & rounding

| Vị trí | Pattern |
|--------|---------|
| Dialog header/footer | `h-8 text-[13px] rounded-lg` |
| Icon nhỏ (X, Trash2) | `h-7 w-7 p-0` hoặc `h-6 w-6 p-0` |
| Danh Mục CRUD | `rounded-[8px]` |
| Nghiệp Vụ | `rounded-lg` |
| Ghost icon button | `variant='ghost' size='sm' text-gray-400 hover:text-gray-600` |

### Nút Làm mới

```tsx
<Button variant='ghost' size='sm'
  className='h-8 w-8 p-0 text-gray-500 hover:text-gray-700 hover:bg-gray-100'
  onClick={handleRefresh} disabled={refreshing} title='Làm mới' data-qa='btn_lam_moi'>
  <RefreshCw className={cn('h-4 w-4', refreshing && 'animate-spin')} />
</Button>
```

---

## 3. Form Fields — 2 Pattern

### 3.1 Pattern A: Danh Mục CRUD (DmFormField)

```tsx
<DmFormField label='Mã' required error={errors.code} tooltip='Tự động tạo nếu trống' className='col-span-X'>
  {isReadonly
    ? <DmFieldValue value={value} />
    : <DmFormInput data-qa='i_code'
        value={(f.code as string) ?? ''}
        onChange={(e) => updateField('code', e.target.value)}
        onBlur={() => handleBlur('code')} />}
</DmFormField>
```

Các DmFormField components:
- **Text ngắn**: `DmFormInput`
- **Text dài**: `DmFormTextarea rows={2}`
- **FK chọn (có API riêng)**: `TableSearchCombobox` + ApiService + loadOptions
- **FK tạm (chưa có API)**: `DmGroupInput withChevron`
- **MST tra cứu**: `DmTaxCodeInput`
- **View mode**: `DmFieldValue` / `DmTabFieldValue`

#### 3.1.1 DmValidatedInput — Email / Phone / Website (Validate Realtime)

> Dùng `DmValidatedInput` thay cho `DmFormInput` cho các field email, số điện thoại, website.
> Component tự xử lý validate realtime + border đổi màu + progressive message.

```tsx
import { DmValidatedInput } from '@/modules/KetoanApp/components'

// Email
<DmFormField label='Email' error={errors.email}>
  <DmValidatedInput inputType='email' data-qa='i_email'
    value={f.email ?? ''}
    onChange={(e) => updateField('email', e.target.value)}
    onBlur={() => handleBlur('email')} />
</DmFormField>

// Số điện thoại
<DmFormField label='Điện thoại' error={errors.phone}>
  <DmValidatedInput inputType='phone' data-qa='i_phone'
    value={f.phone ?? ''}
    onChange={(e) => updateField('phone', e.target.value)}
    onBlur={() => handleBlur('phone')} />
</DmFormField>

// Website
<DmFormField label='Website' error={errors.website}>
  <DmValidatedInput inputType='website' data-qa='i_website'
    value={f.website ?? ''}
    onChange={(e) => updateField('website', e.target.value)}
    onBlur={() => handleBlur('website')} />
</DmFormField>
```

**Quy tắc:**
- `DmValidatedInput` **tự quản lý** `dirty` state nội bộ → không cần `touched` từ hook
- Border: mặc định → `border-success` (xanh) khi hợp lệ → `border-destructive` (đỏ) khi sai
- Progressive message: **chỉ hiển thị khi field có giá trị** — field trống = không message
- Message rỗng (`''`) từ `MessageProgressHelper` → **không render thẻ `<p>`** (tránh DOM rỗng)
- `handleBlur` trong hook vẫn cần validate `phone`/`mobile`/`website` để `validateAll` hoạt động

> ⚠️ **FK field có API riêng** (như Đơn vị → DVTCApiService) → luôn dùng `TableSearchCombobox` gọi API. `DmGroupInput withChevron` chỉ là tạm thời khi chưa có API. Xem `b0/SKILL.md` Section C.1 để có pattern đầy đủ.

### 3.2 Pattern B: Nghiệp Vụ (Label + Input)

```tsx
<div className='space-y-1'>
  <Label className='text-[13px] font-bold text-black'>
    Tên field <span className='text-red-500'>*</span>
  </Label>
  {isReadOnly ? (
    <div className='text-[13px] text-black'>{value || '-'}</div>
  ) : (
    <div className='space-y-0.5'>
      <Input
        data-qa='i_field'
        value={value}
        onChange={e => setField('field', e.target.value)}
        onBlur={() => handleBlur('field')}
        className={cn(
          'h-[30px] text-[13px] rounded-lg bg-white',
          touched.field && errors.field ? 'border-destructive' : 'border-[#AEB3BA]',
        )} />
      {touched.field && errors.field && (
        <p className='text-xs text-destructive flex items-center gap-1'>
          <AlertCircle className='h-3 w-3' />{errors.field}
        </p>)}
    </div>
  )}
</div>
```

Các field components:
- **Text**: `Input`
- **FK đơn**: `SearchCombobox`
- **FK nhiều cột**: `TableSearchCombobox` + column definitions
- **Enum**: `Select` + `SelectItem`
- **Ngày**: `DatePicker`
- **Số tiền**: `Input type='text' inputMode='numeric' text-right`
- **View mode**: `<div className='text-[13px] text-black'>`

---

## 4. SearchCombobox / TableSearchCombobox (FK Fields)

### SearchCombobox (FK đơn)

```tsx
<SearchCombobox
  value={line.debitAccount}
  initialLabel={line.debitAccount}
  onChange={(val, label) => updateLine(index, 'debitAccount', val || label)}
  loadOptions={loadTaiKhoan}         // async (keyword) => ComboboxOption[]
  placeholder='TK Nợ'
  dataQa='sel_tk_no'
  className='h-6 text-[13px] border-0 bg-transparent'  // inline trong table
/>
```

### TableSearchCombobox (FK nhiều cột hiển thị)

```tsx
<TableSearchCombobox
  value={formData.accountObjectId}
  initialLabel={formData.accountObjectName}
  displayField='name'
  onChange={(id, rowData) => {
    setField('accountObjectId', id)
    setField('accountObjectName', rowData.name || '')
    setField('accountObjectAddress', rowData.address || '')
  }}
  loadOptions={loadDoiTuong}         // async (keyword) => TableComboboxRow[]
  columns={doiTuongColumns}          // TableComboboxColumn[]
  placeholder='Chọn đối tượng...'
  dataQa='sel_doi_tuong'
  showQuickAdd
  debounceMs={800}
/>
```

**Column definitions (TableComboboxColumn[]):**
```tsx
const doiTuongColumns: TableComboboxColumn[] = [
  { field: 'code', title: 'Mã', width: 100 },
  { field: 'name', title: 'Tên', width: 220 },
  { field: 'taxCode', title: 'MST', width: 130 },
]
```

### TableSearchCombobox — View Mode & `initialLabel` (⚠️ BẮT BUỘC)

> **Cốt lõi:** `initialLabel` PHẢI khớp với `displayField`. Khi ở **view mode** (`disabled={true}`), dropdown không mở được → `rows` rỗng → `selectedLabel` rỗng → **chỉ còn `initialLabel` làm fallback**. Nếu `initialLabel` không khớp `displayField`, người dùng sẽ thấy **sai dữ liệu**.

#### Rule 1: `initialLabel` luôn khớp `displayField`

| `displayField` | `initialLabel` phải là | Ví dụ form state |
|---|---|---|
| `accountNumber` | Số tài khoản (string) | `formData.bankAccountNumber` |
| `code` | Mã (string) | `formData.objectCode` |
| `name` | Tên (string) | `formData.accountObjectName` |

```tsx
// ❌ SAI: displayField='accountNumber' nhưng initialLabel là bankName
<TableSearchCombobox
  displayField='accountNumber'
  initialLabel={formData.bankName}          // ❌ Hiển thị tên NH thay vì số TK!
/>

// ✅ ĐÚNG: displayField='accountNumber' → initialLabel là accountNumber
<TableSearchCombobox
  displayField='accountNumber'
  initialLabel={formData.bankAccountNumber} // ✅ Hiển thị đúng số tài khoản
/>
```

#### Rule 2: View mode KHÔNG được hiển thị sai dữ liệu

Khi `disabled={isReadOnly}`:
- Người dùng **không thể click mở dropdown** → `rows` không bao giờ được load
- `selectedLabel` luôn là `''` (vì `rows` rỗng)
- Fallback về `initialLabel`
- **Nếu `initialLabel` không khớp `displayField` → UI hiển thị sai!**

```tsx
// ❌ SAI trong view mode: initialLabel là bankName, displayField là accountNumber
// Kết quả: view mode hiển thị "Vietcombank" thay vì "1234567890"
<TableSearchCombobox
  value={formData.bankAccountID}
  initialLabel={formData.bankName}          // ❌ Sai khi view mode
  displayField='accountNumber'
  disabled={isReadOnly}
/>

// ✅ ĐÚNG: initialLabel khớp displayField, view mode hiển thị đúng
<TableSearchCombobox
  value={formData.bankAccountID}
  initialLabel={formData.bankAccountNumber} // ✅ Đúng số TK
  displayField='accountNumber'
  disabled={isReadOnly}
/>
```

#### Rule 3: Nếu DTO không có display value → resolve bằng `useEffect`

Khi API DTO chỉ có FK ID (vd: `bankAccountID`) mà **không có** display value (vd: `accountNumber`), cần:

1. **Thêm field display value vào `TGFormState`** (vd: `bankAccountNumber: string`)
2. **Resolve FK ID → display value bằng `useEffect`** khi mở dialog edit/view
3. **Dùng display value làm `initialLabel`**

```tsx
// Step 1: Types — thêm field display value
// TG.types.ui.ts:
export interface TGFormState {
  bankAccountID: string       // FK ID từ API
  bankAccountNumber: string   // ← Display value (thêm mới)
  bankName: string
  // ...
}

// Step 2: Dialog — resolve FK ID khi edit/view
useEffect(() => {
  if (!open || mode === 'create') return
  if (formData.bankAccountID && !formData.bankAccountNumber) {
    TKNHApiService.list({ pageIndex: 1, pageSize: 1, keyword: formData.bankAccountID })
      .then(r => {
        if (r.success && r.data?.items?.length) {
          const match = r.data.items.find(x => x.id === formData.bankAccountID)
          if (match) {
            setField('bankAccountNumber', match.accountNumber ?? '')
          }
        }
      })
      .catch(() => {})
  }
}, [open, mode, formData.bankAccountID, formData.bankAccountNumber])

// Step 3: Combobox — initialLabel khớp displayField
<TableSearchCombobox
  value={formData.bankAccountID}
  initialLabel={formData.bankAccountNumber}  // ← Khớp displayField
  displayField='accountNumber'
  disabled={isReadOnly}
  onChange={(id, rowData) => {
    setField('bankAccountID', id)
    setField('bankAccountNumber', rowData.accountNumber ?? '') // ← Update display value
  }}
/>
```

> **Tóm tắt:** `initialLabel` = giá trị hiển thị trong input khi chưa có row được chọn. Nó PHẢI cùng loại với `displayField`. View mode (`disabled`) phụ thuộc hoàn toàn vào `initialLabel` → nếu sai → UI hiển thị sai.

---

## 5. Validate — onBlur (BẮT BUỘC)

```tsx
// ✅ Validate khi rời field — không gây jitter
onBlur={() => handleBlur('fieldName')}

// ❌ KHÔNG validate onChange
```

**3 cấp độ error:**
1. **Inline error** — dưới field: `<AlertCircle />` + message
2. **Toast tổng hợp** — `showValidationErrorsToast(errors)` trước submit
3. **Server error** — `ValidationErrorDialog`

---

## 6. 3 Mode View/Create/Edit

```tsx
const isView = viewOnly === true          // Pattern Danh Mục
const isReadOnly = mode === 'view'         // Pattern Nghiệp Vụ
```

| Mode | Behavior |
|------|----------|
| **View** | DmFieldValue / DmTabFieldValue (A) hoặc `<div>` (B) |
| **Create** | Input trống, autoFillCode(), submit POST |
| **Edit** | Input có giá trị từ DTO, submit PUT |

> **Cấm:** dùng `disabled` trên input cho view mode. Phải render thẻ khác.

---

## 7. Dialog Footer

> ⚠️ **QUY TẮC MẶC ĐỊNH:** Footer chỉ gồm **[Hủy] [Lưu]**. Nút **"Lưu & Thêm"** chỉ thêm khi user yêu cầu riêng.

### Pattern A: DmDialogFooter (Danh Mục CRUD) — mặc định

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

### Pattern B: Custom Footer (Nghiệp Vụ) — mặc định

```tsx
<div className='flex items-center justify-between px-5 py-2.5 bg-white border-t border-[#AEB3BA]'>
  <span>Đơn vị</span>
  <div className='flex gap-2'>
    {/* View: Ghi sổ / Bỏ ghi và sửa / Đóng */}
    {/* Edit: Hủy (btn-secondary) / Lưu (btn-primary) */}
  </div>
</div>
```

---

## 8. ClassName Quy Ước (Từ Code Thực Tế)

| Thành phần | Pattern A (Danh Mục) | Pattern B (Nghiệp Vụ) |
|-----------|---------------------|----------------------|
| Input height | `h-8` (DmFormInput mặc định) | `h-[30px]` |
| Input border | DmFormInput mặc định | `border-[#AEB3BA]` |
| Input error | `error={errors.x}` prop | `border-destructive` |
| Input rounding | `rounded-[8px]` | `rounded-lg` |
| Body font | `text-[13px]` | `text-[13px]` |
| Header border | không có `border-b` | không có `border-b` |
| Body bg | white | `bg-[#f4f5f7]` |
| Table header bg | — | `bg-[#ededf1]` |
| Table row hover | — | `hover:bg-gray-50/50` |
| Label style | DmFormField auto | `font-bold text-black` |
| Required | `required` prop | `<span className='text-red-500'>*</span>` |
| Dialog width | `maxWidth='920px'` | `maxWidth='none'` (100vw) |
| Close button | `h-7 w-7 text-gray-400 rounded-[8px]` | `h-7 w-7 text-black` |
| Tabs container | `rounded-[8px] overflow-hidden` | tab button trong section |
| Tabs | `className='gap-0'` | — |
| TabsList | `bg-transparent border-b border-[#AEB3BA] p-0 gap-1 rounded-none` | — |
| DmTabTrigger | `rounded-none border-b-1 border-gray-200` | — |
| TabsContent | `border border-[#AEB3BA] h-[280px] overflow-y-auto` (CỐ ĐỊNH chiều cao, TẤT CẢ tab giống nhau) | — |

> ⚠️ **TẤT CẢ TabsContent PHẢI có `h-[280px] overflow-y-auto`** — nếu không sẽ bị nhảy layout khi chuyển tab.
> ⚠️ **Mỗi tab có nội dung KHÁC NHAU** — không tự ý đưa phone/email vào tab Tiền lương. Phân phối fields theo đúng MISA.
> ⚠️ **Nếu MISA có field mà BE chưa có** → vẫn render UI, gửi qua `formData`, tạo inbox BE bổ sung.

---

## 9. Bảng Hạch Toán Inline (Pattern B)

```tsx
<div className='bg-white rounded-lg shadow-sm overflow-hidden'>
  <div className='border-b border-[#AEB3BA] px-3'>
    <button className='py-2.5 text-base font-normal text-primary border-b-2 border-primary -mb-[1px] px-1' data-qa='tab_hach_toan'>
      Hạch toán
    </button>
  </div>
  <div className='p-0'>
    <div className='overflow-x-auto border border-[#AEB3BA]'>
      <table className='w-full text-[13px] border-collapse'>
        <thead>
          <tr className='bg-[#ededf1]'>
            <th className='w-10 px-2 py-2 text-center font-semibold border-r'>#</th>
            <th className='px-2 py-2 text-left font-semibold border-r min-w-[200px]'>Diễn giải</th>
            <th className='w-[110px] px-2 py-2 text-center font-semibold border-r'>TK Nợ</th>
            <th className='w-[110px] px-2 py-2 text-center font-semibold border-r'>TK Có</th>
            <th className='w-[130px] px-2 py-2 text-right font-semibold border-r'>Số tiền</th>
            {/* Các cột FK... */}
            {!isReadOnly && <th className='w-10 px-2 py-2 border-r'></th>}
          </tr>
        </thead>
        <tbody>
          {lines.map((line, i) => (
            <tr key={i} className='hover:bg-gray-50/50 border-b last:border-b-0'>
              <td className='px-2 py-1.5 text-center border-r'>{i + 1}</td>
              <td className='px-2 py-1.5 border-r'>
                {isReadOnly ? <span>{line.desc}</span> :
                  <Input className='h-6 border-0 p-0 text-[13px] bg-transparent focus-visible:ring-0 rounded-none' />}
              </td>
              {/* SearchCombobox inline: className='h-6 text-[13px] border-0 bg-transparent' */}
              {/* Input số: type='text' inputMode='numeric' text-right */}
              {!isReadOnly && (
                <td className='px-2 py-1.5 text-center'>
                  <Button variant='ghost' size='sm' className='h-6 w-6 p-0 icon-danger'><Trash2 className='h-3.5 w-3.5' /></Button>
                </td>)}
            </tr>
          ))}
          {/* Sum row: <tr className='bg-[#f2f2f4] font-medium'> */}
        </tbody>
      </table>
    </div>
    {/* Nút Thêm dòng / Xóa hết dòng */}
    {!isReadOnly && (
      <div className='flex gap-2 mt-2.5'>
        <Button variant='ghost' size='sm' data-qa='btn_them_dong' onClick={addLine}
          className='text-[13px] font-medium text-black hover:text-black hover:bg-gray-100 h-7 px-2'>
          <Plus className='h-3.5 w-3.5 mr-1' /> Thêm dòng</Button>
        <Button variant='ghost' size='sm' data-qa='btn_xoa_het_dong' onClick={...} disabled={...}
          className='text-[13px] font-medium text-black hover:text-black hover:bg-gray-100 h-7 px-2'>
          <Trash2 className='h-3.5 w-3.5 mr-1' /> Xóa hết dòng</Button>
      </div>
    )}
  </div>
</div>
```

---

## 10. Grid Layout

### Pattern A: Grid form

```tsx
<div className='grid grid-cols-5 gap-x-3 gap-y-3'>   {/* 5 cột mặc định */}
  <DmFormField ... />                                   {/* 1 cột */}
  <DmFormField className='col-span-3' ... />            {/* 3 cột */}
  <DmFormField className='col-span-2' ... />            {/* 2 cột */}
</div>
```

### Pattern B: Flex 2 cột (Nghiệp Vụ / Danh Mục có sidebar)

```tsx
{/* Dùng cho cả Pattern B Nghiệp Vụ (full-screen) và Pattern A Danh Mục (920px) khi layout có 2 cột trái-phải rõ rệt */}
<div className='flex gap-6'>
  <div className='flex-1 space-y-3'>                    {/* Main form */}
    <div className='grid grid-cols-2 gap-4'>...</div>   {/* Row 2 field */}
    <div className='space-y-1'>...</div>                {/* Full-width field */}
  </div>
  <div className='w-[250px] md:w-[300px] flex-shrink-0 space-y-3'>  {/* Sidebar */}
    <DatePicker ... />
    <Input ... />
  </div>
</div>
```

> ⚠️ **Bài học từ NVFormDialog:** Khi clone MISA thấy layout 2 cột (trái: Mã+Tên+Đơn vị+Chức danh; phải: Ngày sinh+Giới tính+CMND+Nơi cấp) → phải dùng flex 2 cột. Không ép tất cả vào grid-cols-5.

---

## 11. data-qa (BẮT BUỘC)

| Phần tử | Prefix | Ví dụ |
|--------|--------|-------|
| Button | `btn_` | `btn_them_moi`, `btn_luu`, `btn_huy`, `btn_dong_dialog` |
| Input | `i_` | `i_code`, `i_name`, `i_address`, `i_tim_kiem` |
| Select/Combobox | `sel_` | `sel_doi_tuong`, `sel_ref_type`, `sel_gender` |
| DatePicker | `dt_` | `dt_ref_date`, `dt_posted_date` |
| Checkbox | `chk_` | `chk_nha_cung_cap`, `chk_chon_tat_ca` |
| Radio | `r_` | `r_to_chuc`, `r_ca_nhan` |
| Tab | `tab_` | `tab_hach_toan` |
| Table | `tbl_` | `tbl_danh_sach` |
| Row action | `btn_xem_{id}`, `btn_sua_{id}`, `btn_xoa_{id}` | (DmRowActions tự sinh) |

---

## 12. Format Utilities & Quy Tắc Hiển Thị Dữ Liệu

> **Tham chiếu chuẩn quốc tế:** ISO 8601 (date), ISO 4217 (currency), ISO 31-0 (numbers), Nielsen Norman Group (table UX: số căn phải, text căn trái), Edward Tufte (data-ink ratio: không dùng `-` trong ô trống).

### 12.1 Danh Mục Format Functions

| Hàm | Input | Output | Null/Empty | Source |
|-----|-------|--------|-----------|--------|
| `formatCurrency(n)` | `number` | `"1.000.000 ₫"` | Không check null | `@/shared/utils` |
| `formatNumber(n)` | `number` | `"1.234.567"` | Không check null | `@/shared/utils` |
| `formatDate(s)` | `string \| null \| undefined` | `"15-01-2024"` | `"-"` | `@/shared/utils` |
| `formatDateTime(s)` | `string \| null \| undefined` | `"15-01-2024 10:30:45"` | `"-"` | `@/shared/utils` |
| `formatPercent(n, decimals?)` | `number` | `"12.50%"` | Không check null | `@/shared/utils` |
| `formatPhoneNumber(s)` | `string \| null \| undefined` | `"0912 345 678"` | `"-"` | `@/shared/utils` |
| `formatTaxCode(s)` | `string` | `"1234-567-890"` | Không check null | `@/shared/utils` |
| `formatFileSize(bytes)` | `number` | `"1.2 MB"` | `"0 B"` khi 0 | `@/shared/utils` |
| `formatVatRate(rate)` | `number \| null \| undefined` | `"10%"`, `"KCT"`, `"KKKNT"` | `""` | `@/shared/utils` |
| `formatDateForInput(s)` | `string \| Date \| null` | `"2024-01-15"` (HTML5) | `""` | `@/shared/utils` |
| `formatDateTimeForInput(s)` | `string \| Date \| null` | `"2024-01-15T10:30"` (HTML5) | `""` | `@/shared/utils` |

### 12.2 Nguyên Tắc Alignment Theo Loại Dữ Liệu

> **Chuẩn UX quốc tế (Nielsen Norman Group, ISO):**
> - **Số → canh phải (`text-right`)**: Giúp mắt so sánh độ lớn dễ dàng (cùng đơn vị, thẳng hàng decimal).
> - **Text → canh trái (mặc định)**: Hướng đọc tự nhiên từ trái→phải.
> - **Mã ngắn / trạng thái → canh giữa (`text-center`)**: Các giá trị có độ dài cố định, ngắn.
> - **Header đồng bộ với data**: Header của cột số canh phải giống data; header text canh trái.

| # | Loại dữ liệu | Ví dụ field | Alignment | Format | Ghi chú |
|---|-------------|------------|-----------|--------|---------|
| 1 | **Tiền tệ (table list)** | `totalAmount`, `debitAmount`, `creditAmount`, `amount` | **Right** `text-right` | `formatNumber()` | Không `₫` — sạch, dễ scan |
| 2 | **Tiền tệ (dialog header/footer)** | Tổng tiền dialog | — | `formatCurrency()` | Có `₫` — xác nhận "đây là tiền" |
| 3 | **Tiền tệ (bảng hạch toán)** | Số tiền từng dòng | **Right** `text-right` | `formatNumber()` | Không `₫` |
| 4 | **Số lượng** | `quantity`, `qty` | **Right** `text-right` | `formatNumber()` | Số nguyên hoặc decimal |
| 5 | **Đơn giá** | `unitPrice`, `unitCost` | **Right** `text-right` | `formatNumber()` | |
| 6 | **Tỷ giá / Hệ số** | `exchangeRate`, `coefficient` | **Right** `text-right` | `formatNumber()` | Hiển thị đủ decimal |
| 7 | **Phần trăm** | `percent`, `discountRate` | **Right** `text-right` | `formatPercent(n, 2)` | `"12.50%"` |
| 8 | **Thuế suất VAT** | `vatRate` | **Right** `text-right` | `formatVatRate()` | `"10%"` / `"KCT"` / `"KKKNT"` |
| 9 | **Ngày tháng** | `refDate`, `postedDate`, `voucherDate` | **Left** (mặc định) | `formatDate()` | `dd-MM-yyyy` |
| 10 | **Ngày giờ** | `postedDate` (trong dialog) | **Left** (mặc định) | `formatDateTime()` | `dd-MM-yyyy HH:mm:ss` |
| 11 | **Mã code** | `code`, `refNo`, `refNoManagement`, `invoiceNumber` | **Left** (mặc định) | Raw `\| ''` | Style `text-blue-700 font-medium` |
| 12 | **Tên** | `name`, `accountObjectName`, `employeeName` | **Left** (mặc định) | Raw `\| ''` | Style `text-black truncate` |
| 13 | **Địa chỉ** | `address`, `accountObjectAddress` | **Left** (mặc định) | Raw `\| ''` | `truncate` |
| 14 | **Diễn giải** | `description`, `reason` | **Left** (mặc định) | Raw `\| ''` | `truncate` + `title={fullText}` |
| 15 | **Số điện thoại** | `phone`, `phoneNumber` | **Left** (mặc định) | `formatPhoneNumber()` | `"0912 345 678"` |
| 16 | **Mã số thuế** | `taxCode` | **Left** (mặc định) | `formatTaxCode()` | `"1234-567-890"` |
| 17 | **Email** | `email` | **Left** (mặc định) | Raw `\| ''` | `truncate` |
| 18 | **Boolean / Trạng thái** | `isPosted`, `isActive`, `isLocked` | **Center** `text-center` | Badge component | Pill: xanh lá (true), amber/đỏ (false) |
| 19 | **Enum / Loại** | `refType`, `paymentMethod`, `gender` | **Left** (mặc định) | Label lookup | Qua `*_LABELS` map |
| 20 | **Object / FK (đã resolve)** | `accountObjectName`, `employeeName` | **Left** (mặc định) | Raw `\| ''` | Đã join sẵn từ API |

### 12.2a Quy Tắc Font-Weight Cho Cell Trong Bảng

> ⚠️ **BẮT BUỘC:** Cell trong bảng mặc định dùng `font-normal` (400) — nét chữ thanh, dễ đọc. **KHÔNG dùng `font-medium` (500) làm mặc định** cho bất kỳ cell nào.

| Loại cell | Font-weight | Ghi chú |
|-----------|------------|--------|
| **Mặc định** (text, tên, địa chỉ, diễn giải, số tiền...) | `font-normal` (400) | Mặc định của trình duyệt — không cần khai báo class |
| **Số chứng từ / Mã link xanh** (`refNo`, `code`, `invoiceNumber`, `voucherCode`...) | `font-medium` (500) | Giữ để nhấn mạnh tính định danh |
| **Badge trạng thái** (`isPosted`, `isActive`) | `font-medium` | Giữ trong class `text-xs font-medium` của badge |
| **Hàng tổng cộng** | `font-semibold` (600) | Đậm hơn để phân biệt với data rows |
| **Header bảng** | `font-semibold` (600) | Mặc định trong `DmTableHead` |

```tsx
// ❌ SAI — font-medium mặc định cho mọi cell
const CELL_CLASS: Record<string, string> = {
  totalAmount: 'font-medium',
  name:        'font-medium text-black',
}
const getCellClass = (...) => {
  return (CELL_CLASS[field] ? `${CELL_CLASS[field]}` : 'text-black font-medium')
}

// ✅ ĐÚNG — font-normal mặc định, chỉ refNo giữ font-medium
const CELL_CLASS: Record<string, string> = {
  refNo: 'font-medium text-blue-700',  // ← chỉ field định danh link xanh
}
const getCellClass = (...) => {
  return (CELL_CLASS[field] ? `${CELL_CLASS[field]}` : 'text-black')
}
```

### 12.3 Bảng Tổng Hợp CELL_VALUE & CELL_CLASS Mẫu

> Áp dụng pattern này cho **MỌI** master page trong KetoanApp:

```tsx
import { formatNumber, formatDate, formatDateTime, formatPercent, formatVatRate } from '@/shared/utils'

const CELL_VALUE: Record<string, (item: XxxDto) => string> = {
  // === Số tiền (Right-align) ===
  totalAmount:    (i) => formatNumber(i.totalAmount),
  debitAmount:    (i) => formatNumber(i.debitAmount),
  unitPrice:      (i) => formatNumber(i.unitPrice),

  // === Số lượng (Right-align) ===
  quantity:       (i) => formatNumber(i.quantity),

  // === Ngày (Left-align, mặc định) ===
  refDate:        (i) => formatDate(i.refDate),
  postedDate:     (i) => i.postedDate ? formatDate(i.postedDate) : '',
  voucherDate:    (i) => formatDate(i.voucherDate),

  // === Mã code (Left-align, xanh primary) ===
  refNo:          (i) => i.refNo || '',
  code:           (i) => i.code || '',

  // === Tên (Left-align, bold) ===
  name:                       (i) => i.name || '',
  accountObjectName:          (i) => i.accountObjectName || '',
  employeeName:               (i) => i.employeeName || '',

  // === Text dài (Left-align, truncate) ===
  description:                 (i) => i.description || '',
  accountObjectAddress:        (i) => i.accountObjectAddress || '',

  // === Boolean (Center, Badge) ===
  isPosted:      (i) => i.isPosted ? 'Đã ghi sổ' : 'Chưa ghi sổ',
  isActive:      (i) => i.isActive ? 'Đang dùng' : 'Ngừng dùng',

  // === Enum (Left-align, Label lookup) ===
  refType:       (i) => getReceiptTypeLabel(Number(i.refType), i.reasonTypeId),
}

const CELL_CLASS: Record<string, string> = {
  // Mã (luôn xanh + font-medium để nhấn mạnh)
  refNo:         'font-medium text-blue-700',
  code:          'font-medium text-blue-700',

  // Tên
  name:                       'text-black truncate',
  accountObjectName:          'text-black truncate',
  employeeName:               'text-black truncate',

  // Text dài
  description:                 'text-black truncate',
  accountObjectAddress:        'text-black truncate',
}
```

### 12.4 Alignment Trong JSX — Pattern Chuẩn

```tsx
// Trong DmTableHead:
<DmTableHead
  className={cn(
    // Số → canh phải
    (col.field === 'totalAmount' || col.field === 'debitAmount' || col.field === 'quantity') && 'text-right',
    // Boolean / Badge → canh giữa
    (col.field === 'isPosted' || col.field === 'isActive') && 'text-center',
  )}
>

// Trong DmTableCell (data rows):
<DmTableCell
  className={cn(
    getCellClass(col.field, item),
    // Số → canh phải
    (col.field === 'totalAmount' || col.field === 'debitAmount' || col.field === 'quantity') && 'text-right',
    // Boolean / Badge → canh giữa
    (col.field === 'isPosted' || col.field === 'isActive') && 'text-center',
  )}
>
```

### 12.5 Quy Tắc Giá Trị Rỗng

| Ngữ cảnh | Quy tắc | Ví dụ |
|----------|---------|-------|
| **Table cell (CELL_VALUE)** | `''` — chuỗi rỗng | `(i) => i.code \|\| ''` |
| **Dialog header/footer total** | `formatCurrency(0)` — không bỏ trống | `formatCurrency(totalAmount)` luôn hiển thị |
| **Form input (view mode)** | `''` — để trống | `<div>{value \|\| ''}</div>` |
| **Ngày null** | `''` — không dùng `'-'` | `(i) => i.postedDate ? formatDate(i.postedDate) : ''` |
| **Fallback render function** | `?? (() => '')` | `(CELL_VALUE[col.field] ?? (() => ''))(item)` |

> ⚠️ **TUYỆT ĐỐI CẤM dùng `'-'`** cho giá trị rỗng — đây là "chartjunk", gây rối mắt, vi phạm nguyên tắc data-ink ratio. Ô trống = không có dữ liệu, không cần đánh dấu.

### 12.6 Quy Tắc Dùng `truncate`

| Cột | `truncate`? | Tooltip `title`? | Lý do |
|-----|------------|-----------------|-------|
| `name`, `accountObjectName` | ✅ Có | ✅ Có | Tên đối tượng dài |
| `description` | ✅ Có | ✅ Có | Diễn giải dài |
| `address` | ✅ Có | ✅ Có | Địa chỉ dài |
| `code`, `refNo` | Không | Không | Mã thường ngắn < 20 ký tự |
| `totalAmount`, `quantity` | Không | Không | Số đã format ngắn |
| `isPosted`, `isActive` | Không | Không | Badge cố định |
| `refDate`, `postedDate` | Không | Không | Ngày format cố định `dd-MM-yyyy` |

> **`DmTableCell` đã mặc định `truncate`** — nhưng với cột tên, địa chỉ nên thêm `title={fullText}` để hiển thị tooltip khi hover.

### 12.7 Độ Rộng Cột Gợi Ý Theo Loại Dữ Liệu

| Loại dữ liệu | Độ rộng gợi ý | Lý do |
|-------------|-------------|-------|
| Checkbox (chọn) | `40px` | Cố định |
| STT | `60px` | Số thứ tự 1-999 |
| Mã (code, refNo) | `120-160px` | Mã ~10-20 ký tự |
| Ngày (refDate) | `110px` | `dd-MM-yyyy` = 10 ký tự |
| Số tiền | `130-150px` | `9.999.999.999` max |
| Trạng thái (badge) | `120px` | `"Chưa ghi sổ"` ~12 ký tự |
| Tên (name) | `180-250px` | Tên dài, có `truncate` |
| Diễn giải (desc) | `200-300px` | Text dài, có `truncate` |
| Địa chỉ | `200-300px` | Text dài, có `truncate` |
| Ghost action | `0px` | Overlay, không chiếm space |

### 12.8 Cột Định Danh (Identifier Column) — Click Mở View (BẮT BUỘC)

> **Tham khảo đầy đủ:** `tao-master-page` Section 2.1a.
> **Reference implementation:** `PhieuThuPage.tsx`.

Cột định danh (mã, số chứng từ, số tài khoản...) phải có style xanh + click được để mở dialog **xem chi tiết**. Đây là hành vi bổ sung cho double-click (mở Edit).

| Loại trang | Cột định danh | Class bắt buộc |
|-----------|--------------|----------------|
| Nghiệp vụ (phiếu thu/chi, mua/bán, kho...) | `refNo`, `refNoManagement`, `invoiceNumber`, `voucherCode`, `returnNo`, `returnCode`, `discountNo`, `discountCode`, `orderNo`, `orderCode` | `text-[#1B6FC8] font-medium cursor-pointer hover:underline` |
| Danh mục CRUD (KH, NCC, HH, NV, Kho, Tiền tệ...) | `code` | `font-medium text-blue-700 cursor-pointer hover:underline` |
| Đơn vị tính | `name` (không có `code`) | `text-black cursor-pointer hover:underline` |
| Tài khoản (bảng cây) | `accountNumber` | `font-mono text-[#1B6FC8] cursor-pointer hover:underline` |

**Quy tắc render (áp dụng cho mọi pattern):**
- Bọc giá trị trong `<span onClick={e => { e.stopPropagation(); ... }}>` để không trigger `onDoubleClick` của row
- `data-qa` format: `link_{fieldName}_{item.id}`
- Handler: nghiệp vụ dùng `setSelectedId`+`setDialogMode('view')`, danh mục dùng `setSelectedItem`

```tsx
// Pattern nghiệp vụ (trong getCellClass + render cell)
const getCellClass = (field: string, _item?: Dto) => {
  if (field === 'refNo') return 'text-[#1B6FC8] font-medium cursor-pointer hover:underline'
  // ...
}
// Trong render:
{col.field === 'refNo' ? (
  <span className='cursor-pointer hover:underline'
    onClick={(e) => { e.stopPropagation(); setSelectedId(item.id); setDialogMode('view'); setDialogOpen(true) }}
    data-qa={`link_refNo_${item.id}`}>{item.refNo || ''}</span>
) : /* badge / CELL_VALUE fallback */}

// Pattern danh mục (trong CELL_CLASS + render cell)
const CELL_CLASS = { code: 'font-medium text-blue-700 cursor-pointer hover:underline', ... }
// Trong render:
{col.field === 'code' ? (
  <span className='cursor-pointer hover:underline'
    onClick={(e: React.MouseEvent) => { e.stopPropagation(); setSelectedItem(item); setDialogOpen(true) }}
    data-qa={`link_code_${item.id}`}>{item.code || ''}</span>
) : ((CELL_VALUE[col.field] ?? (() => ''))(item))}
```

---

## 13. Import Chuẩn — Tránh Runtime Error

```tsx
// ✅ cn()
import { cn } from '@/shared/components/ui/utils'

// ✅ Validate
import { validateAllFields, hasAnyError } from '@/shared/utils/ValidationUtils'
import { showValidationErrorsToast } from '@/shared/utils/ValidationToastHelper'

// ❌ SAI
import { cn } from '@/lib/utils'
import { cn } from '@/shared/utils/cn'
```

---

## 14. Nguyên Tắc Cốt Lõi

- File `.tsx` chỉ chứa UI — **toàn bộ logic** đặt trong `/hooks/`
- **KHÔNG** gọi API trực tiếp từ Pages / Components / Dialogs
- **KHÔNG** hardcode API URL
- **KHÔNG** tạo lại utils / components đã có trong `/shared`
- **KHÔNG** dùng `any` trong TypeScript
- Dùng `ConfirmDialog` cho xóa, `ValidationErrorDialog` cho lỗi server
- ⚠️ **KHÔNG tự thêm field vào `types.api.ts` (DTO)** — field UI có mà BE chưa có → tạo inbox/yêu cầu BE bổ sung. FE và BE phải thống nhất DTO.

---

## 15. Checklist Chung

- [ ] Component đúng pattern (DmFormField cho Danh Mục, Label+Input cho Nghiệp Vụ)
- [ ] 3 mode hoạt động (View/Create/Edit) với isReadonly flag
- [ ] View mode: DmFieldValue / DmTabFieldValue / `<div>` (không input disabled)
- [ ] Validate onBlur + inline error message
- [ ] Input số: `type='text' inputMode='numeric'` + `text-right`
- [ ] FK: SearchCombobox / TableSearchCombobox / DmGroupInput
- [ ] data-qa đầy đủ (btn_, i_, sel_, dt_, chk_, r_, tab_)
- [ ] `cn()` import đúng: `@/shared/components/ui/utils`
- [ ] Dialog footer đúng pattern
- [ ] Nút X custom (ẩn Radix mặc định)
- [ ] Compile không lỗi, không runtime error
- [ ] **KHÔNG tự thêm field vào types.api.ts — field UI có mà BE chưa có → tạo inbox BE**
- [ ] ⚠️ **Reset state dialog:** Hook có `useEffect([initialData])` reset `formData` — form phải theo giá trị mới khi đóng/mở lại

---

## 🔥 Lỗi Hay Gặp Khi Code Dialog (Checklist Tránh Lặp)

> **Mục đích:** Liệt kê các lỗi phổ biến trong dialog KetoanApp. Đọc trước khi code để tránh.

### 1. ❌ KHÔNG set `font-family` ở bất kỳ đâu

Font kế thừa từ `body` (`globals.css`: Inter → InterVariable → "Noto Sans" → "Open Sans" → sans-serif). Mọi `font-family` override trong dialog đều bị cấm.

```
❌ SAI: className='font-sans', style={{ fontFamily: 'Inter' }}
✅ ĐÚNG: KHÔNG set font-family — để element kế thừa từ body
```

### 2. ❌ Thiếu `showQuickAdd` trên TableSearchCombobox cho FK

**MỌI** `TableSearchCombobox` dùng chọn FK (NCC, Hàng hóa, Kho, Nhân viên, Tài khoản...) PHẢI có nút (+) tạo nhanh:

```
❌ SAI: <TableSearchCombobox value={...} loadOptions={loadNCC} columns={nccColumns}
           onChange={handleNccChange} />

✅ ĐÚNG: <TableSearchCombobox value={...} loadOptions={loadNCC} columns={nccColumns}
           onChange={handleNccChange}
           showQuickAdd
           onCreateClick={() => { setNccDialogOpen(true) }} />
```

**Quy tắc:** Nếu combobox chọn từ danh mục (có thể tạo mới) → có `showQuickAdd`. Nếu combobox chọn từ enum cố định (trạng thái, loại) → không cần.

### 3. ❌ Import sai `formatCurrency` path

Một số dialog import `formatCurrency` từ `@/shared/InvoiceDesigner/utils/data-binding.utils` — đây là path sai. Luôn import từ `@/shared/utils`:

```
❌ SAI: import { formatCurrency } from '@/shared/InvoiceDesigner/utils/data-binding.utils'
✅ ĐÚNG: import { formatCurrency } from '@/shared/utils'
```

### 4. ❌ Thiếu `UnsavedChangesConfirm` trong dialog

Dialog nghiệp vụ full-screen PHẢI có `UnsavedChangesConfirm` để cảnh báo khi user vô tình đóng:

```
✅ ĐÚNG: <UnsavedChangesConfirm
           open={dialogOpen}
           dirty={isDirty}
           onConfirm={() => { /* đóng */ }}
         />
```

### 5. ❌ Form field số dùng `type='number'`

```
❌ SAI: <Input type='number' ... />
✅ ĐÚNG: <Input type='text' inputMode='numeric' className='... text-right' ... />
```

### 6. ❌ View mode dùng `<Input disabled>` thay vì `<DmFieldValue>`

```
❌ SAI: <Input value={formData.name} disabled />
✅ ĐÚNG: <DmFieldValue value={formData.name} />
```

### 7. ❌ FK field chỉ gửi ID, thiếu code/name cho display

Khi chọn FK trong TableSearchCombobox, ngoài `id` cần lưu thêm `code` và `name` để hiển thị trong view mode và gửi lên payload:

```
❌ SAI: onChange={(id) => setField('nccId', id)}
✅ ĐÚNG: onChange={(id, rowData) => {
           setField('nccId', id)
           setField('nccCode', rowData.code || '')
           setField('nccName', rowData.name || '')
         }}
```

### 8. ❌ Dialog không reset form khi đóng/mở lại

Hook phải có `useEffect` reset `formData` theo `initialData` để khi đóng/mở dialog form luôn fresh:

```tsx
// Trong hook
useEffect(() => {
  if (initialData) setFormData(initialData)
}, [initialData])
```
