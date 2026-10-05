---
name: platform-engineer
description: Platform engineering expertise for building internal developer platforms and self-service infrastructure. Use when designing developer portals, creating.
---

# Platform Engineer

Specialized expertise in platform engineering, covering internal developer platforms, self-service infrastructure, standardized pipelines, developer experience metrics, service mesh networking, secrets management, and platform governance. This skill provides production-ready patterns for teams building platforms that treat infrastructure as a product.

## When to Use This Skill

Use this skill for:

- Designing internal developer platforms (IDPs) and developer portals
- Creating golden paths and paved roads for development teams
- Building self-service infrastructure provisioning workflows
- Standardizing CI/CD pipelines across an organization
- Measuring and improving developer experience (DevEx)
- Implementing service mesh and internal networking patterns
- Managing secrets, configuration, and environment promotion
- Enforcing platform governance through policy-as-code

**Trigger phrases**: "platform engineering", "internal developer platform", "golden path", "self-service infrastructure", "developer portal", "Backstage", "platform team", "paved road", "developer experience", "DORA metrics", "service catalog", "policy-as-code"

## What This Skill Does

Provides production-ready platform engineering patterns including:

- **IDP Design**: Platform team topology, service catalogs, Backstage/Port configuration
- **Self-Service Infra**: Terraform modules as products, Crossplane compositions, portal-driven provisioning
- **Pipeline Standards**: Template CI/CD pipelines, shared actions/templates, progressive rollout strategies
- **DevEx Metrics**: DORA measurement, cognitive load assessment, adoption tracking
- **Service Mesh**: Traffic management, mutual TLS, service discovery, API gateway integration
- **Secrets Management**: Vault integration, external-secrets-operator, sealed secrets, config promotion
- **Governance**: OPA/Kyverno policies, cost tagging, resource quotas, compliance automation

## Instructions

### Step 1: Design the Internal Developer Platform

An internal developer platform (IDP) is a self-service layer that abstracts away infrastructure complexity and provides development teams with golden paths for common workflows. The platform team operates as a product team, treating developers as customers and iterating on the platform based on feedback and usage data.

**Platform Team Topology**:

| Role | Responsibility |
|------|---------------|
| **Platform Product Manager** | Roadmap, developer interviews, prioritization |
| **Platform Engineer** | Core platform services, APIs, automation |
| **Developer Advocate** | Documentation, onboarding, feedback loops |
| **SRE/Reliability** | Platform SLOs, incident response, capacity |
| **Security Champion** | Policy authoring, compliance, threat modeling |

**Golden Path Principles**:

- A golden path is an opinionated, supported, and well-documented way to accomplish a common task (deploying a service, provisioning a database, setting up monitoring)
- Golden paths are recommendations, not mandates. Teams can deviate when they have a valid reason, but the golden path should cover 80% of use cases
- Every golden path includes: a template or scaffold, automated validation, documentation, and an owner who maintains it
- Measure golden path adoption to understand where the platform delivers value and where gaps exist

**Backstage Service Catalog Configuration**:

```yaml
# catalog-info.yaml - Backstage entity descriptor
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Handles payment processing and billing
  annotations:
    backstage.io/techdocs-ref: dir:.
    github.com/project-slug: myorg/payment-service
    pagerduty.com/service-id: P1234ABC
    grafana/dashboard-selector: "payment-service"
    sonarqube.org/project-key: myorg_payment-service
  tags:
    - python
    - grpc
    - tier-1
  links:
    - url: https://grafana.internal/d/payment-svc
      title: Grafana Dashboard
    - url: https://runbooks.internal/payment-service
      title: Runbook
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: billing-platform
  dependsOn:
    - component:default/user-service
    - resource:default/payments-db
  providesApis:
    - payment-api
  consumesApis:
    - user-api
    - notification-api
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: payment-api
  description: Payment processing API
spec:
  type: grpc
  lifecycle: production
  owner: team-payments
  system: billing-platform
  definition:
    $text: ./proto/payment.proto
```

**Backstage Software Template for New Services**:

