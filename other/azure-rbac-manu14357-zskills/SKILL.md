---
name: azure-rbac
description: >
  Design and apply Azure role-based access control with least privilege at the right scope.
  Use this skill when users ask about permissions, role assignments, access errors, or governance.
  Covers built-in roles, custom roles, managed identities, PIM, and access reviews per Well-Architected principles.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [well-architected]
  security: [least-privilege, identity]
---

# Azure RBAC

Grant the minimum required access at management group, subscription, resource group, or resource scope.
Build scalable, auditable identity infrastructure using groups, managed identities, and Privileged Identity Management.

## Use This Skill When

- The user needs role assignment design or access error diagnosis
- The user wants to secure team access or workload permissions
- The user needs compliance-ready access governance (audit trail, reviews)
- The user wants to migrate from per-user to group-based RBAC

## Context: RBAC Maturity

**Immature**: Ad hoc assignments, direct user permissions, no audit trail  
**Developing**: Some group-based access, manual reviews, audit logs exist  
**Managed**: Group-based RBAC, scoped assignments, automated access reviews, PIM for elevation → **Target**  
**Optimized**: Zero Trust with managed identities, ephemeral access, real-time risk-based access decisions

## Required Inputs

- **Principals**: Users, groups, service principals, managed identities
- **Required actions**: Specific operations (create, delete, read, write)
- **Resource scope**: Subscription, resource group, or individual resource
- **Compliance needs**: Audit trail required? Access reviews? Time-bound access?
- **Escalation model**: Who approves elevated access? How long is it valid?

## Decision Tree

```
Is this human access (person) or workload identity (application)?
├─ Human:
│  ├─ Is this just viewing resources? → Reader role
│  ├─ Is this deploying/configuring? → Contributor role (at resource group scope)
│  ├─ Is this infrastructure admin work? → PIM-eligible Owner (with approval)
│  └─ Is this on a single resource? → Role-scoped to that resource
└─ Workload:
   ├─ Is this a new app? → Create user-assigned managed identity, assign narrow role
   ├─ Needs secret access? → Key Vault Secrets User role
   ├─ Needs storage access? → Storage Blob Data Contributor (scoped)
   └─ Needs database? → SQL DB Contributor (scoped)

Should this access be permanent or temporary?
├─ Permanent → Standard role assignment (group-based for humans)
└─ Temporary/Elevated → PIM-eligible role (approval workflow, 4-hour max)

How many users need this access?
├─ 1-2 people → Consider if per-user assignment is necessary
├─ 3+ people → MUST use security group assignment
└─ 10+ people → Automate group membership from identity provider
```

## Workflow

### Phase 1: Map Workload to Required Roles

1. **Identify actions needed**:
   ```
   Workload: Web App
   ├─ Needs: Read secrets from Key Vault
   ├─ Needs: Write logs to Storage Account
   ├─ Needs: Query SQL Database
   ├─ Needs: Read configuration from App Configuration
   └─ Needs: Call downstream API (no Azure role, only app auth)
   ```

2. **Match to built-in roles** (prefer over custom):
   ```
   - Key Vault Secrets User (for secret read)
   - Storage Blob Data Contributor (for write to blob)
   - SQL DB Contributor (for database access)
   - App Configuration Data Reader (for config)
   ```

3. **Prefer built-in roles** unless none match exactly:
   ```
   ✓ Use: "Key Vault Secrets User" (specific, audited)
   ✓ Use: "Storage Blob Data Contributor" (Microsoft-maintained)
   ✗ Avoid: Custom role with Microsoft.Storage/*
   ✗ Avoid: Contributor role (too broad)
   ```

### Phase 2: Human Access (Groups & PIM)

1. **Create security groups** for role assignment:
   ```bash
   # Azure AD group for developers
   az ad group create --display-name "contoso-app-developers" --mail-nickname "app-devs"
   
   # Add users to group
   az ad group member add --group app-devs --member-id $USER_ID
   ```

2. **Assign group to role at correct scope**:
   ```bash
   # Resource group scope (can deploy resources in group)
   az role assignment create \
     --role "Contributor" \
     --assignee-object-id $GROUP_ID \
     --scope "/subscriptions/$SUBID/resourceGroups/$RG"
   
   # Single resource scope (can configure only this resource)
   az role assignment create \
     --role "Key Vault Secrets User" \
     --assignee-object-id $GROUP_ID \
     --scope "/subscriptions/$SUBID/resourceGroups/$RG/providers/Microsoft.KeyVault/vaults/$KV"
   ```

3. **Use PIM for elevated access** (Owner, Admin):
   ```bash
   # Make group eligible for Owner role (requires approval to activate)
   az rest --method post --uri "https://graph.microsoft.com/v1.0/privilegedIdentityManagement/roleAssignments" \
     --body '{"roleDefinitionId":"'$OWNER_ROLE_ID'","principalId":"'$GROUP_ID'","resourceId":"'$SCOPE'","type":"eligible"}'
   ```

4. **Set up access reviews** (quarterly):
   ```bash
   # Schedule review of all role assignments
   # Portal: Azure AD > Identity Governance > Access Reviews
   # Review: "Do these developers still need this access?"
   ```

