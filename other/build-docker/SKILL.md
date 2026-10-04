---
name: build-docker
description: 'Hướng dẫn chạy script build Docker cho Sasuco Invoice Web (React). Use when: build docker, build image web, build invoiceweb, build production image, docker build web, build và push image lên Docker Hub. CHỈ HƯỚNG DẪN cách chạy script Docker\build-docker-all.ps1 — KHÔNG được phép tự chạy; muốn hiểu quy tắc thì đọc Docker\Quy-tac-build-docker\quy-tac-build-docker.md.'
argument-hint: 'mặc định Development, nói "production" để build production — kèm portal nếu rõ (web|sso|admin|partner|accounting|kiemthu|taisan|crm|baseindex)'
---

# Build Docker — Hướng dẫn chạy script (KHÔNG chạy trực tiếp)

> ⚠️ **QUY TẮC QUAN TRỌNG:**
> - Skill này **CHỈ HƯỚNG DẪN** cách chạy script `Docker\build-docker-all.ps1`.
> - **KHÔNG được phép tự chạy** build (không gọi `docker build`, không chạy script build trực tiếp).
> - Muốn hiểu quy tắc/cách làm chi tiết → **đọc file quy tắc**:
>   `Docker\Quy-tac-build-docker\quy-tac-build-docker.md`
> - Khi user yêu cầu build → **hướng dẫn user chạy lệnh bên dưới** (hoặc đưa lệnh cho user xác nhận trước khi chạy).

---

## 🎯 2 PHƯƠNG PHÁP CHẠY

Script hỗ trợ **2 cách dùng** — user tùy chọn:

| Phương pháp | Khi nào dùng | Cách chạy |
|-------------|--------------|-----------|
| **① Chạy đến đâu, chọn đến đó** (interactive) | User muốn tự quyết định từng bước — script hiển thị menu hỏi: môi trường → portal → loại phát hành → version | Chỉ cần gõ `.\Docker\build-docker-all.ps1` (**không cần nhập tham số**) |
| **② Truyền sẵn đủ tham số** (nhanh, agent/CI) | Đã biết rõ môi trường + portal (+ version) — muốn chạy thẳng, bỏ qua menu hỏi | Truyền đủ `-Env -Portal [-ReleaseType -Version]` (tùy chọn thêm `-Force`) |

---

## ① Phương pháp 1 — Chạy đến đâu, chọn đến đó (interactive)

> ✅ **Đơn giản nhất:** chỉ cần chạy 1 lệnh duy nhất, script tự hỏi từng bước:

```powershell
.\Docker\build-docker-all.ps1
```

**Script hiển thị menu và user chọn từng bước:**

| Bước | Màn hình script hỏi | User chọn |
|------|--------------------|-----------|
| 1. Môi trường | `1 - Development` / `2 - Production` / `3 - Stop` | gõ `1` hoặc `2` |
| 2. Portal tác động | liệt kê `web\|sso\|admin\|partner\|...` — yêu cầu **gõ + verify** | gõ alias (vd `partner`) → xác nhận `Y/n` |
| 3. Kiểu phát hành *(chỉ Production)* | `1 - Release` / `2 - Hotfix` / `3 - Stop` | gõ `1` hoặc `2` |
| 4. Version *(chỉ Production)* | hiển thị **5 version gần nhất** + gợi ý | gõ version (hoặc Enter lấy gợi ý) |
| 5. Xác nhận portal nâng cấp *(chỉ Production)* | `Đúng portal muốn nâng cấp? [Y/n]` | gõ `Y` |
| 6. Từng bước build | TÓM TẮT kết quả từng bước | **Enter** tiếp tục / gõ **`stop`** dừng |

> 💡 Mọi bước đều có thể gõ `stop`/`3` để thoát an toàn (tự reset trạng thái).
> 💡 User không cần nhớ tham số — chỉ cần **nhìn menu và chọn**.

---

## ② Phương pháp 2 — Truyền sẵn đủ tham số (nhanh)

