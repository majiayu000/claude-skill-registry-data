---
name: manage-queues
description: Manage delayed request queues including workload, system, and utility queues to release blocked requests or abort unnecessary items
---

# Manage Queues

Monitor and manage delayed request queues to handle queued queries, release blocked requests, and abort unnecessary items to maintain system flow and meet SLAs.

## Instructions

### When to Use This Skill
- Queries are stuck in queues and need intervention
- Users report excessive wait times
- Need to release specific queued requests
- Emergency situation requires clearing problematic queue items
- Regular queue maintenance and monitoring

### Available MCP Tools
- `show_delayed_queue` - View delayed requests by type (workload, system, utility)
- `release_delayed_request` - Release a blocked request from queue
- `abort_delayed_request` - Abort/cancel a delayed request

### Step-by-Step Workflow

1. **Assess Queue Status**
   - Use `show_delayed_queue` with type='ALL' to see all queued items
   - Identify queue types: workload (throttled), system (locks), utility (maintenance)
   - Note queue depths and wait times

2. **Analyze Queued Requests**
   - Review each delayed request: who, what, how long
   - Identify legitimate delays vs stuck requests
   - Prioritize based on business impact and wait time

3. **Determine Root Cause**
   - Workload queue: Throttle limits or resource constraints
   - System queue: Lock conflicts or blocking sessions
   - Utility queue: Concurrent maintenance operations
   - Cross-reference with session and workload monitoring

4. **Take Appropriate Action**

   **For Releasing Requests:**
   - Use when request is valid but delayed too long
   - Verify adequate resources before release
   - Release highest priority items first
   - Monitor system impact after release

   **For Aborting Requests:**
   - Use when request is no longer needed or problematic
   - Confirm with request owner if possible
   - Abort lowest priority or stuck items
   - Document reason for abort

5. **Monitor Results**
   - Check queue depth after actions
   - Verify released queries execute successfully
   - Ensure no cascade effects from releases
   - Track if queuing recurs (indicates systemic issue)

6. **Address Underlying Issues**
   - If queues persistently fill, investigate root cause
   - May need workload tuning, throttle adjustment, or capacity
   - Document patterns for long-term optimization

## Examples

### Example 1: Check Queue Status
```
User: "Are there any queries waiting in queue?"

Action:
1. Call show_delayed_queue with type='ALL'
2. Summarize: "5 workload queue, 2 system queue, 0 utility queue"
3. Report wait times and affected users
4. Flag any excessive waits (>SLA threshold)
```

### Example 2: Release Priority Request
```
User: "The CEO's dashboard query is stuck, can you release it?"

Action:
1. Use show_delayed_queue to locate the request
2. Verify it's in queue (not executing or blocked)
3. Confirm system has capacity for release
4. Call release_delayed_request with request ID
5. Monitor to ensure it executes: "Request released and now executing"
6. If still blocked, investigate further
```

### Example 3: Clear Abandoned Requests
```
User: "There are old queries in queue from last night, clean them up"

Action:
1. Show delayed queue and identify old requests
2. Check request age and originating user
3. Verify users are no longer waiting (offline, session closed)
4. Call abort_delayed_request for each abandoned item
5. Report: "Aborted 12 requests older than 8 hours"
6. Investigate why they were delayed so long
```

### Example 4: Manage Queue During Peak
```
User: "Month-end queue is backing up, help manage it"

Action:
1. Check show_delayed_queue for workload distribution
2. Identify critical vs non-critical delayed requests
3. Release critical month-end reports selectively
4. Abort or delay non-critical ad-hoc queries
5. Monitor queue depth trends
6. Communicate with users about delays
7. Recommend: "Consider temporary throttle adjustment for peak period"
```

### Example 5: Resolve Lock-Related Queue
```
User: "Queries are stuck in system queue"

Action:
1. Use show_delayed_queue with type='SYSTEM'
2. Identify requests waiting on locks
3. Use detect_blocking to find blocking sessions
4. Options:
   a. Wait for blocker to complete (if nearly done)
   b. Terminate blocking session (if stuck/problematic)
   c. Abort delayed request (if blocker will run long)
5. Take action and verify queue clears
6. Report resolution and prevent recurrence
```

## Best Practices

- Check queues proactively, don't wait for user complaints
- Workload queues are usually intentional (throttles working)
- System queues often indicate blocking - find and resolve blocker
- Utility queues are typically brief unless maintenance stuck
- Always verify why request is queued before releasing or aborting
- Communicate with users before aborting their requests when possible
- Release requests cautiously - could overload system if many released at once
- Document queue management actions for audit trail
- Track queue patterns to identify systemic issues
- Long queues may indicate need for capacity or workload tuning
- Emergency releases should be followed by root cause analysis
- Consider impact on other queued items when releasing selectively
- Set SLA thresholds for queue wait times and alert when exceeded
- Coordinate with DBAs before making major queue management decisions
