---
name: soql-security
description: "Use when writing, reviewing, or troubleshooting Apex queries that may expose SOQL injection or CRUD/FLS issues. Triggers: 'Database.query', 'WITH USER_MODE', 'WITH SECURITY_ENFORCED', 'stripInaccessible', 'security review finding'. NOT for record-sharing design unless the main issue is Apex query security."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Operational Excellence
tags: ["soql", "security", "crud", "fls", "injection"]
triggers:
  - "security review flagged SOQL injection"
  - "CRUD or FLS not being enforced in Apex"
  - "stripInaccessible not stripping fields correctly"
  - "user is seeing data they should not via Apex"
  - "how do I safely use Database.query with user input"
  - "WITH USER_MODE not working as expected"
inputs: ["query context", "user input path", "sharing model"]
outputs: ["security review findings", "secure query rewrite guidance", "crud-fls enforcement recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce expert in secure Apex data access. Your goal is to prevent SOQL injection and enforce CRUD, FLS, and sharing correctly in every query path.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- Is the code internal-only, component-facing, Experience Cloud-facing, or API-facing?
- Is the query static SOQL, dynamic SOQL, or both?
- Does the class run `with sharing`, `without sharing`, or inherit sharing?
- Is partial field stripping acceptable, or must inaccessible fields fail fast?

## How This Skill Works

### Mode 1: Build from Scratch

1. Start with static SOQL whenever possible.
2. If dynamic SOQL is necessary, bind values and allowlist every structural element.
3. Choose the security enforcement pattern up front: `WITH USER_MODE`, `WITH SECURITY_ENFORCED`, or `stripInaccessible()`.
4. Keep sharing, CRUD/FLS, and error behavior explicit for the caller.
5. For writes, sanitize records before DML when the operation should honor user permissions.

### Mode 2: Review Existing

1. Find every `Database.query()` call and trace where its inputs come from.
2. Separate injection risk from CRUD/FLS risk. They are different findings.
3. Check public entry points first: `@AuraEnabled`, `@InvocableMethod`, `@RestResource`, and community-facing code.
4. Inspect `without sharing` or inherited-sharing classes for intentional security bypasses.
5. Verify PMD suppressions or review comments actually document the reason for system-context behavior.

### Mode 3: Troubleshoot

1. Identify whether the failure is injection exposure, missing access, or over-restrictive enforcement.
2. If the query breaks only for some users, compare sharing and FLS behavior, not just query syntax.
3. If a security review flagged the code, map the finding to the exact query and data path.
4. Choose the smallest safe remediation: bind, allowlist, `WITH USER_MODE`, or `stripInaccessible`.
5. Re-test with a realistic low-access user, not only with admin context.

## Secure Query Patterns

### Keep These Problems Separate

| Problem | What It Means | Default Fix |
|---------|---------------|-------------|
| SOQL injection | User input changes the query structure | Static SOQL, bind variables, allowlists |
| CRUD/FLS bypass | Apex exposes fields or objects the running user should not access | `WITH USER_MODE`, `WITH SECURITY_ENFORCED`, or `stripInaccessible()` |
| Sharing bypass | Code sees records the user should not see | `with sharing` or explicit documented exception |

### Query Construction Rules

- Never concatenate user-controlled values into a SOQL string.
- Treat field names, object names, sort directions, and operators as structural input that must be allowlisted.
- Prefer static SOQL unless the business requirement truly needs runtime field or object selection.
- If dynamic SOQL remains, explain why it could not be static.

### Enforcement Decision Matrix

| Scenario | Use |
|----------|-----|
| Component-facing or API-facing Apex | `WITH USER_MODE` |
| All-or-nothing field access on read | `WITH SECURITY_ENFORCED` |
| Partial read results are acceptable | `stripInaccessible(AccessType.READABLE, records)` |
| Insert or update on behalf of the user | `stripInaccessible(AccessType.CREATABLE/UPDATABLE, records)` |
| Intentional admin/system context | Document why the bypass is required and auditable |

#
## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] No string concatenation of user input into SOQL
- [ ] Dynamic `ORDER BY`, `LIMIT`, and field names are allowlisted
- [ ] Public Apex entry points enforce sharing and CRUD/FLS intentionally
- [ ] `without sharing` usage is justified inline
- [ ] DML paths sanitize records when user permissions should apply

## Salesforce-Specific Gotchas

- **`String.escapeSingleQuotes()` is not a full injection defense**: It only helps quoted values, not field names, operators, or `ORDER BY`.
- **`WITH SECURITY_ENFORCED` fails the whole query**: One inaccessible field causes a `QueryException`, so use it only when fail-fast behavior is acceptable.
- **`stripInaccessible()` does not restore sharing**: It removes inaccessible fields but does not change record visibility semantics.
- **Component-facing Apex is not a security boundary by itself**: LWC, Aura, and API callers still rely on the server-side query to enforce access correctly.
- **`without sharing` plus broad SOQL is a real data-exposure risk**: If that context is intentional, it must be documented, reviewed, and narrow in scope.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Dynamic SOQL built with string concatenation** -> Flag as Critical. Treat it as an injection path until proven otherwise.
- **Public Apex querying without explicit CRUD/FLS strategy** -> Flag as High. This commonly passes tests but fails security review.
- **`without sharing` with no justification** -> Flag as High. Hidden system-context access is an audit problem.
- **User-controlled sort fields, object names, or operators with no allowlist** -> Flag as High. Structural injection is still injection.
- **PMD suppressions without rationale** -> Flag as Medium. Security exceptions must be traceable.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| SOQL security review | Injection, sharing, and CRUD/FLS findings with concrete fixes |
| Secure query rewrite | Static or dynamic-safe SOQL with the right enforcement mode |
| Security review remediation | Smallest safe change that satisfies behavior and compliance |

## Related Skills

- **apex/governor-limits**: Safe queries still need to be bulkified and limit-aware.
- **lwc/lifecycle-hooks**: Component-facing Apex called from LWC must enforce access on the server side.
- **admin/permission-sets-vs-profiles**: If security checks behave unexpectedly, confirm the permission model as well as the Apex.
