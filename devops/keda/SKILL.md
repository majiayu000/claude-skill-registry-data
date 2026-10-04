---
name: keda
description: "Configure Kubernetes Event-driven Autoscaling (KEDA); deploy ScaledObjects, ScaledJobs, TriggerAuthentications, and queue/metric-driven autoscalers."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["keda", "kubernetes", "autoscaling", "event-driven", "prometheus", "kafka", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# KEDA (Kubernetes Event-driven Autoscaling) AI Skill Guide

## Overview & Engine Architecture

KEDA (Kubernetes Event-driven Autoscaling) is a CNCF graduated project that enables fine-grained autoscaling (including scaling to and from zero: $0 \leftrightarrow N$) for any container in Kubernetes based on event metrics from external systems (e.g., Kafka, RabbitMQ, Redis, AWS SQS, Azure Service Bus, GCP Pub/Sub, Prometheus). While standard Kubernetes Horizontal Pod Autoscaler (HPA) is restricted to CPU and memory metrics, KEDA acts as a custom metrics adapter, translating external queue lag or metric counts into an automated HPA resource definition.

Claude operates as a Principal Kubernetes Infrastructure & Platform Engineer, specializing in **KEDA ScaledObject and ScaledJob definitions**, **TriggerAuthentication security bindings**, **metric threshold tuning**, **cooldown period stabilization**, and **scale-to-zero worker pipelines**.

### KEDA Architecture & Autoscaling Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                       KEDA Architecture                     │
│                                                             │
│  External Event Sources (Kafka, RabbitMQ, SQS, Prometheus)  │
│  └── Queue Lag / Message Backlog / Metric Telemetry         │
│                                                             │
│  KEDA Operator & Controller                                 │
│  ├── ScaledObject / ScaledJob CRD Controller                │
│  ├── Activator (Detects $0 \rightarrow 1$ Scale-Up Event)   │
│  └── TriggerAuthentication (Decoupled Secret References)    │
│                                                             │
│  KEDA External Metrics Server                               │
│  └── Exposes External Metrics to Kubernetes API Server      │
│                                                             │
│  Kubernetes Native Core                                     │
│  ├── Horizontal Pod Autoscaler (HPA) (Auto-Managed by KEDA) │
│  └── Target Workload (Deployment / StatefulSet / Job Pods)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Never Manually Create HPAs for KEDA Workloads**: KEDA dynamically creates, manages, and updates the underlying Kubernetes `HorizontalPodAutoscaler` object for each `ScaledObject`. Creating a manual HPA against the same target causes severe controller race conditions and flapping.
2. **Decouple Credentials with TriggerAuthentication**: Never embed plain-text connection strings or passwords inside `ScaledObject` trigger definitions. Always use `TriggerAuthentication` or `ClusterTriggerAuthentication` pointing to Kubernetes Secrets, HashiCorp Vault, or cloud IAM identities (AWS IRSA / Azure Workload Identity).
3. **Prevent Pod Flapping with Cooldown Periods**: Set an adequate `cooldownPeriod` (e.g., 300 seconds) and configure HPA behavior stabilization windows (`scaleDown.stabilizationWindowSeconds`) to prevent rapid oscillations when queue lengths drop intermittently.
4. **Choose ScaledJobs for Long-Running Tasks**: If processing an individual message takes minutes to hours (e.g., video transcoding or AI batch training), use a `ScaledJob` instead of a `ScaledObject` to spin up isolated, self-terminating Kubernetes Jobs per work item.

---

## Production Kubernetes YAML Automation: Queue Worker Autoscaling

Save this manifest as `keda-rabbitmq-autoscaler.yaml` to deploy an event-driven worker with automatic $0 \leftrightarrow N$ scaling based on queue depth:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rabbitmq-credentials
  namespace: processing
type: Opaque
stringData:
  host: "amqp://guest:guest@rabbitmq.processing.svc.cluster.local:5672/"
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: keda-rabbitmq-auth
  namespace: processing
spec:
  secretTargetRef:
    - parameter: host
      name: rabbitmq-credentials
      key: host
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-processor
  namespace: processing
spec:
  replicas: 0 # Scales from zero automatically via KEDA
  selector:
    matchLabels:
      app: order-processor
  template:
    metadata:
      labels:
        app: order-processor
    spec:
      containers:
        - name: worker
          image: mycompany/order-processor:v1.2.0
          env:
            - name: RABBITMQ_URL
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-credentials
                  key: host
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor-scaler
  namespace: processing
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-processor
  minReplicaCount: 0 # Enables scale-to-zero when queue is empty
  maxReplicaCount: 20
  cooldownPeriod: 300 # Seconds to wait before scaling to zero
  pollingInterval: 15 # Seconds between metric checks
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
            - type: Percent
              value: 50
              periodSeconds: 60
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        queueName: customer-orders
        mode: QueueLength
        value: "20" # Target 20 messages per pod replica
      authenticationRef:
        name: keda-rabbitmq-auth
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`ScaledObject` status shows `Ready: False`** | KEDA operator cannot authenticate to external trigger or target resource doesn't exist. | 1. Run `kubectl describe scaledobject <name> -n <ns>`.<br>2. Check `TriggerAuthentication` secret references.<br>3. Verify network reachability from KEDA operator pod to external broker. |
| **Workload will not scale to zero (`minReplicaCount: 0`)** | Active HTTP connection, lingering messages in dead-letter queue, or `cooldownPeriod` hasn't expired. | Inspect trigger metrics to confirm queue depth is strictly 0 and wait for `cooldownPeriod` to elapse. |
| **HPA reports `unable to get external metric`** | KEDA Metrics Server is unready or TLS certificates between API server and KEDA metrics adapter failed. | 1. Check KEDA metrics server pods: `kubectl get pods -n keda`.<br>2. Test APIService status: `kubectl get apiservice v1beta1.external.metrics.k8s.io`. |
| **Pod thrashing (rapid scale up followed by immediate scale down)** | Metric threshold (`value`) is too low or downstream processing empties queue faster than stabilization window. | Increase trigger threshold `value` and configure `scaleDown.stabilizationWindowSeconds` to 300s. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Inspect ScaledObject operational status and conditions
kubectl get scaledobjects -n processing
kubectl describe scaledobject order-processor-scaler -n processing

# 2. Inspect auto-generated HPA created by KEDA
kubectl get hpa keda-hpa-order-processor-scaler -n processing

# 3. View real-time logs from KEDA Operator controller
kubectl logs -f -n keda -l app.kubernetes.io/name=keda-operator

# 4. Temporarily pause KEDA autoscaling for maintenance
kubectl annotate scaledobject order-processor-scaler autoscaling.keda.sh/paused="true" -n processing
```

---

## Agent Operational Directive

> **MANDATORY**: Never declare manual `HorizontalPodAutoscaler` objects for workloads managed by KEDA. Always inspect `kubectl describe scaledobject` to verify trigger authentication and metrics adapter health.
