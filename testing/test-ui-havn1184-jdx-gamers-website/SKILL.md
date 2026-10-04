---
name: test-ui
description: 'Test UI tự động bằng Playwright: truy cập localhost:3000, đăng nhập, mở dialog/page, test create/update từng field, chặn payload/response API để phát hiện field thiếu (FE ko gửi/BE ko trả), field update thiếu, field FK select chỉ gửi ID thiếu display. Dùng khi: test form CRUD, kiểm tra field mapping FE-BE, verify payload API, phát hiện field bị bỏ sót khi create/update, test dialog/form bất kỳ.'
argument-hint: 'Route màn hình + tên dialog cần test. VD: #/ketoan/don-vi-tinh → Dialog Đơn vị tính'
---

# Test UI — Kiểm Thử Giao Diện & Field Mapping FE-BE Bằng Playwright

> **Mục tiêu:** Tự động mở browser, login, navigate đến màn hình, mở dialog, test create/update từng field, chặn & phân tích payload/response API → báo cáo field thiếu, field sai, FK thiếu display.

---

## 🎯 Tổng Quan

```
[1] Login localhost:3000 → [2] Navigate route → [3] Mở dialog → [4] Quét fields
→ [5] Fill + Lưu (Create) → [6] Chặn payload/response → [7] Mở lại Edit
→ [8] Đọc lại + so sánh → [9] Báo cáo field thiếu/sai
```

### Các loại kiểm tra:

| Loại | Mô tả | Output |
|------|-------|--------|
| **Create** | Fill tất cả field → Lưu → đọc response + payload | Field nào không có trong payload? Field nào không có trong response? |
| **Update** | Sửa từng field → Lưu → đọc lại → so sánh | Field nào update thiếu? Field nào sai giá trị? |
| **FK Select** | Chọn đối tượng từ combobox → kiểm tra payload chỉ gửi ID | Có gửi kèm code/name không? Response có trả đủ display fields? |
| **FK Response** | Sau create/edit → kiểm tra response có đủ field để hiển thị | Thiếu code? Thiếu name? Thiếu các field liên quan? |

---

## 🔧 Cấu Hình Đầu Vào

Trước khi chạy test, xác định rõ:

| Thông tin | Bắt buộc | Mô tả | Ví dụ |
|-----------|----------|-------|-------|
| **Route** | ✅ | Hash route của màn hình | `#/ketoan/don-vi-tinh` |
| **Tên form/dialog** | ✅ | Tên hiển thị trong báo cáo | `Đơn vị tính` |
| **Selector nút Thêm** | ✅ | data-qa hoặc text | `[data-qa="btn_them_moi"]` |
| **Selector nút Sửa** | ✅ | data-qa dòng đầu tiên | `[data-qa="btn_sua"]` |
| **Selector nút Lưu** | ✅ | data-qa hoặc text | `[data-qa="btn_luu"]` |
| **Selector dialog** | Không | Mặc định `[role="dialog"]` | `.dm-dialog` |
| **Loại test** | ✅ | `all` / `create-only` / `update-only` / `fk-only` | `all` |
| **DTO source** | Không | Đường dẫn file types API hoặc DTO text từ user để đối chiếu | `src/modules/.../DM.types.api.ts` |
| **FK fields** | Không | Danh sách FK (bao gồm TK nợ/có) cần kiểm tra đặc biệt | `[{ dataQa: 'sel_kh', fkField: 'accountObjectId', displayFields: ['objectCode', 'objectName'] }]` |

---

## 📋 Quy Tắc Xác Định Field Trong Payload

> **Quy tắc chung để xác định field nào cần gửi lên BE, field nào không.**

### Rule mặc định (áp dụng khi user không có yêu cầu đặc biệt):

| Pattern | Có gửi lên payload? | Giải thích | Ví dụ |
|---------|---------------------|------------|-------|
| **Field editable trên UI (có `<Label>`)** | ✅ **PHẢI CÓ** | Mọi field người dùng có thể nhập/sửa trên UI → PHẢI gửi lên payload. Đây là rule quan trọng nhất. | `Người liên hệ` → `contactPerson` |
| **Field KHÔNG có label, auto-fill khi select bản ghi** | ❌ **KHÔNG** | Field được fill tự động từ dữ liệu của bản ghi được chọn (VD: chọn NCC → fill Địa chỉ, MST) → không gửi, BE tự resolve | `Địa chỉ`, `Mã số thuế` (fill từ NCC) |
| **FK select từ danh mục (TableSearchCombobox)** | ✅ **Chỉ gửi ID** | Combobox chọn đối tượng → gửi `xxxId` lên payload. KHÔNG gửi code/name kèm theo | `accountObjectId`, `employeeId` |
| **FK response display** | ✅ **Expect name/code** | Sau khi gửi ID, expect response từ BE có kèm `name`/`code`/`number` để hiển thị | Response có `accountObjectCode`, `accountObjectName` |
| **TK nợ / TK có (debitAccount/creditAccount)** | ✅ **Chỉ gửi ID** | Gửi `debitAccountId` / `creditAccountId`. KHÔNG gửi `debitAccountNumber` / `creditAccountNumber` | Chỉ `debitAccountId: "abc-123"`, không gửi `debitAccountNumber: "111"` |
| **TK nợ/có response display** | ✅ **Expect number** | Sau khi gửi ID, expect response có `debitAccountNumber` / `creditAccountNumber` | Response có `debitAccountNumber: "111"`, `creditAccountNumber: "331"` |
| **Field auto-code** | ❌ **KHÔNG** | Số chứng từ, mã tự sinh do BE tạo → FE không gửi | `orderCode` |
| **Field computed** | ❌ **KHÔNG** | Field được tính toán (tổng tiền, thành tiền...) → BE tự tính hoặc FE tính rồi gửi kết quả | `totalAmount` (FE tính từ details) |

### Rule đặc biệt (override khi user yêu cầu):

> **Nếu user có yêu cầu đặc biệt (VD: field không có label cũng gửi lên payload), thì thực hiện theo yêu cầu đặc biệt đó, KHÔNG theo rule mặc định.**

| Tình huống | Hành động |
|------------|----------|
| User yêu cầu field X (dù không label) cũng gửi | Thêm field đó vào `buildPayload` |
| User yêu cầu field Y gửi kèm cả code/name (không chỉ ID) | Giữ nguyên logic gửi code/name |
| User yêu cầu field Z không gửi dù có label | Bỏ field đó khỏi payload |

### Cách phân loại field khi test:

```
1. Quét tất cả field trong dialog → phân biệt có <Label> / không có <Label>
2. Với field có Label → mặc định EXPECT có trong payload
3. Với field không có Label → mặc định EXPECT KHÔNG có trong payload
4. Nếu user có yêu cầu đặc biệt → override rule mặc định
5. Với FK combobox → kiểm tra payload CHỈ có ID, response CÓ kèm display fields
```

### Mapping Label → Payload cho Đơn mua (ví dụ):

| # | Label | data-qa | Field formData | Gửi payload? | Payload key |
|---|-------|---------|---------------|-------------|-------------|
| 1 | Nhà cung cấp* | `sel_ncc` | `accountObjectId` | ✅ ID | `accountObjectId` |
| 2 | Địa chỉ | `txt_supplier_address` | `supplierAddress` | ❌ (auto-fill từ NCC) | — |
| 3 | Mã số thuế | `txt_supplier_tax` | `supplierTaxCode` | ❌ (auto-fill từ NCC) | — |
| 4 | Người liên hệ | `txt_contact_person` | `contactPerson` | ✅ CÓ | `contactPerson` |
| 5 | Diễn giải | `txt_description` | `description` | ✅ CÓ | `description` |
| 6 | Nhân viên mua hàng | `sel_nhan_vien` | `employeeId` | ✅ ID | `employeeId` |
| 7 | Điều khoản TT | `sel_payment_terms` | `paymentTermId` | ✅ ID | `paymentTerms` |
| 8 | Số ngày nợ | `txt_credit_days` | `creditDays` | ✅ CÓ | `creditDays` |
| 9 | Ngày đơn hàng* | `dt_order_date` | `orderDate` | ✅ CÓ | `orderDate` |
| 10 | Số đơn hàng | `txt_order_code` | `orderCode` | ❌ (auto-code) | — |
| 11 | Tình trạng* | `sel_order_status` | `orderStatus` | ✅ CÓ | `orderStatus` |
| 12 | Ngày giao hàng | `dt_delivery_date` | `deliveryDate` | ✅ CÓ | `deliveryDate` |

### Mapping Bảng hàng tiền (details[]):

| # | Cột | Có label? | Gửi payload? | Payload key |
|---|-----|----------|-------------|-------------|
| 1 | Mã hàng | ✅ | ✅ ID | `itemId` |
| 2 | Tên hàng | ✅ | ✅ (qua description) | `description` |
| 3 | ĐVT | ✅ | ✅ | `unit` |
| 4 | Số lượng | ✅ | ✅ | `quantity` |
| 5 | SL nhận | ✅ (readonly) | ✅ | `receivedQuantity` |
| 6 | Đơn giá | ✅ | ✅ | `unitPrice` |
| 7 | Thành tiền | ✅ | ✅ | `amount` |
| 8 | % Thuế GTGT | ✅ | ✅ | `taxRate` |
| 9 | Khoản mục CP | ✅ | ✅ ID | `costItemId` |

