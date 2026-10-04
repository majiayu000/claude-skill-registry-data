---
name: tao-master-page
description: 'Tạo hoặc chỉnh sửa Master Page trong KetoanApp. Dùng DmPageHeader + DmSearchToolbar + DmTable + DmTablePagination + DmRowActions. Hỗ trợ: bảng phẳng CRUD, bảng có cấu hình cột (TableSettingsPanel), bảng dữ liệu dạng cây (tree table với nút mở rộng/thu gọn). Đầu vào: danh sách field hiển thị, yêu cầu tạo mới hoặc sửa bảng có sẵn.'
---

# Tạo Master Page — SASUCO KetoanApp

> **Kế thừa:** `tao-ui-giao-dien-new` (foundation UI), `filter-phan-trang` (logic phân trang), `dat-ten` (quy tắc đặt tên).
> **Script kiểm tra:** `check-master-page.cjs` (từ `tao-ui-master-page`).

---

## 0. Font Chữ Toàn Cục — TUYỆT ĐỐI Không Ghi Đè

**Global font:** `Inter` (ưu tiên 1) → `InterVariable` → `"Noto Sans"` → `"Open Sans"` → `sans-serif`

> ⚠️ **QUAN TRỌNG:** Font được khai báo tập trung trong `src/styles/globals.css` trên `body` và `html`. **KHÔNG BAO GIỜ** set `font-family` riêng cho bất kỳ element nào trong bảng (`DmTable`, `DmTableHead`, `DmTableCell`, `th`, `td`, `input`, `button`). Tất cả element kế thừa font từ `body`.

**Nguyên nhân font trong bảng đôi khi khác:**
1. Tailwind v4 dùng `@theme` CSS thay vì `tailwind.config.js` — nếu `--font-sans` không được khai báo trong `@theme inline`, Tailwind fallback về `ui-sans-serif` (Segoe UI trên Windows) thay vì Inter.
2. `font-family` bị set cục bộ trên một component nào đó ghi đè global.

**Quy tắc:**
- ❌ **CẤM:** `className='font-sans'`, `style={{ fontFamily: '...' }}`, hoặc bất kỳ CSS `font-family` nào trên table/dialog/page
- ✅ **ĐÚNG:** Không set `font-family` — để element tự kế thừa từ `body`
- ✅ Nếu component bắt buộc cần font vì bị reset (vd: `button`, `input` trong một số browser): dùng `font-family: inherit`

---

## 1. Chọn Pattern Phù Hợp

Trước khi code, xác định loại bảng dựa trên yêu cầu:

| Pattern | Khi nào dùng | Đặc điểm |
|---------|-------------|----------|
| **A — CRUD cơ bản** | Danh mục ít cột (≤5), không cần cấu hình cột | `FIXED_COLS` + `useTableLayout` + `DmRowActions` |
| **B — CRUD có cấu hình cột** | Danh mục nhiều cột (>5), user cần ẩn/hiện/sắp xếp cột | `ALL_COLUMNS` + `useTableSettings` + `TableSettingsPanel` |
| **C — CRUD có action tùy chỉnh** | Cần thêm nút ngoài View/Edit/Clone/Delete | Button thủ công + `DropdownMenu` thay `DmRowActions` |
| **D — Bảng dữ liệu dạng cây** | Dữ liệu phân cấp (cha-con): Tài khoản, Đơn vị tổ chức | Tree hook + `ChevronDown`/`ChevronRight` + expand/collapse |

---

## 2. Cấu Trúc Chung Mọi Pattern

```
Page File (*Page.tsx)
├── PAGE_ID + PAGE_FEATURES                     ← metadata
├── COLUMNS / FIXED_COLS                        ← định nghĩa cột
├── CELL_VALUE / rowValue()                     ← render giá trị mỗi ô
├── CELL_CLASS / colClass()                     ← className mỗi ô
├── Component
│   ├── DmPageHeader                            ← tiêu đề + nút Thêm
│   ├── White Card (bg-white rounded-xl)
│   │   ├── DmSearchToolbar                     ← ô tìm kiếm + extraActions
│   │   ├── ── Header Table (shrink-0 overflow-hidden) ← CỐ ĐỊNH, không scroll dọc
│   │   ├── ── Body Table (flex-1 overflow-auto)      ← scroll dọc body
│   │   ├── ── Footer/Total Table (shrink-0)          ← CỐ ĐỊNH (nếu có)
│   │   └── DmTablePagination                   ← phân trang (luôn ở cuối)
│   ├── Ghost scrollbar (<div ref={ghostRef}>)  ← đồng bộ scroll ngang
│   ├── <FormDialog />                          ← dialog CRUD
│   └── <ConfirmDialog />                       ← xác nhận xóa
└── HOOK: use{Name}PageList()                   ← logic fetch + filter + pagination
```

### Layout chuẩn — Header cố định + Body scroll riêng

> ⚠️ **BẮT BUỘC:** Header bảng PHẢI được tách riêng ra ngoài vùng scroll dọc. Body nằm trong vùng `flex-1 overflow-auto`. Điều này đảm bảo header luôn hiển thị khi user scroll xuống dưới.
> **File tham khảo:** `PhieuThuPage.tsx`

