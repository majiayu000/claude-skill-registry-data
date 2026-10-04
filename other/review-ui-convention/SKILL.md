---
name: review-ui-convention
description: 'Review UI convention của page/dialog/form KetoanApp — đối chiếu với tao-ui-giao-dien-new Section 12 (format, alignment, CELL_VALUE, CELL_CLASS, truncate, column width, button, icon, data-qa) + tao-phieu-thu Section 1 (isPosted colors, refNo blue, amber, badge, total row). Dùng khi: kiểm tra giao diện, review UI, kiểm tra convention, review page/dialog, soát lỗi UI.'
argument-hint: 'Đường dẫn file page hoặc dialog cần review...'
---

# Review UI Convention — KetoanApp

> **Mục đích:** Rà soát toàn bộ giao diện 1 file page/dialog KetoanApp, đảm bảo tuân thủ tất cả quy tắc UI trong `tao-ui-giao-dien-new` và `tao-phieu-thu`.
>
> **Đối tượng:** File `.tsx` — Master Page, Dialog, hoặc Sub Page.
>
> **Kết quả:** Báo cáo chi tiết từng vi phạm kèm vị trí (dòng) + suggested fix + phân loại Critical / Warning / Info.

---

## Quy Trình

### Bước 1 — Load prompt review

Đọc file `.github/prompts/prompt-review-ui-convention.md` — đây là checklist đầy đủ 14 mục (A→N).

### Bước 2 — Đọc & phân loại file

`read_file` file cần review. Xác định loại (page/dialog/sub-page), có `isPosted` không, có `CELL_VALUE`/`CELL_CLASS`/`getCellClass`/`ALL_COLUMNS` không.

### Bước 3 — Chạy từng mục kiểm tra

Thực hiện tuần tự các mục trong prompt:
- **A**: Phân loại file
- **B**: CELL_VALUE (format đúng? thiếu key? dùng `'-'`?)
- **C**: CELL_CLASS (đủ class? đúng class?)
- **D**: Alignment (text-right cho số, text-center cho badge)
- **E**: getCellClass (màu isPosted, refNo blue)
- **F**: Badge (pill, màu đúng state)
- **G**: truncate & tooltip
- **H**: Độ rộng cột
- **I**: Hàng tổng cộng (nếu có)
- **J**: Button & icon
- **K**: Data QA
- **L**: Dialog structure (nếu là dialog) + DmValidatedInput email/phone/website
- **M**: Master Page structure (nếu là page)

### Bước 4 — Tổng hợp báo cáo

Xuất báo cáo theo format mục N trong prompt:
- ✅ Pass items
- ❌ Vi phạm (Critical / Warning / Info)
- Điểm tuân thủ (%)

---

## 🔥 Lỗi Hay Gặp Khi Review (Checklist Bổ Sung)

> **Mục đích:** Danh sách các lỗi lặp đi lặp lại qua các lần review, giúp agent review và developer tránh ngay từ đầu.

### 1. ⚠️ Dùng `formatCurrency()` thay vì `formatNumber()` trong table list

**Vị trí:** `CELL_VALUE` của Master Page, các cột số tiền (`totalAmount`, `amount`...)

```
❌ SAI: formatCurrency(i.totalAmount) → "1,500,000 ₫"
✅ ĐÚNG: formatNumber(i.totalAmount)   → "1,500,000"
```

**Quy tắc:** Trong danh sách bảng, dùng `formatNumber()`. `formatCurrency()` chỉ dùng trong dialog/view hiển thị tiền tệ đầy đủ.

### 2. ⚠️ Dùng `|| '-'` hoặc `?? '-'` làm fallback

**Vị trí:** `CELL_VALUE`, `DmTableCell` children

```
❌ SAI: item.voucherCode || '-'
✅ ĐÚNG: item.voucherCode || ''
```

**Quy tắc:** Ô trong bảng mà không có dữ liệu → để trống `''`, không dùng dấu gạch ngang `'-'`.

### 3. ⚠️ Thiếu 3-tầng bảng Header/Body/Footer

**Vị trí:** Master Page JSX

**Dấu hiệu:** Toàn bộ bảng (header + body) nằm trong 1 `<DmTable>` duy nhất.

**Quy tắc:** Header phải nằm riêng với `shrink-0 overflow-hidden`, body trong `flex-1 overflow-auto`. Tham khảo `PhieuThuPage.tsx`.

### 4. ⚠️ Thiếu `<colgroup>` + `getColumnWidth` + `useColumnResize`

**Dấu hiệu:** `col.width` được dùng trực tiếp trong `style={{ width: col.width }}`.

```
❌ SAI: style={{ width: col.width }}
✅ ĐÚNG: style={{ width: getColumnWidth(col.id, col.width) }}
        + dùng colgroup trong <DmTable>
        + dùng useColumnResize({ columns, tableRef })
        + đồng bộ headerScrollRef
```

### 5. ⚠️ Nút "Thêm mới" không ở vị trí bên phải cùng trong toolbar

**Vị trí:** `DmSearchToolbar extraActions` — cùng hàng với các công cụ "Làm mới", "Xuất khẩu"

**Quy tắc:** Nút "Thêm mới" PHẢI nằm bên phải cùng trong thanh toolbar (`DmSearchToolbar.extraActions`), cùng hàng với các công cụ "Làm mới", "Xuất khẩu". KHÔNG đặt trong `DmPageHeader actions` (hàng riêng biệt). Nút "Thêm mới" là phần tử CUỐI CÙNG trong `extraActions`, sau tất cả các nút tiện ích.

