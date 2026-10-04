---
name: lam-task-inbox
description: 'Nhận và xử lý 1 task inbox cụ thể theo ID: đọc mô tả (FE yêu cầu) + phản hồi (BE result) → so sánh BE fix đủ chưa → test API (test-api) → implement code FE → test UI (Playwright) → báo cáo hoàn thành. Dùng khi: user đưa ID task inbox, "làm task inbox #xxx". KHÔNG dùng để check inbox hàng loạt — dùng inbox-check cho việc đó.'
argument-hint: 'ID của task inbox cần xử lý. VD: task-abc123, #456, hoặc để trống để tự check inbox.'
---

# Làm Task Inbox — FrontendWeb

> **Mục tiêu:** Nhận 1 task inbox → đọc cả mô tả FE (description) và phản hồi BE (result) → so sánh BE đã fix đủ field chưa → test API bằng `test-api` → nếu OK mới implement code FE → test UI bằng Playwright → báo cáo.

---

## 🔢 AgentType Enum

| Giá trị | Tên | Vai trò |
|---------|-----|---------|
| `0` | Backend | BE — nhận task từ FE, implement API |
| `1` | **FrontendWeb** | **Chúng ta — tạo task yêu cầu BE, implement FE sau khi BE done** |
| `2` | FrontendApp | Mobile App |
| `3` | QA | Kiểm thử |
| `4` | DocWriter | Viết tài liệu |

---

## ⚠️ QUY TẮC BẮT BUỘC

1. **Phân biệt 2 luồng task inbox:**
   - **Task do FE tạo gửi BE** (`CreatedByUser: "FrontendWeb"`, `AssignedTo: "Backend"`): Đây là yêu cầu FE gửi BE bổ sung API. Khi BE Done → FE cần **verify BE + test API** rồi mới code FE.
   - **Task giao cho FE** (`AssignedTo: "FrontendWeb"`): Task thuần FE, làm trực tiếp.
2. **KHÔNG tự ý thêm cột vào bảng data** — chỉ sửa bảng (page, table settings, ALL_COLUMNS) nếu task description mô tả rõ cần hiển thị cột mới.
3. **Phải so sánh FE description vs BE result** — kiểm tra BE đã implement đủ field FE yêu cầu chưa trước khi code.
4. **Phải test API trước khi code FE** — dùng skill `test-api` để verify field mapping đúng (bắt buộc với luồng FE→BE).
5. **Trước khi sửa code FE → phải load skill liên quan** — không tự suy diễn.
6. **Mọi inbox reply đều phải hiển thị draft để user review trước khi gửi.**

---

## 🔧 MCP Tools Sử Dụng

```
# Xem chi tiết task inbox
mcp_hub-mcp_inbox-detail
  taskId: string
  → Trả về: title, description, agentType, status, priority, result (BE result nếu có)

# Báo cáo tiến độ (→ InProgress)
mcp_hub-mcp_report-task-progress
  taskId:       string
  progressNote: string

# Đánh dấu hoàn thành
mcp_hub-mcp_inbox-completed
  taskId: string
  result: string

# Hủy task
mcp_hub-mcp_inbox-cancel
  taskId:       string
  cancelReason: string
```

---

## 🚀 Quy Trình Xử Lý (8 Bước)

```
┌──────────────────────────────────────────────────────────────────┐
│ B1: inbox-detail → đọc description (FE yêu cầu) + result (BE)   │
│ B2: Xác định luồng: FE→BE hay FE thuần?                         │
│ B3: Kiểm tra status → BE Done mới tiếp tục                      │
│ B4: So sánh FE yêu cầu vs BE result → BE fix đủ chưa?           │
│ B5: Test API bằng test-api → verify field mapping               │
│ B6: Implement code FE (chỉ nếu B4+B5 PASS)                      │
│ B7: Test UI bằng Playwright (test-field-update)                 │
│ B8: Báo cáo → report-task-progress → inbox-completed            │
└──────────────────────────────────────────────────────────────────┘
```

