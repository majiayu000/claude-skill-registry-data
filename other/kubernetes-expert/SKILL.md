---
name: kubernetes-expert
description: Deep Kubernetes expertise for container orchestration, deployment patterns, and cluster management. Use when deploying to K8s, writing Helm charts.
---

# Kubernetes Expert

Specialized expertise in Kubernetes container orchestration, providing guidance on deployment strategies, security hardening, resource optimization, and operational best practices for production-grade cluster management.

## When to Use This Skill

Use this skill for:

- Deploying applications to Kubernetes clusters
- Writing or reviewing Helm charts
- Configuring RBAC, NetworkPolicies, and security contexts
- Troubleshooting pod failures, networking issues, or resource constraints
- Optimizing resource requests/limits and autoscaling
- Setting up monitoring, logging, and observability
- Managing multi-tenant or multi-cluster environments

**Trigger phrases**: "kubernetes", "k8s", "helm", "pod", "deployment", "kubectl", "container orchestration", "cluster", "ingress", "service mesh"

## What This Skill Does

Provides production-ready Kubernetes patterns including:

- **Workload Management**: Deployments, StatefulSets, DaemonSets, Jobs, CronJobs
- **Networking**: Services, Ingress, NetworkPolicies, Service Mesh integration
- **Configuration**: ConfigMaps, Secrets, environment management
- **Storage**: PersistentVolumes, StorageClasses, volume management
- **Security**: RBAC, PodSecurityPolicies/Standards, security contexts
- **Scaling**: HPA, VPA, cluster autoscaling, resource optimization
- **Operations**: Health checks, rolling updates, rollbacks, debugging

## Instructions

### Step 1: Assess the Kubernetes Context

Before making changes, understand the environment:

```bash
# Check cluster info
kubectl cluster-info
kubectl get nodes -o wide

# Review existing resources
kubectl get all -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### Step 2: Follow Deployment Best Practices

**Deployment Template**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-name
  labels:
    app: app-name
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app-name
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: app-name
        version: v1
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: app-name
        image: registry/app:tag
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          protocol: TCP
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
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
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
```

### Step 3: Implement Security Hardening

**NetworkPolicy for Zero-Trust**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app-ingress
spec:
  podSelector:
    matchLabels:
      app: app-name
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

**RBAC Configuration**:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: app-namespace
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: app-namespace
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: app-namespace
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

### Step 4: Configure Autoscaling

**Horizontal Pod Autoscaler**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-name
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### Step 5: Debugging and Troubleshooting

**Common Diagnostic Commands**:

```bash
# Pod issues
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Resource issues
kubectl top pods -n <namespace>
kubectl top nodes

# Network debugging
kubectl run debug --rm -it --image=nicolaka/netshoot -- /bin/bash

# Event monitoring
kubectl get events -n <namespace> --sort-by='.lastTimestamp' -w
```

**Common Issues and Solutions**:

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| CrashLoopBackOff | `kubectl logs --previous` | Fix app error, check resources |
| ImagePullBackOff | `kubectl describe pod` | Fix image name, add imagePullSecrets |
| Pending pods | `kubectl describe pod` | Check resources, node selectors |
| OOMKilled | Check memory limits | Increase memory limit or optimize app |

## Best Practices

- **Always set resource requests and limits** - Prevents noisy neighbor issues
- **Use namespaces for isolation** - Separate environments and teams
- **Implement health checks** - Both liveness and readiness probes
- **Apply security contexts** - Run as non-root, drop capabilities
- **Use NetworkPolicies** - Default deny, explicit allow
- **Version your images** - Never use `latest` tag in production
- **Use PodDisruptionBudgets** - Ensure availability during updates
- **Implement proper logging** - Structured logs to stdout/stderr

## Common Patterns

### Pattern 1: Blue-Green Deployment

Use separate deployments with service selector switching:

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  template:
    metadata:
      labels:
        app: myapp
        version: blue
---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  template:
    metadata:
      labels:
        app: myapp
        version: green
---
# Service - switch selector to route traffic
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
```

### Pattern 2: Sidecar Pattern

Extend pod functionality with sidecar containers:

```yaml
spec:
  containers:
  - name: main-app
    image: app:v1
  - name: log-shipper
    image: fluentd:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  volumes:
  - name: logs
    emptyDir: {}
```

### Pattern 3: Init Container for Dependencies

```yaml
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.35
    command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 2; done']
  containers:
  - name: app
    image: app:v1
```

## Helm Chart Best Practices

**Chart Structure**:

```
mychart/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── NOTES.txt
└── charts/
```

**Template Best Practices**:

```yaml
# Use helpers for consistent naming
{{- define "mychart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

# Use conditionals for optional resources
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
...
{{- end }}

# Use range for multiple items
{{- range .Values.extraEnvVars }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}
```

## Quality Checklist

- [ ] Resource requests and limits defined for all containers
- [ ] Liveness and readiness probes configured
- [ ] Security context with non-root user
- [ ] NetworkPolicies applied (default deny)
- [ ] RBAC with least privilege
- [ ] Secrets managed properly (not in plain text)
- [ ] PodDisruptionBudget configured
- [ ] HPA configured if needed
- [ ] Image tags are specific (not `latest`)
- [ ] Labels and annotations applied consistently

## Related Skills

- `cicd-architect` - Kubernetes deployment pipelines
- `cloud-architect` - Managed Kubernetes services (EKS, AKS, GKE)
- `security-review` - Kubernetes security assessment
- `terraform-specialist` - Infrastructure provisioning for clusters

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: awesome-claude-code-subagents patterns, Kubernetes best practices


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
