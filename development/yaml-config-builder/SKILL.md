---
name: yaml-config-builder
description: Generate properly structured YAML configuration files for applications, services, and infrastructure with correct syntax and common patterns. Triggers on "create YAML config", "generate YAML for", "YAML configuration file", "config.yml for".
---

# YAML Config Builder

Generate properly structured, production-ready YAML configuration files for various applications and services.

## Output Requirements

**File Output:** `.yaml` or `.yml` files
**Naming Convention:** `{service-name}.yaml` or `config.yaml`
**Indentation:** 2 spaces (never tabs)
**Encoding:** UTF-8

## When Invoked

Immediately generate a complete, valid YAML configuration file. Include sensible defaults and comments for customization.

## YAML Syntax Rules

### Formatting
- 2-space indentation, consistent throughout
- No tabs ever
- Blank lines between major sections
- Comments with `#` for documentation

### Strings
- Quote strings containing special characters: `":"`, `"#"`, `"{"`, etc.
- Quote strings that look like numbers or booleans: `"true"`, `"123"`
- Multi-line strings use `|` (literal) or `>` (folded)

### Lists and Maps
```yaml
# List syntax
items:
  - first
  - second
  - third

# Map syntax
config:
  key: value
  nested:
    deep: value
```

## Configuration Templates

### Application Configuration
```yaml
# Application Configuration
# Environment: production

app:
  name: my-application
  version: 1.0.0
  environment: production
  debug: false

server:
  host: 0.0.0.0
  port: 8080
  timeout: 30s
  max_connections: 1000

database:
  host: localhost
  port: 5432
  name: app_production
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}
  pool:
    min: 5
    max: 20
    idle_timeout: 300s

cache:
  enabled: true
  provider: redis
  host: localhost
  port: 6379
  ttl: 3600

logging:
  level: info
  format: json
  output:
    - stdout
    - file:/var/log/app/app.log

features:
  feature_x: true
  feature_y: false
  experimental:
    new_ui: false
```

### Docker Compose
```yaml
version: "3.8"

services:
  app:
    image: myapp:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./data:/app/data
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: app-network
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "20"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run linting
        run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app: my-app
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
        version: v1
    spec:
      containers:
        - name: my-app
          image: myregistry/my-app:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
  namespace: production
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### ESLint Configuration
```yaml
root: true

env:
  browser: true
  es2022: true
  node: true

extends:
  - eslint:recommended
  - plugin:@typescript-eslint/recommended
  - plugin:react/recommended
  - plugin:react-hooks/recommended
  - prettier

parser: "@typescript-eslint/parser"

parserOptions:
  ecmaVersion: latest
  sourceType: module
  ecmaFeatures:
    jsx: true

plugins:
  - "@typescript-eslint"
  - react
  - react-hooks
  - import

rules:
  no-console: warn
  no-unused-vars: off
  "@typescript-eslint/no-unused-vars": error
  "@typescript-eslint/explicit-function-return-type": off
  react/react-in-jsx-scope: off
  import/order:
    - error
    - groups:
        - builtin
        - external
        - internal
        - parent
        - sibling
        - index

settings:
  react:
    version: detect
```

## Environment Variable Patterns

Use environment variable substitution syntax appropriate for the tool:
- Shell: `${VAR_NAME}` or `$VAR_NAME`
- Docker Compose: `${VAR_NAME:-default}`
- Kubernetes: `$(VAR_NAME)` or valueFrom references

## Validation Checklist

Before outputting, verify:
- [ ] Valid YAML syntax (parseable)
- [ ] Consistent 2-space indentation
- [ ] No tabs
- [ ] Proper quoting of special strings
- [ ] Comments are helpful, not redundant
- [ ] Sensitive values use environment variables
- [ ] Required fields are present for the target tool

## Example Invocations

**Prompt:** "Create docker-compose.yml for a Node.js app with PostgreSQL and Redis"
**Output:** Complete `docker-compose.yml` with all three services configured.

**Prompt:** "Generate GitHub Actions workflow for Python project with testing and deployment"
**Output:** Complete `.github/workflows/ci.yml` with test and deploy jobs.

**Prompt:** "YAML config for a REST API application"
**Output:** Complete `config.yaml` with server, database, logging, and feature flag sections.
