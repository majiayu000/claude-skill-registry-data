---
name: k8s
description: "Generate production-grade Kubernetes manifests — Deployments with probes and security contexts, Services, Ingress with TLS, HPA, PDB, NetworkPolicy, ConfigMaps, Secrets — with optional Helm charts, Kustomize overlays, Istio mesh, and ArgoCD GitOps"
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--helm` — generate a Helm chart instead of plain manifests
- `--namespace <name>` — target namespace (default: app name)
- `--replicas <n>` — initial replica count (default: 2)
- `--ingress <domain>` — configure ingress with this domain
- `--istio` — include Istio service mesh annotations
- `--argocd` — generate ArgoCD Application manifest
- `--kustomize` — generate Kustomize overlays for dev/staging/prod
- A specific resource to generate: `deployment`, `service`, `ingress`, `hpa`, `configmap`, `secret`, `pdb`
- If no arguments, generate the full manifest set as plain YAML

============================================================
PHASE 1 — APPLICATION ANALYSIS
============================================================

Scan the project to determine Kubernetes requirements:

**Container image**:
- Check for existing Dockerfile — extract EXPOSE port, HEALTHCHECK, CMD
- If no Dockerfile, note that one is needed (reference `deploy/docker` skill)
- Determine image name from: git remote URL, package.json name, go.mod module

**Ports and protocols**:
- Read application config for listen port (default: 3000/8080)
- Check for gRPC (protobuf files), WebSocket endpoints, metrics endpoint (`/metrics`)

**Resource requirements** — estimate based on stack:
- Node.js: 128Mi-512Mi memory, 100m-500m CPU
- Go: 64Mi-256Mi memory, 50m-250m CPU
- Java/Spring: 512Mi-1Gi memory, 250m-1000m CPU
- Python: 128Mi-512Mi memory, 100m-500m CPU

**Dependencies**:
- Database: detected from Prisma, SQLAlchemy, GORM, etc.
- Cache: Redis/Memcached references
- Message queues: RabbitMQ, Kafka, NATS
- External services: API calls, third-party integrations

**Health endpoints**:
- Check for `/health`, `/healthz`, `/ready`, `/readyz`, `/live`, `/livez`
- If none found, note to create them

**Environment variables**:
- Scan for `process.env.`, `os.Getenv`, `os.environ` references
- Categorize as: config (ConfigMap) vs secrets (Secret)

============================================================
PHASE 2 — GENERATE NAMESPACE AND RBAC
============================================================

Create `k8s/namespace.yml` with standard Kubernetes labels:
- `app.kubernetes.io/name`
- `app.kubernetes.io/managed-by: skill-deploy-k8s`

Create `k8s/serviceaccount.yml` with matching labels.

============================================================
PHASE 3 — GENERATE CORE MANIFESTS
============================================================

Create all manifests in `k8s/` directory (or `helm/{app-name}/templates/` if `--helm`).

**Deployment** (`k8s/deployment.yml`):
- `apiVersion: apps/v1`
- Minimum 2 replicas for HA
- Rolling update strategy: `maxSurge: 1`, `maxUnavailable: 0`
- Pod anti-affinity: prefer spreading across nodes
- Resource requests AND limits (always set both)
- Liveness probe: HTTP GET on health endpoint, `initialDelaySeconds: 15`, `periodSeconds: 10`
- Readiness probe: HTTP GET on ready endpoint, `initialDelaySeconds: 5`, `periodSeconds: 5`
- Startup probe (for slow-starting apps like Java): `failureThreshold: 30`, `periodSeconds: 10`
- `terminationGracePeriodSeconds: 30`
- Security context: `runAsNonRoot: true`, `runAsUser: 1001`, `fsGroup: 1001`, `seccompProfile: RuntimeDefault`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: ["ALL"]`
- Environment from ConfigMap and Secret refs
- Image pull policy: `IfNotPresent` for tagged, `Always` for `latest`

**Service** (`k8s/service.yml`):
- `type: ClusterIP` (default — use Ingress for external access)
- Target port matching container port
- Named port for service mesh compatibility

**Ingress** (`k8s/ingress.yml`, if domain provided):
- `networking.k8s.io/v1`
- TLS with cert-manager annotation: `cert-manager.io/cluster-issuer: letsencrypt-prod`
- nginx SSL redirect: `nginx.ingress.kubernetes.io/ssl-redirect: "true"`
- Path-based routing (`/` -> service)

**HPA** (`k8s/hpa.yml`):
- `autoscaling/v2`
- Min replicas: 2, Max replicas: 10
- CPU target: 70%, Memory target: 80%
- Scale-down stabilization: 300s (prevent flapping)
- Scale-up stabilization: 60s
- Scale-down policy: max 25% reduction per 60s

