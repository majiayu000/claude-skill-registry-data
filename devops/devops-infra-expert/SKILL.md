---
name: "devops-infra-expert"
description: "Comprehensive guide for DevOps, Infrastructure as Code, and Observability. Covers Docker, Kubernetes, CI/CD, Network Security, Monitoring, and Workspace Management."
---

# DevOps & Infrastructure Expert Guide

This skill provides the operational standards for deploying, scaling, and monitoring modern cloud-native applications.

## 🏗 Infrastructure as Code (IaC)
- **Terraform/Pulumi**: Use IaC for all cloud resources. Maintain state securely.
- **Docker**: Create optimized, multi-stage Dockerfiles. Use small base images (e.g., Alpine or Distroless).
- **Kubernetes (K8s)**: Use `kind` for local development. Define clear resource limits and readiness/liveness probes.

---

### 🐳 Dockerfile — Canonical 7-Stage Build  (E05 Gap B04 · CHE_RULES §XI Table 2 row 761)

Stage order (cache-friendliest first):
1. `base` — small runtime base (prefer `gcr.io/distroless/static-debian12` for Go/Rust; `node:20-alpine` for TS)
2. `deps` — install system deps + extract package manager lockfile layer
3. `src` — COPY only `package.json` / `Cargo.toml` / `go.mod` + lockfile FIRST, THEN COPY rest (cache survives source changes)
4. `builder` — compile + `RUN --mount=type=cache,target=/root/.cache/go-build` (buildx cache mount for reuse across builds)
5. `test` — run unit tests in builder layer (FAST FAIL — breaks build before prod image)
6. `migrate` — optional: bundle migration binaries (ONLY for stateful services)
7. `runtime` — `COPY --from=builder /app/bin /usr/local/bin/app`. **NON-NEGOTIABLE USER rule**: `USER nonroot:nonroot` (UID/GID 65532) BEFORE CMD.

**Runtime hardening NON-NEGOTIABLE for ALL production images:**
```dockerfile
HEALTHCHECK --interval=10s --timeout=3s --start-period=60s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
WORKDIR /app
USER nonroot:nonroot
EXPOSE 8080/tcp
ENTRYPOINT ["/usr/local/bin/app"]
CMD ["serve"]
```
Images are scanned in CI with `trivy image --severity CRITICAL,HIGH --exit-code 1`. Any `libssl`/`glibc` HIGH → rebuild base layer.

---

### ⛵ kind Cluster — Local Kubernetes  (E05 Gap B04 · CHE_RULES §XI Table 2 row 762)

Single command reproducible cluster (use for tests AND local development):
```yaml
# kind-config.yaml — 2 workers + load balancer + ingress
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - { role: control-plane, kubeadmConfigPatches: [{ kind: InitConfiguration, nodeRegistration: { kubeletExtraArgs: { node-labels: "ingress-ready=true" } }} ] }
  - { role: worker }
  - { role: worker }
```
Bootstrap order (NON-NEGOTIABLE — MetalLB MUST come before ingress controllers):
1. `kind create cluster --config kind-config.yaml`
2. Install **MetalLB** via Helm + allocate `IPAddressPool` CIDR (required for `LoadBalancer` services locally)
3. Install **ingress-nginx** Helm chart + `nodeSelector: ingress-ready=true`
4. **Only then**: deploy app workloads + `Ingress` resources.

**CI hint**: GitHub Actions `helm/kind-action@v1` does steps 1-3 in 45s — do NOT waste CI minutes re-building this from scratch per step.

---

### ☸️ Kubernetes — Workload Patterns  (E05 Gap B04 · CHE_RULES §XI Table 2 rows 763-765)

