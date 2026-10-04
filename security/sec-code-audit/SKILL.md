---
name: sec-code-audit
version: 1.0.0
description: Perform a defensive, security-focused code audit covering injection, authorization, secrets, unsafe deserialization, and crypto.
author: matrixx0070
tags: [security, code-audit, appsec, injection, authorization, defensive]
capabilities: []
---

## When to use

Use this before merging security-sensitive changes, when reviewing untrusted or legacy code, or during a scheduled appsec pass. The goal is to find defensive weaknesses and recommend fixes.

**Not for:** writing working exploits or PoCs; scanning dependencies for CVEs (use `sec-dependency-audit`); or architecture-level risk enumeration (use `sec-threat-model`). Review the code you can read — do not attack a running system.

## Method

1. **Map inputs and sinks.** Trace where external data enters (requests, files, env, messages) and where it reaches dangerous sinks (SQL, shell, eval, file paths, HTML, deserializers, template engines).
2. **Injection.** Confirm parameterized queries, escaped output, allow-listed commands, and safe path joins. *Decision point:* any string-concatenated query, shell call, or dynamic template is a finding until proven safe.
3. **AuthN/AuthZ.** Verify every privileged action checks identity AND permission server-side. Hunt for missing checks, IDOR (object references without ownership checks), and client-trusted roles.
4. **Secrets.** Look for hardcoded keys, tokens, passwords, and any secret written to logs or returned to clients. Confirm secrets load from config or a vault.
5. **Deserialization & parsing.** Flag unsafe deserialization (pickle, native serialize, YAML unsafe load), XXE-prone XML parsers, and prototype pollution.
6. **Crypto & sessions.** *Decision point:* if you see a hand-rolled cipher, MD5/SHA1 for passwords, or a predictable token, escalate to Critical and stop to confirm blast radius before continuing.

## Example

In `getInvoice(req)` you find `db.query("SELECT * FROM invoices WHERE id=" + req.params.id)`. Finding: **SQL injection**, Critical, `invoice.js:42`, category Injection. Fix: use a parameterized query — `db.query("SELECT * FROM invoices WHERE id=?", [req.params.id])`. Also note the missing ownership check (IDOR) — any user can read any invoice id.

## Pitfalls

- **Grepping for `eval` and stopping.** Real injection hides behind wrappers and helpers; follow the data, not the keyword.
- **Reporting without a fix.** A finding with no concrete remediation gets ignored. Always include the corrected pattern.
- **Trusting framework defaults blindly.** ORMs and templates have raw-query and raw-HTML escape hatches; check whether they are used.
- **Severity inflation.** Marking everything Critical trains reviewers to ignore you. Rank honestly by impact and reachability.

## Output format

```
## Summary
Files reviewed: <list>. Overall risk posture: <sentence>.

## Findings
| Severity | File:line | Category | Description | Recommended fix |
|----------|-----------|----------|-------------|-----------------|

## Quick wins
- <low-effort, high-value fix>

## Follow-ups
- <needs design change or owner decision>
```
