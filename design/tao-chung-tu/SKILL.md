---
name: tao-chung-tu
description: 'Gắn field "Tham chiếu chứng từ" (chọn 1 hoặc nhiều chứng từ, từ nhiều loại nghiệp vụ khác nhau: mua hàng, bán hàng, thu chi, kho...) vào bất kỳ dialog/drawer nghiệp vụ nào trong KetoanApp — dùng component dùng chung `ChonChungTuThamChieuDrawer` + `ThamChieuChungTuField`. Bao gồm: cách nhúng field vào 1 form mới, cách đăng ký thêm 1 loại chứng từ vào registry, cách bật deep-link `?view={id}` để trang đích tự mở dialog xem chi tiết khi click số chứng từ ở tab mới.'
argument-hint: 'Tên form cần thêm field tham chiếu chứng từ. VD: Thêm field tham chiếu chứng từ vào GGHBDialog'
---

# Tham Chiếu Chứng Từ — Component Dùng Chung

> **Mục tiêu:** Cho phép 1 form nghiệp vụ (VD: Chứng từ mua hàng) "tham chiếu" tới 1 hoặc
> nhiều chứng từ khác (có thể thuộc loại nghiệp vụ khác — bán hàng, thu chi, kho...) mà
> KHÔNG phải tự viết lại UI chọn chứng từ mỗi lần. Chỉ cần nhúng 1 component có sẵn.

**Đã triển khai tham khảo tại:** `CTMHDialog.tsx` (Chứng từ mua hàng) — field "Tham chiếu
chứng từ" nằm ngay dưới "Nhân viên mua hàng" ở tab "Phiếu nhập".

---

## 1. Kiến Trúc

```
src/modules/KetoanApp/components/ChonChungTuThamChieu/
├── types.ts                  ← ReferenceVoucherRow, VoucherTypeConfig, SelectedReferenceDoc...
├── periodOptions.ts           ← Danh sách "Khoảng thời gian" + computePeriodRange()
├── voucherTypeRegistry.ts     ← Registry: loại chứng từ → hàm search() (ĐĂNG KÝ Ở ĐÂY)
├── accountObjectLoader.ts     ← Loader gộp Khách hàng + NCC + Nhân viên cho "Tìm theo Đối tượng"
├── openVoucherInNewTab.ts     ← window.open('/#{path}?view={id}') theo pageIdToPath
├── ChonChungTuThamChieuDrawer.tsx  ← Drawer chọn chứng từ (Sheet, side='right', 900px)
├── ThamChieuChungTuField.tsx  ← 1 dòng field: Label + nút "..." + chip số chứng từ đã chọn
└── index.ts                   ← Barrel export (đã gộp vào `@/modules/KetoanApp/components`)
```

Import từ `@/modules/KetoanApp/components` (barrel chung), KHÔNG import trực tiếp từ
`ChonChungTuThamChieu/*` trừ khi cần tránh vòng lặp import kiểu (xem mục 4).

---

## 2. Nhúng Field Vào 1 Form Mới (việc thường làm nhất)

### Bước 1 — Thêm field vào FormState (types `.types.ui.ts`)

```ts
// {SN}.types.ui.ts
import type { SelectedReferenceDoc } from '@/modules/KetoanApp/components/ChonChungTuThamChieu/types'
//            ⚠️ import trực tiếp từ file types.ts (KHÔNG qua barrel) — xem mục 4 (vòng lặp import)

export interface {SN}FormState {
  // ...các field khác
  /** UI-only — BE chưa có field lưu tham chiếu chứng từ, KHÔNG gửi lên BE.
   *  Chỉ lưu trong phiên làm việc hiện tại của dialog. */
  referenceDocuments: SelectedReferenceDoc[]
}

export const {SN}_INITIAL_FORM: {SN}FormState = {
  // ...
  referenceDocuments: [],
}
```

### Bước 2 — Render `ThamChieuChungTuField` trong dialog/drawer

```tsx
import { ThamChieuChungTuField } from '@/modules/KetoanApp/components'

<ThamChieuChungTuField
  value={formData.referenceDocuments}
  onChange={(v) => setField('referenceDocuments', v)}
  disabled={isReadOnly}
/>
```

Đặt ngay dưới field cuối cùng của khối "thông tin chung" (thường là sau "Diễn giải" /
"Nhân viên..."), KHÔNG cần bọc thêm `<div className='grid ...'>` — component tự chiếm 1
dòng full-width.

### Bước 3 (tùy chọn) — Giới hạn loại chứng từ được chọn

