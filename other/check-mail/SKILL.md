---
name: check-mail
description: "Đọc Gmail, báo cáo thư chưa đọc. Dùng khi muốn check inbox nhanh mà không cần mở browser."
allowed-tools: Bash
user-invocable: true
---

Chạy mail reader và báo cáo kết quả:

```bash
python3 tools/check-mail.py
```

Nếu có thư urgent (invoice, payment, lỗi, khẩn, deadline), highlight lên đầu.
Nếu inbox sạch, báo ngắn: "Không có thư mới."
