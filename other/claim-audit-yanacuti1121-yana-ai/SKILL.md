---
name: claim-audit
description: "Extract every verifiable claim from a piece of content, check each against sources, and sort into 4 buckets: correct, unsourced, needs-fixing, misleading. Use when asked to 'kiểm chứng luận điểm', 'audit claims', 'verify this article', 'tách luận điểm', 'check facts in this doc', 'đối chiếu với nguồn', or 'is this content accurate'. Do NOT use for: verifying a single claim before stating it — see /fact-check command. Do NOT use for: code correctness — see verification-engine."
tier: TIER 2 — CORRECTNESS
source: yana-ai (anh Tâm prompt pack, 2026-06-10)
---

# Claim Audit — Kiểm chứng luận điểm theo 4 nhóm

Bóc tách các luận điểm có thể kiểm chứng từ một nội dung cho trước,
đối chiếu từng cái với nguồn gốc, rồi phân loại độ tin cậy.

> Prompt gốc: *"Đọc nội dung bên dưới, tách từng luận điểm có thể kiểm chứng,
> rồi đối chiếu với nguồn, dữ liệu hoặc tài liệu liên quan. Sau đó chia thành
> bốn nhóm: đúng, thiếu nguồn, cần sửa, và có nguy cơ gây hiểu nhầm."*

---

## Khi nào dùng

- Review bài viết / README / docs / marketing copy trước khi publish
- Audit output của LLM khác trước khi tin
- Kiểm tra tài liệu kỹ thuật có khớp với codebase thực tế không
- Đối chiếu báo cáo với dữ liệu gốc

## Quy trình 3 bước

```
1. TÁCH — đọc toàn bộ nội dung, liệt kê MỌI luận điểm kiểm chứng được.
   Luận điểm = câu khẳng định có thể đúng/sai (số liệu, tên, hành vi,
   quan hệ nhân quả). Ý kiến chủ quan ("đẹp", "nên") → bỏ qua, ghi chú riêng.

2. ĐỐI CHIẾU — với mỗi luận điểm, tìm nguồn mạnh nhất có thể:
   file:line trong repo > git history > docs chính thức > web search.
   Ghi rõ nguồn đã check, kể cả khi không tìm thấy.

3. PHÂN NHÓM — xếp vào đúng 1 trong 4 nhóm, không có nhóm "không rõ":
   không tìm được nguồn thì là "thiếu nguồn", không phải bỏ trống.
```

## 4 nhóm phân loại

| Nhóm | Định nghĩa | Hành động đề xuất |
|------|-----------|-------------------|
| ✅ Đúng | Khớp nguồn, có trích dẫn | Giữ nguyên |
| 📎 Thiếu nguồn | Có thể đúng nhưng chưa verify được | Thêm nguồn hoặc gỡ |
| ✏️ Cần sửa | Sai so với nguồn — có bản đúng | Sửa theo nguồn, ghi diff |
| ⚠️ Gây hiểu nhầm | Đúng kỹ thuật nhưng ngữ cảnh/cách diễn đạt làm sai lệch | Viết lại + giải thích vì sao |

## Format output

```markdown
## Claim Audit — <tên nội dung>

Tổng: 14 luận điểm | ✅ 8 · 📎 3 · ✏️ 2 · ⚠️ 1

### ✏️ Cần sửa
1. "Hệ thống có 95 agents" → nguồn MANIFEST.json:12 ghi 97
   Sửa thành: "97 agents"

### ⚠️ Gây hiểu nhầm
1. "Test coverage 100%" — đúng cho module X nhưng câu đặt ở phần
   giới thiệu toàn dự án → người đọc hiểu là cả repo. Đề xuất: ...
```

## Anti-Fake-Pass

```
❌ Xếp "✅ Đúng" mà không ghi nguồn cụ thể (file:line / URL / commit)
❌ Bỏ sót luận điểm vì "hiển nhiên đúng" — hiển nhiên vẫn phải tách ra
❌ Gộp 2 luận điểm thành 1 dòng — mỗi claim phải audit độc lập
❌ Dùng trí nhớ của model làm "nguồn" — trí nhớ không phải evidence
❌ Có nhóm thứ 5 kiểu "chưa rõ" — luật là đúng 4 nhóm, ép phân loại
```

## See also

- `/fact-check` — verify 1 claim đơn lẻ trước khi phát biểu
- `verification-engine` — verify code/build claims bằng lệnh chạy thật
- `gates/truth_gate.md` — chặn claim không evidence ở mức session
