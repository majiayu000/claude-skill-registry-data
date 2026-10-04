---
name: sf-security-model
description: Salesforce security model and secure-coding enforcement for Apex, LWC, and metadata - org/object/field/record layers, permission sets vs profiles vs permission set groups vs muting permission sets, CRUD and FLS enforcement with WITH USER_MODE, AccessLevel.USER_MODE, Security.stripInaccessible, and Schema describe checks, sharing keywords and Apex managed sharing __Share records, Lightning Web Security and CSP, SOQL injection, XSS, open redirect and CSRF fixes, Named Credentials and protected custom metadata for secrets, Shield Platform Encryption impacts, and Event Monitoring. Use when writing or reviewing @AuraEnabled controllers, triggers, dynamic SOQL, lwc:dom="manual" markup, permission set metadata, integration users, or when running vf-check analyzer or the sf-security-reviewer agent.
---

# Salesforce Security Model

## When to use

- Any Apex class that queries or writes data, especially `@AuraEnabled`, `@InvocableMethod`, `@RestResource`, `global`, or Visualforce controller entry points.
- Building or reviewing permission metadata (`permissionsets/`, `permissionsetgroups/`, object/field permissions).
- Dynamic SOQL/SOSL, `Database.query`, string-concatenated queries, `lwc:dom="manual"`, `innerHTML`, redirects, HTTP callouts with credentials.
- Wave 2 of the vibe-force workflow: `sf-security-reviewer` reads this skill before reviewing a diff; `vf-check analyzer` enforces the machine-verifiable subset.
- Auditing the standing posture of a whole org rather than one change: skill `sf-org-security-audit`, which reuses the permission queries in `references/permission-architecture.md`.

## API version 67.0 default-mode change (read this first)

`config/vibe-force.defaults.json` pins `apiVersion` `67.0`. That version changed the Apex security defaults:

| Behaviour | API 66.0 and earlier | API 67.0 and later |
| --- | --- | --- |
| Database operation access mode | system mode (FLS/object perms ignored) | **user mode** (FLS, object perms, sharing enforced) |
| Class with no sharing declaration | resolved per inheritance chain / entry point, often `without sharing` | **`with sharing`** |
| Trigger body DML/SOQL | system mode | **user mode**, which overrides the trigger's own `without sharing` context |
| Anonymous Apex, Connect in Apex | `with sharing` | `with sharing` |
| `WITH SECURITY_ENFORCED` in a SOQL `SELECT` in Apex | allowed, with limitations | **not allowed** - the compiler rejects it; use `WITH USER_MODE` |

Consequences for vibe-force code: never rely on the default. Declare `with sharing` / `inherited sharing` / `without sharing` explicitly on every class with data access, and set an explicit access mode (`WITH USER_MODE`, `WITH SYSTEM_MODE`, `as user`, `as system`, `AccessLevel.*`) on every database operation so the code reads the same on any API version. Triggers cannot carry a sharing declaration: they always run `without sharing`, so delegate to a handler class (see skill `sf-apex-development`).

## Security layer decision table

| Layer | Controls | Configured with | Enforced in Apex by |
| --- | --- | --- | --- |
| Org | login IP ranges, hours, MFA, session settings | Setup, security policies | nothing in code |
| Object (CRUD) | create/read/edit/delete per object | permission sets, permission set groups, profiles | user mode, `Schema.DescribeSObjectResult.isCreateable/isAccessible/isUpdateable/isDeletable`, `stripInaccessible` |
| Field (FLS) | read/edit per field | permission sets (`fieldPermissions`) | user mode, `Schema.DescribeFieldResult`, `stripInaccessible` |
| Record | which rows a user sees | OWD, role hierarchy, sharing rules, manual shares, Apex managed sharing, restriction rules | class sharing keyword + user mode |
| Apex/VF class | who may invoke the class | `classAccesses` / `pageAccesses` in permission sets | runtime access check on `@AuraEnabled` and VF entry points |
| Client | DOM/script isolation | Lightning Web Security, CSP | LWS sandbox, `lightning/ui*Api` (enforces FLS server-side) |

Object/field permissions and sharing are independent and can coexist; where they conflict, object-level and field-level permissions take precedence over sharing rules.

## Core patterns

### 1. Query in user mode (default choice)