**PodDisruptionBudget** (`k8s/pdb.yml`):
- `minAvailable: 1` for small replica counts

**ConfigMap** (`k8s/configmap.yml`):
- Non-sensitive configuration values extracted from env analysis

**Secret** (`k8s/secret.yml`):
- Placeholder secret with `stringData` (not base64 in source)
- Clearly marked as "REPLACE BEFORE APPLYING"

**NetworkPolicy** (`k8s/networkpolicy.yml`):
- Default deny ingress
- Allow ingress only from ingress controller namespace
- Allow egress to database/cache services and DNS (kube-dns port 53)

============================================================
PHASE 4 — HELM CHART (if --helm)
============================================================

Generate Helm chart structure under `helm/{app-name}/`:
- `Chart.yaml`, `values.yaml`, `values-dev.yaml`, `values-staging.yaml`, `values-prod.yaml`
- `templates/`: deployment, service, ingress, hpa, pdb, configmap, secret, serviceaccount, networkpolicy, `_helpers.tpl`, `NOTES.txt`

**values.yaml** — parameterize all environment-specific values:
- `image.repository`, `image.tag`, `image.pullPolicy`
- `replicaCount`, `resources.requests`, `resources.limits`
- `ingress.enabled`, `ingress.hosts`, `ingress.tls`
- `autoscaling.enabled`, `autoscaling.minReplicas`, `autoscaling.maxReplicas`
- `env` as key-value map

**_helpers.tpl** — standard helper templates: `fullname`, `name`, `chart`, `labels`, `selectorLabels`

============================================================
PHASE 5 — KUSTOMIZE (if --kustomize)
============================================================

Generate Kustomize structure under `k8s/`:
- `base/` with `kustomization.yaml` and all core manifests
- `overlays/dev/` — 1 replica, lower resources, debug logging
- `overlays/staging/` — 2 replicas, production-like resources, info logging
- `overlays/prod/` — 3+ replicas, full resources, warn logging, PDB enabled

============================================================
PHASE 6 — ISTIO / SERVICE MESH (if --istio)
============================================================

- Pod annotation: `sidecar.istio.io/inject: "true"`
- Namespace label: `istio-injection: enabled`
- Generate `VirtualService` for traffic routing
- Generate `DestinationRule` for connection pool settings
- Generate `PeerAuthentication` for mTLS (STRICT mode)

============================================================
PHASE 7 — ARGOCD (if --argocd)
============================================================

Generate `argocd/application.yml`:
- Source from git remote with `targetRevision: HEAD`
- Path to k8s/ or helm/ directory
- Sync policy: automated with prune and self-heal enabled


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## Kubernetes Manifests Generated

### Files Created
{list all generated files with one-line descriptions}

### Resource Summary
| Resource | Name | Key Settings |
|----------|------|--------------|
| Namespace | {ns} | -- |
| Deployment | {name} | {replicas} replicas, {memory} memory |
| Service | {name} | ClusterIP, port {port} |
| Ingress | {name} | {domain}, TLS enabled |
| HPA | {name} | {min}-{max} replicas |
| PDB | {name} | minAvailable: 1 |

### Apply Commands
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/

### Pre-Apply Checklist
- [ ] Replace placeholder secrets in k8s/secret.yml
- [ ] Verify container image is pushed to registry
- [ ] Ensure namespace exists in target cluster
- [ ] Configure cert-manager ClusterIssuer if using TLS
- [ ] Review resource limits for your workload
```

============================================================
NEXT STEPS
============================================================

1. Build and push the container image (run `deploy/docker` if needed)
2. Replace placeholder secrets with real values (or use external secrets operator)
3. Apply manifests to a dev cluster first: `kubectl apply -f k8s/ -n {namespace}`
4. Verify pods are running: `kubectl get pods -n {namespace}`
5. Check probes: `kubectl describe pod -n {namespace}`
6. Consider GitOps with ArgoCD or Flux for automated deployments (use `--argocd`)


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /k8s — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT use `apiVersion: extensions/v1beta1` — use current stable APIs
- Do NOT set resource limits without requests (always set both)
- Do NOT use `latest` tag in deployment manifests — use specific tags or SHA digests
- Do NOT store real secrets in YAML files committed to git
- Do NOT set `replicas` in Deployment when HPA is enabled (HPA manages replicas)
- Do NOT use `hostNetwork: true` or `hostPort` without explicit justification
- Do NOT use `privileged: true` in security context
- Do NOT skip liveness/readiness probes — they are required for production
- Do NOT use `LoadBalancer` service type without considering cost — prefer `ClusterIP` + Ingress
- Do NOT overwrite existing manifests without reading them first
- Do NOT generate manifests for services not detected in the project
