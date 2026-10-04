---
name: sdd-review
description: Ghi nhận Human Final Review bền vững cho SDD/ADD artifact và chuyển trạng thái sau khi review
user-invocable: true
---

# Human Review State Manager (`/sdd-review`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`HUMAN REVIEW: RECORDED`, `HUMAN REVIEW: BLOCKED`, `PENDING`, `APPROVED`, `REVISE`, `REJECTED`, `PENDING HUMAN REVIEW`, `APPLIED`, `NOT APPLICABLE`), file paths, and CLI commands are language-invariant.

Dùng skill này sau khi Human reviewer có thẩm quyền đã đọc recommendation và evidence. `Tech Lead` có thể review architecture, governance hoặc RFC khi repository giao thẩm quyền. Skill cập nhật đúng `Human Final Review` block; Agent không được tự chọn quyết định thay cho Human.

## Tham số

### Chọn target — dùng đúng một cách

- `--target=<repo-relative-path>`: đường dẫn tương đối tới feature artifact, `.sdd/reviews/` report, `.sdd/rfcs/` RFC hoặc `.sdd/architecture-profile.md` có review block.
- Hoặc dùng `--feature=<feature-slug> --artifact=<context|spec|plan|tasks>`.

Không dùng đồng thời hai cách. Không nhận absolute path, path ngoài repository, secret/private-key path, `node_modules/`, `dist/`, `.git/` hoặc `CONSTITUTION.md`.

### Ghi quyết định của Human

- `--status=<APPROVED|REVISE|REJECTED>`: bắt buộc.
- `--decision`, `--reviewer`, `--follow-up`: bắt buộc.
- `--reviewed-at=<ISO-8601 timestamp có timezone>`: tùy chọn; thiếu thì lấy thời gian hệ thống.

`APPROVED`, `REVISE`, `REJECTED` đều cần decision, reviewer, timestamp và follow-up. Không dùng placeholder hoặc chuỗi rỗng.

## Quy trình thực hiện

1. Resolve target; dừng nếu không tồn tại, có nhiều review block hoặc thiếu `## Human Final Review`.
2. Đọc `.claude/skills/_shared/ai-review-protocol.md`; yêu cầu recommendation `PENDING HUMAN REVIEW` đủ Scope, Recommendation, Evidence, Risks and assumptions, Alternatives considered, Required human decision.
3. Kiểm tra status và dữ liệu Human.
4. Nếu target là dispatch report, kiểm tra batch/task, frozen contract, scope/boundary, command/checkpoint và runtime evidence không bị claim quá mức.
5. Nếu target là post-code report `.sdd/reviews/post-code-<feature>-<delivery-or-timestamp>.md`, bắt buộc có changed boundary, `REQ-XXX` coverage, exact approved command/result, lint/audit/trace/sync state, residual risk và required Human decision.
6. Nếu review cũ `APPROVED`, chỉ review lại khi scope đã đổi và Agent đã tạo recommendation mới; intent, requirement, file boundary, exact command, checkpoint category hoặc shared-contract decision đổi đều invalidate approval.
7. Chỉ cập nhật năm field trong `## Human Final Review`; không sửa recommendation, requirements, source, architecture, tasks hay RFC.
8. Với `SPEC.md` + `APPROVED`, kiểm tra SemVer, `REQ-XXX`, EARS/acceptance/out-of-scope, recommendation và review fields trước khi đổi header thành `Status: APPROVED & LOCKED`.
9. Với Architecture Profile, review chỉ xác nhận selected binding/evidence/exact command đã trình bày; không resolve phần thiếu.

## Post-code review và completion

Post-code review áp dụng khi delivery thay đổi source behavior, tests, API/public/shared contract, runtime/dependency/security configuration, persistence schema hoặc business state. Thiếu report hợp lệ, `REVISE` hoặc `REJECTED` block delivery; docs-only không cần post-code review chỉ vì thay Markdown.

Kết quả hợp lệ:

```text
HUMAN REVIEW: RECORDED
Target: <path>
Previous status: <old status>
New status: <APPROVED|REVISE|REJECTED>
Reviewer: <identity>
Reviewed at: <timestamp>
Spec lock: APPLIED | NOT APPLICABLE | BLOCKED
Next step: <follow-up>
```

Nếu validation fail, không sửa file và báo `HUMAN REVIEW: BLOCKED` kèm điều kiện cần khắc phục.

## Điều kiện không được tự động vượt qua

- Không có recommendation hợp lệ `PENDING HUMAN REVIEW`.
- Thiếu field Human bắt buộc hoặc target ngoài phạm vi.
- Review cũ `APPROVED` nhưng không có scope change/recommendation mới.
- Spec không đạt DoD khi cần lock.
- Post-code report thiếu delivery evidence bắt buộc.
- Architecture Profile thiếu binding/evidence/exact command.
- RFC chưa qua `/sdd-rfc --approve`.

`/sdd-review` chỉ ghi nhận quyết định do người gọi cung cấp. Nó không xác minh quyền reviewer trong tổ chức.

## Hướng dẫn sử dụng
- **Khi dùng:** Persist a decision supplied by an authorized Human into one existing review block.
- **Không dùng:** Không dùng để invent a decision, edit recommendation/source, approve self-authored work, or replace RFC approval.
- **Input:** Exactly one target selector, status, non-placeholder decision/reviewer/follow-up; optional timezone-aware `--reviewed-at`; reject forbidden paths.
- **Điều kiện trước:** Target has one canonical recommendation and one `Human Final Review`; reviewer authority is supplied by Human/repository governance.
- **Evidence:** Updated five review fields, prior/new status, reviewer/timestamp, Spec lock result and persisted Follow-up.
- **Dừng khi:** Target invalid/multiple blocks, missing fields, stale approval without new recommendation, failed DoD or missing post-code evidence.
- **Human quyết định:** The invoking authorized Human owns the decision; `/sdd-review` records but does not verify organizational membership.
- **Lệnh tiếp theo:** Use the exact persisted Follow-up; for approved feature artifacts, `/sdd-plan`, `/sdd-tasks` or `/add-execute` only when its gate says eligible.
- **Ví dụ:** `/sdd-review --feature=feat-orders --artifact=plan --status=APPROVED --decision="Plan matches locked scope" --reviewer="Human owner" --follow-up="/sdd-tasks --feature=feat-orders"`.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md), giữ nguyên `HUMAN REVIEW: RECORDED | BLOCKED` report. Tóm tắt target, previous/new status, reviewer/timestamp, Spec lock và persisted Follow-up. `APPROVED` chỉ có thể `continue` theo Follow-up đã persist; `REVISE`/`REJECTED` là `Human decision required` hoặc `BLOCKED` theo Follow-up, không fabricated execution command. Validation failure là `BLOCKED`; không sửa recommendation/source/artifact ngoài năm review field.