Nếu form chỉ nên tham chiếu tới 1 vài loại cụ thể (thay vì toàn bộ registry), truyền
`allowedTypes` (mảng `value` trong registry — xem mục 3):

```tsx
<ThamChieuChungTuField
  value={formData.referenceDocuments}
  onChange={(v) => setField('referenceDocuments', v)}
  allowedTypes={['mua-hang', 'mua-dich-vu', 'don-mua']}
/>
```

### ⚠️ Không gửi `referenceDocuments` lên BE

`buildPayload()` KHÔNG được thêm `referenceDocuments` — BE hiện chưa có field tương ứng
trong `Create.../Update...Request`. Field này chỉ tồn tại trong phiên làm việc hiện tại
của dialog (giống cách `attachments` được xử lý trong `CTMH.types.ui.ts`). Nếu BE sau này
bổ sung field lưu trữ tham chiếu chứng từ, map `referenceDocuments` → payload rồi mới gửi.

---

## 3. Đăng Ký Thêm 1 Loại Chứng Từ Mới Vào Registry

Registry nằm ở `voucherTypeRegistry.ts` — 1 mảng `VOUCHER_TYPE_REGISTRY: VoucherTypeConfig[]`.
Thêm 1 loại chứng từ mới = thêm 1 phần tử, KHÔNG sửa `ChonChungTuThamChieuDrawer.tsx`.

```ts
export interface VoucherTypeConfig {
  value: string    // khóa duy nhất — dùng trong `allowedTypes` và trong Select "Loại chứng từ"
  label: string     // tên hiển thị
  pageId: string    // PHẢI khớp 1 key trong `pageIdToPath` (routes/routeConfig.tsx) — dùng để mở tab mới
  search: (params: VoucherSearchParams) => Promise<Omit<ReferenceVoucherRow, 'typeValue' | 'typeLabel'>[]>
}
```

### Ví dụ tối thiểu

```ts
{
  value: 'ten-loai-chung-tu',
  label: 'Tên hiển thị',
  pageId: 'ten-page-id',  // khớp key trong pageIdToPath
  search: async ({ fromDate, toDate, keyword, accountObjectId, pageSize }) => {
    const r = await XxxApiService.list({ page: 1, pageSize: pageSize ?? 200, search: keyword, fromDate, toDate, accountObjectId })
    if (!r.success || !r.data) return []
    return r.data.items.map(v => ({
      id: v.id,
      voucherDate: v.xxxDate,
      voucherCode: v.xxxCode,
      accountObjectName: v.accountObjectName,
      totalAmount: v.totalAmount,
    }))
  },
}
```

### ⚠️ Bẫy thường gặp khi map DTO → `ReferenceVoucherRow` (đã khảo sát toàn bộ module nghiệp vụ)

Mỗi module đặt tên field khác nhau — **không suy đoán, phải đọc đúng type DTO của module
đó** (`{SN}.types.api.ts`). Bảng dưới đây là kết quả khảo sát các module đã đăng ký sẵn,
tham khảo để biết mức độ khác biệt:

| Vấn đề | Giải thích | Cách xử lý |
|---|---|---|
| Tên field mã chứng từ khác nhau | `refNo` (PT/PC/CTBH), `refNoFinance` (TG), `voucherCode` (CTMH), `orderCode`/`orderNo` (DM/DDH), `returnCode`/`returnNo`, `discountCode`/`discountNo`, hoặc `invoiceNumber` chính là mã (HD/HDDV/HDDR) | Đọc đúng field trong `ListItem` DTO của module đó |
| Tên field ngày khác nhau | `refDate`, `voucherDate`, `orderDate`, `returnDate`, `discountDate`, `invoiceDate` | Tương tự |
| `accountObjectId` thường KHÔNG có trên list item | Chỉ PT, PC, DM, DDH, CTBH (optional) có `accountObjectId` trên `ListItem`; các module khác chỉ có `accountObjectName` | Nếu thiếu, để `accountObjectId: undefined` trong row — KHÔNG cố suy ra từ tên |
| API không hỗ trợ khoảng ngày (`fromDate`/`toDate`) | PT, PC, TG (cả 3 tab), NK, XK, CK chỉ nhận 1 `refDate` đơn lẻ, không nhận range | Gọi API không kèm ngày (hoặc bỏ qua), rồi lọc lại bằng helper `withinRange(dateStr, fromDate, toDate)` đã có sẵn trong `voucherTypeRegistry.ts` |
| Response phân trang không đồng nhất | Hầu hết `{ items, total, page, limit, totalPages }`, nhưng TLHM/GGHM/TLHB dùng `{ items, total, page, pageSize }`, CK dùng `{ items, total, totalPages, currentPage }` | Chỉ cần lấy `.items`, không phụ thuộc field phân trang khác |
| `debitAccountNumber`/`creditAccountNumber` hầu như không có ở list item | Kể cả các "chứng từ 2 vế" đơn giản (PT/PC/TG) cũng KHÔNG trả TK Nợ/Có ở list — chỉ có trên Detail | Để trống (`undefined`) — bảng chọn chứng từ sẽ hiển thị cột TK Nợ/Có rỗng cho các loại này, chấp nhận được vì đây là bảng chọn nhanh, không phải bảng hạch toán |
| Đơn mua / Đơn đặt hàng không có khái niệm ghi sổ | `DM`, `DDH` không có `isPosted`/`postedDate` | Không map các field đó (row không có `isPosted`) |

