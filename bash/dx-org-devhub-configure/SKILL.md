---
name: dx-org-devhub-configure
description: "Enable Dev Hub on a Salesforce org, view its status and scratch org allocation, or read its current DevHubSettings preferences, using the Salesforce CLI (sf). Use when someone wants to turn on or enable Dev Hub, set up an org for scratch orgs or 2GP/unlocked packages, check whether Dev Hub is already enabled, see scratch org allocation (Active/Daily limits, remaining, and a pre-flight warning near the limit), see which Dev Hub preferences (packaging, org shape export, scratch org snapshots) are on or off, configure those preferences, list active scratch orgs, or list authenticated orgs when none is specified. Enabling deploys enableScratchOrgManagementPref, is irreversible, needs a System Administrator (ModifyAllData or ModifyMetadata), and does not work in sandboxes. DO NOT TRIGGER for creating or deleting individual scratch orgs."
allowed-tools: Read, Bash(bash), Bash(sf api request rest), Bash(sf data query), Bash(sf org list), Bash(sf project deploy), Bash(sf config get), Bash(sf org display), Bash(sf org open), Bash(jq)
metadata:
  version: "1.1"
  domains: ["Developer Experience"]
  # DevHubSettings metadata + the Tooling API DevHubSettings endpoint require
  # DevHubSettings base fields need API 47.0+, but enableShapeExportPref needs
  # 55.0+ and enableScratchOrgSnapshotPref needs 61.0+, so the script reads and
  # deploys at 62.0 (see scripts/devhub.sh SETTINGS_API_VERSION).
  minApiVersion: "62.0"
  # Enabling needs ModifyAllData OR ModifyMetadata (either suffices). accessCheck
  # is a flat array with no OR operator, so declaring both would read as AND and
  # could falsely gate an admin holding only one. Declare the canonical
  # System-Administrator perm; the OR alternative stays documented in the
  # description and body.
  accessCheck: "UserPermissions.ModifyAllData"
  cliTools:
    - tool: ["jq"]
      semver: ">=1.6.0"
    - tool: ["sf"]
      semver: ">=2.0.0"
---

# Enable Dev Hub & View Scratch Org Allocation

Enable **Dev Hub** on a Salesforce org, verify whether it is already on, and see
the org's **scratch org allocation** (Active and Daily limits, how many
remain, and a pre-flight warning when close to the limit) — for the default
org or a named org. The skill can also read the org's current **DevHubSettings
preferences**, configure Dev Hub sub-preferences (packaging, org shape export,
scratch org snapshots), list the active scratch orgs created from a Dev Hub,
and list which orgs are authenticated when none is specified.

Dev Hub is the org feature that lets you **create and manage scratch orgs** and
**second-generation (2GP) / unlocked packages**.

## When to use

Trigger on requests like:

- "Enable Dev Hub" / "Turn on Dev Hub" / "Set up this org for scratch orgs."
- "Is Dev Hub enabled on my org?" / "Check if Dev Hub is on."
- "How many scratch orgs can I create?" / "What's my scratch org allocation /
  limit?" / "How many scratch orgs do I have left?"
- "Turn on packaging / 2GP / unlocked packages" / "Enable org shape export" /
  "Enable scratch org snapshots" (Dev Hub sub-preferences).
- "Which Dev Hub preferences are turned on?" / "Show my current DevHubSettings."
- "List the scratch orgs on my Dev Hub."
- "What orgs do I have authenticated?" / "I didn't pass an org — what's available?"

## When NOT to use

Do **not** trigger this skill for:

- **Creating or deleting an individual scratch org** — that is
  `sf org create scratch` / `sf org delete scratch`, a different workflow. This
  skill enables the *Dev Hub feature* and reports *allocation*; it does not
  create scratch orgs.

## How Dev Hub enablement is determined

The standard object **`ScratchOrgInfo`** is provisioned and becomes queryable
**only when Dev Hub is enabled**. So a successful `SELECT COUNT() FROM
ScratchOrgInfo` means Dev Hub is **ON**; an `INVALID_TYPE` error means it is
**OFF**. This is the reliable signal.

> Do **not** infer enablement from `sf org list limits` alone: it reports
> `ActiveScratchOrgs` / `DailyScratchOrgs` rows even on orgs where Dev Hub is
> **off**, so limits show allocation but not enablement.

## How enabling works (important)

- The Dev Hub master switch is the **deployable** Metadata API field
  **`DevHubSettings.enableScratchOrgManagementPref`**. There is **no**
  `enableDevHub` field and **no** dedicated `sf` command to turn it on —
  deploying this setting is exactly what the Setup toggle does.
- **Enabling is irreversible** — once on, Dev Hub cannot be turned off.
- **Requires** a user with **ModifyAllData** or **ModifyMetadata** (a **System
  Administrator** has these). A user without them gets `INSUFFICIENT_ACCESS`.
- **Cannot** be enabled in a **sandbox**, or in an org that has a **registered
  namespace**. The script checks the org's edition/sandbox facts before an
  `--enable --apply` and refuses (no deploy attempted) if the target is a
  sandbox; there's no reliable CLI signal for a registered namespace, so that
  stays a documented caveat rather than an enforced check.