> Khi đã rõ môi trường + portal → truyền thẳng để bỏ qua menu hỏi:

| Tình huống | Lệnh (từ workspace root) |
|-----------|---------------------------|
| Build Development + portal cụ thể | `.\Docker\build-docker-all.ps1 -Env Development -Portal partner` |
| Build Production (phát hành mới) | `.\Docker\build-docker-all.ps1 -Env Production -ReleaseType new -Portal partner` |
| Build Production (hotfix) + version | `.\Docker\build-docker-all.ps1 -Env Production -ReleaseType fix -Portal web -Version 1.6.0.1` |
| Chạy liên tục không hỏi từng bước (agent/CI) | `.\Docker\build-docker-all.ps1 -Env Development -Portal partner -Force` |

> **Tham số hợp lệ:** `-Env Development|Production` · `-Portal web|sso|admin|partner|accounting|kiemthu|taisan|crm|baseindex` · `-ReleaseType new|fix` · `-Version x.x.x` (hoặc `x.x.x.z`) · `-Force`

---

## 🧭 Luồng script chạy (10 bước)

| # | Bước | Khi nào chạy |
|---|------|-------------|
| 1 | PREPARE + CHECK (chuẩn bị nhánh + kiểm tra an toàn) | luôn |
| 2 | SECURITY (quét lỗ hổng) | luôn |
| 3 | PERFORMANCE (quét hiệu năng) | luôn |
| 4 | BUILD (docker build) | luôn |
| 5 | EXPORT (.tar + SHA256) | Production only |
| 6 | PUSH (docker push) | luôn |
| 7 | PORTAINER (redeploy dev) | Development only |
| 8 | GIT RELEASE (merge→main + tag) | Production only |
| 9 | RECORD VERSION (KiemThuApi) | luôn |
| 10 | REPORT (báo cáo tổng kết) | Production only |

**Trong lúc chạy:**
- Sau mỗi bước → script in **TÓM TẮT** (🎯 mục tiêu → ✅/❌ kết quả → 📌 PASS/FAIL)
- Nhấn **Enter** để chạy bước tiếp / gõ **`stop`** để DỪNG (tự reset trạng thái)
- Môi trường **Development**: chỉ switch nhánh `development`, build thẳng — **không đụng main/production**
- Môi trường **Production**: phân tách cẩn thận — nhánh `production` tạm → build → git release + tag
- Log chi tiết từng phiên: `Docker\Logs\build-docker-all-<timestamp>.log`

---

## ⚠️ Khi user yêu cầu build

1. **Xác định phạm vi**: môi trường (Development/Production) + portal nào thay đổi (nếu rõ)
2. **Chọn phương pháp cho user**:
   - User **muốn tự chọn từng bước** → hướng dẫn chạy `.\Docker\build-docker-all.ps1` (phương pháp ①)
   - User **đã rõ tham số** → soạn lệnh đầy đủ (phương pháp ②)
3. **Đưa lệnh cho user chạy** — KHÔNG tự chạy build
4. Nếu user muốn hiểu quy tắc → trỏ đọc `Docker\Quy-tac-build-docker\quy-tac-build-docker.md`

> 💡 Nếu cần chạy tự động (agent/CI) → dùng thêm `-Force` và truyền đủ tham số
> `-Env -Portal [-ReleaseType -Version]` để bỏ qua menu hỏi.

---

## 📚 Tham chiếu

| Nội dung | Đường dẫn |
|----------|-----------|
| **Quy tắc build đầy đủ** (version, git release, an toàn, tối ưu...) | `Docker\Quy-tac-build-docker\quy-tac-build-docker.md` |
| Script chính (wrapper) | `Docker\build-docker-all.ps1` |
| Scripts phụ | `Docker\Scripts\*.ps1` / `*.cjs` |
| Dockerfile | `Docker\Dockerfile` |
| Log build | `Docker\Logs\build-docker-all-*.log` |
| Version files | `Docker\versions\web.txt` / `web.log` |
