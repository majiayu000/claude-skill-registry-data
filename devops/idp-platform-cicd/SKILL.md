---
name: idp-platform-cicd
description: Design and manage Internal Developer Platform (IDP) CI/CD workflows, Backstage scaffolding, platform engineering pipelines, golden path templates, and self-service infrastructure. Use when working with platform engineering, developer portals, service catalogs, or golden path templates.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# IDP Platform CI/CD Skill

You are a Senior Platform Engineer specializing in Internal Developer Platforms (IDP). You design golden paths, self-service infrastructure, and platform engineering workflows that enable developers to ship faster while maintaining compliance and best practices.

## Core Responsibilities

1. **Golden Path Templates**
   - Design opinionated templates for common use cases
   - Bake in security, observability, and compliance
   - Standardize across microservices
   - Provide clear documentation and runbooks

2. **Service Catalog Management**
   - Backstage (or similar) configuration
   - Service discovery and dependency mapping
   - Ownership tracking and metadata
   - API documentation integration

3. **Self-Service Infrastructure**
   - Build self-service workflows for developers
   - Implement approval gates and policy enforcement
   - Automate resource provisioning
   - Provide clear cost visibility

4. **Platform APIs**
   - Design platform APIs for internal consumption
   - Implement API gateways and rate limiting
   - Version and deprecate APIs gracefully

5. **Developer Experience (DevEx)**
   - Reduce cognitive load for developers
   - Provide intuitive CLI tools and UIs
   - Minimize time to production
   - Create comprehensive documentation

## Golden Path Architecture

### Template Structure

```
golden-paths/
├── nodejs-service/
│   ├── template.yaml          # Backstage template
│   ├── skeleton/
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   ├── .github/
│   │   │   └── workflows/
│   │   │       └── pipeline.yaml
│   │   ├── k8s/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── src/
│   └── docs/
│       └── index.md
├── python-service/
├── data-pipeline/
└── frontend-spa/
```

### Backstage Template Example

```yaml
# template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-service
  title: Node.js Microservice
  description: A golden path template for Node.js microservices with observability, security, and best practices built-in
  tags:
    - nodejs
    - typescript
    - microservice
    - recommended
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      required:
        - name
        - owner
        - description
      properties:
        name:
          title: Service Name
          type: string
          description: Unique name for the service
          ui:field: EntityNamePicker
        owner:
          title: Owner
          type: string
          description: Team that owns this service
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: Group
        description:
          title: Description
          type: string
          description: Brief description of the service
        environment:
          title: Environment
          type: string
          default: dev
          enum: [dev, staging, prod]
        database:
          title: Database Required
          type: boolean
          default: false
        cache:
          title: Cache Required
          type: boolean
          default: false

    - title: CI/CD Configuration
      properties:
        repository:
          title: Repository Location
          type: string
          enum: [github, gitlab]
          default: github
        deployStrategy:
          title: Deployment Strategy
          type: string
          enum: [rolling, blue-green, canary]
          default: rolling

  steps:
    - id: fetch-base
      name: Fetch Skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          description: ${{ parameters.description }}
          environment: ${{ parameters.environment }}
          database: ${{ parameters.database }}
          cache: ${{ parameters.cache }}

    - id: publish
      name: Publish Repository
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: ${{ parameters.description }}
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}
        defaultBranch: main
        repoVisibility: internal
        topics:
          - nodejs
          - microservice
          - ${{ parameters.environment }}

    - id: register
      name: Register Service
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

    - id: create-argocd-app
      name: Create ArgoCD Application
      action: http:backstage:request
      input:
        method: POST
        path: /proxy/argocd/api/v1/applications
        headers:
          Content-Type: application/json
        body:
          apiVersion: argoproj.io/v1alpha1
          kind: Application
          metadata:
            name: ${{ parameters.name }}
            namespace: argocd
          spec:
            project: default
            source:
              repoURL: ${{ steps.publish.output.remoteUrl }}
              targetRevision: HEAD
              path: k8s/
            destination:
              server: https://kubernetes.default.svc
              namespace: ${{ parameters.environment }}
            syncPolicy:
              automated:
                prune: true
                selfHeal: true
              syncOptions:
                - CreateNamespace=true

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Open in Catalog
n        icon: catalog
        entityRef: ${{ steps.register.output.entityRef }}
      - title: ArgoCD Application
        url: https://argocd.company.com/applications/${{ parameters.name }}
```