- Available in **Developer, Enterprise, Performance, Unlimited**, and **trial**
  editions — `status` and `--allocation` show the org's edition when known.

## Steps

1. **CRITICAL:** Run the bundled helper script, which handles Dev Hub detection,
   the enablement deploy (with a safe dry-run default), allocation math, and
   structured output, and works on macOS and Linux. Always invoke it by
   **absolute path** from the skill directory — never `./scripts/`, which
   resolves against the user's current directory and will either run the wrong
   script or fail. The script self-checks this: if `$0` is not absolute it exits
   with a usage error, so pass the full path to `<skill_dir>` (the directory
   containing this SKILL.md).

   ```bash
   bash "<skill_dir>/scripts/devhub.sh" <alias-or-username>            # status: on? + edition + allocation
   bash "<skill_dir>/scripts/devhub.sh"                               # default org (target-org)
   bash "<skill_dir>/scripts/devhub.sh" <org> --allocation           # allocation + pre-flight warnings
   bash "<skill_dir>/scripts/devhub.sh" <org> --show-settings        # current DevHubSettings preferences
   bash "<skill_dir>/scripts/devhub.sh" --list-orgs                  # authenticated orgs (no org needed)
   bash "<skill_dir>/scripts/devhub.sh" <org> --enable               # validate enabling (dry run)
   bash "<skill_dir>/scripts/devhub.sh" <org> --enable --apply       # actually enable (irreversible)
   bash "<skill_dir>/scripts/devhub.sh" <org> --list-scratch         # list active scratch orgs
   ```

   `<skill_dir>` is the absolute path to the directory containing this SKILL.md.

2. **For enablement, default to a dry run first.** Run `--enable` (no `--apply`)
   to validate the deploy, then relay the result. Because enabling is
   **irreversible**, only run `--enable --apply` when the user has clearly asked
   to actually enable Dev Hub. Applied operations require an explicit org alias
   or username; the script refuses to mutate an implicit default org. The
   script also refuses to enable on a **sandbox** — it checks the org's edition
   facts first and returns an eligibility explanation instead of deploying, and
   `status` on a sandbox reports the same ineligibility. When the target is
   ineligible (a sandbox, or an org with a registered namespace), **declining to
   enable is the correct, complete outcome even if the user explicitly asked to
   apply it** — do not deploy. Give a full answer that (1) states Dev Hub
   **cannot** be enabled on this org, (2) says **why** (a sandbox cannot host a
   Dev Hub; a registered namespace also blocks it), and (3) gives the
   **alternative** — enable Dev Hub on the source **production** org, or a
   **Developer Edition / trial** org, with a **System Administrator**, and use
   that as the Dev Hub. Do not report a scratch-org allocation for an ineligible
   org. If the deploy is rejected for permissions, surface the Setup-UI fallback
   it prints.

3. Relay the script output. When an org can't be authenticated, the script
   never logs in on its own — it prints the exact `sf org login web` command as
   guidance; surface that command to the user so they can run it themselves,
   then re-run the skill. When no org and no default are configured, it also
   lists the authenticated orgs it found so the user can pick one. Pick
   optional flags based on the request (see below): `--allocation` for limits
   only, `--show-settings` for current preference values, `--list-orgs` for
   discovery, `--list-scratch` to enumerate scratch orgs, `--packaging` /
   `--snapshots` / `--shape` to turn on sub-preferences, `--json` for automation.

## Before you finish

Verify these before returning your answer:

- [ ] **CRITICAL:** Invoked the helper via its **absolute path** (`bash "<skill_dir>/scripts/devhub.sh" …`), never `./scripts/` (the script rejects a non-absolute `$0`).
- [ ] Did **not** run `--apply` unless the user clearly asked to actually enable Dev Hub or deploy a preference — enabling is **irreversible**.
- [ ] Did **not** attempt to log in on the user's behalf — if the org isn't authenticated, relayed the `sf org login web` guidance the script printed instead of running it.
- [ ] Relayed the script's own output (status/allocation/settings, the pre-flight warnings, the discovered orgs, the sandbox-eligibility refusal, or the login/Setup-UI guidance it printed), rather than substituting a hand-written answer.

## Options

| Flag | Purpose |
|------|---------|
| `--allocation`, `-A` | Show only the scratch org allocation (Active/Daily), including pre-flight `WARN`/`NOTE` lines when close to the limit. |
| `--show-settings`, `-s` | Show the org's current `DevHubSettings` preference values (packaging, snapshots, shape, etc.), ON/OFF. Requires Dev Hub to already be enabled. |
| `--list-orgs` | List authenticated orgs (alias, username, connected status, default marker). No target org required. |
| `--list-scratch`, `-l` | List active scratch orgs created from this Dev Hub. |
| `--enable`, `-e` | Enable Dev Hub (deploys `enableScratchOrgManagementPref=true`). Dry run unless `--apply`; refuses on a sandbox. |
| `--configure`, `-c` | Configure sub-preferences without (re)enabling the master switch. Pair with a pref flag. |
| `--packaging` | `enablePackaging2=true` (Unlocked + 2GP packages). |
| `--snapshots` | `enableScratchOrgSnapshotPref=true`. |
| `--shape` | `enableShapeExportPref=true`. |
| `--scratch-management` | `enableScratchOrgManagementPref=true` (the Dev Hub switch). |
| `--pref KEY=VALUE` | Any `DevHubSettings` sub-pref (KEY starts with `enable`, VALUE `true`/`false`). Repeatable. |
| `--apply` | Actually deploy to the explicit org argument. Default for `--enable`/`--configure` is a validate-only dry run. |
| `--json` | Emit machine-readable JSON. |
| `--fail-if-disabled` | Exit `3` if Dev Hub is not enabled (CI/cron gate). |
| `--help`, `-h` | Show usage. |

