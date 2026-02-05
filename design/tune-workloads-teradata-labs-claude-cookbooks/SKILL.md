---
name: tune-workloads
description: Analyze workload classification and **autonomously configure** classification rules, filters, and priorities to improve accuracy and meet business requirements
---

# Tune Workloads

Analyze and **autonomously optimize** workload definitions including classification rules, filters, priorities, and exception handling to ensure queries are properly managed according to business requirements.

## 🎯 New Autonomous Capabilities

**This skill can now execute changes, not just recommend them!**

With tdwm-mcp v1.5.0, this skill has evolved from advisory to autonomous:
- ✅ **ADD** classification criteria to existing workloads
- ✅ **ADD** sub-criteria for fine-grained targeting (FTSCAN, MINSTEPTIME, etc.)
- ✅ **VALIDATE** classification types and operators before execution
- ✅ **USE TEMPLATES** for common classification patterns
- ✅ **VERIFY** changes were applied correctly
- ✅ **ACTIVATE** rulesets to apply all changes

## Instructions

### When to Use This Skill
- Queries are being misclassified into wrong workloads
- Need to add classification rules to existing workload
- Workload SLAs are not being met due to classification issues
- After application changes or new deployments
- Regular workload management review and optimization
- Need to adjust classification criteria dynamically

### Available MCP Tools

**Monitoring & Analysis:**
- `list_active_WD` - Review active workload definitions
- `list_WDs` - List all workloads (active and inactive)
- `show_tdwm_summary` - Analyze workload distribution
- `show_tasm_statistics` - Review TASM rule effectiveness
- `show_tasm_even_history` - See workload classification decisions
- `show_query_band` - Review query band usage
- `list_rulesets` - List all available rulesets

**Configuration Management (NEW ✨):**
- `add_classification_to_rule` - Add classification criteria to workload/filter/throttle
- `add_subcriteria_to_target` - Add sub-criteria (FTSCAN, MINSTEPTIME, etc.)
- `activate_ruleset` - Apply all pending changes

### Available MCP Resources (NEW ✨)

**Templates:**
- `tdwm://templates/filter` - List all filter templates
- `tdwm://template/filter/application-basic` - Filter by application
- `tdwm://template/filter/user-group` - Filter by user/account
- `tdwm://template/filter/query-complexity` - Filter by complexity metrics

**Reference Data:**
- `tdwm://reference/classification-types` - All 31 classification types
- `tdwm://reference/operators` - Classification operators (I, O, IO)
- `tdwm://reference/subcriteria-types` - Sub-criteria types
- `tdwm://reference/filter-actions` - Filter actions (ACCEPT/REJECT)

**Discovery:**
- `tdwm://rulesets` - List all rulesets
- `tdwm://system/active-ruleset` - Get currently active ruleset
- `tdwm://ruleset/{name}/filters` - List filters in ruleset
- `tdwm://ruleset/{name}/throttles` - List throttles in ruleset
- `tdwm://ruleset/{name}/pending-changes` - Check pending changes

**Workflows:**
- `tdwm://workflow/add-classification` - Step-by-step classification addition guide

### Step-by-Step Workflow

#### Phase 1: Discovery & Analysis (Read-Only)

1. **Assess Current Workload Configuration**
   - Get active ruleset: `tdwm://system/active-ruleset`
   - List all workloads: `list_active_WD` and `list_WDs`
   - Review workload distribution: `show_tdwm_summary`
   - Document workload hierarchy and priorities

2. **Analyze Classification Accuracy**
   - Use `show_tdwm_summary` to see query distribution
   - Check `show_tasm_even_history` for misclassification patterns
   - Identify queries landing in DEFAULT or wrong workloads
   - Review `show_query_band` to verify tagging is working

3. **Review Existing Rules**
   - List filters: `tdwm://ruleset/{name}/filters`
   - For each filter: `tdwm://ruleset/{name}/filter/{filter_name}`
   - List throttles: `tdwm://ruleset/{name}/throttles`
   - For each throttle: `tdwm://ruleset/{name}/throttle/{throttle_name}`
   - Check for gaps, overlaps, or conflicts in rule logic

