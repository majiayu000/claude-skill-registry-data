---
name: monitor-workloads
description: Monitor workload definitions, distribution, and TASM statistics using real-time resources to understand classification effectiveness and workload performance
---

# Monitor Workloads

Monitor Teradata workload definitions, activation status, query distribution, and TASM statistics using real-time MCP resources to understand how workload management is functioning and identify optimization opportunities.

## 🔍 Enhanced Capabilities

**This skill now leverages real-time workload monitoring resources!**

With tdwm-mcp v1.5.0, this skill provides:
- ✅ **REAL-TIME WORKLOAD DATA** - Instant workload distribution without queries
- ✅ **CLASSIFICATION ANALYSIS** - Understand how queries are routed to workloads
- ✅ **TASM EFFECTIVENESS TRACKING** - Monitor rule performance and statistics
- ✅ **CONFIGURATION DISCOVERY** - Explore filters, throttles, and rules per workload
- ✅ **INTEGRATED METRICS** - Workloads + queries + resources in one view

## Instructions

### When to Use This Skill
- User asks about workload configuration or status
- Need to understand how queries are being classified
- Investigating workload distribution or rule effectiveness
- Reviewing TASM performance and statistics
- Identifying misclassification issues
- Assessing workload balance and priority effectiveness

### Available MCP Tools

**Workload Monitoring:**
- `list_active_WD` - List currently active workload definitions
- `list_WDs` - List all workloads (active and inactive)
- `show_tdwm_summary` - Display workload distribution dashboard
- `show_tasm_statistics` - View TASM performance metrics
- `show_tasm_even_history` - Review TASM event history and classification decisions

**Related Analysis:**
- `list_query_band` - See query bands used for classification
- `list_delayed_request` - View queries delayed by throttles
- `show_trottle_statistics` - Throttle impact per workload

### Available MCP Resources (NEW ✨)

**Real-Time Workload Data:**
- `tdwm://system/workloads` - Active workload list with status
- `tdwm://system/summary` - Workload distribution and resource usage
- `tdwm://system/delayed-queries` - Queries delayed by workload
- `tdwm://system/throttle-statistics` - Throttle impact per workload

**Configuration Discovery:**
- `tdwm://rulesets` - List all available rulesets
- `tdwm://system/active-ruleset` - Currently active ruleset
- `tdwm://ruleset/{name}/filters` - Filters routing to workloads
- `tdwm://ruleset/{name}/throttles` - Throttles protecting workloads

**Reference:**
- `tdwm://reference/workload-states` - Workload state meanings
- `tdwm://reference/classification-flow` - How TASM classifies queries

### Step-by-Step Workflow

#### Phase 1: Quick Assessment (Use Resources First)

1. **Get Real-Time Workload Overview**
   - Read resource: `tdwm://system/workloads`
   - Shows all active workloads with status
   - Provides quick inventory of workload configuration

2. **Check Workload Distribution**
   - Read resource: `tdwm://system/summary`
   - Shows how queries and resources are distributed
   - Identifies which workloads are busy
   - Provides utilization percentages

#### Phase 2: Detailed Analysis (Use Tools)

3. **Review Workload Configuration**
   - Use `list_active_WD` to see enabled workloads with details
   - Use `list_WDs` to see all workloads (active + inactive)
   - Understand workload hierarchy and priorities
   - Document workload purposes

4. **Analyze Workload Distribution**
   - Use `show_tdwm_summary` for detailed distribution data
   - See query counts, concurrency, resource usage per workload
   - Identify which workloads are handling most traffic
   - Compare against expected distribution

5. **Check TASM Statistics**
   - Use `show_tasm_statistics` to view performance metrics
   - Review rule activations, throttle actions, exceptions
   - Identify patterns in workload management actions
   - Calculate rule effectiveness rates

6. **Review TASM Events**
   - Use `show_tasm_even_history` for classification decisions
   - Analyze why queries landed in specific workloads
   - Look for unexpected or problematic patterns
   - Identify misclassification root causes

#### Phase 3: Configuration Exploration

