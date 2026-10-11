---
name: custom-permissions
description: "Use when creating, assigning, or checking custom permissions to control feature access beyond CRUD and FLS. Trigger keywords: 'custom permission', 'FeatureManagement.checkPermission', '$Permission global variable', 'feature gate', 'named access grant', 'beta feature flag'. NOT for permission sets (use permission-set-architecture)."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - User Experience
triggers:
  - "how do I check a custom permission in Apex or a validation rule"
  - "I want to gate a feature so only certain users can see or use it"
  - "how do I use $Permission in a formula field or flow"
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
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Custom Permissions

Use this skill when a feature or capability needs a named access gate that goes beyond object, field, or record permissions. Custom permissions grant boolean access to a named capability and can be checked in validation rules, formula fields, Apex, Flow, Visualforce, and Connected App policies.

---

## Before Starting

- Confirm you need a custom permission, not a permission set feature license or a record-level sharing rule. Custom permissions are for feature on/off gates, not record visibility.
- Identify all platform contexts that must check the permission (validation rule, formula, Apex, Flow). Each uses a different syntax.
- Gather the exact API name you want. API names must start with a letter and may only contain letters, digits, and underscores. The name cannot be changed after creation without updating every reference.
- Determine which permission sets will carry the permission. Custom permissions cannot be assigned directly to profiles — they must ride inside a permission set.

---

## Core Concepts

### What Custom Permissions Are

Custom permissions are named boolean access grants. Unlike CRUD, FLS, and tab access, they carry no implicit meaning to the platform — they exist solely so developers and admins can build their own feature gates. Each custom permission has a label and an API name and can optionally be tied to a Connected App. When granted, the permission evaluates to `true` in every supported context for that running user's session.

Source: Salesforce Help — [Custom Permissions Overview](https://help.salesforce.com/s/articleView?id=sf.custom_perms_overview.htm)

### Creating Custom Permissions

Custom permissions are created in **Setup > Custom Permissions**. Click **New**, enter a label and an API name, then optionally provide a description and a Connected App association.

Key constraints on the API name:
- Must begin with a letter (not a digit or underscore).
- Only alphanumeric characters and underscores are allowed.
- Cannot end with a double underscore followed by a letter (reserved for managed packages).
- Cannot be changed after the permission is referenced in production without a coordinated update of all dependent metadata and code.

The `CustomPermission` metadata type is supported by the Metadata API and SFDX source format. The file lives at `customPermissions/My_Custom_Permission.customPermission-meta.xml`.

### Assigning Custom Permissions to Permission Sets

Custom permissions live in permission sets, not profiles. In Setup, open a permission set, navigate to **Custom Permissions**, and enable the desired permission. In the Metadata API, the permission set XML includes a `<customPermissions>` node:

```xml
<customPermissions>
    <enabled>true</enabled>
    <name>My_Custom_Permission</name>
</customPermissions>
```

A single custom permission can appear in multiple permission sets and permission set groups. When any one of those is assigned to a user, the permission evaluates to `true` for that user.

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

**Connected Apps**

A custom permission can be required for a user to authorize a Connected App. Configure this in the Connected App definition under **Custom Permissions**. Users who lack the permission are blocked at OAuth authorization time with an `access_denied` error.

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

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Custom permission API name starts with a letter and contains only alphanumeric characters and underscores.
- [ ] Permission is added to at least one permission set (not directly to a profile).
- [ ] All platform contexts that check the permission use the correct syntax for their context.
- [ ] Apex unit tests assign the permission set to the test user via `System.runAs` and a `PermissionSetAssignment` insert.
- [ ] Validation rule bypass uses `NOT($Permission.X)` as an outer AND condition so the original rule logic is preserved.
- [ ] The custom permission metadata file and updated permission set XML are committed to source control.
- [ ] `check_custom_permissions.py` has been run on the metadata directory to confirm all permissions are covered by at least one active permission set.

---

## Salesforce-Specific Gotchas

1. **Custom permissions cannot be assigned directly to profiles** — they must live inside a permission set. If every user on a profile needs the permission, create a permission set, add the permission, and assign it to all users with that profile. This is a permanent platform constraint as of Spring '25.

2. **Apex test classes do not inherit the running user's real permission sets** — `FeatureManagement.checkPermission()` returns `false` in test context unless you explicitly create the permission set, add the custom permission to it, and assign it to the test user with a `PermissionSetAssignment` record inside `System.runAs`. Skipping this causes false-passing tests in development environments that have the permission set already assigned.

3. **`$Permission` in Flow is only available inside formula resources** — it cannot be typed directly into a Decision element condition row. Create a formula resource (type: Boolean) with value `$Permission.My_Permission`, then reference that resource in the Decision element.

4. **API name changes break all references without warning** — renaming a custom permission does not cascade to validation rules, formula fields, or Apex code. Formulas referencing the old name silently evaluate to `false`; Apex code fails at deploy time if the reference is in a compile-time string but may silently fail at runtime in dynamic contexts. Treat the API name as immutable once the permission is in production.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Custom permission metadata | `CustomPermission` XML file deployable via SFDX or Metadata API |
| Permission set update | Updated `.permissionset-meta.xml` containing the `<customPermissions>` node |
| Apex guard clause | `FeatureManagement.checkPermission` call wrapped in a helper method with test coverage pattern |
| Validation rule expression | `NOT($Permission.X)` bypass wrapper for existing validation rule formulas |
| Checker report | Output of `check_custom_permissions.py` showing perm-set-to-permission assignments and orphaned permissions |

---

## Related Skills

- `admin/permission-set-architecture` — use when the question is how to structure permission sets and groups, not how to create or check a custom permission.
- `admin/validation-rules` — use when validation rule logic is the primary concern and the custom permission is only the bypass mechanism.
- `security/security-health-check` — use when auditing org-wide access and permission hygiene at scale.