```apex
public with sharing class ExpenseSelector {
    public static List<Expense__c> recent(Integer rowLimit) {
        return [
            SELECT Id, Name, Amount__c, Client__c, Date__c
            FROM Expense__c
            WHERE Date__c = LAST_N_DAYS:30
            WITH USER_MODE
            ORDER BY Date__c DESC
            LIMIT :rowLimit
        ];
    }
}
```

`WITH USER_MODE` processes every clause including `WHERE`, supports polymorphic fields (`Owner`, `Task.WhatId`), reports all FLS errors, and exposes them through `QueryException.getInaccessibleFields()`. It is the only clause-based option at our target version: in API 67.0 and later a SOQL `SELECT` in Apex cannot use `WITH SECURITY_ENFORCED` at all. Legacy (pre-67.0) code that still carries `WITH SECURITY_ENFORCED` must be migrated to `WITH USER_MODE` when its class is raised to 67.0; that clause also reported only the first error, skipped the `WHERE` clause, ignored polymorphic fields, and was never allowed in AppExchange packages.

### 2. DML in user mode, with error introspection

```apex
public with sharing class ExpenseWriter {
    public static void save(List<Expense__c> expenses) {
        List<Database.SaveResult> results = Database.insert(expenses, false, AccessLevel.USER_MODE);
        for (Database.SaveResult r : results) {
            if (!r.isSuccess()) {
                for (Database.Error e : r.getErrors()) {
                    System.debug(LoggingLevel.WARN, e.getStatusCode() + ' on ' + e.getFields());
                }
            }
        }
    }
}
```

Statement form: `insert as user expenses;` / `update as system expenses;`. On a user-mode `DmlException`, `getDmlFieldNames()` returns the fields that failed FLS.

### 3. Graceful degradation with `stripInaccessible`

```apex
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.READABLE,
    [SELECT Name, BudgetedCost, ActualCost FROM Campaign WITH SYSTEM_MODE]
);
if (decision.getRemovedFields().get('Campaign')?.contains('ActualCost') == true) {
    // render the table without ActualCost instead of throwing
}
List<Campaign> safe = (List<Campaign>) decision.getRecords();
```

`AccessType` values: `READABLE`, `CREATABLE`, `UPDATABLE`, `UPSERTABLE`. `Id` is never stripped. `AggregateResult` is unsupported and throws. Use `getModifiedIndexes()` to detect that anything was stripped, and `sObject.isSet('Field__c')` to test a specific field.

### 4. Dynamic SOQL without injection

```apex
Map<String, Object> binds = new Map<String, Object>{ 'title' => '%' + userInput + '%' };
List<Personnel__c> rows = Database.queryWithBinds(
    'SELECT Id, Name, Title__c FROM Personnel__c WHERE Title__c LIKE :title',
    binds,
    AccessLevel.USER_MODE
);
```

`Database.queryWithBinds` (API 57.0+) resolves binds from a map, so the variables need not be in scope. Bind map keys are compared case-insensitively; duplicate case-variant keys throw `QueryException`. `String.escapeSingleQuotes` only helps inside single-quoted literals and is explicitly not the recommended defence. Field and object names cannot be bound: allowlist them (`Set<String>` of permitted API names) plus a describe accessibility check.

### 5. Record access beyond sharing rules: Apex managed sharing

```apex
Job__Share share = new Job__Share(
    ParentId = job.Id,
    UserOrGroupId = job.Recruiter__c,
    AccessLevel = 'Edit',
    RowCause = Schema.Job__Share.RowCause.Recruiter__c
);
Database.SaveResult sr = Database.insert(share, false, AccessLevel.USER_MODE);
```

Share objects are `<Object>Share` / `MyObject__Share`. Access levels: `Read`, `Edit`, `All` (`All` is managed-sharing only; `None` applies to `AccountShare` only). Apex sharing reasons (`RowCause`) are custom-object-only and survive owner changes; `RowCause = 'Manual'` shares are deleted when the owner changes. The object's OWD must not already be the most permissive setting, otherwise insert fails with `FIELD_FILTER_VALIDATION_EXCEPTION`. Details and the recalculation batch pattern: `references/sharing-and-record-access.md`.

### 6. Ship permission sets, not profiles

