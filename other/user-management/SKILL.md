---
name: user-management
description: "Use this skill to create, deactivate, freeze, or manage Salesforce users, assign user licenses and feature licenses, configure profiles and roles, set login hours and IP restrictions, and set up delegated administration. Triggers: 'add a new user in Salesforce', 'create a user and assign a licence', adding a new user, deactivating a departing employee, license assignment, freezing a user account, delegated admin setup. NOT for designing the permission set / PSG model — use admin/permission-set-architecture. NOT for who can see which records — use admin/sharing-and-visibility. Also covers: bulk user loads by CSV, Bulk API 2.0 upsert on Username, the UserLogin freeze object, licence and permission-set-licence reclamation, Role metadata deployment, and the offboarding checklist as SOQL."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Operational Excellence
triggers:
  - "add a new user in Salesforce"
  - "how do I add a new user"
  - "deactivate a user who left the company"
  - "freeze a user account without deactivating it"
  - "bulk load users from a CSV with Data Loader"
  - "freeze multiple users at once"
  - "duplicate username error when creating a user"
  - "deactivated user still shows as a queue member"
  - "permission set license still used after the user left"
  - "blank column did not clear the field in a user update"
  - "MIXED_DML_OPERATION when creating a user in a test"
  - "removed login hours from the profile but users are still locked out"
  - "find users who have not logged in for 90 days"
  - "set up delegated administration so a manager can reset passwords"
  - "restrict user login to certain hours or IP addresses"
  - "user cannot log in after hours or from home office"
tags:
  - user-management
  - users
  - licenses
  - profiles
  - delegated-admin
inputs:
  - "User's name, email address, and desired username (must be globally unique in email format)"
  - "Profile to assign and any roles the user should occupy in the hierarchy"
  - "User license type required (Salesforce, Salesforce Platform, Chatter Free, etc.)"
  - "Any feature licenses needed (Marketing User, Service Cloud User, etc.)"
outputs:
  - "Active Salesforce user record with profile, role, and license assigned"
  - "Delegated administration group configuration (for delegated admin tasks)"
  - "Login restriction settings (hours and IP ranges per profile)"
  - "User deactivation or freeze checklist with reassignment steps"
dependencies: []
version: 1.1.2
author: Pranav Nagrecha
updated: 2026-10-03
---

# User Management

Use this skill when creating, modifying, deactivating, or freezing Salesforce users, assigning licenses, configuring roles and profiles, restricting login access, or setting up delegated administration. This skill covers the full user lifecycle from provisioning to offboarding.

---

## Before Starting

Gather this context before working on any user management task:

| Context | What to confirm |
|---|---|
| License availability | Confirm the org has unused licenses of the required type (Setup → Company Information → User Licenses / Feature Licenses / Permission Set Licenses). |
| Profile selection | Identify the right profile. Profile controls object permissions, FLS, page layouts, tab visibility, login hours, and IP restrictions. |
| Role hierarchy | Determine if the user needs a role. Roles affect record access through hierarchy — a user without a role sees only records they own if OWD is Private. |
| Offboarding status | When deactivating, determine whether to reassign open records, reassign approval processes, and whether to freeze first. |

---

## Questions to Ask Before Configuring

Ask these before opening Setup or writing the CSV. Users are records, not metadata, and records
cannot be rolled back by redeploying — the Object Reference's own warning is that "because users can
never be deleted, we recommend that you exercise caution when creating them."

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "What is the username convention, and does it already exist in a sandbox?" | `Username` is unique across **all** Salesforce orgs, not just this one, and a taken username is never released | The exact suffix rule, and a pre-load uniqueness check instead of a failed batch |
| "Is this one user, or a batch — and will the job be re-run?" | One user is a Setup click; a batch is a CSV whose second run must upsert on `Username` rather than create | The tool choice (Setup / Data Loader / `composite/sobjects`) and whether `allOrNone` is on |
| "Which permission set **licences** does this person need, and who is holding the spare ones?" | PSLs are counted separately from user licences and are not released by deactivation | A reclamation list of PSLs held by inactive users, run before buying more |
| "Is this person going to be a record owner, an approver, a queue member, or a manager of other users?" | Each one is a separate offboarding query later; none is cleaned up by deactivation | The offboarding checklist for this user, written at provisioning time |
| "Do they need role-hierarchy visibility, and is the role already deployed?" | `Role` is metadata and deploys ahead of the user load; a user created with a role in the same transaction as ordinary records hits mixed DML | Deploy order: roles and profiles first, users second, permission sets third |
| "Are login hours or IP ranges in scope, and is this the right lever?" | Both live on the Profile and therefore apply to everyone sharing it, and neither ends an existing session | Either a profile change, or a hand-off to `security/ip-range-and-login-flow-strategy` |
| "Who is allowed to do this next time?" | Creating an internal user needs Manage Internal Users; freezing needs Manage Users; reading PSL assignments needs View Setup and Configuration or Assign Permission Sets | A delegated group scoped to real profiles, not a second System Administrator |

