---
name: azure
description: "MANDATORY parallel execution patterns (30x speedup), monitor metrics aggregation, --output tsv formatting, and common pitfalls"
connection_type: azure
preload: false
---

# Azure CLI Skill

Execute Azure CLI commands with proper credential injection.

## CLI Tips

### Parallel Execution Requirement (CRITICAL)

**ALL independent operations MUST run in parallel using background jobs (&) and wait**

ENFORCEMENT RULES:

- **FORBIDDEN**: Sequential loops like `for item in $items; do cmd $item; done` (causes O(n) runtime)
- **MANDATORY**: Every independent operation spawns a background job: `{ cmd1 } & { cmd2 } & { cmd3 } & wait`
- **DETECTION**: If your script processes N resources/metrics/regions and N > 1, the script MUST contain at least N background jobs
- **TIME IMPACT**: Sequential execution with 30 VMs × 2 seconds per call = 60 seconds. Parallel = 2 seconds (30x faster)
- **VALIDATION CHECKLIST** (agent must mentally verify before output):
  - Count independent operations: \_\_\_
  - Count background jobs (&): \_\_\_
  - These numbers MUST match, or script will be REJECTED
  - Do all operations depend on each other? (Only valid exception to parallel requirement)

PARALLEL PATTERN (CORRECT):

```bash
for vm in $vms; do
  operation "$vm" &  # ← Spawn as background job
done
wait  # ← Wait for all to complete
```

SEQUENTIAL PATTERN (FORBIDDEN - ONLY if operations have data dependencies):

```bash
result=$(operation1)
operation2 "$result"  # ← Only valid if operation2 requires operation1's output
```

### Agent Output Rules

- The script output is for the agent itself to read and process, NOT for human reading
- Do NOT add visual formatting, icons, or decorative elements (no emojis, borders, or separators)
- NEVER USE echo statements for section breaks, headers, or formatting (no "--------", "====", or similar)
- Focus on raw data extraction and minimal, parseable output
- Use plain text format with consistent delimiters for easy parsing
- Prioritize machine-readability over human presentation
- NEVER run commands or scripts that print, log, or expose environment variables, credentials, or Azure keys (e.g., AZURE_USERNAME, AZURE_PASSWORD, AZURE_TENANT)

### Execution Guidelines

- **PARALLEL EXECUTION IS MANDATORY**: Always use background jobs (`&`) and `wait` for independent operations
  - Process multiple VMs/resources in parallel: `{ ... } &` with `wait` at the end
  - Fetch multiple metrics for the same resource in parallel, then `wait` before processing
  - Sequential loops are FORBIDDEN unless operations have strict dependencies
  - Parallel execution reduces runtime from O(n \* time_per_operation) to O(max_operation_time) - use it always
- Always consolidate related steps into single CLI Bash script if possible
- Only use read-only commands (e.g., list, show, get) - never modify resources
- Always format CLI output as plain text (never JSON or table) so that it's easy for the agent to parse. For Azure use --output tsv for text output. Also use filtering/query flags to limit output to what is needed. These practices are crucial for efficiency and accuracy.

### Efficient CLI Script Example

**ANTI-PATTERN EXAMPLE (SEQUENTIAL - SLOW - UNACCEPTABLE)**

```bash
#!/bin/bash
# RUNTIME: ~60 seconds for 30 VMs (2 sec per call × 30)
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ")

echo "Azure VM Metrics Summary ($START_TIME to $END_TIME)"

# Get resource groups
az group list --output tsv --query "[*].[name]" | while read rg_name; do
    vms=$(az vm list -g "$rg_name" --output tsv --query "[*].[name]")
    if [ -n "$vms" ]; then
        echo "Resource Group: $rg_name"

        # This SEQUENTIAL loop is FORBIDDEN
        echo "$vms" | while read vm_name; do
            echo "  VM: $vm_name"

            # Sequential metric fetches - UNACCEPTABLE
            az monitor metrics list \
                --resource "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$rg_name/providers/Microsoft.Compute/virtualMachines/$vm_name" \
                --metric "Percentage CPU" \
                --start-time "$START_TIME" \
                --end-time "$END_TIME" \
                --interval PT1H \
                --aggregation Average \
                --output tsv

            az monitor metrics list \
                --resource "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$rg_name/providers/Microsoft.Compute/virtualMachines/$vm_name" \
                --metric "Network In Total" \
                --start-time "$START_TIME" \
                --end-time "$END_TIME" \
                --interval PT1H \
                --aggregation Total \
                --output tsv
        done
    fi
done
# TOTAL TIME: ~60 seconds (UNACCEPTABLE for 30+ VMs)
```

