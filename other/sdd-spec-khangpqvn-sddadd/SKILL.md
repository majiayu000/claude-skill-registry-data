---
name: sdd-spec
description: Pha 1 SDD — tạo SPEC.md với EARS, SemVer, BDD, error contract và DoD
user-invocable: true
---

# SDD Phase 1 — Specification (`/sdd-spec`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `PENDING`, `APPROVED`, `APPROVED & LOCKED`, `DRAFT`), EARS keywords (`WHEN`, `WHILE`, `WHERE`, `IF`, `THEN`, `SHALL`), file paths, and CLI commands are language-invariant.

Dùng `CONTEXT.md` và `CONSTITUTION.md` để tạo `.sdd/features/{feature-slug}/SPEC.md`.

## Tham số

- `--feature=<feature-slug>`: Feature identifier.

> **Cập nhật Spec đã `APPROVED & LOCKED`?** Dùng `/sdd-update --artifact=spec --bump=<patch|minor|major>` thay vì chạy lại skill này. `/sdd-spec` dùng để tạo Spec lần đầu hoặc làm lại khi context thay đổi lớn.

## Shared methodology contract

Đọc [AI Review Protocol](../_shared/ai-review-protocol.md). Kế thừa `Intent Packet`, `Describe-back record` và `Methodology Profile` từ Context. Ghi depth/rationale/risk posture trong Spec header; không tự đổi level đã được chọn. Methodology metadata không chọn technology hoặc bypass Architecture Profile gate.

## Architecture Profile preflight

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Đọc profile trước Context và Constitution.
- `SPEC.md` chỉ mô tả behavior, data contract, error và NFR; không sinh ORM decorator, framework schema, package hoặc CLI command chưa approved.
- Ghi profile version và binding feature cần dùng.
- Binding chưa resolve được phép trong Spec nhưng phải là planning blocker; `PLAN.md` dừng đến khi Human reviewer có thẩm quyền approve.

## Clarification-First — bắt buộc trước khi viết requirement

Trước khi draft requirement, AI phải liệt kê điểm chưa chắc chắn từ `CONTEXT.md` theo 3 loại:

1. **Business logic gaps** — Rule nào chưa xác định rõ?
2. **Constraint kỹ thuật thiếu** — NFR nào chưa có giá trị cụ thể?
3. **Edge case chưa đề cập** — Tình huống hiếm nhưng quan trọng?

Với mỗi điểm, nêu điều chưa chắc, assumption sẽ dùng nếu phải chọn và ảnh hưởng của assumption. **Dừng và chờ Human reviewer có thẩm quyền confirm trước khi viết requirement.** Nếu được phép tiếp tục với assumption, ghi rõ assumption đó vào Spec.

## Spec Depth — kế thừa và áp dụng

`Depth` dùng đúng một trong `SKIP | SKETCH | DETAILED | FORMAL` theo Methodology Profile:

| Level | Dùng khi | Output tối thiểu |
| :--- | :--- | :--- |
| `SKIP` | Scope đã được Human chấp nhận là exploratory/throwaway hoặc không thêm behavior/contract material | Lý do, evidence, boundary và decision; không dùng để né review. |
| `SKETCH` | Logic/risk thấp, phạm vi nhỏ | Requirement, acceptance, out-of-scope và clarification cho ambiguity. |
| `DETAILED` | Mặc định cho integration, authorization, concurrency, third-party hoặc risk đáng kể | Đủ tám thành phần Spec. |
| `FORMAL` | Money, compliance, destructive/irreversible work, migration, security/authorization, core business state hoặc external contract | Detailed cộng state/transition, invariant và adversarial review. |

Không level nào bỏ Human review, Feature Lock, Architecture Profile evidence, exact approved command hoặc material checkpoint. `FORMAL` không tự tạo formal-verification tooling khi chưa có binding/evidence.

## 8 Thành phần Spec bắt buộc

| # | Thành phần | Câu hỏi phải trả lời |
| :--- | :--- | :--- |
| 1 | **Context & Goal** | Tại sao feature tồn tại? |
| 2 | **Actors & Roles** | Ai tương tác? Với quyền gì? |
| 3 | **Functional Requirements** | Hệ thống làm gì? (EARS) |
| 4 | **Non-functional Requirements** | Tốt đến mức nào? |
| 5 | **Data Model** | Dữ liệu có cấu trúc gì? |
| 6 | **Error Handling** | Khi sai thì làm gì? |
| 7 | **Acceptance Criteria** | Định nghĩa xong là gì? |
| 8 | **Out of Scope** | Hệ thống không làm gì? |

## EARS Notation — 5 patterns

Mọi Functional Requirement phải thuộc đúng một pattern:

- **Ubiquitous**: `The <system> SHALL <action>`
- **Event-driven**: `WHEN <trigger>, the <system> SHALL <action>`
- **State-driven**: `WHILE <in state>, the <system> SHALL <action>`
- **Optional**: `WHERE <feature is included>, the <system> SHALL <action>`
- **Unwanted**: `IF <invalid/error condition>, THEN the <system> SHALL <action>`

Mỗi happy path (`WHEN`) cần ít nhất một `IF ... THEN ...` cho error tương ứng. Tránh từ mơ hồ; mọi NFR phải có giá trị đo được.

