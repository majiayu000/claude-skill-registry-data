---
name: sdd-layer-edit
description: Chỉnh sửa luồng nghiệp vụ xuyên Domain, Usecase, Interface và Infra theo Architecture Profile
user-invocable: true
---

# SDD Cross-Layer Proposal (`/sdd-layer-edit`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`), `@ears` references, file paths, and CLI commands are language-invariant.

Dùng để chuẩn bị bounded cross-layer change proposal xuyên Clean Architecture, giữ contract: interface gọi usecase; usecase phụ thuộc domain và port; infra triển khai port. Skill này **chỉ đề xuất, không tự thực thi**: nó không sửa `src/`, không cấp execution grant, không thay thế `/add-execute` và không phải shortcut để bỏ qua `TASKS.md`, Shadow Plan, Action Record hoặc material checkpoint.

## Khi nào dùng / không dùng

- **Dùng khi:** feature đã có `SPEC.md`, `PLAN.md`, `TASKS.md` và cần map bounded cross-layer change qua nhiều layer trước khi task được dispatch.
- **Không dùng khi:** cần sửa source ngay (route `/add-execute --feature=<slug> --task=<T00X>`), requirement/contract thay đổi (dùng `/sdd-update`), hoặc cần đổi governance (dùng `/sdd-agents-edit`, `/sdd-claude-edit` hoặc `/sdd-rfc`).

## Architecture Profile gate (BLOCKING)

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Đọc profile, constraint, feature `SPEC.md`, `PLAN.md`, `TASKS.md` và review block trước khi lập proposal.
- Domain/usecase có thể được plan bằng core-only TypeScript. Interface/infra chỉ được đề xuất adapter khi HTTP framework, validation, database hoặc ORM/query layer tương ứng đã selected, evidenced và `APPROVED`.
- Thiếu binding, exact test/build/lint command hoặc Human Final Review: dừng, lưu `PENDING HUMAN REVIEW`. Không sinh controller, repository, migration, DTO decorator, cache client hoặc command suy đoán.
- Xuất Shadow Plan gồm profile evidence, file scope, exact command và risk; proposal ở `PENDING HUMAN REVIEW` cho tới khi Human reviewer có thẩm quyền `APPROVED` execution scope.

## Tham số

- `--feature=<feature-slug>`: Feature chứa Spec tương ứng.
- `--action=<add|modify|refactor>`: Loại thay đổi.
- `--target=<name>`: Usecase hoặc Entity mục tiêu, ví dụ `CreateOrder`.

## Layer boundary

1. **Domain (`src/domain/`)**: Entity, Value Object hoặc Domain Event thuần TypeScript; không import third-party package hoặc adapter.
2. **Usecase (`src/usecase/`)**: Interactor/Application Service và port cho repository/external service; business method có `@ears .sdd/features/{slug}/SPEC.md#REQ-XXX`.
3. **Interface (`src/interface/`)**: Chỉ dùng transport, validation, authentication adapter đã approved; chỉ gọi usecase, không gọi DB/repository trực tiếp.
4. **Infra (`src/infra/`)**: Triển khai port bằng DB/cache/external client đã approved; cấm hardcode API key/password, raw `DELETE` không `WHERE` và thao tác trái safety constraint.

## AI Recommendation và Human Final Review

Skill này chỉ tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm requirement, boundary, file, risk, alternative và verification, lưu trong feature artifact/review với `Human Final Review.Status: PENDING`. Human reviewer có thẩm quyền `APPROVED` proposal và execution scope. Skill không tự sửa `src/`, không cấp grant và không tự approve; phần write chỉ chạy trong `/add-execute` với task grant hợp lệ, nơi Action Record được persist.

## Hướng dẫn sử dụng
- **Khi dùng:** Chuẩn bị bounded cross-layer proposal từ locked Spec/Plan/Tasks; không phải write path.
- **Không dùng:** Không dùng để independently execute or edit source, bypass TASKS/Shadow Plan, cấp grant, hoặc thay `/add-execute`.
- **Input:** `--feature`, `--action=add|modify|refactor`, `--target`; reject unapproved adapter/package/command and direct write requests.
- **Điều kiện trước:** Reviews, Feature Lock, profile bindings and exact command are readable; proposal recommendation remains `PENDING HUMAN REVIEW`.
- **Evidence:** Canonical recommendation, Shadow Plan, layer/file boundary, profile evidence, risk and exact verification proposal.
- **Dừng khi:** Missing binding/command/review, scope crosses locked boundary, contract owner absent, or material checkpoint is not approved.
- **Human quyết định:** Human approves proposal and task scope; actual writes happen only in `/add-execute` under a matching approved task grant.
- **Lệnh tiếp theo:** `/add-execute --feature=<feature-slug> --task=<T00X>` using the approved task and persisted Follow-up; never run layer-edit as executor.
- **Ví dụ:** `/sdd-layer-edit --feature=feat-orders --action=modify --target=CreateOrder` prepares proposal only.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Nêu requirement, layer/file boundary, profile binding, Shadow Plan, exact command, checkpoint/review state và proposed evidence; skill này không có changed-source evidence vì không ghi file. Kết quả là `Human decision required` cho review target đã persist, và `Lệnh tiếp theo` là `/add-execute --feature=<feature-slug> --task=<T00X>` sau approval. Binding/exact command/review thiếu là `BLOCKED`; không sinh controller, repository, migration, decorator, cache client hoặc command adapter-specific.
