---
name: tao-bao-cao
description: 'Tạo hoặc chỉnh sửa trang Báo cáo (sổ sách/tổng hợp) trong KetoanApp. Mỗi báo cáo gồm 2 phần: Drawer tham số (phải, tự mở mặc định khi vào trang) + Master page kết quả (bảng có thể header đơn giản hoặc header nhóm cột, luôn có hàng Tổng cộng cố định). Đầu vào: tên báo cáo, danh sách tham số lọc, cấu trúc cột kết quả (đơn giản/nhóm), endpoint API.'
---

# Tạo Trang Báo Cáo — KetoanApp

> **Kế thừa:** `tao-master-page` (pattern 3-tầng header/body cố định — chỉ lấy Ý TƯỞNG, KHÔNG dùng chung component `DmTable*`), `dialog-drawer-ui` Pattern B (Right Drawer dùng `Sheet`), `tao-phieu-thu` Section 0.0 & 2 (header/body/Tổng cộng 3-tầng sticky, đồng bộ scroll ngang), `dat-ten` (quy tắc đặt tên).
>
> **Component bảng riêng cho báo cáo:** `ReportTable*` (`ReportTable`, `ReportTableHeader`, `ReportTableHeaderRow`, `ReportTableHead`, `ReportTableBody`, `ReportTableRow`, `ReportTableCell`) tại `features/bao-cao/shared/components/ReportTable.tsx`. Đây là bản sao có chỉnh sửa từ `DmTable.tsx` (component bảng của trang CRUD danh mục/nghiệp vụ) — **TUYỆT ĐỐI KHÔNG sửa `DmTable.tsx` gốc hay tái dùng `DmTable*` cho trang báo cáo**, để không ảnh hưởng các bảng CRUD đang chạy. Khác biệt chính: `ReportTableHead` có border đủ 4 cạnh (trên/dưới/hai bên) tạo khung lưới cho header theo đúng thiết kế mẫu; không có prop `pinned`/resize cột (báo cáo không cần ghim/resize).
>
> **Reference implementation:** `features/bao-cao/so-chi-tiet-cac-tai-khoan/` (SCTK) và `features/bao-cao/so-quy-tien-mat/` (SQTM — có header nhóm cột 2 dòng). Đọc code thật ở đây khi cần ví dụ đầy đủ.
>
> **Áp dụng cho:** TẤT CẢ báo cáo sổ sách/tổng hợp trong module Báo cáo (`features/bao-cao/{ten-bao-cao}/`) — bảng cân đối tài khoản, sổ quỹ tiền mặt, tổng hợp bán hàng, công nợ... Không áp dụng cho trang CRUD danh mục/nghiệp vụ (dùng `tao-master-page`/`tao-phieu-thu` thẳng).

---

## 0. Kiến Trúc Tổng Quan

```
Report Hub (KetoanBaoCaoPage)
  │  click báo cáo "active"
  ▼
navigateToPage('{report-id}')            ← điều hướng THẲNG, KHÔNG mở dialog/drawer ở Hub
  │
  ▼
{SN}Page.tsx (master page) mount
  │  useState(true) — drawer tham số TỰ MỞ ngay khi vào trang
  ▼
{SN}Drawer.tsx (đè lên master page đang hiển thị data mặc định/rỗng)
  │  user chỉnh tham số → [Xem báo cáo]
  ▼
validate → serialize query string → navigate() lại chính route đó → đóng drawer
  │
  ▼
use{SN}PageResult() đọc URL → gọi API báo cáo → render bảng kết quả
```

**Nguyên tắc cốt lõi — tách trách nhiệm dialog/page (BẮT BUỘC, giữ nguyên như SCTK):**
- `use{SN}DialogParam` (hook đứng sau Drawer): **CHỈ** validate + serialize params + `navigate()`. **KHÔNG BAO GIỜ** gọi API báo cáo.
- `use{SN}PageResult` (hook đứng sau Page): đọc query string từ URL, **là nơi DUY NHẤT gọi API báo cáo**, quản lý loading/phân trang.
- Đổi tham số → luôn đi qua URL (query string), không giữ state tham số rời rạc giữa 2 hook.

