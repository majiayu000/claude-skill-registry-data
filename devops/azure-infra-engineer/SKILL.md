---
name: azure-infra-engineer
description: Azure-specific infrastructure expertise for designing and managing cloud environments. Use when provisioning Azure resources with Bicep or Terraform.
---

# Azure Infrastructure Engineer

Specialized expertise in Microsoft Azure infrastructure design and operations, providing guidance on resource organization, networking, identity management, compute and containers, data services, monitoring, and infrastructure as code using Bicep, Terraform, and Azure CLI.

## When to Use This Skill

Use this skill for:

- Provisioning and managing Azure resources with Bicep or Terraform
- Designing Azure networking topologies (VNets, hub-spoke, Private Endpoints)
- Configuring Azure AD (Entra ID) roles, managed identities, and conditional access
- Deploying and operating AKS clusters and containerized workloads
- Implementing Azure Monitor, Log Analytics, and Application Insights
- Managing Azure storage accounts, databases, and data encryption
- Building CI/CD pipelines for Azure infrastructure deployments
- Applying Azure Policy and governance at scale

**Trigger phrases**: "Azure", "Bicep", "ARM template", "Azure AD", "Entra ID", "AKS", "VNet", "NSG", "Private Endpoint", "Azure Monitor", "Log Analytics", "Azure Policy", "managed identity", "Azure DevOps", "Azure Front Door"

## What This Skill Does

Provides production-ready Azure infrastructure patterns including:

- **Resource Organization**: Management groups, subscriptions, naming conventions, tagging, Azure Policy
- **Networking**: VNets, subnets, NSGs, Azure Firewall, Private Link, peering, Application Gateway
- **Identity and Access**: Entra ID, RBAC, managed identities, service principals, PIM
- **Compute and Containers**: AKS, Container Apps, Azure Functions, VM Scale Sets
- **Data and Storage**: Storage accounts, lifecycle policies, Azure SQL, Cosmos DB, encryption
- **Monitoring**: Azure Monitor, Log Analytics, Application Insights, alerts, workbooks
- **Infrastructure as Code**: Bicep modules, Terraform azurerm, CI/CD pipelines, What-If deployments

## Instructions

### Step 1: Organize Azure Resources with Governance

A well-structured Azure environment begins with a clear hierarchy of management groups, subscriptions, resource groups, and consistent naming and tagging. Azure Policy enforces organizational standards at scale.

**Resource Hierarchy**:

```
Tenant Root Group
├── Platform (Management Group)
│   ├── Identity (Subscription)       → rg-identity-prod
│   ├── Management (Subscription)     → rg-management-prod
│   └── Connectivity (Subscription)   → rg-hub-network-prod, rg-dns-prod
├── Landing Zones (Management Group)
│   ├── Corp    → App Team A (Subscription), App Team B (Subscription)
│   └── Online  → Public Web (Subscription)
└── Sandbox (Management Group)        → Dev/Test (Subscription)
```

**Naming Convention Module (Bicep)**:

```bicep
// naming.bicep - Azure resource naming: {type}-{workload}-{env}-{region}-{instance}
@allowed(['dev', 'staging', 'prod'])
param environment string
param workloadName string
param regionShort string
param instance string = '001'

output resourceGroup string = 'rg-${workloadName}-${environment}-${regionShort}-${instance}'
output vnet string = 'vnet-${workloadName}-${environment}-${regionShort}-${instance}'
output nsg string = 'nsg-${workloadName}-${environment}-${regionShort}'
output aks string = 'aks-${workloadName}-${environment}-${regionShort}-${instance}'
output keyVault string = 'kv-${workloadName}-${environment}-${regionShort}'
output storageAccount string = 'st${workloadName}${environment}${regionShort}'
output logAnalytics string = 'log-${workloadName}-${environment}-${regionShort}'
```