7. **Discover Workload Filters**
   - Get active ruleset: `tdwm://system/active-ruleset`
   - List filters: `tdwm://ruleset/{name}/filters`
   - For each filter, check which workload it routes to
   - Identify gaps in coverage (queries not matching any filter)

8. **Discover Workload Throttles**
   - List throttles: `tdwm://ruleset/{name}/throttles`
   - Check which throttles protect which workloads
   - Review throttle limits and current usage
   - Identify workloads without protection

9. **Assess Effectiveness**
   - Determine if workloads are being used as intended
   - Check if classification rules are working correctly
   - Verify resource distribution matches priorities
   - Identify workloads that need tuning

## Examples

### Example 1: Quick Workload Status Check (Fast)

**Scenario**: "Show me the current workload configuration"

**Action** (Resource-First Approach):
```
1. Read active workloads:
   tdwm://system/workloads
   → PRODUCTION_HIGH (active, priority 1)
   → ETL_BATCH (active, priority 2)
   → INTERACTIVE (active, priority 2)
   → ANALYTICS (active, priority 3)
   → AD_HOC (active, priority 4)
   → DEFAULT (active, priority 5)
   → YEAR_END (inactive - seasonal)
   → MAINTENANCE (inactive - special purpose)

2. Check distribution:
   tdwm://system/summary
   → PRODUCTION_HIGH: 12 queries, 25% resources
   → ETL_BATCH: 45 queries, 45% resources
   → INTERACTIVE: 28 queries, 20% resources
   → ANALYTICS: 8 queries, 7% resources
   → AD_HOC: 5 queries, 3% resources
   → DEFAULT: 2 queries, <1% resources

3. Report:
   "Current Workload Configuration:

    Active Workloads (6):
    - PRODUCTION_HIGH: Priority 1, 12 queries, 25% resources
    - ETL_BATCH: Priority 2, 45 queries, 45% resources (dominant)
    - INTERACTIVE: Priority 2, 28 queries, 20% resources
    - ANALYTICS: Priority 3, 8 queries, 7% resources
    - AD_HOC: Priority 4, 5 queries, 3% resources
    - DEFAULT: Priority 5, 2 queries, <1% resources (minimal, good)

    Inactive Workloads (2):
    - YEAR_END: Seasonal (activate December-January)
    - MAINTENANCE: Special purpose (activate during maintenance windows)

    Assessment:
    ✅ ETL batch is dominant workload (expected for current time)
    ✅ DEFAULT has minimal queries (good classification)
    ✅ Resource distribution aligns with priorities"
```

**Result**: Complete workload inventory in seconds

---

### Example 2: Investigate Workload Distribution Imbalance

**Scenario**: "Why is DEFAULT workload so busy? It should be nearly empty."

**Action** (Distribution Analysis):
```
1. Check current distribution:
   tdwm://system/summary
   → DEFAULT: 35 queries, 18% resources (⚠️ TOO HIGH!)
   → Expected: <5% resources

2. Get detailed summary:
   show_tdwm_summary()
   → DEFAULT workload details:
     - 35 active queries
     - Average runtime: 12 minutes
     - No throttle applied
     - Using 18% of system resources

3. Review TASM classification history:
   show_tasm_even_history(workload="DEFAULT")
   → Last 50 events show:
     - 65% "No matching filter" (no rule matched)
     - 35% "NEW_BI_TOOL query band not recognized"

4. Check query bands:
   list_query_band(type="TRANSACTION")
   → Filter for DEFAULT workload sessions
   → Common query bands:
     - APP=NEW_BI_TOOL (20 queries)
     - No query band set (15 queries)

5. Identify users:
   list_sessions()
   → Filter for DEFAULT workload
   → 20 queries from bi_users (NEW_BI_TOOL application)
   → 15 queries from adhoc_users (no query band)

6. Check existing filters:
   tdwm://ruleset/Tactical/filters
   → No filter matches APP=NEW_BI_TOOL
   → Ad-hoc users expected to not set query band

7. Report:
   "DEFAULT Workload Analysis: 35 queries (18% resources)

    Root Causes:
    1. NEW_BI_TOOL (20 queries, 57% of DEFAULT):
       → New BI application deployed last week
       → Sets query band 'APP=NEW_BI_TOOL'
       → No filter exists to route these queries
       → ACTION REQUIRED: Create filter for NEW_BI_TOOL

    2. Ad-hoc users (15 queries, 43% of DEFAULT):
       → No query band set (expected)
       → ACTION: Acceptable, or educate users

    Impact:
    - 18% of resources going to DEFAULT (should be <5%)
    - NEW_BI_TOOL queries not getting appropriate priority
    - Potential SLA violations for BI users

    RECOMMENDATION:
    Use tune-workloads skill to add classification:
    - Create or update filter to match APP=NEW_BI_TOOL
    - Route to INTERACTIVE workload or create dedicated BI workload
    - Will reduce DEFAULT from 18% to <5% resources"
```

