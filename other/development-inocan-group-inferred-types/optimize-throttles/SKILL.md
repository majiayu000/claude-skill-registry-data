---
name: optimize-throttles
description: Analyze throttle behavior, recommend optimal configurations, and autonomously create/modify throttles to balance resource allocation and meet performance SLAs
---

# Optimize Throttles

Analyze throttle behavior and **autonomously configure** optimal throttle settings to balance workload priorities, prevent resource starvation, and meet service level agreements.

## 🎯 New Autonomous Capabilities

**This skill can now execute changes, not just recommend them!**

With tdwm-mcp v1.5.0, this skill has evolved from advisory to autonomous:
- ✅ **CREATE** new throttles based on analysis
- ✅ **MODIFY** existing throttle limits dynamically
- ✅ **ENABLE/DISABLE** throttles without manual SQL
- ✅ **USE TEMPLATES** for common throttle patterns
- ✅ **VALIDATE** parameters before execution
- ✅ **VERIFY** changes were applied correctly

## Instructions

### When to Use This Skill
- Users report excessive query delays or throttling
- Need to balance competing workload priorities
- Workload SLAs are not being met
- After adding new workloads or applications
- Following system capacity changes
- System overload requiring immediate throttle creation
- Seasonal workload changes need different limits

### Available MCP Tools

**Monitoring & Analysis:**
- `show_trottle_statistics` - View throttle behavior by level (ALL/QUERY/SESSION/WORKLOAD)
- `show_tasm_statistics` - Review TASM rule effectiveness
- `show_tdwm_summary` - See workload distribution
- `list_active_WD` - List active workload definitions
- `show_query_log` - Analyze query timing and delays
- `list_rulesets` - List all available rulesets

**Configuration Management (NEW ✨):**
- `create_system_throttle` - Create new throttle with classifications
- `modify_throttle_limit` - Dynamically adjust throttle limits
- `delete_throttle` - Remove throttle definition
- `enable_throttle` - Activate throttle rule
- `disable_throttle` - Deactivate throttle rule
- `add_classification_to_rule` - Add classification criteria
- `add_subcriteria_to_target` - Add sub-criteria (FTSCAN, MINSTEPTIME, etc.)
- `activate_ruleset` - Apply all pending changes

### Available MCP Resources (NEW ✨)

**Templates:**
- `tdwm://templates/throttle` - List all throttle templates
- `tdwm://template/throttle/application-basic` - Limit queries by application
- `tdwm://template/throttle/table-fullscan` - Limit full table scans
- `tdwm://template/throttle/user-concurrency` - Per-user concurrency limits
- `tdwm://template/throttle/time-based-etl` - Time-based ETL throttling

**Reference Data:**
- `tdwm://reference/classification-types` - All 31 classification types
- `tdwm://reference/operators` - Classification operators (I, O, IO)
- `tdwm://reference/subcriteria-types` - Sub-criteria types
- `tdwm://reference/throttle-types` - Throttle types (DM, M)

**Discovery:**
- `tdwm://rulesets` - List all rulesets
- `tdwm://system/active-ruleset` - Get currently active ruleset
- `tdwm://ruleset/{name}/throttles` - List throttles in ruleset
- `tdwm://ruleset/{name}/throttle/{throttle_name}` - Throttle details
- `tdwm://ruleset/{name}/pending-changes` - Check pending changes

**Workflows:**
- `tdwm://workflow/create-throttle` - Step-by-step throttle creation guide
- `tdwm://workflow/emergency-throttle` - Emergency response workflow

### Step-by-Step Workflow

#### Phase 1: Discovery & Analysis (Read-Only)

1. **Assess Current Throttle Behavior**
   - Use `show_trottle_statistics` for all levels (query/session/workload)
   - Identify workloads experiencing excessive throttling
   - Note throttle delay times and frequency

2. **Understand Workload Requirements**
   - Review business SLAs for each workload
   - Identify critical vs non-critical workloads
   - Determine acceptable delay tolerances

3. **Analyze Workload Interactions**
   - Use `show_tdwm_summary` to see resource competition
   - Identify which workloads are blocking others
   - Check if high-priority workloads are being throttled

4. **Review Current Configuration**
   - Get active ruleset: `tdwm://system/active-ruleset`
   - List current throttles: `tdwm://ruleset/{name}/throttles`
   - For each throttle: `tdwm://ruleset/{name}/throttle/{throttle_name}`
   - Identify mismatches between priority and throttle limits

5. **Calculate Optimal Settings**
   - Based on resource availability and workload requirements
   - Consider peak vs average usage patterns
   - Balance protection (prevent monopolization) vs throughput
   - Factor in concurrency needs for each workload