```tsx
export default function XxxPage() {
  // Ref cho header scroll (để đồng bộ scroll ngang với body)
  const headerScrollRef = useRef<HTMLDivElement>(null)

  // Wrap onTableScroll để đồng bộ scroll ngang cho header
  const handleTableScroll = useCallback(() => {
    onTableScroll()
    const sl = tableRef.current?.scrollLeft ?? 0
    if (headerScrollRef.current) headerScrollRef.current.scrollLeft = sl
  }, [onTableScroll])

  return (
    <div className='bg-[#e8ecf1] flex flex-col gap-1 h-full'>
      <DmPageHeader title='...' description='...' actions={<Button>Thêm</Button>} />

      <div className='flex-1 min-h-0 px-3 md:px-6 pb-3'>
        <div className='h-full flex flex-col bg-white rounded-xl overflow-hidden'>

          {/* Search / BulkActionBar */}
          {selection.selectedCount > 0 ? (
            <BulkActionBar ... />
          ) : (
            <DmSearchToolbar search={...} onSearchChange={...} extraActions={...} />
          )}

          {/* ── Header bảng — CỐ ĐỊNH trên, nằm NGOÀI vùng scroll dọc ── */}
          <div ref={headerScrollRef} className='shrink-0 overflow-hidden'>
            <DmTable style={{ minWidth: minTableWidth }}>
              {/* colgroup — BẮT BUỘC: đồng bộ column width giữa header và body table.
                  Nếu thiếu → tableLayout:fixed tính width từ row đầu tiên mỗi bảng → lệch cột. */}
              <colgroup>
                <col style={{ width: 40 }} />
                {colsForRender.map(col => {
                  const w = getColumnWidth(col.id, col.width)
                  return <col key={col.id} style={{ width: w }} />
                })}
                <col style={{ width: 0 }} />
              </colgroup>
              <DmTableHeader>
                <DmTableHeaderRow>
                  {/* Checkbox */}
                  <DmTableHead className='w-10 text-center sticky left-0 z-30 bg-[#f0f2f6]'
                    style={{ width: 40, minWidth: 40 }}>
                    <input type='checkbox' ... />
                  </DmTableHead>

                  {/* Các cột dữ liệu — dùng getColumnWidth + onResizeMouseDown */}
                  {colsForRender.map(col => {
                    const w = getColumnWidth(col.id, col.width)
                    return (
                    <DmTableHead
                      key={col.id}
                      pinned={col.pinned === 'left' || col.pinned === 'right'}
                      onResizeMouseDown={(e) => handleResizeStart(col.id, e)}
                      style={{ width: w, minWidth: w,
                        ...(col.stickyLeft !== undefined ? { left: col.stickyLeft } : {}),
                        ...(col.stickyRight !== undefined ? { right: col.stickyRight } : {}),
                      }}
                      className={cn(
                        col.stickyLeft !== undefined && 'sticky z-30 bg-[#f0f2f6]',
                        col.stickyRight !== undefined && 'sticky z-30 bg-[#f0f2f6]',
                        col.pinned === 'left' && 'shadow-[2px_0_4px_-2px_rgba(0,0,0,0.12)]',
                        col.pinned === 'right' && 'shadow-[-2px_0_4px_-2px_rgba(0,0,0,0.12)]',
                      )}
                    >
                      {col.displayName ?? col.title}
                    </DmTableHead>
                    )
                  })}

                  {/* Ghost action column */}
                  <DmTableHead className='sticky right-0 z-30 bg-[#f0f2f6]'
                    style={{ width: 0, minWidth: 0, padding: 0, border: 'none' }} />
                </DmTableHeaderRow>
              </DmTableHeader>
            </DmTable>
          </div>

          {/* ── Vùng body — scroll dọc ── */}
          <div ref={tableRef} className='flex-1 min-h-0 overflow-auto scrollbar-hidden' onScroll={handleTableScroll}>
            <DmTable style={{ minWidth: minTableWidth }}>
              {/* colgroup — BẮT BUỘC: phải giống hệt header table để đồng bộ column width */}
              <colgroup>
                <col style={{ width: 40 }} />
                {colsForRender.map(col => {
                  const w = getColumnWidth(col.id, col.width)
                  return <col key={col.id} style={{ width: w }} />
                })}
                <col style={{ width: 0 }} />
              </colgroup>
              <DmTableBody>
                {/* Loading / Empty / Rows */}
                {items.map(item => (
                  <DmTableRow key={item.id} className='group' onDoubleClick={() => handleEdit(item)}>
                    {/* Checkbox sticky left */}
                    <DmTableCell className='text-center sticky left-0 z-20 bg-white group-hover:bg-gray-50'
                      style={{ width: 40, minWidth: 40 }}>
                      <input type='checkbox' ... />
                    </DmTableCell>

                    {colsForRender.map(col => {
                      const w = getColumnWidth(col.id, col.width)
                      return (
                      <DmTableCell key={col.id}
                        style={{ width: w,
                          ...(col.stickyLeft !== undefined ? { left: col.stickyLeft } : {}),
                          ...(col.stickyRight !== undefined ? { right: col.stickyRight } : {}),
                        }}
                        className={cn(
                          CELL_CLASS[col.field] ?? 'text-black',
                          col.stickyLeft !== undefined && 'sticky z-20 bg-white group-hover:bg-gray-50',
                          col.stickyRight !== undefined && 'sticky z-20 bg-white group-hover:bg-gray-50',
                        )}
                      >
                        {(CELL_VALUE[col.field] ?? (() => ''))(item)}
                      </DmTableCell>
                      )
                    })}

                    {/* Ghost action column */}
                    <DmTableCell className='sticky right-0 z-20 bg-transparent'
                      style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
                      <div className='absolute right-0 top-0 bottom-0 flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-12 pr-2'>
                        <DmRowActions actions={getRowActions(item)} />
                      </div>
                    </DmTableCell>
                  </DmTableRow>
                ))}
              </DmTableBody>
            </DmTable>
          </div>

          {/* ── Footer / Tổng cộng — CỐ ĐỊNH dưới (nếu có) ── */}
          {/* <div ref={totalScrollRef} className='shrink-0 overflow-hidden border-t-2 border-[#ced1d6]'>
            <DmTable style={{ minWidth: minTableWidth }}>...</DmTable>
          </div> */}

          {/* Pagination */}
          <DmTablePagination ... />

          {/* Ghost scrollbar */}
          <div ref={ghostRef} className='overflow-x-auto shrink-0' onScroll={onGhostScroll}>
            <div style={{ minWidth: minTableWidth, height: 1 }} />
          </div>
        </div>
      </div>

      {/* Dialogs NGOÀI CardContent */}
      <XxxFormDialog ... />
      <ConfirmDialog ... />
    </div>
  )
}
```

### Cấu trúc thẻ div — 3 tầng bảng

| Tầng | Class | Mục đích |
|------|-------|----------|
| **Header** | `shrink-0 overflow-hidden` | Cố định trên, không scroll dọc. Scroll ngang đồng bộ qua `headerScrollRef` |
| **Body** | `flex-1 min-h-0 overflow-auto scrollbar-hidden` | Scroll dọc, chiếm toàn bộ không gian còn lại |
| **Footer** | `shrink-0 overflow-hidden` | Cố định dưới (hàng tổng cộng phiếu thu/chi). Scroll ngang đồng bộ qua `totalScrollRef` |

> **Tất cả 3 tầng dùng CHUNG `minTableWidth`** để đảm bảo độ rộng cột đồng bộ. Scroll ngang được đồng bộ qua callback `handleTableScroll`.

### 2.1 Row Double-Click → Mở Edit (BẮT BUỘC)

**TẤT CẢ** các master page phải có `onDoubleClick` trên `DmTableRow` để mở form chỉnh sửa:

```tsx
<DmTableRow
  key={item.id}
  data-qa='xxx-row'
  className="group"
  onDoubleClick={() => handleEdit(item)}   // ← BẮT BUỘC
>
```

**Quy tắc:**
- Double-click vào bất kỳ row nào → mở form **Edit** (giống như click nút Sửa)
- Với pattern `useDmRowActions`: inline logic giống `onEdit`
  ```tsx
  onDoubleClick={() => { setSelectedItem(item); setDialogOpen(true) }}
  ```
- Với pattern Button thủ công: gọi trực tiếp hàm `handleEdit`
  ```tsx
  onDoubleClick={() => handleEdit(item)}
  ```
- Với bảng cây (Pattern D): gọi `onRowDoubleClick` đã định nghĩa sẵn trong page
  ```tsx
  onDoubleClick={() => onRowDoubleClick(item)}
  ```

### 2.1a Click Vào Cột Định Danh → Mở View (BẮT BUỘC)

> **Reference implementation:** `PhieuThuPage.tsx` — tham khảo cách làm chuẩn.

**TẤT CẢ** các master page phải cho phép **click chuột trái** vào cột định danh (mã, số chứng từ, số tài khoản...) để mở dialog **xem chi tiết** (View mode). Đây là hành vi bổ sung cho double-click (mở Edit).

#### Cột định danh theo loại trang

| Loại trang | Cột định danh | Ví dụ |
|-----------|--------------|-------|
| **Nghiệp vụ** (phiếu thu/chi, mua/bán, kho...) | `refNo`, `refNoManagement`, `invoiceNumber`, `voucherCode`, `returnNo`, `returnCode`, `discountNo`, `discountCode`, `orderNo`, `orderCode` | `PT-2024-001` |
| **Danh mục** (khách hàng, NCC, hàng hóa, nhân viên, kho, tiền tệ...) | `code` | `KH001`, `NCC002` |
| **Đơn vị tính** | `name` (không có `code`) | `Chiếc`, `Cái` |
| **Tài khoản** | `accountNumber` | `1111` |

#### Pattern A: Trang nghiệp vụ (dùng `getCellClass` + `dialogOpen`/`dialogMode`/`selectedId`)

```tsx
// ── Bước 1: Thêm cursor-pointer hover:underline vào getCellClass ──
const getCellClass = (field: string, _item?: ReceiptDto) => {
  if (field === 'refNo') return 'text-[#1B6FC8] font-medium cursor-pointer hover:underline'
  // ...
}

// ── Bước 2: Trong render cell, thêm nhánh clickable span ──
// (đặt SAU badge check, TRƯỚC CELL_VALUE fallback)
{col.field === 'refNo' ? (
  <span
    className='cursor-pointer hover:underline'
    onClick={(e) => { e.stopPropagation(); setSelectedId(item.id); setDialogMode('view'); setDialogOpen(true) }}
    data-qa={`link_refNo_${item.id}`}
  >
    {item.refNo || ''}
  </span>
) : col.field === 'refNoManagement' ? (
  <span
    className='cursor-pointer hover:underline'
    onClick={(e) => { e.stopPropagation(); setSelectedId(item.id); setDialogMode('view'); setDialogOpen(true) }}
    data-qa={`link_refNoManagement_${item.id}`}
  >
    {item.refNoManagement || ''}
  </span>
) : badge_fields.includes(col.field) ? (
  // badge rendering...
) : (
  // CELL_VALUE fallback
  (CELL_VALUE[col.field] ?? (() => ''))(item)
)}
```