## Adversarial quality pass

Trước recommendation, thực hiện và ghi disposition cho mọi finding:

1. **Pre-mortem:** giả định feature đã gây incident; nêu failure scenario, impact và rule/evidence cần bổ sung.
2. **Domain walkthrough:** xem normal flow, error flow, boundary/state transition, actor/authorization, duplicate/concurrency và data lifecycle khi applicable.
3. Mỗi finding phải thành một trong: clarified rule, approved assumption, deferred item hoặc blocking Human decision.

Pass này không thay Human review và không cho phép Agent tự bù rule thiếu bằng assumption không được ghi nhận.

## Feature Lock

`SPEC.md` phải có `## Feature Lock` trước recommendation:

```markdown
- Locked scope: <behavior and contract in this feature or sprint>
- Deferred work: <explicitly excluded future work>
- Change path: /sdd-update --feature=<slug> --artifact=spec --bump=<...> --reason="..."
- Lock boundary: Feature/sprint only; this does not lock unrelated project work.
```

Sau `APPROVED & LOCKED`, behavior hoặc contract chỉ thay đổi qua `/sdd-update`.

## Các bước

1. Đọc Context, Describe-back, Methodology Profile và Constitution.
2. Chạy Clarification-First; chờ Human reviewer có thẩm quyền xác nhận trước bước tiếp theo.
3. Áp dụng depth đã chọn và high-risk review route.
4. Ghi SemVer và `Status: DRAFT`.
5. Viết Spec theo depth; Functional Requirement dùng EARS.
6. Chạy adversarial quality pass và ghi disposition.
7. Ghi Feature Lock và deferred work.
8. Kiểm tra DoD, cập nhật changelog và tạo recommendation.

## DoD

- [ ] Describe-back/Clarification-First không còn contradiction hoặc material question không disposition.
- [ ] Methodology Profile có depth, rationale, risk posture, review route khi high-risk và decision owner.
- [ ] Depth được áp dụng theo contract; `SKIP` có Human-accepted rationale/evidence.
- [ ] Có đủ tám thành phần phù hợp với depth; mọi Functional Requirement dùng EARS.
- [ ] Mỗi happy path có ít nhất một Unwanted EARS tương ứng; NFR đo được.
- [ ] Adversarial pre-mortem và domain walkthrough đã ghi; finding có disposition.
- [ ] Feature Lock ghi locked scope, deferred work và `/sdd-update` path.
- [ ] SemVer/changelog đúng và Human Final Review đã `APPROVED` trước lock.

## AI Recommendation và Human Final Review

Sau khi tạo/sửa `SPEC.md`, lưu canonical recommendation gồm Methodology Profile, requirement gap, EARS risk, adversarial findings/disposition, high-risk review route, edge case, Out of Scope, Feature Lock và SemVer impact. Giữ `Human Final Review.Status: PENDING`; `/sdd-plan` bị block đến khi Human reviewer có thẩm quyền ghi `APPROVED`. Agent không được đặt `APPROVED & LOCKED` thay con người.

## Hướng dẫn sử dụng
- **Khi dùng:** Draft/rebuild a Spec from an approved Context using the inherited depth and EARS; nền tảng của mọi task `@ears`.
- **Không dùng:** Không dùng để sửa Spec `APPROVED & LOCKED` (dùng `/sdd-update --artifact=spec`), hoặc ghi framework/ORM schema/command chưa approved.
- **Input:** Bắt buộc `--feature`; reject missing Clarification-First disposition, guessed bindings và non-EARS requirement.
- **Điều kiện trước:** `CONTEXT.md` có persisted `APPROVED`, Describe-back khớp evidence, Methodology Profile depth đã chọn, high-risk review route được Human chấp nhận.
- **Evidence:** `SPEC.md` SemVer + `Status: DRAFT`, tám thành phần, EARS/Unwanted pairs, Feature Lock, adversarial disposition và recommendation `PENDING HUMAN REVIEW`.
- **Dừng khi:** Material question chưa disposition, high-risk route chưa có evidence, depth bị tự đổi, hoặc Agent thêm rule bằng assumption chưa ghi nhận.
- **Human quyết định:** Human lock Spec và quyết định gap NFR/edge case; Agent không tự đặt `APPROVED & LOCKED`.
- **Lệnh tiếp theo:** `/sdd-review --feature=<feature-slug> --artifact=spec --status=<APPROVED|REVISE|REJECTED> ...`; `continue` chỉ sau `APPROVED & LOCKED`: `/sdd-plan --feature=<feature-slug>`.
- **Ví dụ:** `/sdd-spec --feature=feat-orders` với `FORMAL` depth vì đụng schema, dừng nếu DB binding chưa resolve.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Sau DoD pass nhưng Spec chưa lock, chọn `Human decision required`; Human reviewer có thẩm quyền ghi decision, reviewer identity và Follow-up không phải placeholder bằng `/sdd-review --feature=<feature-slug> --artifact=spec --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. `continue` chỉ sau `APPROVED & LOCKED`: `/sdd-plan --feature=<feature-slug>`. Clarification, EARS, high-risk route hoặc binding evidence còn thiếu là `BLOCKED`; nêu gap/disposition, không sinh Plan hoặc command adapter-specific.
