---
name: azure-quotas
description: >
  Assess and manage Azure service quotas and limits to prevent deployment and scaling failures.
  Use this skill when users ask about quota errors, capacity planning, regional availability, or resource limits.
compatibility:
  models: [any-llm]
  cloud: azure
  tags: [capacity, limits, planning, troubleshooting]
---

# Azure Quotas

Plan quota headroom early so deployments and scale events do not fail unexpectedly.
Identify bottlenecks before they become crises.

## Use This Skill When

- The user sees quota or capacity errors in Azure (DeploymentQuotaExceeded, etc.)
- The user plans a new deployment in a constrained region or subscription
- The user needs preflight checks before scaling operations
- The user wants to verify available capacity before committing to architecture

## Context: Quota Management Maturity

**Immature**: Hit quota limits unexpectedly, manual increases, no planning  
**Developing**: Track some quotas, request increases reactively  
**Managed**: Automated quota tracking, capacity planning, reserved capacity → **Target**  
**Optimized**: Predictive quota management, auto-scaling to new regions, zero surprises

## Required Inputs

- **Subscription ID & region**: Where are you deploying?
- **Planned resources**: How many VMs? App Services? SQL databases?
- **Scale targets**: Current vs. planned capacity?
- **Timeline**: Immediate (next week)? Next quarter? Next year?
- **Compliance**: Any data residency or region-specific needs?

## Decision Tree

```
Where does this workload run?
├─ Single region (lowest complexity)
│  └─ Can fall back to alternative region if quota exceeded?
├─ Multi-region (higher complexity, but better resilience)
│  └─ Distribute across regions to avoid single-region limits
└─ Hybrid (on-premises + Azure)
   └─ Plan data transfer, bandwidth quotas

What's the expected scale?
├─ Small (< 10 VMs, < 100 GB data)
│  └─ Quota rarely an issue
├─ Medium (10-100 VMs, 100 GB - 1 TB data)
│  └─ Plan quotas for compute tier
└─ Large (> 100 VMs, > 1 TB data)
   └─ Request increases in advance, plan multi-region

Are quotas the risk, or SKU availability?
├─ Quota (limit per subscription) → Request increase
├─ SKU availability (no machines available) → Fallback to alternative SKU or region
└─ Cost (exceeding budget) → Use Reserved Instances to cap costs
```

## Workflow

### Phase 1: Identify Quota-Limited Services

1. **Compute quotas** (most common bottleneck):
   ```bash
   # Check vCPU quotas by family
   az vm list-usage --location "eastus" -o table
   
   # Output
   Name                       CurrentValue    Limit
   Standard D Family vCPUs    10              20    ← Can add 10 more
   Standard B Family vCPUs    5               20    ← Plenty available
   Standard E Family vCPUs    0               20    ← None used yet
   ```

2. **Storage quotas**:
   ```bash
   # Get current storage account usage
   az storage account list --query "[].{name:name, tier:sku.name, kind:kind}" -o table
   
   # Limit: 250 storage accounts per subscription
   # Each can be up to 5PB (petabytes)
   ```

3. **Database quotas**:
   ```bash
   # SQL Server quota (per region, per subscription)
   az sql server list --query "[].{name:name, region:location}" -o table
   
   # Limit: 15 servers per subscription, per region
   ```

4. **Networking quotas**:
   ```
   Network Security Groups: 100 per region
   VNets: 100 per subscription
   Public IPs: 60 per region
   Load Balancers: 1 per region (basic), 100 (standard)
   Application Gateways: 20 per subscription
   ```

5. **Other quota-limited services**:
   ```
   App Service Plans: 100 per resource group
   Batch Accounts: 1-3 per region
   Cognitive Services: Varies by service (Speech, Vision, etc.)
   Media Services: Limited slots per subscription
   Redis Cache: 50 per subscription
   Search Services: 15 per subscription
   ```

### Phase 2: Check Current Usage vs. Limits

