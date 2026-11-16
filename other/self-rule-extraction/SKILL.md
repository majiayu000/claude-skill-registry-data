---
name: self-rule-extraction
description: "Mine session history for recurring mistakes and distill them into short CLAUDE.md rules. Use when asked to 'rút rule', 'tự rút rule', 'extract rules from sessions', 'lỗi lặp đi lặp lại', 'review past sessions for mistakes', 'optimize CLAUDE.md from history', 'gom lỗi thành rule', or 'what do I keep fixing'. Do NOT use for: generating a CLAUDE.md from scratch — see claude-md-enhancer. Do NOT use for: one-off retrospectives — see session-wrap."
tier: TIER 3 — CONSISTENCY
source: yana-ai (anh Tâm prompt pack, 2026-06-10)
---

# Self-Rule Extraction — Tự rút rule từ lịch sử session

Đọc lại lịch sử các phiên làm việc, tìm lỗi con người phải sửa đi sửa lại,
rồi đúc kết thành rule ngắn để bổ sung vào CLAUDE.md / `core/rules/`.

> Prompt gốc: *"Đọc lại 50 session gần nhất, tìm lỗi tôi cứ phải sửa đi sửa lại,
> rồi gom lỗi lặp lại thành rule ngắn để thêm vào CLAUDE.md."*

---

## Khi nào dùng

- Cảm giác "AI cứ mắc lại đúng lỗi cũ" — cần biến feedback thành rule vĩnh viễn
- Sau một chuỗi session dài (sprint, milestone) — chốt bài học
- CLAUDE.md đang phình nhưng vẫn thiếu rule cho lỗi thực tế hay gặp
- Định kỳ (tuần/tháng) như một bước bảo trì cấu hình

## Nguồn dữ liệu để đào

```
1. Session logs       — ~/.claude/projects/<project>/  (transcript JSONL)
2. Assistant memory   — .claude/assistant/memory.md (log các session)
3. Git history        — git log --grep="fix" --oneline (fix lặp cùng chủ đề)
4. Audit trail        — core/memory/audit/agent-actions.log (BLOCK lặp lại)
5. Feedback trực tiếp — các lần user nói "không", "sai rồi", "đã bảo là..."
```

## Quy trình 4 bước

```
1. THU THẬP — quét N session gần nhất (mặc định 50), ghi lại mọi
   correction: user sửa output, revert commit, lặp lại yêu cầu cũ.

2. GOM CỤM — nhóm các correction theo chủ đề. Một cụm chỉ đáng làm rule
   khi xuất hiện ≥ 3 lần ở ≥ 2 session khác nhau.

3. ĐÚC RULE — mỗi cụm → 1 rule ≤ 3 dòng, dạng mệnh lệnh, có ví dụ sai/đúng.
   Rule phải actionable: agent đọc xong biết phải làm gì khác đi.

4. ĐỀ XUẤT — KHÔNG tự ghi vào CLAUDE.md. Trình danh sách rule kèm evidence
   (session nào, bao nhiêu lần) để con người duyệt từng rule.
```

## Format rule đề xuất

```markdown
### Rule đề xuất #1: <tên ngắn>
**Lỗi lặp:** <mô tả 1 câu>
**Bằng chứng:** xuất hiện 5 lần (sessions: 06-02, 06-04 ×2, 06-07, 06-09)
**Rule:** <mệnh lệnh ≤ 3 dòng>
**Đặt ở:** CLAUDE.md § <section> | core/rules/<file>.md
```

## Ngưỡng chất lượng

| Tiêu chí | Ngưỡng |
|----------|--------|
| Tần suất tối thiểu | ≥ 3 lần, ≥ 2 session |
| Độ dài rule | ≤ 3 dòng (rule dài = không ai đọc) |
| Số rule mỗi lần chạy | ≤ 7 (nhiều hơn = loãng) |
| Trùng rule hiện có | grep core/rules/ + CLAUDE.md trước khi đề xuất |

## Anti-Fake-Pass

```
❌ Đề xuất rule không kèm evidence (session ID + số lần) — bịa pattern
❌ Rule trùng nội dung rule đã có trong core/rules/ — phải grep trước
❌ Tự ghi thẳng vào CLAUDE.md không qua duyệt của con người
❌ Gom "lỗi" từ 1 session duy nhất — đó là incident, không phải pattern
❌ Rule mơ hồ kiểu "cẩn thận hơn" — không actionable thì không phải rule
```

## See also

- `claude-md-enhancer` — tạo/cấu trúc CLAUDE.md từ đầu
- `session-wrap` — tổng kết 1 session đơn lẻ
- `rule-consistency-policy.md` — check trùng trước khi thêm rule mới
