---
name: sf-org-security-audit
description: Standing security audit of a Salesforce org and its source - who holds ModifyAllData, ViewAllData, AuthorApex and ViewEncryptedData, the object and field matrix behind every permission set, profile sprawl, Apex class and @AuraEnabled exposure, org-wide defaults and without-sharing code, guest user and Experience Cloud surface, Named and External Credentials, secrets in source and in git history, and the Setup-only checks (Health Check, session and password policy, login IP ranges, MFA, Setup Audit Trail) that no CLI command covers. Produces a severity-ranked findings report with evidence and a fix per item. Use when onboarding an org, preparing a security review or audit response, or periodically. Not for reviewing a diff - that is the sf-security-reviewer agent - and not for writing secure Apex, which is skill sf-security-model.
---

# Salesforce Org Security Audit

## When to use

| Situation | Use this skill |
| --- | --- |
| Auditing the standing security posture of an org | Yes |
| Preparing for a customer or internal security review | Yes |
| Onboarding an org you did not configure | Yes |
| Reviewing the security of the diff you just wrote | Agent `sf-security-reviewer` |
| Writing Apex that enforces CRUD, FLS and sharing | Skill `sf-security-model` |
| Maintainability rather than exposure | Skill `sf-technical-debt-audit` |
| Callout authentication design | Skill `sf-integration-patterns` |
| Analyzer security rules on source | Skill `sf-code-analyzer-quality` |

This audit is read-only: queries, retrieves and greps. It never changes a permission, a setting or
a record, and it is legitimate against production.

## Scope and safety

| Rule | Why |
| --- | --- |
| Read-only commands only: `sf data query`, `sf project retrieve preview`, `sf org list ...`, `vf-check static` | An audit that mutates is an incident |
| Never `VF_ALLOW_PROD=1` | That flag exists to let a mutating check through; nothing here needs it |
| Retrieve into a scratch directory, never over the working tree | A retrieved profile overwriting source is a silent change |
| Evidence or it did not happen | Every finding carries a query result, a `file:line`, or a named Setup page |
| Handle findings like the vulnerability they describe | The report names exposures; treat it as confidential and never paste org ids, usernames or tokens into a public channel |

Production posture: `vf-check` prints a production banner for read-only checks rather than refusing
them (`scripts/checks/lib/org.mjs`). Queries against a production alias are fine here. Running
`vf-check apex` against production is not part of this audit.

## Audit layers

| Layer | The question | How to measure |
| --- | --- | --- |
| Identity | Who can log in, from where, with what factor | Setup: session, password, login IP, MFA; `sf org list users` |
| Grants | Who holds administrative permissions | `PermissionSetAssignment` SOQL, pattern 3 |
| Access matrix | What each permission set opens up | `ObjectPermissions` and `FieldPermissions` SOQL, pattern 4 |
| Record access | Org-wide defaults, sharing rules, `without sharing` code | Source `<sharingModel>` plus grep, pattern 7 |
| Code exposure | `@AuraEnabled`, `@RestResource`, `webService`, Apex class access | Source inventory plus `SetupEntityAccess`, pattern 6 |
| Public surface | Guest users, Sites, Experience Cloud | `networks/` metadata plus guest profile, pattern 8 |
| Integration | Named and External Credentials, Remote Site Settings, connected apps | Source inventory, pattern 9 |
| Secrets | Literal credentials in source or history | Grep plus git history, pattern 9 |
| Change control | Who changed security settings, and when | Setup Audit Trail, pattern 10 |

## Core patterns

### 1. Fix the scope and the evidence trail

```bash
sf org display --target-org vf-prod
sf org list users --target-org vf-prod
mkdir -p .vibeforce/reports/audit && export AUDIT=.vibeforce/reports/audit
```

Record the org id, the edition, the alias, whether the source tree is the whole org, and the date.
Every command below writes into `$AUDIT`, so the report can cite raw output rather than memory.

### 2. Retrieve the security-relevant metadata

