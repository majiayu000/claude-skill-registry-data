---
name: knative-serving
description: Deploy serverless workloads with Knative Serving for scale-to-zero and autoscaling. Use for creating Knative Services, configuring autoscaling, traffic splitting, and revisions. Triggers on "knative service", "scale-to-zero", "serverless deployment", "ksvc", "knative autoscaling", "traffic splitting", or when deploying agents as serverless workloads.
---

# Knative Serving

## Overview

Deploy AI agents as serverless workloads using Knative Serving, enabling automatic scale-to-zero and request-based autoscaling.

## Knative Architecture

```
                    Request
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      Knative Service                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Route                                                │  │
│  │  • Traffic splitting between revisions                │  │
│  │  • A/B testing, canary deployments                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Configuration                                        │  │
│  │  • Desired state specification                        │  │
│  │  • Creates new Revision on each update                │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Revision (Immutable)                                 │  │
│  │  • Snapshot of code + config                          │  │
│  │  • Autoscaled via KPA/HPA                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Knative Service Definition

### Basic Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: customer-support-agent
  namespace: agents
  labels:
    agentstack.io/agent-id: agt_abc123
    agentstack.io/project-id: prj_xyz789
    agentstack.io/framework: google-adk
spec:
  template:
    metadata:
      annotations:
        # Autoscaling configuration
        autoscaling.knative.dev/class: kpa.autoscaling.knative.dev
        autoscaling.knative.dev/metric: concurrency
        autoscaling.knative.dev/target: "10"
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "100"
        autoscaling.knative.dev/scale-down-delay: "30s"
        # Container configuration
        autoscaling.knative.dev/initial-scale: "1"
    spec:
      containerConcurrency: 10
      timeoutSeconds: 300  # 5 minutes for LLM calls
      containers:
        - image: ghcr.io/raphaelmansuy/customer-support-agent:v1.0.0
          ports:
            - containerPort: 8080
              protocol: TCP
          env:
            - name: AGENT_ID
              value: "agt_abc123"
            - name: PROJECT_ID
              value: "prj_xyz789"
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: agent-secrets
                  key: OPENAI_API_KEY
          resources:
            requests:
              cpu: 100m
              memory: 512Mi
            limits:
              cpu: 2000m
              memory: 2Gi
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Production Service with Queue-Proxy Config

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: enterprise-agent
  namespace: agents
  annotations:
    # Revision history limit
    serving.knative.dev/rolloutDuration: "120s"
spec:
  template:
    metadata:
      annotations:
        # Use HPA for production
        autoscaling.knative.dev/class: hpa.autoscaling.knative.dev
        autoscaling.knative.dev/metric: cpu
        autoscaling.knative.dev/target: "70"
        autoscaling.knative.dev/min-scale: "2"
        autoscaling.knative.dev/max-scale: "50"
        # Queue-proxy settings
        queue.sidecar.serving.knative.dev/resourcePercentage: "20"
    spec:
      containerConcurrency: 0  # Unlimited (use with HPA)
      timeoutSeconds: 600
      serviceAccountName: agent-runner
      containers:
        - image: ghcr.io/raphaelmansuy/enterprise-agent:v2.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 4000m
              memory: 4Gi
          volumeMounts:
            - name: model-cache
              mountPath: /cache
      volumes:
        - name: model-cache
          emptyDir:
            sizeLimit: 5Gi
```

## Autoscaling Configuration

### Concurrency-Based (KPA) - Default

Best for request-heavy workloads:

```yaml
annotations:
  autoscaling.knative.dev/class: kpa.autoscaling.knative.dev
  autoscaling.knative.dev/metric: concurrency
  autoscaling.knative.dev/target: "10"       # Target concurrent requests per pod
  autoscaling.knative.dev/target-utilization-percentage: "70"
```

### CPU-Based (HPA)

Best for compute-intensive agents:

```yaml
annotations:
  autoscaling.knative.dev/class: hpa.autoscaling.knative.dev
  autoscaling.knative.dev/metric: cpu
  autoscaling.knative.dev/target: "70"       # Target CPU percentage
```

### RPS-Based

For rate-limited scenarios:

```yaml
annotations:
  autoscaling.knative.dev/class: kpa.autoscaling.knative.dev
  autoscaling.knative.dev/metric: rps
  autoscaling.knative.dev/target: "100"      # Target requests per second
```

### Scale Bounds

```yaml
annotations:
  autoscaling.knative.dev/min-scale: "0"     # Scale to zero (default)
  autoscaling.knative.dev/max-scale: "100"   # Maximum replicas
  autoscaling.knative.dev/initial-scale: "1" # Initial pods on deploy
```

### Scale-Down Delay

Prevent thrashing:

```yaml
annotations:
  autoscaling.knative.dev/scale-down-delay: "30s"    # Wait before scaling down
  autoscaling.knative.dev/stable-window: "60s"       # Stability window
  autoscaling.knative.dev/panic-window-percentage: "10"
  autoscaling.knative.dev/panic-threshold-percentage: "200"
```

## Traffic Splitting

### Canary Deployment

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: customer-support-agent
spec:
  template:
    metadata:
      name: customer-support-agent-v2
    spec:
      containers:
        - image: ghcr.io/raphaelmansuy/customer-support-agent:v2.0.0
  traffic:
    - revisionName: customer-support-agent-v1
      percent: 90
    - revisionName: customer-support-agent-v2
      percent: 10
```

### Blue-Green Deployment

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: customer-support-agent
spec:
  template:
    metadata:
      name: customer-support-agent-green
    spec:
      containers:
        - image: ghcr.io/raphaelmansuy/customer-support-agent:v2.0.0
  traffic:
    # Route all traffic to previous version
    - revisionName: customer-support-agent-blue
      percent: 100
    # Tag new version for testing
    - revisionName: customer-support-agent-green
      percent: 0
      tag: green  # Accessible at green-<service>.<domain>
```

### Rollout Complete Traffic

```yaml
traffic:
  - revisionName: customer-support-agent-green
    percent: 100
  - revisionName: customer-support-agent-blue
    percent: 0
```

## Private Services (Internal Only)

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: internal-agent
  labels:
    networking.knative.dev/visibility: cluster-local
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/raphaelmansuy/internal-agent:v1.0.0
```

## Domain Mapping

```yaml
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: support.agentstack.io
  namespace: agents
spec:
  ref:
    name: customer-support-agent
    kind: Service
    apiVersion: serving.knative.dev/v1
```

## ConfigMaps for Global Settings

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-autoscaler
  namespace: knative-serving
data:
  # Global defaults
  container-concurrency-target-default: "100"
  container-concurrency-target-percentage: "0.7"
  enable-scale-to-zero: "true"
  scale-to-zero-grace-period: "30s"
  scale-to-zero-pod-retention-period: "0s"
  stable-window: "60s"
  panic-window-percentage: "10.0"
  panic-threshold-percentage: "200.0"
  max-scale: "100"
```

## Observability Integration

### Enable Metrics

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-observability
  namespace: knative-serving
data:
  metrics.backend-destination: prometheus
  metrics.request-metrics-backend-destination: prometheus
  metrics.opencensus-address: ""
```

### Enable Tracing

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-tracing
  namespace: knative-serving
data:
  backend: zipkin
  zipkin-endpoint: "http://zipkin.observability:9411/api/v2/spans"
  sample-rate: "0.1"
```

## Resources

- `references/cold-start-optimization.md` - Reducing cold start latency
- `references/kagent-integration.md` - Integrating with kagent orchestrator
- `assets/service-template.yaml` - Base service template
