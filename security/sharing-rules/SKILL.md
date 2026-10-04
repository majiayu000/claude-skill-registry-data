---
name: sharing-rules
description: "Use when access must reach past the record owner's role hierarchy. Trigger keywords: sharing rule, criteria-based sharing rule, owner-based sharing rule, sharing rule recalculation, guest user sharing rule, share with a public group, SharingRules metadata. NOT for org-wide defaults - use admin/sharing-and-visibility. NOT for programmatic shares - use apex/apex-managed-sharing. NOT for subtracting access - use admin/restriction-rules."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Scalability
  - Operational Excellence
triggers:
  - "why can't sales ops see opportunities owned by the EMEA team"
  - "give a support team read access to cases they do not own"
  - "share records automatically based on a field value like region or account type"
  - "my sharing rule saved but the users still cannot see anything"
  - "sharing changes are taking hours to reach users after a reorg"
  - "expose records to unauthenticated visitors on an Experience Cloud site"
  - "how many sharing rules can one object carry before it becomes a problem"
  - "deploy sharing rules from sandbox to production with the Metadata API"
  - "which sharing rule granted this user access to this record"
tags:
  - sharing-rules
  - criteria-based-sharing
  - owner-based-sharing
  - record-access
  - guest-user-sharing
  - sharing-recalculation
inputs:
  - "Object in scope and its org-wide default — a sharing rule is meaningless on an object whose OWD is already Public Read/Write"
  - "Who needs the access, expressed as a group Salesforce can name: public group, role, role and internal subordinates, queue, territory, or guest user"
  - "What determines the access — who owns the record (owner-based) or what is on the record (criteria-based)"
  - "Access level required: Read Only or Read/Write, plus per-child access if the object is Account"
  - "Record and user volume on the object, because that is what turns recalculation from seconds into hours"
outputs:
  - "A rule design naming rule type, source group, target group, access level, and the exact criteria fields"
  - "Deployable `<Object>.sharingRules-meta.xml` and the matching package.xml manifest entries"
  - "Verification SOQL against the object's `__Share` table filtered to `RowCause = 'Rule'`"
  - "A recalculation plan for structural changes, including when to use deferred sharing maintenance"
  - "Checker-script output listing malformed, over-broad, or non-deployable rules"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-08-15
---

# Sharing Rules

A sharing rule is a standing instruction to the platform: *whenever a record matches this condition, write an access grant for this group.* It is the workhorse declarative mechanism for granting record access sideways — to peers, to a service desk, to a partner team — without changing ownership, without a manual share per record, and without inventing a role that does not reflect the business.

This skill owns the rules themselves. The surrounding access model — org-wide defaults, the role hierarchy, manual sharing, implicit sharing, `View All` bypasses — belongs to `admin/sharing-and-visibility`, and this skill assumes that model is already decided.

---

## Before Starting

Gather this context before designing or touching any rule:

- **What is the object's org-wide default?** Access grants exist only where the OWD is restrictive. Salesforce documents that "when an object has its organization-wide default set to Private or Public Read Only, Salesforce uses access grants to define how much access a user or group has to that object's records" — outside that, the share table is not the mechanism and a sharing rule buys nothing.
- **Owner-based or criteria-based?** The question is not "which is easier" but "what actually determines who should see this." If the answer is a sentence about *who owns it*, the rule is owner-based. If it is a sentence about *what is on the record*, the rule is criteria-based. A rule written in the wrong shape silently stops matching the moment ownership or the field changes.
- **Is the target group already a real Salesforce group?** Sharing rules can only target things the platform can name: public groups, roles, roles and internal subordinates, managers, queues, territories, portal roles, guest users. If the intended audience is "the people who work on this account," no rule can express that — that is teams or Apex managed sharing.
- **How many rules does the object already carry?** The Salesforce Security Guide states the cap directly: "You can define up to 300 total sharing rules for each object, including up to 50 criteria-based or guest user sharing rules, if available for the object." The 50 sits *inside* the 300 rather than on top of it, and guest rules draw on the same 50. Treat the count as a budget from the first rule, not something to discover at the ceiling.
- **What is the record and user volume?** Recalculation cost scales with records × affected group membership. On an object with a few thousand records nobody notices. At millions, a single role move can queue hours of maintenance.

