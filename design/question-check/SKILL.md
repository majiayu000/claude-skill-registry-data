---
name: question-check
description: 'Quy trình xử lý Questions kỹ thuật được giao cho FrontendWeb. Dùng khi: kiểm tra câu hỏi mới, trả lời câu hỏi từ agent khác, reassign câu hỏi không thuộc phạm vi. BẮT BUỘC: chỉ đọc/tìm thông tin để trả lời — KHÔNG tự ý sửa code.'
---

# Question Check — FrontendWeb

> **QUY TẮC BẮT BUỘC:**
> - ✅ CHỈ đọc file / tìm thông tin để trả lời
> - ❌ KHÔNG tự ý sửa code theo yêu cầu trong câu hỏi
> - ❌ KHÔNG gọi tool nào ngoài read/search
> - Nếu câu trả lời dẫn đến cần thay đổi code → ghi vào answer, **chờ user yêu cầu trực tiếp**

---

## MCP Tools — Question

```
# Lấy danh sách câu hỏi được giao cho FrontendWeb
mcp_hub-mcp_question-get
  targetAgentType: 1        ← FrontendWeb
  status:          "Open"   ← câu hỏi chưa xử lý

# Xem chi tiết câu hỏi
mcp_hub-mcp_question-detail
  id:          string
  projectCode: string

# Trả lời câu hỏi
mcp_hub-mcp_question-reply
  id:          string
  projectCode: string
  answer:      string   ← nội dung trả lời đầy đủ

# Đóng câu hỏi sau khi trả lời xong
mcp_hub-mcp_question-close
  id:          string
  projectCode: string
  closeReason: string

# Chuyển câu hỏi sang agent khác (nếu không thuộc phạm vi FW)
mcp_hub-mcp_question-reassign
  id:                 string
  projectCode:        string
  newTargetAgentType: number   ← 0=Backend | 2=FrontendApp | 3=QA | 4=DocWriter
  reason:             string
```

---

## Quy Trình Chuẩn

1. `question-get` → lấy danh sách câu hỏi Open dành cho FrontendWeb
2. `question-detail` → đọc đầy đủ nội dung + context
3. Xác định: câu hỏi có thuộc phạm vi FrontendWeb không?
   - **Thuộc phạm vi** → tìm kiếm thông tin trong codebase → `question-reply`
   - **Không thuộc phạm vi** → `question-reassign` sang agent phù hợp
4. `question-close` → đóng câu hỏi khi đã trả lời xong

---

## Phạm Vi FrontendWeb

**Thuộc phạm vi — CÓ THỂ trả lời:**
- Cấu trúc component, hook, service trong `/src`
- Route, navigation, HashRouter
- UI behavior, form validation, API call từ React
- State management, TypeScript types

**KHÔNG thuộc phạm vi → reassign:**
- Câu hỏi về server logic, database → reassign Backend (0)
- Câu hỏi về Flutter/Mobile app → reassign FrontendApp (2)
- Câu hỏi về test plan, test case → reassign QA (3)

---

## AgentType Enum

| Giá trị | Tên |
|---------|-----|
| `0` | Backend |
| `1` | FrontendWeb ← (chúng ta) |
| `2` | FrontendApp |
| `3` | QA |
| `4` | DocWriter |