```yaml
# template.yaml - Backstage scaffolder template
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: create-microservice
  title: Create a New Microservice
  description: Scaffolds a production-ready microservice with CI/CD, monitoring, and docs
  tags:
    - recommended
    - golden-path
spec:
  owner: team-platform
  type: service
  parameters:
    - title: Service Details
      required:
        - name
        - owner
        - language
      properties:
        name:
          title: Service Name
          type: string
          pattern: "^[a-z][a-z0-9-]*$"
          ui:autofocus: true
        owner:
          title: Owning Team
          type: string
          ui:field: OwnerPicker
          ui:options:
            allowedKinds: [Group]
        language:
          title: Language
          type: string
          enum: [go, python, typescript]
          default: go
        description:
          title: Description
          type: string
    - title: Infrastructure
      properties:
        database:
          title: Database
          type: string
          enum: [none, postgresql, redis, both]
          default: none
        exposePublicly:
          title: Expose via public API gateway
          type: boolean
          default: false
  steps:
    - id: fetch-template
      name: Fetch service template
      action: fetch:template
      input:
        url: ./skeleton/${{ parameters.language }}
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          description: ${{ parameters.description }}
          database: ${{ parameters.database }}
    - id: create-repo
      name: Create GitHub repository
      action: publish:github
      input:
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}
        defaultBranch: main
        protectDefaultBranch: true
        requireCodeOwnerReviews: true
    - id: register-catalog
      name: Register in Backstage catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['create-repo'].output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml
  output:
    links:
      - title: Repository
        url: ${{ steps['create-repo'].output.remoteUrl }}
      - title: Service in Catalog
        icon: catalog
        entityRef: ${{ steps['register-catalog'].output.entityRef }}
```

**Platform as a Product Mindset**:

- Conduct regular developer interviews and surveys to understand pain points
- Maintain a public platform roadmap visible to all engineering teams
- Track Net Promoter Score (NPS) for the platform quarterly
- Publish a platform changelog and announce new capabilities proactively
- Treat breaking changes with the same rigor as public API changes (deprecation notices, migration guides, support windows)

### Step 2: Build Self-Service Infrastructure

Self-service infrastructure enables developers to provision resources without filing tickets or waiting for a platform team member. The key is packaging infrastructure modules as reusable, versioned products with clear interfaces, sensible defaults, and built-in compliance.

**Terraform Module as a Product**:

```hcl
# modules/rds-postgresql/main.tf
# A self-service PostgreSQL module with opinionated defaults

variable "name" {
  description = "Database instance name"
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,28}$", var.name))
    error_message = "Name must be lowercase alphanumeric with hyphens, 3-29 characters."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "size" {
  description = "T-shirt size for the database (small, medium, large)"
  type        = string
  default     = "small"
  validation {
    condition     = contains(["small", "medium", "large"], var.size)
    error_message = "Size must be small, medium, or large."
  }
}

locals {
  instance_class = {
    small  = "db.t4g.medium"
    medium = "db.r6g.large"
    large  = "db.r6g.2xlarge"
  }
  storage_gb = {
    small  = 50
    medium = 200
    large  = 1000
  }
  # Enforce cost tags and compliance automatically
  required_tags = {
    ManagedBy   = "platform-team"
    Environment = var.environment
    Service     = var.name
    CostCenter  = var.cost_center
    Provisioner = "self-service-terraform"
  }
}

resource "aws_db_instance" "main" {
  identifier     = "${var.name}-${var.environment}"
  engine         = "postgres"
  engine_version = "16.2"
  instance_class = local.instance_class[var.size]

  allocated_storage     = local.storage_gb[var.size]
  max_allocated_storage = local.storage_gb[var.size] * 2
  storage_encrypted     = true
  kms_key_id            = var.kms_key_arn

  multi_az               = var.environment == "production" ? true : false
  backup_retention_period = var.environment == "production" ? 30 : 7
  deletion_protection     = var.environment == "production" ? true : false

  db_subnet_group_name   = var.subnet_group_name
  vpc_security_group_ids = [aws_security_group.db.id]

  performance_insights_enabled = true
  monitoring_interval          = 60
  monitoring_role_arn          = var.monitoring_role_arn

  tags = local.required_tags
}

output "connection_string_secret_arn" {
  description = "ARN of the Secrets Manager secret containing the connection string"
  value       = aws_secretsmanager_secret.connection.arn
}

output "endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
}
```

