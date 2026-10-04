---
name: tao-ui-giao-dien
description: 'FOUNDATION — Quy tắc nền tảng UI dùng chung cho MỌI loại giao diện trong SASUCO InvoiceEasy: buttons (btn-primary/btn-secondary/btn-danger), table row action icons (.icon-primary/.icon-warning/.icon-success/.icon-danger), data-qa attributes, format utilities (formatCurrency/formatDate/formatNumber), SearchCombobox cho foreignKey, textarea invoice-textarea, conditional styling với cn(). Skill này là nền tảng — các skill tao-master-page / tao-dialog / tao-sub-page đều kế thừa rules ở đây.'
---

# Quy Tắc UI Nền Tảng — SASUCO InvoiceEasy

> **ĐÂY LÀ SKILL FOUNDATION** — Áp dụng cho MỌI loại UI.
> Khi làm master page → load thêm `tao-master-page`.
> Khi làm dialog/form → load thêm `tao-dialog`.
> Khi làm sub page (full-screen) → load thêm `tao-sub-page`.

---

## Nguyên Tắc Cốt Lõi

- File `.tsx` chỉ chứa UI — **toàn bộ logic** đặt trong `/hooks/`
- Card wrapper chuẩn: `<Card className='border-[#e0e0e0]'><CardContent className='p-6'>`
- Spacing giữa sections: `space-y-6`
- Dùng `ConfirmDialog`, `ValidationErrorDialog`, `PagingUtils` từ `@/shared/components/common`

---

## Chọn Loại UI

| Loại UI | Khi nào dùng |
|---|---|
| **Master Page** | Danh sách dữ liệu có phân trang, CRUD qua dialog overlay, ≤ 8 cột |
| **Dialog** | Form ≤ 10 fields, tác vụ nhanh, CRUD đơn giản, vừa trong 600–800px |
| **Sub Page** | Form > 10 fields nhiều section, cần breadcrumb/back, có tab/wizard, hiển thị table con |

> Load skill tương ứng: `tao-ui-master-page` / `tao-ui-dialog` / `tao-ui-sub-page`

---

## Input Fields — Quy Tắc Chung

> Áp dụng cho cả Dialog và Sub Page.

**Validate on BLUR — BẮT BUỘC:**
- ✅ `onBlur={() => handleBlur('fieldName')}` — validate khi rời field
- ❌ validate trong `onChange` — làm UI jitter khi đang gõ

**View mode — thay input bằng div:**
- Văn bản: `<div className='px-3 py-2 text-gray-900'>{value || '-'}</div>`
- Đa dòng: thêm `whitespace-pre-wrap`
- Số tiền: thêm `text-right`
- Trạng thái: dùng `<Badge>`

**Input số:**
- `type='text' inputMode='numeric'` — **không dùng** `type='number'`
- Hiển thị: `formatNumber(n)` — parse về số: `value.replace(/\./g, '')`
- Căn phải: `text-right`

**Input lỗi:** `cn('invoice-input', errors.field && 'border-destructive')` + `<AlertCircle className='h-3 w-3' />`

**ForeignKey:** dùng `SearchCombobox` — không dùng `<input>` nhập thủ công ID

---

## Form Row Layout — Grid vs Flex (BẮT BUỘC)

> **🚨 NGUYÊN NHÂN GÂY INPUT "DÚM LẠI/CONPACT":** `flex` + `items-end` + `w-fraction` làm các cột co theo nội dung, input bị ép nhỏ, mất hết không gian bề ngang. Cực kỳ tinh vi, khó phát hiện, nhưng chỉ cần sai 1 dòng layout là toàn bộ form hỏng.

### Quy tắc

| Pattern | Dùng khi | ✅ / ❌ |
|---------|----------|---------|
| `grid grid-cols-2 gap-4` | Form 2 cột (label+input mỗi cột) | ✅ **LUÔN DÙNG** |
| `grid grid-cols-3 gap-4` | Form 3 cột | ✅ |
| `flex gap-3` + `flex-1 min-w-0` | Filters/search bar (co giãn tự do) | ✅ |
| `flex gap-3 items-end` + `w-2/3` `w-1/3` | Form row với tỉ lệ khác nhau | ❌ **CẤM** |

### Ví dụ

