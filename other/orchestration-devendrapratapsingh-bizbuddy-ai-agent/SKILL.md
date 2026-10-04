---
name: orchestration
description: Design and manage container orchestration, Kubernetes clusters, service mesh, and workload scheduling. Use when working with Kubernetes manifests, Helm charts, service mesh configuration, pod scheduling, or container orchestration patterns.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Container Orchestration Skill

You are a Senior DevOps Engineer specializing in container orchestration and Kubernetes. You design, deploy, and manage scalable, resilient container platforms with advanced scheduling, networking, and observability features.

## Core Responsibilities

1. **Kubernetes Architecture**
   - Design multi-tenant cluster architectures
   - Configure node pools and workload isolation
   - Implement cluster autoscaling (HPA, VPA, Cluster Autoscaler)
   - Manage cluster networking (CNI, Ingress, Service Mesh)

2. **Workload Management**
   - Design deployment strategies (Rolling, Blue/Green, Canary)
   - Configure resource requests and limits
   - Implement pod disruption budgets
   - Manage secrets and ConfigMaps

3. **Service Mesh**
   - Istio/Linkerd installation and configuration
   - Traffic management and routing
   - mTLS and security policies
   - Observability integration

4. **Storage Orchestration**
   - Dynamic volume provisioning
   - Storage class management
   - Stateful workload patterns
   - Backup and disaster recovery

5. **Multi-Cluster Management**
   - Fleet management and GitOps
   - Cross-cluster service discovery
   - Disaster recovery across regions
   - Federation patterns

## Kubernetes Manifest Standards

### Production-Ready Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
  labels:
    app.kubernetes.io/name: {{ .Values.app.name }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/version: {{ .Values.app.version | quote }}
    app.kubernetes.io/component: api
    app.kubernetes.io/part-of: {{ .Values.app.system }}
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: {{ .Values.app.replicas }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Values.app.name }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ .Values.app.name }}
        app.kubernetes.io/instance: {{ .Release.Name }}
        app.kubernetes.io/version: {{ .Values.app.version | quote }}
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        checksum/secrets: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
    spec:
      serviceAccountName: {{ .Values.app.name }}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app.kubernetes.io/name
                      operator: In
                      values:
                        - {{ .Values.app.name }}
                topologyKey: kubernetes.io/hostname
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - application
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: {{ .Values.app.name }}
      containers:
        - name: {{ .Values.app.name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          env:
            - name: NODE_ENV
              value: "{{ .Values.environment }}"
            - name: PORT
              value: "8080"
            - name: LOG_LEVEL
              value: "{{ .Values.log.level }}"
          envFrom:
            - configMapRef:
                name: {{ .Values.app.name }}-config
            - secretRef:
                name: {{ .Values.app.name }}-secrets
                optional: true
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /health/startup
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir:
            sizeLimit: 100Mi
      terminationGracePeriodSeconds: 30
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
spec:
  minAvailable: {{ div .Values.app.replicas 2 | add 1 }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Values.app.name }}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ .Values.app.name }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
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
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### Service and Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
  labels:
    app.kubernetes.io/name: {{ .Values.app.name }}
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: {{ .Values.app.name }}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
  labels:
    app.kubernetes.io/name: {{ .Values.app.name }}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://{{ .Values.ingress.host }}"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
    nginx.ingress.kubernetes.io/cors-allow-headers: "DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - {{ .Values.ingress.host }}
      secretName: {{ .Values.app.name }}-tls
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ .Values.app.name }}
                port:
                  number: 80
---
# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.app.namespace }}
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: {{ .Values.app.name }}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: monitoring
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: database
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

## Helm Chart Structure

```
myapp/
├── Chart.yaml
├── values.yaml
├── values-production.yaml
├── values-staging.yaml
├── README.md
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── serviceaccount.yaml
    ├── pdb.yaml
    ├── hpa.yaml
    └── tests/
        └── test-connection.yaml
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for the MyApp microservice
type: application
version: 1.2.3
appVersion: "2.5.1"
home: https://github.com/org/myapp
sources:
  - https://github.com/org/myapp
maintainers:
  - name: Platform Team
    email: platform@company.com
keywords:
  - microservice
  - api
  - nodejs
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: 18.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
annotations:
  artifacthub.io/changes: |
    - kind: added
      description: Added support for topology spread constraints
    - kind: changed
      description: Updated resource requests and limits
```

### values.yaml

```yaml
# Default values for myapp

app:
  name: myapp
  namespace: default
  version: "1.0.0"
  replicas: 2
  system: platform

environment: development

image:
  repository: ghcr.io/org/myapp
  tag: latest
  pullPolicy: IfNotPresent
  pullSecrets: []

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  className: nginx
  host: myapp.local
  tls:
    enabled: true
    secretName: myapp-tls

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

nodeSelector: {}

tolerations: []

affinity: {}

persistence:
  enabled: false
  storageClass: ""
  size: 10Gi

config:
  LOG_LEVEL: info
  METRICS_ENABLED: "true"
  TRACING_ENABLED: "true"

secrets: {}
  # DATABASE_URL: ""
  # API_KEY: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

networkPolicy:
  enabled: true

metrics:
  enabled: true
  port: 8080
  path: /metrics
```

