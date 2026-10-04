---
name: sdd-update
description: Cập nhật artifact SDD của feature (SPEC.md, CONTEXT.md, PLAN.md hoặc TASKS.md) sau khi đã approved — bump SemVer cho Spec, invalidate review cũ và chuẩn bị recommendation mới
user-invocable: true
---

# SDD Artifact Update (`/sdd-update`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `APPROVED`, `APPROVED & LOCKED`, `DRAFT`), EARS keywords, `REQ-XXX` identifiers, SemVer, file paths, and CLI commands are language-invariant.

Dùng khi cần sửa artifact SDD đã approved mà không sinh lại từ đầu. Skill này luôn invalidate review/downstream readiness bị ảnh hưởng; không cấp execution grant và không cho phép tiếp tục code trước review mới.

## Khi nào dùng skill này

| Tình huống | Lệnh đúng |
| :--- | :--- |
| `SPEC.md` đã `APPROVED & LOCKED`, cần sửa/thêm requirement | `/sdd-update --artifact=spec` |
| `CONTEXT.md` đã approved, stakeholder hoặc constraint thay đổi | `/sdd-update --artifact=context` |
| `PLAN.md` đã approved, cần sửa component/risk mà Spec không đổi | `/sdd-update --artifact=plan` |
| `TASKS.md` đã approved, cần thêm/sửa task mà Plan không đổi | `/sdd-update --artifact=tasks` |
| `SPEC.md` vẫn ở `DRAFT`, cần sửa trong lần đầu | `/sdd-spec` — không cần `/sdd-update` |
| Context thay đổi lớn, làm lại từ đầu | `/sdd-context` rồi `/sdd-spec` |
| Sửa xuyên nhiều artifact do breaking change | `/sdd-update --artifact=spec --bump=major` → review → rồi `/sdd-plan`, `/sdd-tasks` |

## Tham số

- `--feature=<feature-slug>`: Feature identifier. Bắt buộc.
- `--artifact=<spec|context|plan|tasks>`: Artifact cần cập nhật. Mặc định: `spec`.
- `--bump=<patch|minor|major>`: Loại thay đổi SemVer. Bắt buộc khi `--artifact=spec`.
- `--reason=<mô-tả>`: Lý do cập nhật. Bắt buộc. Khuyến khích gắn REQ-XXX khi áp dụng, ví dụ `"[REQ-003] Add OTP rate-limit: max 5 attempts per 10 minutes"`.

## Chọn bump đúng (chỉ áp dụng cho `--artifact=spec`)

| Loại thay đổi | Bump |
| :--- | :--- |
| Làm rõ behavior đã có, thêm error case, clarify edge case không phá contract | `patch` |
| Thêm behavior tương thích ngược, thêm optional flow hoặc NFR mới | `minor` |
| Thay đổi API, DB schema, data contract hoặc behavior không tương thích ngược | `major` |

`--bump=major` bắt buộc phải ghi migration plan, rollback plan và risk trong Spec trước khi Agent được execute downstream.

## Shared methodology contract

Đọc [AI Review Protocol](../_shared/ai-review-protocol.md). Mọi update phải thêm `## Change Impact Record` trước recommendation:

```markdown
## Change Impact Record
- Changed intent, requirement, architecture, or task assumption: <what changed>
- Feature Lock boundary affected: <locked scope/deferred work/no change>
- Material state-change classification: <none or category list>
- Downstream artifacts invalidated: <Context/Spec/Plan/Tasks/code/tests/contracts>
- Required trace, test, and sync actions: </sdd-trace, exact command, /sdd-sync or N/A>
- Review follow-up: <review route and approval required>
```

Không dùng Context-only update để che behavior change. Nếu Context thay đổi intent, actor, boundary, constraint hoặc risk, record phải quyết định rõ `Spec revision required: yes | no` và evidence. Spec update phải đánh giá Plan/Tasks trước resume.

## Architecture Profile preflight

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Đọc profile và governance trước khi sửa artifact.
- Requirement bổ sung phải technology-neutral; không sinh ORM decorator, HTTP route, framework schema hoặc command chưa approved.
- Binding chưa resolve vẫn được phép trong Spec nhưng phải là `PLAN.md` planning blocker.

## Clarification-First — bắt buộc trước khi thêm requirement hoặc sửa behavior

Trước khi viết thay đổi, liệt kê điểm chưa chắc chắn theo 3 loại:

1. **Business logic gaps** — Rule mới/sửa có assumption nào chưa được xác nhận?
2. **Constraint kỹ thuật** — NFR thêm vào có giá trị đo được chưa? (timeout, rate limit, threshold)
3. **Edge case chưa xử lý** — Thay đổi này ảnh hưởng tình huống nào đang có trong Spec?

Dừng và chờ Human reviewer có thẩm quyền confirm trước khi ghi thay đổi. Nếu được phép tiếp tục với assumption, ghi rõ assumption đó trong artifact.

## Quy trình

### Khi `--artifact=spec`

1. Đọc `SPEC.md` hiện tại, `CONTEXT.md`, `CONSTITUTION.md`, Architecture Profile, Plan và Tasks nếu tồn tại.
2. Chạy Clarification-First; chờ confirm.
3. Đặt header Spec về `Status: DRAFT` nếu đang ở `APPROVED & LOCKED`.
4. Thêm/sửa requirement theo EARS; cập nhật BDD, error behavior, acceptance, Out of Scope và Feature Lock liên quan.
5. Bump version theo SemVer và ghi changelog entry.
6. Đánh giá Plan/Tasks, `@ears` trong `src/`, tests và shared contract bị invalidated trước khi cho phép resume.
7. Ghi Change Impact Record, invalidate recommendation cũ và tạo recommendation mới.

