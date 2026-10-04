---
name: sdd-plan
description: Pha 2 SDD — tạo PLAN.md theo Clean Architecture, Architecture Profile, data flow và risk
user-invocable: true
---

# SDD Phase 2 — Architecture Planning (`/sdd-plan`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`PENDING HUMAN REVIEW`, `PENDING`, `APPROVED`), file paths, and CLI commands are language-invariant.

Dùng `SPEC.md` và `CONSTITUTION.md` để tạo `.sdd/features/{feature-slug}/PLAN.md`.

## Tham số

- `--feature=<feature-slug>`: Feature identifier.

> **Sửa PLAN.md đã approved mà Spec không đổi?** Dùng `/sdd-update --artifact=plan --reason="..."`. `/sdd-plan` tạo Plan từ đầu từ Spec đã approved — dùng khi Plan chưa có hoặc Spec thay đổi lớn yêu cầu lập lại Plan.

## Shared methodology contract

Đọc [AI Review Protocol](../_shared/ai-review-protocol.md), `Intent Packet`, `Methodology Profile` và `Feature Lock` của feature. Plan chỉ triển khai locked scope, không đưa deferred work vào component/task. Kế thừa depth đã chọn từ Context/Spec; Plan không tự tăng hoặc hạ `SKIP | SKETCH | DETAILED | FORMAL`. High-risk route từ Spec phải có evidence `APPROVED` trước khi plan technical work thuộc route đó.

## Architecture Profile gate (BLOCKING)

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

1. Đọc profile, governance và repository evidence.
2. Chỉ dùng layout đã chọn: `domain/` → `usecase/` → `interface/` / `infra/` adapter.
3. Feature cần HTTP, persistence, validation, cache, async messaging hoặc runnable test/build command chưa `APPROVED` thì dừng; không sinh Plan adapter-specific.
4. Lưu `PENDING HUMAN REVIEW` recommendation nêu binding thiếu, evidence và exact follow-up.
5. Profile/evidence mâu thuẫn thì Human reviewer có thẩm quyền phải quyết định trước Plan.

## Các bước

1. Ghi Architecture Profile Reference, binding, evidence và command đã verified.
2. Ghi mapping `REQ-XXX` → component, data flow, ownership và file path theo Clean Architecture.
3. Vẽ data flow: Client → approved interface adapter → usecase → port → approved infra adapter → store/service; mỗi flow nêu `REQ-XXX` liên quan.
4. Ghi state-change category cho component/flow: `none`, shared/public contract, persistence schema/business-data mutation, permission/security/dependency/runtime configuration, external/irreversible side effect.
5. Ghi shared-contract impact: no impact hoặc contract ID/version, producer/consumer, owner, compatibility decision và sync-back owner.
6. Tạo `## Consistency Map`: requirement, Plan component, task expectation, exact verification command, test/trace evidence, `/sdd-sync` decision và post-code review trigger.
7. Dùng estimated effort chỉ để nhận diện task candidate quá lớn; estimate không tự cho phép dispatch, retry hoặc approval.
8. Đánh giá risk về security, concurrency, performance, migration và rollback.
9. Ghi **Questions for Human reviewer** — xem mục bên dưới.
10. Kiểm tra DoD và tạo recommendation.

## Questions for Human reviewer — bắt buộc trong PLAN.md

`PLAN.md` phải có section `## Questions for Human reviewer` liệt kê những điểm Spec còn mơ hồ mà planning phát hiện. Đây là giá trị cốt lõi của pha Plan: AI đọc Spec và báo cáo những gì nó phải assume để lập plan.

**Format từng câu hỏi:**

```markdown
### Q1: <Tên vấn đề ngắn gọn>
- **Điều chưa rõ**: <Spec nói gì (hoặc không nói gì) khiến plan phải assume>
- **Assumption hiện tại**: <Nếu không được clarify, plan sẽ dùng assumption này>
- **Ảnh hưởng nếu assumption sai**: <Component hoặc behavior nào bị thay đổi>
- **Câu hỏi cụ thể**: <Câu hỏi Yes/No hoặc cần giá trị cụ thể>
```

