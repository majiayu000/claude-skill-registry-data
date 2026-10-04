---
name: add-execute
description: Pha 4–5 ADD — preflight, điều phối và thực thi task/feature theo Architecture Profile và governance
user-invocable: true
---

# ADD Phase 4–5 — Unified Execution và Validation (`/add-execute`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`, `SHADOW PLAN`, `BLOCKED`), rule codes, `@ears` references, file paths, and CLI commands are language-invariant.

`/add-execute` là entry point công khai duy nhất để preflight, cấp execution evidence, điều phối và thực thi task đã approved. `Dispatch Record`/grant/consumer là evidence nội bộ; user không copy hoặc truyền opaque token.

## Tham số

```text
/add-execute --feature=<feature-slug> --task=<T00X> [--strict-checkpoint]
/add-execute --feature=<feature-slug> --all [--strict-checkpoint]
/add-execute --feature=<feature-slug> --task=<T00X> --retry [--strict-checkpoint]
/add-execute --feature=<feature-slug> --task=<T00X> --resume [--strict-checkpoint]
```

- `--feature=<feature-slug>`: Bắt buộc.
- Chọn đúng một selector: `--task=<T00X>` cho một task, hoặc `--all` cho snapshot task eligible của feature.
- `--retry` và `--resume` loại trừ nhau, chỉ dùng với `--task`, không kết hợp `--all`.
- `--strict-checkpoint`: Tùy chọn, tăng gate Human checkpoint cho mọi task; không thay baseline material-state checkpoint.
- Reject `--agent-execution`, `--project-ownership`, `--team-size`, `--dispatch-record`, `--dispatch-grant` và `--dispatch-consumer`. Không user nào chọn route hoặc tự cung cấp authority token.

## Governance và runtime resolver (BLOCKING)

1. Đọc `.sdd/shared_context.md`. Chỉ dùng canonical settings khi có đúng một `# Project Ownership: solo|team` và đúng một `# Agent Execution: direct|orchestrated` hợp lệ. Thiếu, trùng hoặc malformed canonical header là `BLOCKED`.
2. Chỉ khi cả hai canonical header vắng mặt, dùng đúng một legacy source hợp lệ: `# Collaboration Mode: solo|team` hoặc legacy record hợp lệ. Legacy source duplicate, malformed hoặc coexist là `BLOCKED`; ghi migration warning và không rewrite governance.
3. Không nhận invocation override. `Project Ownership` quyết định Human accountability/delivery; không quyết định Agent route.
4. `direct` chạy trong session hiện tại. `orchestrated` chỉ launch worker khi Claude Code `Agent` availability đã được quan sát. Runtime worker unavailable là `BLOCKED`; không fallback sang `direct`.
5. Runtime policy metadata không phải host enforcement. Persist `Runtime identity/enforcement: UNVERIFIED` khi không có host-controlled claim observed; không claim replay prevention từ Markdown, consumer reference hoặc YAML policy.

## Selection và preflight (BLOCKING)

Đọc `AGENTS.md`, `CONSTITUTION.md`, `CLAUDE.md`, Architecture Profile, constraints, `.sdd/mcp-config.yaml`, shared contract record, feature `CONTEXT.md`, `SPEC.md`, `PLAN.md`, `TASKS.md`, persisted reviews và handoff state.

- `TASKS.md` phải có `Human Final Review: APPROVED`.
- `--task` chỉ chọn task được nêu. `--all` tạo snapshot theo thứ tự khai báo trong `TASKS.md` của task chưa complete và eligible tại lúc preflight bắt đầu; không tự thêm task mới eligible sau đó.
- Với từng selected task, xác minh task marker/dependency, approved intent/file boundary, profile binding, exact verification command, checkpoint, frozen-contract owner/version, post-code route và no overlap/shared-contract authorization.
- `--all` preflight toàn snapshot trước grant, worker launch, grant consumption, command, edit hay action. Bất kỳ failed precondition nào là `BLOCKED`; không cấp partial grant.
- Classify selected work: `single-owned`, `parallel-owned`, `sequential-handoff` hoặc `blocked`. `parallel-owned` chỉ cho task không dependency, non-overlapping boundary và không shared-contract mutation. Shared work, retry, integration và dependent work luôn tuần tự.
- Missing evidence, drift, unapproved command, scope expansion, package/config change, policy violation hoặc material decision mới là `BLOCKED`. Không suy đoán binding hay command.

