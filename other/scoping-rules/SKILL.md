---
name: scoping-rules
description: "Use when setting the default filtered set of records a user sees in list views, reports and SOQL without removing their access. Trigger keywords: scoping rule, Filter by scope, default record scope, RestrictionRule enforcementType Scoping, Object Manager scoping rule, recordFilter. NOT for the SOQL USING SCOPE clause - use apex/soql-using-scope-clause. NOT for blocking record access - use admin/restriction-rules."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Performance
  - Security
triggers:
  - "how do I make reps see only their own branch's accounts by default without taking away access"
  - "why can my user still open a record that my scoping rule filtered out"
  - "set the default list view scope so support agents only see their department's contacts"
  - "what is the difference between a scoping rule and a restriction rule in Salesforce"
  - "my scoping rule has no effect on the list view and nothing is filtered"
  - "how do I deploy a scoping rule between sandbox and production"
  - "can a scoping rule be used to hide records from a user for compliance"
  - "why does my scoping rule SOQL operator get rejected without USING SCOPE EVERYTHING"
tags:
  - scoping-rules
  - restriction-rule
  - record-visibility
  - list-views
  - filter-by-scope
  - record-filter
  - user-criteria
inputs:
  - "Target object: which of the seven supported standard objects (Account, Case, Contact, Event, Lead, Opportunity, Task) or which custom object the default scope applies to"
  - "The record-side criterion: the field on the target object that identifies 'relevant to this user', and whether its value can be derived from a User field or needs a SOQL subquery through a junction object"
  - "The user-side criterion: which subset of users the rule applies to, expressed as a filter on User fields (role, profile, department, IsActive, custom permission)"
  - "Whether any user could ever be matched by two rules on the same object — the platform supports only one scoping or restriction rule per object per user"
  - "Org edition, because the active-rules-per-object cap differs between Developer and Performance/Unlimited"
  - "Which list views and reports should ship with Filter by scope already turned on, and who owns switching it"
outputs:
  - "A deployable RestrictionRule metadata file with enforcementType Scoping, recordFilter, userCriteria and targetEntity"
  - "A package.xml fragment naming the RestrictionRule type and the restrictionRules/ directory layout"
  - "A per-org ID remapping list for any role, profile, record type or user ID hardcoded in the criteria"
  - "The list of list views (filterScope ScopingRule) and reports (scope) that must be updated for the rule to be visible to users"
  - "A written statement of whether the requirement is a focus requirement or an access requirement, and the redirect to admin/restriction-rules when it is the latter"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-08-15
---

# Scoping Rules

This skill activates when the requirement is "these users should *land on* a smaller set of records by default" — a focus and productivity requirement, not an access requirement. A scoping rule narrows what a user sees first in list views, reports and SOQL; it removes nothing. The user can switch scope and reach every record their sharing model already gave them.

Two names collide around this feature and both cause real misroutes. The Setup feature is a scoping rule. The SOQL `USING SCOPE` clause is a query modifier — see `apex/soql-using-scope-clause`. They meet at exactly one point (`USING SCOPE scopingRule`) and are otherwise unrelated. The sibling feature that actually blocks access is a restriction rule — see `admin/restriction-rules`.

---

## Before Starting

Gather this context before touching anything:

