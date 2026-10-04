---
name: restriction-rules
description: "Use when narrowing access that sharing already granted. Trigger keywords: restriction rule, recordFilter, userCriteria, RestrictionRule metadata, hide records, restrict visibility. NOT for list-view scope only - use admin/scoping-rules."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Operational Excellence
triggers:
  - "how do I stop one team from seeing contracts that belong to another team"
  - "why can a user still see records after I activated a restriction rule"
  - "restrict tasks and events so reps see only the ones they own"
  - "can I use AND or OR in a restriction rule record filter"
  - "how many active restriction rules am I allowed on a single object"
  - "why does my restriction rule not apply to the integration user"
  - "deploy a restriction rule from sandbox to production"
  - "is a restriction rule enough to keep sensitive data away from a profile"
  - "restriction rule has no effect on an admin with View All Data"
tags:
  - restriction-rules
  - record-access
  - sharing
  - data-segregation
  - metadata-api
  - security
inputs:
  - "Target object API name, confirmed against the supported targetEntity list for enforcementType Restrict"
  - "Which users the rule applies to, expressed as one EQUALS test on a $User field (ProfileId, UserRoleId, IsActive, UserType)"
  - "Which records those users keep, expressed as one EQUALS test on a record field"
  - "Org edition — the active-rule ceiling differs between Enterprise/Developer and Performance/Unlimited"
  - "An inventory of who holds View All / View All Data / Modify All / Modify All Data on the object, and which Apex or integration paths run in system mode"
outputs:
  - "Deployable RestrictionRule metadata (.rule) with enforcementType, targetEntity, userCriteria, recordFilter and version"
  - "A written bypass inventory naming every documented path around the rule and who currently holds it"
  - "A test plan that proves the filter in the record UI, in a report, and in SOQL as the restricted user"
  - "A deployment plan covering change set or unlocked package delivery and cross-org Id remapping"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-08-15
---

# Restriction Rules

This skill activates when record access has to be taken *away* from users who already hold it — a compliance carve-out, a team-versus-team data wall, or a "reps see only the tasks they own" requirement. Every other layer in the sharing model grants; the restriction rule is the one that subtracts. It is also the layer most often oversold, so a large part of this skill is being precise about what it does not reach.

---

## Before Starting

Gather this before designing anything:

- **Is the object even eligible?** For `enforcementType` `Restrict`, `targetEntity` accepts `Contract`, `Event`, `Quote`, `Task`, `TimeSheet`, `TimeSheetEntry`, plus custom objects and external objects. Account, Opportunity, Case, Contact, and Lead are not on that list. If the request is "hide some Opportunities," the answer is not a restriction rule.
- **Can the requirement be written as a single EQUALS test?** The criteria language supports only the `=` operator. There is no `AND`, no `OR`, no `!=`, no formula. If the requirement needs two conditions joined, it either gets pushed into a single roll-up-style field on the record or it is not a restriction rule.
- **Who holds View All / Modify All on this object, and which code runs in system mode?** Both are documented bypasses. Enumerate them *before* you promise anyone the data is hidden, not after the audit finds it.
- **What edition is the org?** Enterprise and Developer allow up to two active restriction rules per object; Performance and Unlimited allow up to five. The ceiling counts active rules. Scoping rules have their own separate ceiling (two per object in Developer, five in Performance and Unlimited — the guide states no Enterprise number), so the two kinds do not share a budget. What they do share is the per-user constraint: only one restriction or scoping rule may apply to any given user on a given object.

---

## Core Concepts

### Subtraction, not a grant

A restriction rule never gives anyone access. Salesforce states it plainly: "When a restriction rule is applied to a user, the records that the user is granted access to via org-wide defaults, sharing rules, and other sharing mechanisms are filtered by criteria that you specify." The rule runs *after* the sharing model has produced a result set and removes rows from it. If OWD, the role hierarchy, and sharing rules never granted the record in the first place, the restriction rule is irrelevant to that record.