---

### Bước 1 — Đọc Chi Tiết Task

```typescript
// Gọi MCP tool để lấy chi tiết task
mcp_hub-mcp_inbox-detail({ taskId: "<ID từ user>" })
```

**Thông tin cần trích xuất:**

| Trường | Ý nghĩa | Dùng để |
|--------|---------|---------|
| `title` | Tiêu đề task | Tổng quan |
| `description` | **Mô tả từ FE** — field nào cần bổ sung, API endpoint nào | So sánh với BE result |
| `assignedTo` | Ai được giao ("Backend" / "FrontendWeb") | Xác định luồng |
| `createdByUser` | Ai tạo task ("FrontendWeb" / "Backend") | Xác định luồng |
| `status` | Trạng thái hiện tại | Kiểm tra BE done chưa |
| `result` | **Phản hồi từ BE** — API đã sửa những gì, field nào đã thêm | So sánh với FE description |

---

### Bước 2 — Xác Định Luồng Task

Có 2 luồng chính:

#### Luồng A: FE tạo task gửi BE (`createdByUser` = "FrontendWeb", `assignedTo` = "Backend")

Đây là **FE yêu cầu BE bổ sung API**. BE đã làm xong (status = Done/Completed) → FE cần:

1. ✅ **Verify BE**: so sánh FE description vs BE result (B4)
2. ✅ **Test API**: dùng `test-api` verify field mapping (B5)
3. ✅ **Implement FE**: chỉ code FE sau khi API đã verified (B6)

#### Luồng B: Task giao trực tiếp cho FE (`assignedTo` = "FrontendWeb")

Task thuần FE (sửa UI, thêm field vào form có sẵn API...). Làm trực tiếp B6.

```typescript
const isFeToBeTask = detail.createdByUser === 'FrontendWeb' && detail.assignedTo === 'Backend';
const isDirectFeTask = detail.assignedTo === 'FrontendWeb';

if (isFeToBeTask) {
  // Luồng A: FE yêu cầu BE → cần verify BE + test API trước
  console.log('📋 Task do FE tạo gửi BE. Cần verify BE + test API trước khi code FE.');
} else if (isDirectFeTask) {
  // Luồng B: Task giao trực tiếp cho FE
  console.log('📋 Task giao trực tiếp cho FE. Bắt đầu implement.');
} else {
  // Không phải FE → DỪNG
  console.log('❌ Task không liên quan đến FrontendWeb. DỪNG.');
  return;
}
```

---

### Bước 3 — Kiểm Tra Trạng Thái (Status)

> Chỉ tiếp tục khi BE đã Done (có result). Nếu BE chưa xong → báo & DỪNG.

| Status | Hành động |
|--------|-----------|
| `Pending` | ⚠️ DỪNG: "Task Pending — BE chưa làm. Chờ BE implement API trước." |
| `InProgress` (không có result) | ⚠️ DỪNG: "BE đang làm dở, chưa có kết quả." |
| `InProgress` (có result) | ✅ Tiếp tục |
| `Done` / `Completed` | ✅ Tiếp tục |
| `Cancelled` | ❌ DỪNG: "Task đã bị hủy." |

---

### Bước 4 — So Sánh FE Yêu Cầu vs BE Result

> **QUAN TRỌNG (luồng A):** Kiểm tra BE đã fix đúng và đủ những gì FE yêu cầu chưa.

#### 4.1 Trích xuất field FE yêu cầu từ `description`

VD: `"Bổ sung field isActive, province, branchAddress cho API POST/PUT"`
→ FE yêu cầu: `["isActive", "province", "branchAddress"]`

#### 4.2 Trích xuất field BE đã làm từ `result`

VD: `"Đã bổ sung 3 field (isActive, province, branchAddress)..."`
→ BE đã làm: `["isActive", "province", "branchAddress"]`

#### 4.3 Đối chiếu

