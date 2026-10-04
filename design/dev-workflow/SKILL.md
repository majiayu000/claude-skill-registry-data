---
name: dev-workflow
description: 'Agent điều phối toàn bộ quy trình phát triển Frontend 5 bước: B0-Clone giao diện tham khảo → B1-Đọc inbox tạo tài liệu → B2-Implement code + tự review → B3-Review chuyên sâu → B4-Commit & đóng task. Dùng khi cần thực thi một yêu cầu từ inbox từ đầu đến cuối.'
argument-hint: 'URL_CLONE=<url> DIR_CLONE=<dir> INBOX_ID=<id> DOC_FOLDER=<folder>. VD: URL_CLONE=https://actasp.misa.vn/... DIR_CLONE=exports/clone-results/ten-tinh-nang INBOX_ID=task-123 DOC_FOLDER=src/modules/business/docs/Nang-cap'
---

# Dev Workflow — Agent Điều Phối 5 Bước

> **Đầu vào bắt buộc (user cung cấp khi khởi chạy):**
>
> | Biến | Mô tả | Ví dụ |
> |------|-------|-------|
> | `URL_CLONE` | URL trang web cần clone để làm tài liệu tham khảo | `https://actasp.misa.vn/app/BA/.../List` |
> | `DIR_CLONE` | Thư mục lưu kết quả clone | `exports/clone-results/ten-tinh-nang` |
> | `INBOX_ID` | ID hoặc tiêu đề task trong inbox | `task-abc123` |
> | `DOC_FOLDER` | Thư mục lưu tài liệu thiết kế | `src/modules/business/docs/Nang-cap` |
>
> **Nếu thiếu bất kỳ biến nào → DỪNG, hỏi user trước khi bắt đầu.**

---

## ⚙️ Quy Tắc Chung

- **Tuần tự tuyệt đối:** Không nhảy bước, không bỏ qua bước kiểm tra.
- **Dừng có lý do:** Nếu bất kỳ bước nào thất bại → dừng, báo cáo bước nào, lý do cụ thể.
- **Sau mỗi bước thành công:** Ghi nhận kết quả ngắn gọn rồi tự động chuyển sang bước tiếp.
- **Không tự sáng tạo:** Luôn theo skill/prompt được chỉ định, không suy diễn thêm.

---

## 🛑 BƯỚC 0 — CLONE GIAO DIỆN THAM KHẢO

### Mục tiêu

Dùng Playwright chụp và trích xuất toàn bộ UI từ `URL_CLONE` để làm tài liệu thiết kế tham khảo.

### Thực thi

1. **Load skill** `clone-web-playwright`:
   - Đọc file `.claude/skills/clone-web-playwright/SKILL.md`
   - Áp dụng toàn bộ quy trình trong skill đó

2. **Thực hiện clone** theo skill `clone-web-playwright`:
   - URL đích: `URL_CLONE`
   - Thư mục output: `DIR_CLONE`
   - Dùng chế độ tối ưu token (mặc định trong skill)

3. **Xác nhận kết quả:**
   - File `DIR_CLONE/analysis/page-structure.md` tồn tại?
   - File `DIR_CLONE/raw/page-snapshot.json` tồn tại?
   - Ảnh `DIR_CLONE/screenshots/fullpage.png` tồn tại?

### Điều kiện chuyển bước

✅ **PASS** khi cả 3 file trên tồn tại và có nội dung.
❌ **FAIL** → dừng, báo lỗi cụ thể (lỗi Playwright, URL không hợp lệ, timeout auth...).

---

## 📝 BƯỚC 1 — ĐỌC INBOX & TẠO TÀI LIỆU YÊU CẦU

### Mục tiêu

Kết hợp nội dung inbox + kết quả clone B0 → tạo tài liệu thiết kế đầy đủ theo chuẩn dự án.

### Thực thi

**1.1 — Đọc inbox:**

```
mcp_hub-mcp_inbox-detail
  taskId: INBOX_ID
```

Nếu không tìm thấy task → thử `mcp_hub-mcp_inbox-check` (agentType: 1) để lấy danh sách rồi tìm lại.

**1.2 — Báo cáo đang xử lý:**

```
mcp_hub-mcp_report-task-progress
  taskId: INBOX_ID
  progressNote: "Đang phân tích yêu cầu và tạo tài liệu thiết kế"
```

**1.3 — Load prompt tạo tài liệu:**

Đọc file `.github/prompts/prompt-tao-tai-lieu-upgrade-fix.prompt.md` — áp dụng TOÀN BỘ quy trình trong prompt đó:
- B1: Thu thập thông tin từ inbox (Luồng B) + từ kết quả clone ở B0
- B2: Xác định vị trí tài liệu → lưu vào `DOC_FOLDER/nc-{ten-tinh-nang}-{yyyy-mm-dd}.md`
- B3 → B6: Xác định thư mục, menu, soạn tài liệu, review tài liệu

**1.4 — Xác nhận:**

File tài liệu đã được tạo tại `DOC_FOLDER/nc-*.md` và có đủ các section (0–7)?

### Điều kiện chuyển bước

✅ **PASS** khi file tài liệu tồn tại, có section 7 Checklist đầy đủ.
❌ **FAIL** → dừng, báo lý do (không đọc được inbox, mâu thuẫn kiến trúc, thiếu thông tin...).

---

## 💻 BƯỚC 2 — IMPLEMENT CODE & TỰ REVIEW SƠ BỘ

### Mục tiêu

Triển khai code từ tài liệu B1 theo đúng chuẩn dự án, rồi tự kiểm tra trước khi qua review chuyên sâu.

### Thực thi

**2.1 — Load prompt triển khai:**

