---
name: test-form-multi-tab
description: 'Test form đa tab (nhiều UI form trong 1 dialog): kiểm tra field mapping từng tab, shared vs riêng, payload đúng theo từng ngữ cảnh, FK ID vs display, response display fields. Dùng khi: test dialog có nhiều tab nghiệp vụ (CTBH, Phiếu thu, Phiếu xuất, Hóa đơn...).'
argument-hint: 'Đường dẫn dialog + danh sách tab cần test. VD: CTBHDialog → Tab CT ghi nợ, Phiếu thu, Thu tiền gửi, Phiếu xuất, Hóa đơn'
---

# Test Form Đa Tab — Kiểm Tra Field Mapping Cho Dialog Có Nhiều UI Form

> **Mục tiêu:** Test toàn diện field mapping FE-BE trên dialog có nhiều tab nghiệp vụ, mỗi tab là 1 form khác nhau nhưng dùng chung DTO. Phát hiện field thiếu, field sai ngữ cảnh, FK gửi sai, response thiếu display fields.

---

## 🎯 Tổng Quan

```
[1] Đọc types UI → xác định tất cả field + tab
[2] Đọc types API → xác định BE DTO hiện có
[3] Đọc dialog → xác định cách dùng field trong từng tab
[4] Phân loại: shared / tab-specific / UI-only
[5] So sánh UI FormState vs BE RequestDTO
[6] So sánh UI display needs vs BE ResponseDTO
[7] Báo cáo chi tiết: field thiếu, field thừa, FK sai
```

### Hai chế độ test:

| Chế độ | Dùng khi | Output |
|--------|----------|--------|
| **Code Analysis** (khuyên dùng) | Đã có đủ types + dialog code, không cần browser | Bảng field thiếu, phân loại shared/tab-specific |
| **Playwright UI Test** | Cần kiểm tra payload thực tế, test end-to-end | Payload thực tế, response thực tế |

### Các loại kiểm tra:

| Loại | Mô tả | Output |
|------|-------|--------|
| **Shared vs Tab-specific** | Xác định field nào dùng chung, field nào riêng từng tab | Ma trận field × tab |
| **Payload đúng ngữ cảnh** | Kiểm tra payload gửi đúng field theo tab đang active | Field nào gửi sai ngữ cảnh? |
| **FK ID vs Display** | Combobox gửi ID, BE trả về display fields | Thiếu ID? Thiếu display? |
| **Response display** | Response có đủ field để UI hiển thị khi edit | Thiếu field hiển thị? |
| **Table data (EditableDataTable)** | Cột trong bảng có map đúng DTO detail? | Thiếu cột? Sai field? |
| **Cross-form comparison** | So sánh nhiều form để tìm pattern chung | Form nào đầy đủ nhất? Form nào thiếu nhiều nhất? |

---

## ⚡ Quick Start — Code Analysis (Không Cần Browser)

> **Đây là chế độ nhanh nhất.** Chỉ cần đọc 3 file: types UI, types API, dialog code.

### Bước 0: Thu thập file

```bash
# 3 file bắt buộc:
1. types/{XXX}.types.ui.ts   # FormState, INITIAL values
2. types/{XXX}.types.api.ts   # BE DTO (Request/Response)
3. dialogs/{XXX}Dialog.tsx    # Cách dùng field trong từng tab
```

### Bước 1: Trích xuất danh sách tab

Đọc dialog → tìm `activeTab` / `detailTab` / `visibleTabs`:

```tsx
// Pattern 1: Tab cố định
type DetailTab = 'chung-tu-ghi-no' | 'phieu-xuat' | 'hoa-don'

// Pattern 2: Tab động (theo điều kiện)
const visibleTabs = getVisibleTabs(formData.returnType, formData.isReturnToWarehouse)
```

### Bước 2: Xác định field dùng trong mỗi tab

Đọc từng `renderXxxTab()` → liệt kê `formData.xxx`:

```
Tab giam-cong-no: accountObjectId, accountObjectName, accountObjectAddress, employeeId, description
Tab phieu-nhap:   accountObjectId, accountObjectName, receiverName, receiverAddress, importReason
Tab phieu-chi:    accountObjectId, accountObjectName, payeeName, payeeAddress, paymentReason
Tab hoa-don:      accountObjectId, accountObjectName, accountObjectTaxCode, invoiceNumber, invoiceDate
```

