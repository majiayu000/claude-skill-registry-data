---
name: ha:setup-failure-debug
description: Debug Home Assistant integration setup failures — ConfigEntryNotReady retry loops, ConfigEntryAuthFailed/reauth loops, unique-ID collisions (already_configured, duplicate devices after a host change), and "Setup failed for <domain>" logs. Use when an integration won't finish setup, keeps retrying, keeps re-prompting for reauth, or aborts as already configured.
effort: medium
---

# Setup-Failure Debugging

> Orientation: this is the structured-diagnosis analogue of debugging a database
> constraint violation — parse the exact failure signature, check the gate before the code,
> and trace every path that can trip it. Here the "constraint" is a config-flow/setup gate.

Systematic approach to diagnosing why an integration fails to set up. Load when you see a
`ConfigEntryNotReady` retry loop, a `ConfigEntryAuthFailed`/reauth loop, an
`already_configured` abort, duplicate devices after a host/IP change, or a
`Setup failed for <domain>` log line.

## Iron Laws

1. **READ THE FAILURE SIGNATURE** — The exception type and message tell you exactly which
   gate failed. `ConfigEntryNotReady` = transient setup failure (HA will retry);
   `ConfigEntryAuthFailed` = auth (triggers reauth); `AbortFlow("already_configured")` =
   unique-ID collision in the flow; `Setup failed for <domain>: Unable to import` = manifest
   /import problem. Parse it first, and confirm the raised type matches the cause (P3). "For
   temporary errors, use `ConfigEntryNotReady` exception to let HA automatically retry." —
   balloob, https://github.com/home-assistant/core/pull/174850#discussion_r3478681149
2. **CHECK THE GATE BEFORE THE CODE** — Verify *where* validation happens. The config flow
   must validate the connection before creating the entry (`test-before-configure`); setup
   raises `ConfigEntryNotReady`/`ConfigEntryAuthFailed` on failure (`test-before-setup`).
   Client creation + first refresh live in `__init__.py`/coordinator, not the flow (P16).
   "move the client initialization to `__init__.py`... When we can't fetch data we raise
   ConfigEntryNotReady" — joostlek,
   https://github.com/home-assistant/core/pull/169500#discussion_r3570262283
3. **TRACE ALL SETUP + UNIQUE-ID PATHS** — Find every `async_set_unique_id`,
   `_abort_if_unique_id_configured`, `async_create_entry`, `async_config_entry_first_refresh`,
   and `raise ConfigEntryNotReady/AuthFailed`. The bug is often in a path you didn't consider
   (reauth, reconfigure, discovery). Unique IDs must be stable, immutable device identifiers
   (P7). "Host and port do not qualify for a unique identifier, as they can change." —
   frenck, https://github.com/home-assistant/core/pull/148104#discussion_r2186877132
4. **TRANSIENT UNTIL PROVEN PERMANENT** — A `ConfigEntryNotReady` retry loop is *designed* to
   retry transient errors. If it never succeeds, the failure is permanent (bad auth, wrong
   host, unsupported firmware) but misclassified — assume transient-network until you prove a
   permanent cause, then raise the correct permanent exception instead (P16). "The first
   refresh method needs to be called within the `async_setup_entry`" — MartinHjelmare,
   https://github.com/home-assistant/core/pull/166175#discussion_r3032611222

## Step-by-Step Debugging

### Step 1: Parse the Failure

Extract from the log / exception:

- **Exception type** — `ConfigEntryNotReady`, `ConfigEntryAuthFailed`, `ConfigEntryError`,
  `AbortFlow` (with reason, e.g. `already_configured`), or an import/`ModuleNotFoundError`
- **Domain** — which integration (`Setup failed for <domain>`)
- **Message / translation key** — the human-readable cause (P3)
- **Behavior** — one-shot failure, an *endless retry* loop, or a *reauth* loop
- **Trigger** — first setup, a reload, an HA restart, or after the user changed the host/IP

### Step 2: Find the Gate

Use Grep to locate where the failing gate is enforced:

- Config flow gate (`test-before-configure`): `async_set_unique_id`,
  `_abort_if_unique_id_configured`, and the connection test in `config_flow.py`
- Setup gate (`test-before-setup`): `raise ConfigEntryNotReady`, `raise ConfigEntryAuthFailed`,
  `async_config_entry_first_refresh` in `__init__.py`/`coordinator.py`

