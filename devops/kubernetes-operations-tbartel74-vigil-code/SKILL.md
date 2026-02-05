---
name: kubernetes-operations
description: Kubernetes deployment and operations for Vigil Guard v2.0.0. Use when deploying Vigil Guard to K8s clusters, configuring services for 11 containers including heuristics-service and semantic-service, managing namespaces, troubleshooting pods, or migrating from Docker Compose to Kubernetes.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Vigil Guard Kubernetes Operations (v2.0.0)

## Overview

Project-specific guidance for deploying and operating Vigil Guard v2.0.0 on Kubernetes clusters. This skill bridges the generic kubernetes-expert knowledge with Vigil Guard's 3-branch parallel detection architecture (11 services).

## When to Use This Skill

- Deploying Vigil Guard to Kubernetes
- Migrating from Docker Compose to K8s
- Configuring K8s services for 11 Vigil Guard components
- Deploying 3-branch detection services (heuristics, semantic, LLM Guard)
- Troubleshooting Vigil Guard pods
- Setting up monitoring (Grafana, ClickHouse) on K8s
- Managing secrets for Vigil Guard services
- Scaling Vigil Guard components

## Vigil Guard Service Architecture (v2.0.0 - 11 Services)

### 3-Branch Parallel Detection Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VIGIL GUARD v2.0.0 ON KUBERNETES                         │
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │   Caddy     │────▶│  Web UI     │────▶│  Backend    │                   │
│  │  (Ingress)  │     │  Frontend   │     │  Express    │                   │
│  └─────────────┘     └─────────────┘     └──────┬──────┘                   │
│                                                  │                          │
│  ┌──────────────────────────────────────────────┼──────────────────────────┐│
│  │                        n8n (24 nodes)        ▼                          ││
│  │  ┌─────────────────────────────────────────────────────────────────┐   ││
│  │  │              3-BRANCH PARALLEL DETECTION (v2.0.0)               │   ││
│  │  │                                                                 │   ││
│  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │   ││
│  │  │   │ Heuristics  │  │  Semantic   │  │ Prompt Guard│            │   ││
│  │  │   │  :5005      │  │   :5006     │  │   :8000     │            │   ││
│  │  │   │  (30%)      │  │   (35%)     │  │   (35%)     │            │   ││
│  │  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │   ││
│  │  │          │                │                │                    │   ││
│  │  │          └────────────────┼────────────────┘                    │   ││
│  │  │                           ▼                                     │   ││
│  │  │                    ┌─────────────┐                              │   ││
│  │  │                    │ Arbiter v2  │                              │   ││
│  │  │                    │  Decision   │                              │   ││
│  │  │                    └─────────────┘                              │   ││
│  │  └─────────────────────────────────────────────────────────────────┘   ││
│  │                                                                         ││
│  │  ┌─────────────┐  ┌─────────────┐                                      ││
│  │  │  Language   │  │  Presidio   │                                      ││
│  │  │  Detector   │  │  PII API    │                                      ││
│  │  │   :5002     │  │   :5001     │                                      ││
│  │  └─────────────┘  └─────────────┘                                      ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │              DATA LAYER                                                 ││
│  │  ┌─────────────┐     ┌─────────────┐                                   ││
│  │  │ ClickHouse  │     │   Grafana   │                                   ││
│  │  │  (Analytics)│◀────│ (Monitoring)│                                   ││
│  │  │   :8123     │     │   :3001     │                                   ││
│  │  └─────────────┘     └─────────────┘                                   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Service Port Reference (v2.0.0)

| Service | Port | Branch | Weight | Timeout | Purpose |
|---------|------|--------|--------|---------|---------|
| n8n | 5678 | - | - | - | Workflow engine |
| heuristics-service | 5005 | A | 30% | 1000ms | Pattern matching |
| semantic-service | 5006 | B | 35% | 2000ms | Embedding similarity |
| prompt-guard-api | 8000 | C | 35% | 3000ms | LLM validation |
| presidio-pii-api | 5001 | - | - | - | PII detection |
| language-detector | 5002 | - | - | - | Language detection |
| web-ui-backend | 8787 | - | - | - | Configuration API |
| web-ui-frontend | 80 | - | - | - | React UI |
| clickhouse | 8123 | - | - | - | Analytics DB |
| grafana | 3001 | - | - | - | Monitoring |
| caddy | 80 | - | - | - | Reverse proxy |