```xml
<!-- manifest/security-audit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>Security</members><name>Settings</name></types>
    <types><members>*</members><name>PermissionSet</name></types>
    <types><members>*</members><name>PermissionSetGroup</name></types>
    <types><members>*</members><name>Profile</name></types>
    <types><members>*</members><name>SharingRules</name></types>
    <types><members>*</members><name>NamedCredential</name></types>
    <types><members>*</members><name>ExternalCredential</name></types>
    <types><members>*</members><name>RemoteSiteSetting</name></types>
    <version>67.0</version>
</Package>
```

```bash
sf project retrieve start --manifest manifest/security-audit.xml \
  --target-org vf-prod --output-dir "$AUDIT/metadata"
```

Retrieving into `--output-dir` keeps the working tree untouched. The directory layout under it
depends on the retrieve, so locate the retrieved types rather than assuming a path:

```bash
find "$AUDIT/metadata" -type d \( -name profiles -o -name permissionsets -o -name permissionsetgroups \
  -o -name namedCredentials -o -name externalCredentials -o -name remoteSiteSettings -o -name sharingRules \)
```

An `ls` against a guessed path that does not exist prints an error and counts as zero - on a
security audit that reads as a clean result. Always count from `find` output.

Profiles retrieve as a sparse representation - a permission missing from a retrieved profile is not proof it is not granted, so
confirm grants with the queries in patterns 3 and 4 rather than by reading profile XML.

### 3. Who holds the dangerous permissions

```bash
sf data query --target-org vf-prod --json \
  --query "SELECT Assignee.Username, Assignee.IsActive, PermissionSet.Name FROM PermissionSetAssignment WHERE PermissionSet.PermissionsModifyAllData = true" > "$AUDIT/modifyalldata.json"

sf data query --target-org vf-prod --json \
  --query "SELECT Assignee.Username, PermissionSet.Name FROM PermissionSetAssignment WHERE PermissionSet.PermissionsViewAllData = true" > "$AUDIT/viewalldata.json"
```

Repeat for `PermissionsAuthorApex`, `PermissionsViewEncryptedData`, `PermissionsManageUsers` and
`PermissionsCustomizeApplication` `[unverified: only PermissionsModifyAllData, PermissionsViewAllData,
PermissionsViewAllRecords and PermissionsModifyAllRecords are confirmed field names in this
repository - run sf sobject describe --sobject PermissionSet --target-org <alias> before relying on
the rest]`. Findings, in descending severity:

| Finding | Severity |
| --- | --- |
| An integration or service account holds `ModifyAllData` | high |
| A named person holds `ModifyAllData` outside the admin group | high |
| An inactive user still holds an administrative permission | medium |
| `ViewAllData` granted for a reporting need a report type would satisfy | medium |
| `AuthorApex` outside the release process | medium |

A grant that appears through a profile's own permission set still counts as a grant, which is why
profile sprawl (pattern 5) is a security topic and not only a tidiness one. `[unverified: the
`IsOwnedByProfile` field used below to separate profile-owned permission sets from standalone ones
was not confirmed in this session - describe the object first, or drop the filter and group by
`Parent.Name`.]`

### 4. The access matrix per permission set

```bash
sf data query --target-org vf-prod --json \
  --query "SELECT Parent.Name, SobjectType, PermissionsRead, PermissionsCreate, PermissionsEdit, PermissionsDelete, PermissionsViewAllRecords, PermissionsModifyAllRecords FROM ObjectPermissions WHERE Parent.IsOwnedByProfile = false" > "$AUDIT/objectperms.json"

sf data query --target-org vf-prod --json \
  --query "SELECT Parent.Name, Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE SobjectType = 'Account'" > "$AUDIT/fieldperms-account.json"
```

Audit the sensitive objects first: anything holding personal data, financial data, or credentials.
`PermissionsViewAllRecords` and `PermissionsModifyAllRecords` bypass sharing for that object - each
one needs a named reason, and an object-level bypass granted to a broad permission set is a high
finding.

