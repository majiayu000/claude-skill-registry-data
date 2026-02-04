---
name: security-review
description: Thorough, adversarial security review of API endpoints, UI flows that call those endpoints, and any database-interacting code. Use when the user asks for a security review, permission/authorization audit, red-team style assessment, or vulnerability analysis. Assume access to source code and a running system; perform threat modeling and check current vulnerabilities relevant to the stack.
---

# Security Review

## Overview

Perform a red-team style review of API endpoints, the UI flows that call them, permission boundaries, and database interactions. Produce prioritized findings with concrete exploit paths and fixes.

## Workflow Decision Tree

1. **Confirm scope**
   - If the user names specific endpoints/features, proceed. Otherwise ask for the feature list, roles, environments, and access level.
   - If the system is running and reachable, do both static review and dynamic tests. If not, do static-only and flag verification gaps.

2. **Inventory & mapping (static first)**
   - Enumerate API endpoints, handlers, auth middleware, and data access points.
   - Map UI flows to endpoints and identify where permissions should be enforced server-side.
   - Identify database tables and relationships accessed by the feature; use MCP DB tools to understand schema and permission boundaries.

3. **Threat model the feature**
   - Use STRIDE for endpoints and data flows; use LINDDUN for privacy risks; align with OWASP ASVS / OWASP API Security Top 10 categories.
   - Identify trust boundaries, entry points, assets, and abuse cases.

4. **Deep-dive reviews**
   - Authorization and permission gaps (vertical + horizontal)
   - Input validation and injection exposure
   - Session, token, and credential handling
   - Data access and tenancy isolation
   - Abuse protections (rate limits, replay, enumeration, business logic)

5. **Dynamic testing (when running system is available)**
   - Attempt privilege escalation, IDOR, forced browsing, parameter tampering, and workflow bypasses.
   - Validate server-side enforcement vs. client-side checks.

6. **Vulnerability intelligence**
   - Identify framework/runtime versions and key dependencies.
   - Use WebSearch + WebFetch to confirm the latest vulnerabilities (CVEs/advisories) relevant to those components; cite sources.

7. **Deliverable**
   - Provide a structured report with findings, evidence, exploit paths, fixes, and verification steps.

## Required Tools and Data Sources

- **Codebase search**: use `rg` to find endpoints, auth checks, role gates, and DB access.
- **Running system**: use available API/UI access to validate real-world enforcement.
- **Database schema**: use MCP `dbhub` and `dbhub-crm` to understand tables, relationships, and likely access boundaries.
- **Vulnerability intel**: use WebSearch/WebFetch to verify current, authoritative advisories.

## Core Review Steps

### 1) Scope and Inventory

- List endpoints, handlers, and related UI flows.
- Identify roles/permissions expected for each operation.
- Enumerate data assets involved (PII, financial, operational data) and identify where they live in DB.

### 2) Authorization & Permission Audit

- Confirm **server-side** authorization for every sensitive action.
- Test for IDOR and horizontal access (e.g., `customer_id`, `account_id` swaps).
- Test vertical escalation (low-priv user accessing admin endpoints).
- Verify permission checks near data access (before queries, not just in UI).

### 3) Data Access and DB Boundaries

- Trace requests to DB queries and ensure least-privilege access.
- Look for direct SQL execution, weak row filtering, or missing tenant scoping.
- Use MCP schemas to identify related tables that should be constrained by permissions.

### 4) Input Validation & Injection Surface

- Check for SQLi, command injection, SSRF, path traversal, and deserialization issues.
- Validate JSON schema / parameter validation at boundaries.
- Verify output encoding for any reflected data.

### 5) Authn/Session/Secrets

- Review token handling, session fixation, CSRF exposure for state-changing operations.
- Validate logout/invalidation and token rotation.
- Scan for hardcoded secrets, weak key storage, or overly broad API keys.

### 6) Abuse & Business Logic

- Test rate limits, brute-force protections, and enumeration controls.
- Attempt workflow bypasses and state manipulation.
- Check audit logging for sensitive changes and access.

## Reporting Guidance

- Provide a ranked list of findings (Critical/High/Medium/Low/Info).
- Each finding should include:
  - **Summary**
  - **Evidence** (code path, endpoint, or reproduction steps)
  - **Impact**
  - **Exploit path**
  - **Fix recommendation**
  - **Verification steps / tests**
- Call out assumptions and any untested areas.

## References

- **Threat modeling**: See `references/threat-modeling.md`
- **Security checklist**: See `references/security-checklist.md`
- **Report template**: See `references/report-template.md`
