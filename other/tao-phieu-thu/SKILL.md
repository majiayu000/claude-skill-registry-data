---
name: tao-phieu-thu
description: 'Tạo hoặc chỉnh sửa trang Phiếu thu/Phiếu chi/Tiền gửi/Tiền vay trong KetoanApp. Extend từ tao-master-page, thêm rule: action trên dòng phụ thuộc trạng thái ghi sổ (isPosted), màu sắc phân biệt chưa/đã ghi sổ, cột số chứng từ màu primary, header chỉ hiển thị biểu tượng ghim nếu được chọn ghim trong setting.'
---

# Tạo Trang Phiếu Thu / Chi / Tiền Gửi — KetoanApp

> **Kế thừa:** `tao-master-page` (toàn bộ cấu trúc page), `tao-dialog-full` (dialog full-screen), `tao-ui-giao-dien-new` (foundation UI), `filter-phan-trang` (logic phân trang), `dat-ten` (quy tắc đặt tên).
>
> **Áp dụng cho:** TẤT CẢ các trang nghiệp vụ có trạng thái ghi sổ:
> - Phiếu thu tiền mặt (`phieu-thu`)
> - Phiếu chi tiền mặt (`phieu-chi`)
> - Tiền gửi ngân hàng (`tien-gui`)
> - Tiền vay (`tien-vay`)
> - Và các trang tương tự có field `isPosted: boolean`

---
## ⚠️ NGUYÊN TẮC SỐ 0: Giá Trị Rỗng → Để Trống, KHÔNG Dùng `-`

> **Đây là lỗi phổ biến nhất.** TUYỆT ĐỐI CẤM dùng `'-'` cho giá trị null/undefined/rỗng.

```tsx
// ❌ SAI — hiển thị dấu gạch ngang gây rối mắt
refNo:       (i) => i.refNo || '-'
description: (i) => i.description || '-'
postedDate:  (i) => i.postedDate ? formatDate(i.postedDate) : '-'

// ✅ ĐÚNG — để trống, giao diện sạch
refNo:       (i) => i.refNo || ''
description: (i) => i.description || ''
postedDate:  (i) => i.postedDate ? formatDate(i.postedDate) : ''
```

**Quy tắc cho MỌI field trong CELL_VALUE:**
- `|| ''` thay vì `|| '-'`
- `? formatDate(x) : ''` thay vì `? formatDate(x) : '-'`
- Fallback render: `(CELL_VALUE[col.field] ?? (() => ''))(item)` thay vì `() => '-'`

---
## 0. Quy Tắc Chung Kế Thừa Từ `tao-master-page`

Tải toàn bộ `tao-master-page/SKILL.md` làm nền tảng. Skill này CHỈ bổ sung các quy tắc đặc thù cho trang nghiệp vụ có trạng thái ghi sổ.

**Những gì đã có từ `tao-master-page` (không lặp lại):**
- Cấu trúc page: `DmPageHeader` → Card → `DmSearchToolbar` → **Header cố định** → **Body scrollable** → **Tổng cộng cố định** → `DmTablePagination` → Ghost scrollbar
- **Header & Tổng cộng cố định (BẮT BUỘC):** Header và hàng tổng cộng nằm NGOÀI vùng scroll, mỗi phần trong một `<DmTable>` riêng với `shrink-0 overflow-hidden`. Chỉ body mới scroll. Scroll ngang được đồng bộ qua `headerScrollRef`, `totalScrollRef`, `handleTableScroll`. Xem Section 0.0 bên dưới.
- Ghost column (width=0, sticky right) cho cột thao tác
- `onDoubleClick` mở View (xem chi tiết, `setDialogMode('view')`)
- **Click vào cột định danh (refNo/refNoManagement/invoiceNumber...) → mở View (BẮT BUỘC):** Xem `tao-master-page` Section 2.1a. `PhieuThuPage.tsx` là reference implementation chuẩn cho pattern này.
- Dialog dùng chung cho cả Tạo & Sửa
- Map DTO → FormState thủ công (cấm `as unknown as`)
- Pattern `useTableLayout`, `useTableSettings`, `useBulkSelection`, `useExcelExport`
- **Quy tắc hiển thị & format field:** alignment theo loại dữ liệu, `formatCurrency` vs `formatNumber`, `truncate`, độ rộng cột → xem **`tao-ui-giao-dien-new` Section 12**
- **`ALL_COLUMNS` mặc định `pinned: null`** — KHÔNG set `pinned: 'right'` hay `'left'` làm mặc định. Chỉ user chủ động ghim qua `TableSettingsPanel` mới tạo pin icon.
- **`ALL_COLUMNS` — HIỂN THỊ ĐẦY ĐỦ, KHÔNG TỰ Ý BỚT CỘT (BẮT BUỘC):** Khi đã khai báo các cột trong `ALL_COLUMNS`, **TẤT CẢ** các cột đó PHẢI có mặt trong bảng hiển thị. **TUYỆT ĐỐI CẤM** tự ý lược bỏ, ẩn, hoặc không include bất kỳ cột nào đã được chỉ định. Việc ẩn/hiện cột chỉ được thực hiện qua `TableSettingsPanel` bởi người dùng, không phải do developer tự quyết định.
- **Dialog footer action:** tuân thủ quy tắc bên dưới (Section 3.4)
- **`DmTableCell` mặc định `truncate`** — tự động cắt text dài bằng ellipsis. Không cần thêm `truncate` khi dùng `DmTableCell`. Nội dung sẽ không tràn sang cột khác nhờ `tableLayout: fixed` + `overflow: hidden`.
- **Ghost column cần `overflow: visible`** — cột action sticky right phải có `style={{ overflow: 'visible' }}` để button nổi không bị cắt.
- **Resize cột: kéo cạnh phải header để thay đổi độ rộng, lưu vào localStorage.** Dùng `useColumnResize` hook + `getColumnWidth` cho cả 3 bảng. Xem Section 13.
- **BulkActionBar:** Khi có ít nhất 1 dòng được chọn, hiển thị `BulkActionBar` thay cho `DmSearchToolbar`. Import `BulkActionBar` từ `@/shared/components/common`. Xem Section 0.0.3 bên dưới.

---

### 0.0 Layout Ba Phần: Header Cố Định + Body Scroll + Tổng Cộng Cố Định (BẮT BUỘC)

> **Header và hàng Tổng cộng PHẢI luôn hiển thị, không bị trôi khi scroll dọc.**

Bảng được chia thành **3 `<DmTable>` riêng biệt**:
1. **Header** — `<div ref={headerScrollRef} className='shrink-0 overflow-hidden'>`
2. **Body** — `<div ref={tableRef} className='flex-1 min-h-0 overflow-auto scrollbar-hidden'>`
3. **Tổng cộng** — `<div ref={totalScrollRef} className='shrink-0 overflow-hidden'>`

Scroll ngang được đồng bộ qua `handleTableScroll`.

#### 0.0.1 Ref & Scroll Sync

```tsx
import React, { useState, useMemo, useRef, useCallback } from 'react'

// ── Ref cho header & tổng cộng (để đồng bộ scroll ngang với bảng chính) ──
const headerScrollRef = useRef<HTMLDivElement>(null)
const totalScrollRef = useRef<HTMLDivElement>(null)

// ── Wrap onTableScroll để đồng bộ scroll ngang cho header & hàng tổng cộng ──
const handleTableScroll = useCallback(() => {
  onTableScroll()
  const sl = tableRef.current?.scrollLeft ?? 0
  if (headerScrollRef.current) headerScrollRef.current.scrollLeft = sl
  if (totalScrollRef.current) totalScrollRef.current.scrollLeft = sl
}, [onTableScroll])
```

> `tableRef` từ `useTableLayout()`. `onTableScroll` là callback gốc của hook.

#### 0.0.2 Layout JSX

```tsx
<div className='h-full flex flex-col bg-white rounded-xl overflow-hidden'>

  {/* Search toolbar */}
  <DmSearchToolbar ... />

  {/* ── 1. Header — cố định trên ── */}
  <div ref={headerScrollRef} className='shrink-0 overflow-hidden'>
    <DmTable style={{ minWidth: minTableWidth }}>
      <DmTableHeader>
        <DmTableHeaderRow>
          <DmTableHead ... /> {/* checkbox */}
          {colsForRender.map(col => <DmTableHead ... />)}
          <DmTableHead ... /> {/* ghost */}
        </DmTableHeaderRow>
      </DmTableHeader>
    </DmTable>
  </div>

  {/* ── 2. Body — scrollable ── */}
  <div ref={tableRef} className='flex-1 min-h-0 overflow-auto scrollbar-hidden' onScroll={handleTableScroll}>
    <DmTable style={{ minWidth: minTableWidth }}>
      <DmTableBody>
        {/* CHỈ chứa data rows, KHÔNG header, KHÔNG total */}
      </DmTableBody>
    </DmTable>
  </div>

  {/* ── 3. Tổng cộng — cố định dưới ── */}
  {list.items.length > 0 && (
    <div ref={totalScrollRef} className='shrink-0 overflow-hidden'>
      <DmTable style={{ minWidth: minTableWidth }}>
        <DmTableBody>
          <DmTableRow className='bg-[#ECEDEF] border-t-2 border-[#ced1d6] font-semibold'>
            ...
          </DmTableRow>
        </DmTableBody>
      </DmTable>
    </div>
  )}

  {/* Pagination */}
  <DmTablePagination ... />

  {/* Ghost scrollbar */}
  <div ref={ghostRef} ... />
</div>
```

> ⚠️ **Mỗi `<DmTable>` phải có cùng `minWidth: minTableWidth`** để các cột khớp nhau theo chiều ngang.

### 0.0.3 Conditional: BulkActionBar vs DmSearchToolbar

Khi có ít nhất 1 dòng được chọn → hiển thị `BulkActionBar`; ngược lại → hiển thị `DmSearchToolbar`:

```tsx
{/* Search Toolbar HOẶC BulkActionBar (khi có dòng được chọn) */}
{selection.selectedCount > 0 ? (
  <BulkActionBar
    selectedCount={selection.selectedCount}
    onClear={selection.clear}
    onDelete={() => setBulkDeleteOpen(true)}
  />
) : (
  <DmSearchToolbar
    searchPlaceholder='Tìm theo số chứng từ, diễn giải...'
    searchValue={searchText}
    onSearchChange={setSearchText}
    onRefresh={doSearch}
    rightSection={
      <div className='flex items-center gap-2'>
        <TableSettingsPanel ... />
        <ExportButton type='excel' onClick={exportExcel} />
        <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_them' onClick={() => { setSelectedId(null); setDialogMode('create'); setDialogOpen(true) }}>
          <Plus className='h-3.5 w-3.5 mr-1' />Thêm
        </Button>
      </div>
    }
  />
)}
```

> **Import:** `import { BulkActionBar } from '@/shared/components/common'`

---

## ⚠️ NGUYÊN TẮC 0.1: Dialog PHẢI Là Full-Screen — Dùng `tao-dialog-full`

> **Áp dụng cho TẤT CẢ dialog của phiếu thu, phiếu chi, tiền gửi, tiền vay.**
> Không dùng dialog popup giới hạn (`max-w-4xl`, `max-h-[90vh]`).
>
> **Đọc toàn bộ `tao-dialog-full/SKILL.md` để biết chi tiết layout, CSS, component.** Skill này CHỈ bổ sung các quy tắc đặc thù cho dialog nghiệp vụ có ghi sổ.

### 0.1.1 Điểm Khác Biệt So Với `tao-dialog-full` Cơ Bản

| Thành phần | `tao-dialog-full` cơ bản | Phiếu thu/chi (có ghi sổ) |
|-----------|--------------------------|---------------------------|
| Footer Create | `[Hủy] [Lưu] [Lưu & Thêm]` | `[Hủy] [Lưu] [Lưu & Ghi sổ]` |
| Footer View | Không có | `[Sửa] [Ghi sổ]` hoặc `[Bỏ ghi và sửa]` |
| Footer Edit | `[Hủy] [Lưu]` | `[Hủy] [Lưu]` (giống) |
| Hook method | `handleSubmitAndNew` | `handleCreateAndPost` (Lưu & Ghi sổ) |
| `isPosted` field | Không bắt buộc | BẮT BUỘC có |

### 0.1.2 Footer Đặc Thù Cho Phiếu Thu/Chi

```tsx
{isReadOnly ? (
  <>
    {!formData.isPosted && (
      <>
        <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_sua' onClick={handleSwitchToEdit}>
          <Pencil className='h-3.5 w-3.5 mr-1' />Sửa
        </Button>
        <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_ghi_so' disabled={operating} onClick={() => setPostOpen(true)}>
          <BookOpen className='h-3.5 w-3.5 mr-1' />Ghi sổ
        </Button>
      </>
    )}
    {formData.isPosted && (
      <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_bo_ghi_va_sua' disabled={operating} onClick={() => setUnpostOpen(true)}>
        Bỏ ghi và sửa
      </Button>
    )}
  </>
) : mode === 'edit' ? (
  <>
    <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy' disabled={submitting}
      onClick={() => {
        if (dirtyRef.current) { setUnsavedOpen(true); pendingCloseRef.current = () => onOpenChange(false) }
        else onOpenChange(false)
      }}>Hủy</Button>
    <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_luu' disabled={submitting} onClick={handleSubmit}>
      {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu
    </Button>
  </>
) : (
  <>
    <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy' disabled={submitting}
      onClick={() => onOpenChange(false)}>Hủy</Button>
    <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_luu' disabled={submitting} onClick={handleSubmit}>
      {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu
    </Button>
    <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_luu_va_ghi_so' disabled={submitting} onClick={handleCreateAndPost}>
      {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu &amp; Ghi sổ
    </Button>
  </>
)}
```

### 0.1.3 Post/Unpost Handlers

```tsx
// View (unposted) → Edit
const handleSwitchToEdit = () => {
  if (!editingId) return
  setField('isPosted', false)
  initEdit(editingId)
}

// View (posted) → Bỏ ghi sổ → Edit
const handleUnpostAndEdit = async () => {
  if (!editingId) return
  setOperating(true)
  const ok = await handleUnpost(editingId)
  setOperating(false)
  if (ok) {
    setUnpostOpen(false)
    setField('isPosted', false)
    initEdit(editingId)
  }
}
```

### 0.1.4 Confirm Post/Unpost Dialogs

```tsx
<ConfirmDialog open={postOpen} onOpenChange={setPostOpen}
  title='Ghi sổ {TEN_PHIEU}'
  message={`Bạn có chắc chắn muốn ghi sổ {TEN_PHIEU} ${formData.refNo}? Sau khi ghi sổ sẽ không thể chỉnh sửa.`}
  confirmLabel='Ghi sổ'
  onConfirm={async () => {
    if (!editingId) return
    setOperating(true)
    const ok = await handlePost(editingId)
    setOperating(false)
    if (ok) { setPostOpen(false); onOpenChange(false) }
  }} />

<ConfirmDialog open={unpostOpen} onOpenChange={setUnpostOpen}
  title='Bỏ ghi sổ {TEN_PHIEU}'
  message={`Bạn có chắc chắn muốn bỏ ghi sổ {TEN_PHIEU} ${formData.refNo}?`}
  confirmLabel='Bỏ ghi sổ' variant='destructive'
  onConfirm={handleUnpostAndEdit} />
```

### 0.1.5 Confirm Đóng Khi Có Thay Đổi Chưa Lưu (BẮT BUỘC)