#### Phase 2: Execute Changes (Autonomous - NEW!)

6. **Select Approach: Template or Custom**
   - **Template-Based** (Recommended):
     - Browse templates: `tdwm://templates/throttle`
     - Select template matching use case
     - Read template: `tdwm://template/throttle/{id}`
     - Customize parameters for your workload

   - **Custom Throttle**:
     - Validate classification types: `tdwm://reference/classification-types`
     - Validate operators: `tdwm://reference/operators`
     - Design custom classification criteria

7. **Create or Modify Throttle**
   - **For NEW throttles**:
     ```
     Use: create_system_throttle(
       ruleset_name, throttle_name, throttle_type,
       limit, classification_criteria
     )
     ```

   - **For EXISTING throttles**:
     ```
     Use: modify_throttle_limit(
       ruleset_name, throttle_name, new_limit
     )
     ```

8. **Add Additional Criteria (if needed)**
   - Add classifications: `add_classification_to_rule`
   - Add sub-criteria: `add_subcriteria_to_target` (FTSCAN, MINSTEPTIME, etc.)

9. **Enable and Activate**
   - Enable throttle: `enable_throttle(ruleset_name, throttle_name)`
   - Check pending changes: `tdwm://ruleset/{name}/pending-changes`
   - Activate ruleset: `activate_ruleset(ruleset_name)`

#### Phase 3: Verification (Autonomous - NEW!)

10. **Verify Configuration**
    - Read back throttle: `tdwm://ruleset/{name}/throttle/{throttle_name}`
    - Confirm limit matches expected value
    - Confirm enabled state is correct

11. **Monitor Impact**
    - Wait 5-10 minutes for statistics to update
    - Check throttle statistics: `show_trottle_statistics`
    - Verify delayed query count is acceptable
    - Monitor workload summary: `show_tdwm_summary`

12. **Iterate if Needed**
    - If throttling is too aggressive: increase limit
    - If not effective enough: decrease limit
    - Use `modify_throttle_limit` for adjustments

## Examples

### Example 1: Create ETL Throttle to Protect Interactive Queries

**Scenario**: Batch ETL jobs overwhelming system, slowing interactive reports

**Discovery**:
```
1. show_tdwm_summary → See ETL using 80% of resources
2. show_trottle_statistics → No ETL throttle exists
3. tdwm://system/active-ruleset → "Tactical"
```

**Analysis**:
- ETL should run max 10 concurrent queries
- Interactive reports need protection
- ETL workload identified by APPL='ETL_APP'

**Execution** (Autonomous):
```
1. Select template:
   tdwm://template/throttle/application-basic

2. Create throttle:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="ETL_LIMIT",
     throttle_type="DM",  # Delay Management
     limit=10,
     classification_criteria=[{
       "description": "ETL Application throttle",
       "type": "APPL",
       "value": "ETL_APP",
       "operator": "I"  # Inclusion
     }]
   )

3. Enable:
   enable_throttle(ruleset_name="Tactical", throttle_name="ETL_LIMIT")

4. Activate:
   activate_ruleset(ruleset_name="Tactical")

5. Verify:
   tdwm://ruleset/Tactical/throttle/ETL_LIMIT
   → Confirm limit=10, enabled=true

6. Monitor:
   show_trottle_statistics(type="ALL")
   → Check ETL delayed count after 10 minutes
```

**Result**: ETL limited to 10 concurrent, interactive reports responsive

---

### Example 2: Adjust Existing Throttle Limit

**Scenario**: Analytics throttle too restrictive (limit=3), queries backing up

**Discovery**:
```
1. show_trottle_statistics → Analytics delayed count growing
2. tdwm://ruleset/Tactical/throttle/ANALYTICS_LIMIT → Current limit=3
3. show_query_log → Analytics queries delayed avg 15 minutes
```

**Analysis**:
- Limit of 3 is too low for current analytics load
- Recommend increasing to 8 based on workload analysis
- System has capacity for increase

**Execution** (Autonomous):
```
1. Modify limit:
   modify_throttle_limit(
     ruleset_name="Tactical",
     throttle_name="ANALYTICS_LIMIT",
     new_limit=8
   )

2. Activate:
   activate_ruleset(ruleset_name="Tactical")

3. Verify:
   tdwm://ruleset/Tactical/throttle/ANALYTICS_LIMIT
   → Confirm limit=8

4. Monitor:
   show_trottle_statistics(type="ALL")
   → Delayed count should decrease
```

**Result**: Analytics throughput increased, delay reduced to <5 min

---