> ⚠️ **Quan trọng:** Dùng `e.stopPropagation()` để tránh trigger `onDoubleClick` của row.

#### Pattern B: Trang danh mục (dùng `CELL_CLASS` + `selectedItem`)

```tsx
// ── Bước 1: Thêm cursor-pointer hover:underline vào CELL_CLASS ──
const CELL_CLASS: Record<string, string> = {
  code: 'font-medium text-blue-700 cursor-pointer hover:underline',
  name: 'font-medium text-black uppercase',
}

// ── Bước 2: Trong render cell, bọc span clickable cho cột code ──
{col.field === 'code' ? (
  <span
    className='cursor-pointer hover:underline'
    onClick={(e: React.MouseEvent) => { e.stopPropagation(); setSelectedItem(item); setDialogOpen(true) }}
    data-qa={`link_code_${item.id}`}
  >
    {item.code || ''}
  </span>
) : (
  (CELL_VALUE[col.field] ?? (() => ''))(item)
)}
```

#### Pattern C: Bảng cây (Tài khoản) — custom Table

```tsx
// ── Bọc accountNumber trong span clickable ──
<span
  className='font-mono text-[#1B6FC8] cursor-pointer hover:underline'
  onClick={(e) => { e.stopPropagation(); openView(item) }}
  data-qa={`link_accountNumber_${item.id}`}
>
  {item.accountNumber}
</span>
```

#### Pattern D: Đơn vị tính (dùng `name` làm định danh)

```tsx
// ── CELL_CLASS ──
name: 'text-black cursor-pointer hover:underline',

// ── Render cell ──
{col.field === 'name' ? (
  <span
    className='cursor-pointer hover:underline'
    onClick={(e: React.MouseEvent) => { e.stopPropagation(); handleEdit(item) }}
    data-qa={`link_name_${item.id}`}
  >
    {(CELL_VALUE[col.field] ?? (() => ''))(item)}
  </span>
) : (
  (CELL_VALUE[col.field] ?? (() => ''))(item)
)}
```

#### Màu chuẩn cho cột định danh

| Màu | Class |
|-----|-------|
| Xanh primary | `text-[#1B6FC8]` (nghiệp vụ) hoặc `text-blue-700` (danh mục) |
| Font weight | `font-medium` |
| Hover | `hover:underline` |
| Con trỏ | `cursor-pointer` |

#### Checklist áp dụng

- [ ] Xác định cột định danh của trang (refNo/code/accountNumber/name)
- [ ] Cập nhật `getCellClass` hoặc `CELL_CLASS`: thêm `cursor-pointer hover:underline`
- [ ] Thêm conditional render span clickable trong cell
- [ ] `e.stopPropagation()` để không trigger double-click row
- [ ] `data-qa` format: `link_{fieldName}_{item.id}`
- [ ] Gọi đúng handler: `setSelectedId`+`setDialogMode('view')` cho nghiệp vụ, `setSelectedItem` cho danh mục
- [ ] Nếu trang chưa có `onDoubleClick` → bổ sung luôn (xem Section 2.1)

### 2.2 Dialog Dùng Chung Cho Cả Tạo & Sửa (BẮT BUỘC)

**Nguyên tắc cốt lõi:** Tạo và Sửa dùng **CÙNG MỘT dialog component**. Không tạo 2 dialog riêng biệt.

Điểm khác biệt duy nhất giữa Tạo và Sửa:
| | Tạo (Create) | Sửa (Edit) |
|---|---|---|
| `mode` | `'create'` | `'edit'` |
| `initialData` | `null` | item được chọn |
| Form hiển thị | Form trống | Form được fill sẵn data |

```tsx
// ✅ ĐÚNG: 1 dialog, 2 mode
const [dialogOpen, setDialogOpen] = useState(false)
const [selectedItem, setSelectedItem] = useState<XxxDto | null>(null)
const [cloneFrom, setCloneFrom] = useState<XxxDto | null>(null)

function handleCreate()              { setSelectedItem(null); setCloneFrom(null); setDialogOpen(true) }
function handleEdit(item: XxxDto)    { setSelectedItem(item); setCloneFrom(null); setDialogOpen(true) }
function handleClone(item: XxxDto)   { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) }

// JSX: chỉ 1 dialog duy nhất
<XxxFormDialog
  open={dialogOpen}
  onOpenChange={setDialogOpen}
  initialData={selectedItem}
  cloneFrom={cloneFrom}
  onSuccess={refetch}
/>
```

```tsx
// ❌ SAI: 2 dialog riêng cho Tạo và Sửa
<XxxCreateDialog ... />
<XxxEditDialog ... />
```

**Trong dialog component**, dùng `mode` để phân biệt:
- `mode === 'create'` → gọi API `create()`, form rỗng
- `mode === 'edit'`   → gọi API `update()`, form fill từ `initialData`

#### ⚠️ Map DTO → FormState — Tránh `as unknown as`

**🚫 TUYỆT ĐỐI CẤM** dùng `item as unknown as FormState` khi truyền data từ row vào dialog Edit.

**Lý do:** Tên field giữa DTO (API response) và FormState (dialog form) thường **khác nhau**. Ép kiểu `as unknown as` không map field → form hiển thị sai hoặc thiếu data.

**Ví dụ lỗi phổ biến:**
| DTO field | FormState field | `as unknown as`? |
|-----------|----------------|-------------------|
| `debitAmount` | `totalDebit` | ❌ Sai — form nhận `undefined` |
| `creditAmount` | `totalCredit` | ❌ Sai — form nhận `undefined` |
| `customerCode` | `objectCode` | ❌ Sai — form nhận `undefined` |

**Pattern đúng — Map thủ công từng field:**

```tsx
// ✅ ĐÚNG: Map từng field từ DTO → FormState
function handleEdit(item: XxxDto) {
  setDialogMode('edit')
  setDialogData({
    id: item.id,
    refDate: item.refDate?.slice(0, 10) ?? '',
    // Map tên field khác nhau
    totalDebit: item.debitAmount,        // ← DTO debitAmount → FormState totalDebit
    totalCredit: item.creditAmount,      // ← DTO creditAmount → FormState totalCredit
    objectCode: item.customerCode,       // ← DTO customerCode → FormState objectCode
    objectName: item.customerName,       // ← DTO customerName → FormState objectName
    // Các field cùng tên có thể spread
    accountNumber: item.accountNumber,
    description: item.description,
  } as XxxFormState)
  setDialogOpen(true)
}
```

```tsx
// ❌ SAI: Ép kiểu không map field — totalDebit sẽ là undefined!
function handleEdit(item: XxxDto) {
  setDialogData(item as unknown as XxxFormState)  // ← KHÔNG map field!
  setDialogOpen(true)
}
```

**Quy tắc:**
- Luôn kiểm tra tên field giữa DTO và FormState
- Nếu khác tên → map thủ công
- Nếu cùng tên và cùng kiểu → có thể spread
- Viết comment mapping cho từng field khác tên (vd: `// ← DTO debitAmount → FormState totalDebit`)

> Xem chi tiết pattern Edit/Nhân bản trong memory `edit-form-pattern.md`.

### 2.3 Cột Thao Tác — Ghost Column (BẮT BUỘC)

**🚫 CẤM:** Tạo cột "Thao tác" hiển thị luôn (có header text + width cụ thể như `action: 120`).

**✅ BẮT BUỘC:** Dùng **ghost column** (width: 0, sticky right) — action button CHỈ hiện khi hover row:

```tsx
{/* Header: cột ảo width=0, không text */}
<DmTableHead className='sticky right-0 z-30 bg-[#ECEDEF]'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none' }} />

{/* Body: cột ảo chứa action nổi khi hover */}
<DmTableCell className='sticky right-0 z-20 bg-transparent'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-16 pr-2'>
    {/* Button hoặc DmRowActions */}
  </div>
</DmTableCell>
```

**Quy tắc:**
- Header ghost **KHÔNG** có text "Thao tác" — để trống, width=0
- Body ghost dùng `group` + `group-hover:opacity-100` → chỉ hiện khi hover row
- `colSpan` cho loading/empty **KHÔNG** tính cột ghost (vd: 5 cột data → colSpan=5)
- Cần `className='group'` trên `DmTableRow` để hover trigger hoạt động

**Lý do:** Ghost column tiết kiệm không gian, giao diện sạch hơn, đồng bộ với tất cả master page khác.

---

## 3. Pattern A — CRUD Cơ Bản (VD: Khoản mục chi phí)

> File tham khảo: `src/modules/KetoanApp/features/danh-muc/khoan-muc-chi-phi/pages/KhoanMucChiPhiPage.tsx`

### 3.1 Định nghĩa cột

```tsx
import type { ColumnSetting } from '@/shared/hooks/useTableSettings'

/** Cột cố định — không cho user tùy chỉnh */
const FIXED_COLS = [
  { id: 'code',        field: 'code',        title: 'Mã ...',      visible: true, width: 200, order: 0, pinned: null },
  { id: 'name',        field: 'name',        title: 'Tên ...',     visible: true, width: 320, order: 1, pinned: null },
  { id: 'description', field: 'description', title: 'Diễn giải',   visible: true, width: 300, order: 2, pinned: null },
  { id: 'isActive',    field: 'isActive',    title: 'Trạng thái',  visible: true, width: 120, order: 3, pinned: null },
] as const
```

### 3.2 Render giá trị & class

```tsx
// Cách 1: switch function (đơn giản)
// ⚠️ Giá trị rỗng (null/undefined/'') → hiển thị chuỗi rỗng '', KHÔNG dùng '-'
// ⚠️ Text dài → dùng CSS truncate (class 'truncate'), không cắt bằng JS
const rowValue = (item: XxxDto, field: string): string => {
  switch (field) {
    case 'code':     return item.code || ''
    case 'name':     return item.name || ''
    case 'description': return item.description || ''  // text dài → để CSS truncate xử lý
    case 'isActive': return item.isActive ? 'Đang dùng' : 'Ngừng dùng'
    default:         return ''
  }
}

const colClass = (field: string): string => {
  if (field === 'code' || field === 'name') return 'text-black truncate'
  if (field === 'description') return 'text-black truncate'  // ← text dài: truncate + title
  if (field === 'isActive') return 'text-center'
  return 'text-black'
}

// Cách 2: lookup object (dùng khi cần dùng lại cho export Excel)
const CELL_VALUE: Record<string, (item: XxxDto) => string> = {
  code:     (i) => i.code || '',
  name:     (i) => i.name || '',
  description: (i) => i.description || '',
  isActive: (i) => i.isActive ? 'Đang dùng' : 'Ngừng dùng',
}
const CELL_CLASS: Record<string, string> = {
  code: 'text-blue-700 font-medium cursor-pointer hover:underline truncate',
  name: 'text-black truncate',
  description: 'text-black truncate',
}
```

### 3.2a Quy tắc hiển thị text trong ô bảng

**Giá trị rỗng → để trống:**
- Khi field `null`, `undefined`, hoặc `''` → trả về `''` (chuỗi rỗng), KHÔNG dùng `'-'`
- Pattern: `item.code || ''` (không phải `item.code || '-'`)

**Text dài → CSS truncate (ellipsis `....`):**
- Thêm class `truncate` vào `DmTableCell` cho các cột có thể chứa text dài (code, name, description...)
- Thêm `title={fullText}` vào element chứa text để hiển thị tooltip khi hover
- KHÔNG cắt text bằng JS — để CSS `text-overflow: ellipsis` xử lý

```tsx
// ✅ ĐÚNG: truncate + title cho tooltip
<DmTableCell className={cn('truncate', colClass(col.field))} title={rowValue(item, col.field)}>
  {rowValue(item, col.field)}
</DmTableCell>

// ❌ SAI: cắt text bằng JS
<DmTableCell>{item.description?.slice(0, 50) + '...'}</DmTableCell>
```

### 3.3 Dùng `useTableLayout` để tính layout

```tsx
import { useTableLayout } from '@/shared/hooks'

const { colsForRender, minTableWidth, colSpanAll, tableRef, ghostRef, onTableScroll, onGhostScroll }
  = useTableLayout(FIXED_COLS as any)
```

- `colsForRender` — các cột sau khi tính sticky offset
- `minTableWidth` — tổng chiều rộng tối thiểu bảng
- `colSpanAll` — số cột colspan cho loading/empty (checkbox + data + ghost action)

### 3.4 Row Actions với `useDmRowActions`

```tsx
import { useDmRowActions } from '@/shared/hooks'

const getRowActions = useDmRowActions<XxxDto>({
  canView:  true,                                          // mặc định true
  canEdit:  true,
  canClone: true,
  canDelete: true,
  onView:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onEdit:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onClone:  (item) => { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) },
  onDelete: (item) => { setDeleteItem(item); setDeleteOpen(true) },
  // extraActions: (item) => [{ icon: ..., label: ..., variant: ..., onClick: ... }]
})
```

### 3.5 Bảng (DmTable)

```tsx
<DmTable style={{ minWidth: minTableWidth }} data-qa='tbl_danh_sach'>
  <DmTableHeader>
    <DmTableHeaderRow>
      {/* Checkbox cột đầu */}
      <DmTableHead className='w-10 text-center sticky left-0 z-30 bg-[#ECEDEF]'
        style={{ width: 40, minWidth: 40 }}>
        <input type='checkbox' ... />
      </DmTableHead>

      {/* Các cột dữ liệu */}
      {colsForRender.map(col => (
        <DmTableHead key={col.id} style={{ width: col.width, minWidth: col.width }}>
          {col.displayName ?? col.title}
        </DmTableHead>
      ))}

      {/* Cột ảo sticky phải (width=0, chứa action nổi khi hover) */}
      <DmTableHead className='sticky right-0 z-30 bg-[#ECEDEF]'
        style={{ width: 0, minWidth: 0, padding: 0, border: 'none' }} />
    </DmTableHeaderRow>
  </DmTableHeader>

  <DmTableBody>
    {loading ? (
      <DmTableRow><DmTableCell colSpan={colSpanAll} className='text-center py-12 text-gray-400'>Đang tải...</DmTableCell></DmTableRow>
    ) : items.length === 0 ? (
      <DmTableRow><DmTableCell colSpan={colSpanAll} className='text-center py-12 text-gray-400'>Không có dữ liệu</DmTableCell></DmTableRow>
    ) : items.map(item => (
      <DmTableRow key={item.id} data-qa='xxx-row' className='group' onDoubleClick={() => { setSelectedItem(item); setDialogOpen(true) }}>
        {/* Checkbox */}
        <DmTableCell className='text-center sticky left-0 z-20 bg-white group-hover:bg-gray-50'
          style={{ width: 40, minWidth: 40 }}>
          <input type='checkbox' ... />
        </DmTableCell>

        {/* Data cells */}
        {colsForRender.map(col => (
          <DmTableCell key={col.id} style={{ width: col.width }}
            className={cn(colClass(col.field))}>
            {rowValue(item, col.field)}
          </DmTableCell>
        ))}

        {/* Ghost action column */}
        <DmTableCell className='sticky right-0 z-20 bg-transparent'
          style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
          <div className='absolute right-0 top-0 bottom-0 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-16 pr-2'>
            <DmRowActions actions={getRowActions(item)} />
          </div>
        </DmTableCell>
      </DmTableRow>
    ))}
  </DmTableBody>
</DmTable>
```

### 3.6 Trạng thái hiển thị

