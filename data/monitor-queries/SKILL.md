---
name: monitor-queries
description: Track query execution using real-time resources, analyze query bands, access query logs, and identify performance patterns across the Teradata system
---

# Monitor Queries

Track and analyze query execution patterns, query bands, and historical query performance to understand system workload characteristics and identify optimization opportunities using real-time MCP resources and tools.

## 🔍 Enhanced Capabilities

**This skill now leverages real-time query monitoring resources!**

With tdwm-mcp v1.5.0, this skill provides:
- ✅ **REAL-TIME QUERY TRACKING** - Instant query data without database overhead
- ✅ **QUERY BAND ANALYSIS** - Understand workload classification
- ✅ **HISTORICAL LOGS** - Analyze past query performance
- ✅ **TASM EVENT HISTORY** - Track classification decisions and delays
- ✅ **INTEGRATED METRICS** - Query performance + resource usage in one view

## Instructions

### When to Use This Skill
- User wants to analyze query performance trends
- Need to track queries by application or user type
- Investigating query patterns by query band
- Reviewing historical query execution
- Analyzing throttle delays and workload classification
- Identifying slow or resource-intensive queries

### Available MCP Tools

**Query Monitoring:**
- `list_query_band` - Display query bands by type (transaction, profile, session)
- `show_query_log` - Access historical query execution logs
- `list_sessions` - View currently executing queries (with session context)
- `show_session_sql_text` - Get SQL text for specific session
- `show_tasm_even_history` - Review TASM classification decisions

**Analysis:**
- `show_tdwm_summary` - Workload distribution context
- `show_tasm_statistics` - TASM rule effectiveness
- `show_trottle_statistics` - Throttle impact on queries
- `list_delayed_request` - Queries in delay queue

### Available MCP Resources (NEW ✨)

**Real-Time Query Data:**
- `tdwm://system/sessions` - Active queries (part of session data)
- `tdwm://system/delayed-queries` - Queries waiting in delay queues
- `tdwm://system/summary` - Query distribution across workloads
- `tdwm://system/throttle-statistics` - Throttle delays per workload

**Historical Analysis:**
- Query logs accessed via `show_query_log` tool
- TASM events accessed via `show_tasm_even_history` tool

**Reference:**
- `tdwm://reference/query-states` - Query execution states
- `tdwm://reference/delay-reasons` - Why queries are delayed

### Step-by-Step Workflow

#### Phase 1: Quick Assessment (Use Resources First)

1. **Get Real-Time Query Overview**
   - Read resource: `tdwm://system/summary`
   - Shows query distribution across workloads
   - Identifies which workloads are active
   - Provides high-level throughput metrics

2. **Check Delayed Queries**
   - Read resource: `tdwm://system/delayed-queries`
   - Shows queries waiting in throttle queues
   - Identifies which workloads are experiencing delays
   - Provides wait time metrics

#### Phase 2: Detailed Analysis (Use Tools)

3. **Understand Query Classification**
   - Use `list_query_band` to see how queries are tagged
   - Review transaction, profile, and session-level query bands
   - Identify workload categories and application tagging
   - Verify query bands match expected patterns

4. **Analyze Current Query Activity**
   - Use `list_sessions` to see active queries
   - Group queries by band, user, or application
   - Identify patterns in query types and complexity
   - Check for runaway or long-running queries

5. **Review Historical Performance**
   - Use `show_query_log` for past query execution data
   - Analyze execution times, resource consumption, frequency
   - Identify trends, outliers, or degrading performance
   - Compare current vs historical patterns

6. **Analyze TASM Classification**
   - Use `show_tasm_even_history` to see classification decisions
   - Understand why queries landed in specific workloads
   - Identify misclassification issues
   - Track rule effectiveness

#### Phase 3: Performance Investigation

7. **Identify Throttle Impact**
   - Read resource: `tdwm://system/throttle-statistics`
   - Use `show_trottle_statistics` tool for details
   - Identify which workloads are being throttled
   - Calculate average delay times

8. **Find Slow Queries**
   - Use `show_query_log` sorted by execution time
   - Identify top slow queries by workload
   - Get SQL text using `show_session_sql_text`
   - Analyze query complexity and optimization opportunities