**Report Hub không còn sở hữu dialog/drawer tham số của bất kỳ báo cáo nào** — `handleSelectItem` cho báo cáo `active` chỉ `navigateToPage(item.id)`; trang báo cáo tự lo việc mở drawer mặc định.

---

## 1. Cấu Trúc File

```
features/bao-cao/{ten-bao-cao}/
├── types/{SN}.types.ts         ← Request/Response DTO (map 1:1 BE) + FormState + FormErrors
├── services/{SN}ApiService.ts  ← Gọi API báo cáo
├── hooks/
│   ├── use{SN}.dlg.param.ts    ← Validate + serialize params → navigate (KHÔNG gọi API báo cáo)
│   └── use{SN}.page.result.ts  ← Đọc URL → gọi API → phân trang (nơi DUY NHẤT gọi API báo cáo)
├── dialogs/
│   └── {SN}Drawer.tsx          ← Drawer tham số (Sheet, side='right')
├── pages/
│   └── {SN}Page.tsx            ← Master page kết quả
└── index.ts                    ← Barrel export
```

> Kỳ báo cáo dùng chung enum `ReportPeriodType` (0=Tùy chọn, 1=Tháng này, 2=Tháng trước, 3=Quý này, 4=Quý trước, 5=Năm nay, 6=Năm trước) và component `ReportPeriodPicker` từ `features/bao-cao/shared/components/` — KHÔNG định nghĩa lại.

---

## 2. Drawer Tham Số — `{SN}Drawer.tsx`

### 2.1 Quy tắc bắt buộc

| Thuộc tính | Giá trị |
|-----------|---------|
| Container | `Sheet` + `SheetContent side='right'` |
| Title | **LUÔN LUÔN** `"Tham số báo cáo"` — không đổi theo tên báo cáo |
| Width | `w-[560px]` (tham số đơn giản: chỉ kỳ báo cáo + vài field) đến `w-[900px]` (có bảng chọn nhiều dòng, vd danh sách tài khoản/khách hàng). Mặc định gợi ý: `720px` |
| Auto-open | Trang cha (`{SN}Page.tsx`) khởi tạo `useState(true)` — KHÔNG chờ user bấm nút mới hiện lần đầu |
| Footer trái | `[Hủy]` `[Xóa điều kiện]` |
| Footer phải | `[Xem báo cáo]` (`btn-primary`) |

### 2.2 Code mẫu