**Result**: Root cause identified, specific action recommended

---

### Example 3: TASM Performance Review (Effectiveness)

**Scenario**: "Is TASM working effectively? Are rules firing as expected?"

**Action** (TASM Analysis):
```
1. Get TASM statistics:
   show_tasm_statistics()
   → Total requests processed: 1,847 (last hour)
   → Filter actions: 1,802 (97.6% classification rate)
   → Throttle delays: 45 (2.4% delayed)
   → Exceptions: 3 (0.16% errors)

2. Break down by workload:
   show_tasm_statistics(group_by="workload")
   → PRODUCTION_HIGH: 245 requests, 0 delays
   → ETL_BATCH: 892 requests, 12 delays (throttled)
   → INTERACTIVE: 467 requests, 8 delays
   → ANALYTICS: 156 requests, 15 delays (throttled)
   → AD_HOC: 84 requests, 10 delays (throttled)
   → DEFAULT: 3 requests (excellent!)

3. Review recent TASM events:
   show_tasm_even_history(time_range="last_1_hour")
   → Filter events: 1,802 successful classifications
   → Throttle events: 45 delay queue placements
   → No classification: 3 (went to DEFAULT)

4. Check throttle effectiveness:
   tdwm://system/throttle-statistics
   → ETL_BATCH throttle: Limit 20, delayed 12 (working)
   → ANALYTICS throttle: Limit 10, delayed 15 (aggressive)
   → AD_HOC throttle: Limit 5, delayed 10 (aggressive)

5. Analyze delays:
   list_delayed_request()
   → 8 queries currently in delay queue
   → Average delay time: 2.3 minutes (acceptable)
   → Max delay time: 8.7 minutes (one query)

6. Report:
   "TASM Performance Review:

    Overall Effectiveness: ✅ EXCELLENT
    - 97.6% classification rate (target >95%)
    - Only 3 queries in DEFAULT (0.16%)
    - 2.4% queries throttled (working as designed)

    Workload Breakdown:
    - PRODUCTION_HIGH: 245 requests, 0 delays (protected priority)
    - ETL_BATCH: 892 requests, 12 delays (1.3% delay rate, healthy)
    - INTERACTIVE: 467 requests, 8 delays (1.7% delay rate, healthy)
    - ANALYTICS: 156 requests, 15 delays (9.6% delay rate, aggressive)
    - AD_HOC: 84 requests, 10 delays (11.9% delay rate, aggressive)

    Throttle Effectiveness:
    ✅ ETL throttle working well (1.3% delay rate)
    ✅ Interactive protected (1.7% delay rate)
    ⚠️  Analytics throttle may be too restrictive (9.6% delay rate)
    ⚠️  Ad-hoc throttle may be too restrictive (11.9% delay rate)

    Recommendations:
    1. Monitor ANALYTICS and AD_HOC workloads
       → 9-12% delay rates higher than ideal (<5%)
       → Consider increasing throttle limits slightly

    2. Investigate 3 DEFAULT queries
       → Find why they didn't classify
       → Add filters if needed

    3. TASM is performing well overall
       → No major configuration changes needed"
```

**Result**: Comprehensive effectiveness assessment with specific recommendations

---

### Example 4: Discover Workload Configuration (Exploration)

**Scenario**: "What filters and throttles are configured for the ETL_BATCH workload?"