```tsx
<span className={cn(
  'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
  item.isActive
    ? 'bg-green-50 text-green-700 border border-green-200'
    : 'bg-red-50 text-red-700 border border-red-200'
)}>
  {item.isActive ? 'Đang sử dụng' : 'Ngừng sử dụng'}
</span>
```

---

## 4. Pattern B — CRUD Có Cấu Hình Cột (VD: Nhân viên)

> File tham khảo: `src/modules/KetoanApp/features/danh-muc/nhan-vien/pages/NhanVienPage.tsx`
> ALL_COLUMNS: `src/shared/constants/table-settings.const.ts`

### 4.1 Khai báo ALL_COLUMNS

```tsx
// Trong src/shared/constants/table-settings.const.ts
import type { ColumnSetting } from '@/shared/hooks/useTableSettings'

export const NV_ALL_COLUMNS: ColumnSetting[] = [
  { id: 'code',         field: 'code',         title: 'Mã nhân viên',     visible: true,  width: 150, order: 0,  pinned: null },
  { id: 'name',         field: 'name',         title: 'Tên nhân viên',    visible: true,  width: 220, order: 1,  pinned: null },
  { id: 'department',   field: 'department',   title: 'Phòng ban',        visible: true,  width: 180, order: 2,  pinned: null },
  { id: 'position',     field: 'position',     title: 'Chức vụ',          visible: true,  width: 180, order: 3,  pinned: null },
  { id: 'phone',        field: 'phone',        title: 'Số điện thoại',    visible: true,  width: 150, order: 4,  pinned: null },
  { id: 'email',        field: 'email',        title: 'Email',            visible: false, width: 200, order: 5,  pinned: null },
  { id: 'address',      field: 'address',      title: 'Địa chỉ',          visible: false, width: 250, order: 6,  pinned: null },
]
// defaultVisibleCount=5 → 5 cột đầu visible, còn lại ẩn
```

### 4.2 Dùng `useTableSettings`

```tsx
import { useTableSettings } from '@/shared/hooks'
import { TableSettingsPanel } from '@/shared/components/table-settings'
import { Settings } from 'lucide-react'
import { NV_ALL_COLUMNS } from '@/shared/constants/table-settings.const'

const { columns, visibleColumns, saveSettings, restoreDefaults }
  = useTableSettings({ tableId: 'employee', allColumns: NV_ALL_COLUMNS, defaultVisibleCount: 5 })

const { colsForRender, ... } = useTableLayout(visibleColumns)  // ← dùng visibleColumns

// Nút cài đặt trong extraActions của DmSearchToolbar:
const [settingsOpen, setSettingsOpen] = useState(false)

<Button variant='ghost' size='sm'
  className='h-8 w-8 p-0 text-gray-500 hover:text-gray-700 hover:bg-gray-100'
  onClick={() => setSettingsOpen(true)} title='Cài đặt bảng'>
  <Settings className='h-4 w-4' />
</Button>

<TableSettingsPanel
  open={settingsOpen}
  onOpenChange={setSettingsOpen}
  columns={columns}
  onSave={saveSettings}
  onRestoreDefaults={restoreDefaults}
/>
```

> ⚠️ `useTableLayout` nhận `visibleColumns` (đã filter+sort), **KHÔNG** nhận `columns` (đầy đủ).

---

## 5. Pattern C — CRUD Có Action Tùy Chỉnh (VD: Ngân hàng)

> File tham khảo: `src/modules/KetoanApp/features/danh-muc/ngan-hang/pages/NganHangPage.tsx`

Khi cần action ngoài View/Edit/Clone/Delete (vd: ToggleActive, Export riêng), dùng Button thủ công + `DropdownMenu` thay vì `DmRowActions`:

```tsx
{/* Ghost action column — Button thủ công */}
<DmTableCell className='sticky right-0 z-20 bg-transparent'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-16 pr-2'>
    <Button variant='ghost' size='sm' className='icon-warning border rounded-lg bg-white'
      title='Sửa' data-qa={`btn_sua_${item.id}`} onClick={() => handleEdit(item)}>
      <Pencil className='h-4 w-4' />
    </Button>
    <Button variant='ghost' size='sm' className='icon-danger border rounded-lg bg-white'
      title='Xóa' data-qa={`btn_xoa_${item.id}`} onClick={() => handleDeleteRow(item)}>
      <Trash2 className='h-4 w-4' />
    </Button>
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' size='sm' className='border rounded-lg bg-white'
          title='Chức năng khác' data-qa={`btn_khac_${item.id}`}>
          <MoreHorizontal className='h-4 w-4' />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' className='w-40'>
        <DropdownMenuItem onSelect={() => handleClone(item)} data-qa={`btn_nhan_ban_${item.id}`}>
          <Copy className='h-4 w-4' /> Nhân bản
        </DropdownMenuItem>
        <DropdownMenuItem onSelect={async () => { await handleToggleActive(...); refetch() }}>
          {item.isActive ? <><Ban className='h-4 w-4' />Ngừng sử dụng</> : <><CheckCircle className='h-4 w-4' />Kích hoạt</>}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </div>
</DmTableCell>
```

> ⚠️ Khi dùng Button thủ công trong ghost column, **phải** thêm `border rounded-lg bg-white` để đồng bộ style với `DmRowActions`.

---

## 6. Pattern D — Bảng Dữ Liệu Dạng Cây (Tree Table)

> File tham khảo:
> - `src/modules/KetoanApp/features/danh-muc/don-vi-to-chuc/pages/DonViToChucPage.tsx` (DmTable)
> - `src/modules/KetoanApp/features/danh-muc/tai-khoan/pages/TaiKhoanPage.tsx` (shadcn Table)
> - Hook cây: `useDVTC.tree.ts`, `useTK.tree.ts`

### 6.1 Đặc điểm bảng cây

| Đặc điểm | Mô tả |
|----------|-------|
| Dữ liệu | API trả về dạng cây lồng (`children[]`) hoặc danh sách phẳng có `parentId` |
| Cột đầu tiên | Có nút `ChevronRight`/`ChevronDown` để mở rộng/thu gọn, indent theo `depth * 20px` |
| Search bar | Có thêm nút **Mở rộng tất cả / Thu gọn tất cả** (`SquarePlus`/`SquareMinus`) ở `extraActions` |
| Tổng số | Hiển thị số node trong cây (đệ quy), bên dưới bảng |
| Phân trang | **KHÔNG có** — hiển thị toàn bộ cây |
| Checkbox | Thường không có (trừ khi có yêu cầu đặc biệt) |

### 6.2 Hook cây (Tree Hook)

Hook cây có 2 kiểu tùy theo API:

**Kiểu A — API trả thẳng cây (`getTree()`):**

