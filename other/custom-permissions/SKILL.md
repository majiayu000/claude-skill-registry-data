---
name: custom-permissions
description: "Use when creating, assigning, or checking custom permissions to control feature access beyond CRUD and FLS. Trigger keywords: 'custom permission', 'FeatureManagement.checkPermission', '$Permission global variable', 'feature gate', 'named access grant', 'beta feature flag', 'SetupEntityAccess', 'requiredPermission', 'who has this custom permission'. NOT for gating Apex service code and its tests — use apex/apex-custom-permissions-check. NOT for permission set design — use admin/permission-set-architecture."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - User Experience
triggers:
  - "how do I check a custom permission in Apex or a validation rule"
  - "I want to gate a feature so only certain users can see or use it"
  - "how do I use $Permission in a formula field or flow"
  - "create a custom permission and grant it through a permission set"
  - "custom permission returns false even though the user has the permission set"
  - "find out which users hold a custom permission"
  - "deploy failed because the permission set references a custom permission that does not exist"
  - "hide a Lightning page component unless the user has a custom permission"
  - "let the integration user bypass a validation rule without deactivating it"
  - "who has this custom permission assigned, query it"
  - "custom permission description too long, deploy rejected with max length 255"
tags:
  - custom-permissions
  - access-control
  - permission-set
  - feature-flags
  - apex
inputs:
  - "API name of the custom permission to create or check"
  - "permission sets that should grant the permission"
  - "platform contexts that need to read the permission (Apex, Flow, formula, validation rule)"
outputs:
  - "configured custom permission record with correct API name and label"
  - "permission set XML including the custom permission node"
  - "Apex, formula, validation rule, or Flow expressions that read the permission"
  - "checker report of which permission sets grant which custom permissions"
  - "SetupEntityAccess verification query proving who holds the permission today"
  - "component visibility filter using {!$Permission.CustomPermission.X}"
dependencies: []
version: 1.2.2
author: Pranav Nagrecha
updated: 2026-09-19
---

# Custom Permissions

Use this skill when a feature or capability needs a named access gate that goes beyond object, field, or record permissions. Custom permissions grant boolean access to a named capability and can be checked in validation rules, formula fields, Apex, Flow, LWC, Visualforce, and Lightning page component visibility. Each of those contexts spells the check differently.

---

## Before Starting

- Confirm you need a custom permission, not a permission set feature license or a record-level sharing rule. Custom permissions are for feature on/off gates, not record visibility.
- Identify all platform contexts that must check the permission (validation rule, formula, Apex, Flow). Each uses a different syntax.
- Gather the exact API name you want. `DeveloperName` must begin with a letter, contain only alphanumerics and underscores, not include spaces, **not end with an underscore, and not contain two consecutive underscores**; limit 80 characters (Object Reference, `CustomPermission.DeveloperName`). The name cannot be changed after creation without updating every reference.
- Determine which permission sets will carry the permission. A `Profile` can also carry one — `Profile.customPermissions` exists in the Metadata API from version 31.0 — but a profile-borne grant is invisible in the Custom Permissions related list, so grant through a permission set (`references/gotchas.md` Gotcha 1).

---

## Questions to Ask Before Configuring

Ask these before creating anything. A custom permission is trivial to create and permanent in practice, so the cost of a wrong answer is paid later, by whoever inherits the org.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "What exactly does holding this permission let someone do, in one sentence?" | If the sentence needs an "and", this is two permissions; a single flag that means several things cannot be revoked partially | The permission's `description`, and possibly a second permission |
| "Which contexts read it — validation rule, formula, Flow, Apex, LWC, component visibility?" | Each has a different spelling, and component visibility needs the extra `CustomPermission.` segment | The consumer list, and the set of syntaxes to get right (Gotcha 6) |
| "Does anything already hold this access through a profile?" | `Profile.customPermissions` deploys cleanly and hides in the profile-owned permission set | A `SetupEntityAccess` baseline before you add a second grant path (Gotcha 1) |
| "Does another custom permission have to be on for this one to make sense?" | `requiredPermission` enforces that at the platform level instead of in prose | A `CustomPermissionDependencyRequired` node and a single-package deploy order |
| "Who revokes it, and what proves it was revoked?" | A metadata diff cannot prove revocation — only enabled grants are ever retrieved | An owner and a live `SetupEntityAccess` query as the evidence artifact (Gotcha 8) |
| "Is this a bypass? If so, which named rules does it suppress?" | An unnamed bypass becomes an org-wide off switch nobody dares remove | The rule list in the `description` and a scoped `Bypass_Validation_<Domain>` name |
| "Is the grant permanent, or should it expire?" | Data-fix and migration bypasses outlive their reason by default | A time-limited permission set assignment (`admin/permission-set-expiration`) |

