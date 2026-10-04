---
name: bug-check
description: "Quy trình xử lý bug của FrontendWeb: kiểm tra, retest, reply và xử lý bug được giao (BackendReplied/Fixed/NeedMoreInfo). Việc sửa code BẮT BUỘC tuân thủ đúng skill liên quan — không tự suy diễn, không sáng tạo pattern mới."
---

# Bug Check — FrontendWeb

## Phạm Vi Trách Nhiệm

**FrontendWeb XỬ LÝ:** Bug liên quan đến React Web (`/src`), HashRouter (`#/`), UI/form/validation, API call từ web.

**KHÔNG thuộc phạm vi:**
- Tiêu đề có `[App kinh doanh]`, `[App đối tác]`, `[Mobile ...]` → FrontendApp
- Logic server, database → Backend

---

## MCP Tools

```
# Lấy bug cần xử lý (1 bug/lần, kèm replies)
mcp_hub-mcp_bug-check
  agentType: "FrontendWeb"

# Xem chi tiết bug theo ID
mcp_hub-mcp_bug-detail
  bugId: string

# Đóng bug Fixed → Closed (sau khi FE verify OK)
mcp_hub-mcp_bug-close
  bugId:          string
  retestNote:     string   ← mô tả FE đã verify gì
  attachmentUrls?: string[] ← ảnh minh chứng (tùy chọn)

# Reopen khi vẫn lỗi / bổ sung thông tin (NeedMoreInfo)
mcp_hub-mcp_bug-reopen
  bugId:          string
  content:        string   ← lý do reopen / thông tin bổ sung
  attachmentUrls?: string[]
```

> **Lưu ý:** `bug-check` tự động set bug → InProgress khi lấy.
> Xử lý xong 1 bug (reopen hoặc xác nhận đã fix) → gọi lại `bug-check` để lấy bug tiếp theo.

---

## Quy Trình Chuẩn

### Bước 1 — Lấy bug
```
mcp_hub-mcp_bug-check(agentType: "FrontendWeb")
```
→ Đọc kỹ: tiêu đề, mô tả, replies của Backend, trạng thái hiện tại.

### Bước 2 — Phân loại

| Trạng thái | Backend phân loại | Hành động |
|------------|-------------------|-----------|
| `BackendReplied` | `ClientError` — lỗi do FE | **Sửa code FE** → retest → xác nhận |
| `BackendReplied` | `NeedMoreInfo` | Bổ sung thông tin → `bug-reopen` |
| `Fixed` | BE đã sửa xong | Verify tích hợp FE+BE → xác nhận |
| Bất kỳ | Bug không thuộc FE | `bug-reopen` + giải thích rõ → yêu cầu reassign |

### Bước 3 — Sửa code (nếu `ClientError`)

> **BẮT BUỘC trước khi sửa:**
> 1. Xác định loại công việc (UI, API call, validate, ...)
> 2. Load **đúng skill** tương ứng từ bảng dưới
> 3. Làm theo skill — **không tự suy diễn, không sáng tạo pattern mới**
> 4. Nếu không có skill phù hợp → DỪNG, báo user

| Loại sửa | Skill cần load |
|----------|----------------|
| Sửa UI, button, table, layout | `tao-ui-giao-dien` |
| Sửa dialog/form | `tao-ui-dialog` + `tao-ui-giao-dien` |
| Sửa master page | `tao-ui-master-page` + `tao-ui-giao-dien` |
| Sửa validate form | `validate-input` |
| Sửa API call / service | `tich-hop-api-ui` + `tao-apiservice` |
| Sửa filter/phân trang | `filter-phan-trang` |
| Sửa file (replace, refactor) | `sua-file-an-toan` |
| Sửa nhiều file / phức tạp | `checklist-sau-code` sau khi xong |

### Bước 4 — Xác nhận kết quả

> **Phân biệt nguồn tạo bug** (`Source` trong bug detail):
> - `Source: 2` = Bug do **Agent tạo** → `bug-close` → **Closed luôn**
> - `Source: 1` = Bug do **người dùng tạo thủ công** → `bug-close` → **Closed** (FE xác nhận xong là đủ)

**Đã fix OK (cả Source=1 và Source=2):**
```
mcp_hub-mcp_bug-close
  bugId:      <bugId>
  retestNote: "FE đã verify OK — [mô tả ngắn đã sửa gì / đã test gì]"
```
→ Bug chuyển **Fixed → Closed**.

**Vẫn lỗi / không thuộc phạm vi:**
```
mcp_hub-mcp_bug-reopen
  bugId:   string
  content: "Lý do: ... | Đề nghị: reassign sang [Backend/FrontendApp]"
```

---

## Quy Tắc Cứng

- ❌ Không sửa code khi chưa xác định được skill áp dụng
- ❌ Không tự sáng tạo pattern ngoài skill
- ❌ Không sửa code Flutter, backend, infrastructure
- ✅ 1 bug xử lý xong hoàn toàn → mới gọi `bug-check` tiếp theo
- ✅ Luôn retest thực tế trên UI sau khi sửa trước khi xác nhận Fixed
