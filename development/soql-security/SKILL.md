---
name: soql-security
description: "Use when writing, reviewing, or troubleshooting Apex queries that may expose SOQL injection or CRUD/FLS issues. Triggers: 'Database.query', 'WITH USER_MODE', 'WITH SECURITY_ENFORCED', 'stripInaccessible', 'security review finding'. NOT for enforcing FLS on records before DML — use apex/apex-stripinaccessible-and-fls-enforcement. NOT for the with sharing / without sharing choice — use apex/apex-with-without-sharing-decision."
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
  - "apex SOQL security review CRUD FLS injection"
  - "rewrite this dynamic SOQL so user input cannot change the query"
  - "make my AuraEnabled query respect field-level security"
inputs: ["query context", "user input path", "sharing model"]
outputs: ["security review findings", "secure query rewrite guidance", "crud-fls enforcement recommendations"]
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-10-03
---

You are a Salesforce expert in secure Apex data access. Your goal is to prevent SOQL injection and enforce CRUD, FLS, and sharing correctly in every query path.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- Is the code internal-only, component-facing, Experience Cloud-facing, or API-facing?
- Is the query static SOQL, dynamic SOQL, or both?
- Does the class run `with sharing`, `without sharing`, or inherit sharing?
- What `apiVersion` is the class pinned to in its `.cls-meta.xml`? That value, not the org's release, decides the default access mode and which idioms compile — see [`agents/_shared/AGENT_CONTRACT.md`](../../../agents/_shared/AGENT_CONTRACT.md) § *Apex security idiom by API version* for the canonical table. If you cannot see it, say which row you assumed.
- Is partial field stripping acceptable, or must inaccessible fields fail fast?

## Questions to Ask Before Configuring

Ask these before writing or rewriting a query; each answer changes which enforcement idiom is correct.

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| "What `apiVersion` is this class (or trigger) saved at?" | At 67.0+ database operations run in user mode by default, classes with no sharing keyword run `with sharing`, and `WITH SECURITY_ENFORCED` is not supported; at 66.0 and earlier the opposite defaults apply | The row of the version table the fix must target | A fix that compiles at the version actually deployed instead of one that breaks the build or silently changes access |
| "Which callers reach this method: LWC/Aura, REST, Experience Cloud guest or member, batch, or trigger?" | Public entry points need user-mode reads; batch and integration code may legitimately need `WITH SYSTEM_MODE` | The list of entry points to test with a low-access user | Elevation that is written down per statement, not inherited from a missing keyword |
| "Which parts of the query come from input: values only, or also field names, sort order, object names, or LIMIT?" | Bind variables protect values only; structural input needs an allowlist | An allowlist per structural parameter | A query whose shape cannot be changed by the caller |
| "If the user cannot read one of the selected fields, should the call fail or return the rest?" | `WITH USER_MODE` throws `QueryException`; `Security.stripInaccessible` removes the field | The fail-fast or degrade decision per method | Predictable UI behavior instead of a blank component or a silent data leak |
| "Is there a business reason any record must be visible regardless of sharing?" | Justifies `without sharing` or `WITH SYSTEM_MODE` and its scope | A one-line rationale stored next to the bypass | An auditable exception that survives a security review |

What a proper configuration adds over "just adding WITH USER_MODE": the enforcement idiom matches the class's `apiVersion`, structural input is allowlisted, and every system-mode bypass is deliberate and documented, so the code passes security review and does not change behavior on the next version bump.

## How This Skill Works

### Mode 1: Build from Scratch

1. Start with static SOQL whenever possible.
2. If dynamic SOQL is necessary, bind values and allowlist every structural element.
3. Choose the security enforcement pattern up front: `WITH USER_MODE` for reads, `stripInaccessible()` where partial results are acceptable. Never write `WITH SECURITY_ENFORCED` into new code — it was removed in API 67.0 and does not compile there.
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
| CRUD/FLS bypass | Apex exposes fields or objects the running user should not access | `WITH USER_MODE` or `stripInaccessible()` (user mode is already the default from `apiVersion` 67.0 — state it anyway) |
| Sharing bypass | Code sees records the user should not see | `with sharing` or explicit documented exception |

### Query Construction Rules