**Crossplane Composition for Self-Service**:

```yaml
# crossplane/composition-postgresql.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: postgresql.databases.platform.example.com
  labels:
    provider: aws
spec:
  compositeTypeRef:
    apiVersion: databases.platform.example.com/v1alpha1
    kind: PostgreSQLInstance
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBInstance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "16"
            storageEncrypted: true
            publiclyAccessible: false
            performanceInsightsEnabled: true
          providerConfigRef:
            name: aws-provider
      patches:
        - fromFieldPath: spec.parameters.size
          toFieldPath: spec.forProvider.dbInstanceClass
          transforms:
            - type: map
              map:
                small: db.t4g.medium
                medium: db.r6g.large
                large: db.r6g.2xlarge
        - fromFieldPath: spec.parameters.environment
          toFieldPath: spec.forProvider.multiAZ
          transforms:
            - type: map
              map:
                dev: "false"
                staging: "false"
                production: "true"
    - name: connection-secret
      base:
        apiVersion: kubernetes.crossplane.io/v1alpha1
        kind: Object
        spec:
          forProvider:
            manifest:
              apiVersion: v1
              kind: Secret
              metadata:
                namespace: default
---
# Developer-facing claim (simple interface)
apiVersion: databases.platform.example.com/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: orders-db
  namespace: team-orders
spec:
  parameters:
    size: medium
    environment: production
  compositionSelector:
    matchLabels:
      provider: aws
```

**PR-Based Self-Service Workflow**:

```
Developer creates PR          Platform CI validates         Merge triggers provisioning
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  infra-requests/  │         │  Terraform plan  │         │  Terraform apply │
│  orders-db.yaml  │────────►│  Policy check    │────────►│  Register in     │
│                  │         │  Cost estimate   │         │  service catalog │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

A PR-based workflow lets developers request infrastructure by committing a YAML or HCL file to a designated repository. Automated checks run `terraform plan`, validate against policies, estimate costs, and require platform team approval only when thresholds are exceeded.

### Step 3: Standardize Deployment Pipelines

Shared pipeline templates reduce duplication, enforce organizational standards, and give every team a reliable deployment experience without reinventing CI/CD from scratch. The platform team owns and versions these templates.

**Shared GitHub Actions Reusable Workflow**:

```yaml
# .github/workflows/deploy-service.yml (in the shared workflows repo)
name: Deploy Service
on:
  workflow_call:
    inputs:
      service-name:
        required: true
        type: string
      environment:
        required: true
        type: string
        description: "Target environment (dev, staging, production)"
      image-tag:
        required: true
        type: string
      deployment-strategy:
        required: false
        type: string
        default: "rolling"
        description: "rolling, blue-green, or canary"
    secrets:
      KUBE_CONFIG:
        required: true
      SLACK_WEBHOOK:
        required: false

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Kubernetes manifests
        run: |
          kubectl kustomize deploy/overlays/${{ inputs.environment }} | \
            kubeval --strict --kubernetes-version 1.29.0
      - name: Policy check with OPA
        uses: open-policy-agent/opa-github-action@v2
        with:
          input: deploy/overlays/${{ inputs.environment }}
          policy: policies/

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Rolling deployment
        if: inputs.deployment-strategy == 'rolling'
        run: |
          kubectl set image deployment/${{ inputs.service-name }} \
            app=${{ inputs.image-tag }} \
            --namespace=${{ inputs.service-name }}
          kubectl rollout status deployment/${{ inputs.service-name }} \
            --namespace=${{ inputs.service-name }} \
            --timeout=300s

      - name: Canary deployment
        if: inputs.deployment-strategy == 'canary'
        run: |
          # Deploy canary with 10% traffic
          kubectl apply -f - <<EOF
          apiVersion: flagger.app/v1beta1
          kind: Canary
          metadata:
            name: ${{ inputs.service-name }}
            namespace: ${{ inputs.service-name }}
          spec:
            targetRef:
              apiVersion: apps/v1
              kind: Deployment
              name: ${{ inputs.service-name }}
            progressDeadlineSeconds: 600
            analysis:
              interval: 60s
              threshold: 5
              maxWeight: 50
              stepWeight: 10
              metrics:
                - name: request-success-rate
                  thresholdRange:
                    min: 99
                  interval: 60s
                - name: request-duration
                  thresholdRange:
                    max: 500
                  interval: 60s
          EOF

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deploy ${{ inputs.service-name }} to ${{ inputs.environment }}: ${{ job.status }}"
            }