9. **Track Application Workload**
   - Filter queries by query band (application)
   - Calculate throughput, average execution time
   - Compare against SLA targets
   - Identify deviations from baseline

## Examples

### Example 1: Quick Query Distribution Check (Fast)

**Scenario**: "Show me current query activity across workloads"

**Action** (Resource-First Approach):
```
1. Read workload summary:
   tdwm://system/summary
   → ETL workload: 45 queries, 60% of resources
   → Interactive: 23 queries, 30% of resources
   → Ad-hoc: 8 queries, 10% of resources
   → DEFAULT: 3 queries (misclassified?)

2. Check delayed queries:
   tdwm://system/delayed-queries
   → 5 queries in delay queue
   → 4 from Ad-hoc workload (expected throttling)
   → 1 from Interactive workload (investigate?)

3. Review throttle statistics:
   tdwm://system/throttle-statistics
   → Ad-hoc throttle: 4 delayed (limit=5)
   → Interactive throttle: 1 delayed (limit=15, unusual)
   → ETL throttle: 0 delayed (limit=20)

4. Report:
   "Current query activity:
    - 79 total queries across 4 workloads
    - ETL dominant (45 queries, 60% resources) - expected
    - 5 queries delayed by throttles - mostly ad-hoc (working as designed)
    - 1 interactive query delayed (unusual, may need investigation)
    - 3 queries in DEFAULT workload (check classification)"
```

**Result**: Complete query overview in seconds, identified 2 areas to investigate

---

### Example 2: Find Slow Queries (Historical Analysis)

**Scenario**: "Which queries ran slowly in the last hour?"

**Action** (Historical + Tool Approach):
```
1. Query historical logs:
   show_query_log(time_range="last_1_hour", sort_by="duration_desc")
   → 247 queries executed in last hour
   → Top 10 by duration shown

2. Analyze top slow queries:
   Query #1: 45 minutes, user=etl_batch, workload=ETL
   Query #2: 32 minutes, user=report_user, workload=Interactive
   Query #3: 28 minutes, user=adhoc_user, workload=Ad-hoc
   ... (7 more)

3. Get SQL text for top slow query:
   show_session_sql_text(query_id=12345)  # If still running
   → Or query log contains SQL text
   → Query: Complex multi-table join with aggregation
   → 5 table joins, full table scans detected

4. Check query bands:
   list_query_band(type="TRANSACTION")
   → Top slow query #1: APP=ETL_NIGHTLY_BATCH
   → Top slow query #2: APP=EXECUTIVE_DASHBOARD
   → Top slow query #3: No query band set (ad-hoc tool)

5. Analyze patterns:
   - ETL query (45 min): Expected for nightly batch
   - Report query (32 min): Longer than usual, may need optimization
   - Ad-hoc query (28 min): No query band, running in Ad-hoc workload

6. Report:
   "Slow queries in last hour:

    Top 10 queries ranged from 15-45 minutes:
    - 4 ETL queries: 25-45 min (expected for batch processing)
    - 3 Interactive queries: 18-32 min (1 slower than baseline)
    - 3 Ad-hoc queries: 15-28 min (acceptable for ad-hoc)

    RECOMMENDATION:
    - Query #2 (Executive Dashboard, 32 min) normally runs in 15 min
      → Investigate query plan changes or data volume increase
    - Query #3 (Ad-hoc, 28 min) has no query band
      → User should set query band for better classification"
```

**Result**: Identified specific slow queries with actionable recommendations

---

### Example 3: Analyze Application Workload (ETL Performance)

**Scenario**: "How is the ETL application performing today?"