---

## Core Concepts

### Owner-based vs criteria-based

| | Owner-based (`SharingOwnerRule`) | Criteria-based (`SharingCriteriaRule`) |
|---|---|---|
| Matches on | Who owns the record (`sharedFrom`) | Field values on the record (`criteriaItems` + `booleanFilter`) |
| Re-evaluates when | Ownership changes, or source/target group membership changes | The criteria fields change, plus group membership changes |
| Typical use | "Everything the West reps own goes to the Services desk" | "Every Account with Type = Partner goes to the channel team" |
| Extra required field | — | `includeRecordsOwnedByAll`, and **you can't edit it after the rule is created** |
| API version | 33.0+ | 33.0+ |

Both extend `SharingBaseRule`, which carries the fields that actually decide access: `accessLevel` (required), `sharedTo` (required), `label` (required), an optional `description` of up to 1,000 characters, and — on Account rules only — `accountSettings`.

### What a rule can and cannot grant

A sharing rule **adds** an access grant. It never removes one. There is no "deny" sharing rule, no ordering between rules, and no precedence: the most permissive grant on a record wins, whatever produced it. If the requirement is "these users must stop seeing records they currently see," a sharing rule is the wrong tool — see `admin/restriction-rules`.

Design for `Read` or `Edit`. `All` — Full Access, where "the specified user or group can view, edit, transfer, share, and delete the record" — appears in the enumeration inherited from the removed `CriteriaBasedSharingRule` type and on the share row, but it is not access a sharing rule can ask for. The Apex Developer Guide scopes it to "managed sharing" and the share-object field reference is blunter: "The All access level is an internal value and can't be granted." Account rules carry a nested `accountSettings` block whose `caseAccessLevel`, `contactAccessLevel`, and `opportunityAccessLevel` are each required and each take `None`, `Read`, or `Edit` — this is how one Account rule cascades to the account's children, and it is where over-sharing usually enters an org unnoticed.

### Who you can share to

`sharedTo` names the recipient. The elements that matter in practice:

| `sharedTo` element | Grants to | Note |
|---|---|---|
| `group` | A public group | The workhorse; see `admin/queues-and-public-groups` |
| `role` | Users in one role | Narrow — no subordinates |
| `roleAndSubordinatesInternal` | A role plus its internal subordinates | Current name after the Secure Roles rename |
| `queue` | A queue | Salesforce: "Applies only to lead, case, and CustomObject sharing rules" |
| `territory` / `territoryAndSubordinates` | Territory members | Pairs with `SharingTerritoryRule` |
| `managers` / `managerSubordinates` | A user's management chain / their subordinates | Manager groups, not the role hierarchy |
| `allInternalUsers` | "A group containing all internal and nonportal users" | Effectively org-wide; justify it in writing |
| `guestUser` | Named guest users | `SharingGuestRule` only |

Prefer a public group over a bare `role` even when the role is currently the right population. The group survives a reorg; the role reference does not.

### Guest user sharing rules

`SharingGuestRule` (API 47.0+) is a separate array on `SharingRules`, not a variant of the other two. Two hard constraints come straight from the Metadata API reference: "For `SharingGuestRule`, the `accessLevel` field can be set only to `Read`", and `includeHVUOwnedRecords` is required and "you can't edit this field after the sharing rule is created." Criteria (`criteriaItems`, `booleanFilter`) arrived in API 48.0.

Everything else about unauthenticated access — which objects the guest profile can even read, what the site exposes — is `admin/experience-cloud-guest-access` and `security/guest-user-security`. Come here only for the rule itself.

### The share row a rule produces