- **Is this a focus requirement or an access requirement?** Ask the stakeholder what should happen when the user deliberately looks. If the answer is "they'd see it, that's fine, we just don't want it cluttering their view" — scoping rule. If the answer is "they must not see it" — stop, this is the wrong skill, go to `admin/restriction-rules` or the sharing model. Salesforce is unambiguous: scoping rules "don't restrict the access that your users have to records. Your users can still open and report on all the records that they can access according to your org's sharing settings."
- **Which object?** Scoping rules are supported on "custom objects and the account, case, contact, event, lead, opportunity, and task standard objects." Nothing else. There is no scoping rule on Order, Campaign, Asset, or Knowledge.
- **What edition is the org?** The feature is "Available in: Lightning Experience in Performance, Unlimited, and Developer editions." Classic is out. Enterprise is not listed for scoping rules even though it is listed in the restriction-rule limits — confirm against the target org before promising the feature.
- **Who has the permission?** Creating and managing scoping rules requires **Manage Sharing**. Viewing them requires **View Setup and Configuration** *and* **View Restriction and Scoping Rules**. An admin with a full-access profile will not notice this; a delegated admin will.
- **Can two rules ever match the same user?** Salesforce states: "Create only one scoping or restriction rule per object per user." This is a design constraint you satisfy in `userCriteria`, not a validation the platform enforces for you. Overlapping `userCriteria` across a scoping rule and a restriction rule on the same object counts as a violation.
- **Does the criterion need a subquery?** A simple field-to-User-field comparison (`Department=$User.Department`) can be built in Object Manager. Anything that has to hop through a junction object needs the SOQL operator, and "you can use a SOQL operator in record criteria only when creating scoping rules via the API."

---

## Core Concepts

### There is no `ScopingRule` metadata type

This is the single most common authoring error. A scoping rule is a `RestrictionRule` with `enforcementType` set to `Scoping`. There is no separate metadata type, no separate Tooling API object, and no `scopingRules/` folder.

```xml
<!-- force-app/main/default/restrictionRules/SR_Department_A_Contacts.rule-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<RestrictionRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <active>true</active>
    <description>View contacts from Department A.</description>
    <enforcementType>Scoping</enforcementType>
    <masterLabel>SR for Department A contacts</masterLabel>
    <recordFilter>Department=$User.Department</recordFilter>
    <targetEntity>Contact</targetEntity>
    <userCriteria>$User.UserRoleId = '00Exxxxxxxxxxxx'</userCriteria>
    <version>1</version>
</RestrictionRule>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <types>
    <members>*</members>
    <name>RestrictionRule</name>
  </types>
  <version>67.0</version>
</Package>
```

The file suffix is `.rule` and the directory is `restrictionRules`. `RestrictionRule` is available in Metadata API and Tooling API version 52.0 and later.

| Field | Required | Notes |
|---|---|---|
| `enforcementType` | Yes | `Scoping` for a scoping rule. The other documented values are `Restrict` (a restriction rule — a different feature) and `FieldRestrict`, which the reference marks "Don't use". |
| `targetEntity` | Yes | The object being scoped. Salesforce advises against editing this after creation; delete and recreate instead. |
| `recordFilter` | Yes | The record-side criterion. Supports boolean, date, dateTime, double, int, reference, string, time, and single picklist values. |
| `userCriteria` | Yes | The user-side criterion. Determines *who* the rule applies to. |
| `masterLabel` | Yes | Rule label. |
| `description` | Yes | Documented as required, unlike on most metadata types. Generators trim it for brevity; do not. |
| `active` | No | Defaults to `false`. Omitting it and then wondering why nothing filtered is one of the two standard "my rule does nothing" causes; the other is the list-view wiring below. |
| `version` | Yes | Integer rule version. |

The equivalent Tooling API payload wraps the same fields under `Metadata`, with `FullName` alongside:

```json
{
    "FullName":"Department A contact scoping rule",
    "Metadata": {
         "active":true,
         "description":"View contacts from Department A.",
         "enforcementType":"Scoping",
         "masterLabel":"SR for Department A",
         "recordFilter":"Department=$User.Department",
         "targetEntity":"Contact",
         "userCriteria":"$User.UserRoleId = '00Exxxxxxxxxxxx'",
         "version":1
    }
}
```

### Scoping rule vs restriction rule

Both are `RestrictionRule`. They differ in `enforcementType`, in which objects they support, and — decisively — in how many surfaces they reach.