```

**Consuming the Shared Workflow (in a service repo)**:

```yaml
# .github/workflows/deploy.yml (in each service repo)
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.build.outputs.tag }}
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        id: build
        run: |
          TAG="${GITHUB_SHA::8}"
          docker build -t myregistry/${{ github.event.repository.name }}:${TAG} .
          docker push myregistry/${{ github.event.repository.name }}:${TAG}
          echo "tag=myregistry/${{ github.event.repository.name }}:${TAG}" >> "$GITHUB_OUTPUT"

  deploy-staging:
    needs: build
    uses: myorg/platform-workflows/.github/workflows/deploy-service.yml@v2
    with:
      service-name: ${{ github.event.repository.name }}
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
      deployment-strategy: rolling
    secrets:
      KUBE_CONFIG: ${{ secrets.STAGING_KUBE_CONFIG }}
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    needs: deploy-staging
    uses: myorg/platform-workflows/.github/workflows/deploy-service.yml@v2
    with:
      service-name: ${{ github.event.repository.name }}
      environment: production
      image-tag: ${{ needs.build.outputs.image-tag }}
      deployment-strategy: canary
    secrets:
      KUBE_CONFIG: ${{ secrets.PROD_KUBE_CONFIG }}
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

**Deployment Strategy Comparison**:

| Strategy | Risk | Rollback Speed | Complexity | Best For |
|----------|------|---------------|------------|----------|
| **Rolling** | Medium | Minutes | Low | Stateless services, non-critical |
| **Blue-Green** | Low | Seconds | Medium | Stateful services, zero-downtime |
| **Canary** | Lowest | Seconds | High | High-traffic, user-facing services |
| **Recreate** | High | Minutes | Lowest | Dev/test, batch workloads |

### Step 4: Measure Developer Experience

Platform engineering succeeds only when it measurably improves developer productivity and satisfaction. DORA metrics provide a baseline, but a complete picture requires supplementing them with qualitative signals like cognitive load and developer satisfaction.

**DORA Metrics Dashboard Configuration (Prometheus + Grafana)**:

```yaml
# prometheus-rules/dora-metrics.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: dora-metrics
  namespace: monitoring
spec:
  groups:
    - name: dora.deployment_frequency
      interval: 1h
      rules:
        - record: dora:deployment_frequency:rate7d
          expr: |
            sum(
              increase(deployment_total{environment="production"}[7d])
            ) by (team)
        - record: dora:deployment_frequency:daily
          expr: |
            sum(
              increase(deployment_total{environment="production"}[1d])
            ) by (team)

    - name: dora.lead_time
      interval: 1h
      rules:
        - record: dora:lead_time_seconds:p50
          expr: |
            histogram_quantile(0.5,
              sum(rate(lead_time_seconds_bucket{environment="production"}[7d])) by (le, team)
            )
        - record: dora:lead_time_seconds:p95
          expr: |
            histogram_quantile(0.95,
              sum(rate(lead_time_seconds_bucket{environment="production"}[7d])) by (le, team)
            )

    - name: dora.change_failure_rate
      interval: 1h
      rules:
        - record: dora:change_failure_rate:ratio7d
          expr: |
            sum(increase(deployment_rollback_total{environment="production"}[7d])) by (team)
            /
            sum(increase(deployment_total{environment="production"}[7d])) by (team)

    - name: dora.mttr
      interval: 1h
      rules:
        - record: dora:mttr_seconds:avg7d
          expr: |
            avg(incident_resolution_seconds{severity=~"sev1|sev2"}) by (team)
```