What a proper configuration adds over just clicking New User: the load is re-runnable and validated
before it touches the org, every licence the person consumes is known and reclaimable, and the day
they leave there is a checklist that finds their queues, approvals, reports and permission set
licences instead of a deactivation that silently leaves all four behind.

---

## Core Concepts

### User License Types

Every Salesforce user must have exactly one user license. The license type determines which features and apps are available to that user.

| License | Access |
|---|---|
| Salesforce | Full CRM access to Sales Cloud, Service Cloud, and related apps. The most capable and most expensive license. |
| Salesforce Platform | Access to custom apps, Chatter, and core platform features. Does NOT include standard Sales or Service Cloud objects (Leads, Opportunities, Cases, Forecasts). |
| Force.com (App Subscription) | Legacy license for a single custom app. Limited standard object access. |
| Chatter Free | No CRM data access. Can use Chatter, groups, files. Does not consume a paid license. Cannot be converted to a standard license without deleting and recreating the user. |
| Chatter External | For external collaborators outside the org. No internal data access. |
| Identity | Authentication and SSO only. No Salesforce data access. |

Feature licenses layer additional capabilities on top of the user license (e.g., Marketing User, Service Cloud User, Knowledge User, Mobile User). Permission set licenses (PSLs) enable specific feature-level entitlements (e.g., Einstein Prediction Builder) assigned via permission sets rather than the profile.

### Deactivating vs Freezing a User

**Deactivating** permanently prevents login. The user record is preserved with all history intact — owned records remain, name appears in history, workflow emails still address the user. A deactivated user does NOT consume a license. You cannot deactivate the last active System Administrator.

**Freezing** is a temporary lock that immediately prevents login without changing ownership, removing the user from queues, or reassigning workflow. Use freeze during offboarding when you need to block access instantly but have not finished reassigning records and approval processes. A frozen user still consumes a license. You can unfreeze at any time.

Best practice: Freeze first → reassign records and approvals → then deactivate.

### Profile Assignment

Every user has exactly one profile. Profiles cannot be removed — only replaced. Profile settings that directly affect user behavior include:

| Setting | Effect |
|---|---|
| Object permissions | CRUD + View All + Modify All per object |
| Field-level security | Read/Edit per field (overrides page layout) |
| App and tab visibility | Which Lightning apps and tabs are shown |
| Page layout assignment | Which layouts are seen per object and record type |
| Login hours | Time windows during which users may log in |
| Login IP ranges | Whitelisted IP ranges; login from outside this range triggers verification email or blocks access depending on org settings |

### Role Hierarchy and Record Visibility

Roles are optional but impact record sharing. When OWD is Private or Public Read Only, users in a higher role can see records owned by users in lower roles (unless the sharing model disables role hierarchy for an object — this is only possible for custom objects).

A user with no role sits outside the hierarchy and can only see records they own unless explicitly shared. Assigning a role is critical when onboarding users who need visibility into subordinates' pipeline or cases.

---

## Common Patterns

### Pattern 1: New Employee Provisioning

**When to use:** A new hire needs Salesforce access.

**How it works:**
1. Setup → Users → New User
2. Fill required fields: Last Name, Alias (auto-suggested), Email, Username (must be globally unique across all Salesforce orgs; convention is `firstname.lastname@company.org.sandbox` for sandboxes), Nickname
3. Select User License first — this filters the available profiles to only compatible options
4. Select Profile
5. Select Role if the org uses roles for sharing
6. Check any needed Feature Licenses (Marketing User, Offline User, etc.)
7. Save — Salesforce sends a welcome email with a password setup link
8. Assign permission sets after creation (not during) via the Permission Set Assignments related list

**Why not the alternative:** Setting up a user without selecting the license first leads to choosing an incompatible profile, which causes a validation error mid-save.