```ts
// useXxxTree.ts
import { useState, useEffect, useCallback, useMemo } from 'react'
import { useDebounce } from '@/shared/hooks/useDebounce'
import type { XxxDto } from '../types'
import { XxxApiService } from '../services'

export interface XxxTreeRow {
  node: XxxDto
  depth: number
  hasChildren: boolean
  expanded: boolean
}

function countNodes(nodes: XxxDto[]): number {
  return nodes.reduce((sum, n) => sum + 1 + (n.children ? countNodes(n.children) : 0), 0)
}

function collectIds(nodes: XxxDto[], out: Set<string>): void {
  for (const node of nodes) {
    out.add(node.id)
    if (node.children?.length) collectIds(node.children, out)
  }
}

function filterTree(nodes: XxxDto[], predicate: (n: XxxDto) => boolean): XxxDto[] {
  const result: XxxDto[] = []
  for (const node of nodes) {
    const children = node.children ? filterTree(node.children, predicate) : []
    if (predicate(node) || children.length > 0) {
      result.push({ ...node, children })
    }
  }
  return result
}

function flattenTree(
  nodes: XxxDto[], depth: number, expanded: Set<string>,
  forceExpand: boolean, out: XxxTreeRow[]
): void {
  for (const node of nodes) {
    const hasChildren = !!node.children?.length
    const isExpanded = forceExpand || expanded.has(node.id)
    out.push({ node, depth, hasChildren, expanded: isExpanded })
    if (hasChildren && isExpanded) {
      flattenTree(node.children!, depth + 1, expanded, forceExpand, out)
    }
  }
}

export function useXxxTree() {
  const [tree, setTree] = useState<XxxDto[]>([])
  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [search, setSearch] = useState('')
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  const debouncedSearch = useDebounce(search, 800)

  const fetchData = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true); else setLoading(true)
    try {
      const res = await XxxApiService.getTree()
      if (res.success && res.data) {
        setTree(res.data)
        const ids = new Set<string>()
        collectIds(res.data, ids)
        setExpanded(ids)
      }
    } catch { /* apiCall tự log */ }
    finally { setLoading(false); setRefreshing(false) }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const isFiltering = !!debouncedSearch

  const filteredTree = useMemo(() => {
    if (!isFiltering) return tree
    const kw = debouncedSearch.trim().toLowerCase()
    return filterTree(tree, node =>
      (node.code?.toLowerCase().includes(kw)) ||
      (node.name?.toLowerCase().includes(kw))
    )
  }, [tree, isFiltering, debouncedSearch])

  const rows = useMemo(() => {
    const out: XxxTreeRow[] = []
    flattenTree(filteredTree, 0, expanded, isFiltering, out)
    return out
  }, [filteredTree, expanded, isFiltering])

  const totalCount = useMemo(() => countNodes(filteredTree), [filteredTree])

  const toggleExpand = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id); else next.add(id)
      return next
    })
  }

  const expandAll = useCallback(() => {
    const ids = new Set<string>()
    collectIds(tree, ids)
    setExpanded(ids)
  }, [tree])

  const collapseAll = useCallback(() => setExpanded(new Set()), [])

  return {
    rows, totalCount, loading, refreshing,
    search, setSearch,
    toggleExpand, expandAll, collapseAll,
    handleRefresh: () => fetchData(true),
    refetch: () => fetchData(),
  }
}
```

**Kiểu B — API trả danh sách phẳng, tự dựng cây (`getAll()` + `buildTree`):**

Thêm hàm `buildTree()` vào hook:

```ts
function buildTree(items: XxxDto[]): XxxDto[] {
  const map = new Map<string, XxxDto>()
  const roots: XxxDto[] = []
  for (const item of items) {
    map.set(item.id, { ...item, children: [] })
  }
  for (const item of items) {
    const node = map.get(item.id)!
    if (item.parentId && map.has(item.parentId)) {
      map.get(item.parentId)!.children!.push(node)
    } else if (!item.parentId) {
      roots.push(node)
    }
  }
  return roots
}

// Trong fetchData:
const res = await XxxApiService.getAll()
if (res.success && res.data) {
  const treeData = buildTree(res.data.items)
  setTree(treeData)
  // ...
}
```

### 6.3 Search Toolbar Với Nút Mở Rộng/Thu Gọn

```tsx
const [treeExpanded, setTreeExpanded] = useState(true)

<DmSearchToolbar
  search={search}
  onSearchChange={setSearch}
  placeholder='Tìm kiếm theo mã, tên...'
  extraActions={
    <>
      {/* Nút Làm mới */}
      <Button variant='ghost' size='sm'
        className='h-8 w-8 p-0 text-gray-500 hover:text-gray-700 hover:bg-gray-100'
        onClick={handleRefresh} disabled={refreshing} title='Làm mới'
        data-qa='btn_lam_moi'>
        <RefreshCw className={cn('h-4 w-4', refreshing && 'animate-spin')} />
      </Button>

      {/* Nút Mở rộng / Thu gọn tất cả */}
      <Button variant='ghost' size='sm'
        className='h-8 w-8 p-0 text-gray-500 hover:text-gray-700 hover:bg-gray-100'
        onClick={() => { treeExpanded ? collapseAll() : expandAll(); setTreeExpanded(!treeExpanded) }}
        title={treeExpanded ? 'Thu gọn tất cả' : 'Mở rộng tất cả'}
        data-qa='btn_toggle_expand'>
        {treeExpanded ? <SquareMinus className='h-4 w-4' /> : <SquarePlus className='h-4 w-4' />}
      </Button>

      {/* (Tùy chọn) Nút Xuất Excel */}
      <Button variant='ghost' size='sm' ... onClick={handleExportToExcel}>
        <FileSpreadsheet className='h-4 w-4' />
      </Button>
    </>
  }
/>
```

### 6.4 Cột Đầu Tiên Có Nút Mở Rộng/Thu Gọn + Indent

```tsx
<DmTableCell className='text-black' style={{ width: 260, minWidth: 260 }}>
  <div className='flex items-center' style={{ paddingLeft: `${row.depth * 20}px` }}>
    {row.hasChildren ? (
      <button type='button'
        className='mr-1 p-0.5 rounded hover:bg-gray-200 shrink-0'
        data-qa={`btn_toggle_${item.id}`}
        title={row.expanded ? 'Thu gọn' : 'Mở rộng'}
        onClick={e => { e.stopPropagation(); toggleExpand(item.id) }}>
        {row.expanded
          ? <ChevronDown className='h-3.5 w-3.5' />
          : <ChevronRight className='h-3.5 w-3.5' />
        }
      </button>
    ) : (
      <span className='inline-block w-[22px] shrink-0' />
    )}
    <span className='truncate'>{item.code || ''}</span>
  </div>
</DmTableCell>
```

> ⚠️ **Quan trọng:** Node không có con vẫn cần `<span className='inline-block w-[22px]' />` để giữ thẳng hàng indent với các node khác.

### 6.5 Row Class Cho Node Cha

```tsx
<DmTableRow
  key={item.id}
  className={cn('cursor-pointer', row.hasChildren && 'font-semibold')}
  data-qa='xxx-row'
  onDoubleClick={() => onRowDoubleClick(item)}>
```

### 6.6 Tổng Số + Không Có Phân Trang

```tsx
{/* Thay DmTablePagination bằng tổng số */}
<div className='px-4 py-3 border-t border-[#e0e0e0] text-sm text-gray-600'>
  Tổng số: <span className='font-semibold text-gray-900'>{totalCount}</span> bản ghi
</div>
```

> ⚠️ Bảng cây **KHÔNG dùng** `DmTablePagination`. Thay vào đó hiển thị tổng số node.

### 6.7 colSpanAll Cho Bảng Cây

Bảng cây thường không có cột checkbox, nên tính `colSpanAll` thủ công:

```tsx
// Không dùng useTableLayout (vì không cần minTableWidth động)
const colSpanAll = 7  // STT + 5 cột dữ liệu + cột ghost action
```

Hoặc nếu vẫn dùng DmTable với useTableLayout:

```tsx
// Bỏ CHECKBOX_COL_WIDTH — truyền mảng visibleColumns rỗng cho cột checkbox
// hoặc tự tính:
const colSpanAll = colsForRender.length + 1  // data columns + ghost action (không checkbox)
```

---

## 7. Page Hook Mẫu (`use{Name}PageList`)

```ts
// src/modules/KetoanApp/features/danh-muc/{ten-feature}/hooks/use{Name}.page.list.ts
import { useState, useEffect, useCallback } from 'react'
import { useDebounce } from '@/shared/hooks/useDebounce'
import { getPageSizeFromStorage } from '@/shared/utils/PagingUtils'
import type { XxxDto } from '../types'
import { XxxApiService } from '../services'

export function useXxxPageList() {
  const [items, setItems] = useState<XxxDto[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(() => getPageSizeFromStorage(50))
  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 800)

  const fetchData = useCallback(async (isRefresh?: boolean) => {
    if (isRefresh) setRefreshing(true); else setLoading(true)
    try {
      const r = await XxxApiService.list({
        pageIndex: page,
        pageSize: limit,
        keyword: debouncedSearch || undefined,
      })
      if (r.success && r.data) {
        setItems(r.data.items)
        setTotal(r.data.total)
        setPage(r.data.page)
        setLimit(r.data.limit)
      }
    } catch { /* apiCall tự log */ }
    finally { setLoading(false); setRefreshing(false) }
  }, [debouncedSearch, page, limit])

  useEffect(() => { fetchData() }, [fetchData])

  // Reset page=1 khi search thay đổi
  useEffect(() => { setPage(1) }, [debouncedSearch])

  return {
    items, total, page, limit,
    loading, refreshing,
    search, setSearch,
    setPage,
    setLimit: (s: number) => { setLimit(s); setPage(1) },
    handleRefresh: () => { setPage(1); fetchData(true) },
    refetch: () => fetchData(),
  }
}
```

