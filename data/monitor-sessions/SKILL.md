---
name: monitor-sessions
description: Monitor active Teradata sessions using real-time resources, view SQL execution details, identify blocking issues, and optionally take control actions
---

# Monitor Sessions

Monitor and analyze active sessions in the Teradata database system to identify performance issues, blocking problems, and resource consumption patterns using real-time MCP resources and tools.

## 🔍 Enhanced Capabilities

**This skill now leverages real-time MCP resources for faster monitoring!**

With tdwm-mcp v1.5.0, this skill provides:
- ✅ **REAL-TIME RESOURCES** - Instant session data without running queries
- ✅ **SQL TEXT VISIBILITY** - View query text and execution steps
- ✅ **BLOCKING DETECTION** - Identify lock chains and contention
- ✅ **CONTROL ACTIONS** - Optional session termination when needed
- ✅ **INTEGRATED CONTEXT** - Sessions + workload + resource data in one view

## Instructions

### When to Use This Skill
- User asks to check active sessions or current database activity
- Need to identify who is running what queries
- Investigating performance issues or blocked sessions
- Monitoring specific user activity
- Response to complaints about slow queries or system unresponsiveness

### Available MCP Tools

**Session Monitoring:**
- `list_sessions` - List all active user sessions with details
- `show_session_sql_text` - View full SQL text for specific session
- `show_session_sql_steps` - View execution steps for session query
- `monitor_session_query_band` - View query band settings for sessions
- `identify_blocking` - Identify sessions blocking other sessions

**Control Actions (Optional):**
- `abort_sessions_user` - Terminate all sessions for a specific user

**Related Monitoring:**
- `show_tdwm_summary` - View workload distribution (context for sessions)
- `show_query_log` - Historical query analysis

### Available MCP Resources (NEW ✨)

**Real-Time Session Data:**
- `tdwm://system/sessions` - Real-time snapshot of all active sessions
- `tdwm://system/summary` - Workload distribution showing session context
- `tdwm://system/workloads` - Active workloads (to understand session classification)

**Query Analysis:**
- `tdwm://system/delayed-queries` - Sessions waiting in delay queues
- `tdwm://system/throttle-statistics` - Throttle impact on sessions

**Reference:**
- `tdwm://reference/session-states` - Explanation of session states
- `tdwm://reference/blocking-types` - Types of blocking scenarios

### Step-by-Step Workflow

#### Phase 1: Quick Assessment (Use Resources First)

1. **Get Real-Time Session Overview**
   - Read resource: `tdwm://system/sessions`
   - Provides instant snapshot of all active sessions
   - Review session count, usernames, current states
   - Identify sessions of interest (long-running, high CPU, blocked)

2. **Understand Workload Context**
   - Read resource: `tdwm://system/summary`
   - Shows how sessions are distributed across workloads
   - Identifies which workloads are busy
   - Provides system-wide context

#### Phase 2: Detailed Analysis (Use Tools)

3. **List Active Sessions**
   - Use `list_sessions` for detailed, sortable session data
   - Review session IDs, usernames, runtime, CPU time, I/O
   - Filter by user, state, or runtime criteria
   - Identify sessions requiring deeper investigation

4. **Examine Session SQL**
   - For suspicious or long-running sessions:
     - Use `show_session_sql_text` to see full query text
     - Use `show_session_sql_steps` to see execution steps
   - Analyze query complexity and optimization
   - Check if queries match expected workload patterns

5. **Check for Blocking**
   - Use `identify_blocking` to find lock contention
   - Identify both blocking and blocked sessions
   - Document blocking chains (Session A blocks B blocks C)
   - Determine if blocking is normal (brief) or problematic (long)

6. **Review Query Bands**
   - Use `monitor_session_query_band` to see session tags
   - Verify queries are properly classified
   - Check if query bands match expected application

#### Phase 3: Analysis and Reporting

7. **Correlate Session Data**
   - Cross-reference sessions with workload summary
   - Check if throttles are delaying sessions (resource: `tdwm://system/throttle-statistics`)
   - Identify patterns: multiple users, same application, similar queries

8. **Provide Recommendations**
   - Summarize active session count and patterns
   - Highlight problematic sessions (blocking, long-running, high resource)
   - Provide session IDs and usernames for follow-up
   - Recommend actions: optimize query, adjust workload, abort session

#### Phase 4: Control Actions (Optional)

