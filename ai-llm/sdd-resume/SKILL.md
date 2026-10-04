---
name: sdd-resume
description: Khôi phục ngữ cảnh feature dở dang từ TASKS.md, SPEC.md và Architecture Profile
user-invocable: true
---

# SDD Resume (`/sdd-resume`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `PENDING`, `APPROVED`, `BLOCKED`), file paths, and CLI commands are language-invariant.

Dùng khi bắt đầu phiên mới để quét task dở dang và nạp lại feature context.

## Tham số

- `--feature=<feature-slug>`: Tùy chọn; feature cần tiếp tục. Không truyền thì quét `.sdd/features/` tìm `TASKS.md` có `[/]` hoặc task `[ ]` đầu tiên.

## Quy trình

1. Quét feature/task dở dang trong `.sdd/features/`.
2. Đọc `CONTEXT.md`, `SPEC.md`, Architecture Profile theo [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md), `PLAN.md`, `TASKS.md`, `.sdd/shared_context.md` và `## Current Handoff State` nếu có.
3. Báo feature, task đã xong/tổng số, task tiếp theo, Intent/DoD, approved scope/file boundary, active contract version, profile version/binding, state-change category/checkpoint, exact command, review state, exact next decision/command và unresolved blocker. Detect active Execution Record và báo execution ID/state, selected task grant ID/attempt/route/state/consumption state, `/add-execute`-issued consumer reference, atomic execution claim evidence, consumer/consumption evidence, worker references và runtime evidence. Historical Dispatch Record chỉ báo như immutable evidence, không dùng làm authority mới.
4. Với legacy high-risk feature thiếu metadata, dừng và yêu cầu Human disposition: chấp nhận evidence hiện tại hoặc yêu cầu targeted update. Không retroactively invalidate artifact chỉ vì format cũ.
5. Task `RETRY_PENDING` chỉ retry qua `/add-execute --feature=<feature-slug> --task=<task-id> --retry` sau khi revalidate immutable task boundary, contract/profile/checkpoint, Human approval và observed runtime evidence.
6. Task `RUNNING` bị gián đoạn hoặc `BLOCKED` chỉ resume qua `/add-execute --feature=<feature-slug> --task=<task-id> --resume` sau khi resolution evidence closes/retires stale record. `ESCALATED` cần Human disposition explicit authorizing recovery trước `--resume`; changed immutable inputs cần approval mới.
7. Không giả định Agent ID, host task mirror hoặc permission của session cũ còn tồn tại.
8. Chỉ đề xuất `/add-execute --feature=<feature-slug> --task=<task-id>` hoặc `/add-execute --feature=<feature-slug> --all` khi task scope, required binding, exact verification command, review state, required checkpoint và contract ownership đều hợp lệ. Skill tự resolve direct/orchestrated từ persisted governance, tạo Execution Record/grant/consumer mới và chỉ launch worker khi runtime capability observed. Consumed hoặc non-eligible grant không được reuse; chỉ route qua named `--resume` hoặc `--retry` khi đủ điều kiện.
9. Nếu profile binding/review/checkpoint còn `PENDING`, contract drift, hoặc blocker chưa resolve, báo blocker theo protocol; không đề xuất execution command suy đoán.

## AI Recommendation và Human Final Review

Sau khi khôi phục context, tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm task tiếp theo, active contract version, approved scope, pending checkpoint, evidence gap, unresolved blocker và exact resume command. Lưu tại `.sdd/reviews/resume-<slug>.md` với `PENDING HUMAN REVIEW`; chỉ cập nhật `TASKS.md` bằng `## Current Handoff State` và record không chứa thêm `Human Final Review` block. Không gọi `/add-execute` trước khi Human reviewer có thẩm quyền ghi `APPROVED` khi checkpoint required; Agent không tự approve resume scope.

## Hướng dẫn sử dụng
- **Khi dùng:** Nạp lại persisted feature context trong session mới và đề xuất eligible route.
- **Không dùng:** Không dùng để issue grants, reuse consumed grants, assume old workers, or authorize resume without evidence.
- **Input:** Optional `--feature`; reject guessed task IDs, stale runtime identity and direct execution override.
- **Điều kiện trước:** Verified repository, TASKS/handoff records, profile, reviews, checkpoint and contract ownership are readable.
- **Evidence:** `.sdd/reviews/resume-<slug>.md`, Current Handoff State, active Execution Record and revalidation result.
- **Dừng khi:** Pending review/checkpoint, drift, unresolved blocker, consumed grant, missing command or unavailable orchestrated runtime.
- **Human quyết định:** Human dispositions `ESCALATED`/checkpoint recovery; resume recommendation is not a grant.
- **Lệnh tiếp theo:** Only the named `/add-execute ... --resume|--retry` or fresh task command shown by observed eligible state.
- **Ví dụ:** `/sdd-resume --feature=feat-orders` reports T003 `RUNNING` and requires `/add-execute --feature=feat-orders --task=T003 --resume` only after resolution evidence.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Tóm tắt selected task, approved boundary, profile/exact command, review/checkpoint, contract, Execution Record/grant/consumer và runtime evidence quan sát. `continue` chỉ tới `/add-execute --feature=<feature-slug> --task=<task-id>` hoặc feature snapshot `/add-execute --feature=<feature-slug> --all` khi mọi precondition hợp lệ; `RETRY_PENDING` chỉ dùng `/add-execute --feature=<feature-slug> --task=<task-id> --retry` sau immutable-state revalidation, interrupted/resolved state chỉ dùng `/add-execute --feature=<feature-slug> --task=<task-id> --resume` sau resolution evidence. Pending checkpoint là `Human decision required`; consumed/non-eligible grant, drift, missing evidence hoặc unavailable orchestrated runtime là `BLOCKED`, không suy đoán session/worker cũ.