### Recommended Namespace Structure (v2.0.0)

```yaml
# Namespaces
vigil-guard:           # Main application namespace
  - n8n (StatefulSet)
  - web-ui-frontend (Deployment)
  - web-ui-backend (Deployment)
  # 3-Branch Detection (v2.0.0)
  - heuristics-service (Deployment)     # Branch A
  - semantic-service (Deployment)       # Branch B
  - prompt-guard-api (Deployment)       # Branch C
  # PII Detection
  - presidio-pii-api (Deployment)
  - language-detector (Deployment)
  - caddy (Deployment or Ingress)

vigil-monitoring:      # Monitoring namespace
  - clickhouse (StatefulSet)
  - grafana (Deployment)

vigil-secrets:         # External secrets (optional)
  - External Secrets Operator
```

## Docker Compose to Kubernetes Migration (v2.0.0)

### Mapping docker-compose.yml to K8s Resources

| Docker Compose | Kubernetes Resource | Notes |
|----------------|---------------------|-------|
| `services:` (11) | Deployment/StatefulSet | StatefulSet for n8n, ClickHouse |
| `ports:` | Service (ClusterIP/NodePort) | Use ClusterIP for internal |
| `volumes:` | PVC + PV | StorageClass for dynamic |
| `environment:` | ConfigMap + Secret | Secrets for passwords |
| `depends_on:` | initContainers | Or rely on readiness probes |
| `networks:` | Network Policies | vigil-net → vigil-network-policy |
| `restart: always` | Pod restartPolicy: Always | Default for Deployments |

### Service Configurations (v2.0.0)

#### Heuristics Service (Branch A - NEW in v2.0.0)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vigil-heuristics
  namespace: vigil-guard
  labels:
    app: vigil-heuristics
    branch: "a"
    version: "2.0.0"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vigil-heuristics
  template:
    metadata:
      labels:
        app: vigil-heuristics
        branch: "a"
    spec:
      containers:
        - name: heuristics
          image: vigil-guard/heuristics-service:2.0.0
          ports:
            - containerPort: 5005
          env:
            - name: PORT
              value: "5005"
            - name: PATTERN_TIMEOUT_MS
              value: "1000"
            - name: CONFIG_PATH
              value: "/config/unified_config.json"
          volumeMounts:
            - name: workflow-config
              mountPath: /config
              readOnly: true
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 5005
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 5005
            initialDelaySeconds: 5
            periodSeconds: 10
      volumes:
        - name: workflow-config
          configMap:
            name: vigil-workflow-config
---
apiVersion: v1
kind: Service
metadata:
  name: vigil-heuristics
  namespace: vigil-guard
spec:
  type: ClusterIP
  selector:
    app: vigil-heuristics
  ports:
    - port: 5005
      targetPort: 5005
```

#### Semantic Service (Branch B - NEW in v2.0.0)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vigil-semantic
  namespace: vigil-guard
  labels:
    app: vigil-semantic
    branch: "b"
    version: "2.0.0"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vigil-semantic
  template:
    metadata:
      labels:
        app: vigil-semantic
        branch: "b"
    spec:
      containers:
        - name: semantic
          image: vigil-guard/semantic-service:2.0.0
          ports:
            - containerPort: 5006
          env:
            - name: PORT
              value: "5006"
            - name: MODEL_NAME
              value: "all-MiniLM-L6-v2"
            - name: EMBEDDING_DIM
              value: "384"
            - name: TIMEOUT_MS
              value: "2000"
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /health
              port: 5006
            initialDelaySeconds: 30
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 5006
            initialDelaySeconds: 20
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vigil-semantic
  namespace: vigil-guard
spec:
  type: ClusterIP
  selector:
    app: vigil-semantic
  ports:
    - port: 5006
      targetPort: 5006
```

#### n8n (StatefulSet - Updated for v2.0.0)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vigil-n8n
  namespace: vigil-guard