> **Nguyên tắc:** Khi mở form **tạo mới**, đóng trực tiếp không cần confirm. Khi mở form **sửa** và có thay đổi thực sự từ user, mới hiển thị popup xác nhận.

| Mode | Có dirty? | Hành vi khi bấm [Hủy] hoặc nút X |
|------|----------|-----------------------------------|
| **Create** | Bất kể | Đóng trực tiếp, **không** confirm |
| **Edit** | `dirtyRef.current === true` | Mở popup "Bạn có thay đổi chưa lưu" |
| **Edit** | `dirtyRef.current === false` | Đóng trực tiếp |
| **View** | — | Đóng trực tiếp |

**Lý do:** Khi tạo mới, form auto-fill các giá trị mặc định (số phiếu, ngày, TK Nợ/Có) từ `initCreate` → `dirtyRef` bị set `true` ngay lập tức dù user chưa làm gì. Nếu hiển thị confirm, user sẽ thấy popup không cần thiết.

#### 0.1.5.1 Code nút X (Header) & nút Hủy (Footer)

```tsx
// ── Nút X trong Header ───────────────────────────────────────────
<Button
  variant='ghost' size='sm'
  className='h-7 w-7 p-0 text-black hover:text-black hover:bg-gray-100'
  onClick={() => {
    // Create / View → đóng luôn, không confirm
    if (mode === 'create' || mode === 'view') {
      onOpenChange(false)
      return
    }
    // Edit → chỉ confirm nếu có thay đổi thực sự
    if (dirtyRef.current) {
      setUnsavedOpen(true)
      pendingCloseRef.current = () => onOpenChange(false)
    } else {
      onOpenChange(false)
    }
  }}
>
  <X className='h-4 w-4' />
</Button>

// ── Nút [Hủy] trong Footer ────────────────────────────────────────
const handleCancel = () => {
  // Create → đóng luôn, không confirm
  if (mode === 'create') {
    onOpenChange(false)
    return
  }
  // Edit → chỉ confirm nếu có thay đổi thực sự
  if (dirtyRef.current) {
    setUnsavedOpen(true)
    pendingCloseRef.current = () => onOpenChange(false)
  } else {
    onOpenChange(false)
  }
}

// Dùng trong footer:
<Button onClick={handleCancel}>Hủy</Button>
```

#### 0.1.5.2 Footer Create — Không check dirtyRef ở nút Hủy

```tsx
{/* Create mode footer */}
<>
  <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy' disabled={submitting}
    onClick={() => onOpenChange(false)}>
    Hủy
  </Button>
  <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_luu' disabled={submitting} onClick={handleSubmit}>
    {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu
  </Button>
  <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_luu_va_ghi_so' disabled={submitting} onClick={handleCreateAndPost}>
    {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu &amp; Ghi sổ
  </Button>
</>
```

#### 0.1.5.3 Footer Edit — Chỉ check dirtyRef ở nút Hủy

```tsx
{/* Edit mode footer */}
<>
  <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy' disabled={submitting}
    onClick={() => {
      if (dirtyRef.current) { setUnsavedOpen(true); pendingCloseRef.current = () => onOpenChange(false) }
      else onOpenChange(false)
    }}>Hủy</Button>
  <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_luu' disabled={submitting} onClick={handleSubmit}>
    {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu
  </Button>
</>
```

#### 0.1.5.4 ConfirmDialog "Thay đổi chưa lưu"

```tsx
<ConfirmDialog
  open={unsavedOpen}
  onOpenChange={setUnsavedOpen}
  title='Thay đổi chưa lưu'
  message='Bạn có thay đổi chưa lưu. Bạn có chắc chắn muốn thoát?'
  confirmLabel='Thoát'
  variant='destructive'
  onConfirm={() => {
    setUnsavedOpen(false)
    dirtyRef.current = false
    // pendingCloseRef đã được set trước khi mở dialog
    if (pendingCloseRef.current) {
      pendingCloseRef.current()
      pendingCloseRef.current = null
    }
  }}
/>
```

---

## 1. Quy Tắc Màu Sắc Dòng Dữ Liệu

### 1.1 Màu theo trạng thái ghi sổ

| Trạng thái | Màu chữ toàn hàng | Class |
|-----------|-------------------|-------|
| **Đã ghi sổ** (`isPosted: true`) | Đen (`text-black`) | `text-black` |
| **Chưa ghi sổ** (`isPosted: false`) | Amber (`text-amber-600`) | `text-amber-600` |

### 1.2 Cột số chứng từ (refNo) — Luôn màu primary

Bất kể trạng thái ghi sổ, cột `refNo` **luôn** có màu xanh dương (primary):

```
refNo: 'font-medium text-blue-700'
```

### 1.3 Hàm `getCellClass` chuẩn

```tsx
/** Trả về class cho cell dựa trên field & trạng thái ghi sổ */
const getCellClass = (field: string, item: XxxListItem): string => {
  // Số chứng từ luôn xanh primary
  if (field === 'refNo') return 'font-medium text-blue-700'
  // Chưa ghi sổ → màu amber toàn bộ các cột còn lại
  if (!item.isPosted) return 'text-amber-600'
  // Đã ghi sổ → dùng class mặc định từ CELL_CLASS, fallback về đen
  return (CELL_CLASS[field] ? `${CELL_CLASS[field]}` : 'text-black')
}
```

### 1.4 Cột trạng thái (isPosted) — Badge

Cột `isPosted` hiển thị dạng badge (pill), không phải text thuần:

```tsx
{col.field === 'isPosted' ? (
  <span className={cn(
    'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
    item.isPosted
      ? 'bg-green-50 text-green-700 border border-green-200'
      : 'bg-amber-50 text-amber-700 border border-amber-200',
  )}>
    {item.isPosted ? 'Đã ghi sổ' : 'Chưa ghi sổ'}
  </span>
) : (
  (CELL_VALUE[col.field] ?? (() => '-'))(item)
)}
```

### 1.5 Cột "Số tiền" (totalAmount) — Canh phải (BẮT BUỘC)

Cả **header** và **value** của cột `totalAmount` đều canh phải (`text-right`):

```tsx
// Trong DmTableHead:
className={cn(
  ...,
  col.field === 'totalAmount' && 'text-right',
)}

// Trong DmTableCell:
className={cn(
  getCellClass(col.field, item),
  ...,
  col.field === 'totalAmount' && 'text-right',
)}
```

> Áp dụng cho TẤT CẢ các cột có tiêu đề "Số tiền" / "Tổng tiền" / "Số dư" — bất kỳ cột nào hiển thị giá trị tiền tệ.

### 1.6 Cột Định Danh (refNo) — Link Mở Xem Chi Tiết (BẮT BUỘC)

> **Cột định danh** (số chứng từ, số đơn hàng, mã...) là cột đầu tiên có nội dung đại diện cho bản ghi. Cột này PHẢI hiển thị dạng link: chữ xanh, hover gạch chân, click mở dialog View.

#### 1.6.1 Quy tắc hiển thị

| Thuộc tính | Giá trị |
|-----------|---------|
| Màu chữ | `text-blue-700` (primary) |
| Font weight | `font-medium` |
| Con trỏ | `cursor-pointer` |
| Hover | `hover:underline` |
| Click | `e.stopPropagation()` → `setSelectedId(item.id); setDialogMode('view'); setDialogOpen(true)` |

#### 1.6.2 `getCellClass` — thêm `cursor-pointer hover:underline`

```tsx
const getCellClass = (field: string, item: XxxListItem): string => {
  // Cột định danh (số chứng từ) luôn xanh + link style
  if (field === 'refNo') return 'font-medium text-blue-700 cursor-pointer hover:underline'
  // Chưa ghi sổ → màu amber
  if (!item.isPosted) return 'text-amber-600'
  // Đã ghi sổ → dùng class mặc định
  return (CELL_CLASS[field] ? `${CELL_CLASS[field]}` : 'text-black')
}
```

#### 1.6.3 Render cell — `<span>` clickable cho cột định danh

Trong `colsForRender.map()`, thêm điều kiện cho cột định danh **trước** các điều kiện khác:

```tsx
{col.field === 'isPosted' ? (
  <span className={cn(...)}>...</span>  // Badge trạng thái
) : col.field === 'refNo' ? (
  <span
    className='cursor-pointer hover:underline'
    onClick={(e: React.MouseEvent) => {
      e.stopPropagation()
      setSelectedId(item.id)
      setDialogMode('view')
      setDialogOpen(true)
    }}
    data-qa={`link_refno_${item.id}`}
  >
    {item.refNo || ''}
  </span>
) : (
  (CELL_VALUE[col.field] ?? (() => ''))(item)
)}
```

#### 1.6.4 Cột định danh cho từng loại chứng từ

| Loại trang | Field định danh | Tên hiển thị |
|-----------|----------------|-------------|
| Phiếu thu | `refNo` | Số phiếu thu |
| Phiếu chi | `refNo` | Số phiếu chi |
| Tiền gửi | `refNo` | Số tiền gửi |
| Tiền vay | `refNo` | Số tiền vay |
| Đơn hàng | `orderNo` | Số đơn hàng |
| Danh mục (CRUD) | `code` | Mã |

> **Nguyên tắc chung:** Cột đầu tiên chứa mã/số đại diện cho bản ghi (không phải ngày tháng, không phải tên/diễn giải) → render dạng link xanh, click mở View.

---

## 2. Quy Tắc Hàng Tổng Cộng Cuối Bảng (BẮT BUỘC)

> **Mọi bảng phiếu thu/chi/tiền gửi PHẢI có hàng tổng cộng ở cuối bảng.**

### 2.1 Cấu trúc hàng tổng cộng

| Vị trí | Nội dung |
|--------|----------|
| Cột checkbox | Để trống |
| Cột đầu tiên (idx=0) | Chữ **"Tổng cộng"** in đậm |
| Các cột text/không phải số | Để trống |
| Cột `totalAmount` | `formatNumber(totalSum)` — canh phải, in đậm |
| Các cột số khác (nếu có) | Tính tổng tương ứng |
| Cột ghost action | Để trống |

### 2.2 Code mẫu — Hàng tổng cộng tách riêng, luôn hiển thị

> **Hàng tổng cộng PHẢI nằm NGOÀI vùng scroll**, trong một `<DmTable>` riêng, để luôn hiển thị khi bảng có scrollbar dọc. Không đặt trong `DmTableBody` của bảng chính.

#### 2.2.1 Ref & scroll sync

```tsx
// ── Ref cho hàng tổng cộng (để đồng bộ scroll ngang với bảng chính) ──
const totalScrollRef = useRef<HTMLDivElement>(null)

// ── Wrap onTableScroll để đồng bộ scroll ngang cho hàng tổng cộng ──
const handleTableScroll = useCallback(() => {
  onTableScroll()
  if (totalScrollRef.current && tableRef.current) {
    totalScrollRef.current.scrollLeft = tableRef.current.scrollLeft
  }
}, [onTableScroll])
```

> Dùng `handleTableScroll` thay cho `onTableScroll` trong `onScroll` của div bảng chính.

#### 2.2.2 Tính tổng

```tsx
const totalSum = useMemo(() => list.items.reduce((s, i) => s + i.totalAmount, 0), [list.items])
```

#### 2.2.3 Layout — hàng tổng cộng nằm NGOÀI vùng scroll

```tsx
{/* Vùng bảng chính (scrollable) */}
<div ref={tableRef} className='flex-1 min-h-0 overflow-auto scrollbar-hidden' onScroll={handleTableScroll}>
  <DmTable style={{ minWidth: minTableWidth }}>
    <DmTableHeader>...</DmTableHeader>
    <DmTableBody>
      {/* CHỈ chứa data rows, KHÔNG có total row */}
    </DmTableBody>
  </DmTable>
</div>

{/* ── Hàng tổng cộng — luôn hiển thị, nằm NGOÀI vùng scroll ── */}
{list.items.length > 0 && (
  <div ref={totalScrollRef} className='shrink-0 overflow-hidden'>
    <DmTable style={{ minWidth: minTableWidth }}>
      <DmTableBody>
        <DmTableRow className='bg-[#ECEDEF] border-t-2 border-[#ced1d6] font-semibold'>
          {/* Checkbox rỗng */}
          <DmTableCell
            className='text-center sticky left-0 z-20 bg-[#ECEDEF]'
            style={{ width: 40, minWidth: 40 }}
          />
          {colsForRender.map((col, idx) => (
            <DmTableCell
              key={col.id}
              style={{
                width: col.width,
                minWidth: col.width,
                ...(col.stickyLeft !== undefined ? { left: col.stickyLeft } : {}),
                ...(col.stickyRight !== undefined ? { right: col.stickyRight } : {}),
              }}
              className={cn(
                'text-black',
                col.stickyLeft !== undefined && 'sticky z-20 bg-[#ECEDEF]',
                col.stickyRight !== undefined && 'sticky z-20 bg-[#ECEDEF]',
                col.pinned === 'left' && 'shadow-[2px_0_4px_-2px_rgba(0,0,0,0.06)]',
                col.pinned === 'right' && 'shadow-[-2px_0_4px_-2px_rgba(0,0,0,0.06)]',
                col.field === 'totalAmount' && 'text-right',
              )}
            >
              {idx === 0 ? 'Tổng cộng' : col.field === 'totalAmount' ? formatNumber(totalSum) : ''}
            </DmTableCell>
          ))}
          {/* Ghost rỗng */}
          <DmTableCell className='sticky right-0 z-20 bg-[#ECEDEF]'
            style={{ width: 0, minWidth: 0, padding: 0, border: 'none' }} />
        </DmTableRow>
      </DmTableBody>
    </DmTable>
  </div>
)}
```

### 2.3 Quy tắc hiển thị

- **Vị trí:** Nằm NGOÀI vùng scroll của bảng chính, trong một `<DmTable>` riêng. Luôn hiển thị, không bị cuốn theo scroll dọc.
- **`totalScrollRef`:** Ref trên wrapper `div` của hàng tổng cộng. Scroll ngang được đồng bộ với bảng chính qua `handleTableScroll`.
- **Wrapper class:** `shrink-0 overflow-hidden` — không co giãn, ẩn scrollbar dư thừa.
- **Background:** `bg-[#ECEDEF]` — cùng màu với header
- **Border-top:** `border-t-2 border-[#ced1d6]` — đường kẻ đậm phân tách với dữ liệu
- **Font:** `font-semibold` — in đậm toàn hàng
- **Chữ "Tổng cộng":** nằm ở cột dữ liệu đầu tiên (`idx === 0`), canh trái
- **Số tổng:** format qua `formatNumber()`, canh phải
- **Chỉ hiển thị khi có dữ liệu:** `list.items.length > 0`
- **Sticky columns:** tổng cộng row cũng phải sticky cùng vị trí với data rows

---

### 2.1 Ma trận action theo trạng thái

> **Quy tắc quan trọng:** Khi đã ghi sổ → KHÔNG thể sửa trực tiếp. Phải "Bỏ ghi và sửa" (gọi API unpost → mở dialog edit).

| Action | Chưa ghi sổ | Đã ghi sổ | Vị trí |
|--------|:----------:|:---------:|--------|
| **Xem** (View) | ✅ | ✅ | Button riêng |
| **Xóa** (Delete) | ✅ | ❌ | Button riêng |
| **Bỏ ghi và sửa** (Unpost & Edit) | ❌ | ✅ | Button riêng |
| **Ghi sổ** (Post) | ✅ (trong dropdown) | ❌ | Dropdown "Chức năng khác" |
| **Nhân bản** (Clone) | ✅ (trong dropdown) | ✅ (trong dropdown) | Dropdown "Chức năng khác" |