**Action** (Application-Specific Analysis):
```
1. Get real-time ETL query count:
   tdwm://system/summary
   → ETL workload: 45 active queries

2. Check query bands for ETL:
   list_query_band(type="TRANSACTION")
   → Filter for APP=ETL_*
   → Found query bands:
     - ETL_NIGHTLY_BATCH (23 queries)
     - ETL_INCREMENTAL (15 queries)
     - ETL_VALIDATION (7 queries)

3. Query historical ETL performance:
   show_query_log(
     filter_by_query_band="ETL_*",
     time_range="today"
   )
   → 342 ETL queries completed today
   → Average execution time: 8.5 minutes
   → Baseline average: 7.2 minutes (↑ 18% slower)

4. Identify ETL bottlenecks:
   show_query_log(
     filter_by_query_band="ETL_*",
     sort_by="duration_desc"
   )
   → Top 5 slow ETL queries: 45, 42, 38, 35, 32 minutes
   → All from ETL_NIGHTLY_BATCH workload
   → All started between 02:00-03:00 AM

5. Check for throttle delays:
   show_trottle_statistics(type="WORKLOAD")
   → ETL workload: 12 queries delayed today
   → Average delay: 3.2 minutes
   → Total delay time: 38 minutes

6. Review TASM classification:
   show_tasm_even_history(workload="ETL")
   → All ETL queries correctly classified
   → No misclassification issues

7. Report:
   "ETL Application Performance Today:

    Volume:
    - 342 completed queries, 45 currently active
    - 3 sub-applications: NIGHTLY_BATCH, INCREMENTAL, VALIDATION

    Performance:
    - Average: 8.5 min (↑18% from 7.2 min baseline)
    - Top 5 slow: 32-45 minutes (NIGHTLY_BATCH workload)
    - 12 queries throttled, avg delay 3.2 min (acceptable)

    Analysis:
    - Slowdown started in 02:00-03:00 AM window
    - All queries correctly classified
    - Possible causes:
      → Data volume increase
      → System resource contention during that window
      → Concurrent ETL jobs competing

    RECOMMENDATION:
    - Review data volume trends for NIGHTLY_BATCH
    - Consider staggering batch job start times
    - Monitor resource utilization during 02:00-03:00 window"
```

**Result**: Comprehensive ETL performance analysis with specific recommendations

---

### Example 4: Investigate Query Classification Issues

**Scenario**: "Why are some queries landing in DEFAULT workload?"

**Action** (Classification Analysis):
```
1. Check DEFAULT workload queries:
   tdwm://system/summary
   → DEFAULT workload: 8 queries (should be minimal)

2. Get query bands for DEFAULT queries:
   list_query_band(type="SESSION")
   → Filter for sessions in DEFAULT workload
   → 5 queries: No query band set
   → 3 queries: Query band = APP=NEW_BI_TOOL

3. Review TASM classification history:
   show_tasm_even_history(workload="DEFAULT")
   → Last 50 events show:
     - 62% "No matching rule" (no query band)
     - 38% "Rule evaluation failed" (NEW_BI_TOOL not in any filter)

4. Check existing filters:
   tdwm://ruleset/Tactical/filters
   → ETL_FILTER: Matches APP=ETL_*
   → INTERACTIVE_FILTER: Matches APP=DASHBOARD_*
   → ANALYTICS_FILTER: Matches APP=ANALYTICS_*
   → No filter matches APP=NEW_BI_TOOL

5. Identify users:
   list_sessions()
   → Filter for DEFAULT workload
   → 5 queries from adhoc_users (expected - no query band)
   → 3 queries from bi_power_users (unexpected - new tool)

6. Report:
   "DEFAULT Workload Analysis:

    Root Causes:
    1. Ad-hoc users (5 queries) not setting query bands
       → EXPECTED: Ad-hoc tools often don't set query bands
       → ACTION: None needed, or educate users to set manually

    2. New BI tool (3 queries) sets query band 'NEW_BI_TOOL'
       → UNEXPECTED: No filter matches this query band
       → ACTION REQUIRED: Create filter to route NEW_BI_TOOL queries

    RECOMMENDATION:
    Use tune-workloads skill to add classification for NEW_BI_TOOL:
    - Add APPL classification to appropriate filter
    - Route to INTERACTIVE or dedicated BI workload
    - Activate changes to fix classification"
```

**Result**: Root cause identified, specific action recommended

---

### Example 5: Track Query Volume Trends (Capacity Planning)

**Scenario**: "Is query volume increasing over time?"