### Pattern 2: Employee Offboarding

**When to use:** An employee leaves and their account must be secured and cleaned up.

**How it works:**
1. **Freeze immediately** — Setup → Users → click the user name → Freeze. This blocks login within seconds.
2. **Reassign open records** — Use a list view filtered to `Owner = departing user`, mass-reassign to a manager or queue.
3. **Reassign approval processes** — Setup → Approval Processes → check if user is an approver. Use "Automated Approver" or re-route to a queue.
4. **Reassign queue membership** — Setup → Queues → remove from all queues.
5. **Transfer Salesforce Knowledge articles** if user owns draft articles.
6. **Deactivate** — Setup → Users → Edit → uncheck Active. Cannot undo while records reference that user as approver in active approval processes.

**Why not the alternative:** Skipping the freeze and going straight to reassignment risks the user logging in during the reassignment window.

### Pattern 3: Delegated Administration

**When to use:** A manager or HR team needs to create/edit users in a specific group of profiles and reset passwords without having System Administrator access.

**How it works:**
1. Setup → Delegated Administration → New Delegated Group
2. Name the group (e.g., "HR User Admins")
3. Add Delegated Administrators — the users who will have delegated rights
4. Add Managed Profiles — the profiles that delegates can assign to users they manage
5. Add User Administration section — set which user fields delegates can edit
6. Optionally add custom object administration
7. Assign delegated users the Manage Users permission via their profile or a permission set

**Why not the alternative:** Giving HR the System Administrator profile creates excessive access. Delegated admin scopes the authority to the specified profiles only.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Block a user immediately (offboarding today) | Freeze → reassign → deactivate | Freeze is instant; deactivate after cleanup |
| User needs Sales Cloud access | Salesforce user license + Salesforce profile | Platform license excludes standard CRM objects |
| External partner needs Chatter collaboration only | Chatter Free or Chatter External license | No paid license consumed for non-CRM users |
| Manager needs to onboard team members | Delegated administration | Scoped authority without System Admin profile |
| User traveling needs login from any IP | Remove IP ranges from profile or add trusted range | IP restrictions are profile-wide, not per-user |
| User cannot log in after 6pm | Check Login Hours on the profile | Hours setting blocks login outside window |
| New user in Sales role can't see team's opportunities | Assign a Role in the hierarchy | Without a role, user sits outside sharing hierarchy |
| Need to audit who was assigned a license | Setup → Company Information → User Licenses | Shows allocated vs used counts per license type |

---


## Recommended Workflow

1. **Answer the questions above and pick the lane.** One user with no licence question is a Setup
   click. Anything with a batch, a licence constraint, or an offboarding tail goes through
   `templates/user-management-template.md` and the artefacts in
   `references/metadata-examples.md`.

2. **Check capacity before you build anything.** Run the `UserLicense`, `PermissionSetLicense` and
   `PermissionSetLicenseAssign` queries in `references/metadata-examples.md` section 7. Reclaim PSLs
   held by inactive users first. Never filter on `UserLicense.UsedLicenses` — it is not filterable in
   API v64.0 and later.

3. **Deploy the metadata that users point at, before the users.** `Role` files (section 2) and the
   `Profile` `userLicense` / `loginHours` / `loginIpRanges` blocks (section 3), via the `package.xml`
   in section 4. Validate with `sf project deploy validate` first — a role deploy triggers sharing work.

4. **Build the load artefact and lint it before it touches the org.** Author the CSV from section 1
   or the `composite/sobjects` payload from section 6, then run
   `python3 scripts/check_user_management.py --manifest-dir force-app/main/default --csv users.csv`.
   It fails the file on duplicate usernames, missing required columns and non-multiple-of-60 login
   hours — all of which are irreversible or confusing once loaded.

5. **Load, then assign permission sets as a separate call.** Users and their
   `PermissionSetAssignment` rows cannot go in one `composite/sobjects` request; Setup-area objects
   cannot be batched with others. Use `allOrNone: true` so a partial failure does not leave you
   guessing which globally-unique usernames were consumed.

6. **For offboarding, run the sequence in order:** freeze via `UserLogin.IsFrozen` (a two-step
   query-then-update, section 8) → work every query in section 9 → delete
   `PermissionSetLicenseAssign` rows → set `User.IsActive = false`. Use `#N/A`, not a blank cell, for
   any field you intend to clear.