The practical consequence is that a restriction rule cannot fix an over-permissive OWD. It hides the symptom on a fixed list of surfaces while the underlying grant stays intact in the sharing tables, where anything that reads outside those surfaces still finds it.

### Where the filter is enforced — and where it is not

Salesforce enumerates the enforcement surfaces: **Links, List Views, Lookups, Records, Related Lists, Reports, Search, SOQL, SOSL**. That is a wide net and it covers the API, which is why restriction rules are genuinely more than a UI decoration.

It is not, however, an absolute boundary. Salesforce documents eight gaps — seven where a restricted user still reaches filtered data, and one where the platform reports as though the rule did not exist. Quote them to any stakeholder who asks for a compliance guarantee:

| Gap | What Salesforce documents |
|---|---|
| **System-mode code** | "Restriction rules aren't applied for code executed in System Mode." |
| **View All Records / View All Data** | Those users "can view all records regardless of restriction rules." |
| **Modify All Records / Modify All Data** | Those users "can view, edit, and delete all records regardless of restriction rules." |
| **`UserRecordAccess`** (audit gap, not an access path) | "The UserRecordAccess object doesn't consider whether a user's access is blocked due to a restriction rule." Access-audit tooling built on that object reports the pre-restriction answer. |
| **Calendar with Show Details** | "In calendars, if the Show Details access level is selected, users can see the subject of all events, regardless of the restriction rules created." |
| **Subordinates' calendars** | "Users can see their subordinates' events in calendars even if the users have an active restriction rule applied." |
| **Global search shortcuts** | "After restriction rules are applied, users can still see records that they previously had access to in the global search box shortcuts." |
| **Chatter publisher** | "If a user creates an event or a task record using the Chatter publisher, the record name is visible in the related Chatter post." |

Call a restriction rule a run-time visibility filter with eight documented gaps, and design accordingly. If the requirement must survive an integration user with Modify All Data or a `without sharing` class, the answer is a tighter OWD plus removal of whichever sharing layer granted the access — see `admin/sharing-and-visibility`. `references/gotchas.md` works through what each gap looks like in production.

### The criteria language is one EQUALS test on each side

`userCriteria` picks the audience; `recordFilter` picks what that audience keeps. Both are strings, both are limited to `=`, and both are evaluated at query time.

| Constraint | Detail |
|---|---|
| Operators | "Restriction rules support only the EQUALS operator." "The AND, OR, or any other operators aren't supported." |
| Formulas | "The use of formulas isn't supported." |
| Data types | boolean, date, dateTime, double, int, reference, string, time, and single picklist. Custom picklist values are supported in both record and user criteria — but "if you delete a custom picklist value used in a restriction rule, the rule no longer works as intended." |
| Ids | "If you reference IDs in the `recordFilter` field, use 15-character IDs instead of 18-character IDs." |
| Multi-value | Comma-separated Id or string values are supported in record criteria. Double quotes mark a value whose internal comma is not a delimiter: `Name__c='Tom, Anita, "Torres, Jia"'`. |
| Null | "Including a null or blank value in record criteria isn't supported and can result in unexpected behavior." |
| Traversal | Dot notation reaches another object's field, but only one hop: "You can use only one 'dot' (one lookup level from the targetEntity)." Referencing `Owner` requires naming the object type: `Owner:User.ProfileId`, not `Owner.ProfileId`. |
| Lookups | "If a restriction rule's record criteria uses a lookup field and the related record doesn't exist, access isn't granted." |

Working `recordFilter` / `userCriteria` pairs straight from the Salesforce examples:

| Intent | `recordFilter` | `userCriteria` | `targetEntity` |
|---|---|---|---|
| Reps see only tasks they own | `OwnerId = $User.Id` | `$User.ProfileId = '00exxxxxxxxxxxx'` | `Task` |
| Events owned by the same role | `Owner:User.UserRoleId = $User.UserRoleId` | `$User.IsActive = true` | `Event` |
| Events owned by the same profile | `Owner:User.ProfileId = $User.ProfileId` | `$User.IsActive = true` | `Event` |
| Portal users see their department's contracts | `Department__c = $User.Department` | `$User.UserType = 'CSPLitePortal'` | `Contract` |
| One record type of task only | `recordTypeId = '011xxxxxxxxxxxx'` | `$User.ProfileId = '00exxxxxxxxxxxx'` | `Task` |