**DORA Maturity Levels**:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | On-demand (multiple/day) | Weekly-daily | Monthly-weekly | Monthly+ |
| **Lead Time for Changes** | < 1 hour | 1 day - 1 week | 1 week - 1 month | 1 month+ |
| **Change Failure Rate** | < 5% | 5-10% | 10-15% | 15%+ |
| **MTTR** | < 1 hour | < 1 day | < 1 week | 1 week+ |

**Developer Experience Survey Template**:

Track these dimensions quarterly to complement quantitative metrics:

- **Flow state**: "How often do you get into a state of deep focus during your workday?" (1-5 scale)
- **Feedback loops**: "How quickly can you see the result of a code change in a staging environment?" (minutes/hours/days)
- **Cognitive load**: "How much mental effort is required to deploy a change to production?" (1-5 scale)
- **Tool satisfaction**: "Rate your satisfaction with the following platform capabilities" (CI/CD, monitoring, provisioning, docs)
- **Toil assessment**: "What percentage of your time is spent on repetitive manual tasks?" (0-100%)
- **Golden path adoption**: "Do you use the platform-provided templates for new services?" (always/sometimes/never)

**Platform Adoption Tracking**:

```sql
-- Track golden path adoption over time
SELECT
  date_trunc('month', created_at) AS month,
  COUNT(*) FILTER (WHERE scaffold_template IS NOT NULL) AS golden_path_repos,
  COUNT(*) FILTER (WHERE scaffold_template IS NULL) AS custom_repos,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE scaffold_template IS NOT NULL)
    / COUNT(*), 1
  ) AS adoption_pct
FROM repositories
WHERE created_at >= NOW() - INTERVAL '12 months'
GROUP BY 1
ORDER BY 1;

-- Measure time-to-first-deploy for new services
SELECT
  scaffold_template,
  PERCENTILE_CONT(0.5) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM first_deploy_at - created_at) / 3600
  ) AS median_hours_to_first_deploy
FROM repositories
WHERE first_deploy_at IS NOT NULL
GROUP BY scaffold_template;
```

### Step 5: Implement Service Mesh and Networking

A service mesh provides a uniform layer for service-to-service communication, handling traffic management, security (mutual TLS), and observability without requiring application code changes. The platform team configures and operates the mesh so development teams get these capabilities for free.

**Istio Service Mesh Configuration**:

```yaml
# istio/peer-authentication.yaml
# Enforce mutual TLS across the mesh
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
# istio/virtual-service.yaml
# Traffic management with canary routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
  namespace: payments
spec:
  hosts:
    - payment-service
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: payment-service
            subset: canary
          weight: 100
    - route:
        - destination:
            host: payment-service
            subset: stable
          weight: 95
        - destination:
            host: payment-service
            subset: canary
          weight: 5
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
  namespace: payments
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
  subsets:
    - name: stable
      labels:
        version: stable
    - name: canary
      labels:
        version: canary
```

**API Gateway Pattern with Ingress**:

```yaml
# gateway/ingress-gateway.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: platform-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: platform-tls-cert
      hosts:
        - "api.example.com"
        - "*.internal.example.com"
---
# Rate limiting configuration
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit
  namespace: istio-system
spec:
  workloadSelector:
    labels:
      istio: ingressgateway
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: GATEWAY
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 1000
                tokens_per_fill: 100
                fill_interval: 1s
```

**Service Discovery Pattern**:

```
                    ┌──────────────────────────────────┐
                    │        Platform Gateway           │
                    │   (TLS termination, rate limit)   │
                    └───────────────┬──────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
     ┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
     │  order-service   │  │ payment-service │  │  user-service   │
     │  (Envoy sidecar) │  │ (Envoy sidecar) │  │ (Envoy sidecar) │
     └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
              │                     │                     │
              │    mTLS encrypted   │    mTLS encrypted   │
              │    service-to-service communication       │
              │                     │                     │
     ┌────────▼─────────────────────▼─────────────────────▼────────┐
     │                    Kubernetes DNS                            │
     │  order-service.orders.svc.cluster.local                     │
     │  payment-service.payments.svc.cluster.local                 │
     └─────────────────────────────────────────────────────────────┘
```

