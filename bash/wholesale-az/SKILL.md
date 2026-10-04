---
name: wholesale-az
description: >
  Safe Azure CLI operations for the Brown & Brown Wholesale (WHS-346) fleet.
  Captures identities, subscriptions, service connections, managed identities,
  known traps (az account clear, device code login), one-shot pipeline patterns,
  and federated credential workflows. Load BEFORE any az CLI command in the
  wholesale repo when the task involves authentication, deployment, role
  assignments, service connections, or managed identities.
---

# Wholesale Azure CLI Operations

Safe, known-good patterns for Azure CLI operations in the WHS-346 wholesale fleet.
Load this BEFORE running any `az` command that touches identity, auth, deployment,
or role assignments.

## Machine profiles

### bb-mac (macOS, Leo's machine)
- SSH reachable: `ssh bb-mac`
- Authenticated as: `BBAdminLAcosta@bbins.com` (user, not SPN)
- Object ID: `f183a4a9-8ab5-4e4c-84b6-9d713e109d03`
- az CLI works; `az devops` configured for `brownandbrowninc` / `Wholesale Architecture`
- Has `azure-devops` extension v1.0.6+
- Auth is via `az login` interactive session (NOT managed identity, NOT SPN)
- Can query service connections, pipelines, Graph API (read-only for most resources)

### Linux workstation (this machine)
- May or may not have active `az login`
- Has `azure-devops` extension v1.0.8+
- Can use device code login: `az login --use-device-code`
- Has `~/.local/bin/az` wrapper that routes through CPC SOCKS tunnel
- The wrapper uses `AZURE_CONFIG_DIR=~/.azure-bbadmin` with BBAdmin auth
- ACR module restores work through the SOCKS proxy for `az deployment group what-if`
- `az bicep what-if` works locally via the SOCKS wrapper (proven Jul 2026)

### CPC (Cloud PC, Windows bastion)
- SSH reachable from Linux: `ssh cpc`
- Windows machine on the corporate network, inside the VNet spoke
- Used as a SOCKS5 proxy tunnel for Azure CLI from Linux (`localhost:1080`)
- Tunnel service: `cloudpc-tunnel.service` (auto-started by workspace activation)
- Has SSHD running for SSH access
- Can resolve private endpoint DNS names (proven: KV, SQL FQDNs resolve to PE NIC IPs)
- Has `scripts/azc` for Azure CLI via CloudPC
- **Critical: CPC has BOTH a local Windows user profile AND the AD (Azure AD) user profile**
  - If AD auth breaks (e.g., AD user password expired, domain trust issue), the LOCAL user
    profile can still be used as a jump box to restart services
  - The SSH service (sshd) runs as a Windows service and can be restarted from the local profile

### Recovering CPC SSH when the AD user connection is severed

If `ssh cpc` fails because the AD user profile can't authenticate (password expired,
domain trust broken, etc.):

1. **Use the local user profile as a jump box:**
   ```bash
   ssh localuser@cpc
   ```
   The local Windows user profile exists independently of AD and can still authenticate.

2. **Restart the SSH service from the local profile:**
   ```powershell
   Restart-Service sshd
   ```
   Or via `services.msc` GUI if RDP is available.

3. **Verify AD user can authenticate again:**
   ```bash
   ssh cpc
   ```

4. **If SSHD itself is broken, restart via the Windows Services console** or
   ```powershell
   Get-Service sshd | Restart-Service
   ```

### Re-authenticating Azure CLI (az login)

The `az` CLI wrapper at `~/.local/bin/az` is the **preferred** entry point for Azure
CLI operations from Linux. It:
- Routes traffic through the CPC SOCKS5 proxy (`127.0.0.1:1080`)
- Uses `AZURE_CONFIG_DIR=~/.azure-bbadmin` for BBAdmin credentials
- Sets `DOTNET_SYSTEM_NET_DISABLEIPV6=1` for bicep module restores
- Uses environment variables for proxy configuration

If the tunnel is down, activate the workspace:
```bash
wsenv --activate ws
```

To check tunnel status:
```bash
ss -tlnp | grep 1080
```