```tsx
import { X } from 'lucide-react'
import { Sheet, SheetContent } from '@/shared/components/ui/sheet'
import { Button } from '@/shared/components/ui/button'
import { ReportPeriodPicker } from '@/modules/KetoanApp/features/bao-cao/shared/components'
import { use{SN}DialogParam } from '../hooks'
import type { {SN}FormState } from '../types'

interface {SN}DrawerProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  initialParams?: {SN}FormState
}

export function {SN}Drawer({ open, onOpenChange, initialParams }: {SN}DrawerProps) {
  const { formData, setFormData, errors, touched, handleBlur, handleSubmit, handleReset } =
    use{SN}DialogParam({ initialParams, onClose: () => onOpenChange(false), open })

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side='right'
        className='ketoan-app w-[720px] sm:max-w-[720px] p-0 gap-0 flex flex-col h-full [&>button]:hidden'
      >
        {/* Header — title CỐ ĐỊNH */}
        <div className='flex items-center justify-between px-5 py-3 border-b border-[#B7BCC3] flex-shrink-0'>
          <span className='text-[20px] font-bold text-gray-900'>Tham số báo cáo</span>
          <Button variant='ghost' size='sm'
            className='h-7 w-7 p-0 text-gray-400 hover:text-gray-600 rounded-[8px]'
            onClick={() => onOpenChange(false)} data-qa='btn_dong_drawer'>
            <X className='h-4 w-4' />
          </Button>
        </div>

        {/* Body — tham số riêng từng báo cáo */}
        <div className='flex-1 min-h-0 overflow-y-auto px-5 py-4 space-y-4'>
          <ReportPeriodPicker
            periodType={formData.periodType}
            fromDate={formData.fromDate}
            toDate={formData.toDate}
            onPeriodTypeChange={v => setFormData(prev => ({ ...prev, periodType: v }))}
            onFromDateChange={v => setFormData(prev => ({ ...prev, fromDate: v }))}
            onToDateChange={v => setFormData(prev => ({ ...prev, toDate: v }))}
            onBlurFromDate={() => handleBlur('fromDate')}
            onBlurToDate={() => handleBlur('toDate')}
            fromDateError={errors.fromDate}
            toDateError={errors.toDate}
            fromDateTouched={touched.fromDate}
            toDateTouched={touched.toDate}
          />
          {/* ... các field lọc riêng của báo cáo (bảng chọn tài khoản/khách hàng, checkbox...) */}
        </div>

        {/* Footer — trái Hủy/Xóa điều kiện, phải Xem báo cáo */}
        <div className='flex items-center justify-between gap-3 px-5 py-3 border-t border-[#B7BCC3] flex-shrink-0 bg-white'>
          <div className='flex gap-2'>
            <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_huy'
              onClick={() => onOpenChange(false)}>Hủy</Button>
            <Button className='btn-secondary h-8 text-[13px] rounded-lg' data-qa='btn_xoa_dieu_kien'
              onClick={handleReset}>Xóa điều kiện</Button>
          </div>
          <Button className='btn-primary h-8 text-[13px] rounded-lg' data-qa='btn_xem_bao_cao'
            onClick={handleSubmit}>Xem báo cáo</Button>
        </div>
      </SheetContent>
    </Sheet>
  )
}
```

### 2.3 Hành vi 3 nút footer

| Nút | Hành vi |
|-----|---------|
| `Hủy` | Đóng drawer, **không** navigate, **không** đổi dữ liệu đang hiển thị trên master page |
| `Xóa điều kiện` | Reset form về mặc định, **không** đóng drawer (user xem lại rồi mới bấm Xem báo cáo) |
| `Xem báo cáo` | Validate → serialize query string → `navigate()` sang chính route đó với params mới → đóng drawer |

---

## 3. Master Page Kết Quả — `{SN}Page.tsx`

### 3.0 Khung trang dùng chung — BẮT BUỘC dùng `ReportMasterLayout`

> `ReportMasterLayout` (`features/bao-cao/shared/components/ReportMasterLayout.tsx`) bọc toàn bộ phần khung lặp lại giữa các báo cáo: back+breadcrumb, "Chọn tham số", card trắng, toolbar, tên bảng, loading/empty state, pagination. **KHÔNG tự dựng lại khung này trong từng `{SN}Page.tsx`** — chỉ viết phần bảng riêng (`children`).

```
┌ Ngoài card ─────────────────────────────────────────────────────┐
│ [←] Báo cáo > {Tên báo cáo}         "Danh sách báo cáo đã lưu"  [Chọn tham số] │
└───────────────────────────────────────────────────────────────────┘
┌ Card trắng (bg-white rounded-xl) ─────────────────────────────────┐
│ [toolbarLeft — tuỳ báo cáo]           [search + toolbarRight — tuỳ báo cáo] │
│                    TÊN BÁO CÁO IN HOA (căn giữa)                  │
│ ┌─ children: Header bảng — LUÔN hiện kể cả khi rỗng ─────────────┐ │
│ ├─ children: Body bảng (scroll dọc + ngang) ─────────────────────┤ │
│ └─ children: Tổng cộng — LUÔN hiện kể cả khi rỗng ────────────────┘ │
│ [pagination — nếu báo cáo có phân trang]                          │
└─────────────────────────────────────────────────────────────────┘
```

