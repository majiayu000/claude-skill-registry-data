---
name: infisical-patterns
description: This skill activates when managing environment variables, configuring .infisical.json, organizing workspace environments, or discussing secret management patterns with Infisical CLI. It provides conventions for secret naming, folder organization, auth selection, and local development workflows.
---

# Infisical Patterns

Core patterns for managing secrets with Infisical.

## .infisical.json Convention

The `.infisical.json` file binds a project directory to an Infisical workspace:

```json
{
  "workspaceId": "abc123-def456-ghi789",
  "defaultEnvironment": "dev",
  "gitBranchToEnvironmentMapping": null
}
```

**Rules:**
- **Commit** `.infisical.json` to git (it contains no secrets, just workspace binding)
- **Do NOT commit** `.env`, `.env.local`, or any file containing secret values

## Secret Naming Convention

Use `UPPER_SNAKE_CASE` for all secret names:

```bash
# Correct
DATABASE_URL
REDIS_HOST
STRIPE_SECRET_KEY
AWS_ACCESS_KEY_ID

# Wrong
databaseUrl          # camelCase
redis-host           # kebab-case
stripe.secret.key    # dotted
```

## Folder Organization

Organize secrets by **consumer/service** so each folder maps directly to an `infisical run --path=` invocation and machine identity scope.

### Pattern A: By Consumer/Service (Recommended)

Best for multi-service projects. Each service gets exactly the secrets it needs via `--path`.

```
/ (root)                → Shared secrets (DATABASE_URL, REDIS_URL)
├── /backend            → Backend-only (JWT_SECRET, INTERNAL_API_KEY, SENTRY_DSN)
├── /frontend           → Frontend-only (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_STRIPE_KEY)
├── /mobile             → Mobile-only (PUSH_NOTIFICATION_KEY, DEEP_LINK_SECRET)
└── /ci                 → CI/CD-only (DEPLOY_KEY, DOCKER_TOKEN, CODECOV_TOKEN)
```

Why this works:
- `infisical run --path=/backend` injects root secrets + `/backend` secrets — exactly what backend needs
- Machine identities scoped to `/backend` can't read `/ci` secrets
- Maps to team ownership and deployment targets

```bash
# Backend gets shared + backend-only secrets
infisical run --env=production --path=/backend -- node server.js

# Frontend gets shared + frontend-only secrets
infisical run --env=production --path=/frontend -- npm run build

# CI gets shared + CI-only secrets
infisical run --env=production --path=/ci -- ./deploy.sh

# Set a secret in a service folder
infisical secrets set JWT_SECRET=supersecret --env=production --path=/backend

# List secrets for a specific service
infisical secrets --env=production --path=/backend
```

### Pattern B: By Function/Type (Single-service only)

Acceptable for monoliths where everything runs as one process. All folders collapse under `--path=/` since the single service needs all secrets anyway.

```
/ (root)
├── /database           → DB_HOST, DB_PASSWORD
├── /api-keys           → STRIPE_KEY, SENDGRID_KEY
├── /auth               → JWT_SECRET, SESSION_SECRET
```

Note: `infisical run --path=/database` only injects `/database` secrets, not `/api-keys` or `/auth`. For a service needing all of them, use `--path=/` which makes the folders purely organizational.

### When to Choose

| Scenario | Pattern | Reason |
|----------|---------|--------|
| Multiple services (API + web + mobile) | By consumer | Each service uses `--path=/service` |
| Microservices | By consumer | Per-service machine identity scoping |
| Monolith / single process | By function | One `--path=/` anyway, folders are just organization |
| Monorepo with shared infra | By consumer | Map folders to deployment targets |

## Local Development Pattern

### Preferred: Runtime Injection

```bash
# Inject secrets as environment variables at runtime
infisical run --env=dev -- npm run dev

# With watch mode (re-injects when secrets change in dashboard)
infisical run --watch --env=dev -- npm run dev

# With Docker Compose
infisical run --env=dev -- docker compose up
```

### Acceptable: Export to .env

When tools require a `.env` file:

```bash
# Export to .env
infisical export --env=dev > .env

# Keep .env.example up to date
infisical secrets generate-example-env --env=dev > .env.example
```

### .env.example Maintenance

Always maintain `.env.example` with descriptive comments:

```bash
# Database
DATABASE_URL=           # PostgreSQL connection string
DB_POOL_SIZE=           # Connection pool size (default: 10)

# Authentication
JWT_SECRET=             # Secret for signing JWTs
SESSION_SECRET=         # Express session secret

# External APIs
STRIPE_SECRET_KEY=      # Stripe API secret key (sk_...)
SENDGRID_API_KEY=       # SendGrid email API key
```

## Auth Pattern Selection

### Development (Interactive)

```bash
infisical login
```

### CI/CD (Machine Identity - Universal Auth)

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID=<client-id>
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET=<client-secret>
infisical login --method=universal-auth \
  --client-id=$INFISICAL_UNIVERSAL_AUTH_CLIENT_ID \
  --client-secret=$INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET
```

### Kubernetes (Native Auth)

```bash
infisical login --method=kubernetes \
  --machine-identity-id=$MACHINE_IDENTITY_ID
```

### Cloud Providers (Native Auth)

```bash
# AWS
infisical login --method=aws-iam --machine-identity-id=$MACHINE_IDENTITY_ID

# GCP
infisical login --method=gcp-id-token --machine-identity-id=$MACHINE_IDENTITY_ID

# Azure
infisical login --method=azure --machine-identity-id=$MACHINE_IDENTITY_ID
```

## Self-Hosted Configuration

```bash
# Via CLI flag (per-command)
infisical login --domain=https://secrets.company.com
infisical run --domain=https://secrets.company.com --env=production -- npm start

# Via environment variable (recommended for CI/servers)
export INFISICAL_API_URL=https://secrets.company.com/api
infisical login --method=universal-auth ...
infisical run --env=production -- npm start
```

## Environment Management

### Standard Environments

| Environment | Usage |
|---|---|
| `dev` | Local development |
| `staging` | Pre-production testing |
| `production` | Live production |

### Custom Environments

Create in Infisical dashboard for additional stages:
- `qa` - Quality assurance testing
- `preview` - PR preview deployments
- `demo` - Demo/sales environments

### Per-Environment Secrets

```bash
# Different values per environment
infisical secrets set DATABASE_URL=postgres://localhost/myapp_dev --env=dev
infisical secrets set DATABASE_URL=postgres://staging-db/myapp --env=staging
infisical secrets set DATABASE_URL=postgres://prod-db/myapp --env=production
```

## AI Agent Credential Security & Agent Vault

When AI agents, MCP servers, or automated tools interact with applications, prevent exposing raw production secrets to the LLM context:

### 1. Infisical Agent Vault (Credential Proxy)
- **Principle**: The AI agent does not directly hold sensitive API keys. Instead, outgoing tool requests pass through Infisical Agent Vault as an egress proxy.
- **Workflow**:
  - The agent is given a scoped placeholder or local proxy endpoint.
  - Agent Vault injects the actual authenticated headers/secrets at egress before reaching downstream APIs.
  - Zero sensitive credentials appear in LLM conversation logs, system prompts, or tool inputs/outputs.

### 2. Scoped Machine Identities for AI Workflows
- Always create a dedicated machine identity for automated agent execution with read-only permissions scoped strictly to `/dev` or `/testing`:
  ```bash
  infisical login --method=universal-auth \
    --client-id=$INFISICAL_AGENT_CLIENT_ID \
    --client-secret=$INFISICAL_AGENT_CLIENT_SECRET
  ```
- Never execute AI coding tools with human admin tokens.

### 3. Agent Sentinel Audit
- Use Infisical Agent Sentinel to enforce access policies, rate limits, and audit logs for MCP tool calls requesting secrets.

## Anti-Patterns

### Never Commit .env Files

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

### Never Hardcode Secrets

```python
# WRONG
api_key = "sk_live_abc123"

# CORRECT
import os
api_key = os.environ["STRIPE_SECRET_KEY"]
```

### Never Use Same Secrets Across Environments

Each environment should have unique credentials. Never copy production secrets to development.

### Never Pass Secrets as CLI Arguments

```bash
# WRONG - visible in process list and shell history
./app --db-password=secret123

# CORRECT - injected as environment variables
infisical run --env=production -- ./app
```

### Never Bake Secrets into Docker Images

```dockerfile
# WRONG - secret persists in image layers
ENV API_KEY=sk_live_abc123

# CORRECT - inject at runtime
CMD ["infisical", "run", "--env=production", "--", "node", "server.js"]
```

### Never Use Overly Broad Permissions

Grant machine identities access only to the environments they need. A CI identity for staging should NOT have production access.
