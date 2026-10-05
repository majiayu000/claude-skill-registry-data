---
name: mem0
description: Cung cấp khả năng ghi nhớ lâu dài (Long-term context) và truy vấn Graph Memory thông qua Mem0 MCP Server.
---

# 🧠 Mem0 - Graph Memory Integration Guide

Skill này cho phép Agent kết nối với **Mem0**, một tầng bộ nhớ thông minh (persistent memory layer) giúp ghi nhớ sở thích người dùng, ngữ cảnh dự án và các mối quan hệ phức tạp giữa các thực thể (Graph Memory).

## 🚀 Hướng dẫn thiết lập

### Cách 1: Mem0 Cloud (Khuyên dùng)
1. Truy cập [mem0.ai](https://mem0.ai) và tạo API Key.
2. Thêm MCP Server vào IDE của bạn (Cursor, Claude Desktop, Antigravity):
   - **Command:** `npx -y @mem0/mcp-server`
   - **Env Variables:** `MEMO_API_KEY=your_api_key_here`

### Cách 2: Self-hosted (Local)
1. Cài đặt Mem0 local qua pip: `pip install mem0ai`.
2. Sử dụng MCP Bridge để kết nối script Python của Mem0 thành công cụ cho Agent.

## 🛠️ Các công cụ khả dụng

Khi MCP Server được kích hoạt, Agent có thể gọi các công cụ:
- `add_memory`: Lưu trữ một thông tin mới vào bộ nhớ.
- `search_memories`: Tìm kiếm các thông tin liên quan theo ngữ nghĩa.
- `search_graph`: Truy vấn các mối quan hệ (ví dụ: "Ai đang làm việc ở dự án X?").
- `delete_memory`: Xóa các thông tin đã lỗi thời.

## 💡 Best Practices cho Agent

### 1. Tự động lưu trữ (Autonomous Storage)
Sau mỗi lần giải quyết xong một vấn đề phức tạp, hãy sử dụng `add_memory` để lưu lại giải pháp:
> "User ưu tiên sử dụng Clean Architecture cho các dự án C# và luôn yêu cầu tích hợp CancellationToken."

### 2. Thu hồi thông tin (Context Recall)
Trước khi bắt đầu một task lớn, hãy dùng `search_memories` để kiểm tra xem đã có kiến thức tương tự trong quá khứ chưa.

### 3. Suy luận Graph (Relational Reasoning)
Sử dụng dữ liệu từ `search_graph` để hiểu cấu trúc hệ thống nếu không có tài liệu bằng văn bản.

## ⚠️ Lưu ý
- Không lưu trữ các thông tin nhạy cảm (Password, Secret Key) vào Mem0.
- Định kỳ sử dụng `search_memories` để cập nhật/sửa đổi các kiến thức đã thay đổi.

---
*Powered by: Unified AI Agent Toolkit v2.3*