---

## � Đối Chiếu DTO BE Với Payload Thực Tế

> **Mục tiêu:** Khi user cung cấp DTO BE mới → so sánh với DTO hiện tại trong code FE → báo cáo khác biệt → hỏi user có muốn cập nhật không → đối chiếu payload FE gửi lên với DTO để phát hiện field thừa/thiếu.

### Quy Trình Đối Chiếu DTO

```
[1] User cung cấp DTO mới (hoặc agent tự tìm từ types file)
[2] So sánh DTO mới vs DTO hiện tại trong code
[3] Báo cáo field: thêm mới / xóa / đổi kiểu / đổi optional→required
[4] Hỏi user: "Có muốn cập nhật types theo DTO mới không?"
[5] Nếu user đồng ý → cập nhật types file
[6] Đối chiếu payload FE thực tế với DTO → báo cáo field thừa/thiếu
```

### Quy Tắc Expect Payload Dựa Trên DTO

| Tình huống | Expect | Hành động nếu sai |
|-----------|--------|-------------------|
| **Field trong DTO là required** | ✅ PHẢI có trong payload | Thêm field vào `buildFormData` |
| **Field trong DTO là optional** | CÓ THỂ có hoặc không | Chỉ báo lỗi nếu field đó có trên UI editable |
| **Field KHÔNG có trong DTO nhưng có trong payload** | ❌ Field dư thừa | Xóa field khỏi payload, kiểm tra `buildFormData` |
| **Field trên UI editable nhưng không có trong payload** | ❌ THIẾU | Thêm field vào `buildFormData` |
| **Field từ TableSearchCombobox (FK)** | ✅ CHỈ gửi `xxxId` | Xóa code/name khỏi payload nếu có |
| **Field TK nợ / TK có** | ✅ CHỈ gửi `debitAccountId` / `creditAccountId` | KHÔNG gửi `debitAccountNumber` / `creditAccountNumber` |
| **Field auto-code (mã tự sinh)** | ❌ KHÔNG gửi | BE tự sinh |
| **Field computed (tổng tiền...)** | Tuỳ DTO | Nếu DTO có → gửi; nếu không → không gửi |

### Cách Đối Chiếu DTO (Không Cần Chạy Playwright)

> Khi user cung cấp DTO dạng text/json/typescript → agent có thể đối chiếu trực tiếp với types file hiện tại mà không cần mở browser.

```typescript
// Bước 1: Đọc DTO hiện tại từ file types
// VD: src/modules/KetoanApp/features/nghiep-vu/mua-hang/don-mua/types/DM.types.api.ts

// Bước 2: Parse DTO mới từ user input
// User cung cấp dạng:
//   interface DonMuaDto {
//     id: string
//     orderCode: string
//     orderDate: string
//     totalAmount: number
//     // ... thêm field mới
//     postedDate?: string   // ← field mới
//   }

// Bước 3: So sánh & báo cáo
// Output: Bảng diff DTO
```

### Bảng Báo Cáo Diff DTO

| # | Field | Trạng thái | DTO cũ | DTO mới | Hành động |
|---|-------|-----------|--------|---------|----------|
| 1 | `postedDate` | 🟢 THÊM MỚI | — | `string?` | Thêm vào types |
| 2 | `oldField` | 🔴 ĐÃ XÓA | `number` | — | Xóa khỏi types |
| 3 | `totalAmount` | 🟡 ĐỔI KIỂU | `number` | `string` | Cập nhật types |
| 4 | `orderCode` | 🟡 OPTIONAL→REQUIRED | `string?` | `string` | Cập nhật types |

### Mapping Payload Thực Tế vs DTO

> Sau khi cập nhật DTO, đối chiếu payload FE gửi lên với DTO mới:

| # | Field DTO | Required? | Có trong payload? | Payload key | Trạng thái |
|---|----------|----------|-------------------|-------------|-----------|
| 1 | `accountObjectId` | ✅ | ✅ | `accountObjectId` | ✅ OK |
| 2 | `contactPerson` | ❌ | ❌ | — | ⚠️ CÓ TRÊN UI → THIẾU |
| 3 | `creditDays` | ❌ | ✅ | `creditDays` | ✅ OK |
| 4 | `orderCode` | ❌ | ❌ | — | ✅ Auto-code, không gửi |
| 5 | `debitAccountNumber` | ❌ | ❌ | — | ✅ TK chỉ gửi ID |

### Quy Tắc Ưu Tiên Xác Định Field Gửi Payload

```
1. Nếu user cung cấp DTO → ưu tiên DTO làm chuẩn
2. Nếu không có DTO → đọc types file (.types.api.ts) làm chuẩn
3. Nếu không có types file → dùng rule mặc định (field có label → gửi)
4. Rule đặc biệt (TK nợ/có, TableSearchCombobox) luôn override rule mặc định
```

---

## 🏦 Quy Tắc Đặc Biệt: TK Nợ / TK Có (Accounting Accounts)

> **Quy tắc:** Khi dialog có field chọn tài khoản nợ/có (debit/credit account):
> - **Payload:** CHỈ gửi `debitAccountId` / `creditAccountId` — KHÔNG gửi account number
> - **Response:** Expect BE trả về `debitAccountNumber` / `creditAccountNumber` để hiển thị
> - **Edit form:** Resolve account number từ ID để hiển thị đúng cho user

### Ví dụ Payload Đúng/Sai

```typescript
// ✅ ĐÚNG: Chỉ gửi ID
{
  "accountingDetails": [
    { "debitAccountId": "abc-123", "creditAccountId": "def-456", "amount": 1000000 }
  ]
}

// ❌ SAI: Gửi cả account number (dư thừa, BE tự resolve)
{
  "accountingDetails": [
    {
      "debitAccountId": "abc-123",
      "debitAccountNumber": "111",    // ← KHÔNG GỬI
      "creditAccountId": "def-456",
      "creditAccountNumber": "331",   // ← KHÔNG GỬI
      "amount": 1000000
    }
  ]
}
```

### Expect Response Từ BE

```typescript
// ✅ ĐỦ: Response có account number để hiển thị
{
  "accountingDetails": [
    {
      "debitAccountId": "abc-123",
      "debitAccountNumber": "111",     // ← CẦN CÓ
      "creditAccountId": "def-456",
      "creditAccountNumber": "331",    // ← CẦN CÓ
      "amount": 1000000
    }
  ]
}

// ❌ THIẾU: Response không có account number → FE không hiển thị được
{
  "accountingDetails": [
    { "debitAccountId": "abc-123", "creditAccountId": "def-456", "amount": 1000000 }
  ]
}
```

### Resolve TK Hiển Thị Khi Edit

> Khi mở form edit, nếu response chỉ có `debitAccountId` mà không có `debitAccountNumber`:
> → FE phải tự resolve bằng cách fetch danh sách tài khoản (AccountApiService)

```typescript
// Pattern resolve trong buildFormData (Pattern A - Ưu tiên)
const buildFormData = useCallback(async (d: XxxDetail): Promise<XxxFormState> => {
  // Thu thập tất cả accountId cần resolve
  const accountIds = d.accountingDetails
    .flatMap(line => [line.debitAccountId, line.creditAccountId])
    .filter((id): id is string => !!id)

  // Fetch song song
  const [accountMap] = await Promise.all([
    accountIds.length > 0
      ? AccountApiService.list({ pageIndex: 1, pageSize: 9999 })
          .then(r => new Map(r.data?.items?.map(a => [a.id, a]) ?? []))
          .catch(() => new Map())
      : new Map(),
  ])

  // Map → form state
  const formData: XxxFormState = {
    ...d,
    accountingDetails: d.accountingDetails.map(line => {
      const debitAcc = line.debitAccountId ? accountMap.get(line.debitAccountId) : null
      const creditAcc = line.creditAccountId ? accountMap.get(line.creditAccountId) : null
      return {
        ...line,
        debitAccountNumber: line.debitAccountNumber || debitAcc?.number || '',
        creditAccountNumber: line.creditAccountNumber || creditAcc?.number || '',
      }
    }),
  }
  return formData
}, [])
```

---

## 🔍 Resolve TableSearchCombobox Khi Mở Form Edit

> **Quy tắc:** Khi mở form edit, các field dùng `TableSearchCombobox` cần resolve lại giá trị để hiển thị đúng.

### Nguyên tắc

| Tình huống | Cách xử lý |
|-----------|-----------|
| Combobox hiển thị **name** khi select | Resolve cũng phải hiển thị **name** |
| Combobox hiển thị **code - name** khi select | Resolve cũng phải hiển thị **code - name** |
| Combobox hiển thị **number** (TK) | Resolve cũng phải hiển thị **number** |
| Response BE đã có đủ display fields | KHÔNG cần resolve thêm |
| Response BE chỉ có ID | PHẢI resolve bằng API getById hoặc list |

