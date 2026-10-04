---
name: tao-ui-sub-page
description: 'Quy tắc tạo Sub Page (trang full-screen đặc biệt, không dùng dialog) trong SASUCO InvoiceEasy. Dùng khi: form quá nhiều fields không vừa dialog, trang có nhiều section/tab phức tạp, cần breadcrumb + nút Back, trang chi tiết hóa đơn, trang wizard nhiều bước, trang cấu hình phức tạp. Cấu trúc: Breadcrumb→PageHeader→Content Sections (Cards). Luôn load thêm tao-ui-giao-dien (foundation).'
---

# Quy Tắc Sub Page — SASUCO InvoiceEasy

> **Rules nền tảng (buttons, icon classes, data-qa, SearchCombobox, Textarea, format)** → đọc `tao-ui-giao-dien`.

---

## Khi Nào Dùng Sub Page (không dùng Dialog)

→ Xem bảng **Chọn Loại UI** tại `tao-ui-giao-dien`.

---

## PAGE_ID + PAGE_FEATURES (BẮT BUỘC)

> **Mọi Sub Page PHẢI khai báo `PAGE_ID` và `PAGE_FEATURES` để sơ đồ dự án và export menu permission hoạt động.**

```tsx
// Metadata cho so do du an
export const PAGE_ID = 'ten-page-id'  // phai khop navItem.id trong NavMenu
export const PAGE_FEATURES = [
  { label: 'Làm mới',         code: 'btn-refresh' },
  { label: 'Lưu thay đổi',    code: 'btn-save' },
  { label: 'Quay lại',        code: 'btn-back' },
]
// ---
```

- `PAGE_ID` phải khớp với `navItem.id` trong `NavMenu` portal tương ứng
- `PAGE_FEATURES` liệt kê TẤT CẢ các nút/thao tác thực tế có trong trang
- `code` prefix: `btn-` cho nút toolbar/header, `row-` cho action trên dòng
- Đặt ở đầu file, ngay trước `export function XxxPage()`
- Xem chi tiết tại `export-menu-page-permission/SKILL.md`

---

## Cấu Trúc Layout (BẮT BUỘC)

```
<>
  ├── [1] Sticky Header (Breadcrumb + Page Header) — nổi lên khi scroll
  └── [2] Content Cards (cuộn bên dưới sticky)
        ├── Card thông tin chính
        ├── Card thông tin phụ (nếu có)
        ├── Card bảng chi tiết / detail lines (nếu có)
        └── Card lịch sử / log (nếu có)
</>
```

> **Layout `main` của portal có `p-6`** — sticky phải bù trừ đúng để không hở.

→ **Skeleton JSX + Routing:** `.claude/skills/templates-for-skills/tpl.sub-page.skeleton-and-routing.md`

---

## [1] Sticky Header — Breadcrumb & Page Header

**Kỹ thuật sticky trong portal có `p-6` (BẮT BUỘC):**

```tsx
{/* Sticky header — bù trừ p-6 của main trong portal */}
<div className="sticky -top-6 z-20 bg-white border-b border-gray-100 shadow-sm -mx-6 -mt-6 px-6 pt-3 pb-3 space-y-2">
  {/* Breadcrumb */}
  <nav className="flex items-center gap-1 text-sm text-gray-500">
    ...
  </nav>
  {/* Page Header */}
  <div className="flex items-center justify-between">
    ...
  </div>
</div>

{/* Nội dung cuộn */}
<div className="space-y-3 px-6 pt-4 pb-6">
  ...cards...
</div>
```

**Giải thích kỹ thuật `-top-6 / -mx-6 / -mt-6`:**
- `main` của portal có `p-6` (24px) — scroll container là `main`
- `top: 0` bám vào *content edge* (trong padding) → còn 24px gap hở phía trên
- `-top-6` (top: -24px) → bám vào *visual top* (ngoài padding), loại bỏ gap
- `-mt-6 -mx-6` → kéo element ra ngoài padding box để nền trắng phủ kín toàn bộ
- `px-6` bên trong → căn nội dung thẳng hàng với các card bên dưới

> ⚠️ Nếu `main` của portal có padding khác (`p-4`, `p-8`...) thì điều chỉnh `-top-{n}`, `-mt-{n}`, `-mx-{n}` tương ứng.

