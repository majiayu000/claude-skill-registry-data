---
name: event-monitoring
description: "Shield Event Monitoring: event log types, downloading logs via REST API and SOQL, real-time event monitoring with streaming API, and threat detection policies. NOT for debug logs (use debug-logs-and-developer-console). NOT for custom platform event publishing/subscribing (use platform-events-apex)."
category: security
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Operational Excellence
triggers:
  - "how do I download event log files from Salesforce"
  - "track user login activity and suspicious behavior in my org"
  - "set up real-time event monitoring to detect session hijacking"
  - "query EventLogFile to see who exported report data"
  - "enable threat detection for credential stuffing attacks"
  - "API anomaly detection with Shield event monitoring"
tags:
  - event-monitoring
  - shield
  - event-log-file
  - threat-detection
  - real-time-events
  - audit
inputs:
  - "Salesforce org with Shield or Event Monitoring add-on license"
  - "API access credentials (connected app OAuth or session ID)"
  - "target event types to monitor (e.g., Login, Report, ApexExecution)"
  - "retention window requirements (1-day free vs. 30-day Shield)"
outputs:
  - "SOQL queries for EventLogFile retrieval"
  - "REST API calls to download log CSV content"
  - "Real-Time Event Monitoring channel and member configuration (Metadata API XML)"
  - "Transaction Security policy design recommendations"
  - "Threat detection event object query patterns"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Event Monitoring

This skill activates when a practitioner needs to audit user activity, download event log files, configure real-time threat detection, or investigate security anomalies in a Salesforce org. It covers both batch EventLogFile-based monitoring and real-time streaming-based monitoring via Shield. It does not cover debug logs (see debug-logs-and-developer-console) or custom platform event publishing (see platform-events-apex).

---

## Before Starting

Gather this context before working on anything in this domain:

- **License check**: Event Monitoring requires either a Salesforce Shield subscription or the Event Monitoring add-on. Without one of these, only five basic event types (Login, Logout, URI, API Total Usage, Apex Unexpected Exception) are available with 1-day retention.
- **Real-Time vs. Batch**: Event Log Files (batch, next-day) and Real-Time Event Monitoring (streaming, immediate) are distinct access patterns. Confirm which the request requires.
- **Permissions**: "View Event Log Files" permission is needed for EventLogFile access. "View Real-Time Event Monitoring Data" permission is required for RTEM streaming events.
- **Log delay**: Standard Event Log Files are generated once per day with a 24-hour delay. Hourly log files are available for Shield customers only.
- **CSV delivery**: EventLogFile content is a gzip-compressed CSV retrieved via a separate REST call — not returned inline in the SOQL query result.

---

## Core Concepts

### Mode 1 — Event Log Files (Batch)

Event Log Files are the primary mechanism for historical audit analysis. They are stored as the `EventLogFile` sObject and queryable via SOQL.

Key fields on `EventLogFile`:
- `EventType` — category of activity (e.g., `Login`, `Report`, `ApexExecution`, `URI`, `API`, `VisualforceRequest`, `BulkApi`, `Dashboard`, `ContentTransfer`, `Knowledge`)
- `LogDate` — the calendar date the log covers; not a timestamp of individual events
- `LogFile` — virtual field; retrieve via REST as `/sobjects/EventLogFile/{Id}/LogFile` to get gzip CSV bytes
- `LogFileLength` — file size in bytes
- `Interval` — `Hourly` (Shield only) or `Daily`
- `Sequence` — for hourly logs, the sequence number within the day

There are 70+ event types. Security-relevant examples: `Login`, `LoginAs`, `Logout`, `API`, `Report`, `ContentTransfer`, `ApexExecution`, `BulkApi`, `URI`, `VisualforceRequest`.

**Retention:**
- Without Shield or add-on: 1-day retention, 24-hour delay, 5 event types only
- With Shield or Event Monitoring add-on: 30-day retention, daily logs for all 70+ types; hourly logs for Shield

**SOQL query pattern:**
```soql
SELECT Id, EventType, LogDate, LogFileLength, Interval
FROM EventLogFile
WHERE EventType = 'Login'
  AND LogDate = LAST_N_DAYS:7
ORDER BY LogDate DESC
```

**Download log content via REST (Id from above SOQL):**
```
GET /services/data/v63.0/sobjects/EventLogFile/{Id}/LogFile
Authorization: Bearer {sessionId}
```
Response: gzip-compressed CSV. First row is the column header. Each subsequent row is one event record. Column names and semantics are event-type specific and documented in the EventLogFile Object Reference.

### Mode 2 — Real-Time Event Monitoring (RTEM)

Real-Time Event Monitoring delivers security events as they happen, via Streaming API (CometD) or Pub/Sub API. Events fire in real time rather than in a next-day batch.

**Requires:** Salesforce Shield OR Event Monitoring add-on, plus the "View Real-Time Event Monitoring Data" user permission.

