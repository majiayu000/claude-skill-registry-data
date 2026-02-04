---
name: troubleshooting-notifications
description: Investigates Mission Control notifications to identify root causes and provide remediation. Use when users mention notification IDs, ask about alerts or notifications, request help understanding "why did I get this notification", want to troubleshoot a specific alert, or ask about notification patterns and history. This skill retrieves notification details, analyzes historical patterns, routes to resource-specific troubleshooting (config items or health checks), correlates findings, and delivers actionable remediation steps with prevention recommendations.
allowed-tools: get_notification_detail, get_notifications_for_resource
---

# Notification Troubleshooting Skill

## When to Invoke This Skill

Invoke this skill when users:

- Mention a specific notification ID or title
- Ask to investigate or troubleshoot a notification
- Ask "why did I get this alert/notification"
- Request help understanding a Mission Control notification
- Ask about notification history or patterns

## Core Purpose

This skill enables Claude to investigate Mission Control notifications, trace them to their root cause, and provide actionable remediation steps by systematically analyzing notification details, resource context, and historical patterns.

## Understanding Notifications

A **Notification** represents an alert or event triggered by Mission Control when a resource experiences issues or state changes. Each notification contains:

- **id**: Unique identifier for the notification
- **title**: Short summary of the notification
- **message**: Detailed description of what triggered the notification
- **severity**: Alert level (critical, error, warning, info)
- **resource_id**: ID of the affected resource
- **resource_type**: Type of resource ("ConfigItem", "HealthCheck", etc.)
- **created_at**: When the notification was created
- **status**: Current status (active, resolved, acknowledged)

## Systematic Troubleshooting Workflow

Follow this step-by-step approach:

### Step 1: Retrieve Notification Details

**CALL** `get_notification_detail` with the notification ID

**OBSERVE** the response and extract:

- `title` and `message` - what is the alert about?
- `severity` - how critical is this?
- `resource_id` and `resource_type` - what resource is affected?
- `created_at` - when did this start?
- `status` - is this still active?

**ANALYZE** the message field carefully - it often contains:

- Error messages or stack traces
- Threshold violations
- State transition information
- Specific failure reasons

### Step 2: Analyze Notification History

**CALL** `get_notifications_for_resource` for the affected resource

**LOOK FOR** patterns:

- **Recurring notifications**: Same issue happening repeatedly
- **Frequency changes**: Issue getting worse or better
- **Event correlation**: Multiple related notifications around same time
- **Resolution patterns**: What changed when past notifications resolved

**IDENTIFY** if this is:

- A new issue (first occurrence)
- A recurring problem (happened before)
- Part of a larger incident (multiple resources affected)

### Step 3: Route to Resource-Specific Troubleshooting

Based on `resource_type`, invoke the appropriate skill:

**IF** `resource_type == "ConfigItem"`:

```
CALL Skill tool with skill="mission-control-skills:config_item"
PROVIDE the resource_id and context from notification
```

**IF** `resource_type == "HealthCheck"`:

```
CALL Skill tool with skill="mission-control-skills:health"
PROVIDE the resource_id and context from notification
```

**The invoked skill will**:

- Investigate the specific resource
- Analyze current state and changes
- Identify root cause
- Provide remediation steps

### Step 4: Correlate Findings

**SYNTHESIZE** information from:

1. Notification message and severity
2. Historical notification patterns
3. Resource-level investigation findings
4. Timing of events and changes

**DETERMINE**:

- Root cause of the notification
- Why it triggered at this specific time
- Whether issue is ongoing or resolved
- Related resources that may be affected

### Step 5: Provide Recommendations

**DELIVER**:

1. **Root Cause**: Clear explanation of what went wrong
2. **Evidence**: Specific data points supporting the diagnosis
3. **Remediation**: Step-by-step actions to resolve
4. **Prevention**: How to avoid this notification in the future

## Common Notification Scenarios

### Scenario 1: Config Item Unhealthy Notification

```
1. GET notification details
   → severity: error
   → message: "ConfigItem kubernetes/prod/api-deployment is unhealthy"
   → resource_type: ConfigItem
   → resource_id: "config-123"

2. GET notification history for config-123
   → 3 similar notifications in past 24h
   → Pattern: recurring every 4 hours

3. INVOKE config_item skill with resource_id
   → Skill finds: Pod CrashLoopBackOff
   → Root cause: OOMKilled - memory limit too low

4. SYNTHESIZE findings
   → Notification triggered by health check failure
   → Recurring because pod keeps restarting
   → Memory limit increased 3 days ago (from changes)

5. RECOMMEND
   → Increase memory limit from 512Mi to 1Gi
   → Monitor for next hour to confirm resolution
   → Set alert threshold higher to avoid false positives
```

### Scenario 2: Health Check Failure Notification

```
1. GET notification details
   → severity: critical
   → message: "Database connection timeout"
   → resource_type: HealthCheck
   → resource_id: "hc-456"

2. GET notification history for hc-456
   → First occurrence - new issue
   → No previous failures for this check

3. INVOKE health skill with resource_id
   → Skill finds: Network policy blocking connection
   → Changed 30 minutes ago

4. SYNTHESIZE findings
   → New network policy deployed
   → Blocks egress to database port
   → Health check can't reach database

5. RECOMMEND
   → Update network policy to allow database traffic
   → Test health check manually after fix
   → Review change approval process
```

## Error Handling

**IF** `get_notification_detail` returns not found:

- Verify notification ID is correct
- Check if user has permissions to view notification
- Ask user to confirm the notification ID

**IF** `resource_id` is null or missing:

- Notification may be system-level (not resource-specific)
- Analyze message for manual troubleshooting clues
- Search for related notifications in same timeframe

**IF** `resource_type` is not ConfigItem or HealthCheck:

- Investigate the resource type directly
- Use general troubleshooting principles
- Document findings and ask for guidance

**IF** notification history is empty:

- This is a new type of issue
- Focus more on recent changes
- Less context available for pattern analysis

## Critical Requirements

**Evidence-Based Analysis**:

- Quote specific error messages from notification
- Reference timestamps and correlation
- Support conclusions with data from tools

**Hierarchical Investigation**:

- Start with notification (symptom)
- Trace to resource (source)
- Navigate relationships (context)
- Identify change (cause)

**Actionable Remediation**:

- Provide specific commands or actions
- Explain why each step will help
- Include validation steps
- Consider prevention measures

## Skill Invocation Pattern

When routing to other skills, use this format:

```markdown
Based on the notification for resource_type="ConfigItem", I'm now invoking the config_item troubleshooting skill to investigate the underlying resource.

[CALL Skill tool with skill="mission-control-skills:config_item"]

[After skill returns]
The config_item skill has identified: [summarize findings]
Combined with the notification history showing [pattern], the root cause is [diagnosis].
```

## Key Success Criteria

✓ Notification context fully understood
✓ Historical patterns analyzed
✓ Appropriate skill invoked for resource type
✓ Root cause identified with evidence
✓ Clear remediation steps provided
✓ Prevention recommendations included