Đọc file `.github/prompts/prompt-code-tu-tai-lieu.prompt.md` → áp dụng toàn bộ quy trình:
- B1: Đọc tài liệu từ B1 (phải có `✅ APPROVED` hoặc đã pass review)
- B2: Load các skill cần thiết theo tài liệu
- B3: Triển khai code theo thứ tự: `types → services → hooks → components → dialogs → pages → route → menu`
- B4: Đối chiếu tài liệu vs code
- B5: Kiểm tra runtime Playwright

**2.2 — Cập nhật tiến độ:**

```
mcp_hub-mcp_report-task-progress
  taskId: INBOX_ID
  progressNote: "Đã implement code, đang tự review..."
```

**2.3 — Tự Review (Self-Review):**

Kiểm tra nhanh theo checklist B4 của `prompt-code-tu-tai-lieu.prompt.md`:
- Mỗi endpoint → ApiService method đúng?
- Mỗi field response → type FE đúng?
- Mỗi màn hình trong tài liệu đã tạo?
- Route đúng path + lazy import?
- Compile errors: `get_errors` → 0 errors

Nếu phát hiện lỗi → sửa ngay, lặp lại đến khi không còn lỗi.

### Điều kiện chuyển bước

✅ **PASS** khi: 0 compile errors + tất cả file trong tài liệu đã tồn tại + runtime Playwright không có Critical errors.
❌ **FAIL** → dừng, báo file nào lỗi, lỗi cụ thể là gì.

---

## 🔍 BƯỚC 3 — REVIEW CODE CHUYÊN SÂU

### Mục tiêu

Review toàn bộ code vừa implement theo bộ tiêu chuẩn 11 bước của dự án.

### Thực thi

**3.1 — Load prompt review:**

Đọc file `.github/prompts/prompt-review-sau-code.md` → thực thi TOÀN BỘ 11 bước B1–B11:
- B1: Đọc tài liệu & xác định phạm vi
- B2: Kiểm tra cấu trúc & tên file
- B3: Code quality (no `any`, no `console.log`, comments tiếng Việt...)
- B4: API Service vs tài liệu BE
- B5: Tích hợp API → UI (phân tầng, ValidationErrorDialog...)
- B6: UI giao diện (master/dialog/sub-page conventions)
- B7: Validate & format chuẩn hóa
- B8: Routes & Menu
- B9: Runtime Playwright — click HẾT nút, mở HẾT dialog
- B10: Báo cáo kết quả chi tiết

**3.2 — Xử lý lỗi phát hiện:**

- **Critical:** Sửa ngay, chạy lại bước bị fail, lặp tối đa 3 lần
- **Non-critical (minor/suggestion):** Ghi nhận vào báo cáo, không block
- **Sau 3 lần vẫn còn Critical:** Dừng, báo user quyết định

**3.3 — Cập nhật tiến độ:**

```
mcp_hub-mcp_report-task-progress
  taskId: INBOX_ID
  progressNote: "Review hoàn thành: [Pass/Fail]. [Tóm tắt kết quả B2-B9]"
```

### Điều kiện chuyển bước

✅ **PASS** khi B10 báo cáo `✅ PASS — Tất cả critical đã fix`.
❌ **FAIL** → dừng, xuất báo cáo B10 đầy đủ để user quyết định.

---

## 🚀 BƯỚC 4 — COMMIT & HOÀN THÀNH TÁC VỤ

### Mục tiêu

Commit toàn bộ thay đổi (code + tài liệu) và đóng task trong hệ thống.

### Thực thi

**4.1 — Kiểm tra lần cuối:**

```bash
get_errors          # Phải = 0
git status --short  # Liệt kê file thay đổi
git branch --show-current  # Phải là branch development hoặc branch hiện tại
```

**4.2 — Load skill commit:**

Đọc `.claude/skills/commit-local-push-server/SKILL.md` → áp dụng quy trình commit.

**4.3 — Commit:**

```bash
git add <các file code và tài liệu đã thay đổi>
git commit -m "feat: <tên tính năng> from inbox INBOX_ID

<Tóm tắt ngắn: file mới, file sửa, tính năng chính>"
```

Quy tắc commit message:
- Prefix: `feat:` (tính năng mới), `fix:` (sửa lỗi), `refactor:` (tái cấu trúc)
- Body: liệt kê file chính đã thay đổi
- **Không commit** `auth.json`, `.env`, credentials

**4.4 — Push (nếu đủ 5 commits chưa push):**

```bash
git log origin/development..HEAD --oneline | wc -l
# Nếu ≥ 5 → git push origin development
```

**4.5 — Đóng task inbox:**

```
mcp_hub-mcp_inbox-completed
  taskId: INBOX_ID
  result: "✅ Hoàn thành. Commit: [hash]. Files: [danh sách ngắn]. Runtime: Pass."
```

### Điều kiện hoàn thành

✅ **DONE** khi: commit thành công + inbox task đã đóng (status Completed).
❌ **FAIL** → báo lỗi cụ thể (conflict git, MCP error...).

---

## 📊 BÁO CÁO KẾT THÚC

Sau khi hoàn thành, xuất báo cáo:

```
## ✅ Dev Workflow — Hoàn Thành

| Bước | Kết quả | Chi tiết |
|------|:-------:|---------|
| B0 — Clone | ✅ / ❌ | Đường dẫn: DIR_CLONE |
| B1 — Tài liệu | ✅ / ❌ | File: DOC_FOLDER/nc-*.md |
| B2 — Implement | ✅ / ❌ | Files mới: [...] / Files sửa: [...] |
| B3 — Review | ✅ / ❌ | Critical fixed: N / Runtime: Pass/Fail |
| B4 — Commit | ✅ / ❌ | SHA: [commit-hash] / Inbox: Completed |
```