```tsx
// ✅ ĐÚNG — grid 2 cột bằng nhau, input luôn full-width trong cột
<div className='grid grid-cols-2 gap-4'>
  <div className='space-y-1.5'>
    <Label>Tên doanh nghiệp <span className='text-red-500'>*</span></Label>
    <Input className='invoice-input' value={form.tenNNT} ... />
  </div>
  <div className='space-y-1.5'>
    <Label>Mã số thuế <span className='text-red-500'>*</span></Label>
    <Input className='invoice-input' value={form.mst} ... />
  </div>
</div>

// ❌ SAI — flex + items-end + w-fraction = input dúm lại vì flex container co theo nội dung
<div className='flex gap-3 items-end'>
  <div className='space-y-1.5 w-2/3'>...</div>
  <div className='space-y-1.5 w-1/3'>...</div>
</div>
```

### Tại sao `flex` gây lỗi còn `grid` thì không?

- **Flex**: `items-end` căn chỉnh các item theo baseline dưới cùng → mỗi cột cao thấp khác nhau (khi có error message) → input bị co lại. `w-2/3` và `w-1/3` KHÔNG đảm bảo tổng = 100% khi có `gap`.
- **Grid**: `grid-cols-2` ép mỗi cột luôn bằng đúng 50% chiều ngang container → input luôn giãn full-width trong cột → không bao giờ dúm.

> ⚠️ **RULE CỨNG:** Mọi form row có ≥ 2 cột trong Card **PHẢI** dùng `grid grid-cols-N gap-4`. Tuyệt đối không dùng `flex` + `w-fraction` cho form row.

---

## Buttons

> **Chỉ dùng CSS class từ `globals.css` — không dùng Tailwind `bg-*` cho button**

| Class | Khi nào dùng |
|-------|-------------|
| `.btn-primary` | Thêm mới, Lưu, Xác nhận, Tạo mới |
| `.btn-secondary` | Đóng, Hủy, Xuất Excel, Làm mới |
| `.btn-danger` | Xóa (phải kèm `ConfirmDialog`) |

**Nút Làm mới:** thêm `animate-spin` khi đang tải, `disabled={refreshing}`.

---

## Table Row Action Icons

> Dùng cho cột **Thao tác** trong bảng — `variant='ghost' size='sm'` + icon class bên dưới.

> **Vị trí:** Không có cột Thao tác visible. Action hiện dạng overlay khi hover row, neo vào cột `sticky right-0` với `width=0`. Luôn ở mép phải viewport, không bị scroll ngang che khuất (`opacity-0 group-hover:opacity-100`).

| Icon class | Màu hex | Lucide Icon | Dùng cho |
|-----------|---------|-------------|---------|
| `.icon-primary` | `#1565C0` xanh | `Eye` | Xem chi tiết |
| `.icon-warning` | `#ff9800` cam | `Pencil` | Chỉnh sửa |
| `.icon-success` | `#4caf50` xanh lá | `Copy` | Nhân bản |
| `.icon-danger` | `#f44336` đỏ | `Trash2` | Xóa |

### Button Component Pattern cho Row Action

> **Dùng `DmRowActions` từ `@/modules/KetoanApp/components` cho action chuẩn.**
> Khi cần thêm nút tùy chỉnh (vd: `...` dropdown trigger), dùng `Button` thủ công với cùng style bên dưới.

```tsx
// Pattern A — Dùng DmRowActions (khuyến nghị cho standard CRUD)
<DmRowActions actions={getRowActions(item)} />

// Pattern B — Button thủ công (khi cần custom layout hoặc mix với DropdownMenu)
<Button variant='ghost' size='sm'
  className='icon-warning border rounded-lg bg-white'  // ← icon class + border + rounded-lg + bg-white
  title='Sửa'
  data-qa={`btn_sua_${item.id}`}
  onClick={() => handleEdit(item)}
>
  <Pencil className='h-4 w-4' />  {/* ← icon size cố định */}
</Button>
```

| Quy tắc | ✅ Đúng | ❌ Sai |
|---------|--------|-------|
| Button variant | `variant='ghost'` | `variant='outline'` |
| Button size | `size='sm'` | `size='icon'` hoặc `size='xs'` |
| Class nền | `border rounded-lg bg-white` | `h-7 w-7 p-0` (tự set kích thước cứng) |
| Màu icon | Dùng icon class (`.icon-warning`, `.icon-danger`, etc.) | Dùng `text-red-500` hoặc Tailwind màu |
| Icon size | `className='h-4 w-4'` | `className='h-3 w-3'` hoặc `h-5 w-5` |
| Nút `...` (chức năng khác) | `variant='ghost' size='sm' className='border rounded-lg bg-white'` | `rounded-full` hoặc `h-7 w-7 p-0` |

