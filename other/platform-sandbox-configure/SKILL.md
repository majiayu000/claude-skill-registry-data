---
name: platform-sandbox-configure
description: "MUST USE this skill for ANY sandbox request — including simply getting a sandbox's details, status, license type, or pending-activation state by name or ID. TRIGGER when the user: types \"sandbox -help\"/\"sandbox help\"; mentions a sandbox ID (07E prefix); asks to list or show sandboxes; asks for the details, status, license type, or config of a sandbox by name or ID; activates or discards a completed refresh; deletes a sandbox; verifies activation or deletion; creates or refreshes a sandbox. DO NOT TRIGGER when: the user wants to clone a sandbox."
metadata:
  version: "1.1"
  domains: ["Platform"]
  minApiVersion: "66.0"
  relatedSkills:
    - "automation-sandbox-post-copy-config-generate"
    - "automation-sandbox-post-copy-configure"
  accessCheck: "UserPermissions.ManageSandboxes"
  cliTools:
    - tool: ["sf"]
      semver: ">=2.0.0"
---

# Sandbox Lifecycle Management

Manage Salesforce sandbox environments through Connect REST API — list inventory, activate or discard completed refreshes, create and refresh sandboxes, and permanently delete sandboxes.

## When This Skill Owns the Task

Use `platform-sandbox-configure` when the work involves:
- Listing or retrieving all sandboxes (GET /sandbox/reports)
- Getting details or status of a specific sandbox by name or by ID (07E prefix)
- Checking license usage and remaining capacity by license type (GET /sandbox/licenses)
- Activating a sandbox after a refresh completes (applying the refresh)
- Discarding a completed refresh (keeping existing sandbox data unchanged)
- Permanently deleting a sandbox to free up licenses
- Verifying activation or deletion completed
- Creating a new sandbox (Developer, Developer Pro, Partial Copy, or Full)
- Refreshing an existing sandbox with latest production data

Delegate elsewhere when the user is:
- Cloning a sandbox → Tooling API (`SandboxInfo` sObject)
- Generating a post-copy automation JSON config from an SOP → `automation-sandbox-post-copy-config-generate`
- Applying/running a post-copy automation JSON config against a sandbox → `automation-sandbox-post-copy-configure`

---

## Help (Interactive Menu)

When the user types `sandbox -help` or `sandbox help`, respond with ONLY a text message showing the numbered operation list below. **Do NOT call any API or tool — just display this menu and wait for the user to reply with a number.**

The agent MUST respond with this exact markdown (not in a code block — render it directly as a bullet list):

**Sandbox Lifecycle Management**

**1. Inventory & Details**
- a. List all sandboxes — Names, types, statuses, IDs
- b. Get details (by name) — Status, license, config
- c. Get details (by ID) — Provide a 07E ID directly
- d. Check license usage — Available vs. used counts by license type

**2. Create & Refresh**
- a. Create a new sandbox — Dev, Dev Pro, Partial, Full
- b. Refresh a sandbox — Latest production data

**3. Activate, Discard & Delete**
- a. Activate a sandbox — Apply a completed refresh
- b. Discard a refresh — Reject, keep existing data
- c. Delete a sandbox — Permanent removal

**4. Verify & Monitor**
- a. Verify activation status — Check if activate completed
- b. Verify deletion status — Check if delete completed

**5. Post-Copy Automation**
- a. Create Post Copy Automation JSON Configs — Generate a config from an SOP
- b. Run Post Copy Automation — Apply a config JSON to a sandbox

Reply with a code (e.g. "3a") or describe what you need.

**After the user replies, ask for the required input:**