### Các Bước Resolve

```
[1] Nhận DTO từ API GET /{id}
[2] Với mỗi TableSearchCombobox field:
    ├── Nếu DTO đã có display field (name/code/number) → dùng luôn
    └── Nếu DTO chỉ có ID → fetch API để lấy display value
[3] Set vào formData TRƯỚC KHI render form
```

### Ví dụ Màn Hình Chi Tiền

```typescript
// DTO từ BE: BankPaymentDetail
{
  "id": "xxx",
  "refNo": "CT00001",
  "accountObjectId": "kh-123",
  // BE KHÔNG trả objectCode, objectName
  "bankAccountId": "bank-456",
  // BE KHÔNG trả bankAccountNumber, bankName
}

// Hook resolve:
const buildFormData = async (d: BankPaymentDetail) => {
  const [khRes, bankRes] = await Promise.all([
    d.accountObjectId ? KHApiService.getById(d.accountObjectId) : null,
    d.bankAccountId ? BankAccountApiService.getById(d.bankAccountId) : null,
  ])

  return {
    ...d,
    // Resolve KH: TableSearchCombobox hiển thị "code - name"
    objectCode: khRes?.data?.code || '',
    objectName: khRes?.data?.name || '',
    // Resolve TK ngân hàng: TableSearchCombobox hiển thị "number - name"
    bankAccountNumber: bankRes?.data?.accountNumber || '',
    bankName: bankRes?.data?.bankName || '',
  }
}
```

### ⚠️ Lưu ý Quan Trọng Khi Resolve

- **Luôn resolve trong `buildFormData` của Hook** (Pattern A) — KHÔNG resolve trong `useEffect` của Dialog (Pattern B)
- **Fetch song song** bằng `Promise.all` để giảm latency
- **Có fallback** khi API fail (`.catch(() => null)`)
- **Nếu BE đã trả đủ display fields** → không cần resolve, dùng thẳng từ DTO

---

## �🚀 Script Mẫu — Tạo File Test

> **BẮT BUỘC:** Tạo script dựa trên template `e2e/test-field-update.ts`, bổ sung thêm network interception.

### Template script (lưu vào `e2e/test-ui-<ten-trang>.ts`):

```typescript
/**
 * Script TEST UI — Test field mapping FE-BE cho dialog/form
 *
 * Cách dùng:
 *   1. Sửa CONFIG bên dưới
 *   2. Chạy: npx tsx e2e/test-ui-<ten-trang>.ts
 *
 * Tự động:
 *   - Login localhost:3000 (0985908750 / Hoadon@2022!#)
 *   - Navigate đến route
 *   - Mở dialog Thêm mới
 *   - Quét fields
 *   - Fill dữ liệu → Lưu → Chặn payload + response
 *   - Mở lại Edit → Đọc dữ liệu → So sánh
 *   - Báo cáo field thiếu trong payload, response, và field update sai
 */
import { chromium, Browser, BrowserContext, Page } from 'playwright';
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createConnection } from 'node:net';

// ═══════════════════════════════════════════════════════════
// 🎯 CONFIG — SỬA TẠI ĐÂY
// ═══════════════════════════════════════════════════════════
const CONFIG = {
  /** Hash route của màn hình cần test */
  route: '#/ketoan/don-vi-tinh',

  /** Tên form/dialog (dùng trong báo cáo) */
  formName: 'Đơn vị tính',

  /** Loại test: 'all' | 'create-only' | 'update-only' | 'fk-only' */
  testMode: 'all' as 'all' | 'create-only' | 'update-only' | 'fk-only',

  /** Selector nút Thêm mới */
  addButtonSelector: '[data-qa="btn_them_moi"]',

  /** Selector nút Sửa (dòng đầu tiên) */
  editButtonSelector: '[data-qa="btn_sua"]',

  /** Selector nút Lưu */
  saveButtonSelector: '[data-qa="btn_luu"]',

  /** Selector dialog container */
  dialogSelector: '[role="dialog"]',

  /** Danh sách FK fields cần kiểm tra đặc biệt (select đối tượng + TK nợ/có) */
  fkFields: [
    // { dataQa: 'sel_khach_hang', fkField: 'accountObjectId', displayFields: ['objectCode', 'objectName'] },
    // { dataQa: 'sel_tk_no', fkField: 'debitAccountId', displayFields: ['debitAccountNumber'] },
    // { dataQa: 'sel_tk_co', fkField: 'creditAccountId', displayFields: ['creditAccountNumber'] },
  ],

  /** Đường dẫn file types API để đối chiếu DTO (tùy chọn) */
  dtoSource: '',

  /** Thời gian chờ (ms) */
  waitTime: 500,
  saveWaitTime: 1500,
  pageLoadWaitTime: 800,
};

// ═══════════════════════════════════════════════════════════
// 🔑 CREDENTIALS
// ═══════════════════════════════════════════════════════════
const AUTH = {
  baseUrl: 'http://localhost:3000',
  username: '0985908750',
  password: 'Hoadon@2022!#',
};

// ═══════════════════════════════════════════════════════════
// 📡 NETWORK INTERCEPTOR
// ═══════════════════════════════════════════════════════════

interface CapturedRequest {
  url: string;
  method: string;
  postData?: string;
  timestamp: number;
}

interface CapturedResponse {
  url: string;
  status: number;
  body?: string;
  timestamp: number;
}

const capturedRequests: CapturedRequest[] = [];
const capturedResponses: CapturedResponse[] = [];

function setupNetworkInterceptor(page: Page) {
  // Chặn request
  page.on('request', (request) => {
    if (request.method() === 'POST' || request.method() === 'PUT' || request.method() === 'PATCH') {
      capturedRequests.push({
        url: request.url(),
        method: request.method(),
        postData: request.postData() || undefined,
        timestamp: Date.now(),
      });
    }
  });

  // Chặn response
  page.on('response', async (response) => {
    const url = response.url();
    const method = response.request().method();
    if (method === 'POST' || method === 'PUT' || method === 'PATCH' || method === 'GET') {
      try {
        const body = await response.text();
        capturedResponses.push({
          url,
          status: response.status(),
          body: body.length < 50000 ? body : body.substring(0, 50000) + '...(truncated)',
          timestamp: Date.now(),
        });
      } catch {
        capturedResponses.push({ url, status: response.status(), timestamp: Date.now() });
      }
    }
  });
}

function clearCapturedData() {
  capturedRequests.length = 0;
  capturedResponses.length = 0;
}

/** Lấy request POST/PUT cuối cùng liên quan đến form */
function getLastApiCall(): CapturedRequest | undefined {
  return [...capturedRequests].reverse().find(r =>
    r.postData && !r.url.includes('/auth/') && !r.url.includes('/login')
  );
}

/** Lấy response cuối cùng liên quan đến form */
function getLastApiResponse(): CapturedResponse | undefined {
  return [...capturedResponses].reverse().find(r =>
    r.body && !r.url.includes('/auth/') && !r.url.includes('/login')
  );
}

// ═══════════════════════════════════════════════════════════
// 🛠 HELPERS
// ═══════════════════════════════════════════════════════════

let counter = 0;

function generateTestValue(field: any): string {
  counter++;
  const label = (field.label || '').toLowerCase();
  const name = (field.name || '').toLowerCase();
  const dataQa = (field.dataQa || '').toLowerCase();

  if (label.includes('email') || name.includes('email') || dataQa.includes('email'))
    return `test-auto-${counter}@example.com`;
  if (label.includes('điện thoại') || label.includes('sđt') || label.includes('phone') || name.includes('phone') || dataQa.includes('phone'))
    return `098${String(counter).padStart(7, '0')}`;
  if (label.includes('mst') || label.includes('mã số thuế') || name.includes('tax') || dataQa.includes('tax'))
    return `0123456${String(counter).padStart(3, '0')}`;
  if (label.includes('số tài khoản') || name.includes('account') || dataQa.includes('account'))
    return `${counter}234567890`;
  if (field.type === 'number')
    return String(10000 + counter);
  if (label.includes('mã') || name.includes('code') || dataQa.includes('ma'))
    return `TEST-${Date.now().toString(36).toUpperCase()}-${counter}`;
  if (label.includes('tên') || name.includes('name') || dataQa.includes('ten'))
    return `Test Tự Động ${counter} - ${field.label || field.name}`;
  if (label.includes('địa chỉ') || name.includes('address') || dataQa.includes('dia_chi'))
    return '123 Đường Test, P.Bến Thành, Q.1, TP.HCM';
  if (label.includes('mô tả') || label.includes('ghi chú') || name.includes('description') || dataQa.includes('mo_ta'))
    return `[TEST AUTO] Mô tả kiểm tra field update - #${counter}`;
  if (label.includes('link') || label.includes('url') || label.includes('website'))
    return `https://test-${counter}.example.com`;
  if (field.type === 'email') return `test-auto-${counter}@example.com`;
  if (field.type === 'tel') return `098${String(counter).padStart(7, '0')}`;

  return `TEST-${counter}`;
}