| Aspect | Scoping rule (`enforcementType: Scoping`) | Restriction rule (`enforcementType: Restrict`) |
|---|---|---|
| Effect on access | None. The user can still open and report on everything sharing gave them | Removes access to non-matching records |
| Surfaces reached | List Views, Reports, SOQL — three, per the official surface table | "Links, List Views, Lookups, Records, Related Lists, Reports, Search, SOQL, SOSL" |
| Applied by default | Only in SOQL. List views and reports require **Filter by scope** to be selected | Always, wherever the rule applies |
| User can turn it off | Yes — that is the point | No |
| Supported objects | Custom objects plus Account, Case, Contact, Event, Lead, Opportunity, Task | Custom objects, external objects, Contract, Event, Quote, Task, TimeSheet, TimeSheetEntry |
| Operators in criteria | The same single operator: "Unless you use SOQL, scoping rules support only the EQUALS operator. The AND and OR operators aren't supported." The SOQL operator is the only way past that, and it is API-only | "Restriction rules support only the EQUALS operator. The AND, OR, or any other operators aren't supported" |
| Is it a security control | No | Yes, with caveats — it is not applied to code running in system mode, and View All Records / View All Data override it |

Note the object lists barely overlap: Account, Case, Contact, Lead and Opportunity can be scoped but not restricted; Contract, Quote, TimeSheet and external objects can be restricted but not scoped. Event and Task are the only standard objects on both lists.

### Where the scope actually applies

Salesforce publishes a three-row surface table, and the rows are not the same shape:

| Feature | Behaviour |
|---|---|
| List Views | "Applied in Lightning Experience if **Filter by scope** is selected" |
| Reports | "Applied in Lightning Experience if **Filter by scope** is selected" |
| SOQL | "Applied, unless a scope other than scopingRule is specified" |

Two consequences fall straight out of this and both are counterintuitive.

First, **a correctly built, active scoping rule changes nothing a user can see until someone selects Filter by scope**. The `ListView` metadata type's `filterScope` enumeration spells it out: the `ScopingRule` value means "Records that meet a scoping rule's record criteria. In Lightning Experience, scoping rules are applied to list views only if the user selects **Filter by scope**." You wire this up as configuration — "for list views and reports, you can apply the scope through Metadata API (using the filterScope field on the ListView type and the scope field on the Report type)".

Second, **SOQL is the surface where the scope is on by default**. `USING SCOPE` carries a `scopingRule` value — "Filter for records based on the applicable scoping rule. This option is available if an admin has activated at least one scoping rule on the object." Confirm support for a given object by reading `supportedScopes` from `describeSObject()` (SOAP) or the sObject Describe REST endpoint. That default-on behaviour is why the rule's own SOQL operator has to opt out, which is the next concept.

Search and SOSL are absent from the table. Restriction rules name Search and SOSL explicitly; the scoping table does not. Do not promise a stakeholder that global search will be scoped.

### Criteria syntax: `recordFilter` and `userCriteria`

The criteria language is much narrower than it looks. Outside the SOQL operator there is exactly one operator: "Unless you use SOQL, scoping rules support only the EQUALS operator. The AND and OR operators aren't supported." A two-condition requirement — region *and* open status — has no declarative form; fold the second condition into a formula field the criterion can equal, or move to the SOQL operator and the API. The one multi-value affordance is the comma: "Comma-separated ID or string values are supported in the Record Criteria field." Null and blank values are out too — "including a null or blank value in record criteria isn't supported and can result in unexpected behavior".

Simple comparison form, buildable in Object Manager:

```text
recordFilter:  Department=$User.Department
userCriteria:  $User.UserRoleId = '00Exxxxxxxxxxxx'
```

Multiple values are comma-separated on the right-hand side, and a double-quoted segment protects a literal comma inside a value:

```text
recordFilter:  Name__c='Tom, Anita, "Torres, Jia"'
recordFilter:  Agent__c.Owner:User.ManagerId=001xx000003HNy7, 001xx000003HNut
userCriteria:  $User.IsActive=true
```

