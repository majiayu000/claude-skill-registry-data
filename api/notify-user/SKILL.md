---
name: notify-user
description: Send email notifications to users via Mailgun API. Use when scheduled jobs complete, encounter errors, need user input, or have important updates to report. Requires Mailgun credentials configured via credential-activation skill.
version: 1.0.0
allowed-tools: Bash, Read
metadata:
  requires: credential-activation
  credentials:
    - MAILGUN_API_KEY
    - MAILGUN_DOMAIN
    - MAILGUN_REGION
    - MAILGUN_FROM_EMAIL
    - NOTIFICATION_EMAIL
---

# Notify User Skill

Send email notifications to users when important events occur.

## Prerequisites

This skill requires Mailgun credentials. Before first use, ensure credentials are configured:

1. **Check if credentials exist**:
   ```bash
   # These should be set as environment variables
   echo "MAILGUN_API_KEY: ${MAILGUN_API_KEY:+configured}"
   echo "MAILGUN_DOMAIN: ${MAILGUN_DOMAIN:-not set}"
   echo "MAILGUN_REGION: ${MAILGUN_REGION:-US}"
   echo "NOTIFICATION_EMAIL: ${NOTIFICATION_EMAIL:-not set}"
   ```

2. **If not configured**: Use the `credential-activation` skill to guide the user through setup.

## Credential Requirements

| Variable | Description | Example |
|----------|-------------|---------|
| `MAILGUN_API_KEY` | Mailgun private API key | `key-abc123...` |
| `MAILGUN_DOMAIN` | Verified sending domain | `mail.teamday.ai` |
| `MAILGUN_REGION` | API region: `US` or `EU` | `US` |
| `MAILGUN_FROM_EMAIL` | Sender email address | `agent@mail.teamday.ai` |
| `NOTIFICATION_EMAIL` | Default recipient | `user@example.com` |

## API Endpoints

| Region | Endpoint |
|--------|----------|
| US (default) | `https://api.mailgun.net/v3/{domain}/messages` |
| EU | `https://api.eu.mailgun.net/v3/{domain}/messages` |

## Send a Simple Notification

```bash
# Determine API endpoint based on region
if [ "$MAILGUN_REGION" = "EU" ]; then
  MAILGUN_API="https://api.eu.mailgun.net"
else
  MAILGUN_API="https://api.mailgun.net"
fi

# Send notification
curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL:-Agent <agent@${MAILGUN_DOMAIN}>}" \
  -F to="${NOTIFICATION_EMAIL}" \
  -F subject="[TeamDay Agent] Notification" \
  -F text="Your notification message here"
```

## Send an HTML Notification

```bash
if [ "$MAILGUN_REGION" = "EU" ]; then
  MAILGUN_API="https://api.eu.mailgun.net"
else
  MAILGUN_API="https://api.mailgun.net"
fi

curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL:-Agent <agent@${MAILGUN_DOMAIN}>}" \
  -F to="${NOTIFICATION_EMAIL}" \
  -F subject="[TeamDay Agent] Important Update" \
  -F text="Plain text version of the message" \
  --form-string html='<html>
<body style="font-family: system-ui, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
  <h1 style="color: #333;">Agent Notification</h1>
  <p>Your HTML content here</p>
  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
  <p style="color: #666; font-size: 12px;">This is an automated message from your TeamDay agent.</p>
</body>
</html>'
```

## Notification Templates

### Job Completed Successfully

```bash
SUBJECT="[TeamDay Agent] Job Completed: ${JOB_NAME}"
MESSAGE="Your scheduled job '${JOB_NAME}' has completed successfully.

Summary:
- Job: ${JOB_NAME}
- Status: Success
- Completed at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Results:
${RESULTS_SUMMARY}

This job will continue running on schedule unless you disable it."
```

### Job Terminated (Objective Complete)

```bash
SUBJECT="[TeamDay Agent] Objective Achieved: ${JOB_NAME}"
MESSAGE="Great news! Your scheduled job '${JOB_NAME}' has achieved its objective and has been automatically disabled.

Summary:
- Job: ${JOB_NAME}
- Status: Objective Completed
- Final run: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Final Report:
${FINAL_REPORT}

The job has been disabled. No further runs will occur unless you re-enable it."
```