function normalizeForCompare(value: string): string {
  return value.replace(/\s+/g, ' ').replace(/[–—−]/g, '-').trim().toLowerCase();
}

function getFailReason(key: string, expected: string, actual: string): string {
  if (!actual || actual === '(không đọc được)')
    return 'Giá trị trả về rỗng → field có thể không được map với BE hoặc không có trong API response';
  if (expected.length !== actual.length)
    return `Độ dài khác nhau (mong đợi ${expected.length}, thực tế ${actual.length}) → có thể bị truncate`;
  const expNoNum = normalizeForCompare(expected.replace(/[0-9]/g, ''));
  const actNoNum = normalizeForCompare(actual.replace(/[0-9]/g, ''));
  if (expNoNum === actNoNum)
    return 'Chỉ khác số → định dạng số (dấu phân cách, thập phân) bị thay đổi khi lưu';
  if (actual.includes('??') || actual.includes('�'))
    return 'Lỗi encoding Unicode → BE không hỗ trợ UTF-8 hoặc double-encode';
  return 'Giá trị khác biệt → kiểm tra mapping FE-BE, format, hoặc transform trong hook';
}

// ═══════════════════════════════════════════════════════════
// 🌐 BROWSER SETUP
// ═══════════════════════════════════════════════════════════

function isDaemonRunning(): Promise<boolean> {
  return new Promise((resolve) => {
    const sock = createConnection({ port: 9222, host: '127.0.0.1' }, () => {
      sock.destroy(); resolve(true);
    });
    sock.on('error', () => resolve(false));
    sock.setTimeout(1000, () => { sock.destroy(); resolve(false); });
  });
}

async function connectToDaemon(): Promise<{ browser: Browser; context: BrowserContext; page: Page } | null> {
  try {
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const contexts = browser.contexts();
    if (contexts.length === 0) return null;
    const page = await contexts[0].newPage();
    console.log('✅ Đã connect daemon CDP.');
    return { browser, context: contexts[0], page };
  } catch { return null; }
}

async function ensureLoggedIn(page: Page): Promise<void> {
  await page.goto(AUTH.baseUrl, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(CONFIG.pageLoadWaitTime);

  const passInput = page.locator('input[type="password"]').first();
  const needLogin = await passInput.isVisible({ timeout: 3000 }).catch(() => false);

  if (needLogin) {
    console.log('🔐 Đang đăng nhập...');
    await page.getByPlaceholder(/0123456789/).first().fill(AUTH.username);
    await passInput.fill(AUTH.password);
    await page.getByRole('button', { name: /Đăng nhập/i }).click();
    await passInput.waitFor({ state: 'detached', timeout: 20000 }).catch(() => {});
    await page.waitForTimeout(2500);
    console.log('✅ Đăng nhập OK');
  } else {
    console.log('✅ Đã có session, không cần login');
  }
}

// ═══════════════════════════════════════════════════════════
// 🔍 QUÉT FIELDS
// ═══════════════════════════════════════════════════════════

async function scanFields(page: Page): Promise<any[]> {
  return page.evaluate((dialogSelector) => {
    const dialog = document.querySelector(dialogSelector);
    const scope = dialog || document;

    const inputs = scope.querySelectorAll(
      'input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]), textarea, select, [role="combobox"]'
    );

    return Array.from(inputs)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 20 || rect.height < 20) return null;

        const htmlEl = el as HTMLElement;
        const inputEl = el as HTMLInputElement;

        const dataQa = htmlEl.getAttribute('data-qa') || '';
        const name = inputEl.name || '';
        const id = htmlEl.id || '';
        const placeholder = inputEl.placeholder || '';
        const type = inputEl.type || el.tagName.toLowerCase();
        const tag = el.tagName.toLowerCase();
        const role = htmlEl.getAttribute('role') || '';
        const value = inputEl.value || '';
        const disabled = htmlEl.hasAttribute('disabled');
        const readOnly = htmlEl.hasAttribute('readonly');

        let label = '';
        if (id) {
          const lbl = scope.querySelector(`label[for="${id}"]`);
          if (lbl) label = lbl.textContent?.trim() || '';
        }

        return {
          dataQa, name, id, type, tag, role, placeholder, label,
          disabled, readOnly, value,
          y: Math.round(rect.top), x: Math.round(rect.left),
        };
      })
      .filter(Boolean)
      .sort((a, b) => a!.y - b!.y || a!.x - b!.x);
  }, CONFIG.dialogSelector) as any[];
}

// ═══════════════════════════════════════════════════════════
// 🎯 LOCATOR BUILDER
// ═══════════════════════════════════════════════════════════

function getLocator(page: Page, field: any) {
  if (field.dataQa) return page.locator(`[data-qa="${field.dataQa}"]`);
  if (field.name) return page.locator(`[name="${field.name}"]`);
  if (field.id) return page.locator(`#${field.id}`);
  return null;
}

// ═══════════════════════════════════════════════════════════
// 📊 PHÂN TÍCH PAYLOAD & RESPONSE
// ═══════════════════════════════════════════════════════════

interface FieldAnalysis {
  fieldName: string;
  dataQa: string;
  label: string;
  testValue: string;
  inPayload: boolean;
  payloadKey?: string;
  inResponse: boolean;
  responseKey?: string;
  updateOk: boolean;
  savedValue: string;
  notes: string[];
}

async function analyzePayloadResponse(
  payload: Record<string, unknown> | null,
  response: Record<string, unknown> | null,
  filledData: Record<string, string>,
  savedData: Record<string, string>,
  fields: any[],
): Promise<FieldAnalysis[]> {
  const results: FieldAnalysis[] = [];

  for (const field of fields) {
    if (field.disabled || field.readOnly) continue;
    const key = field.dataQa || field.name || field.id;
    const expectedValue = filledData[key] || '';
    const actualValue = savedData[key] || '(không đọc được)';
    const notes: string[] = [];

    // Kiểm tra trong payload
    let inPayload = false;
    let payloadKey: string | undefined;
    if (payload) {
      const flatPayload = flattenObject(payload);
      // Tìm key tương ứng trong payload
      const match = findFieldInPayload(key, flatPayload);
      if (match) {
        inPayload = true;
        payloadKey = match;
      } else {
        notes.push('❌ KHÔNG có trong payload gửi lên BE → FE không gửi field này');
      }
    }

    // Kiểm tra trong response
    let inResponse = false;
    let responseKey: string | undefined;
    if (response) {
      const flatResponse = flattenObject(response);
      const match = findFieldInPayload(key, flatResponse);
      if (match) {
        inResponse = true;
        responseKey = match;
      } else {
        notes.push('❌ KHÔNG có trong response từ BE → không thể hiển thị lại trên UI');
      }
    }

    // Kiểm tra update
    const updateOk = normalizeForCompare(actualValue) === normalizeForCompare(expectedValue);
    if (!updateOk) {
      notes.push(getFailReason(key, expectedValue, actualValue));
    }

    results.push({
      fieldName: key,
      dataQa: field.dataQa || '',
      label: field.label || '',
      testValue: expectedValue,
      inPayload,
      payloadKey,
      inResponse,
      responseKey,
      updateOk,
      savedValue: actualValue,
      notes,
    });
  }

  return results;
}

