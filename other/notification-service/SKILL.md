---
name: notification-service
description: Use this skill whenever writing notification dispatch, template rendering, delivery tracking, retry logic, quiet hours enforcement, channel routing, or any notification system code in the Myelin platform. This defines the notification type registry, delivery contract, retry policy, and the unsubscribe/preference rules. Load before writing any notification or messaging code.
---

This skill defines the notification service for the Myelin platform. Notifications are a compliance surface — some are mandatory (distress escalations, consent changes, result issuance) and must never be suppressed. Others are learner-preference-driven and must respect opt-out. Every notification must be logged for delivery auditing.

---

## Notification Type Registry

| Type code | Channel | Mandatory | Audience | Trigger |
|-----------|---------|-----------|---------|---------|
| `SUBMISSION_OUTCOME` | Email + in-app | No | Learner | Lecturer sets review outcome |
| `PEER_REVIEW_ASSIGNED` | Email + in-app | No | Learner | Peer review allocated |
| `LOGBOOK_SIGNOFF` | Email + in-app | No | Learner | Mentor signs off logbook entry |
| `MENTOR_INVITE` | Email | Yes | Mentor | Admin issues mentor invite |
| `RESULT_STATEMENT_ISSUED` | Email + in-app | Yes | Learner | Result statement generated |
| `RESULT_STATEMENT_AMENDED` | Email + in-app | Yes | Learner | Result statement amended |
| `CONSENT_REQUIRED` | In-app | Yes | Learner | New consent version published |
| `DATA_SUBJECT_REQUEST` | Email (Admin) | Yes | Admin | Data subject rights request received |
| `AI_ESCALATION_ALERT` | Email + SMS | Yes | Admin | Distress escalation created |
| `PLACEMENT_STARTED` | Email + in-app | No | Learner + Admin | Placement status set to ACTIVE |
| `PLACEMENT_COMPLETED` | Email + in-app | No | Learner + Admin | Placement end date reached |
| `COHORT_INVITE` | Email | No | Learner | Enrolled into cohort |

Mandatory notifications (`mandatory: true`) bypass all user opt-out preferences. They cannot be suppressed.

---

## Notification Record Schema

Every notification dispatch produces a persisted record before sending.

```javascript
const notificationRecord = {
  notificationId:  '',   // uuid
  tenantId:        '',
  recipientId:     '',   // user ID
  recipientEmail:  '',   // resolved at dispatch time, not stored permanently
  type:            '',   // type code from registry above
  channel:         '',   // 'EMAIL' | 'SMS' | 'IN_APP'
  subject:         '',   // email subject or in-app title
  bodyRef:         '',   // reference to rendered template snapshot (not the template itself)
  status:          '',   // 'QUEUED' | 'SENT' | 'DELIVERED' | 'FAILED' | 'BOUNCED'
  scheduledAt:     '',   // ISO 8601 — when to send (respects quiet hours)
  sentAt:          null, // ISO 8601 — when actually dispatched
  deliveredAt:     null, // ISO 8601 — when delivery confirmed by provider
  failedAt:        null, // ISO 8601 — if delivery failed
  failureReason:   null,
  retryCount:      0,
  maxRetries:      3,
  providerRef:     null  // provider message ID for tracking
};
```

---

## Dispatch Function

```javascript
async function dispatchNotification(type, recipientId, tenantId, templateVars) {
  const recipientPrefs = await getUserNotificationPrefs(recipientId, tenantId);
  const typeConfig     = NOTIFICATION_REGISTRY[type];

  if (!typeConfig) throw new Error(`UNKNOWN_NOTIFICATION_TYPE: ${type}`);

  const channels = resolveChannels(typeConfig, recipientPrefs);

  for (const channel of channels) {
    const rendered = await renderTemplate(type, channel, templateVars, tenantId);
    const sendAt   = resolveScheduledTime(typeConfig, recipientPrefs, channel);

    const record = await insertNotificationRecord({
      notificationId: generateUUID(),
      tenantId,
      recipientId,
      recipientEmail: rendered.recipientEmail,
      type,
      channel,
      subject:     rendered.subject,
      bodyRef:     rendered.bodyRef,
      status:      'QUEUED',
      scheduledAt: sendAt.toISOString()
    });

    await enqueueNotificationJob(record.notificationId, sendAt);
  }
}
```

---

## Channel Resolution

```javascript
function resolveChannels(typeConfig, recipientPrefs) {
  // Mandatory types always use all configured channels
  if (typeConfig.mandatory) return typeConfig.channels;

  // Non-mandatory: intersect with recipient's opt-in preferences
  return typeConfig.channels.filter(channel => {
    if (channel === 'EMAIL')  return recipientPrefs.emailEnabled !== false;
    if (channel === 'SMS')    return recipientPrefs.smsEnabled === true; // SMS opt-in, not opt-out
    if (channel === 'IN_APP') return recipientPrefs.inAppEnabled !== false;
    return false;
  });
}
```