What a proper configuration adds over just creating the permission: the flag means one thing, every context that reads it uses the right syntax, the grant path is a permission set you can audit and expire, and there is a query that answers "who holds this today" without a Setup click-through.

---

## Core Concepts

### What Custom Permissions Are

Custom permissions are named boolean access grants. Unlike CRUD, FLS, and tab access, they carry no implicit meaning to the platform — they exist solely so developers and admins can build their own feature gates. Each custom permission has a label and an API name and can optionally be tied to a Connected App. When granted, the permission evaluates to `true` in every supported context for that running user's session.

Source: Salesforce Help — [Custom Permissions Overview](https://help.salesforce.com/s/articleView?id=sf.custom_perms_overview.htm)

### Creating Custom Permissions

Custom permissions are created in **Setup > Custom Permissions**. Click **New**, enter a label and an API name, then optionally provide a description and a Connected App association.

Key constraints on the API name (`CustomPermission.DeveloperName`, Object Reference):
- Must begin with a letter, and must not include spaces.
- Only alphanumeric characters and underscores are allowed.
- Must not end with an underscore, and must not contain two consecutive underscores — `__` is the namespace separator (`NamespacePrefix__componentName`).
- Limit 80 characters, unique in the org.
- Cannot be changed after the permission is referenced in production without a coordinated update of all dependent metadata and code.

`label` and `connectedApp` are capped at 80 characters and `description` at 255 (Metadata API Developer Guide, `CustomPermission` field table).

The `CustomPermission` metadata type is supported by the Metadata API (version 31.0 and later) and SFDX source format. The file lives at `customPermissions/My_Custom_Permission.customPermission-meta.xml`, and the filename stem is the API name — there is no `<fullName>` element in source format. Deployable shapes, package.xml, and the verification queries are in `references/metadata-examples.md`.

### Assigning Custom Permissions to Permission Sets

Grant custom permissions through permission sets. In Setup, open a permission set, navigate to **Custom Permissions**, and enable the desired permission. In the Metadata API, the permission set XML includes a `<customPermissions>` node (`PermissionSetCustomPermissions`, API 31.0+):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Refund Pilot</label>
    <customPermissions>
        <enabled>true</enabled>
        <name>My_Custom_Permission</name>
    </customPermissions>
</PermissionSet>
```

A single custom permission can appear in multiple permission sets and permission set groups. When any one of those is assigned to a user, the permission evaluates to `true` for that user.

`Profile` accepts the identical shape through `ProfileCustomPermissions`, also from API version 31.0. It deploys, and it hides — see `references/gotchas.md` Gotcha 1 and `admin/permission-sets-vs-profiles`. Permission set structure, grouping, and muting are `admin/permission-set-architecture`.

### Checking Custom Permissions in Each Platform Context

**Validation Rules and Formula Fields**

Use the `$Permission` global merge field. This returns `true` or `false`:

```
$Permission.My_Custom_Permission
```

To let users with the permission bypass a validation rule:

```
AND(
  NOT($Permission.My_Custom_Permission),
  /* original rule conditions */
)
```

Source: Salesforce Help — [Use Custom Permissions in Formulas](https://help.salesforce.com/s/articleView?id=sf.custom_perms_build_in_formula.htm)

**Apex**

Use `FeatureManagement.checkPermission(String apiName)`. It returns a `Boolean` and does not consume a SOQL row or any measurable governor resource:

```apex
if (FeatureManagement.checkPermission('My_Custom_Permission')) {
    // user holds the permission — allow the action
}
```

Source: Apex Developer Reference — [FeatureManagement Class](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_class_System_FeatureManagement.htm)

**Flow**

`$Permission` is a global resource available in Flow, but only as a formula resource — not directly in a Decision element condition row. The pattern is:

1. Create a formula resource of type Boolean with the value `$Permission.My_Custom_Permission`.
2. Reference that resource variable in a Decision element condition.

**Visualforce**

```
{!$Permission.My_Custom_Permission}
```

This evaluates to the string `"true"` or `"false"` in merge field contexts, or as a Boolean in `rendered` attributes.

**Lightning Page Component Visibility, Dynamic Forms, and In-App Guidance**

Component-visibility filters use a different grammar — note the extra `CustomPermission.` segment:

```
{!$Permission.CustomPermission.My_Custom_Permission}
```

Supported for app, Home, and record pages only (Metadata API Developer Guide, `FlexiPage` component-visibility expressions; the same expression appears in `Prompt.uiFormulaRule`). Owned by `admin/dynamic-forms-and-actions` and `admin/in-app-guidance-and-walkthroughs`.

**LWC**

```javascript
import hasPerm from '@salesforce/customPermission/My_Custom_Permission';
```

The import resolves to `true` or `undefined`, never `false`, and it shapes the DOM rather than enforcing anything. The Apex method behind the component needs its own check. Owned by `apex/apex-custom-permissions-check`.

**Connected Apps**

The `CustomPermission` metadata type has a `connectedApp` field: "The name of the connected app that's associated with this permission. Limit: 80 characters." UNVERIFIED (2026-09-04): the Metadata API guide does not document what that association enforces at authorization time, and the `CustomPermission` sObject exposes no connected-app field to query it back — do not promise an `access_denied` on OAuth. To require permissions for a connected app, the grounded field is `ConnectedApp.permissionSetName` (API 46.0+), which needs `isAdminApproved` set to `true`.

---

## Common Patterns

### Pattern: Feature Gate for Beta or Graduated Rollout

**When to use:** A new feature is ready for testing by a subset of users before general availability. You want to control who sees it without a code deployment.

**How it works:**
1. Create a custom permission: API name `Beta_New_Case_Console`.
2. Create a permission set: `Beta Testers — Case Console`. Add the custom permission to it.
3. Assign the permission set to pilot users only.
4. In an LWC, call a `@AuraEnabled(cacheable=true)` Apex method that returns `FeatureManagement.checkPermission('Beta_New_Case_Console')`.
5. Conditionally render the feature component based on the returned Boolean.
6. Guard the Apex action itself with the same check so the gate cannot be bypassed via API.
7. Expand rollout by assigning the permission set to more users — no code change required.

**Why not the alternative:** A custom Boolean field on the User object requires a SOQL query in Apex and cannot be read by `$Permission` in formulas. `FeatureManagement.checkPermission` is instant, session-accurate, and has no governor-limit cost.

### Pattern: Admin-Only Bypass in Validation Rules

**When to use:** A validation rule must enforce data quality for regular users but admins or integration users need an escape hatch without deactivating the rule.

**How it works:**
1. Create a custom permission: `Bypass_Validation_Rule_Account`.
2. Add it to the integration user's permission set.
3. Wrap the existing validation rule with an outer AND condition:

```
AND(
  NOT($Permission.Bypass_Validation_Rule_Account),
  /* original rule conditions here */
)
```

**Why not the alternative:** `$Profile.Name` is fragile — profiles get renamed and new admin profiles would require a rule update. Custom permissions decouple the bypass from profile identity entirely.

### Pattern: Conditional UI Visibility Gate in LWC

**When to use:** A button, panel, or action should only appear for users with a specific named entitlement, and server-side enforcement is required.

**How it works:**
1. Create a custom permission: `View_Refund_Controls`.
2. Expose an Apex wire adapter or `@AuraEnabled` method that returns `FeatureManagement.checkPermission('View_Refund_Controls')`.
3. In the LWC template, use `lwc:if` to conditionally render the element.
4. In the Apex action handler, repeat the check before executing any sensitive logic.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Gate a feature for a named group of users | Custom permission on a permission set | Named, auditable, toggleable without code change |
| Bypass a validation rule for integration users | `NOT($Permission.My_Permission)` as outermost AND | Decoupled from profile identity, survives renames |
| Check access in Apex | `FeatureManagement.checkPermission('ApiName')` | No SOQL, no governor limit cost, session-accurate |
| Check access in Flow | Formula resource of type Boolean: `$Permission.ApiName` | `$Permission` is only available inside formula resources |
| Check access in Visualforce | `{!$Permission.ApiName}` in rendered attribute or expression | Global merge field works natively in VF |
| Grant the permission to specific users | Add to a dedicated permission set and assign that set | Cannot assign a custom permission directly to a profile |
| Verify access in an Apex test | Assign the permission set to the test user in `@TestSetup` | `FeatureManagement.checkPermission` returns false in test context without explicit perm set assignment |

---


## Recommended Workflow

1. **Answer the seven questions above** and fill `templates/custom-permissions-template.md`. The consumer list you produce there is the input to every later step; if the permission's purpose needs an "and", split it into two permissions now.
2. **Baseline the existing grants.** Run the `SetupEntityAccess` -> `PermissionSetAssignment` query in `references/metadata-examples.md` for the permission (or for `SetupEntityType = 'CustomPermission'` org-wide) and read `PermissionSet.IsOwnedByProfile` — profile-borne grants will not show up anywhere else (`references/gotchas.md` Gotcha 1).
3. **Author the `.customPermission-meta.xml`** from the matching shape in `references/metadata-examples.md` (feature flag, bypass, dependent, or connected-app). Write a `description` that names the consumers; leave `isLicensed` out entirely — it is read-only (Gotcha 7).
4. **Author the grant** as a `<customPermissions>` node in a permission set, not a profile. For a bypass, decide expiry here and use `admin/permission-set-expiration` if the grant is temporary.
5. **Write each consumer in its own syntax** — `NOT($Permission.X)` for validation rules (contract in `templates/admin/validation-rule-patterns.md`), a Boolean formula resource for Flow, `FeatureManagement.checkPermission('X')` for Apex, `@salesforce/customPermission/X` for LWC, and `{!$Permission.CustomPermission.X}` for component visibility. The last one is the one that gets copied wrong (Gotcha 6).
6. **Lint, then validate.** Run `python3 skills/admin/custom-permissions/scripts/check_custom_permissions.py --manifest-dir <dir>` — it flags dangling grants as ERROR, missing `requiredPermission` targets, empty descriptions, and `$Permission.X` / `checkPermission('X')` references to permissions absent from the tree. Then `sf project deploy validate`, deploying definitions before grants before consumers.
7. **Verify in the org and record the evidence.** Re-run the `SetupEntityAccess` query and keep the result as the access-review artifact; a metadata diff cannot prove a revocation (Gotcha 8). Work the Review Checklist below.

---

## Review Checklist

- [ ] Custom permission API name starts with a letter and contains only alphanumeric characters and underscores.
- [ ] Permission is added to at least one permission set (not directly to a profile).
- [ ] All platform contexts that check the permission use the correct syntax for their context.
- [ ] Apex unit tests assign the permission set to the test user via `System.runAs` and a `PermissionSetAssignment` insert.
- [ ] Validation rule bypass uses `NOT($Permission.X)` as an outer AND condition so the original rule logic is preserved.
- [ ] The custom permission metadata file and updated permission set XML are committed to source control.
- [ ] `check_custom_permissions.py` has been run on the metadata directory and reports no ERROR.
- [ ] Every custom permission has a non-empty `description` naming its consumers.
- [ ] `description` is under 255 characters (`CP-DESC-01` ERROR) and ideally under 200 (`CP-DESC-02` INFO, headroom only) — if the consumer list alone does not fit, split the permission rather than compressing it.
- [ ] `isLicensed` does not appear in any authored `.customPermission-meta.xml` (it is read-only).
- [ ] Component visibility filters use `{!$Permission.CustomPermission.X}`, not the formula spelling.
- [ ] Any `requiredPermission` target ships in the same deployment package as its parent.
- [ ] Grants were verified in the org with the `SetupEntityAccess` query, and `IsOwnedByProfile` was checked for hidden profile grants.

---

## Salesforce-Specific Gotchas

1. **Grant through permission sets, not profiles — but know that a profile grant deploys** — `Profile.customPermissions` exists in the Metadata API from version 31.0, the same version as the permission set element. A profile-borne grant is real and is invisible in the Custom Permissions related list. Full detail in `references/gotchas.md` Gotcha 1.

2. **Apex test classes do not inherit the running user's real permission sets** — `FeatureManagement.checkPermission()` returns `false` in test context unless you explicitly create the permission set, add the custom permission to it, and assign it to the test user with a `PermissionSetAssignment` record inside `System.runAs`. Skipping this causes false-passing tests in development environments that have the permission set already assigned.

3. **`$Permission` in Flow is only available inside formula resources** — it cannot be typed directly into a Decision element condition row. Create a formula resource (type: Boolean) with value `$Permission.My_Permission`, then reference that resource in the Decision element.

4. **API name changes break all references without warning** — renaming a custom permission does not cascade to validation rules, formula fields, or Apex code. Formulas referencing the old name silently evaluate to `false`; Apex code fails at deploy time if the reference is in a compile-time string but may silently fail at runtime in dynamic contexts. Treat the API name as immutable once the permission is in production.

5. **A `description` over 255 characters fails the deploy** — the consumer list (the only place it survives, Gotcha 9) plus any rationale text overflows the Metadata API's 255-character `CustomPermission.description` limit fast; `scripts/check_custom_permissions.py` flags it (`CP-DESC-01` ERROR at 255+, `CP-DESC-02` INFO headroom at 200+) before the deploy does.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Custom permission metadata | `CustomPermission` XML file deployable via SFDX or Metadata API |
| Permission set update | Updated `.permissionset-meta.xml` containing the `<customPermissions>` node |
| Apex guard clause | `FeatureManagement.checkPermission` call wrapped in a helper method with test coverage pattern |
| Validation rule expression | `NOT($Permission.X)` bypass wrapper for existing validation rule formulas |
| Checker report | Output of `check_custom_permissions.py`: coverage table, ERROR on dangling grants, WARN on missing dependency targets, empty descriptions, and undefined `$Permission` / `checkPermission` references |
| Access evidence | `SetupEntityAccess` -> `PermissionSetAssignment` result set, timestamped, from `references/metadata-examples.md` |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing or reviewing the deployable XML, package.xml, deploy order, or the `SetupEntityAccess` verification queries |
| `references/gotchas.md` | A permission "isn't working", a grant cannot be explained, or a metadata diff is being used as access evidence |
| `references/examples.md` | Working an end-to-end scenario: beta gate, validation-rule bypass, or the Apex test-setup pattern |
| `references/well-architected.md` | Justifying custom permission vs custom setting vs permission set license, or citing the source behind a claim |
| `references/llm-anti-patterns.md` | Reviewing AI-generated custom permission guidance before it ships |
| `templates/custom-permissions-template.md` | Starting a task — capture the API name, consumer list, and grant plan before authoring metadata |

---

## Related Skills

- `admin/permission-set-architecture` — use when the question is how to structure permission sets and groups, not how to create or check a custom permission.
- `admin/permission-sets-vs-profiles` — use when deciding whether a grant belongs on a profile at all; owns the migration argument behind Gotcha 1.
- `admin/permission-set-expiration` — use when a bypass or pilot grant must expire on a date rather than be remembered.
- `admin/validation-rules` — use when validation rule logic is the primary concern and the custom permission is only the bypass mechanism; owns the `NOT($Permission.X)` bypass contract with `templates/admin/validation-rule-patterns.md`.
- `admin/dynamic-forms-and-actions` — use for field and component visibility rules; owns the `{!$Permission.CustomPermission.X}` filter syntax.
- `admin/in-app-guidance-and-walkthroughs` — use for prompts and walkthroughs; owns `uiFormulaRule` targeting on custom permissions.
- `admin/flow-for-admins` — use when the check happens inside a Flow; owns the Boolean formula-resource pattern.
- `apex/apex-custom-permissions-check` — use when the gate lives in Apex or LWC; owns `FeatureManagement.checkPermission`, the `@salesforce/customPermission` import, managed-package namespacing, and the test patterns.
- `security/security-health-check` — use when auditing org-wide access and permission hygiene at scale.