### Bước 3: Phân loại Shared vs Tab-specific

| Nguyên tắc | Mô tả |
|-----------|-------|
| **Shared** | Field xuất hiện ở ≥2 tab, cùng tên field, cùng ý nghĩa |
| **Tab-specific** | Field CHỈ xuất hiện ở 1 tab, hoặc khác ý nghĩa dù cùng tên |
| **UI-only** | Field có trong FormState nhưng đã đánh dấu `KHÔNG gửi BE` |

### Bước 4: So sánh với BE DTO

```
Tạo bảng:
| UI Field | BE Request DTO | BE Response DTO | Trạng thái |
|----------|:--------------:|:---------------:|-----------|
| accountObjectName | ✅ | ✅ | OK |
| receiverName | ❌ | ❌ | THIẾU |
| employeeId | ❌ | ❌ | THIẾU |
```

### Bước 5: Phân loại mức độ ưu tiên

| Mức | Tiêu chí | Hành động |
|-----|----------|-----------|
| 🔴 BẮT BUỘC | Ảnh hưởng chức năng (FK, post/unpost) | Inbox BE ngay |
| 🟠 Tab-specific | Form khác cần field riêng | Inbox BE |
| 🟡 UI-only | Chưa confirm, không gửi BE | Theo dõi, confirm sau |
| ⚪ Display | Chỉ cần trong response | Inbox BE (response only) |

### Bước 6: So sánh chéo nhiều form

| Tiêu chí | Form A (CTBH) | Form B (TLHB) | Pattern chung? |
|----------|:------------:|:------------:|:--------------:|
| Số tab | 5 | 4 | — |
| Shared fields thiếu | 15 | 4 | `creditDays`, `paymentDueDate`, `salesChannel`... |
| Tab-specific thiếu | 10 | 11 | `recipientName`/`receiverName`, `exportReason`/`importReason`... |
| Details thiếu | 14 | 3 | `debitAccountId`, `creditAccountId`, `costItemId`... |
| Tổng | 39 | 18 | — |

→ **Kết luận:** Các field như `employeeId`, `accountObjectAddress`, `externalOrderCode`, `salesChannel` lặp lại ở nhiều form → cần BE thống nhất bổ sung vào base DTO.

### Bước 7: Tạo báo cáo & inbox draft

Format báo cáo theo mẫu Section 6. Nếu phát hiện thiếu → tạo inbox task cho BE.

---

## 0. Thông Tin Cần Thu Thập Trước Khi Test

> **BẮT BUỘC hỏi user các thông tin sau trước khi bắt đầu test. KHÔNG tự suy đoán.**

### 0.1 Danh sách câu hỏi

```markdown
⚠️ GIẢI PHÁP CẦN XÁC NHẬN — Trước khi test form đa tab, cần các thông tin sau:

1. **Dialog cần test?**
   - Đường dẫn file dialog (vd: `src/.../CTBHDialog.tsx`)
   - Route để navigate (vd: `#/ketoan/ban-hang/chung-tu-ban-hang`)

2. **Danh sách tab trong dialog?**
   - Tên tab + key (vd: `chung-tu-ghi-no`, `phieu-xuat`, `hoa-don`)
   - Tab nào là form thay thế (dùng chung field, đổi label)?
   - Tab nào là form khác (field riêng)?

3. **Test data?**
   - ID khách hàng có sẵn để test?
   - ID hàng hóa / dịch vụ?
   - Cần tạo mới hay dùng bản ghi có sẵn?
   - Tài khoản kế toán (TK 131, 5111) có ID sẵn?

4. **API endpoints?**
   - GET list: `GET /api/accounting/v1/...`
   - POST create: `POST /api/accounting/v1/...`
   - PUT update: `PUT /api/accounting/v1/.../{id}`
   - GET detail: `GET /api/accounting/v1/.../{id}`
   - GET default: `GET /api/accounting/v1/.../default`

5. **Phạm vi test?**
   - Test tất cả tab hay chỉ 1-2 tab?
   - Test Create + Edit + View?
   - Test cả bảng EditableDataTable?
   - Test cả FK resolve khi edit?

6. **Auth / Môi trường?**
   - URL localhost? Port?
   - Tài khoản đăng nhập test?