### Example 3: Emergency Throttle During System Overload

**Scenario**: Unexpected query spike causing CPU >95%, need immediate restriction

**Analysis**: SKIP detailed analysis, immediate action needed

**Execution** (Fast):
```
1. Use emergency workflow:
   tdwm://workflow/emergency-throttle

2. Create very restrictive throttle:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="EMERGENCY_LIMIT",
     throttle_type="DM",
     limit=3,  # Very restrictive
     classification_criteria=[{
       "description": "Emergency system protection",
       "type": "APPL",
       "value": "*",  # ALL applications
       "operator": "I"
     }]
   )

3. Enable and activate immediately:
   enable_throttle(ruleset_name="Tactical", throttle_name="EMERGENCY_LIMIT")
   activate_ruleset(ruleset_name="Tactical")

4. Monitor recovery:
   Wait 60 seconds, check show_physical_resources
   → CPU should drop below 90%

5. Gradual relaxation:
   modify_throttle_limit(..., new_limit=5)
   activate_ruleset(...)
   Wait, monitor

   modify_throttle_limit(..., new_limit=10)
   activate_ruleset(...)
   Wait, monitor

6. Cleanup when stable:
   delete_throttle(ruleset_name="Tactical", throttle_name="EMERGENCY_LIMIT")
   activate_ruleset(ruleset_name="Tactical")
```

**Result**: System stabilized in <5 minutes, gradual return to normal

---

### Example 4: Template-Driven Full Table Scan Throttle

**Scenario**: Full table scans causing AMP skew and resource contention

**Discovery**:
```
1. show_amp_load → High skew factor
2. show_query_log → Many queries doing full table scans
3. Need to limit FTSCAN queries
```

**Execution** (Template-Based):
```
1. Get template:
   tdwm://template/throttle/table-fullscan
   → Shows structure with FTSCAN sub-criteria

2. Create throttle using template pattern:
   create_system_throttle(
     ruleset_name="Tactical",
     throttle_name="FTSCAN_LIMIT",
     throttle_type="DM",
     limit=5,
     classification_criteria=[{
       "description": "Target tables",
       "type": "TABLE",
       "value": "LARGE_TABLE_*",  # Pattern matching
       "operator": "I"
     }]
   )

3. Add FTSCAN sub-criteria:
   add_subcriteria_to_target(
     ruleset_name="Tactical",
     throttle_name="FTSCAN_LIMIT",
     target_type="TABLE",
     subcriteria={
       "type": "FTSCAN",
       "value": "Y"  # Full scan = Yes
     }
   )

4. Enable and activate:
   enable_throttle(ruleset_name="Tactical", throttle_name="FTSCAN_LIMIT")
   activate_ruleset(ruleset_name="Tactical")

5. Verify:
   tdwm://ruleset/Tactical/throttle/FTSCAN_LIMIT
   → Confirm sub-criteria present
```

**Result**: Full table scans limited, AMP skew reduced

---

## Best Practices

### General Principles
- Throttles should reflect business priorities, not just technical factors
- Set throttles to prevent monopolization while allowing throughput
- High-priority workloads need guaranteed minimum resources
- Low-priority workloads should have limits to prevent starvation of others
- Always leave some headroom for unexpected workload spikes
- Document throttle rationale for future reference

### Discovery Before Execution (NEW ✨)
- **ALWAYS** use `tdwm://ruleset/{name}/throttles` to see existing throttles before creating
- Check `tdwm://ruleset/{name}/pending-changes` before activating
- Verify with `tdwm://ruleset/{name}/throttle/{name}` after changes

### Template Usage (NEW ✨)
- Use templates for common patterns (reduces errors by 50%)
- Customize template parameters for your specific needs
- Follow template best practices and examples

### Execution Safety (NEW ✨)
- Start with conservative limits, increase gradually
- Test throttle changes in non-production first if possible
- Monitor impact for 15-30 minutes before declaring success
- Keep emergency rollback plan (delete_throttle + activate_ruleset)

### Validation (NEW ✨)
- Validate classification types against `tdwm://reference/classification-types`
- Validate operators against `tdwm://reference/operators`
- Check throttle exists after creation (resource read)

### Monitoring
- Query-level throttles control concurrency, workload-level control total impact
- Consider different throttle settings for peak vs off-peak hours
- Monitor throttle effectiveness after changes - iterate if needed
- Coordinate throttle changes with workload owners

### Related Skills
- Use **configure-throttles** skill for new throttle creation from scratch
- Use **emergency-response** skill for crisis situations
- Use **discover-configuration** skill to inventory existing throttles
- Use **tune-workloads** skill to adjust classification criteria