/** Làm phẳng object lồng nhau thành key-value */
function flattenObject(obj: Record<string, unknown>, prefix = ''): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}.${key}` : key;
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      Object.assign(result, flattenObject(value as Record<string, unknown>, newKey));
    } else {
      result[newKey] = value;
    }
  }
  return result;
}

/** Tìm field trong payload dựa trên data-qa */
function findFieldInPayload(dataQa: string, flatPayload: Record<string, unknown>): string | undefined {
  const lower = dataQa.toLowerCase();

  // Map data-qa pattern → payload key patterns
  const patterns: Record<string, string[]> = {
    'i_ma': ['code', 'ma'],
    'i_ten': ['name', 'ten'],
    'i_dia_chi': ['address', 'diaChi'],
    'i_dien_thoai': ['phone', 'phoneNumber', 'dienThoai'],
    'i_email': ['email'],
    'i_mst': ['taxCode', 'tax', 'mst', 'maSoThue'],
    'i_mo_ta': ['description', 'moTa', 'note', 'ghiChu'],
    'sel_': ['id', 'id$'],
    'i_so_tai_khoan': ['accountNumber', 'bankAccount', 'soTaiKhoan'],
  };

  // Thử match pattern data-qa
  for (const [prefix, keys] of Object.entries(patterns)) {
    if (lower.startsWith(prefix.toLowerCase())) {
      for (const k of keys) {
        // Tìm key kết thúc bằng mẫu
        for (const pk of Object.keys(flatPayload)) {
          const pkLower = pk.toLowerCase();
          if (k.endsWith('$')) {
            if (pkLower.endsWith(k.replace('$', ''))) return pk;
          } else if (pkLower === k) {
            return pk;
          } else if (pkLower.includes(k) && pkLower.length < k.length + 10) {
            return pk;
          }
        }
      }
    }
  }

  return undefined;
}

// ═══════════════════════════════════════════════════════════
// 🔬 KIỂM TRA FK SELECT
// ═══════════════════════════════════════════════════════════

interface FkCheckResult {
  fkFieldConfig: typeof CONFIG.fkFields[0];
  onlyIdInPayload: boolean;
  payloadContainsCode: boolean;
  payloadContainsName: boolean;
  responseHasId: boolean;
  responseHasCode: boolean;
  responseHasName: boolean;
  responseMissingDisplay: string[];
  payloadKeys: string[];
  responseKeys: string[];
}

async function checkFkFields(
  payload: Record<string, unknown> | null,
  response: Record<string, unknown> | null,
): Promise<FkCheckResult[]> {
  if (!payload || !response) return [];

  const flatPayload = flattenObject(payload);
  const flatResponse = flattenObject(response);
  const results: FkCheckResult[] = [];

  for (const fkConfig of CONFIG.fkFields) {
    const payloadKeys = Object.keys(flatPayload).filter(k => k.toLowerCase().includes(fkConfig.fkField.toLowerCase()));
    const responseKeys = Object.keys(flatResponse).filter(k => k.toLowerCase().includes(fkConfig.fkField.toLowerCase()));

    // Kiểm tra payload chỉ gửi ID
    const payloadContainsCode = payloadKeys.some(k => k.toLowerCase().includes('code'));
    const payloadContainsName = payloadKeys.some(k => k.toLowerCase().includes('name'));
    const onlyIdInPayload = !payloadContainsCode && !payloadContainsName;

    // Kiểm tra response có đủ display fields
    const responseHasId = responseKeys.some(k => k.toLowerCase().includes('id'));
    const responseHasCode = responseKeys.some(k => k.toLowerCase().includes('code'));
    const responseHasName = responseKeys.some(k => k.toLowerCase().includes('name'));

    const responseMissingDisplay: string[] = [];
    for (const df of fkConfig.displayFields) {
      const hasField = Object.keys(flatResponse).some(k => k.toLowerCase().includes(df.toLowerCase()));
      if (!hasField) responseMissingDisplay.push(df);
    }

    results.push({
      fkFieldConfig: fkConfig,
      onlyIdInPayload,
      payloadContainsCode,
      payloadContainsName,
      responseHasId,
      responseHasCode,
      responseHasName,
      responseMissingDisplay,
      payloadKeys,
      responseKeys,
    });
  }

  return results;
}

// ═══════════════════════════════════════════════════════════
// 📝 BÁO CÁO KẾT QUẢ
// ═══════════════════════════════════════════════════════════

function generateReport(
  fieldResults: FieldAnalysis[],
  fkResults: FkCheckResult[],
  apiUrl: string,
  outputDir: string,
) {
  const now = new Date().toISOString().replace(/[:.]/g, '-');
  const reportPath = join(outputDir, `test-ui-report-${CONFIG.formName.replace(/\s+/g, '-').toLowerCase()}-${now}.md`);

  const okCount = fieldResults.filter(r => r.updateOk).length;
  const failCount = fieldResults.filter(r => !r.updateOk).length;
  const missingPayload = fieldResults.filter(r => !r.inPayload);
  const missingResponse = fieldResults.filter(r => !r.inResponse);

  let report = `# 🧪 Báo Cáo Test UI — ${CONFIG.formName}\n\n`;
  report += `- **Thời gian:** ${new Date().toLocaleString('vi-VN')}\n`;
  report += `- **Route:** \`${CONFIG.route}\`\n`;
  report += `- **API gọi:** \`${apiUrl || '(không bắt được)'}\`\n\n`;

  // Tổng quan
  report += `## 📊 Tổng Quan\n\n`;
  report += `| Chỉ số | Kết quả |\n|---|---|\n`;
  report += `| Tổng fields | ${fieldResults.length} |\n`;
  report += `| ✅ Update OK | ${okCount} |\n`;
  report += `| ❌ Update LỖI | ${failCount} |\n`;
  report += `| ⚠️ Thiếu trong Payload | ${missingPayload.length} |\n`;
  report += `| ⚠️ Thiếu trong Response | ${missingResponse.length} |\n`;
  report += `| 🔗 FK fields | ${fkResults.length} |\n\n`;

  // Chi tiết fields
  report += `## 📋 Chi Tiết Từng Field\n\n`;
  report += `| Field | Label | Test Value | Saved Value | Payload | Response | Update | Ghi chú |\n`;
  report += `|-------|-------|------------|-------------|---------|----------|--------|--------|\n`;

  for (const r of fieldResults) {
    const payloadIcon = r.inPayload ? `✅ \`${r.payloadKey}\`` : '❌ THIẾU';
    const responseIcon = r.inResponse ? `✅ \`${r.responseKey}\`` : '❌ THIẾU';
    const updateIcon = r.updateOk ? '✅ OK' : '❌ LỖI';
    const notes = r.notes.join('<br>');
    report += `| \`${r.fieldName}\` | ${r.label} | ${r.testValue.substring(0, 30)} | ${r.savedValue.substring(0, 30)} | ${payloadIcon} | ${responseIcon} | ${updateIcon} | ${notes} |\n`;
  }

  // FK Report
  if (fkResults.length > 0) {
    report += `\n## 🔗 Kiểm Tra FK Select\n\n`;
    report += `| FK Field | Chỉ gửi ID? | Payload có Code? | Payload có Name? | Response có ID? | Response có Code? | Response có Name? | Thiếu display |\n`;
    report += `|----------|------------|-----------------|-----------------|----------------|-----------------|-----------------|--------------|\n`;

    for (const r of fkResults) {
      report += `| \`${r.fkFieldConfig.fkField}\` | ${r.onlyIdInPayload ? '✅ YES' : '❌ NO'} | ${r.payloadContainsCode ? '⚠️ CÓ' : '✅ KHÔNG'} | ${r.payloadContainsName ? '⚠️ CÓ' : '✅ KHÔNG'} | ${r.responseHasId ? '✅' : '❌'} | ${r.responseHasCode ? '✅' : '❌'} | ${r.responseHasName ? '✅' : '❌'} | ${r.responseMissingDisplay.join(', ') || '✅ Đủ'} |\n`;
    }
  }

  // Hành động đề xuất
  if (missingPayload.length > 0 || missingResponse.length > 0 || failCount > 0) {
    report += `\n## 🔧 Hành Động Đề Xuất\n\n`;

    if (missingPayload.length > 0) {
      report += `### Fields thiếu trong Payload (FE không gửi lên BE):\n\n`;
      for (const r of missingPayload) {
        report += `- **\`${r.fieldName}\`** (${r.label}): Kiểm tra hook \`buildFormData\` hoặc logic map DTO → payload\n`;
      }
      report += `\n`;
    }

    if (missingResponse.length > 0) {
      report += `### Fields thiếu trong Response (BE không trả về):\n\n`;
      for (const r of missingResponse) {
        report += `- **\`${r.fieldName}\`** (${r.label}): Cần yêu cầu BE bổ sung field này vào response hoặc FE tự tính\n`;
      }
      report += `\n`;
    }

    if (failCount > 0) {
      report += `### Fields Update Lỗi:\n\n`;
      for (const r of fieldResults.filter(r => !r.updateOk)) {
        report += `- **\`${r.fieldName}\`**: ${r.notes.join(' | ')}\n`;
      }
      report += `\n`;
    }

    // FK recommendations
    for (const r of fkResults.filter(r => r.responseMissingDisplay.length > 0)) {
      report += `### FK \`${r.fkFieldConfig.fkField}\` thiếu display fields:\n`;
      report += `- Response thiếu: ${r.responseMissingDisplay.join(', ')}\n`;
      report += `- Cần: BE trả thêm các field này HOẶC FE tự resolve bằng API khác\n\n`;
    }
  }

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(reportPath, report, 'utf-8');
  console.log(`\n📄 Báo cáo đã lưu: ${reportPath}`);
  return report;
}

// ═══════════════════════════════════════════════════════════
// 🚀 MAIN
// ═══════════════════════════════════════════════════════════

