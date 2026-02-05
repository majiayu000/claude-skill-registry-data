---
name: monitor-resources
description: Monitor AMP processor load, system physical resources, and capacity using real-time resources to track system health and identify performance bottlenecks
---

# Monitor Resources

Monitor system-level resources including AMP processors, CPU, memory, I/O, and physical capacity using real-time MCP resources to ensure optimal system performance and identify capacity constraints.

## 🔍 Enhanced Capabilities

**This skill now leverages real-time resource monitoring!**

With tdwm-mcp v1.5.0, this skill provides:
- ✅ **REAL-TIME RESOURCE METRICS** - Instant CPU/memory/I/O data without overhead
- ✅ **AMP LOAD MONITORING** - Track processor utilization and skew
- ✅ **CAPACITY ANALYSIS** - Understand headroom and growth runway
- ✅ **TOP CONSUMER IDENTIFICATION** - Find users/queries consuming most resources
- ✅ **INTEGRATED VIEW** - Resources + sessions + queries in one analysis

## Instructions

### When to Use This Skill
- User asks about system performance or capacity
- Need to check if system is overloaded or underutilized
- Investigating resource bottlenecks or performance degradation
- Capacity planning or health check requests
- Correlating resource usage with query performance

### Available MCP Tools

**Resource Monitoring:**
- `monitor_amp_load` - Track AMP processor utilization and skew
- `monitor_awt` - View AWT task resource usage
- `show_top_users` - Identify users consuming most resources
- `monitor_config` - View system configuration parameters

**Related Monitoring:**
- `list_sessions` - See sessions consuming resources
- `show_tdwm_summary` - Workload distribution context
- `list_resources` - List available system resources

### Available MCP Resources (NEW ✨)

**Real-Time Resource Data:**
- `tdwm://system/physical-resources` - CPU, memory, I/O utilization
- `tdwm://system/amp-load` - AMP processor load and skew metrics
- `tdwm://system/sessions` - Session resource consumption
- `tdwm://system/summary` - Workload resource distribution

**Reference:**
- `tdwm://reference/resource-thresholds` - Healthy vs warning vs critical levels
- `tdwm://reference/amp-skew-causes` - Common causes of AMP skew

### Step-by-Step Workflow

#### Phase 1: Quick Assessment (Use Resources First)

1. **Get Real-Time Resource Overview**
   - Read resource: `tdwm://system/physical-resources`
   - Instant snapshot of CPU, memory, I/O utilization
   - Identify if system is under stress
   - Provides capacity headroom visibility

2. **Check AMP Load Balance**
   - Read resource: `tdwm://system/amp-load`
   - Shows AMP processor utilization
   - Identifies load skew (imbalance)
   - Provides per-AMP breakdown

#### Phase 2: Detailed Analysis (Use Tools)

3. **Assess Overall System Load**
   - Use `monitor_amp_load` for detailed AMP processor data
   - Identify if system is CPU-bound or has capacity
   - Look for imbalanced load across AMPs (skew factor)
   - Track peak vs average utilization

4. **Check Task-Level Resources**
   - Use `monitor_awt` to view AWT task allocation
   - Identify if task slots are exhausted
   - Check for queries waiting on resources
   - Understand task concurrency limits

5. **Identify Top Consumers**
   - Use `show_top_users` to find resource-heavy users/queries
   - Determine if resource usage is legitimate or problematic
   - Prioritize optimization efforts
   - Correlate with session and query data

6. **Review System Configuration**
   - Use `monitor_config` to verify system settings
   - Check resource allocation parameters
   - Validate configuration against best practices

#### Phase 3: Correlation and Reporting

7. **Correlate with Workload Activity**
   - Read resource: `tdwm://system/summary`
   - Correlate resource usage with workload distribution
   - Identify which workloads are consuming resources
   - Understand if usage patterns are expected

8. **Analyze Session Resource Consumption**
   - Read resource: `tdwm://system/sessions`
   - Identify individual sessions consuming excessive resources
   - Correlate high-resource sessions with users/queries
   - Determine if termination needed

9. **Report Findings**
   - Summarize system health: green (healthy), amber (warning), red (critical)
   - Identify bottlenecks or constraints
   - Provide utilization percentages and trends
   - Recommend actions if issues found

## Examples

### Example 1: Quick System Health Check (Fast)

**Scenario**: "Is the system running okay right now?"