**CORRECT EXAMPLE (PARALLEL - FAST - REQUIRED)**

```bash
#!/bin/bash
# Set date range for 30 days
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ")

echo "Azure VM Metrics Summary ($START_TIME to $END_TIME)"

# Function to get VM metrics with compact output
get_vm_metrics() {
    local resource_group=$1
    local vm_name=$2
    local metric_name=$3
    local aggregation=$4
    local unit=$5

    result=$(az monitor metrics list \
        --resource "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$resource_group/providers/Microsoft.Compute/virtualMachines/$vm_name" \
        --metric "$metric_name" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --interval PT1H \
        --aggregation "$aggregation" \
        --output tsv \
        --query "value[0].timeseries[0].data[*].[timeStamp,${aggregation,,}]")

    if [ -n "$result" ]; then
        echo "$metric_name ($aggregation):"
        echo "$result" | while IFS=$'\t' read timestamp value; do
            if [ -n "$value" ] && [ "$value" != "null" ]; then
                date_only=$(echo $timestamp | cut -d'T' -f1)
                if [ "$unit" = "%" ]; then
                    # Round percentage to 1 decimal
                    value_rounded=$(printf "%.1f" $value)
                    echo "  $date_only: ${value_rounded}%"
                elif [ "$unit" = "GB" ]; then
                    # Convert bytes to GB and round to 1 decimal
                    value_gb=$(echo "scale=1; $value / 1073741824" | bc -l)
                    echo "  $date_only: ${value_gb}GB"
                else
                    # Round to whole number for counts
                    value_rounded=$(printf "%.0f" $value)
                    echo "  $date_only: $value_rounded"
                fi
            fi
        done

        # Calculate summary stats
        if [ "$unit" = "%" ]; then
            avg=$(echo "$result" | awk -F'\t' '{if($2!="" && $2!="null") {sum+=$2; count++}} END {if(count>0) printf "%.1f", sum/count}')
            max=$(echo "$result" | awk -F'\t' 'BEGIN{max=0} {if($2!="" && $2!="null" && $2>max) max=$2} END {printf "%.1f", max}')
            echo "  → Avg: ${avg}%, Peak: ${max}%"
        else
            avg=$(echo "$result" | awk -F'\t' '{if($2!="" && $2!="null") {sum+=$2; count++}} END {if(count>0) printf "%.0f", sum/count}')
            max=$(echo "$result" | awk -F'\t' 'BEGIN{max=0} {if($2!="" && $2!="null" && $2>max) max=$2} END {printf "%.0f", max}')
            echo "  → Avg: $avg, Peak: $max"
        fi
        echo ""
    fi
}

# Function to process a single VM with parallel metric fetches
process_vm() {
    local rg_name=$1
    local vm_name=$2

    echo "  VM: $vm_name"

    # Fetch all metrics in parallel for this VM
    get_vm_metrics "$rg_name" "$vm_name" "Percentage CPU" "Average" "%" &
    get_vm_metrics "$rg_name" "$vm_name" "Network In Total" "Total" "bytes" &
    get_vm_metrics "$rg_name" "$vm_name" "Network Out Total" "Total" "bytes" &

    # Wait for all metrics to complete
    wait
    echo ""
}

# List resource groups and VMs
echo "Resource Groups and VMs:"
az group list --output tsv --query "[*].[name]" | while read rg_name; do
    vms=$(az vm list -g "$rg_name" --output tsv --query "[*].[name]")
    if [ -n "$vms" ]; then
        echo "Resource Group: $rg_name"

        # Process all VMs in this resource group in parallel
        echo "$vms" | while read vm_name; do
            process_vm "$rg_name" "$vm_name" &
        done

        # Wait for all VMs in this resource group to complete
        wait
        echo ""
    fi
done
```

**PERFORMANCE COMPARISON TABLE**
| Pattern | VMs | Time/Call | Total Time | Speed |
|---------|-----|-----------|-----------|-------|
| Sequential (❌) | 30 | 2 sec | ~60 sec | Baseline |
| Parallel (✅) | 30 | 2 sec | ~2 sec | **30x faster** |
| Sequential (❌) | 100 | 2 sec | ~200 sec | Baseline |
| Parallel (✅) | 100 | 2 sec | ~2 sec | **100x faster** |