### The metadata shape

`RestrictionRule` is one metadata type serving both mechanisms: suffix `.rule`, directory `restrictionRules`, available in API version 52.0 and later. `enforcementType` decides which mechanism you get.

```xml
<!-- restrictionRules/Tasks_You_Own.rule -->
<?xml version="1.0" encoding="UTF-8"?>
<RestrictionRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <active>true</active>
    <description>Allows users with a specific profile to see only tasks that they own.</description>
    <enforcementType>Restrict</enforcementType>
    <masterLabel>Tasks You Own</masterLabel>
    <recordFilter>OwnerId = $User.Id</recordFilter>
    <targetEntity>Task</targetEntity>
    <userCriteria>$User.ProfileId = '00exxxxxxxxxxxx'</userCriteria>
    <version>1</version>
</RestrictionRule>
```

| Field | Value | Notes |
|---|---|---|
| `enforcementType` | `Restrict` | Documented enum values are `Restrict`, `Scoping`, and `FieldRestrict`. `Scoping` produces a scoping rule from the same file — see `admin/scoping-rules`. The reference marks the third one "FieldRestrict—Don't use."; it parses and deploys anyway, so the checker flags it. |
| `targetEntity` | `Task` | Restricted to the supported object list. "We recommend that you don't edit the `targetEntity` field after the restriction rule is created." |
| `userCriteria` | `$User.ProfileId = '00e…'` | Required. One EQUALS test. Org-specific Ids here must be remapped on deployment. |
| `recordFilter` | `OwnerId = $User.Id` | Required. One EQUALS test. 15-character Ids. |
| `active` | `true` | Optional, defaults to `false`. Only `true` rules count against the per-object ceiling. |
| `version` | `1` | Required int. |
| `description`, `masterLabel` | strings | Both required by the metadata type. |

Managing these rules requires the **Manage Sharing** permission (view, create, update, delete). The **View Restriction and Scoping Rules** permission grants read-only visibility through the API. The Tooling API exposes the same object with `IsActive`, `DeveloperName`, `RecordFilter`, `TargetEntity`, `UserCriteria` and `EnforcementType` fields at `POST /services/data/vXX.0/tooling/sobjects/RestrictionRule`.

---

## Common Patterns

### Pattern: own-records-only on Task or Event

**When to use:** activity data carries client detail that must not spread laterally across a shared services team, and the org's activity sharing setting is too coarse to express it.

**How it works:** set `userCriteria` to the profile that must be constrained and `recordFilter` to `OwnerId = $User.Id`. Every other layer keeps working — managers above the user in the hierarchy are unaffected unless a second rule targets them too, because a rule only applies to users its `userCriteria` matches.

**Why not tighten activity sharing instead:** activity access settings are org-wide and blunt; the restriction rule constrains exactly one profile and leaves everyone else on the existing model.

**What breaks:** the Open Activities and Activity History related lists behave badly under restriction rules — Salesforce recommends the Activity Timeline instead, because those related lists can show "fewer than 50 records ... when more activities exist that the user has access to." Plan the page layout change with the rule, not after it.

### Pattern: department-scoped Contract visibility for external users

**When to use:** Experience Cloud users on a high-volume licence should see only the contracts for their own department, and sharing sets are granting a wider set.

**How it works:** `userCriteria` of `$User.UserType = 'CSPLitePortal'` selects the audience; `recordFilter` of `Department__c = $User.Department` keeps only the matching contracts. The custom `Department__c` field on the contract has to be populated by automation before the rule is switched on — an unpopulated field is a blank value on the record side, and blanks behave unpredictably in record criteria.

