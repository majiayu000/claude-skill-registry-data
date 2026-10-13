---
name: operating-n8n-production
version: "2.1.0"
description: >
  Manages n8n workflow automation in production — credential management,
  execution monitoring, error handling, workflow versioning, worker health,
  and blocked workflow recovery. Covers the Base44 Bearer credentials pattern
  and SCH-02 lane field fix for the FlashFusion platform. Activates when
  running n8n in production, fixing blocked or failing workflows, rotating
  n8n credentials, monitoring execution logs, handling silent workflow
  failures, diagnosing n8n errors, setting up error alerting, managing
  workflow versions, or debugging n8n integration with Supabase or Base44.
  Also triggers on: n8n down, workflow not running, credential expired,
  execution failed, n8n cloud vs self-hosted, n8n webhook error.
  NOTE: n8n MCP is currently CONNECTION_ISSUE. All live ops use manual
  fallbacks at https://krosebrook.app.n8n.cloud until MCP is restored.
allowed-tools: Read Write Bash
disable-model-invocation: false
---

# n8n Production Operations

Covers the operational layer between building workflows and keeping them
running reliably. Building is covered in `workflow-automation` and
`ai-agents-workflow`. This skill takes over after the workflow ships.

---

## DEPENDENCY_DECLARATION

```yaml
tools_required:
  - name: n8n
    status: CONNECTION_ISSUE
    fallback: Manual operations at https://krosebrook.app.n8n.cloud
    note: All sections requiring n8n MCP must include the manual URL fallback
FAIL_IF:
  - n8n MCP unavailable → print: "n8n MCP has a connection issue. Navigate manually to https://krosebrook.app.n8n.cloud to complete this step." Do not attempt MCP calls.
  - n8n MCP returns auth error → same as above
```

