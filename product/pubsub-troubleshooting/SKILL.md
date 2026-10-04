---
name: Pub/Sub Troubleshooting Guide
description: |
  This skill provides Pub/Sub troubleshooting guidance for message delivery issues. Use when debugging Pub/Sub topics, subscriptions, message acknowledgment, push failures, or dead letter queues. Triggers when user mentions "Pub/Sub not working", "messages lost", "subscription backlog", "push endpoint failing", "dead letter", or needs help with Pub/Sub debugging.
version: 1.0.0
---

# Pub/Sub Troubleshooting Guide

## Quick Diagnostic Commands

```bash
# List all topics
gcloud pubsub topics list --project=$PROJECT_ID

# List all subscriptions
gcloud pubsub subscriptions list --project=$PROJECT_ID

# Get subscription details
gcloud pubsub subscriptions describe $SUBSCRIPTION --project=$PROJECT_ID

# Check topic's subscriptions
gcloud pubsub topics list-subscriptions $TOPIC --project=$PROJECT_ID
```

## Message Flow Debugging

### Verify Publishing Works

```bash
# Publish test message
gcloud pubsub topics publish $TOPIC \
  --message='{"test": true, "timestamp": "'$(date -Iseconds)'"}' \
  --project=$PROJECT_ID

# Result shows message ID if successful
```

### Verify Subscription Receives

```bash
# For PULL subscription - pull without ack
gcloud pubsub subscriptions pull $SUBSCRIPTION \
  --limit=5 \
  --project=$PROJECT_ID

# Pull and acknowledge
gcloud pubsub subscriptions pull $SUBSCRIPTION \
  --limit=5 \
  --auto-ack \
  --project=$PROJECT_ID
```

### Check Push Delivery Logs

```bash
gcloud logging read "resource.type=pubsub_subscription AND resource.labels.subscription_id=$SUBSCRIPTION" \
  --limit=20 \
  --project=$PROJECT_ID
```

## Common Issues & Solutions

### 1. Messages Not Delivered (Push)

**Symptoms**: Messages published but never reach endpoint

**Diagnosis**:
```bash
# Check push config
gcloud pubsub subscriptions describe $SUBSCRIPTION \
  --format="yaml(pushConfig)" \
  --project=$PROJECT_ID
```

**Common Causes**:

#### Wrong Endpoint URL
```bash
# Fix: Update endpoint
gcloud pubsub subscriptions modify-push-config $SUBSCRIPTION \
  --push-endpoint="https://correct-url.run.app/pubsub" \
  --project=$PROJECT_ID
```

#### Endpoint Not Returning 200
Push requires 200, 201, 202, or 204 response.

```javascript
// Endpoint must acknowledge properly
app.post('/pubsub', (req, res) => {
  const message = req.body.message;

  try {
    processMessage(message);
    res.status(200).send('OK'); // MUST return 2xx
  } catch (err) {
    console.error('Processing failed:', err);
    res.status(500).send('Error'); // Message will retry
  }
});
```

#### Authentication Failure
```bash
# Add OIDC token for authenticated endpoints
gcloud pubsub subscriptions modify-push-config $SUBSCRIPTION \
  --push-endpoint="https://service.run.app/pubsub" \
  --push-auth-service-account="push-invoker@$PROJECT_ID.iam.gserviceaccount.com" \
  --project=$PROJECT_ID

# Grant invoker role
gcloud run services add-iam-policy-binding $SERVICE \
  --member="serviceAccount:push-invoker@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --region=$REGION
```

### 2. Message Backlog Growing

**Symptoms**: Subscription has increasing unacked messages

**Diagnosis**:
```bash
# Check metrics
gcloud monitoring metrics list \
  --filter="metric.type:pubsub.googleapis.com/subscription/num_undelivered_messages" \
  --project=$PROJECT_ID

# Or use Console: Cloud Console → Pub/Sub → Subscriptions → Metrics
```

**Common Causes**:

#### Subscriber Not Running
```bash
# For pull: Check if client is active
# For push: Check endpoint availability
curl -I https://endpoint.run.app/health
```

#### Processing Too Slow
```bash
# Increase ack deadline
gcloud pubsub subscriptions update $SUBSCRIPTION \
  --ack-deadline=60 \
  --project=$PROJECT_ID
```

#### Too Many Retries
```bash
# Add dead letter to stop infinite retries
gcloud pubsub subscriptions update $SUBSCRIPTION \
  --dead-letter-topic=$DEAD_LETTER_TOPIC \
  --max-delivery-attempts=5 \
  --project=$PROJECT_ID
```

### 3. Duplicate Messages

**Symptoms**: Same message delivered multiple times

**Causes**:
1. Ack not sent before deadline
2. Subscriber crashed before acking
3. At-least-once delivery (by design)