#### Deployment (minimum viable manifest):
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  revisionHistoryLimit: 5            # prevent old ReplicaSet sprawl
  strategy: { type: RollingUpdate, rollingUpdate: { maxSurge: 1, maxUnavailable: 0 } } # ZERO downtime
  selector: { matchLabels: { app: api } }
  template:
    spec:
      serviceAccountName: api            # NEVER use default SA with broad perms
      securityContext:
        runAsNonRoot: true; runAsUser: 65532; fsGroup: 65532; allowPrivilegeEscalation: false; readOnlyRootFilesystem: true; capabilities: { drop: [ALL] }
      priorityClassName: business-critical     # companion PriorityClass resource
      topologySpreadConstraints:              # distribute pods across nodes/zones (prevents correlated failures)
        - { maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: ScheduleAnyway, labelSelector: { matchLabels: { app: api } } }
      containers:
        - name: api
          image: myregistry/api:v1.2.3           # PIN specific tag. NEVER :latest in prod
          resources:  # requests MUST equal limits for Guaranteed QoS (critical workloads)
            requests: { cpu: "500m", memory: "512Mi" }
            limits:   { cpu: "500m", memory: "512Mi" }
          # Probe trinity — EVERY workload needs all 3.  NO naked workloads.
          startupProbe:   { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 5, failureThreshold: 24 }  # max 2 minutes to boot
          livenessProbe:  { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 10, failureThreshold: 3 }   # restart loop
          readinessProbe: { httpGet: { path: /readyz,  port: 8080 }, periodSeconds: 5,  failureThreshold: 2 }   # stop routing, do NOT restart
          envFrom: [{ configMapRef: { name: api-config } }, { secretRef: { name: api-secrets } }]
          ports: [{ containerPort: 8080, name: http }]
```
#### Companions (every production Deployment needs at least 3):
- **HPA** (HorizontalPodAutoscaler) `minReplicas: 3 / maxReplicas: 20 / targetCPUUtilizationPercentage: 70` + KEDA if scaling off custom metrics (queue depth etc.)
- **PDB** (PodDisruptionBudget) `minAvailable: 2` — guarantees ≥ 2 alive during node drains / voluntary evictions (prevents outages during cluster upgrades)
- **NetworkPolicy** `default-deny-all` base + explicit allow-lists (zero-trust, no broad cluster-wide CIDR egress by default)

---

### 🎯 Helm Charts — Structure & Values Hierarchy  (E05 Gap B04 · CHE_RULES §XI Table 2 row 766)

#### Chart skeleton:
```
charts/myapp/
  Chart.yaml          # apiVersion: v2; appVersion = semver of binary; version = chart semver
  values.yaml         # BASE defaults (prod-like conservative values)
  values-dev.yaml     # overlay for dev (fewer replicas, debug images)
  values-stg.yaml     # overlay for staging (prod-like + canary window)
  values-prod.yaml    # overlay ONLY high-level overrides (replica count, HPA max)
  templates/
    _helpers.tpl      # name/selector/label partials — MUST exist for every chart
    deployment.yaml
    hpa.yaml
    pdb.yaml
    networkpolicy.yaml
    ingress.yaml
    service.yaml
    sa.yaml
    templates/hooks/
      pre-install-migration.yaml   # runs ONCE before install/upgrade (DB migrations)
