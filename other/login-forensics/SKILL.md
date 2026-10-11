---
name: login-forensics
description: "Investigate Salesforce login activity using LoginHistory, IdentityVerificationHistory, and Login Forensics (Event Monitoring add-on): reconstruct per-user login timelines, identify failed logins, analyze source IPs, review identity verification events, and configure Login Flows for step-up authentication. NOT for MFA setup (use org-setup-and-configuration). NOT for downloading EventLogFile CSVs or configuring real-time threat detection (use event-monitoring)."
category: security
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Operational Excellence
triggers:
  - "a user account may have been compromised and I need to see their recent login history"
  - "how do I find all failed login attempts for a specific user in the last 30 days"
  - "we had a suspected credential stuffing attack and need to identify affected accounts by source IP"
  - "show me which users logged in from an unexpected country or IP address"
  - "how do I check if a user bypassed MFA or identity verification during login"
  - "I need to audit who logged in during a specific time window for a compliance review"
  - "set up a Login Flow to enforce step-up authentication for privileged users"
tags:
  - login-forensics
  - login-history
  - identity-verification
  - login-flow
  - security-audit
  - incident-response
inputs:
  - "Salesforce org with System Administrator profile or 'View Login Forensics' permission (for Login Forensics add-on)"
  - "UserId or username of the account(s) under investigation"
  - "Time window for investigation (LoginHistory stores up to 6 months)"
  - "For Login Forensics feature: Event Monitoring add-on license required"
outputs:
  - "SOQL queries against LoginHistory and IdentityVerificationHistory for incident reconstruction"
  - "Login Forensics session detail queries (requires Event Monitoring add-on)"
  - "IP-based anomaly analysis query patterns"
  - "Login Flow configuration guidance for step-up authentication"
  - "Remediation checklist: freeze account, revoke sessions, rotate credentials"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Login Forensics

This skill activates when a practitioner needs to investigate individual or bulk user login activity in a Salesforce org — reconstructing timelines, identifying failed or anomalous logins, analyzing source IPs, reviewing identity verification outcomes, and tracing session origins. It covers the `LoginHistory` sObject (free, 6-month retention), the Login Forensics feature in the Event Monitoring add-on (extended session metadata), `IdentityVerificationHistory`, and Login Flows. It does not cover MFA configuration (use org-setup-and-configuration), EventLogFile bulk log download (use event-monitoring), or real-time threat detection (use event-monitoring).

---

## Before Starting

Gather this context before working on anything in this domain:

- **LoginHistory retention**: The `LoginHistory` standard object retains records for up to 6 months. Records older than 6 months are automatically purged. If the investigation window exceeds 6 months, no recovery path exists unless the org exports to a SIEM.
- **Login Forensics vs. LoginHistory**: "Login Forensics" (capital F) refers specifically to a feature in the Event Monitoring add-on that provides enriched per-session data beyond what `LoginHistory` contains — including session duration, pages accessed, and correlated API calls. Free orgs only have `LoginHistory`. Confirm which the requester has.
- **Permission required**: SOQL on `LoginHistory` requires the "View Login Forensics" permission (Salesforce Shield / Event Monitoring add-on) OR System Administrator profile. Standard users cannot query other users' `LoginHistory` records.
- **LoginHistory is read-only**: You cannot insert, update, or delete `LoginHistory` records. Attempts will throw a `System.DmlException`.
- **Limits**: SOQL against `LoginHistory` supports a maximum of 30,000 rows per query. For high-volume orgs, always filter by `LoginTime` and `UserId` to avoid governor limit failures.

---

## Core Concepts

### Mode 1 — LoginHistory SOQL (Free, All Orgs)

The `LoginHistory` sObject is available in every Salesforce org at no extra cost and stores up to 6 months of login records. Key fields:

| Field | Type | Notes |
|---|---|---|
| `UserId` | ID | The user who attempted the login |
| `LoginTime` | DateTime | UTC timestamp of the login attempt |
| `LoginType` | String | e.g., `Application`, `SAML Federated SSO`, `Remote Access 2.0` |
| `LoginUrl` | String | The login endpoint used (e.g., `login.salesforce.com`, custom domain) |
| `SourceIp` | String | IPv4 or IPv6 source address |
| `Status` | String | `Success`, `Failed`, `Invalid Password`, `No Salesforce.com Access`, etc. |
| `Browser` | String | User-Agent browser string |
| `Platform` | String | Operating system reported by the client |
| `AuthenticationServiceId` | ID | Identity provider for SSO logins |

Query pattern for failed logins over a period:

```soql
SELECT UserId, LoginTime, LoginType, SourceIp, Status, Browser, Platform
FROM LoginHistory
WHERE LoginTime >= 2025-01-01T00:00:00Z
  AND LoginTime <= 2025-03-31T23:59:59Z
  AND Status != 'Success'
ORDER BY LoginTime DESC
LIMIT 1000
```

