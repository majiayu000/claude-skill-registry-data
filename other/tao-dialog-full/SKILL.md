---
name: tao-dialog-full
description: 'Tạo Dialog full-screen cho nghiệp vụ KetoanApp. Layout: Header (title + tổng tiền + nút X) → Body (2 cột: trái flex-1 fields, phải w-[250px] ngày/số phiếu) → Bảng hạch toán EditableDataTable (white card + tab) → Footer (Hủy/Lưu/Lưu & Ghi sổ). Kế thừa từ PCDialog/PTDialog. Dùng chung cho Phiếu thu, Phiếu chi, Tiền gửi, Tiền vay và mọi dialog full-screen tương tự.'
---

# Tạo Dialog Full-Screen — KetoanApp

> **Kế thừa:** `tao-ui-giao-dien-new` (foundation UI), `tao-dialog-new` (cấu trúc dialog), `table-combobox-id-only` (FK chỉ gửi ID).
>
> **Base code:** `PCDialog.tsx` (Phiếu chi) và `PTDialog.tsx` (Phiếu thu) — 2 dialog full-screen chuẩn trong KetoanApp.
>
> **Áp dụng cho:** TẤT CẢ dialog full-screen nghiệp vụ: Phiếu thu, Phiếu chi, Tiền gửi, Tiền vay, và mọi dialog có cấu trúc tương tự.

---

## 0. Tổng Quan Layout Full-Screen

```
┌──────────────────────────────────────────────────────────────────┐
│ HEADER (flex-shrink-0, border-b)                                │
│ [Title + refType Select]          [Tổng tiền: 999,999] [X]      │
├──────────────────────────────────────────────────────────────────┤
│ BODY (flex-1, min-h-0, overflow-hidden, bg-[#f4f5f7],        │
│       flex flex-col)                                            │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ SECTION: Thông tin chung (flex-shrink-0, fixed top)        │ │
│ │ ┌───────────────────────────────┐ ┌─────────────────────┐   │ │
│ │ │ CỘT TRÁI (flex-1)            │ │ CỘT PHẢI (w-[250px]) │   │ │
│ │ │ • Field 1    • Field 2       │ │ • Ngày hạch toán *   │   │ │
│ │ │ • Field 3 (full width)       │ │ • Ngày chứng từ *    │   │ │
│ │ │ • Field 4 (full width)       │ │ • Số phiếu *         │   │ │
│ │ │ • Field 5    • Field 6       │ │                       │   │ │
│ │ └───────────────────────────────┘ └─────────────────────┘   │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ SECTION: Hạch toán (flex-1, min-h-0, fill remaining space) │ │
│ │ ┌─ Tab header: "Hạch toán" (flex-shrink-0, fixed)         │ │
│ │ ├─ Table scroll area (flex-1, min-h-0, overflow-y-auto)    │ │
│ │ ├─ Sum Row (Tổng cộng)                                     │ │
│ │ └─ Error message (nếu có)                                  │ │
│ └──────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│ FOOTER (flex-shrink-0, border-t)                                │
│ [placeholder]                 [Hủy] [Lưu] [Lưu & Ghi sổ]        │
└──────────────────────────────────────────────────────────────────┘
```

### 0.1 Kích Thước Chuẩn

| Phần | Width | Height | Giải thích |
|------|-------|--------|------------|
| Cột trái (fields) | `flex-1` | — | Chiếm phần còn lại sau khi trừ cột phải + gap |
| Cột phải (ngày/số) | `w-[250px] flex-shrink-0` | — | Cố định 250px, không co giãn |
| Gap giữa 2 cột | `gap-6` (24px) | — | Khoảng cách giữa cột trái và cột phải |
| Input | `h-[30px] text-[13px] rounded-lg` | — | Chiều cao & style chuẩn |
| Select | `h-8 text-[13px] rounded-lg` | — | Chiều cao select chuẩn |
| Label | `text-[13px] font-semibold text-black` | — | Style label chuẩn |
| Header | — | `py-3.5` | Padding top/bottom |
| Footer | — | `py-2.5` | Padding top/bottom |
| Info section (fixed) | — | `flex-shrink-0` | Cố định trên cùng, không scroll |
| Table section (fill) | — | `flex-1 min-h-0` | Fill hết chiều cao còn lại |
| Table scroll area | — | `flex-1 min-h-0 overflow-y-auto` | Chỉ bảng scroll, tab header cố định |

---

## 1. DialogContent — Full-Screen Pattern (BẮT BUỘC)

