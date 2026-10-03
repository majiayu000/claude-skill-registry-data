---
name: devops-platform
description: Production-grade DevOps and platform engineering guidance — Docker, Kubernetes, CI/CD pipelines, Terraform/IaC, GitOps, deployment strategies (rolling/blue-green/canary), monitoring and alerting, and cloud patterns across AWS/Azure/GCP. Use this whenever the user asks about containerizing an app, writing a Dockerfile or Kubernetes manifest, setting up CI/CD (GitHub Actions, GitLab CI, Jenkins, Azure DevOps), Terraform/Pulumi infrastructure, ArgoCD/Flux/GitOps, autoscaling, secrets management, observability (Prometheus, Grafana, Datadog, OpenTelemetry), or rollback/deployment strategy — even if they just say "help me deploy this" or "why is my pod crash-looping."
---

# DevOps & Platform Engineering

Approach every platform task as the engineer who gets paged at 3am when it breaks. The pipeline isn't done when it works on the happy path — it's done when a failure is easy to detect, easy to explain, and easy to reverse. Every config decision here exists to serve one of those three properties.

---

## Step 0: Ground the Platform Work

Before writing any pipeline, container, or deployment config, get clear on:

1. **What is being deployed?** Stateless service, stateful service, batch job, scheduled task — each has a different deployment shape.
2. **What are the environments?** Dev, staging, prod — what's the promotion path between them, and what gates it?
3. **What's the rollback strategy?** If this deploy fails, how long to last-known-good, and is that automatic or manual?
4. **What does healthy look like?** Define the health check before writing the deployment manifest, not after.
5. **Who gets paged, and on what signal?** Observability and alerting are part of the deployment, not an afterthought bolted on later.

