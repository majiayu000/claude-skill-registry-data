---
name: ve-theo-template
description: 'Vẽ frontend theo template từ ảnh chụp màn hình. Dùng khi: user cung cấp file ảnh (.png/.jpg) chụp giao diện từ MISA ASP hoặc bất kỳ web nào, cần phân tích layout trong ảnh và sinh code SASUCO tương ứng. Skill: dùng view_image đọc ảnh → phân tích bố cục, fields, buttons, table columns → ánh xạ sang SASUCO conventions → sinh code. Luôn load kèm tao-ui-giao-dien (foundation) + tao-ui-master-page/tao-ui-dialog/tao-ui-sub-page tùy loại UI.'
---

# Vẽ Frontend Theo Template Ảnh — SASUCO InvoiceEasy

> **Mục tiêu:** User chụp ảnh giao diện từ web tham khảo → Agent phân tích ảnh → sinh code SASUCO tuân thủ conventions.

---

## Nguồn Template

| Nguồn | Cách dùng | Công cụ |
|-------|-----------|---------|
| **Ảnh chụp màn hình** (file `.png` / `.jpg` / `.webp`) | `view_image` để xem ảnh → phân tích trực quan | `view_image` |

> **User tự chụp ảnh** giao diện cần sao chép. Agent không tự mở browser.
> Nếu user cung cấp nhiều ảnh (ảnh tổng thể + ảnh chi tiết từng vùng), phân tích từng ảnh rồi tổng hợp.

### Đường dẫn mặc định

| Loại ảnh | Đường dẫn |
|----------|-----------|
| **Danh mục** (tài khoản, khách hàng, hàng hóa...) | `C:\Users\sasuco-tuan\Downloads\screenshot\danh-muc\<tên-danh-mục>.png` |
| **Chứng từ** | `C:\Users\sasuco-tuan\Downloads\screenshot\chung-tu\<tên-chứng-từ>.png` |

> User chỉ cần nói tên danh mục, agent tự ghép đường dẫn. VD: "vẽ theo template tai-khoan" → `C:\Users\sasuco-tuan\Downloads\screenshot\danh-muc\tai-khoan.png`

---

## Quy Trình 3 Pha

```
[Pha 1] Đọc & phân tích ảnh ──→ [Pha 2] Phân tích & Ánh xạ ──→ [Pha 3] Sinh code SASUCO
    ↓                              ↓                              ↓
view_image đọc ảnh,           Xác định loại UI,             Sinh types → services
phân tích bố cục              liệt kê fields/columns,         → hooks → pages/dialogs
từng thành phần               ánh xạ terminology              theo đúng conventions
```

---

## Pha 1 — Đọc & Phân Tích Ảnh

### Bước 1.1: Mở ảnh bằng `view_image`

```bash
# User cung cấp đường dẫn file ảnh
view_image → filePath: "<đường_dẫn_tuyệt_đối_đến_ảnh>"
```

### Bước 1.2: Phân tích ảnh — danh sách câu hỏi cần trả lời

Sau khi xem ảnh, agent PHẢI trả lời được các câu hỏi sau:

#### Tổng thể
1. **Đây là loại UI gì?** Bảng danh sách / Form dialog / Trang chi tiết / Kết hợp?
2. **Có mấy vùng chính?** Header / Filter / Table / Footer / Sidebar?
3. **Màu sắc chủ đạo?** Nền, viền, button?

#### Form / Dialog (nếu có)
4. **Tiêu đề form/dialog là gì?**
5. **Có bao nhiêu field?** Liệt kê từng field:
   - Label hiển thị là gì?
   - Kiểu dữ liệu: text / số / ngày / dropdown / checkbox / textarea?
   - Có bắt buộc không? (dấu * đỏ)
   - Có icon/button "+" cạnh dropdown không?
6. **Form bố cục mấy cột?** (1 cột / 2 cột / grid)
7. **Có tab không?** Mấy tab, tên từng tab?
8. **Các nút ở footer:** Tên nút, màu sắc, vị trí?

#### Bảng danh sách (nếu có)
9. **Bảng có những cột nào?** Tên cột, căn lề (trái/phải/giữa)?
10. **Cột nào là số tiền / số lượng?** → dùng `text-right` + `formatCurrency`/`formatNumber`
11. **Cột nào là ngày tháng?** → dùng `formatDate`
12. **Cột nào là trạng thái?** → dùng `<Badge>`
13. **Cột thao tác có những icon nào?** Xem / Sửa / Xóa / Nhân bản?
14. **Có phân trang không?** Nằm ở đâu?
15. **Có filter/search không?** Những filter nào?

#### Header / Toolbar (nếu có)
16. **Tiêu đề trang là gì?**
17. **Có breadcrumb không?**
18. **Có những nút hành động nào?** Thêm mới / Làm mới / Xuất Excel / ...?