RTEM events follow the naming convention `ObjectNameEvent` (e.g., `LoginEvent`, `ApiAnomalyEvent`, `FileEvent`). Corresponding storage objects (`ObjectNameEventStore` or `ObjectNameEventStream` for older API versions) persist event data for post-hoc SOQL queries.

Key RTEM event types:
- `LoginEvent` / `LoginEventStream` — every login attempt
- `LogoutEvent` / `LogoutEventStream` — logouts
- `LoginAsEvent` / `LoginAsEventStream` — admin impersonation of another user
- `ApiEventStream` — individual API calls
- `ReportEventStream` — report runs
- `LightningUriEventStream` — Lightning page navigations
- `ListViewEventStream` — list view access
- `UriEventStream` — classic UI navigation
- `FileEvent` — file downloads and uploads
- `PermissionSetEvent` — permission set assignment changes

**Threat Detection events** (ML-powered, Shield only):
- `ApiAnomalyEvent` — anomalous API call patterns (available API v50.0+)
- `ReportAnomalyEvent` — unusual report export behavior
- `SessionHijackingEvent` — session token reused from a different IP or browser fingerprint
- `CredentialStuffingEvent` — high-volume brute-force login attempts
- `GuestUserAnomalyEvent` — anomalous guest user behavior
- `LoginAnomalyEvent` — login pattern deviations
- `PermissionSetEvent` — anomalous permission assignment activity

**ML processing lag note:** Threat Detection models require brief processing time. The `EventDate` on anomaly events reflects when the ML model reported the anomaly — not the exact moment the suspicious action occurred. Do not treat the timestamp as perfectly synchronous with the underlying activity.

### Mode 3 — Transaction Security Policies

Transaction Security Policies evaluate RTEM events and fire automated enforcement actions in real time. They are the enforcement layer on top of RTEM.

Available enforcement actions:
- Block the operation immediately
- Require multi-factor authentication (MFA) step-up
- Send email or in-app notification
- Trigger custom Apex logic

Policies are configured in Setup > Security > Transaction Security Policies. Each policy references an RTEM event type, defines condition logic, and specifies the action.

**Not all RTEM events support Transaction Security Policies.** Several event types (e.g., `MobileEmailEvent`, `MobileScreenshotEvent`, `IdentityProviderEvent`, `IdentityVerificationEvent`) do not support policy enforcement. Always verify the `Can Be Used in a Transaction Security Policy?` flag in the Object Reference before designing enforcement logic.

---

## Common Patterns

### Pattern: Bulk Log Download for SIEM Integration

**When to use:** You need to feed Salesforce event data into a SIEM (Splunk, Sumo Logic, etc.) or export logs for compliance analysis.

**How it works:**
1. SOQL query `EventLogFile` for the desired `EventType` and `LogDate` range.
2. For each record returned, issue an authenticated REST GET on `/services/data/v63.0/sobjects/EventLogFile/{Id}/LogFile`.
3. Decompress the gzip response. Parse the CSV. The first row contains column headers.
4. Load parsed rows into the SIEM or data store.
5. Track the latest `LogDate` successfully processed to avoid re-ingesting on subsequent runs.

**Why not the alternative:** Attempting to read the `LogFile` field inline in SOQL returns only a relative endpoint path, not the binary content. The CSV bytes always require a separate authenticated REST call.

### Pattern: Real-Time Threat Alerting with RTEM + Transaction Security

**When to use:** You need immediate enforcement response to suspicious activity — e.g., block or challenge a session hijack in progress rather than discover it next day.

**How it works:**
1. Confirm Shield license and enable RTEM in Setup > Security > Real-Time Event Monitoring.
2. Create a `PlatformEventChannel` with `channelType=event` and `eventType=monitoring`.
3. Add target events as `PlatformEventChannelMember` records (one per event type per channel).
4. Subscribe via CometD or Pub/Sub API to receive events in real time.
5. For automated enforcement, create a Transaction Security Policy on the event type (e.g., block logins from unrecognized IP ranges using `LoginEvent`).

**Metadata API configuration:**
```xml
<!-- PlatformEventChannel -->
<PlatformEventChannel>
  <channelType>event</channelType>
  <eventType>monitoring</eventType>
  <label>Security Monitoring Channel</label>
</PlatformEventChannel>

<!-- PlatformEventChannelMember for ApiAnomalyEvent -->
<PlatformEventChannelMember>
  <eventChannel>Security_Monitoring_Channel__chn</eventChannel>
  <selectedEntity>ApiAnomalyEvent</selectedEntity>
</PlatformEventChannelMember>
```

**Why not the alternative:** EventLogFile batch approach cannot block or challenge a suspicious session in real time — it only reveals what happened the following day.

### Pattern: SOQL-Based Login Forensics

**When to use:** A user account may have been compromised; you need to reconstruct login history, source IPs, browser fingerprints, and login status codes.

