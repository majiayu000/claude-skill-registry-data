---
name: sdd-audit
description: Kiểm định Constitution, Clean Architecture, EARS trace và binding theo Architecture Profile
user-invocable: true
---

# SDD Audit (`/sdd-audit`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`FAIL`, `WARNING`, `PASS`, `CONFIGURATION GAP`, `PENDING HUMAN REVIEW`, `APPROVED`), rule codes (`SEC-01`, `DATA-01`, `ARCH-01`, `ENG-01`), file paths, and CLI commands are language-invariant.

Dùng để kiểm định source và artifact theo `CONSTITUTION.md` trước commit hoặc Pull Request.

## Tham số

- `--feature=<feature-slug>`: Tùy chọn; giới hạn một feature. Không có thì audit toàn repository.

## Architecture Profile

Tuân thủ [Architecture Profile Protocol](../_shared/architecture-profile-protocol.md).

- Audit governance/layer boundary được phép với core-only baseline.
- Route, authentication middleware, ORM/SQL, queue, dependency scan và test command chỉ kiểm tra khi binding tương ứng đã approved/evidenced.
- Binding chưa chọn phải báo `CONFIGURATION GAP`, không kết luận `PASS`/`FAIL` dựa trên framework, SQL dialect, ORM method hay command suy đoán.

## Ba tầng audit

1. **Hard rule:** `SEC-01` secret/PII protection; `SEC-02` identity, authorization ownership và unauthorized behavior cho feature cần access control; `DATA-01` retention, recovery, authorization, audit và deletion policy khi feature đổi core business data.
2. **Architecture:** `ARCH-01` dependency direction và cấm direct DB access từ interface; `ARCH-02` kiểm tra async/reliability behavior theo Spec/profile.
3. **Engineering:** `ENG-01` EARS trace trong `src/usecase/`; `ENG-02` safe error contract theo transport đã approved; `ENG-03` exact approved verification command.

## Kết quả

- `FAIL`: Layer 1 violation hoặc blocker phải sửa.
- `WARNING`: Vấn đề Layer 2/3 cần remediation hoặc rationale approved.
- `PASS`: Check đã chạy và đạt.
- `CONFIGURATION GAP`: Chưa đủ binding/evidence để audit adapter-specific.

## AI Recommendation và Human Final Review

Sau audit, tạo canonical recommendation gồm finding, severity, evidence, remediation option và residual risk. Lưu trong feature artifact hoặc `.sdd/reviews/audit-<slug>.md` với `PENDING HUMAN REVIEW`. Human reviewer có thẩm quyền quyết định disposition; `Tech Lead` có thể review architecture khi repository giao thẩm quyền. Layer 1 failure và blocker còn mở vẫn block. Agent không tự approve audit.

## Hướng dẫn sử dụng
- **Khi dùng:** Read-only audit Constitution, architecture, EARS trace and approved binding evidence before delivery.
- **Không dùng:** Không dùng để self-remediate, edit source/artifact, claim `PASS` for unrun checks, or grant execution.
- **Input:** Optional `--feature`; reject framework-specific conclusions when binding is not approved.
- **Điều kiện trước:** Target repository/feature and profile are readable; adapter checks require matching approved binding and command.
- **Evidence:** Audit recommendation/report with finding severity, path/line evidence, `CONFIGURATION GAP` and residual risk.
- **Dừng khi:** Layer 1 violation, configuration gap, missing exact command, or unresolved finding requiring behavior/governance decision.
- **Human quyết định:** Human disposes findings; code remediation is proposed only and writes occur through approved `/add-execute` task.
- **Lệnh tiếp theo:** `/sdd-review --target=<audit-report> --status=<APPROVED|REVISE|REJECTED> ...`; use `/sdd-update` when a requirement must change.
- **Ví dụ:** `/sdd-audit --feature=feat-orders` produces findings without editing `src/`.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Nêu audit scope, profile/binding state, `PASS`/`WARNING`/`FAIL`/`CONFIGURATION GAP`, report path và residual risk. Kết quả chỉ `PASS` không có warning/finding mới vẫn là `Human decision required` khi recommendation audit còn `PENDING HUMAN REVIEW`; Human reviewer có thẩm quyền ghi decision, reviewer identity và Follow-up không phải placeholder bằng `/sdd-review --target=<feature artifact hoặc .sdd/reviews/audit-<slug>.md> --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. Chỉ follow-up đã persist mới chọn downstream route. Findings thay đổi behavior/governance/profile/contract là `Human decision required` với target review/update phù hợp; Layer 1 `FAIL` hoặc configuration gap là `BLOCKED`. Không claim `PASS` cho check chưa chạy và không tự remediation/bypass gate.