> ⚠️ **Không dùng `h-7 w-7 p-0`** — để `size='sm'` tự kiểm soát kích thước nút, đồng bộ với `DmRowActions`. Kích thước `size='sm'` cho nút icon-only tự động thành `h-8 w-8`.

---

## Textarea

`invoice-textarea` dùng border dashed (`border-2 border-dashed`) — nhận biết trường tự do đa dòng.

| Trường hợp | Class |
|-----------|-------|
| Mô tả, ghi chú | `invoice-textarea` |
| Code / nội dung kỹ thuật | `invoice-textarea font-mono text-xs` |
| ❌ Cấm | `invoice-input` cho textarea |

**Kích thước rows:**

| Loại nội dung | `rows` |
|--------------|--------|
| Mô tả ngắn | `2` |
| Ghi chú | `3` |
| Nội dung dài | `4–5` |
| Code / HTML | `8–12` |

Ưu tiên dùng `<FormFieldTextarea>` từ `@/shared/components/common` cho dialog 3 mode (View/Create/Edit).

→ **Template code mẫu:** `.claude/skills/templates-for-skills/tpl.foundation.textarea.md`

---

## SearchCombobox — BẮT BUỘC cho foreignKey

> **Cấm dùng `<input type='text'>` để nhập thủ công ID tham chiếu.** Luôn dùng `SearchCombobox`.

| Prop | Type | Bắt buộc | Ghi chú |
|------|------|----------|---------|
| `value` | `string` | ✅ | id đang chọn |
| `onChange` | `(value: string, label: string) => void` | ✅ | callback khi chọn |
| `loadOptions` | `(keyword: string) => Promise<ComboboxOption[]>` | ✅ | hàm load từ API |
| `placeholder` | `string` | | Text khi chưa chọn |
| `searchPlaceholder` | `string` | | Placeholder ô tìm kiếm |
| `dataQa` | `string` | ✅ | Prefix `sel_` |
| `disabled` | `boolean` | | |
| `debounceMs` | `number` | | mặc định 400ms |
| `className` | `string` | | override kích thước |

**Quy tắc cross-portal API:**
- Được phép gọi cross-portal từ BaseIndexApp, SsoApp... qua service đã có sẵn
- Không tạo lại service nếu đã có trong `BaseIndexApp/features/`
- `ComboboxOption` luôn có `value = id`, `label = name`, `subLabel = code hoặc thông tin phụ`

→ **Template loadOptions + cách dùng:** `.claude/skills/templates-for-skills/tpl.foundation.search-combobox.md`

---

## Styling Có Điều Kiện

```tsx
// ✅ Đúng — dùng cn()
<div className={cn('base', isActive && 'bg-blue-600 text-white')}>

// ❌ Sai — Tailwind JIT không quét được
<div className={`bg-${color}-500`}>
```

---

## Format Utilities (từ `@/shared/utils`)

| Hàm | Output |
|-----|--------|
| `formatCurrency(n)` | `"1.000.000 ₫"` |
| `formatDate(s)` | `"15-01-2024"` |
| `formatDateTime(s)` | `"15-01-2024 10:30:45"` |
| `formatNumber(n)` | `"1.234.567"` |
| `formatPercent(n)` | `"87.50%"` |
| `formatPhoneNumber(s)` | `"0912 345 678"` |
| `formatTaxCode(s)` | `"0123-456-789"` |

Tất cả xử lý `null/undefined` → trả về `"-"`.

---

## data-qa (BẮT BUỘC cho mọi phần tử tương tác)

| Phần tử | Prefix | Ví dụ |
|--------|--------|-------|
| Button | `btn_` | `btn_them_moi`, `btn_luu`, `btn_xoa` |
| Input / Textarea | `i_` | `i_ten`, `i_tim_kiem`, `i_so_luong` |
| Select / Combobox | `sel_` | `sel_trang_thai`, `sel_khach_hang` |
| Checkbox / Radio | `chk_` | `chk_chon_tat_ca` |
| DatePicker | `dt_` | `dt_tu_ngay`, `dt_den_ngay` |
| Tab | `tab_` | `tab_thong_tin`, `tab_lich_su` |

