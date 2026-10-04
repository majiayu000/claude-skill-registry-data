---
name: oci-setup
description: Set up this plugin against an Oracle Cloud tenancy — first-time setup, configure the plugin, authenticate to Oracle Cloud, log in, "get me started", install the oci CLI, pick or create a compartment, choose an SSH key, refresh OPERATOR_CIDR after "my IP changed", reconfigure, switch profile, answer "which tenancy am I using".
argument-hint: "[profile-name]"
allowed-tools: Bash(oci *) Bash(curl *) Bash(ssh-keygen *) Read Write AskUserQuestion
---

# OCI setup

Interactive first-run setup. Discover everything the API can tell you; ask only
what it cannot. Never ask the user to paste an OCID. Profile name comes from the
argument, else `default-free`. Manual procedure:
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/set-up-the-cli.md`. If configuration already
exists (step 5), read it and offer **Reconfigure** instead of the whole flow.

## Step 1 — Is the CLI present?

`oci --version`. Install only if that fails: `brew install oci-cli` on macOS, or on
Linux/WSL `bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"`.
Distro packages lag; prefer Oracle's script.

**"Oracle Cloud Shell" cannot be installed.** It is a browser terminal in the OCI
Console with the CLI and credentials already configured — a valid zero-setup
fallback when local install or auth gives trouble, where every command here works
unchanged.

## Step 2 — Authenticate

Ask with AskUserQuestion which mode:

| Mode | `OCI_CLI_AUTH` | Use for |
|---|---|---|
| Browser session token | `security_token` | Interactive use. Recommended. Expires ~1 hour. Nothing long-lived on disk. |
| API signing key | `api_key` | Automation and cron. Never expires. Guard it like a password. |

Browser login is interactive and cannot be completed for the user. Run it in the
**background** so the browser opens without blocking:

```bash
oci session authenticate --profile-name <profile>
```

`--region` is effectively required; omitted, the command prompts with a picker.
The home region is not discoverable until after auth, so let it prompt or pass a
region the user already knows. Tell the user to complete the browser login, then
wait for the background command to finish. `oci setup config` (the `api_key` path)
is likewise interactive — hand it to the user.

Never claim login succeeded without verifying:

```bash
oci session validate --profile <profile> --auth security_token
```

## Step 3 — Auto-discover; do not ask

```bash
export OCI_CLI_PROFILE=<profile> OCI_CLI_AUTH=security_token
CFG="$HOME/.oci/config"

# Tenancy OCID from the config the auth step wrote, and the configured region
grep -A8 "^\[$OCI_CLI_PROFILE\]" "$CFG" | grep '^tenancy' | cut -d= -f2 | tr -d ' '
grep -A8 "^\[$OCI_CLI_PROFILE\]" "$CFG" | grep '^region'  | cut -d= -f2 | tr -d ' '

# Home region — never hardcode a region
oci iam region-subscription list \
  --query 'data[?"is-home-region"]."region-name" | [0]' --raw-output

oci iam availability-domain list --compartment-id "$OCI_TENANCY_ID" --query 'data[].name'
echo "$(curl -s https://checkip.amazonaws.com)/32"
```

Warn **loudly** if the configured region differs from the home region, before
anything is created: Always Free compute and storage exist ONLY in the home
region; anywhere else bills.

Show the detected IP for confirmation. A VPN, CGNAT, or corporate proxy can make
it differ from what a browser reports — it must be the address *this machine*
egresses from, because it becomes the only address allowed to SSH in.

SSH key: `ls "$HOME"/.ssh/*.pub`. One match → use it. Several → ask which. None →
offer `ssh-keygen -t ed25519 -C "oci-free-tier" -f ~/.ssh/oci_free_tier`. The
**public** key is what gets injected; the private key is the only way in. Lose it
and the instance is permanently unreachable — there is no password reset.

## Step 4 — Ask only what cannot be discovered

Only the compartment. List them, let the user pick, or offer to create a
dedicated one:

```bash
oci iam compartment list --compartment-id "$OCI_TENANCY_ID" --all \
  --query 'data[].{name:name,id:id,state:"lifecycle-state"}' --output table

oci iam compartment create --compartment-id "$OCI_TENANCY_ID" \
  --name "<name>" --description "Always Free resources managed via oracle-cloud-cli-ops" \
  --wait-for-state ACTIVE
```

A dedicated compartment beats the tenancy root for two concrete reasons: an
inventory listing only what this plugin created, and a single thing to empty at
teardown.

## Step 5 — Keep runtime context only

Do not write a plugin configuration file. Keep discovered values in the current
session and rediscover them when another skill runs. OCI credentials remain in
the user's standard `~/.oci/config`.

## Step 6 — Verify and report

```bash
oci iam compartment get --compartment-id "$OCI_COMPARTMENT_ID" \
  --query 'data.{name:name,state:"lifecycle-state"}'
```

Report profile, auth mode, home region vs configured region, compartment name,
availability-domain count, operator CIDR, and SSH public key path. Then state the
Always Free allowance — **2 OCPUs, 12 GB RAM, 200 GB storage, home region only** —
and point at `${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md` before provisioning
anything.

## Reconfigure — never re-run the whole flow for a partial change

| Change | Do only this |
|---|---|
| IP changed | Re-run the `checkip` command and confirm the new `/32`. Updating live security rules is `oci-operate`'s job, not this skill's. |
| Different compartment | Re-run step 4 and select the compartment again. |
| Different profile | Authenticate it (step 2), select it for the session, and re-check the home region — a different profile can mean a different tenancy. |
| New SSH key | Select the new public key. Running instances keep the old key; only new launches pick it up. |

## Hard rules

- Never print, log, echo, or commit private keys, session tokens, or the contents
  of `~/.oci/config`.
- Never write real OCIDs, IPs, or CIDRs into any tracked repo file — they belong
  only in the current shell. Truncate
  anything shown for confirmation.
- Treat `NotAuthenticated` as an expired session token first: run
  `oci session refresh --profile "$OCI_CLI_PROFILE"` before investigating IAM,
  rewriting config, or re-authenticating.
- `NotAuthorizedOrNotFound` on an OCID you know exists is usually authorization,
  not a typo — OCI hides existence from unauthorized callers. Never respond by
  broadening IAM permissions.
- Create nothing in this flow except, with explicit consent, a compartment and an
  SSH key.