Note `Owner:User` — an owner reference must carry its type, because `OwnerId` is polymorphic. Dot-notation lookups are limited to one level.

SOQL operator form, for when the relationship needs a junction hop. This is API-only — Object Manager will not build it:

```text
SOQL(Id, SELECT AccountId FROM BranchUnitCustomer USING SCOPE EVERYTHING WHERE BranchUnitId IN(SELECT CurrentBranchId From Banker WHERE UserOrContactId = $User.Id))
```

The rules that govern that string:

| Constraint | Statement |
|---|---|
| Left operand | "The left operand must query a single ID (primary key) or reference (foreign key) field" from the target entity |
| Scope clause | "The SELECT statement, including nested SELECT statements, must include USING SCOPE EVERYTHING" |
| Valid scope | "USING SCOPE EVERYTHING is the only valid scope clause syntax for scoping rules" |
| User variable | "The SOQL operator doesn't support $User syntax except for $User.Id" |
| Object identity | "In SOQL operators, the SOQL query object and the scoping rule target entity can't be the same object" |
| Objects barred from the subquery | "These objects aren't supported in the SOQL operator": ActivityHistory, Attachments, Event, EventAttendee, Note, OpenActivity, tag objects, Task. Event and Task are scopeable *target entities* and still cannot appear inside the operator |

`USING SCOPE EVERYTHING` is mandatory in every nested `SELECT` for a reason that follows from the surface table: SOQL is scoped by default when an active scoping rule exists, so a subquery inside the rule's own criteria would be filtered by the rule it is defining. `EVERYTHING` breaks that recursion.

---

## Common Patterns

### Pattern: user-attribute scoping (no subquery)

**When to use:** the "relevant to me" value already lives on both the record and the User record — department, division, region, branch code, a custom `Territory__c` text field.

**How it works:**

1. Confirm the field exists on the target object and the matching field exists on User. Both must be one of the supported data types (boolean, date, dateTime, double, int, reference, string, time, or single picklist value).
2. In Setup, open Object Manager → the object → Scoping Rules → New. Set the record criteria to `Field = $User.Field`.
3. Set user criteria narrowly enough that no user is matched by any other scoping or restriction rule on that object.
4. Save the rule inactive, deploy, then activate.
5. Update the relevant list views to `filterScope` `ScopingRule` and the relevant reports' `scope` so users land on the scoped view rather than having to find the toggle.

**Why not a sharing change:** an OWD tightening or a restriction rule would take the records away. The stakeholder asked for a cleaner default view, not for a wall. Removing access to solve a clutter problem is the error this whole feature exists to avoid.

### Pattern: junction-hop scoping (SOQL operator)

**When to use:** the relationship is indirect — a banker is assigned to a branch, the branch is linked to accounts through `BranchUnitCustomer`; a specialist is assigned to a product line, the product line reaches Opportunity through a junction.

**How it works:**

1. Write the subquery standalone first and run it in an API client as the target user. If it is slow standalone, it will be slow as a rule.
2. Wrap it: `SOQL(<target ID or reference field>, <SELECT … USING SCOPE EVERYTHING …>)`.
3. Add `USING SCOPE EVERYTHING` to every nested `SELECT`, not only the outer one.
4. Deploy through Tooling API or Metadata API — Object Manager cannot express this.
5. Test with a user who matches `userCriteria` and a user who does not, and confirm the second user's view is unchanged.

**Why not build it in Setup:** the Object Manager editor produces comparison criteria only. Attempting to paste a `SOQL(...)` string into the Setup UI is not a supported path.

### Pattern: user-switchable scope via the utility bar

**When to use:** the same user legitimately works in more than one scope — a banker covering two branches, a rep covering two territories — and needs to move between them without an admin.

**How it works:** Salesforce's documented approach is a Flow surfaced in the Lightning Utility Bar: "You can set up a flow that your users access using the Lightning Utility Bar to set the scope of records that the user sees in list views, reports, and other features." The Flow writes the user-side value (for example a `Current_Branch__c` field on User) that `recordFilter` compares against; the rule itself never changes.