### 2.2 Pattern Ghost Column — Button + DropdownMenu (Pattern B)

> Dùng Pattern B từ `update-action` với điều kiện `isPosted`.
>
> **Nguyên tắc:** Đã ghi sổ → KHÔNG có nút Sửa. Thay vào đó là nút "Bỏ ghi và sửa" (gọi unpost API → mở edit dialog).

```tsx
{/* Cột neo sticky phải — width=0, action hiện khi hover row */}
<DmTableCell className='sticky right-0 z-20 bg-transparent'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-16 pr-2'>

    {/* [1] Xem — luôn có */}
    <Button variant='ghost' size='sm'
      className='border rounded-lg bg-white'
      title='Xem' data-qa={`btn_xem_${item.id}`}
      onClick={(e) => { e.stopPropagation(); setSelectedId(item.id); setDialogMode('view'); setDialogOpen(true) }}>
      <Eye className='h-4 w-4' />
    </Button>

    {/* [2] Xóa — CHỈ khi chưa ghi sổ */}
    {!item.isPosted && (
      <Button variant='ghost' size='sm'
        className='icon-danger border rounded-lg bg-white'
        title='Xóa' data-qa={`btn_xoa_${item.id}`}
        onClick={(e) => { e.stopPropagation(); setDeleteItem(item); setDeleteOpen(true) }}>
        <Trash2 className='h-4 w-4' />
      </Button>
    )}

    {/* [3] Bỏ ghi và sửa — CHỈ khi đã ghi sổ (gọi thẳng API unpost → mở edit dialog, KHÔNG popup xác nhận) */}
    {item.isPosted && (
      <Button variant='ghost' size='sm'
        className='icon-warning border rounded-lg bg-white'
        title='Bỏ ghi và sửa' data-qa={`btn_bo_ghi_va_sua_${item.id}`}
        onClick={(e) => { e.stopPropagation(); handleUnpostAndEdit(item) }}>
        <Pencil className='h-4 w-4' />
      </Button>
    )}

    {/* [4] DropdownMenu — Chức năng khác */}
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' size='sm'
          className='border rounded-lg bg-white'
          title='Chức năng khác' data-qa={`btn_khac_${item.id}`}>
          <MoreHorizontal className='h-4 w-4' />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' className='w-44'>
        {!item.isPosted ? (
          <>
            {/* Chưa ghi sổ: Ghi sổ + Nhân bản */}
            <DropdownMenuItem onSelect={() => { setPostItem(item); setPostOpen(true) }}
              data-qa={`btn_ghi_so_${item.id}`}>
              <BookOpen className='h-4 w-4' /> Ghi sổ
            </DropdownMenuItem>
            <DropdownMenuItem onSelect={() => { setSelectedId(null); setDialogMode('create'); setDialogOpen(true) }}
              data-qa={`btn_nhan_ban_${item.id}`}>
              <Copy className='h-4 w-4' /> Nhân bản
            </DropdownMenuItem>
          </>
        ) : (
          <>
            {/* Đã ghi sổ: Chỉ còn Nhân bản (KHÔNG có Bỏ ghi sổ riêng — đã có nút "Bỏ ghi và sửa" bên ngoài) */}
            <DropdownMenuItem onSelect={() => { setSelectedId(null); setDialogMode('create'); setDialogOpen(true) }}
              data-qa={`btn_nhan_ban_${item.id}`}>
              <Copy className='h-4 w-4' /> Nhân bản
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>

  </div>
</DmTableCell>
```

### 2.3 Imports cần thiết cho Pattern

```tsx
import { Eye, Pencil, Trash2, MoreHorizontal, Copy, BookOpen } from 'lucide-react'
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
} from '@/shared/components/ui/dropdown-menu'
```

> ⚠️ **KHÔNG import `DmRowActions` hoặc `useDmRowActions`** — Pattern này dùng Button thủ công hoàn toàn.

---

## 3. State & Confirm Handlers

### 3.1 State cần có

```tsx
const [dialogOpen, setDialogOpen] = useState(false)
const [dialogMode, setDialogMode] = useState<'view' | 'edit' | 'create'>('create')
const [selectedId, setSelectedId] = useState<string | null>(null)

const [deleteItem, setDeleteItem] = useState<XxxListItem | null>(null)
const [deleteOpen, setDeleteOpen] = useState(false)
const [postItem, setPostItem] = useState<XxxListItem | null>(null)
const [postOpen, setPostOpen] = useState(false)
const [unpostItem, setUnpostItem] = useState<XxxListItem | null>(null)
const [unpostOpen, setUnpostOpen] = useState(false)
const [operating, setOperating] = useState(false)
const [bulkDeleteOpen, setBulkDeleteOpen] = useState(false)
const [settingsOpen, setSettingsOpen] = useState(false)
```

### 3.2 Confirm handlers

```tsx
const formHook = useXxxDlgForm({
  onSuccess: list.refetch,
  onClose: () => setDialogOpen(false),
})

const handleDeleteConfirm = async () => {
  if (!deleteItem) return
  setOperating(true)
  try {
    await formHook.handleDelete(deleteItem.id)
    setDeleteOpen(false)
    list.refetch()
  } finally { setOperating(false) }
}

const handlePostConfirm = async () => {
  if (!postItem) return
  setOperating(true)
  try {
    await formHook.handlePost(postItem.id)
    setPostOpen(false)
    list.refetch()
  } finally { setOperating(false) }
}

const handleUnpostConfirm = async () => {
  if (!unpostItem) return
  setOperating(true)
  try {
    await formHook.handleUnpost(unpostItem.id)
    setUnpostOpen(false)
    list.refetch()
  } finally { setOperating(false) }
}

/** Gọi thẳng API bỏ ghi sổ rồi mở form sửa (không popup xác nhận) */
const handleUnpostAndEdit = async (item: XxxListItem) => {
  setOperating(true)
  try {
    await formHook.handleUnpost(item.id)
    // Sau khi bỏ ghi sổ thành công → mở dialog edit luôn
    setDialogMode('edit')
    setSelectedId(item.id)
    setDialogOpen(true)
  } finally { setOperating(false) }
}
```

### 3.3 Các ConfirmDialog cần có

```tsx
{/* Confirm xóa */}
<ConfirmDialog
  open={deleteOpen}
  onOpenChange={setDeleteOpen}
  title='Xóa phiếu thu'
  message={`Bạn có chắc chắn muốn xóa phiếu thu ${deleteItem?.refNo ?? ''}? Thao tác này không thể hoàn tác.`}
  onConfirm={handleDeleteConfirm}
  variant='destructive'
  loading={operating}
/>

{/* Confirm ghi sổ */}
<ConfirmDialog
  open={postOpen}
  onOpenChange={setPostOpen}
  title='Ghi sổ phiếu thu'
  message={`Xác nhận ghi sổ phiếu thu ${postItem?.refNo ?? ''}?`}
  onConfirm={handlePostConfirm}
  loading={operating}
/>

{/* Confirm bỏ ghi sổ (nếu page có nút bỏ ghi sổ riêng trong dropdown) */}
<ConfirmDialog
  open={unpostOpen}
  onOpenChange={setUnpostOpen}
  title='Bỏ ghi sổ phiếu thu'
  message={`Xác nhận bỏ ghi sổ phiếu thu ${unpostItem?.refNo ?? ''}? Bút toán đã sinh sẽ bị gỡ.`}
  onConfirm={handleUnpostConfirm}
  variant='destructive'
  loading={operating}
/>

{/* Confirm xóa hàng loạt */}
<ConfirmDialog
  open={bulkDeleteOpen}
  onOpenChange={setBulkDeleteOpen}
  title='Xóa hàng loạt'
  message={`Bạn có chắc chắn muốn xóa ${selection.selectedCount} phiếu thu đã chọn?`}
  onConfirm={handleBulkDeleteConfirm}
  variant='destructive'
  loading={operating}
/>
```

---

### 3.4 Dialog Footer Actions (BẮT BUỘC)

> Action trong footer dialog PHỤ THUỘC vào `mode` và `isPosted`.
>
> ⚠️ **QUY TẮC QUAN TRỌNG:** `handleSubmit` (nút "Lưu") **CHỈ gọi API tạo/cập nhật, KHÔNG gọi API ghi sổ**. Chỉ `handleCreateAndPost` (nút "Lưu & Ghi sổ") mới gọi đồng thời cả tạo + ghi sổ. **TUYỆT ĐỐI CẤM** auto-post trong `handleSubmit` hoặc `handleSubmitAndNew`.

| Mode | Điều kiện | Buttons |
|------|----------|---------|
| **View** | `!isPosted` (chưa ghi sổ) | `[Sửa]` `[Ghi sổ]` |
| **View** | `isPosted` (đã ghi sổ) | `[Bỏ ghi và sửa]` |
| **Create** | — | `[Hủy]` `[Lưu]` `[Lưu & Ghi sổ]` |
| **Edit** | — | `[Hủy]` `[Lưu]` |

```tsx
{isReadOnly ? (
  <>
    {!formData.isPosted && (
      <>
        <Button onClick={handleSwitchToEdit}><Pencil /> Sửa</Button>
        <Button onClick={() => setPostOpen(true)}><BookOpen /> Ghi sổ</Button>
      </>
    )}
    {formData.isPosted && (
      <Button
        className='btn-primary'
        disabled={operating}
        onClick={() => setUnpostOpen(true)}
      >
        {operating && <Loader2 />} Bỏ ghi và sửa
      </Button>
    )}
  </>
) : mode === 'edit' ? (
  <>
    <Button onClick={handleCancel}>Hủy</Button>
    <Button onClick={handleSubmit}>Lưu</Button>
  </>
) : (
  <>
    <Button onClick={handleCancel}>Hủy</Button>
    <Button onClick={handleSubmit}>Lưu</Button>
    <Button onClick={handleCreateAndPost}>Lưu & Ghi sổ</Button>
  </>
)}
```

**Giải thích:**
- **View unposted:** `[Sửa]` để chuyển sang edit mode (không cần bỏ ghi vì chưa ghi sổ). `[Ghi sổ]` để post rồi đóng dialog.
- **View posted:** `[Bỏ ghi và sửa]` — gọi `handleUnpost()` → nếu OK → `initEdit()` để chuyển sang edit mode. Lý do: bản ghi đã ghi sổ không thể update trực tiếp, phải bỏ ghi trước.
- **Create `[Lưu]`:** Gọi `handleSubmit` → **CHỈ gọi API create, KHÔNG gọi API post**. Bản ghi được tạo với trạng thái chưa ghi sổ.
- **Create `[Lưu & Ghi sổ]`:** Gọi `handleCreateAndPost` → create() → post() (tạo mới rồi ghi sổ ngay).
- **Edit `[Lưu]`:** Gọi `handleSubmit` → **CHỈ gọi API update, KHÔNG gọi API post**.
- **Edit `[Hủy]`:** Đóng dialog (có xác nhận nếu unsaved).

> ⚠️ **TUYỆT ĐỐI CẤM:** `handleSubmit` (nút "Lưu") không được tự động gọi `post()` sau khi create/update. Nếu user muốn ghi sổ, họ phải bấm nút "Lưu & Ghi sổ" (create) hoặc "Ghi sổ" (view).

**Hook bắt buộc phải có:**
```tsx
const { handleSubmit, handleCreateAndPost, handlePost, handleUnpost, initEdit } = useXxxDlgForm(...)
```

Trong đó `handleCreateAndPost` = `create()` → `post()` (gọi liên tiếp, chỉ thành công khi cả 2 OK).

---

### 3.5 TableSearchCombobox Trong Bảng Hạch Toán

> **KHÔNG dùng `compact` prop** — để input height tự nhiên `h-8 rounded-[8px]` giống các input khác.

Tất cả `TableSearchCombobox` nằm trong bảng hạch toán (`EditableDataTable`) của dialog **KHÔNG** có `compact` prop:

```tsx
// ✅ ĐÚNG — không compact, input height tự nhiên
<TableSearchCombobox
  value={String(value ?? '')}
  initialLabel={String(value ?? '')}
  displayField='accountNumber'
  onChange={(id) => updateLine(idx, { debitAccountId: id } as Partial<PTAccountingLineFormState>)}
  loadOptions={loadTaiKhoanTable}
  columns={taiKhoanColumns}
  dataQa={`sel_tk_no_${idx}`}
  disabled={isReadOnly}
/>

// ❌ SAI — compact làm input quá thấp, khó thao tác
<TableSearchCombobox compact ... />
```

**Áp dụng cho các cột sau trong bảng hạch toán:**
- **TK Nợ** (`debitAccountId`)
- **TK Có** (`creditAccountId`)
- **Đối tượng** (`accountObjectCode`)

### 3.5.1 Input Trong Bảng Data — Bắt Buộc Có `px-2` (BẮT BUỘC)

> **Tất cả `<Input>` nằm trong `EditableDataTable` PHẢI có padding ngang (`px-2`).**

```tsx
// ❌ SAI — p-0 làm text dính sát viền, khó đọc
<Input
  type='text' inputMode='numeric'
  value={String(value ?? '0')}
  onChange={e => updateLine(idx, { quantity: e.target.value } as any)}
  readOnly={isReadOnly}
  className='h-[26px] p-0 text-[13px] text-right rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0'
/>

// ✅ ĐÚNG — px-2 tạo khoảng cách giữa text và viền
<Input
  type='text' inputMode='numeric'
  value={String(value ?? '0')}
  onChange={e => updateLine(idx, { quantity: e.target.value } as any)}
  readOnly={isReadOnly}
  className='h-[26px] px-2 text-[13px] text-right rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0'
/>
```

**Áp dụng cho TẤT CẢ các `<Input>` trong `EditableDataTable`:**
- **Số lượng** — `text-right`
- **Đơn giá** — `text-right`
- **Thành tiền** (nếu là input) — `text-right`
- **Tỉ lệ CK (%)** — `text-right`
- **Tiền chiết khấu** — `text-right`
- **Tên hàng** / **Diễn giải** — text bình thường (không `text-right`)
- **Lệnh SX** — text bình thường
- **Ghi chú** — text bình thường

### 3.5.2 Bảng Data Không Bị Co Cột Khi Thu Nhỏ (BẮT BUỘC)

> **`EditableDataTable` PHẢI dùng `table-fixed` + `style={{ width }}` trên `<td>` để cột giữ nguyên kích thước, không bị co khi container thu nhỏ.**

**Đã fix trong component dùng chung `EditableDataTable.tsx`:**
```tsx
// ✅ ĐÚNG — table-fixed giữ nguyên width cột, scroll ngang khi container hẹp
<table className='w-full table-fixed text-[13px]'>

// <td> khớp width với <th>
<td style={col.width ? { width: col.width } : undefined}>
```

**Kết quả:**
- Các cột giữ nguyên `width` đã khai báo trong `EditableColumnDef`
- `TableSearchCombobox` không bị shrink
- Khi container thu nhỏ → scroll ngang (`overflow-x-auto` có sẵn)

> **Quy tắc:** `p-0` → `px-2`. Giữ nguyên các class khác (`h-[26px]`, `text-[13px]`, `rounded-lg`, `border-[#B7BCC3]`, ...).

---

### 3.6 Payload POST/PUT — Dùng ID Cho Tài Khoản Nợ/Có (BẮT BUỘC)

