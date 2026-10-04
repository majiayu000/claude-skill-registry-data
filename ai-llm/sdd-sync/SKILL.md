---
name: sdd-sync
description: Đồng bộ Master Feature Registry và shared contract trong .sdd
user-invocable: true
---

# SDD Registry Sync (`/sdd-sync`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`, `CONFIGURATION GAP`), file paths, and CLI commands are language-invariant.

Dùng để quét và cập nhật Master Feature Registry (`.sdd/README.md`) cùng shared API/state contract (`.sdd/shared_context.md`) sau khi feature thay đổi.

## Tham số

- `--feature=<feature-slug>`: Tùy chọn; chỉ đồng bộ feature này. Không truyền thì giữ hành vi quét mọi feature.
- `--reason=<change-summary>`: Tùy chọn; lý do sync. Bắt buộc khi sync theo change đã biết để liên kết Action Record/change impact.

## Architecture Profile reference

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Đọc `.sdd/architecture-profile.md` trước khi trích xuất/cập nhật shared contract.
- Chỉ ghi HTTP route, event schema, DTO validator, persistence identifier và command khi profile binding/evidence tương ứng đã `APPROVED`.
- Binding chưa chọn: ghi behavior và data shape technology-neutral; không thêm framework route syntax, decorator, ORM schema hoặc command suy đoán.
- Artifact feature mâu thuẫn profile `APPROVED`: giữ evidence, báo `CONFIGURATION GAP` và yêu cầu Human reviewer có thẩm quyền disposition; không tự rewrite contract.

## Quy trình

1. Quét `.sdd/features/` hoặc feature được chọn; đọc header từng `SPEC.md` để lấy status, SemVer và số `REQ-XXX`.
2. Phân loại thay đổi dự kiến. Chỉ cập nhật registry không làm thay đổi contract có thể tiếp tục với Action Record. Mọi shared/public contract change là material state change.
3. Trước shared-contract write, xác minh checkpoint persisted đã `APPROVED` cho feature/contract, cùng decision, reviewer và timestamp. Nếu thiếu, tạo recommendation `PENDING HUMAN REVIEW`, lưu tại `.sdd/reviews/sync-<slug>.md`, rồi dừng; recommendation sau action không thể hợp thức hóa write trước đó.
4. Trước khi sửa shared contract, đọc ownership và frozen contract record trong `.sdd/shared_context.md`. Chỉ contract owner hoặc Lead được sửa; actor khác dừng và gửi change request.
5. Sau checkpoint hợp lệ, cập nhật `.sdd/README.md`; tổng hợp contract được evidence xác nhận; ghi producer, contract ID/version/status, owner, linked `REQ-XXX`/task/review/Execution Record evidence, consumers, compatibility, unresolved decision, last sync và Action Record reference.
6. Ghi hoặc đề xuất `/sdd-trace` khi contract version, requirement hoặc implementation evidence thay đổi. Action Record phải tham chiếu checkpoint đã tồn tại trước action.

## Output

```text
SDD SYNC
Feature: <slug | all>
Reason: <summary | full registry sync>
Contract: <ID/version/status or N/A>
Producer: <feature>
Owner: <role>
Consumers: <list or none>
Compatibility: <compatible | migration required | pending decision>
Evidence: <REQ/task/review/action record>
Unresolved decision: <none or decision>
Next trace/sync step: <command or N/A>
```

## AI Recommendation và Human Final Review

Nếu sync chỉ cập nhật registry không thay đổi contract, ghi Action Record và recommendation theo protocol nếu artifact scope thay đổi. Nếu shared contract đã thay đổi, checkpoint phải tồn tại trước action; Action Record sau sync tham chiếu checkpoint đó và nêu changed producer/version/status/owner/consumer/compatibility, drift evidence, unresolved decision và residual integration risk. Agent không tự kết luận registry hoặc contract đã `APPROVED`.

## Hướng dẫn sử dụng
- **Khi dùng:** Đồng bộ registry or an already-approved shared contract after feature evidence changes.
- **Không dùng:** Không dùng để tự rewrite contract, infer adapter syntax, or write without pre-existing checkpoint and owner authority.
- **Input:** Optional `--feature`, `--reason` required for known change; reject unapproved binding and non-owner contract writes.
- **Điều kiện trước:** Profile, feature evidence, shared context and ownership/frozen contract record are readable; contract checkpoint is `APPROVED` before write.
- **Evidence:** `SDD SYNC` report, registry diff, producer/version/owner/consumers/compatibility, Action Record and trace decision.
- **Dừng khi:** Missing owner/checkpoint/binding, contract drift, unresolved compatibility, or recommendation would be created only after an unsafe write.
- **Human quyết định:** Contract owner/Lead approves material contract change; Agent only performs approved bounded sync.
- **Lệnh tiếp theo:** `/sdd-trace --feature=<feature-slug> --diff` when requirement/contract evidence changed; otherwise use observed `Next trace/sync step`.
- **Ví dụ:** `/sdd-sync --feature=feat-orders --reason="Record approved contract v2"` after checkpoint evidence exists.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Giữ `SDD SYNC` report hiện có và tóm tắt registry-only hay shared-contract mutation, owner/checkpoint, compatibility, evidence và unresolved decision. Registry-only sync có thể `continue` theo `Next trace/sync step` đã observed; shared-contract write cần checkpoint/review là `Human decision required`. Missing binding, owner, checkpoint hoặc contract drift là `BLOCKED`; không rewrite contract hoặc suy đoán adapter syntax.