**Tagging Strategy (Terraform)**:

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Workload    = var.workload_name
    CostCenter  = var.cost_center
    Owner       = var.team_email
    ManagedBy   = "terraform"
    Compliance  = var.compliance_level
  }
}
```

**Azure Policy for Governance (Bicep)**:

```bicep
// Require CostCenter tag on resource groups
resource requireTagsPolicy 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'require-cost-center-tag'
  properties: {
    displayName: 'Require CostCenter tag on resource groups'
    policyDefinitionId: '/providers/Microsoft.Authorization/policyDefinitions/96670d01-0a4d-4649-9c89-2d3abc0a5025'
    parameters: { tagName: { value: 'CostCenter' } }
    enforcementMode: 'Default'
  }
}

// Restrict deployments to approved regions
resource allowedLocationsPolicy 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'allowed-locations'
  properties: {
    displayName: 'Restrict resource deployment to approved regions'
    policyDefinitionId: '/providers/Microsoft.Authorization/policyDefinitions/e56962a6-4747-49cd-b67b-bf8b01975c4c'
    parameters: { listOfAllowedLocations: { value: ['westeurope', 'northeurope', 'eastus2'] } }
    enforcementMode: 'Default'
  }
}
```

### Step 2: Design Azure Networking

Azure networking forms the backbone of any cloud deployment. A hub-spoke topology with centralized firewall inspection, private endpoints for PaaS services, and NSG rules enforces defense in depth.

**Hub-Spoke Topology**:

```
                    ┌────────────────────────────┐
                    │      Azure Front Door       │
                    └─────────────┬──────────────┘
                    ┌─────────────▼──────────────┐
                    │   Hub VNet (10.0.0.0/16)    │
                    │  ┌──────────────────────┐   │
                    │  │ Azure Firewall        │   │
                    │  │ VPN/ExpressRoute GW   │   │
                    │  │ Azure Bastion          │   │
                    │  └──────────────────────┘   │
                    └──────┬──────────────┬──────┘
               VNet Peering│              │VNet Peering
          ┌────────────────▼──┐    ┌──────▼───────────────┐
          │ Spoke: Prod        │    │ Spoke: Dev            │
          │ 10.1.0.0/16        │    │ 10.2.0.0/16           │
          │ App / Data / PE    │    │ App / Data             │
          └────────────────────┘    └────────────────────────┘
```

**Hub VNet with Firewall (Bicep)**:

```bicep
resource hubVnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: 'vnet-hub-prod-weu'
  location: location
  properties: {
    addressSpace: { addressPrefixes: ['10.0.0.0/16'] }
    subnets: [
      { name: 'AzureFirewallSubnet', properties: { addressPrefix: '10.0.1.0/24' } }
      { name: 'GatewaySubnet', properties: { addressPrefix: '10.0.2.0/24' } }
      { name: 'AzureBastionSubnet', properties: { addressPrefix: '10.0.3.0/24' } }
    ]
  }
}

resource firewall 'Microsoft.Network/azureFirewalls@2023-09-01' = {
  name: 'fw-hub-prod-weu'
  location: location
  properties: {
    sku: { name: 'AZFW_VNet', tier: 'Premium' }
    ipConfigurations: [{ name: 'fw-ipconfig', properties: {
      subnet: { id: hubVnet.properties.subnets[0].id }
      publicIPAddress: { id: firewallPublicIp.id }
    }}]
    firewallPolicy: { id: firewallPolicy.id }
  }
}
```

**NSG and Private Endpoint (Terraform)**:

```hcl
resource "azurerm_network_security_group" "app" {
  name                = "nsg-app-prod-weu"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowAppGatewayInbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "10.0.4.0/24"
    destination_address_prefix = "*"
  }
  security_rule {
    name = "DenyAllInbound"
    priority = 4096; direction = "Inbound"; access = "Deny"
    protocol = "*"; source_port_range = "*"; destination_port_range = "*"
    source_address_prefix = "*"; destination_address_prefix = "*"
  }
  tags = local.common_tags
}