> **KHÔNG truyền `debitAccount`/`creditAccount` (số tài khoản) lên API.**  
> Dùng `debitAccountId`/`creditAccountId` (UUID của tài khoản).

**API expectation:**
- **POST/PUT payload:** `debitAccountId`, `creditAccountId` (ID, không phải số)
- **GET response:** `debitAccountId`, `debitAccountNumber`, `debitAccountName`, `creditAccountId`, `creditAccountNumber`, `creditAccountName`

**TableSearchCombobox (TK Nợ / TK Có):** `loadOptions` trả về `value: tk.id`, `cells.accountNumber = tk.accountNumber`. Combobox dùng `value={row.debitAccountId}`, `initialLabel={row.debitAccountNumber}`, `displayField='accountNumber'`.

**Payload gửi lên:** `debitAccountId: line.debitAccountId || null`, `creditAccountId: line.creditAccountId || null`.

**GET → FormState mapping:** `debitAccountNumber: line.debitAccountNumber ?? line.debitAccount ?? ''` (fallback `debitAccount` nếu BE cũ chưa có `debitAccountNumber`).

#### 3.6.0 Kiểm Tra Interface — `debitAccountId` & `creditAccountId` Bắt Buộc Có (BẮT BUỘC)

> **Trước khi tạo payload, PHẢI kiểm tra interface request DTO đã có `debitAccountId` và `creditAccountId` chưa.**

```
B1: Kiểm tra interface request DTO (CreateXxxRequest / UpdateXxxRequest)
B2: Có field debitAccountId và creditAccountId?
  ├── CÓ   → Tiếp tục, gửi payload với debitAccountId / creditAccountId
  └── KHÔNG → DỪNG LẠI, báo user: "Interface {TenDTO} chưa có debitAccountId/creditAccountId.
              Vui lòng yêu cầu BE bổ sung các field này vào request DTO."
```

**Format báo cáo khi interface thiếu:**

| # | Field | API Endpoint | Method | Vị trí | DTO hiện tại | Hành động |
|---|-------|-------------|--------|--------|-------------|----------|
| 1 | `debitAccountId` | `POST/PUT /api/accounting/v1/...` | Request | `CreateXxxRequest` KHÔNG có `debitAccountId` | BE thêm `debitAccountId` (UUID) vào request DTO |
| 2 | `creditAccountId` | `POST/PUT /api/accounting/v1/...` | Request | `CreateXxxRequest` KHÔNG có `creditAccountId` | BE thêm `creditAccountId` (UUID) vào request DTO |

> ⚠️ **TUYỆT ĐỐI KHÔNG** tự ý thêm `debitAccountId`/`creditAccountId` vào payload khi interface chưa có — API sẽ từ chối hoặc bỏ qua field. Phải yêu cầu BE bổ sung vào DTO trước.

---

### 3.6.1 Default TK Nợ / TK Có — Chỉ Hiển Thị Khi Có ID (BẮT BUỘC)

> **Nguyên tắc:** Nếu field TK Nợ / TK Có tồn tại nhưng **KHÔNG được chỉ định default** → **KHÔNG có giá trị mặc định**, để trống hoàn toàn. Chỉ khi **có chỉ định default cụ thể** (từ `getDefault()` hoặc cấu hình) thì mới resolve ID và hiển thị. **TUYỆT ĐỐI KHÔNG** hiển thị số tài khoản khi chưa có ID — gây hiểu lầm cho user là đã chọn.

> **Quy tắc resolve default:** Khi có default, dùng API `getById` (dùng `TKApiService.getById(accountId)`) để lấy thông tin tài khoản, **KHÔNG** dùng pattern list+filter 9999 records. Nếu chưa có `getById` endpoint, dùng `list` với keyword chính xác để tìm kiếm.

#### 3.6.1.1 `XXX_INITIAL_LINE` — KHÔNG hardcode default số tài khoản

```tsx
// ❌ SAI — hiển thị số '1111' nhưng debitAccountId rỗng → user tưởng đã chọn
export const PT_INITIAL_LINE: PTAccountingLineFormState = {
  debitAccountId: '',
  debitAccountNumber: '1111',   // ← SAI: hiển thị số ảo
  creditAccountId: '',
  creditAccountNumber: '1388',  // ← SAI: hiển thị số ảo
}

// ✅ ĐÚNG — để trống, chỉ fill khi resolve được ID
export const PT_INITIAL_LINE: PTAccountingLineFormState = {
  debitAccountId: '',
  debitAccountNumber: '',   // ← để trống
  creditAccountId: '',
  creditAccountNumber: '',  // ← để trống
}
```

#### 3.6.1.2 Hook `resolveAccountNumber` — Resolve số TK → ID (dùng getById hoặc list+filter)

Trong hook `useXxxDlgForm`, thêm hàm `resolveAccountNumber` để resolve số tài khoản từ default config:

```tsx
/** Resolve số tài khoản → ID.
 *  Ưu tiên dùng getById nếu BE hỗ trợ.
 *  Nếu chỉ có accountNumber (string), dùng list + filter FE (tối đa 200 records). */
const resolveAccountNumber = useCallback(async (accountNumber: string): Promise<{ id: string; number: string } | null> => {
  if (!accountNumber) return null
  try {
    // Cách 1 (ƯU TIÊN): Nếu có accountId từ default → dùng getById
    // const tk = await TKApiService.getById(accountId)

    // Cách 2: Nếu chỉ có accountNumber → list + filter (pageSize vừa đủ, KHÔNG 9999)
    const tkRes = await TKApiService.list({ pageIndex: 1, pageSize: 100, keyword: accountNumber })
    if (tkRes.success && tkRes.data?.items) {
      const found = tkRes.data.items.find(tk => tk.accountNumber === accountNumber)
      if (found) return { id: found.id, number: found.accountNumber }
    }
  } catch { /* ignore */ }
  return null
}, [])
```

#### 3.6.1.3 `initCreate` — Chỉ set accountNumber khi có ID

```tsx
const initCreate = useCallback(async () => {
  // ...
  try {
    const r = await XxxApiService.getDefault()
    if (r.success && r.data) {
      const cashAccountNumber = fields.find(f => f.columnName === 'cashAccountNumber')?.defaultValue
      // ↑ KHÔNG fallback '1111' — nếu BE không trả default thì để trống

      // Resolve default TK → chỉ hiển thị number khi có ID
      let debitAccountId = ''
      let debitAccountNumber = ''
      if (cashAccountNumber) {
        const resolved = await resolveAccountNumber(cashAccountNumber)
        if (resolved) {
          debitAccountId = resolved.id
          debitAccountNumber = resolved.number  // ← chỉ set khi có ID
        }
      }

      const defaultLine: XxxLineFormState = {
        ...XXX_INITIAL_LINE,
        debitAccountId,
        debitAccountNumber,  // ← rỗng nếu không resolve được
      }
      // ...
    }
  } catch {
    // Không có default → để trống hoàn toàn
    setFormData({ ...XXX_INITIAL_FORM, accountingDetails: [{ ...XXX_INITIAL_LINE }] })
  }
}, [resolveAccountNumber])
```

#### 3.6.1.4 Dialog — KHÔNG set accountNumber/accountObjectId trong onChange Đối tượng

```tsx
// ❌ SAI — sync accountObjectId từ parent xuống line (2 field độc lập)
onChange={(id, rowData) => {
  updateLine(0, {
    debitAccountNumber: formData.cashAccountNumber || '1111',  // ← SAI
    creditAccountNumber: '1388',                               // ← SAI
    accountObjectId: id,                                       // ← SAI
  })
}}

// ✅ ĐÚNG — chỉ sync description & accountObjectName, không đụng TK & accountObjectId
onChange={(id, rowData) => {
  updateLine(0, {
    description: `Thu tiền của ${rowData.name || ''}`,
    accountObjectName: rowData.name || '',
    // ← KHÔNG set debitAccountNumber / creditAccountNumber / accountObjectId
  })
}}
```

#### 3.6.1.5 Flow Tổng Quan — Default TK Nợ / TK Có

```
Có field debitAccountId / creditAccountId trong form?
  ├── KHÔNG → KHÔNG có default, để trống hoàn toàn
  └── CÓ
      ↓
  Có được chỉ định default (getDefault() hoặc config)?
      ├── KHÔNG → KHÔNG có giá trị mặc định, TK Nợ/Có rỗng (cả ID & number)
      └── CÓ
          ↓
      resolveAccountNumber(defaultAccountNumber)
          ├── KHÔNG tìm thấy → TK Nợ/Có rỗng (KHÔNG hiển thị số ảo)
          └── TÌM THẤY     → set debitAccountId + debitAccountNumber
                              TableSearchCombobox hiển thị đúng số TK

Payload gửi lên BE:
  → CHỈ gửi debitAccountId / creditAccountId (UUID)
  → KHÔNG gửi debitAccountNumber / creditAccountNumber
  → Nếu interface request DTO chưa có debitAccountId/creditAccountId
    → DỪNG, báo user yêu cầu BE bổ sung
```

> ⚠️ **QUY TẮC QUAN TRỌNG:** 
> - **Không có chỉ định default** → form trống, không cố gắng tự suy đoán STK mặc định
> - **Có chỉ định default** → resolve qua API, chỉ hiển thị khi có ID
> - **Payload** → chỉ gửi `debitAccountId`, `creditAccountId`
> - **Interface thiếu** → báo user, không tự ý thêm field vào payload

---

## 4. Quy Tắc Header — Biểu Tượng Ghim

### 4.1 Chỉ hiển thị ghim khi user đã chọn ghim trong Table Settings

`DmTableHead` component đã hỗ trợ prop `pinned`. **CHỈ** truyền `pinned=true` khi cột có `col.pinned === 'left' || col.pinned === 'right'`:

```tsx
{colsForRender.map(col => (
  <DmTableHead
    key={col.id}
    pinned={col.pinned === 'left' || col.pinned === 'right'}
    // ... các style khác
  >
    {col.displayName ?? col.title}
  </DmTableHead>
))}
```

> ⚠️ **KHÔNG** truyền `pinned` dựa trên `col.stickyLeft`/`col.stickyRight` — đó là vị trí sticky do layout tính toán, không phải do user chủ động ghim.

**Giải thích:**
- `col.pinned` đến từ `useTableSettings` → phản ánh lựa chọn của user trong `TableSettingsPanel`
- `col.stickyLeft`/`col.stickyRight` đến từ `useTableLayout` → vị trí sticky được tính toán tự động
- Pin icon (`<Pin>`) chỉ hiển thị khi user CHỦ ĐỘNG ghim cột, không phải khi cột vô tình ở vị trí sticky

---

## 5. PAGE_FEATURES Chuẩn

```tsx
export const PAGE_FEATURES = [
  { label: 'Làm mới', code: 'btn-refresh' },
  { label: 'Thêm mới', code: 'btn-create' },
  { label: 'Ghi sổ', code: 'btn-post' },
  { label: 'Bỏ ghi sổ', code: 'btn-unpost' },
  { label: 'Xem chi tiết', code: 'row-view' },
  { label: 'Chỉnh sửa', code: 'row-edit' },
  { label: 'Nhân bản', code: 'row-clone' },
  { label: 'Xóa', code: 'row-delete' },
  { label: 'Thiết lập bảng', code: 'btn-table-settings' },
]
```

---

## 6. Quy Tắc Đặt Tên File

| Thành phần | Pattern | Ví dụ (Phiếu thu) |
|-----------|---------|-------------------|
| Page | `{TenNghiepVu}Page.tsx` | `PhieuThuPage.tsx` |
| Dialog | `{VietTat}Dialog.tsx` | `PTDialog.tsx` |
| Hook page list | `use{VietTat}.page.list.ts` | `usePT.page.list.ts` |
| Hook dialog form | `use{VietTat}.dlg.form.ts` | `usePT.dlg.form.ts` |
| Types API | `{VietTat}.types.api.ts` | `PT.types.api.ts` |
| Types UI | `{VietTat}.types.ui.ts` | `PT.types.ui.ts` |
| Service | `{VietTat}ApiService.ts` | `PTApiService.ts` |
| ALL_COLUMNS constant | `{VIET_TAT}_ALL_COLUMNS` | `PT_ALL_COLUMNS` |
| tableId | kebab-case | `'phieu-thu'` |
| PAGE_ID | kebab-case | `'phieu-thu'` |

---

## 7. Checklist Sau Khi Code

- [ ] **🚫 TUYỆT ĐỐI KHÔNG có `'-'` trong CELL_VALUE** — tất cả dùng `|| ''` hoặc `? ... : ''`
- [ ] **Fallback render không dùng `() => '-'`** — dùng `() => ''`
- [ ] Action đúng theo ma trận: View luôn có, Xóa chỉ khi chưa ghi sổ, **Bỏ ghi và sửa** (button riêng) chỉ khi đã ghi sổ
- [ ] Dropdown "Chức năng khác": Ghi sổ + Nhân bản (chưa ghi sổ), Nhân bản (đã ghi sổ — KHÔNG có Bỏ ghi sổ vì đã có nút "Bỏ ghi và sửa" bên ngoài)
- [ ] `DmTableHead` chỉ có `pinned` prop khi `col.pinned === 'left' || col.pinned === 'right'`
- [ ] Có đủ **5** `ConfirmDialog`: **thay đổi chưa lưu** (chỉ cho Edit), xóa, ghi sổ, bỏ ghi sổ, xóa hàng loạt
- [ ] **Bỏ ghi và sửa (page):** gọi thẳng API `formHook.handleUnpost(item.id)` → mở dialog edit, **KHÔNG popup xác nhận**, icon `Pencil`, `data-qa='btn_bo_ghi_va_sua_'`
- [ ] `formHook` có `handleDelete`, `handlePost`, `handleUnpost`
- [ ] `PAGE_FEATURES` có đủ `btn-post`, `btn-unpost`, `row-view`, `row-edit`, `row-clone`, `row-delete`
- [ ] `data-qa` đúng format: `btn_xem_`, `btn_xoa_`, `btn_ghi_so_`, `btn_bo_ghi_va_sua_`, `btn_nhan_ban_`, `btn_khac_`
- [ ] **ALL_COLUMNS hiển thị đầy đủ:** TẤT CẢ cột khai báo trong `ALL_COLUMNS` đều có mặt trong bảng, KHÔNG tự ý bỏ bớt cột nào

---

## 8. Quy Tắc FK — Select Chỉ Gửi ID, BE Resolve & Trả Display Fields

> **Nguyên tắc:** TableSearchCombobox select đối tượng → CHỈ gửi FK ID lên BE, KHÔNG gửi code/name/display. BE tự resolve FK và trả về đầy đủ display fields trong response.

### 8.1 Payload POST/PUT — Chỉ Gửi ID

```typescript
// ✅ ĐÚNG: Chỉ gửi ID
{ "fromBankAccountID": "uuid-abc", "toBankAccountID": "uuid-def" }

// ❌ SAI: Gửi cả bankName (dư thừa, BE tự resolve)
{ "fromBankAccountID": "uuid-abc", "fromBankName": "Vietcombank CN HCM" }
```

| Field | Gửi lên BE | BE trả về trong response | UI hiển thị |
|-------|-----------|------------------------|-------------|
| TK ngân hàng đi | `fromBankAccountID` ✅ | `fromBankName`, `fromBankAccountNumber` | `ctnb_sel_tk_di`, `ctnb_i_ten_nh_di` |
| TK ngân hàng đến | `toBankAccountID` ✅ | `toBankName`, `toBankAccountNumber` | `ctnb_sel_tk_den`, `ctnb_i_ten_nh_den` |
| TK Nợ (hạch toán) | `debitAccountId` ✅ | `debitAccount`, `debitAccountNumber` | `ctnb_sel_tk_no_0` |
| TK Có (hạch toán) | `creditAccountId` ✅ | `creditAccount`, `creditAccountNumber` | `ctnb_sel_tk_co_0` |