Nếu sau khi đọc Spec kỹ AI không có câu hỏi nào, phải **chủ động hỏi lại**: "Tôi đã assume những điều sau — chúng có đúng không?" rồi liệt kê assumption. Không có câu hỏi không có nghĩa Spec hoàn hảo; thường có nghĩa assumption ẩn chưa được surface.

## PLAN.md phải có

- **Architectural Approach** — pattern, design pattern, lý do chọn.
- **REQ-to-Component Mapping** — mọi `REQ-XXX` có component/data flow rõ ràng.
- **Components** — tên, trách nhiệm, interface, file path theo layer.
- **Data Flow** — user input → processing → storage → response, gắn `REQ-XXX`.
- **State-change classification** — category và checkpoint need cho từng flow có state change.
- **Shared-contract impact** — owner, compatibility, consumer và sync-back responsibility khi applicable.
- **Consistency Map** — requirement, Plan, expected task, exact command, trace/test/sync evidence và post-code review trigger.
- **Dependencies** — thứ tự implement, external dep.
- **Risks & Mitigations** — ít nhất 3 rủi ro kỹ thuật với mitigation.
- **Questions for Human reviewer** — xem trên.

## DoD

- [ ] Depth từ Methodology Profile được giữ nguyên; deferred scope không vào Plan.
- [ ] Boundary và dependency direction rõ ràng.
- [ ] Mỗi `REQ-XXX` có component, data flow hoặc disposition rõ ràng.
- [ ] Component có trách nhiệm, layer và path cụ thể.
- [ ] Data flow chỉ dùng approved adapter.
- [ ] State-change category và checkpoint requirement đã phân loại cho mọi flow/task candidate.
- [ ] Shared contract impact và compatibility/sync-back owner đã ghi khi applicable.
- [ ] Consistency Map liên kết requirement, Plan, expected task, exact command, trace/test/sync evidence và post-code review trigger.
- [ ] Có ít nhất ba risk và mitigation.
- [ ] Section "Questions for Human reviewer" có ít nhất 1 câu hỏi hoặc ghi rõ "Không có câu hỏi mở — assumption: [danh sách]".
- [ ] Technical question/assumption được nêu hoặc đã approved.

## AI Recommendation và Human Final Review

Sau khi tạo/sửa `PLAN.md`, lưu canonical recommendation gồm locked scope, inherited depth, architecture option, `REQ-XXX` mapping, dependency direction, state-change/checkpoint, shared-contract impact, risk, mitigation, decision kỹ thuật mở, delivery validation/post-code review trigger và requirement bị ảnh hưởng. Human review giữ `PENDING`; task decomposition/execution cần `APPROVED`. Agent phải dừng, không self-approve.

## Hướng dẫn sử dụng
- **Khi dùng:** Lập technical Plan từ locked Spec khi bindings and exact commands are resolved.
- **Không dùng:** Không dùng để plan deferred scope, invent adapters/commands, or execute tasks.
- **Input:** Bắt buộc `--feature`; reject unresolved HTTP/persistence/validation/test bindings and unapproved high-risk route.
- **Điều kiện trước:** Context/Spec reviews approved, Feature Lock active, Architecture Profile evidence and exact command approved.
- **Evidence:** `PLAN.md` mapping, data flow, consistency map, state-change/checkpoint, risks, questions and recommendation.
- **Dừng khi:** Missing/conflicting binding, unresolved Human question, deferred scope leakage, or required review absent.
- **Human quyết định:** Human approves architecture, risk and open assumptions; plan approval does not grant task execution.
- **Lệnh tiếp theo:** `/sdd-review --feature=<feature-slug> --artifact=plan --status=APPROVED ...`, then `/sdd-tasks --feature=<feature-slug>`.
- **Ví dụ:** `/sdd-plan --feature=feat-orders` stops rather than inventing a persistence adapter when DB binding is unresolved.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Plan hoàn chỉnh nhưng review `PENDING` chọn `Human decision required`; Human reviewer có thẩm quyền ghi decision, reviewer identity và Follow-up không phải placeholder bằng `/sdd-review --feature=<feature-slug> --artifact=plan --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. `continue` chỉ sau Plan `APPROVED`: `/sdd-tasks --feature=<feature-slug>`. Missing binding/exact command, conflicting evidence hoặc unresolved Human question là `BLOCKED`; nêu profile evidence và không sinh task adapter-specific.