```

### 0.2 Format Trả Lời Mẫu

```json
{
  "dialog": "CTBHDialog",
  "dialogPath": "src/modules/KetoanApp/features/nghiep-vu/ban-hang/chung-tu-ban-hang/dialogs/CTBHDialog.tsx",
  "route": "#/ketoan/ban-hang/chung-tu-ban-hang",
  "tabs": [
    { "key": "chung-tu-ghi-no", "label": "Chứng từ ghi nợ", "type": "shared" },
    { "key": "chung-tu-ghi-no", "label": "Phiếu thu", "type": "shared", "condition": "paid + Cash" },
    { "key": "chung-tu-ghi-no", "label": "Thu tiền gửi", "type": "shared", "condition": "paid + BankTransfer" },
    { "key": "phieu-xuat", "label": "Phiếu xuất", "type": "separate" },
    { "key": "hoa-don", "label": "Hóa đơn", "type": "separate" }
  ],
  "apis": {
    "list": "GET /api/accounting/v1/sales/vouchers",
    "create": "POST /api/accounting/v1/sales/vouchers",
    "update": "PUT /api/accounting/v1/sales/vouchers/{id}",
    "detail": "GET /api/accounting/v1/sales/vouchers/{id}",
    "default": "GET /api/accounting/v1/sales/vouchers/default"
  },
  "testData": {
    "customerId": "...",
    "inventoryItemId": "...",
    "bankAccountId": "..."
  },
  "scope": "create + edit + view | all tabs | table + FK",
  "auth": { "url": "http://localhost:3000", "username": "...", "password": "..." }
}
```

---

## 1. Bước 1 — Phân Loại Field: Shared vs Tab-Specific

### 1.1 Nguyên tắc phân loại

| Loại | Định nghĩa | Ví dụ CTBH |
|------|-----------|------------|
| **Shared** | Cùng 1 field, dùng cho nhiều tab thay thế nhau | `contactName`: CT ghi nợ → "Người liên hệ", Phiếu thu → "Người nộp" |
| **Tab-specific** | Field chỉ tồn tại ở 1 tab, không dùng ở tab khác | `recipientName`: chỉ có ở Phiếu xuất |
| **Parent shared** | Field cấp cha, gửi chung payload dù đang ở tab nào | `refNo`, `refDate`, `accountObjectId` |

### 1.2 Ma trận field × tab

Tạo bảng ma trận để xác định field nào thuộc tab nào:

```
| Field               | CT ghi nợ | Phiếu thu | Thu tiền gửi | Phiếu xuất | Hóa đơn |
|---------------------|:---------:|:---------:|:------------:|:----------:|:-------:|
| accountObjectName   |    ✅     |    ✅     |      ✅      |     ✅     |   ✅    |
| contactName         |    ✅     |    ✅     |      ✅      |            |         |
| recipientName       |           |           |              |     ✅     |         |
| buyerName           |           |           |              |            |   ✅    |
| ...                 |           |           |              |            |         |
```

### 1.3 Script phân tích tự động

```node
// node -e "..." — đọc FormState từ types, đối chiếu với render trong dialog
// Output: ma trận field × tab
```

---

## 2. Bước 2 — Test Create: Payload Đúng Ngữ Cảnh

### 2.1 Mục tiêu

- ✅ Payload CHỈ chứa field của tab đang active
- ✅ Field shared gửi đúng tên field
- ✅ Field tab-specific KHÔNG bị gửi nhầm sang tab khác
- ✅ FK gửi ID, không gửi display (code/name)

### 2.2 Quy trình test

```
[1] Mở dialog Create
[2] Chọn tab cần test
[3] Fill tất cả field hiển thị
[4] Bấm Lưu → chặn POST payload
[5] So sánh payload với danh sách field expected của tab đó
[6] Báo cáo:
    - Field có trong payload nhưng không thuộc tab này → THỪA
    - Field thuộc tab này nhưng không có trong payload → THIẾU
    - FK field có gửi kèm display không? → SAI FK