**Action** (Configuration Discovery):
```
1. Get active ruleset:
   tdwm://system/active-ruleset
   → "Tactical"

2. List all filters:
   tdwm://ruleset/Tactical/filters
   → Found 8 filters

3. Find ETL_BATCH filter:
   tdwm://ruleset/Tactical/filter/ETL_FILTER
   → Name: ETL_FILTER
   → Action: ACCEPT
   → Workload: ETL_BATCH
   → Enabled: true
   → Classifications:
     - APPL = 'ETL_*' (Inclusion)
     - USER = 'etl_batch' (Inclusion)

4. List all throttles:
   tdwm://ruleset/Tactical/throttles
   → Found 6 throttles

5. Find ETL_BATCH throttle:
   tdwm://ruleset/Tactical/throttle/ETL_LIMIT
   → Name: ETL_LIMIT
   → Type: DM (Delay Management)
   → Limit: 20 concurrent queries
   → Enabled: true
   → Classifications:
     - APPL = 'ETL_*' (Inclusion)

6. Check current utilization:
   tdwm://system/summary
   → ETL_BATCH workload:
     - 18 active queries (under 20 limit)
     - No queries delayed currently
     - 45% of system resources

7. Review classification effectiveness:
   show_tasm_even_history(workload="ETL_BATCH")
   → All ETL queries correctly classified
   → Filter matching on APPL and USER working

8. Report:
   "ETL_BATCH Workload Configuration:

    Filter (ETL_FILTER):
    - Routes queries to ETL_BATCH workload
    - Matches queries where:
      → Application starts with 'ETL_' (query band), OR
      → Username is 'etl_batch'
    - Status: Enabled and working correctly

    Throttle (ETL_LIMIT):
    - Limits ETL_BATCH to 20 concurrent queries
    - Type: Delay Management (queues excess queries)
    - Status: Enabled, currently under limit (18/20)

    Current State:
    - 18 active queries (2 slots available)
    - 0 queries delayed (throttle not engaged)
    - 45% of system resources (dominant workload)

    Classification Effectiveness:
    ✅ All ETL queries correctly classified
    ✅ No misclassifications detected
    ✅ Filter working as designed

    Configuration Assessment:
    ✅ Properly configured with both filter and throttle
    ✅ Throttle limit appropriate for current load
    ✅ Classification criteria catching all ETL queries"
```

**Result**: Complete configuration documentation for workload

---

### Example 5: Compare Workload Design vs Actual Usage (Audit)

**Scenario**: "Are our workloads being used as originally designed?"