**Action** (Resource-First Approach):
```
1. Read real-time physical resources:
   tdwm://system/physical-resources
   → CPU: 45% utilized (healthy)
   → Memory: 62% utilized (healthy)
   → I/O: 38% utilized (healthy)
   → Disk: 71% capacity used

2. Check AMP load balance:
   tdwm://system/amp-load
   → Average AMP CPU: 43%
   → Max AMP CPU: 51%
   → Min AMP CPU: 38%
   → Skew factor: 1.13 (healthy, < 1.5)

3. Review workload distribution:
   tdwm://system/summary
   → 47 active queries distributed across 3 workloads
   → Resources well-balanced

4. Report:
   "✅ System Health: HEALTHY

    Resource Utilization:
    - CPU: 45% (55% headroom available)
    - Memory: 62% (38% headroom available)
    - I/O: 38% (62% headroom available)
    - AMP Load: Balanced (skew factor 1.13)

    Current Activity:
    - 47 active queries, well-distributed
    - No resource bottlenecks detected
    - System has capacity for additional workload"
```

**Result**: Complete health check in seconds, clear green status

---

### Example 2: Investigate Performance Degradation (Critical)

**Scenario**: "Why are queries running slow? System feels sluggish."

**Action** (Resource Analysis):
```
1. Check physical resources:
   tdwm://system/physical-resources
   → CPU: 94% utilized (⚠️ CRITICAL)
   → Memory: 89% utilized (⚠️ WARNING)
   → I/O: 87% utilized (⚠️ WARNING)
   → All metrics in red zone

2. Check AMP load:
   tdwm://system/amp-load
   → Average AMP CPU: 92%
   → Max AMP CPU: 98%
   → Min AMP CPU: 76%
   → Skew factor: 1.29 (moderate skew)

3. Identify top consumers:
   show_top_users()
   → User: etl_batch - 42% of CPU
   → User: adhoc_user01 - 23% of CPU
   → User: report_user - 15% of CPU
   → Top 3 users = 80% of total CPU

4. Check sessions for top consumer:
   tdwm://system/sessions
   → Filter for etl_batch
   → 8 active sessions, all long-running (>30 min)
   → All from ETL workload

5. Review workload distribution:
   tdwm://system/summary
   → ETL workload: 67% of resources
   → Interactive workload: 23% of resources (suffering)
   → Ad-hoc workload: 10% of resources

6. Check for throttle delays:
   tdwm://system/delayed-queries
   → 15 queries delayed
   → 12 from Interactive workload (waiting for resources)
   → 3 from Ad-hoc workload

7. Report:
   "🔴 System Health: CRITICAL - Resource Exhaustion

    Root Cause:
    - System at 94% CPU capacity
    - ETL workload consuming 67% of resources
    - User 'etl_batch' alone using 42% of system CPU

    Impact:
    - Interactive queries delayed (12 queries waiting)
    - Average query time increased
    - System approaching capacity limit

    Immediate Actions Required:
    1. URGENT: Review etl_batch sessions (8 long-running queries)
       → Determine if queries are stuck or legitimately long
       → Consider aborting if runaway queries detected

    2. SHORT-TERM: Increase throttle on ETL workload
       → Limit ETL concurrent queries to protect Interactive
       → Use optimize-throttles skill

    3. MEDIUM-TERM: Schedule ETL jobs during off-peak hours
       → Current ETL running during business hours
       → Move to nighttime window if possible"
```

**Result**: Clear root cause identified, specific actions recommended with priority

---

### Example 3: Diagnose AMP Skew Issue (Performance)

**Scenario**: "Queries are slow even though CPU shows only 60% utilized"