1. **Get quota status**:
   ```bash
   # All quotas for a region
   az provider show --namespace Microsoft.Compute \
     --query "resourceTypes[?resourceType=='virtualMachines'].limits" -o table
   
   # Output
   limitName                  limitValue
   vCpuCountPerRegion         20
   vCpuCountPerVmFamily       20
   standardBFamilyvCpusCount  20
   standardDFamilyvCpusCount  20
   ```

2. **Calculate usage**:
   ```bash
   # Count running VMs and vCPUs
   az vm list --query "[] | length(@)" -o json  → 8 VMs
   az vm list --query "sum(hardwareProfile.vmSize)" → 24 vCPUs
   
   # Available headroom
   Quota: 20 vCPUs
   Used: 24 vCPUs ← OVER QUOTA!
   Available: -4 ← Must request increase
   ```

3. **Regional availability**:
   ```bash
   # Check which regions have which SKUs available
   az vm list-skus --location "eastus" --resource-type virtualMachines \
     --query "[?name=='Standard_D4s_v3'].restrictions[].restrictionInfo" -o table
   
   # If no restrictions shown, SKU available in that region
   ```

### Phase 3: Request Quota Increases

1. **Request vCPU increase** (most common):
   ```bash
   # Using Azure Portal or CLI
   az provider register --namespace Microsoft.Capacity
   
   # Submit request
   az rest --method post \
     --uri "https://management.azure.com/subscriptions/$SUBID/providers/Microsoft.Capacity/quotaRequests?api-version=2021-12-01" \
     --body '{
       "sku": { "name": "StandardDFamily" },
       "properties": {
         "quotaIncreaseAmount": 20
       }
     }'
   ```

2. **Timeline for approval**:
   ```
   vCPU quota increases:
   ├─ Low demand regions (< 10 vCPU increase) → Auto-approved, 5 minutes
   ├─ Medium increase (10-50 vCPU) → Reviewed, 1-2 business days
   ├─ Large increase (> 50 vCPU) → Manual review, 3-5 business days
   └─ Regional capacity issues → May be denied or partially approved
   ```

3. **What if denied?**
   ```
   ├─ Fallback to alternative SKU (larger memory, different vCPU count)
   ├─ Deploy to different region (check availability first)
   ├─ Use spot VMs (temporary, interruptible, no quota cost)
   └─ Scale sequentially instead of all at once
   ```

### Phase 4: Capacity Planning

1. **Forecast future needs**:
   ```
   Current state (baseline):
   ├─ VMs: 5 × D4s_v3 (32 vCPUs)
   ├─ Target SLA: 99.9% uptime
   └─ Growth: 20% year-over-year
   
   Planned expansion (6 months):
   ├─ Add new customer segment: +8 VMs (64 vCPUs)
   ├─ High-availability zones: Need redundant instances
   └─ Total needed: 96 vCPUs (3× current)
   
   Recommendation:
   └─ Request 120 vCPU quota now (headroom for spikes)
   ```

2. **Design for quota resilience**:
   ```
   Option 1: Single region (simpler, quota-constrained)
   ├─ All VMs in eastus
   ├─ If quota exhausted, deployment fails
   ├─ RTO: Long (manual intervention needed)
   
   Option 2: Multi-region (resilient, but complex)
   ├─ Primary: eastus (60% of VMs)
   ├─ Secondary: westus2 (40% of VMs)
   ├─ If eastus quota full, auto-failover to westus2
   ├─ RTO: Seconds (auto-failover)
   ```

3. **Reserved capacity** (guaranteed slots):
   ```bash
   # Reserve vCPU capacity for 1-3 year term
   # Cost: 30-50% savings vs. on-demand
   # Benefit: Guaranteed availability, no quota issues
   
   # Example: 96 vCPU (24 × D4s_v3 for 3 years)
   Cost on-demand: ~$3,500/month = $126K/year
   Cost reserved: ~$1,750/month (50% off) = $63K/year
   Savings: $63K/year over 3 years
   ```

