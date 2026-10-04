---
name: gcp-cloud-run
description: |
  Use when working with Gcp Cloud Run — google Cloud Run service management,
  revision traffic splitting, scaling configuration, concurrency tuning, and
  container diagnostics via gcloud CLI.
connection_type: gcp
preload: false
---

# Cloud Run Skill

Manage and analyze Google Cloud Run services using `gcloud run` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume service names, regions, or revision names.

```bash
# Discover services
gcloud run services list --format=json \
  | jq '[.[] | {name: .metadata.name, region: .metadata.labels."cloud.googleapis.com/location", url: .status.url, ready: .status.conditions[] | select(.type=="Ready") | .status}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for svc in $(gcloud run services list --format="value(metadata.name,metadata.labels.cloud\\.googleapis\\.com/location)" | tr '\t' ','); do
  {
    name=$(echo "$svc" | cut -d',' -f1)
    region=$(echo "$svc" | cut -d',' -f2)
    gcloud run services describe "$name" --region="$region" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# Get service details
get_service_details() {
  local name="$1" region="$2"
  gcloud run services describe "$name" --region="$region" --format=json \
    | jq '{name: .metadata.name, url: .status.url, latestRevision: .status.latestReadyRevisionName, traffic: .status.traffic, template: {image: .spec.template.spec.containers[0].image, cpu: .spec.template.spec.containers[0].resources.limits.cpu, memory: .spec.template.spec.containers[0].resources.limits.memory, concurrency: .spec.template.spec.containerConcurrency, timeout: .spec.template.spec.timeoutSeconds, scaling: {minScale: .spec.template.metadata.annotations."autoscaling.knative.dev/minScale", maxScale: .spec.template.metadata.annotations."autoscaling.knative.dev/maxScale"}}}'
}

# List revisions
list_revisions() {
  local name="$1" region="$2"
  gcloud run revisions list --service="$name" --region="$region" --format=json \
    | jq '[.[] | {name: .metadata.name, ready: (.status.conditions[] | select(.type=="Ready") | .status), created: .metadata.creationTimestamp, image: .spec.containers[0].image}]'
}

# Get service logs
get_service_logs() {
  local name="$1" region="$2" limit="${3:-50}"
  gcloud logging read "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"$name\" AND resource.labels.location=\"$region\"" --limit="$limit" --format=json
}

# Get traffic split
get_traffic() {
  local name="$1" region="$2"
  gcloud run services describe "$name" --region="$region" --format=json \
    | jq '.status.traffic[] | {revision: .revisionName, percent: .percent, latest: .latestRevision}'
}
```

## Common Operations

### 1. Service Health Overview

```bash
services=$(gcloud run services list --format="value(metadata.name,metadata.labels.cloud\\.googleapis\\.com/location)" | tr '\t' ',')
for svc in $services; do
  {
    name=$(echo "$svc" | cut -d',' -f1)
    region=$(echo "$svc" | cut -d',' -f2)
    get_service_details "$name" "$region"
  } &
done
wait
```

### 2. Revision and Traffic Management

```bash
# Current traffic distribution
get_traffic "$SERVICE" "$REGION"

# List recent revisions
list_revisions "$SERVICE" "$REGION"

# Check revision health
gcloud run revisions list --service="$SERVICE" --region="$REGION" --format=json \
  | jq '[.[] | {name: .metadata.name, ready: (.status.conditions[] | select(.type=="Ready") | .status), reason: (.status.conditions[] | select(.type=="Ready" and .status!="True") | .reason)}]'
```

### 3. Scaling Configuration

```bash
gcloud run services describe "$SERVICE" --region="$REGION" --format=json \
  | jq '{minInstances: .spec.template.metadata.annotations."autoscaling.knative.dev/minScale", maxInstances: .spec.template.metadata.annotations."autoscaling.knative.dev/maxScale", concurrency: .spec.template.spec.containerConcurrency, cpu: .spec.template.spec.containers[0].resources.limits.cpu, memory: .spec.template.spec.containers[0].resources.limits.memory, cpuThrottling: .spec.template.metadata.annotations."run.googleapis.com/cpu-throttling", startupCpuBoost: .spec.template.metadata.annotations."run.googleapis.com/startup-cpu-boost"}'
```

### 4. Concurrency and Performance

```bash
# Check request metrics
gcloud monitoring time-series list \
  --filter="metric.type=\"run.googleapis.com/request_count\" AND resource.labels.service_name=\"$SERVICE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Check instance count
gcloud monitoring time-series list \
  --filter="metric.type=\"run.googleapis.com/container/instance_count\" AND resource.labels.service_name=\"$SERVICE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Request latency
gcloud monitoring time-series list \
  --filter="metric.type=\"run.googleapis.com/request_latencies\" AND resource.labels.service_name=\"$SERVICE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json
```

### 5. IAM and Ingress Configuration

```bash
# Check IAM policy (who can invoke)
gcloud run services get-iam-policy "$SERVICE" --region="$REGION" --format=json

# Check ingress settings
gcloud run services describe "$SERVICE" --region="$REGION" --format=json \
  | jq '{ingress: .metadata.annotations."run.googleapis.com/ingress", vpcAccess: .spec.template.metadata.annotations."run.googleapis.com/vpc-access-connector", vpcEgress: .spec.template.metadata.annotations."run.googleapis.com/vpc-access-egress"}'
```

## Output Format

Present results as a structured report:
```
Gcp Cloud Run Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

1. **Scale to zero**: Min instances of 0 (default) means cold starts. Set `autoscaling.knative.dev/minScale` annotation for latency-sensitive services.
2. **CPU throttling**: By default, CPU is only allocated during request processing. Set `cpu-throttling=false` for background tasks, but this increases cost.
3. **Concurrency vs instances**: Low concurrency with high traffic spawns many instances. Default concurrency is 80. Tune based on actual workload.
4. **Ingress restrictions**: `internal` ingress blocks all public traffic. `internal-and-cloud-load-balancing` allows GLB but not direct access.
5. **Container contract**: Cloud Run expects the container to listen on the PORT environment variable (default 8080), not a hardcoded port.