Grant all functional access through permission sets and compose them with permission set groups; use muting permission sets to subtract from a group rather than forking a permission set. Profiles stay minimal (`Minimum Access - Salesforce` plus license/defaults). Metadata shapes, retrieval caveats, and deployment ordering: `references/permission-architecture.md`.

### 7. Secrets never live in source

| Need | Use | Never |
| --- | --- | --- |
| Outbound HTTP auth | Named Credential + External Credential (`callout:MyNC/path`) | hardcoded tokens, `setHeader('Authorization', 'Bearer ...')` |
| Package-scoped secret | protected custom metadata type in a namespaced managed package | custom setting readable by users |
| Org-local operational secret | protected custom setting / custom metadata restricted by permission set | Apex constant, static resource |
| Crypto keys/IVs | `Crypto.generateAesKey`, stored via the above | literal key/IV in Apex (`ApexBadCrypto`) |

Credentials in `ExternalCredential` are encrypted by the platform with org-specific keys. vibe-force hooks scan writes for credential-looking literals and block them in `standard` and `strict` hook modes; `vf-check analyzer` flags `ApexSuggestUsingNamedCred` and `ApexBadCrypto`.

### 8. Client-side security

- Lightning Web Security is the default architecture for orgs created in Winter '23 and later and GA for all orgs since Summer '23; it replaces Lightning Locker with per-namespace JavaScript virtualization. Components must not override `window`/`document` functions, must load libraries via `lightning/platformResourceLoader` from a static resource, and must not use inline `<script>`.
- CSP for Lightning is `default-src 'self'`, `script-src 'self'`, `object-src 'self'`, `style-src 'self' https:`, `img-src 'self' http: https: data:`, `connect-src 'self'`, `frame-src https:`, `frame-ancestors https:`, `font-src https: data:`. Enable the stricter CSP org setting and develop against it. `unsafe-inline` and `unsafe-eval` are not blocked by CSP today but are rejected in AppExchange security review.
- `lightning/uiRecordApi`, `lightning-record-form`, and the other Lightning Data Service wire adapters apply sharing, CRUD, and FLS for you. Prefer them over custom `@AuraEnabled` data plumbing (skill `sf-lwc-development`).
- Every `@AuraEnabled` method is a public web service: assume an attacker calls it with arbitrary parameters, regardless of what your component sends.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
| --- | --- | --- |
| `public class Svc { ... }` with DML | sharing mode depends on API version and call chain | declare `with sharing` (or `inherited sharing` for reusable services) |
| `[SELECT ... FROM Account]` in a class saved at 66.0 and callers assuming FLS | pre-67.0 default is system mode | add `WITH USER_MODE` |
| `Database.query('... WHERE Name = \'' + input + '\'')` | SOQL injection | `Database.queryWithBinds` with `AccessLevel.USER_MODE` |
| `String.escapeSingleQuotes(input)` on an unquoted boolean/number position | escaping does nothing outside quotes | typecast or allowlist |
| `with sharing` used as an FLS control | sharing keywords set record access only | add user mode or `stripInaccessible` |
| `stripInaccessible` result discarded (`insert original;`) | inaccessible fields still written | insert `decision.getRecords()` |
| `WITH SECURITY_ENFORCED` anywhere in new Apex | rejected by the compiler at API 67.0 and later | `WITH USER_MODE` |
| `this.template.querySelector('div').innerHTML = serverHtml` | XSS inside the component | render with template directives, or sanitize before `lwc:dom="manual"` |
| `PageReference(ApexPages.currentPage().getParameters().get('retURL'))` | open redirect (`ApexOpenRedirect`) | allowlist relative paths |
| DML in a constructor or `@AuraEnabled(cacheable=true)` getter | CSRF-on-GET (`ApexCSRF`) | move state changes to an explicit POST-style action |
| `System.debug(userRecord)` with PII, `APEX_CODE=FINEST` in prod | debug logs leak PII; FINEST logs every variable assignment | scrub logs, cap log level (skill `sf-debugging-logs`) |
| Integration user with `Modify All Data` | no least privilege, blast radius on token leak | dedicated integration permission set, object-scoped |

## Verification

