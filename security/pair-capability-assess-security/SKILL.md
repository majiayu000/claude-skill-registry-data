---
name: pair-capability-assess-security
description: "Assess security posture using resolution cascade (Argument > Adoption > Assessment). Reads security guidelines and package-level .pair.security.md files, identifies gaps, proposes controls, writes adoption file, composes /pair-capability-record-decision. Idempotent."
version: 0.1.0
author: Learnn
---

# /pair-capability-assess-security — Security Assessment

Evaluate and document the project security posture. Follows the resolution cascade: explicit argument wins, then existing adoption, then full assessment from guidelines. Reads package-level `.pair.security.md` files to avoid duplicating rules already defined in submodules.

## Arguments

| Argument  | Required | Description                                                                                        |
| --------- | -------- | -------------------------------------------------------------------------------------------------- |
| `$scope`  | No       | Limit assessment to one package: `web`, `mobile`, `services`. Omit for full project assessment.    |
| `$choice` | No       | Override: skip assessment and adopt a specific security control set directly (e.g. `owasp-top10`). |

## Composed Skills

| Skill                              | Type       | Required                               |
| ---------------------------------- | ---------- | -------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records security strategy as ADL |

## Adoption Files

- **Primary target**: [adoption/tech/security.md](../../../.pair/adoption/tech/security.md) — global security principles and WordPress-specific rules
- **Package targets** (read + write): `.pair.security.md` files in `apps/web/.pair/`, `apps/mobile/.pair/`, `services/.pair/`
- **Ownership**: Global principles section (shared file — package-specific rules live in submodule files)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm with developer:

   > Security control override: **$choice**.
   > This will be adopted without full assessment.
   > Confirm?

4. **Check**: Does [adoption/tech/security.md](../../../.pair/adoption/tech/security.md) already exist with different controls?
   - If yes, warn: "Current security adoption exists. Override to **$choice**?"
5. **Verify**: Developer confirms. Proceed to Step 4.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/security.md](../../../.pair/adoption/tech/security.md) exist and is it populated (not template)?
2. **Skip**: If missing or empty, go to Path C.
3. **Act**: Read current adoption. Read all package `.pair.security.md` files present. Present:

   > Security adoption already exists.
   > Global principles: **[list]**
   > Package files found: **[web | mobile | services]**
   > Open vulnerabilities tracked: **[count from package files]**

4. **Check**: Does a corresponding decision record exist? (Scan [adoption/decision-log/](../../../.pair/adoption/decision-log) for `*security*` files.)
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Adoption and decision record consistent. Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2 (full assessment mode).

### Step 2: Read Guidelines