> ⚠️ **TUYỆT ĐỐI KHÔNG dùng `sticky`/margin âm** (`sticky -top-6 ... -mx-6 -mt-6`) cho khối ngoài cùng. `<main>` của `KetoanPortal` (layout chứa mọi trang KetoanApp) **KHÔNG có padding nào để bù trừ** — dùng hack này từng đẩy thanh trên của trang báo cáo đè lên navbar chính (52px, z-30) khiến nút "Chọn tham số" và link "Danh sách báo cáo đã lưu" bị navbar che mất một phần. `ReportMasterLayout` đã dùng đúng pattern `px-3 md:px-6 py-3` (giống `DmPageHeader`, không sticky) — không cần và không được thêm sticky/margin âm nữa.

> **`onBack` — quay lại Report Hub PHẢI mở đúng tab/danh mục báo cáo vừa rời đi**, không phải mặc định tab "Tất cả" + danh mục đầu tiên. Truyền query string `tab`/`category` qua `navigateToPage`'s `options.search` (đã hỗ trợ sẵn ở `KetoanNavigationContext`); `KetoanBaoCaoPage` tự đọc `?tab=...&category=...` để khởi tạo `activeTab`/`activeCategoryKey` lúc mount:
> - Báo cáo thuộc 1 category trong `REPORT_CATEGORIES` (`reportCatalog.ts`) → `navigateToPage('bao-cao', { search: 'tab=all&category={categoryKey}' })`
> - Báo cáo đặt tạm ở tab "Khác" (`OTHER_TAB_SECTIONS` trong `KetoanBaoCaoPage.tsx`, như SCTK) → `navigateToPage('bao-cao', { search: 'tab=other' })`

```tsx
import { ReportMasterLayout } from '@/modules/KetoanApp/features/bao-cao/shared/components'

<ReportMasterLayout
  reportLabel='Sổ quỹ tiền mặt'                      // breadcrumb "Báo cáo > {reportLabel}"
  onBack={() => navigateToPage('bao-cao', { search: 'tab=all&category=tien-mat' })}
  onOpenParamDrawer={() => setParamDrawerOpen(true)}
  tableTitle={data?.title ?? 'Sổ quỹ tiền mặt'}       // in hoa, căn giữa (tự động)
  tableSubTitle={data?.subTitle}
  loading={loading}                                   // CHỈ trạng thái đang fetch — không có prop hasData/emptyMessage
  toolbarLeft={/* tuỳ báo cáo — được phép để trống */}
  toolbarRight={/* search + refresh/export/mail/print... — xem bên dưới */}
  pagination={hasData && <DmTablePagination ... />}    // trang tự quyết định ẩn/hiện theo hasData
>
  {/* Header LUÔN render, Tổng cộng LUÔN render — chỉ phần rows bên trong Body đổi theo hasData/kết quả tìm kiếm — xem Section 3.2 */}
</ReportMasterLayout>
```