`--enable` may be combined with sub-pref flags to enable and configure at once
(e.g. `--enable --packaging --apply`). If omitted, the org defaults to
`target-org`, then `target-dev-hub`.

## Output examples

The script prints the authoritative output at runtime. If you need to calibrate
what an enabled-vs-disabled status transcript looks like (including the
allocation table and the enable/Setup-UI guidance), read
[`examples/status-output.md`](examples/status-output.md) — otherwise skip it to
keep this workflow lean.

## Structured output for automation (`--json`)

Use `--json` in any mode for machine-readable output (no prose). Status returns
`devHubEnabled`, `status`, `edition`, `isSandbox`, and an `allocation` object
(with `usedPct` per limit and a `warnings` array); `--show-settings` returns
`org` and a `settings` map of preference key → boolean; `--list-orgs` returns
a normalized array of `{alias, username, connectedStatus, isDefault}`;
enablement returns `success`, `applied`, and `devHubVerifiedState`.
Deterministic, no LLM needed.

```bash
bash "<skill_dir>/scripts/devhub.sh" my-devhub --json
# {"org":"my-devhub","devHubEnabled":true,"status":"enabled", ... }
```

`--fail-if-disabled` exits `3` (and prints an `ALERT:` line to stderr) if Dev
Hub is not enabled, so a scheduled job can gate on it.

## Exit codes

- `0` success
- `1` an org could not be queried, or a deploy failed (auth/connection/deploy)
- `2` bad usage or a missing dependency (`sf` or `jq`)
- `3` Dev Hub is not enabled (only when `--fail-if-disabled` is set)

## Authentication (guidance only)

This skill **never runs an interactive login itself** — it has no `--login` or
`--instance-url` flag, and it never invokes `sf org login web` or
`sf org login device`. If the target org can't be queried (not authenticated,
expired session, wrong instance), the script prints the exact login command as
copy-paste **guidance** and stops; relay that command to the user and let them
run it, then re-run the skill:

```text
  my-org                         could not query org (...)

  This org is not authenticated (or the session expired). Authentication is
  a precondition for this skill — run one of these yourself, then re-run:
    sf org login web --alias 'my-org'                                             # prod / DE / trial
    sf org login web --alias <my-alias> --instance-url https://MYDOMAIN.my.salesforce.com   # sandbox / My Domain
  List existing logins with:  sf org list
```

When no org and no default is configured at all, the script also runs org
discovery (`--list-orgs`) and lists the authenticated orgs it found, so the
user can pick one instead of guessing an alias.

## Manual fallback (if the script is unavailable)

```bash
# Detect Dev Hub (INVALID_TYPE error means OFF; a count means ON):
sf data query --query "SELECT COUNT() FROM ScratchOrgInfo" --target-org <org> --json

# Read current DevHubSettings preferences (requires Dev Hub already ON):
sf api request rest "/services/data/v62.0/tooling/sobjects/DevHubSettings/DevHub" \
  --target-org <org> --json

# Enable Dev Hub via the Tooling API (what the Setup toggle does; irreversible):
sf api request rest "/services/data/v62.0/tooling/sobjects/DevHubSettings/DevHub" \
  --method PATCH \
  --body '{"FullName":"DevHub","Metadata":{"enableScratchOrgManagementPref":true}}' \
  --target-org <org>

# Or enable in the UI: Setup > Quick Find > "Dev Hub" > turn Enable Dev Hub On.

# View scratch org allocation:
sf org list limits --target-org <org> --json | jq '.result[] | select(.name|test("ScratchOrg"))'

# List authenticated orgs:
sf org list --json
```

## Notes

- Requires the Salesforce CLI (`sf`) and `jq` on the PATH, plus at least one
  authenticated org. This skill only ever prints the `sf org login web`
  command as guidance — it never runs it.
- After enabling, set the org as your default Dev Hub:
  `sf config set target-dev-hub <org>`.
- Enabling **packaging** (`enablePackaging2`) requires Dev Hub to be on first —
  `--enable --packaging` handles the ordering in a single deploy.
- Non-admin users still need object access (Read/Create on `ScratchOrgInfo` and
  `ActiveScratchOrg`) to create/view scratch orgs, and the "Create and Update
  Second-Generation Packages" permission to build 2GP/unlocked packages.