```tsx
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent
    maxWidth='none'
    className='w-[100vw] max-w-[100vw] h-[100vh] max-h-[100vh] p-0 gap-0 rounded-none shadow-[0_5px_20px_rgba(0,0,0,0.1)] border-0 flex flex-col bg-white overflow-hidden [&>button:first-child]:hidden'
  >
    {renderHeader()}
    {renderBody()}
    {renderFooter()}
  </DialogContent>
</Dialog>
```

| Prop | Giá trị | Giải thích |
|------|---------|-----------|
| `maxWidth` | `'none'` | Bỏ giới hạn chiều rộng mặc định |
| `w-[100vw] max-w-[100vw]` | Full viewport width | Tràn toàn màn hình |
| `h-[100vh] max-h-[100vh]` | Full viewport height | Tràn toàn màn hình |
| `p-0 gap-0 rounded-none` | Zero padding/gap/radius | Sát viền, không bo góc |
| `flex flex-col` | Flex column | Layout Header → Body → Footer |
| `overflow-hidden` | Ẩn overflow | Body tự scroll riêng |
| `[&>button:first-child]:hidden` | Ẩn nút X mặc định | Dùng nút X tự tạo trong Header |

---

## 2. Header Pattern

```tsx
const renderHeader = () => (
  <div className='flex items-center justify-between px-5 py-3.5 bg-white flex-shrink-0 border-b border-[#B7BCC3]'>
    <div className='flex items-center gap-3'>
      <span className='font-semibold text-black text-base'>
        {TITLE} {formData.refNo}
      </span>
      {/* refType Select (nếu có) */}
      <div className='flex items-center gap-1.5'>
        <Select
          value={String(formData.refType)}
          onValueChange={(v) => setField('refType', Number(v))}
          disabled={isReadOnly}
        >
          <SelectTrigger className={cn(
            'w-[260px] h-8 text-[13px] font-medium truncate border-[#B7BCC3] rounded-lg bg-white',
            isReadOnly && 'opacity-70'
          )} data-qa='sel_ref_type'>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(TYPE_LABELS).map(([val, label]) => (
              <SelectItem key={val} value={val} className='text-[13px] font-medium'>{label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        {!isReadOnly && touched.refType && errors.refType && (
          <span className='text-xs text-destructive flex items-center gap-1'>
            <AlertCircle className='h-3 w-3' />{errors.refType}
          </span>
        )}
      </div>
    </div>
    <div className='flex items-center gap-4'>
      <div className='text-right'>
        <div className='text-[11px] text-black leading-tight'>Tổng tiền</div>
        <div className='font-bold text-base text-black'>{formatCurrency(totalAmount)}</div>
      </div>
      <Button
        variant='ghost' size='sm'
        data-qa='btn_dong_dialog'
        className='h-7 w-7 p-0 text-black hover:text-black hover:bg-gray-100'
        onClick={() => {
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
    </div>
  </div>
)
```

**Đặc điểm Header:**
- `flex-shrink-0` — không bị co lại khi body scroll
- `border-b border-[#B7BCC3]` — đường kẻ phân cách với body
- Nút X có **unsaved guard**: nếu form dirty → mở ConfirmDialog; nếu không → đóng luôn
- `title`: do user truyền vào (VD: "Chi tiền", "Thu tiền")
- `refType Select`: tùy chọn, nếu không có refType thì bỏ

### 2.1 State cần có trong Dialog

```tsx
const [confirmClearOpen, setConfirmClearOpen] = useState(false)
const [unsavedOpen, setUnsavedOpen] = useState(false)
const dirtyRef = useRef(false)
const pendingCloseRef = useRef<(() => void) | null>(null)
```

### 2.2 Theo dõi dirty state

```tsx
// Reset dirty khi mở dialog
useEffect(() => {
  if (!open) return
  dirtyRef.current = false
}, [open, editingId])

// Set dirty khi form thay đổi trong mode edit/create
useEffect(() => {
  if (open && mode !== 'view') {
    dirtyRef.current = true
  }
}, [open, mode, formData])

// Cleanup pending close khi unsaved dialog đóng
useEffect(() => {
  if (!unsavedOpen && pendingCloseRef.current && !dirtyRef.current) {
    pendingCloseRef.current()
    pendingCloseRef.current = null
  }
}, [unsavedOpen])
```

---

## 3. Body Pattern

> **QUAN TRỌNG:** Body dùng `flex flex-col` với `overflow-hidden`. **KHÔNG scroll body** — chỉ bảng hạch toán được scroll (`overflow-y-auto`). Phần thông tin chung cố định (`flex-shrink-0`), bảng hạch toán fill hết chiều cao còn lại (`flex-1 min-h-0`).