- **`toolbarLeft`/`toolbarRight`:** action tuỳ báo cáo, được phép để trống nếu không cần. **Chỉ bật icon nào có chức năng thật — không dựng UI giả không nối logic.** `DmSearchToolbar` có sẵn ở `src/modules/KetoanApp/components` nhưng cố định search bên trái, không phù hợp bố cục "trái action, phải search+action" — tự dựng `Input` + icon `Search` (lucide-react) trong `toolbarRight`, đặt trước các nút action, không cần `DmSearchToolbar`.
- **Ô tìm kiếm — lọc phía CLIENT trên dữ liệu đã tải, KHÔNG gọi lại API báo cáo:** dùng `useState` cho `searchText` + `useMemo` lọc mảng rows đã có sẵn theo các field text liên quan (diễn giải/số chứng từ/ghi chú...). Xem `SQTMPage.tsx`/`SCTKPage.tsx` làm mẫu. Khi có tìm kiếm mà không khớp dòng nào → hiện `"Không tìm thấy dữ liệu phù hợp"` (khác với `"Không có dữ liệu"` khi API chưa trả về gì).
- **Hàng Tổng cộng khi đang lọc:** tính lại tổng từ tập đã lọc (`filteredRows.reduce(...)`) thay vì dùng thẳng tổng do API trả (`grandTotal*`), để không gây hiểu nhầm số liệu — trừ các trường không có ý nghĩa cộng dồn theo tập con (vd Tồn/Dư lũy kế) thì vẫn giữ nguyên giá trị API.
- **`hasData`/`loading`/`emptyMessage`:** `ReportMasterLayout` tự xử lý 3 trạng thái (loading → `PageLoader`, `!hasData` → text rỗng, còn lại → render `children` + `pagination`). Trang `{SN}Page.tsx` **không cần** tự viết `if (loading) ... else if (!hasData) ...` nữa.
- **`children`:** CHỈ chứa bảng 3-tầng (`ReportTable*`) — xem Section 3.2. Không bọc thêm `div` ngoài cùng khác vì `ReportMasterLayout` đã lo phần card/toolbar/title.

### 3.2 Bảng kết quả — BẮT BUỘC dùng `ReportTable*`, KHÔNG dùng `Table` shadcn thô, KHÔNG dùng `DmTable*`

> Ý tưởng 3-tầng lấy từ `tao-phieu-thu` Section 0.0 (3-tầng) và Section 2 (hàng Tổng cộng), nhưng component thực tế là `ReportTable*` (`features/bao-cao/shared/components/ReportTable.tsx`) — bảng dùng riêng cho báo cáo, tách biệt hoàn toàn khỏi `DmTable*` của trang CRUD. Khác biệt cho báo cáo: **không có checkbox/cột action**, **header có thể là nhóm cột 2 dòng**, và **header có border đủ 4 cạnh** (tự động, không cần thêm class).

```tsx
import {
  ReportTable, ReportTableHeader, ReportTableHeaderRow, ReportTableHead,
  ReportTableBody, ReportTableRow, ReportTableCell,
} from '@/modules/KetoanApp/features/bao-cao/shared/components'
```

#### 3.2.1 Ref & đồng bộ scroll ngang — BẮT BUỘC có ghost scrollbar

> ⚠️ **Không được bỏ qua ghost scrollbar.** Nếu chỉ dùng `overflow-auto` trơn trên body, scrollbar gốc của trình duyệt bị CSS toàn cục làm mờ 50% + cao 8px (xem `src/styles/globals.css`) nên **hầu như không nhìn thấy được** dù bảng có tràn ngang — người dùng sẽ tưởng bảng không scroll được. Bắt buộc: ẩn scrollbar gốc bằng class `scrollbar-hidden` trên body, thay bằng 1 thanh ghost scrollbar riêng luôn hiển thị rõ, đồng bộ 2 chiều với body.

```tsx
const headerRef = useRef<HTMLDivElement>(null)
const bodyRef = useRef<HTMLDivElement>(null)
const totalRef = useRef<HTMLDivElement>(null)
const ghostRef = useRef<HTMLDivElement>(null)
const syncingScroll = useRef(false)

const handleBodyScroll = useCallback(() => {
  const sl = bodyRef.current?.scrollLeft ?? 0
  if (headerRef.current) headerRef.current.scrollLeft = sl
  if (totalRef.current) totalRef.current.scrollLeft = sl
  if (!syncingScroll.current && ghostRef.current) {
    syncingScroll.current = true
    ghostRef.current.scrollLeft = sl
    syncingScroll.current = false
  }
}, [])

const handleGhostScroll = useCallback(() => {
  if (syncingScroll.current || !bodyRef.current || !ghostRef.current) return
  syncingScroll.current = true
  bodyRef.current.scrollLeft = ghostRef.current.scrollLeft
  syncingScroll.current = false
  handleBodyScroll() // đồng bộ tiếp header/total theo vị trí mới
}, [handleBodyScroll])
```

