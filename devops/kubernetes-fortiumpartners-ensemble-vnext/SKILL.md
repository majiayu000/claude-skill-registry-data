---
name: kubernetes
description: Author production-ready Kubernetes manifests — Deployments, Services, security hardening, Kustomize.
when_to_use: "Reach for this when writing raw Kubernetes resource YAML (apiVersion/kind such as Deployment, Service, Pod, or kustomization.yaml). For packaging those resources as reusable Helm charts use helm; for Fly.io PaaS (no K8s) use flyio; to detect the infra tooling in use run tooling-detector. Container-orchestration manifest skill."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.yaml"
  - "**/*.yml"
  - "k8s/**"
  - "manifests/**"
  - "kustomization.yaml"
---

# Kubernetes Quick Reference

**Version**: 1.0.0 | **Target Size**: <100KB | **Purpose**: Fast reference for Kubernetes manifest development and deployment

---

## Overview

Kubernetes is a container orchestration platform for automating deployment, scaling, and management of containerized applications. This quick reference provides essential patterns for creating production-ready Kubernetes manifests with security hardening and best practices.

**When to Load This Skill**:
- Detected: `*.yaml` with `apiVersion: v1|apps/v1`, `kind: Deployment|Service|Pod`, `kustomization.yaml`
- Manual: `--tools=kubernetes` flag
- Use Case: Container orchestration and production deployments

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **REFERENCE.md**: Comprehensive guide with advanced patterns and 20+ production examples

---

## Table of Contents