### Bước 1.3: Nếu có nhiều ảnh, phân tích tuần tự

- Ảnh 1: tổng thể → xác định loại UI
- Ảnh 2: form chi tiết → liệt kê fields
- Ảnh 3: dialog mở rộng → phân tích tab/field bổ sung

> Sau khi phân tích xong → **BẮT BUỘC tóm tắt phát hiện cho user xác nhận** trước khi sang Pha 2.

---

## Pha 2 — Phân Tích & Ánh Xạ

### Bước 2.1: Xác định loại UI cần sinh

| Dấu hiệu trong ảnh | Loại UI SASUCO | Skill cần load |
|--------------------|----------------|----------------|
| Bảng danh sách + phân trang + filter | **Master Page** | `tao-ui-master-page` + `filter-phan-trang` |
| Popup/modal form ≤10 fields | **Dialog** | `tao-ui-dialog` |
| Trang full-screen, nhiều section, breadcrumb | **Sub Page** | `tao-ui-sub-page` |
| Kết hợp bảng + dialog | **Master Page + Dialog** | Cả 3 skill trên |

### Bước 2.2: Ánh xạ thành phần UI từ ảnh sang SASUCO

#### Form Fields
| Thấy trong ảnh | Ánh xạ sang SASUCO |
|---------------|---------------------|
| Ô nhập text | `<Input>` + validate onBlur |
| Ô nhập số | `type='text' inputMode='numeric' text-right` |
| Textarea nhiều dòng | `className='invoice-textarea'` |
| Dropdown chọn danh mục | `<SearchCombobox dataQa='cmb_...' />` |
| Dropdown chọn enum cố định | `<Select />` |
| Date picker | `<DatePicker data-qa='dt_...' />` |
| Checkbox | `<Checkbox />` |
| Label có dấu * đỏ | field bắt buộc → validate required |

#### Buttons
| Thấy trong ảnh | Ánh xạ sang SASUCO |
|---------------|---------------------|
| Nút xanh/primary (Lưu, Thêm mới, Xác nhận) | `className='btn-primary'` |
| Nút xám/secondary (Hủy, Đóng, Làm mới) | `className='btn-secondary'` |
| Nút đỏ (Xóa) | `className='btn-danger'` + `ConfirmDialog` |

#### Table
| Thấy trong ảnh | Ánh xạ sang SASUCO |
|---------------|---------------------|
| Cột số tiền (căn phải) | `className='text-right'` + `formatCurrency()` |
| Cột số lượng (căn phải) | `className='text-right'` + `formatNumber()` |
| Cột ngày tháng | `formatDate()` format `dd-MM-yyyy` |
| Cột trạng thái | `<Badge>` |
| Icon Xem (mắt) | `Eye` + `className='icon-primary'` |
| Icon Sửa (bút chì) | `Pencil` + `className='icon-warning'` |
| Icon Xóa (thùng rác) | `Trash2` + `className='icon-danger'` |
| Icon Nhân bản | `Copy` + `className='icon-success'` |
| Header bảng nền xám | `className='bg-[#f8f9fa]'` |
| Phân trang | `<PagingUtils />` |

### Bước 2.3: Ánh xạ terminology từ ảnh → SASUCO

> Dịch label/field trong ảnh sang tiếng Việt phù hợp ngữ cảnh SASUCO.

| Thường thấy trong ảnh tham khảo | SASUCO terminology |
|-------------------------------|---------------------|
| Mã / Số / Code | Mã / Số |
| Tên / Name | Tên |
| Diễn giải / Description | Diễn giải / Nội dung |
| Số tiền / Amount / Giá trị | Số tiền / Thành tiền |
| Ngày / Date | Ngày |
| Trạng thái / Status | Trạng thái |
| Ghi chú / Note | Ghi chú |
| Địa chỉ / Address | Địa chỉ |
| Số điện thoại / Phone | Số điện thoại |

### Bước 2.4: Liệt kê cấu trúc file dự kiến

Trước khi sinh code, trình bày rõ ràng:

```
DỰ KIẾN CẤU TRÚC:
src/modules/<Portal>/
  features/<feature>/
    <FeatureName>/
      <FeatureName>Types.ts          ← Types & interfaces
      <FeatureName>ApiService.ts     ← API service class
      hooks/
        use<FeatureName>List.ts      ← Hook fetch danh sách + filter
        use<FeatureName>Form.ts      ← Hook form (create/edit)
      dialogs/
        <FeatureName>Dialog.tsx      ← Dialog component
      pages/
        <FeatureName>Page.tsx        ← Master page component
      index.ts                       ← Barrel exports
```

> **BẮT BUỘC:** Trình bày cấu trúc dự kiến cho user xác nhận TRƯỚC KHI sinh code.