### Job Blocked/Failed

```bash
SUBJECT="[TeamDay Agent] Action Required: ${JOB_NAME}"
MESSAGE="Your scheduled job '${JOB_NAME}' has encountered an issue and requires your attention.

Summary:
- Job: ${JOB_NAME}
- Status: Blocked
- Issue detected: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Issue Details:
${ERROR_DESCRIPTION}

Recommended Actions:
${RECOMMENDED_ACTIONS}

The job has been automatically disabled to prevent repeated failures."
```

### Progress Update

```bash
SUBJECT="[TeamDay Agent] Progress Update: ${JOB_NAME}"
MESSAGE="Progress update for your scheduled job '${JOB_NAME}'.

Current Status:
- Progress: ${PROGRESS_PERCENT}% complete
- Current phase: ${CURRENT_PHASE}
- Estimated completion: ${ETA}

Recent Activity:
${ACTIVITY_LOG}

The job will continue running on schedule."
```

## Complete Example: Notify on Job Termination

```bash
#!/bin/bash

# Configuration (from environment)
JOB_NAME="daily-docs-monitor"
TERMINATION_REASON="Objective completed - all documentation changes tracked"
WORK_SUMMARY="
- Monitored Anthropic docs for 30 days
- Detected 5 significant updates
- Created daily summaries in daily-notes/
- Final report saved to reports/anthropic-tracking-final.md
"

# Determine API endpoint
if [ "$MAILGUN_REGION" = "EU" ]; then
  MAILGUN_API="https://api.eu.mailgun.net"
else
  MAILGUN_API="https://api.mailgun.net"
fi

# Compose and send notification
curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL:-Agent <agent@${MAILGUN_DOMAIN}>}" \
  -F to="${NOTIFICATION_EMAIL}" \
  -F subject="[TeamDay Agent] Job Terminated: ${JOB_NAME}" \
  -F text="Your scheduled job '${JOB_NAME}' has been terminated.

Reason: ${TERMINATION_REASON}

Work Summary:
${WORK_SUMMARY}

---
This is an automated message from your TeamDay agent.
Location: $(pwd)
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"

# Check result
if [ $? -eq 0 ]; then
  echo "Notification sent successfully"
else
  echo "Failed to send notification"
fi
```

## Sending to Multiple Recipients

```bash
curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL}" \
  -F to="user1@example.com" \
  -F to="user2@example.com" \
  -F cc="manager@example.com" \
  -F subject="Team Notification" \
  -F text="Message to the team"
```

## Error Handling

Always check the response from Mailgun:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL}" \
  -F to="${NOTIFICATION_EMAIL}" \
  -F subject="Test" \
  -F text="Test message")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "Email sent successfully"
  echo "Response: $BODY"
else
  echo "Failed to send email (HTTP $HTTP_CODE)"
  echo "Error: $BODY"
fi
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check MAILGUN_API_KEY |
| 400 Bad Request | Invalid domain or parameters | Verify MAILGUN_DOMAIN is configured in Mailgun |
| 403 Forbidden | Domain not verified | Complete domain verification in Mailgun dashboard |
| Sandbox restriction | Recipient not authorized | Add recipient to authorized list (sandbox only) |

## Best Practices

1. **Don't spam users** - Only send important notifications
2. **Include context** - Always mention which job/space the notification is from
3. **Provide actionable info** - Tell users what to do next
4. **Handle failures gracefully** - Log errors but don't crash on email failure
5. **Use templates** - Consistent formatting improves readability

## Integration with self-scheduler

When a scheduled job completes or is terminated, use this pattern:

```bash
# In your scheduled job's termination logic:

# 1. Disable the job
# (Update .claude/scheduled/job-name.md with enabled: false)

# 2. Send notification
source /path/to/notify-user-template.sh
send_notification "Job Completed" "Your job has finished successfully."
```

## Troubleshooting

### Credentials not found?
Use the `credential-activation` skill to configure Mailgun credentials.

### Emails not arriving?
1. Check Mailgun logs in dashboard
2. Verify domain DNS settings
3. Check spam folder
4. For sandbox: ensure recipient is authorized

### Rate limited?
Mailgun has sending limits. For high-volume needs, upgrade your Mailgun plan.
