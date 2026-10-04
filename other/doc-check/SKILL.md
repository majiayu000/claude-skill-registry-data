---
name: doc-check
description: "Tra cứu đặc tả API endpoint phục vụ xây dựng giao diện và logic FE. Dùng khi: cần biết request/response của API, tìm endpoint theo tính năng, xem tham số đầu vào, kiểu dữ liệu trả về, auth requirements, lấy projectCode, liệt kê danh sách endpoint theo nhóm, theo dõi thay đổi API."
argument-hint: "Mô tả tính năng hoặc tên endpoint cần tra cứu. VD: 'API tạo hóa đơn', 'lấy danh sách khách hàng'..."
---

# Doc Check — Tra Cứu Đặc Tả API Endpoint

## Mục Đích

Giúp FE **tìm và đọc đặc tả API** một cách nhanh chóng để:
- Xác định đúng endpoint cần gọi
- Biết chính xác request body / query params / path params
- Biết cấu trúc response (fields, types)
- Biết yêu cầu xác thực (auth, roles)
- Tránh sai sót khi viết ApiService, hook, và UI

---

## Bộ Tool MCP Có Sẵn

| Tool | Mục đích | Khi nào dùng |
|------|---------|--------------|
| `mcp_hub-mcp_doc-get-projects-list` | Liệt kê tất cả project tài liệu đang active | Khi chưa biết `projectCode` |
| `mcp_hub-mcp_doc-get-project-context` | Lấy URL môi trường, authType, danh sách groups | Khi cần biết base URL hoặc groups của project |
| `mcp_hub-mcp_doc-search-api-docs` | **Tìm endpoint bằng ngôn ngữ tự nhiên** (hybrid search) | Đây là bước đầu tiên khi tìm endpoint |
| `mcp_hub-mcp_doc-get-endpoint` | Lấy đặc tả đầy đủ 1 endpoint theo `endpointId` | Sau khi có `endpointId` từ kết quả search |
| `mcp_hub-mcp_doc-get-by-id` | Lấy đặc tả đầy đủ 1 endpoint theo ObjectId | Thay thế khi có `id` nhưng không có `projectCode` |
| `mcp_hub-mcp_doc-get-by-endpoint` | Lấy đặc tả theo HTTP method + path | Khi đã biết rõ method và path chính xác |
| `mcp_hub-mcp_doc-get-list-endpoints` | Liệt kê tất cả endpoint (tóm tắt, không có spec) | Khi muốn duyệt danh sách theo group |
| `mcp_hub-mcp_doc-get-changes` | Lấy danh sách endpoint được cập nhật từ ngày X | Khi cần biết API nào đã thay đổi gần đây |
| `mcp_hub-mcp_doc-search-user-docs` | Tìm tài liệu nghiệp vụ: UserGuide, BusinessRule | Khi cần hiểu luồng nghiệp vụ, quy tắc kinh doanh |
| `mcp_hub-mcp_doc-search-list-articles` | Liệt kê tóm tắt bài viết tài liệu | Khi muốn xem danh sách bài viết theo loại |
| `mcp_hub-mcp_doc-search-get-article` | Lấy full content bài viết theo `slug` hoặc `articleId` | Sau khi có slug từ `search-list-articles` |

---

## Quy Trình Chuẩn — Tìm Đặc Tả Endpoint

### Bước 1 — Xác định projectCode

> Nếu chưa biết `projectCode`, gọi:

```
mcp_hub-mcp_doc-get-projects-list
```

Các `projectCode` thường dùng trong SASUCO:

| projectCode | Mô tả |
|-------------|-------|
| `INVOICE` | Hóa đơn điện tử — portal Business/Admin |
| `BASE_INDEX` | Dữ liệu nền — danh mục, tổ chức, hàng hóa |
| `KETOAN_HKD` | Kế toán hộ kinh doanh |
| `PARTNER` | Portal đối tác |
| `SSO` | Xác thực, đăng nhập, quản lý người dùng |

---

### Bước 2 — Tìm Endpoint Theo Tính Năng

Gọi `mcp_hub-mcp_doc-search-api-docs` với câu query mô tả tính năng:

```
projectCode: "INVOICE"
query: "tạo hóa đơn điều chỉnh"
limit: 5
```

**Kết quả trả về:**
- `endpointId` — dùng để gọi `get-endpoint`
- `title`, `httpMethod`, `routePath` — tóm tắt
- `score` — độ tương đồng

> Nếu biết trước `groupCode` → truyền thêm để thu hẹp kết quả.

---

### Bước 3 — Lấy Đặc Tả Đầy Đủ

Gọi `mcp_hub-mcp_doc-get-endpoint` với `endpointId` và `projectCode` từ bước 2:

```
endpointId: "<id từ kết quả search>"
projectCode: "INVOICE"
```

**Đặc tả đầy đủ bao gồm:**
- HTTP method + route path
- Request body schema (fields, types, required/optional)
- Query params / path params
- Response schema (success + error)
- `requiresAuth`, `requiredRoles`
- Tags, version, mô tả chi tiết

---

### Bước 4 — Áp Dụng Vào FE

Sau khi có đặc tả, thực hiện:

1. **Định nghĩa TypeScript interfaces** cho request/response theo schema
2. **Viết ApiService** theo skill `tao-apiservice`
3. **Viết Hook** gọi service theo skill `tich-hop-api-ui`
4. **Build UI** với đúng tên field, validation rules theo required fields

---

## Tra Cứu Khi Đã Biết Method + Path

Nếu đã biết chính xác method và path (VD từ code cũ hoặc Swagger):

```
mcp_hub-mcp_doc-get-by-endpoint:
  projectCode: "INVOICE"
  method: "POST"
  path: "/api/hoa-don/dieu-chinh"
```

---

## Duyệt Endpoint Theo Nhóm

Khi muốn xem toàn bộ endpoint trong 1 nhóm:

```
# Bước 1: Lấy danh sách groups
mcp_hub-mcp_doc-get-project-context:
  projectCode: "INVOICE"

# Bước 2: List endpoint theo groupCode
mcp_hub-mcp_doc-get-list-endpoints:
  projectCode: "INVOICE"
  groupCode: "HOA_DON"
```

---

## Kiểm Tra API Thay Đổi Gần Đây

Khi cần biết API nào đã được cập nhật (VD sau khi backend deploy):

```
mcp_hub-mcp_doc-get-changes:
  projectCode: "INVOICE"
  sinceDate: "2026-01-01T00:00:00Z"
```

---

## Tra Cứu Quy Tắc Nghiệp Vụ

Khi cần hiểu luồng nghiệp vụ trước khi code:

```
mcp_hub-mcp_doc-search-user-docs:
  query: "quy trình hủy hóa đơn đã ký"
  projectCode: "INVOICE"
  docType: 2   # 2 = BusinessRule
```

| docType | Loại tài liệu |
|---------|--------------|
| 1 | UserGuide — hướng dẫn sử dụng |
| 2 | BusinessRule — quy tắc nghiệp vụ |
| 3 | Changelog — lịch sử thay đổi |
| 4 | TestGuide — hướng dẫn kiểm thử |
| 5 | Deployment — hướng dẫn triển khai |

---

## Ví Dụ Thực Tế

### Ví dụ 1: Tìm API lấy danh sách hóa đơn

```
1. search-api-docs: query="danh sách hóa đơn", projectCode="INVOICE"
   → kết quả: endpointId="abc123", GET /api/hoa-don

2. get-endpoint: endpointId="abc123", projectCode="INVOICE"
   → response schema: { items: HoaDonItem[], total: number, page: number }
   → query params: page, pageSize, tuNgay, denNgay, trangThai, searchTerm

3. Áp dụng:
   - Interface: HoaDonListParams { page, pageSize, tuNgay?, denNgay?, trangThai?, searchTerm? }
   - Interface: HoaDonItem { id, soHoaDon, ngayHoaDon, tongTien, trangThai, ... }
   - ApiService: HoaDonApiService.getList(params)
```

### Ví dụ 2: Tìm API tạo hóa đơn khi đã biết path

```
1. get-by-endpoint: method="POST", path="/api/hoa-don", projectCode="INVOICE"
   → request body: { mauSo, ky, ngayHoaDon, khachHangId, danhSachHang, ... }
   → required: [mauSo, ky, ngayHoaDon, khachHangId]
   → requiresAuth: true, requiredRoles: ["INVOICE_CREATE"]

2. Áp dụng:
   - Validate form: mauSo, ky, ngayHoaDon, khachHangId là bắt buộc
   - ApiService: HoaDonApiService.create(request)
   - UI: hiển thị lỗi inline cho các trường required
```

---

## Lưu Ý Quan Trọng

- **Luôn dùng `urlLocal`** khi đọc project context — agent chạy local
- **`endpointId` ≠ `id` trong URL** — đây là ObjectId MongoDB 24 ký tự hex
- **Khi search trả về nhiều kết quả** — chọn kết quả có `score` cao nhất và `httpMethod` phù hợp
- **Không tự suy đoán schema** — luôn gọi `get-endpoint` để lấy spec chính xác
- **Sau khi lấy spec** → áp dụng đúng tên field trong TypeScript interface, không đổi tên tùy ý
