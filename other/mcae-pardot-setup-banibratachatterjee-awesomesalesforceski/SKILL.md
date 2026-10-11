---
name: mcae-pardot-setup
description: "Use this skill when configuring a new or existing Marketing Cloud Account Engagement (MCAE, formerly Pardot) business unit: Salesforce v2 connector activation, connector user permissions, Salesforce User Sync, prospect field sync rules, tracking domain setup, and Account Engagement Lightning App installation. NOT for Marketing Cloud Engagement (email studio, journeys) or Einstein Marketing features."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Operational Excellence
  - Reliability
triggers:
  - "How do I connect a new Pardot business unit to our Salesforce org?"
  - "The Account Engagement connector is showing as paused — how do I activate it?"
  - "Prospects aren't syncing between MCAE and Salesforce — what permissions does the connector user need?"
  - "How do I enable Salesforce User Sync so marketing team members are managed from Salesforce instead of Pardot?"
  - "What's the correct setup sequence for a new Account Engagement business unit from scratch?"
  - "Campaign sync between Account Engagement and Salesforce isn't working — how do I map campaign member statuses?"
tags:
  - mcae
  - pardot
  - account-engagement
  - connector
  - user-sync
  - business-unit
  - marketing-automation
  - prospect-sync
inputs:
  - "Salesforce org edition and whether Account Engagement is provisioned (BU ID / tracker domain)"
  - "Connector user identity: which Salesforce user will serve as the sync user"
  - "List of objects intended for sync: Leads, Contacts, Accounts, Opportunities, Campaigns"
  - "Marketing team headcount and whether Salesforce User Sync should be enabled"
  - "Tracking domain or vanity domain for visitor tracking pixel"
  - "Whether multiple business units are in scope"
outputs:
  - "Connector activation confirmation and connector user permission checklist"
  - "Salesforce User Sync enablement guide with role-to-profile mapping"
  - "Field sync rule matrix: which fields use Salesforce value, Pardot value, or most-recently-updated"
  - "Campaign connector configuration steps with Campaign Member status mapping"
  - "Tracking domain setup checklist"
  - "Account Engagement Lightning App installation confirmation"
  - "Review checklist for end-to-end sync validation"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-07
---

# MCAE (Pardot) Setup