resource "azurerm_private_endpoint" "sql" {
  name                = "pe-sql-prod-weu"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "psc-sql-prod"
    private_connection_resource_id = azurerm_mssql_server.main.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }
  private_dns_zone_group {
    name                 = "pdz-sql"
    private_dns_zone_ids = [azurerm_private_dns_zone.sql.id]
  }
}
```

**VNet Peering (Azure CLI)**:

```bash
az network vnet peering create \
  --name "hub-to-spoke-prod" --resource-group "rg-hub-network-prod" \
  --vnet-name "vnet-hub-prod-weu" \
  --remote-vnet "/subscriptions/$SPOKE_SUB_ID/resourceGroups/rg-app-prod/providers/Microsoft.Network/virtualNetworks/vnet-app-prod-weu" \
  --allow-vnet-access --allow-forwarded-traffic --allow-gateway-transit
```

### Step 3: Configure Identity and Access Management

Azure identity management centers on Entra ID (formerly Azure AD), RBAC role assignments, managed identities for workloads, and Privileged Identity Management for just-in-time access. Always prefer managed identities over service principal secrets.

**RBAC Role Assignments (Bicep)**:

```bicep
var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'
var kvSecretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'

resource acrPullAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, principalId, acrPullRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

**Managed Identity with Role Grants (Terraform)**:

```hcl
resource "azurerm_user_assigned_identity" "app" {
  name                = "id-app-prod-weu"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "app_kv_secrets" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

resource "azurerm_role_assignment" "app_storage_blob" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

**Federated Credentials for GitHub Actions (Azure CLI)**:

```bash
az ad app create --display-name "sp-github-deploy-prod"
APP_ID=$(az ad app list --display-name "sp-github-deploy-prod" --query "[0].appId" -o tsv)
az ad sp create --id "$APP_ID"

az ad app federated-credential create --id "$APP_ID" --parameters '{
  "name": "github-actions-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:myorg/myrepo:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