```

### 2.3 Bảng expected payload theo từng tab

| Tab | Field gửi | Field KHÔNG gửi |
|-----|-----------|-----------------|
| CT ghi nợ (`unpaid`) | `paymentMethod: 0`, `paymentTermId`, `accountObjectTaxCode` | `isPaidImmediately`, `bankAccountId`, `recipientName`, `exportReason` |
| Phiếu thu (`paid` + `Cash`) | `paymentMethod: 1`, `isPaidImmediately: true`, `contactName`, `submitReason` | `recipientName`, `exportReason`, `buyerName` |
| Thu tiền gửi (`paid` + `BankTransfer`) | `paymentMethod: 2`, `isPaidImmediately: true`, `bankAccountId`, `submitReason` | `recipientName`, `exportReason`, `buyerName` |
| Phiếu xuất | `recipientName`, `exportReason`, `attachedDocCount` | `contactName`, `description`, `submitReason` |
| Hóa đơn | `buyerName`, `buyerTaxCode`, `invoiceNumber`, `invoiceSerial`, `invoiceDate` | `recipientName`, `exportReason`, `submitReason` |

### 2.4 Kiểm tra FK ID

Đối với mọi `TableSearchCombobox`:

| Combobox | value (gửi BE) | KHÔNG gửi |
|----------|----------------|------------|
| Mã KH | `accountObjectId` | `accountObjectCode`, `accountObjectName` |
| Nhân viên | `employeeId` | `employeeName` |
| TK ngân hàng | `bankAccountId` | `bankAccountNumber`, `bankName` |
| Điều khoản TT | `paymentTermId` | `paymentTermName` |
| TK công nợ | `debitAccountId` | `debitAccountNumber` |
| TK doanh thu | `creditAccountId` | `creditAccountNumber` |
| TK chiết khấu | `discountAccountId` | `discountAccountNumber` |

---

## 3. Bước 3 — Test Edit: Response Display Fields

### 3.1 Mục tiêu

- ✅ Response có đủ display fields để UI hiển thị
- ✅ FK được resolve: có `debitAccountNumber` khi có `debitAccountId`
- ✅ Các field tab-specific có trong response

### 3.2 Quy trình test

```
[1] Tạo bản ghi mới (dùng 1 tab bất kỳ)
[2] Lưu → lấy ID từ response
[3] Mở Edit với ID đó
[4] Chặn GET detail response
[5] So sánh response với danh sách field UI cần hiển thị
[6] Báo cáo:
    - Field UI cần hiển thị nhưng response không có → THIẾU
    - Field FK có ID nhưng không có display → THIẾU DISPLAY
```

### 3.3 Danh sách display fields bắt buộc trong response

| UI Field | Response field cần có |
|----------|----------------------|
| Tên KH | `accountObjectName` |
| Mã KH | `accountObjectCode` |
| Tên NV | `employeeName` |
| Số TK NH | `bankAccountNumber` |
| Tên NH | `bankName` |
| Điều khoản TT | `paymentTermName` |
| TK công nợ (dòng) | `debitAccountNumber` (khi có `debitAccountId`) |
| TK doanh thu (dòng) | `creditAccountNumber` (khi có `creditAccountId`) |
| Mã hàng (dòng) | `inventoryItemCode` |
| Tên hàng (dòng) | `inventoryItemName` |
| Mã kho (dòng) | `warehouseCode` |

---

## 4. Bước 4 — Test View: Tab-Specific Fields

### 4.1 Mục tiêu

- ✅ Khi chuyển tab, field tab-specific hiển thị đúng
- ✅ View mode readonly, không cho sửa

### 4.2 Quy trình test

```
[1] Mở View bản ghi có sẵn
[2] Chuyển qua từng tab
[3] Kiểm tra field hiển thị của tab đó:
    - CT ghi nợ: có Người liên hệ, Mã số thuế, Diễn giải
    - Phiếu thu: có Người nộp, Lý do nộp
    - Phiếu xuất: có Người nhận, Lý do xuất
    - Hóa đơn: có Người mua hàng, Mã QHNS, CCCD