## Execution Record và task grant

Trước action, `/add-execute` ghi `## Execution Record — E-<feature>-<selection>-A<attempt>` dưới `## Current Handoff State` của `TASKS.md`, theo [AI Review Protocol](../_shared/ai-review-protocol.md). Record có execution mode resolved, selected task order, classification, immutable inputs, one task execution grant per task attempt, opaque consumer, runtime/claim evidence, integration state, retry count và residual blocker.

Mỗi task chỉ eligible khi matching grant có `task grant state=DISPATCHED` và `consumption state=UNCONSUMED`. Trước Shadow Plan, command, edit hoặc bất kỳ action nào, persist matching grant thành `RUNNING`/`CONSUMED` với consumer/consumption evidence. Grant missing, consumed, cross-feature, cross-task, cross-record, stale/mismatched consumer hoặc claim mismatch là `BLOCKED`; không reset/reuse grant.

Khi `--all` dừng vì sequential failure, Human gate, drift hoặc cancellation evidence, retire/revoke mọi selected grant chưa consumed và persist reason. Record/grant Markdown là cooperative evidence, không atomic cross-session lock.

## Direct và orchestrated execution

### Direct

Với `Agent Execution: direct`, `/add-execute` cấp consumer reference cho session hiện tại, persist record/grant rồi consume matching grant trước task action. Direct không bypass Shadow Plan, checkpoint, Action Record, exact command, validation, post-code review hoặc integration checks.

### Orchestrated

Với `Agent Execution: orchestrated`, `/add-execute` là coordinator. Sau observed `Agent` availability, cấp worker packet immutable cho từng task:

```text
EXECUTION ID: <id>
FEATURE: <feature-slug>
TASK ID: <T00X>
EXECUTION GRANT ID: <grant-id>
GRANT ATTEMPT: <n>
GRANT STATE: DISPATCHED
CONSUMPTION STATE: UNCONSUMED
CONSUMER: <execution-issued opaque consumer reference>
TASK: <ID, title, Intent/DoD and REQ references>
OWNED FILE BOUNDARY: <exact paths only>
FROZEN CONTRACT: <ID/version/owner or N/A>
PROFILE EVIDENCE: <approved binding/version>
ALLOWED COMMANDS: <exact approved commands only>
STATE-CHANGE CATEGORY: <none/categories>
CHECKPOINT: <review reference or N/A>
AUDIT EVIDENCE REFERENCE: <Execution Record/review/action evidence>
HOST EXECUTION-CLAIM EVIDENCE: <matching claim or UNVERIFIED>
PROHIBITIONS: no out-of-boundary edits, package/config/contract changes, self-approval, commit or push.
STOP CONDITIONS: drift, scope conflict, missing command/checkpoint, policy/security issue, retry ineligibility.
```

Worker phải đối chiếu packet với Execution Record trước consumption. Chỉ `parallel-owned` launch song song; `sequential-handoff`, shared work, retry và integration chạy theo thứ tự record. Worker trả Action-Record-compatible result, changed paths, command/result, requirement coverage, consumer/consumption evidence, blocker và sync-back decision. Coordinator xác minh boundary, contract compatibility, validation và integration trước complete.

## Quy trình mỗi task

