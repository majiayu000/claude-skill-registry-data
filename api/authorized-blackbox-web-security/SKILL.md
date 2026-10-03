---
name: authorized-blackbox-web-security
description: Run user-authorized black-box web security tests and evidence-based reports. Use for 黑盒安全测试、渗透测试、数据泄露、未授权访问、公开 JS/API、登录爆破防护、CORS 或安全响应头检查。
---

# Authorized Black-Box Web Security

## Purpose

Use this skill to run a careful, user-authorized black-box security assessment from a public URL and produce a practical report. The default goal is to prove realistic data exposure or unauthorized modification risk without noisy traffic, broad enumeration, or harm to existing customer records.

This is for defensive work on assets the user owns or is authorized to test.

## Safety Boundary

Before testing, confirm the request is framed as authorized. If ownership or authorization is ambiguous, ask for confirmation before sending security probes.

Never perform:

- DDoS, stress testing, high-volume scanning, or load generation.
- Credential stuffing, real-password guessing, leaked credential testing, or broad brute force.
- Broad ID enumeration, scraping, or downloading sensitive datasets.
- Destructive changes to existing customer/user records.
- Persistence, malware, phishing, browser exploit chains, or bypassing third-party controls.

Allowed by default when authorized:

- Low-rate endpoint checks.
- Public asset and public JS analysis.
- Header/CORS checks.
- Login protection probes with nonexistent usernames, capped attempts, and delays.
- One clearly labeled probe record when a public submit path exists.
- Non-mutating write authorization checks that use invalid bodies or nonexistent IDs.

If the user explicitly allows destructive writes, still prefer a single uniquely named probe record and mutate only that probe. Revert it when the API allows and record the probe ID for cleanup.

## First Move

If a target URL and authorization are already clear, start testing immediately. If not, ask only for the missing minimum:

```text
请确认目标 URL、你是否授权测试，以及是否允许创建一个唯一标记的测试记录。
```

When the user specifies a black-box scope, do not use local repository code as report evidence. Local code may be used later only if the user asks for remediation or white-box follow-up.

## Evidence Workspace

Create a timestamped temp directory:

```bash
OUT="/tmp/blackbox-web-security-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT/assets" "$OUT/evidence"
```

Save response headers, bodies, extracted asset lists, and summarized JSON there. Avoid placing raw sensitive data in the final report.

Use safe variable names in zsh. Do not assign to `path`, because it can clobber command lookup.

## Recon Workflow

Start from the public entry URL only:

1. Fetch the HTML and response headers.
2. Extract script, CSS, modulepreload, and asset URLs.
3. Download business JS chunks with low concurrency or sequential curl.
4. Search public assets for:
   - API roots and domains.
   - Auth headers and token storage keys.
   - Hardcoded secrets, fallback tokens, default credentials.
   - Route lists and role-specific pages.
   - API paths, write methods, admin paths, upload/download endpoints.
   - Source map references.
5. Check common direct exposures at low volume:
   - Swagger/OpenAPI paths.
   - H2/admin consoles only if relevant to the stack or visible in assets.
   - Source maps for discovered JS bundles.
6. Check DNS/subdomain clues only lightly. Do not brute-force subdomains.

Useful commands:

```bash
curl -sS -D "$OUT/evidence/landing.headers" -o "$OUT/landing.html" "$TARGET"
rg -n "https?://|/api/|token|Authorization|X-.*Token|swagger|h2-console" "$OUT/assets" -S
```

## Validation Workflow

### Authentication And Authorization

For each sensitive endpoint discovered:

- Try no-auth once.
- Try discovered public/static token only if it was exposed by public assets.
- Record HTTP status, business code/message, data shape, count, and sample keys.
- Redact names, mobile numbers, emails, IDs, and personal/student/teacher details in reports.

Prefer summaries like:

```json
{"endpoint":"/api/admin/teachers","http_code":200,"code":"0","data_type":"array","count":1,"sample_keys":["id","username","status"]}
```

### Controlled Write Proof

Use this only when there is a safe public create path or the user explicitly allowed destructive testing.

Recommended path:

1. Create exactly one probe record through a public submit endpoint.
2. Include a unique marker such as `codex-security-probe-<timestamp>`.
3. Read only that probe through the suspected unauthorized admin path.
4. Change one harmless status field once, then revert.
5. Record probe ID, final state, and cleanup instructions.

If the create/list path fails, do not keep retrying. Report the failure and use a non-mutating write reachability check instead, such as:

- POST invalid body with exposed admin token and compare no-auth response.
- POST to a nonexistent ID and compare no-auth response.

If exposed token returns validation/business errors while no-auth returns unauthorized, that proves the request passed authorization without modifying data.

### Login Protection

Use nonexistent usernames only.

Default cap:

- Max 5 attempts per role/endpoint.
- Sleep at least 0.4-1.0 seconds between attempts.
- Record status code, response body, total time, and whether `429`, captcha, lockout, or delay escalation appears.

Do not use real accounts or guess passwords.

### CORS And Headers

Check:

- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Credentials`
- `Access-Control-Allow-Headers`
- Preflight behavior for sensitive custom headers.
- Whether disallowed origins can read responses in browsers.

Also check:

- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-Frame-Options` or CSP `frame-ancestors`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

Remember: CORS is not authentication. Curl/Postman/server-side attackers can still use leaked tokens even if browsers cannot read cross-origin responses.

### Role Boundary Checks

For teacher, parent, user, or legacy APIs:

- Check no-token behavior.
- Check role-specific token headers only if the token value is legitimately available from the black-box path.
- If legacy header-only access exists, use only IDs discovered from authorized/compromised views and do not brute-force IDs.

## Severity Defaults

- **Critical**: Public or static admin token accepted by backend; unauthenticated access to admin data; unauthorized write to privileged records.
- **High**: No effective login brute-force protections on admin/teacher/parent/user login; IDOR exposing student/user data; role boundary bypass.
- **Medium**: Health/debug endpoints leaking dependency status; CORS that enables browser-based data theft with credentials; sensitive metadata exposure.
- **Low**: Missing hardening headers, verbose errors, inconsistent auth status codes, non-exploitable route disclosure.

Calibrate severity by actual impact and whether the PoC reaches data or write paths.

## Report Format

Create a report file when working inside a repo, usually:

```text
docs/security/<project>-blackbox-security-report-<yyyy-mm-dd>.md
```

Use the user's language. Default structure:

```markdown
# <Project> 黑盒安全测试报告

测试时间：
入口范围：
测试方式：
流量边界：
证据目录：

## 执行摘要
## 攻击路径
## 发现 1：...
### 证据
### 影响
### 修复建议
## 受控写入验证结果
## 其他非发现项
## 优先修复清单
## 复测标准
```

Include exact PoC commands but redact sensitive output. Do not paste full datasets. Show enough to prove impact:

- HTTP status.
- Business code/message.
- Count.
- Redacted sample keys.
- Probe ID only if it is a test record.

Always include non-findings so future testers do not repeat the same checks.

## Final Response

Keep the closeout concise:

- Link to the report file.
- Name the top critical/high issues.
- State whether controlled writes succeeded, failed, or were skipped.
- Mention evidence directory.
- Mention any cleanup markers.

Do not claim destructive proof if only validation-error reachability was confirmed.