az role assignment create --assignee "$APP_ID" --role "Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/rg-app-prod"
```

**Conditional Access and PIM Best Practices**:

| Control | Recommendation |
|---------|---------------|
| **MFA Enforcement** | Require MFA for all users accessing Azure Portal and CLI |
| **Device Compliance** | Require compliant or hybrid-joined devices for admin access |
| **PIM Activation** | Require justification and approval for Owner/Contributor roles |
| **PIM Duration** | Set maximum activation to 4 hours for privileged roles |
| **Access Reviews** | Run quarterly reviews on all custom role assignments |
| **Break-Glass Accounts** | Maintain two cloud-only emergency accounts excluded from conditional access |

### Step 4: Deploy Compute and Container Workloads

Azure provides compute options from fully managed serverless (Functions, Container Apps) to orchestrated containers (AKS) and traditional VMs. Choose based on control, scale, and operational overhead requirements.

**AKS Cluster with Node Pools (Bicep)**:

```bicep
resource aks 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: 'aks-app-prod-weu-001'
  location: location
  identity: { type: 'UserAssigned', userAssignedIdentities: { '${managedIdentity.id}': {} } }
  properties: {
    kubernetesVersion: '1.29'
    dnsPrefix: 'aks-app-prod'
    networkProfile: {
      networkPlugin: 'azure'; networkPolicy: 'calico'
      serviceCidr: '172.16.0.0/16'; dnsServiceIP: '172.16.0.10'
    }
    agentPoolProfiles: [
      {
        name: 'system'; count: 3; vmSize: 'Standard_D4s_v5'; mode: 'System'
        availabilityZones: ['1', '2', '3']; vnetSubnetID: aksSubnet.id
        enableAutoScaling: true; minCount: 3; maxCount: 5
        nodeTaints: ['CriticalAddonsOnly=true:NoSchedule']
      }
      {
        name: 'apppool'; count: 3; vmSize: 'Standard_D8s_v5'; mode: 'User'
        availabilityZones: ['1', '2', '3']; vnetSubnetID: aksSubnet.id
        enableAutoScaling: true; minCount: 3; maxCount: 20
        nodeLabels: { workload: 'application' }
      }
      {
        name: 'spotpool'; count: 0; vmSize: 'Standard_D8s_v5'; mode: 'User'
        scaleSetPriority: 'Spot'; spotMaxPrice: -1; scaleSetEvictionPolicy: 'Delete'
        vnetSubnetID: aksSubnet.id; enableAutoScaling: true; minCount: 0; maxCount: 10
        nodeTaints: ['kubernetes.azure.com/scalesetpriority=spot:NoSchedule']
      }
    ]
    addonProfiles: {
      azureKeyvaultSecretsProvider: { enabled: true, config: { enableSecretRotation: 'true' } }
      omsagent: { enabled: true, config: { logAnalyticsWorkspaceResourceID: logAnalytics.id } }
    }
    securityProfile: { workloadIdentity: { enabled: true } }
    autoUpgradeProfile: { upgradeChannel: 'stable' }
    oidcIssuerProfile: { enabled: true }
  }
}
```

**Azure Container Apps (Terraform)**:

```hcl
resource "azurerm_container_app" "api" {
  name                         = "ca-api-prod"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Multiple"

  identity { type = "UserAssigned"; identity_ids = [azurerm_user_assigned_identity.app.id] }

  template {
    min_replicas = 2; max_replicas = 10
    container {
      name = "api"; image = "${azurerm_container_registry.main.login_server}/api:latest"
      cpu = 1.0; memory = "2Gi"
      env { name = "AZURE_CLIENT_ID"; value = azurerm_user_assigned_identity.app.client_id }
      liveness_probe  { transport = "HTTP"; path = "/healthz"; port = 8080 }
      readiness_probe { transport = "HTTP"; path = "/ready"; port = 8080 }
    }
    custom_scale_rule {
      name = "http-scaling"; custom_rule_type = "http"
      metadata = { concurrentRequests = "50" }
    }
  }
  ingress { external_enabled = true; target_port = 8080; transport = "http" }
}
```

### Step 5: Manage Data and Storage Services

Azure data services span blob storage, relational databases, NoSQL, and caching. Use lifecycle policies to optimize storage costs, private endpoints to secure data access, and encryption with customer-managed keys for compliance.

**Storage Account with Lifecycle Policy (Bicep)**:

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stapprodweu001'
  location: location
  sku: { name: 'Standard_ZRS' }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    networkAcls: { defaultAction: 'Deny', bypass: 'AzureServices' }
  }
}

resource lifecyclePolicy 'Microsoft.Storage/storageAccounts/managementPolicies@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: { policy: { rules: [{
    name: 'archive-old-blobs'; type: 'Lifecycle'
    definition: {
      filters: { blobTypes: ['blockBlob'], prefixMatch: ['data/'] }
      actions: { baseBlob: {
        tierToCool: { daysAfterModificationGreaterThan: 30 }
        tierToArchive: { daysAfterModificationGreaterThan: 90 }
        delete: { daysAfterModificationGreaterThan: 2555 }
      }}
    }
  }]}}
}
```

**Azure SQL with Failover Group (Terraform)**:

```hcl
resource "azurerm_mssql_server" "primary" {
  name                         = "sql-app-prod-weu"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = "westeurope"
  version                      = "12.0"
  minimum_tls_version          = "1.2"
  azuread_administrator {
    login_username = "AzureAD Admin"
    object_id      = var.aad_admin_object_id
  }
  identity { type = "SystemAssigned" }
}

resource "azurerm_mssql_database" "main" {
  name      = "sqldb-app-prod"
  server_id = azurerm_mssql_server.primary.id
  sku_name  = "GP_Gen5_4"
  zone_redundant = true
  transparent_data_encryption_key_vault_key_id = azurerm_key_vault_key.sql_tde.id

  short_term_retention_policy { retention_days = 14; backup_interval_in_hours = 12 }
  long_term_retention_policy {
    weekly_retention = "P4W"; monthly_retention = "P12M"
    yearly_retention = "P5Y"; week_of_year = 1
  }
}

resource "azurerm_mssql_failover_group" "main" {
  name      = "fog-app-prod"
  server_id = azurerm_mssql_server.primary.id
  databases = [azurerm_mssql_database.main.id]
  partner_server { id = azurerm_mssql_server.secondary.id }
  read_write_endpoint_failover_policy { mode = "Automatic"; grace_minutes = 60 }
}
```

