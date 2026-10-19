---
name: cloud-azure
description: >
  Attack Azure / Entra ID — managed-identity token theft, Entra (Azure AD) role abuse, and app/
  storage misconfig. Load when the target is on Azure, you hold Azure creds/a token, or see
  Entra/AAD/azurewebsites/blob.core.windows.net. Signals: 169.254.169.254 IMDS, Managed Identity,
  az cli, Entra roles, service principals.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A01:2021-Broken-Access-Control, A05:2021-Security-Misconfiguration]
cwe: [CWE-269, CWE-732]
mitre: [T1078.004, T1552.005]
tools: [az, AzureHound, ScoutSuite, MicroBurst]
schema_version: 1
---

# Azure / Entra ID attacks

## When it applies
Target on Azure and you have some access — SSRF into a VM/App Service with a **Managed Identity**,
a leaked service-principal secret/cert, or a foothold. Goal: steal tokens, abuse Entra roles, reach resources.

## Why it works
Azure resources authenticate via **Managed Identities** and **service principals**; the IMDS hands
out OAuth tokens for them. Entra (Azure AD) roles and app permissions are widely over-assigned, and
several (adding credentials to a service principal, role assignment, Owner on a subscription) escalate to control.

## Method
1. **Managed Identity → token** (via SSRF, or on the host): `GET http://169.254.169.254/metadata/identity/
   oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/` with header
   `Metadata: true` (→ `cloud-imds-ssrf`). Also request tokens for Graph, Key Vault, Storage.
2. **Authenticate & enumerate**: `az login` with the SP or token; enumerate roles/resources; map
   Entra with **AzureHound** (BloodHound for Azure); ScoutSuite/MicroBurst for misconfig.
3. **Entra / IAM privesc**: add credentials to a service principal you can manage → auth as it;
   abusive Entra roles (Application/Cloud App Admin, Privileged Role Admin); role assignment
   (`Microsoft.Authorization/roleAssignments/write`) → grant yourself Owner; consent grants.
4. **Resources & secrets**: Key Vault (token for `vault.azure.net`), Storage blobs
   (→ storage misconfig), Automation Accounts / runbooks (RCE as their identity), App Service.
5. **Prove impact** read-only as the escalated principal; avoid persistent role changes.

## Gotchas
- Two planes: **ARM** (resources) and **Microsoft Graph / Entra** (identity) — get tokens for the right `resource`/audience.
- Managed-identity SSRF needs the `Metadata: true` header — header-less SSRF won't work (that's the mitigation).
- AzureHound reveals Entra attack paths you'd miss manually — run it early.

## Verify success
Escalated access proven — a token/role letting you act beyond your start (Key Vault secret read,
subscription role you granted, resource action as a managed identity).

## References
Azure IMDS & Managed Identity docs; AzureHound/BloodHound; MicroBurst; Entra privesc research.