```tsx
const renderBody = () => (
  <div className='flex-1 min-h-0 overflow-hidden bg-[#f4f5f7] flex flex-col'>
    {loadingDetail ? (
      <div className='flex items-center justify-center h-40'>
        <Loader2 className='animate-spin h-6 w-6 text-black' />
      </div>
    ) : (
      <>
        {/* ── Section: Thông tin chung (fixed top) ──────────────── */}
        <div className='p-5 pb-0 flex-shrink-0'>
          <div className='flex gap-6'>
            {/* Cột trái: flex-1 — các field nghiệp vụ */}
            <div className='flex-1 space-y-3'>
              {/* Các field do user định nghĩa — xem Section 3.1 */}
            </div>

            {/* Cột phải: w-[250px] flex-shrink-0 — Ngày + Số phiếu */}
            <div className='w-[250px] flex-shrink-0 space-y-3'>
              {/* Các field ngày/số do user định nghĩa — xem Section 3.2 */}
            </div>
          </div>
        </div>

        {/* ── Section: Bảng hạch toán (fill remaining space) ────── */}
        <div className='p-5 pt-4 flex-1 min-h-0 flex flex-col'>
          {/* Xem Section 4 */}
        </div>
      </>
    )}
  </div>
)
```

**Đặc điểm Body:**
- `flex-1 min-h-0 overflow-hidden bg-[#f4f5f7] flex flex-col` — flex column, **KHÔNG scroll** toàn bộ body
- `min-h-0` — QUAN TRỌNG: cho phép flex child co lại
- Info section: `p-5 pb-0 flex-shrink-0` — cố định trên cùng, không scroll
- Table section: `p-5 pt-4 flex-1 min-h-0 flex flex-col` — fill hết không gian còn lại
- Chỉ table scroll (`overflow-y-auto` ở trong white card — xem Section 4)
- Loading: spinner nằm giữa

### 3.1 Cột Trái (flex-1) — Field Pattern

Các field được tổ chức linh hoạt theo nhu cầu. Pattern phổ biến:

```tsx
<div className='flex-1 space-y-3'>
  {/* Pattern A: 2 field ngang hàng (grid-cols-2) */}
  <div className='grid grid-cols-2 gap-4'>
    {/* Field 1 */}
    <div className='space-y-1'>
      <Label className='text-[13px] font-semibold text-black'>Tên field</Label>
      <Input ... />
    </div>
    {/* Field 2 */}
    <div className='space-y-1'>
      <Label className='text-[13px] font-semibold text-black'>Tên field</Label>
      <Input ... />
    </div>
  </div>

  {/* Pattern B: Field full-width */}
  <div className='space-y-1'>
    <Label className='text-[13px] font-semibold text-black'>Tên field</Label>
    <Input ... />
  </div>

  {/* Pattern C: Field với TableSearchCombobox */}
  <div className='space-y-1'>
    <Label className='text-[13px] font-semibold text-black'>Đối tượng</Label>
    <TableSearchCombobox
      value={formData.xxxId}
      initialLabel={formData.xxxName}
      displayField='name'
      onChange={(id, rowData) => {
        if (isReadOnly) return
        setField('xxxId', id)
        setField('xxxName', rowData.name || '')
      }}
      loadOptions={loadXxx}
      columns={xxxColumns}
      dataQa='sel_xxx'
      showQuickAdd
      debounceMs={800}
      disabled={isReadOnly}
    />
  </div>
</div>
```

### 3.2 Cột Phải (w-[250px]) — Ngày & Số Phiếu

Cột phải **mặc định** chứa: Ngày hạch toán, Ngày chứng từ, Số phiếu. User có thể thêm/bớt field.