### Các loại chứng từ CHƯA đăng ký (biết trước để không đoán nhầm)

- **Số dư đầu kỳ** (`so-du-dau-ky`) — có 7 API list riêng biệt theo loại đối tượng
  (accounts/bank/customers/vendors/employees/inventories/wip), không có khái niệm "mã
  chứng từ" thống nhất, số tiền tách `debitAmount`/`creditAmount`. KHÔNG khớp interface
  `VoucherTypeConfig` hiện tại — cần adapter riêng nếu thực sự cần, không đăng ký đại khái.
- **Tài sản cố định** (ghi tăng/ghi giảm/đánh giá lại/điều chuyển/khấu hao TSCĐ...) — các
  trang này CHƯA có route/page trong `routeConfig.tsx` tại thời điểm viết skill này (chỉ có
  `pageId` placeholder trong `defaultPageByTopMenu`, chưa có route thật). Khi các trang này
  được xây xong, đăng ký vào registry theo đúng mẫu ở mục 3.

---

## 4. Vì Sao Import Trực Tiếp `ChonChungTuThamChieu/types.ts` Thay Vì Qua Barrel

`{SN}.types.ui.ts` của 1 module nghiệp vụ **không được** `import type { SelectedReferenceDoc }
from '@/modules/KetoanApp/components'` (qua barrel) — vì barrel đó re-export
`voucherTypeRegistry.ts`, và registry lại `import` `{SN}ApiService`/`{SN}.types.api.ts` của
chính module đó → tạo **vòng lặp import** (`{SN}.types.ui.ts` → components barrel →
`ChonChungTuThamChieu` barrel → `voucherTypeRegistry.ts` → `{SN}ApiService` →
`{SN}.types.api.ts`/`.types.ui.ts` → lặp lại).

**Luôn import type trực tiếp từ file lá** (không qua barrel nào cả):

```ts
import type { SelectedReferenceDoc } from '@/modules/KetoanApp/components/ChonChungTuThamChieu/types'
```

`types.ts` không import bất kỳ file nào khác trong feature — an toàn tuyệt đối khỏi vòng lặp.

---

## 5. Bật Deep-Link `?view={id}` Cho 1 Trang Master Mới

Khi user click vào số chứng từ (chip) trong `ThamChieuChungTuField`, `openVoucherInNewTab()`
mở `/#{path}?view={id}` ở tab mới (quy ước có sẵn trong codebase — xem `XKDialog`,
`GGHBDialog`, `TLHBDialog`). Để trang đích **tự động mở dialog xem chi tiết** bản ghi đó,
thêm đoạn sau vào master page (đã làm mẫu tại `ChungTuMuaHangPage.tsx`):

```tsx
import { useEffect } from 'react'

/** Đọc query param từ hash URL của HashRouter (#/path?key=value) — đọc thẳng
 *  window.location.hash để đảm bảo đúng kể cả khi component lazy-load */
function getHashParam(key: string): string | null {
  try {
    const hash = window.location.hash
    const qIdx = hash.indexOf('?')
    if (qIdx === -1) return null
    return new URLSearchParams(hash.slice(qIdx + 1)).get(key)
  } catch {
    return null
  }
}

// Trong component page, sau khi khai báo setSelectedId/setDialogMode/setDialogOpen:
useEffect(() => {
  const viewId = getHashParam('view')
  if (viewId) {
    setSelectedId(viewId)
    setDialogMode('view')
    setDialogOpen(true)
  }
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [])
```

> Đây là pattern đã có sẵn trong `KiemThuApp` (`useBugPage.ts`, `useTestCasePage.ts`) —
> KHÔNG dùng `useSearchParams()` của `react-router-dom` vì dưới `HashRouter`, hành vi khi
> component lazy-load đôi khi không ổn định; đọc thẳng `window.location.hash` đáng tin cậy hơn.