**Why not fix it in the sharing set:** sharing sets grant along a contact/account relationship, which is a different axis from department. The restriction rule filters the result of the sharing set without rewriting it.

### Pattern: staged rollout with `active` false

**When to use:** any first restriction rule on a populated object.

**How it works:** deploy with `<active>false</active>`, then measure the `recordFilter` as a query against the target object using an API client — Salesforce's own guidance is to "take the record criteria to your API client of choice and run the query," and to "add three to five percent overhead to the record filter's performance" for objects with large data volumes. Activate only when the returned row set matches the intended survivor list and the query time is acceptable.

**Why not activate directly:** an over-tight `recordFilter` removes rows silently. Nothing errors, no one is notified, and the first signal is a user reporting that a record they worked yesterday has disappeared.

---

## Decision Guidance

| Situation | Recommended approach | Reason |
|---|---|---|
| Object is Account, Opportunity, Case, Contact, or Lead | Tighten OWD and remove the layer that granted the access | Those objects are not valid `targetEntity` values for `enforcementType` `Restrict` |
| The goal is a tidier default list view or report, access unchanged | `admin/scoping-rules` | Scoping rules set the default record set and change no access |
| Criteria need two conditions, a negation, or a formula | Compute the answer into one field on the record, then filter on that field | Only the EQUALS operator is supported; `AND`, `OR` and formulas are not |
| The party to be blocked holds Modify All Data | Remove the permission, or accept that the rule does not apply to them | Documented: those users view, edit, and delete all records regardless |
| The exposure path is Apex or an integration running in system mode | Fix the sharing model, or set the Apex to user mode | Documented: restriction rules are not applied for code executed in System Mode |
| A third active restriction rule is needed on the object in Enterprise Edition | Consolidate two rules into one, or move the requirement into the sharing model | Two active per object in Enterprise and Developer; five in Performance and Unlimited. Scoping rules count against their own separate ceiling, not this one |
| Child records also need hiding | Author a separate rule on the child object | "Creating a restriction rule for an object doesn't automatically restrict access to its child objects" |
| Two rules could both match one user | Rewrite the `userCriteria` so exactly one matches | "Create only one restriction or scoping rule per object per user" — and where both do match, "only one of the active rules is observed," with no documented rule for which |
| Target is an external object | Confirm the adapter first | Only Salesforce Connect OData 2.0, OData 4.0, and Cross-Org adapters support restriction rules; the custom adapter does not |

---

## Recommended Workflow

1. **Confirm eligibility and edition.** Check the object against the supported `targetEntity` list and count the rules already active on it. If the object is ineligible or the ceiling is reached, stop and route the requirement to `admin/sharing-and-visibility` instead of forcing a rule.
2. **Write the bypass inventory before writing the rule.** List every user and permission set granting View All / View All Data / Modify All / Modify All Data on the object, every Apex class and integration that touches it in system mode, and whether calendars, Chatter publisher posts, or search shortcuts are in scope. Hand this list to whoever asked for the restriction and get their agreement in writing that the residual paths are acceptable.
3. **Express the requirement as two EQUALS tests.** One on a `$User` field for `userCriteria`, one on a record field for `recordFilter`. Use 15-character Ids, name the object type when traversing `Owner` (`Owner:User.…`), and confirm the record field is populated on every row that must survive.
4. **Deploy inactive and measure.** Ship the `.rule` file with `<active>false</active>`, then run the `recordFilter` as a query against the target object and compare the returned rows against the intended survivor list. Budget three to five percent overhead on large-data-volume objects.
5. **Activate and test as the restricted user.** Log in as a user whose `userCriteria` matches and verify the filter in the record UI, in a report, in a related list, and in a SOQL call. Then verify a non-matching user is unaffected. Do not use `UserRecordAccess` as the test — it does not account for restriction rules.
6. **Run the checker and promote.** `python3 skills/admin/restriction-rules/scripts/check_restriction_rules.py --manifest-dir <metadata-dir>` flags unsupported operators, 18-character Ids, ineligible target objects, bare `Owner.` traversals, an `enforcementType` of `FieldRestrict`, and active-rule counts over the edition ceiling for that enforcement type. Promote by change set or unlocked package and remap any org-specific Ids in `recordFilter` and `userCriteria` for the target org.