### 5. Profile sprawl

```bash
find "$AUDIT/metadata" -path "*/profiles/*.profile-meta.xml"        | wc -l
find "$AUDIT/metadata" -path "*/permissionsets/*.permissionset-meta.xml" | wc -l
```

Posture, in order of preference: permission set groups for personas, permission sets for features,
profiles reduced to login and default settings. A large profile count with few permission sets
means access cannot be reviewed - the finding is "grants are not reviewable", and its severity
depends on what those profiles open up (pattern 4), not on the count.

### 6. Code exposure surface

```bash
grep -rn "@AuraEnabled" force-app --include="*.cls" | wc -l
grep -rn "@RestResource\|global class\|webService" force-app --include="*.cls"
grep -rln "without sharing" force-app --include="*.cls"

sf data query --target-org vf-prod --json \
  --query "SELECT Parent.Name, SetupEntityId FROM SetupEntityAccess WHERE SetupEntityType = 'ApexClass'" > "$AUDIT/apexclassaccess.json"
```

Every `@AuraEnabled` and `@RestResource` method is an API an authenticated user can call directly:
the client never enforces anything. Check each one for user-mode data access and a sharing keyword
(skill `sf-security-model`). A generic endpoint - "run this SOQL", "update this record with this
map" - is a high finding regardless of who holds the class access.

### 7. Record access: org-wide defaults and elevation

```bash
grep -rh "<sharingModel>" force-app/main/default/objects/*/*.object-meta.xml | sort | uniq -c
grep -rn "without sharing" force-app --include="*.cls"
grep -rn "__Share\b" force-app --include="*.cls"
```

An object whose sharing model is `ReadWrite` needs a reason; `Private` plus sharing rules is the
defensible default for anything sensitive. Every `without sharing` class and every Apex managed
sharing insert is an elevation path: it must be narrow, documented, and covered by a negative test
(skill `sf-security-model`, references `sharing-and-record-access.md`).

### 8. Public surface

```bash
ls force-app/main/default/networks/ 2>/dev/null
ls force-app/main/default/sites/ 2>/dev/null
grep -rn "Site\.\|Network\.\|UserInfo.getUserType" force-app --include="*.cls"
```

If the org has Sites or Experience Cloud, the guest user is an unauthenticated identity with real
permissions. Audit it as its own user: what objects it reads, which Apex classes it can run, which
Flows it can start, and whether any `without sharing` code runs on its behalf. Guest access to
person data is a high finding on sight, and personal-information visibility settings on the `User`
object are not enforced by user mode or `stripInaccessible` (skill `sf-security-model`, reference
`crud-fls-enforcement.md`).

### 9. Integrations and secrets

```bash
find "$AUDIT/metadata" -path "*/namedCredentials/*"    -type f
find "$AUDIT/metadata" -path "*/externalCredentials/*" -type f
find "$AUDIT/metadata" -path "*/remoteSiteSettings/*"  -type f

grep -rniE "password|secret|token|api[_-]?key|authorization" force-app --include="*.cls" --include="*.js" --include="*.xml"
git log -p --all -S"password" -- force-app | head -100
```

A Remote Site Setting with no matching Named Credential usually means a callout is authenticating
by hand, with the credential somewhere in source. A secret found in git history is still a secret:
the finding is "rotate the credential", not "remove the line".

### 10. The Setup-only layer

No CLI command covers these; a person opens Setup and records the answer. They belong in the report
with the same severity scale as everything else.