Query pattern for a specific user's full login timeline:

```soql
SELECT LoginTime, LoginType, SourceIp, Status, Browser, Platform
FROM LoginHistory
WHERE UserId = '005XXXXXXXXXXXXXXX'
ORDER BY LoginTime DESC
LIMIT 500
```

IP-based breadth query — find all users who logged in from a suspicious IP block:

```soql
SELECT UserId, LoginTime, SourceIp, Status
FROM LoginHistory
WHERE SourceIp LIKE '203.0.113.%'
  AND LoginTime >= LAST_N_DAYS:30
ORDER BY LoginTime DESC
```

### Mode 2 — Login Forensics Feature (Event Monitoring Add-On)

The Login Forensics feature (available with Salesforce Shield or the Event Monitoring add-on) extends session-level data beyond `LoginHistory`. It surfaces:

- Session duration and activity patterns per login session
- Correlated API usage within a session
- More granular event details accessible via the `LoginEvent` object in Real-Time Event Monitoring

The `LoginEvent` object is part of Real-Time Event Monitoring (RTEM) and is distinct from `LoginHistory`. It fires as a streaming event, not a stored record. To analyze historical login events at this level, use the `EventLogFile` with `EventType = 'Login'` (covered by the event-monitoring skill).

For Login Forensics specifically, the workflow is:

1. Navigate to Setup > Login Forensics to access the UI-based drill-down for per-session investigation.
2. Filter by user, date range, or session ID.
3. Export session data for SIEM ingestion if needed.

### Mode 3 — IdentityVerificationHistory and Login Flows

**IdentityVerificationHistory** tracks when Salesforce prompted a user for identity verification (e.g., email verification code, SMS, TOTP authenticator) and whether they passed or bypassed:

```soql
SELECT UserId, VerificationTime, Activity, Status, Comments
FROM IdentityVerificationHistory
WHERE UserId = '005XXXXXXXXXXXXXXX'
ORDER BY VerificationTime DESC
LIMIT 200
```

Status values include `Success`, `Failure`, `Skipped`, and `Trusted`. A `Skipped` or `Trusted` status means the user was not prompted — investigate whether their device/network was trusted unexpectedly.

**Login Flows** are Screen Flows attached to a profile or connected app via Setup > Login Flows. They intercept the login process after credential validation and before session creation, allowing conditional step-up authentication:

- Use case: require an additional TOTP code for users in a privileged profile
- Use case: block logins from non-approved countries by calling a Flow-invocable Apex class that checks `$Flow.CurrentDate` and source IP
- Login Flows do not themselves log events; the underlying `LoginHistory` record is still created

---

## Common Patterns

### Pattern: Incident Response Login Timeline Reconstruction

**When to use:** A user account is suspected compromised. You need to reconstruct the full timeline of login events, including source IPs, browser fingerprints, and failure patterns, to determine the blast radius.

**How it works:**
1. Query `LoginHistory` for the user over the suspected window:
   ```soql
   SELECT LoginTime, LoginType, SourceIp, Status, Browser, Platform, LoginUrl
   FROM LoginHistory
   WHERE UserId = '005XXXXXXXXXXXXXXX'
     AND LoginTime >= LAST_N_DAYS:30
   ORDER BY LoginTime DESC
   ```
2. Pivot on `SourceIp` — group IPs that appear across multiple users to detect credential stuffing:
   ```soql
   SELECT SourceIp, COUNT(Id) loginCount, COUNT_DISTINCT(UserId) affectedUsers
   FROM LoginHistory
   WHERE LoginTime >= LAST_N_DAYS:7
     AND Status != 'Success'
   GROUP BY SourceIp
   ORDER BY loginCount DESC
   ```
3. Cross-reference with `IdentityVerificationHistory` to see whether MFA was completed or skipped:
   ```soql
   SELECT UserId, VerificationTime, Activity, Status
   FROM IdentityVerificationHistory
   WHERE UserId = '005XXXXXXXXXXXXXXX'
   ORDER BY VerificationTime DESC
   LIMIT 50
   ```
4. Freeze the user account in Setup > Users while the investigation continues.
5. Revoke active sessions: Setup > Session Management, or via Apex: `Auth.SessionManagement.revokeSessionsForUser(userId)`.

**Why not to rely on the UI alone:** Setup > Login History in the UI only shows the most recent 20,000 records and does not support complex filtering or cross-user pivots. SOQL is mandatory for incident response at any scale.

### Pattern: Geo-Anomaly Detection Without Shield

**When to use:** The org does not have Shield or Event Monitoring, but the security team wants to identify logins from unexpected geographies using free tools.