4. **Identify Classification Gaps**
   - Queries not matching any classification rules
   - Missing criteria for new applications
   - Overly broad or narrow classification
   - Need for sub-criteria refinement

5. **Calculate Optimal Classification**
   - Based on application characteristics and query bands
   - Consider user groups and account names
   - Factor in query complexity metrics (if needed)
   - Determine priority relative to business requirements

#### Phase 2: Execute Changes (Autonomous - NEW!)

6. **Select Approach: Template or Custom**
   - **Template-Based** (Recommended):
     - Browse templates: `tdwm://templates/filter`
     - Select template matching use case
     - Read template: `tdwm://template/filter/{id}`
     - Customize parameters for your workload

   - **Custom Classification**:
     - Validate classification types: `tdwm://reference/classification-types`
     - Validate operators: `tdwm://reference/operators`
     - Design custom classification criteria

7. **Add Classification to Rule**
   - **For existing workload/filter/throttle**:
     ```
     Use: add_classification_to_rule(
       ruleset_name, rule_name, rule_type,
       classification_criteria
     )
     ```

   - **Classification criteria structure**:
     ```
     [{
       "description": "Human-readable description",
       "type": "APPL|USER|ACCT|...",  # From reference
       "value": "actual_value",
       "operator": "I|O|IO"  # Inclusion/Exclusion/Inconclusive
     }]
     ```

8. **Add Sub-Criteria (if needed)**
   - For fine-grained control, add sub-criteria:
     ```
     Use: add_subcriteria_to_target(
       ruleset_name, rule_name, target_type,
       subcriteria
     )
     ```

   - **Common sub-criteria**:
     - `FTSCAN: "Y"` - Full table scan queries
     - `MINSTEPTIME: "300"` - Queries running > 5 minutes
     - `MINPARSERTIME: "10"` - Queries with parsing time > 10 seconds

9. **Activate Changes**
   - Check pending changes: `tdwm://ruleset/{name}/pending-changes`
   - Activate ruleset: `activate_ruleset(ruleset_name)`

#### Phase 3: Verification (Autonomous - NEW!)

10. **Verify Configuration**
    - Read back filter/throttle: `tdwm://ruleset/{name}/filter/{name}`
    - Confirm classification was added
    - Confirm enabled state is correct

11. **Monitor Impact**
    - Wait 5-10 minutes for statistics to update
    - Check workload distribution: `show_tdwm_summary`
    - Verify queries now classified correctly
    - Monitor TASM events: `show_tasm_even_history`

12. **Iterate if Needed**
    - If still misclassifying: add more criteria
    - If too broad: add exclusion criteria (operator "O")
    - Use `add_classification_to_rule` for adjustments

## Examples

### Example 1: Fix ETL Misclassification (Autonomous)

**Scenario**: ETL queries ending up in DEFAULT workload instead of ETL workload

**Discovery**:
```
1. show_tdwm_summary → See 50% queries in DEFAULT (should be in ETL)
2. show_query_band → ETL sets query band 'APP=ETL_LOADER'
3. tdwm://system/active-ruleset → "Tactical"
4. tdwm://ruleset/Tactical/filter/ETL_FILTER → No APPL classification exists
```

**Analysis**:
- ETL workload exists but classification is incomplete
- ETL sets query band but filter doesn't check it
- Need to add APPL classification to ETL_FILTER

**Execution** (Autonomous):
```
1. Validate classification type:
   tdwm://reference/classification-types
   → Confirm "APPL" is valid classification type

2. Add APPL classification to ETL filter:
   add_classification_to_rule(
     ruleset_name="Tactical",
     rule_name="ETL_FILTER",
     rule_type="filter",
     classification_criteria=[{
       "description": "Match ETL application query band",
       "type": "APPL",
       "value": "ETL_LOADER",
       "operator": "I"  # Inclusion
     }]
   )

3. Check pending changes:
   tdwm://ruleset/Tactical/pending-changes
   → Confirm APPL classification queued

4. Activate:
   activate_ruleset(ruleset_name="Tactical")

5. Verify:
   tdwm://ruleset/Tactical/filter/ETL_FILTER
   → Confirm APPL classification present

6. Monitor (wait 10 minutes):
   show_tdwm_summary
   → ETL queries now in ETL workload (not DEFAULT)
```