| Check | Setup location | Looking for |
| --- | --- | --- |
| Health Check score and risks | Security → Health Check | Score, and every High-Risk setting against the baseline |
| Session settings | Security → Session Settings | Timeout, lock to IP, clickjack protection, HttpOnly |
| Password policy | Security → Password Policies | Expiry, history, complexity, lockout |
| MFA | Identity → and the MFA assistant | Every interactive user covered |
| Login IP ranges and login hours | Profiles | Admin profiles restricted |
| Connected apps and OAuth scopes | Apps → Connected Apps | `full` and `refresh_token` scopes, who approved them |
| API access | Profiles and permission sets | `API Enabled` on people who do not integrate |
| Certificate and key management | Security → Certificate and Key Management | Expiry dates |
| Setup Audit Trail | Security → View Setup Audit Trail | Security changes in the last 6 months, and by whom |
| Shield Platform Encryption, Event Monitoring | Depends on licensing | Whether they are available and used |

`[unverified: whether the Health Check score, session settings and Setup Audit Trail are readable
through the API in this org's edition was not confirmed in this session. Treat this layer as manual
until you verify it with sf sobject describe against the relevant object.]`

### 11. The report

```markdown
## Security audit - <org alias> - <ISO date>
Scope: <what was audited>   Not audited: <what was out of reach>

| severity | layer | finding | evidence | fix | owner |
| --- | --- | --- | --- | --- | --- |

severities: high (data exposure or privilege escalation available today)
            medium (grant wider than needed, or a control with a gap)
            low (hardening opportunity, no current exposure)

## Setup-only layer
| check | result | finding |

## Accepted risks
<item> - <accepted by whom> - <review date>
```

Write it to `.vibeforce/reports/security-audit-<ISO>.md`. A re-run diffed against the previous
report is what turns an audit into a control.

## Anti-patterns

| Anti-pattern | Consequence | Fix |
| --- | --- | --- |
| Reading retrieved profile XML and concluding a permission is absent | Profiles retrieve sparsely; the grant may still exist | Confirm with `ObjectPermissions` and `PermissionSetAssignment` queries |
| Auditing source only | Org-only grants and Setup settings stay invisible | Retrieve, query, and record the Setup-only layer |
| Reporting "too many profiles" as the finding | Count is not exposure | Name what the profiles grant, with evidence |
| Fixing a finding during the audit | The audit becomes an unreviewed change | Report; remediate through the normal gated path |
| Running the audit as an integration user | You see only what that user sees | Run as an admin, and say which user produced the evidence |
| Pasting query output with usernames or org ids into a ticket | The report becomes the exposure | Redact identities; reference row counts and ids held separately |
| Treating a clean Code Analyzer run as a security audit | Static rules cover code, not grants | Both; they measure different layers |
| Leaving `[unverified]` items out of the report | Unknowns read as passes | List them under "Not audited" |

## Verification

```bash
# static security rules over the whole tree, not the diff
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --json
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --json

# grants, read-only, production-safe
sf data query --target-org vf-prod --query "SELECT COUNT(Id) FROM PermissionSetAssignment WHERE PermissionSet.PermissionsModifyAllData = true"

# what a retrieve would bring back, without touching the working tree
sf project retrieve preview --target-org vf-prod
```

Exit codes: `0` pass, `1` gate failed, `2` misconfiguration or missing tool, `3` org or network
error. A finding in this audit is not a `vf-check` failure - the gates run on the diff; the audit
runs on the org. Both belong in the report.

## References

- [`references/org-security-checklist.md`](references/org-security-checklist.md) - the full checklist: per-layer checks, the query or Setup path, the expected answer, and the severity when it differs.
- Related skills: `sf-security-model` (enforcement in code, permission architecture, sharing), `sf-technical-debt-audit` (the maintainability half of the same sweep), `sf-integration-patterns` (Named and External Credentials), `sf-code-analyzer-quality` (security rules and custom regex rules), `sf-data-management` (data exports and PII handling), `sf-debugging-logs` (Event Monitoring).
- Agent `sf-security-reviewer` for the per-diff review that this audit does not replace.
- Official: [Apex Security and Sharing](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security_sharing_chapter.htm), [Enforce User Mode](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_enforce_usermode.htm), [stripInaccessible](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_with_security_stripInaccessible.htm), [Named Credentials](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm).
