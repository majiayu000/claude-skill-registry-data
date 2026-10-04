---
name: inbox-check
description: 'Quy trình xử lý Inbox Tasks của FrontendWeb: kiểm tra, xử lý task được giao qua hệ thống Inbox. BẮT BUỘC: trước khi thực thi bất kỳ nội dung task nào, phải xác định skill áp dụng — nếu chưa có skill, DỪNG và hỏi user.'
---

# Inbox Check — FrontendWeb

> **QUY TẮC SỐ 1 — BẮT BUỘC:**
> Trước khi thực hiện bất kỳ task inbox nào:
> 1. Đọc nội dung task → xác định loại công việc
> 2. Tìm skill phù hợp trong `.claude/skills/`
> 3. **Nếu có skill** → load skill đó, làm theo skill
> 4. **Nếu chưa có skill** → DỪNG, báo user: _"Nhiệm vụ này chưa có skill. Vui lòng xác nhận hướng xử lý trước khi tiếp tục."_
> 5. **Không tự suy diễn** cách làm khi không có skill hướng dẫn

> **Lưu ý phân loại:**
> - Bug → dùng skill `fix-bug`
> - Question → dùng skill `question-check`
> - Inbox Task → skill này

---

## Mapping Loại Task → Skill

| Loại task | Nhận biết | Skill cần load |
|------------|-----------|----------------|
| Tạo UI master page | "tạo trang danh sách", "thêm tab" | `tao-ui-master-page` + `tao-ui-giao-dien` + `filter-phan-trang` |
| Tạo dialog/form | "tạo dialog", "tạo form CRUD" | `tao-ui-dialog` + `tao-ui-giao-dien` |
| Tạo sub page | "trang full-screen", "có breadcrumb" | `tao-ui-sub-page` + `tao-ui-giao-dien` |
| Tích hợp API | "tích hợp API", "kết nối endpoint" | `tich-hop-api-ui` + `tao-apiservice` |
| Validate form | "validate", "inline error" | `validate-input` |
| Upload file CDN | "upload CDN", "đính kèm file" | `cdn-upload` |
| Khởi tạo tính năng | "tạo feature mới", "khởi tạo module" | `tich-hop-api-ui` + `dat-ten` + `cau-truc-du-an` |
| Kiểm thử | "viết test case", "E2E", "Playwright" | `kiem-thu` |

---

## MCP Tools — Inbox Task

```
# Kiểm tra task mới
mcp_hub-mcp_inbox-check
  agentType: 1   ← FrontendWeb

# Xem chi tiết
mcp_hub-mcp_inbox-detail
  taskId: string

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

## Quy Trình Chuẩn

1. `inbox-check` → lấy danh sách task Pending
2. `inbox-detail` → đọc nội dung đầy đủ
3. Xác định skill → load skill → thực thi
4. `report-task-progress` → cập nhật đang làm
5. `inbox-completed` → ghi kết quả + đóng task
