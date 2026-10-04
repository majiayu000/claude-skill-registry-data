---
name: find-bug-by-logs
description: 'Tìm nguyên nhân gây lỗi bằng cách nghĩ đơn giản: xác định màn hình/URL/endpoint lỗi → auto login + navigate bằng Playwright headless → thao tác tái hiện lỗi → thu thập console logs + network logs → phân tích nguyên nhân → sửa lỗi → retest → xóa logs tạm khi fix xong. Dùng khi: gặp bug khó tìm nguyên nhân, overthinking không ra, cần dữ liệu thực tế từ runtime để phân tích.'
argument-hint: 'Portal + route màn hình bị lỗi. VD: ketoan "#/ketoan/danh-muc/khach-hang", invoice "#/business/invoice-management"'
---

# 🔍 Find Bug By Logs — Tìm Lỗi Bằng Console & Network Logs

> **Triết lý:** Thay vì nghĩ quá nhiều (overthinking) mà vẫn không tìm được nguyên nhân → **nghĩ đơn giản**: xác định đúng màn hình/URL/endpoint → thu thập logs thực tế từ browser → phân tích → sửa → test lại.

---

## 🎯 Quy Trình 4 Bước

```
┌──────────────────────────────────────────────────────────────┐
│  B1: XÁC ĐỊNH              B2: THU THẬP LOGS               │
│  Màn hình/URL/Endpoint     Auto login + Playwright          │
│  bị lỗi                    → Navigate → Thao tác            │
│                            → Capture console + network      │
├──────────────────────────────────────────────────────────────┤
│  B3: PHÂN TÍCH             B4: SỬA & RETEST                 │
│  Đọc logs → Tìm root cause → Sửa code → Chạy retest         │
│  Nghĩ đơn giản, không      → So sánh logs trước/sau         │
│  overthinking              → Xóa logs tạm khi sạch          │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Run

```bash
# === B1-B2: Thu thập logs lỗi ===
node .claude/skills/find-bug-by-logs/scripts/find-bug-by-logs.cjs ketoan "#/ketoan/danh-muc/khach-hang"

# Với steps tùy chỉnh để tái hiện lỗi
node .claude/skills/find-bug-by-logs/scripts/find-bug-by-logs.cjs ketoan "#/ketoan/danh-muc/khach-hang" --steps .claude/skills/find-bug-by-logs/steps-sample.json

# === B4: Retest sau khi sửa ===
node .claude/skills/find-bug-by-logs/scripts/find-bug-by-logs.cjs ketoan "#/ketoan/danh-muc/khach-hang" --retest
```

---

## B1 — Xác Định Phạm Vi Lỗi

> **Nguyên tắc: Nghĩ đơn giản — đừng overthinking!**

Trước khi debug, trả lời 3 câu hỏi:

| Câu hỏi | Cách xác định | Ví dụ |
|---------|---------------|-------|
| **Màn hình nào?** | Hash route hiện tại | `#/ketoan/danh-muc/khach-hang` |
| **URL/Endpoint nào?** | Tab Network trong browser, hoặc search trong API Service | `POST /api/ketoan/customers` |
| **Thao tác nào gây lỗi?** | Mô tả steps: click nút nào, fill field nào... | Click "Thêm" → fill form → bấm "Lưu" |

### Các nguồn thông tin để xác định:

```
✅ Mô tả từ user: "Trang khách hàng bị lỗi khi lưu"
✅ Console browser: mở F12 → Console → đọc dòng màu đỏ
✅ Network tab: mở F12 → Network → tìm request 4xx/5xx
✅ Vite overlay: màn hình đỏ với stack trace (dễ tìm nhất!)
✅ Log BE (nếu có): response lỗi từ server
```

---

## B2 — Thu Thập Logs Bằng Script

### Script tự động làm gì:

```
[1] API Login → lấy accessToken
[2] Mở Playwright headless → set token vào localStorage
[3] Navigate đến màn hình lỗi
[4] Tự động quét button → click "Thêm" → mở dialog
[5] Capture TẤT CẢ:
    • Console errors (màu đỏ)
    • Page errors (uncaught exceptions)
    • Network errors (request failed)
    • API errors (response 4xx/5xx)
    • Vite error overlay
[6] Xuất báo cáo JSON → .claude/skills/find-bug-by-logs/logs/
```

### Output: file JSON có cấu trúc:

```json
{
  "timestamp": "2026-07-19T...",
  "portal": "ketoan",
  "route": "#/ketoan/danh-muc/khach-hang",
  "consoleErrors": [
    { "text": "TypeError: Cannot read property 'id' of undefined", "location": {...} }
  ],
  "apiResponses": [
    { "status": 500, "url": "/api/ketoan/customers", "method": "POST" }
  ],
  "networkErrors": [
    { "url": "...KHDialog.tsx", "failure": "net::ERR_ABORTED" }
  ],
  "viteOverlay": "Error at KHDialog.tsx:45 ..." 
}
```

---

## B3 — Phân Tích Logs Để Tìm Nguyên Nhân

> **🧠 QUAN TRỌNG: Đừng overthinking! Đọc logs theo thứ tự ưu tiên:**

### Thứ tự đọc logs:

| Ưu tiên | Loại log | Cách đọc |
|:--:|----------|----------|
| 1 | **Vite overlay** | Đọc ngay — chỉ thẳng file + dòng lỗi. Nếu có → fix luôn, khỏi cần đọc gì khác |
| 2 | **Console error đầu tiên** | Thường là root cause. Các lỗi sau có thể là domino effect |
| 3 | **API error** | `4xx` = FE gửi sai → kiểm tra payload. `5xx` = BE lỗi → báo BE |
| 4 | **Network error** | File `.tsx/.ts` load fail → import sai path hoặc file không tồn tại |
| 5 | **Page error** | Uncaught exception → thường do null/undefined reference |

