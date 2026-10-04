---
name: Cloud Run Debugging Techniques
description: |
  This skill provides Cloud Run debugging techniques and troubleshooting patterns. Use when debugging Cloud Run services, investigating errors, analyzing logs, or resolving deployment issues. Triggers when user mentions "Cloud Run error", "container crash", "cold start", "timeout", "502 error", "deployment failed", or needs help with Cloud Run troubleshooting.
version: 1.0.0
---

# Cloud Run Debugging Techniques

## Quick Diagnostic Commands

### Service Status
```bash
# List all services with status
gcloud run services list --project=$PROJECT_ID

# Get detailed service info
gcloud run services describe $SERVICE --region=$REGION --project=$PROJECT_ID

# Check current revision health
gcloud run revisions list --service=$SERVICE --region=$REGION --limit=5
```

### Log Analysis
```bash
# Recent errors
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=50 --project=$PROJECT_ID \
  --format="table(timestamp,severity,textPayload)"

# Specific service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE" \
  --limit=100 --project=$PROJECT_ID

# Request failures (4xx/5xx)
gcloud logging read "resource.type=cloud_run_revision AND httpRequest.status>=400" \
  --limit=20 --project=$PROJECT_ID \
  --format="table(timestamp,httpRequest.status,httpRequest.requestUrl,httpRequest.latency)"
```

## Common Issues & Solutions

### 1. Cold Start Latency

**Symptoms**: First request takes 5-30+ seconds

**Diagnosis**:
```bash
# Check if min instances is 0
gcloud run services describe $SERVICE --format="yaml(spec.template.metadata.annotations)"
```

**Solutions**:
```bash
# Set minimum instances
gcloud run services update $SERVICE --min-instances=1 --region=$REGION

# Optimize container startup
# - Use smaller base images (alpine, distroless)
# - Lazy load heavy dependencies
# - Reduce container size
```

**Code Optimization**:
```javascript
// Lazy load heavy modules
let heavyModule;
function getHeavyModule() {
  if (!heavyModule) {
    heavyModule = require('heavy-module');
  }
  return heavyModule;
}
```

### 2. Container Crashes (503)

**Symptoms**: Service unavailable, container restarts

**Diagnosis**:
```bash
# Check for crash logs
gcloud logging read "resource.type=cloud_run_revision AND textPayload:crash OR textPayload:killed OR textPayload:OOM" \
  --limit=20 --project=$PROJECT_ID

# Check memory usage
gcloud logging read "resource.type=cloud_run_revision AND textPayload:memory" \
  --limit=10 --project=$PROJECT_ID
```

**Common Causes**:
1. **OOM (Out of Memory)**: Increase memory limit
2. **Unhandled exceptions**: Add global error handlers
3. **PORT not handled**: Ensure app listens on `process.env.PORT`

**Solutions**:
```bash
# Increase memory
gcloud run services update $SERVICE --memory=1Gi --region=$REGION
```

```javascript
// Ensure PORT handling
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Listening on ${PORT}`));

// Add global error handler
process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err);
  process.exit(1);
});
```

### 3. Timeout Errors (504)

**Symptoms**: Requests fail after 60 seconds (default timeout)

**Diagnosis**:
```bash
# Check current timeout
gcloud run services describe $SERVICE --format="value(spec.template.spec.timeoutSeconds)"

# Find slow requests
gcloud logging read "resource.type=cloud_run_revision AND httpRequest.latency>5s" \
  --limit=20 --project=$PROJECT_ID
```

**Solutions**:
```bash
# Increase timeout (max 3600s)
gcloud run services update $SERVICE --timeout=300 --region=$REGION
```

**Better Approach**: Use async processing
```javascript
// Return quickly, process async
app.post('/long-task', async (req, res) => {
  const taskId = generateTaskId();

  // Acknowledge immediately
  res.status(202).json({ taskId, status: 'processing' });

  // Process in background (use Pub/Sub or Cloud Tasks)
  await pubsub.topic('tasks').publish(Buffer.from(JSON.stringify(req.body)));
});
```

### 4. Authentication Errors (401/403)

**Symptoms**: "IAM permission denied" or 401 responses

**Diagnosis**:
```bash
# Check service authentication settings
gcloud run services describe $SERVICE --format="yaml(spec.template.metadata.annotations.'run.googleapis.com/ingress')"