**Why not one rule per branch:** the per-object active-rule cap is low (two in Developer editions, five in Performance and Unlimited editions), and a user matched by two rules on the same object violates the one-rule-per-object-per-user constraint. One parameterised rule plus a mutable user attribute scales; N rules does not.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| "Reps shouldn't have to scroll past other regions' accounts" | Scoping rule on Account | Focus requirement — access is not in question |
| "Reps must not be able to see other regions' accounts" | `admin/restriction-rules` or tighten OWD/sharing | Scoping rules remove nothing; a user can switch scope |
| Auditor or regulator asks for enforced record segregation | Sharing model, then `admin/restriction-rules` | A control the user can switch off is not a control |
| Need to filter one Apex query to a subset | `apex/soql-using-scope-clause` | A query modifier, not a Setup feature — no rule needed |
| Object is Order, Campaign, Asset, Quote, or Contract | Not a scoping rule | Outside the supported object list |
| Criterion is `Contact.Department = User.Department` | Object Manager scoping rule | Simple comparison; no API needed |
| Criterion needs a junction object hop | Tooling or Metadata API with the SOQL operator | The SOQL operator is API-only |
| More than five scopes needed on one object | One parameterised rule + a mutable User field | The per-object active-rule cap is edition-bound |
| The record set is enormous and the criteria are expensive | Test in a full sandbox first | "Salesforce reserves the right to disable a scoping rule if a rule you create is inefficient or if your data model has so much data that scoping rules cause slowness when applied" |
| Rule is built and active but users see no change | Check **Filter by scope** on the list view / report | List views and reports are opt-in; SOQL is not |

---

## Recommended Workflow

1. **Classify the requirement.** Ask whether the user is allowed to see the excluded records if they go looking. "Yes, we just want a cleaner default" → continue here. "No" → stop and route to `admin/restriction-rules`, and say plainly that a scoping rule would not satisfy the requirement.
2. **Verify feasibility.** Confirm the target object is one of the seven supported standard objects or a custom object, confirm the org is Performance, Unlimited, or Developer edition on Lightning Experience, and confirm the acting identity holds **Manage Sharing**.
3. **Design the two criteria.** Write `recordFilter` and `userCriteria` as literal strings. Decide at this point whether a single EQUALS comparison suffices or the SOQL operator is required — AND and OR do not exist outside the SOQL operator — because that decision also determines whether the rule can be built in Object Manager at all. Check every referenced field against the supported data-type list and the one-level dot-notation limit.
4. **Prove no user is double-matched.** Enumerate the other active scoping and restriction rules on the same object and confirm their `userCriteria` are disjoint from yours. One scoping or restriction rule per object per user is the platform's stated constraint, and overlap produces unpredictable behaviour rather than an error.
5. **Build inactive, deploy, then activate.** Author the `.rule` file under `restrictionRules/` with `active` set to `false`, deploy it, remap any hardcoded role, profile, record type or user IDs for the destination org, then activate. Deploying active skips the remap window.
6. **Wire the surfaces.** Set `filterScope` to `ScopingRule` on the list views that should default to the scope, set `scope` on the reports, and confirm with an affected user. Without this the rule is live and invisible.
7. **Run the checker and review the gotchas.** Run `python3 skills/admin/scoping-rules/scripts/check_scoping_rules.py --manifest-dir <metadata-dir>`, then read `references/gotchas.md` before sign-off — the deactivation ordering trap and the org-ID portability trap both bite after deployment, not during it.

---

## Review Checklist