## Platform CI/CD Pipeline

```yaml
name: Platform CI/CD

on:
  push:
    branches: [main]
    paths:
      - 'platform/**'
      - 'golden-paths/**'
  pull_request:
    branches: [main]
    paths:
      - 'platform/**'
      - 'golden-paths/**'

env:
  TERRAFORM_VERSION: '1.7.0'
  BACKSTAGE_VERSION: '1.20.0'

jobs:
  # Validate Templates
  validate-templates:
    name: Validate Golden Path Templates
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Backstage CLI
        run: npm install -g @backstage/cli

      - name: Validate template schema
        run: |
          for template in golden-paths/*/template.yaml; do
            echo "Validating $template"
            backstage-cli template:validate "$template"
          done

      - name: Template dry-run
        run: |
          for template in golden-paths/*/template.yaml; do
            echo "Testing $template"
            backstage-cli template:dry-run --file "$template" \
              --parameter name=test-service \
              --parameter owner=platform-team \
              --parameter description="Test service"
          done

  # Platform Infrastructure
  platform-infra:
    name: Platform Infrastructure
    runs-on: ubuntu-latest
    needs: validate-templates
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TERRAFORM_VERSION }}

      - name: Terraform Format Check
        run: terraform fmt -check -recursive platform/

      - name: Terraform Validate
        working-directory: platform/terraform
        run: |
          terraform init -backend=false
          terraform validate

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: platform/
          framework: terraform

      - name: Terraform Plan
        if: github.event_name == 'pull_request'
        working-directory: platform/terraform
        run: terraform plan -no-color
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        working-directory: platform/terraform
        run: terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

  # Backstage Deployment
  deploy-backstage:
    name: Deploy Backstage
    runs-on: ubuntu-latest
    needs: platform-infra
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Backstage Image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./packages/backend/Dockerfile
          push: false
          tags: backstage:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Backstage Tests
        run: yarn test

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/backstage backstage=backstage:${{ github.sha }}
          kubectl rollout status deployment/backstage

      - name: Verify Deployment
        run: |
          kubectl get pods -l app=backstage
          kubectl get svc backstage
```

## Platform API Design

### Self-Service API Structure

```yaml
openapi: 3.0.3
info:
  title: Platform Self-Service API
  description: API for developers to provision resources and manage services
  version: 1.0.0
  contact:
    name: Platform Team
    email: platform@company.com

paths:
  /services:
    post:
      summary: Create a new service
      operationId: createService
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServiceRequest'
      responses:
        '201':
          description: Service created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Service'
        '400':
          $ref: '#/components/responses/BadRequest'

  /databases:
    post:
      summary: Provision a database
      operationId: provisionDatabase
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DatabaseRequest'
      responses:
        '202':
          description: Database provisioning initiated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AsyncTask'

  /environments:
    get:
      summary: List available environments
      operationId: listEnvironments
      responses:
        '200':
          description: List of environments
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Environment'

components:
  schemas:
    ServiceRequest:
      type: object
      required:
        - name
        - team
        - template
      properties:
        name:
          type: string
          pattern: '^[a-z0-9-]+$'
        team:
          type: string
        template:
          type: string
          enum: [nodejs, python, golang, data-pipeline]
        environment:
          type: string
          default: dev

    DatabaseRequest:
      type: object
      required:
        - service
        - engine
        - instance_class
      properties:
        service:
          type: string
        engine:
          type: string
          enum: [postgresql, mysql, redis, mongodb]
        instance_class:
          type: string
          default: db.t3.micro
        backup_retention:
          type: integer
          default: 7

    AsyncTask:
      type: object
      properties:
        task_id:
          type: string
        status:
          type: string
          enum: [pending, running, completed, failed]
        resource_id:
          type: string

    Environment:
      type: object
      properties:
        name:
          type: string
        status:
          type: string
        cost_center:
          type: string
```

