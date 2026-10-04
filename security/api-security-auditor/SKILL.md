---
name: api-security-auditor
description: Audit API theo OWASP, Clean Architecture và Architecture Profile
user-invocable: true
---

# API Security Auditor (`/api-security-auditor`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Canonical tokens (`CRITICAL`, `HIGH`, `CONFIGURATION GAP`, `PASSED`, `APPROVED`, `PENDING HUMAN REVIEW`), OWASP codes, file paths, and CLI commands are language-invariant.

Audit API theo OWASP, `CONSTITUTION.md` và Clean Architecture.

## Tham số

- `--file=<path>`: HTTP boundary/controller/adapter cần audit.
- `--feature=<slug>`: Audit toàn feature.
- `--owasp=<A01..A10>`: Chỉ audit một OWASP category.

## Architecture Profile gate

1. Đọc Architecture Profile, governance và evidence liên quan.
2. Core-only check được phép: authorization ownership trong `usecase/`, domain invariant, PII masking, typed error và cấm `interface/` truy cập DB trực tiếp.
3. HTTP middleware, route/config, validation schema, authentication package, DB/ORM remediation, dependency scan command và framework-specific test chỉ dùng khi profile có binding `APPROVED` và evidence.
4. Binding thiếu thì báo `CONFIGURATION GAP`; không sinh import, package name, SQL dialect, ORM API, config file hoặc command suy đoán.

## OWASP checklist theo Clean Architecture

- **A01 Broken Access Control:** Ownership/tenant/role check nằm trong usecase theo `SPEC.md`; interface chỉ chuyển identity đã xác thực.
- **A02 Cryptographic Failures:** Không hardcode/log secret; crypto, token, TLS, key rotation chỉ dùng mechanism approved; mask PII.
- **A03 Injection:** Validate input tại interface boundary; parameterize persistence call trong `src/infra/`; không dùng untrusted interpolation.
- **A04 Insecure Design:** Domain invariant, state transition, idempotency và rate limit khớp EARS/Spec.
- **A05 Security Misconfiguration:** Chỉ audit header, CORS, body limit, debug bypass, TLS/trust proxy sau HTTP binding.
- **A06 Vulnerable Components:** Chỉ chạy exact dependency/security scan command đã approved/evidenced.
- **A07 Authentication Failures:** Signature, expiry, claim, revocation, reset/MFA và brute-force behavior theo Spec/profile.
- **A08 Integrity Failures:** Verify webhook/external payload integrity; validate external data tại boundary; cấm dynamic code execution.
- **A09 Logging Failures:** Security event có correlation, PII masking và logger adapter approved.
- **A10 SSRF:** Validate external URL/protocol/destination theo policy; timeout/redirect/DNS policy dùng client adapter selected.

## Output

```text
API SECURITY AUDIT REPORT
Feature: {slug} | Profile: v{version}

CRITICAL:
  [A01|A03|SEC-01|SEC-02] {path}:{line} — {verified finding and evidence}
HIGH:
  [A02|A04-A10] {path}:{line} — {finding}
CONFIGURATION GAP:
  {missing binding; adapter-specific remediation omitted}
PASSED:
  {verified profile-compatible control}
REMEDIATION:
  - Binding: {approved binding or human decision required}
  - Change: {profile-compatible action}
  - Verification: {exact approved command or N/A with reason}
  - Spec/Plan impact: {artifact or N/A}
```

Nếu finding đổi business behavior, cập nhật `SPEC.md` trước code. Governance change cần RFC. Binding gap phải lưu `PENDING HUMAN REVIEW`; không remediation framework-specific.

## Hướng dẫn sử dụng
- **Khi dùng:** Đọc-only audit API boundary hoặc toàn feature theo OWASP và profile evidence.
- **Không dùng:** Không dùng để tự sửa source, chọn package/framework, chạy scan chưa approved hoặc cấp execution authority.
- **Input:** `--file` hoặc `--feature`; tùy chọn `--owasp`; reject secret values, guessed bindings và write request.
- **Điều kiện trước:** Target tồn tại; Architecture Profile, Spec và governance đã đọc; binding adapter-specific phải `APPROVED` để kết luận tương ứng.
- **Evidence:** `API SECURITY AUDIT REPORT`, path/line finding, profile version, exact approved command/result hoặc `N/A` reason, recommendation pending.
- **Dừng khi:** Binding thiếu/conflict, target ngoài boundary, unresolved critical/high finding hoặc behavior change chưa có Spec decision.
- **Human quyết định:** Human phân loại finding và duyệt behavior/profile change; remediation chỉ thành action qua `/add-execute` task đã approved.
- **Lệnh tiếp theo:** `/sdd-update --feature=<slug> --artifact=spec --bump=<patch|minor|major> --reason="..."` khi finding đổi behavior; nếu không, theo Follow-up đã persist.
- **Ví dụ:** `/api-security-auditor --file=src/interface/http/orders.ts --owasp=A01` chỉ tạo proposal audit, không sửa file.

## Completion output

Dùng [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract) sau `API SECURITY AUDIT REPORT`. Nêu audit scope/profile, severity/finding evidence, recommendation/report path, exact verification result và residual risk. Kết quả không có finding/blocker mới chọn `continue` với action không-command: giữ audit evidence và chỉ theo persisted feature/delivery Follow-up hiện có; không tự suy ra route mới. Business behavior change là `Human decision required` để update/review Spec; governance change route qua RFC; `CONFIGURATION GAP` hoặc unresolved `CRITICAL`/`HIGH` là `BLOCKED`. Không generate framework/package/scan command chưa approved và không tự apply remediation.