1. **Act**: Read security guidelines:
   - [Security README](../../../.pair/knowledge/guidelines/quality-assurance/security/README.md) — framework overview, tool matrix, severity classification
   - [Security Guidelines](../../../.pair/knowledge/guidelines/quality-assurance/security/security-guidelines.md) — OWASP-based standards
   - [Security by Design](../../../.pair/knowledge/guidelines/quality-assurance/security/security-by-design.md) — design principles
   - [Authentication & Authorization](../../../.pair/knowledge/guidelines/quality-assurance/security/authentication-authorization.md) — identity controls
   - [Vulnerability Prevention](../../../.pair/knowledge/guidelines/quality-assurance/security/vulnerability-prevention.md) — proactive controls
   - [Sensitive Data](../../../.pair/knowledge/guidelines/quality-assurance/security/sensitive-data.md) — data handling rules
   - [API Security](../../../.pair/knowledge/guidelines/quality-assurance/security/api-security.md) — API-specific controls
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — project type, scale, compliance requirements (if available)
   - [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — platforms and languages (determines which controls apply)
   - All existing `.pair.security.md` files — rules already documented per package
3. **Verify**: Guidelines and project context loaded.

### Step 3: Assess Security Posture

1. **Act**: If `$scope` is provided, assess only that package. Otherwise assess all packages present.

2. **Act**: For each package in scope, evaluate against OWASP Top 10 categories:
   - A01 Broken Access Control
   - A02 Cryptographic Failures
   - A03 Injection
   - A04 Insecure Design
   - A05 Security Misconfiguration
   - A06 Vulnerable and Outdated Components
   - A07 Identification and Authentication Failures
   - A08 Software and Data Integrity Failures
   - A09 Security Logging and Monitoring Failures
   - A10 Server-Side Request Forgery

3. **Act**: Assign severity to each gap found (P0 Critical / P1 High / P2 Medium / P3 Low) using the classification in the security README.

4. **Act**: Check which package `.pair.security.md` files already exist:
   - If a file exists, read it and treat documented rules as already addressed — do NOT duplicate them in the global adoption file.
   - If a file is missing for a package with code, flag it as a gap.

5. **Act**: Present findings summary to developer:

   > **Security Assessment Summary — [scope]**
   >
   > OWASP Coverage:
   >
   > - A01 Access Control: [OK | gaps found]
   > - A02 Cryptographic Failures: [OK | gaps found]
   > - ... (all 10 categories)
   >
   > Open vulnerabilities by severity:
   >
   > - P0 Critical: N
   > - P1 High: N
   > - P2 Medium: N
   >
   > Missing package security files: [list]
   >
   > Recommendation: [summary of controls to adopt]

6. **Verify**: Developer approves the assessment and proposed controls.

### Step 4: Write Adoption Files

1. **Act**: Update [adoption/tech/security.md](../../../.pair/adoption/tech/security.md):
   - Write or update **Security Principles** section with approved global controls.
   - Write or update **WordPress-Specific** section if WordPress is in scope.
   - Do NOT write package-specific rules — those belong in `.pair.security.md` submodule files.
   - Preserve existing content in sections not touched by this assessment.

2. **Act**: For each package missing a `.pair.security.md` file:
   - Create the file at `apps/<package>/.pair/.pair.security.md` (or `services/.pair/.pair.security.md`).
   - Follow the structure of existing package files (open vulnerabilities + security rules + exceptions + what's done correctly + references).
   - Add the new file reference to the **Security Review Process** section of `adoption/tech/security.md`.

3. **Verify**: All adoption files written and consistent. No rule is duplicated between global and package files.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `security-strategy`
   - `$summary`: "Security posture assessed for [scope]: [N] controls adopted, [N] open vulnerabilities tracked"
2. **Verify**: ADL created at `adoption/decision-log/YYYY-MM-DD-security-strategy.md`. Adoption file consistent with ADL.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:     Security
├── Scope:      [full | web | mobile | services]
├── Path:       [Argument Override | Adoption Exists | Full Assessment]
├── OWASP:      [N/10 categories covered]
├── Open vulns: [P0: N | P1: N | P2: N | P3: N]
├── Adoption:   [adoption/tech/security.md — written | confirmed | updated]
├── Pkg files:  [list of .pair.security.md files created or confirmed]
├── Record:     [ADL path — created | exists | backfilled]
└── Status:     [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: `/pair-process-review` invokes `/pair-capability-assess-security` during the adoption compliance phase. May pass `$scope` to limit assessment to the package touched by the PR.
- **Output**: Returns security findings relevant to the PR — open vulnerabilities, missing controls, OWASP gaps. `/pair-process-review` includes these findings in the review report.
- ADL is NOT written during review — adoption changes require explicit developer approval outside the review flow.

When invoked **independently**:

- Full interactive flow. Developer commits changes when satisfied.

## Edge Cases

- **Package `.pair.security.md` exists but is outdated** (references fixed vulnerabilities): Prompt developer to confirm which items are resolved before updating.
- **Argument conflicts with adoption**: Warn developer, ask for confirmation. If confirmed, update adoption and create new decision record.
- **No PRD available**: Proceed with assessment. Warn: "No PRD found — compliance requirements (GDPR, PCI-DSS) must be confirmed manually."
- **Package code exists but no `.pair.security.md`**: Create the file. Warn: "No security file found for [package] — creating from assessment findings."
- **Decision record already exists for same scope+decision**: Skip writing (no duplicates).
- **All packages already have `.pair.security.md` and global adoption exists**: Path B (adoption exists) — confirm and exit.

## Graceful Degradation

- If security guidelines are not found, use OWASP Top 10 as minimal framework and ask developer to confirm which categories are in scope.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording: "Decision not recorded — /pair-capability-record-decision not installed."
- If adoption directory doesn't exist, create it on first write.
- If a package `.pair.security.md` exists but is empty/template, treat as missing (Path C).

## Notes

- **Global vs package rules**: Global `adoption/tech/security.md` owns cross-cutting principles. Package `.pair.security.md` files own implementation-specific rules and open vulnerabilities. Never duplicate a rule in both.
- **Security decisions are non-architectural** → produce ADL (not ADR), unless the security choice structurally affects the system (e.g. adopting a zero-trust mesh that changes service boundaries).
- **Idempotency**: the resolution cascade IS the idempotency mechanism. If adoption exists and is consistent with package files, assessment is already done.
- **Open vulnerabilities**: tracked in package `.pair.security.md` files under `## Open Vulnerabilities`. Once a vulnerability is fixed and a PBI closed, remove it from the file.
- Educational content (OWASP descriptions, threat models, WHY) stays in guidelines. This skill references guidelines for assessment criteria and control recommendations.