## Policy Enforcement

### OPA (Open Policy Agent) Rules

```rego
# policies/service.rego
package platform.service

import future.keywords.if
import future.keywords.in

# Allow only approved templates
approved_templates := ["nodejs-service", "python-service", "golang-service", "data-pipeline"]

allow if {
    input.template in approved_templates
}

# Require cost center for production
deny[msg] if {
    input.environment == "production"
    not input.cost_center
    msg := "Cost center required for production resources"
}

# Limit resource sizing in dev
deny[msg] if {
    input.environment == "development"
    input.instance_class != "db.t3.micro"
    msg := "Only db.t3.micro allowed in development"
}

# Require tags
deny[msg] if {
    required_tags := {"owner", "team", "project", "environment"}
    missing := required_tags - {key | input.tags[key]}
    count(missing) > 0
    msg := sprintf("Missing required tags: %v", [missing])
}
```

### Policy Check Pipeline

```yaml
policy-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Setup OPA
      run: |
        curl -L -o opa https://openpolicyagent.org/downloads/v0.60.0/opa_linux_amd64
        chmod +x opa
        sudo mv opa /usr/local/bin/

    - name: Test Policies
      run: |
        opa test policies/ --verbose

    - name: Validate Against Policies
      run: |
        cat service-request.json | opa eval --data policies/ --input /dev/stdin "data.platform.service.deny"
```

## Service Catalog Standards

### catalog-info.yaml Template

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{ values.name }}
  description: ${{ values.description }}
  tags:
    - ${{ values.language }}
    - microservice
    - ${{ values.environment }}
  annotations:
    github.com/project-slug: myorg/${{ values.name }}
    backstage.io/techdocs-ref: dir:.
    argocd/app-name: ${{ values.name }}
    grafana/dashboard-selector: "tags=service,${{ values.name }}"
    sentry.io/project-slug: ${{ values.name }}
    datadog/slo.dashboard: https://app.datadoghq.com/slo/${{ values.name }}
spec:
  type: service
  lifecycle: production
  owner: ${{ values.owner }}
  system: ${{ values.system | default("platform") }}
  dependsOn:
    - resource:default/${{ values.database_name }}
  providesApis:
    - ${{ values.name }}-api
  consumesApis:
    - platform-auth-api
    - platform-audit-api
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: ${{ values.name }}-api
  description: API for ${{ values.description }}
spec:
  type: openapi
  lifecycle: production
  owner: ${{ values.owner }}
  definition:
    $text: ./openapi.yaml
```

## Cost Management

```yaml
cost-gates:
  runs-on: ubuntu-latest
  steps:
    - name: Estimate Infrastructure Costs
      uses: infracost/actions/setup@v2

    - name: Breakdown
      run: |
        infracost breakdown --path plan.json \
          --format json \
          --out-file /tmp/infracost.json

    - name: Post Comment
      run: |
        infracost comment github --path /tmp/infracost.json \
          --github-token ${{ github.token }} \
          --repo $GITHUB_REPOSITORY \
          --pull-request ${{ github.event.pull_request.number }} \
          --behavior update
```

## Golden Path Checklist

- [ ] Security defaults (secrets management, encryption)
- [ ] Observability (metrics, logs, traces)
- [ ] Health checks and readiness probes
- [ ] Graceful shutdown handling
- [ ] Configuration management (env vars, config maps)
- [ ] CI/CD pipeline included
- [ ] Documentation and runbooks
- [ ] Cost estimates provided
- [ ] Dependency scanning enabled
- [ ] Resource limits defined