### 8.2 Response Phải Có Display Fields Để UI Hiển Thị

Khi edit/view, dialog cần hiển thị lại đúng giá trị đã chọn. **Tất cả display fields phải có trong response DTO.**

#### 8.2.1 Phương pháp kiểm tra: Lấy UI làm chuẩn, đối chiếu DTO response

```
B1: Liệt kê mọi field UI hiển thị trong dialog (data-qa → formData key)
B2: Đối chiếu formData key → DTO response field
B3: Field nào UI có mà DTO KHÔNG có → BE THIẾU
```

#### 8.2.2 Các field BE thường xuyên thiếu trong response — Báo Cáo Chi Tiết

> **Quy tắc báo cáo:** Mỗi field thiếu PHẢI chỉ rõ:
> 1. **Field name** — field bị thiếu trong DTO
> 2. **API endpoint** — đường dẫn API bị ảnh hưởng
> 3. **HTTP method** — GET/POST/PUT
> 4. **Vị trí** — Response (GET response thiếu) hay Request (POST/PUT không chấp nhận)
> 5. **DTO hiện tại** — tên interface/class BE đang dùng
> 6. **So sánh** — DTO tương tự có field này không (làm bằng chứng BE đã có pattern)

**Format mẫu:**

| # | Field | API Endpoint | Method | Vị trí | DTO hiện tại | So sánh | Hành động |
|---|-------|-------------|--------|--------|-------------|---------|----------|
| 1 | `postedDate` | `/api/accounting/v1/bank/transfers` | **GET** | **Response** | `BankTransferDetail` KHÔNG có `postedDate` | `BankDepositDetail` (receipt/payment) CÓ `postedDate` | BE thêm `postedDate` vào `BankTransferDetail` response |
| 2 | `postedDate` | `/api/accounting/v1/bank/transfers` | **POST/PUT** | **Request** | `CreateBankTransferRequest` KHÔNG có `postedDate` | `CreateBankReceiptRequest` CÓ `postedDate?` | BE thêm `postedDate?` vào `CreateBankTransferRequest` |
| 3 | `refNoManagement` | `/api/accounting/v1/bank/transfers` | **GET** | **Response** | `BankTransferDetail` KHÔNG có `refNoManagement` | `BankDepositDetail` CÓ `refNoManagement` | BE thêm `refNoManagement` vào `BankTransferDetail` response |
| 4 | `refNoManagement` | `/api/accounting/v1/bank/transfers` | **POST/PUT** | **Request** | `CreateBankTransferRequest` KHÔNG có `refNoManagement` | `CreateBankReceiptRequest` CÓ `refNoManagement?` | BE thêm `refNoManagement?` vào `CreateBankTransferRequest` |
| 5 | `accountingDetails[].debitAccountId` | `/api/accounting/v1/bank/transfers` | **GET** | **Response** | `BADepositDetailLineDto.debitAccountId?` (optional) | UI cần biết để hiển thị combobox | BE đổi `debitAccountId` thành required (không optional) trong response |
| 6 | `accountingDetails[].creditAccountId` | `/api/accounting/v1/bank/transfers` | **GET** | **Response** | `BADepositDetailLineDto.creditAccountId?` (optional) | UI cần biết để hiển thị combobox | BE đổi `creditAccountId` thành required (không optional) trong response |

> **Ví dụ báo cáo cụ thể cho BE:**
>
> ```
> BE cần thêm `postedDate` vào:
> - GET /api/accounting/v1/bank/transfers/{id} response (BankTransferDetail)
> - POST/PUT /api/accounting/v1/bank/transfers request (CreateBankTransferRequest)
>
> Lý do: UI có field `ctnb_dt_posted_date` (DatePicker Ngày hạch toán).
> Khi edit/view, FE map `d.postedDate` → formData.postedDate để hiển thị.
> Nhưng BankTransferDetail KHÔNG có field này → UI luôn trống.
> BankDepositDetail (receipt/payment) ĐÃ CÓ → pattern BE đã có.
> ```

> **Cách FE workaround khi BE thiếu:** Dialog dùng `useEffect` gọi API danh mục để resolve số tài khoản → ID. Pattern này **TỐN KÉM** (fetch toàn bộ 9999 records), nên ưu tiên yêu cầu BE bổ sung field vào response.

### 8.3 TableSearchCombobox — Cách Map Dữ Liệu

```tsx
// ── loadOptions: gọi API danh mục, trả về TableComboboxRow[] ──
const loadTaiKhoanNganHang = async (keyword: string): Promise<TableComboboxRow[]> => {
  const r = await TKNHApiService.list({ pageIndex: 1, pageSize: 20, keyword })
  if (r.success && r.data) {
    return r.data.items.map((tk) => ({
      value: tk.id,                                    // ← FK ID gửi lên BE
      cells: {
        accountNumber: tk.accountNumber ?? '',          // ← display field
        bankName: tk.bankName ?? '',                    // ← display field
        bankBranch: (tk as any).bankBranch ?? '',       // ← display field
      },
    }))
  }
  return []
}

// ── onChange: CHỈ set ID (FK) + display fields cho UI ──
const handleTKDiChange = (id: string, rowData: Record<string, string>) => {
  setField('fromBankAccountID', id)                    // ← FK gửi lên BE
  setField('fromBankAccountNumber', rowData.accountNumber ?? '')  // ← để UI hiển thị
  setField('fromBankName', rowData.bankName ?? '')              // ← để UI hiển thị
}
```

### 8.4 Flow Khi Edit/View — Map Response → FormState

```typescript
// initEdit: Map BankTransferDetail → FormState
setFormData({
  // FK IDs — BE phải trả về
  fromBankAccountID: d.fromBankAccountID ?? '',     // ✅ BE có
  toBankAccountID: d.toBankAccountID ?? '',          // ✅ BE có

  // Display fields — BE phải trả về từ FK ID
  fromBankName: d.fromBankName ?? '',                // ✅ BE có
  toBankName: d.toBankName ?? '',                    // ✅ BE có

  // ❌ BE KHÔNG trả về → formData rỗng → UI trống
  postedDate: '',                                    // ← BE thiếu postedDate
  refNoManagement: '',                               // ← BE thiếu refNoManagement

  // Accounting lines:
  accountingDetails: d.accountingDetails?.map(line => ({
    debitAccountId: (line as any).debitAccountId ?? '',   // 🟡 optional
    debitAccount: line.debitAccount ?? '',                // ✅ BE có
    creditAccountId: (line as any).creditAccountId ?? '', // 🟡 optional
    creditAccount: line.creditAccount ?? '',              // ✅ BE có
  }))
})
```

### 8.5 Workaround Khi BE Thiếu Display Fields

```tsx
// Pattern: useEffect resolve FK khi edit/view
// Dùng khi BE response không có display field (ví dụ: fromBankAccountNumber)
useEffect(() => {
  if (!open || mode === 'create') return
  if (formData.fromBankAccountID && !formData.fromBankAccountNumber) {
    TKNHApiService.getById(formData.fromBankAccountID)
      .then(r => {
        if (r.success && r.data) {
          setField('fromBankAccountNumber', (r.data as any).accountNumber ?? '')
        }
      })
      .catch(() => {})
  }
}, [open, mode, formData.fromBankAccountID, formData.fromBankAccountNumber])
```

> ⚠️ **Workaround chỉ dùng cho display fields phụ** (số tài khoản đầy đủ, địa chỉ...).  
> **Các field chính** (bankName, postedDate, refNoManagement) → PHẢI yêu cầu BE bổ sung vào DTO.  
> Nếu BE không bổ sung, gửi inbox task cho BE với danh sách field thiếu kèm route + DTO hiện tại.

---

## 9. Quy Tắc Form — Default API, Init Create & Payload (BẮT BUỘC)

### 9.1 Gọi API Default Để Lấy Số Chứng Từ & Ngày Chứng Từ

> **Khi mở form tạo mới, PHẢI gọi API `getDefault()` để lấy số chứng từ tiếp theo và ngày chứng từ mặc định.**

```tsx
const initCreate = useCallback(async () => {
  setMode('create')
  setEditingId(null)
  setErrors({})
  setTouched({})
  try {
    const r = await XxxApiService.getDefault()
    if (r.success && r.data) {
      const { nextVoucherCode, defaultVoucherDate } = r.data
      setFormData({
        ...XXX_INITIAL_FORM,
        voucherCode: nextVoucherCode ?? '',        // ← Số chứng từ từ BE
        voucherDate: (defaultVoucherDate ?? '').slice(0, 10), // ← Ngày chứng từ từ BE
      })
      return
    }
  } catch {
    // fallthrough — để form trống nếu API default lỗi
  }
  setFormData({ ...XXX_INITIAL_FORM })
}, [])
```

#### 9.1.1 Nếu Không Biết Cấu Trúc Default API → Yêu Cầu Cung Cấp

> **TUYỆT ĐỐI KHÔNG** tự đoán structure của `getDefault()` response.  
> Nếu chưa có docs về response của `GET /api/accounting/v1/xxx/default`:

```
⚠️ GIẢI PHÁP CẦN XÁC NHẬN:
Chưa biết cấu trúc response của API getDefault() cho module này.
Vui lòng cung cấp response schema (các field trả về) của:
  GET /api/accounting/v1/{route}/default

Ví dụ mẫu (từ module khác):
{
  "nextDiscountCode": "GGHM00001",   // Số chứng từ tiếp theo
  "defaultDiscountDate": "2026-07-07" // Ngày chứng từ mặc định
}
```

#### 9.1.2 Default API Có Thể Trả Về Nhiều Field Khác

Ngoài `nextVoucherCode` và `defaultVoucherDate`, API default **có thể** trả về thêm:
- `defaultPostedDate` — ngày hạch toán mặc định
- `defaultCurrencyId` — loại tiền mặc định
- `defaultExchangeRate` — tỷ giá mặc định
- Các field tùy chỉnh khác theo từng nghiệp vụ

> **Quy tắc:** Nếu API default trả về field nào có trên UI → fill vào form field đó.  
> Nếu không chắc field nào có thể có → kiểm tra response thực tế hoặc hỏi BE.

### 9.2 TẤT CẢ Field Trên UI Phải Có Trong Payload (Trừ Readonly)

> **Nguyên tắc:** Mọi field hiển thị trên UI (form/dialog) mà user có thể nhập liệu → PHẢI có mặt trong payload gửi lên BE.  
> **Ngoại lệ:** Các field được đánh dấu `readOnly` hoặc `disabled` (do fill tự động từ dữ liệu khác).

**Quy trình kiểm tra:**

```
B1: Liệt kê tất cả field trong FormState (types UI)
B2: Đối chiếu từng field với CreateRequest / UpdateRequest (types API)
B3: Field có trong FormState mà KHÔNG có trong Request DTO:
    ├── Là readonly/disabled? → Bỏ qua (field hiển thị tham khảo)
    └── User nhập được?      → BÁO LỖI: Interface thiếu field này
```

**Ví dụ báo cáo field thiếu:**

| # | FormState Field | Request Field | Trạng thái | Hành động |
|---|----------------|---------------|-----------|----------|
| 1 | `employeeId` | `employeeId` | ❌ Thiếu | BE thêm `employeeId` vào `CreateXxxRequest` |
| 2 | `bankAccountId` | — | ❌ Thiếu | BE thêm `bankAccountId` vào `CreateXxxRequest` |
| 3 | `invoiceTemplateCode` | — | readonly (fill từ CTMH) | Bỏ qua |

### 9.3 TK Fields — Gửi ID, Không Gửi AccountNumber

> **⚠️ TUYỆT ĐỐI CẤM gửi `debitAccountNumber` / `creditAccountNumber` lên payload.**
> Payload CHỈ chứa `debitAccountId` / `creditAccountId` (UUID).
> `debitAccountNumber` / `creditAccountNumber` là display-only, DTO cho phép nhưng set `null` khi gửi.
> 
> **Quy tắc:** Với các field tài khoản (debitAccount, creditAccount, bankAccount...):
> - **Combobox** hiển thị `accountNumber` cho user dễ nhận diện
> - **Payload** CHỈ gửi `debitAccountId` / `creditAccountId` / `bankAccountId` (UUID)
> - **BE** tự resolve ID → accountNumber và trả về trong response

```typescript
// ✅ ĐÚNG: Payload build — CHỈ gửi ID, number = null
details: formData.details.map(l => ({
  debitAccountId: l.debitAccountId || null,
  debitAccountNumber: null, // ← KHÔNG gửi, BE tự resolve
  creditAccountId: l.creditAccountId || null,
  creditAccountNumber: null, // ← KHÔNG gửi, BE tự resolve
}))

// ❌ SAI: Gửi accountNumber — BE không resolve được, dễ lỗi
details: formData.details.map(l => ({
  debitAccountNumber: l.debitAccountNumber || null, // ← SAI
  creditAccountNumber: l.creditAccountNumber || null, // ← SAI
}))
```

#### 9.3.1 Không Chỉ Định TK → Hiển Thị Combobox Cho User Chọn

> Nếu **KHÔNG** có default TK (không có `getDefault()` trả về TK, không có config), form **KHÔNG** tự điền số TK mặc định. Combobox sẽ để trống và user tự chọn.

#### 9.3.2 Có Chỉ Định AccountNumber → Dùng Hook `useAccountId` Để Lấy ID

> Khi default API hoặc config trả về **số tài khoản** (string, không phải UUID), PHẢI resolve sang ID qua hook `useAccountId`:

```tsx
// Hook useAccountId — resolve accountNumber → { id, accountNumber }
const useAccountId = () => {
  const resolveAccountNumber = useCallback(async (accountNumber: string): Promise<{ id: string; number: string } | null> => {
    if (!accountNumber) return null
    try {
      // ƯU TIÊN: dùng getById nếu BE hỗ trợ
      // Hoặc: list + filter với keyword chính xác (pageSize vừa đủ, KHÔNG 9999)
      const tkRes = await TKApiService.list({ pageIndex: 1, pageSize: 100, keyword: accountNumber })
      if (tkRes.success && tkRes.data?.items) {
        const found = tkRes.data.items.find(tk => tk.accountNumber === accountNumber)
        if (found) return { id: found.id, number: found.accountNumber }
      }
    } catch { /* ignore */ }
    return null
  }, [])
  return { resolveAccountNumber }
}
```

#### 9.3.3 Field Khác Có Sẵn AccountNumber → Cũng Dùng Hook Để Lấy ID

> Nếu một field khác (VD: `bankAccountNumber` từ chứng từ gốc) có sẵn `accountNumber`, cũng gọi `resolveAccountNumber()` để lấy `bankAccountId` trước khi gửi payload:

```tsx
// Khi chọn chứng từ gốc → fill bankAccountNumber → resolve ID
if (d.bankAccountNumber) {
  const resolved = await resolveAccountNumber(d.bankAccountNumber)
  if (resolved) {
    setField('bankAccountId', resolved.id)
    setField('bankAccountNumber', resolved.number)
  }
}
```

#### 9.3.4 Gửi ID Lên BE → Expect BE Trả Về AccountNumber

