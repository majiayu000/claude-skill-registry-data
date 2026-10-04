---
name: sdd-context
description: Pha 0 SDD — khám phá ngữ cảnh và tạo .sdd/features/{feature-slug}/CONTEXT.md
user-invocable: true
---

# SDD Phase 0 — Context Discovery (`/sdd-context`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `PENDING`, `APPROVED`), file paths, and CLI commands are language-invariant.

Dùng khi bắt đầu feature để làm rõ bài toán nghiệp vụ và tạo `CONTEXT.md`.

## Tham số

- `--feature=<feature-slug>`: Feature identifier kebab-case, ví dụ `feat-001-order-checkout`.

> **Cập nhật CONTEXT.md đã approved?** Dùng `/sdd-update --artifact=context --reason="..."` thay vì chạy lại skill này. `/sdd-context` dùng để tạo Context lần đầu hoặc làm lại khi yêu cầu thay đổi hoàn toàn.

## Shared methodology contract

Đọc [AI Review Protocol](../_shared/ai-review-protocol.md) trước khi tạo artifact. `CONTEXT.md` mới phải dùng `Intent Packet`, `Describe-back record` và `Methodology Profile` trong protocol. Intent giữ technology-neutral; solution kỹ thuật chỉ được ghi như question, constraint hoặc decision đã approved, không phải requirement mặc định.

## Architecture Profile preflight

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Đọc profile và governance bắt buộc.
- `CONTEXT.md` được tạo với core-only baseline; không chọn HTTP framework, DB, ORM, validation library hoặc test command.
- Ghi profile version, baseline, evidence và chỉ unknown liên quan feature.
- Evidence mâu thuẫn profile thì dừng và tạo `PENDING HUMAN REVIEW` recommendation.

## Các bước

1. Tạo `.sdd/features/{feature-slug}/CONTEXT.md`.
2. Ghi `## Intent Packet`: `WHAT`, `WHY`, `Definition of Done`, boundaries, exclusions và decision owner.
3. Thu thập problem, user pain và desired behavior; chưa thiết kế giải pháp kỹ thuật.
4. Lập domain glossary, entity/state và business rule.
5. Xác định stakeholder, decision maker, business constraint và open question.
6. Ghi `## Methodology Profile` với depth `SKIP | SKETCH | DETAILED | FORMAL`, rationale, risk posture, high-risk review route và unresolved-decision owner. Depth là recommendation, không bỏ gate.
7. Gán disposition cho từng open question material: resolved, approved assumption, deferred hoặc blocking decision.
8. Ghi `## Describe-back record`: Agent diễn giải lại WHAT, WHY, DoD, boundaries/exclusions, assumptions/unknowns và material-question disposition; đối chiếu với Intent Packet, glossary và constraints.
9. Nếu intent bị trộn với solution, material question chưa disposition, describe-back mâu thuẫn evidence, hoặc Agent tự thêm technology/solution không có evidence, dừng trước `/sdd-spec`.
10. Kiểm tra DoD, ghi artifact và cập nhật `.sdd/README.md`.

## DoD

- [ ] `Intent Packet` nêu observable WHAT, WHY, Definition of Done, boundary/exclusion và decision owner.
- [ ] Team/Developer hiểu problem, không nhầm với solution.
- [ ] Domain glossary rõ nghĩa.
- [ ] Tech, business và time constraint đã ghi.
- [ ] Có decision maker rõ ràng.
- [ ] Methodology Profile có depth, rationale, risk posture và review route khi high-risk.
- [ ] Open question quan trọng đã trả lời, có approved assumption, deferred rõ ràng hoặc được đánh dấu blocking.
- [ ] Describe-back record khớp Intent Packet, glossary và constraints; assumption/unknown có impact và disposition.
- [ ] Không chuyển sang Spec khi intent lẫn solution, có material question chưa disposition hoặc describe-back mâu thuẫn.

## AI Recommendation và Human Final Review

Sau khi tạo/sửa `CONTEXT.md`, lưu canonical recommendation trong artifact, gồm Intent Packet, Describe-back record, business question, assumption, stakeholder, constraint, exclusion, Methodology Profile và alternative. Giữ `Human Final Review.Status: PENDING`. Chỉ chuyển sang `/sdd-spec` sau `APPROVED` có decision, reviewer và timestamp. Agent phải dừng, không self-approve.

## Hướng dẫn sử dụng
- **Khi dùng:** Khởi tạo Context lần đầu để chốt intent, boundaries, glossary và question disposition.
- **Không dùng:** Không dùng để update approved Context, chọn framework, hoặc thiết kế implementation.
- **Input:** Bắt buộc `--feature=<feature-slug>`; reject technology-specific requirements and unresolved material questions.
- **Điều kiện trước:** Governance, profile, constraints and repository evidence readable; existing Context updates route through `/sdd-update`.
- **Evidence:** `CONTEXT.md` Intent Packet, Methodology Profile, Describe-back record and recommendation `PENDING HUMAN REVIEW`.
- **Dừng khi:** Intent/solution mixed, describe-back contradiction, material question lacks disposition, or profile evidence conflicts.
- **Human quyết định:** Human approves Context before Spec and decides blocking assumptions via `/sdd-review`.
- **Lệnh tiếp theo:** `/sdd-review --feature=<feature-slug> --artifact=context --status=APPROVED ...`; then `/sdd-spec --feature=<feature-slug>` only after persisted approval.
- **Ví dụ:** `/sdd-context --feature=feat-order-checkout` for a new business outcome, not a framework design.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). `continue` chỉ sau `CONTEXT.md` có persisted `APPROVED`: `/sdd-spec --feature=<feature-slug>`. Với recommendation/review còn `PENDING`, chọn `Human decision required`; Human reviewer dùng `/sdd-review --feature=<feature-slug> --artifact=context --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"` sau khi chọn các giá trị thật, không dùng placeholder. Không gọi `/sdd-spec` trước persisted `APPROVED`. Intent/Describe-back/profile evidence mâu thuẫn là `BLOCKED`; nêu evidence và yêu cầu Human disposition, không tự chọn technology hoặc assumption.