**Action** (AMP Skew Analysis):
```
1. Check overall CPU:
   tdwm://system/physical-resources
   → CPU: 62% average (seems okay?)

2. Check AMP load detail:
   tdwm://system/amp-load
   → Average AMP CPU: 62%
   → Max AMP CPU: 95% (⚠️ AMP 7 maxed out!)
   → Min AMP CPU: 38%
   → Skew factor: 2.5 (🔴 SEVERE SKEW)

3. Analyze per-AMP breakdown:
   monitor_amp_load()
   → AMP 7: 95% (bottleneck!)
   → AMP 3: 89%
   → AMP 12: 87%
   → AMPs 1,2,4-6,8-11: 45-55% (normal)
   → AMPs 13-16: 38-42% (underutilized)

4. Identify queries hitting skewed AMPs:
   show_top_users()
   → User: report_generator - heavy queries
   → Queries accessing specific tables

5. Check session SQL:
   list_sessions()
   → Filter for report_generator
   → All queries accessing SALES_FACT table
   → Large table with potential distribution issue

6. Review reference:
   tdwm://reference/amp-skew-causes
   → Cause #1: Poor primary index design
   → Cause #2: NULL values in PI column
   → Cause #3: Hot values in PI column

7. Report:
   "⚠️  System Health: DEGRADED - AMP Skew Issue

    Problem:
    - System shows 62% average CPU (seems healthy)
    - BUT AMP 7 is at 95% (bottleneck!)
    - Skew factor 2.5 = SEVERE SKEW

    Impact:
    - Queries wait for overloaded AMP 7
    - 60% of AMPs underutilized
    - System effectively at 95% capacity (limited by one AMP)

    Root Cause Analysis:
    - Report queries all hitting SALES_FACT table
    - Table data concentrated on specific AMPs
    - Indicates poor primary index or data distribution

    Recommended Actions:
    1. IMMEDIATE: Review SALES_FACT table design
       → Check primary index column
       → Analyze data distribution (HELP STATISTICS)
       → Look for NULL values or hot keys

    2. SHORT-TERM: Consider table redistribution
       → Redesign primary index for better distribution
       → Test with EXPLAIN plans

    3. LONG-TERM: Implement data distribution monitoring
       → Regular skew checks
       → Alert on skew factor > 2.0"
```

**Result**: Identified hidden bottleneck (AMP skew), specific table and recommendations

---

### Example 4: Capacity Planning Analysis (Proactive)

**Scenario**: "Do we have capacity for 25% more users next quarter?"

**Action** (Capacity Planning):
```
1. Get current resource baseline:
   tdwm://system/physical-resources
   → CPU: 67% average (peak hours)
   → Memory: 74% average
   → I/O: 58% average
   → Disk: 68% capacity used

2. Analyze peak utilization (tool for historical data):
   monitor_amp_load()
   → Peak CPU (last 30 days): 85%
   → Average CPU (last 30 days): 52%
   → Peak typically 10:00 AM - 3:00 PM

3. Calculate current headroom:
   - CPU: 33% headroom at average, 15% at peak
   - Memory: 26% headroom
   - I/O: 42% headroom
   - Comfortable threshold: Keep peak < 80%

4. Project 25% user increase:
   - Assume linear scaling (conservative)
   - Current peak: 85%
   - With 25% more: 85% × 1.25 = 106% (🔴 OVER CAPACITY)

5. Analyze workload composition:
   tdwm://system/summary
   → Interactive: 45% of resources
   → ETL: 35% of resources
   → Ad-hoc: 20% of resources
   → User increase likely impacts Interactive + Ad-hoc

6. Recalculate with workload-specific growth:
   - Interactive/Ad-hoc: 65% of total, growing 25%
   - ETL: 35% of total, no growth
   - New peak: (65% × 1.25) + 35% = 81% + 35% = 116% (still over!)

7. Determine capacity gap:
   - Need: 116% capacity
   - Have: 100% capacity
   - Gap: 16% additional capacity needed
   - OR reduce peak utilization by optimizing queries

8. Report:
   "📊 Capacity Planning Analysis: 25% User Growth

    Current State:
    - Average: 67% CPU, 74% Memory
    - Peak: 85% CPU (10 AM - 3 PM)
    - Headroom at peak: 15%

    With 25% User Growth:
    - Projected peak: 106-116% CPU
    - Result: 🔴 INSUFFICIENT CAPACITY

    Capacity Gap:
    - Need: 16% additional capacity
    - Options to address:

    Option 1: Hardware Expansion
    - Add 2-3 nodes to cluster (20% capacity increase)
    - Cost: ~$X (hardware + licensing)
    - Timeline: 8-12 weeks

    Option 2: Query Optimization + Throttling
    - Optimize top 20 slow queries (target 15% improvement)
    - Adjust throttle limits to smooth peak load
    - Cost: Development time only
    - Timeline: 4-6 weeks
    - May achieve 10-15% efficiency gain

    Option 3: Hybrid Approach
    - Optimize queries (10% gain)
    - Add 1 node (10% capacity)
    - Adjust workload distribution
    - Cost: Partial hardware investment
    - Timeline: 6-8 weeks

    RECOMMENDATION:
    Start Option 2 immediately (query optimization), then reassess.
    If growth is certain, plan Option 1 in parallel (long lead time)."
```

**Result**: Detailed capacity analysis with multiple options and costs

---

### Example 5: Real-Time Resource Correlation (Advanced)

**Scenario**: "Why is I/O spiking even though CPU is only 50%?"

