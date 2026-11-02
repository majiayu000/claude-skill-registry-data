---
name: operate-azure
description: Use when operating Azure by CLI — confirm sign-in, tenant and active subscription first, choose read-only or IaC or a recorded one-off, query with az graph, avoid az rest and RBAC traps, and keep Terraform-managed resources hands-off.
---

# Operate Azure

Read-only by default. **Never change prd by hand when the resource is IaC-managed; change the code
and promote it** ([set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md)).
A CLI session is for investigation, small CLI-managed fixes with a record, and emergencies —
with the revert plan written before the command runs.

## 1. Audit — signed in, and where (change nothing)

```bash
az version                                                       # CLI present, version line
az account show -o json | jq -r '.tenantId, .id, .name'          # ACTIVE tenant and subscription
az account list --query '[].{sub:name, id:id, default:isDefault}' -o table
az ad signed-in-user show --query userPrincipalName -o tsv       # who am I
az graph query -q "Resources | summarize count() by type | top 5 by count_" -o table   # needs extension resource-graph
```

Also check the track before touching anything (step 3). Most "wrong resource" incidents start
with the right command in the wrong subscription.

## 2. Decide

- **Read-only investigation (default)** — `show`, `list`, `az graph query`, `az rest --method GET`.
- **The resource is IaC-managed and needs a change** — change the code, open a PR, promote it.
  No hand edits on prd; on dev/stg a hand edit creates drift — still say no.
- **CLI-managed resource, one-off change justified** — smallest command that does it, JSON output
  pasted into the ticket as the record, revert command named before running. Firewall IP rules
  and role assignments made this way are removed again (step 5, step 7).

## 3. Detect the track

| Signal | Track | Then |
|---|---|---|
| `terraform/` covers it — `tofu -chdir=terraform/envs/<env> state list \| grep -i <name>`, or it appears in `*.tf` | IaC | Read-only here; change via [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md) |
| Repo has `*.bicep` files or `az deployment group` scripts | Bicep | Change the template, deploy through the repo's deployment flow |
| Neither, and tags/history say CLI | CLI-managed | One-off change with a record (step 2) |

```bash
tofu -chdir=terraform/envs/<env> state list 2>/dev/null | grep -i <name>
grep -rn "azurerm_" terraform/ --include='*.tf' 2>/dev/null | grep -i <name> | head -5
find . -name '*.bicep' -not -path '*/node_modules/*' | head -5
az resource show --ids <resource-id> --query tags -o json     # a `managed-by`-style tag tells you who owns it
```

## 4. Install only what is missing

```bash
brew install azure-cli jq                 # verify version before pinning (../_shared/stack-versions.md)
az extension add --name resource-graph    # for az graph query
az extension add --name account
```

`azd` and Bicep only when the project already uses them; the full table is in
[cli-toolbox](../_shared/cli-toolbox.md).

## 5. Do the work

**Sign in per tenant — never rely on the default subscription:**

```bash
az login --tenant <tenant-id>
az account set --subscription <subscription-id>
az account show --query id -o tsv          # confirm the subscription you intended
```

**Find things:**

```bash
az graph query -q "Resources | where name contains '<app>' | project name, resourceGroup, type, location" -o table
az resource list --resource-group <rg> -o table      # ARM resources of the ACTIVE subscription only
```

`az resource list` sees only ARM resources. Service principals, groups and users are Entra
objects, not ARM resources — use [operate-entra-and-exchange](../operate-entra-and-exchange/SKILL.md).

**RBAC:**

```bash
az role assignment list --assignee <object-id> --scope <scope> -o table
az role assignment create --assignee <object-id> --role "<role-name>" --scope <scope>
az role assignment delete --id <assignment-id>        # the explicit counterpart; create does not clean up
```

Propagation takes 2–5 minutes — a "still forbidden" right after a grant is usually not an error.
Key Vault secrets need a **data-plane** role (`Key Vault Secrets User`), not a management role;
"secret not found" is usually a missing data-plane role or the wrong subscription, not a missing
secret.

**`az rest` — GET, merge, PUT:**

```bash
# endpoint with no CLI command — e.g. static web app app settings; exact path and api-version per resource docs
az rest --method GET --url "https://management.azure.com<resource-id>/<settings-path>?api-version=<api-version>" -o json > settings.json
jq '.properties.appSettings.newKey = "newValue"' settings.json > settings.merged.json   # merge in jq, never by hand
# then PUT settings.merged.json back at the same URL — a PUT replaces the WHOLE set
```

**Output:** `-o tsv` prints booleans capitalised (`True`/`False`). Compare case-insensitively or
use `-o json | jq`.

**Firewall-gated data stores** (SQL, storage, Key Vault): add a temporary IP rule, work, remove it
in the same session — the remove command written down before the add runs (patterns file).

**Hygiene:** name `<app>-<env>-<type>`, tag `app`/`env`, resource locks `CanNotDelete` on prd:

```bash
az lock create --name lock-<app>-prd --lock-type CanNotDelete --resource-group <rg>
az consumption usage list --top 5 -o table          # current-month cost; budgets per subscription
```

## 6. Wire

- **Identifiers** (`<tenant-id>`, `<subscription-id>`, resource IDs) live in the IaC repo's
  `envs/*.tfvars` and backend config — real values there, placeholders everywhere else.
- **Secrets** never in the shell profile or repo: [manage-secrets](../../infra/manage-secrets/SKILL.md).
  Locally, `az login` beats any stored token — no secret to leak.
- **IaC changes** go through [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md),
  with OIDC per environment instead of local credentials.
- Tools and versions: [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).

## 7. Verify

```bash
az account show --query id -o tsv | grep -q <subscription-id> && echo right-subscription
az resource show --ids <resource-id> --query tags -o json    # tags name the owning system
az graph query -q "Resources | where name == '<name>' | project name, type" -o table   # exactly one row
az role assignment list --assignee <object-id> --scope <scope> -o table                # the grant exists
az storage account network-rule list --account-name <account> -o table                 # no leftover client-IP rule
```

Expected: `right-subscription`, one row for the resource, the new role listed, and no temporary
IP rule left behind.

## References
- [azure-patterns.md](./azure-patterns.md): the traps — default subscription, RBAC propagation,
  data-plane roles, `az rest` PUT semantics, TSV booleans, firewall rules, locks and cost.
- [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).
- [operate-entra-and-exchange](../operate-entra-and-exchange/SKILL.md): everything not an ARM resource.
- [manage-secrets](../../infra/manage-secrets/SKILL.md),
  [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md).
- [security-baseline](../../core/_shared/security-baseline.md).