[4] Kiểm tra tất cả field readonly
```

---

## 5. Bước 5 — Test Table Data (EditableDataTable)

### 5.1 Mục tiêu

- ✅ Các cột trong bảng map đúng DTO `details[]`
- ✅ Cột ẩn/hiện theo điều kiện (showAccounts, discountType)
- ✅ Cột FK (TableSearchCombobox) hiển thị đúng

### 5.2 Danh sách cột cần kiểm tra

| Cột | Key | Điều kiện hiển thị | Map DTO |
|-----|-----|-------------------|---------|
| Mã hàng | `inventoryItemId` | Luôn | `details[].inventoryItemId` |
| Tên hàng | `inventoryItemName` | Luôn | `details[].inventoryItemName` |
| TK công nợ | `debitAccountId` | `showAccounts` | `details[].debitAccountId` |
| TK doanh thu | `creditAccountId` | `showAccounts` | `details[].creditAccountId` |
| ĐVT | `unit` | Luôn | `details[].unit` |
| Số lượng | `quantity` | Luôn | `details[].quantity` |
| Đơn giá | `unitPrice` | Luôn | `details[].unitPrice` |
| Thành tiền | `amount` | Luôn | `details[].amount` |
| Tỷ lệ CK (%) | `discountRate` | `discountType !== 'none'` | `details[].discountRate` |
| Tiền CK | `discountAmount` | `discountType !== 'none'` | `details[].discountAmount` |
| TK chiết khấu | `discountAccountId` | `discountType !== 'none'` | `details[].discountAccountId` |
| Đơn giá vốn | `costUnitPrice` | Luôn | `details[].costUnitPrice` |
| Tiền vốn | `costTotalAmount` | Luôn | `details[].costTotalAmount` |
| Mã nhóm | `itemGroupCode` | Luôn | `details[].itemGroupCode` |
| Nguồn gốc DT | `revenueSource` | Luôn | `details[].revenueSource` |
| Khoản mục CP | `expenseItemId` | Luôn | `details[].expenseItemId` |

---

## 6. Bước 6 — Báo Cáo Tổng Hợp

### 6.1 Format báo cáo field thiếu trong payload

| # | Tab | Field | Trạng thái | Hành động |
|---|-----|-------|-----------|----------|
| 1 | CT ghi nợ | `creditDays` | ❌ Thiếu trong payload | BE bổ sung `creditDays` vào DTO |
| 2 | Phiếu xuất | `recipientName` | ❌ Thiếu, đang map sai sang `contactName` | BE bổ sung `recipientName` vào DTO |

### 6.2 Format báo cáo field thiếu trong response

| # | Tab | UI Field | Response field thiếu | Hành động |
|---|-----|----------|---------------------|----------|
| 1 | All | Mã KH (combobox) | `accountObjectCode` | BE bổ sung vào response |
| 2 | All | TK công nợ (dòng) | `debitAccountNumber` (khi có `debitAccountId`) | BE resolve FK → trả về number |

### 6.3 Format báo cáo FK sai

| # | Combobox | Gửi lên | Đúng phải là | Hành động |
|---|----------|---------|-------------|----------|
| 1 | TK công nợ | `debitAccountNumber: "131"` | `debitAccountId: "uuid"` | Sửa payload gửi ID |
| 2 | Mã KH | `accountObjectName: "Cty A"` | Không gửi | Bỏ display field khỏi payload |

---

## 7. Checklist Sau Khi Test

- [ ] **Tất cả tab** đã test Create
- [ ] **Tất cả tab** đã test Edit (response display)
- [ ] **Tất cả tab** đã test View (readonly)
- [ ] **Shared fields** không bị gửi trùng lặp
- [ ] **Tab-specific fields** không xuất hiện ở tab khác
- [ ] **FK** CHỈ gửi ID, không gửi code/name
- [ ] **Response** có đủ display fields cho FK
- [ ] **EditableDataTable** cột map đúng DTO
- [ ] **Discount columns** hiển thị/ẩn đúng theo `discountType`
- [ ] **TK columns** hiển thị/ẩn đúng theo `showAccounts`
- [ ] **Payload** không chứa field UI-only chưa confirm BE
- [ ] **Báo cáo** đã gửi inbox task cho BE nếu phát hiện thiếu

---

## 8. File Tham Khảo

| File | Mô tả |
|------|-------|
| `src/modules/KetoanApp/features/nghiep-vu/ban-hang/chung-tu-ban-hang/dialogs/CTBHDialog.tsx` | Dialog mẫu đa tab |
| `src/modules/KetoanApp/features/nghiep-vu/ban-hang/chung-tu-ban-hang/types/CTBH.types.ui.ts` | UI types + INITIAL values |
| `src/modules/KetoanApp/features/nghiep-vu/ban-hang/chung-tu-ban-hang/types/CTBH.types.api.ts` | BE DTO |
| `src/modules/KetoanApp/features/nghiep-vu/ban-hang/chung-tu-ban-hang/hooks/useCTBH.dlg.form.ts` | Hook form + buildPayload |
| `.claude/skills/tao-phieu-thu/SKILL.md` | Rule shared/tab-specific fields |
| `.claude/skills/test-ui/SKILL.md` | Skill test UI Playwright |