This skill activates when a practitioner needs to configure a Marketing Cloud Account Engagement business unit from initial provisioning through a fully functioning bidirectional sync with Salesforce — including connector activation, connector user permissions, Salesforce User Sync, prospect field sync rules, campaign connector, and tracking domain setup. It does not cover Marketing Cloud Engagement (the email-studio product), Einstein predictive features, or Pardot API integrations.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Connector state.** Every new MCAE business unit provisions a Salesforce v2 connector that starts in a **Paused** state. Until it is explicitly activated in Account Engagement Settings > Connectors, no prospect data flows in either direction. This is the single most common cause of "nothing is syncing" tickets on fresh BU setups.
- **Connector user identity.** The connector user is the Salesforce user whose credentials the v2 connector runs under. It must hold the Marketing User checkbox, View All Data, Modify All Data, and API Enabled permissions, and must have read/write access to every object and field intended for sync. Using a shared service account (not a named person's account) is strongly recommended to avoid sync breakage when the person leaves.
- **User Sync pre-condition.** Salesforce User Sync can only be enabled by an MCAE admin after the connector is active and at least one Account Engagement user role has been mapped to a Salesforce profile. Once enabled, it is irreversible in standard orgs — MCAE users are then managed entirely from Salesforce, and any MCAE-native user management UI is hidden.
- **BU-to-org cardinality.** Each MCAE business unit connects to exactly one Salesforce org. Each Salesforce user can belong to only one MCAE business unit per Salesforce org. If a user needs access to multiple BUs in the same org, that requires separate Salesforce logins or a BU switching workflow — not a simple permission grant.
- **Account Engagement Lightning App.** Admins must install the Account Engagement Lightning App from AppExchange (or via Setup > App Manager) before MCAE UI elements appear in the Salesforce Lightning interface. Without it, non-Classic users see no marketing navigation.

---

## Core Concepts

### Salesforce v2 Connector and Its Paused Default State

When Salesforce provisions a new MCAE business unit, it auto-creates a Salesforce v2 connector record in that BU. This connector is deliberately started in a **Paused** state — it does not sync data until an MCAE admin navigates to **Account Engagement Settings > Connectors**, opens the connector, and clicks **Resume**. The connector must also be verified (pass an auth check) before resumption is allowed.

The v2 connector replaced the deprecated v1 connector. Key behaviors of v2:
- Uses OAuth 2.0 rather than username/password credentials.
- Syncs via a designated connector user whose Salesforce profile drives field-level access.
- Supports multi-BU orgs by having one connector per BU, each pointing to the same Salesforce org.
- Respects Salesforce field-level security (FLS) on the connector user — if the connector user cannot read a field, that field does not sync.

Source: Salesforce Help — Connect Account Engagement and Salesforce (https://help.salesforce.com/s/articleView?id=sf.pardot_sf_connector_parent.htm)

### Connector User Permissions

The connector user is the Salesforce identity the v2 connector authenticates as. It needs:

| Permission | Why Required |
|---|---|
| **Marketing User** checkbox (on User record) | Required for campaign membership write operations |
| **View All Data** | Allows connector to read all Lead, Contact, Account, Opportunity records across ownership |
| **Modify All Data** | Allows connector to write sync'd field values back to CRM records |
| **API Enabled** | Required for REST API calls the connector makes |
| **Read/Write FLS on all sync'd fields** | FLS on the connector user's profile controls which fields appear in sync — missing FLS silently prevents that field from syncing |

The connector user should not be a real person's login. Service account best practice: a dedicated Salesforce user with a System Administrator or custom "MCAE Connector" profile that cannot be deactivated accidentally when someone leaves the organization.

Source: Salesforce Help — Configure the Account Engagement Connector User (https://help.salesforce.com/s/articleView?id=sf.pardot_sf_connector_user.htm)

### Salesforce User Sync

Salesforce User Sync is the mechanism that manages MCAE user creation, deactivation, and role assignment entirely through Salesforce user records and profiles — eliminating the need to separately administer users in the MCAE admin UI.

How it works:
1. An MCAE admin maps one or more Salesforce profiles to MCAE user roles (e.g., Salesforce "Marketing User" profile → MCAE "Marketing" role).
2. Once User Sync is enabled, any Salesforce user assigned to a mapped profile is automatically provisioned in MCAE with the corresponding role.
3. Deactivating a Salesforce user also deactivates their MCAE access automatically.
4. MCAE-native user creation is disabled once User Sync is on.

**Irreversibility:** User Sync cannot be turned off once enabled in a standard production org without a Salesforce Support case. Enable it only when the profile-to-role mapping is finalized and tested.

Source: Salesforce Help — Salesforce User Sync Basics (https://help.salesforce.com/s/articleView?id=sf.pardot_user_sync_basics.htm)

### Prospect Sync and Field-Level Sync Rules

MCAE syncs prospect records to Salesforce Lead and Contact records bidirectionally. Each synced field has a **sync rule** that governs conflict resolution when both sides have different values:

- **Use Salesforce's Value** — Salesforce always wins; MCAE field is overwritten on next sync.
- **Use Pardot's Value** — MCAE always wins; CRM field is overwritten on next sync.
- **Use Most Recently Updated** — whichever side was changed more recently wins. This is the safest default for most fields.

Important constraints:
- MCAE creates a new prospect record when a Lead or Contact with a matching email address is created in Salesforce (or when a form fill is submitted). If an email exists in both MCAE and Salesforce under different records, a merge conflict can produce duplicate prospects.
- Deleted CRM Leads/Contacts optionally sync their deletion to MCAE prospects via the **Recycle Bin sync** setting. This is off by default. Enabling it is destructive — deleted CRM records will archive (soft-delete) the corresponding MCAE prospect.

Source: Salesforce Help — Account Engagement and Salesforce Sync (https://help.salesforce.com/s/articleView?id=sf.pardot_sf_sync_overview.htm)

### Campaign Connector and Attribution

The MCAE campaign connector links MCAE campaigns to Salesforce campaigns for attribution reporting. Required setup:

1. Each MCAE campaign must be associated with a Salesforce campaign (one-to-one mapping).
2. Salesforce campaign **Member Status** values must be mapped to MCAE prospect activities (e.g., "Sent" → email send, "Opened" → email open, "Clicked" → email click, "Responded" → form fill).
3. The Campaign Member record is created in Salesforce when a prospect engages with the associated MCAE campaign.

Without this mapping, MCAE sends do not generate Salesforce Campaign Member records, and first-touch / multi-touch attribution in CRM reports is missing.

---

## Common Patterns

### Pattern: Net-New Business Unit Setup

**When to use:** A new MCAE business unit has just been provisioned for the first time. Nothing is configured.

**How it works:**

1. Install the Account Engagement Lightning App from AppExchange or Setup > App Manager (if not already present).
2. In Salesforce Setup, designate the connector user: assign Marketing User checkbox, confirm View All Data, Modify All Data, and API Enabled permissions.
3. In MCAE, navigate to Account Engagement Settings > Connectors. Open the auto-created Salesforce v2 connector. Verify the connector (it will perform an auth handshake). Click Resume to activate it.
4. Configure the tracking domain under Account Engagement Settings > Domain Management. Set up a CNAME DNS record pointing your chosen subdomain to the MCAE tracking server. Without this, visitor tracking and email link tracking are broken.
5. Set field-level sync rules for all mapped fields. Set high-traffic fields (First Name, Last Name, Email, Company) to "Use Most Recently Updated." Set CRM-authoritative fields (Account ID, Owner ID) to "Use Salesforce's Value."
6. Map Salesforce profiles to MCAE user roles, then enable Salesforce User Sync. Verify that existing MCAE users are not orphaned (they must have matching Salesforce user records before sync is turned on).
7. Configure the campaign connector: create a Salesforce campaign for each MCAE campaign, set Campaign Member Status values, and verify that campaign membership is created on a test form submission.

**Why not configure User Sync before the connector is active:** User Sync depends on a functioning connector. Enabling it before connector activation leaves the BU in an inconsistent state where user records cannot propagate.

### Pattern: Multi-Business-Unit Org

**When to use:** The Salesforce org has multiple MCAE business units (e.g., one per region or product line).

**How it works:**

1. Each BU has its own connector. Each connector has its own connector user (or a shared service account with BU-specific permission sets).
2. Each BU has its own MCAE campaign, prospect, and asset namespace. Prospects do not automatically share across BUs. A Salesforce Lead/Contact can exist in multiple BUs but must be explicitly added to each BU.
3. Users are assigned to BUs individually. A user cannot belong to two BUs in the same org simultaneously via the standard UI. If a Salesforce user needs access to multiple BUs, they need separate Salesforce user records (one per BU) or a Salesforce Support-assisted BU access grant.
4. Tracking domains must be configured per BU. Reusing the same domain across BUs causes tracking attribution to be ambiguous.

**Why not use one BU for all divisions:** Single-BU orgs are simpler but restrict segmentation, campaign autonomy, and reporting to a flat namespace. Multi-BU is the standard pattern for enterprises with distinct marketing teams that should not share prospect lists.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New BU just provisioned, connector shows Paused | Navigate to Account Engagement Settings > Connectors, verify and resume the v2 connector | Default state is Paused; sync will not start until explicitly activated |
| Prospects not syncing despite active connector | Audit connector user FLS on all synced objects and fields | Missing FLS silently excludes fields from sync; connector does not raise an obvious error |
| Marketing team managed separately in MCAE and Salesforce | Enable Salesforce User Sync after mapping profiles to roles | Eliminates dual-admin burden; Salesforce deactivation automatically revokes MCAE access |
| Field value conflicts between MCAE and CRM | Set conflict-prone fields to "Use Most Recently Updated" | Prevents one system permanently overwriting legitimate edits from the other |
| CRM campaign attribution missing in reports | Configure campaign connector with Campaign Member Status mapping | Without mapping, MCAE activities do not generate Campaign Member records in CRM |
| Visitor tracking not recording page visits | Configure tracking domain CNAME in DNS and in MCAE Domain Management | Tracking pixel will not fire until a properly configured tracking domain is active |
| User needs access to multiple BUs in same org | Use separate Salesforce user records per BU or open a Salesforce Support case | Standard MCAE does not support one Salesforce user being active in multiple BUs simultaneously |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Verify Account Engagement Lightning App is installed.** In Salesforce Setup, search for App Manager and confirm the Account Engagement Lightning App is present and assigned to appropriate admin and marketing profiles. Without it, no MCAE navigation appears in Lightning.
2. **Create and configure the connector user.** In Salesforce Setup > Users, identify or create the designated connector service account. Confirm it has: Marketing User checkbox enabled, View All Data, Modify All Data, API Enabled permissions, and read/write FLS on every field intended for sync. Document the user's profile and permission set assignments.
3. **Activate the Salesforce v2 connector.** In Account Engagement Settings > Connectors, open the auto-created connector. Run the verification (auth handshake). Click Resume. Confirm the connector status changes from Paused to Active. Monitor the connector status page for the first 15 minutes to catch auth errors.
4. **Configure the tracking domain.** In Account Engagement Settings > Domain Management, add the tracking subdomain. Create the corresponding CNAME DNS record at the domain registrar pointing to the MCAE tracking server hostname. Allow DNS propagation (up to 24–48 hours). Verify the domain shows as Active in MCAE.
5. **Set field-level sync rules.** Review the default sync rule for each mapped field. Set CRM-authoritative fields (Owner, Account lookup, custom CRM IDs) to "Use Salesforce's Value." Set MCAE-authoritative fields (marketing opt-out, MCAE score, grade) to "Use Pardot's Value." Set shared fields (name, company, phone) to "Use Most Recently Updated."
6. **Enable Salesforce User Sync.** Map Salesforce profiles to MCAE user roles in Account Engagement Settings > User Management. Verify that every current MCAE user has a matching Salesforce user record. Enable User Sync. Confirm that existing MCAE users are synchronized to the correct roles and that newly added Salesforce users on mapped profiles appear in MCAE automatically.
7. **Configure campaign connector and validate end-to-end sync.** Associate MCAE test campaigns with Salesforce campaigns. Map Campaign Member Status values. Submit a test form fill, confirm a new prospect is created in MCAE, synced to a Salesforce Lead or Contact, and a Campaign Member record is created in the associated Salesforce campaign. Run through the review checklist.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Account Engagement Lightning App is installed and visible in Lightning navigation for admin and marketing users
- [ ] Connector user holds Marketing User, View All Data, Modify All Data, and API Enabled permissions
- [ ] Connector user has read/write FLS on all objects and fields intended for sync (Lead, Contact, Account, Opportunity, Campaign)
- [ ] Salesforce v2 connector status is Active (not Paused, not Error) in Account Engagement Settings > Connectors
- [ ] Tracking domain CNAME is configured in DNS and shows Active in MCAE Domain Management
- [ ] Field-level sync rules are configured for all synced fields; no field is left on a default that contradicts org data ownership policy
- [ ] Salesforce User Sync is enabled and profile-to-role mapping is complete
- [ ] At least one MCAE user is confirmed provisioned via User Sync (not manually created in MCAE after sync was enabled)
- [ ] Campaign connector is active; at least one MCAE campaign is linked to a Salesforce campaign with Campaign Member Status values mapped
- [ ] End-to-end test: test form submission creates an MCAE prospect, syncs to a Salesforce Lead or Contact, and generates a Campaign Member record
- [ ] Recycle Bin sync setting is explicitly set (enabled or disabled) based on stakeholder decision — not left on an untested default

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Connector starts Paused — sync never starts without explicit activation** — Every new MCAE business unit auto-creates a v2 connector in a Paused state. This is not an error; it is the designed default. Practitioners who expect sync to begin immediately after BU provisioning will wait indefinitely. The fix is to navigate to Account Engagement Settings > Connectors, verify the connector, and click Resume.
2. **Connector user FLS silently blocks field sync without an error** — If the connector user's profile does not have read or write permission on a specific field, that field simply does not sync. There is no error in the connector status, no sync failure alert, and no log entry visible to the admin. Practitioners must proactively audit FLS on every field, not rely on the system to surface missing permissions.
3. **User Sync is irreversible — enabling it permanently changes the user management model** — Once Salesforce User Sync is turned on, MCAE-native user creation and role editing in the MCAE admin UI are hidden. Rolling this back requires a Salesforce Support case. Enable User Sync only after testing profile-to-role mappings in a sandbox and confirming every active MCAE user has a matching Salesforce record. Do not enable User Sync as a quick step during initial setup without this verification.
4. **Prospect email address is the sync key — duplicate emails cause phantom records** — MCAE matches CRM Leads and Contacts to prospects by email address. If the same email exists as both a Lead and a Contact in Salesforce, MCAE creates two separate prospects, one for each. If the email exists in MCAE and a newly imported CRM record uses the same email, a sync conflict can result in data overwrite rather than merge. Deduplication should be run in both systems before the first sync.
5. **Recycle Bin sync is off by default — but enabling it retroactively deletes MCAE prospects** — The Recycle Bin sync option causes MCAE prospects to be archived (soft-deleted) when their matching CRM Lead or Contact is deleted. This setting is off by default. If it is enabled after the BU has been running, any CRM records already in the Recycle Bin will trigger prospect archival on the next sync cycle. Turning this on without auditing the Recycle Bin first can cause unexpected bulk prospect deletion.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Connector activation checklist | Step-by-step verification that the v2 connector is active, authenticated, and syncing |
| Connector user permission matrix | Table of required Salesforce permissions and FLS for the connector service account |
| Field sync rule matrix | List of all synced fields with their configured sync rule and ownership rationale |
| Salesforce User Sync enablement guide | Profile-to-role mapping table and step-by-step User Sync activation sequence |
| Campaign connector configuration steps | Instructions for linking MCAE campaigns to Salesforce campaigns with Member Status mapping |
| Tracking domain setup checklist | DNS CNAME configuration steps and MCAE Domain Management activation verification |
| End-to-end test script | Form fill → prospect creation → CRM sync → Campaign Member creation validation steps |

---

## Related Skills

- `lead-scoring-requirements` — governs how MCAE prospect score and grade fields are mapped to Salesforce Lead fields and used in MQL logic; build this skill's outputs after MCAE sync is active
- `integration/mulesoft-salesforce-connector` — if prospect data flows through MuleSoft before reaching Salesforce, this skill covers the connector configuration layer that sits upstream of MCAE sync