9. **Take Action if Needed**
   - **For runaway queries**: Consider using `abort_sessions_user`
   - **For blocking issues**: Identify which session to terminate
   - **Emergency situations**: Act quickly to restore service
   - **Always document**: Record what was terminated and why

## Examples

### Example 1: Quick Session Check Using Resources (Fast)

**Scenario**: "Show me what's currently running on the database"

**Action** (Resource-First Approach):
```
1. Read real-time sessions:
   tdwm://system/sessions
   → Instant snapshot: 47 active sessions

2. Analyze resource data:
   - 23 sessions in ETL workload (expected for this time)
   - 15 sessions in INTERACTIVE workload
   - 9 sessions in DEFAULT workload
   - Most sessions <5 minutes runtime (normal)
   - 2 sessions running >30 minutes (investigate)

3. Get workload context:
   tdwm://system/summary
   → ETL workload using 60% of resources
   → Interactive workload using 30%
   → System healthy, no overload

4. Report:
   "47 active sessions, system healthy. ETL workload dominant (expected).
    2 long-running sessions (ID 1234, 5678) worth monitoring."
```

**Result**: Complete overview in seconds without running any queries

---

### Example 2: Investigate Specific User (Detailed)

**Scenario**: "What is user john_smith doing right now?"

**Action** (Resource + Tool Approach):
```
1. Check resource first:
   tdwm://system/sessions
   → Filter for user='john_smith'
   → Found 3 active sessions: 1245, 1246, 1247

2. Get detailed session data:
   list_sessions()
   → Filter output for john_smith
   → Session 1245: Running 45 minutes, high CPU
   → Session 1246: Running 2 minutes, normal
   → Session 1247: Idle, 0 CPU

3. Examine long-running session 1245:
   show_session_sql_text(session_id=1245)
   → Query: Large aggregation on fact table
   → No obvious optimization issues

   show_session_sql_steps(session_id=1245)
   → Currently in step 5 of 8
   → Doing JOIN operation
   → No blocking detected

4. Check query band:
   monitor_session_query_band()
   → Filter for session 1245
   → Query band: APP=ANALYTICS_TOOL, USER=john_smith
   → Classified in ANALYTICS workload (correct)

5. Report:
   "john_smith has 3 sessions:
    - Session 1245: Long-running analytics query (45 min), progressing normally
    - Session 1246: Recent query, completing soon
    - Session 1247: Idle connection

    No issues detected. Long query is expected for analytics workload."
```

**Result**: Complete user activity profile with context

---

### Example 3: Diagnose Blocking Issues (Critical)

**Scenario**: "Some queries seem stuck, check for blocking"

**Action** (Blocking Analysis):
```
1. Quick resource check:
   tdwm://system/sessions
   → 12 sessions in "blocked" state
   → Multiple sessions waiting on locks

2. Identify blocking chains:
   identify_blocking()
   → Blocking detected!
   → Session 2001 (user: etl_batch) is blocking 8 sessions
   → Session 2050 (user: report_user) is blocking 4 sessions

3. Analyze blocking session 2001:
   show_session_sql_text(session_id=2001)
   → UPDATE statement on CUSTOMER table
   → Has been running for 90 minutes
   → Holding exclusive table lock

   list_sessions()
   → Filter for session 2001
   → Started at 02:00 AM (ETL window)
   → Should have completed by now

4. Check blocked sessions:
   list_sessions()
   → Filter for blocked sessions
   → All trying to SELECT from CUSTOMER table
   → Waiting for lock release
   → Users complaining about reports not loading

5. Analyze second blocker (session 2050):
   show_session_sql_text(session_id=2050)
   → Long-running report query
   → Holding shared lock, blocking UPDATE attempts

6. Review reference:
   tdwm://reference/blocking-types
   → Scenario: ETL update blocking reports = Type 1 blocking
   → Recommendation: Complete ETL or abort if stuck

7. Report:
   "BLOCKING DETECTED - 12 sessions blocked:

    Primary blocker: Session 2001 (etl_batch)
    - Running 90 minutes (abnormally long)
    - UPDATE on CUSTOMER table
    - Blocking 8 report sessions
    - RECOMMENDATION: Check if ETL is stuck, may need to abort

    Secondary blocker: Session 2050 (report_user)
    - Long-running report (60 min)
    - Blocking 4 UPDATE attempts
    - RECOMMENDATION: Let complete or optimize query

    IMMEDIATE ACTION NEEDED for Session 2001"
```

**Result**: Clear identification of blocking issues with recommendations

---

### Example 4: Emergency Session Termination (Control Action)

