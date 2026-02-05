---
name: k8s-reviewer
description: |
  WHEN: Kubernetes manifest review, Helm charts, resource limits, probes, RBAC
  WHAT: Resource configuration + Health probes + Security context + RBAC policies + Helm best practices
  WHEN NOT: Docker only → docker-reviewer, Terraform → terraform-reviewer
---

# Kubernetes Reviewer Skill

## Purpose
Reviews Kubernetes manifests and Helm charts for resource configuration, security, and best practices.

## When to Use
- Kubernetes YAML review
- Helm chart review
- Pod security review
- Resource limits check
- RBAC configuration review

## Project Detection
- `*.yaml` in k8s/, manifests/, deploy/
- `Chart.yaml` (Helm)
- `kustomization.yaml`
- `deployment.yaml`, `service.yaml`

## Workflow

### Step 1: Analyze Project
```
**Manifest Type**: Deployment, Service, Ingress
**Helm**: Chart v3
**Namespace**: production
**Cluster**: EKS/GKE/AKS
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full K8s review (recommended)
- Resource limits and requests
- Health probes configuration
- Security context and RBAC
- Helm chart structure
multiSelect: true
```

## Detection Rules

### Resource Limits
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No resource limits | Add limits and requests | CRITICAL |
| Limits = Requests | Set different values | MEDIUM |
| Too high limits | Right-size based on usage | MEDIUM |
| No LimitRange | Add namespace LimitRange | MEDIUM |

```yaml
# BAD: No resource management
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          image: myapp:latest
          # No resources defined!

# GOOD: Proper resource management
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:v1.2.3
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

### Health Probes
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No liveness probe | Add liveness check | HIGH |
| No readiness probe | Add readiness check | HIGH |
| No startup probe | Add for slow-starting apps | MEDIUM |
| Same liveness/readiness | Differentiate purposes | MEDIUM |

```yaml
# GOOD: Complete probe configuration
spec:
  containers:
    - name: app
      image: myapp:v1.2.3
      ports:
        - containerPort: 8080

      # Startup probe - for slow starting containers
      startupProbe:
        httpGet:
          path: /health/startup
          port: 8080
        failureThreshold: 30
        periodSeconds: 10

      # Liveness probe - restart if unhealthy
      livenessProbe:
        httpGet:
          path: /health/live
          port: 8080
        initialDelaySeconds: 0
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3

      # Readiness probe - remove from service if not ready
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
        timeoutSeconds: 3
        failureThreshold: 3
```

### Security Context
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Running as root | Set runAsNonRoot: true | CRITICAL |
| No security context | Add pod/container security | HIGH |
| Privileged container | Remove privileged: true | CRITICAL |
| Writable root filesystem | Set readOnlyRootFilesystem | HIGH |

```yaml
# BAD: No security constraints
spec:
  containers:
    - name: app
      image: myapp:latest
      # No security context!

# GOOD: Secure configuration
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000

      containers:
        - name: app
          image: myapp:v1.2.3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache

      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
```

### Image Policy
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Using :latest tag | Pin specific version | HIGH |
| No image pull policy | Set imagePullPolicy | MEDIUM |
| Public registry | Use private registry | MEDIUM |

```yaml
# BAD
image: myapp:latest
# or
image: myapp  # Implies :latest

# GOOD
image: gcr.io/myproject/myapp:v1.2.3
imagePullPolicy: IfNotPresent
```

### Pod Disruption Budget
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No PDB for critical apps | Add PodDisruptionBudget | HIGH |

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # or maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

### RBAC
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Using default SA | Create dedicated ServiceAccount | HIGH |
| Cluster-wide permissions | Use namespaced Role | HIGH |
| Wildcard permissions | Specify explicit resources | CRITICAL |

```yaml
# BAD: Overly permissive
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]

# GOOD: Least privilege
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: production
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
  name: myapp-rolebinding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
```

### Helm Charts
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Hardcoded values | Use values.yaml | MEDIUM |
| No default values | Provide sensible defaults | MEDIUM |
| No NOTES.txt | Add post-install notes | LOW |

```yaml
# values.yaml
replicaCount: 3

image:
  repository: myapp
  tag: "v1.2.3"
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

# templates/deployment.yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## Response Template
```
## Kubernetes Review Results

**Project**: [name]
**Type**: Deployment, Service, Ingress
**Namespace**: production

### Resource Limits
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | deployment.yaml | No resource limits defined |

### Health Probes
| Status | File | Issue |
|--------|------|-------|
| HIGH | deployment.yaml | Missing readiness probe |

### Security
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | deployment.yaml | Running as root |

### RBAC
| Status | File | Issue |
|--------|------|-------|
| HIGH | rbac.yaml | Wildcard permissions |

### Recommended Actions
1. [ ] Add resource requests and limits
2. [ ] Configure liveness and readiness probes
3. [ ] Add security context with non-root user
4. [ ] Apply least privilege RBAC
```

## Best Practices
1. **Resources**: Always set requests and limits
2. **Probes**: All three probe types for production
3. **Security**: Non-root, read-only fs, drop capabilities
4. **RBAC**: Least privilege, namespaced roles
5. **Images**: Pin versions, use private registry

## Integration
- `docker-reviewer`: Container image review
- `terraform-reviewer`: Infrastructure as code
- `infra-security-reviewer`: Cluster security