| Selection | Follow-up question |
|---|---|
| 1a | No input needed — proceed immediately |
| 1b | "What's the sandbox name?" |
| 1c | "What's the sandbox ID? (starts with 07E)" |
| 1d | No input needed — proceed immediately |
| 2a | First call `GET /sandbox/licenses` (Section 9) and show available/used counts; then ask for name + license type (Developer, Developer_Pro, Partial_Copy, Full) |
| 2b | First call `GET /sandbox/reports` (Section 1) and list refresh-eligible sandboxes (`isPendingActivation: false`); then ask which to refresh |
| 3a | "Which sandbox? Provide a name or 07E ID." |
| 3b | "Which sandbox? Provide a name or 07E ID." |
| 3c | "Which sandbox? Provide a name or 07E ID." |
| 4a | "Which sandbox did you activate? Provide a name or 07E ID." |
| 4b | "Which sandbox did you delete? Provide a name or 07E ID." |
| 5a | "Delegating to the post-copy config generator — please share the SOP (file, text, or screenshot)." |
| 5b | "Delegating to the post-copy config runner — please share the config JSON file and the target sandbox." |

Execute the corresponding operation below. **Exception:** 5a/5b delegate — 5a → `automation-sandbox-post-copy-config-generate`; 5b → `automation-sandbox-post-copy-configure`. This skill does not implement post-copy automation; do not generate or apply a config directly.

---

## API Base

**CRITICAL:** For sandbox operations in this skill, use the Connect REST API. Two discovery paths exist:
- **By name:** Call `GET /sandbox/reports` to list all sandboxes and find the matching one by `sandboxName`.
- **By ID (07E prefix):** Call `GET /sandbox/sandboxes/{sandboxId}` directly — do NOT call `/sandbox/reports`.

Both paths return sandbox records with `sandboxId` (prefix `07E`) which is required for all lifecycle mutation operations.

```bash
sf api request rest "/services/data/v66.0/sandbox/reports" --method GET
```

See `references/api-response-shapes.md` for the full response shape.

**IMPORTANT:** Do NOT use Tooling API (`SandboxInfo`/`SandboxProcess`) for discovery — mutation endpoints require the Connect REST API's `sandboxId` (07E), NOT `SandboxInfo.Id` (0GQ) or `SandboxProcess.Id` (0GR).

**NEVER use SOQL / `run_soql_query` / `sf data query` for lifecycle reads (status, inventory, details, license, pending-activation).** This data lives ONLY in the Connect REST API — no SObject returns it. (`sf data query --use-tooling-api` on `SandboxInfo` is still valid for Create/Refresh mutations, not a lifecycle read.)

**Report API results exactly as they come back — never invent an error or a cause.** `count: 0` is a *successful* result (sandbox absent) — record `not_found`, don't reinterpret as a failure or retry via SOQL. If the API errors, capture the error body verbatim — do NOT speculate why (e.g. "must be a scratch org"); this endpoint doesn't report org edition/type, so any such guess is a fabrication.

Required permission: `ManageSandboxes`

## Irreversible Actions — Always Confirm First

| Action | Why irreversible |
|---|---|
| Create | Consumes a license of the selected type |
| Activate | Overwrites sandbox with refreshed data |
| Discard | Refresh data is lost |
| Delete | Sandbox permanently removed |
| Refresh with `AutoActivate=true` | Auto-applies on completion — same effect as Activate |

---

## Operations

### 1. List Sandbox Inventory

**Endpoint:** `GET /services/data/v66.0/sandbox/reports`

Returns a list of all sandboxes with their IDs, names, statuses, and license types.

```bash
sf api request rest "/services/data/v66.0/sandbox/reports" --method GET
```

See `references/api-response-shapes.md` for the full response shape.

**Use when:** User asks "show me all sandboxes", "how many sandboxes do I have", "what's the status of my sandboxes"

**Key response fields:**
- `sandbox.sandboxId` (07E prefix) — Required for all mutation operations
- `sandbox.sandboxName` — The sandbox name (top-level field)
- `sandbox.license` — Developer, Developer Pro, Partial Copy, Full
- `sandbox.isPendingActivation` — true if refresh is pending activation
- `sandbox.canActivate` / `canDelete` / `canDiscard` — Permission flags

---

### 2. Get Sandbox Details

**Endpoint:** `GET /services/data/v66.0/sandbox/sandboxes/{sandboxId}`

Returns detailed info for a specific sandbox.

**Use when:** User asks about a specific sandbox's status, configuration, or metadata.