```typescript
const missing = feRequested.filter(f => !beImplemented.includes(f));
if (missing.length > 0) {
  // ⚠️ BE thiếu field → DỪNG, báo cáo
}
```

| Kết quả | Hành động |
|---------|-----------|
| BE implement đủ tất cả field | ✅ Tiếp tục B5 |
| BE thiếu field | ⚠️ Báo: "BE chưa implement đủ. Thiếu: [list]." → DỪNG |
| BE implement sai khác | ⚠️ Báo chi tiết → hỏi user |

> Với **luồng B** (task thuần FE): bỏ qua B4, vào thẳng B6.

---

### Bước 5 — Test API Bằng test-api

> **BẮT BUỘC với luồng A (FE→BE):** Phải test API thật để verify field mapping trước khi code FE.

```
Load: .claude/skills/test-api/SKILL.md
→ Test endpoint POST + PUT của feature:
  - Đọc DTO từ types
  - Gọi POST tạo bản ghi với đầy đủ field mới
  - GET đọc lại → field nào được lưu, field nào bị mất?
  - Gọi PUT update từng field → GET đọc lại → kiểm tra
  - Báo cáo: field OK / field lỗi
```

| Kết quả test-api | Hành động |
|------------------|-----------|
| Tất cả field OK (POST + PUT) | ✅ Tiếp tục B6 |
| Có field lỗi (API không lưu) | ⚠️ Báo: "API không lưu field [list]. Cần BE sửa." → DỪNG |
| API lỗi 500 / không connect | ⚠️ Báo: "Backend lỗi." → DỪNG |

> **Nếu test-api FAIL:** Soạn inbox draft gửi BE báo lỗi. **Không code FE khi API chưa hoạt động đúng.**

> Với **luồng B** (task thuần FE): bỏ qua B5, vào thẳng B6.

---

### Bước 6 — Implement Code FE

> **CHỈ thực hiện sau khi B4 (so sánh) và B5 (test-api) đều PASS (với luồng A).**
> Với luồng B: vào thẳng bước này.

**Trước khi code, xác định phạm vi:**

Dùng skill `xac-dinh-pham-vi` để tìm chính xác file cần sửa:
```
Load: .claude/skills/xac-dinh-pham-vi/SKILL.md
→ Tìm file dialog/service/hook/page liên quan
```

Dựa vào loại thay đổi, load skill phù hợp:

| Loại thay đổi | Skill cần load |
|---------------|----------------|
| Thêm/sửa field trong dialog | `tao-dialog` + `tao-dialog-new` + `tao-ui-giao-dien-new` |
| Thêm/sửa validate | `validate-input` |
| Sửa API service | `tao-apiservice` + `tich-hop-api-ui` |
| Thêm/sửa filter/phân trang | `filter-phan-trang` |
| Thêm nút "+" tạo nhanh FK | `them-nhanh-fk` |
| Thêm DatePicker | `date-input` |
| Tích hợp auto-code | `auto-code-generation` |
| Sửa layout/page | `tao-ui-master-page` |
| Sửa sub-page | `tao-ui-sub-page` |

**Quy trình implement:**

```
[6.1] Load skill phù hợp → đọc SKILL.md
[6.2] Đọc file hiện tại cần sửa (dialog/hook/service/page)
[6.3] Sửa code theo đúng field đã verified ở B5
[6.4] Đảm bảo tuân thủ quy tắc: data-qa, validate, typing, v.v.
[6.5] Check lint/compile errors → sửa nếu có
```

**⚠️ Nguyên tắc quan trọng:**

- **KHÔNG tự ý thêm cột vào bảng data** — chỉ sửa bảng (page, table settings, ALL_COLUMNS) nếu task description nói rõ cần hiển thị trên bảng. Nếu task chỉ nói "thêm field vào dialog" thì không đụng vào bảng.
- Chỉ sửa những gì task yêu cầu — không refactor ngoài phạm vi
- Giữ nguyên pattern có sẵn trong file
- Thêm `data-qa` cho mọi field mới
- Validate onBlur cho mọi input mới
- Cập nhật types nếu thêm field mới

