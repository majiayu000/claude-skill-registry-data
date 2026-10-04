---
name: optimize-skill-sasuco
description: 'Thống kê tần suất sử dụng skill trong dự án SASUCO InvoiceEasy dựa trên git log. Đưa ra ma trận ưu tiên tối ưu token (Usage × Size = Priority Score). Dùng khi: cần biết skill nào tốn token nhất, skill nào ít được dùng, ra quyết định tối ưu bộ skill.'
---

# Optimize Skill SASUCO — Phân Tích & Tối Ưu Token

> **Mục đích:** Thống kê tần suất sử dụng skill trong dự án, đưa ra ma trận
> ưu tiên (Usage × Size) để quyết định skill nào cần tối ưu / gộp / xóa.

---

## Bước 1 — Chạy Script Phân Tích

```bash
node .claude/skills/optimize-skill-sasuco/analyze-skill-usage.cjs
```

Script sẽ tự động:
- Đọc toàn bộ git log từ đầu năm 2026
- Mapping từ khóa trong commit message → skill tương ứng
- Đếm tần suất mỗi skill
- Đo kích thước file SKILL.md từng skill
- Tính Priority Score = Usage × Size (KB)
- Xuất ra ma trận ưu tiên

---

## Bước 2 — Đọc Kết Quả

Kết quả gồm 4 bảng:

### 2.1 TOP 20 Skills theo commit keyword

Tần suất skill xuất hiện trong commit messages. Skill có tần suất cao = được
gọi nhiều = tốn nhiều token nhất.

### 2.2 TOP 15 Modules theo commit scope

Xem module/portal nào được sửa nhiều nhất (`admin`, `business`, `crm`, ...).

### 2.3 TOP 15 Directories theo số lần sửa file

Thư mục nào có nhiều file thay đổi nhất → biết khu vực code sôi động nhất.

### 2.4 Ma Trận Ưu Tiên (Usage × Size)

| Mức | Score | Ý nghĩa |
|-----|-------|---------|
| 🔴 RẤT CAO | > 400 | Cần tối ưu ngay — dùng nhiều + file lớn |
| 🟡 CAO | 150-400 | Ưu tiên thứ 2 |
| 🟢 TB | 50-150 | Có thể tối ưu nếu còn thời gian |
| ⚪ THẤP | < 50 | Không cần ưu tiên |
| ⚫ CHƯA DÙNG | 0 | Không có commit liên quan → xem xét xóa/gộp |

---

## Bước 3 — Quyết Định Hành Động

Dựa vào ma trận, quyết định:

| Hành động | Khi nào áp dụng |
|-----------|----------------|
| **Rút gọn SKILL.md** | Score 🔴 hoặc 🟡, file > 8KB |
| **Gộp nhiều skill nhỏ** | Nhiều skill ⚪ liên quan đến cùng 1 chủ đề |
| **Xóa skill** | Score ⚫ (chưa dùng) và không phải foundation |
| **Giữ nguyên** | Score ⚪ nhưng là foundation (`quy-tac-code`, `cau-truc-du-an`) |

---

## Bước 4 — Theo Dõi Định Kỳ

Chạy script mỗi tháng để theo dõi xu hướng:

```bash
# Lưu kết quả có timestamp
node .claude/skills/optimize-skill-sasuco/analyze-skill-usage.cjs > stats/skill-usage-$(Get-Date -Format "yyyy-MM-dd").txt
```

---

## Cấu Trúc Script

```
.claude/skills/optimize-skill-sasuco/
├── SKILL.md                    ← File này
└── analyze-skill-usage.cjs     ← Script phân tích (Node.js)
```

Script dùng `git log` + `fs` (Node.js built-in), không cần cài thêm dependency.