- Never concatenate user-controlled values into a SOQL string.
- Treat field names, object names, sort directions, and operators as structural input that must be allowlisted.
- Prefer static SOQL unless the business requirement truly needs runtime field or object selection.
- If dynamic SOQL remains, explain why it could not be static.

### Enforcement Decision Matrix

| Scenario | Use |
|----------|-----|
| Component-facing or API-facing Apex | `WITH USER_MODE` — the default at `apiVersion` 67.0+, still worth stating |
| All-or-nothing field access on read | `WITH USER_MODE` — any inaccessible field throws `QueryException` and the whole query fails, the same fail-fast contract `WITH SECURITY_ENFORCED` offered, and unlike it this still compiles at 67.0+ |
| Partial read results are acceptable | `stripInaccessible(AccessType.READABLE, records)` |
| Insert or update on behalf of the user | `stripInaccessible(AccessType.CREATABLE/UPDATABLE, records)` — still right at 67.0+, where default user mode throws and fails the whole DML instead |
| Intentional admin/system context | `WITH SYSTEM_MODE` / `AccessLevel.SYSTEM_MODE` on the statement, plus a comment: from 67.0 elevation is opt-in, so the bypass is written down and auditable |

## Recommended Workflow

1. Read the `.cls-meta.xml` (or `.trigger-meta.xml`) `apiVersion` and record which access-mode defaults apply; see [`references/gotchas.md`](references/gotchas.md) Gotchas 2, 4, and 6.
2. List every `Database.query`, `Database.queryWithBinds`, `Database.countQuery`, `Search.query`, and inline SOQL in the class, and mark which inputs reach each one.
3. Remove injection first: convert values to bind variables (or a `queryWithBinds` map) and allowlist every structural element; never escape a value that is already bound.
4. Choose the access idiom per statement: `WITH USER_MODE` or `AccessLevel.USER_MODE` for user-facing reads, `Security.stripInaccessible` where partial results are acceptable, `WITH SYSTEM_MODE` plus a rationale comment where elevation is required.
5. Run `python3 skills/apex/soql-security/scripts/check_soql_security.py force-app/main/default/classes` and resolve every CRITICAL and HIGH finding.
6. Prove the result with a test that runs as a low-access user (`System.runAs`) and asserts both the allowed and the denied path; see [`references/deployable-example.md`](references/deployable-example.md).

---

## Review Checklist

- [ ] No string concatenation of user input into SOQL
- [ ] Dynamic `ORDER BY`, `LIMIT`, and field names are allowlisted
- [ ] Public Apex entry points enforce sharing and CRUD/FLS intentionally
- [ ] `without sharing` usage is justified inline
- [ ] DML paths sanitize records when user permissions should apply

## Salesforce-Specific Gotchas

One-line summaries; the full what / when / how-to-avoid entries live in [`references/gotchas.md`](references/gotchas.md).

| Gotcha | Short form |
|---|---|
| `String.escapeSingleQuotes()` | Protects quoted values only, never field names, operators, `ORDER BY`, or `LIMIT` |
| FLS failure on read | `WITH USER_MODE` throws for the whole query; it never returns a partial row |
| `WITH SECURITY_ENFORCED` | Not supported in Apex SOQL at `apiVersion` 67.0+; use `WITH USER_MODE` |
| Triggers | The trigger itself runs without sharing, but at 67.0+ its unqualified SOQL and DML run in user mode |
| `stripInaccessible()` | Removes fields, never records, and throws when the object itself is not accessible |
| `without sharing` plus broad SOQL | A real exposure; keep it narrow and write the reason next to it |

## Proactive Triggers

Surface these without being asked:

| Pattern found | Severity | Why |
|---|---|---|
| Dynamic SOQL built with string concatenation | Critical | Treat it as an injection path until proven otherwise |
| Public Apex at `apiVersion` 66.0 or earlier querying with no CRUD/FLS idiom | High | It commonly passes tests and fails security review |
| `without sharing` with no written justification | High | Hidden system-context access is an audit problem |
| User-controlled sort field, object name, or operator with no allowlist | High | Structural injection is still injection |
| `WITH SECURITY_ENFORCED` in a class saved at 67.0+ | Critical | The class does not compile |
| PMD suppression with no rationale | Medium | Security exceptions must be traceable |

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