---

### Bước 7 — Test UI Bằng Playwright

Sau khi code FE xong, test lại bằng Playwright:

```
Load: .claude/skills/test-field-update/SKILL.md
→ Test dialog/form vừa sửa
```

**Nếu test FAIL:** Phân tích → sửa code FE hoặc báo lỗi BE.
**Nếu test PASS:** → Chuyển sang B8.

---

### Bước 8 — Báo Cáo Kết Quả & Hoàn Thành

#### 8.1 Báo cáo tiến độ (report-task-progress)

```typescript
mcp_hub-mcp_report-task-progress({
  taskId: "<taskId>",
  progressNote: `
📋 Phân tích task:
  - FE yêu cầu: <field list từ description>
  - BE đã implement: <field list từ result>
  - Đối chiếu: <đủ/thiếu field nào>

🧪 Kết quả test-api:
  - POST: <field OK / field lỗi>
  - PUT: <field OK / field lỗi>

✅ Đã implement FE:
📁 Files đã sửa:
  - <danh sách file>

🧪 Kết quả test UI (Playwright):
  - <Pass/Fail + chi tiết từng field>
  `
})
```

#### 8.2 Đánh dấu hoàn thành (inbox-completed)

```typescript
mcp_hub-mcp_inbox-completed({
  taskId: "<taskId>",
  result: `
✅ Hoàn thành task: <title>

📋 Đối chiếu FE-BE:
  - FE yêu cầu: <fields>
  - BE implement: <fields>
  - Kết quả: <đủ / thiếu field nào>

🧪 Test API: <Pass/Fail>
  - POST: <field OK / field lỗi>
  - PUT: <field OK / field lỗi>

📝 Implement FE:
  - <liệt kê chi tiết>

📁 Files đã sửa:
  - <danh sách file>

🧪 Test UI (Playwright): <Pass/Fail>

⚠️ Lưu ý (nếu có):
  - <các vấn đề cần lưu ý>
  `
})
```

---

## 📋 Mapping Loại Task → Cách Xử Lý

| Mô tả trong task | Cách xử lý | Skill chính |
|------------------|------------|-------------|
| "Thêm field X vào dialog Y" | Đọc dialog → thêm field → sửa hook → sửa types → test | `tao-dialog` |
| "Sửa validate field X" | Đọc hook → sửa logic validate → test | `validate-input` |
| "Thêm API endpoint mới" | Đọc docs → tạo/update service → tích hợp hook | `tao-apiservice` + `tich-hop-api-ui` |
| "Đổi UI dialog/table" | Đọc component → sửa layout → test UI | `tao-ui-giao-dien-new` |
| "Thêm tab mới vào dialog" | Đọc dialog → thêm tab → thêm section → test | `tao-dialog` + `tao-dialog-new` |
| "Sửa filter/phân trang" | Đọc page → sửa search params → test | `filter-phan-trang` |
| "Thêm nút tạo nhanh FK" | Đọc dialog → thêm nút "+" cạnh combobox | `them-nhanh-fk` |
| "Bổ sung field API" (FE→BE task) | Verify BE + test-api → implement FE | `test-api` + `tao-dialog` |

---

## ❌ Các Trường Hợp Dừng & Báo Cáo