**Operational semantics (apply when FAIL_IF fires):**
- Do NOT simulate, guess, or fabricate MCP responses. Print the manual fallback
  path for the requested operation (see each section's CONNECTION CHECK box) and
  hand off the n8n UI steps to the user with the exact URL.
- "Just do it" override: if the user explicitly says "try the MCP anyway" or
  "attempt it regardless," attempt the call once and report the exact error
  returned. Do not retry silently.
- Recovery: when MCP reconnects, confirm via Settings → Integrations → MCP in
  Claude.ai. No skill changes needed — MCP calls resume automatically.

---

## Decision Tree

```
What do you need?
  │
  ├─ Fix a blocked workflow (Base44, SCH-02, or credential error)
  │    → Section 1: Blocked Workflow Recovery
  │    → [n8n MCP required for automated fix — manual fallback documented]
  │
  ├─ A workflow failed silently — nothing ran, no error
  │    → Section 2: Silent Failure Diagnosis
  │    → [n8n MCP required for log access — manual fallback documented]
  │
  ├─ Set up monitoring so failures surface automatically
  │    → Section 3: Error Alerting Setup
  │    → [n8n MCP required for workflow creation — manual fallback documented]
  │
  ├─ Rotate or audit credentials
  │    → Section 4: Credential Management
  │    → [n8n MCP required for credential read/write — manual fallback documented]
  │
  ├─ Version or backup workflows before a change
  │    → Section 5: Workflow Versioning
  │    → [n8n MCP required for export — manual fallback documented]
  │
  └─ Worker is slow, hanging, or unresponsive
       → Section 6: Worker Health
       → [n8n MCP required for status read — manual fallback documented]
```

---

## Section 1: Blocked Workflow Recovery

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot update credentials or trigger workflows via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Credentials** (for Base44 fix)
> Manual path: **https://krosebrook.app.n8n.cloud → Workflows → [workflow name] → Edit** (for SCH-02 fix)
> Steps below are valid — execute them in the n8n Cloud UI, not via MCP.

### The Base44 Bearer Credentials Problem

**Symptom:** Workflows calling Base44 APIs return 401 Unauthorized or
silently fail without execution. Affects the 11 workflows connected to
the FlashFusion platform (app.flashfusion.co).

**Root cause:** Base44 uses short-lived Bearer tokens, not static API keys.
n8n credential stores treat these as static credentials. When the token
expires, every workflow using that credential fails at the HTTP Request node.

**Fix:**

1. In Base44, navigate to Settings → API → Generate Token
2. Copy the new Bearer token
3. In n8n: **https://krosebrook.app.n8n.cloud → Credentials** → find
   `Base44 Bearer` credential → Edit
4. Update the Authorization header value: `Bearer <new_token>`
5. Save. Run the simplest affected workflow manually to confirm.
6. Set a calendar reminder to rotate this token on its expiry schedule.
   If Base44 doesn't show an expiry, rotate every 30 days.

**Prevention:** Add a workflow that tests the Base44 credential weekly
and sends a Slack/email notification before it expires. Wire it to the
Error Alerting setup in Section 3.

### The SCH-02 Lane Field Problem

**Symptom:** Scheduling or routing workflows fail at a Set node or
Switch node with a field reference error or undefined value.

**Root cause:** The `lane` field used in SCH-02 routing logic references
a data path that doesn't exist in the current execution context — either
the upstream node changed its output schema, or the field was renamed.

**Fix:**

1. Open the failing workflow at:
   **https://krosebrook.app.n8n.cloud → Workflows → [failing workflow name]**
2. Open the SCH-02 Switch node
3. Check each condition's field reference — look for `{{ $json.lane }}`
   or similar
4. Run the upstream node manually, inspect its output in the panel
5. Update the field reference to match the actual output path
6. Re-test with a manual execution before re-enabling the schedule

**Pattern going forward:** Use explicit field mapping nodes (Set nodes)
immediately after any webhook or HTTP Request node to normalize field
names before they're referenced downstream. This prevents schema drift
from breaking routing logic.

---

## Section 2: Silent Failure Diagnosis

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot read execution logs or query workflow state via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Executions** (left sidebar)
> Filter by workflow name to isolate failures. All diagnosis steps below
> require manual navigation in the n8n Cloud UI.

Workflows that don't run and produce no error are the hardest to debug.

**Diagnosis checklist:**

1. **Is the workflow active?**
   Navigate to **https://krosebrook.app.n8n.cloud → Workflows** → locate
   the workflow → confirm the Active toggle is ON (top-right when editing).
   Inactive workflows ignore triggers entirely.

2. **Is the trigger healthy?**
   - Webhook: visit the webhook URL directly — does n8n respond?
   - Schedule: **Executions tab** → filter by workflow → is there a
     last-run timestamp?
   - Polling: check if the connected service (Gmail, Slack, etc.) has
     authorized the n8n OAuth app recently

3. **Did the execution run but produce nothing visible?**
   Go to **https://krosebrook.app.n8n.cloud → Executions** → filter by
   workflow → look for executions with 0 items processed. This indicates
   the trigger fired but the filter/IF node blocked all items.

4. **Is the error swallowed downstream?**
   Check all Error Trigger nodes attached to this workflow. A downstream
   node might be catching and discarding errors silently.

5. **n8n Cloud: Check quota**
   **https://krosebrook.app.n8n.cloud → Settings → Usage and Plan**
   n8n Cloud plans have execution limits. A maxed quota silently stops
   new executions from starting.

---

## Section 3: Error Alerting Setup

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot create or modify workflows via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Workflows → New Workflow**
> Build the Error Handler workflow in the n8n Cloud UI using the steps below.

**Goal:** Every workflow failure surfaces as a notification within 5 minutes.

### The Error Trigger pattern

1. Navigate to **https://krosebrook.app.n8n.cloud → Workflows → New Workflow**
2. Add a node of type `Error Trigger` — this catches errors from all
   other workflows in the instance by default
3. Wire it to a notification node (Slack DM, email, or both)
4. Use this message template:

```
Workflow: {{ $json.workflow.name }}
Error: {{ $json.execution.error.message }}
Node: {{ $json.execution.error.node.name }}
Time: {{ $now.toLocaleString() }}
Link: {{ $json.execution.url }}
```

5. Name it `Error Handler` and activate it
6. Test by intentionally breaking a simple workflow and confirming
   the notification arrives

### Per-workflow error handling

For high-criticality workflows (client-facing, payment-related):
- Add a `Try / Catch` pattern: wrap the main logic in a sub-workflow,
  catch failures at the top level, send a specific alert with context
- Include the input data that caused the failure (sanitized of PII)

---

## Section 4: Credential Management

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot read, update, or audit credentials via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Settings → Credentials**
> Export the credential list from the UI; all rotation steps below
> require manual execution in the n8n Cloud UI.

### Credential audit (run quarterly)

1. Navigate to **https://krosebrook.app.n8n.cloud → Settings → Credentials**
2. For each credential: note the service, who owns it, last-used date,
   and rotation schedule
3. Flag any credential unused for 90+ days — disable it
4. Flag any credential with no rotation date — add one

### Rotation procedure

For each credential type:
- **OAuth (Google, Slack, HubSpot):** Re-authorize in n8n. The OAuth
  flow refreshes tokens automatically, but explicit re-auth is required
  annually for most providers.
- **API keys (Anthropic, Supabase, Airtable):** Generate a new key in
  the provider → update in n8n → verify with a manual workflow run →
  revoke the old key.
- **Bearer tokens (Base44):** See Section 1.
- **Webhook secrets:** Regenerate in the source system → update in n8n
  → update in all HTTP Request nodes that reference it.

**Never delete a credential before verifying no active workflows use it.**
n8n does not warn you when a credential deletion will break live workflows.

---

## Section 5: Workflow Versioning

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot trigger workflow exports via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Workflows → [workflow name]
> → ⋮ (three-dot menu) → Export → Download JSON**
> All versioning steps below require manual execution in the n8n Cloud UI.

n8n does not have native version history on free/starter plans.

**Manual versioning procedure (before any significant change):**

1. Navigate to **https://krosebrook.app.n8n.cloud → Workflows →
   [workflow name]**
2. Open ⋮ menu → Export → Download JSON
3. Save to `~/drive/n8n-backups/YYYY-MM-DD-workflow-name.json`
4. Make the change
5. Run a manual test execution
6. If the test fails: import the saved JSON to restore
   (**https://krosebrook.app.n8n.cloud → Workflows → Import from File**)

**Naming convention for exports:**
`YYYY-MM-DD_workflow-name_v[major].[minor].json`

Example: `2026-06-06_ff-intake-routing_v2.3.json`

**For n8n Cloud Pro and above:** Use the built-in version history panel
(**Workflows → [workflow name] → History** tab in editor).
Tag significant versions with a note before making breaking changes.

---

## Section 6: Worker Health

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot query worker status or stop stuck executions via MCP.
> Manual path: **https://krosebrook.app.n8n.cloud → Executions** (stuck
> executions appear with a spinner; click → Stop Execution)
> For usage/quota issues: **https://krosebrook.app.n8n.cloud → Settings →
> Usage and Plan**

### Indicators of an unhealthy worker

- Executions start but never complete (stuck in "running" state)
- Webhook responses become slow (>3s for simple flows)
- Schedule triggers fire late or miss windows
- Memory usage trending up over days without restarts

### n8n Cloud

If executions are stuck:
1. Navigate to **https://krosebrook.app.n8n.cloud → Executions**
2. Select stuck execution (shows spinner/running status) → Stop Execution
3. If multiple are stuck: contact n8n support at https://community.n8n.io —
   this often indicates a worker restart is needed on their end.

### Self-hosted n8n

```bash
# Check process health
pm2 status n8n       # if using pm2
docker stats n8n     # if using Docker

# Restart worker (gracefully drains active executions first)
pm2 reload n8n
# or
docker restart n8n

# Check logs for memory or crash patterns
pm2 logs n8n --lines 200
docker logs n8n --tail 200
```

**Recommended:** set a weekly restart schedule during low-traffic hours
to prevent memory accumulation. n8n is stateless between restarts for
all execution data (stored in DB), so restarts are safe.

---

## Self-Verification Checklist

- [ ] **n8n MCP connection confirmed active before attempting programmatic ops.**
  FAIL: MCP attempted while status is CONNECTION_ISSUE — check Claude.ai
  Settings → Integrations; use manual URL https://krosebrook.app.n8n.cloud
  as fallback until restored.

- [ ] **Base44 Bearer token is valid and has a rotation reminder set.**
  FAIL: A workflow using `Base44 Bearer` credential returns 401 → rotate
  immediately per Section 1.

- [ ] **SCH-02 lane field references match actual upstream output schema.**
  FAIL: Switch node condition references a field not present in upstream
  node output → remap per Section 1.

- [ ] **Error Trigger workflow is active and tested.**
  FAIL: No `Error Handler` workflow exists or it is inactive → build per
  Section 3 before any production workflow goes live.

- [ ] **Credential audit has been run in the last 90 days.**
  FAIL: Last audit >90 days ago or no audit date recorded → run per
  Section 4, Credential audit procedure.

- [ ] **All high-criticality workflows have a pre-change export.**
  FAIL: No timestamped JSON backup exists for a workflow before modifying
  it → export first per Section 5.

- [ ] **Worker health has been checked this month.**
  FAIL: Stuck executions present in Executions tab without resolution →
  stop them manually per Section 6.

---

## CLAIMS
- [GENERATED] Base44 uses short-lived Bearer tokens incompatible with n8n's
  static credential model — rotation must be manual until Base44 provides
  OAuth. Verified through operational behavior of the FlashFusion platform.
- [GENERATED] Schema drift between workflow nodes is the most common cause
  of silent routing failures in n8n; explicit field normalization nodes
  prevent this. Observed across SCH-02 lane field incidents.
- [GENERATED] n8n MCP CONNECTION_ISSUE does not affect the underlying n8n
  Cloud workflows themselves — only Claude's ability to interact with them
  programmatically. Workflows continue to run on their own schedules.

## COUNTEREXAMPLE
- The Error Trigger approach catches most failures but not execution timeout
  failures, which produce no error event in n8n's current architecture —
  these require external health checks (e.g., a cron job pinging a
  completion webhook).

## CONTRADICTIONS
- "Test before every change" conflicts with n8n Cloud's execution quota
  limits on lower plans; on quota-constrained plans, prioritize testing
  only the changed path rather than the full workflow.
- ! n8n MCP CONNECTION_ISSUE is declared in this skill, but Claude's
  connectors list shows n8n as a connected MCP server. These two states
  are temporarily out of sync. When MCP reconnects, the DEPENDENCY_DECLARATION
  and FAIL_IF blocks remain correct behavior — they are
  no-ops when the connection is healthy (FAIL_IF condition evaluates
  false; CONNECTION CHECKs pass through normally).

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **Root cause of n8n MCP CONNECTION_ISSUE unknown.** Could be expired
  auth token, MCP server config drift, or n8n cloud outage. Check
  https://status.n8n.io and re-authenticate in Claude.ai Settings →
  Integrations if token expiry is suspected.
- **No automated detection of MCP reconnection.** Skill cannot self-heal
  when n8n MCP comes back online — user must validate manually and remove
  the CONNECTION_ISSUE annotation in the next version bump.
- **Webhook URLs and auth headers for Chain 1 and other workflows are
  not embedded here.** If n8n.cloud UI is also unavailable (not just MCP),
  there is no offline-accessible copy of webhook endpoints.
- **n8n quota behavior on CONNECTION_ISSUE.** Unclear whether n8n Cloud
  continues counting executions against quota when MCP is the connection
  method vs. direct webhook triggers. Likely yes (quota is per execution,
  not per access method).