Table row actions thêm suffix `_{id}`: `btn_xem_{id}`, `btn_sua_{id}`, `btn_xoa_{id}`

---

## Responsive Mobile (BẮT BUỘC cho MỌI loại UI)

> Mọi trang, dialog, component **PHẢI** hỗ trợ mobile (≥320px). Không để layout vỡ trên màn hình nhỏ.

### Breakpoints Tailwind dùng trong dự án

| Breakpoint | Pixel | Dùng khi |
|---|---|---|
| `sm:` | ≥640px | Tablet nhỏ, landscape mobile |
| `md:` | ≥768px | Tablet |
| `lg:` | ≥1024px | Desktop |

### Header Page (BẮT BUỘC)

```tsx
// ✅ ĐÚNG — stack dọc trên mobile, ngang trên sm+
<div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
  <div>
    <h1>Tiêu đề trang</h1>
    <p className='text-sm text-gray-500'>Mô tả</p>
  </div>
  <div className='flex gap-2 flex-shrink-0'>
    {/* Buttons */}
  </div>
</div>

// ❌ SAI — bị đè / overflow trên mobile
<div className='flex items-center justify-between'>
```

### Grid Cards / Summary Cards

```tsx
// ✅ 4 cards
<div className='grid grid-cols-2 sm:grid-cols-4 gap-4'>
// ✅ 3 cards  
<div className='grid grid-cols-1 sm:grid-cols-3 gap-4'>
// ✅ 6 cards
<div className='grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4'>

// ❌ SAI — cố định cols không responsive
<div className='grid grid-cols-4 gap-4'>
```

### Filters Row

```tsx
// ✅ ĐÚNG — flex-wrap tự xuống dòng
<div className='flex flex-wrap gap-3 items-end'>
  <input className='flex-1 min-w-[200px]' />
  <select className='w-[160px]' />
</div>

// ❌ SAI — overflow ngang
<div className='flex gap-4'>
```

### Quy Tắc Kiểm Tra (Checklist Responsive)

- [ ] Header: `flex-col sm:flex-row sm:justify-between gap-3`
- [ ] Grid cards cố định: có breakpoint `sm:` hoặc `lg:`
- [ ] Filters: `flex-wrap` để tự xuống dòng
- [ ] Table: có `overflow-x-auto` wrapper
- [ ] Dialog: `maxWidth` phù hợp, padding `p-4 md:p-6`
- [ ] Không có `grid grid-cols-N` (N≥3) **không có breakpoint** ở cấp page

---

## Import Chuẩn — Tránh Runtime Error

> **CRITICAL:** Các import sau hay bị nhầm — gây lỗi runtime Vite "Module not found" dù TypeScript không báo lỗi.

### `cn()` — Conditional className

```typescript
// ✅ ĐÚNG — dùng trong src/modules/**
import { cn } from '@/shared/components/ui/utils'

// ❌ SAI — path không tồn tại, gây runtime error
import { cn } from '@/shared/utils/cn'
import { cn } from '@/lib/utils'
```

> Kiểm tra: tìm file `utils.ts` trong `src/shared/components/ui/` — đây là nơi export `cn`.

### Validate Utils

```typescript
// ✅ ĐÚNG
import { validateAllFields, hasAnyError } from '@/shared/utils/ValidationUtils'
import { showValidationErrorsToast } from '@/shared/utils/ValidationToastHelper'

// ❌ SAI — validateAllFields KHÔNG export từ ValidationToastHelper
import { validateAllFields, hasAnyError, showValidationErrorsToast } from '@/shared/utils/ValidationToastHelper'
```

### Checklist trước khi submit code có import mới

- [ ] `cn` → `@/shared/components/ui/utils` ✅
- [ ] `validateAllFields` / `hasAnyError` → `@/shared/utils/ValidationUtils` ✅
- [ ] `showValidationErrorsToast` → `@/shared/utils/ValidationToastHelper` ✅
- [ ] Sau khi sửa import → `npm run dev` và kiểm tra console không có "Module not found"

---

## Auto-Discovery — Tích Hợp Sơ Đồ Dự Án (BẮT BUỘC)

