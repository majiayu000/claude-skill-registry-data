---
name: oci-session
description: Install the OCI CLI and establish an authenticated session before any other OCI work. Use for installing oci, `oci session authenticate`, expired or invalid session tokens, NotAuthenticated errors, switching profiles, choosing between browser session tokens and API keys, discovering tenancy/compartment/home-region values, and recording them as configuration.
---

# OCI session

Nothing else in this repository works until `oci` is installed, authenticated, and
pointed at the right region. Full procedure:
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/set-up-the-cli.md`. This skill handles
authentication itself; the `oci-setup` skill wraps it for first-time setup and
writes the configuration the other skills read.

## Establish context first

1. Check whether the CLI exists: `oci --version`. Install only if missing —
   `brew install oci-cli`, or Oracle's install script on Linux/WSL.
2. Check for existing credentials before creating new ones: `ls ~/.oci/config`
   and `env | grep '^OCI_'`.
3. Use the selected profile from `~/.oci/config` and discover all other values
   at runtime. Never invent OCIDs or rely on a plugin configuration file.

## Correct two things users often say

- **"Install Oracle Cloud Shell."** Cloud Shell is a browser terminal in the OCI
  Console — it cannot be installed. Install the OCI CLI instead, and mention that
  Cloud Shell is a zero-setup fallback where every runbook command works
  unchanged.
- **"Just use my API key."** Prefer `oci session authenticate` for interactive
  work: nothing long-lived lands on disk. Reserve API keys for automation, and
  prefer instance principals when running on an OCI instance.

## Authenticate

Browser session login is interactive and cannot be completed on the user's
behalf. Run it in the background so the browser opens without blocking, then tell
the user to complete the login:

```bash
oci session authenticate --profile-name <profile> --region <region>
```

Then verify rather than assuming:

```bash
export OCI_CLI_PROFILE=<profile> OCI_CLI_AUTH=security_token
oci session validate --profile "$OCI_CLI_PROFILE" --auth security_token
```

Session tokens expire in roughly an hour. Every session-token call needs
`--auth security_token` or `OCI_CLI_AUTH=security_token`.

## Treat NotAuthenticated as an expired token

On `NotAuthenticated` mid-session, refresh before investigating anything else:

```bash
oci session refresh --profile "$OCI_CLI_PROFILE"
```

Do not re-run full authentication, rewrite config, or start diagnosing IAM
policies until a refresh has been tried.

`NotAuthorizedOrNotFound` against an OCID you know exists is usually
authorization, not a typo — OCI hides existence from unauthorized callers. Do not
respond by broadening IAM permissions.

## Discover values, never hardcode them

```bash
# Tenancy OCID from the config the auth step wrote
grep -A8 "^\[$OCI_CLI_PROFILE\]" ~/.oci/config | grep '^tenancy' | cut -d= -f2 | tr -d ' '

# Home region — the only region where Always Free compute and storage exist
oci iam region-subscription list \
  --query 'data[?"is-home-region"]."region-name" | [0]' --raw-output

oci iam compartment list --compartment-id "$OCI_TENANCY_ID" --all
oci iam availability-domain list --compartment-id "$OCI_TENANCY_ID" --query 'data[].name'
```

Confirm the profile's configured `region` equals the home region and say so
explicitly. A mismatch silently makes everything billable — flag it before any
resource is created.

Recommend a dedicated compartment over the tenancy root; it makes inventory and
teardown far easier.

## Handling credentials

- Never print, log, echo, or commit private keys, session tokens, or the contents
  of `~/.oci/config`.
- Never write real OCIDs, IP addresses, or CIDRs into tracked files. Keep them in
  the current shell or query them again when needed.
- When showing a value for confirmation, truncate it.
- Do not run `oci setup repair-file-permissions` on a whim; report permission
  warnings to the user instead.

## Finish by verifying

```bash
oci iam compartment get --compartment-id "$OCI_COMPARTMENT_ID" \
  --query 'data.{name:name,state:"lifecycle-state"}'
```

Report the profile, auth mode, home region, configured region, and compartment
name. Then point at `${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md` before any
provisioning begins.