```
#### Values precedence (HIGH → LOW, NON-NEGOTIABLE):
1. `--set key=value` / `-f my-custom.yaml` (explicit CLI)
2. `-f values-prod.yaml` (env overlay)
3. `-f values-stg.yaml`
4. `-f values-dev.yaml`
5. `values.yaml` (base defaults)

**_helpers naming convention (consumed by every template — prevent drift):**
```yaml
{{- define "myapp.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
```
Helm hooks for schema migrations: `annotations: helm.sh/hook: pre-install,pre-upgrade; helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded` so stale migration Jobs are cleaned. Failure policy: `hook-failed` = block release immediately (Do NOT proceed with app deployment against unmigrated schema).

---

### 🧩 Kustomize — Base / Overlays  (E05 Gap B04 · CHE_RULES §XI Table 2 row 767)

Use for internal services where Helm templating overhead is unnecessary; CI-friendly because there is no release state to drift:
```
k8s/
  base/                          # identical across envs
    kustomization.yaml · deployment.yaml · service.yaml · sa.yaml · hpa.yaml
  overlays/
    dev/
      kustomization.yaml  (resources: [../../base]) + replicas dev=1 + patch Json6902 debug=true
      configMapGenerator:  [ {name: api-config, files: [config.dev.env]} ]
      secretGenerator:     [ {name: api-secret,  envs: [.env.secret.dev]} ]  # .gitignore-d
    stg/   # replicas stg=2 + patch stg env vars
    prod/  # replicas prod=4 + topology spread + sealed-secrets (NOT plain)
  components/                # reusable vertical slices (e.g. "observability sidecars")
    otel-sidecar/  ·  istio-mesh/
```
NON-NEGOTIABLE Kustomize rules: **always `kustomize build k8s/overlays/prod > /tmp/manifest.yaml` then `kubectl diff -f /tmp/manifest.yaml` BEFORE `apply -f`**. Never blind-apply.

---

### 🗺 Terraform — Provider Pin + Module Pattern + Remote State  (E05 Gap B04 · CHE_RULES §XI Table 2 row 768)

#### Provider pinning (NON-NEGOTIABLE — prevent accidental upgrades):
```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws"; version = "~> 5.40" }  # ~> X.Y allows patches ONLY
  }
  required_version = "~> 1.7"
  # REMOTE STATE backend (S3 + DynamoDB lock — NEVER local terraform.tfstate)
  backend "s3" {
    bucket         = "tfstate-accountid-region"
    key            = "${var.project}/${var.environment}/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```
#### Module structure (EVERY module — no monolith main.tf 1000L):
```
modules/rds/
  main.tf        # resources only
  variables.tf   # ALL inputs type-annotated + description
  outputs.tf     # ONLY what callers need (don't leak internals)
  README.md      # example usage snippet
```
#### tfvars hierarchy (HIGH → LOW, match Helm values pattern):
1. `TF_VAR_*` env vars (CI OIDC or local export)
2. `-var-file=environments/dev.tfvars` (env-specific, committed)
3. `terraform.tfvars` (workspace-wide defaults — gitignored usually)
Plan gate in CI: `terraform plan -detailed-exitcode` returns exit 2 if plan contains changes; block merge on drift.

---

## 🚀 CI/CD & Deployment
- **GitHub Actions**: Automate linting, testing, and deployment. Use OIDC for secure cloud provider authentication.
- **Strategies**: Implement Blue/Green or Canary deployments for zero-downtime releases.
- **Environment Management**: Use separate environments (Dev, Staging, Prod). Keep configurations in environment variables or secret managers.

## 📡 Networking & Security
- **Network Design**: Implement VPCs, subnets, and security groups. Follow the principle of least privilege.
- **SSL/TLS**: Ensure all traffic is encrypted. Automate certificate renewal (e.g., Let's Encrypt).
- **Secrets**: Never commit secrets to Git. Use tools like `TruffleHog` to detect leaks.

---

## 📈 Observability & Monitoring (E05 Gap B05 · CHE_RULES §XI Table 2 rows 769-776)

### 🌳 Methodologies — When to use which lens

| Lens | Scope | What you measure | Canonical questions |
|---|---|---|---|
| **🔴 Three Pillars** | Cross-cutting | Logs · Metrics · Traces | "What happened (logs)? How often (metrics)? Where exactly (traces)?" |
| **🔴 RED** | per **Service** | **R**ate (req/s) · **E**rrors (5xx / total) · **D**uration (p50 / p95) | "Is my service SLO-compliant right now?" — 70% of alerting lives here |
| **🔴 Four Golden Signals** | per **Endpoint/Route** | **L**atency · **T**raffic · **E**rrors · **S**aturation | "Why is /checkout slow? — queue saturation at DB" — drill-down from RED |
| **🔴 USE** | per **Resource** (node/VM/pod) | **U**tilization · **S**aturation · **E**rrors | "Is my node CPU/Disk at 95% + queueing + IO errors?" — triage infra capacity |

Non-negotiable combo: RED for service-level SLO alerts → 4GS for endpoint drill → USE for resource root cause. Never alert on raw CPU alone (USE without RED = false positive flood).

---

### 🔥 Prometheus — Recording Rules · Alerts · PromQL  (E05 Gap B05 · CHE_RULES §XI Table 2 row 769)

#### Metric naming convention (`job:metric:operator` — NEVER freeform):
```yaml
groups:
  - name: api_recording
    interval: 30s
    rules:
      # GOOD: service:http_requests:rate5m  (job:metric:operator)
      - record: service:http_requests:rate5m
        expr: sum by (service, route, status_class) (rate(http_requests_total[5m]))
      - record: service:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum by (service, route, le) (rate(http_request_duration_seconds_bucket[5m])))
```
NON-NEGOTIABLE PromQL: **`rate()[5m]` as default**. `irate()` ONLY for 5s-resolution spike graphs in dashboards, NEVER for alerts (irate misses slow burns + drops out on scrape hiccups). Minimum window = 2× scrape interval × (at least 2 buckets) → 5m is safe for 15s scrapes.

#### Alertmanager severity ladder (block noisy non-actionable alerts):
| Severity | When | Action |
|---|---|---|
| `critical` | User-visible outage NOW or < 5min away | PagerDuty → on-call |
| `warn` | Degraded but SLO not breached yet (p95 > 2s for 10min) | Slack alert channel |
| `info` | Announcement (deploy version bump, certificate renewal in 7 days) | Email digest |
Use **inhibition rules**: a `critical` SERVICE_DOWN alert MUST silence all descendant `warn` endpoint alerts for the same service (prevents alert storm of 50 alerts from 1 root cause).

---

### 🧱 OpenTelemetry Collector — Pipeline Architecture  (E05 Gap B05 · CHE_RULES §XI Table 2 row 770)

```yaml
receivers:   # INGEST data from services
  otlp:      { protocols: { grpc: { endpoint: 0.0.0.0:4317 }, http: { endpoint: 0.0.0.0:4318 } } }
  prometheus: { config: { scrape_configs: [ { job_name: otel, scrape_interval: 15s, static_configs: [{ targets: ["0.0.0.0:8888"] }] } ] } }

processors:  # TRANSFORM — order MATTERS (top→bottom).  batch + memory_limiter NON-NEGOTIABLE.
  memory_limiter: { check_interval: 1s, limit_mib: 1024, spike_limit_mib: 256 }  # first = OOM guard
  batch:            { send_batch_size: 8192, timeout: 200ms }                       # second = compress batching
  resource:         { attributes: [ { key: deployment.environment, value: "${ENV:DEPLOY_ENV}" }, { key: service.version, from_context: Resource } ] }
  k8sattributes:    { extract: { metadata: [ podName, namespace, nodeName, podUID ] } }  # k8s enricher
  tail_sampling:    { policies: [ { name: errors-rate, type: rate_limiting, rate_limiting: { spans_per_second: 50 } }, { name: drop-health, type: string_attribute, string_attribute: { key: http.route, values: ["/healthz","/readyz"] , invert_match: true } } ] }

exporters:   # SHIP out to storage
  otlp/loki:       { endpoint: "loki-gateway:3100", headers: { "X-Scope-OrgID": "tenant1" } }   # logs
  prometheusremotewrite: { endpoint: "http://mimir-nginx/api/v1/push" }                            # metrics
  otlp/tempo:      { endpoint: "tempo-distributor:4317", tls: { insecure: true } }                 # traces
  otlp/saas:       { endpoint: "ingest.datadoghq.com:443" }  # optional SaaS export alongside self-hosted

service:
  pipelines:
    traces:  { receivers: [otlp],         processors: [memory_limiter, resource, k8sattributes, tail_sampling, batch], exporters: [otlp/tempo, otlp/saas] }
    metrics: { receivers: [otlp, prometheus], processors: [memory_limiter, resource, batch], exporters: [prometheusremotewrite, otlp/saas] }
    logs:    { receivers: [otlp],         processors: [memory_limiter, resource, k8sattributes, batch], exporters: [otlp/loki, otlp/saas] }
```
Tail-based sampling is NON-NEGOTIABLE for cost control in high-traffic services: keep 100% of error spans + 1% of healthy + forced sampling for flagged `user_id`. DO NOT use head-based sampling for anything beyond dev.

---

### 📈 Grafana + Loki + Tempo — Query Patterns  (E05 Gap B05 · CHE_RULES §XI Table 2 row 771)

#### Loki — LogQL (avoid `.*` regex = expensive full-table scan):
```logql
// GOOD: label match first → pipeline filter (no regex until after narrow)
{app="api", namespace="prod", container="app"}
  |= "error"                            // fast substring match filter FIRST
  | json                                // parse JSON AFTER filter (much cheaper)
  | route = "/api/checkout"             // label extracted from JSON
  | duration_ms > 2000                  // numeric compare
  | line_format "[{{.trace_id}}] {{.status}} {{.route}} {{.duration_ms}}ms"
```
NON-NEGOTIABLE rule for Loki retention: **`retention_period: 744h` (31 days) for prod; 168h (7d) for dev/stg**. Logs older than 31 days → archive to S3 Glacier via ruler storage, do NOT keep in hot Loki.

#### Tempo — TraceQL (find the slow span):
```traceql
// Service api, duration > 2 seconds, status = error
{ .service.name = "api" && duration > 2s && status = error }
  | childCount > 5                      # only traces with many spans (interesting)
  // then open Gantt → jump to slowest span → click "Logs for this span" (auto-jumps to matching Loki context)
```
Correlation is critical: Grafana datasource provisioning (in Kustomize Helm chart) MUST enable **Loki ↔ Tempo bidirectional links** so every log line has `[Trace →]` button, every trace span has `[Logs for span ←]` button. Do NOT hard-code dashboards → deploy via `ConfigMap` + Grafana sidecar `sidecar.dashboards.enabled: true` (as-code, not UI-only).

---

### 🛡 Sentry SDK — PII Filtering + Env-Separated DSN  (E05 Gap B05 · CHE_RULES §XI Table 2 row 772)

**NON-NEGOTIABLE: ONE DSN per environment. NEVER share a DSN across dev/stg/prod.**
```ts
// TypeScript SDK init pattern (same idiom in Go/Python/Rust SDKs)
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.SENTRY_DSN,  // different secret per env; CI sets SENTRY_ENVIRONMENT
  environment: process.env.SENTRY_ENVIRONMENT ?? "local",
  release: process.env.SENTRY_RELEASE ?? `unknown@${commitSha}`,
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,  // prod sample 10% for cost
  beforeSend(event) {
    // 🔴 PII FILTER — runs BEFORE event leaves the process (never send raw)
    if (event.user?.email)    delete event.user.email
    if (event.user?.id)       event.user.id = hashPii(event.user.id, process.env.NOTIFICATION_PII_HASH_SECRET!)
    for (const exc of event.exception?.values ?? []) {
      for (const frame of exc.stacktrace?.frames ?? []) {
        // Strip any local file paths containing /home/ (risk of leaking dev usernames)
        if (frame.abs_path?.startsWith("/home/")) frame.abs_path = frame.filename
      }
    }
    return event
  },
  integrations: defaultIntegrations => defaultIntegrations
    .filter(i => i.name !== "Dedupe")  // we want duplicates → count frequency for alerting
    .concat([new Sentry.Integrations.Http({ tracing: true })]),
})
```
Breadcrumb + Contexts pattern: EVERY user request → `Sentry.setUser({ id: hashed_id })` + `Sentry.setTag("service.version", pkg.version)` + `Sentry.setContext("request", { route, method, traceId })` so events are sliceable by version. Never log secrets into Sentry `extra` field (same rule as structured logs per engineering-contracts §19).

---

### 🐕 Datadog — Unified Tag Taxonomy  (E05 Gap B05 · CHE_RULES §XI Table 2 row 773)

**3 mandatory tags on EVERY single telemetry item (metric point / log line / trace span) — NON-NEGOTIABLE:**
| Tag | Example | Purpose |
|---|---|---|
| `env`       | `env:prod` | Segment dashboards/alerts between dev/stg/prod — ZERO cross-env leakage |
| `service`   | `service:api-checkout` | RED / APM default aggregation key |
| `version`   | `version:v1.42.0` | Correlate deploys → regressions (overlay deploy marker on metrics) |

Additional tags: `team:payments`, `region:eu-west-2`, `pod_name`, `node_name`, `k8s_namespace`. **MAX 12 custom tags per telemetry type** (beyond → cardinality explosion cost $10k+/mo).

#### APM + DogStatsD:
- Services emit `DATADOG_TRACE_ENABLED=true` + `DD_TRACE_OTEL_ENABLED=true` (bridges OpenTelemetry spans natively into Datadog APM without double-instrumentation)
- Custom business metrics via DogStatsD UDP (port 8125): `statsd.increment("checkout.success", 1, { tags: ["plan:premium","currency:gbp"] })` — NOT HTTP, never block request handler thread
- Grok parser for raw logs: extract `%{data:route}` and `%{number:status_code:integer}` so log attributes become tags → queryable in Log Explorer facets without index explosion. Synthetic heartbeat monitors ping every critical public endpoint (30s intervals) in prod.

---

## ☁️ B-P1 CloudNative · GitOps + Policy + Cost-Control (E05 §XI P1 coverage 55% → ~70%)

### ArgoCD ApplicationSet Generator (Multi-team multi-env GitOps scale)
Single `ApplicationSet` replaces 200 duplicated `Application` manifests. Use generators in priority order:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  generators:
  - matrix:
      generators:
      - list: { elements: [{env: dev},{env: staging},{env: prod}] }     # 3 envs
      - git:                                                        # 12 services per env = 36 apps
          repoURL: https://github.com/org/k8s-apps.git
          directories: [{ path: services/* }]
  template:
    metadata: { name: '{{path.basename}}-{{env}}' }
    spec:
      project: '{{env}}'
      destination: { server: 'https://kubernetes.default.svc', namespace: '{{path.basename}}-{{env}}' }
      source: { repoURL: ..., path: '{{path}}/overlays/{{env}}', targetRevision: 'env/{{env}}' }
      syncPolicy:
        automated:
          prune: true           # NON-NEGOTIABLE: delete old Deployments/ConfigMaps when removed from git
          selfHeal: true        # Drift auto-repair. NO manual kubectl edit in prod — open PR + merge.
        syncOptions: ['CreateNamespace=true','PrunePropagationPolicy=foreground']
```
**ArgoCD Image Updater** = commits new image tags automatically to git on registry push → zero manual PRs for deploy-train pipeline.

### Crossplane XR / XRC (Terraform for K8s native teams, self-service cloud via kubectl)
Crossplane = cloud infra via K8s CRDs, NO separate Terraform apply jobs for app teams. Steps:
1. **Platform team writes XR (Composite Resource Definition) + Composition**:
   ```yaml
   # XR schema: PostgresDB is a NEW kubectl resource exposed to product teams
   apiVersion: apiextensions.crossplane.io/v1
   kind: CompositeResourceDefinition
   spec:
     group: myorg.example
     names: { kind: PostgresDB, plural: postgresdbs }
     claimNames: { kind: DB }          # teams `kubectl apply -f db.yaml` 10 lines, no Terraform
     versions:
     - name: v1alpha1
       schema:
         openAPIV3Schema:
           type: object
           properties:
             spec:
               properties:
                 size: { type: string, enum: [small,medium,large] }
                 engineVersion: { type: string, default: "16" }
   ```
2. **Composition maps DB → AWS RDS (provider-aws)** with ALL guardrails: encryption-at-rest, deletion-protection, VPC private, backup 30-day, multi-AZ. Team CANNOT accidentally create public DB = security by-composition.
3. **Claim**: `kubectl apply -f <<< {apiVersion: myorg.example/v1alpha1, kind: DB, metadata: {name: orders}, spec: {size: medium}}` → platform guardrails enforced, team self-service in 30 seconds.

### OpenCost / Kubecost Cost Attribution (cloud bill → team/service)
Cost visibility = capacity planning + responsible spend. Every Deployment MUST have 3 labels for OpenCost aggregation:
```yaml
metadata:
  labels:
    app: checkout          # 1: component
    team: payments         # 2: team owner
    cost-center: pc-prod-2138 # 3: finance allocation
```
OpenCost Prometheus exporter (`opencost/opencost` Helm chart) scrapes every 60s → Grafana panel shows $/day per namespace + $/deployment + $/pod. Monthly > $50 drift unaccounted = automatic ticket to team owner alert via Prometheus + alertmanager.

### OPA/Gatekeeper ConstraintTemplate (POLICY AS CODE, non-negotiable security defaults prod)
2 ConstraintTemplate shipped in EVERY prod cluster, NO EXCEPTIONS:
```yaml
# 1. K8sAllowedRepos: ONLY allow approved image registries (dockerhub is public → supply chain poison risk)
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
spec:
  match: { kinds: [{ apiGroups: [""], kinds: ["Pod"] }] }
  parameters:
    repos: ["123456789012.dkr.ecr.eu-west-2.amazonaws.com/","ghcr.io/org-name/"]
---
# 2. K8sRequiredLabels: fail admission if Deployment missing team+app+cost-center (open cost aggregation)
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
spec:
  match: { kinds: [{ apiGroups: ["apps"], kinds: ["Deployment","StatefulSet"]}] }
  parameters: { labels: ["team","app","cost-center"] }
```
`violations` show in ArgoCD Sync status → app developer cannot merge PR that breaks policy. 3rd-party constraint (optional): `K8sPSPAllowPrivilegeEscalationContainer: false` → block `securityContext.allowPrivilegeEscalation=true` (HIGH severity CVE pattern).

---

## 📦 Workspace Management
- **Nx**: Use for monorepo orchestration. Optimize build times using caching and affected commands.
- **Higiene**: Maintain a clean worktree. Automate the removal of temporary artifacts.

## 🔗 References
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Nx Documentation](https://nx.dev/)
- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices) · [buildx cache mounts](https://docs.docker.com/build/attestations/slsa-provenance)
- [kind sigs.k8s.io](https://kind.sigs.k8s.io) · [MetalLB](https://metallb.universe.tf)
- [K8s Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes) · [PDB](https://kubernetes.io/docs/tasks/run-application/configure-pdb) · [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale) · [TopologySpreadConstraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices) · [Helm Hooks](https://helm.sh/docs/topics/charts_hooks)
- [Kustomize sigs.k8s.io](https://kubectl.docs.kubernetes.io/references/kustomize)
- [Prometheus Recording Rules Naming](https://prometheus.io/docs/practices/rules) · [Alertmanager Inhibition](https://prometheus.io/docs/alerting/latest/configuration/#inhibit_rule)
- [OTel Collector Pipeline](https://opentelemetry.io/docs/collector/architecture) · [OTel Tail-based Sampling](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)
- [Loki LogQL](https://grafana.com/docs/loki/latest/query) · [Tempo TraceQL](https://grafana.com/docs/tempo/latest/traceql) · [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning)
- [Sentry beforeSend Filtering](https://docs.sentry.io/platforms/javascript/guides/nextjs/configuration/filtering)
- [Datadog Unified Tagging](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging) · [Datadog Grok Parser](https://docs.datadoghq.com/logs/log_configuration/parsing)