Every grant lands as a row in the object's share table: `AccountShare`, `OpportunityShare`, and for a custom object, `MyCustomObject__Share`. Four fields carry the meaning:

| Field | Holds | Note |
|---|---|---|
| `ParentId` (custom) / `AccountId` etc. (standard) | The shared record | "This field can't be updated." |
| `UserOrGroupId` | The recipient | User or Group Id |
| `AccessLevel` (custom) / `AccountAccessLevel` etc. (standard) | `Read`, `Edit`, or `All` | "The All access level is an internal value and can't be granted." |
| `RowCause` | Why the grant exists | "This field can't be updated." |

`RowCause` is the field that makes an access audit possible. Salesforce: "when a record owner manually shares a record with a user or group, Salesforce creates a sharing row with a `Manual` row cause. When a sharing rule shares the record with a user or group, Salesforce creates a sharing row with a `Rule` row cause." The documented set also includes `Owner`, `Team`, `ImplicitChild`, `ImplicitParent`, `TerritoryRule`, `TerritoryManual`, and `Territory2AssociationManual`.

The consequence to internalise: **`RowCause = 'Rule'` rows are system-maintained.** "The reason determines the type of sharing, which controls who can alter the sharing record." You do not insert them, you do not delete them, and deleting one by hand is not how you revoke access — changing the rule, the criteria, or the ownership is.

```soql
-- Which grants exist on one Account, and what produced each of them
SELECT Id, UserOrGroupId, AccountAccessLevel, OpportunityAccessLevel, RowCause
FROM AccountShare
WHERE AccountId = '001XX000003DHPh'

-- Only the rule-produced grants on a custom object
SELECT Id, ParentId, UserOrGroupId, AccessLevel, RowCause
FROM Project__Share
WHERE RowCause = 'Rule'
```

### Recalculation

Salesforce does not evaluate sharing rules at query time. "Rather than applying every sharing rule, traversing all hierarchies, and analyzing record access inheritance in real time, Salesforce calculates record access data only when configuration changes occur." Those precomputed rows are what a query joins against, which is why access is fast and why *changing* the model is expensive.

Recalculation is asynchronous — "automatic sharing recalculation is processed asynchronously and in parallel" — but it is not unobservable, and most advice on this topic gets that backwards. Salesforce documents both a progress view and a completion signal: "You can monitor the progress of your parallel sharing rule or organization-wide default recalculation on the Background Jobs page or view recent sharing operations on the View Setup Audit Trail page," and "You receive an email notification when the recalculation is completed for all affected objects." It is triggered by far more than editing a rule: role moves, group membership edits, queue changes, ownership transfers, and criteria-field updates all cause the platform to rewrite share rows and group maintenance tables. The architect guidance is explicit that "it can take some time to recalculate access for a large number of users, and adjust the tables that record their access rights," and that "the size and complexity of an organization's queues and hierarchies directly affect the duration of record access calculations."

While the job runs the model is partly frozen. The Security Guide documents share locks: "You can't modify the org-wide defaults when a sharing rule recalculation for any object is in progress. Similarly, you can't modify sharing rules when recalculation for an org-wide default update is in progress" — though "You can make changes to the org-wide defaults and sharing rules for other objects." That lock, not politeness, is why an impatient admin cannot simply re-edit their way out of a slow rule.

For bulk structural change there is a deliberate escape hatch: defer sharing calculation, "which allows users to defer the processing of sharing rules until after new users, rules, and other content have been loaded." It is gated by a specific permission and it suspends and resumes two distinct processes — group membership calculation and sharing rule calculation. Deferral does not make the work smaller; it batches many small recalculations into one large one you schedule.

Deep-dive on the failure modes — the unwatched recalculation, the ownership-change deletions, the criteria-churn trap — is in `references/gotchas.md`. Read it before you promise a business stakeholder a completion time.

---

## Common Patterns

### Pattern: Peer visibility inside a region

