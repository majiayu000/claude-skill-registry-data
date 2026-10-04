---
name: observer-reporter
description: Monitor, observe, and report on infrastructure health, application metrics, and system observability. Use when setting up monitoring, creating dashboards, configuring alerts, or analyzing system metrics.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# DevOps Observer Reporter Skill

You are a Senior DevOps Engineer specializing in observability, monitoring, and reporting. You design and implement comprehensive monitoring solutions, create insightful dashboards, configure intelligent alerting, and generate actionable reports.

## Core Responsibilities

1. **Metrics Collection**
   - Prometheus/Grafana setup
   - Application metrics instrumentation
   - Infrastructure metrics
   - Business metrics tracking

2. **Logging**
   - Centralized logging (ELK, Loki, CloudWatch)
   - Log aggregation and parsing
   - Log retention policies
   - Structured logging standards

3. **Tracing**
   - Distributed tracing (Jaeger, Zipkin, Tempo)
   - Service mesh observability
   - Trace correlation
   - Performance analysis

4. **Alerting**
   - Alert routing and escalation
   - On-call rotations
   - Alert fatigue reduction
   - SLO/SLI monitoring

5. **Dashboards**
   - Executive dashboards
   - Operational runbooks
   - Capacity planning
   - Cost analysis

## Monitoring Stack

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    region: us-east-1

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Kubernetes API Server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

  # Kubernetes Nodes
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      insecure_skip_verify: true
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Kubernetes Pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

  # Application Metrics
  - job_name: 'application'
    static_configs:
      - targets: ['app:8080']
    metrics_path: /metrics
    scrape_interval: 5s
```

### Prometheus Recording Rules

```yaml
# recording-rules.yml
groups:
  - name: infrastructure
    interval: 30s
    rules:
      - record: instance:node_cpu_utilisation:rate5m
        expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      - record: instance:node_memory_utilisation:ratio
        expr: 1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

      - record: cluster:node_cpu_saturation_load1:
        expr: |
          node_load1
          /
          instance:node_num_cpu:sum

  - name: slo
    interval: 5m
    rules:
      - record: slo:api_availability:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{job="api",code=~"2.."}[5m]))
          /
          sum(rate(http_requests_total{job="api"}[5m]))

      - record: slo:api_latency:ratio_rate5m
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{job="api"}[5m])) by (le)
          )
```

### Alerting Rules

```yaml
# alert-rules.yml
groups:
  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: instance:node_cpu_utilisation:rate5m > 80
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% (current value: {{ $value }}%)"

      - alert: HighMemoryUsage
        expr: instance:node_memory_utilisation:ratio > 0.85
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% (current value: {{ $value | humanizePercentage }})"

      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{fstype!="tmpfs"}
            /
            node_filesystem_size_bytes{fstype!="tmpfs"}
          ) < 0.1
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is below 10% (mountpoint: {{ $labels.mountpoint }})"

  - name: application
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.01
        for: 2m
        labels:
          severity: critical
          team: oncall
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 1% (current: {{ $value | humanizePercentage }})"

      - alert: SLOBudgetBurn
        expr: |
          (
            (
              1 - slo:api_availability:ratio_rate5m
            ) - (1 - 0.99)
          ) / (1 - 0.99) > 14.4
          and
          (
            1 - slo:api_availability:ratio_rate1h
          ) - (1 - 0.99) > (1 - 0.99) * 0.028
        labels:
          severity: warning
        annotations:
          summary: "SLO budget burn rate is high"
          description: "Burn rate is {{ $value }}x faster than acceptable"

      - alert: PodCrashLooping
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
          team: oncall
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"
          description: "Pod has restarted {{ $value }} times in the last 15 minutes"
```

## Grafana Dashboards

### Infrastructure Dashboard

```json
{
  "dashboard": {
    "title": "Infrastructure Overview",
    "tags": ["infrastructure", "prometheus"],
    "timezone": "UTC",
    "panels": [
      {
        "id": 1,
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "instance:node_cpu_utilisation:rate5m",
            "legendFormat": "{{ instance }}"
          }
        ],
        "yAxes": [
          {
            "label": "Percentage",
            "max": 100,
            "min": 0
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"type": "gt", "params": [80]},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "reducer": {"type": "avg"},
              "type": "query"
            }
          ]
        }
      },
      {
        "id": 2,
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "instance:node_memory_utilisation:ratio * 100",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Disk I/O",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(node_disk_io_time_seconds_total[5m])",
            "legendFormat": "{{ device }}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Network Traffic",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "{{ device }} - RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "{{ device }} - TX"
          }
        ]
      }
    ]
  }
}
```

### SLO Dashboard

```json
{
  "dashboard": {
    "title": "SLO Compliance",
    "panels": [
      {
        "id": 1,
        "title": "Availability SLO",
        "type": "stat",
        "targets": [
          {
            "expr": "slo:api_availability:ratio_rate5m",
            "legendFormat": "Current"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 0.99},
                {"color": "green", "value": 0.999}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Error Budget",
        "type": "gauge",
        "targets": [
          {
            "expr": "(1 - slo:api_availability:ratio_rate30d) / (1 - 0.99)"
          }
        ]
      },
      {
        "id": 3,
        "title": "Burn Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "(
              (1 - slo:api_availability:ratio_rate1h) - (1 - 0.99)
            ) / (1 - 0.99)"
          }
        ]
      }
    ]
  }
}
```

## Logging Configuration

### Loki

```yaml
# loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  max_chunk_age: 1h
  chunk_target_size: 1048576
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 168h

storage_config:
  boltdb:
    directory: /tmp/loki/index
  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

### Promtail Configuration