| Tình huống | Hành động |
|------------|-----------|
| Task không liên quan FE (không phải FE→BE, không phải giao FE) | Báo: "Task không liên quan đến FrontendWeb." → DỪNG |
| Status = `Pending` (BE chưa làm) | Báo: "BE chưa implement API. Chờ BE Done." → DỪNG |
| Status = `InProgress` (không có result) | Báo: "BE đang làm dở, chưa có kết quả." → DỪNG |
| Status = `Completed` (đã done từ trước) | Báo: "Task đã hoàn thành trước đó." → DỪNG |
| Status = `Cancelled` | Báo: "Task đã bị hủy." → DỪNG |
| BE thiếu field (B4 đối chiếu) | Báo: "BE chưa implement đủ field: [list]." → DỪNG |
| Test API FAIL (B5) | Báo: "API chưa hoạt động đúng. Chi tiết: [lỗi]." → DỪNG |
| Thiếu thông tin (không rõ form/dialog) | Hỏi user: "Task không ghi rõ cần sửa form nào." |
| Không có skill phù hợp | Báo: "Chưa có skill hướng dẫn. Vui lòng xác nhận hướng xử lý." |

---

## 📎 Ví Dụ Thực Tế

### Ví dụ 1: Task FE→BE — Yêu cầu BE bổ sung API

```
User: /lam-task-inbox 6a43a79aec618b5b6da32457

Agent:
  B1: inbox-detail → description: "Bổ sung field isActive, province, branchAddress
      cho API POST/PUT /api/accounting/v1/master/bank-accounts"
      → assignedTo: "Backend", createdByUser: "FrontendWeb"
      → status: "Done"
      → result: "Đã bổ sung 3 field (isActive, province, branchAddress)..."

  B2: Luồng A (FE→BE) ✅

  B3: Status Done ✅

  B4: Đối chiếu:
      FE yêu cầu: [isActive, province, branchAddress]
      BE implement: [isActive, province, branchAddress]
      → ĐỦ ✅

  B5: Test API:
      Load test-api skill → test POST/PUT
      → POST: isActive ✅, province ✅, branchAddress ✅
      → PUT: isActive ✅, province ✅, branchAddress ✅
      → ALL PASS ✅

  B6: Implement FE:
      - types: thêm province, branchAddress vào DTO
      - Dialog đã có sẵn UI → không cần sửa dialog
      - KHÔNG thêm cột vào bảng (task không yêu cầu)

  B7: Test UI → PASS ✅

  B8: report + completed
```

### Ví dụ 2: Task FE→BE — BE thiếu field

```
User: /lam-task-inbox task-xxx

Agent:
  B1: inbox-detail
      → description: "Bổ sung field email, phone, address vào API Customers"
      → result: "Đã thêm field email, phone vào API Customers"

  B4: Đối chiếu:
      FE yêu cầu: [email, phone, address]
      BE implement: [email, phone]
      → THIẾU: [address] ⚠️

  → Báo: "BE chưa implement đủ. Thiếu field: address.
     Cần tạo inbox-to-be yêu cầu BE bổ sung thêm."
  → DỪNG — không code FE
```

### Ví dụ 3: Task giao trực tiếp cho FE

```
User: /lam-task-inbox task-yyy

Agent:
  B1: inbox-detail
      → assignedTo: "FrontendWeb"
      → description: "Sửa validate email trong dialog Khách hàng"

  B2: Luồng B (FE trực tiếp) ✅

  B3: Status OK ✅

  B6: Implement FE ngay (bỏ qua B4, B5):
      Load validate-input skill
      → useKHForm.ts: sửa validate email

  B7: Test UI → PASS

  B8: report + completed
```

---

## 🔗 Skill Liên Quan

| Skill | Vai trò |
|-------|---------|
| `inbox-check` | Kiểm tra & xử lý nhiều task inbox |
| `inbox-to-be` | Gửi task cho BE |
| `test-api` | **Test API endpoint trước khi code FE** (bắt buộc với luồng FE→BE) |
| `test-field-update` | Test tự động field update trên UI bằng Playwright |
| `xac-dinh-pham-vi` | Tìm file cần sửa từ tên feature |
| `tao-dialog` / `tao-dialog-new` | Tạo/sửa dialog |
| `validate-input` | Validate form input |
| `tao-apiservice` | Tạo/sửa API service |
| `tich-hop-api-ui` | Tích hợp API vào UI |