**When to use:** OWD on Opportunity is Private. Reps in one region must read each other's pipeline. The role hierarchy gives their manager visibility but gives them nothing, because hierarchy access travels up, never sideways.

**How it works:**

1. Build one public group holding the region's roles (`admin/queues-and-public-groups`), not a list of named users.
2. Create an owner-based rule: `sharedFrom` = that group, `sharedTo` = the same group, `accessLevel` = `Read`.
3. New joiners inherit access the moment they land in a member role. There is no per-user step.

**Why not the alternative:** a criteria-based rule on a region field looks equivalent and is not. It re-evaluates when the field changes, so a mis-keyed region silently moves the record out of the group's view; and it does not follow ownership, so a transferred deal keeps matching the old region until someone edits the field.

### Pattern: Field-driven access to a sensitive subset

**When to use:** One team should see only the records carrying a particular classification — `Type = 'Partner'`, `Stage = 'Legal Review'`, a compliance checkbox. Ownership is irrelevant and scattered.

**How it works:** a criteria-based rule with `criteriaItems` and, when there is more than one condition, an explicit `booleanFilter`. Set `includeRecordsOwnedByAll` deliberately — it decides "whether records owned by users who can't have an assigned role are included in the records shared," which is exactly the integration users and portal-adjacent accounts everyone forgets — and remember you cannot change it later without recreating the rule.

**Why not the alternative:** granting the team `View All` on the object is one click and is unbounded. The criteria rule is the narrow version of the same access.

### Pattern: Publishing records to an Experience Cloud site

**When to use:** anonymous visitors must read a catalogue, a knowledge-adjacent custom object, or a public listing.

**How it works:** a `SharingGuestRule` targeting the site's guest user via `sharedTo` → `guestUser`, `accessLevel` = `Read` (the only value it accepts), with `includeHVUOwnedRecords` set correctly on the first attempt.

**Why not the alternative:** an ordinary criteria-based rule pointed at a group that happens to contain the guest user is not the same object and is the single most common way orgs accidentally over-expose data to the internet.

---

## Decision Guidance

| Situation | Recommended approach | Reason |
|---|---|---|
| Access follows who owns the record | Owner-based rule, source and target as public groups | Survives reorgs; no field to keep clean |
| Access follows a value on the record | Criteria-based rule with explicit `booleanFilter` | The record carries its own routing |
| Criteria field changes on most records every week | Reconsider — use owner-based or a team | Each change is a recalculation event |
| Access must be removed from a population | `admin/restriction-rules` | Sharing rules only add |
| Recipient is "whoever is working this record" | Account/Opportunity/Case teams, or `apex/apex-managed-sharing` | Not a group the platform can name |
| Logic needs cross-object or computed conditions | `apex/apex-managed-sharing` with a custom sharing reason | Criteria evaluate fields on the record only |
| Anonymous site visitors | `SharingGuestRule`, Read only | The only supported guest mechanism |
| Manager chain, not the role hierarchy | `sharedTo` → `managers` / `managerSubordinates` | Manager groups are a separate axis |
| Loading users, roles, groups and rules together | Defer sharing calculation, then resume once | One large recalculation beats hundreds of small ones |
| Rule count on the object is climbing every quarter | Consolidate onto groups; re-examine OWD and hierarchy | Rule sprawl is a symptom of a wrong baseline |

---

## Metadata Shape

All rules for one object live in a single file. Retrieve the object's existing file and add to it rather than authoring the envelope by hand — a retrieved file already carries the element order the API validates against. `operation` takes a value from the `FilterOperation` enumeration: `equals`, `notEqual`, `lessThan`, `greaterThan`, `lessOrEqual`, `greaterOrEqual`, `contains`, `notContain`, `startsWith`, `includes`, `excludes`.