## Service Mesh (Istio)

### Virtual Service and Destination Rule

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
  namespace: default
spec:
  hosts:
    - myapp.example.com
  gateways:
    - public-gateway
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: myapp-canary
            port:
              number: 80
          weight: 100
    - route:
        - destination:
            host: myapp
            port:
              number: 80
          weight: 90
        - destination:
            host: myapp-canary
            port:
              number: 80
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: gateway-error,connect-failure,refused-stream
      timeout: 10s
      fault:
        delay:
          percentage:
            value: 0.1
          fixedDelay: 5s
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
  namespace: default
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 100
        maxRetries: 3
    loadBalancer:
      simple: LEAST_CONN
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: myapp
  namespace: default
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: myapp
  namespace: default
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/ingress-nginx/sa/ingress-nginx"]
      to:
        - operation:
            methods: ["GET", "POST", "PUT", "DELETE"]
            paths: ["/api/*"]
```

## ArgoCD GitOps

### Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops
    targetRevision: HEAD
    path: apps/myapp/overlays/production
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: app.version
          value: "2.5.1"
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

### ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/org/gitops
        revision: HEAD
        directories:
          - path: apps/*/overlays/production
    - clusters:
        selector:
          matchLabels:
            environment: production
  template:
    metadata:
      name: '{{path.basename}}-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/gitops
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: '{{server}}'
        namespace: production
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Stateful Workloads

### StatefulSet with Persistent Storage

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
spec:
  serviceName: postgres
  replicas: 3
  podManagementPolicy: OrderedReady
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
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POSTGRES_REPLICATION_USER
              value: replicator
            - name: POSTGRES_REPLICATION_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: replication-password
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
            - name: config
              mountPath: /etc/postgresql/postgresql.conf
              subPath: postgresql.conf
          resources:
            requests:
              memory: "2Gi"
              cpu: "1000m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 5
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        storageClassName: fast-ssd
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: database
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      name: postgres
  clusterIP: None
```

## Job and CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: database
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  startingDeadlineSeconds: 60
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: backup
          containers:
            - name: backup
              image: postgres:15-alpine
              command:
                - /bin/sh
                - -c
                - |
                  pg_dump -h postgres-0.postgres.database.svc.cluster.local \
                    -U postgres \
                    -d myapp \
                    -F c \
                    -f /backup/backup-$(date +%Y%m%d-%H%M%S).dump
              env:
                - name: PGPASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: postgres-credentials
                      key: password
              volumeMounts:
                - name: backup
                  mountPath: /backup
              resources:
                requests:
                  memory: "512Mi"
                  cpu: "250m"
                limits:
                  memory: "1Gi"
                  cpu: "500m"
          volumes:
            - name: backup
              persistentVolumeClaim:
                claimName: backup-pvc
          restartPolicy: OnFailure
          activeDeadlineSeconds: 3600
```

## Cluster Autoscaling

### Cluster Autoscaler Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
        - name: cluster-autoscaler
          image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
          command:
            - ./cluster-autoscaler
            - --cloud-provider=aws
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
            - --balance-similar-node-groups
            - --skip-nodes-with-system-pods=false
            - --skip-nodes-with-local-storage=false
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=5m
            - --scale-down-utilization-threshold=0.5
          resources:
            requests:
              memory: "500Mi"
              cpu: "100m"
            limits:
              memory: "1000Mi"
              cpu: "500m"
```

## Troubleshooting Commands

```bash
# Check pod status
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>

# View logs
kubectl logs <pod-name> -n <namespace> --tail=100 -f
kubectl logs -l app=myapp -n <namespace> --tail=100 --all-containers

# Exec into pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Port forward
kubectl port-forward svc/myapp 8080:80 -n <namespace>

# Check resource usage
kubectl top pods -n <namespace>
kubectl top nodes

# Events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Debug networking
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never

# Check service endpoints
kubectl get endpoints <service-name> -n <namespace>
kubectl get svc <service-name> -n <namespace>

# Rollout management
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
kubectl rollout undo deployment/<name> -n <namespace>

# Resource usage
kubectl resource-capacity --pods --util --sort cpu.util

# Check HPA
kubectl get hpa -n <namespace>
kubectl describe hpa <hpa-name> -n <namespace>

# Force delete stuck resources
kubectl delete pod <pod-name> -n <namespace> --force --grace-period=0
```

## Orchestration Checklist

- [ ] Resource requests and limits defined
- [ ] Health probes configured (liveness, readiness, startup)
- [ ] Pod disruption budget set
- [ ] Horizontal pod autoscaling enabled
- [ ] Security context configured
- [ ] Network policies defined
- [ ] Service mesh configured (if applicable)
- [ ] Ingress with TLS configured
- [ ] Persistent volumes properly sized
- [ ] ConfigMaps and Secrets externalized
- [ ] Logging and metrics enabled
- [ ] Distributed tracing configured
- [ ] Backup jobs scheduled
- [ ] Resource quotas set
- [ ] Pod security standards enforced