7. **Verify against the org, not the deploy result.** Run the combined verification query at the end
   of `references/metadata-examples.md`, then walk the Review Checklist below. Record anything you
   deviated from in the template's Notes section.

---

## Review Checklist

Run through these before marking a user management task complete:

- [ ] Correct user license type selected and license is available in the org
- [ ] Profile selected is compatible with the license and grants appropriate object/field access
- [ ] Role assigned if org uses role hierarchy for record sharing
- [ ] Required feature licenses checked (Marketing User, Service Cloud User, etc.)
- [ ] For new users: welcome email sent and username follows org naming convention
- [ ] For deactivated users: open records reassigned, queues updated, approval processes rerouted
- [ ] For frozen users: freeze is confirmed in Setup before beginning reassignment
- [ ] Login hours and IP ranges on the profile match the security policy for this user group
- [ ] Delegated admin groups include only the profiles that delegates should be able to manage
- [ ] System Administrator count verified — org must retain at least one active System Admin
- [ ] For bulk loads: CSV linted with `scripts/check_user_management.py --csv` before import (no duplicate usernames, all required columns present)
- [ ] For deactivated users: `PermissionSetLicenseAssign` rows deleted — permission set licences are NOT released by deactivation
- [ ] For any field cleared in a Bulk API update: written as `#N/A`, not left blank, and re-queried to confirm

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Deactivating a user does not remove them from queues or approval steps** — Active approval processes referencing the deactivated user will stall until the approver is changed. Check Approval Processes before deactivating. Queues also retain the deactivated user as a member; manually remove them or cases/leads will still route to the queue but no active member will receive notifications.

2. **Username must be globally unique across all Salesforce orgs, not just your production org** — If a sandbox user with `user@company.com` exists and you try to create the same username in production, it will fail. Standard convention is to suffix sandbox usernames: `user@company.com.staging`. Changing the username after creation sends a new verification email to the new address.

3. **Login hours block logins but do not terminate active sessions** — If a user is logged in before the cutoff hour and the hour passes, their existing session remains active. You must also configure session settings to enforce logout at the end of login hours (Setup → Session Settings → "Force logout on session timeout"). Without this, restricting hours only prevents new logins, not active work.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| User record | Active Salesforce user with license, profile, role, and feature licenses assigned |
| Delegated administration group | Scoped admin group with delegates, managed profiles, and field edit permissions |
| Offboarding checklist | Step-by-step freeze → reassign → deactivate workflow for a departing employee |
| Login restriction configuration | Profile-level login hours and IP range settings |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing the user CSV, the `Role` or `Profile` XML, the `composite/sobjects` payload, the freeze/deactivate sequence, or any of the licence and offboarding queries |
| `references/gotchas.md` | Something worked in Setup but not through the API, or a deactivation left something behind |
| `references/examples.md` | Working a full scenario end to end — onboarding, emergency offboarding, delegated admin |
| `references/llm-anti-patterns.md` | Reviewing AI-generated user-management advice before acting on it |
| `references/well-architected.md` | Justifying the licence, delegation or login-restriction decision, and for the source list behind every claim in this package |
| `templates/user-management-template.md` | Capturing an actual provisioning, offboarding or delegation task |

---

## Related Skills

- `admin/permission-set-architecture` — Designing the permission set and PSG model that sits on top of the base profile. This skill assigns; that one designs.
- `admin/permission-sets-vs-profiles` — Deciding what belongs on the profile versus a permission set before you pick a profile here
- `admin/delegated-administration` — The full delegated group model. Pattern 3 below is the provisioning-side summary only
- `admin/integration-user-management` — Service accounts and API-only users, which have a different licence and login-restriction shape from employees
- `admin/user-access-policies` — Automating assignment changes across users as criteria change, instead of per-user edits
- `admin/mass-transfer-ownership` — Reassigning the records that offboarding query 1 in `references/metadata-examples.md` turns up
- `admin/sharing-and-visibility` — Role hierarchy behaviour, OWD and sharing rules. Roles are deployed here; what a role grants is decided there
- `admin/object-creation-and-design` — Object permissions live on profiles; read this when a new object needs access granted to user groups
- `security/mfa-enforcement-patterns` — MFA and session policy, the controls login hours cannot provide
- `security/ip-range-and-login-flow-strategy` — Per-user and risk-based login control when profile-wide IP ranges are too blunt
- `security/login-forensics` — Failed-login clustering, geography and session anomalies beyond the `LoginHistory` query in this skill