### Phase 5: Pre-Deployment Validation

1. **Quota checklist before major deployments**:
   ```
   Deployment: Production migration (100 VMs, 400 vCPUs)
   
   ✓ vCPU quota: 500 available, need 400 → OK
   ✓ Storage accounts: 10 used, limit 250 → OK
   ✓ SQL Servers: 2 used, limit 15 → OK
   ✓ App Service Plans: 8 used, limit 100 → OK
   ✓ Public IPs: 12 used, limit 60 → OK
   ✓ NSGs: 25 used, limit 100 → OK
   
   ✓ Regional availability: Standard_D4s_v3 in eastus → OK
   ✓ Fallback region: westus2 has same SKU available → OK
   
   Status: GREEN - Ready to deploy
   ```

2. **Quota monitoring during scale**:
   ```bash
   # Set alert for quota usage
   az monitor metrics alert create \
     --name "cpu-quota-warning" \
     --resource-group $RG \
     --scopes "/subscriptions/$SUBID" \
     --condition "total ComputeQuotaUsage >= 80" \
     --window-size "PT15M" \
     --evaluation-frequency "PT5M" \
     --actions email_action "ops@company.com"
   ```

### Phase 6: Handle Quota Errors

1. **Common errors & solutions**:
   ```
   Error: DeploymentQuotaExceeded
   ├─ Cause: vCPU quota exhausted
   ├─ Solution: Request increase or deploy to alternate region
   
   Error: SkuNotAvailable
   ├─ Cause: SKU not available in chosen region
   ├─ Solution: Use different region, different SKU, or spot VMs
   
   Error: ResourceQuotaExceeded (non-compute)
   ├─ Cause: Limit on databases, storage accounts, etc.
   ├─ Solution: Check specific service quotas, request if needed
   ```

2. **Workarounds for immediate needs**:
   ```
   If quota exceeded AND request takes days:
   
   Option 1: Use Spot VMs (low-cost, interruptible)
   ├─ Immediately available (no quota)
   ├─ 70-90% cost savings
   ├─ Risk: Can be evicted (5-30 min notice)
   └─ Use for: Non-critical workloads, batch jobs, auto-scale
   
   Option 2: Fallback to different region
   ├─ Check alternate region quota (often more available)
   ├─ Deploy there temporarily
   ├─ Risk: Higher latency, data residency may not apply
   
   Option 3: Downsize temporary
   ├─ Use smaller VMs to fit current quota
   ├─ Scale up later when quota increase approved
   ├─ Risk: Performance impact during wait
   ```

## Output Contract

1. **Current Quota Status**
   - Quotas per service (compute, storage, database, networking)
   - Current usage vs. limit
   - Headroom available

2. **Capacity Assessment**
   - Can planned workload fit in current quotas?
   - What quotas need increases?
   - Timeline for requests

3. **Risk Analysis**
   - Single point of quota failure?
   - Regional availability constraints?
   - Fallback regions and their quotas?

4. **Recommendations**
   - Increase requests (which, how much, when?)
   - Architectural changes (multi-region, different SKU)?
   - Reserved capacity (cost savings)?

5. **Pre-Deployment Checklist**
   - All quotas sufficient? (Yes/No)
   - Fallback strategy documented?
   - Monitoring alerts configured?

## Guardrails

- **Always check quotas before major deployments**: Don't discover limits mid-cutover.
- **Request increases in advance**: Lead time can be days; don't wait until needed.
- **Verify SKU availability by region**: Not all sizes available everywhere.
- **Plan multi-region for resilience**: Single-region is quota-constrained and brittle.
- **Monitor quota usage**: Set alerts at 70% to plan proactively.
- **Document quota-critical paths**: Identify which failures are quota-related vs. other issues.
- **Test fallback regions**: Ensure workload actually runs in alternate region before relying on it.