**Action** (Design Validation):
```
1. Document design intent (from requirements):
   - PRODUCTION_HIGH: Critical production apps, <10% queries, 30% resources
   - ETL_BATCH: Nightly ETL, 40% queries, 40% resources
   - INTERACTIVE: User dashboards, 30% queries, 20% resources
   - ANALYTICS: Analytics queries, 15% queries, 8% resources
   - AD_HOC: Ad-hoc exploration, 5% queries, 2% resources
   - DEFAULT: Miscellaneous, <1% queries, <1% resources

2. Get actual distribution:
   tdwm://system/summary
   ACTUAL:
   - PRODUCTION_HIGH: 12% queries, 25% resources ✅ Close
   - ETL_BATCH: 45% queries, 45% resources ✅ Close
   - INTERACTIVE: 28% queries, 20% resources ✅ Match!
   - ANALYTICS: 8% queries, 7% resources ✅ Match!
   - AD_HOC: 5% queries, 3% resources ⚠️  Slightly high
   - DEFAULT: 2% queries, <1% resources ⚠️  Should be <1%

3. Analyze deviations:

   PRODUCTION_HIGH (12% vs designed 10%):
   - show_tasm_even_history(workload="PRODUCTION_HIGH")
   → Slightly more production apps than expected
   → Within acceptable range

   AD_HOC (5% queries, 3% resources vs designed 5% queries, 2% resources):
   - show_query_log(workload="AD_HOC")
   → Ad-hoc queries running longer than expected
   → Using more resources per query

   DEFAULT (2% vs designed <1%):
   - show_tasm_even_history(workload="DEFAULT")
   → NEW_BI_TOOL queries not classified (need filter)

4. Check SLA compliance:
   - PRODUCTION_HIGH: 99.9% uptime requirement
     → show_query_log(workload="PRODUCTION_HIGH", calc="avg_response_time")
     → Average: 0.8 seconds (target <1 second) ✅

   - INTERACTIVE: 95th percentile <5 seconds
     → show_query_log(workload="INTERACTIVE", calc="p95_response_time")
     → 95th percentile: 4.2 seconds ✅

   - ETL_BATCH: Complete within 4-hour window
     → show_query_log(workload="ETL_BATCH", time_range="last_night")
     → Completed in 3.5 hours ✅

5. Report:
   "Workload Design vs Actual Usage Audit:

    Overall Assessment: 🟢 MOSTLY ALIGNED

    Workload Comparison:
    ✅ PRODUCTION_HIGH: 12% queries vs 10% design (acceptable)
    ✅ ETL_BATCH: 45% queries vs 40% design (acceptable)
    ✅ INTERACTIVE: 28% queries vs 30% design (perfect)
    ✅ ANALYTICS: 8% queries vs 15% design (underutilized)
    ⚠️  AD_HOC: 3% resources vs 2% design (slightly over)
    ⚠️  DEFAULT: 2% queries vs <1% design (needs attention)

    SLA Compliance:
    ✅ PRODUCTION_HIGH: 0.8s avg (<1s target)
    ✅ INTERACTIVE: 4.2s p95 (<5s target)
    ✅ ETL_BATCH: 3.5hrs window (<4hrs target)

    Issues Found:
    1. DEFAULT workload higher than design (2% vs <1%):
       → Root cause: NEW_BI_TOOL not classified
       → ACTION: Create filter for NEW_BI_TOOL

    2. AD_HOC using more resources than design (3% vs 2%):
       → Ad-hoc queries running longer than expected
       → ACTION: Review slow ad-hoc queries, consider optimization

    3. ANALYTICS underutilized (8% vs 15% design):
       → Less analytics usage than projected
       → ACTION: No immediate action, monitor trend

    Recommendations:
    - Fix DEFAULT classification issue (Priority 1)
    - Investigate AD_HOC resource usage (Priority 2)
    - Update design docs to reflect ANALYTICS lower usage (Priority 3)
    - Overall workload management is effective, minor tuning needed"
```

**Result**: Comprehensive design validation with prioritized actions

---

## Best Practices

### Resource-First Approach (NEW ✨)
- **START with resources** for instant workload overview (`tdwm://system/workloads`)
- Resources provide real-time snapshot without adding system load
- Use tools for detailed analysis and historical data
- Combine resources + tools for complete picture

### Workload Inventory Management
- Active workloads define current system behavior - verify they match intent
- Inactive workloads should be documented (seasonal, emergency, retired)
- DEFAULT workload should have minimal traffic (<5% queries, <1% resources)
- Workload names should clearly indicate purpose and priority

### Distribution Analysis
- Workload distribution should align with business priorities
- Compare actual distribution against design/SLA targets
- High DEFAULT workload usage indicates classification problems
- Resource % should roughly match priority rankings

### TASM Effectiveness Monitoring
- Monitor TASM statistics regularly to catch rule issues early
- Target: >95% classification rate (queries not in DEFAULT)
- High exception counts indicate classification problems
- Track TASM statistics over time to identify trends

### Configuration Discovery (NEW ✨)
- Use MCP resources to explore filters and throttles per workload
- Verify each workload has both filter (routing) and throttle (protection)
- Check classification criteria match expected query patterns
- Validate throttle limits against actual concurrency needs

### Classification Troubleshooting
- DEFAULT workload is the catch-all - investigate why queries land there
- Use TASM event history to understand classification decisions
- Verify query bands are being set by applications
- Check filter criteria match actual query band values

### SLA Validation
- Document SLA targets for each workload
- Regularly compare actual performance against SLA targets
- Use query logs to calculate response time percentiles
- Alert on SLA violations

### Related Skills
- Use **tune-workloads** skill to fix classification issues
- Use **manage-workloads** skill to create filters/throttles for workloads
- Use **optimize-throttles** skill to adjust throttle limits
- Use **discover-configuration** skill for systematic configuration audit
- Use **monitor-queries** skill to correlate query patterns with workloads