**Cosmos DB Partition Strategy (Bicep)**:

```bicep
resource ordersContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-11-15' = {
  parent: database
  name: 'orders'
  properties: { resource: {
    id: 'orders'
    partitionKey: { paths: ['/customerId'], kind: 'Hash', version: 2 }
    indexingPolicy: {
      indexingMode: 'consistent'
      includedPaths: [{ path: '/orderDate/?' }, { path: '/status/?' }]
      excludedPaths: [{ path: '/orderDetails/*' }, { path: '/"_etag"/?' }]
      compositeIndexes: [[
        { path: '/customerId', order: 'ascending' }
        { path: '/orderDate', order: 'descending' }
      ]]
    }
    defaultTtl: 7776000
  }}
}
```

### Step 6: Implement Monitoring and Observability

Azure Monitor, Log Analytics, and Application Insights form the core observability stack. Configure diagnostic settings on every resource, centralize logs in a Log Analytics workspace, and create actionable alerts with well-defined action groups.

**Log Analytics and Application Insights (Bicep)**:

```bicep
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-app-prod-weu'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 90
    workspaceCapping: { dailyQuotaGb: 10 }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-app-prod-weu'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

// Enable diagnostic settings on Key Vault (repeat pattern for all resources)
resource kvDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-kv-to-law'
  scope: keyVault
  properties: {
    workspaceId: logAnalytics.id
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}
```

**Alert Rules and Action Groups (Terraform)**:

```hcl
resource "azurerm_monitor_action_group" "critical" {
  name = "ag-critical-prod"; resource_group_name = azurerm_resource_group.main.name
  short_name = "critical"
  email_receiver { name = "oncall-team"; email_address = "oncall@company.com" }
  webhook_receiver { name = "pagerduty"; service_uri = var.pagerduty_webhook_url }
}

resource "azurerm_monitor_metric_alert" "aks_cpu" {
  name                = "alert-aks-cpu-high"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_kubernetes_cluster.main.id]
  severity = 2; frequency = "PT1M"; window_size = "PT5M"
  criteria {
    metric_namespace = "Insights.Container/nodes"
    metric_name      = "cpuUsagePercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 85
  }
  action { action_group_id = azurerm_monitor_action_group.critical.id }
}
```

**Useful KQL Queries for Workbooks**:

```kusto
// AKS pod restarts (last 24h)
KubePodInventory
| where TimeGenerated > ago(24h) and PodRestartCount > 0
| summarize TotalRestarts = sum(PodRestartCount) by Namespace, Name
| order by TotalRestarts desc | take 20

// Application Insights: slow requests (p95 > 2s)
requests
| where timestamp > ago(1h)
| summarize p95 = percentile(duration, 95), count() by operation_Name
| where p95 > 2000 | order by p95 desc

// Failed Entra ID sign-ins
SigninLogs
| where TimeGenerated > ago(24h) and ResultType != "0"
| summarize Failures = count() by UserPrincipalName, ResultType, ResultDescription
| order by Failures desc | take 25
```

### Step 7: Implement Infrastructure as Code Pipelines

Use Bicep modules or Terraform with the azurerm provider for declarative infrastructure. Integrate What-If (Bicep) or plan (Terraform) steps into CI/CD pipelines for safe, reviewable deployments. Manage Terraform state in Azure Storage with locking via blob lease.

