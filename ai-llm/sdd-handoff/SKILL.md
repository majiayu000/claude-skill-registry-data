---
name: sdd-handoff
description: Lưu trạng thái feature dở dang, cập nhật TASKS.md và tạo handoff report cho phiên sau
user-invocable: true
---

# SDD Handoff (`/sdd-handoff`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`), task status markers (`[x]`, `[/]`, `[ ]`), file paths, and CLI commands are language-invariant.

Dùng trước khi kết thúc phiên có feature chưa hoàn thành. Skill tổng hợp tiến độ, lưu điểm dừng và tạo handoff report cho phiên tiếp theo.

## Tham số

- `--feature=<feature-slug>`: Tùy chọn; feature đang thực hiện, ví dụ `feat-001-order-checkout`. Không truyền thì quét feature active trong `.sdd/features/`.

## Quy trình

1. Mở `.sdd/features/{feature-slug}/TASKS.md` và ghi đúng task status:
   - `[x]`: Hoàn thành; required exact verification command đã pass, hoặc `N/A` với lý do hợp lệ; Action Record, checkpoint, sync-back và post-code review `APPROVED` khi trigger delivery áp dụng đã có. Nếu post-code review còn thiếu, giữ `[/]`.
   - `[/]`: Đang thực hiện.
   - `[ ]`: Chưa thực hiện.
2. Ghi feature/task đang dở, profile version/binding evidence, active contract version, approved scope/file boundary, state-change checkpoint, exact command đã chạy/kết quả, method đang dở, blocker và open question. Nếu có Execution Record, giữ execution ID, feature, selected task execution grant ID/attempt/route/state/consumption state, `/add-execute`-issued consumer reference, atomic execution claim evidence, consumer/consumption evidence, selection/state, worker reference, runtime identity/enforcement evidence, pending approval và exact resume operation. Historical Dispatch Record giữ nguyên như immutable evidence, không reuse cho execution mới.
3. Thêm/cập nhật `## Current Handoff State` cuối `TASKS.md` với Action Record và Execution Record theo [AI Review Protocol](../_shared/ai-review-protocol.md), exact next decision/command và sync-back state. Agent/host task reference hết hạn hoặc unavailable phải được ghi rõ; không tự reassign ownership.
4. Handoff ngay khi scope expansion, blocker, contract drift hoặc decision mới xuất hiện; không tiếp tục absorb unrelated cleanup.
5. Xuất tóm tắt và hướng dẫn phiên sau. Human khởi động phiên Claude Code mới bằng launcher chuẩn không bỏ qua permission, rồi dùng `/sdd-resume --feature=<feature-slug>` sau khi xác nhận đúng repository.

## AI Recommendation và Human Final Review

Trước khi kết thúc phiên, tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm task tiếp theo, active contract version, approved scope, pending checkpoint, evidence gap, blocker, exact next decision/command và resume command. Lưu tại `.sdd/reviews/handoff-<slug>.md` với `PENDING HUMAN REVIEW`; chỉ cập nhật `TASKS.md` bằng `## Current Handoff State` và record không chứa thêm `Human Final Review` block. Human reviewer có thẩm quyền xác nhận resume scope trước material state change hoặc strict-checkpoint task; Agent không tự đánh dấu handoff hoàn tất hoặc approve hành động tiếp theo.

## Hướng dẫn sử dụng
- **Khi dùng:** Persist an interrupted feature state for a later session without authorizing new execution.
- **Không dùng:** Không dùng để cấp grant, approve scope, reassign ownership, or absorb unrelated cleanup.
- **Input:** Optional `--feature`; reject invented task/worker IDs, authority tokens and resume claims.
- **Điều kiện trước:** Existing TASKS, records, profile and handoff state are readable; update only `Current Handoff State` plus handoff review.
- **Evidence:** `.sdd/reviews/handoff-<slug>.md`, TASKS markers, Action/Execution Record, exact command result and blocker.
- **Dừng khi:** Scope expansion, contract drift, missing evidence, stale ownership or required checkpoint cannot be represented safely.
- **Human quyết định:** Human confirms resume scope/checkpoint; handoff recommendation never grants execution or replaces `/sdd-review`.
- **Lệnh tiếp theo:** In a new verified session, `/sdd-resume --feature=<feature-slug>`; then only an eligible `/add-execute` route.
- **Ví dụ:** `/sdd-handoff --feature=feat-orders` records a blocked T003 without changing its owner.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Nêu feature/task marker, active contract/profile/review/checkpoint/grant state, Action/Execution Record, exact command/result và blocker đã persist. `continue` chỉ sau khi Human đã mở đúng repository trong một phiên Claude Code mới bằng launcher chuẩn không bỏ qua permission: `/sdd-resume --feature=<feature-slug>`, rồi chỉ dùng eligible `/add-execute --feature=<feature-slug> --task=<task-id> --resume` hoặc `/add-execute --feature=<feature-slug> --all` sau revalidation. Material checkpoint pending, drift hoặc incomplete evidence là `Human decision required` hoặc `BLOCKED`; không dùng script hoặc flag bỏ qua permission, không reassign ownership hay reuse grant cũ.