async function main() {
  console.log(`\n🧪 TEST UI — ${CONFIG.formName}`);
  console.log(`   Route: ${AUTH.baseUrl}/${CONFIG.route}`);
  console.log(`   Mode: ${CONFIG.testMode}`);
  console.log('═'.repeat(60));

  // ── Kết nối browser ──
  let browser: Browser;
  let context: BrowserContext;
  let page: Page;

  const daemon = await isDaemonRunning();
  if (daemon) {
    const conn = await connectToDaemon();
    if (conn) {
      browser = conn.browser;
      context = conn.context;
      page = conn.page;
    } else {
      browser = await chromium.launch({ headless: false });
      context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      page = await context.newPage();
    }
  } else {
    console.log('⚠️ Daemon không chạy, mở browser mới.');
    browser = await chromium.launch({ headless: false });
    context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    page = await context.newPage();
  }

  // Setup network interceptor
  setupNetworkInterceptor(page);

  try {
    // ── B1: Login & Navigate ──
    await ensureLoggedIn(page);
    await page.goto(`${AUTH.baseUrl}/${CONFIG.route}`);
    await page.waitForTimeout(CONFIG.pageLoadWaitTime);

    // Đóng popup nếu có
    await page.getByRole('button', { name: /Đã hiểu|OK|Đồng ý/i }).click({ timeout: 3000 }).catch(() => {});

    // ── B2: Mở dialog Thêm mới ──
    console.log('\n📋 Bước 1: Mở dialog Thêm mới...');
    try {
      await page.locator(CONFIG.addButtonSelector).click({ timeout: 5000 });
    } catch {
      await page.getByRole('button', { name: /Thêm/i }).first().click({ timeout: 5000 });
    }
    await page.waitForTimeout(CONFIG.waitTime);

    // ── B3: Quét fields ──
    console.log('📋 Bước 2: Quét fields trong dialog...');
    const fields = await scanFields(page);

    if (fields.length === 0) {
      console.log('❌ KHÔNG TÌM THẤY FIELD NÀO!');
      await page.screenshot({ path: 'test-results/test-ui-no-fields.png', fullPage: true });
      return;
    }

    console.log(`   Tìm thấy ${fields.length} fields:`);
    for (const f of fields) {
      const id = f.dataQa || f.name || f.id;
      const hasQa = f.dataQa ? '✅' : '⚠️';
      console.log(`   ${hasQa} ${id.padEnd(30)} [${f.type}] ${f.label || ''}`);
    }

    const missingQa = fields.filter(f => !f.dataQa && !f.disabled && !f.readOnly);
    if (missingQa.length > 0) {
      console.log(`\n⚠️ CẢNH BÁO: ${missingQa.length} fields KHÔNG có data-qa:`);
      missingQa.forEach(f => console.log(`   → ${f.name || f.id} (${f.label || f.placeholder})`));
    }

    if (CONFIG.testMode === 'create-only' || CONFIG.testMode === 'all') {
      // ── B4: Fill dữ liệu test + Lưu (Create) ──
      console.log('\n📋 Bước 3: Fill dữ liệu test...');
      clearCapturedData(); // Clear trước khi fill

      const filledData: Record<string, string> = {};

      for (const field of fields) {
        if (field.disabled || field.readOnly) {
          console.log(`   ⏭️ Bỏ qua disabled/readOnly: ${field.dataQa || field.name}`);
          continue;
        }

        const locator = getLocator(page, field);
        if (!locator) {
          console.log(`   ❌ Không tìm được locator: ${field.name || field.id}`);
          continue;
        }

        const key = field.dataQa || field.name || field.id;
        const testValue = generateTestValue(field);

        try {
          if (field.role === 'combobox') {
            await locator.click();
            await page.waitForTimeout(300);
            const firstOption = page.locator('[role="option"]').first();
            if (await firstOption.isVisible({ timeout: 2000 }).catch(() => false)) {
              const optionText = await firstOption.textContent();
              await firstOption.click();
              await page.waitForTimeout(200);
              filledData[key] = optionText?.trim() || '';
              console.log(`   ✅ ${key} → chọn "${filledData[key]}"`);
            } else {
              console.log(`   ⚠️ ${key} → combobox không có option`);
            }
          } else if (field.tag === 'select') {
            const options = await locator.locator('option').all();
            if (options.length > 1) {
              await locator.selectOption({ index: 1 });
              filledData[key] = await locator.inputValue();
              console.log(`   ✅ ${key} → "${filledData[key]}"`);
            }
          } else {
            await locator.fill(testValue);
            filledData[key] = testValue;
            console.log(`   ✅ ${key} → "${testValue}"`);
          }
        } catch (e: any) {
          console.log(`   ❌ ${key} → LỖI: ${e.message}`);
        }
      }

      console.log(`\n   📝 Đã fill ${Object.keys(filledData).length} fields`);

      // ── B5: Lưu & chặn payload/response ──
      console.log('\n📋 Bước 4: Lưu (Create) + chặn API...');
      try {
        await page.locator(CONFIG.saveButtonSelector).click({ timeout: 5000 });
      } catch {
        await page.getByRole('button', { name: /Lưu|Cất|Lưu lại/i }).click({ timeout: 5000 });
      }
      await page.waitForTimeout(CONFIG.saveWaitTime);

      // Phân tích payload & response
      const apiCall = getLastApiCall();
      const apiResponse = getLastApiResponse();

      let payload: Record<string, unknown> | null = null;
      let response: Record<string, unknown> | null = null;

      if (apiCall) {
        console.log(`\n📡 API Gọi: ${apiCall.method} ${apiCall.url}`);
        try {
          payload = JSON.parse(apiCall.postData || '{}');
          console.log(`   Payload keys: ${Object.keys(payload).join(', ')}`);
        } catch {
          console.log('   ⚠️ Không parse được payload');
        }
      }

      if (apiResponse) {
        console.log(`📡 Response: ${apiResponse.status} ${apiResponse.url}`);
        try {
          response = JSON.parse(apiResponse.body || '{}');
          if (response?.data) {
            const dataKeys = Object.keys(response.data as Record<string, unknown>);
            console.log(`   Response data keys: ${dataKeys.join(', ')}`);
          }
        } catch {
          console.log('   ⚠️ Không parse được response');
        }
      }

      // ── Phân tích field trong payload/response ──
      const fieldResults = await analyzePayloadResponse(
        payload,
        response?.data ? (response.data as Record<string, unknown>) : response,
        filledData,
        {},
        fields,
      );

      // ── FK check ──
      const fkResults = await checkFkFields(
        payload,
        response?.data ? (response.data as Record<string, unknown>) : response,
      );

      // ── In kết quả nhanh ──
      console.log('\n' + '═'.repeat(60));
      console.log('📊 PHÂN TÍCH PAYLOAD & RESPONSE (CREATE)');
      console.log('═'.repeat(60));

      const missingPayload = fieldResults.filter(r => !r.inPayload);
      const missingResponse = fieldResults.filter(r => !r.inResponse);

      if (missingPayload.length > 0) {
        console.log(`\n❌ PAYLOAD THIẾU (${missingPayload.length} fields không được gửi lên BE):`);
        missingPayload.forEach(r => console.log(`   → ${r.fieldName} (${r.label})`));
      }

      if (missingResponse.length > 0) {
        console.log(`\n❌ RESPONSE THIẾU (${missingResponse.length} fields không có trong response):`);
        missingResponse.forEach(r => console.log(`   → ${r.fieldName} (${r.label})`));
      }

      // FK Report
      if (fkResults.length > 0) {
        console.log(`\n🔗 KIỂM TRA FK:`);
        for (const r of fkResults) {
          console.log(`   → ${r.fkFieldConfig.fkField}:`);
          console.log(`     Payload chỉ gửi ID: ${r.onlyIdInPayload ? '✅ YES' : '❌ NO (gửi cả code/name)'}`);
          console.log(`     Response thiếu display: ${r.responseMissingDisplay.join(', ') || '✅ ĐỦ'}`);
        }
      }

      // ── B6: Mở lại Edit để đọc dữ liệu ──
      if (CONFIG.testMode === 'all') {
        console.log('\n📋 Bước 5: Tìm bản ghi → mở Edit...');

        const maKey = Object.keys(filledData).find(k => k.includes('ma') || k.includes('code'));
        if (maKey && filledData[maKey]) {
          try {
            await page.locator('[data-qa="i_keyword"]').fill(filledData[maKey]);
            await page.locator('[data-qa="btn_tim_kiem"]').click();
            await page.waitForTimeout(1000);
          } catch { /* fallback */ }
        }

        await page.waitForTimeout(500);
        try {
          await page.locator(CONFIG.editButtonSelector).first().click({ timeout: 5000 });
        } catch {
          await page.locator('.icon-primary').first().click({ timeout: 5000 });
        }
        await page.waitForTimeout(CONFIG.waitTime);

        // ── B7: Đọc lại dữ liệu ──
        console.log('📋 Bước 6: Đọc lại dữ liệu sau lưu...');
        const savedData: Record<string, string> = {};

        for (const field of fields) {
          if (field.disabled || field.readOnly) continue;
          const locator = getLocator(page, field);
          if (!locator) continue;
          const key = field.dataQa || field.name || field.id;

          try {
            if (field.role === 'combobox') {
              savedData[key] = (await locator.textContent())?.trim() || '';
            } else {
              savedData[key] = (await locator.inputValue()) || '';
            }
          } catch {
            savedData[key] = '(không đọc được)';
          }
        }

        // ── B8: So sánh update ──
        console.log('\n📋 Bước 7: So sánh dữ liệu update...');
        const updateResults: { field: string; expected: string; actual: string; ok: boolean; note: string }[] = [];

        for (const [key, expectedValue] of Object.entries(filledData)) {
          const actualValue = savedData[key] || '(không đọc được)';
          const ok = normalizeForCompare(actualValue) === normalizeForCompare(expectedValue);
          updateResults.push({
            field: key, expected: expectedValue, actual: actualValue, ok,
            note: ok ? '✅ OK' : getFailReason(key, expectedValue, actualValue),
          });
        }

        const okCount = updateResults.filter(r => r.ok).length;
        const failCount = updateResults.filter(r => !r.ok).length;

        console.log(`\n✅ OK: ${okCount}  ❌ LỖI: ${failCount}  📋 Tổng: ${updateResults.length}`);

        for (const r of updateResults) {
          console.log(`${r.ok ? '✅' : '❌'} ${r.field}`);
          if (!r.ok) {
            console.log(`   Mong đợi: "${r.expected}"`);
            console.log(`   Thực tế:  "${r.actual}"`);
            console.log(`   Lý do:    ${r.note}`);
          }
        }

        // Cập nhật field results với saved data
        for (const ur of updateResults) {
          const fr = fieldResults.find(f => f.fieldName === ur.field);
          if (fr) {
            fr.updateOk = ur.ok;
            fr.savedValue = ur.actual;
            if (!ur.ok) fr.notes.push(ur.note);
          }
        }
      }

      // ── B9: Generate báo cáo ──
      const apiUrl = apiCall?.url || '';
      const report = generateReport(fieldResults, fkResults, apiUrl, 'test-results');
      console.log(report);

      // Screenshot
      await page.screenshot({
        path: `test-results/test-ui-${CONFIG.formName.replace(/\s+/g, '-').toLowerCase()}.png`,
        fullPage: true,
      });

    }
  } catch (e: any) {
    console.log(`\n❌ LỖI KHÔNG MONG ĐỢI: ${e.message}`);
    await page.screenshot({ path: 'test-results/test-ui-error.png', fullPage: true });
  } finally {
    const usingDaemon = await isDaemonRunning();
    if (!usingDaemon) {
      await browser.close();
    }
    console.log('\n🏁 Test UI hoàn tất.');
  }
}

