---
name: azure-storage
description: >
  Design and operate Azure Storage services for durability, performance, and secure access.
  Use this skill when users ask about Blob, Files, Queues, Tables, or Data Lake storage patterns.
  Covers redundancy, tiering, access models, lifecycle policies, and compliance.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [well-architected]
  storage: [blob, files, queues, tables, adls]
---

# Azure Storage

Select and configure Azure storage with optimal redundancy, performance tiering, and access controls.
Balance cost, durability, latency, and compliance requirements.

## Use This Skill When

- The user needs file, object, or queue storage in Azure
- The user needs lifecycle, replication, or retention policy design
- The user needs secure access model for storage workloads
- The user wants to optimize storage costs while maintaining SLA

## Context: Storage Maturity

**Immature**: Hot tier only, public access, no lifecycle, account key auth  
**Developing**: Correct tiering, RBAC, some lifecycle rules  
**Managed**: LRS for dev, GRS for prod, managed identity auth, lifecycle to cool/archive → **Target**  
**Optimized**: Geo-redundant reads, tiered access based on traffic, real-time cost optimization

## Required Inputs

- **Data type**: Documents, logs, video, database backups, transactional
- **Access pattern**: Frequent (hot), occasional (cool), rare (archive), cold
- **Size & growth**: 10GB initial, 10% monthly growth? Or 1TB spike?
- **Latency requirement**: <100ms or batch-oriented?
- **Durability**: RPO/RTO targets? Geographic redundancy needed?
- **Access model**: Public, private, user-scoped, application-only?
- **Compliance**: Data residency, encryption, retention, audit requirements?
- **Budget**: Cost-driven or performance-driven?

## Decision Tree

```
What type of data needs storage?
├─ Unstructured files (docs, images, video) → Blob Storage
├─ Shared file system (SMB/NFS for apps) → Azure Files
├─ Message queue → Queue Storage
├─ NoSQL key-value → Table Storage
├─ Big data analytics → Data Lake Storage
└─ Structured relational → SQL Database (not storage)

How frequently is this data accessed?
├─ Daily (hot, <1 day SLA) → Hot tier ($0.012/GB/month)
├─ Weekly-monthly (cool, <30 day SLA) → Cool tier ($0.001/GB/month)
├─ Rarely, compliance hold (archive, <90 day SLA) → Archive tier ($0.0004/GB/month)
└─ Cold (7+ year retention) → Cold tier ($0.00099/GB/month)

Do you need geographic failover?
├─ Single region (dev/test) → LRS (locally redundant, cheapest, 11x durability)
├─ Single region + replication → ZRS (zone redundant, same-region HA)
├─ Multi-region failover → GRS (geo-redundant, read from secondary)
└─ Multi-region read (active-active) → RA-GRS (read-access geo-redundant)

How should apps access storage?
├─ Internal/private → Private endpoints, firewall rules
├─ Managed identity → System/user-assigned identity with role
├─ Public but controlled → SAS tokens (time-bound, scoped)
└─ Public read-only → Blob public access (for content CDN)
```

## Workflow

### Phase 1: Choose Storage Type & Account

1. **Create storage account**:
   ```bash
   az storage account create \
     --resource-group $RG \
     --name "st${app}${env}" \
     --location eastus \
     --kind StorageV2 \
     --sku Standard_GRS \
     --access-tier Hot \
     --https-only \
     --default-action Deny
   ```

2. **Configure networking** (private by default):
   ```bash
   # Block all public access
   az storage account update \
     --resource-group $RG \
     --name "st${app}${env}" \
     --public-network-access-enabled false
   
   # Or allow only specific IPs/VNets
   az storage account network-rule add \
     --resource-group $RG \
     --account-name "st${app}${env}" \
     --vnet-name $VNET \
     --subnet-name $SUBNET
   ```

3. **Enable encryption** (at-rest, in-transit):
   ```bash
   # HTTPS only (enforced above)
   # At-rest: Default Microsoft-managed keys OR customer-managed key (CMK)
   
   # Use CMK from Key Vault for sensitive data
   az storage account update \
     --resource-group $RG \
     --name "st${app}${env}" \
     --encryption-key-name "storage-cmk" \
     --encryption-key-vault $KV_ID
   ```

### Phase 2: Create Containers/Shares & Set Tiering

1. **For Blob Storage**:
   ```bash
   # Create container
   az storage container create \
     --account-name "st${app}${env}" \
     --name "documents" \
     --public-access off
   
   # Or create via Python/C#
   # container_client = blob_client.create_container(name="documents")
   ```

2. **Set access tier** (per blob or policy-driven):
   ```bash
   # Set individual blob to cool tier
   az storage blob update \
     --account-name "st${app}${env}" \
     --container-name "documents" \
     --name "old-file.pdf" \
     --access-tier Cool
   ```

3. **For Azure Files**:
   ```bash
   # Create file share
   az storage share create \
     --account-name "st${app}${env}" \
     --name "shared-files"
   
   # Create subdirectories
   az storage directory create \
     --account-name "st${app}${env}" \
     --share-name "shared-files" \
     --name "projects/2024"
   ```

### Phase 3: Configure Access Controls

1. **Using managed identity** (preferred):
   ```bash
   # App Service or AKS pod runs with managed identity
   # Assign role to identity
   PRINCIPAL_ID=$(az identity show --resource-group $RG --name $IDENTITY --query principalId -o tsv)
   
   az role assignment create \
     --role "Storage Blob Data Contributor" \
     --assignee-object-id $PRINCIPAL_ID \
     --scope "/subscriptions/$SUBID/resourceGroups/$RG/providers/Microsoft.Storage/storageAccounts/st${app}${env}"
   
   # In code: DefaultAzureCredential() fetches token automatically
   ```