#### 3.2.2 Layout JSX — header đơn giản (1 dòng)

```tsx
<div className='flex-1 min-h-0 flex flex-col'>
  {/* Header — cố định trên */}
  <div ref={headerRef} className='shrink-0 overflow-hidden'>
    <ReportTable style={{ minWidth: MIN_TABLE_WIDTH }}>
      <colgroup>{COLUMNS.map(c => <col key={c.field} style={{ width: c.width }} />)}</colgroup>
      <ReportTableHeader>
        <ReportTableHeaderRow>
          {COLUMNS.map(c => (
            <ReportTableHead key={c.field} className={c.align === 'right' ? 'text-right' : undefined}>
              {c.label}
            </ReportTableHead>
          ))}
        </ReportTableHeaderRow>
      </ReportTableHeader>
    </ReportTable>
  </div>

  {/* Body — scroll dọc + ngang. scrollbar-hidden BẮT BUỘC (xem 3.2.1) */}
  <div ref={bodyRef} className='flex-1 min-h-0 overflow-auto scrollbar-hidden' onScroll={handleBodyScroll}>
    <ReportTable style={{ minWidth: MIN_TABLE_WIDTH }}>
      <colgroup>{COLUMNS.map(c => <col key={c.field} style={{ width: c.width }} />)}</colgroup>
      <ReportTableBody>
        {rows.map(row => (
          <ReportTableRow key={row.id}>
            {COLUMNS.map(c => (
              <ReportTableCell key={c.field} className={c.align === 'right' ? 'text-right' : undefined}>
                {renderCell(c, row)}
              </ReportTableCell>
            ))}
          </ReportTableRow>
        ))}
      </ReportTableBody>
    </ReportTable>
  </div>

  {/* Tổng cộng — cố định dưới, LUÔN hiện khi có data (xem tao-phieu-thu Section 2.2.3) */}
  {rows.length > 0 && (
    <div ref={totalRef} className='shrink-0 overflow-hidden'>
      <ReportTable style={{ minWidth: MIN_TABLE_WIDTH }}>
        <colgroup>{COLUMNS.map(c => <col key={c.field} style={{ width: c.width }} />)}</colgroup>
        <ReportTableBody>
          <ReportTableRow className='bg-[#ECEDEF] border-t-2 border-[#ced1d6] font-semibold hover:bg-[#ECEDEF]'>
            {COLUMNS.map((c, idx) => (
              <ReportTableCell key={c.field} className={c.align === 'right' ? 'text-right' : undefined}>
                {idx === 0 ? 'Tổng cộng' : (c.totalField ? formatNumber(totals[c.totalField]) : '')}
              </ReportTableCell>
            ))}
          </ReportTableRow>
        </ReportTableBody>
      </ReportTable>
    </div>
  )}

  {/* Ghost scrollbar — luôn hiển thị rõ, đồng bộ scroll ngang với body (BẮT BUỘC, xem 3.2.1) */}
  <div ref={ghostRef} className='overflow-x-auto shrink-0' onScroll={handleGhostScroll}>
    <div style={{ minWidth: MIN_TABLE_WIDTH, height: 1 }} />
  </div>
</div>
```

#### 3.2.3 Header nhóm cột (phức tạp, 2 dòng — vd Bảng cân đối tài khoản, Sổ quỹ tiền mặt)

Dùng 2 `ReportTableHeaderRow`: cột **không nhóm** (Số tài khoản, Tên tài khoản) dùng `rowSpan={2}`; cột **nhóm** (Đầu kỳ, Phát sinh, Cuối kỳ) dùng `colSpan` ở dòng 1, các cột con (Nợ/Có...) ở dòng 2:

```tsx
<ReportTableHeader>
  <ReportTableHeaderRow>
    <ReportTableHead rowSpan={2}>Số tài khoản</ReportTableHead>
    <ReportTableHead rowSpan={2}>Tên tài khoản</ReportTableHead>
    <ReportTableHead colSpan={2} className='text-center'>Đầu kỳ</ReportTableHead>
    <ReportTableHead colSpan={4} className='text-center'>Phát sinh</ReportTableHead>
    <ReportTableHead colSpan={2} className='text-center'>Cuối kỳ</ReportTableHead>
  </ReportTableHeaderRow>
  <ReportTableHeaderRow>
    <ReportTableHead className='text-right'>Nợ</ReportTableHead>
    <ReportTableHead className='text-right'>Có</ReportTableHead>
    <ReportTableHead className='text-right'>Nợ</ReportTableHead>
    <ReportTableHead className='text-right'>Có</ReportTableHead>
    <ReportTableHead className='text-right'>Nợ lũy kế</ReportTableHead>
    <ReportTableHead className='text-right'>Có lũy kế</ReportTableHead>
    <ReportTableHead className='text-right'>Nợ</ReportTableHead>
    <ReportTableHead className='text-right'>Có</ReportTableHead>
  </ReportTableHeaderRow>
</ReportTableHeader>
```

> **`colgroup` phải có đúng số `<col>` bằng tổng số cột LÁ** (8 cột con ở ví dụ trên, không tính cột nhóm) — giống hệt số cột trong `ReportTableBody`. `border-collapse` trên `ReportTable` tự động vẽ khung lưới quanh mọi ô header kể cả ô `rowSpan`/`colSpan`.

### 3.3 Độ rộng cột — không cắt chữ header

- Mỗi cột khai báo `width` cố định (px) đủ hiển thị **toàn bộ** label header không bị wrap/truncate (ước lượng ~`8-9px` mỗi ký tự + `24px` padding, làm tròn lên).
- `MIN_TABLE_WIDTH = tổng width tất cả cột`. Khi `MIN_TABLE_WIDTH` > khung nhìn card → 3 tầng bảng tự scroll ngang đồng bộ qua `handleBodyScroll`, hiển thị qua ghost scrollbar (xem 3.2.1) — KHÔNG dựa vào scrollbar gốc của trình duyệt.
- KHÔNG dùng `truncate` trên `ReportTableHead` cho báo cáo (khác với CRUD table) — header báo cáo luôn hiện đầy đủ chữ.

### 3.4 Các thành phần dùng chung khác

| Thành phần | Dùng khi |
|-----------|---------|
| `ReportMasterLayout` (`features/bao-cao/shared/components`) | Khung trang — xem Section 3.0. `PageLoader` + empty-state đã tích hợp sẵn bên trong, không cần tự viết. |
| `ValidationErrorDialog` (`@/shared/components/common`) | Lỗi trả về từ server — render ngoài `ReportMasterLayout`, cùng cấp `{SN}Drawer` |
| `DmTablePagination` (`@/modules/KetoanApp/components`) | Báo cáo có phân trang server — truyền vào prop `pagination` của `ReportMasterLayout`, props riêng `total/page/limit/onPageChange/onLimitChange`. Component này KHÔNG thuộc bộ `ReportTable*`, vẫn dùng chung với CRUD vì không phải là bảng dữ liệu. |

---

## 4. Đăng Ký Route & Catalog (khi báo cáo chuyển từ `coming-soon` → thật)

1. Build đủ `types/services/hooks/dialogs/pages` theo cấu trúc Section 1.
2. Thêm route con trong `src/modules/KetoanApp/routes/routeConfig.tsx` — **PHẢI đặt TRƯỚC route cha `bao-cao`** (React Router match theo thứ tự khai báo):
   ```tsx
   { path: 'bao-cao/{report-id}', element: <{SN}Page />, pageId: '{report-id}', mainMenu: 'dashboard' },
   ```
   và thêm entry vào `pageIdToPath` map cùng file.