**Key response fields:**
- `status` — Active, Pending Activation, Activating, Completed, etc.
- `isPendingActivation` — true if a refresh completed and awaits user decision
- `sandboxType` — Developer, DeveloperPro, PartialCopy, Full
- `sourceId` — ID of the source org

---

### 3. Activate Sandbox (Apply Refresh)

**Endpoint:** `PATCH /services/data/v66.0/sandbox/activate/{sandboxId}`

**CRITICAL DOMAIN RULE:** This operation ONLY applies to sandboxes with a completed refresh in "Pending Activation" state. It applies the refreshed data to the sandbox. It does NOT "bring an inactive sandbox online" or "start" a sandbox.

**Pre-conditions:**
- Sandbox must be in `Pending Activation` status
- A refresh must have completed successfully
- User must have `ManageSandboxes` permission

**Before calling PATCH /activate:**
- [ ] Confirmed sandbox is in `Pending Activation` status via GET `/sandbox/sandboxes/{id}` (`isPendingActivation: true`)
- [ ] Confirmed a refresh has completed successfully
- [ ] Received explicit user confirmation — this overwrites the sandbox with the refreshed data and cannot be undone

**Use when:** User says "activate it", "apply the refresh", "use the latest data"

**After activation:** The sandbox runs with the newly refreshed production data.

---

### 4. Verify Activation

**Endpoint:** `GET /services/data/v66.0/sandbox/sandboxes/{sandboxId}`

Poll this endpoint after activation to confirm status changed to `Active`. This is a verification step, not a standalone user action.

**Use when:** Agent needs to confirm activation completed (called automatically after activate).

---

### 5. Discard Sandbox (Reject Refresh)

**Endpoint:** `DELETE /services/data/v66.0/sandbox/discardsandbox/{sandboxId}`

**CRITICAL DOMAIN RULE:** This operation ONLY applies to sandboxes with a completed refresh in "Pending Activation" state. It rejects the refresh — the existing sandbox continues running with its current data unchanged. It does NOT:
- Free up licenses
- Soft-delete or hide the sandbox
- Reset the sandbox to match production

**Pre-conditions:**
- Sandbox must be in `Pending Activation` status
- A refresh must have completed

**Before calling DELETE /discardsandbox:**
- [ ] Confirmed sandbox is in `Pending Activation` status via GET `/sandbox/sandboxes/{id}` (`isPendingActivation: true`)
- [ ] Confirmed this is a discard (reject refresh), NOT a delete (permanent removal)
- [ ] Received explicit user confirmation — the refresh data will be permanently lost and cannot be undone

**Use when:** User says "discard the refresh", "keep existing data", "don't apply the refresh", "reject the refresh"

**WARNING:** Discard is not reversible. The user will need to trigger a new refresh if they want fresh production data later.

---

### 6. Delete Sandbox (Permanent)

**Endpoint:** `DELETE /services/data/v66.0/sandbox/deletesandbox/{sandboxId}`

Permanently removes a sandbox and frees the license.

**Pre-conditions:**
- Sandbox must exist
- User must have `ManageSandboxes` permission

**Before calling DELETE /deletesandbox:**
- [ ] Surfaced sandbox details (name, license, status) with user and received explicit delete approval

**Use when:** User says "delete this sandbox", "remove it permanently", "free up the license"

**WARNING:** This is irreversible. Always confirm with the user before executing. Surface the sandbox name, license, and status as a safety check.

**If asked to restore a deleted sandbox:** No recovery path is documented today — escalate to Support rather than guessing at one.

---

### 7. Create a New Sandbox

Creates a new sandbox from scratch. Two approaches are supported — pick based on the user's preference; default to Approach A unless the user asks for a definition file or a repeatable DX blueprint.

**Pre-conditions:**
- Available license of the requested type must exist in the org
- Sandbox name must be unique and not already in use
- User must have `ManageSandboxes` permission

