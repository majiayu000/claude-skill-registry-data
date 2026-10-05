---
name: dengbao-code-audit
description: Scan source code, configuration, deployment files, and project documents from a China MLPS 2.0 Level 3 / 等保三级 code-security perspective. Use when auditing internal or public-facing software systems for authentication, authorization, audit logging, data security, interface security, transport security, exposed operations surfaces, backup/recovery, release-change evidence, and missing compliance materials, then producing a Markdown security findings report and remediation plan.
---

# Dengbao Code Audit

## Purpose

Use this skill to perform a source-level security audit for internal systems, especially systems that may be deployed on the public internet and need to prepare for 等保三级-style checks.

This skill does not replace formal MLPS/等保测评. It produces an engineering-focused code audit report with evidence, risk grading, and remediation guidance.

## Required Output

Save the final report as Markdown. Prefer:

```text
reports/等保代码安全检测报告.md
```

If a report path is requested by the user, use that path.

## Workflow

1. Identify the project root and scan scope.
   - Include source code, configs, deployment manifests, CI/CD files, scripts, README/docs, and environment templates.
   - Exclude dependency/vendor/build directories such as `node_modules`, `.git`, `dist`, `build`, `target`, `.venv`, `venv`, `coverage`.
   - If the system is public-facing, raise the risk level of auth, permission, data leakage, and exposed service findings.

2. Run the bundled inventory script when useful:

```bash
python3 <skill-dir>/scripts/inventory.py <project-root> --output <workdir>/dengbao-inventory.json
```

3. Run the bundled pattern scanner for first-pass evidence:

```bash
python3 <skill-dir>/scripts/grep_rules.py <project-root> --output <workdir>/dengbao-findings.json
```

4. Read the most relevant code paths instead of relying only on grep output.
   - Trace request entry points to auth middleware/guards/interceptors.
   - Check whether permission decisions happen on the backend, not only in frontend routes/buttons.
   - Check whether audit logs contain actor, IP, time, operation, object, result, and failure reason for important operations.
   - Check whether sensitive data is encrypted or desensitized at storage, transmission, logs, export, and backup boundaries.
   - Check deployment files for public ports, admin panels, debug flags, TLS, domain/certificate references, and database/cache exposure.

5. Create a draft report with the helper if desired:

```bash
python3 <skill-dir>/scripts/summarize_findings.py \
  --inventory <workdir>/dengbao-inventory.json \
  --findings <workdir>/dengbao-findings.json \
  --output <project-root>/reports/等保代码安全检测报告.md
```

6. Replace script-only conclusions with reviewed findings.
   - A regex hit is evidence, not proof.
   - If implementation cannot be confirmed from source, mark it as `待确认` and list the material needed.
   - Do not report secrets verbatim. Redact tokens, passwords, private keys, session IDs, and connection strings.

## What To Inspect

Load these references as needed:

- `references/checklist.md`: category-by-category audit checklist and evidence requirements.
- `references/severity-rubric.md`: risk grading rules and public-facing adjustment.
- `references/framework-patterns.md`: framework-specific code paths and common risky patterns.
- `references/remediation-playbook.md`: standard remediation guidance and acceptance criteria.
- `references/report-template.md`: final Markdown report structure.

## Finding Requirements

Each finding must include:

- Risk level: `高危`, `中危`, `低危`, or `待确认`.
- Category: one of 登录认证, 权限控制, 安全审计, 数据安全, 接口安全, 传输安全, 运维暴露面, 备份恢复, 发布变更, 文档材料.
- Evidence: file path and line number when available.
- Impact: what can go wrong in this system.
- Remediation: concrete code/config/process change.
- Acceptance criteria: how the team can verify the fix.

## Reporting Rules

- Lead with an executive summary and top risks.
- Group detailed findings by risk level, then by category.
- Include a coverage table for all 10 check categories, even if the conclusion is `待确认`.
- Include a prioritized remediation roadmap: 立即整改, 近期整改, 持续治理.
- Separate code-confirmed issues from documentation/process gaps.
- Be practical. Avoid vague statements like "strengthen security" without a testable action.

## High-Priority Red Flags

Always check carefully for:

- Public endpoints without backend authentication.
- Authorization enforced only by frontend menus/routes.
- Admin or privileged APIs without MFA or stronger controls.
- Hardcoded credentials, JWT secrets, access keys, database URLs, or private keys.
- SQL/NoSQL query concatenation with user-controlled input.
- Command execution, file path construction, template rendering, or SSRF using user input.
- File upload without extension, MIME, size, content, and storage path controls.
- Sensitive data in logs, exports, responses, localStorage, or backups.
- Open CORS, debug mode, permissive security headers, insecure cookies.
- Docker/Kubernetes/Nginx configs exposing SSH, database, Redis, MQ, admin consoles, or debug ports.