**Breadcrumb:**
- `<nav className="flex items-center gap-1 text-sm text-gray-500">`
- Dùng `ChevronRight` icon giữa các cấp
- Cấp cuối: `text-gray-900 font-medium`, không phải button

**Page Header:**
- Luôn có nút **Back** (`ArrowLeft`): `btn-secondary p-2`, `data-qa='btn_quay_lai'`
- Tiêu đề `text-xl font-semibold text-gray-900` thay đổi theo mode: "Chi tiết" / "Chỉnh sửa" / "Tạo mới"
- Action buttons theo mode:
  - View → nút "Chỉnh sửa" (`btn-primary`)
  - Edit/Create → nút "Hủy" (`btn-secondary`) + nút "Lưu thay đổi"/"Tạo mới" (`btn-primary`)
- Nút Hủy và Lưu đều `disabled={saving}`

→ **Template:** `.claude/skills/templates-for-skills/tpl.sub-page.breadcrumb-and-header.md`

---

## [2] Content Cards

**Card thông tin cơ bản:**
- `<CardHeader className='pb-4'>` + `<CardTitle className='text-base font-semibold'>`
- `<CardContent className='space-y-3'>` — **KHÔNG** dùng `grid grid-cols-2` trực tiếp trong CardContent
- Bố cục bên trong: **grid theo từng hàng (row)**, mỗi hàng là một `div.grid.grid-cols-N.gap-3.items-end`
- Field yêu cầu bị gộp lại trong `col-span-2` hoặc `col-span-3` nếu cần chiếm nhiều cột

**Quy tắc chọn số cột (grid-cols-N):**
- Thường dùng `grid-cols-5` hoặc `grid-cols-6` — khợp với lưới của Card thông tin phiếu thu/chi
- Mỗi field mặc định chiếm 1 cột; field hủy tên / textarea / lý do dùng `col-span-2` hoặc `col-span-3`

**Mỗi field trong grid:**
```tsx
<div className='space-y-1.5'>
  <Label>Nhãn <span className='text-red-500'>*</span></Label>  {/* hoặc không có * */}
  {/* input / DatePicker / SearchCombobox / readonly div */}
  {touched.field && errors.field && (
    <p className='flex items-center gap-1 text-xs text-destructive'>
      <AlertCircle className='h-3 w-3' />{errors.field}
    </p>
  )}
</div>
```

**Nút thêm nhanh FK (nằm trong label row):**
```tsx
<div className='flex items-center justify-between'>
  <Label>FK Field <span className='text-red-500'>*</span></Label>
  <Tooltip>
    <TooltipTrigger asChild>
      <Button type='button' variant='ghost' size='sm'
        data-qa='btn_tao_nhanh_xxx'
        className='h-7 w-7 rounded-full p-0 text-[#1565C0] bg-blue-50 hover:bg-[#1565C0] hover:text-white hover:shadow-md hover:scale-105 transition-all duration-200'
        onClick={onTaoNhanh}
      >
        <Plus className='h-3.5 w-3.5' />
      </Button>
    </TooltipTrigger>
    <TooltipContent>Tạo mới ...</TooltipContent>
  </Tooltip>
</div>
```

**Field chỉ đọc (view mode hoặc auto-generated):**
```tsx
<div className='h-9 flex items-center px-3 text-gray-900 rounded-md border border-slate-100 bg-slate-50'>
  {value || '—'}
</div>
```

**Field số tiền (read-only, right-align):**
```tsx
<div className={cn(
  'h-9 flex items-center justify-end px-3 text-sm font-semibold rounded-md border',
  errors.soTien && touched.soTien
    ? 'border-destructive text-destructive'
    : 'border-slate-100 bg-slate-50 text-gray-900'
)}>
  {formatCurrency(total)}
</div>
```

→ **Template:** `.claude/skills/templates-for-skills/tpl.sub-page.card-info.md`

**Card bảng chi tiết (detail lines):**
- `<CardContent className='p-0'>` — bảng sát cạnh card, không padding
- Nút "Thêm dòng" trong CardHeader, ẩn khi `isView`
- Dòng tổng cộng: `bg-[#f8f9fa] font-medium`, chỉ có cột tổng `text-right`

→ **Template:** `.claude/skills/templates-for-skills/tpl.sub-page.card-detail-lines.md`

---

## Mode trong Sub Page