---

## Review Checklist

- [ ] `targetEntity` is on the supported list for `enforcementType` `Restrict`
- [ ] Active `Restrict` rule count on this object is within the edition ceiling (2 for Enterprise/Developer, 5 for Performance/Unlimited); active `Scoping` rules are counted separately against their own ceiling
- [ ] No user matches the `userCriteria` of more than one active restriction or scoping rule on this object
- [ ] `recordFilter` and `userCriteria` each contain exactly one `=` and no `AND`, `OR`, or formula
- [ ] Any Id literal is 15 characters, and every org-specific Id is on the deployment remap list
- [ ] `enforcementType` is `Restrict` (or deliberately `Scoping`) — never `FieldRestrict`, which the reference marks "Don't use."
- [ ] No custom picklist value referenced by the rule is scheduled for deletion — deleting it stops the rule working as intended
- [ ] `Owner` traversals use the `Owner:User.` object-type form, and no expression crosses more than one lookup level from the `targetEntity`
- [ ] The record field used in `recordFilter` is populated on every record intended to survive — no blanks or nulls
- [ ] The bypass inventory is written down and signed off, including View All / Modify All holders and system-mode code paths
- [ ] Child objects have their own rule where the requirement extends to them
- [ ] Activity related lists have been replaced with the Activity Timeline on any layout for a restricted Task or Event
- [ ] The rule was tested as a matching user and as a non-matching user, in UI, report, and SOQL
- [ ] Access-audit tooling built on `UserRecordAccess` has been annotated as not restriction-rule aware

---

## Salesforce-Specific Gotchas

Short form; the mechanics and recovery steps for each are in `references/gotchas.md`.

1. **A rule is not a security boundary** — eight documented paths still reach filtered records, and two of them (system mode, Modify All Data) are exactly the paths an integration takes.
2. **`UserRecordAccess` lies about it** — the object that access-audit tooling is usually built on returns the pre-restriction answer.
3. **Only EQUALS exists** — no `AND`, `OR`, or formula, so multi-condition requirements have to be precomputed into a field before the rule can express them.
4. **18-character Ids are the wrong length here** — record criteria wants 15, and the common source of an Id (a copy out of a browser URL or a Data Loader export) is often 18.
5. **`Owner.` fails, `Owner:User.` works** — the Owner reference needs an explicit object type, which is unlike every other dot-notation traversal on the platform.
6. **Restricting a parent does not restrict its children** — each object needs its own rule.
7. **Activity related lists undercount** — Open Activities and Activity History can show fewer than 50 rows when more exist that the user can access.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `.rule` metadata file | Deployable `RestrictionRule` with `enforcementType`, `targetEntity`, `userCriteria`, `recordFilter`, `active`, `version` |
| Bypass inventory | Named list of View All / Modify All holders, system-mode code paths, and surface-specific leaks, with sign-off |
| Filter validation query | The `recordFilter` expressed as a SOQL query, with the row count it returns before activation |
| Test evidence | Screenshots or query results as a matching user and as a non-matching user, across UI, report, and SOQL |
| Deployment plan | Change set or unlocked package contents plus the cross-org Id remap table |

---

## Related Skills

- `admin/scoping-rules` — the sibling `enforcementType`; filters the default record set in list views and reports without changing access
- `admin/sharing-and-visibility` — the grant side of the model; go here when the correct fix is a tighter OWD rather than a filter on top
- `admin/sharing-rules` — the layer that most often granted the access a restriction rule is being asked to take back
- `security/record-access-troubleshooting` — for tracing one named user against one named record; note the `UserRecordAccess` caveat above before trusting its output
- `apex/apex-security-patterns` — user mode versus system mode in Apex, which decides whether the rule applies to your code at all
