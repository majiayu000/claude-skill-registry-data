---
name: k8s-generator
description: Generate production-ready Kubernetes manifests with Deployments, Services, ConfigMaps, and Ingress
allowed-tools: ["Read", "Write", "Glob", "Grep"]
version: 1.0.0
author: GLINCKER Team
license: Apache-2.0
keywords: [kubernetes, k8s, deployment, devops, cloud-native]
---

# Kubernetes Generator

Generate complete Kubernetes manifests by analyzing your application. Creates Deployments, Services, ConfigMaps, Secrets, Ingress, and HPA with production best practices.

## What This Skill Does

- Auto-generates K8s manifests from project analysis
- Creates proper resource limits and requests
- Implements health checks (liveness/readiness probes)
- Generates ConfigMaps and Secrets management
- Includes Horizontal Pod Autoscaler (HPA)
- Follows 12-factor app principles

## Instructions

### Phase 1: Application Analysis

Analyze the application to determine requirements:

```bash
# Detect application type
Use Glob/Grep to find:
- Dockerfile → Container config
- .env → Environment variables
- Port bindings
- Volume requirements
```

### Phase 2: Generate Core Manifests

**Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
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
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        envFrom:
        - configMapRef:
            name: myapp-config
        - secretRef:
            name: myapp-secrets
```

**Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP
```

**ConfigMap**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  NODE_ENV: production
  LOG_LEVEL: info
  API_URL: https://api.example.com
```

**HPA (Horizontal Pod Autoscaler)**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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
```

**Ingress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

## Advanced Features

### Multi-Environment Setup

Generate manifests for dev/staging/prod with Kustomize:

```yaml
# base/kustomization.yaml
resources:
- deployment.yaml
- service.yaml
- configmap.yaml

# overlays/production/kustomization.yaml
bases:
- ../../base
replicas:
- name: myapp
  count: 5
images:
- name: myapp
  newTag: v1.2.3
```

### Database StatefulSet

For stateful applications:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

## Best Practices Applied

1. **Resource Limits**: Always set requests and limits
2. **Health Checks**: Liveness and readiness probes
3. **Replicas**: Minimum 2 for HA
4. **Labels**: Consistent labeling for service discovery
5. **Security**: Use non-root containers, read-only file systems
6. **Secrets**: Never commit sensitive data

## Tool Requirements

- **Read**: Analyze application config
- **Write**: Generate manifest files
- **Glob**: Find relevant files
- **Grep**: Search for patterns

## Examples

### Example 1: Simple Web App

**User**: "Generate K8s manifests for my Node.js app"

**Output**:
- Deployment with 3 replicas
- ClusterIP Service
- ConfigMap for env vars
- HPA (2-10 pods)
- Ingress with TLS

### Example 2: Microservices

**User**: "Create K8s setup for microservices architecture"

**Output**:
- Multiple Deployments (one per service)
- Services with ClusterIP
- NetworkPolicy for security
- Istio VirtualService/DestinationRule

## Changelog

### Version 1.0.0
- Initial release
- Full manifest generation
- HPA support
- Ingress configuration
- Multi-environment setup

## Author

**GLINCKER Team**
- Repository: [claude-code-marketplace](https://github.com/GLINCKER/claude-code-marketplace)