SMS is opt-in (must be explicitly enabled). Email and in-app are opt-out (enabled by default, user may disable).

---

## Quiet Hours Enforcement

Non-mandatory notifications must not be dispatched during the recipient's configured quiet hours. Default quiet hours: 22:00–07:00 local time.

```javascript
function resolveScheduledTime(typeConfig, recipientPrefs, channel) {
  const now = new Date();

  // Mandatory notifications are sent immediately
  if (typeConfig.mandatory) return now;

  // SMS always respects quiet hours
  const quietStart = recipientPrefs.quietHoursStart || 22;
  const quietEnd   = recipientPrefs.quietHoursEnd   || 7;
  const localHour  = getLocalHour(now, recipientPrefs.timezone);

  const inQuietHours = quietStart > quietEnd
    ? (localHour >= quietStart || localHour < quietEnd)  // crosses midnight
    : (localHour >= quietStart && localHour < quietEnd);

  if (inQuietHours) {
    // Schedule for start of next send window
    const nextWindow = getNextSendWindowStart(now, quietEnd, recipientPrefs.timezone);
    return nextWindow;
  }

  return now;
}
```

---

## Retry Policy

```javascript
async function processNotificationJob(notificationId) {
  const record = await getNotificationRecord(notificationId);

  try {
    const result = await sendViaProvider(record);
    await updateNotificationRecord(notificationId, {
      status:      'SENT',
      sentAt:      new Date().toISOString(),
      providerRef: result.messageId
    });
  } catch (err) {
    const newRetryCount = record.retryCount + 1;

    if (newRetryCount >= record.maxRetries) {
      await updateNotificationRecord(notificationId, {
        status:        'FAILED',
        failedAt:      new Date().toISOString(),
        failureReason: err.message,
        retryCount:    newRetryCount
      });

      // Mandatory notification failure — alert Super Admin
      if (NOTIFICATION_REGISTRY[record.type].mandatory) {
        await alertSuperAdminOfDeliveryFailure(record);
      }
    } else {
      // Exponential backoff: 5min, 20min, 60min
      const backoffMs = [300000, 1200000, 3600000][newRetryCount - 1] || 3600000;
      await rescheduleNotificationJob(notificationId, new Date(Date.now() + backoffMs));
      await updateNotificationRecord(notificationId, {
        retryCount: newRetryCount,
        status:     'QUEUED'
      });
    }
  }
}
```

Mandatory notification failure at max retries triggers a Super Admin alert. This covers distress escalations and result statement deliveries — their failure is never silently discarded.

---

## Template Requirements

Templates are tenant-customisable. Each tenant may provide their own logo, brand colour, and footer text. The following fields are required in every outbound email template:

- Institution name and logo
- Platform name (Myelin)
- Clear subject line stating the notification type
- Action button (where applicable)
- Plain-text fallback version
- Unsubscribe link (non-mandatory notifications only — mandatory notifications must not include an unsubscribe link)
- Privacy Notice link
- POPIA-compliant footer: "This message was sent to you as part of your enrolment at [institution]. View your communication preferences at [link]."

---

## In-App Notification Feed

In-app notifications are stored and served as a feed. They are not transient — unread notifications persist until the learner marks them read or they expire (30 days for non-mandatory types).

```javascript
async function getInAppNotifications(session, unreadOnly = false) {
  await db.query(`SET LOCAL app.current_tenant_id = '${session.tenantId}'`);
  return db.query(`
    SELECT notification_id, type, subject, body_ref, status,
           sent_at, read_at
    FROM notifications
    WHERE tenant_id = $1
      AND recipient_id = $2
      AND channel = 'IN_APP'
      AND (expires_at IS NULL OR expires_at > NOW())
      AND ($3 = false OR read_at IS NULL)
    ORDER BY sent_at DESC
    LIMIT 50
  `, [session.tenantId, session.userId, unreadOnly]);
}

async function markNotificationRead(session, notificationId) {
  await db.query(`
    UPDATE notifications
    SET read_at = NOW()
    WHERE notification_id = $1
      AND tenant_id = $2
      AND recipient_id = $3
  `, [notificationId, session.tenantId, session.userId]);
}
```

---

## What Not To Do

- Do not suppress mandatory notifications for any user preference or opt-out setting
- Do not dispatch SMS notifications as opt-out — SMS is always opt-in
- Do not send notifications outside quiet hours for non-mandatory types
- Do not silently discard failed mandatory notification deliveries — alert Super Admin
- Do not include an unsubscribe link in mandatory notification templates
- Do not store the full rendered email body in the notification record — store a ref to the template snapshot
- Do not allow retry count to exceed `maxRetries` without setting status to `FAILED`