```yaml
# promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - docker: {}
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: replace
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod
```

## Distributed Tracing

### Jaeger

```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: simplest
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  ingress:
    enabled: true
```

### OpenTelemetry Collector

```yaml
# otel-collector-config.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  resource:
    attributes:
      - key: environment
        value: production
        action: upsert

exporters:
  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: true

  prometheus:
    endpoint: 0.0.0.0:8889

  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```

## Reporting

### Cost Reporting

```python
#!/usr/bin/env python3
# scripts/cost_report.py

import boto3
import datetime
from dataclasses import dataclass
from typing import List
import pandas as pd

@dataclass
class CostData:
    service: str
    amount: float
    date: datetime.date

class CostReporter:
    def __init__(self):
        self.client = boto3.client('ce')

    def get_costs(self, start_date: str, end_date: str) -> List[CostData]:
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )

        costs = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                costs.append(CostData(
                    service=group['Keys'][0],
                    amount=float(group['Metrics']['BlendedCost']['Amount']),
                    date=datetime.datetime.strptime(date, '%Y-%m-%d').date()
                ))
        return costs

    def generate_report(self, days: int = 30) -> pd.DataFrame:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)

        costs = self.get_costs(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

        df = pd.DataFrame(costs)
        pivot = df.pivot_table(
            index='date',
            columns='service',
            values='amount',
            aggfunc='sum'
        ).fillna(0)

        return pivot

    def export_to_html(self, df: pd.DataFrame, output_path: str):
        html = df.to_html(
            classes='table table-striped',
            float_format='${:,.2f}'.format
        )

        with open(output_path, 'w') as f:
            f.write(f"""
            <html>
            <head>
                <title>Cost Report</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container mt-5">
                    <h1>AWS Cost Report</h1>
                    <p>Generated: {datetime.datetime.now()}</p>
                    {html}
                </div>
            </body>
            </html>
            """)

if __name__ == "__main__":
    reporter = CostReporter()
    report = reporter.generate_report()
    reporter.export_to_html(report, 'cost_report.html')
    print(f"Total cost: ${report.sum().sum():,.2f}")
```

### Daily Status Report

```bash
#!/bin/bash
# scripts/daily_report.sh

REPORT_FILE="/tmp/daily_report_$(date +%Y%m%d).md"

cat > $REPORT_FILE << EOF
# Daily Infrastructure Report

**Date:** $(date)
**Generated by:** DevOps Observer Reporter

## System Status

### Kubernetes Cluster
EOF

# Get cluster status
echo "#### Nodes" >> $REPORT_FILE
kubectl get nodes -o wide >> $REPORT_FILE 2>&1 || echo "Error fetching nodes" >> $REPORT_FILE

echo "#### Pods (Warning/Error)" >> $REPORT_FILE
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded >> $REPORT_FILE 2>&1 || echo "No pods with warnings" >> $REPORT_FILE

# Get Prometheus metrics
echo "" >> $REPORT_FILE
echo "### Key Metrics" >> $REPORT_FILE

echo "#### CPU Usage (Top 5)" >> $REPORT_FILE
curl -s "http://prometheus:9090/api/v1/query?query=topk(5,instance:node_cpu_utilisation:rate5m)" | jq -r '.data.result[] | "- \(.metric.instance): \(.value[1])%"' >> $REPORT_FILE 2>&1

echo "#### Memory Usage (Top 5)" >> $REPORT_FILE
curl -s "http://prometheus:9090/api/v1/query?query=topk(5,instance:node_memory_utilisation:ratio)" | jq -r '.data.result[] | "- \(.metric.instance): \(.value[1])"' >> $REPORT_FILE 2>&1

echo "#### Error Rate" >> $REPORT_FILE
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{code=~\"5..\"}[1h]))" | jq -r '.data.result[] | "- \(.value[1]) errors/sec"' >> $REPORT_FILE 2>&1

# Cost info
echo "" >> $REPORT_FILE
echo "### Cost Overview" >> $REPORT_FILE
echo "See detailed cost report at: https://grafana.company.com/d/cost-dashboard" >> $REPORT_FILE

# Send report
if command -v slack &> /dev/null; then
    slack upload --file $REPORT_FILE --channels "#infrastructure-alerts"
fi

echo "Report generated: $REPORT_FILE"
```

## Health Checks

```yaml
# health-check-config.yml
probes:
  - name: api-health
    type: http
    interval: 30s
    timeout: 5s
    config:
      url: http://api/health
      method: GET
      expected_status: 200
      expected_body: '{"status":"ok"}'

  - name: database-connectivity
    type: tcp
    interval: 60s
    timeout: 10s
    config:
      host: postgres.database
      port: 5432

  - name: certificate-expiry
    type: tls
    interval: 24h
    config:
      host: api.example.com
      port: 443
      min_days_valid: 30

  - name: dns-resolution
    type: dns
    interval: 300s
    config:
      nameserver: 8.8.8.8
      domains:
        - api.example.com
        - database.example.com

alerts:
  - name: api-down
    condition: probe_success{probe="api-health"} == 0
    for: 2m
    severity: critical

  - name: database-unreachable
    condition: probe_success{probe="database-connectivity"} == 0
    for: 1m
    severity: critical

  - name: cert-expiring
    condition: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
    severity: warning
```

## Observability Checklist

- [ ] Metrics collection configured
- [ ] Alerting rules defined
- [ ] Dashboards created
- [ ] Logging centralized
- [ ] Distributed tracing enabled
- [ ] SLOs defined and monitored
- [ ] On-call rotations configured
- [ ] Runbooks documented
- [ ] Cost monitoring enabled
- [ ] Performance baselines established