```tsx
<div className='w-[250px] flex-shrink-0 space-y-3'>
  {/* Ngày hạch toán */}
  <div className='space-y-1'>
    <Label className='text-[13px] font-semibold text-black'>
      Ngày hạch toán <span className='text-red-500'>*</span>
    </Label>
    <div className='space-y-0.5'>
      <DatePicker
        dataQa='dt_posted_date'
        value={formData.postedDate}
        onChange={v => setField('postedDate', v)}
        onBlur={() => handleBlur('postedDate')}
        disabled={isReadOnly}
        className={cn(
          'h-[30px] text-[13px] rounded-lg bg-white w-full',
          !isReadOnly && touched.postedDate && errors.postedDate
            ? 'border-destructive' : 'border-[#B7BCC3]',
        )}
      />
      {!isReadOnly && touched.postedDate && errors.postedDate && (
        <p className='text-xs text-destructive flex items-center gap-1'>
          <AlertCircle className='h-3 w-3' />{errors.postedDate}
        </p>
      )}
    </div>
  </div>

  {/* Ngày chứng từ */}
  <div className='space-y-1'>
    <Label className='text-[13px] font-semibold text-black'>
      Ngày chứng từ <span className='text-red-500'>*</span>
    </Label>
    <div className='space-y-0.5'>
      <DatePicker
        dataQa='dt_ref_date'
        value={formData.refDate}
        onChange={v => setField('refDate', v)}
        onBlur={() => handleBlur('refDate')}
        disabled={isReadOnly}
        className={cn(
          'h-[30px] text-[13px] rounded-lg bg-white w-full',
          !isReadOnly && touched.refDate && errors.refDate
            ? 'border-destructive' : 'border-[#B7BCC3]',
        )}
      />
      {!isReadOnly && touched.refDate && errors.refDate && (
        <p className='text-xs text-destructive flex items-center gap-1'>
          <AlertCircle className='h-3 w-3' />{errors.refDate}
        </p>
      )}
    </div>
  </div>

  {/* Số phiếu */}
  <div className='space-y-1'>
    <Label className='text-[13px] font-semibold text-black'>
      Số {TEN_PHIEU} <span className='text-red-500'>*</span>
    </Label>
    <div className='space-y-0.5'>
      <Input
        data-qa='i_ref_no'
        value={formData.refNo}
        onChange={e => setField('refNo', e.target.value)}
        onBlur={() => handleBlur('refNo')}
        readOnly={isReadOnly}
        className={cn(
          'h-[30px] text-[13px] rounded-lg bg-white',
          !isReadOnly && touched.refNo && errors.refNo
            ? 'border-destructive' : 'border-[#B7BCC3]',
        )}
      />
      {!isReadOnly && touched.refNo && errors.refNo && (
        <p className='text-xs text-destructive flex items-center gap-1'>
          <AlertCircle className='h-3 w-3' />{errors.refNo}
        </p>
      )}
    </div>
  </div>
</div>
```

---

## 4. Bảng Dữ Liệu (EditableDataTable) — Hạch Toán

> Bảng dữ liệu PHẢI được bọc trong **white card** với flex layout: `flex flex-col flex-1 min-h-0` để fill hết chiều cao còn lại.
> Tab header cố định (`flex-shrink-0`), vùng bảng scroll nội bộ (`flex-1 min-h-0 overflow-y-auto`).

```tsx
{/* ── Section: Bảng dữ liệu ────────────────────────────────── */}
<div className='bg-white rounded-lg shadow-sm overflow-hidden flex flex-col flex-1 min-h-0'>
  {/* Tab header (fixed) */}
  <div className='border-b border-[#B7BCC3] px-3 flex-shrink-0'>
    <button
      type='button'
      className='py-2.5 px-4 text-base font-semibold text-primary border-b-2 border-primary mb-3'
      data-qa='tab_xxx'
    >
      {TABLE_TAB_LABEL}  {/* Do user truyền vào, VD: "Hạch toán" */}
    </button>
  </div>

  {/* Table scroll area */}
  <div className='flex-1 min-h-0 overflow-y-auto'>
    <EditableDataTable<Record<string, unknown>>
      columns={accountingColumns}
      rows={formData.accountingDetails as unknown as Record<string, unknown>[]}
      onChange={(newRows) => setAccountingLines(newRows as unknown as XxxLineFormState[])}
      isReadonly={isReadOnly}
      createEmptyRow={createEmptyLine}
      emptyText='Chưa có dòng dữ liệu'
      addButtonLabel='Thêm dòng'
      data-qa='tbl_xxx'
      sumRow={formData.xxxDetails && (formData.xxxDetails as unknown[]).length > 0 ? (
        <tr className='bg-[#ECEDEF] border-t border-solid border-[#B7BCC3]'>
          <td className='px-2 py-1.5'></td>
          <td className='px-2 py-1.5'>
            <span className='font-semibold text-black'>Tổng cộng</span>
          </td>
          <td className='px-2 py-1.5'></td>
          <td className='px-2 py-1.5'></td>
          <td className='px-2 py-1.5 text-right font-bold text-base text-black'>
            {formatCurrency(totalAmount)}
          </td>
          <td className='px-2 py-1.5'></td>
          <td className='px-2 py-1.5'></td>
          <td className='px-2 py-1.5'></td>
          {!isReadOnly && <td className='px-2 py-1.5'></td>}
        </tr>
      ) : null}
    />
    {errors.xxxDetails && (
      <p className='text-xs text-destructive flex items-center gap-1 mt-1.5'>
        <AlertCircle className='h-3 w-3' />{errors.xxxDetails}
      </p>
    )}
  </div>
</div>
```