> **Payload:** `debitAccountId: "uuid"`  
> **Response:** `debitAccountId: "uuid"`, `debitAccountNumber: "1111"`, `debitAccountName: "Tiền mặt"`  
> Khi edit/view, map `debitAccountNumber` từ response vào form để combobox hiển thị đúng.

#### 9.3.5 Kiểm Tra Interface Trước Khi Gửi ID

> **Trước khi dùng `debitAccountId`/`creditAccountId` trong payload, PHẢI kiểm tra request DTO đã có field đó chưa.**  
> Nếu chưa có → DỪNG, báo cáo yêu cầu BE bổ sung (theo format Section 3.6.0).

---

## 10. Quy Tắc Resolve FK Ngược Khi Edit/View (BẮT BUỘC)

> **Khi mở form Edit/View, các field FK chỉ có ID → PHẢI resolve ngược lại để hiển thị display value (code/name) cho user.**

### 10.1 Nguyên Tắc: Resolve Đúng Những Gì Combobox Hiển Thị

| Combobox `displayField` | Khi chọn → lưu gì? | Khi edit → resolve hiển thị gì? |
|------------------------|--------------------|-------------------------------|
| `displayField='code'` | `accountObjectCode: rd.code`, `accountObjectName: rd.name` | Resolve và set **code** vào `initialLabel` |
| `displayField='name'` | `employeeName: rd.name` | Resolve và set **name** vào `initialLabel` |
| `displayField='accountNumber'` | `bankAccountNumber: rd.accountNumber` | Resolve và set **accountNumber** vào `initialLabel` |

> **Quy tắc:** Combobox hiển thị field gì khi select → khi edit phải resolve và hiển thị đúng field đó.

### 10.2 Pattern Resolve — Dùng `useEffect` Trong Dialog

```tsx
// ── Resolve accountObjectId → accountObjectCode khi edit/view ──────────
useEffect(() => {
  if (!open || mode === 'create') return
  if (formData.accountObjectId && !formData.accountObjectCode) {
    XxxApiService.getById(formData.accountObjectId)
      .then(r => {
        if (r.success && r.data) {
          // displayField='code' → set code vào initialLabel
          setField('accountObjectCode', r.data.code ?? '')
          // Các field phụ khác (chỉ set nếu chưa có)
          if (!formData.accountObjectName) setField('accountObjectName', r.data.name ?? '')
        }
      })
      .catch(() => {})
  }
}, [open, mode, formData.accountObjectId, formData.accountObjectCode])
```

### 10.3 Code Mẫu Cho Từng Loại Combobox

```tsx
// displayField='code' (VD: Nhà cung cấp)
<TableSearchCombobox
  value={formData.accountObjectId || ''}
  initialLabel={formData.accountObjectCode || formData.accountObjectName || ''}
  displayField='code'    // ← Hiển thị code
  onChange={(id, rd) => {
    setField('accountObjectId', id)
    setField('accountObjectCode', rd.code || '')  // ← Lưu code
    setField('accountObjectName', rd.name || '')  // ← Lưu name (phụ)
  }}
/>

// Khi edit → resolve API → setField('accountObjectCode', r.data.code)

// displayField='name' (VD: Nhân viên)
<TableSearchCombobox
  value={formData.employeeId || ''}
  initialLabel={formData.employeeName || ''}
  displayField='name'    // ← Hiển thị name
  onChange={(id, rd) => {
    setField('employeeId', id)
    setField('employeeName', rd.name || '')  // ← Lưu name
  }}
/>

// Khi edit → resolve API → setField('employeeName', r.data.name)

// displayField='accountNumber' (VD: TK ngân hàng)
<TableSearchCombobox
  value={formData.bankAccountId || ''}
  initialLabel={formData.bankAccountNumber || ''}
  displayField='accountNumber'  // ← Hiển thị accountNumber
  onChange={(id, rd) => {
    setField('bankAccountId', id)
    setField('bankAccountNumber', rd.accountNumber || '')
  }}
/>

// Khi edit → resolve API → setField('bankAccountNumber', r.data.accountNumber)
```

### 10.4 BE Phải Trả Về Display Fields Trong Response

> **CLOSE THE LOOP:** BE response cho GET detail PHẢI chứa tất cả display fields mà combobox cần hiển thị.

| Combobox | value (FK ID) | Cần trong response |
|----------|--------------|-------------------|
| Nhà cung cấp | `accountObjectId` | `accountObjectCode`, `accountObjectName` |
| Nhân viên | `employeeId` | `employeeCode`, `employeeName` |
| TK ngân hàng | `bankAccountId` | `bankAccountNumber`, `bankName` |
| TK Nợ/Có | `debitAccountId` / `creditAccountId` | `debitAccountNumber`, `debitAccountName` |

> Nếu response thiếu field → báo cáo yêu cầu BE bổ sung (dùng format Section 8.2.2).

---

## 11. Quy Tắc Gọi API Tài Khoản — TUYỆT ĐỐI KHÔNG Truyền `isActive`

> **Khi gọi API danh mục tài khoản (TKApiService, TKNHApiService...) để lấy danh sách hoặc resolve: TUYỆT ĐỐI KHÔNG truyền tham số `isActive`.**

```tsx
// ❌ SAI — truyền isActive làm giới hạn kết quả, user có thể không chọn được TK đã ngừng
const r = await TKApiService.list({ pageIndex: 1, pageSize: 20, keyword, isActive: true })

// ✅ ĐÚNG — không truyền isActive, để BE tự quyết định
const r = await TKApiService.list({ pageIndex: 1, pageSize: 20, keyword })
```

> **Lý do:** TK có thể đã bị vô hiệu hóa (isActive=false) nhưng vẫn được dùng trong các phiếu cũ. Khi edit các phiếu cũ, cần resolve được cả TK đã ngừng. BE sẽ tự xử lý logic lọc phù hợp.

**Áp dụng cho TẤT CẢ API danh mục liên quan đến tài khoản:**
- `TKApiService.list()` — Danh mục tài khoản kế toán
- `TKNHApiService.list()` — Tài khoản ngân hàng
- Các API danh mục khác có field FK tương tự

---

## 12. Cập Nhật Checklist

Bổ sung các mục sau vào checklist:
- [ ] Ghost column dùng Button thủ công + `DropdownMenu`, KHÔNG dùng `DmRowActions`
- [ ] Icon đúng: `Eye` cho Xem, `Trash2` cho Xóa, `BookOpen` cho Ghi sổ, `Pencil` cho Bỏ ghi và sửa, `Copy` cho Nhân bản, `MoreHorizontal` cho dropdown trigger
- [ ] Class variant đúng: `icon-warning` cho Bỏ ghi và sửa, `icon-danger` cho Xóa
- [ ] **Dialog footer đúng action:** View unposted → [Sửa][Ghi sổ], View posted → [Bỏ ghi và sửa] (1 button, unpost rồi edit), Create → [Hủy][Lưu][Lưu & Ghi sổ], Edit → [Hủy][Lưu]
- [ ] **Confirm đóng dialog:** Create → đóng trực tiếp không confirm. Edit → confirm nếu `dirtyRef.current === true`. View → đóng trực tiếp.
- [ ] **Nút [Hủy] Create footer:** `onClick={() => onOpenChange(false)}` — KHÔNG check `dirtyRef`, KHÔNG mở `unsavedOpen`
- [ ] **Nút X Header:** check `mode === 'create' || mode === 'view'` → đóng luôn. Edit → check `dirtyRef`.
- [ ] **Hook `handleSubmit` KHÔNG auto-post:** `handleSubmit` (nút "Lưu") chỉ gọi API create/update, TUYỆT ĐỐI KHÔNG gọi `post()` bên trong. Không có auto-post trong `handleSubmit` hoặc `handleSubmitAndNew`.
- [ ] Hook có `handleCreateAndPost`: `create()` → `post()` liên tiếp. Đây là nơi DUY NHẤT gọi đồng thời cả tạo và ghi sổ.
- [ ] **Cột "Số tiền" canh phải:** header `text-right` + cell `text-right`
- [ ] **Có hàng tổng cộng:** `bg-[#ECEDEF]`, `border-t-2`, chữ "Tổng cộng" ở cột đầu, `formatNumber(totalSum)` ở cột số tiền
- [ ] **TK Nợ/Có dùng ID:** payload gửi `debitAccountId`/`creditAccountId`, UI hiển thị `debitAccountNumber`/`creditAccountNumber`, combobox `value=tk.id`
- [ ] **Default STK resolve ID:** `initCreate` gọi `resolveAccountNumber()` → chỉ set `accountNumber` khi có `accountId`. Không hardcode số mặc định trong `XXX_INITIAL_LINE`
- [ ] **`XXX_INITIAL_LINE` không hardcode số TK:** `debitAccountNumber: ''`, `creditAccountNumber: ''` — để trống hoàn toàn
- [ ] **Dialog onChange Đối tượng không set TK Nợ/Có:** không gọi `updateLine` với `debitAccountNumber`/`creditAccountNumber` cứng
- [ ] **Default `itemsPerPage` = 50 & lưu localStorage:** `getPageSizeFromStorage(50)` thay vì `getPageSizeFromStorage(10)`. `handleItemsPerPageChange` PHẢI gọi `savePageSizeToStorage(size)` để lưu lại khi user đổi số dòng/trang.
- [ ] **🖥️ Dialog full-screen:** DialogContent `maxWidth='none'` + `w-[100vw] h-[100vh] p-0 gap-0 rounded-none` + `flex flex-col overflow-hidden` + `[&>button:first-child]:hidden`
- [ ] **🖥️ KHÔNG dùng `DialogHeader`/`DialogTitle`/`DialogFooter`** — thay bằng custom div
- [ ] **🖥️ Body gray bg + min-h-0:** `<div className='flex-1 min-h-0 overflow-y-auto bg-[#f4f5f7]'>` + inner `<div className='p-5 space-y-4'>`
- [ ] **🖥️ Header:** refNoManagement + refType Select + Tổng tiền + Nút X (unsaved guard chỉ cho Edit, Create/View đóng trực tiếp)
- [ ] **🖥️ Footer py-2.5:** `<div className='flex items-center justify-between px-5 py-2.5 bg-white flex-shrink-0 border-t border-[#B7BCC3]'>`
- [ ] **🖥️ Buttons `btn-secondary`/`btn-primary`:** KHÔNG dùng `variant='outline'` — dùng `btn-secondary h-8 text-[13px] rounded-lg` hoặc `btn-primary h-8 text-[13px] rounded-lg`
- [ ] **🖥️ Input chuẩn:** `h-[30px] text-[13px] rounded-lg border-[#B7BCC3] bg-white`
- [ ] **🖥️ Input trong bảng data có `px-2`:** KHÔNG dùng `p-0` — dùng `px-2` cho tất cả `<Input>` trong `EditableDataTable`
- [ ] **🖥️ Label chuẩn:** `text-[13px] font-semibold text-black`
- [ ] **🖥️ Hạch toán trong card:** `bg-white rounded-lg shadow-sm overflow-hidden` + tab header `border-b-2 border-primary`
- [ ] **🖥️ Error inline:** `<p className='text-xs text-destructive flex items-center gap-1'><AlertCircle className='h-3 w-3' />{...}</p>`
- [ ] **🌐 Gọi API getDefault() trong initCreate:** lấy `nextVoucherCode` + `defaultVoucherDate`, fill vào form. Nếu API default trả thêm field khác (postedDate, currencyId...) → fill tương ứng.
- [ ] **🌐 Không biết cấu trúc default API → DỪNG & hỏi user:** "Chưa biết cấu trúc response của API getDefault(). Vui lòng cung cấp response schema."
- [ ] **🌐 TẤT CẢ field trên UI (có thể nhập) → có trong payload:** kiểm tra từng FormState field → CreateRequest/UpdateRequest. Field user nhập được mà thiếu trong DTO → báo cáo.
- [ ] **🌐 TK fields gửi ID:** `debitAccountId` / `creditAccountId` / `bankAccountId` trong payload, KHÔNG gửi `debitAccountNumber` / `bankAccountNumber`.
- [ ] **🌐 Combobox để trống nếu không có default TK:** không tự điền STK mặc định khi chưa có ID.
- [ ] **🌐 Có accountNumber default → resolve ID qua `useAccountId`:** dùng `TKApiService.list({ keyword })` với pageSize vừa đủ, KHÔNG dùng `pageSize: 9999`.
- [ ] **🌐 TK API list KHÔNG truyền `isActive`:** `TKApiService.list({ pageIndex, pageSize, keyword })` — không có `isActive: true`.
- [ ] **🌐 Edit/View → resolve FK ngược:** `useEffect` resolve `accountObjectId` → `accountObjectCode`, `employeeId` → `employeeName`, `bankAccountId` → `bankAccountNumber`.
- [ ] **🌐 Resolve hiển thị đúng displayField:** combobox `displayField='code'` → resolve set `code`. `displayField='name'` → resolve set `name`. `displayField='accountNumber'` → resolve set `accountNumber`.
- [ ] **🌐 Response DTO phải có display fields cho FK:** `accountObjectCode`, `accountObjectName`, `employeeName`, `bankAccountNumber`, `debitAccountNumber`, `creditAccountNumber`.

---

## 8. Hook Dlg Form — Các Hàm Bắt Buộc

Hook `useXxxDlgForm` phải export các hàm sau để page sử dụng:

```tsx
export function useXxxDlgForm(options?: { onSuccess?: () => void; onClose?: () => void }) {
  // ... state, validate, submit ...

  /** Lưu (create/update) — CHỈ gọi API tạo/cập nhật, KHÔNG gọi API ghi sổ */
  const handleSubmit = async () => { /* validate → create() hoặc update() → toast → onSuccess */ }

  /** Xóa bản ghi */
  const handleDelete = async (id: string) => { /* gọi API delete */ }

  /** Ghi sổ */
  const handlePost = async (id: string) => { /* gọi API post */ }

  /** Bỏ ghi sổ */
  const handleUnpost = async (id: string) => { /* gọi API unpost */ }

  /** Tạo mới & Ghi sổ — gọi create() → post() liên tiếp. ĐÂY LÀ NƠI DUY NHẤT gọi đồng thời cả tạo và ghi sổ. */
  const handleCreateAndPost = async () => { /* validate → create() → post() */ }

  return {
    // ... form state & handlers ...
    handleSubmit,
    handleDelete,
    handlePost,
    handleUnpost,
    handleCreateAndPost,
    serverErrorOpen, setServerErrorOpen,
    serverError,
  }
}
```

> ⚠️ **QUY TẮC SỐ 1:** `handleSubmit` (nút "Lưu") **CHỈ gọi API create/update — KHÔNG BAO GIỜ gọi API post**.  
> ⚠️ **QUY TẮC SỐ 2:** `handleCreateAndPost` (nút "Lưu & Ghi sổ") **gọi create() → post() liên tiếp**. Đây là nơi DUY NHẤT kết hợp cả 2 thao tác.  
> ⚠️ **QUY TẮC SỐ 3:** Không có hàm `handleSubmitAndNew` cho dialog nghiệp vụ có ghi sổ — dialog nghiệp vụ dùng `handleCreateAndPost` thay vì "Lưu & Thêm".

---

## 13. Quy Tắc Resize Cột — Kéo Thay Đổi Độ Rộng & Lưu localStorage (BẮT BUỘC)

> **Các cột trên page phải thay đổi được độ rộng bằng cách kéo cạnh phải của header, và lưu độ rộng mới vào localStorage.**