**Solutions**:

```javascript
// Implement idempotency
app.post('/pubsub', async (req, res) => {
  const messageId = req.body.message.messageId;

  // Check if already processed
  const processed = await cache.get(`msg:${messageId}`);
  if (processed) {
    return res.status(200).send('Already processed');
  }

  // Process and mark as done
  await processMessage(req.body.message);
  await cache.set(`msg:${messageId}`, true, 'EX', 86400);

  res.status(200).send('OK');
});
```

### 4. Messages Expire/Lost

**Symptoms**: Messages disappear without processing

**Diagnosis**:
```bash
# Check retention settings
gcloud pubsub subscriptions describe $SUBSCRIPTION \
  --format="yaml(messageRetentionDuration,expirationPolicy)" \
  --project=$PROJECT_ID
```

**Solutions**:
```bash
# Increase retention (max 7 days)
gcloud pubsub subscriptions update $SUBSCRIPTION \
  --message-retention-duration=7d \
  --project=$PROJECT_ID

# Remove expiration
gcloud pubsub subscriptions update $SUBSCRIPTION \
  --expiration-period=never \
  --project=$PROJECT_ID
```

### 5. Dead Letter Queue Filling Up

**Symptoms**: Messages in dead letter topic

**Diagnosis**:
```bash
# Pull from dead letter
gcloud pubsub subscriptions pull $DEAD_LETTER_SUB \
  --limit=5 \
  --project=$PROJECT_ID
```

**Investigate**:
- Check message content for malformation
- Check endpoint logs for processing errors
- Verify authentication

**Reprocess Dead Letters**:
```javascript
// Cloud Function to reprocess
exports.reprocessDeadLetter = async (message) => {
  const originalMessage = JSON.parse(Buffer.from(message.data, 'base64'));

  // Republish to original topic with delay
  await pubsub.topic('original-topic').publish(
    Buffer.from(JSON.stringify(originalMessage)),
    { retryCount: (originalMessage.retryCount || 0) + 1 }
  );
};
```

## Push vs Pull Decision Guide

| Factor | Use PUSH | Use PULL |
|--------|----------|----------|
| Latency | Low latency needed | Can tolerate delay |
| Scale | Moderate volume | High volume |
| Control | Simple endpoint | Complex processing |
| Batching | Single messages | Need batching |
| Error handling | Retry built-in | Custom retry logic |

## Subscription Configuration

### Optimal Push Config
```bash
gcloud pubsub subscriptions create $SUBSCRIPTION \
  --topic=$TOPIC \
  --push-endpoint="https://service.run.app/pubsub" \
  --push-auth-service-account="invoker@$PROJECT_ID.iam.gserviceaccount.com" \
  --ack-deadline=30 \
  --message-retention-duration=1d \
  --min-retry-delay=10s \
  --max-retry-delay=600s \
  --dead-letter-topic=$DEAD_LETTER_TOPIC \
  --max-delivery-attempts=5 \
  --project=$PROJECT_ID
```

### Optimal Pull Config
```bash
gcloud pubsub subscriptions create $SUBSCRIPTION \
  --topic=$TOPIC \
  --ack-deadline=60 \
  --message-retention-duration=7d \
  --retain-acked-messages \
  --expiration-period=never \
  --project=$PROJECT_ID
```

## Message Format Reference

### Push Message Format
```json
{
  "message": {
    "data": "eyJkZXZpY2VJZCI6ImVzcDMyLTAwMSJ9",
    "messageId": "2070443601311540",
    "message_id": "2070443601311540",
    "publishTime": "2024-01-15T10:00:00.000Z",
    "publish_time": "2024-01-15T10:00:00.000Z"
  },
  "subscription": "projects/my-project/subscriptions/my-sub"
}
```

### Decoding Message
```javascript
app.post('/pubsub', (req, res) => {
  const message = req.body.message;
  const data = JSON.parse(
    Buffer.from(message.data, 'base64').toString()
  );

  console.log('Received:', data);
  res.status(200).send('OK');
});
```

## Monitoring Queries

```bash
# Unacked messages
gcloud monitoring read "pubsub.googleapis.com/subscription/num_undelivered_messages" \
  --start-time="2024-01-15T00:00:00Z" \
  --end-time="2024-01-15T23:59:59Z"

# Push latency
gcloud logging read "resource.type=pubsub_subscription AND textPayload:latency" \
  --limit=100 --project=$PROJECT_ID
```

## Quick Fixes Summary

| Problem | Solution |
|---------|----------|
| Push not delivering | Check endpoint URL, add OIDC auth |
| Backlog growing | Increase ack deadline, add dead letter |
| Messages lost | Increase retention to 7d |
| Duplicates | Implement idempotency with message ID |
| Permission denied | Grant pubsub.publisher / pubsub.subscriber |