**Before creating — always confirm first:**
- [ ] Collected Name/License; asked about that license's optional inputs (`references/definition-file-approach.md`)
- [ ] Shown this confirmation summary — common fields plus the license's own fields:

  > **Creating a new sandbox — please confirm:**
  > - **Name:** `<SandboxName>`
  > - **Description:** `<Description or "(none)">`
  > - **Create From:** Production
  > - **License:** `<Developer | Developer Pro | Partial Copy | Full>`
  > - *(plus this license's fields — see `references/definition-file-approach.md`)*
  >
  > Feel free to change any of these before I proceed.

- [ ] Received explicit confirmation — this consumes a license of the selected type

#### Approach A — Tooling API record (direct)

**API:** Tooling API — `SandboxInfo` sObject

**Required inputs:**
- `SandboxName` — Name for the new sandbox (alphanumeric, max 10 chars)
- `LicenseType` — One of: `Developer`, `Developer_Pro`, `Partial_Copy`, `Full`

**Optional inputs:**
- `Description` — sandbox purpose
- `Features` — storage upgrade: `Developer`→400 MB, `Developer_Pro`→2 GB (irreversible); not for `Partial_Copy`/`Full`
- `ApexClassId` — Apex class implementing `SandboxPostCopy` (runs post-creation)
- `ActivationUserGroupId` — Access group (default: All Active Users)
- `TemplateId` / `HistoryDays` / `CopyChatter` / `CopyArchivedActivities` — `Partial_Copy`/`Full`-only; per-license table in `references/definition-file-approach.md`

```bash
# Create a Developer sandbox
sf data create record --sobject SandboxInfo --use-tooling-api --values "SandboxName='mybox' LicenseType='Developer'"
```

#### Approach B — Sandbox definition file (Salesforce CLI)

DX-native path: write a JSON definition file, then `sf org create sandbox --definition-file <file> --alias <name> --target-org <org>`. Prefer for a checked-in, repeatable config or name-based Apex/group references. See `references/definition-file-approach.md` for the JSON example, command, and field table.

**After creation:** A `SandboxProcess` record is created with Status = `Processing`. The sandbox copy begins immediately.

**Wrong type created:** Delete and recreate with the correct type.

**Renaming:** Not a standalone action — only takes effect via a Refresh's `SandboxName` input.

---

### 8. Refresh an Existing Sandbox

Refreshes a sandbox with the latest production data. Two approaches are supported — pick based on the user's preference; default to Approach A unless the user asks for a definition file.

#### Approach A — Tooling API record (direct)

**API:** Tooling API — `SandboxInfo` sObject (PATCH)

Refreshes by updating the existing `SandboxInfo` record.

**Required inputs:**
- Sandbox name — to look up the `SandboxInfo` record ID (0GQ prefix)

**Optional inputs:**
- `SandboxName` — New name for the refreshed sandbox (if user wants to rename it; alphanumeric, max 10 chars)
- `Description` — New or updated description for the sandbox
- `AutoActivate` — `true` to auto-activate when refresh completes (default: false)
- `Features` — storage upgrade: `Developer`→400 MB, `Developer_Pro`→2 GB (irreversible); not for `Partial_Copy`/`Full`
- `ActivationUserGroupId` — Access group (default: All Active Users)
- `TemplateId` / `HistoryDays` / `CopyChatter` — `Partial_Copy`/`Full`-only; per-license table in `references/definition-file-approach.md`

**Before triggering refresh — always confirm first:**
- [ ] Collected the sandbox name; asked about its license's optional inputs (`references/definition-file-approach.md`)
- [ ] Shown this confirmation summary:

  > **Refreshing sandbox `<name>` — please confirm:**
  > - **Rename to:** `<SandboxName or "(no change)">`
  > - **Description:** `<Description or "(no change)">`
  > - **Auto-Activate:** `<Yes | No (default)>`
  > - **Sandbox Access:** `<ActivationUserGroupId or "All Active Users">`
  > - *(plus this license's fields — see `references/definition-file-approach.md`)*
  >
  > Feel free to change any of these before I proceed.

- [ ] Received explicit confirmation — refresh overwrites the sandbox with production data; Auto-Activate=Yes applies automatically (equivalent to Activate)

**Steps:**

```bash
# 1. Look up SandboxInfo record Id by name
sf data query --query "SELECT Id, SandboxName, LicenseType, Description FROM SandboxInfo WHERE SandboxName = '<name>'" --use-tooling-api --json

# 2. PATCH to trigger refresh; include SandboxName/Description only if the user changed them
# Description is free text — escape any embedded single quotes (' -> \') before interpolating
sf data update record --sobject SandboxInfo --use-tooling-api --record-id <0GQ-id> --values "AutoActivate=true SandboxName='<newName>' Description='<description>'"
```

#### Approach B — Sandbox definition file (Salesforce CLI)

Refresh from the same JSON definition-file blueprint used for create, using `sf org refresh sandbox --name <name> --definition-file <file> --target-org <org>`. See `references/definition-file-approach.md` for the JSON example, command, and field table.

**Pre-conditions:**
- Sandbox must exist and be in a refreshable state
- Refresh interval must have elapsed (Developer = 1 day, Dev Pro = 1 day, Partial = 5 days, Full = 29 days)
- User must have `ManageSandboxes` permission

**After refresh:** A new `SandboxProcess` record is created with Status = `Processing`. If `AutoActivate=true`, the sandbox activates automatically when done. Otherwise it enters `Pending Activation` state.

**Refresh interval not met:** State the last-refreshed date and eligible date. For a fresher copy sooner, a clone (delegated) works if a spare license exists.

---

### 9. Check License Usage

**Endpoint:** `GET /services/data/v66.0/sandbox/licenses`

Returns license capacity, usage, and remaining counts per license type — no sandbox name or ID needed.

```bash
sf api request rest "/services/data/v66.0/sandbox/licenses" --method GET
```

See `references/api-response-shapes.md` for the full response shape.

**Use when:** User asks "how many sandbox licenses do I have left", "what's my license usage", "can I create another Full sandbox", or before creating/refreshing a sandbox to confirm capacity exists for that `licenseType`.

**Key response fields:**
- `licenseType` — `DEVELOPER`, `DEVELOPER_PRO`, `PARTIAL`, `FULL`
- `limit` — Total licenses of this type
- `used` — Currently allocated
- `available` — Remaining (i.e. `limit - used`)

**Create/Refresh blocked by a license limit:** offer to pick an available type, free one up by deleting a stale sandbox, ask the admin for a license increase, or — if it's an expired Courtesy Full Copy — purchase/convert it.

---

## Decision Guide for Agents

Resolve `sandboxId` first: by name, call `GET /sandbox/reports` and match `sandboxName`; by ID (07E prefix), call `GET /sandbox/sandboxes/{sandboxId}` directly — don't call `/sandbox/reports`.

| User says... | Operation | Key check |
|---|---|---|
| "Show all my sandboxes" | GET /sandbox/reports | — |
| "What's the status of X?" | GET /sandbox/reports (by name) or GET /sandbox/sandboxes/{id} (by ID) | — |
| "Activate sandbox X" | 1. Resolve `sandboxId`<br>2. PATCH /sandbox/activate/{sandboxId} | Must be isPendingActivation: true; confirm with user first |
| "Discard the refresh on X" | 1. Resolve `sandboxId`<br>2. DELETE /sandbox/discardsandbox/{sandboxId} | Must be isPendingActivation: true; confirm with user first |
| "Delete sandbox X" | 1. Resolve `sandboxId`<br>2. DELETE /sandbox/deletesandbox/{sandboxId} | Confirm with user first |

---

## Common Mistakes to Avoid

| Mistake | Correct understanding |
|---|---|
| Using activate to "start" any sandbox | Activate ONLY applies completed refreshes |
| Using discard to "hide" or "soft-delete" | Discard ONLY rejects a pending refresh |
| Activating without checking status first | Always verify isPendingActivation = true |
| Skipping confirmation on Create, Activate, Discard, Delete, or Refresh with `AutoActivate=true` | See Irreversible Actions above — always confirm first |
| Offering `AutoActivate` during Create | Refresh-only field |
| Offering `ApexClassId` during Refresh | Create-only field |