```xml
<!-- force-app/main/default/sharingRules/Account.sharingRules-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<SharingRules xmlns="http://soap.sforce.com/2006/04/metadata">
    <sharingOwnerRules>
        <fullName>West_Reps_To_Services_Desk</fullName>
        <accessLevel>Read</accessLevel>
        <accountSettings>
            <caseAccessLevel>Read</caseAccessLevel>
            <contactAccessLevel>Read</contactAccessLevel>
            <opportunityAccessLevel>None</opportunityAccessLevel>
        </accountSettings>
        <description>Services desk reads accounts owned by West sales, cases and contacts included, pipeline excluded.</description>
        <label>West Reps to Services Desk</label>
        <sharedFrom>
            <group>West_Sales_Reps</group>
        </sharedFrom>
        <sharedTo>
            <group>Services_Desk</group>
        </sharedTo>
    </sharingOwnerRules>
    <sharingCriteriaRules>
        <fullName>Partner_Accounts_To_Channel</fullName>
        <accessLevel>Edit</accessLevel>
        <accountSettings>
            <caseAccessLevel>Read</caseAccessLevel>
            <contactAccessLevel>Edit</contactAccessLevel>
            <opportunityAccessLevel>Read</opportunityAccessLevel>
        </accountSettings>
        <label>Partner Accounts to Channel Team</label>
        <sharedTo>
            <group>Channel_Team</group>
        </sharedTo>
        <booleanFilter>1 AND 2</booleanFilter>
        <criteriaItems>
            <field>Type</field>
            <operation>equals</operation>
            <value>Partner</value>
        </criteriaItems>
        <criteriaItems>
            <field>Active__c</field>
            <operation>equals</operation>
            <value>true</value>
        </criteriaItems>
        <includeRecordsOwnedByAll>false</includeRecordsOwnedByAll>
    </sharingCriteriaRules>
</SharingRules>
```

The manifest addresses the concrete rule types, not the `SharingRules` container. This is the sample the Metadata API Developer Guide ships for "retrieving a specific criteria-based sharing rule for the lead object, retrieving all ownership-based sharing rules for all objects, and retrieving all territory-based sharing rules for the account object":

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Lead.testShareRule</members>
        <name>SharingCriteriaRule</name>
    </types>
    <types>
        <members>*</members>
        <name>SharingOwnerRule</name>
    </types>
    <types>
        <members>Account.*</members>
        <name>SharingTerritoryRule</name>
    </types>
    <version>33.0</version>