### Phase 3: Workload Identity (Managed Identities)

1. **Create managed identity**:
   ```bash
   # System-assigned (tied to one resource)
   az webapp identity assign --resource-group $RG --name $APP_NAME
   
   # User-assigned (reusable across resources)
   az identity create --resource-group $RG --name $IDENTITY_NAME
   ```

2. **Assign minimal roles**:
   ```bash
   # Get managed identity object ID
   PRINCIPAL_ID=$(az identity show --resource-group $RG --name $IDENTITY_NAME --query principalId)
   
   # Grant only Key Vault Secrets User (not full contributor)
   az role assignment create \
     --role "Key Vault Secrets User" \
     --assignee-object-id $PRINCIPAL_ID \
     --scope /subscriptions/$SUBID/resourceGroups/$RG/providers/Microsoft.KeyVault/vaults/$KV
   ```

3. **Use access from app** (no credentials needed):
   ```csharp
   // .NET example: Managed identity token obtained automatically
   var credential = new DefaultAzureCredential();
   var kvClient = new SecretClient(new Uri("https://$KV.vault.azure.net"), credential);
   var secret = await kvClient.GetSecretAsync("MySecret");
   ```

### Phase 4: Custom Roles (Rare)

1. **Create only if no built-in role fits**:
   ```json
   {
     "Name": "Application Configuration Reader",
     "Description": "Read app config but cannot create/delete",
     "Actions": [
       "Microsoft.AppConfiguration/configurationStores/read",
       "Microsoft.AppConfiguration/configurationStores/keyValues/read"
     ],
     "NotActions": [],
     "DataActions": [],
     "AssignableScopes": [
       "/subscriptions/SUBID"
     ]
   }
   ```

2. **Apply custom role**:
   ```bash
   az role definition create --role-definition @custom-role.json
   ```

### Phase 5: Audit & Remediation

1. **List all role assignments**:
   ```bash
   # All assignments in subscription
   az role assignment list --all --output table
   
   # Flag: Owner roles that should be PIM-eligible
   az role assignment list --all --query "[?roleDefinitionName=='Owner']"
   ```

2. **Find overpermissioned identities**:
   ```bash
   # Identities with Contributor (too broad)
   az role assignment list --all --query "[?roleDefinitionName=='Contributor']"
   
   # Action: Replace with scoped, specific roles
   ```

3. **Set up recurring access review**:
   - Quarterly: Does each identity still need this access?
   - Remove: Identities no longer used
   - Reduce: Downgrade Contributor → specific roles

## Output Contract

1. **Access Model Design**
   - Human access via security groups (group IDs, members)
   - Workload access via managed identities (system/user-assigned)
   - Elevated access via PIM (approval workflow)

2. **Role Mapping**
   - Principal → Role → Scope
   - Justification for each assignment
   - Built-in vs. custom rationale

3. **Implementation Plan**
   - CLI/PowerShell commands (ready to copy/paste)
   - Order of operations (dependencies)
   - Validation steps (verify permissions work)

4. **Governance & Audit**
   - Access review cadence (quarterly)
   - Who approves elevated access? (PIM approvers)
   - Audit log destination (Log Analytics workspace)

5. **Migration Path** (if consolidating old assignments)
   - Current state (existing assignments)
   - Target state (new group-based model)
   - Per-user assignments to retire
   - Timeline and testing plan

## Practical Examples

### Example 1: Web App + Managed Identity

**Workload**: ASP.NET app reads secrets from Key Vault, writes logs to Storage

```
1. Create system-assigned managed identity on App Service
2. Assign roles:
   - Key Vault Secrets User (scope: Key Vault)
   - Storage Blob Data Contributor (scope: logs container)
3. In code: new DefaultAzureCredential() fetches token automatically
4. No credentials in config
```

### Example 2: Developer Team with PIM

**Team**: 5 developers need temporary admin access for troubleshooting

```
1. Create "contoso-admins" security group, add developers
2. Make group PIM-eligible for Owner role (approval required)
3. Developer clicks "Activate Role" in portal
4. Admin gets email to approve
5. 4-hour access granted, auto-revokes after
6. Audit trail in Activity Log
```

### Example 3: Service-to-Service Access

**Pattern**: Microservice A calls Microservice B in AKS

```
1. Create user-assigned managed identity "service-a-identity"
2. AKS pod runs with this identity (via workload identity)
3. Service B checks incoming token for identity
4. No secrets, credentials, or connection strings needed
```

## Guardrails

- **Avoid Owner role**: Only use for emergency escalation; make it PIM-eligible with approval.
- **Avoid Contributor role**: Replace with scoped, specific roles (e.g., Storage Blob Data Contributor).
- **Never assign per-user**: Use groups for 3+ users; automate group sync from identity provider.
- **Use managed identities for workloads**: No secrets in config, automatic credential rotation.
- **Scope assignments narrowly**: Assign at resource group, not subscription, when possible.
- **Require MFA for elevated access**: PIM + MFA for Owner, Admin, or sensitive resource roles.
- **Audit quarterly**: Access reviews, remove unused identities, downgrade overpermissioned accounts.
- **Document why**: Each elevated permission must have clear business justification.