- [ ] The requirement was classified as focus, not access, and that classification is written down where the stakeholder can see it
- [ ] `enforcementType` is `Scoping`, and the file lives in `restrictionRules/` with a `.rule` suffix
- [ ] `description` is populated — it is a required field, not documentation
- [ ] `targetEntity` is on the scoping-supported object list, and has not been edited since creation
- [ ] `userCriteria` cannot match a user who is also matched by another scoping or restriction rule on the same object
- [ ] Active rule count on the object is within the edition cap (two in Developer, five in Performance and Unlimited)
- [ ] Every `SELECT` and nested `SELECT` inside a SOQL operator carries `USING SCOPE EVERYTHING`
- [ ] No `$User` reference other than `$User.Id` appears inside a SOQL operator
- [ ] Owner references are typed (`Owner:User`, not bare `Owner`) and no lookup path exceeds one level
- [ ] Every hardcoded 15/18-character ID in the criteria has been remapped for the destination org
- [ ] The list views and reports that should default to the scope have `filterScope` / `scope` set, and this was verified by logging in as an affected user
- [ ] Query performance was measured in a full sandbox with production-scale data, not in a scratch org
- [ ] A rollback plan exists that deletes or re-points every list view and report with **Filter by scope** selected *before* the rule is disabled — once it is disabled they are "neither functional nor modifiable"

---

## Salesforce-Specific Gotchas

Short form; the mechanism and the recovery for each are in `references/gotchas.md`.

1. **A live rule that filters nothing** — list views and reports only honour a scoping rule when **Filter by scope** is selected, so a correctly built, active rule is invisible until the views are wired up.
2. **Disabling the rule strands its dependents** — "To disable a scoping rule, first delete the list views and reports that have **Filter by scope** selected. After a scoping rule is disabled, the list views and reports aren't functional nor modifiable." Unwind the surfaces first; there is no repair afterwards.
3. **Hardcoded org IDs do not survive promotion** — role, profile and record type IDs embedded in `userCriteria` or `recordFilter` differ per org and must be remapped on every hop.
4. **Salesforce can switch your rule off** — inefficient criteria or an oversized data model give Salesforce the documented right to disable the rule, and nothing in Setup announces it.
5. **`targetEntity` is effectively immutable** — Salesforce advises deleting and recreating rather than editing it, which means a new rule name and a fresh pass over every list view that referenced the old one.
6. **Scoping quietly narrows duplicate detection** — potential duplicates are limited by scope even when the duplicate rule has *Bypass sharing rules* turned on.
7. **One operator, no AND, no OR** — outside the SOQL operator the criteria language supports only EQUALS, so a two-condition requirement needs a formula field or the API path.
8. **The scope stops at the target object** — a rule on one object doesn't affect child objects, related lists stay unscoped apart from the contact role related list, and Event and Task cannot be queried inside a SOQL operator even though both are scopeable target entities.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `.rule` metadata file | `RestrictionRule` with `enforcementType: Scoping`, ready to deploy under `restrictionRules/` |
| `package.xml` fragment | `<name>RestrictionRule</name>` types block for retrieve and deploy |
| Tooling API payload | JSON body with `FullName` and a `Metadata` block, for orgs where a Setup-free path is preferred |
| Surface wiring list | The list views (`filterScope` = `ScopingRule`) and reports (`scope`) that must change for users to see the effect |
| ID remap table | Every org-specific ID in the criteria, with its value per environment |
| Classification note | The written focus-vs-access determination, including the redirect when the answer was access |

---

## Related Skills

- `apex/soql-using-scope-clause` — the SOQL query modifier that shares the word "scope"; also the correct home for `USING SCOPE scopingRule` in a selector, and for the `USING SCOPE EVERYTHING` requirement inside a rule's SOQL operator
- `admin/restriction-rules` — the same `RestrictionRule` type with `enforcementType: Restrict`; use it when the requirement is that the user must not reach the record at all
- `admin/sharing-and-visibility` — the layer underneath: OWD, role hierarchy and sharing rules decide what a user *can* reach, which is the ceiling a scoping rule filters below
- `admin/list-views-and-compact-layouts` — where `filterScope` is set on a list view, and therefore where a scoping rule becomes visible to a user at all