**Bicep Module Structure**:

```
infra/
├── main.bicep
├── modules/
│   ├── networking/   (vnet.bicep, nsg.bicep, private-endpoint.bicep)
│   ├── compute/      (aks.bicep, container-app.bicep)
│   ├── data/         (sql.bicep, cosmos.bicep, storage.bicep)
│   ├── identity/     (managed-identity.bicep, role-assignment.bicep)
│   └── monitoring/   (log-analytics.bicep, alerts.bicep)
└── environments/     (dev.bicepparam, staging.bicepparam, prod.bicepparam)
```

**Terraform State Backend**:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstateprod"
    container_name       = "tfstate"
    key                  = "app-prod.tfstate"
    use_oidc             = true
  }
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.85" }
  }
}

provider "azurerm" {
  features {
    key_vault { purge_soft_delete_on_destroy = false }
    resource_group { prevent_deletion_if_contains_resources = true }
  }
  use_oidc = true
}
```

**GitHub Actions for Bicep (What-If on PR, deploy on merge)**:

```yaml
name: Deploy Azure Infrastructure
on:
  push: { branches: [main], paths: ['infra/**'] }
  pull_request: { branches: [main], paths: ['infra/**'] }
permissions: { id-token: write, contents: read, pull-requests: write }

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      - run: az bicep build --file infra/main.bicep
      - if: github.event_name == 'pull_request'
        run: az deployment sub what-if --location westeurope --template-file infra/main.bicep --parameters infra/environments/prod.bicepparam

  deploy:
    needs: validate
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      - run: az deployment sub create --location westeurope --template-file infra/main.bicep --parameters infra/environments/prod.bicepparam --name "deploy-$(date +%Y%m%d-%H%M%S)"
```

## Best Practices

- **Use managed identities everywhere** instead of storing credentials; eliminate service principal secrets wherever possible
- **Enable Private Endpoints** for all PaaS services (Storage, SQL, Key Vault, ACR) and disable public network access
- **Deploy across availability zones** for all production workloads to survive datacenter failures
- **Apply Azure Policy at the management group level** to enforce governance consistently across all subscriptions
- **Tag every resource** with at minimum: Environment, Workload, CostCenter, Owner, and ManagedBy
- **Use What-If or terraform plan** before every deployment to preview changes and catch drift
- **Centralize logs** in a single Log Analytics workspace per environment with diagnostic settings on every resource
- **Enable soft delete and purge protection** on Key Vault and Storage accounts to prevent accidental data loss
- **Run Azure Advisor and Defender for Cloud** recommendations regularly to maintain security posture and optimize costs

## Quality Checklist

- [ ] Management group hierarchy follows Azure Landing Zone patterns
- [ ] Naming convention applied consistently across all resources
- [ ] Required tags enforced via Azure Policy
- [ ] Hub-spoke networking topology deployed with NSGs on every subnet
- [ ] Private Endpoints configured for all PaaS services
- [ ] Managed identities used instead of service principal secrets
- [ ] RBAC follows least-privilege with no Owner at subscription level
- [ ] AKS uses workload identity and Defender for Containers
- [ ] Storage accounts deny public access and enforce TLS 1.2
- [ ] Diagnostic settings enabled on all resources pointing to Log Analytics
- [ ] Alert rules configured for critical metrics with action groups
- [ ] Infrastructure defined in Bicep or Terraform with CI/CD pipeline
- [ ] What-If or plan step runs on every pull request

## Related Skills

- `cloud-architect` - Multi-cloud architecture patterns and Well-Architected Framework
- `terraform-specialist` - Advanced Terraform patterns and module design
- `kubernetes-expert` - Kubernetes workload design and operations
- `cicd-architect` - CI/CD pipeline design and deployment strategies
- `security-review` - Security assessment and compliance review

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Azure Well-Architected Framework, Azure Landing Zones, Cloud Adoption Framework


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