If az login is needed (token expired or `az account clear` was run -- DON'T):
```bash
az login --use-device-code
```
This requires Leo to complete the browser flow. There is NO non-interactive way
to re-authenticate BBAdmin.

**CRITICAL: NEVER use `az account clear`**. If you need a fresh token, either:
- Wait for the existing token to expire (1 hour)
- Run `az account get-access-token` to get a fresh token without clearing
- Let the wrapper handle token refresh automatically

## FORBIDDEN commands

### NEVER run `az account clear`
This kills the session and leaves no token for `az devops` or `az rest`.
There is no recovery without Leo's interactive browser auth.
If you think you need a fresh token, use `az account get-access-token` instead,
or wait for token expiry (1 hour).
If it's already been run, you're blocked until Leo completes `az login --use-device-code`.
See "Re-authenticating Azure CLI" above for recovery steps.

To prevent accidents, add to shell rc:
```bash
alias az='function __az() { if [[ "$*" == *"account clear"* ]]; then echo "NOT ALLOWED: az account clear kills the session. Use az account get-access-token for fresh tokens." >&2; return 1; fi; command az "$@"; }; __az'
```

### NEVER try `az login --identity` on a non-Azure machine
This tries 169.254.169.254 (IMDS) and hangs/times out. Only works on Azure VMs.
Use `az login --use-device-code` instead.

### NEVER try `az login --service-principal` without explicit [LEO] approval
This requires a client secret that does not exist for the managed identity SPN.

## Identity landscape

### The pipeline identity (DEV)
| Field | Value |
|---|---|
| Name | `ID-WHS-346-IAC-CentralUS-DEV` |
| Type | User-Assigned Managed Identity |
| Client ID | `827e8919-6711-4cbd-97b9-5beda27ded45` |
| SPN Object ID | `85c0a90f-4ef0-42a5-b745-01b52fc634be` |
| Tenant ID | `f1289cc5-8456-4f28-8eab-700d1300fc5d` |
| Subscription | `21b25913-29c0-40f8-8911-6fe519539060` (WHS-346-Wholesale-DEV) |
| Resource Group | `RG-WHS-346-CORE-CentralUS-DEV` |
| ARM Resource ID | `/subscriptions/21b25913/.../userAssignedIdentities/ID-WHS-346-IAC-CentralUS-DEV` |
| Auth in ADO | Workload Identity Federation (EntraID issuer) |
| Service Connection | `SC-WHS-346-Wholesale-DEV` (ID: `22bc45a9-da2a-4dc0-96a0-40c1c4d4fa8f`) |
| Federated Credentials | 9 existing FICs for ADO service connections |

### The pipeline identity (PROD)
| Field | Value |
|---|---|
| Client ID | `f0c6d46c-64a0-4343-a200-5f835625845f` |
| SPN Object ID | `9f624f0b-0bcb-47ef-a479-65693dc9b969` |
| Subscription | `b2a995ac-59dc-4cd3-bbe8-77a96b6377e3` (WHS-346-Wholesale-PROD) |
| Service Connection | `SC-WHS-346-Wholesale-PROD` (ID: `47861f28-af91-4f83-b763-3b2c37e0c8ba`) |
| DO NOT USE for local dev | PROD is approval-gated |

### BBAdmin (Leo's user identity)
| Field | Value |
|---|---|
| UPN | `BBAdminLAcosta@bbins.com` |
| Display Name | `Admin Leonardo Acosta` |
| Object ID | `f183a4a9-8ab5-4e4c-84b6-9d713e109d03` |
| Subscription access | Multiple subs including `21b25913` and `b2a995ac` |
| RBAC roles on DEV sub | Monitoring Reader, Cost Management Reader, Grafana Admin, Key Vault Administrator, Storage Blob Data Owner, Storage Queue Data Contributor, Azure Service Bus Data Owner, App Configuration Data Owner, Website Contributor, Reader, Log Analytics Reader, Storage Blob Data Contributor, SQL DB Contributor, Monitoring Contributor, Application Insights Component Contributor |
| `roleAssignments/write` | **NOT granted** (cannot create RBAC assignments) |
| MI Federated Credential Contributor | **GRANTED** on `ID-WHS-346-IAC-CentralUS-DEV` (run 62053, 2026-09-17) |
| App registration access | Cannot read/modify app registrations (not an owner) |

### Other identities
- PRimate app registration: `5246f8af` (used for AI review)
- ADO Resource ID: `499b84ac-1321-427f-aa17-267ca6975798`

## Service connection queries

Query service connection details from bb-mac:
```bash
ssh bb-mac "az devops service-endpoint show --id <id> --query '{auth:authorization, data:data}' -o json"
```

List WHS-346 service connections:
```bash
ssh bb-mac "az devops service-endpoint list --query \"[?contains(name, 'WHS-346')].{name:name, id:id}\" -o json"
```

Get the app/client ID from a service connection:
```bash
ssh bb-mac "az devops service-endpoint show --id <id> --query 'authorization.parameters.serviceprincipalid' -o tsv"
```

## Managed identity operations

Check if an SPN is a managed identity:
```bash
ssh bb-mac "az rest --method GET \
  --uri 'https://graph.microsoft.com/v1.0/servicePrincipals/<spn-object-id>?\$select=servicePrincipalType' \
  --query 'servicePrincipalType' -o tsv"
```

List federated credentials on a managed identity:
```bash
ssh bb-mac "az rest --method GET \
  --uri 'https://graph.microsoft.com/v1.0/servicePrincipals/<spn-object-id>/federatedIdentityCredentials' \
  --query 'value[].{name:name, issuer:issuer, subject:subject}' -o json"
```

Add a federated credential (requires MI Federated Identity Credential Contributor role):
```bash
az identity federated-credential create \
  --identity-name 'ID-WHS-346-IAC-CentralUS-DEV' \
  --resource-group 'RG-WHS-346-CORE-CentralUS-DEV' \
  --name '<credential-name>' \
  --issuer '<issuer-url>' \
  --subject '<subject-identifier>'
```

## Pipeline operations

Queue a pipeline for DEV (never PROD without approval):
```bash
ssh bb-mac "az pipelines run --id <def-id> --branch dev"
```

Key pipeline definitions (resolve from `scripts/lib/ado-pipelines.json`):
- Wholesale foundation: dev=449, test=451, stage=452, prod=418
- Fireball: dev=450, test=478, stage=486, prod=566
- Cost center: dev=447, test=448, stage=469, prod=570
- One-shot grant pipeline: 772 (`ops-grant-bbadmin-mi-fic`)

Create a new pipeline from YAML:
```bash
ssh bb-mac "az pipelines create \
  --name '<name>' \
  --branch dev \
  --repository 'Wholesale Architecture' \
  --repository-type tfsgit \
  --yml-path '.azuredevops/build/operations/<file>.yml' \
  --skip-first-run"
```

## RBAC grant pattern (one-shot pipeline)

To grant a role that BBAdmin cannot assign directly, use a one-shot pipeline
that runs under the CHS-owner service connection. Template at
`.azuredevops/build/operations/grant-bbadmin-mi-fic.yml`.

Key pattern:
```yaml
pool:
  vmImage: ubuntu-latest
variables:
  - template: ../_templates/pool-vars.yml
    parameters:
      env: dev
steps:
  - task: AzureCLI@2
    inputs:
      azureSubscription: $(SERVICE_CONNECTION)
      scriptType: bash
      scriptLocation: inlineScript
      inlineScript: |
        az role assignment create \
          --assignee-object-id '<principal-oid>' \
          --assignee-principal-type User \
          --role '<role-name>' \
          --scope '<scope-resource-id>'
```

## Subscription inventory

| Subscription ID | Name | Environment |
|---|---|---|
| `21b25913-29c0-40f8-8911-6fe519539060` | WHS-346-Wholesale-DEV | DEV |
| `b2a995ac-59dc-4cd3-bbe8-77a96b6377e3` | WHS-346-Wholesale-PROD | PROD |
| `d645419b-96bb-4026-a310-72827580cf56` | ALL-Wholesale | Shared |
| `979366b2-fe6a-4ee9-a57d-5b280907c375` | ALL-Wholesale-DEV | Shared DEV |

## Graph API patterns

Query service principal details:
```bash
ssh bb-mac "az rest --method GET \
  --uri 'https://graph.microsoft.com/v1.0/servicePrincipals?\$filter=appId eq '<client-id>'&\$select=id,appId,servicePrincipalType'"
```

Check BBAdmin's group memberships:
```bash
ssh bb-mac "az rest --method GET --uri 'https://graph.microsoft.com/v1.0/me/memberOf'"
```

## Known traps

1. `az ad app show --id <client-id>` fails for managed identities (they're not app registrations)
2. `az ad sp credential reset` fails with "Managed and social identities cannot be modified"
3. The role name is `Managed Identity Federated Identity Credential Contributor` (note "Identity" appears twice)
4. Role GUID `c69a1474-6a44-49bd-a55c-0f82b0be4f0b` is WRONG; correct GUID is `7e559ce2-48d7-4b27-9128-fa1b247f1308`
5. `az pipelines run --commit-id` needs the commit to be reachable from the branch on the ADO remote
6. Azure DevOps REST API logs require authentication (can't curl directly; use `az rest`)
7. `az account clear` on bb-mac also kills `az devops` auth -- they share the token
8. `az login --identity` hangs on non-Azure machines (IMDS unreachable)