### Khi `--artifact=context`

1. Đọc `CONTEXT.md` hiện tại và `SPEC.md` để hiểu phạm vi đang lock.
2. Chạy Clarification-First cho thay đổi context.
3. Cập nhật Intent Packet, stakeholder, constraint, glossary hoặc open question bị ảnh hưởng.
4. Nếu intent, actor, boundary, constraint hoặc risk thay đổi, ghi rõ `Spec revision required: yes | no` và evidence trong Change Impact Record. Nếu `yes`, dừng để `/sdd-update --artifact=spec` trước downstream execution.
5. Ghi Change Impact Record, invalidate recommendation cũ và tạo recommendation mới.

### Khi `--artifact=plan`

1. Đọc `PLAN.md` hiện tại, `SPEC.md` `APPROVED & LOCKED` và Architecture Profile.
2. Chạy Clarification-First cho thay đổi plan.
3. Cập nhật component, data flow, state-change classification, consistency map, contract impact hoặc risk bị ảnh hưởng.
4. Xác định task trong `TASKS.md` bị invalidated; ghi trace/test/sync follow-up.
5. Ghi Change Impact Record, invalidate recommendation cũ và tạo recommendation mới.

### Khi `--artifact=tasks`

1. Đọc `TASKS.md` hiện tại, `PLAN.md` `APPROVED` và `SPEC.md` `APPROVED & LOCKED`.
2. Chạy Clarification-First cho task mới/sửa.
3. Thêm/sửa task: atomic, independent hoặc có `blockedBy`, exact verification command, scope category, checkpoint và sync-back responsibility.
4. Xác định task nào cần invalidate; cập nhật dependency và contract owner nếu cần.
5. Ghi Change Impact Record, invalidate recommendation cũ và tạo recommendation mới.

## DoD

- [ ] Clarification-First đã chạy; assumption được ghi hoặc Human đã confirm.
- [ ] Change Impact Record nêu changed assumption, Feature Lock boundary, material state-change, invalidated downstream artifacts, trace/test/sync và review follow-up.
- [ ] Context change về intent/actor/boundary/constraint/risk quyết định rõ Spec revision required.
- [ ] Spec change đánh giá Plan/Tasks trước resume; requirement mới/sửa dùng EARS và SemVer đúng loại.
- [ ] Plan/Tasks change giữ profile binding, exact command, state-change checkpoint và sync-back responsibility.
- [ ] Recommendation mới ở `PENDING HUMAN REVIEW`; downstream execution dừng đến khi Human approve.

## AI Recommendation và Human Final Review

Sau khi cập nhật artifact, tạo canonical recommendation từ `.claude/skills/_shared/ai-review-protocol.md`, gồm Change Impact Record, invalidated scope, review route và exact next command. Giữ `Human Final Review.Status: PENDING`; downstream execution bị block đến khi Human reviewer có thẩm quyền ghi `APPROVED`. Agent không tự approve artifact đã sửa.

## Ví dụ

```text
/sdd-update --feature=feat-user-register --artifact=spec --bump=patch --reason="[REQ-003] Add OTP rate-limit: max 5 attempts per 10 minutes"
/sdd-update --feature=feat-user-register --artifact=context --reason="Add compliance team as stakeholder; add GDPR constraint"
/sdd-update --feature=feat-user-register --artifact=plan --reason="Add Redis session risk and mitigation after security review"
/sdd-update --feature=feat-user-register --artifact=tasks --reason="Add T009 for concurrent registration dedup check"
```

## Hướng dẫn sử dụng
- **Khi dùng:** Cập nhật một approved Context/Spec/Plan/Tasks artifact with explicit impact and review reset.
- **Không dùng:** Không dùng để che behavior change, resume execution, issue grants, or bypass Clarification-First.
- **Input:** `--feature`, `--artifact`, `--reason`; `--bump` required for Spec; reject technology guesses and missing reason.
- **Điều kiện trước:** Existing artifact, downstream artifacts, profile and governance are readable; changed scope is recorded before edit.
- **Evidence:** `Change Impact Record`, invalidated downstream state, new recommendation `PENDING HUMAN REVIEW` and review target.
- **Dừng khi:** Unresolved clarification, breaking change without migration/rollback, profile gap, or downstream impact cannot be bounded.
- **Human quyết định:** Human approves revised artifact; Agent does not resume code or execution until fresh review.
- **Lệnh tiếp theo:** `/sdd-review --feature=<feature-slug> --artifact=<context|spec|plan|tasks> --status=APPROVED ...`, then use the persisted Follow-up.
- **Ví dụ:** `/sdd-update --feature=feat-orders --artifact=spec --bump=patch --reason="Clarify duplicate order error"`.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Tóm tắt `Change Impact Record`, artifact/task/code/test/contract invalidated và review target. Update xong luôn là `Human decision required`; Human reviewer có thẩm quyền ghi decision, reviewer identity và Follow-up không phải placeholder bằng `/sdd-review --feature=<feature-slug> --artifact=<context|spec|plan|tasks> --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. Chỉ sau review mới chọn command downstream mà Follow-up đã persist. Clarification, profile gap hoặc breaking impact chưa có migration/rollback là `BLOCKED`; không resume task hoặc execution.
