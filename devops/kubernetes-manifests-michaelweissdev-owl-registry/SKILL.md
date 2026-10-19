---
name: kubernetes-manifests
description: >
  Design, author, harden, and validate production-grade Kubernetes resource manifests
  and Helm charts. Use when authoring or reviewing Deployments, StatefulSets, Services,
  Ingress, NetworkPolicies, ConfigMaps, Secrets, RBAC, PodDisruptionBudgets, container
  resource requests/limits, health probes, or security contexts.
compatibility: >
  Agent Skills-compatible coding agents with access to kubectl, kubeconform, or helm tooling. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "kubernetes, k8s, manifests, helm, rbac, securitycontext, networkpolicy, devops"
  topics: "devops"
---

# Production Kubernetes Resource Manifest Engineering

Kubernetes orchestrates containerized workloads across distributed infrastructure. Writing production-ready manifests requires strict isolation, deterministic scheduling, resilient lifecycles, and defense-in-depth container sandboxing. Every workload deployed to a cluster must specify explicit resource contracts, defensive security contexts, fine-grained RBAC, and granular network policies.

## Purpose & Overview

This skill guides the authoring, templating, auditing, and validation of declarative Kubernetes manifests. Following these standards ensures:
- Workloads are resilient against pod evictions, node drains, and cascading restarts.
- Containers run under strict unprivileged boundaries (non-root, read-only root filesystems, dropped capabilities).
- Ingress and intra-cluster communication are restricted via zero-trust NetworkPolicies.
- Manifests can be deterministically validated offline with `kubeconform` before applying to clusters.

---

## Core Principles & Rules

1. **Always Enforce Unprivileged Pod and Container Security Contexts**:
   - Set `runAsNonRoot: true`, `runAsUser: 10001` (or UID > 10000), `runAsGroup: 10001`.
   - Set `allowPrivilegeEscalation: false`.
   - Set `readOnlyRootFilesystem: true`. Use explicit `emptyDir` mounts for `/tmp` or write buffers.
   - Drop all Linux capabilities with `capabilities: { drop: ["ALL"] }`.
   - Set `seccompProfile: { type: "RuntimeDefault" }`.

2. **Always Define Both Resource Requests and Limits**:
   - `requests` dictate scheduling placement; `limits` prevent noisy-neighbor starvation and runaway memory leaks.
   - For memory, set `requests.memory` equal to `limits.memory` where possible to achieve Guaranteed QoS and avoid random OOM kills under node pressure.
   - Avoid infinite or absent CPU limits that allow runaway threads to consume host cores.

3. **Configure the Complete Probe Triumvirate**:
   - **`startupProbe`**: For slow-starting processes to avoid premature liveness restarts.
   - **`readinessProbe`**: Controls traffic routing in Service endpoints; failing readiness cuts incoming traffic without terminating the pod.
   - **`livenessProbe`**: Detects deadlocks; failure triggers pod termination and restart. Keep `periodSeconds` reasonable (e.g. 10s-15s) and `timeoutSeconds` short (e.g. 2s-5s).

4. **Zero-Trust Network Policies by Default**:
   - Create a default-deny ingress and egress `NetworkPolicy` per namespace.
   - Whitelist explicit egress only to necessary external destinations, DNS (`kube-system` port 53), and dependent services.

5. **Disable Default Service Account Token Automounting**:
   - Set `automountServiceAccountToken: false` on ServiceAccounts and Pod specs unless the container specifically needs to talk to the Kubernetes API.

6. **Guard Availability with PodDisruptionBudgets (PDB)**:
   - For workloads with replica count >= 2, always attach a PDB specifying `minAvailable` or `maxUnavailable` to guard against node drains and maintenance.

---

## Standard Workflows & Procedures

### Workflow: Creating a Production Deployment

1. **Namespace & Isolation**: Target a dedicated application namespace.
2. **Pod Identity**: Define a dedicated `ServiceAccount` with `automountServiceAccountToken: false`.
3. **Configuration & Secrets**: Separate static configuration (`ConfigMap`) from sensitive credentials (`Secret` or CSI Secret Store driver).
4. **Workload Definition**:
   - Specify labels following standard conventions (`app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`).
   - Define probes (`startupProbe`, `readinessProbe`, `livenessProbe`).
   - Define exact `resources` requests and limits.
   - Configure Pod and Container `securityContext`.
5. **Traffic & Routing**: Attach a ClusterIP `Service` targeting named container ports. Expose externally via `Ingress` with TLS and `ingressClassName`.
6. **Network & Disruption**: Attach a `NetworkPolicy` and `PodDisruptionBudget`.
7. **Offline Validation**: Run `kubeconform` against target Kubernetes schema version before committing or applying.

---

## Real-World Examples & Patterns