### Pattern lỗi thường gặp & cách fix:

| Pattern | Nguyên nhân | Cách fix |
|---------|-------------|----------|
| `Cannot read property 'X' of undefined` | Thiếu null check, data từ API chưa về | Optional chaining `?.` hoặc conditional render |
| `Failed to load module: ...` | Import sai path hoặc file đã bị xóa | Kiểm tra import, dùng `grep_search` tìm đúng path |
| `POST ... 400 Bad Request` | Payload FE gửi thiếu/sai field | So sánh payload với DTO/API spec |
| `POST ... 500 Internal Server Error` | BE throw exception | Gửi bug cho BE kèm payload + stack trace |
| `vite-error-overlay: ...` | Lỗi compile/biên dịch | Đọc stack trace, fix đúng file đúng dòng |
| `hook invalid ...` | React hook gọi sai thứ tự/điều kiện | Đưa hook lên top-level của component |

---

## B4 — Sửa & Retest

### Quy trình sửa → test → xóa:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ SỬA CODE │ →  │ RETEST   │ →  │ CÒN LỖI? │ →  │ SỬA TIẾP │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │                │
                     ▼                ▼ (hết lỗi)
              node ... --retest  ┌──────────┐
                                 │ XÓA LOGS │
                                 └──────────┘
```

### Retest command:

```bash
# Chạy lại test, so sánh với kết quả trước
node .claude/skills/find-bug-by-logs/scripts/find-bug-by-logs.cjs ketoan "#/ketoan/danh-muc/khach-hang" --retest

# Output:
# ╔══════════════════════════════════════════════╗
# ║  📊 SO SÁNH RETEST                         ║
# ║  Trước: 5 lỗi                              ║
# ║  Sau:   0 lỗi                              ║
# ║  ✅ ALL CLEAN — Đã xóa logs tạm            ║
# ╚══════════════════════════════════════════════╝
```

---

## 🔧 Steps File — Tái Hiện Lỗi Phức Tạp

Khi lỗi cần nhiều bước thao tác, tạo file JSON mô tả steps:

```json
[
  { "action": "click", "selector": "[data-qa='btn_them_moi']", "description": "Mở dialog thêm mới" },
  { "action": "fill", "selector": "[data-qa='dt_ma_kh']", "value": "KH001", "description": "Nhập mã KH" },
  { "action": "fill", "selector": "[data-qa='dt_ten_kh']", "value": "Test", "description": "Nhập tên KH" },
  { "action": "wait", "ms": 500, "description": "Chờ validate" },
  { "action": "click", "selector": "[data-qa='btn_luu']", "description": "Bấm Lưu" },
  { "action": "wait", "ms": 2000, "description": "Chờ API response" }
]
```

### Các action hỗ trợ:

| Action | Mô tả | Params |
|--------|-------|--------|
| `click` | Click vào element | `selector` |
| `fill` | Nhập text vào input | `selector`, `value` |
| `select` | Chọn option trong dropdown | `selector`, `value` |
| `wait` | Đợi N milliseconds | `ms` |
| `navigate` | Điều hướng URL | `url` |
| `press` | Nhấn phím | `key` (Enter, Escape, Tab...) |

---

## 🧠 Quy Tắc "Nghĩ Đơn Giản"

> **Nguyên tắc vàng:** 1 dữ liệu thực tế từ logs > 100 giả thuyết trong đầu.

Khi gặp bug mà đã nghĩ quá nhiều hướng mà vẫn không ra — **dừng suy đoán, chạy script thu thập logs**:

| ❌ Overthinking | ✅ Hành động cụ thể |
|----------------|---------------------|
| "Có thể do Redux state sai..." | Chạy script → đọc console error đầu tiên |
| "Chắc là do async/await..." | Xem log network → request nào fail? |
| "Có thể circular dependency..." | Đọc Vite overlay trong log → file nào + dòng nào? |
| "Hay là do config webpack..." | Xem file log JSON → sort theo timestamp |

---

## 📋 Cấu Hình

| Biến | Giá trị mặc định | Mô tả |
|------|-----------------|-------|
| `BASE_URL` | `http://100.64.0.15:3004` | URL frontend |
| `API_URL` | `http://100.64.0.15:5301` | URL backend API |
| `HEADLESS` | `true` | Chạy ẩn browser |
| `LOG_DIR` | `scripts/../logs/` | Thư mục lưu logs tạm |

### Tài khoản test:

| Portal | Username | Password |
|--------|----------|----------|
| ketoan, invoice, crm, kiemthu, taisan, sso, baseindex | `0985908756` | `Admin@123` |
| admin | `0966188166` | `admin@123` |
| partner | `0987839490` | `Admin@123` |

---

## ⚠️ Lưu Ý

1. **Script luôn chạy headless** — không cần xem browser, logs là đủ để phân tích
2. **Console errors được dedup** — tránh spam cùng 1 lỗi
3. **Lọc bỏ noise** — bỏ qua lỗi từ extension, webpack-internal, favicon...
4. **Logs tự xóa khi ALL CLEAN** — không để rác trong repo
5. **File logs nằm trong `.claude/skills/find-bug-by-logs/logs/`** — thư mục này nên được `.gitignore`