**Scenario**: "User adhoc_user01 is running runaway queries, kill all their sessions"

**Action** (Control Action):
```
1. Verify problem first:
   tdwm://system/sessions
   → User adhoc_user01 has 15 active sessions
   → All running identical query
   → System CPU at 95% (critical)

2. Get detailed view:
   list_sessions()
   → Filter for adhoc_user01
   → 15 sessions, each using 6% CPU
   → Total: 90% of system CPU
   → All started within 5 minutes (query blast)

3. Check query:
   show_session_sql_text(session_id=3001)  # Pick one session
   → SELECT with CROSS JOIN (Cartesian product!)
   → Missing WHERE clause
   → Generating billions of rows

4. Confirm termination decision:
   - Runaway query confirmed
   - No business justification for Cartesian product
   - System critically overloaded
   - User needs to be stopped

5. Execute termination:
   abort_sessions_user(username="adhoc_user01")
   → Terminating all 15 sessions for adhoc_user01
   → Result: "15 sessions terminated"

6. Monitor recovery:
   tdwm://system/summary
   → Wait 30 seconds
   → CPU dropping from 95% to 45%
   → System recovering

7. Document incident:
   "Emergency termination of adhoc_user01 sessions at 14:23:
    - 15 runaway queries with Cartesian product
    - Consuming 90% of system CPU
    - Missing WHERE clause in query
    - System returned to normal after termination
    - User notified to fix query before resubmitting"
```

**Result**: System stabilized, incident documented

---

### Example 5: Routine Session Audit (Proactive)

**Scenario**: Daily morning check of overnight session activity

**Action** (Comprehensive Audit):
```
1. Get high-level overview:
   tdwm://system/summary
   → 34 active sessions (normal for 8 AM)
   → ETL workload: 12 sessions
   → Interactive: 18 sessions
   → Ad-hoc: 4 sessions

2. Check real-time sessions:
   tdwm://system/sessions
   → No sessions running >2 hours (good)
   → No blocked sessions
   → Resource usage balanced

3. Review delayed queries:
   tdwm://system/delayed-queries
   → 3 queries in delay queue (acceptable)
   → All from ad-hoc workload (expected throttling)

4. Check throttle statistics:
   tdwm://system/throttle-statistics
   → ETL throttle: 0 delayed (nighttime processing complete)
   → Ad-hoc throttle: 3 delayed (working as designed)
   → Interactive throttle: 0 delayed (good performance)

5. List all sessions for record:
   list_sessions()
   → Full session inventory captured
   → No anomalies detected

6. Check for any blocking:
   identify_blocking()
   → No blocking detected

7. Report:
   "Morning session audit - 8:00 AM:
    ✅ 34 active sessions (normal)
    ✅ No blocking issues
    ✅ No long-running sessions (all <2 hours)
    ✅ Throttles working as expected
    ✅ System healthy

    Overnight ETL completed successfully.
    Interactive users beginning morning queries.
    No issues requiring attention."
```

**Result**: Clean bill of health, documented baseline

---

## Best Practices

### Resource-First Approach (NEW ✨)
- **START with resources** for instant overview (`tdwm://system/sessions`)
- Resources are faster than running queries
- Use tools for detailed analysis only when needed
- Resources provide point-in-time snapshot

### Investigation Workflow
- Always start with system-wide view before drilling into specifics
- Cross-reference session data with workload summary for context
- Document session IDs prominently for easy reference
- Consider time of day and expected workload patterns

### Blocking Analysis
- Check for blocking proactively during performance investigations
- Analyze blocking chains to find root cause (first blocker)
- Understand business impact (how many users affected)
- Distinguish normal brief locks from problematic long locks

### Control Actions
- **ONLY abort sessions when necessary** (runaway queries, system emergency)
- Always document what was terminated and why
- Notify users when their sessions are terminated
- Consider less drastic options first (throttling, priority adjustment)

### Session State Understanding
- Reference `tdwm://reference/session-states` for state meanings
- "Active" = currently executing
- "Blocked" = waiting on lock
- "Idle" = connected but not executing

### Monitoring Frequency
- Critical systems: Check every 15-30 minutes
- Normal systems: Check 2-3 times per day
- Always check during peak hours (morning, midday)
- Set up alerts for blocking or long-running sessions

### Related Skills
- Use **monitor-queries** skill for historical query analysis
- Use **control-sessions** skill for detailed session management
- Use **monitor-resources** skill for CPU/memory/I/O correlation
- Use **emergency-response** skill for crisis situations