# Check IAM bindings
gcloud run services get-iam-policy $SERVICE --region=$REGION
```

**Solutions**:
```bash
# Allow unauthenticated (public API)
gcloud run services add-iam-policy-binding $SERVICE \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=$REGION

# Or for authenticated with specific service account
gcloud run services add-iam-policy-binding $SERVICE \
  --member="serviceAccount:client@project.iam.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --region=$REGION
```

### 5. Deployment Failures

**Symptoms**: Deploy command fails

**Diagnosis**:
```bash
# Check Cloud Build logs
gcloud builds list --limit=5
gcloud builds describe $BUILD_ID
```

**Common Causes**:
1. **Dockerfile errors**: Validate locally first
2. **Permission issues**: Check service account permissions
3. **Resource limits**: Check quotas

**Debug Locally**:
```bash
# Build locally to test
docker build -t test-image .
docker run -p 8080:8080 -e PORT=8080 test-image
curl http://localhost:8080/health
```

### 6. Networking Issues

**Symptoms**: Can't connect to other services, VPC issues

**Diagnosis**:
```bash
# Check VPC connector
gcloud run services describe $SERVICE \
  --format="yaml(spec.template.metadata.annotations.'run.googleapis.com/vpc-access-connector')"

# Check egress settings
gcloud run services describe $SERVICE \
  --format="yaml(spec.template.metadata.annotations.'run.googleapis.com/vpc-access-egress')"
```

**Solutions**:
```bash
# Add VPC connector for internal resources
gcloud run services update $SERVICE \
  --vpc-connector=my-connector \
  --vpc-egress=private-ranges-only \
  --region=$REGION
```

## Debug Logging

### Enable Structured Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [new winston.transports.Console()]
});

// Structured log that Cloud Logging understands
logger.info('Request received', {
  requestId: req.id,
  path: req.path,
  method: req.method,
  userId: req.userId
});
```

### Correlation with Trace ID
```javascript
app.use((req, res, next) => {
  // Extract Cloud Trace ID
  const traceHeader = req.headers['x-cloud-trace-context'];
  if (traceHeader) {
    const [traceId] = traceHeader.split('/');
    req.traceId = traceId;

    // Include in all logs
    console.log(JSON.stringify({
      severity: 'INFO',
      message: 'Request received',
      'logging.googleapis.com/trace': `projects/${PROJECT_ID}/traces/${traceId}`
    }));
  }
  next();
});
```

## Health Check Endpoint

```javascript
// Comprehensive health check
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: Date.now(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    checks: {}
  };

  try {
    // Check database
    await db.collection('health').doc('check').get();
    health.checks.database = 'ok';
  } catch (err) {
    health.checks.database = 'failed';
    health.status = 'unhealthy';
  }

  try {
    // Check Pub/Sub
    await pubsub.topic('telemetry').get();
    health.checks.pubsub = 'ok';
  } catch (err) {
    health.checks.pubsub = 'failed';
    health.status = 'unhealthy';
  }

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

## Performance Optimization

### Request Concurrency
```bash
# Check current concurrency
gcloud run services describe $SERVICE --format="value(spec.template.spec.containerConcurrency)"

# Adjust based on workload (default 80)
gcloud run services update $SERVICE --concurrency=100
```

### CPU Allocation
```bash
# CPU always allocated (reduces cold start impact)
gcloud run services update $SERVICE --cpu-boost --region=$REGION

# Or always-on CPU
gcloud run services update $SERVICE --no-cpu-throttling --region=$REGION
```

## Quick Fixes Reference

| Issue | Quick Fix Command |
|-------|-------------------|
| Cold starts | `--min-instances=1` |
| OOM crashes | `--memory=1Gi` |
| Timeouts | `--timeout=300` |
| Slow scaling | `--max-instances=10` |
| CPU throttling | `--no-cpu-throttling` |
| Auth errors | `--allow-unauthenticated` |