### 4.1 EditableDataTable Props

| Prop | Mô tả |
|------|-------|
| `columns` | `EditableColumnDef<T>[]` — định nghĩa cột (key, label, width, render...) |
| `rows` | `T[]` — dữ liệu các dòng |
| `onChange` | Callback khi dữ liệu thay đổi |
| `isReadonly` | `true` khi mode='view' |
| `createEmptyRow` | Factory tạo dòng trống — dùng `useCallback` để tránh re-render |
| `emptyText` | Text hiển thị khi bảng trống |
| `addButtonLabel` | Label nút "Thêm dòng" (mặc định: "Thêm dòng") |
| `sumRow` | JSX dòng tổng cộng — render dưới cùng bảng |
| `data-qa` | Attribute test |

### 4.2 Summit Row Pattern

Sum row có background `bg-[#ECEDEF]`, border-top `border-[#B7BCC3]`:

```tsx
sumRow={
  <tr className='bg-[#ECEDEF] border-t border-solid border-[#B7BCC3]'>
    {/* Các cột trống cho STT + các cột không có tổng */}
    <td className='px-2 py-1.5'></td>
    <td className='px-2 py-1.5'>
      <span className='font-semibold text-black'>Tổng cộng</span>
    </td>
    {/* ... thêm td trống cho các cột khác ... */}
    <td className='px-2 py-1.5 text-right font-bold text-base text-black'>
      {formatCurrency(totalAmount)}
    </td>
    {/* ... thêm td trống cho các cột còn lại ... */}
    {!isReadOnly && <td className='px-2 py-1.5'></td>} {/* Cột xóa nếu không readonly */}
  </tr>
}
```

> **Quy tắc sumRow:** Mỗi cột trong `columns` cần 1 `<td>` tương ứng. Cột cuối cùng (action/xóa) chỉ hiển thị khi `!isReadOnly`.

### 4.3 Column Definition Pattern

```tsx
const accountingColumns = useMemo<EditableColumnDef<Record<string, unknown>>[]>(() => [
  {
    key: '_stt', label: '#', type: 'display', width: '40px',
    render: (_value, _row, idx) => (
      <span className='text-center text-[13px] text-gray-500'>{idx + 1}</span>
    ),
  },
  {
    key: 'description', label: 'Diễn giải', width: '250px',
    render: (value, _row, idx) => (
      <Input
        value={String(value ?? '')}
        onChange={e => updateLine(idx, { description: e.target.value })}
        readOnly={isReadOnly}
        className='h-[26px] text-[13px] rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0'
        data-qa={`i_line_description_${idx}`}
      />
    ),
  },
  {
    key: 'debitAccountId', label: 'TK Nợ', width: '100px',
    render: (_value, row, idx) => (
      <TableSearchCombobox
        value={String(row.debitAccountId ?? '')}
        initialLabel={String(row.debitAccountNumber ?? '')}
        displayField='accountNumber'
        onChange={(id, rowData) => updateLine(idx, {
          debitAccountId: id,
          debitAccountNumber: rowData.accountNumber || '',
        })}
        loadOptions={loadTaiKhoan}
        columns={taiKhoanColumns}
        dataQa={`sel_tk_no_${idx}`}
        disabled={isReadOnly}
      />
    ),
  },
  {
    key: 'amount', label: 'Số tiền',
    render: (value, _row, idx) => (
      <Input
        type='text' inputMode='numeric'
        value={value ? formatNumber(Number(value) || 0) : ''}
        onChange={e => updateLine(idx, {
          amount: e.target.value.replace(/\./g, '').replace(/[^0-9]/g, ''),
        })}
        readOnly={isReadOnly}
        className='h-[26px] p-0 text-[13px] text-right rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0'
        data-qa={`i_line_amount_${idx}`}
      />
    ),
  },
  // ... các cột khác
], [isReadOnly, updateLine])
```

**Style cho input trong bảng:**
- `h-[26px]` (nhỏ hơn input ngoài form `h-[30px]`)
- `text-[13px] rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0`
- Input số: `p-0 text-right` + format `formatNumber()`
- TableSearchCombobox trong bảng: không cần `compact`, dùng height mặc định