### Step 6: Manage Secrets and Configuration

A platform-grade secrets strategy ensures that no team stores credentials in Git, environment variables are managed consistently across environments, and configuration promotion from dev to production is auditable and safe.

**HashiCorp Vault Integration with Kubernetes**:

```hcl
# vault/terraform/kubernetes-auth.tf
# Configure Vault Kubernetes auth method
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
  path = "kubernetes/production"
}

resource "vault_kubernetes_auth_backend_config" "production" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = var.kubernetes_api_url
  kubernetes_ca_cert = var.kubernetes_ca_cert
}

# Create a policy for the payment service
resource "vault_policy" "payment_service" {
  name = "payment-service"
  policy = <<-EOT
    path "secret/data/payment-service/*" {
      capabilities = ["read"]
    }
    path "database/creds/payment-service-readonly" {
      capabilities = ["read"]
    }
    path "transit/encrypt/payment-service" {
      capabilities = ["update"]
    }
    path "transit/decrypt/payment-service" {
      capabilities = ["update"]
    }
  EOT
}

# Bind the Kubernetes service account to the Vault policy
resource "vault_kubernetes_auth_backend_role" "payment_service" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "payment-service"
  bound_service_account_names      = ["payment-service"]
  bound_service_account_namespaces = ["payments"]
  token_policies                   = [vault_policy.payment_service.name]
  token_ttl                        = 3600
  token_max_ttl                    = 86400
}
```

**External Secrets Operator Configuration**:

```yaml
# external-secrets/cluster-secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.internal.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes/production"
          role: "external-secrets"
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
---
# external-secrets/payment-service-secrets.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: payment-service-secrets
  namespace: payments
spec:
  refreshInterval: 5m
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: payment-service-secrets
    creationPolicy: Owner
    template:
      engineVersion: v2
      data:
        DATABASE_URL: "postgresql://{{ .db_username }}:{{ .db_password }}@payments-db:5432/payments?sslmode=require"
        STRIPE_API_KEY: "{{ .stripe_key }}"
  data:
    - secretKey: db_username
      remoteRef:
        key: secret/data/payment-service/database
        property: username
    - secretKey: db_password
      remoteRef:
        key: secret/data/payment-service/database
        property: password
    - secretKey: stripe_key
      remoteRef:
        key: secret/data/payment-service/stripe
        property: api_key
```

**Environment Promotion Pattern (Config-as-Code)**:

```
config/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── configmap.yaml
├── overlays/
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   ├── configmap-patch.yaml    # DEV-specific config
│   │   └── replicas-patch.yaml     # replicas: 1
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   ├── configmap-patch.yaml    # STAGING-specific config
│   │   └── replicas-patch.yaml     # replicas: 2
│   └── production/
│       ├── kustomization.yaml
│       ├── configmap-patch.yaml    # PROD-specific config
│       ├── replicas-patch.yaml     # replicas: 3, minAvailable: 2
│       └── hpa-patch.yaml          # autoscaling enabled
```

```yaml
# config/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: payments
resources:
  - ../../base
patches:
  - path: configmap-patch.yaml
  - path: replicas-patch.yaml
  - path: hpa-patch.yaml
configMapGenerator:
  - name: payment-service-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
      - ENABLE_DEBUG_ENDPOINTS=false
      - RATE_LIMIT_RPS=1000
      - CACHE_TTL_SECONDS=300
```

**Sealed Secrets for GitOps**:

```yaml
# Encrypted secret safe to commit to Git
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: payment-service-sealed
  namespace: payments
spec:
  encryptedData:
    STRIPE_KEY: AgBy3i4OJSWK+PiTySYZZA9rO...truncated
    DB_PASSWORD: AgCtr8cVnFlSh2+PjGMDwE4O...truncated
  template:
    metadata:
      name: payment-service-secrets
      namespace: payments
    type: Opaque
```

Sealed secrets allow you to store encrypted secrets in Git alongside application manifests. The Sealed Secrets controller running in the cluster holds the private key and decrypts them at deploy time. This is ideal for GitOps workflows where all configuration (including secrets) should be version-controlled.