Verify (P16): does the flow validate the connection *before* `async_create_entry`? Is the
client created and first-refreshed in `__init__.py`/the coordinator (not the flow)?

### Step 3: Find the Unique-ID Source

Use Grep to find where the unique ID comes from (`async_set_unique_id(...)`,
`_attr_unique_id`, `entry.unique_id`). Confirm it is a stable, immutable identifier — serial,
`format_mac()`, burned-in ID — and **not** host/port/IP/hostname/name/URL/user-config (P7). A
unique ID derived from a host or IP is the root cause of both `already_configured` aborts and
duplicate devices after a host change.

### Step 4: Trace Setup Paths

Find ALL paths that create an entry, set a unique ID, or run first refresh:

Use Grep to find `async_step_user`, `async_step_reauth`, `async_step_reconfigure`,
`async_step_zeroconf`/`dhcp`/`ssdp` (discovery), `async_setup_entry`,
`async_config_entry_first_refresh`, and every `raise ConfigEntryNotReady`/`AuthFailed` under
the integration directory. Reauth and discovery paths are the ones most often missed.

### Step 5: Inspect the Registries (READ-ONLY)

The stored state that a collision or duplicate is measured against lives in `config/.storage/`.
Inspect it to see what HA already recorded — **never hand-edit these files** (that corrupts the
instance; fix the code or use the UI / a migration instead):

- `config/.storage/core.config_entries` — existing entries, their `unique_id`, `domain`,
  `data` (host/host-changed), and `state`
- `config/.storage/core.device_registry` — devices and their `identifiers`/`connections`
  (duplicates show as two devices with different identifiers for the same hardware)
- `config/.storage/core.entity_registry` — entities and their `unique_id`

```bash
python -m json.tool config/.storage/core.config_entries | grep -A3 '"domain": "<domain>"'
```

### Step 6: Identify the Cause

| Symptom | Likely Cause | Fix Pattern |
|---------|--------------|-------------|
| Setup retries forever, never ready | A permanent error (bad auth, 404, unsupported) raised as `ConfigEntryNotReady` | Raise `ConfigEntryAuthFailed` for auth, `ConfigEntryError` for permanent failures (P3) |
| Reauth loop — keeps re-prompting | `ConfigEntryAuthFailed` raised on transient errors, or the reauth step doesn't update the existing entry | Only raise `ConfigEntryAuthFailed` on 401/403; reauth must update the entry, not create a new one |
| `already_configured` abort on a legitimately new device | Unique-ID collision — the ID isn't unique per device, or a host/IP-based ID matches an existing entry | Use a stable immutable unique ID (P7); add a reconfigure step to update host |
| Duplicate devices after a host/IP change | Unique ID derived from host/IP (P7 violation) — the new host reads as a new device | Migrate unique ID to serial/MAC (`async_migrate_entry`, PR3); add reconfigure |
| `Setup failed for <domain>: Unable to import` | Missing/incorrect manifest `requirements`, or a blocking import at module load | Fix manifest `requirements`; move heavy imports (P4) |
| Setup logs a blocking-call warning | Blocking I/O during setup (P4) | Move the call to the executor / async library (see `blocking-io-check`) |

### Step 7: Apply Fix

See `${CLAUDE_SKILL_DIR}/references/setup-failure-patterns.md` for detailed fix patterns per
failure type.

## Quick Fixes by Failure Type

**`ConfigEntryNotReady`** → transient only; HA auto-retries with exponential backoff. Raise it
for temporary connection failures — never for auth or permanently-bad config.

**`ConfigEntryAuthFailed`** → triggers the reauth flow. Raise only for authentication failures
(expired/invalid credentials, 401/403). The reauth step must **update** the existing entry.

**`AbortFlow("already_configured")`** → the unique ID already exists. Correct when the device
is genuinely already added; a bug when the ID isn't a stable per-device identifier (P7) or when
a host change should have been a reconfigure.

## References

- `${CLAUDE_SKILL_DIR}/references/setup-failure-patterns.md` — detailed patterns for each
  setup-failure type: transient-vs-permanent classification, reauth that updates the entry,
  unique-ID stability and migration, discovery collisions, and manifest/import failures
