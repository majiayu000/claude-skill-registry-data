---
name: kubernetes-best-practices
description: Provides production-ready Kubernetes manifest guidance including resource management, security, high availability, and configuration best practices. This skill should be used when working with Kubernetes YAML files, deployments, pods, services, or when users mention k8s, container orchestration, or cloud-native applications.
---

# Kubernetes Best Practices

This skill provides guidance for writing production-ready Kubernetes manifests and managing cloud-native applications.

## Resource Management

**Memory**: Set requests and limits to the same value to ensure QoS class and prevent OOM kills.

**CPU**: Set requests only, omit limits to allow performance bursting and avoid throttling.

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "256Mi"
    # No CPU limit
```

## Image Versioning

Always pin specific versions, never use `:latest` tag unless explicitly requested:

```yaml
# Good
image: nginx:1.25.3

# Bad
image: nginx:latest
```

For immutability, consider pinning to specific digests.

## Configuration Management

**Secrets**: Sensitive data (passwords, tokens, certificates)
**ConfigMaps**: Non-sensitive configuration (feature flags, URLs, settings)

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: log-level
```

**Best practices:**
- Never hardcode secrets in manifests
- Use external secret management (Sealed Secrets, External Secrets Operator)
- Rotate secrets regularly
- Limit access with RBAC

## Workload Selection

Choose the appropriate workload type:

- **Deployment**: Stateless applications (web servers, APIs, microservices)
- **StatefulSet**: Stateful applications (databases, message queues)
- **DaemonSet**: Node-level services (log collectors, monitoring agents)
- **Job/CronJob**: Batch processing and scheduled tasks

## Security Context

Always implement security best practices:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

**Security checklist:**
- Run as non-root user
- Drop all capabilities by default
- Use read-only root filesystem
- Disable privilege escalation
- Implement network policies
- Scan images for vulnerabilities

## Health Checks

Implement all three probe types:

**Liveness**: Restart container if unhealthy
**Readiness**: Remove from service endpoints if not ready
**Startup**: Allow slow-starting containers time to initialize

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

startupProbe:
  httpGet:
    path: /startup
    port: 8080
  periodSeconds: 10
  failureThreshold: 30
```

## High Availability

**Replica counts**: Set minimum 2 for production workloads

**Pod Disruption Budgets**: Maintain availability during voluntary disruptions

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web-app
```

**Additional HA considerations:**
- Use anti-affinity rules for pod distribution across nodes
- Configure graceful shutdown periods
- Implement horizontal pod autoscaling
- Set appropriate resource requests for scheduling

## Namespace Organization

Use namespaces for environment isolation and apply resource quotas:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: prod-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    persistentvolumeclaims: "10"
```

**Benefits**: Logical separation, resource limits, RBAC boundaries, cost tracking

## Labels and Annotations

Use consistent, recommended labels:

```yaml
metadata:
  labels:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/instance: myapp-prod
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: ecommerce
    app.kubernetes.io/managed-by: helm
```

## Service Types

- **ClusterIP**: Internal cluster communication (default)
- **NodePort**: External access via node ports (dev/test)
- **LoadBalancer**: Cloud provider load balancer (production)
- **ExternalName**: DNS CNAME record (external services)

## Storage

Choose appropriate storage class and access mode:

**Access Modes:**
- ReadWriteOnce (RWO): Single node read-write
- ReadOnlyMany (ROX): Multiple nodes read-only
- ReadWriteMany (RWX): Multiple nodes read-write

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 10Gi
```

## Validation and Testing

Always validate before applying to production:

1. **Client-side validation**: `kubectl apply --dry-run=client -f manifest.yaml`
2. **Server-side validation**: `kubectl apply --dry-run=server -f manifest.yaml`
3. **Test in staging**: Deploy to non-production environment first
4. **Monitor metrics**: Watch resource usage and application health
5. **Gradual rollout**: Use rolling updates with health checks

## Application Checklist

When creating or reviewing Kubernetes manifests:

- [ ] Resource requests and limits configured
- [ ] Specific image version pinned (not :latest)
- [ ] Secrets and ConfigMaps used for configuration
- [ ] Security context implemented (non-root, dropped capabilities)
- [ ] Health checks configured (liveness, readiness, startup)
- [ ] Pod Disruption Budget defined for HA workloads
- [ ] Consistent labels applied
- [ ] Appropriate workload type selected
- [ ] Namespace and resource quotas configured
- [ ] Validated with dry-run before applying