### Step 7: Enforce Platform Governance and Guardrails

Governance ensures that self-service does not mean uncontrolled. Policy-as-code enables the platform team to enforce organizational standards (cost tagging, security baselines, resource limits) automatically, without bottlenecking teams with manual reviews.

**OPA/Gatekeeper Policy for Required Labels**:

```yaml
# policies/required-labels-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: object
                properties:
                  key:
                    type: string
                  allowedRegex:
                    type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_].key}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }

        violation[{"msg": msg}] {
          label := input.parameters.labels[_]
          label.allowedRegex != ""
          value := input.review.object.metadata.labels[label.key]
          not re_match(label.allowedRegex, value)
          msg := sprintf("Label '%v' value '%v' does not match pattern '%v'", [label.key, value, label.allowedRegex])
        }
---
# policies/required-labels-constraint.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-platform-labels
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet", "DaemonSet"]
    excludedNamespaces:
      - kube-system
      - istio-system
      - monitoring
  parameters:
    labels:
      - key: "app.kubernetes.io/name"
      - key: "app.kubernetes.io/owner"
        allowedRegex: "^team-[a-z-]+$"
      - key: "platform.example.com/cost-center"
        allowedRegex: "^CC-[0-9]{4}$"
```

**Kyverno Policy for Resource Quotas**:

```yaml
# policies/kyverno-resource-limits.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
  annotations:
    policies.kyverno.io/title: Require Resource Limits
    policies.kyverno.io/description: >-
      All containers must specify CPU and memory requests and limits.
      This prevents noisy-neighbor issues and enables accurate capacity planning.
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-resource-limits
      match:
        any:
          - resources:
              kinds:
                - Pod
      exclude:
        any:
          - resources:
              namespaces:
                - kube-system
                - istio-system
      validate:
        message: >-
          All containers must have CPU and memory requests and limits defined.
          See https://platform.internal/docs/resource-limits for guidance.
        pattern:
          spec:
            containers:
              - resources:
                  requests:
                    memory: "?*"
                    cpu: "?*"
                  limits:
                    memory: "?*"
                    cpu: "?*"
    - name: enforce-max-limits
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: >-
          Container memory limit cannot exceed 8Gi and CPU limit cannot exceed 4 cores.
          Request a quota increase at https://platform.internal/quota-request if needed.
        deny:
          conditions:
            any:
              - key: "{{ request.object.spec.containers[].resources.limits.memory }}"
                operator: GreaterThan
                value: "8Gi"
              - key: "{{ request.object.spec.containers[].resources.limits.cpu }}"
                operator: GreaterThan
                value: "4"
```

**Cost Tagging Enforcement with Terraform Sentinel**:

```python
# sentinel/enforce-cost-tags.sentinel
import "tfplan/v2" as tfplan

required_tags = ["CostCenter", "Environment", "Owner", "ManagedBy"]

taggable_resources = [
  "aws_instance",
  "aws_s3_bucket",
  "aws_db_instance",
  "aws_rds_cluster",
  "aws_elasticache_cluster",
  "aws_eks_cluster",
  "aws_lambda_function",
]

all_taggable = filter tfplan.resource_changes as _, rc {
  rc.type in taggable_resources and
  rc.change.actions contains "create" or rc.change.actions contains "update"
}

deny_missing_tags = rule {
  all all_taggable as _, resource {
    all required_tags as tag {
      resource.change.after.tags contains tag
    }
  }
}

main = rule {
  deny_missing_tags
}
```

**Platform SLOs**:

Define SLOs for the platform itself so teams can depend on it with confidence:

| Platform Capability | SLO Target | Measurement |
|---------------------|-----------|-------------|
| **CI/CD pipeline availability** | 99.9% | Percentage of pipeline runs that start within 2 minutes of trigger |
| **Build time (p95)** | < 10 minutes | 95th percentile of build duration across all services |
| **Deployment success rate** | > 99% | Percentage of deployments that complete without rollback |
| **Secret rotation latency** | < 5 minutes | Time from Vault secret update to pod receiving new value |
| **Service catalog freshness** | < 15 minutes | Time from push to main until Backstage catalog reflects the change |
| **Self-service provisioning** | < 30 minutes | Time from PR merge to resource fully provisioned |