---

## 8. Import Tổng Hợp

```tsx
// Components từ KetoanApp
import {
  DmPageHeader, DmSearchToolbar, DmTablePagination,
  DmTable, DmTableHeader, DmTableHeaderRow, DmTableHead,
  DmTableBody, DmTableRow, DmTableCell, DmRowActions,
} from '@/modules/KetoanApp/components'

// Shared hooks
import {
  useTableLayout, useDmRowActions, useBulkSelection,
  useTableSettings, useRowDoubleClick, useExcelExport,
  useResizableColumns,
} from '@/shared/hooks'
import type { ColumnSetting } from '@/shared/hooks/useTableSettings'

// Shared components
import { ConfirmDialog, BulkActionBar } from '@/shared/components/common'
import { TableSettingsPanel } from '@/shared/components/table-settings'

// Lucide icons thường dùng
import {
  Plus, RefreshCw, FileSpreadsheet, Settings,
  Eye, Pencil, Trash2, Copy, MoreHorizontal,
  ChevronDown, ChevronRight, SquarePlus, SquareMinus,
  Ban, CheckCircle, ToggleLeft, ToggleRight,
} from 'lucide-react'

// Utils
import { cn } from '@/shared/components/ui/utils'
```

---

## 9. PAGE_ID + PAGE_FEATURES

**BẮT BUỘC** khai báo ở đầu file Page:

```tsx
export const PAGE_ID = 'ten-page-id'  // phải khớp navItem.id trong NavMenu
export const PAGE_FEATURES = [
  { label: 'Làm mới',     code: 'btn-refresh' },
  { label: 'Thêm mới',    code: 'btn-create' },
  { label: 'Xem chi tiết',code: 'row-view' },
  { label: 'Chỉnh sửa',   code: 'row-edit' },
  { label: 'Nhân bản',    code: 'row-clone' },
  { label: 'Xóa',         code: 'row-delete' },
]
```

- `code` prefix: `btn-` cho nút toolbar/header, `row-` cho action trên dòng, `batch-` cho thao tác hàng loạt
- Liệt kê **TẤT CẢ** các nút/thao tác thực tế có trong trang

---

## 10. Check List Trước Khi Commit

- [ ] Page dùng `DmPageHeader` (có title, description, actions)
- [ ] Page dùng `DmSearchToolbar` (có search, extraActions)
- [ ] Page dùng `DmTable` + `DmTableHeader`/`DmTableBody`/`DmTableRow`/`DmTableCell`
- [ ] Page dùng `DmTablePagination` (trừ bảng cây → hiển thị tổng số)
- [ ] **Header cố định:** Header bảng tách riêng `<div>` với `shrink-0 overflow-hidden`, body `flex-1 overflow-auto` (Section 2)
- [ ] **colgroup đồng bộ:** Cả header và body table đều có `<colgroup>` giống hệt nhau để tránh lệch column width (Section 2)
- [ ] **Scroll đồng bộ:** `headerScrollRef` + `handleTableScroll` đồng bộ scroll ngang giữa header và body
- [ ] **Resize cột:** Có `useColumnResize` + `getColumnWidth` trong header & body + `onResizeMouseDown` (Section 13)
- [ ] Có ghost scrollbar (`ghostRef`) đồng bộ với table
- [ ] Cột action dùng sticky right width=0 + opacity hover
- [ ] **DmTableRow có `onDoubleClick` mở form Edit** (bắt buộc cho mọi pattern)
- [ ] Có `PAGE_ID` + `PAGE_FEATURES` đầy đủ
- [ ] `data-qa` trên tất cả button, row (`tbl_danh_sach`, `btn_*`, `{feature}-row`)
- [ ] Layout: `bg-[#e8ecf1]` → white card `rounded-xl` → table
- [ ] Dialog và ConfirmDialog nằm NGOÀI CardContent
- [ ] Logic ở hook, UI chỉ render
- [ ] Validate input trước khi gọi API
- [ ] **Giá trị rỗng:** dùng `''` (chuỗi rỗng), TUYỆT ĐỐI KHÔNG dùng `'-'` trong CELL_VALUE
- [ ] Bảng cây: có nút Mở rộng/Thu gọn ở extraActions
- [ ] Bảng cây: indent `depth * 20px`, node không con có spacer `w-[22px]`
- [ ] Bảng cây: `font-semibold` cho node cha
- [ ] Nếu dùng `useTableSettings`: khai báo `ALL_COLUMNS` trong `shared/constants/table-settings.const.ts`

---

## 11. Script Kiểm Tra

```bash
# Kiểm tra 1 page
node .claude/skills/tao-ui-master-page/check-master-page.cjs src/modules/KetoanApp/features/.../pages/XxxPage.tsx

# Kiểm tra nhiều page
node .claude/skills/tao-ui-master-page/check-master-page.cjs "src/modules/KetoanApp/**/pages/*Page.tsx"
```

---

## 12. Thư Mục Feature Chuẩn

```
features/danh-muc/{ten-feature}/
├── pages/
│   └── XxxPage.tsx              ← Master Page
├── dialogs/
│   └── XxxFormDialog.tsx        ← Dialog CRUD
├── hooks/
│   ├── useXxx.page.list.ts      ← Hook fetch danh sách
│   ├── useXxx.dlg.form.ts       ← Hook xử lý form dialog
│   ├── useXxx.tree.ts           ← (nếu là bảng cây) Hook quản lý cây
│   └── index.ts                 ← Barrel export
├── services/
│   └── XxxApiService.ts         ← API Service
└── types/
    └── types.ts                 ← Type definitions
```

---

## 13. Resize Cột — Kéo Thay Đổi Độ Rộng & Lưu localStorage (BẮT BUỘC)

> **TẤT CẢ master page dùng `DmTable` PHẢI tích hợp resize cột.** User kéo cạnh phải header để thay đổi độ rộng, lưu vào localStorage.
> **Nguồn tham khảo đầy đủ:** `tao-phieu-thu` Section 13.

### 13.1 Hook `useColumnResize`

Hook đặt tại `src/modules/KetoanApp/hooks/useColumnResize.ts`. Nhận `columns` (từ `useTableSettings`) và `onColumnsChange` (chính là `saveSettings`).

```tsx
import { useColumnResize } from '@/modules/KetoanApp/hooks/useColumnResize'

// Với Pattern A (FIXED_COLS):
const { handleResizeStart, getColumnWidth } = useColumnResize(visibleColumns, saveSettings)

// Với Pattern B (ALL_COLUMNS + useTableSettings):
const { columns, visibleColumns, saveSettings, restoreDefaults }
  = useTableSettings({ tableId: 'xxx', allColumns: XXX_ALL_COLUMNS, defaultVisibleCount: 5 })
const { handleResizeStart, getColumnWidth } = useColumnResize(visibleColumns, saveSettings)
```

- `handleResizeStart(colId, mouseEvent)` — gắn vào `onMouseDown` của resize handle trong `DmTableHead`
- `getColumnWidth(colId, defaultWidth)` — trả về width thực tế (đang resize hoặc mặc định), dùng thay cho `col.width` trong style
- Tự động set `cursor: col-resize` và `userSelect: none` trên body trong khi kéo
- Khi thả chuột, gọi `onColumnsChange` để lưu vào localStorage thông qua `useTableSettings`

### 13.2 `DmTableHead` — Resize Handle