3. Trong `reportCatalog.ts`, đổi `status: 'coming-soon'` → `'active'` cho item tương ứng.
4. Trong `KetoanBaoCaoPage.handleSelectItem`, thêm nhánh cho id báo cáo đó gọi `navigateToPage('{report-id}')` (KHÔNG mở dialog/drawer ở Hub).

---

## 5. Checklist Trước Khi Báo Cáo Hoàn Thành

- [ ] Hook `dlg.param` chỉ validate + navigate, **không** gọi API báo cáo
- [ ] Hook `page.result` đọc URL, là nơi **duy nhất** gọi API báo cáo
- [ ] Drawer dùng `Sheet side='right'`, title cố định `"Tham số báo cáo"`
- [ ] Drawer **tự mở mặc định** (`useState(true)`) khi vào trang, Hub không mở hộ
- [ ] Footer drawer đúng bố cục: trái `[Hủy][Xóa điều kiện]`, phải `[Xem báo cáo]`
- [ ] Master page dùng `ReportMasterLayout` (KHÔNG tự dựng lại khung trang, KHÔNG dùng `sticky`/margin âm cho khối ngoài cùng — `main` của `KetoanPortal` không có padding để bù trừ, sticky/margin âm sẽ đè lên navbar chính)
- [ ] `{SN}Page.tsx` chỉ chứa bảng 3-tầng trong `children` của `ReportMasterLayout` — back/breadcrumb/toolbar/title/loading/empty/pagination đều do `ReportMasterLayout` xử lý
- [ ] Toolbar (`toolbarLeft`/`toolbarRight`): trái action / phải search+action — chỉ bật icon có chức năng thật; ô search (nếu có) lọc CLIENT-SIDE trên data đã tải, KHÔNG gọi lại API
- [ ] Tên bảng in hoa, căn giữa, mặc định = title từ API
- [ ] Bảng dùng `ReportTable/ReportTableHeader/ReportTableHeaderRow/ReportTableHead/ReportTableBody/ReportTableRow/ReportTableCell` (`features/bao-cao/shared/components/ReportTable.tsx`) — KHÔNG dùng `Table` shadcn thô, KHÔNG dùng `DmTable*`
- [ ] Header hỗ trợ cả đơn giản (1 dòng) và nhóm cột (`colSpan`/`rowSpan`, 2 dòng) tuỳ báo cáo — mỗi ô header có border đủ 4 cạnh (tự động từ `ReportTableHead`), CĂN GIỮA mặc định (tự động từ `ReportTableHead`, override bằng `text-right`/`text-left` khi cần)
- [ ] 3 tầng header/body/total tách riêng, đồng bộ scroll ngang qua ref
- [ ] **Header và hàng Tổng cộng LUÔN hiện — kể cả khi chưa có dữ liệu** (nằm ngoài vùng scroll dọc của body). Chỉ phần BODY đổi theo trạng thái: dòng dữ liệu thật, hoặc 1 dòng `colSpan={COLUMNS.length}` hiện `"Không có dữ liệu"` / `"Không tìm thấy dữ liệu phù hợp"` (khi đang lọc). KHÔNG thay cả `children` bằng text rỗng như cách làm cũ (từng khiến header/Tổng cộng biến mất theo).
- [ ] Cột đủ rộng hiển thị full header, bảng rộng quá thì scroll ngang (không wrap/truncate header)
- [ ] **Ghost scrollbar bắt buộc:** body có `scrollbar-hidden`, có `ghostRef` riêng luôn hiển thị rõ + đồng bộ 2 chiều — không dựa vào scrollbar gốc trình duyệt (bị làm mờ 50% qua CSS toàn cục, dễ bị tưởng "không scroll được")
- [ ] Route đăng ký đúng thứ tự (con trước cha) + `pageIdToPath` + `reportCatalog.ts` status `'active'` + nhánh `handleSelectItem` ở Hub