spec:
  serviceName: vigil-n8n
  replicas: 1  # n8n doesn't support multi-replica well
  selector:
    matchLabels:
      app: vigil-n8n
  template:
    metadata:
      labels:
        app: vigil-n8n
        version: "2.0.0"
    spec:
      containers:
        - name: n8n
          image: n8nio/n8n:latest
          ports:
            - containerPort: 5678
          env:
            - name: N8N_HOST
              value: "0.0.0.0"
            - name: N8N_PROTOCOL
              value: "http"
            - name: WEBHOOK_URL
              value: "http://vigil-n8n:5678"
            - name: GENERIC_TIMEZONE
              value: "Europe/Warsaw"
            # v2.0.0: 3-Branch service URLs
            - name: HEURISTICS_SERVICE_URL
              value: "http://vigil-heuristics:5005"
            - name: SEMANTIC_SERVICE_URL
              value: "http://vigil-semantic:5006"
            - name: PROMPT_GUARD_URL
              value: "http://vigil-prompt-guard:8000"
          volumeMounts:
            - name: n8n-data
              mountPath: /home/node/.n8n
            - name: workflow-config
              mountPath: /home/node/.n8n/config
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 2Gi
          livenessProbe:
            httpGet:
              path: /healthz
              port: 5678
            initialDelaySeconds: 60
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /healthz
              port: 5678
            initialDelaySeconds: 30
            periodSeconds: 10
      volumes:
        - name: workflow-config
          configMap:
            name: vigil-workflow-config
  volumeClaimTemplates:
    - metadata:
        name: n8n-data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        resources:
          requests:
            storage: 5Gi
---
apiVersion: v1
kind: Service
metadata:
  name: vigil-n8n
  namespace: vigil-guard
spec:
  type: ClusterIP
  selector:
    app: vigil-n8n
  ports:
    - port: 5678
      targetPort: 5678
```

#### Presidio PII API (Deployment)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vigil-presidio-pii
  namespace: vigil-guard
spec:
  replicas: 2  # Can scale for load
  selector:
    matchLabels:
      app: vigil-presidio-pii
  template:
    metadata:
      labels:
        app: vigil-presidio-pii
        version: "2.0.0"
    spec:
      containers:
        - name: presidio
          image: vigil-guard/presidio-pii-api:2.0.0
          ports:
            - containerPort: 5001
          env:
            - name: FLASK_ENV
              value: "production"
            - name: PYTHONUNBUFFERED
              value: "1"
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /health
              port: 5001
            initialDelaySeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 5001
            initialDelaySeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vigil-presidio-pii
  namespace: vigil-guard
spec:
  type: ClusterIP
  selector:
    app: vigil-presidio-pii
  ports:
    - port: 5001
      targetPort: 5001
```

#### ClickHouse (StatefulSet - v2.0.0 Schema)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vigil-clickhouse
  namespace: vigil-monitoring
spec:
  serviceName: vigil-clickhouse
  replicas: 1
  selector:
    matchLabels:
      app: vigil-clickhouse
  template:
    metadata:
      labels:
        app: vigil-clickhouse
    spec:
      containers:
        - name: clickhouse
          image: clickhouse/clickhouse-server:24.1
          ports:
            - containerPort: 8123  # HTTP
            - containerPort: 9000  # Native
          env:
            - name: CLICKHOUSE_USER
              value: "admin"
            - name: CLICKHOUSE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: vigil-secrets
                  key: clickhouse-password
          volumeMounts:
            - name: clickhouse-data
              mountPath: /var/lib/clickhouse
            - name: clickhouse-logs
              mountPath: /var/log/clickhouse-server
            - name: clickhouse-init
              mountPath: /docker-entrypoint-initdb.d
          resources:
            requests:
              cpu: 500m
              memory: 2Gi
            limits:
              cpu: 2000m
              memory: 8Gi
      volumes:
        - name: clickhouse-init
          configMap:
            name: vigil-clickhouse-init
  volumeClaimTemplates:
    - metadata:
        name: clickhouse-data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: ssd  # Use SSD for performance
        resources:
          requests:
            storage: 50Gi
    - metadata:
        name: clickhouse-logs
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
---
# v2.0.0: ClickHouse init with branch columns
apiVersion: v1
kind: ConfigMap
metadata:
  name: vigil-clickhouse-init
  namespace: vigil-monitoring
