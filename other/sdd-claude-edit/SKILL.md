---
name: sdd-claude-edit
description: Cập nhật CLAUDE.md an toàn theo Architecture Profile và repository evidence
user-invocable: true
---

# SDD Project Memory Editor (`/sdd-claude-edit`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`), file paths, and CLI commands are language-invariant.

Dùng khi cập nhật `CLAUDE.md`, là bộ nhớ kiến trúc cho người đọc và phải phản chiếu Architecture Profile đã approved. Skill này không thay thế feature pipeline hoặc `/add-execute`, không cấp execution grant và không mở rộng quyền Agent.

## Khi nào dùng / không dùng

- **Dùng khi:** project memory cần phản ánh binding hoặc guidance đã được approve.
- **Không dùng khi:** cần sửa feature behavior, source code, Spec/Plan/Tasks hoặc cần né Human review.

## Tham số

- `--section=<tên-mục>`: Tùy chọn; mục cần sửa, ví dụ `tech-stack`, `naming-conventions`, `directory-anatomy`, `architecture-dna`.
- `--reason=<lý-do>`: Lý do cập nhật kiến trúc hoặc project memory.

## Cấu trúc 4 sections cốt lõi của CLAUDE.md

`CLAUDE.md` phải phản chiếu **project thực** — không dùng placeholder. Khi sửa, ưu tiên update các sections:

| Section | Nội dung | Khi nào update |
| :--- | :--- | :--- |
| **TL;DR (30 giây)** | Loại service, giao thức chính, dependency quan trọng | Khi scope project thay đổi |
| **Architecture** | Pattern (Clean/Hexagonal/MVC), file structure, dependency direction | Khi profile binding thay đổi |
| **Lesson Learned** | Sự cố, root cause, fix áp dụng — format `[YYYY-MM]` | Sau incident, post-mortem |
| **Current Sprint Focus** | Feature đang build; link đến `TASKS.md` | Đầu mỗi sprint/feature |

`CLAUDE.md` là bộ nhớ kiến trúc cho **con người đọc**. Không dùng để Agent suy đoán stack; Agent đọc Architecture Profile. Không áp đặt section không tồn tại vào `CLAUDE.md` hiện hữu.

## Quy trình

1. Đọc `CLAUDE.md`, `CONSTITUTION.md`, `.sdd/architecture-profile.md`, constraint và evidence repository.
2. Tech stack/architecture binding chỉ được cập nhật trong profile theo [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md); không suy đoán framework, database, ORM/query layer, validation hoặc command từ prose.
3. Profile thay đổi: invalidate recommendation/Plan/Tasks bị ảnh hưởng, tạo `PENDING HUMAN REVIEW`, rồi chỉ phản chiếu binding đã `APPROVED` vào `CLAUDE.md`.
4. Không áp đặt section, version hoặc changelog không tồn tại. Giữ cấu trúc hiện hữu trừ khi Human-approved scope yêu cầu thay đổi.
5. Kiểm tra nội dung `CLAUDE.md` khớp source layout, skill và profile hiện tại.

## AI Recommendation và Human Final Review

Trước khi sửa `CLAUDE.md`, tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm architecture evidence, memory change đề xuất, alternative, drift risk và affected skill. Lưu tại `.sdd/reviews/claude-edit.md` với `PENDING HUMAN REVIEW`. Human reviewer có thẩm quyền phải `APPROVED` trước edit; `Tech Lead` có thể review architecture khi repository giao thẩm quyền. Sau edit refresh recommendation và không tự approve project memory mới.

## Hướng dẫn sử dụng
- **Khi dùng:** Đề xuất cập nhật project memory phản ánh binding hoặc durable guidance đã approved.
- **Không dùng:** Không dùng để chọn stack, sửa feature/source, thay Constitution, hoặc bỏ qua review.
- **Input:** Optional `--section` and `--reason`; reject placeholders and unapproved technology claims.
- **Điều kiện trước:** Profile, governance, constraints and repository evidence readable; recommendation exists before edit.
- **Evidence:** `.sdd/reviews/claude-edit.md`, profile evidence, bounded memory diff, drift check and refreshed recommendation.
- **Dừng khi:** Profile missing/conflict, binding unapproved, section not present without approved scope, or Human review absent.
- **Human quyết định:** Authorized Human approves memory boundary; Agent reflects only approved profile facts and does not self-approve.
- **Lệnh tiếp theo:** `/sdd-review --target=.sdd/reviews/claude-edit.md --status=APPROVED ...`, then use its persisted Follow-up.
- **Ví dụ:** `/sdd-claude-edit --section=architecture-dna --reason="Reflect approved Clean Architecture boundary"`.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Nêu architecture evidence, proposed/reflected memory boundary, drift risk và `.sdd/reviews/claude-edit.md`. Trước edit chọn `Human decision required`; Human reviewer có thẩm quyền ghi decision, reviewer identity và Follow-up không phải placeholder bằng `/sdd-review --target=.sdd/reviews/claude-edit.md --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. Sau edit nêu recommendation được refresh thay vì tự approve. Profile evidence thiếu/conflict là `BLOCKED`; không phản chiếu stack chưa `APPROVED`.
