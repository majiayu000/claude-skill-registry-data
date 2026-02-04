---
name: gcp-gke-monitoring-observability
description: |
  Set up logging, metrics, distributed tracing, and alerting for GKE applications.
  Use when configuring Cloud Logging, creating dashboards in Cloud Monitoring,
  instrumenting Spring Boot with metrics, setting up alerts for error rates or
  resource usage, or implementing distributed tracing with Cloud Trace. Includes
  Prometheus integration, structured logging patterns, and observability best
  practices for microservices.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Monitoring and Observability

## Purpose

Implement comprehensive observability for GKE applications. This skill covers logging, metrics collection, visualization, distributed tracing, and alerting strategies for Spring Boot microservices.

## When to Use

Use this skill when you need to:
- Set up Cloud Logging and Cloud Monitoring for GKE applications
- Instrument Spring Boot applications with Actuator metrics
- Configure Prometheus scraping for custom metrics
- Create dashboards to visualize application performance
- Set up alerts for error rates, resource usage, or SLOs
- Enable distributed tracing with Cloud Trace
- Debug production issues using logs and metrics

Trigger phrases: "set up monitoring", "GKE observability", "configure Prometheus", "create dashboard", "set up alerts", "enable tracing"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Enable Cloud Operations Integration](#step-1-enable-cloud-operations-integration)
  - [Step 2: Configure Spring Boot Actuator](#step-2-configure-spring-boot-actuator)
  - [Step 3: Annotate Pods for Prometheus Scraping](#step-3-annotate-pods-for-prometheus-scraping)
  - [Step 4: View Logs](#step-4-view-logs)
  - [Step 5: Create Monitoring Dashboard](#step-5-create-monitoring-dashboard)
  - [Step 6: Set Up Alerts](#step-6-set-up-alerts)
  - [Step 7: Enable Distributed Tracing](#step-7-enable-distributed-tracing)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Enable observability in three steps:

```bash
# 1. Enable Cloud Monitoring and Logging on cluster
gcloud container clusters update CLUSTER_NAME \
  --region=europe-west2 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-managed-prometheus

# 2. Deploy Prometheus scrape config for Spring Boot Actuator
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: supplier-charges-hub
  namespace: wtr-supplier-charges
spec:
  ports:
  - name: metrics
    port: 8080
    targetPort: 8080
EOF

# 3. View logs and metrics in Cloud Console
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges" --limit=50
```

## Instructions

### Step 1: Enable Cloud Operations Integration

Configure the cluster to collect logs and metrics:

```bash
gcloud container clusters update shared-gke-labs-01-euw2 \
  --region=europe-west2 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-managed-prometheus \
  --enable-cloud-logging \
  --enable-cloud-monitoring
```

**Components:**
- **Cloud Logging**: Captures container stdout/stderr
- **Cloud Monitoring**: System metrics (CPU, memory, disk)
- **Managed Service for Prometheus**: Application metrics (requires annotation)

### Step 2: Configure Spring Boot Actuator

Enable metrics and health endpoints in Spring Boot:

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,configprops
  endpoint:
    health:
      probes:
        enabled: true
      show-details: always
    metrics:
      enabled: true
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
    tags:
      application: supplier-charges-hub
      environment: labs
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
logging:
  pattern:
    console: '{"timestamp":"%d{ISO8601}","level":"%p","logger":"%c{1}","message":"%m"}%n'
```

### Step 3: Annotate Pods for Prometheus Scraping

Mark pods for metrics collection:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      containers:
      - name: supplier-charges-hub-container
        ports:
        - name: metrics
          containerPort: 8080
          protocol: TCP
```

### Step 4: View Logs

Query container logs from Cloud Logging:

```bash
# View recent logs
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges" \
  --limit=50 \
  --format=json | jq '.[] | {timestamp: .timestamp, message: .textPayload}'

# View logs with severity filter
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=wtr-supplier-charges AND severity=ERROR" \
  --limit=20

# View logs from specific pod
gcloud logging read "resource.type=k8s_pod AND resource.labels.pod_name=supplier-charges-hub-xyz123 AND resource.labels.namespace_name=wtr-supplier-charges" \
  --limit=50
```

**Alternative: View via kubectl:**

```bash
# Stream logs
kubectl logs -f deployment/supplier-charges-hub -n wtr-supplier-charges

# View logs from specific container (for multi-container pods)
kubectl logs deployment/supplier-charges-hub -c supplier-charges-hub-container -n wtr-supplier-charges

# View previous logs (after pod restart)
kubectl logs deployment/supplier-charges-hub -n wtr-supplier-charges --previous
```

### Step 5: Create Monitoring Dashboard

Visualize key metrics:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: supplier-charges-hub-metrics
  namespace: wtr-supplier-charges
spec:
  groups:
  - name: application-metrics
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: rate(http_server_requests_seconds_count{status=~"5.."}[5m]) > 0.05
      for: 5m
      annotations:
        summary: "High error rate detected"
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
      for: 10m
      annotations:
        summary: "Pod memory usage > 85%"
```

### Step 6: Set Up Alerts

Create alert policies for critical metrics:

```bash
# Create alert for high error rate
cat > alert-policy.yaml <<EOF
displayName: "Supplier Charges Hub - High Error Rate"
conditions:
  - displayName: "Error rate > 5%"
    conditionThreshold:
      filter: |
        resource.type="k8s_container"
        resource.namespace_name="wtr-supplier-charges"
        metric.type="logging.googleapis.com/user_defined_metric"
        metric.labels.severity="ERROR"
      comparison: COMPARISON_GT
      thresholdValue: 5
      duration: 300s
notificationChannels:
  - projects/ecp-wtr-supplier-charges-labs/notificationChannels/12345
EOF

# Deploy via gcloud (requires proper setup)
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

### Step 7: Enable Distributed Tracing

Add Spring Cloud Sleuth for request tracing:

```gradle
// build.gradle.kts
dependencies {
    implementation("org.springframework.cloud:spring-cloud-starter-sleuth")
    implementation("org.springframework.cloud:spring-cloud-sleuth-zipkin")
}
```

**Configuration:**

```yaml
# application.yml
spring:
  sleuth:
    sampler:
      probability: 0.1  # Sample 10% of requests
  zipkin:
    baseUrl: https://cloudtrace.googleapis.com  # Cloud Trace endpoint
```

**View traces:**

```bash
gcloud traces list --limit=10
gcloud traces describe TRACE_ID
```

## Examples

### Example 1: Complete Observability Setup

```bash
#!/bin/bash
# Set up complete observability stack for Supplier Charges Hub

CLUSTER="shared-gke-labs-01-euw2"
REGION="europe-west2"
PROJECT="ecp-wtr-supplier-charges-labs"
NAMESPACE="wtr-supplier-charges"

echo "=== Setting Up GKE Observability ==="

# Step 1: Enable cluster-level monitoring
echo ""
echo "1. Enabling Cloud Logging and Monitoring..."
gcloud container clusters update $CLUSTER \
  --region=$REGION \
  --project=$PROJECT \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-managed-prometheus

# Step 2: Apply Spring Boot metrics configuration
echo ""
echo "2. Configuring Spring Boot Actuator..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: application-config
  namespace: $NAMESPACE
data:
  application.yml: |
    management:
      endpoints:
        web:
          exposure:
            include: health,info,metrics,prometheus
      endpoint:
        health:
          probes:
            enabled: true
      metrics:
        distribution:
          percentiles-histogram:
            http.server.requests: true
      health:
        livenessState:
          enabled: true
        readinessState:
          enabled: true
    logging:
      pattern:
        console: '{"timestamp":"%d{ISO8601}","level":"%p","message":"%m"}%n'
EOF

# Step 3: Update deployment with Prometheus annotations
echo ""
echo "3. Adding Prometheus scrape annotations..."
kubectl patch deployment supplier-charges-hub \
  -n $NAMESPACE \
  -p '{"spec":{"template":{"metadata":{"annotations":{"prometheus.io/scrape":"true","prometheus.io/port":"8080","prometheus.io/path":"/actuator/prometheus"}}}}}'

# Step 4: Create sample dashboard
echo ""
echo "4. Creating Cloud Monitoring dashboard..."
# (Dashboards created via Cloud Console or Cloud Monitoring API)

echo ""
echo "Observability setup complete!"
echo ""
echo "Next steps:"
echo "1. View logs: gcloud logging read \"resource.type=k8s_container AND resource.labels.namespace_name=$NAMESPACE\" --limit=50"
echo "2. Access Cloud Console: https://console.cloud.google.com/monitoring"
echo "3. Create dashboards in Cloud Monitoring"
```

### Example 2: Log Analysis and Error Tracking

```bash
#!/bin/bash
# Query logs for errors and build report

NAMESPACE="wtr-supplier-charges"
HOURS=24

echo "=== Log Analysis Report ==="
echo ""

echo "1. Total Log Entries (last $HOURS hours)"
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=$NAMESPACE AND timestamp>=\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)\"" \
  --format="value(severity)" | wc -l

echo ""
echo "2. Error Count (last $HOURS hours)"
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=$NAMESPACE AND severity=ERROR AND timestamp>=\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)\"" \
  --limit=100 \
  --format="value(severity)"

echo ""
echo "3. Top Error Messages"
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=$NAMESPACE AND severity=ERROR AND timestamp>=\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)\"" \
  --limit=50 \
  --format="value(textPayload)" | sort | uniq -c | sort -rn | head -10

echo ""
echo "4. Exception Traces"
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=$NAMESPACE AND textPayload=~\"Exception\" AND timestamp>=\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)\"" \
  --limit=20 \
  --format="json" | jq '.[] | {pod: .resource.labels.pod_name, timestamp: .timestamp, message: .textPayload[:200]}'
```

### Example 3: Health Check Endpoint Testing

```bash
#!/bin/bash
# Test and verify observability endpoints

POD=$(kubectl get pods -l app=supplier-charges-hub -n wtr-supplier-charges -o jsonpath='{.items[0].metadata.name}')
NAMESPACE="wtr-supplier-charges"

echo "=== Testing Observability Endpoints ==="

echo ""
echo "1. Health Status"
kubectl exec $POD -c supplier-charges-hub-container -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/health | jq .

echo ""
echo "2. Application Metrics Available"
kubectl exec $POD -c supplier-charges-hub-container -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/metrics | jq '.names | length'

echo ""
echo "3. HTTP Request Metrics"
kubectl exec $POD -c supplier-charges-hub-container -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/metrics/http.server.requests | jq '.measurements[] | select(.statistic=="COUNT")'

echo ""
echo "4. JVM Memory Metrics"
kubectl exec $POD -c supplier-charges-hub-container -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/metrics/jvm.memory.used | jq '.measurements[] | select(.statistic=="VALUE")'

echo ""
echo "5. Prometheus Metrics Format"
kubectl exec $POD -c supplier-charges-hub-container -n $NAMESPACE -- \
  curl -s http://localhost:8080/actuator/prometheus | head -20
```

### Example 4: Create Custom Metrics Dashboard

```bash
#!/bin/bash
# Create a Cloud Monitoring dashboard for Supplier Charges Hub

PROJECT="ecp-wtr-supplier-charges-labs"
DASHBOARD_NAME="supplier-charges-hub-dashboard"

cat > dashboard.json <<EOF
{
  "displayName": "Supplier Charges Hub Dashboard",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "HTTP Requests Rate",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/restart_count\" resource.type=\"k8s_container\" resource.label.namespace_name=\"wtr-supplier-charges\""
                  }
                }
              }
            ]
          }
        }
      },
      {
        "xPos": 6,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Error Rate",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"logging.googleapis.com/user_defined_metric\" resource.type=\"k8s_container\" resource.label.namespace_name=\"wtr-supplier-charges\" metric.labels.severity=\"ERROR\""
                  }
                }
              }
            ]
          }
        }
      },
      {
        "yPos": 4,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Pod Memory Usage",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/memory/used_bytes\" resource.type=\"k8s_container\" resource.label.namespace_name=\"wtr-supplier-charges\""
                  }
                }
              }
            ]
          }
        }
      },
      {
        "xPos": 6,
        "yPos": 4,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Pod CPU Usage",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/cpu/core_usage_time\" resource.type=\"k8s_container\" resource.label.namespace_name=\"wtr-supplier-charges\""
                  }
                }
              }
            ]
          }
        }
      }
    ]
  }
}
EOF

# Create dashboard
gcloud monitoring dashboards create --config-from-file=dashboard.json \
  --project=$PROJECT

echo "Dashboard created: $DASHBOARD_NAME"
```

## Requirements

- GKE cluster with Cloud Logging and Cloud Monitoring enabled
- Spring Boot application with Actuator dependency
- `kubectl` access to the cluster
- `gcloud` CLI configured
- Service account with monitoring permissions: `roles/monitoring.metricWriter`

## See Also

- [gke-deployment-strategies](../gke-deployment-strategies/SKILL.md) - Understand health checks
- [gke-troubleshooting](../gke-troubleshooting/SKILL.md) - Use logs to debug issues
- [gke-cost-optimization](../gke-cost-optimization/SKILL.md) - Monitor resource costs