data:
  init-vigil.sql: |
    CREATE DATABASE IF NOT EXISTS n8n_logs;

    CREATE TABLE IF NOT EXISTS n8n_logs.events_processed (
      timestamp DateTime64(3),
      sessionId String,
      original_input String,
      final_status String,
      threat_score Float32,
      -- v2.0.0: 3-Branch columns
      branch_a_score Float32 DEFAULT 0,
      branch_b_score Float32 DEFAULT 0,
      branch_c_score Float32 DEFAULT 0,
      branch_a_timing_ms UInt32 DEFAULT 0,
      branch_b_timing_ms UInt32 DEFAULT 0,
      branch_c_timing_ms UInt32 DEFAULT 0,
      arbiter_decision String DEFAULT '',
      -- PII columns
      pii_detected UInt8 DEFAULT 0,
      pii_entities String DEFAULT '[]',
      detected_language String DEFAULT '',
      pipeline_version String DEFAULT '2.0.0'
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (timestamp, sessionId)
    TTL timestamp + INTERVAL 90 DAY;
```

### Secrets Management (v2.0.0)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: vigil-secrets
  namespace: vigil-guard
type: Opaque
stringData:
  clickhouse-password: "${CLICKHOUSE_PASSWORD}"
  jwt-secret: "${JWT_SECRET}"
  session-secret: "${SESSION_SECRET}"
  grafana-admin-password: "${GF_SECURITY_ADMIN_PASSWORD}"
---
# Using External Secrets Operator (recommended for production)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: vigil-secrets
  namespace: vigil-guard
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: vault-backend  # or aws-secrets-manager
  target:
    name: vigil-secrets
  data:
    - secretKey: clickhouse-password
      remoteRef:
        key: vigil-guard/clickhouse
        property: password
    - secretKey: jwt-secret
      remoteRef:
        key: vigil-guard/auth
        property: jwt-secret
```

### ConfigMaps for Configuration (v2.0.0)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vigil-workflow-config
  namespace: vigil-guard
data:
  # v2.0.0: unified_config.json v5.0.0 (303 lines - patterns merged)
  unified_config.json: |
    {
      "version": "5.0.0",
      "normalization": { "unicode_form": "NFKC", "max_iterations": 3 },
      "thresholds": { "allow_max": 29, "sanitize_light_max": 64 },
      "pii_detection": { "presidio_enabled": true, "dual_language_mode": true },
      "arbiter": {
        "branch_a_weight": 0.30,
        "branch_b_weight": 0.35,
        "branch_c_weight": 0.35,
        "block_threshold": 70,
        "sanitize_threshold": 30
      },
      "categories": {
        "SQL_XSS_ATTACKS": { "base_weight": 50, "multiplier": 1.3 }
      }
    }
  # v2.0.0: pii.conf (361 lines)
  pii.conf: |
    {
      "entities": ["PERSON", "EMAIL", "PHONE", "PESEL", "NIP", "REGON"],
      "languages": ["pl", "en"],
      "score_threshold": 0.7
    }
---
# Mount in n8n pod
volumeMounts:
  - name: workflow-config
    mountPath: /home/node/.n8n/config
volumes:
  - name: workflow-config
    configMap:
      name: vigil-workflow-config
```

### Ingress Configuration (v2.0.0)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vigil-ingress
  namespace: vigil-guard
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - vigil.example.com
      secretName: vigil-tls
  rules:
    - host: vigil.example.com
      http:
        paths:
          - path: /ui(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: vigil-web-ui-frontend
                port:
                  number: 80
          - path: /api(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: vigil-web-ui-backend
                port:
                  number: 8787
          - path: /n8n(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: vigil-n8n
                port:
                  number: 5678
          - path: /grafana(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: vigil-grafana
                port:
                  number: 3001
```

## Common Operations (v2.0.0)

### Deploy Vigil Guard v2.0.0 to K8s

```bash
# 1. Create namespace
kubectl create namespace vigil-guard
kubectl create namespace vigil-monitoring

# 2. Create secrets
kubectl create secret generic vigil-secrets \
  --from-literal=clickhouse-password=$(openssl rand -base64 32) \
  --from-literal=jwt-secret=$(openssl rand -base64 32) \
  --from-literal=session-secret=$(openssl rand -base64 64) \
  -n vigil-guard

# 3. Apply ConfigMaps
kubectl apply -f k8s/configmaps/

# 4. Deploy services (order matters for v2.0.0)
kubectl apply -f k8s/clickhouse/
kubectl apply -f k8s/presidio/
kubectl apply -f k8s/language-detector/
# v2.0.0: 3-Branch Detection services
kubectl apply -f k8s/heuristics-service/
kubectl apply -f k8s/semantic-service/
kubectl apply -f k8s/prompt-guard/
# Core services
kubectl apply -f k8s/n8n/
kubectl apply -f k8s/web-ui/
kubectl apply -f k8s/grafana/
kubectl apply -f k8s/ingress/

# 5. Verify all 11 services
kubectl get pods -n vigil-guard
kubectl get pods -n vigil-monitoring

# 6. Check 3-branch health
kubectl get pods -n vigil-guard -l branch
```

### Verify 3-Branch Detection Health

```bash
# Check all branch services
kubectl get pods -n vigil-guard -l branch -o wide

# Port forward and test each branch
kubectl port-forward svc/vigil-heuristics 5005:5005 -n vigil-guard &
kubectl port-forward svc/vigil-semantic 5006:5006 -n vigil-guard &
kubectl port-forward svc/vigil-prompt-guard 8000:8000 -n vigil-guard &

# Test Branch A (Heuristics)
curl http://localhost:5005/health

# Test Branch B (Semantic)
curl http://localhost:5006/health

# Test Branch C (LLM Guard)
curl http://localhost:8000/health

# Check ClickHouse for branch columns
kubectl exec -it vigil-clickhouse-0 -n vigil-monitoring -- \
  clickhouse-client -q "SELECT branch_a_score, branch_b_score, branch_c_score, arbiter_decision FROM n8n_logs.events_processed LIMIT 5"
```

### Scale 3-Branch Components

```bash
# Scale Heuristics for more pattern matching capacity
kubectl scale deployment vigil-heuristics --replicas=4 -n vigil-guard

# Scale Semantic for more embedding processing
kubectl scale deployment vigil-semantic --replicas=4 -n vigil-guard

# Enable HPA for branch services
kubectl autoscale deployment vigil-heuristics \
  --cpu-percent=80 \
  --min=2 \
  --max=8 \
  -n vigil-guard

kubectl autoscale deployment vigil-semantic \
  --cpu-percent=80 \
  --min=2 \
  --max=8 \
  -n vigil-guard

# Check HPA status
kubectl get hpa -n vigil-guard
```

### Troubleshoot Vigil Guard Pods

```bash
# Check all pods status
kubectl get pods -n vigil-guard -o wide

# Check 3-branch pods specifically
kubectl get pods -n vigil-guard -l branch

# Check events for issues
kubectl get events -n vigil-guard --sort-by='.lastTimestamp'

# Debug specific pod
kubectl describe pod vigil-heuristics-xxx -n vigil-guard
kubectl logs vigil-heuristics-xxx -n vigil-guard --tail=100

# Check previous container logs (if crashed)
kubectl logs vigil-semantic-xxx -n vigil-guard --previous

# Exec into pod for debugging
kubectl exec -it vigil-n8n-0 -n vigil-guard -- /bin/sh

# Port forward for local testing
kubectl port-forward svc/vigil-n8n 5678:5678 -n vigil-guard
```

### Update Configuration (v2.0.0)

```bash
# Update ConfigMap with unified_config.json v5.0.0
kubectl edit configmap vigil-workflow-config -n vigil-guard

# Restart pods to pick up changes
# Note: n8n reads config on EVERY execution, no restart needed for config changes
# But restart heuristics-service if pattern timeout changed
kubectl rollout restart deployment vigil-heuristics -n vigil-guard
kubectl rollout restart deployment vigil-semantic -n vigil-guard

# Or update specific key
kubectl patch configmap vigil-workflow-config -n vigil-guard \
  --type merge \
  -p '{"data":{"unified_config.json":"{...}"}}'
```

## Troubleshooting (v2.0.0)

### Branch Service Not Responding

```bash
# 1. Check branch pod status
kubectl get pods -n vigil-guard -l branch=a  # Heuristics
kubectl get pods -n vigil-guard -l branch=b  # Semantic
kubectl get pods -n vigil-guard -l branch=c  # Prompt Guard

# 2. Check logs for specific branch
kubectl logs -l branch=a -n vigil-guard --tail=50

# 3. Test branch directly
kubectl port-forward svc/vigil-heuristics 5005:5005 -n vigil-guard
curl -X POST http://localhost:5005/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test", "request_id": "k8s-test"}'
```

### Arbiter Decision Issues

```bash
# 1. Check n8n workflow logs
kubectl logs vigil-n8n-0 -n vigil-guard --tail=100 | grep -i arbiter

# 2. Verify branch scores in ClickHouse
kubectl exec -it vigil-clickhouse-0 -n vigil-monitoring -- \
  clickhouse-client -q "
    SELECT
      sessionId,
      branch_a_score,
      branch_b_score,
      branch_c_score,
      arbiter_decision,
      threat_score
    FROM n8n_logs.events_processed
    ORDER BY timestamp DESC
    LIMIT 10
  "

# 3. Check arbiter weights in config
kubectl get configmap vigil-workflow-config -n vigil-guard -o yaml | grep -A5 arbiter
```

### Pod Won't Start

```bash
# 1. Check pod status
kubectl describe pod <pod-name> -n vigil-guard

# Common issues:
# - ImagePullBackOff: Check image name, registry credentials
# - Pending: Check resource requests, node capacity
# - CrashLoopBackOff: Check logs, environment variables

# 2. For semantic-service: May need more memory for model loading
kubectl patch deployment vigil-semantic -n vigil-guard \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/resources/limits/memory", "value": "2Gi"}]'
```

### Service Not Accessible

```bash
# 1. Check service endpoints
kubectl get endpoints -n vigil-guard

# 2. Check pod labels match selector
kubectl get pods -n vigil-guard --show-labels

# 3. Test internal connectivity
kubectl run debug --rm -it --image=busybox -n vigil-guard -- \
  wget -O- vigil-heuristics:5005/health
```

## Best Practices (v2.0.0)

1. **Use StatefulSets for stateful services** (n8n, ClickHouse)
2. **Use Deployments for stateless services** (Heuristics, Semantic, Presidio, Web UI)
3. **Always set resource limits** to prevent noisy neighbors
4. **Label branch services** with `branch: a|b|c` for easy filtering
5. **Use PodDisruptionBudgets** for high availability
6. **Store secrets in external secret manager** (Vault, AWS SM)
7. **Use NetworkPolicies** to restrict pod-to-pod traffic
8. **Enable pod security standards** (restricted profile)
9. **Back up ClickHouse data** regularly (PVC snapshots)
10. **Monitor branch health** with Prometheus/Grafana (already included)
11. **Set branch timeouts** appropriately (A:1000ms, B:2000ms, C:3000ms)
12. **Use Rolling Updates** with proper readiness probes

## Related Skills

- `helm-chart-management` - For packaging as Helm chart
- `n8n-vigil-workflow` - For 24-node workflow configuration
- `docker-vigil-orchestration` - For Docker Compose reference (11 services)
- `clickhouse-grafana-monitoring` - For monitoring setup with branch columns

## References

- Docker Compose: `docker-compose.yml` (11 services)
- Service configs: `services/*/Dockerfile`
- Workflow: `services/workflow/workflows/Vigil Guard v2.0.0.json` (24 nodes)
- Config: `services/workflow/config/unified_config.json` (v5.0.0, 303 lines)
- Environment variables: `.env.example`

---

**Last Updated:** 2025-12-09
**Version:** v2.0.0
**Architecture:** 3-Branch Parallel Detection (24 nodes)
**Services:** 11 Docker containers
**Branch Weights:** A:30%, B:35%, C:35%