main().catch(console.error);
```

---

## 📋 Hướng Dẫn Agent — Các Bước Thực Hiện

### Bước 0: Xác Định Phạm Vi

1. Dùng skill `xac-dinh-pham-vi` để xác định route, page, dialog cần test
2. Đọc file page/dialog để lấy danh sách `data-qa` selectors
3. Xác định loại test:
   - `all`: Create + Update + FK (mặc định)
   - `create-only`: Chỉ kiểm tra payload/response khi create
   - `update-only`: Chỉ kiểm tra field update sau khi có bản ghi
   - `fk-only`: Chỉ kiểm tra FK select fields

### Bước 0.5: Đối Chiếu DTO BE (Nếu Có)

> **Nếu user cung cấp DTO mới:** Thực hiện đối chiếu DTO trước khi test UI.

1. **Đọc DTO hiện tại** từ file types (VD: `DM.types.api.ts`, `PC.types.api.ts`)
2. **Parse DTO mới** từ input của user (text/json/typescript interface)
3. **So sánh & báo cáo diff:**
   - 🟢 Field THÊM MỚI trong DTO mới
   - 🔴 Field ĐÃ XÓA khỏi DTO mới
   - 🟡 Field ĐỔI KIỂU (number → string, optional → required...)
4. **Hỏi user:** "DTO có thay đổi so với hiện tại. Có muốn cập nhật types theo DTO mới không?"
5. Nếu user đồng ý → cập nhật types file
6. **Dùng DTO (mới hoặc cũ) làm chuẩn** để kiểm tra payload:
   - Các field required trong DTO → PHẢI có trong payload
   - Các field optional nhưng có UI editable → NÊN có trong payload
   - Các field không có trong DTO → KHÔNG được có trong payload

> **Nếu user KHÔNG cung cấp DTO:** Tự động đọc types file hiện tại làm chuẩn để đối chiếu.

### Bước 1: Tạo Script Test

1. Copy template trên → lưu vào `e2e/test-ui-<ten-trang>.ts`
2. Sửa `CONFIG`:
   - `route`: Hash route màn hình
   - `formName`: Tên hiển thị
   - Các selector cho nút Thêm, Sửa, Lưu
   - `fkFields`: Khai báo các FK field cần kiểm tra đặc biệt (bao gồm cả TK nợ/có)
     ```typescript
     fkFields: [
       { dataQa: 'sel_khach_hang', fkField: 'accountObjectId', displayFields: ['objectCode', 'objectName', 'objectAddress'] },
       { dataQa: 'sel_nhan_vien', fkField: 'employeeId', displayFields: ['employeeCode', 'employeeName'] },
       // TK nợ/có: expect response có accountNumber
       { dataQa: 'sel_tk_no', fkField: 'debitAccountId', displayFields: ['debitAccountNumber'] },
       { dataQa: 'sel_tk_co', fkField: 'creditAccountId', displayFields: ['creditAccountNumber'] },
     ],
     ```
   - `dtoSource`: (TÙY CHỌN) Đường dẫn file types hoặc DTO text từ user
     ```typescript
     /** Đường dẫn file types API để đối chiếu DTO */
     dtoSource: 'src/modules/KetoanApp/features/nghiep-vu/mua-hang/don-mua/types/DM.types.api.ts',
     ```

### Bước 2: Chạy Script

```powershell
# Sử dụng daemon nếu đang chạy (không cần login lại)
npx tsx e2e/test-ui-<ten-trang>.ts

# Hoặc chạy standalone (tự mở browser)
```

### Bước 3: Phân Tích Kết Quả

Script sẽ tạo báo cáo `test-results/test-ui-report-<ten-form>-<timestamp>.md` với các phần:

1. **Tổng quan:** Số lượng fields, OK/Lỗi, Thiếu payload/response
2. **Chi tiết từng field:** Bảng field-by-field với payload key, response key, update status
3. **FK Report:** Kiểm tra payload chỉ gửi ID, response có đủ display fields
4. **TK Nợ/Có Report:** Kiểm tra payload chỉ gửi `debitAccountId`/`creditAccountId`, response có `debitAccountNumber`/`creditAccountNumber`
5. **DTO Diff Report:** (nếu có) So sánh DTO cũ vs mới, field thừa/thiếu trong payload so với DTO
6. **Hành động đề xuất:** Các file cần sửa, field cần thêm

### Bước 4: Hành Động Sau Test

Dựa vào báo cáo, thực hiện các hành động:

| Phát hiện | Hành động | Cần xác định |
|-----------|----------|-------------|
| Field thiếu trong payload | Sửa hook `buildFormData` — thêm field vào object gửi lên | — |
| Field thiếu trong response | Gửi inbox cho BE yêu cầu bổ sung, HOẶC FE tự resolve | **API endpoint + method + DTO name** (xem Bước 5) |
| FK gửi cả code/name (không chỉ ID) | Sửa `TableSearchCombobox` onChange → chỉ set ID | — |
| FK response thiếu display | Resolve trong `buildFormData` hook (Pattern A - ưu tiên) | — |
| TK nợ/có gửi cả accountNumber | Sửa `buildFormData` → chỉ gửi `debitAccountId`/`creditAccountId` | — |
| TK nợ/có response thiếu accountNumber | Gửi inbox BE hoặc resolve trong `buildFormData` | — |
| TableSearchCombobox hiển thị sai khi Edit | Thêm resolve trong `buildFormData` (fetch getById/list) | — |
| Field update sai giá trị | Kiểm tra transform/format trong hook, hoặc BE trả về sai | — |
| DTO thay đổi → types chưa cập nhật | Cập nhật types file theo DTO mới | — |

> **Khi báo lỗi BE:** KHÔNG chỉ nói "BE thiếu field X". Phải chỉ rõ: API nào, method nào, DTO nào, thêm vào response hay request. Format: xem **Bước 5** bên dưới.

---

## 📋 Bước 5: Báo Cáo Lỗi BE — Format Chuẩn

> **Khi phát hiện BE thiếu field, PHẢI báo cáo đầy đủ thông tin để BE biết chính xác sửa ở đâu.**

### 5.1 Format Báo Cáo Lỗi BE

Mỗi field thiếu PHẢI được mô tả với **6 thông tin bắt buộc**:

```
Field: <tên field bị thiếu>
  Route: <hash route màn hình>
  API: <HTTP method> <endpoint path>
  Vị trí: <Response|Request>
  DTO: <tên interface/class BE hiện tại>
  So sánh: <DTO tương tự đã có field này (nếu có)>
  Hành động: <mô tả chính xác cách sửa>