**How it works:**
1. Export `LoginHistory` via SOQL using the REST API or Data Loader.
2. Run the exported `SourceIp` values through a free IP geolocation API (e.g., `ip-api.com`) in a local Python script.
3. Flag logins from country codes outside the org's known user base.
4. Note: Salesforce does **not** include country or region in `LoginHistory` natively — IP-to-geo mapping must be done externally.

**Why not built-in geo-blocking:** Transaction Security Policies (event-monitoring skill) can block logins by country in real time, but that requires the Shield or Event Monitoring add-on. For free orgs, Login Hours + Login IP Ranges on profiles are the only native controls.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Investigate a single compromised user's login history | SOQL on `LoginHistory` filtered by `UserId` | Fastest; free; 6-month lookback |
| Find all users affected by a suspicious source IP | SOQL on `LoginHistory` grouped by `SourceIp` | Cross-user pivot not possible in UI |
| Check whether MFA was completed or bypassed | SOQL on `IdentityVerificationHistory` | Dedicated table for verification outcomes |
| Review enriched session-level details (pages visited, API calls per session) | Login Forensics feature in Setup (requires Event Monitoring add-on) | `LoginHistory` alone does not have session-level correlation |
| Block logins from unauthorized countries in real time | Transaction Security Policy (event-monitoring skill) | Real-time enforcement requires RTEM |
| Force step-up auth for a privileged profile at login time | Login Flow attached to the profile | Login Flows intercept login before session creation |
| Export login data to a SIEM for long-term retention beyond 6 months | Automate periodic SOQL export via REST API into external storage | `LoginHistory` purges at 6 months; SIEM provides indefinite retention |

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

Run through these before marking work in this area complete:

- [ ] Confirmed whether the org has the Event Monitoring add-on (determines Login Forensics feature availability)
- [ ] SOQL queries are filtered by `LoginTime` range to avoid querying full table and hitting 30,000-row limit
- [ ] Cross-user IP pivot query run to identify credential stuffing scope
- [ ] `IdentityVerificationHistory` checked for `Skipped` or unexpected `Trusted` statuses
- [ ] Compromised account frozen in Setup > Users and active sessions revoked
- [ ] Investigation window confirmed against 6-month `LoginHistory` retention limit
- [ ] If Login Flow is being configured: tested against all affected profiles in a sandbox first

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **LoginHistory only retains 6 months — there is no admin override** — Records are automatically purged at the 6-month mark. There is no configuration option to extend retention, no recycle bin for these records, and no way to recover purged data. If an investigation spans longer than 6 months, the data simply does not exist in Salesforce unless the org was exporting it to a SIEM continuously.

2. **SourceIp can be a Salesforce internal IP for API logins** — When an integration or connected app authenticates using the OAuth client credentials flow or IP relaxation, the `SourceIp` field may reflect a Salesforce internal datacenter IP rather than the true client IP. This causes IP allowlisting checks to produce false negatives and makes geo-analysis unreliable for API-based logins.

3. **Status field values are not normalized across LoginType** — The `Status` field contains inconsistent values depending on whether the login was a UI login, SAML SSO, or API login. For example, a SAML login failure may appear as `Failed` while a direct login failure appears as `Invalid Password`. Grouping all failures as `Status != 'Success'` is the only reliable cross-type failure query pattern.

4. **Login Forensics (the feature) requires a separate permission — "View Login Forensics"** — Having Event Monitoring access does not automatically grant access to the Login Forensics Setup page. The `View Login Forensics` permission must be explicitly granted on the profile or permission set. Forgetting this is a common cause of 403 errors when trying to access Setup > Login Forensics.

5. **IdentityVerificationHistory 'Trusted' does not mean MFA was performed** — A `Trusted` status means the user's device or network was registered as trusted, so Salesforce skipped the MFA prompt entirely. This is expected behavior if the org allows trusted devices, but it can appear in an audit as an MFA bypass when it is actually by design. Investigate the `Activity` field value (`High Assurance Login`, `Identity Verification`) to understand what was being verified.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| LoginHistory SOQL queries | Parameterized queries for single-user timelines, cross-user IP pivots, and failure-only filters |
| IdentityVerificationHistory SOQL | Queries to surface MFA skips and verification failures |
| Login Forensics investigation workflow | Step-by-step Setup UI procedure for enriched session drill-down (Event Monitoring add-on required) |
| Login Flow configuration guidance | Profile-attached Flow setup for step-up authentication enforcement |
| Incident response checklist | Freeze account, revoke sessions, rotate credentials, notify users |

---

## Related Skills

- `event-monitoring` — Use when you need to download EventLogFile Login logs in bulk, configure real-time event monitoring, or set up Transaction Security Policies to block logins by country or IP
- `org-setup-and-configuration` — Use for MFA enablement, session settings (timeout, IP locking), and Login Hours/IP Ranges on profiles
- `transaction-security-policies` — Use when you need real-time enforcement policies that react to login events automatically