```ts
const { id } = useParams()
const isCreate = !id
const [pageMode, setPageMode] = useState<'view' | 'edit'>(isCreate ? 'edit' : 'view')
const isView = pageMode === 'view'
const isEdit = pageMode === 'edit'
```

---

## Routing Sub Page

- Sub page có **route riêng** trong routeConfig — không phải overlay
- Đường dẫn tạo mới: `ten-feature/tao-moi` (id = undefined → isCreate = true)
- Đường dẫn xem/sửa: `ten-feature/:id`

→ **Template routing:** `.claude/skills/templates-for-skills/tpl.sub-page.skeleton-and-routing.md`

---

## Checklist Sub Page

- [ ] Sticky header dùng đúng kỹ thuật `-top-6 -mx-6 -mt-6` (khớp với `p-6` của portal)
- [ ] Breadcrumb nằm trong sticky header
- [ ] Page Header nằm trong sticky header, action buttons đúng bên phải
- [ ] Có nút Back (`ArrowLeft`) trong Page Header, `data-qa='btn_quay_lai'`
- [ ] Tiêu đề đúng theo mode: Chi tiết / Chỉnh sửa / Tạo mới
- [ ] Action buttons: View → Sửa; Edit/Create → Hủy + Lưu
- [ ] Nút Hủy và Lưu `disabled={saving}`, Lưu có spinner
- [ ] Content cards nằm trong div `space-y-3 px-6 pt-4 pb-6` (bên dưới sticky)
- [ ] Mỗi section dùng `<Card className='border-[#e0e0e0]'>` riêng
- [ ] CardHeader: `<CardTitle className='text-base font-semibold'>`
- [ ] CardContent dùng `space-y-3` — **KHÔNG** dùng `grid-cols-2` trực tiếp trong CardContent
- [ ] Mỗi hàng fields: `<div className='grid grid-cols-N gap-3 items-end'>` (N = 5 hoặc 6)
- [ ] Mỗi field trong hàng: `<div className='space-y-1.5'>` + `Label` + input + error
- [ ] Inline error dùng `AlertCircle` + `flex items-center gap-1 text-xs text-destructive`
- [ ] Nút thêm nhanh FK: `Button variant='ghost' size='sm'` bên trong `flex items-center justify-between`
- [ ] Fields view mode: `<div className='h-9 flex items-center px-3 ... border border-slate-100 bg-slate-50'>`
- [ ] Field số tiền read-only: `justify-end font-semibold border-slate-100 bg-slate-50`

---

## Responsive Mobile (BẮT BUỘC)

> Sub page **PHẢI** hiển thị đúng từ 320px. Xem rules chi tiết tại `tao-ui-giao-dien`.

### Sticky Header — Page Header row

```tsx
{/* Page Header bên trong sticky */}
<div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
  <div className='flex items-center gap-2'>
    <Button variant='outline' size='sm' onClick={handleBack} data-qa='btn_quay_lai'>
      <ArrowLeft className='h-4 w-4' />
    </Button>
    <h1 className='text-xl font-semibold text-gray-900'>Tiêu đề</h1>
  </div>
  <div className='flex gap-2 flex-shrink-0'>
    {/* Action buttons */}
  </div>
</div>

// ❌ SAI — overflow header trên mobile
<div className='flex items-center justify-between'>
```

### Grid fields trong Card

```tsx
// ✅ ĐÚNG — responsive grid
<div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 items-end'>

// Hoặc dùng col-span để ưu tiên field quan trọng trên mobile
<div className='grid grid-cols-1 sm:grid-cols-5 gap-3 items-end'>
  <div className='sm:col-span-2 space-y-1.5'>...</div>
  <div className='sm:col-span-1 space-y-1.5'>...</div>
</div>

// ❌ SAI — cố định nhiều cột không có breakpoint
<div className='grid grid-cols-5 gap-3'>
```

### Checklist thêm vào Checklist Sub Page

- [ ] Sticky header row: `flex-col sm:flex-row sm:justify-between gap-3`
- [ ] Grid fields: có breakpoint `sm:` trước `grid-cols-N` (N≥3)
- [ ] Textarea view mode: thêm `whitespace-pre-wrap`
- [ ] Input số: `type='text' inputMode='numeric'`, `text-right`
- [ ] ForeignKey: `SearchCombobox`
- [ ] Validate on blur, không validate onChange
- [ ] Route sub page đăng ký đúng trong routeConfig
- [ ] Mọi phần tử tương tác có `data-qa`
