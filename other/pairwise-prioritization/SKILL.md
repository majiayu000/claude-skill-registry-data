---
name: pairwise-prioritization
description: "Prioritize a task list by direct pairwise comparison instead of isolated scoring — compare every pair on importance, urgency, and impact, then produce a ranked execution order. Use when asked 'so từng cặp', 'sắp xếp ưu tiên', 'prioritize these tasks', 'việc nào làm trước', 'rank this backlog', 'đặt độ ưu tiên', or 'compare tasks head to head'. Do NOT use for: choosing between solution options — see option-tournament. Do NOT use for: sprint ceremony planning — see /sprint-planning."
tier: TIER 3 — CONSISTENCY
source: yana-ai (anh Tâm prompt pack, 2026-06-10)
---

# Pairwise Prioritization — So từng cặp để xếp ưu tiên

Thay vì chấm điểm rời rạc dễ cảm tính, so sánh trực tiếp từng cặp công việc
để tìm việc nào quan trọng/khẩn/ảnh hưởng lớn hơn, rồi xếp thành danh sách
ưu tiên xử lý.

> Prompt gốc: *"Đây là danh sách việc cần xử lý. Đừng chấm điểm từng việc một
> cách rời rạc. Hãy so sánh từng cặp để xem việc nào quan trọng hơn, khẩn hơn
> hoặc ảnh hưởng lớn hơn, rồi gom lại thành danh sách ưu tiên xử lý."*

---

## Vì sao so cặp thắng chấm điểm

```
Chấm điểm rời rạc:  "Task A: 7/10" — 7 so với cái gì? Mốc trôi theo cảm xúc.
So cặp:             "A vs B: A quan trọng hơn vì chặn release" — luôn có mốc.
```

So cặp ép phải nêu lý do cụ thể cho từng quyết định → audit được, cãi được.

## Quy trình

```
1. CHUẨN HÓA — viết lại mỗi task thành 1 dòng động từ + đối tượng + hệ quả.
   Task mơ hồ ("cải thiện UX") → tách hoặc làm rõ trước khi so.

2. SO CẶP — với n task, so đủ n(n-1)/2 cặp (n ≤ 8) hoặc dùng
   insertion-sort so cặp (n > 8, ~n·log n trận). Mỗi trận trả lời:
   "Nếu chỉ làm được 1 trong 2 hôm nay, làm cái nào?" + lý do 1 câu.

3. TÍNH HẠNG — đếm số trận thắng → xếp hạng. Hòa thực sự → so thêm
   tiêu chí phụ (cái nào unblock nhiều việc khác hơn).

4. GOM NHÓM — cắt danh sách thành 3 băng:
   🔴 Làm ngay (top) · 🟡 Tuần này · ⚪ Để sau / cân nhắc bỏ
```

## Tiêu chí mỗi trận (theo thứ tự)

```
1. Chặn người khác / chặn release không?   (blocker thắng)
2. Hậu quả nếu trì hoãn 1 tuần?            (mất tiền/uy tín thắng)
3. Ảnh hưởng lan rộng bao nhiêu?           (nhiều người/module thắng)
4. Cửa sổ thời gian có đóng không?         (deadline thật thắng deadline tự đặt)
```

## Format output

```markdown
## Priority Ranking — <ngày>

Trận đấu (10 cặp):
A vs B → A (chặn CI của cả team) · A vs C → A (...) · ...

| # | Task | Thắng | Băng |
|---|------|-------|------|
| 1 | Fix _test_router.js | 4/4 | 🔴 |
| 2 | Viết test crypto-store | 3/4 | 🔴 |
| ... |

Bắt đầu từ: #1, vì <1 câu>.
```

## Anti-Fake-Pass

```
❌ Ra bảng xếp hạng mà không log từng trận so cặp kèm lý do
❌ Lý do trận đấu là "quan trọng hơn" suông — phải nêu hệ quả cụ thể
❌ n ≤ 8 mà không so đủ n(n-1)/2 cặp — thiếu trận = hạng không tin được
❌ Mọi task đều vào băng 🔴 — không có ưu tiên nếu tất cả là ưu tiên
❌ Bỏ qua bước chuẩn hóa, so cặp trên task mơ hồ — garbage in, garbage out
```

## See also

- `option-tournament` — so cặp để chọn phương án, không phải xếp task
- `/next-task` — lấy việc tiếp theo từ backlog đã xếp
- `/sprint-planning` — lên kế hoạch sprint đầy đủ