**Result**: ETL queries properly classified, DEFAULT workload reduced by 50%

---

### Example 2: Add User-Based Classification (Autonomous)

**Scenario**: Power BI users need dedicated workload but not all set query band

**Discovery**:
```
1. show_tdwm_summary → Power BI queries mixed across workloads
2. show_query_band → Only 60% of Power BI queries set query band
3. list_active_WD → POWERBI workload exists
4. tdwm://ruleset/Tactical/filter/POWERBI_FILTER → Only has APPL classification
```

**Analysis**:
- Some Power BI users don't set query band (legacy reports)
- Need to add USER classification as fallback
- Power BI users identified by username pattern "pbi_*"

**Execution** (Autonomous):
```
1. Validate classification type:
   tdwm://reference/classification-types
   → Confirm "USER" is valid

2. Add USER classification to existing filter:
   add_classification_to_rule(
     ruleset_name="Tactical",
     rule_name="POWERBI_FILTER",
     rule_type="filter",
     classification_criteria=[{
       "description": "Catch Power BI users without query band",
       "type": "USER",
       "value": "pbi_*",  # Pattern matching
       "operator": "I"
     }]
   )

3. Activate:
   activate_ruleset(ruleset_name="Tactical")

4. Verify:
   tdwm://ruleset/Tactical/filter/POWERBI_FILTER
   → Confirm both APPL and USER classifications present

5. Monitor:
   show_tdwm_summary
   → Power BI workload increased from 60% to 95% capture rate
```

**Result**: Power BI queries properly classified even without query band

---

### Example 3: Limit Long-Running Analytics (Autonomous)

**Scenario**: Analytics queries running >10 minutes should be throttled

**Discovery**:
```
1. show_query_log → Analytics queries running 10-60 minutes
2. tdwm://ruleset/Tactical/throttle/ANALYTICS_LIMIT → Has APPL classification
3. show_trottle_statistics → Short analytics queries also being throttled
```

**Analysis**:
- Throttle catches all analytics queries
- Only long-running queries need throttling
- Need to add MINSTEPTIME sub-criteria (600 seconds = 10 minutes)

**Execution** (Autonomous):
```
1. Validate sub-criteria type:
   tdwm://reference/subcriteria-types
   → Confirm "MINSTEPTIME" is valid

2. Add MINSTEPTIME sub-criteria to throttle:
   add_subcriteria_to_target(
     ruleset_name="Tactical",
     throttle_name="ANALYTICS_LIMIT",
     target_type="APPL",
     subcriteria={
       "type": "MINSTEPTIME",
       "value": "600"  # 10 minutes in seconds
     }
   )

3. Activate:
   activate_ruleset(ruleset_name="Tactical")

4. Verify:
   tdwm://ruleset/Tactical/throttle/ANALYTICS_LIMIT
   → Confirm MINSTEPTIME sub-criteria present

5. Monitor:
   show_trottle_statistics
   → Only long-running analytics queries now throttled
```

**Result**: Short analytics queries run freely, only long queries throttled

---

### Example 4: Template-Driven Application Filter (Autonomous)

**Scenario**: New ML application needs classification into ML workload

**Discovery**:
```
1. show_tdwm_summary → ML queries appearing in DEFAULT
2. show_query_band → ML app sets 'APP=ML_TRAINING'
3. list_active_WD → ML_WORKLOAD exists
4. tdwm://ruleset/Tactical/filters → No ML_FILTER exists yet
```

**Analysis**:
- Need to create new filter for ML workload
- Application sets query band (simple case)
- Can use template for quick creation