**Action** (Multi-Dimensional Analysis):
```
1. Confirm I/O spike:
   tdwm://system/physical-resources
   → CPU: 48% (normal)
   → Memory: 65% (normal)
   → I/O: 91% (🔴 CRITICAL spike!)

2. Check if AMP-related:
   tdwm://system/amp-load
   → AMP CPU: 45-52% across all AMPs (balanced)
   → No CPU bottleneck

3. Identify I/O-heavy sessions:
   list_sessions()
   → Sort by I/O consumption
   → Top session: analytics_user, session 5001
   → 67% of total I/O from this one session!

4. Get SQL for high-I/O session:
   show_session_sql_text(session_id=5001)
   → Query: Full table scan on 50TB fact table
   → No WHERE clause (scanning entire table!)
   → No indexes being used

5. Check query band:
   monitor_session_query_band()
   → Session 5001: APP=AD_HOC_ANALYTICS
   → Classified in Ad-hoc workload

6. Identify pattern:
   list_sessions()
   → Filter for AD_HOC_ANALYTICS application
   → 5 similar sessions, all doing large scans
   → All from same user: analytics_user

7. Calculate impact:
   - 5 sessions × 13-15% I/O each = 65-75% total I/O
   - Remainder (25-35%) from normal queries
   - Ad-hoc queries blocking I/O for other workloads

8. Report:
   "🔴 Resource Issue: I/O Bottleneck

    Problem:
    - I/O at 91% despite normal CPU (48%)
    - Type: I/O-bound, not CPU-bound

    Root Cause:
    - User 'analytics_user' running 5 concurrent full table scans
    - Each query scanning 50TB fact table
    - No WHERE clauses, no indexes
    - Consuming 65-75% of total system I/O

    Impact:
    - Other queries experiencing I/O delays
    - Reports taking 3-5x longer than normal
    - System I/O-bound, not CPU-bound

    Immediate Actions:
    1. URGENT: Abort analytics_user sessions
       → Use control-sessions skill
       → Free up I/O capacity immediately

    2. SHORT-TERM: Contact analytics_user
       → Queries need WHERE clauses
       → Should use summary tables, not raw fact table
       → Educate on query best practices

    3. MEDIUM-TERM: Create throttle for full table scans
       → Use optimize-throttles skill
       → Add FTSCAN sub-criteria to Ad-hoc throttle
       → Limit full scans to 2 concurrent

    4. LONG-TERM: Implement query governor
       → Reject queries scanning >X TB without approval
       → Enforce WHERE clause requirements"
```

**Result**: Identified I/O bottleneck root cause, multi-level action plan

---

## Best Practices

### Resource-First Approach (NEW ✨)
- **START with resources** for instant overview (`tdwm://system/physical-resources`)
- Resources are faster and don't add load to system
- Use tools for detailed analysis and historical data
- Combine resources + tools + session data for complete picture

### Multi-Dimensional Analysis
- Check multiple resource types - bottleneck may not be where expected
- CPU, memory, I/O, disk, AMP load, task slots - all matter
- Don't assume high CPU = performance issue (could be I/O, AMP skew, etc.)
- Correlate resources with workload and session activity

### AMP Skew Understanding
- AMP skew (imbalanced load) indicates data distribution issues
- Skew factor > 1.5 = warning, > 2.0 = critical
- Average CPU can look healthy while one AMP is maxed out
- Skew caused by: poor PI design, NULL values, hot keys, small tables

### Capacity Planning
- Establish baseline metrics for comparison
- Track peak vs average utilization (peak drives capacity needs)
- Monitor trends over time, not just point-in-time snapshots
- Consider both average and peak when planning capacity
- Factor in growth projections and seasonal patterns
- Keep peak utilization < 80% for headroom

### Health Status Thresholds (Reference: tdwm://reference/resource-thresholds)
- **Green (Healthy)**: < 70% average, < 80% peak
- **Amber (Warning)**: 70-85% average, 80-90% peak
- **Red (Critical)**: > 85% average, > 90% peak

### Correlation Best Practices
- Always correlate resources with workload distribution
- Identify which workloads/users are consuming resources
- Check if usage patterns are expected for time of day
- Look for anomalies: unexpected consumers, unusual patterns

### Related Skills
- Use **monitor-sessions** skill for session-level resource analysis
- Use **monitor-queries** skill to correlate queries with resource usage
- Use **control-sessions** skill to abort high-resource sessions
- Use **optimize-throttles** skill to manage resource consumption
- Use **emergency-response** skill for critical resource exhaustion