---

## Pha 3 — Sinh Code Theo SASUCO Conventions

### Bước 3.1: Xác định Portal & Feature

- **Portal:** Invoice / Admin / Partner / SSO / BaseIndex / KetoanHKD
- **Feature:** tên feature theo cấu trúc `modules/<Portal>/features/<feature>`
- **shortName:** Tên viết tắt cho tên file (theo skill `dat-ten`)

### Bước 3.2: Sinh code theo đúng thứ tự

> **Thứ tự sinh code bắt buộc:** Types → Services → Hooks → Pages/Dialogs

#### 3.2.1 Types (`<Name>Types.ts`)

```typescript
/** Item hiển thị trong danh sách */
export interface IXxxItem {
  id: string
  // ... fields từ ảnh template
}

/** Request tạo mới / cập nhật */
export interface IXxxSaveRequest {
  id?: string
  // ... fields từ ảnh template (không cần id nếu tạo mới)
}

/** Response danh sách có phân trang */
export interface IXxxListResponse {
  data: IXxxItem[]
  total: number
}
```

#### 3.2.2 API Service (`<Name>ApiService.ts`)

```typescript
import { apiCall, buildApiUrl, buildApiUrlWithParams } from '@/shared/services/api'

const BASE_PATH = '/api/v1/xxx'

export class XxxApiService {
  static async getList(params: IXxxFilterParams): Promise<ApiResponse<IXxxListResponse>> {
    const url = buildApiUrlWithParams(BASE_PATH, params)
    return apiCall(url)
  }
  static async getById(id: string): Promise<ApiResponse<IXxxItem>> {
    return apiCall(buildApiUrl(BASE_PATH, id))
  }
  static async create(data: IXxxSaveRequest): Promise<ApiResponse<IXxxItem>> {
    return apiCall(buildApiUrl(BASE_PATH), { method: 'POST', body: JSON.stringify(data) })
  }
  static async update(id: string, data: IXxxSaveRequest): Promise<ApiResponse<IXxxItem>> {
    return apiCall(buildApiUrl(BASE_PATH, id), { method: 'PUT', body: JSON.stringify(data) })
  }
  static async delete(id: string): Promise<ApiResponse<void>> {
    return apiCall(buildApiUrl(BASE_PATH, id), { method: 'DELETE' })
  }
}
```

#### 3.2.3 Hooks

- **Hook danh sách:** theo skill `filter-phan-trang` — useDebounce 800ms, sessionStorage currentPage, localStorage pageSize
- **Hook form:** theo skill `validate-input` — validate onBlur, inline error, toast tổng hợp

#### 3.2.4 Pages / Dialogs

- **Master Page:** theo skill `tao-ui-master-page` — Header→Filters→Table→Pagination
- **Dialog:** theo skill `tao-ui-dialog` — DialogHeader+Content+Footer, maxWidth, mode
- **Sub Page:** theo skill `tao-ui-sub-page` — Breadcrumb→Header→Content Cards

### Bước 3.3: Kiểm tra sau khi code

Theo skill `checklist-sau-code`:
- [ ] Không có logic trong component (tất cả trong hooks)
- [ ] `data-qa` đầy đủ trên tất cả input/button
- [ ] Button dùng CSS class (`btn-primary`, `btn-secondary`, `btn-danger`)
- [ ] Table action icon dùng class `icon-*`
- [ ] Validate onBlur, không validate onChange
- [ ] Input số dùng `type='text' inputMode='numeric'`
- [ ] View mode dùng `<div>`, không dùng input disabled
- [ ] Không dùng `any`
- [ ] Import từ `@/shared/...` cho shared components/utils
- [ ] Phân trang server-side, reset page=1 khi filter đổi

---

## Ví Dụ Cụ Thể

### Ví dụ: Sao chép form "Danh mục tài khoản" từ ảnh

**User cung cấp:** Ảnh chụp form Thêm tài khoản từ web tham khảo

**Quy trình:**
1. `view_image` đọc ảnh → phân tích:
   - Đây là **Dialog** (form Thêm tài khoản)
   - Fields: Số TK, Tên TK, Tính chất (dropdown), Trạng thái (checkbox)
   - 2 cột grid
   - Nút Lưu (primary) + Hủy (secondary)
2. Ánh xạ:
   - Portal **KetoanHKD**
   - Feature: `danh-muc/tai-khoan`
   - Dùng `tao-ui-dialog` + `tao-ui-giao-dien`
3. Cấu trúc file: Types → Service → Hook → Dialog
4. Sinh code

### Ví dụ: Sao chép trang "Danh sách tài khoản" từ ảnh

**User cung cấp:** Ảnh chụp trang danh sách tài khoản (bảng + filter + phân trang + nút Thêm mới) từ web tham khảo.

**Quy trình:**