### 13.1 Hook `useColumnResize`

Hook được đặt tại `src/modules/KetoanApp/hooks/useColumnResize.ts`. Nhận `columns` (từ `useTableSettings`) và `onColumnsChange` (chính là `saveSettings`).

```tsx
import { useColumnResize } from '@/modules/KetoanApp/hooks/useColumnResize'

const { handleResizeStart, getColumnWidth } = useColumnResize(visibleColumns, saveSettings)
```

- `handleResizeStart(colId, mouseEvent)` — gắn vào `onMouseDown` của resize handle trong `DmTableHead`
- `getColumnWidth(colId, defaultWidth)` — trả về width thực tế (đang resize hoặc mặc định), dùng thay cho `col.width` trong style
- Tự động set `cursor: col-resize` và `userSelect: none` trên body trong khi kéo
- Khi thả chuột, gọi `saveSettings` để lưu vào localStorage thông qua `useTableSettings`

### 13.2 Sửa `DmTableHead` — Thêm Resize Handle

Component `DmTableHead` (`src/modules/KetoanApp/components/DmTable.tsx`) có thêm prop `onResizeMouseDown`. Khi có prop này, một thanh kéo mỏng (`w-1.5 cursor-col-resize`) sẽ xuất hiện ở cạnh phải của header.

```tsx
export function DmTableHead({ className, children, pinned, onResizeMouseDown, ...props }: 
  React.ComponentProps<'th'> & { pinned?: boolean; onResizeMouseDown?: (e: React.MouseEvent) => void }
) {
  // ...
  return (
    <th className={cn('relative ...', className)} {...props}>
      {/* ... existing content ... */}
      {onResizeMouseDown && (
        <div
          className="absolute right-0 top-0 bottom-0 w-1.5 cursor-col-resize hover:bg-blue-400/30 transition-colors z-10"
          onMouseDown={onResizeMouseDown}
        />
      )}
    </th>
  )
}
```

**Chú ý:** `th` phải có `relative` để resize handle `absolute` hoạt động đúng.

### 13.3 Tích Hợp Vào Page — Cả 3 Bảng Phải Dùng `getColumnWidth`

Vì layout dùng 3 `<DmTable>` riêng biệt (header / body / total), **cả 3 bảng PHẢI dùng `getColumnWidth`** để độ rộng cột đồng bộ khi đang kéo:

```tsx
// ── Trong header table (CHỈ header mới có onResizeMouseDown) ──
{colsForRender.map(col => {
  const w = getColumnWidth(col.id, col.width)
  return (
    <DmTableHead
      key={col.id}
      onResizeMouseDown={(e) => handleResizeStart(col.id, e)}
      style={{ width: w, minWidth: w, ... }}
    >
      {col.displayName ?? col.title}
    </DmTableHead>
  )
})}

// ── Trong body table (KHÔNG có onResizeMouseDown) ──
{colsForRender.map(col => {
  const w = getColumnWidth(col.id, col.width)
  return (
    <DmTableCell style={{ width: w, ... }}>...</DmTableCell>
  )
})}

// ── Trong total table (KHÔNG có onResizeMouseDown) ──
{colsForRender.map((col, idx) => {
  const w = getColumnWidth(col.id, col.width)
  return (
    <DmTableCell style={{ width: w, minWidth: w, ... }}>...</DmTableCell>
  )
})}
```

### 13.4 Nguyên Lý Hoạt Động

1. User kéo cạnh phải header → `handleResizeStart` được gọi
2. `useColumnResize` theo dõi `mousemove` → cập nhật `resizeState.currentWidth` → `getColumnWidth` trả về width mới → cả 3 bảng re-render với width mới
3. User thả chuột → `saveSettings(columns)` được gọi → `useTableSettings` lưu vào localStorage key `table_settings_phieu-thu`
4. Lần sau mở trang, `useTableSettings` đọc từ localStorage → column widths được khôi phục

### 13.5 Lưu Ý

- Độ rộng tối thiểu mỗi cột: **50px** (`MIN_COL_WIDTH`)
- Chỉ header mới có resize handle — body và total chỉ dùng `getColumnWidth` để sync width
- `DmTable` đã có `tableLayout: 'fixed'` nên width được tôn trọng chính xác
- Resize handle chỉ hiển thị khi có prop `onResizeMouseDown` — an toàn khi dùng cho các bảng không cần resize
## 13. Quy Tắc Chiết Khấu — Dialog Nghiệp Vụ

> **Áp dụng cho:** Mọi dialog nghiệp vụ có bảng hàng hóa và hỗ trợ chiết khấu (Chứng từ bán hàng, Đơn mua, Trả lại hàng bán...).

### 13.1 Các Loại Chiết Khấu

| Key | Label | Mô tả |
|-----|-------|-------|
| `none` | Không chiết khấu | **Default** — không hiển thị cột chiết khấu trên bảng |
| `byItem` | Theo mặt hàng | User tự nhập tỷ lệ CK (%) trên từng dòng. Cột TK chiết khấu hiển thị trên bảng |
| `percent` | Theo % hóa đơn | Nhập 1 tỷ lệ % chung → **onBlur** apply xuống tất cả dòng |
| `amount` | Theo số tiền | Nhập 1 số tiền chung → **onBlur** chia theo tỷ lệ thành tiền từng dòng |

### 13.2 DISCOUNT_TYPE_LABELS Chuẩn

```tsx
export const DISCOUNT_TYPE_LABELS: Record<string, string> = {
  none: 'Không chiết khấu',
  byItem: 'Theo mặt hàng',
  percent: 'Theo % hóa đơn',
  amount: 'Theo số tiền',
}
```

### 13.3 Khi Chọn Khác `none` → Bảng Data Thêm Cột

Khi `discountType !== 'none'`, bảng `EditableDataTable` **PHẢI** thêm các cột sau (theo thứ tự):

| Cột | Key | Width | Editable | Ghi chú |
|-----|-----|-------|----------|--------|
| Tỷ lệ CK (%) | `discountRate` | 100px | ✅ (khi `byItem`) / ❌ readonly (khi `percent`) | `text-right`, `inputMode='numeric'` |
| Tiền chiết khấu | `discountAmount` | 150px | ❌ display | Tự tính = `amount * discountRate / 100` |
| TK chiết khấu | `discountAccountId` | 180px | ✅ `TableSearchCombobox` | Default `5111`, resolve ID qua `TKApiService` |

### 13.4 Code Mẫu Cho Từng Loại Chiết Khấu

#### 13.4.1 Select Chiết Khấu + Input Đi Kèm

```tsx
<div className='flex items-center gap-2'>
  Chiết khấu
  <Select value={formData.discountType} onValueChange={(v) => { setField('discountType', v); setDiscountInput('') }} disabled={isReadOnly}>
    <SelectTrigger className='w-[200px] h-8 text-[13px] border-[#B7BCC3] rounded-lg bg-white' data-qa='sel_chiet_khau'>
      <SelectValue />
    </SelectTrigger>
    <SelectContent>
      {Object.entries(DISCOUNT_TYPE_LABELS).map(([val, label]) => (
        <SelectItem key={val} value={val}>{label}</SelectItem>
      ))}
    </SelectContent>
  </Select>

  {/* Theo % hóa đơn — input % bên cạnh */}
  {formData.discountType === 'percent' && (
    <div className='flex items-center gap-1'>
      <Input type='text' inputMode='numeric'
        value={discountInput}
        onChange={e => setDiscountInput(e.target.value.replace(/[^0-9.]/g, ''))}
        onBlur={() => applyDiscountPercent()}
        className='h-[30px] w-[80px] text-[13px] text-right rounded-lg border-[#B7BCC3] bg-white'
        data-qa='i_discount_percent' placeholder='0' />
      <span className='text-[13px] text-gray-500'>%</span>
    </div>
  )}

  {/* Theo số tiền — input số tiền bên cạnh */}
  {formData.discountType === 'amount' && (
    <Input type='text' inputMode='numeric'
      value={discountInput ? formatNumber(Number(discountInput) || 0) : ''}
      onChange={e => setDiscountInput(e.target.value.replace(/\./g, '').replace(/[^0-9]/g, ''))}
      onBlur={() => applyDiscountAmount()}
      className='h-[30px] w-[140px] text-[13px] text-right rounded-lg border-[#B7BCC3] bg-white'
      data-qa='i_discount_amount' placeholder='0' />
  )}
</div>
```

#### 13.4.2 applyDiscountPercent — % Hóa Đơn

```tsx
const applyDiscountPercent = useCallback(() => {
  const rate = discountInput || '0'
  const updated = formData.details.map(line => ({
    ...line,
    discountRate: rate,
    discountAmount: String(Math.round(toNum(line.amount) * Number(rate)) / 100),
  }))
  setDetails(updated)
}, [discountInput, formData.details, setDetails])
```

#### 13.4.3 applyDiscountAmount — Số Tiền Trên Tổng

```tsx
const applyDiscountAmount = useCallback(() => {
  const total = formData.details.reduce((s, l) => s + toNum(l.amount), 0)
  const discountVal = Number(discountInput) || 0
  const updated = formData.details.map(line => {
    const proportion = total > 0 ? toNum(line.amount) / total : 0
    const lineDiscount = Math.round(discountVal * proportion)
    return {
      ...line,
      discountRate: total > 0 ? String(Math.round((lineDiscount / toNum(line.amount)) * 100 * 100) / 100) : '0',
      discountAmount: String(lineDiscount),
    }
  })
  setDetails(updated)
}, [discountInput, formData.details, setDetails])
```

### 13.5 Cột Tỷ Lệ CK (%) & Tiền CK Trong Bảng

```tsx
// Chỉ hiển thị khi discountType !== 'none'
...(formData.discountType !== 'none' ? [
  {
    key: 'discountRate', label: 'Tỷ lệ CK (%)', width: '100px',
    render: (v, _r, idx) => {
      const readOnly = isReadOnly || formData.discountType !== 'byItem'
      return readOnly
        ? <span className='block text-right text-[13px]'>{String(v || '0')}</span>
        : <Input type='text' inputMode='numeric'
            value={String(v ?? '')}
            onChange={e => {
              const rate = e.target.value.replace(/[^0-9.]/g, '')
              const line = formData.details[idx]
              updateLineField(idx, 'discountRate', rate)
              updateLineField(idx, 'discountAmount', String(Math.round(toNum(line.amount) * Number(rate || '0')) / 100))
            }}
            className='h-[26px] px-2 text-[13px] text-right rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0'
            data-qa={`i_line_discount_rate_${idx}`} />
    },
  },
  {
    key: 'discountAmount', label: 'Tiền chiết khấu', width: '150px', type: 'display',
    render: (v) => <span className='block text-right text-[13px]'>{formatNumber(Number(v) || 0)}</span>,
  },
  {
    key: 'discountAccountId', label: 'TK chiết khấu', width: '180px',
    render: (_v, row, idx) => isReadOnly
      ? <span className='text-[13px]'>{String(row.discountAccountNumber ?? '')}</span>
      : <TableSearchCombobox
          value={String(row.discountAccountId ?? '')}
          initialLabel={String(row.discountAccountNumber ?? '')}
          displayField='accountNumber'
          onChange={(id, rd) => {
            updateLine(idx, {
              discountAccountId: id,
              discountAccountNumber: rd.accountNumber || '',
            })
          }}
          loadOptions={loadTaiKhoan}
          columns={taiKhoanColumns}
          dataQa={`sel_line_discount_account_${idx}`} />,
  },
] : []),
```

### 13.6 TK Chiết Khấu — Default 5111, Resolve ID Qua TKApiService

```tsx
// Trong hook useXxxDlgForm:
import { TKApiService } from '@/modules/KetoanApp/features/danh-muc/tai-khoan/services'

const resolveAccountNumber = useCallback(async (accountNumber: string): Promise<{ id: string; number: string } | null> => {
  if (!accountNumber) return null
  try {
    const tkRes = await TKApiService.list({ pageIndex: 1, pageSize: 100, keyword: accountNumber })
    if (tkRes.success && tkRes.data?.items) {
      const found = tkRes.data.items.find(tk => tk.accountNumber === accountNumber)
      if (found) return { id: found.id, number: found.accountNumber }
    }
  } catch { /* ignore */ }
  return null
}, [])

// Trong initCreate:
const discountAccount = await resolveAccountNumber('5111')
const defaultLine: XxxLineFormState = {
  ...XXX_INITIAL_LINE,
  discountAccountId: discountAccount?.id ?? '',
  discountAccountNumber: discountAccount?.number ?? '',
}
```

```tsx
// Trong dialog — loadTaiKhoan cho TableSearchCombobox:
const taiKhoanColumns: TableComboboxColumn[] = [
  { field: 'accountNumber', title: 'Số TK', width: 100 },
  { field: 'accountName', title: 'Tên tài khoản', width: 200 },
]

const loadTaiKhoan = async (keyword: string): Promise<TableComboboxRow[]> => {
  try {
    const r = await TKApiService.list({ pageIndex: 1, pageSize: 20, keyword })
    if (r.success && r.data) {
      return r.data.items.map(tk => ({
        value: tk.id,
        cells: {
          accountNumber: tk.accountNumber ?? '',
          accountName: tk.accountName ?? '',
        },
      }))
    }
  } catch { /* ignore */ }
  return []
}
```

### 13.7 Checklist Chiết Khấu

- [ ] `DISCOUNT_TYPE_LABELS` có đủ 4 option: `none`, `byItem`, `percent`, `amount`
- [ ] Default `discountType = 'none'` trong `XXX_INITIAL_FORM`
- [ ] Khi `discountType !== 'none'` → bảng hiển thị thêm cột: Tỷ lệ CK (%), Tiền chiết khấu, TK chiết khấu
- [ ] Cột `discountRate` readonly khi `percent` hoặc `amount`, editable khi `byItem`
- [ ] `percent` — input % bên cạnh select, onBlur apply xuống toàn bộ dòng
- [ ] `amount` — input số tiền bên cạnh select, onBlur chia theo tỷ lệ thành tiền từng dòng
- [ ] TK chiết khấu default `5111`, resolve ID qua `TKApiService.list({ keyword: '5111' })`
- [ ] `TKApiService.list` KHÔNG truyền `isActive`
- [ ] `discountAccountId` và `discountAccountNumber` có trong `CTBHLineFormState`
- [ ] `discountAccountId` có default trong `XXX_INITIAL_LINE` sau khi resolve
- [ ] `discountAccountId` có trong `buildFormData` khi edit
- [ ] Dòng "Chiết khấu" hiển thị dưới "Tổng tiền hàng" khi `discountType !== 'none'` (xem 13.8)

### 13.8 Dòng Chiết Khấu Dưới Tổng Tiền Hàng

> **Áp dụng cho:** Mọi dialog có chiết khấu hóa đơn — khi `discountType !== 'none'`, PHẢI hiển thị dòng "Chiết khấu" bên dưới "Tổng tiền hàng" trong khu vực tổng kết bên phải.

```tsx
{/* Tổng tiền hàng / Chiết khấu / Tổng tiền thanh toán */}
<div className='w-[260px] flex-shrink-0 space-y-1.5 pt-1'>
  <div className='flex items-center justify-between text-[13px]'>
    <span className='text-black'>Tổng tiền hàng</span>
    <span className='text-black'>{formatNumber(totalGoods)}</span>
  </div>
  {formData.discountType !== 'none' && (
    <div className='flex items-center justify-between text-[13px]'>
      <span className='text-black'>Chiết khấu</span>
      <span className='text-black'>-{formatNumber(totalDiscount)}</span>
    </div>
  )}
  <div className='flex items-center justify-between text-[13px]'>
    <span className='font-semibold text-black'>Tổng tiền thanh toán</span>
    <span className='font-bold text-black'>{formatNumber(totalAmount)}</span>
  </div>
</div>
```

