---
name: python-micrometer-gcp-cloud-monitoring
description: |
  Export Micrometer metrics to GCP Cloud Monitoring (Stackdriver) for GKE deployments.
  Use when setting up metrics export in Kubernetes environments, configuring Workload Identity,
  managing metric prefixes and resource labels, or correlating metrics with GCP services.
  Critical for GKE-based microservices with centralized observability in Google Cloud.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer GCP Cloud Monitoring Integration

## Table of Contents

1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [Quick Start](#quick-start)
4. [Instructions](#instructions)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
8. [See Also](#see-also)

---

## Purpose

GCP Cloud Monitoring (formerly Stackdriver) is the native monitoring system for Google Cloud. This skill covers configuring Micrometer to export metrics to Cloud Monitoring, setting up authentication via Workload Identity, and managing metric naming and resource labels for proper dashboard integration.

## When to Use

Use this skill when you need to:

- **Export metrics to GCP** - Send Micrometer metrics to Cloud Monitoring for GKE deployments
- **Configure Workload Identity** - Set up secure authentication for pods to write metrics without service account keys
- **Set resource labels** - Add GKE-specific labels (cluster, namespace, pod) for filtering in Cloud Console
- **Create Cloud Monitoring dashboards** - Visualize custom metrics in GCP monitoring UI
- **Set up metric-based alerting** - Create alert policies based on exported Micrometer metrics
- **Correlate with GCP services** - Link application metrics with GKE, Pub/Sub, Cloud SQL, and other GCP resources
- **Monitor GKE microservices** - Centralize observability for multiple services in one GCP project

**When NOT to use:**
- For Prometheus-only environments (use Prometheus registry instead)
- Before basic Micrometer setup (use `python-micrometer-metrics-setup` first)
- For local development (expensive to export locally; use Prometheus locally)
- When Workload Identity isn't available (requires GKE 1.12+ with feature enabled)

---

## Quick Start

Add dependency and configure export:

**pom.xml:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-stackdriver</artifactId>
</dependency>

<dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>spring-cloud-gcp-starter-metrics</artifactId>
</dependency>
```

**application.yml:**
```yaml
management:
  metrics:
    export:
      stackdriver:
        enabled: true
        project-id: ${GCP_PROJECT_ID}
        resource-type: k8s_container
        step: 1m
        resource-labels:
          cluster_name: ${GKE_CLUSTER_NAME}
          namespace_name: ${NAMESPACE}
          pod_name: ${POD_NAME}
```

**Deploy with Workload Identity:**
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"
```

## Instructions

### Step 1: Add Dependencies

**Maven:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-stackdriver</artifactId>
    <!-- Version inherited from Spring Boot BOM -->
</dependency>

<!-- Optional: Spring Cloud GCP integration for easier config -->
<dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>spring-cloud-gcp-starter-metrics</artifactId>
</dependency>

<!-- For Workload Identity: auto-detects credentials in GKE -->
<dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>google-cloud-core</artifactId>
</dependency>
```

**Gradle:**
```groovy
dependencies {
    implementation 'io.micrometer:micrometer-registry-stackdriver'
    implementation 'com.google.cloud:spring-cloud-gcp-starter-metrics'
    implementation 'com.google.cloud:google-cloud-core'
}
```

### Step 2: Configure Stackdriver Export

Create comprehensive configuration in `application.yml`:

```yaml
management:
  # Enable/disable export
  metrics:
    export:
      stackdriver:
        enabled: ${STACKDRIVER_ENABLED:true}

        # GCP Project ID (where metrics are stored)
        project-id: ${GCP_PROJECT_ID:my-project}

        # Metric export frequency (1m = 60 second batches)
        step: ${METRIC_EXPORT_STEP:1m}

        # Resource type for GKE (not "gce_instance")
        resource-type: k8s_container

        # Batching configuration
        batch-size: 10000  # Max metrics per batch
        use-insecure: false
        use-compression: true

        # Connection timeouts (total batch retry duration ~5 minutes)
        connect-timeout: 5s
        read-timeout: 10s

        # Resource labels attached to EVERY metric
        resource-labels:
          # GKE-specific labels (required for proper filtering)
          cluster_name: ${GKE_CLUSTER_NAME:local-cluster}
          namespace_name: ${NAMESPACE:default}
          pod_name: ${POD_NAME:unknown-pod}
          container_name: ${CONTAINER_NAME:app}

          # Optional: custom resource labels
          environment: ${ENVIRONMENT:development}
          region: ${GCP_REGION:europe-west2}
          application: ${spring.application.name}

        # Metric naming prefix (custom.googleapis.com = custom namespace)
        use-default-instrumentation: true

        # Optional: disable specific metric exports
        disabled-meters:
          - "jvm.threads"  # Too verbose
          - "logback.events.total"  # Too many variations

    # Common tags applied to ALL metrics
    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:development}
      region: ${GCP_REGION:europe-west2}
      version: ${BUILD_VERSION:unknown}

    # Histogram configuration (important for Stackdriver)
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s,2s,5s
```

### Step 3: Set Up Workload Identity (GKE)

Workload Identity allows pods to authenticate to GCP without managing keys:

**Step 3a: Create GCP Service Account**
```bash
# Set project variables
export PROJECT_ID="my-project"
export SERVICE_ACCOUNT="supplier-charges-api"
export NAMESPACE="supplier-charges"

# Create Google Service Account
gcloud iam service-accounts create ${SERVICE_ACCOUNT} \
  --display-name="Service Account for Supplier Charges API"

# Grant metric writing permission
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"

# Optional: grant Cloud Logging permission for structured logs
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"
```

**Step 3b: Create Kubernetes Service Account**
```yaml
# kubernetes/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: supplier-charges-api
  namespace: supplier-charges
  annotations:
    # Link to GCP Service Account
    iam.gke.io/gcp-service-account: supplier-charges-api@PROJECT_ID.iam.gserviceaccount.com
```

**Step 3c: Bind Kubernetes SA to GCP SA**
```bash
# Allow Kubernetes SA to impersonate GCP SA
gcloud iam service-accounts add-iam-policy-binding \
  ${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${SERVICE_ACCOUNT}]"
```

**Step 3d: Use Service Account in Deployment**
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-api
  namespace: supplier-charges
spec:
  template:
    metadata:
      annotations:
        # Node pool where Workload Identity is enabled
        workload-identity/enable: "true"

    spec:
      # Reference Kubernetes Service Account
      serviceAccountName: supplier-charges-api

      containers:
      - name: app
        image: gcr.io/my-project/supplier-charges-api:latest
        ports:
        - containerPort: 8080

        env:
        # GCP project configuration
        - name: GCP_PROJECT_ID
          value: "my-project"

        - name: STACKDRIVER_ENABLED
          value: "true"

        # GKE resource labels
        - name: GKE_CLUSTER_NAME
          value: "supplier-charges-gke"

        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace

        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name

        - name: CONTAINER_NAME
          value: "app"

        - name: ENVIRONMENT
          value: "production"

        - name: GCP_REGION
          value: "europe-west2"
```

### Step 4: Configure Metric Naming and Metadata

Customize metric names and descriptions:

```java
@Configuration
public class CloudMonitoringMetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> customizeMetricNames() {
        return registry -> {
            // Set metric descriptions (appear in Cloud Monitoring)
            registry.config().meterFilter(
                new MeterFilter() {
                    @Override
                    public DistributionStatisticConfig configure(Meter.Id id, DistributionStatisticConfig config) {
                        return config;
                    }

                    @Override
                    public MeterFilterReply accept(Meter.Id id) {
                        // Set descriptions for custom metrics
                        if (id.getName().equals("charge.approved")) {
                            // Descriptions are optional but help in GCP UI
                        }
                        return MeterFilterReply.NEUTRAL;
                    }
                }
            );
        };
    }

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> addGCPMetadata() {
        return registry -> {
            // Common tags appear in metric filters
            registry.config().commonTags(
                "service", "supplier-charges-api",
                "version", "1.0.0",
                "component", "api"
            );
        };
    }
}
```

### Step 5: Test Metric Export

Verify metrics appear in Cloud Monitoring:

**Check logs for export confirmation:**
```bash
# View pod logs for metric export
kubectl logs -f deployment/supplier-charges-api -n supplier-charges

# Look for messages like:
# "Successfully published X metrics to Stackdriver"
# or "Failed to export metrics: ..."
```

**View metrics in Cloud Console:**
```
1. Open GCP Console → Cloud Monitoring → Metrics
2. Select resource type: "Kubernetes Container"
3. Filter by cluster: supplier-charges-gke
4. View metric type: custom.googleapis.com/charge/...
```

**Query via gcloud CLI:**
```bash
# List all metrics for your project
gcloud monitoring metrics-descriptors list \
  --filter="metric.type:custom.googleapis.com"

# Example output:
# metric.type: custom.googleapis.com/charge/approved
# description: "Charges approved for payment"
# unit: "1" (dimensionless)
```

### Step 6: Create Cloud Monitoring Dashboard

Visualize exported metrics:

```yaml
# terraform/cloud_monitoring.tf
resource "google_monitoring_dashboard" "supplier_charges" {
  dashboard_json = jsonencode({
    displayName = "Supplier Charges API - Metrics"
    mosaicLayout = {
      columns = 12
      tiles = [
        {
          width  = 6
          height = 4
          xyChart = {
            dataSources = [
              {
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"custom.googleapis.com/charge/approved\" resource.type=\"k8s_container\""
                  }
                }
              }
            ]
            timeshiftDuration = "0s"
            yAxis = {
              label = "Charges Approved"
            }
          }
        },
        {
          width  = 6
          height = 4
          xyChart = {
            dataSources = [
              {
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"custom.googleapis.com/charge/value\" resource.type=\"k8s_container\""
                  }
                }
              }
            ]
          }
        }
      ]
    }
  })
}
```

### Step 7: Set Up Alerting

Create alert policies based on exported metrics:

```yaml
# Alert: High charge rejection rate
resource "google_monitoring_alert_policy" "high_rejection_rate" {
  display_name = "Supplier Charges - High Rejection Rate"
  combiner     = "OR"

  conditions {
    display_name = "Rejection rate > 5%"

    condition_threshold {
      filter = <<-EOT
        metric.type="custom.googleapis.com/charge/rejected"
        resource.type="k8s_container"
        resource.label.cluster_name="supplier-charges-gke"
      EOT

      comparison      = "COMPARISON_GT"
      threshold_value = 0.05
      duration        = "300s"

      aggregations {
        alignment_period    = "60s"
        per_series_aligner  = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_SUM"
      }
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.pagerduty.id
  ]
}
```

## Examples

### Example 1: Complete Production Configuration

```yaml
# application-production.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus

  metrics:
    export:
      stackdriver:
        enabled: true
        project-id: waitrose-supplier-charges
        resource-type: k8s_container
        step: 1m
        batch-size: 5000
        connect-timeout: 5s
        read-timeout: 10s

        resource-labels:
          cluster_name: supplier-charges-prod-gke
          namespace_name: supplier-charges
          pod_name: ${POD_NAME}
          container_name: supplier-charges-api
          environment: production
          region: europe-west2

    tags:
      application: supplier-charges-api
      environment: production
      region: europe-west2
      version: ${app.version}

    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s

    enable:
      jvm: true
      process: true
      system: true
      hikaricp: true

  health:
    probes:
      enabled: true
```

### Example 2: Verify Workload Identity

```bash
#!/bin/bash
# test-workload-identity.sh

POD=$(kubectl get pod -n supplier-charges \
  -l app=supplier-charges-api \
  -o jsonpath='{.items[0].metadata.name}')

echo "Testing Workload Identity on pod: $POD"

# Check service account annotation
kubectl get sa supplier-charges-api -n supplier-charges -o yaml | \
  grep "iam.gke.io/gcp-service-account"

# Test GCP credentials from pod
kubectl exec -it $POD -n supplier-charges -- \
  gcloud auth list

# Verify Cloud Monitoring access
kubectl exec -it $POD -n supplier-charges -- \
  gcloud monitoring metrics-descriptors list \
    --filter="metric.type:custom.googleapis.com" | head -5

echo "✓ Workload Identity configured correctly"
```

### Example 3: Monitor Metric Export Health

```java
@Component
public class MetricExportHealthCheck {

    private final MeterRegistry registry;
    private long lastExportTime = System.currentTimeMillis();
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    @Scheduled(fixedRate = 60_000) // Every minute
    public void monitorExportHealth() {
        int meterCount = registry.getMeters().size();

        Gauge.builder("micrometer.export.healthy",
                      this,
                      m -> 1)  // 1 = healthy, 0 = unhealthy
             .description("Metric export health indicator")
             .register(registry);

        long currentTime = System.currentTimeMillis();
        long timeSinceExport = currentTime - lastExportTime;

        if (timeSinceExport > 90_000) { // No export for > 90 seconds
            log.warn("Metric export may be failing (no export for {} seconds)",
                     timeSinceExport / 1000);
        }
    }
}
```

## Requirements

- Spring Boot 2.1+ with Actuator
- `micrometer-registry-stackdriver` dependency
- GCP Project with Cloud Monitoring API enabled
- GKE cluster with Workload Identity enabled
- Appropriate IAM roles for service account
- Java 11+

## Anti-Patterns to Avoid

```yaml
# ❌ Avoid: Missing resource labels
resource-labels:
  # Incomplete - metrics hard to filter in Cloud Monitoring
  environment: production

# ✅ Do: Complete resource labels
resource-labels:
  cluster_name: supplier-charges-gke
  namespace_name: supplier-charges
  pod_name: ${POD_NAME}
  container_name: app

# ❌ Avoid: High cardinality resource labels
resource-labels:
  pod_ip: ${POD_IP}      # Changes constantly
  user_id: ${USER_ID}    # Unbounded values
  request_id: ${REQ_ID}  # Unique per request

# ✅ Do: Stable, bounded resource labels
resource-labels:
  cluster_name: my-cluster
  environment: production
  region: europe-west2

# ❌ Avoid: Disabling metrics without reason
stackdriver:
  enabled: false  # Why? Metrics critical for monitoring

# ✅ Do: Use environment variables for control
stackdriver:
  enabled: ${STACKDRIVER_ENABLED:true}  # Can disable if needed
```

## See Also

- [micrometer-cardinality-control](../micrometer-cardinality-control/SKILL.md) - Manage metric cardinality
- [micrometer-business-metrics](../micrometer-business-metrics/SKILL.md) - Create business metrics
- [micrometer-testing-metrics](../micrometer-testing-metrics/SKILL.md) - Test metrics