**Trang nào chưa thêm đoạn này** thì click chip vẫn mở đúng trang, nhưng KHÔNG tự mở dialog
— user phải tự tìm bản ghi trong danh sách. Ưu tiên thêm vào các trang đích thường được
tham chiếu tới (mua hàng, bán hàng, thu chi...).

---

## 6. Hành Vi UI (theo đúng mẫu thiết kế)

- **"Tìm theo"**: Loại chứng từ / Số chứng từ / Số hóa đơn / Đối tượng.
  - `Loại chứng từ` → "Giá trị" là `Select` liệt kê registry (lọc theo `allowedTypes` nếu có).
  - `Số chứng từ` / `Số hóa đơn` → "Giá trị" là ô nhập text tự do.
  - `Đối tượng` → "Giá trị" là `TableSearchCombobox` gộp Khách hàng + NCC + Nhân viên
    (`accountObjectLoader.ts`).
- **"Khoảng thời gian"**: bắt buộc (*), mặc định "Đầu tháng đến hiện tại", đủ toàn bộ preset
  (quý này, đầu quý đến hiện tại, năm nay, 6 tháng đầu/cuối năm, tháng 1-12, quý 1-4, hôm
  qua/tuần trước/tháng trước/quý trước/năm trước, ngày mai/tuần sau/tháng sau/quý sau, tùy
  chọn). Chọn preset → tự fill "Từ"/"Đến"; chỉ "Tùy chọn" mới cho sửa tay.
- **[Lấy dữ liệu]**: gọi `search()` của (các) loại chứng từ tương ứng, merge kết quả.
- **Search box** dưới bộ lọc: lọc nhanh trên dữ liệu ĐÃ tải (client-side, theo số chứng từ /
  diễn giải / đối tượng) — không gọi lại API.
- **Bảng**: checkbox, Ngày hạch toán, Ngày chứng từ, Số chứng từ, Diễn giải, Đối tượng, Tên
  đối tượng, TK Nợ, TK Có, Số tiền. Dựng bằng 1 `<table>` duy nhất (header `sticky top-0` +
  body trong cùng 1 container scroll, cột định nghĩa qua `<colgroup>`) — KHÔNG dùng 2 khối
  `<div className='grid ...'>` tách rời cho header/body vì sẽ bị lệch cột khi body có scrollbar
  dọc (header không có scrollbar nên hụt mất bề rộng của scrollbar so với body). Click cả dòng
  để toggle checkbox (không chỉ ô checkbox); click riêng ô "Số chứng từ" (`text-blue-700
  hover:underline`, `e.stopPropagation()`) mở chứng từ đó ở tab mới theo `pageId` của loại
  chứng từ tương ứng, không toggle checkbox. Field nào không có dữ liệu → để trống, KHÔNG
  hiển thị `-` hay `undefined`.
- **[Hủy]**: đóng drawer, không thay đổi gì.
- **[Đồng ý]**: nếu chưa chọn dòng nào → `toast.warning('Bạn cần chọn ít nhất 1 chứng từ')`.
  Nếu đã chọn → trả về danh sách, đóng drawer. `ThamChieuChungTuField` GỘP (dedupe theo `id`)
  với danh sách đã chọn trước đó, không ghi đè.
- **Chip đã chọn**: hiển thị số chứng từ (màu xanh, click mở tab mới), có nút "x" nhỏ để bỏ
  từng tham chiếu riêng lẻ mà không cần mở lại drawer.

---

## 7. Checklist Trước Khi Báo Cáo Hoàn Thành

- [ ] Thêm `referenceDocuments: SelectedReferenceDoc[]` vào FormState + initial value
- [ ] Import `SelectedReferenceDoc` type trực tiếp từ `ChonChungTuThamChieu/types` (không qua barrel)
- [ ] Render `<ThamChieuChungTuField value={...} onChange={...} disabled={isReadOnly} />`
- [ ] KHÔNG thêm `referenceDocuments` vào `buildPayload()` (BE chưa hỗ trợ)
- [ ] Nếu chỉ muốn cho chọn vài loại chứng từ cụ thể → truyền `allowedTypes`
- [ ] Nếu đăng ký loại chứng từ mới → đọc đúng field DTO thật (không đoán), xử lý API
      không hỗ trợ khoảng ngày bằng `withinRange()`
- [ ] `pageId` của entry mới PHẢI khớp key trong `pageIdToPath` (`routes/routeConfig.tsx`)
- [ ] Đã thêm `getHashParam('view')` + `useEffect` vào trang đích nếu muốn deep-link tự mở dialog
- [ ] Chạy `npm run type-check` — không có lỗi