**Action** (Trend Analysis):
```
1. Query volume for last 7 days:
   show_query_log(time_range="last_7_days", group_by="day")
   → Day 1 (Mon): 1,245 queries
   → Day 2 (Tue): 1,289 queries
   → Day 3 (Wed): 1,312 queries
   → Day 4 (Thu): 1,356 queries
   → Day 5 (Fri): 1,401 queries
   → Day 6 (Sat): 892 queries (weekend)
   → Day 7 (Sun): 856 queries (weekend)

2. Break down by workload:
   show_query_log(time_range="last_7_days", group_by="workload,day")
   → ETL workload: Flat (~500 queries/day)
   → Interactive workload: Growing (+15% week-over-week)
   → Ad-hoc workload: Growing (+8% week-over-week)

3. Check average execution times:
   show_query_log(time_range="last_7_days", group_by="workload", calc="avg_duration")
   → ETL: 8.5 min (baseline: 7.2 min, ↑18%)
   → Interactive: 2.3 min (baseline: 1.8 min, ↑28%)
   → Ad-hoc: 5.4 min (baseline: 4.9 min, ↑10%)

4. Calculate capacity usage trend:
   - Week 1: ~1,100 queries/day avg (weekday)
   - Week 2 (current): ~1,340 queries/day avg (weekday)
   - Growth rate: +22% in one week

5. Project future capacity:
   - If 22%/week growth continues:
     → 2 weeks: ~1,635 queries/day
     → 4 weeks: ~2,450 queries/day
   - Current system handles ~1,500 queries/day comfortably
   - Approaching capacity limit

6. Report:
   "Query Volume Trend Analysis:

    Current State:
    - Weekday avg: 1,340 queries/day (↑22% from last week)
    - Weekend avg: 874 queries/day (stable)
    - Interactive workload driving growth (+15% week-over-week)

    Performance Impact:
    - All workloads showing increased execution times
    - Interactive workload most affected (+28% avg execution time)
    - Indicates system approaching capacity

    Capacity Projection:
    - At current growth rate, will exceed comfortable capacity in 3-4 weeks
    - Interactive workload is primary growth driver

    RECOMMENDATIONS:
    1. IMMEDIATE: Review throttle limits for Interactive workload
    2. SHORT-TERM: Optimize top slow Interactive queries
    3. MEDIUM-TERM: Plan capacity expansion (hardware or Cloud Expansion)
    4. LONG-TERM: Implement query governance for Interactive workload"
```

**Result**: Clear trend analysis with timeline and recommendations

---

## Best Practices

### Resource-First Approach (NEW ✨)
- **START with resources** for instant overview (`tdwm://system/summary`)
- Resources provide real-time snapshot without database overhead
- Use tools for historical analysis and detailed investigation
- Combine resources + tools for complete picture

### Query Band Understanding
- Query bands are key to workload classification - understand them first
- Transaction bands (per-query) take precedence over session bands
- Profile bands are rarely used, focus on transaction and session
- Applications should set query bands consistently

### Historical Analysis
- Use appropriate time ranges to avoid overwhelming data
- Look for both averages and outliers when analyzing performance
- Compare current metrics against baselines
- Track trends over time (day-over-day, week-over-week)

### Classification Investigation
- Queries in DEFAULT workload indicate classification issues
- Use TASM event history to understand why queries landed in specific workloads
- Verify query bands match filter criteria
- Check for missing or misconfigured filters

### Performance Patterns
- Correlate query patterns with business processes (ETL, reporting, ad-hoc)
- Consider day-of-week and time-of-day patterns
- Identify peak usage windows
- Track query volume trends to predict capacity needs

### Throttle Impact Analysis
- Delayed queries indicate throttle limits are working
- Excessive delays may indicate limits are too restrictive
- Zero delays may indicate throttles are too loose
- Balance throughput vs resource protection

### Related Skills
- Use **monitor-sessions** skill for real-time session analysis
- Use **analyze-performance** skill for detailed query optimization
- Use **tune-workloads** skill to fix classification issues
- Use **optimize-throttles** skill to adjust throttle limits
