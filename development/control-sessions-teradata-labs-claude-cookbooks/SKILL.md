---
name: control-sessions
description: Control active sessions by terminating problematic sessions, managing runaway queries, and handling blocking situations
---

# Control Sessions

Manage and control active database sessions including terminating runaway queries, resolving blocking situations, and handling problematic sessions to maintain system health.

## Instructions

### When to Use This Skill
- Runaway query consuming excessive resources
- Session is blocking critical work
- User requests to kill their own stuck session
- Emergency situation requires immediate session termination
- Unresponsive or hung sessions need cleanup

### Available MCP Tools
- `show_sessions` - View all active sessions
- `show_sql` - Review SQL for specific session
- `terminate_session` - Kill a specific session
- `detect_blocking` - Identify blocking sessions
- `show_top_consumers` - Find resource-heavy sessions

### Step-by-Step Workflow

1. **Identify Problem Sessions**
   - Use `show_sessions` to see all active sessions
   - Use `show_top_consumers` to find resource-heavy sessions
   - Use `detect_blocking` if blocking is suspected
   - Review runtime, resource usage, and state

2. **Investigate Session Activity**
   - Use `show_sql` to see what the session is doing
   - Determine if activity is legitimate or problematic
   - Check session history if available
   - Contact user if unclear whether to terminate

3. **Assess Impact**
   - **Before terminating**, consider:
     - Is this a critical business process?
     - Will termination cause data corruption?
     - Can the user restart easily?
     - Are there dependent processes?
   - Check if less disruptive alternatives exist

4. **Determine Action**

   **Terminate When:**
   - Runaway query with no business value
   - Session is blocking critical work and won't complete soon
   - User confirms session can be killed
   - Session is hung/unresponsive
   - Resource consumption threatens system stability

   **Don't Terminate When:**
   - Critical ETL or batch process (unless truly stuck)
   - Near completion of long-running legitimate work
   - Unsure of impact - investigate further first
   - Alternative solutions available (release queue, wait, etc.)

5. **Execute Termination**
   - Document reason for termination
   - Use `terminate_session` with session ID
   - Verify session actually terminates
   - Monitor for any cascade effects

6. **Follow Up**
   - Notify user of termination and reason
   - Help user restart if needed
   - Investigate why session became problematic
   - Implement preventive measures if pattern exists

## Examples

### Example 1: Kill Runaway Query
```
User: "There's a query using 90% CPU for hours, please kill it"

Action:
1. Use show_top_consumers to identify the session
2. Call show_sql to see the query
3. Verify it's actually problematic (not critical batch)
4. Document: "Session 12345, user john_doe, cartesian join consuming 90% CPU"
5. Call terminate_session(12345)
6. Confirm termination: "Session terminated"
7. Notify user: "Killed runaway query, check for missing join condition"
```

### Example 2: Resolve Blocking
```
User: "Critical report is blocked, unblock it"

Action:
1. Use detect_blocking to identify blocker
2. Check show_sql for blocking session - is it legitimate?
3. Estimate how long blocker will run
4. Decision: Blocker is stuck DDL from 2 hours ago
5. Call terminate_session on blocker
6. Verify blocked session proceeds
7. Report: "Terminated blocking session 67890, report now running"
8. Investigate why DDL was stuck
```

### Example 3: Clean Up Orphaned Sessions
```
User: "Clean up sessions from users who went home"

Action:
1. Use show_sessions to see active sessions
2. Filter for sessions idle > 4 hours or off-hours activity
3. Check show_sql to verify idle (no active query)
4. Identify truly orphaned (user offline, session idle)
5. Terminate orphaned sessions one by one
6. Report: "Terminated 8 orphaned sessions, freed resources"
7. Recommend: "Enable idle session timeout policy"
```

### Example 4: Handle User Request
```
User: "I accidentally started a huge query, can you kill my session?"

Action:
1. Use show_sessions to find user's session
2. Verify ownership matches requesting user
3. Call show_sql to confirm it's the query they want killed
4. Terminate without extensive investigation (user authorized)
5. Confirm: "Session terminated as requested"
6. Advise: "Check your WHERE clause before rerunning"
```

### Example 5: Emergency Resource Protection
```
User: "System is at 99% CPU, we need to shed load now"

Action:
1. Use show_top_consumers to identify heaviest sessions
2. Quick review with show_sql to avoid killing critical work
3. Prioritize terminating:
   - Ad-hoc/development queries over production
   - Newer sessions over long-running
   - Non-critical users over critical
4. Terminate top 3-5 consumers
5. Monitor system recovery with monitor_amp_load
6. Report actions taken and system status
7. Investigate root cause after stabilization
```

## Best Practices

- **Always investigate before terminating** - understand what you're killing
- Document every termination: who, what, when, why
- Notify users when their sessions are terminated (when practical)
- Prefer killing queries over entire sessions when possible
- Check for dependencies before terminating batch/ETL processes
- In blocking scenarios, verify blocker is truly stuck before killing
- Emergency terminations should be followed by root cause analysis
- Consider less disruptive alternatives first (throttling, release queue)
- Be extra careful during business-critical time windows
- Have rollback/restart plan if terminating part of larger process
- Coordinate with application teams for production workload terminations
- Use session termination as last resort, not first response
- Track termination patterns - frequent kills indicate larger issues
- Implement preventive controls (query governors, timeouts) to reduce need
- Establish clear escalation path for termination decisions
- Test user notification process to ensure it works when needed
