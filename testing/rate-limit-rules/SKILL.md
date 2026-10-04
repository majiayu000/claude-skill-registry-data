---
name: rate-limit-rules
description: 'Quy tắc chống rate limit / throttling khi thao tác nhiều tool call liên tiếp trong dự án JDX-Gamers Website — giới hạn số lần đọc file/tìm kiếm/MCP/Playwright mỗi lượt, batching, checkpoint. Dùng khi: thực hiện tác vụ dài nhiều bước, gọi nhiều tool liên tục (đọc file, MCP, browser automation).'
---

# Quy Tắc Chống Rate Limit — JDX-Gamers Agent

> Nguồn gốc: quy tắc throttling cho AI coding agent (GitHub Copilot Chat) — vẫn áp dụng như nguyên tắc tự giới hạn tốc độ thao tác chung khi làm việc với Claude Code, để tránh spam quá nhiều tool call trong 1 lượt.

## Giới Hạn Tool Calls Per Turn

| Loại công việc | Giới hạn / lượt | Hành động sau khi đạt giới hạn |
|---|---|---|
| Đọc file / tìm kiếm code | Tối đa **10 calls** | Tổng hợp → báo cáo → dừng |
| MCP (tạo TC, submit result, tạo bug) | Tối đa **5 calls** | Báo cáo tiến độ → chờ user |
| Playwright browser automation | Tối đa **8 actions** | `waitForTimeout(500)` → snapshot → báo cáo |
| Kết hợp nhiều loại (code + MCP + browser) | Tối đa **6 calls** | Checkpoint bắt buộc |

## Batching MCP Bulk Operations

```
❌ SAI — 7 MCP calls song song 1 lúc
✅ ĐÚNG — chia batch:
   Batch 1: 3 calls → tóm tắt kết quả
   Batch 2: 3 calls → tóm tắt kết quả
   Batch 3: còn lại → tổng kết
```

- Parallel tối đa **3** MCP calls / lượt
- Sau mỗi batch: **tóm tắt kết quả** trước khi tiếp tục

## Checkpoint — Công Việc Dài

1. Sau mỗi phase lớn → **DỪNG**, báo cáo tóm tắt, chờ user xác nhận
2. Sau mỗi **5 STEP test** → checkpoint: đã làm gì, còn gì
3. Không tự chạy liên tục giữa các phase

## Playwright Throttle

```typescript
await page.waitForTimeout(300) // Sau mỗi nhóm thao tác
await page.waitForLoadState('domcontentloaded') // Sau navigate
await page.waitForTimeout(200) // Trước snapshot
```

## Khi Gặp Rate Limit Error

1. DỪNG ngay — không retry tự động
2. Báo cáo trạng thái (đã làm gì, đang ở bước nào)
3. Thông báo: _"Đã đạt rate limit. Vui lòng đợi ~60 giây rồi thử lại để tiếp tục từ [điểm X]."_
4. Sau khi retry → tiếp tục đúng từ bước bị gián đoạn
