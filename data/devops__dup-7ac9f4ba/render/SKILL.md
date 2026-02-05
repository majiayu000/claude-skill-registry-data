---
name: render
description: Comprehensive guide for Render.com deployment and infrastructure management. Use when deploying apps to Render, configuring render.yaml Blueprints, managing web services/workers/cron jobs, setting up Postgres or Key Value datastores, configuring preview environments for PRs, or automating CI/CD with the Render CLI. Includes templates and validation scripts for common deployment patterns.
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Render.com Deployment & Infrastructure

Render manages infrastructure through Blueprints - YAML configuration files that define services, databases, and environment groups as code.

## Quick Start

```bash
# Install Render CLI
brew install render

# Authenticate
render login

# Set workspace
render workspace set

# List services
render services

# Deploy a service
render deploys create SERVICE_ID

# Open SSH session
render ssh SERVICE_ID
```

## Blueprint Configuration

### render.yaml Structure

Every Blueprint file is named `render.yaml` at the repo root:

```yaml
previews:
  generation: automatic # Enable preview environments

services:
  - type: web
    name: my-app
    runtime: node
    plan: starter
    region: oregon
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: APP_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: my-db
          property: connectionString

databases:
  - name: my-db
    plan: basic-256mb
    region: oregon

envVarGroups:
  - name: shared-config
    envVars:
      - key: API_VERSION
        value: v1
```

### Key Fields

| Field     | Purpose                                                     |
| --------- | ----------------------------------------------------------- |
| `name`    | Service identifier (must be unique)                         |
| `type`    | web, pserv, worker, cron, keyvalue                          |
| `runtime` | node, python, ruby, go, rust, elixir, docker, image, static |
| `plan`    | Instance type: free, starter, standard, pro, pro plus       |
| `region`  | oregon (default), ohio, virginia, frankfurt, singapore      |

**See**: [references/blueprint-spec.md](references/blueprint-spec.md) for complete YAML reference.

## Service Types

| Type     | Use Case                                    | Public URL           |
| -------- | ------------------------------------------- | -------------------- |
| `web`    | HTTP apps (Express, FastAPI, Rails)         | Yes                  |
| `pserv`  | Internal services (no public access)        | No (private network) |
| `worker` | Background job processors (Sidekiq, Celery) | No                   |
| `cron`   | Scheduled tasks                             | No                   |
| `static` | CDN-served static sites                     | Yes                  |

```yaml
# Web service
- type: web
  name: api-server
  runtime: node
  buildCommand: npm install
  startCommand: npm start

# Private service (internal only)
- type: pserv
  name: internal-cache
  runtime: docker

# Background worker
- type: worker
  name: job-processor
  runtime: python
  buildCommand: pip install -r requirements.txt
  startCommand: python worker.py

# Cron job (runs every hour)
- type: cron
  name: cleanup-task
  runtime: python
  schedule: "0 * * * *"
  buildCommand: pip install -r requirements.txt
  startCommand: python cleanup.py
```

**See**: [references/service-types.md](references/service-types.md) for detailed comparison.

## Environment Variables

### Setting Values

```yaml
envVars:
  # Hardcoded value
  - key: API_URL
    value: https://api.example.com

  # Generated secret (base64, 256-bit)
  - key: JWT_SECRET
    generateValue: true

  # Prompt in Dashboard (for secrets)
  - key: STRIPE_KEY
    sync: false

  # Reference database property
  - key: DATABASE_URL
    fromDatabase:
      name: my-db
      property: connectionString

  # Reference another service
  - key: REDIS_URL
    fromService:
      type: keyvalue
      name: my-cache
      property: connectionString

  # Link environment group
  - fromGroup: shared-config
```

### Preview Environment Overrides

```yaml
envVars:
  - key: API_KEY
    value: production-key
    previewValue: test-key # Used in preview environments
```

**See**: [references/blueprint-spec.md](references/blueprint-spec.md) for all env var patterns.

## Datastores

### Render Postgres

```yaml
databases:
  - name: my-database
    plan: basic-256mb # basic-256mb, basic-1gb, pro-4gb, etc.
    region: oregon
    postgresMajorVersion: "17"
    diskSizeGB: 15
    ipAllowList: # Restrict external access
      - source: 0.0.0.0/0
        description: everywhere
```

### Render Key Value (Redis-compatible)

```yaml
services:
  - type: keyvalue
    name: my-cache
    plan: starter
    maxmemoryPolicy: allkeys-lru # Eviction policy
    ipAllowList:
      - source: 0.0.0.0/0
        description: everywhere
```

**Key Value policies**: `allkeys-lru`, `volatile-lru`, `noeviction`, `allkeys-lfu`, `volatile-random`, `allkeys-random`, `volatile-ttl`

**See**: [references/datastores.md](references/datastores.md) for connection patterns.

## Multi-Environment Setup

Use Render Projects to organize services by environment:

```yaml
projects:
  - name: my-app
    environments:
      - name: production
        services:
          - type: web
            name: my-app-prod
            runtime: node
            plan: standard
            buildCommand: npm ci && npm run build
            startCommand: npm start
            envVars:
              - key: APP_ENV
                value: production
        databases:
          - name: my-db-prod
            plan: pro-4gb
        networking:
          isolation: enabled # Block cross-env traffic
        permissions:
          protection: enabled # Prevent destructive actions

      - name: staging
        services:
          - type: web
            name: my-app-staging
            runtime: node
            plan: starter
            buildCommand: npm ci && npm run build
            startCommand: npm start
            envVars:
              - key: APP_ENV
                value: staging
        databases:
          - name: my-db-staging
            plan: basic-256mb
```

## Preview Environments

Automatically create full environment copies for pull requests:

```yaml
previews:
  generation: automatic # or manual, off
  expireAfterDays: 7 # Auto-cleanup

services:
  - type: web
    name: my-app
    runtime: node
    plan: standard
    buildCommand: npm ci && npm run build
    startCommand: npm start
    previews:
      plan: starter # Cheaper instance for previews
      numInstances: 1

databases:
  - name: my-db
    plan: pro-4gb
    previewPlan: basic-256mb
    previewDiskSizeGB: 5
```

**Manual mode**: Add `[render preview]` to PR title to create preview.
**Skip preview**: Add `[skip preview]` to PR title.

**See**: [references/preview-environments.md](references/preview-environments.md) for setup guide.

## Helper Scripts

This skill includes automation scripts in `scripts/`:

| Script                    | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `init-blueprint.sh`       | Interactive setup wizard for render.yaml   |
| `generate-render-yaml.py` | Generate render.yaml from templates        |
| `validate-blueprint.py`   | Validate render.yaml syntax and references |
| `deploy-env.sh`           | Deploy to specific environment             |
| `env-sync.sh`             | Sync env vars between local and Render     |

### Script Dependencies

```bash
# Install Python dependencies
pip install -r scripts/requirements.txt
```

### Usage Examples

```bash
# Initialize new blueprint interactively
./scripts/init-blueprint.sh

# Generate from template
python scripts/generate-render-yaml.py --template full-stack --name my-app

# Validate before deploying
python scripts/validate-blueprint.py render.yaml

# Deploy a service (uses service ID from Render Dashboard)
./scripts/deploy-env.sh srv-abc123

# List env vars for a service
./scripts/env-sync.sh list -s srv-abc123

# Compare local .env with Render service
./scripts/env-sync.sh compare -s srv-abc123 -f .env
```

## Common Tasks

### Add New Service to Blueprint

1. Add service definition to `render.yaml`
2. Run `python scripts/validate-blueprint.py render.yaml`
3. Commit and push to trigger Blueprint sync
4. Verify in Render Dashboard

### Connect Services via Private Network

Services in same region communicate over private network:

```yaml
services:
  - type: web
    name: api
    runtime: node
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: CACHE_URL
        fromService:
          type: keyvalue
          name: cache
          property: connectionString # Uses internal URL

  - type: keyvalue
    name: cache
    plan: starter
    ipAllowList: [] # Only internal connections
```

### Scale a Service

```yaml
# Manual scaling
- type: web
  name: my-app
  runtime: node
  buildCommand: npm install
  startCommand: npm start
  numInstances: 3

# Autoscaling (Professional workspace required)
- type: web
  name: my-app
  runtime: node
  buildCommand: npm install
  startCommand: npm start
  scaling:
    minInstances: 1
    maxInstances: 5
    targetCPUPercent: 70
    targetMemoryPercent: 80
```

### Add Persistent Disk

```yaml
- type: web
  name: my-app
  runtime: node
  buildCommand: npm install
  startCommand: npm start
  disk:
    name: app-data
    mountPath: /data
    sizeGB: 10
```

**Warning**: Services with disks cannot scale to multiple instances.

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Install Render CLI
        run: |
          curl -L https://github.com/render-oss/cli/releases/download/v1.1.0/cli_1.1.0_linux_amd64.zip -o render.zip
          unzip render.zip && sudo mv cli_v1.1.0 /usr/local/bin/render

      - name: Deploy
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          render deploys create ${{ secrets.RENDER_SERVICE_ID }} --output json --confirm --wait
```

**See**: [references/ci-cd.md](references/ci-cd.md) for more patterns.

## Troubleshooting

### Blueprint Sync Fails

1. Check YAML syntax: `python scripts/validate-blueprint.py render.yaml`
2. Verify service names are unique
3. Check region consistency (services referencing each other must be in same region)

### Service Won't Deploy

1. Check build logs in Dashboard
2. Verify `buildCommand` and `startCommand`
3. Ensure `PORT` environment variable used (default: 10000)

### Database Connection Issues

1. Use internal URL for same-region services
2. Check IP allowlist for external connections
3. Verify credentials in environment variables

### Preview Environment Not Created

1. Verify `previews.generation: automatic` in render.yaml
2. Check PR title doesn't contain `[skip preview]`
3. Ensure Blueprint is synced and linked to repo

## Reference Documentation

- [Blueprint YAML Reference](references/blueprint-spec.md) - Complete field reference
- [Service Types](references/service-types.md) - Detailed service comparison
- [Datastores](references/datastores.md) - Postgres and Key Value setup
- [Preview Environments](references/preview-environments.md) - PR preview configuration
- [CI/CD Integration](references/ci-cd.md) - Pipeline automation
- [CLI Commands](references/cli-commands.md) - Render CLI reference