**How it works:**
1. Query `EventLogFile` for `EventType = 'Login'` over the desired date range.
2. Download the CSV. Key columns: `USER_ID`, `SOURCE_IP`, `BROWSER_TYPE`, `PLATFORM_TYPE`, `LOGIN_STATUS`, `CLIENT_VERSION`, `SESSION_TYPE`.
3. Filter on `LOGIN_STATUS != 'LOGIN_NO_ERROR'` to isolate authentication failures.
4. Cross-reference `USER_ID` values with User sObject records.
5. For same-day data (not yet in EventLogFile), query `LoginEventStream` directly via SOQL.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Compliance audit — who exported data last quarter | EventLogFile (batch) SOQL + REST download | Historical coverage, up to 30 days with Shield |
| Block suspicious logins in real time | RTEM + Transaction Security Policy on LoginEvent | Fires synchronously; can block or challenge immediately |
| SIEM integration for ongoing ingestion | EventLogFile REST download (daily or hourly) | Structured CSV output; standard log-shipper compatible |
| Detect session hijacking | RTEM SessionHijackingEvent | ML-powered, near-real-time detection |
| Investigate a specific user's API calls | EventLogFile EventType = 'API' | Per-call detail; filter by USER_ID column after download |
| Enforce MFA on logins from new locations | Transaction Security Policy on LoginEvent | Native MFA enforcement; no custom code required |
| Monitor file downloads for data exfiltration | RTEM FileEvent (real-time) or ContentTransfer log (historical) | FileEvent for immediate alerting; ContentTransfer for audit trail |
| Same-day login activity (incident in progress) | Query LoginEventStream or LoginAsEventStream | RTEM storage objects available immediately; EventLogFile unavailable until tomorrow |

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

- [ ] Confirmed org has Shield or Event Monitoring add-on; not relying on free 5-type tier for non-basic event types
- [ ] User has "View Event Log Files" or "View Real-Time Event Monitoring Data" permission as appropriate
- [ ] Log downloads use a separate REST GET on `/sobjects/EventLogFile/{Id}/LogFile`, not inline SOQL
- [ ] SOQL queries filter on `LogDate` (not `CreatedDate`) to match the event coverage window correctly
- [ ] For RTEM, PlatformEventChannel has `eventType=monitoring` set — not a plain custom platform event channel
- [ ] Transaction Security Policy event types verified for policy-enforcement support before implementation
- [ ] Retention window acknowledged: 1-day (free), 30-day (Shield/add-on)
- [ ] Hourly vs. daily `Interval` distinction confirmed; hourly requires Shield subscription

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **LogFile field returns a URL path, not CSV content** — Querying `SELECT LogFile FROM EventLogFile` does not return the CSV bytes. It returns a relative URL path. You must issue a separate authenticated REST GET to `/services/data/vXX.0/sobjects/EventLogFile/{Id}/LogFile` with a valid Bearer token to retrieve the actual gzip CSV.

2. **24-hour delay makes same-day forensics impossible with EventLogFile** — EventLogFile records for a given `LogDate` are not available until the following UTC day. If an incident is unfolding today, EventLogFile cannot show today's activity. Use RTEM storage objects (e.g., `LoginEventStream`) or the Setup > Login History UI for same-day data.

3. **Not all RTEM events support Transaction Security policies** — Several events including `MobileEmailEvent`, `MobileScreenshotEvent`, `IdentityProviderEvent`, and `IdentityVerificationEvent` explicitly do not support policy enforcement. Designing a policy on an unsupported event type will not produce enforcement behavior.

4. **Threat Detection ML events have a processing lag** — `ApiAnomalyEvent`, `ReportAnomalyEvent`, `SessionHijackingEvent`, and similar ML-powered events do not fire the instant the suspicious action occurs. The `EventDate` field reflects when the ML model completed its evaluation. Do not assume this timestamp equals the moment of the underlying suspicious activity.

5. **Free tier covers only 5 event types** — Without Shield or the add-on, only Login, Logout, URI, API Total Usage, and Apex Unexpected Exception events are available. Many practitioners assume all event types are included at no cost. This gap causes silent misses when trying to audit Report exports, ContentTransfer downloads, or VisualforceRequest activity.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| SOQL query for EventLogFile | Parameterized query by EventType and LogDate range for log discovery |
| REST download command | Authenticated GET for log CSV binary content |
| RTEM channel configuration (Metadata API XML) | PlatformEventChannel + PlatformEventChannelMember deployment metadata |
| Transaction Security Policy design | Event type, condition logic, and enforcement action specification |
| Threat detection query | SOQL against EventStore objects for post-hoc anomaly review |

---

## Related Skills

- debug-logs-and-developer-console — for Apex debug logs and Developer Console log analysis (not event monitoring)
- platform-events-apex — for custom platform event publishing and subscriber trigger patterns
- platform-encryption — for Shield Platform Encryption; often deployed alongside Event Monitoring in a Shield org
- apex-security-and-access-control — for CRUD/FLS enforcement patterns referenced in security audit contexts