**Compliance Automation**:

```yaml
# compliance/cis-benchmark-scan.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cis-benchmark-scan
  namespace: platform-compliance
spec:
  schedule: "0 2 * * 1"  # Weekly Monday 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: compliance-scanner
          containers:
            - name: kube-bench
              image: aquasec/kube-bench:v0.7.0
              command: ["kube-bench", "run", "--json"]
              volumeMounts:
                - name: results
                  mountPath: /results
            - name: report-uploader
              image: platform/compliance-reporter:latest
              command: ["upload-results"]
              env:
                - name: REPORT_BUCKET
                  value: "s3://compliance-reports/kube-bench"
                - name: SLACK_CHANNEL
                  value: "#platform-compliance"
          volumes:
            - name: results
              emptyDir: {}
          restartPolicy: Never
```

## Best Practices

- **Treat the platform as a product**: Conduct user research, maintain a roadmap, measure adoption, and iterate
- **Start small and iterate**: Launch with one golden path (for example, deploying a stateless service) and expand based on demand
- **Document everything**: Golden paths without documentation are invisible paths that nobody walks
- **Measure what matters**: Combine DORA metrics with qualitative developer surveys for a complete picture
- **Enforce guardrails, not gates**: Policies should block unsafe actions automatically rather than requiring manual approval queues
- **Version your platform APIs**: Terraform modules, pipeline templates, and Crossplane compositions all need semantic versioning
- **Build escape hatches**: Allow teams to deviate from golden paths with an explicit opt-out process so the platform does not become a blocker
- **Automate compliance**: Use policy-as-code to shift compliance left rather than relying on post-deployment audits
- **Own your SLOs**: The platform team must have SLOs for its own services (pipeline uptime, provisioning latency, catalog freshness)
- **Invest in onboarding**: A 30-minute "first deploy" experience for new engineers is the best advertisement for the platform

## Common Patterns

### Pattern 1: New Service Golden Path

```
Developer opens Backstage -> Selects template -> Fills form
    -> Repo created with CI/CD, monitoring, docs
    -> First deploy to dev in < 30 minutes
    -> Registered in service catalog automatically
```

### Pattern 2: Self-Service Database Provisioning

```
Developer opens PR with database.yaml -> CI runs plan + policy check
    -> Cost estimate posted as PR comment -> Auto-approved under threshold
    -> Merge triggers provisioning -> Connection string in Vault
    -> ExternalSecret syncs to Kubernetes -> App reads from mounted secret
```

### Pattern 3: Progressive Delivery Pipeline

```
Push to main -> Build + test -> Deploy to staging (rolling)
    -> Automated smoke tests -> Deploy to production (canary 5%)
    -> Monitor error rate + latency -> Auto-promote or rollback
    -> Full rollout -> Notify Slack
```

## Quality Checklist

- [ ] Service catalog contains all production services with owners and dependencies
- [ ] At least one golden path template exists for the most common service type
- [ ] Shared CI/CD templates are versioned and consumed by 80%+ of services
- [ ] DORA metrics are collected and visible to all engineering teams
- [ ] Mutual TLS is enforced for all service-to-service communication
- [ ] No secrets are stored in Git (sealed secrets or external-secrets-operator in use)
- [ ] Policy-as-code blocks deployments missing required labels and resource limits
- [ ] Cost tags are enforced on all cloud resources
- [ ] Platform SLOs are defined, measured, and reviewed monthly
- [ ] Developer onboarding documentation is current and tested quarterly

## Related Skills

- `cloud-architect` - Cloud infrastructure design and Well-Architected Framework
- `terraform-specialist` - Deep Terraform module development and state management
- `kubernetes-expert` - Container orchestration and cluster operations
- `cicd-architect` - Advanced CI/CD pipeline design and optimization
- `security-review` - Security assessment and threat modeling

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Team Topologies platform team patterns, CNCF platform engineering maturity model, DORA research


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