### 4.4 Empty Line Factory

```tsx
const createEmptyLine = useCallback((): Record<string, unknown> => {
  return {
    ...XXX_INITIAL_LINE,
    description: formData.description,
  } as unknown as Record<string, unknown>
}, [formData.description])
```

---

## 5. Footer Pattern

```tsx
const renderFooter = () => (
  <div className='flex items-center justify-between px-5 py-2.5 bg-white flex-shrink-0 border-t border-[#B7BCC3]'>
    <span className='text-xs text-black truncate max-w-[50%]' />
    <div className='flex gap-2'>
      {isReadOnly ? (
        <>
          {!formData.isPosted && (
            <>
              <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_sua' onClick={handleSwitchToEdit}>
                <Pencil className='h-3.5 w-3.5 mr-1' />Sửa
              </Button>
              <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_ghi_so' disabled={operating} onClick={() => setPostOpen(true)}>
                {operating && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}
                <BookOpen className='h-3.5 w-3.5 mr-1' />Ghi sổ
              </Button>
            </>
          )}
          {formData.isPosted && (
            <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_bo_ghi_va_sua' disabled={operating} onClick={() => setUnpostOpen(true)}>
              {operating && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}
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
            onClick={() => {
              if (dirtyRef.current) { setUnsavedOpen(true); pendingCloseRef.current = () => onOpenChange(false) }
              else onOpenChange(false)
            }}>Hủy</Button>
          <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_luu' disabled={submitting} onClick={handleSubmit}>
            {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu
          </Button>
          <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_luu_va_them' disabled={submitting} onClick={handleSubmitAndNew}>
            {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu &amp; Thêm
          </Button>
        </>
      )}
    </div>
  </div>
)
```

### 5.1 Ma Trận Action Footer

| Mode | Điều kiện | Buttons |
|------|----------|---------|
| **View** | `!isPosted` (chưa ghi sổ) | `[Sửa]` `[Ghi sổ]` |
| **View** | `isPosted` (đã ghi sổ) | `[Bỏ ghi và sửa]` |
| **Create** | — | `[Hủy]` `[Lưu]` `[Lưu & Thêm]` |
| **Edit** | — | `[Hủy]` `[Lưu]` |

**Nút `[Lưu & Ghi sổ]` (thay cho `[Lưu & Thêm]`):** Nếu nghiệp vụ cần ghi sổ ngay khi tạo, dùng `handleCreateAndPost`:

```tsx
{mode === 'create' && (
  <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_luu_va_ghi_so' disabled={submitting} onClick={handleCreateAndPost}>
    {submitting && <Loader2 className='animate-spin h-3.5 w-3.5 mr-1' />}Lưu &amp; Ghi sổ
  </Button>
)}
```

### 5.2 Button Style Convention

| Class | Dùng cho |
|-------|----------|
| `btn-secondary h-8 text-[13px] rounded-lg` | Hủy, Lưu, Sửa |
| `btn-primary h-8 text-[13px] rounded-lg` | Ghi sổ, Bỏ ghi và sửa, Lưu & Thêm, Lưu & Ghi sổ |
| Icon size trong button | `h-3.5 w-3.5` |

> ❌ KHÔNG dùng `variant='outline'` hoặc Button trần.

---

## 6. Confirm Dialogs

### 6.1 Unsaved Changes Guard

```tsx
<ConfirmDialog
  open={unsavedOpen}
  onOpenChange={(open) => { if (!open) dirtyRef.current = false; setUnsavedOpen(open) }}
  title='Dữ liệu đã bị thay đổi'
  message='Bạn có muốn lưu các thay đổi không?'
  confirmLabel='Có' cancelLabel='Không'
  onConfirm={async () => { setUnsavedOpen(false); dirtyRef.current = false; await handleSubmit() }}
/>
```

### 6.2 Clear All Lines

```tsx
<ConfirmDialog
  open={confirmClearOpen}
  onOpenChange={setConfirmClearOpen}
  title='Xóa hết dòng?'
  message='Toàn bộ dòng sẽ bị xóa. Thao tác này không thể hoàn tác.'
  onConfirm={() => { clearAllLines(); setConfirmClearOpen(false) }}
  variant='destructive'
/>
```

### 6.3 Post / Unpost