2. **Using SAS tokens** (time-bound, scoped):
   ```bash
   # Generate SAS token (expires in 1 hour)
   EXPIRY=$(date -u -d "+1 hour" +%Y-%m-%dT%H:%M:%SZ)
   
   az storage blob generate-sas \
     --account-name "st${app}${env}" \
     --container-name "documents" \
     --name "file.pdf" \
     --permissions r \
     --expiry $EXPIRY
   
   # Give user time-limited URL: https://storage.../file.pdf?sv=...&sig=...
   ```

3. **Using account key** (not recommended for production):
   ```bash
   # Get account key
   KEY=$(az storage account keys list --resource-group $RG --account-name "st${app}${env}" --query "[0].value" -o tsv)
   
   # Connection string for legacy code
   CS="DefaultEndpointsProtocol=https;AccountName=st${app}${env};AccountKey=$KEY;EndpointSuffix=core.windows.net"
   
   # Store in Key Vault
   az keyvault secret set --vault-name $KV --name "storage-connection-string" --value "$CS"
   ```

### Phase 4: Lifecycle Management

1. **Create tiering policy**:
   ```json
   {
     "rules": [
       {
         "name": "auto-cool",
         "enabled": true,
         "type": "Lifecycle",
         "definition": {
           "filters": {
             "blobTypes": ["blockBlob"],
             "prefixMatch": ["logs/"]
           },
           "actions": {
             "baseBlob": {
               "tierToCool": { "daysAfterModificationGreaterThan": 30 },
               "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
               "delete": { "daysAfterModificationGreaterThan": 365 }
             }
           }
         }
       }
     ]
   }
   ```

   ```bash
   # Apply policy
   az storage account management-policy create \
     --account-name "st${app}${env}" \
     --resource-group $RG \
     --policy @lifecycle.json
   ```

2. **Cost impact**:
   ```
   Hot tier: $0.012/GB/month
   Cool tier: $0.001/GB/month (83% savings)
   Archive: $0.0004/GB/month (97% savings)
   
   But: Archive = 4-hour retrieval, deletion costs per GB
   Example: 1TB logs → Hot $12/month → Archive $0.40/month (97% savings)
   ```

### Phase 5: Backup & Retention

1. **Enable soft delete** (recover deleted blobs):
   ```bash
   az storage account blob-service-properties update \
     --account-name "st${app}${env}" \
     --enable-delete-retention true \
     --delete-retention-days 7
   ```

2. **Enable versioning** (keep blob history):
   ```bash
   az storage account blob-service-properties update \
     --account-name "st${app}${env}" \
     --enable-versioning
   
   # Now each write creates a new version
   # Old versions kept until lifecycle policy deletes them
   ```

3. **Immutable policy** (WORM - write once, read many, for compliance):
   ```bash
   # Set time-based retention
   az storage blob properties update \
     --account-name "st${app}${env}" \
     --container-name "compliance" \
     --name "audit.log" \
     --set properties.immutabilityPolicy={expirationTime:\"2025-12-31T23:59:59Z\",policyMode:\"Locked\"}
   
   # Blob cannot be deleted or modified until expiration
   ```

### Phase 6: Monitoring & Alerting

1. **Enable metrics & logging**:
   ```bash
   az storage logging update \
     --account-name "st${app}${env}" \
     --services b \
     --log rwd \
     --retention-days 30
   ```

2. **Set alerts**:
   - Capacity > 80% of account quota
   - Throttling (requests > per-second limit)
   - Unusual deletion patterns
   - Unauthorized access attempts

## Output Contract

1. **Storage Design**
   - Type selected (Blob, Files, Queues, ADLS) and justification
   - Account creation commands
   - Redundancy model (LRS, ZRS, GRS) and failover strategy

2. **Security & Access**
   - Auth method (managed identity, SAS, keys) recommended
   - Network isolation (private endpoints, firewalls)
   - Encryption: at-rest (CMK or Microsoft-managed), in-transit (HTTPS)

3. **Performance & Tiering**
   - Access tier choices (Hot/Cool/Archive/Cold)
   - Lifecycle policy (automatic tiering rules)
   - Cost estimation (hot vs. tiered vs. archive)

4. **Backup & Retention**
   - Soft delete enabled? Versioning? Immutable retention?
   - Lifecycle deletion policy
   - RTO/RPO (can geo-failover if GRS)

5. **Operational Checklist**
   - Monitoring enabled (metrics, logging)
   - Alert thresholds set
   - Cost optimization review cadence (quarterly)

## Guardrails

- **Prefer managed identity**: No secrets in code; DefaultAzureCredential() handles token.
- **Deny public access by default**: Only allow explicit access (IP, VNet, SAS).
- **Use lifecycle policies**: Automatically move cold data to cheaper tiers; avoid manual re-tiering.
- **Enable soft delete**: Protects against accidental deletion; costs minimal.
- **For compliance: Use immutable policies**: Write-once-read-many (WORM) for audit logs.
- **Monitor for throttling**: If sustained >20,000 req/sec, consider sharding (multiple accounts).
- **Audit access**: Enable logging and monitor unexpected access patterns.
- **Encrypt sensitive data**: Use customer-managed keys (CMK) for highly regulated workloads.
