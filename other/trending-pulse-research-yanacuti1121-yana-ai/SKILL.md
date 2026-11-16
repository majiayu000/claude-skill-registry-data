---
name: trending-pulse-research
description: "Research what the community actually thinks about a topic in the LAST 30 DAYS — search Reddit, X, YouTube, Hacker News and GitHub in parallel, weight results by real engagement (upvotes, likes, stars/day), detect cross-platform convergence, and synthesize one grounded brief with citations. Use when asked 'cộng đồng đang nói gì về X', 'what's trending in X', 'last 30 days research', 'tin mới nhất về X trên Reddit/HN', 'is X actually popular or hype', or 'research recent sentiment'. Do NOT use for: deep technical/academic research with no recency requirement — see deep-research or arxiv-research. Do NOT use for: one-off fact lookups — plain web search is enough."
tier: TIER 3 — CONSISTENCY
source: inspired by mvanhorn/last30days-skill (pattern study, 2026-06-11) — independent implementation
---

# Trending Pulse Research — Cộng đồng nói gì trong 30 ngày qua

Khác research thường ở 3 điểm: **giới hạn 30 ngày**, **trọng số engagement
thật** (không phải thứ hạng SEO), và **convergence detection** — một chủ đề
chỉ đáng tin khi nhiều nền tảng độc lập cùng nói về nó.

## Quy trình 4 pha

```
PHA 1 — FAN-OUT (song song, mỗi nền tảng 1 query):
  Reddit  : site:reddit.com <topic>  (sort: top, t=month)
  HN      : hn.algolia.com search <topic> (numericFilters: created_at > now-30d)
  X       : <topic> filter theo ngày nếu công cụ cho phép
  YouTube : <topic> uploaded this month
  GitHub  : repo/issue search, sort stars/created

PHA 2 — SCORE (mỗi item):
  score = engagement_norm × recency_decay × source_diversity
  engagement_norm : upvotes/likes/stars CHIA cho median nền tảng đó
                    (1000 upvote Reddit ≠ 1000 like X)
  recency_decay   : ×1.0 (≤7 ngày) · ×0.7 (≤14) · ×0.4 (≤30)
  Cap: tối đa 3 items / 1 tác giả — chống một giọng nói thống trị brief

PHA 3 — CONVERGE:
  Nhóm các claims xuất hiện ≥2 nền tảng độc lập → "tín hiệu mạnh"
  Claims chỉ 1 nền tảng → "tín hiệu đơn lẻ" (ghi rõ, không trộn lẫn)

PHA 4 — BRIEF (output cố định):
  ## Pulse: <topic> (30 ngày, tính đến <date>)
  **Tín hiệu mạnh** (đa nền tảng): [3-5 bullets + citation từng cái]
  **Tín hiệu đơn lẻ** (chưa kiểm chứng chéo): [bullets]
  **Sentiment**: tích cực/tiêu cực/chia rẽ — kèm tỉ lệ thô
  **Đáng làm gì**: 1-3 hành động cụ thể rút ra
  **Nguồn**: list URL đầy đủ
```

## Luật chất lượng

```
□ MỌI claim trong brief phải có ≥1 URL nguồn — không nguồn = không đưa vào
□ Ngày đăng phải nằm trong cửa sổ 30 ngày — item cũ hơn bị loại,
  kể cả khi rank cao
□ Phân biệt rõ engagement thật vs viral nhờ tranh cãi (đọc sentiment
  của comments, không chỉ đếm số)
□ Nếu một nền tảng không truy cập được → ghi rõ "X: không khảo sát được"
  thay vì im lặng bỏ qua
□ Brief ≤ 1 trang — đây là pulse check, không phải luận văn
```

## Anti-Fake-Pass

```
❌ Trích "cộng đồng nói rằng..." mà không có URL kèm ngày đăng
❌ Dùng kết quả search không lọc thời gian rồi claim "trending tháng này"
❌ Đếm 5 bài cùng 1 tác giả như 5 tín hiệu độc lập (vi phạm cap 3/tác giả)
❌ Suy ra sentiment từ tiêu đề bài viết thay vì nội dung thảo luận
❌ Claim convergence khi 2 nguồn thực chất cùng dẫn về 1 bài gốc
```

## See also

- `deep-research` — nghiên cứu sâu không giới hạn thời gian
- `arxiv-research` — nguồn học thuật
- `semantic-scholar` — citation graph
- `fact-check` (command) — kiểm chứng 1 claim đơn lẻ