```

### 5.2 Bảng Format Chuẩn

| # | Field | API Endpoint | Method | Vị trí | DTO hiện tại | So sánh | Hành động |
|---|-------|-------------|--------|--------|-------------|---------|----------|
| 1 | | | | **Response** / **Request** | | | |

**Giải thích các cột:**

| Cột | Ý nghĩa | Ví dụ |
|-----|---------|-------|
| **Field** | Tên field bị thiếu (camelCase) | `postedDate` |
| **API Endpoint** | Đường dẫn API đầy đủ | `/api/accounting/v1/bank/transfers/{id}` |
| **Method** | HTTP method | GET / POST / PUT |
| **Vị trí** | Missing ở response hay request body | **Response** (GET trả thiếu) / **Request** (POST/PUT không nhận) |
| **DTO hiện tại** | Tên class/interface BE đang dùng + ghi chú | `BankTransferDetail` KHÔNG có field này |
| **So sánh** | DTO tương tự CÓ field này → làm bằng chứng BE đã có pattern | `BankDepositDetail` CÓ `postedDate` |
| **Hành động** | Mô tả chính xác việc BE cần làm | BE thêm `postedDate` vào `BankTransferDetail` response |

### 5.3 Ví Dụ Cụ Thể

```
🔴 BE THIẾU postedDate trong response:

  Route:   #/ketoan/tien-gui/chuyen-tien-noi-bo
  API:     GET /api/accounting/v1/bank/transfers/{id}
  Vị trí:  Response body
  DTO:     BankTransferDetail KHÔNG có postedDate
  So sánh: BankDepositDetail (GET /receipts/{id}) CÓ postedDate
  ↓
  Hành động BE:
    Thêm `postedDate` (DateTime?) vào `BankTransferDetail` response DTO.
    Khi GET /api/accounting/v1/bank/transfers/{id}, trả về postedDate
    từ bản ghi trong DB.

🔴 BE THIẾU postedDate trong request:

  Route:   #/ketoan/tien-gui/chuyen-tien-noi-bo
  API:     POST /api/accounting/v1/bank/transfers
           PUT  /api/accounting/v1/bank/transfers/{id}
  Vị trí:  Request body
  DTO:     CreateBankTransferRequest KHÔNG có postedDate
  So sánh: CreateBankReceiptRequest CÓ postedDate?
  ↓
  Hành động BE:
    Thêm `postedDate?` (DateTime?, optional) vào CreateBankTransferRequest.
    Nếu FE gửi postedDate thì lưu, nếu không gửi thì dùng refDate.

🔴 BE THIẾU refNoManagement trong response:

  Route:   #/ketoan/tien-gui/chuyen-tien-noi-bo
  API:     GET /api/accounting/v1/bank/transfers/{id}
  Vị trí:  Response body
  DTO:     BankTransferDetail KHÔNG có refNoManagement
  So sánh: BankDepositDetail CÓ refNoManagement
  ↓
  Hành động BE:
    Thêm `refNoManagement` (string) vào BankTransferDetail response.
    Khi GET /transfers/{id}, trả về số chứng từ (CTNB00001 format).

🟡 BE thiếu debitAccountId/creditAccountId (optional → required):

  Route:   #/ketoan/tien-gui/chuyen-tien-noi-bo
  API:     GET /api/accounting/v1/bank/transfers/{id}
  Vị trí:  Response body → accountingDetails[]
  DTO:     BADepositDetailLineDto.debitAccountId? (optional)
  ↓
  Hành động BE:
    Đổi debitAccountId, creditAccountId trong BADepositDetailLineDto
    từ optional → required. Khi GET /transfers/{id}, luôn trả về
    debitAccountId và creditAccountId trong mỗi accounting detail line.
    (Hiện tại FE phải workaround bằng fetch 9999 TK records)
```

### 5.4 Quy Trình: Từ Phát Hiện → Báo Cáo → Gửi BE

```
[1] Test UI → phát hiện UI field trống khi edit/view
[2] Kiểm tra: FE có map field từ DTO không?
    ├── CÓ map nhưng DTO không có → BE THIẾU → báo cáo
    └── KHÔNG map → FE thiếu → sửa hook
[3] Ghi nhận API endpoint + method từ DevTools Network tab
    hoặc từ service file (TGApiService.ts)
[4] So sánh với DTO tương tự (receipt/payment) xem có field không
[5] Báo cáo theo format Section 5.2 → gửi inbox cho BE
```

---

## 🔬 Phân Tích FK Select Chuyên Sâu

> **Quy tắc:** TableSearchCombobox khi select 1 đối tượng → CHỈ gửi FK ID lên BE, KHÔNG gửi code/name.

### Kiểm tra payload:

```typescript
// ✅ ĐÚNG: Payload chỉ chứa accountObjectId
{ "accountObjectId": "abc-123", ... }

// ❌ SAI: Payload chứa cả code/name (dư thừa, BE không cần)
{ "accountObjectId": "abc-123", "objectCode": "KH001", "objectName": "Nguyễn Văn A", ... }
```

### Kiểm tra response:

```typescript
// ✅ ĐỦ: Response có objectCode + objectName để hiển thị
{
  "accountObjectId": "abc-123",
  "objectCode": "KH001",
  "objectName": "Nguyễn Văn A",
  "objectAddress": "123 Đường ABC"
}

// ❌ THIẾU: Response chỉ có ID, FE không hiển thị được tên
{ "accountObjectId": "abc-123" }

// ⚠️ Cần resolve: FE phải tự fetch thêm bằng API khác
```

### Khi response thiếu display:

**Pattern A (Ưu tiên):** Resolve trong `buildFormData` của Hook (xem `edit-form-pattern.md` trong user memory).

```typescript
// Trong Hook: resolve FK khi build form data
const [khRes] = await Promise.all([
  d.accountObjectId ? KHApiService.getById(d.accountObjectId).catch(() => null) : null,
]);
if (khRes?.data) {
  formData.objectCode = khRes.data.code;
  formData.objectName = khRes.data.name;
}
```

**Pattern B:** Resolve trong Dialog `useEffect` (kém tối ưu hơn).

---

## 🏦 Phân Tích TK Nợ / TK Có Chuyên Sâu

> **Quy tắc:** Field chọn tài khoản nợ/có trong bảng hạch toán → CHỈ gửi `debitAccountId` / `creditAccountId`, KHÔNG gửi account number.

### Kiểm tra payload accountingDetails[]:

```typescript
// ✅ ĐÚNG: Mỗi dòng hạch toán chỉ gửi ID
{
  "accountingDetails": [
    {
      "debitAccountId": "guid-1",
      "creditAccountId": "guid-2",
      "amount": 1000000,
      "description": "Thu tiền hàng"
    }
  ]
}

// ❌ SAI: Gửi cả account number cùng với ID
{
  "accountingDetails": [
    {
      "debitAccountId": "guid-1",
      "debitAccountNumber": "111",   // ← XÓA
      "creditAccountId": "guid-2",
      "creditAccountNumber": "331",  // ← XÓA
      "amount": 1000000
    }
  ]
}
```

### Kiểm tra response:

```typescript
// ✅ ĐỦ: Response có account number để hiển thị
{
  "accountingDetails": [
    {
      "debitAccountId": "guid-1",
      "debitAccountNumber": "111",    // ← CẦN CÓ
      "creditAccountId": "guid-2",
      "creditAccountNumber": "331",   // ← CẦN CÓ
      "amount": 1000000
    }
  ]
}

// ❌ THIẾU: Response không có account number
// → FE phải resolve bằng AccountApiService.list()
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Dev server phải đang chạy** ở `http://localhost:3000` — KHÔNG tự khởi động
2. **Daemon mode được khuyến nghị** — không cần login lại mỗi lần chạy
3. **KHÔNG đóng browser** khi dùng daemon — script tự connect
4. **Network interceptor** chỉ bắt API calls trong cùng page context
5. **FK fields + TK nợ/có** cần khai báo thủ công trong CONFIG — script không tự phát hiện
6. **DTO đối chiếu** — nếu user cung cấp DTO, ưu tiên DTO làm chuẩn; nếu không, đọc types file hiện tại
7. **Thời gian chờ** có thể cần điều chỉnh tùy theo tốc độ BE
8. **Tiếng Việt Unicode** — script dùng UTF-8, không dùng PowerShell để đọc/ghi kết quả
9. **TableSearchCombobox resolve** — Luôn resolve trong `buildFormData` (Pattern A), KHÔNG resolve trong `useEffect` dialog (Pattern B)
10. **Hiển thị name khi resolve** — Nếu combobox hiển thị "code - name" khi select, resolve cũng phải hiển thị "code - name"

---

## 🛠 Troubleshooting

| Vấn đề | Giải pháp |
|--------|----------|
| Không tìm thấy fields | Kiểm tra `dialogSelector`, tăng `waitTime` |
| Không login được | Kiểm tra credentials, xóa `auth.json` nếu session hết hạn |
| Payload rỗng | API có thể gọi qua WebSocket hoặc khác origin — dùng `page.route()` để intercept |
| Combobox không mở | Tăng `waitTime` sau click, thử dùng `page.keyboard.press('ArrowDown')` |
| Mã tự động (AutoCode) không xuất hiện | Bỏ qua field code khi test create — BE tự sinh |
| Toast lỗi sau lưu | Đọc nội dung toast → báo cáo lỗi validate |
| Response truncated | Tăng giới hạn 50000 trong `capturedResponse.body` |
