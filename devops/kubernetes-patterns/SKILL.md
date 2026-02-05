---
name: Kubernetes Patterns
description: Deployments, services, resource management
---

# Kubernetes Development Patterns

Modern Kubernetes patterns and best practices.

## Deployments

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
        image: myapp:1.0.0
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
```

## Services

### ClusterIP (Internal)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
```

### LoadBalancer (External)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
```

## Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
spec:
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

## ConfigMaps

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  database.url: "postgres://db:5432/myapp"
  log.level: "info"
```

```yaml
# Use in Deployment
spec:
  containers:
  - name: myapp
    envFrom:
    - configMapRef:
        name: myapp-config
```

## Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  database.password: cGFzc3dvcmQxMjM= # base64 encoded
```

```yaml
# Use in Deployment
spec:
  containers:
  - name: myapp
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: myapp-secrets
          key: database.password
```

## Resource Limits

```yaml
resources:
  requests:
    memory: "128Mi"  # Guaranteed
    cpu: "100m"      # Guaranteed
  limits:
    memory: "256Mi"  # Maximum
    cpu: "200m"      # Maximum
```

## HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
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
```

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

## Best Practices

✅ **Do**:
- Set resource requests and limits
- Use liveness and readiness probes
- Use specific image tags
- Configure HPA for scalability
- Use network policies
- Store secrets in Secrets, not ConfigMaps
- Use namespaces for isolation
- Label everything consistently

❌ **Don't**:
- Run without resource limits
- Use `latest` tag
- Store secrets in ConfigMaps
- Skip health checks
- Ignore security contexts
- Allow all traffic (use NetworkPolicies)