1. [Core Resources Quick Reference](#core-resources-quick-reference)
2. [Security Hardening Checklist](#security-hardening-checklist)
3. [Resource Requests and Limits Guidelines](#resource-requests-and-limits-guidelines)
4. [Networking Basics](#networking-basics)
5. [Storage Overview](#storage-overview)
6. [RBAC Basics](#rbac-basics)
7. [Common kubectl Commands](#common-kubectl-commands)
8. [Health Checks and Probes](#health-checks-and-probes)
9. [Configuration Management](#configuration-management)
10. [Troubleshooting Quick Guide](#troubleshooting-quick-guide)

---

## Core Resources Quick Reference

### Pod

Basic unit of deployment - one or more containers running together:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp
  labels:
    app: webapp
spec:
  containers:
  - name: app
    image: nginx:1.21
    ports:
    - containerPort: 80
```

**Key Concepts**:
- Smallest deployable unit in Kubernetes
- Containers in same pod share network and storage
- Typically managed by higher-level controllers (Deployment, StatefulSet)
- Use for debugging, not production deployments

---

### Deployment

Declarative pod management with rolling updates and rollbacks:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: app
        image: nginx:1.21
        ports:
        - containerPort: 80
```

**Key Features**:
- Manages ReplicaSets for pod scaling
- Rolling updates with zero downtime
- Rollback to previous versions
- Self-healing (restarts failed pods)

---

### Service

Network abstraction providing stable endpoint for pods:

**ClusterIP** (internal only):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp
spec:
  type: ClusterIP  # Default
  selector:
    app: webapp
  ports:
  - port: 80        # Service port
    targetPort: 80  # Container port
```

**NodePort** (external access via node port):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp
spec:
  type: NodePort
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080  # External port (30000-32767)
```

**LoadBalancer** (cloud load balancer):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp
spec:
  type: LoadBalancer
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
```

**Service Types**:
- **ClusterIP**: Internal access only (default)
- **NodePort**: External access via node IP:port
- **LoadBalancer**: Cloud provider load balancer
- **ExternalName**: DNS CNAME record

---

### ConfigMap

Non-sensitive configuration data:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-config
data:
  app.conf: |
    [server]
    port = 8080
    timeout = 30
  database.host: postgres.default.svc.cluster.local
  cache.ttl: "3600"
```

**Usage in Pod**:
```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: webapp-config
    # Or individual keys
    env:
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: webapp-config
          key: database.host
    # Or mount as volume
    volumeMounts:
    - name: config
      mountPath: /etc/config
  volumes:
  - name: config
    configMap:
      name: webapp-config
```

---

### Secret

Sensitive data storage (base64 encoded):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: webapp-secrets
type: Opaque
data:
  # Base64 encoded values
  db-password: cGFzc3dvcmQxMjM=
  api-key: YWJjZGVmZ2hpamts
stringData:
  # Plain text (auto-encoded)
  admin-password: changeme
```

**Usage in Pod**:
```yaml
spec:
  containers:
  - name: app
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: webapp-secrets
          key: db-password
    # Or mount as volume
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: webapp-secrets
```

**Secret Types**:
- `Opaque`: Generic secret (default)
- `kubernetes.io/dockerconfigjson`: Docker registry credentials
- `kubernetes.io/tls`: TLS certificate and key
- `kubernetes.io/service-account-token`: Service account token

---

### Ingress

HTTP/HTTPS routing to services:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - www.example.com
    secretName: webapp-tls
  rules:
  - host: www.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp
            port:
              number: 80
```

**Path Types**:
- `Prefix`: Matches path prefix (`/app` matches `/app`, `/app/page`)
- `Exact`: Exact path match only
- `ImplementationSpecific`: Ingress controller-specific

---

## Security Hardening Checklist

### Essential Security Settings

**From infrastructure-developer best practices** (production-validated):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      # Pod-level security context
      securityContext:
        runAsNonRoot: true      # ✅ Prevent root execution
        runAsUser: 1000         # ✅ Specific non-root user
        fsGroup: 2000           # ✅ File system group
        seccompProfile:
          type: RuntimeDefault  # ✅ Seccomp profile

      containers:
      - name: app
        image: myapp:1.2.3      # ✅ Pinned version (not :latest)

        # Container-level security context
        securityContext:
          allowPrivilegeEscalation: false  # ✅ No privilege escalation
          readOnlyRootFilesystem: true     # ✅ Immutable filesystem
          capabilities:
            drop:
            - ALL                            # ✅ Drop all capabilities

        # Resource limits (prevent DoS)
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Security Context Fields

**Pod-level**:
```yaml
securityContext:
  runAsNonRoot: true        # Enforce non-root user
  runAsUser: 1000           # UID to run as
  runAsGroup: 3000          # GID to run as
  fsGroup: 2000             # Volume ownership group
  fsGroupChangePolicy: "OnRootMismatch"
  seccompProfile:
    type: RuntimeDefault    # Seccomp profile
  supplementalGroups: [4000]
```

**Container-level**:
```yaml
securityContext:
  allowPrivilegeEscalation: false
  privileged: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
    - ALL
    add:
    - NET_BIND_SERVICE  # Only if needed for ports <1024
  seccompProfile:
    type: RuntimeDefault
```

### Common Security Anti-Patterns

**❌ INSECURE** (avoid):
```yaml
spec:
  containers:
  - name: app
    image: myapp:latest           # ❌ Mutable tag
    # No security context          # ❌ Running as root
    # No resource limits           # ❌ Resource exhaustion risk
    # No health checks             # ❌ No failure detection
```

**✅ SECURE** (production-ready):
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: myapp:1.2.3            # ✅ Immutable tag
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]
    resources:
      limits:
        memory: "512Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
```

---

## Resource Requests and Limits Guidelines

### Resource Specification

```yaml
resources:
  requests:     # Guaranteed allocation
    memory: "256Mi"
    cpu: "250m"
  limits:       # Maximum allocation
    memory: "512Mi"
    cpu: "500m"
```

**CPU Units**:
- `1` = 1 vCPU/core
- `500m` = 0.5 vCPU (500 millicores)
- `100m` = 0.1 vCPU

**Memory Units**:
- `Mi` = Mebibytes (1024^2 bytes)
- `Gi` = Gibibytes (1024^3 bytes)
- `M` = Megabytes (1000^2 bytes)
- `G` = Gigabytes (1000^3 bytes)

### Resource Guidelines by Workload

**Small web service**:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

**Medium application**:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**Large application**:
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

**Database/stateful**:
```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### QoS Classes

Kubernetes assigns QoS class based on resources:

1. **Guaranteed** (highest priority):
   - Requests = Limits for all containers
   - Last to be evicted

2. **Burstable** (medium priority):
   - Requests < Limits
   - Evicted after BestEffort

3. **BestEffort** (lowest priority):
   - No requests or limits
   - First to be evicted

---

## Networking Basics

### Service Types Comparison

| Type | Use Case | External Access | Cloud Cost |
|------|----------|----------------|------------|
| ClusterIP | Internal only | No | Free |
| NodePort | Development/testing | Yes (node:port) | Free |
| LoadBalancer | Production | Yes (load balancer) | Paid |
| ExternalName | External DNS | N/A | Free |

### Service DNS

Services accessible via DNS:

```
# Within same namespace
<service-name>

# Across namespaces
<service-name>.<namespace>.svc.cluster.local

# Full FQDN
<service-name>.<namespace>.svc.cluster.local
```

**Example**:
```yaml
# Service in namespace "default"
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
---
# Access from pod in any namespace
env:
  - name: DB_HOST
    value: postgres.default.svc.cluster.local
```

### Headless Service

For direct pod access (StatefulSets):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - port: 5432
```

**Pod DNS**:
```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

---

## Storage Overview

### PersistentVolume (PV)

Cluster-level storage resource:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: gp3
  hostPath:
    path: /mnt/data
```

### PersistentVolumeClaim (PVC)

Pod's request for storage:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: webapp-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: gp3
```

**Usage in Pod**:
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: data
      mountPath: /app/data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: webapp-pvc
```

### Access Modes

- `ReadWriteOnce` (RWO): Single node read-write
- `ReadOnlyMany` (ROX): Multiple nodes read-only
- `ReadWriteMany` (RWX): Multiple nodes read-write

### StorageClass

Dynamic provisioning template:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iopsPerGB: "50"
  encrypted: "true"
reclaimPolicy: Delete
allowVolumeExpansion: true
```

---

## RBAC Basics

### Service Account

Pod identity:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: webapp-sa
  namespace: production
```

**Usage in Pod**:
```yaml
spec:
  serviceAccountName: webapp-sa
  containers:
  - name: app
    image: myapp:1.0.0
```

### Role and RoleBinding

Namespace-scoped permissions:

```yaml
# Role: Define permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding: Grant permissions to user/SA
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: ServiceAccount
  name: webapp-sa
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRole and ClusterRoleBinding

Cluster-wide permissions:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-reader
rules:
- apiGroups: [""]
  resources: ["nodes", "namespaces"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-cluster
subjects:
- kind: ServiceAccount
  name: admin-sa
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-reader
  apiGroup: rbac.authorization.k8s.io
```

### RBAC Verbs

- `get`: Retrieve individual resource
- `list`: List resources
- `watch`: Watch for changes
- `create`: Create new resources
- `update`: Update existing resources
- `patch`: Partially update resources
- `delete`: Delete resources
- `deletecollection`: Delete multiple resources

---

## Common kubectl Commands

### Pod Management

```bash
# List pods
kubectl get pods
kubectl get pods -n production
kubectl get pods --all-namespaces
kubectl get pods -o wide  # Show node and IP

# Describe pod
kubectl describe pod webapp-abc123

# View logs
kubectl logs webapp-abc123
kubectl logs webapp-abc123 -f  # Follow logs
kubectl logs webapp-abc123 --previous  # Previous container
kubectl logs webapp-abc123 -c container-name  # Multi-container

# Execute command
kubectl exec -it webapp-abc123 -- /bin/sh
kubectl exec webapp-abc123 -- env

# Port forward
kubectl port-forward webapp-abc123 8080:80
kubectl port-forward svc/webapp 8080:80

# Delete pod
kubectl delete pod webapp-abc123
```

### Deployment Management

```bash
# Create deployment
kubectl create deployment webapp --image=nginx:1.21
kubectl apply -f deployment.yaml

# Scale deployment
kubectl scale deployment webapp --replicas=5

# Update image
kubectl set image deployment/webapp app=nginx:1.22

# Rollout status
kubectl rollout status deployment/webapp

# Rollout history
kubectl rollout history deployment/webapp

# Rollback
kubectl rollout undo deployment/webapp
kubectl rollout undo deployment/webapp --to-revision=2

# Pause/resume
kubectl rollout pause deployment/webapp
kubectl rollout resume deployment/webapp
```

### Service Management

```bash
# List services
kubectl get services
kubectl get svc

# Describe service
kubectl describe svc webapp

# Expose deployment
kubectl expose deployment webapp --port=80 --type=LoadBalancer

# Get endpoints
kubectl get endpoints webapp
```

### Resource Information

```bash
# Get all resources
kubectl get all
kubectl get all -n production

# Get resource YAML
kubectl get deployment webapp -o yaml
kubectl get pod webapp-abc123 -o json

# Get resource with labels
kubectl get pods -l app=webapp
kubectl get pods --selector app=webapp,env=prod

# Get events
kubectl get events
kubectl get events --sort-by='.lastTimestamp'

# Top (resource usage)
kubectl top nodes
kubectl top pods
kubectl top pods -n production
```

### Debugging

```bash
# Describe resource
kubectl describe pod webapp-abc123
kubectl describe node node-1

# Get cluster info
kubectl cluster-info
kubectl version

# API resources
kubectl api-resources
kubectl api-versions

# Explain resource
kubectl explain pod
kubectl explain pod.spec.containers
```

---

## Health Checks and Probes

### Liveness Probe

Determines if container should be restarted:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
    httpHeaders:
    - name: Custom-Header
      value: Awesome
  initialDelaySeconds: 30  # Wait before first check
  periodSeconds: 10        # Check every 10s
  timeoutSeconds: 5        # Timeout after 5s
  failureThreshold: 3      # Restart after 3 failures
  successThreshold: 1      # Success after 1 check
```

### Readiness Probe

Determines if container should receive traffic:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
  successThreshold: 1
```

### Startup Probe

For slow-starting containers:

```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30  # 5 minutes (30 * 10s)
```

### Probe Types

**HTTP GET**:
```yaml
httpGet:
  path: /health
  port: 8080
  scheme: HTTP  # or HTTPS
```

**TCP Socket**:
```yaml
tcpSocket:
  port: 8080
```

**Exec Command**:
```yaml
exec:
  command:
  - cat
  - /tmp/healthy
```

### Probe Timing

```
initialDelaySeconds: Wait before first probe
periodSeconds: Time between probes
timeoutSeconds: Probe timeout
failureThreshold: Failures before action
successThreshold: Successes to recover
```

---

## Configuration Management

### Environment Variables

**Direct values**:
```yaml
env:
- name: LOG_LEVEL
  value: "info"
- name: APP_ENV
  value: "production"
```

**From ConfigMap**:
```yaml
env:
- name: DB_HOST
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: database.host
```

**From Secret**:
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: db-password
```

**From field**:
```yaml
env:
- name: POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
- name: POD_IP
  valueFrom:
    fieldRef:
      fieldPath: status.podIP
```

### EnvFrom (all keys)

```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: app-secrets
- prefix: DB_
  configMapRef:
    name: database-config
```

### Volume Mounts

**ConfigMap as volume**:
```yaml
volumes:
- name: config
  configMap:
    name: app-config
    items:
    - key: app.conf
      path: app.conf
volumeMounts:
- name: config
  mountPath: /etc/config
  readOnly: true
```

**Secret as volume**:
```yaml
volumes:
- name: secrets
  secret:
    secretName: app-secrets
    defaultMode: 0400  # Read-only
volumeMounts:
- name: secrets
  mountPath: /etc/secrets
  readOnly: true
```

---

## Troubleshooting Quick Guide

### Pod Issues

**Pod Pending**:
```bash
# Check events
kubectl describe pod <pod-name>

# Common causes:
# - Insufficient resources
# - PVC not bound
# - Node selector mismatch
# - Image pull errors
```

**CrashLoopBackOff**:
```bash
# Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Common causes:
# - Application error
# - Missing environment variables
# - Failed liveness probe
# - Incorrect command/args
```

**ImagePullBackOff**:
```bash
# Describe pod
kubectl describe pod <pod-name>

# Common causes:
# - Wrong image name/tag
# - Private registry without credentials
# - Network issues
# - Rate limiting
```

**Pod Stuck Terminating**:
```bash
# Force delete
kubectl delete pod <pod-name> --grace-period=0 --force

# Check finalizers
kubectl get pod <pod-name> -o yaml | grep finalizers
```

### Service Issues

**Service not reachable**:
```bash
# Check endpoints
kubectl get endpoints <service-name>

# Check selector labels
kubectl get pods --show-labels
kubectl describe service <service-name>

# Test from another pod
kubectl run test --rm -it --image=curlimages/curl -- \
  curl http://<service-name>.<namespace>.svc.cluster.local
```

### Resource Issues

**Out of resources**:
```bash
# Check node resources
kubectl top nodes
kubectl describe nodes

# Check pod resources
kubectl top pods
kubectl describe pod <pod-name>
```

### Debug Commands

```bash
# Run debug pod
kubectl run debug --rm -it --image=busybox -- /bin/sh

# Copy files from pod
kubectl cp <pod-name>:/path/to/file ./local-file

# Ephemeral debug container
kubectl debug <pod-name> -it --image=busybox
```

---

## Next Steps

**For Advanced Patterns**:
- See **REFERENCE.md** for comprehensive guide with 20+ production examples
- Covers: StatefulSets, DaemonSets, Jobs, CronJobs, HPA/VPA, Network Policies, advanced RBAC, observability

**Common Use Cases**:
- Stateful applications → REFERENCE.md § StatefulSets
- Cluster-wide services → REFERENCE.md § DaemonSets
- Batch processing → REFERENCE.md § Jobs and CronJobs
- Auto-scaling → REFERENCE.md § HPA and VPA
- Network isolation → REFERENCE.md § Network Policies
- Production monitoring → REFERENCE.md § Observability

---

**Progressive Disclosure**: Start here for quick reference, load REFERENCE.md for comprehensive patterns and production examples.

**Performance Target**: <100ms skill loading (this file ~70KB)

**Last Updated**: 2025-10-23 | **Version**: 1.0.0