**KEY DIFFERENCES IN THIS SCRIPT (What Makes It Parallel)**
✅ Line 111: `process_vm "$rg_name" "$vm_name" &` - spawns as background job
✅ Lines 114-115: `wait` - waits for all background jobs before continuing
✅ Lines 93-98: Inside `process_vm`, metrics fetch runs in parallel (with &)

**VALIDATION CHECKLIST FOR AGENT**
Before outputting ANY script, check every item:

- [ ] Count number of independent resources/metrics/regions to process: \_\_\_
- [ ] Count number of `&` background job spawns in script: \_\_\_
- [ ] If these counts don't match, the script is WRONG - REJECT it and rewrite
- [ ] Verify each background job block is followed by a `wait` statement
- [ ] Check that NO sequential loops exist for independent operations
- [ ] Confirm expected runtime is ~2-10 seconds (not ~30+ seconds)
- [ ] Verify Azure monitor aggregation values are correct (Average, Total, Minimum, Maximum, Count)
- [ ] Confirm script uses --output tsv with proper --query filtering

### Common Azure CLI Patterns

- List all resource groups: `az group list --output tsv --query "[*].[name,location]"`
- List VMs in a resource group: `az vm list -g myResourceGroup --output tsv --query "[*].[name,hardwareProfile.vmSize,provisioningState]"`
- Get VM details: `az vm show -g myResourceGroup -n myVM --output tsv --query "[name,hardwareProfile.vmSize,storageProfile.osDisk.diskSizeGb]"`
- List storage accounts: `az storage account list --output tsv --query "[*].[name,resourceGroup,location,sku.name]"`
- List SQL databases: `az sql db list -g myResourceGroup -s myServer --output tsv --query "[*].[name,status,edition,serviceLevelObjective]"`
- Get subscription info: `az account show --output tsv --query "[subscriptionId,name,state]"`
- List App Service plans: `az appservice plan list --output tsv --query "[*].[name,resourceGroup,sku.name,numberOfSites]"`
- List Key Vaults: `az keyvault list --output tsv --query "[*].[name,resourceGroup,location]"`
- Get cost data: `az consumption usage list --start-date 2024-01-01 --end-date 2024-01-31 --output tsv --query "[*].[usageStart,usageEnd,instanceName,pretaxCost]"`

### Azure Service Naming Patterns

- Virtual Machines: Standard naming like Standard_D2s_v3, Standard_B1ms
- Storage: Standard_LRS, Premium_LRS, Standard_GRS
- SQL Database: Basic, Standard (S0-S12), Premium (P1-P15)
- App Service: Free, Shared, Basic (B1-B3), Standard (S1-S3), Premium (P1-P3)

### Parallel vs Sequential Rules

- **ALWAYS PARALLEL**: Multiple VMs, multiple metrics, multiple resource groups, multiple subscriptions
- **ONLY SEQUENTIAL**: Operations that depend on previous results (e.g., create then modify, query then filter)
- **PARALLEL PATTERN**: `{ operation1 & operation2 & operation3 & }; wait`
- **SEQUENTIAL PATTERN**: Only when operation B requires result from operation A
- **NEVER**: Sequential loops for independent operations - this wastes time and tokens

**FORBIDDEN ANTI-PATTERNS** (will cause script rejection):

- ❌ `for vm in $vms; do az ... ; done` (causes O(n) delays; use `for vm in $vms; do az ... & done; wait`)
- ❌ `while read line; do az ... ; done < file` (sequential processing; parallelize with background jobs)
- ❌ Nested loops without background jobs: `for rg in $rgs; do for vm in $vms; do cmd; done; done`
- ❌ One call at a time when batch API is available (e.g., az vm show for each VM instead of az vm list)
- ❌ Processing outputs sequentially when they could be fetched in parallel: `result1=$(cmd1); result2=$(cmd2)` → should be `cmd1 & cmd2 & wait`

**REQUIRED ANTI-PATTERN FIXES**:

- ✅ BEFORE: `for vm in $vms; do az vm show -g $rg -n $vm; done`
- ✅ AFTER: `for vm in $vms; do az vm show -g $rg -n $vm & done; wait`
- ✅ BEFORE: `az vm list -g $rg1; az vm list -g $rg2`
- ✅ AFTER: `az vm list -g $rg1 & az vm list -g $rg2 & wait`

## Output Format

Present results as a structured report:
```
Azure Report
════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