1. `view_image` đọc ảnh → phân tích:
   - Đây là **Master Page** (bảng danh sách có CRUD qua dialog overlay)
   - **Header:** tiêu đề "Danh sách tài khoản" + nút *Làm mới* (secondary) + *Thêm mới* (primary)
   - **Filter:** ô tìm kiếm + dropdown lọc Tính chất + dropdown lọc Trạng thái
   - **Cột bảng:** STT (giữa) · Số TK · Tên TK · Tính chất · Số dư (căn phải, tiền) · Trạng thái (badge) · Thao tác
   - **Cột Thao tác:** Xem (mắt) · Sửa (bút) · Xóa (thùng rác)
   - **Phân trang** ở footer

2. Ánh xạ:
   - Loại UI → **Master Page** → load `tao-ui-master-page` + `filter-phan-trang` (+ `tao-ui-dialog` cho form CRUD overlay)
   - Cột "Số dư" căn phải → `text-right` + `formatCurrency()`
   - Cột "Trạng thái" → `<Badge>`
   - Cột Thao tác theo thứ tự cứng: `Eye` (icon-primary) → `Pencil` (icon-warning) → `Trash2` (icon-danger)
   - Filter tìm kiếm → `useDebounce 800ms`, reset `page=1` khi filter đổi

3. Cấu trúc file dự kiến:

```
src/modules/KetoanHKD/features/danh-muc/tai-khoan/
  TaiKhoanTypes.ts
  TaiKhoanApiService.ts
  hooks/
    useTaiKhoanList.ts       ← filter + phân trang server-side
    useTaiKhoanForm.ts        ← form create/edit
  dialogs/TaiKhoanDialog.tsx
  pages/TaiKhoanPage.tsx
  index.ts
```

4. Sinh code Page theo cấu trúc **Header → Filters → Table → Pagination → Dialogs (ngoài CardContent)**:
   - Khai báo `PAGE_ID` + `PAGE_FEATURES` ở đầu file (BẮT BUỘC — phục vụ sơ đồ dự án + export menu permission):

```tsx
export const PAGE_ID = 'danh-muc-tai-khoan'  // khớp navItem.id trong NavMenu
export const PAGE_FEATURES = [
  { label: 'Làm mới',      code: 'btn-refresh' },
  { label: 'Tạo mới...',   code: 'btn-create' },
  { label: 'Xem chi tiết', code: 'row-view' },
  { label: 'Sửa',          code: 'row-edit' },
  { label: 'Xóa',          code: 'row-delete' },
]
```

   - Table header `bg-[#f8f9fa]`, loading dùng `<PageLoader>`, rỗng hiển thị "Không có dữ liệu"
   - STT = `startIndex + i + 1`, số dư `text-right` + `formatCurrency`, trạng thái `<Badge>`
   - Xóa **phải** qua `ConfirmDialog`, không gọi API trực tiếp
   - Phân trang `<PagingUtils pageSizeOptions={[10,20,50,100]} />`

5. Chạy kiểm tra: `node .claude/skills/tao-ui-master-page/check-master-page.cjs src/modules/KetoanHKD/features/danh-muc/tai-khoan/pages/TaiKhoanPage.tsx`

---

## Tích Hợp Với Các Skill Khác

> Khi thực hiện `ve-theo-template`, BẮT BUỘC load các skill sau:

| Skill | Khi nào load |
|-------|-------------|
| `tao-ui-giao-dien` | **LUÔN LUÔN** — foundation cho mọi UI |
| `tao-ui-master-page` | Khi ảnh có bảng danh sách |
| `tao-ui-dialog` | Khi ảnh có popup/modal form |
| `tao-ui-sub-page` | Khi ảnh có trang full-screen chi tiết |
| `filter-phan-trang` | Khi master page có phân trang |
| `validate-input` | Khi form có validate |
| `dat-ten` | Khi cần đặt tên file/component |
| `xac-dinh-pham-vi` | **ĐẦU TIÊN** — xác định portal, feature, file liên quan |
| `tich-hop-api-ui` | Khi cần tạo types/hooks kết nối API→UI |
| `checklist-sau-code` | Sau khi sinh code, kiểm tra lại |

---

## Cảnh Báo

1. **Không sao chép CSS/HTML trực tiếp từ ảnh** — phải viết lại theo SASUCO conventions
2. **Không sao chép text/label y nguyên nếu là tiếng Anh** — dịch sang tiếng Việt
3. **Ảnh chỉ để tham khảo UI** — không suy diễn logic backend
4. **Tôn trọng bản quyền** — chỉ tham khảo layout, không sao chép nguyên văn code
5. **Luôn xác nhận cấu trúc dự kiến** với user trước khi sinh code
6. **Nếu ảnh mờ/khó đọc** → hỏi lại user, không đoán