> Hệ thống **Sơ đồ dự án** tự động quét toàn bộ codebase để liệt kê trang + chức năng mà không cần cấu hình thủ công.
> **Điều kiện hoạt động:** NavMenu, TopMenu và Page phải export đúng interface bên dưới.
> Đọc skill `tao-layout-navmenu-topmenu` để biết quy tắc đầy đủ cho NavMenu/TopMenu.

### data-qa — Cơ Chế Phát Hiện Tính Năng Tự Động

Sơ đồ dự án **quét source code** để tìm `data-qa` với prefix `btn_`, `row_`, `batch_` và sinh danh sách tính năng tự động.

**Quy tắc quan trọng:**

| Quy tắc | Chi tiết |
|---------|---------|
| **Prefix bắt buộc** | Button: `btn_`; Nút hành động hàng: `row_`; Nút hàng loạt: `batch_` |
| **Format** | Underscore `btn_lam_moi` hoặc hyphen `btn-lam-moi` — cả hai đều được detect |
| **Đặt đúng chỗ** | `data-qa` phải có trong JSX component/page, không trong biến string thuần |
| **Tính độc nhất** | Mỗi `data-qa` trên 1 trang phải là duy nhất — dùng suffix `_{id}` cho row actions |

**Các code phổ biến (auto-scan sẽ dịch sang nhãn tiếng Việt):**

```
btn_lam_moi / btn_them_moi / btn_tao_moi / btn_xoa / btn_sua
btn_xem_chi_tiet / btn_luu / btn_huy / btn_xuat_excel
row_view / row_edit / row_delete / row_clone / row_sign
batch_sign / batch_delete / batch_approve / batch_export
```

### PAGE_ID và PAGE_FEATURES — Khai Báo Tường Minh (Ưu Tiên Cao Nhất)

> Khi cần kiểm soát nhãn hoặc thứ tự tính năng chính xác: export `PAGE_ID` + `PAGE_FEATURES` từ file page.
> Auto-scan data-qa chỉ là fallback — `PAGE_FEATURES` luôn **ghi đè** kết quả auto-scan.

```typescript
// ✅ CHUẨN — đặt ngay sau imports, trước export function
// ─── Metadata cho sơ đồ dự án ─────────────────────────────
export const PAGE_ID = 'ten-trang'   // khớp với id trong NavMenu (kebab-case)
export const PAGE_FEATURES = [
  { label: 'Làm mới',                code: 'btn-refresh' },
  { label: 'Thêm mới',               code: 'btn-create' },
  { label: 'Xem chi tiết (dòng)',    code: 'row-view' },
  { label: 'Sửa (dòng)',             code: 'row-edit' },
  { label: 'Xóa (dòng)',             code: 'row-delete' },
  { label: 'Ký theo lô (đã chọn)',   code: 'batch-sign' },
]
// ──────────────────────────────────────────────────────────

export function TenTrangPage() { ... }
```

**Quy tắc `PAGE_ID`:**
- Phải **khớp hoàn toàn** với `id` khai báo trong NavMenu — sơ đồ dự án mới map được
- Format: `kebab-case`, ví dụ: `'invoice-management'`, `'ban-hang'`, `'khach-hang'`
- Nếu không export `PAGE_ID`: hệ thống fallback sang tên file (vd: `BanHangPage.tsx` → `'ban-hang'`)
- Chỉ cần khi tên file không tự động derive đúng pageId

**Thứ tự features trong `PAGE_FEATURES`:**
1. `btn-*` (button hành động chính) — theo thứ tự xuất hiện trên UI
2. `row-*` (nút hành động trên hàng) — Xem → Sửa → Nhân bản → Xóa
3. `batch-*` (hành động hàng loạt)

### Checklist Auto-Discovery

- [ ] File page có `data-qa` trên **tất cả** button/action tương tác (prefix `btn_`, `row_`, `batch_`)
- [ ] `PAGE_ID` export (nếu tên file không tự derive đúng) hoặc để hệ thống auto-detect từ tên file
- [ ] `PAGE_FEATURES` export khi cần label chính xác / thứ tự cụ thể
- [ ] `PAGE_ID` khớp với `id` trong NavMenu của portal tương ứng
- [ ] Xem skill `tao-layout-navmenu-topmenu` để đảm bảo NavMenu/TopMenu export đúng interface