```
❌ SAI: [Thêm mới] nằm trong DmPageHeader actions (hàng riêng, tách biệt khỏi toolbar)
❌ SAI: [Thêm mới] [search] [filters] ... [Làm mới] [Xuất Excel] [Thiết lập bảng] (Thêm mới bên trái)
✅ ĐÚNG: [search] [filters] ... [Làm mới] [Xuất Excel] [Thiết lập bảng] [Thêm mới] (Thêm mới bên phải cùng, sau tất cả nút tiện ích)
```

### 6. ⚠️ Font chữ trong dialog không đồng nhất

**Dấu hiệu:** Font trong form dialog khác font của body.

**Nguyên nhân:** `font-family` bị set cục bộ trên component nào đó.

**Quy tắc:** KHÔNG set `font-family` ở bất kỳ đâu. Font kế thừa từ `body` (`globals.css`). Nếu dùng Radix/Portal → kiểm tra không có CSS reset font trong portal.

### 7. ⚠️ Nút (+) tạo nhanh FK không hoạt động

**Vị trí:** `TableSearchCombobox` / `SearchCombobox` cho các field FK (Nhà cung cấp, Hàng hóa, Kho, Nhân viên...)

**Dấu hiệu:** Không có `showQuickAdd` prop → không có nút (+) bên cạnh dropdown.

```
❌ SAI: <TableSearchCombobox ... loadOptions={loadNCC} columns={nccColumns} />
✅ ĐÚNG: <TableSearchCombobox ... showQuickAdd loadOptions={loadNCC} columns={nccColumns}
           onCreateClick={() => { setNccDialogOpen(true) }} />
```

**Quy tắc:** MỌI `TableSearchCombobox` dùng để chọn FK (đối tượng, danh mục) PHẢI có `showQuickAdd` + `onCreateClick` mở dialog tạo nhanh.

### 8. ⚠️ Cột checkbox không hiển thị nhưng vẫn có BulkActionBar

**Dấu hiệu:** Có `BulkActionBar` khi `selection.selectedCount > 0` nhưng trong bảng không có checkbox column.

**Quy tắc:** Nếu dùng `BulkActionBar` → phải có cột checkbox đầu tiên trong bảng để user chọn.

### 9. ⚠️ Thiếu `group` class trên `DmTableRow` → ghost action không hiện

**Dấu hiệu:** Hover vào row không hiện các nút action.

```
❌ SAI: <DmTableRow className={cn(!item.isPosted && 'text-amber-700')}>
✅ ĐÚNG: <DmTableRow className={cn('group', !item.isPosted && 'text-amber-700')}>
```

### 10. ⚠️ Import `formatCurrency` sai path (TLHM, GGHM dialogs)

**Dấu hiệu:** Import từ `@/shared/InvoiceDesigner/utils/data-binding.utils`

```
❌ SAI: import { formatCurrency } from '@/shared/InvoiceDesigner/utils/data-binding.utils'
✅ ĐÚNG: import { formatCurrency } from '@/shared/utils'
```

### 11. ⚠️ Cố định header/footer trong master page

**Vị trí:** Master Page JSX — `DmPageHeader`, `DmTablePagination`, footer area

**Dấu hiệu:** Dùng `sticky top-0`, `fixed`, `position: sticky`, `position: fixed` cho header hoặc pagination footer.

```
❌ SAI: <div className="sticky top-0 z-10 bg-white">  (DmPageHeader)
        <div className="sticky bottom-0 z-10 bg-white"> (pagination)
✅ ĐÚNG: <div className="shrink-0">  (DmPageHeader — scroll cùng page)
        <div className="shrink-0">  (pagination — scroll cùng page)
```

**Quy tắc:** KHÔNG cố định header hay footer trong master page. Header và pagination phải scroll tự nhiên cùng nội dung trang. Layout chuẩn: `DmPageHeader (shrink-0)` → `DmSearchToolbar (shrink-0)` → `DmTable (flex-1 overflow-auto)` → `DmTablePagination (shrink-0)` — tất cả trong cùng 1 flex column container.

### 12. ⚠️ Resize cột trong master page

**Vị trí:** Master Page — `useColumnResize`, `getColumnWidth`, `colgroup`

**Dấu hiệu:** Có `useColumnResize` hook, `getColumnWidth`, hoặc `<colgroup>` trong bảng master page.

```
❌ SAI: const { getColumnWidth } = useColumnResize({ columns, tableRef })
        <colgroup>...</colgroup>
        style={{ width: getColumnWidth(col.id, col.width) }}
✅ ĐÚNG: style={{ width: col.width }}  (cố định, không resize)
```

**Quy tắc:** KHÔNG dùng resize cột trong master page. Các cột có độ rộng cố định (`width` trong `ALL_COLUMNS`). Không dùng `useColumnResize`, không dùng `getColumnWidth`, không dùng `<colgroup>`.

---

## Kỹ Năng Liên Quan

| Khi cần | Load skill |
|---------|-----------|
| Quy tắc format gốc | `tao-ui-giao-dien-new` |
| Quy tắc màu phiếu thu/chi | `tao-phieu-thu` |
| Quy tắc master page | `tao-master-page` |
| Quy tắc dialog | `tao-dialog-new` |
| Quy tắc button/foundation | `tao-ui-giao-dien` |

---

## Ví Dụ Sử Dụng

```
User: review UI convention file src/modules/KetoanApp/features/phieu-thu/pages/PhieuThuPage.tsx
Agent: [Đọc prompt-review-ui-convention.md] → [Đọc file] → [Chạy A→N] → [Báo cáo]
```
