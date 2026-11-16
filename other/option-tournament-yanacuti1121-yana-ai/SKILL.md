---
name: option-tournament
description: "Generate many candidate options across different styles (concise, simple, creative, professional), then run pairwise elimination rounds to select the top 3 with reasons. Use when asked for 'phương án', 'cho mấy phương án', 'generate options and pick best', 'so sánh phương án', 'naming candidates', 'top 3 approaches', 'loại dần phương án yếu', or 'which wording is best'. Do NOT use for: prioritizing a task list — see pairwise-prioritization. Do NOT use for: exploring solution trees in reasoning — see tree-of-thoughts."
tier: TIER 3 — CONSISTENCY
source: yana-ai (anh Tâm prompt pack, 2026-06-10)
---

# Option Tournament — Cho phương án thi đấu

Tạo nhiều hướng tiếp cận cho một vấn đề, cho chúng thi đấu loại trực tiếp
từng cặp, giữ lại top 3 kèm lý do.

> Prompt gốc: *"Tạo nhiều phương án cho việc bên dưới, chia theo vài hướng khác
> nhau như ngắn gọn, dễ hiểu, sáng tạo, chuyên nghiệp. Sau đó cho từng phương án
> so với nhau theo từng cặp, loại dần phương án yếu, rồi chọn ra 3 phương án
> tốt nhất kèm lý do."*

---

## Khi nào dùng

- Đặt tên (sản phẩm, hàm, skill, thương hiệu)
- Viết copy (tagline, mô tả, tiêu đề, thông báo lỗi)
- Chọn approach kỹ thuật khi có nhiều cách hợp lệ
- Thiết kế API shape / UX flow có nhiều biến thể

## Quy trình 3 vòng

```
VÒNG 1 — SINH (8-12 phương án)
  Chia theo 4 hướng, mỗi hướng 2-3 phương án:
  • Ngắn gọn     — ít từ nhất có thể
  • Dễ hiểu      — người ngoài ngành đọc hiểu ngay
  • Sáng tạo     — bất ngờ, dễ nhớ
  • Chuyên nghiệp — chuẩn industry, an toàn

VÒNG 2 — ĐẤU LOẠI TỪNG CẶP
  Bốc cặp ngẫu nhiên trong cùng bracket. Mỗi trận:
  so 2 phương án trên đúng các tiêu chí của đề bài,
  ghi 1 câu lý do thắng/thua. Thua → loại. Lặp đến khi còn 3-4.

VÒNG 3 — CHUNG KẾT
  Còn 3-4 phương án → so vòng tròn (round-robin).
  Xếp hạng top 3, mỗi cái kèm: điểm mạnh, điểm yếu, khi nào nên chọn.
```

## Tiêu chí so cặp (chọn 3-4 cái khớp đề bài)

```
□ Đúng yêu cầu gốc (fit)        □ Rõ ràng, không mơ hồ (clarity)
□ Dễ nhớ / dễ gọi (memorability) □ Chi phí thực hiện (cost)
□ Rủi ro hiểu nhầm (risk)        □ Bền theo thời gian (longevity)
```

Tiêu chí phải được chốt TRƯỚC vòng 2 — không đổi giữa chừng.

## Format output

```markdown
## Tournament: <việc cần chọn>

Vòng 1: 10 phương án (ngắn gọn ×3, dễ hiểu ×3, sáng tạo ×2, chuyên nghiệp ×2)
Vòng 2: A vs F → A thắng (lý do 1 câu) ... [log đủ các trận]

### 🏆 Top 3
1. **<phương án>** — mạnh: ... · yếu: ... · chọn khi: ...
2. ...
3. ...

Khuyến nghị: #1, vì <1-2 câu>.
```

## Anti-Fake-Pass

```
❌ Sinh < 8 phương án rồi gọi là "nhiều" — tối thiểu 8, đủ 4 hướng
❌ Nhảy thẳng đến top 3 không log các trận đấu cặp — phải thấy quá trình
❌ Đổi tiêu chí giữa các trận để "ưu ái" một phương án
❌ Top 3 cùng 1 hướng (cả 3 đều "ngắn gọn") mà không giải thích vì sao
   các hướng khác bị loại sạch
❌ Không đưa khuyến nghị cuối — liệt kê 3 cái rồi đẩy việc chọn lại cho người hỏi
```

## See also

- `pairwise-prioritization` — so cặp để xếp ưu tiên task list
- `tree-of-thoughts` — duyệt cây giải pháp trong reasoning nhiều bước
- `multi-agent-debate` — nhiều agent tranh luận thay vì 1 agent tự so