### 1. Hardened Production Deployment Manifest (`deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app.kubernetes.io/name: order-service
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: ecommerce-platform
    app.kubernetes.io/managed-by: gitops
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: order-service
  template:
    metadata:
      labels:
        app.kubernetes.io/name: order-service
        app.kubernetes.io/component: backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: order-service-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        fsGroupChangePolicy: "OnRootMismatch"
        seccompProfile:
          type: RuntimeDefault
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: order-service
                topologyKey: topology.kubernetes.io/zone
      containers:
        - name: app
          image: ghcr.io/org/order-service:v1.4.2@sha256:d8b76b2bf963e6e8e5ab82354c0174be
          imagePullPolicy: IfNotPresent
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
            - name: ENVIRONMENT
              value: "production"
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
          resources:
            requests:
              cpu: 250m
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 512Mi
          startupProbe:
            httpGet:
              path: /healthz/startup
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 12
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: http
            periodSeconds: 5
            timeoutSeconds: 2
            successThreshold: 1
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: http
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir:
            medium: Memory
            sizeLimit: 64Mi
```

### 2. Zero-Trust NetworkPolicy Pattern (`network-policy.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-isolation
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: order-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow incoming traffic only from the Ingress Controller and API Gateway
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: api-gateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Allow CoreDNS lookups in kube-system
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # Allow communication to Postgres database service
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: postgres
      ports:
        - protocol: TCP
          port: 5432
```

### 3. PodDisruptionBudget and RBAC Configuration (`pdb-rbac.yaml`)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-service-pdb
  namespace: ecommerce
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: order-service
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service-sa
  namespace: ecommerce
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: config-reader
  namespace: ecommerce
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: order-service-config-binding
  namespace: ecommerce
subjects:
  - kind: ServiceAccount
    name: order-service-sa
    namespace: ecommerce
roleRef:
  kind: Role
  name: config-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Risk | Production Resolution |
| :--- | :--- | :--- |
| **Missing Resource Limits/Requests** | Noisy neighbors starve adjacent pods; cluster autoscaler cannot make accurate bin-packing decisions. | Set explicit `requests` and `limits` on every container. Set memory request equal to limit to guarantee QoS. |
| **Running as Root (`runAsUser: 0`)** | Container escape exploits grant immediate root access to the host kernel. | Enforce `runAsNonRoot: true` and configure numeric UID/GID > 10000. |
| **Using `latest` image tag** | Unpredictable rollouts; non-reproducible pod restarts; breaks rollback capabilities. | Pin images to immutable semantic tags and sha256 digests (`@sha256:...`). |
| **Liveness probe checking external DB** | Cascading failure: if the database blips, all pods restart simultaneously, amplifying database overload. | Liveness probe checks process health only. Readiness probe checks dependency connectivity. |
| **Writable root filesystem** | Intruders or malware can download payloads and overwrite binaries at runtime. | Set `readOnlyRootFilesystem: true`; use ephemeral `emptyDir` for scratch buffers. |
| **Automounting ServiceAccount Token** | Compromised pods can read secrets and impersonate accounts against the API server. | Explicitly configure `automountServiceAccountToken: false`. |

---

## Verification Checklist

When authoring or inspecting Kubernetes manifests, verify each condition before deploying:

- [ ] **Validation**: `kubeconform -strict -summary -kubernetes-version <version> <manifest>.yaml` returns zero errors.
- [ ] **Client Dry-Run**: `kubectl apply --dry-run=client -f <manifest>.yaml` validates syntax cleanly.
- [ ] **Security Context**: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, and `capabilities.drop: ["ALL"]` are specified.
- [ ] **Seccomp**: `seccompProfile: { type: RuntimeDefault }` is explicitly declared.
- [ ] **Resource Sizing**: Both `requests` and `limits` are declared for CPU and Memory.
- [ ] **Probes**: `readinessProbe` and `livenessProbe` are configured; `startupProbe` added if init duration exceeds 10s.
- [ ] **High Availability**: `replicas >= 2`, Pod anti-affinity enabled across zones, and a `PodDisruptionBudget` is attached.
- [ ] **RBAC & Token**: Pod uses a dedicated `ServiceAccount` with `automountServiceAccountToken: false` unless API access is mandatory.
- [ ] **Network Isolation**: Namespace has a default-deny `NetworkPolicy` and an explicit ingress/egress allow rule for the workload.

---

## Tooling & Reference Guides

- **Validation Command (`kubeconform`)**:
  ```bash
  kubeconform -strict -summary -schema-location default -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' manifests/
  ```
- **Live Dry Run & Diff**:
  ```bash
  kubectl diff -f manifests/
  kubectl apply --dry-run=server -f manifests/
  ```
- **Security Audit Tooling**:
  - `polaris audit --audit-path manifests/`
  - `trivy config manifests/`
  - `kube-linter lint manifests/`
- **Official Documentation**:
  - [Kubernetes Workload Resources](https://kubernetes.io/docs/concepts/workloads/)
  - [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
  - [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