</Package>
```

---

## Recommended Workflow

1. **Confirm the baseline.** Read the object's OWD and the role hierarchy first. If OWD is Public Read/Write, stop — no rule is needed. If the hierarchy already delivers the access, stop — a rule is redundant weight on every future recalculation.
2. **Name the population as a group.** Create or reuse a public group. Reject the design if the audience cannot be expressed as a group, a role, a queue, a territory, or a guest user; route it to teams or `apex/apex-managed-sharing`.
3. **Choose the rule type from the requirement's grammar.** Ownership sentence → owner-based. Field sentence → criteria-based. Write the chosen `accessLevel`, and for Account also the three `accountSettings` values, before touching Setup.
4. **Build it as metadata.** Retrieve the object's existing `<Object>.sharingRules-meta.xml`, add the rule, and deploy. Set `includeRecordsOwnedByAll` (or `includeHVUOwnedRecords` for guest rules) correctly the first time — neither is editable afterwards.
5. **Run the checker.** `python3 skills/admin/sharing-rules/scripts/check_sharing_rules.py --manifest-dir <metadata-dir>` catches missing required fields, `booleanFilter` indexes that reference criteria that do not exist, guest rules above Read, and org-wide recipients.
6. **Verify against the share table, not the UI.** Watch Setup → Background Jobs until the recalculation clears — or wait for the completion email — then query the object's share object filtered to `RowCause = 'Rule'` and confirm the expected `UserOrGroupId` rows exist at the expected access level. Then log in as a target user and open a record that should *not* match.
7. **Plan the recalculation before any bulk change.** For reorgs, mass ownership transfers, or user loads, use deferred sharing calculation, resume once, and treat the resume as a scheduled maintenance window rather than an instant operation.

---

## Review Checklist

- [ ] The object's OWD is Private or Public Read Only — otherwise the rule is inert
- [ ] Rule type matches the requirement's grammar (ownership vs field value)
- [ ] `sharedTo` targets a public group, not a bare role or a list of individuals
- [ ] `accessLevel` is the minimum that satisfies the requirement, not `Edit` by reflex
- [ ] On Account rules, all three `accountSettings` values were chosen deliberately, not left at the picker default
- [ ] `includeRecordsOwnedByAll` / `includeHVUOwnedRecords` was set correctly on creation — it cannot be changed later
- [ ] `booleanFilter` indexes match the number of `criteriaItems` actually present
- [ ] Guest rules use `SharingGuestRule` with `accessLevel` of `Read`
- [ ] Criteria fields are stable — not a status or stage that churns on most records weekly
- [ ] `RowCause = 'Rule'` rows verified by SOQL on the share object, plus one negative test as a non-member
- [ ] Rule count on the object recorded against the documented budget — 300 rules per object, of which at most 50 may be criteria-based or guest rules
- [ ] Any bulk load or reorg that follows has a deferred-sharing-calculation plan

---

## Salesforce-Specific Gotchas

Summaries only — the mechanism, the trigger conditions, and the fix for each are in `references/gotchas.md`.

1. **Saving a rule is not granting access.** Recalculation is asynchronous, so "I created it and nothing happened" is usually a timing report, not a bug — track it on Setup → Background Jobs rather than on the rule page.
2. **Changing the owner rewrites the record's grants.** Manual shares are deleted outright and owner-based rules re-evaluate from the new owner's groups — access can silently disappear from a transfer nobody connected to sharing.
3. **`includeRecordsOwnedByAll` is write-once.** Getting it wrong means deleting and recreating the rule, which is a fresh recalculation on the whole object.
4. **Criteria on a churning field turns every record edit into sharing maintenance.** The rule is correct and the org is slow.
5. **Account rules cascade to Cases, Contacts, and Opportunities** through `accountSettings`, which is how a "read the account" request becomes pipeline exposure.
6. **`RowCause = 'Rule'` rows cannot be deleted to revoke access** — they are system-maintained and will be rewritten.
7. **Sharing to a queue is object-limited** — Salesforce documents `queue` as applying "only to lead, case, and CustomObject sharing rules."

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Rule design record | Rule type, source group, target group, access level, criteria fields, and the reason for each |
| `<Object>.sharingRules-meta.xml` | Deployable rule definitions for the object |
| package.xml entries | `SharingCriteriaRule` / `SharingOwnerRule` / `SharingTerritoryRule` members for retrieve and deploy |
| Verification SOQL | Share-object query filtered to `RowCause = 'Rule'`, plus a negative test |
| Recalculation plan | Which structural changes are batched, when deferral is enabled, and who owns the resume |
| Checker output | Malformed, non-deployable, or over-broad rules found in the metadata |

---

## Related Skills

- `admin/sharing-and-visibility` — the surrounding access model: OWD, role hierarchy, manual sharing, bypass permissions. Decide the baseline there, build the rules here.
- `admin/role-hierarchy-design` — when the real fix is the hierarchy rather than another rule.
- `admin/restriction-rules` — the only declarative way to subtract access; sharing rules cannot.
- `apex/apex-managed-sharing` — programmatic `__Share` inserts with custom sharing reasons, for logic criteria cannot express.
- `admin/queues-and-public-groups` — building the groups that `sharedTo` targets, and the `roleAndSubordinatesInternal` rename in its Gotcha 6.
- `data/sharing-recalculation-performance` — deep treatment of deferral, recalculation windows, and OWD changes at volume.
- `security/record-access-troubleshooting` — tracing one named user's access to one specific record.
- `admin/experience-cloud-guest-access` / `security/guest-user-security` — everything about guest access that is not the sharing rule itself.