If the user hasn't specified these, don't guess silently — a deployment plan built on the wrong assumption (e.g., stateless when it's actually stateful) causes real incidents. Ask, or state the assumption you're making and why.

---

## Docker

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

# Stage 3: Runtime — minimal, non-root
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

**Why each rule matters:**
- **Pin base image versions** — `latest` means the image you tested isn't the image you shipped; you lose the ability to say exactly what's running.
- **Multi-stage builds** — the production image should contain nothing an attacker could use if they got a shell: no compilers, no source, no dev dependencies.
- **Non-root user** — a container escape from a root process is a host compromise; from a non-root process it's much more contained.
- **`.dockerignore`** — exclude `node_modules`, `.git`, `*.md`, tests, local `.env`. Keeps build context small and secrets out of layers.
- **`HEALTHCHECK`** — without it, the orchestrator can only tell if the process is running, not if it's actually serving traffic correctly.

---

## Docker Compose (Local Dev)

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  pg_data:
  redis_data:
```

`depends_on: condition: service_healthy` matters more than it looks — without it, `app` can start before `db` is actually accepting connections, causing flaky failures that only show up under load or on a slow CI runner.

---

## Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0        # zero-downtime rollout
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
        - name: user-service
          image: registry/user-service:1.2.3   # pinned tag, never latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          envFrom:
            - configMapRef:
                name: user-service-config
            - secretRef:
                name: user-service-secrets
          securityContext:
            runAsNonRoot: true
            runAsUser: 1001
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: user-service-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: user-service
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-netpol
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes: [Ingress, Egress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
```

**Mandatory for every workload, and why:**
- `resources.requests`/`limits` — without limits, one misbehaving pod starves every other pod on the node ("noisy neighbor").
- `livenessProbe` + `readinessProbe` — liveness restarts a stuck pod; readiness stops traffic from reaching a pod that's up but not ready (e.g., still warming a cache). Conflating the two causes either premature restarts or traffic sent to dead pods.
- `maxUnavailable: 0` — guarantees the rollout never drops below full capacity; combine with `PodDisruptionBudget` so voluntary disruptions (node drains, cluster upgrades) respect the same floor.
- `NetworkPolicy` — by default every pod in a cluster can talk to every other pod; this is almost never what you want in production. Default-deny and explicitly allow.
- `securityContext` — non-root, no privilege escalation, read-only root filesystem wherever the app allows it.
- `namespace` — never deploy to `default`; it makes RBAC and quota scoping meaningless.

**Horizontal Pod Autoscaler:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
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

---

## Deployment Strategies

Rolling update (above) is the right default, but not always the right choice. Match the strategy to what failure would cost:

| Strategy | How it works | Use when |
|---|---|---|
| **Rolling update** | Replace pods incrementally, old and new versions serve traffic simultaneously | Default choice; stateless services tolerant of brief version-skew |
| **Blue-green** | Deploy full new environment, cut traffic over at once (e.g., via Service selector or load balancer swap) | Need instant, clean rollback and can afford 2x resource cost during cutover |
| **Canary** | Route a small % of traffic to the new version, expand gradually while watching error rate/latency | High-risk changes, large user base, want automated rollback on regression |

If the user hasn't said which they want, rolling update is the safe default — but flag it if the change sounds risky (schema migration, payment path, auth changes) and canary or blue-green would catch a bad deploy before it hits everyone.

---

## CI/CD Pipeline

Stage order, no skipping:

```
lint → type-check → unit-test → build → integration-test → security-scan → deploy-staging → [approval] → deploy-production
```

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  unit-test:
    needs: lint-and-type-check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  build:
    needs: unit-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t $IMAGE_NAME:${{ github.sha }} .
      - name: Generate SBOM
        run: syft $IMAGE_NAME:${{ github.sha }} -o spdx-json > sbom.json
      - name: Push to registry
        run: docker push $IMAGE_NAME:${{ github.sha }}
      - name: Sign image
        run: cosign sign --yes $IMAGE_NAME:${{ github.sha }}

  security-scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: $IMAGE_NAME:${{ github.sha }}
          severity: 'HIGH,CRITICAL'
          exit-code: '1'

  deploy-staging:
    needs: security-scan
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: kubectl set image deployment/app app=$IMAGE_NAME:${{ github.sha }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production   # requires manual approval, configured in repo settings
    steps:
      - name: Deploy to production
        run: kubectl set image deployment/app app=$IMAGE_NAME:${{ github.sha }}
```

**Rules, with reasoning:**
- Secrets live in the platform's secret store (GitHub Secrets, GitLab CI Variables, Azure Key Vault) — never in YAML. A secret committed once is compromised forever, even if you delete it later, because git history and CI logs persist it.
- Cache dependencies between runs (`node_modules`, pip cache, Docker layers) — this is the single biggest lever on pipeline speed, and slow pipelines get bypassed under pressure.
- Security scanning is mandatory, not optional — Trivy for containers, `npm audit`/`pip audit` for dependencies. SBOM generation (Syft) and image signing (cosign) matter for supply-chain integrity if you distribute images externally or operate under compliance requirements (SOC 2, FedRAMP).
- Production requires manual approval — the one gate that stops "it passed CI so it must be fine" from becoming an incident.
- Every run produces an artifact tagged with the commit SHA — traceability from "what's running in prod" back to "what code that actually is" is what makes incident response fast instead of archaeological.

**GitOps alternative:** instead of the pipeline pushing to the cluster directly (`kubectl set image` above), a GitOps controller (ArgoCD, Flux) watches a Git repo of manifests and reconciles the cluster to match. The pipeline's job becomes "update the manifest repo," not "talk to the cluster." This gives you: the cluster state is always exactly what's in Git (drift is auto-corrected), and rollback is `git revert`. Prefer this pattern when the user already has or wants a dedicated ops/manifest repo, or cares about audit trails on cluster changes.

---

## Infrastructure as Code

Always define infrastructure in code — Terraform or Pulumi — never make manual console changes to production. The reasoning: a console change is invisible to everyone else, has no review step, and leaves no record for the next incident's "what changed recently" question.

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"   # state locking — prevents concurrent applies corrupting state
    encrypt        = true
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false   # one per AZ for production; true is fine for dev to save cost
}
```

- Remote state (S3+DynamoDB for Terraform, or equivalent) with locking — two engineers running `apply` at once without a lock corrupts state.
- Separate state per environment — a bug in a `terraform destroy` against staging should be structurally unable to touch prod's state file.
- Module-ize repeated infrastructure rather than copy-pasting between environments; drift between "what dev has" and "what prod has" is a recurring source of "works on staging, breaks in prod."

**Key services by cloud:**

| Concern | AWS | Azure | GCP |
|---|---|---|---|
| Container orchestration | EKS / ECS Fargate | AKS | GKE |
| Serverless | Lambda | Azure Functions | Cloud Run |
| Managed DB | RDS / Aurora | Azure SQL | Cloud SQL |
| Cache | ElastiCache | Azure Cache for Redis | Memorystore |
| Object storage | S3 | Blob Storage | Cloud Storage |
| CDN | CloudFront | Azure CDN | Cloud CDN |
| Secrets | Secrets Manager | Key Vault | Secret Manager |
| Message queue | SQS / SNS | Service Bus | Pub/Sub |
| IaC state backend | S3 + DynamoDB | Azure Storage + blob lease | GCS + Cloud Storage lock |
| AI/ML | Bedrock | Azure OpenAI | Vertex AI |

---

## DNS & Certificate Management

DNS and TLS are the two things that are invisible when they work and catastrophic when they don't. Both need to be versioned, monitored, and automated — not manually touched in a console at 2am.

### DNS

**Rules:**
- All DNS records are defined in code (Terraform `aws_route53_record`, `google_dns_record_set`, Cloudflare Terraform provider). Manual console edits to production DNS records are the same class of mistake as manual production database edits — they happen once, they work, and then nobody can explain what broke six months later.
- **TTL strategy:** Use low TTLs (60–300s) before a planned migration or cutover. Use high TTLs (300–3600s) in steady state to reduce resolver load and improve cache hit rate. Change the TTL down 24 hours before you need it to propagate, not the day of.
- **Never delete a record until you've verified nothing depends on it.** DNS propagation means some clients are still using a record long after you think you've removed it. Audit → reduce TTL → verify no traffic → delete.

**Common DNS operations:**

```bash
# Verify DNS resolution from multiple resolvers
dig api.yourapp.com @8.8.8.8       # Google
dig api.yourapp.com @1.1.1.1       # Cloudflare
dig api.yourapp.com @208.67.222.222 # OpenDNS

# Check propagation globally
# Use: https://dnschecker.org — paste record, check worldwide

# Check what's currently resolving (including cached TTL remaining)
dig +ttl api.yourapp.com

# Trace the full DNS resolution chain
dig +trace api.yourapp.com

# Check all records for a domain
dig api.yourapp.com ANY

# Verify a CNAME points to the right target
dig CNAME api.yourapp.com

# Reverse lookup (IP → hostname)
dig -x 203.0.113.10

# Check nameservers
dig NS yourapp.com

# Test from inside a Kubernetes cluster
kubectl run dns-test --image=busybox:1.36 --rm -it --restart=Never \
  -- nslookup kubernetes.default.svc.cluster.local
```

**Terraform DNS example (AWS Route53):**

```hcl
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "A"
  ttl     = 300

  alias {
    name                   = aws_lb.api.dns_name
    zone_id                = aws_lb.api.zone_id
    evaluate_target_health = true  # Route53 health checks; don't serve if target unhealthy
  }
}

# Blue/green DNS switch — swap alias target in Terraform
# Low TTL before switching, verify propagation, then raise TTL again
```

**DNS health checks and failover:**
```hcl
# Route53 health check + failover routing
resource "aws_route53_health_check" "primary" {
  fqdn              = "api-primary.${var.domain}"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "api_primary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.${var.domain}"
  type           = "A"
  set_identifier = "primary"
  failover_routing_policy { type = "PRIMARY" }
  health_check_id = aws_route53_health_check.primary.id
  alias { ... }
}

resource "aws_route53_record" "api_secondary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.${var.domain}"
  type           = "A"
  set_identifier = "secondary"
  failover_routing_policy { type = "SECONDARY" }
  alias { ... }  # DR region or static error page
}
```

---

### TLS Certificate Management

**Rules:**
- All production TLS certificates are managed by automation — never manually renewed. A manually renewed certificate will expire. It is only a question of when.
- Use **cert-manager** in Kubernetes or **AWS ACM / Let's Encrypt** for cloud load balancers. Zero-touch renewal is the only acceptable standard.
- Certificate expiry monitoring is mandatory — even with automation. Automation fails silently. Alert when a cert is < 30 days from expiry, page when it's < 7 days.
- **Wildcard certificates** reduce certificate sprawl for multi-subdomain setups but require DNS-01 ACME challenge (not HTTP-01). Know which challenge your ACME provider supports.

**cert-manager in Kubernetes:**

```yaml
# ClusterIssuer — Let's Encrypt production
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@yourcompany.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            class: nginx
      # For wildcard certs — DNS-01 challenge via Route53
      - dns01:
          route53:
            region: us-east-1
            hostedZoneID: ZXXXXXXXXXXXXX
---
# Certificate — auto-renewed by cert-manager
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls
  namespace: production
spec:
  secretName: api-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - api.yourapp.com
    - "*.api.yourapp.com"   # wildcard — requires DNS-01
  renewBefore: 360h          # renew 15 days before expiry
```

**Certificate diagnostics:**

```bash
# Check cert expiry (remote)
echo | openssl s_client -connect api.yourapp.com:443 -servername api.yourapp.com 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Check expiry as days remaining
echo | openssl s_client -connect api.yourapp.com:443 2>/dev/null \
  | openssl x509 -noout -enddate \
  | awk -F= '{print $2}' \
  | xargs -I{} date -d "{}" +%s \
  | xargs -I{} sh -c 'echo "$(( ({} - $(date +%s)) / 86400 )) days remaining"'

# Inspect cert chain (verify intermediate certs are included)
openssl s_client -connect api.yourapp.com:443 -showcerts 2>/dev/null \
  | grep -E "^(subject|issuer|notAfter)"

# Check cert SANs (Subject Alternative Names)
openssl s_client -connect api.yourapp.com:443 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName

# Verify local cert file
openssl x509 -in cert.pem -text -noout | grep -A2 "Validity\|Subject\|SAN"

# Test TLS handshake and protocol version
openssl s_client -connect api.yourapp.com:443 -tls1_2   # verify TLS 1.2 works
openssl s_client -connect api.yourapp.com:443 -tls1_3   # verify TLS 1.3 works

# Check cert-manager certificate status in Kubernetes
kubectl get certificate -n production
kubectl describe certificate api-tls -n production
kubectl get certificaterequest -n production   # pending renewals
kubectl get order -n production                # ACME order status
kubectl get challenge -n production            # ACME challenge status

# If cert-manager is stuck — check logs
kubectl logs -n cert-manager deployment/cert-manager --tail=100 | grep -i "error\|warn"
```

**Certificate expiry alert (Prometheus rule):**

```yaml
# Alert when cert < 30 days from expiry — warning
# Alert when cert < 7 days from expiry — critical / page
groups:
  - name: tls-certificates
    rules:
      - alert: CertificateExpiringSoon
        expr: |
          (certmanager_certificate_expiration_timestamp_seconds - time()) / 86400 < 30
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Certificate expiring in {{ $value | humanize }} days"
          description: "{{ $labels.name }} in {{ $labels.namespace }} expires soon. Check cert-manager."

      - alert: CertificateExpiringCritical
        expr: |
          (certmanager_certificate_expiration_timestamp_seconds - time()) / 86400 < 7
        for: 15m
        labels:
          severity: critical
        annotations:
          summary: "CRITICAL: Certificate expires in {{ $value | humanize }} days"
          description: "{{ $labels.name }} in {{ $labels.namespace }}. Immediate action required."
```

---

## Monitoring & Observability

**Three pillars — all three, not one:**

- **Logs** — structured JSON, correlation IDs threaded through every request, shipped to a central aggregator (Elasticsearch, CloudWatch, Datadog). Unstructured logs are searchable by luck, not by design.
- **Metrics** — Prometheus scraping + Grafana dashboards; alert on SLO burn rate, not raw thresholds (see below for why).
- **Traces** — OpenTelemetry instrumentation across service boundaries. In a multi-service system, logs alone can't answer "which of these 6 services added the latency."

**Alert design:**
- Alert on symptoms, not causes — "5xx rate > 1% for 5 minutes," not "CPU > 80%." High CPU might be fine; a symptom-based alert only fires when something the user actually feels is happening.
- Every alert links to a runbook. An alert with no next step just adds 3am stress without adding 3am capability.
- Alert fatigue is a real failure mode — engineers start ignoring pages after enough false ones, and then they ignore the real one too. Fewer, higher-signal alerts beat comprehensive-but-noisy ones. Page for what needs a human right now; log everything else.

**Baseline dashboards:**
- Request rate, error rate, latency (p50/p95/p99) per service
- Deployment markers overlaid on the error-rate graph — the fastest way to confirm or rule out "did the last deploy cause this"
- Queue depth per queue
- DB connection pool utilization and slow-query count
- Infra: CPU, memory, disk per node

---

### Drill-Down Trace Investigation — Finding the Root Cause

When an alert fires, the goal is not to silence the alert. The goal is to find the exact line of code, the exact query, or the exact dependency that caused the failure — and prove it. This is the methodology.

**The investigation ladder — always start at the top, work down:**

```
Alert fires
    ↓
1. Symptom layer    — What does the user experience? What metric is breaching?
    ↓
2. Service layer    — Which service is the entry point of the failure?
    ↓
3. Trace layer      — Which span in the distributed trace is slow or erroring?
    ↓
4. Log layer        — What does the log at that span say? What is the correlation ID?
    ↓
5. Code layer       — Which function, query, or external call produced the error?
    ↓
6. Root cause       — Why did that function/query/call fail? State it in one sentence.
```

Never skip a layer. Jumping from "5xx spike" to "must be the database" without the trace is guessing. Guessing produces wrong fixes that create new incidents.

---

#### Step 1: Establish the Symptom Scope

```promql
# Error rate spike — which service?
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)

# Latency spike — which service? which percentile?
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)

# When did it start? (overlay with deployment markers)
# In Grafana: Annotations → add deploy events → overlay on error rate graph
```

**First question to answer:** Is this one service or multiple? A single-service spike points to that service's code or its direct dependencies. A simultaneous multi-service spike points to a shared dependency (database, cache, DNS, a downstream API) or infrastructure (network, load balancer, cert expiry).

---

#### Step 2: Find the Failing Trace

```bash
# In Jaeger UI — filter by:
# Service: api-service
# Operation: POST /api/orders
# Tags: error=true
# Time range: the spike window
# Sort: by duration descending — slowest traces first

# In Tempo (Grafana) — TraceQL query:
{ status=error && span.http.route="/api/orders" }
| select(duration, rootName, rootServiceName)
| sort(duration desc)

# In Datadog APM:
# Traces → Filter: status:error service:api-service
# Group by: resource name → find which endpoint has the error spike
```

Open the trace with the highest duration or the first error in the spike window. Expand every span.

---

#### Step 3: Read the Trace — Find the Broken Span

A distributed trace is a waterfall of spans. Each span is one unit of work across one service. Read it like a stack trace.

```
Trace: POST /api/orders  duration: 4,821ms  status: ERROR
│
├── api-service: validate_order              12ms   ✅
├── api-service: check_inventory            8ms    ✅
├── api-service: call_payment_service  →    4,790ms ❌  ERROR
│   │
│   └── payment-service: process_charge     4,788ms ❌  ERROR
│       │
│       ├── payment-service: db_begin_txn   3ms    ✅
│       ├── payment-service: stripe_charge  4,782ms ❌  ERROR
│       │   └── [external: api.stripe.com]  timeout after 4,500ms
│       └── payment-service: db_rollback    3ms    ✅
│
└── api-service: emit_order_event           [never reached]
```

**Reading the trace:**
- The 4,821ms is almost entirely inside `stripe_charge` — 4,782ms
- `stripe_charge` timed out at 4,500ms waiting for `api.stripe.com`
- The root cause is not in our code — it is an external Stripe API timeout
- The fix is: implement a circuit breaker on the Stripe client with a fallback queue

**What each span field tells you:**
| Field | What to look for |
|---|---|
| `duration` | Spans that account for >80% of total request time |
| `status` | The first `ERROR` span in the chain — everything above it is a consequence |
| `tags/attributes` | `db.statement` (the actual SQL), `http.url` (the external call), `error.message` |
| `logs/events` | Exception stack traces attached to the span at the moment of failure |

---

#### Step 4: Drill from Trace to Logs

Every span in a properly instrumented system carries a `trace_id` and `span_id`. Use these to pull the exact logs from that span.

```bash
# From the broken span, copy the trace_id (e.g., 4bf92f3577b34da6a3ce929d0e0e4736)

# Elasticsearch / OpenSearch
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736" } },
        { "term": { "span_id": "a3ce929d0e0e4736" } }
      ]
    }
  },
  "sort": [{ "@timestamp": "asc" }]
}

# Loki (Grafana) — LogQL
{service="payment-service"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"

# CloudWatch Insights
fields @timestamp, @message, level, error
| filter trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"
| sort @timestamp asc

# Datadog
service:payment-service trace_id:4bf92f3577b34da6a3ce929d0e0e4736
```

**What to look for in the logs:**
- The exact error message at the moment of failure (not just "error occurred")
- The full exception stack trace — the innermost frame is usually the root cause
- Any retry attempts logged before the final failure
- Any config or connection detail that changed (connection pool exhausted? wrong endpoint?)
- Timestamps — did the error appear instantly (configuration) or after a delay (timeout)?

---

#### Step 5: Isolate the Root Cause — Five Whys on the Trace

Run the Five Whys directly on the trace + log evidence:

```
Why did POST /api/orders return 500?
→ Because the payment service returned an error after 4.8s

Why did the payment service error?
→ Because the Stripe API call timed out at 4,500ms

Why did the Stripe API call timeout?
→ Logs show "connection timeout to api.stripe.com after 4500ms"

Why did the connection to Stripe timeout?
→ Check: is this affecting all calls to Stripe or just some?
  → Metrics: stripe_api_latency_p99 spiked from 200ms to 5,000ms at 14:32 UTC
  → External: Stripe status page (status.stripe.com) shows "Elevated Errors" on Charges API since 14:30 UTC

Root cause: Stripe infrastructure incident. Our code has no bug.
  → Immediate: implement circuit breaker with exponential backoff + retry queue
  → Long-term: async payment processing with webhook confirmation (not synchronous)
```

**Root cause must be stated as:** `"[Component X] failed because [specific condition Y] which was caused by [underlying reason Z]."`

If you cannot state it this specifically, you do not have the root cause — you have a hypothesis. Keep drilling.

---

#### Step 6: Confirm with Metrics Correlation

Before closing the investigation, confirm the root cause with metric evidence:

```promql
# Confirm: did the external dependency's latency spike at the same time as our errors?
histogram_quantile(0.99,
  rate(http_client_request_duration_seconds_bucket{
    target_service="stripe"
  }[1m])
)

# Confirm: did our connection pool exhaust? (if DB root cause suspected)
db_connection_pool_available{service="payment-service"} == 0

# Confirm: did a deploy happen? (overlay deployment events)
# → check CI/CD system for deploys in the 30 min before the spike

# Confirm: did DNS change? (if DNS root cause suspected)
# → check Route53 / Cloudflare change logs for the domain
# → dig api.stripe.com — compare current vs. cached results
```

---

#### Common Root Cause Patterns and Their Trace Signatures

| Symptom in trace | Likely root cause | Where to look |
|---|---|---|
| One deep span holds 95%+ of latency | Slow DB query or external API | `db.statement` tag on that span, slow query log |
| Span fails immediately (< 5ms error) | Config error, auth failure, connection refused | Error message in span tags, `errno` in logs |
| Multiple spans fail simultaneously | Shared dependency (DB, cache, DNS) or network | Check infra metrics at the same timestamp |
| Latency grows gradually over time | Memory leak, connection pool exhaustion, disk fill | Process memory metrics, pool utilization |
| Error only on certain user IDs | Data-specific bug, permissions issue | Filter trace by `user_id` tag, check input values |
| Error only after deploy | Regression | Diff the deploy; check feature flags |
| Error correlates with high traffic | Missing rate limiting, resource saturation | Compare error rate vs. request rate graphs |
| Retries visible in trace before final error | Transient failure — timeout or rate limit | Check retry count on span, upstream rate limit headers |

---

#### OpenTelemetry Instrumentation (to make traces work)

Traces only work if the code is instrumented. Minimum required instrumentation:

```typescript
// Node.js — auto-instrumentation (covers HTTP, DB, Redis automatically)
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,  // Jaeger / Tempo / Datadog OTLP
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: process.env.SERVICE_NAME,           // must match across all services
});
sdk.start();
```

```python
# Python — auto-instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument()     # auto-traces all HTTP routes
SQLAlchemyInstrumentor.instrument()  # auto-traces all DB queries — captures db.statement
```

**Critical: propagate trace context across service calls**

```typescript
// The trace_id must be forwarded when calling downstream services
// OpenTelemetry auto-instrumentation handles this automatically for HTTP clients
// If using a custom HTTP client, manually propagate:

import { propagation, context } from "@opentelemetry/api";

const headers: Record<string, string> = {};
propagation.inject(context.active(), headers);
// headers now contains traceparent and tracestate — forward these to the downstream call
await fetch("http://payment-service/charge", { headers });
```

Without context propagation, the trace breaks at service boundaries — each service shows a disconnected trace, and you lose the end-to-end view that makes root cause analysis possible.

---

## Bundled Reference

Read [deployment-safety.md](./references/deployment-safety.md) when choosing rollout, rollback, and verification controls for a production change.

## Definition of Done — Platform Work

**Container & Orchestration**
- [ ] Dockerfile is multi-stage, non-root, pinned base image, has a `HEALTHCHECK`
- [ ] docker-compose covers all local dev dependencies with health checks and correct `depends_on` conditions
- [ ] Kubernetes manifests have resource requests/limits, both probes, `PodDisruptionBudget`, and a considered `NetworkPolicy`
- [ ] Deployment strategy (rolling/blue-green/canary) matches the actual risk of the change, not just the default

**CI/CD & Infrastructure**
- [ ] CI/CD covers: lint → test → build → scan → staging → approval → production, with SHA-traceable artifacts
- [ ] Secrets live in a secret store, never in YAML or a committed `.env`
- [ ] Infrastructure is defined in Terraform/Pulumi with remote, locked state — no manual console changes
- [ ] Rollback procedure is written down and has actually been tested, not just assumed to work

**DNS & Certificates**
- [ ] All DNS records defined in Terraform/IaC — no manual console edits to production DNS
- [ ] TTL set appropriately: low (60–300s) before migrations, high (300–3600s) in steady state
- [ ] TLS certificates managed by automation (cert-manager, ACM) — zero manual renewals
- [ ] Certificate expiry alerts configured: warning at < 30 days, critical/page at < 7 days
- [ ] DNS resolution verified from multiple resolvers (`dig @8.8.8.8`, `@1.1.1.1`)
- [ ] TLS handshake verified with `openssl s_client` — correct cert, correct chain, no expiry within 30 days

**Monitoring, Observability & Root Cause**
- [ ] Structured JSON logs with `trace_id` and `correlation_id` on every log line
- [ ] Metrics configured: request rate, error rate, latency (p50/p95/p99) per service
- [ ] Distributed tracing instrumented with OpenTelemetry — trace context propagated across all service calls
- [ ] Traces queryable in Jaeger / Tempo / Datadog APM — can find a trace by `trace_id` within 30 seconds
- [ ] Alerts fire on symptoms (5xx rate, latency SLO breach) — not on causes (CPU, memory)
- [ ] Every alert links to a runbook that includes the trace drill-down investigation steps
- [ ] Deployment markers overlaid on error-rate dashboards — "did the last deploy cause this?" answerable in < 60 seconds
- [ ] Root cause investigation ladder defined: alert → symptom → service → trace → log → code → root cause
- [ ] Common root cause patterns documented for this service (slow query, connection pool, external dependency timeouts)