1. Persist consume matching grant, rồi xuất Shadow Plan: Intent/DoD, scope/file boundary, profile evidence, exact command, state-change/checkpoint, contract/version, risk, trace/sync và post-code trigger.
2. Nếu task material state change hoặc dùng `--strict-checkpoint`, dừng trước edit đến khi checkpoint persisted `APPROVED` tồn tại.
3. Chỉ sửa trong boundary approved: domain không adapter/dependency; usecase có `@ears`; interface/infra/shared chỉ dùng adapter/config approved.
4. Chạy exact approved verification command hoặc ghi `N/A` cùng lý do hợp lệ. Không thay bằng command suy đoán.
5. Persist Action Record với grant/consumer/claim, changed boundary, command/result, validation route, residual blocker, sync-back và post-code review reference.
6. Theo trigger, route `/sdd-lint`, `/sdd-audit`, `/sdd-trace`, `/sdd-sync`, `/git-validate`; task chỉ `[x]` khi checkpoint, verification, post-code review và sync-back required đã đủ.
7. Dừng/handoff nếu scope expansion, Spec gap, profile/contract drift, material decision mới hoặc blocker xuất hiện.

## Retry, resume và escalation

- `--retry` chỉ dành cho named task `RETRY_PENDING` do implementation defect trong immutable task boundary, frozen contract, profile binding, exact command và checkpoint không đổi. Retire grant consumed rồi create grant ID/attempt mới; không reuse/reset grant cũ.
- `--resume` chỉ dành cho named interrupted `RUNNING`, resolved `BLOCKED` hoặc Human-dispositioned `ESCALATED` task, sau revalidation và close/retire stale execution evidence. Resume không phải retry.
- Spec/profile/command/checkpoint/contract/ownership/security/policy/dependency/runtime gap là `BLOCKED`, không retryable.
- Sau 5 consecutive implementation failures, giữ `[/]`, persist `ESCALATED` và review report, yêu cầu Human disposition explicit. `--all` không implicit retry hoặc resume.

## AI Recommendation và Human Final Review

Trước execution, lưu canonical recommendation với Intent/DoD, profile evidence, approach, file boundary, exact command, state-change category, checkpoint, risk và sync-back. Sau execution, refresh recommendation cùng Action Record, Execution Record và delivery/post-code review evidence. Agent không self-approve, complete ngoài evidence, commit hoặc push.

## Hướng dẫn sử dụng
- **Khi dùng:** Preflight và thực thi task đã approved; đây là public execution entry point duy nhất.
- **Không dùng:** Không truyền grant/consumer, ownership hoặc execution override; không dùng skill khác để thay execution.
- **Input:** Bắt buộc `--feature` và đúng một `--task` hoặc `--all`; tùy chọn `--retry`, `--resume`, `--strict-checkpoint`; reject flags ở Parameters.
- **Điều kiện trước:** Canonical governance, reviews, Feature Lock, TASKS review `APPROVED`, binding, exact command, checkpoint và contract owner phải resolve.
- **Evidence:** `TASKS.md` `Execution Record`, task grant/consumer, Shadow Plan, Action Record, command result và post-code/sync evidence.
- **Dừng khi:** Thiếu hoặc drift evidence, grant mismatch/consumed, worker unavailable, scope expansion, validation fail hoặc required checkpoint chưa `APPROVED`.
- **Human quyết định:** Human reviewer duyệt checkpoint/material scope; Agent không cấp lại grant, self-approve, commit hoặc push.
- **Lệnh tiếp theo:** Chỉ dùng `/add-execute --feature=<feature-slug> --task=<T00X>` hoặc Follow-up đã persist sau khi preflight pass; retry/resume phải đúng điều kiện riêng.
- **Ví dụ:** `/add-execute --feature=feat-orders --task=T003 --strict-checkpoint` cho một task có state change.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Tóm tắt selected task/snapshot, resolved execution mode/runtime evidence, Execution Record, grant/consumer consumption, Shadow Plan, changed boundary, Action Record, exact command/result, validation, post-code review và residual blocker. `continue` chỉ dùng `/add-execute --feature=<feature-slug> --all` cho feature snapshot mới khi prior selection completed và all preconditions được revalidated; retry/resume chỉ dùng command public với named task sau conditions tương ứng. Required checkpoint/review hoặc post-code evidence thiếu là `Human decision required`; Spec/profile/contract/command gap, worker unavailable cho orchestrated route, validation fail hoặc consumed/mismatched grant là `BLOCKED`. Không expose/reuse authority token, không tự retry, complete, commit hoặc push.