Component `DmTableHead` (`src/modules/KetoanApp/components/DmTable.tsx`) có prop `onResizeMouseDown`. Khi có prop này, một thanh kéo mỏng (`w-1.5 cursor-col-resize`) xuất hiện ở cạnh phải header:

```tsx
export function DmTableHead({ className, children, pinned, onResizeMouseDown, ...props }: 
  React.ComponentProps<'th'> & { pinned?: boolean; onResizeMouseDown?: (e: React.MouseEvent) => void }
) {
  return (
    <th className={cn('relative ...', className)} {...props}>
      {children}
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

> ⚠️ `th` phải có `relative` để resize handle `absolute` hoạt động đúng.

### 13.3 Tích Hợp Vào Page — Dùng `getColumnWidth`

**TẤT CẢ vị trí dùng `col.width` PHẢI thay bằng `getColumnWidth(col.id, col.width)`** để độ rộng cột đồng bộ khi đang kéo:

```tsx
// ── Header (CHỈ header mới có onResizeMouseDown) ──
{colsForRender.map(col => {
  const w = getColumnWidth(col.id, col.width)
  return (
    <DmTableHead
      key={col.id}
      style={{ width: w, minWidth: w }}
      onResizeMouseDown={(e) => handleResizeStart(col.id, e)}
    >
      {col.displayName ?? col.title}
    </DmTableHead>
  )
})}

// ── Body ──
{colsForRender.map(col => (
  <DmTableCell key={col.id}
    style={{ width: getColumnWidth(col.id, col.width), minWidth: getColumnWidth(col.id, col.width) }}
    className={cn(colClass(col.field))}>
    {rowValue(item, col.field)}
  </DmTableCell>
))}

// ── Ghost scrollbar (minWidth cũng dùng getColumnWidth) ──
<div style={{ minWidth: minTableWidth, height: 1 }} />
```

### 13.4 Pattern A (FIXED_COLS) — Tích Hợp `useColumnResize`

Khi dùng `FIXED_COLS` (không có `useTableSettings`), vẫn dùng được `useColumnResize` bằng cách truyền trực tiếp mảng cột và callback lưu:

```tsx
import { useColumnResize } from '@/modules/KetoanApp/hooks/useColumnResize'

const STORAGE_KEY = 'ketoan_xxx_column_widths'

function loadWidths(): Record<string, number> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch { return {} }
}

function saveWidths(widths: Record<string, number>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(widths))
}

// Trong component:
const [columnWidths, setColumnWidths] = useState<Record<string, number>>(() => loadWidths())

// Wrap FIXED_COLS với width đã lưu
const colsWithWidths = useMemo(() =>
  FIXED_COLS.map(col => ({ ...col, width: columnWidths[col.id] ?? col.width })),
  [columnWidths]
)

const { colsForRender, minTableWidth, colSpanAll, tableRef, ghostRef, onTableScroll, onGhostScroll }
  = useTableLayout(colsWithWidths as any)

const { handleResizeStart, getColumnWidth } = useColumnResize(
  colsWithWidths,
  (updatedCols) => {
    const widths: Record<string, number> = {}
    for (const c of updatedCols) { widths[c.id] = c.width }
    saveWidths(widths)
    setColumnWidths(widths)
  }
)
```

> ⚠️ Quan trọng: `useColumnResize` nhận `columns` array phải có trường `width` là số. `colsWithWidths` đảm bảo điều này. `colsForRender` (từ `useTableLayout`) đã thêm các field layout (`_stickyLeft`, `_isFirstRightSticky`...) — KHÔNG truyền `colsForRender` vào `useColumnResize` vì thiếu `width` number.

---

## 🔥 Lỗi Hay Gặp Khi Code Master Page (Checklist Tránh Lặp)

> **Mục đích:** Liệt kê các lỗi phổ biến bị phát hiện qua review. Đọc trước khi code để tránh.

### 1. ❌ Dùng `formatCurrency` trong table list

**Bị:** formatCurrency hiển thị "₫" trong bảng danh sách → gây rối mắt, không đồng nhất.

```
❌ SAI: formatCurrency(i.totalAmount)
✅ ĐÚNG: formatNumber(i.totalAmount)
```

### 2. ❌ Fallback `|| '-'` trong CELL_VALUE

```
❌ SAI: item.voucherCode || '-'
✅ ĐÚNG: item.voucherCode || ''
```

### 3. ❌ 1 DmTable chung cho cả header + body

**Dấu hiệu:** Toàn bộ header + body nằm trong 1 `<DmTable>` duy nhất. Khi scroll xuống header biến mất.

```
❌ SAI: <DmTable>
          <DmTableHeader>...</DmTableHeader>
          <DmTableBody>...</DmTableBody>
        </DmTable>
        (cả 2 nằm trong cùng 1 vùng overflow-auto)

✅ ĐÚNG: <div ref={headerScrollRef} className='shrink-0 overflow-hidden'>
          <DmTable><DmTableHeader>...</DmTableHeader></DmTable>
        </div>
        <div className='flex-1 min-h-0 overflow-auto' ref={tableRef} onScroll={handleTableScroll}>
          <DmTable><DmTableBody>...</DmTableBody></DmTable>
        </div>
```

> **Tham khảo file mẫu:** `Sasuco-web/src/modules/KetoanApp/features/nghiep-vu/thu-tien/phieu-thu/pages/PhieuThuPage.tsx`

### 4. ❌ Thiếu `<colgroup>` trong DmTable

Cả header và body table đều phải có `<colgroup>` với các `<col style={{ width }}>`. Điều này đảm bảo cột header và body khớp nhau.

### 5. ❌ Dùng `col.width` trực tiếp — không resize được

```
❌ SAI: style={{ width: col.width }}
✅ ĐÚNG: style={{ width: getColumnWidth(col.id, col.width) }}
        + useColumnResize({ columns, tableRef })
```

### 6. ❌ Thiếu `headerScrollRef` — scroll ngang không đồng bộ

Khi user scroll ngang trong body, header không scroll theo. Fix:

```tsx
const headerScrollRef = useRef<HTMLDivElement>(null)

const handleTableScroll = useCallback(() => {
  onTableScroll()
  const sl = tableRef.current?.scrollLeft ?? 0
  if (headerScrollRef.current) headerScrollRef.current.scrollLeft = sl
}, [onTableScroll])
```

### 7. ❌ Nút "Thêm mới" không ở cuối bên phải DmPageHeader

```
❌ SAI: <DmPageHeader actions={<>[Làm mới] [Thêm] [Xuất Excel] [Cài đặt]</>}>
✅ ĐÚNG: <DmPageHeader actions={<>[Làm mới] [Xuất Excel] [Cài đặt] [Thêm]</>}>
```

Nút "Thêm" PHẢI là nút cuối cùng bên phải.

### 8. ❌ DmPageHeader chứa nút chức năng thay vì DmSearchToolbar

Các nút "Làm mới", "Xuất Excel", "Thiết lập bảng" nên nằm trong `DmSearchToolbar extraActions`, không phải trong `DmPageHeader actions`. `DmPageHeader actions` chỉ nên có nút "Thêm".

### 9. ❌ Thiếu `group` className trên DmTableRow

```
❌ SAI: <DmTableRow className={cn(!item.isPosted && 'text-amber-700')}>
✅ ĐÚNG: <DmTableRow className={cn('group', !item.isPosted && 'text-amber-700')}>
```

Thiếu `group` → ghost action column không hiện khi hover row.

### 10. ❌ Có BulkActionBar nhưng không có cột checkbox

Nếu dùng `BulkActionBar` và `selection` hook → PHẢI có cột checkbox đầu tiên trong bảng. Ngược lại, nếu không có BulkActionBar thì không cần.

### 11. ❌ Icon `animate-spin` khi exporting bị thiếu

```
❌ SAI: <FileSpreadsheet className='h-4 w-4' />
✅ ĐÚNG: <FileSpreadsheet className={cn('h-4 w-4', exporting && 'animate-spin')} />
```