**Công thức tính trong hook:**

```tsx
const totalGoods = formData.details.reduce((s, l) => s + num(l.amount), 0)
const totalTax = formData.details.reduce((s, l) => s + num(l.taxAmount), 0)
const totalDiscount = formData.details.reduce((s, l) => s + num(l.discountAmount), 0)
const totalAmount = totalGoods + totalTax - totalDiscount
```

**Quy tắc:**
- Dòng "Chiết khấu" CHỈ hiển thị khi `discountType !== 'none'`
- Số tiền chiết khấu hiển thị dạng `-{formatNumber(totalDiscount)}` (có dấu trừ)
- Tổng tiền thanh toán = Tổng tiền hàng + Tổng thuế - Tổng chiết khấu
- Vị trí: giữa dòng "Tổng tiền hàng" và "Tổng tiền thanh toán"

---

## 14. Quy Tắc Payload — Chỉ Gửi Field Có Giá Trị & Đúng Tab Ngữ Cảnh

> **Nguyên tắc cốt lõi:** Payload gửi lên BE CHỈ chứa các field thực sự có giá trị (non-null, non-empty) và thuộc về tab/card đang active. Field null/rỗng hoặc thuộc tab không active → KHÔNG có trong payload.

### 14.1 Hai Lớp Lọc

| Lớp | Quy tắc | Ví dụ |
|-----|---------|-------|
| **Lớp 1: Null/Empty** | Field có giá trị `null`, `undefined`, `''`, `0` (với string) → không gửi | `description: ''` → omit |
| **Lớp 2: Tab ngữ cảnh** | Field chỉ tồn tại trên tab/card KHÔNG active → không gửi | Tab "Chứng từ ghi nợ" không active → không gửi `description` |

### 14.2 Pattern `buildPayload` Chuẩn

```tsx
const buildPayload = (): CreateXxxRequest => {
  // ── Các field chung (luôn có) ──
  const payload: CreateXxxRequest = {
    refNo: formData.refNo || undefined,
    refDate: formData.refDate,
    // ...
  }

  // ── Field theo tab ngữ cảnh ──
  // Tab A (VD: Chứng từ ghi nợ)
  if (formData.paymentStatus === 'unpaid') {
    payload.description = formData.description || undefined
    payload.paymentTermId = formData.paymentTermId || undefined
  }

  // Tab B (VD: Phiếu thu)
  if (formData.paymentStatus === 'paid') {
    if (formData.paymentMethod === BankTransfer) {
      payload.bankAccountId = formData.bankAccountId || undefined
    }
  }

  return payload
}
```

> ⚠️ **TUYỆT ĐỐI KHÔNG** gửi field từ 2 tab xung đột trong cùng 1 payload.  
> VD: Không thể gửi đồng thời `description` (Chứng từ ghi nợ) và `bankAccountId` (Thu tiền gửi) vì chúng thuộc về 2 ngữ cảnh `paymentStatus` khác nhau.

### 14.3 Ví Dụ CTBHDialog — Ma Trận Field Theo Tab

| Tab | Điều kiện | Field đặc thù |
|-----|----------|--------------|
| **Chứng từ ghi nợ** | `paymentStatus === 'unpaid'` | `description`, `paymentTermId` |
| **Phiếu thu** | `paymentStatus === 'paid' && paymentMethod === Cash` | *(dùng field chung)* |
| **Thu tiền gửi** | `paymentStatus === 'paid' && paymentMethod === BankTransfer` | `bankAccountId` |
| **Phiếu xuất** | `checkOutward === true` | *(field trong `outwardReferences[]`)* |
| **Hóa đơn** | `attachInvoice === true` | `invoiceStatus`, `invoiceNumber`, `invoiceSerial`, `invoiceDate`, `eInvoiceType` |

### 14.4 Logic Xung Đột Tab — Mutual Exclusivity

> **Quy tắc:** Các tab thay đổi nội dung dựa trên cùng 1 biến trạng thái thì field của chúng **xung đột** — không thể cùng tồn tại trong payload.

```
Tab thứ nhất (slot chính) thay đổi theo paymentStatus:
  paymentStatus === 'unpaid' → "Chứng từ ghi nợ"
  paymentStatus === 'paid'   → "Phiếu thu" hoặc "Thu tiền gửi"

→ Field của "Chứng từ ghi nợ" và "Phiếu thu" KHÔNG thể cùng tồn tại
→ Payload CHỈ chứa field của tab hiện tại
```

### 14.5 Checklist Payload

- [ ] **Field null/empty → omit:** dùng `|| undefined` cho string, kiểm tra truthy trước khi gán
- [ ] **Field tab-specific → condition:** mỗi field có điều kiện tab rõ ràng trước khi đưa vào payload
- [ ] **Tab xung đột → không trộn:** field từ 2 tab dùng chung 1 slot KHÔNG cùng xuất hiện
- [ ] **Field UI-only → không gửi:** field chỉ có trong FormState nhưng không có trong Request DTO → bỏ qua

---

## 15. Quy Tắc Resolve TK Từ Mã Hàng Trong Bảng Data (BẮT BUỘC)

> **Áp dụng cho:** Mọi dialog nghiệp vụ có bảng hàng hóa (`EditableDataTable`) với cột TK (Nợ/Có/Trả lại/Công nợ/Chiết khấu...).
> Khi user chọn mã hàng, hệ thống có thể biết được số TK (number) từ thông tin hàng hóa (VD: `returnAccountCode`, `saleAccountCode`...).
> **Chỉ biết NUMBER, KHÔNG biết ID** → PHẢI resolve number → ID qua `resolveAccountNumber`.

### 15.1 Nguyên Tắc Cốt Lõi

| Bước | Mô tả |
|------|-------|
| 1. Chọn mã hàng | `TableSearchCombobox` onChange → nhận `rd` chứa `returnAccountCode`, `saleAccountCode`... |
| 2. Resolve number → ID | Gọi `resolveAccountNumber(accountNumber)` → lấy `{ id, number }` |
| 3. Chỉ hiển thị number khi có ID | Combobox `initialLabel` chỉ set `accountNumber` khi đã resolve được `accountId` |
| 4. Payload chỉ gửi ID | `debitAccountId` / `creditAccountId` / `discountAccountId` — KHÔNG gửi `debitAccountNumber` / `creditAccountNumber` |

### 15.2 `resolveAccountNumber` — Bắt Buộc Có Trong Hook

```tsx
// Trong useXxxDlgForm:
import { TKApiService } from '@/modules/KetoanApp/features/danh-muc/tai-khoan/services'

/** Resolve số tài khoản → ID. KHÔNG truyền isActive. */
const resolveAccountNumber = useCallback(async (accountNumber: string): Promise<{ id: string; number: string } | null> => {
  if (!accountNumber) return null
  try {
    const tkRes = await TKApiService.list({ pageIndex: 1, pageSize: 100, keyword: accountNumber })
    if (tkRes.success && tkRes.data?.items) {
      const found = tkRes.data.items.find(tk => tk.accountNumber === accountNumber)
      if (found) return { id: found.id, number: found.accountNumber }
    }
  } catch { /* ignore */ }
  return null
}, [])
```

> ⚠️ **TUYỆT ĐỐI KHÔNG** truyền `isActive` vào `TKApiService.list` — TK đã ngừng vẫn có thể được dùng trong các phiếu cũ.

### 15.3 Dialog — onChange Chọn Mã Hàng (Resolve Async)

```tsx
// Trong dialog, onChange của TableSearchCombobox chọn mã hàng:
onChange={(id, rd) => {
  // ── Set các field cơ bản từ hàng hóa ──
  updateLine(idx, {
    inventoryItemId: id,
    itemCode: rd.code || '',
    inventoryItemName: rd.name || '',
    unit: rd.unit || '',
    unitPrice: rd.unitPrice || String(row.unitPrice ?? ''),
    industryGroupCode: rd.industryGroupCode || '',
    // ── Xóa TK cũ khi chọn hàng mới (đợi resolve xong mới fill) ──
    debitAccountId: '',
    debitAccountNumber: '',
    creditAccountId: '',
    creditAccountNumber: '',
  })

  // ── Resolve TK trả lại (returnAccountCode) từ mã hàng ──
  if (rd.returnAccountCode) {
    resolveAccountNumber(rd.returnAccountCode).then(resolved => {
      if (resolved) {
        updateLine(idx, {
          debitAccountId: resolved.id,
          debitAccountNumber: resolved.number,
        })
      }
      // Nếu resolve thất bại → để trống (KHÔNG hiển thị number khi chưa có ID)
    })
  }

  // ── Nếu có thêm TK khác từ hàng hóa (VD: saleAccountCode, purchaseAccountCode...) ──
  // Resolve tương tự như trên
}}
```

> ⚠️ **QUY TẮC QUAN TRỌNG:** Phải xóa `debitAccountId`/`debitAccountNumber` cũ trước khi resolve mới. Nếu resolve thất bại → để trống, KHÔNG hiển thị số TK cũ hoặc số ảo.

### 15.4 Combobox TK Trong Bảng Data — Chỉ Hiển Thị Number Khi Có ID

```tsx
// TableSearchCombobox cho cột TK trong bảng data:
<TableSearchCombobox
  value={String(row.debitAccountId ?? '')}
  initialLabel={String(row.debitAccountNumber ?? '')}
  displayField='accountNumber'
  onChange={(id, rd) => updateLine(idx, {
    debitAccountId: id,
    debitAccountNumber: rd.accountNumber || '',
  })}
  loadOptions={loadTaiKhoanTable}
  columns={taiKhoanColumns}
  dataQa={`sel_tk_${idx}`}
/>
```

> **Logic:** `value` = `debitAccountId` (ID rỗng → combobox rỗng). `initialLabel` = `debitAccountNumber` (chỉ có giá trị khi ID đã được resolve). Khi user tự chọn TK từ combobox, `onChange` cập nhật cả ID và number.

### 15.5 Payload — Chỉ Gửi ID, Không Gửi Number

```typescript
// ✅ ĐÚNG: buildCreatePayload — CHỈ gửi debitAccountId / creditAccountId
details: formData.details.filter(line => !line.isNote).map(line => ({
  inventoryItemId: line.inventoryItemId || null,
  // ...các field khác...
  debitAccountId: line.debitAccountId || null,       // ← Gửi ID
  creditAccountId: line.creditAccountId || null,      // ← Gửi ID
  // KHÔNG gửi debitAccountNumber / creditAccountNumber
}))

// ❌ SAI: Gửi accountNumber
details: formData.details.map(line => ({
  debitAccountNumber: line.debitAccountNumber || null,  // ← SAI
  creditAccountNumber: line.creditAccountNumber || null, // ← SAI
}))
```

### 15.6 BuildFormData Khi Edit — Resolve TK Number → ID

```typescript
// Trong buildFormData của hook:
const buildFormData = useCallback(async (d: XxxDetail): Promise<XxxFormState> => {
  // ── Thu thập tất cả accountNumber cần resolve ──
  const accountNumbers = [...new Set(
    (d.details ?? []).flatMap(line => [
      line.debitAccountNumber,
      line.creditAccountNumber,
      line.discountAccountNumber,
    ].filter((n): n is string => !!n))
  )]

  // Resolve song song
  const resolutions = await Promise.all(
    accountNumbers.map(num => resolveAccountNumber(num).catch(() => null))
  )
  const accountIdMap = new Map<string, string>()
  accountNumbers.forEach((num, i) => {
    if (resolutions[i]) accountIdMap.set(num, resolutions[i]!.id)
  })

  return {
    // ...
    details: (d.details ?? []).map(line => ({
      // ...
      debitAccountNumber: line.debitAccountNumber ?? '',
      debitAccountId: line.debitAccountNumber
        ? (accountIdMap.get(line.debitAccountNumber) ?? '')
        : '',
      creditAccountNumber: line.creditAccountNumber ?? '',
      creditAccountId: line.creditAccountNumber
        ? (accountIdMap.get(line.creditAccountNumber) ?? '')
        : '',
    })),
  }
}, [resolveAccountNumber])
```

### 15.7 Kiểm Tra Interface Trước Khi Gửi ID

> **Trước khi dùng `debitAccountId`/`creditAccountId` trong payload, PHẢI kiểm tra request DTO đã có field đó chưa.**

```
B1: Kiểm tra interface request DTO (CreateXxxRequest / UpdateXxxRequest)
B2: Có field debitAccountId và creditAccountId trong details?
  ├── CÓ   → Tiếp tục, gửi payload với debitAccountId / creditAccountId
  └── KHÔNG → DỪNG LẠI, báo user:
              "Interface {TenDTO} chưa có debitAccountId/creditAccountId.
              Vui lòng yêu cầu BE bổ sung các field này vào request DTO."
              → Sau đó THÊM field optional vào types FE để chuẩn bị sẵn.
```

### 15.8 Checklist TK Từ Mã Hàng

- [ ] Hook có `resolveAccountNumber` dùng `TKApiService.list` (KHÔNG truyền `isActive`)
- [ ] `onChange` chọn mã hàng: xóa TK cũ, resolve async `returnAccountCode` → ID
- [ ] Chỉ set `debitAccountNumber` khi `debitAccountId` đã được resolve thành công
- [ ] Nếu resolve thất bại → để trống cả ID và number, KHÔNG hiển thị số ảo
- [ ] Combobox TK: `value={debitAccountId}`, `initialLabel={debitAccountNumber}`, `displayField='accountNumber'`
- [ ] Payload `buildCreatePayload`: CHỈ gửi `debitAccountId` / `creditAccountId`, KHÔNG gửi number
- [ ] `buildFormData`: resolve tất cả accountNumber → ID khi edit
- [ ] Interface DTO đã có `debitAccountId?` / `creditAccountId?` trong details
- [ ] Nếu DTO chưa có → báo user + thêm optional field vào types FE

---

## 9. File Tham Khảo

| File | Mô tả |
|------|-------|
| `src/modules/KetoanApp/features/nghiep-vu/tien-mat/phieu-thu/pages/PhieuThuPage.tsx` | Pattern chuẩn cho Phiếu thu |
| `src/modules/KetoanApp/features/nghiep-vu/tien-mat/phieu-chi/pages/PhieuChiPage.tsx` | Pattern chuẩn cho Phiếu chi |
| `src/modules/KetoanApp/features/nghiep-vu/tien-mat/phieu-thu/dialogs/PTDialog.tsx` | Dialog full-screen mẫu (Phiếu thu) |
| `src/modules/KetoanApp/features/nghiep-vu/tien-mat/phieu-thu/hooks/usePT.dlg.form.ts` | Hook form mẫu |
| `src/modules/KetoanApp/features/nghiep-vu/tien-gui/dialogs/TGFormDialog.tsx` | Dialog full-screen mẫu (Tiền gửi: thu/chi/chuyển nội bộ) |
| `src/modules/KetoanApp/features/nghiep-vu/tien-gui/phieu-chi/pages/TGChiPage.tsx` | Pattern chuẩn cho Tiền gửi phiếu chi |
| `src/shared/constants/table-settings.const.ts` | Định nghĩa `PT_ALL_COLUMNS`, `PC_ALL_COLUMNS` |