**Execution** (Template-Based):
```
1. Get template:
   tdwm://template/filter/application-basic
   → Shows APPL-based filter pattern

2. Create filter using create_filter_rule:
   create_filter_rule(
     ruleset_name="Tactical",
     filter_name="ML_FILTER",
     classification_criteria=[{
       "description": "ML Training Application",
       "type": "APPL",
       "value": "ML_TRAINING",
       "operator": "I"
     }],
     action_type="ACCEPT",
     workload_name="ML_WORKLOAD"
   )

3. Enable filter:
   enable_filter_rule(
     ruleset_name="Tactical",
     filter_name="ML_FILTER"
   )

4. Activate:
   activate_ruleset(ruleset_name="Tactical")

5. Verify:
   tdwm://ruleset/Tactical/filter/ML_FILTER
   → Confirm filter created with APPL classification

6. Monitor:
   show_tdwm_summary
   → ML queries now in ML_WORKLOAD
```

**Result**: ML application properly classified into dedicated workload

---

### Example 5: Exclude Full Table Scans from Fast Track (Autonomous)

**Scenario**: Fast track workload getting slow queries due to full table scans

**Discovery**:
```
1. show_tdwm_summary → FAST_TRACK average response time increasing
2. show_query_log → Some FAST_TRACK queries doing full table scans
3. tdwm://ruleset/Tactical/filter/FAST_TRACK_FILTER → Has USER and APPL criteria
```

**Analysis**:
- Fast track should only handle indexed queries
- Full table scans should go to BATCH workload
- Need to add FTSCAN sub-criteria with exclusion

**Execution** (Autonomous):
```
1. Validate sub-criteria type:
   tdwm://reference/subcriteria-types
   → Confirm "FTSCAN" is valid

2. Add exclusion for full table scans:
   add_subcriteria_to_target(
     ruleset_name="Tactical",
     filter_name="FAST_TRACK_FILTER",
     target_type="USER",  # Apply to USER classification
     subcriteria={
       "type": "FTSCAN",
       "value": "N"  # Only queries NOT doing full scan
     }
   )

3. Activate:
   activate_ruleset(ruleset_name="Tactical")

4. Verify:
   tdwm://ruleset/Tactical/filter/FAST_TRACK_FILTER
   → Confirm FTSCAN sub-criteria present

5. Monitor:
   show_tdwm_summary
   → FAST_TRACK average response time improved
   → Full scan queries now in BATCH workload
```

**Result**: Fast track performance improved by excluding full scans

---

## Best Practices

### General Principles
- Start with broad classification (APPL, USER), refine with sub-criteria later
- Use query bands as primary classification method when possible
- Username/account filters are fallbacks when query bands unavailable
- Test classification changes during low-activity periods when possible
- Document business justification for each classification rule
- Monitor classification for 1-2 weeks after changes to verify effectiveness

### Discovery Before Execution (NEW ✨)
- **ALWAYS** use `tdwm://ruleset/{name}/filters` to see existing filters before adding
- Check `tdwm://ruleset/{name}/pending-changes` before activating
- Verify with resource read after changes
- Understand current classification before adding new rules

### Template Usage (NEW ✨)
- Use templates for common patterns (application-based, user-based)
- Customize template parameters for your specific needs
- Follow template best practices and examples

### Execution Safety (NEW ✨)
- Validate classification types against `tdwm://reference/classification-types`
- Validate operators against `tdwm://reference/operators`
- Start with single classification, add more if needed
- Test in non-production first if possible
- Keep emergency rollback plan

### Validation (NEW ✨)
- Always read back filter/throttle after adding classification
- Confirm classification appears in rule definition
- Monitor workload distribution after changes
- Check TASM events to verify classification working

### Monitoring
- Query bands take precedence over username/account classification
- Operator "I" (Inclusion) matches the value
- Operator "O" (Exclusion) excludes the value
- Operator "IO" (Inconclusive) allows TASM to continue evaluation
- Sub-criteria refine the target (FTSCAN, MINSTEPTIME, etc.)
- Coordinate classification changes with application teams
- Regular classification reviews identify drift over time

### Related Skills
- Use **optimize-throttles** skill for concurrency limit adjustments
- Use **manage-workloads** skill for creating new workloads from scratch
- Use **emergency-response** skill for crisis situations
- Use **discover-configuration** skill to inventory existing classifications