```tsx
<ConfirmDialog
  open={postOpen}
  onOpenChange={setPostOpen}
  title='Ghi sổ {TEN_PHIEU}'
  message={`Bạn có chắc chắn muốn ghi sổ {TEN_PHIEU} ${formData.refNo}? Sau khi ghi sổ sẽ không thể chỉnh sửa.`}
  confirmLabel='Ghi sổ'
  onConfirm={async () => {
    if (!editingId) return
    setOperating(true)
    const ok = await handlePost(editingId)
    setOperating(false)
    if (ok) { setPostOpen(false); onOpenChange(false) }
  }}
/>

<ConfirmDialog
  open={unpostOpen}
  onOpenChange={setUnpostOpen}
  title='Bỏ ghi sổ {TEN_PHIEU}'
  message={`Bạn có chắc chắn muốn bỏ ghi sổ {TEN_PHIEU} ${formData.refNo}?`}
  confirmLabel='Bỏ ghi sổ'
  variant='destructive'
  onConfirm={handleUnpostAndEdit}
/>
```

### 6.4 Validation Error

```tsx
<ValidationErrorDialog
  open={serverErrorOpen}
  onOpenChange={setServerErrorOpen}
  title='Lỗi từ máy chủ'
  message={typeof serverError === 'object' && serverError !== null && 'message' in (serverError as Record<string, unknown>)
    ? (serverError as Record<string, unknown>).message as string
    : undefined}
/>
```

---

## 7. Dialog Props Interface (Chuẩn)

```tsx
interface XxxDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  /** Nếu truyền → mở ở mode view/edit; không truyền → mode create */
  editingId?: string | null
  defaultMode?: 'view' | 'edit' | 'create'
  onSuccess: () => void
}
```

### 7.1 Hook Interface

Hook của dialog cần expose các methods sau:

```tsx
const {
  mode,              // 'view' | 'create' | 'edit'
  formData,          // FormState
  errors,            // FormErrors
  touched,           // Record<string, boolean>
  submitting,        // boolean
  loadingDetail,     // boolean
  totalAmount,       // number — tổng tiền từ accounting lines
  serverError,       // unknown
  serverErrorOpen,   // boolean
  setServerErrorOpen,// (open: boolean) => void
  setField,          // (field: string, value: any) => void
  handleBlur,        // (field: string) => void
  updateLine,        // (idx: number, patch: Partial<LineState>) => void
  clearAllLines,     // () => void
  setAccountingLines,// (lines: LineState[]) => void
  handleSubmit,      // () => Promise<void>
  handleSubmitAndNew,// () => Promise<void> — Lưu & Thêm mới
  handlePost,        // (id: string) => Promise<boolean>
  handleUnpost,      // (id: string) => Promise<boolean>
  initCreate,        // () => Promise<void>
  initEdit,          // (id: string) => Promise<void>
  initView,          // (id: string) => Promise<void>
} = useXxxDlgForm({ onSuccess, onClose: () => onOpenChange(false) })
```

### 7.2 Init Mode Handler

```tsx
useEffect(() => {
  if (!open) return
  dirtyRef.current = false
  if (editingId) {
    if (defaultMode === 'view') initView(editingId)
    else initEdit(editingId)
  } else {
    initCreate()
  }
}, [open, editingId, defaultMode, initCreate, initEdit, initView])
```

---

## 8. Chuyển Đổi Mode

### 8.1 View → Edit (Unposted)

```tsx
const handleSwitchToEdit = () => {
  if (!editingId) return
  setField('isPosted', false)
  initEdit(editingId)
}
```

### 8.2 View (Posted) → Bỏ ghi sổ → Edit