```bash
# security-tagged static analysis (PMD + ESLint + Flow + Regex engines)
sf code-analyzer run --workspace . --rule-selector Security --view detail

# path-based CRUD/FLS analysis over Apex (Graph Engine)
sf code-analyzer run --workspace . --rule-selector sfge --target force-app/main/default/classes

# the gate vibe-force runs; fails at configured analyzerFailSeverity (default 3)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# prove enforcement at runtime with a least-privilege user
sf apex run test --tests SecurityEnforcementTest --synchronous --target-org vf-dev

# confirm what a permission set actually grants in the org
sf data query --query "SELECT SobjectType, PermissionsRead, PermissionsCreate, PermissionsEdit, PermissionsDelete FROM ObjectPermissions WHERE ParentId IN (SELECT Id FROM PermissionSet WHERE Name = 'Expense_App_User')" --target-org vf-dev
```

Runtime proof pattern (full version in `references/crud-fls-enforcement.md`): create a minimum-access user, assign only the intended permission set, wrap the call in `System.runAs`, and assert that an unauthorized call throws `System.QueryException` / `System.DmlException` / `SecurityException` rather than silently returning data.

## PR security checklist

1. Every class touching data has an explicit sharing declaration; triggers delegate to handlers.
2. Every SOQL/SOSL/DML has an explicit access mode; `WITH SYSTEM_MODE` / `as system` / `without sharing` carries a comment naming the business reason.
3. No string-concatenated user input in a query; dynamic field/object names allowlisted.
4. `@AuraEnabled` / `@RestResource` / `@InvocableMethod` parameters validated and never used to choose objects or fields directly.
5. No secrets in source; callouts use Named Credentials; endpoints are HTTPS (`ApexInsecureEndpoint`).
6. No `innerHTML`/`lwc:dom="manual"` with server data; no inline script; libraries loaded from static resources.
7. Permission sets updated in the same PR as new objects, fields, Apex classes, and pages; no profile edits.
8. Tests assert negative access with `System.runAs` for at least one least-privilege persona.
9. `vf-check analyzer` and `vf-check local` pass; any suppression has a rule selector, a limit, and a reason.
10. No PII in `System.debug`; no `APEX_CODE=FINEST` trace flags left active.

## References

- `references/crud-fls-enforcement.md` - decision matrix and runnable code for every enforcement mechanism, with tests.
- `references/sharing-and-record-access.md` - OWD, hierarchy, sharing rules, `__Share` objects, recalculation, restriction rules.
- `references/secure-coding-catalogue.md` - vulnerability to vulnerable code to fixed code to detecting rule.
- `references/permission-architecture.md` - permission set, group, and muting metadata, deployment notes.
- Apex Developer Guide: [Apex Security and Sharing Model](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security_sharing_chapter.htm) - authoritative Versioned Behavior Changes list for API 67.0.
- Apex Developer Guide: [Enforce Object and Field Permissions](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_perms_enforcing.htm), [Set an Access Mode for Database Operations](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_enforce_usermode.htm), [stripInaccessible](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_with_security_stripInaccessible.htm), [sharing keywords](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_keywords_sharing.htm), [Apex Managed Sharing](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_bulk_sharing.htm), [Dynamic SOQL](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dynamic_soql.htm)
- Secure Coding Guide: [CRUD/FLS](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_access_control_protect_from_crud_fls_vulnerabilities.htm), [Sharing Violations](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_access_control_protect_from_sharing_violations.htm), [SOQL Injection](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_sql_injection.htm), [XSS](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_cross_site_scripting.htm), [Storing Sensitive Data](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_storing_sensitive_data.htm), [Lightning Security](https://developer.salesforce.com/docs/atlas.en-us.secure_coding_guide.meta/secure_coding_guide/secure_coding_lightning_security.htm)
- LWC Developer Guide: [Secure Apex Classes](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security.html)
- [Lightning Web Security](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-intro.html)
- Metadata API: [PermissionSet](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionset.htm), [PermissionSetGroup](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_permissionsetgroup.htm), [MutingPermissionSet](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_mutingpermissionset.htm), [ExternalCredential](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalcredential.htm)
- Object Reference: [EventLogFile](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_eventlogfile.htm)
- Sibling skills: `sf-apex-development`, `sf-apex-testing`, `sf-lwc-development`, `sf-code-analyzer-quality`, `sf-debugging-logs`, `sf-deployment-strategies`, `sf-post-deploy-verification`, `sf-integration-patterns`.