```tsx
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

---

## 9. CSS Convention Tổng Hợp

| Element | Class |
|---------|-------|
| DialogContent | `w-[100vw] max-w-[100vw] h-[100vh] max-h-[100vh] p-0 gap-0 rounded-none ... [&>button:first-child]:hidden` |
| Header | `flex items-center justify-between px-5 py-3.5 bg-white flex-shrink-0 border-b border-[#B7BCC3]` |
| Body | `flex-1 min-h-0 overflow-hidden bg-[#f4f5f7] flex flex-col` |
| Info section wrapper | `p-5 pb-0 flex-shrink-0` |
| Table section wrapper | `p-5 pt-4 flex-1 min-h-0 flex flex-col` |
| 2-cột layout | `flex gap-6` |
| Cột trái | `flex-1 space-y-3` |
| Cột phải | `w-[250px] flex-shrink-0 space-y-3` |
| Grid 2 field | `grid grid-cols-2 gap-4` |
| Field wrapper | `space-y-1` |
| Label | `text-[13px] font-semibold text-black` |
| Label required | `<span className='text-red-500'>*</span>` |
| Input | `h-[30px] text-[13px] rounded-lg border-[#B7BCC3] bg-white` |
| Input error | `border-destructive` (khi touched + có error) |
| Input trong bảng | `h-[26px] text-[13px] rounded-lg border border-[#B7BCC3] bg-white text-black focus-visible:ring-0` |
| Input số | `text-right` + `type='text' inputMode='numeric'` |
| Select trigger | `h-8 text-[13px] rounded-lg border-[#B7BCC3] bg-white` |
| Error message | `<p className='text-xs text-destructive flex items-center gap-1'><AlertCircle className='h-3 w-3' />{...}</p>` |
| Footer | `flex items-center justify-between px-5 py-2.5 bg-white flex-shrink-0 border-t border-[#B7BCC3]` |
| Button secondary | `btn-secondary h-8 text-[13px] rounded-lg` |
| Button primary | `btn-primary h-8 text-[13px] rounded-lg` |
| Button icon size | `h-3.5 w-3.5` |
| Hạch toán card | `bg-white rounded-lg shadow-sm overflow-hidden flex flex-col flex-1 min-h-0` |
| Hạch toán tab | `border-b border-[#B7BCC3] px-3 flex-shrink-0` |
| Hạch toán tab button | `py-2.5 px-4 text-base font-semibold text-primary border-b-2 border-primary mb-3` |
| Hạch toán scroll area | `flex-1 min-h-0 overflow-y-auto` |
| Summit row | `bg-[#ECEDEF] border-t border-solid border-[#B7BCC3]` |

---

## 10. Imports Cần Thiết

```tsx
import { useEffect, useRef, useState, useMemo, useCallback } from 'react'
import {
  Dialog,
  DialogContent,
} from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'
import { Input } from '@/shared/components/ui/input'
import { Label } from '@/shared/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { Loader2, X, AlertCircle, Pencil, BookOpen } from 'lucide-react'
import { DatePicker } from '@/shared/components/common'
import { TableSearchCombobox } from '@/shared/components/common'
import { ValidationErrorDialog, ConfirmDialog } from '@/shared/components/common'
import { cn } from '@/shared/components/ui/utils'
import { formatCurrency, formatNumber } from '@/shared/utils'
import { EditableDataTable, type EditableColumnDef } from '@/modules/KetoanApp/components'
```

---

## 11. Checklist Tạo Dialog Full-Screen

- [ ] DialogContent có `maxWidth='none'` + full viewport classes
- [ ] KHÔNG dùng `DialogHeader`, `DialogTitle`, `DialogFooter` — custom div thay thế
- [ ] Header: `flex-shrink-0 border-b`, title + refType + Tổng tiền + nút X (unsaved guard)
- [ ] Body: `flex-1 min-h-0 overflow-hidden bg-[#f4f5f7] flex flex-col` — KHÔNG scroll body
- [ ] Info section: `p-5 pb-0 flex-shrink-0` — cố định trên cùng
- [ ] Table section: `p-5 pt-4 flex-1 min-h-0 flex flex-col` — fill hết chiều cao còn lại
- [ ] 2-cột layout: trái `flex-1`, phải `w-[250px] flex-shrink-0`, gap `gap-6`
- [ ] Cột trái: fields theo yêu cầu (grid-cols-2 hoặc full-width)
- [ ] Cột phải: Ngày hạch toán + Ngày chứng từ + Số phiếu (tối thiểu) + `onBlur` + `*` required + error message
- [ ] Bảng dữ liệu bọc trong white card: `bg-white rounded-lg shadow-sm overflow-hidden flex flex-col flex-1 min-h-0`
- [ ] Tab header: `flex-shrink-0` — cố định không scroll
- [ ] Table scroll area: `flex-1 min-h-0 overflow-y-auto` — chỉ bảng scroll
- [ ] Sum row: `bg-[#ECEDEF] border-t border-solid border-[#B7BCC3]`
- [ ] Footer: `py-2.5 flex-shrink-0 border-t`, buttons theo mode
- [ ] Nút X ẩn mặc định bằng `[&>button:first-child]:hidden`
- [ ] Loading state: spinner giữa body
- [ ] Buttons: `btn-secondary` / `btn-primary` — KHÔNG `variant='outline'`
- [ ] Input: `h-[30px]` form, `h-[26px]` trong bảng
- [ ] Label: `text-[13px] font-semibold text-black`
- [ ] Error: `<p className='text-xs text-destructive...'><AlertCircle />...</p>`
- [ ] Confirm dialogs: unsaved guard, clear all lines, post/unpost
- [ ] `dirtyRef` + `pendingCloseRef` cho unsaved changes tracking
