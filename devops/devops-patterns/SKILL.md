---
name: devops-patterns
description: DevOps patterns including CI/CD pipeline design, GitHub Actions, Infrastructure as Code, Docker, Kubernetes, deployment strategies, monitoring, and disaster recovery. Use when setting up CI/CD, deploying applications, managing infrastructure, or creating pipelines.
---

# DevOps Patterns

This skill provides comprehensive guidance for implementing DevOps practices, automation, and deployment strategies.

## CI/CD Pipeline Design

### Pipeline Stages

```yaml
# Complete CI/CD Pipeline
stages:
  - lint          # Code quality checks
  - test          # Run test suite
  - build         # Build artifacts
  - scan          # Security scanning
  - deploy-dev    # Deploy to development
  - deploy-staging # Deploy to staging
  - deploy-prod   # Deploy to production
```

### Pipeline Best Practices

**1. Fast Feedback**: Run fastest checks first
```yaml
jobs:
  # Quick checks first (1-2 minutes)
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run lint

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run type-check

  # Longer tests after (5-10 minutes)
  test:
    needs: [lint, type-check]
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

**2. Fail Fast**: Stop pipeline on first failure
**3. Idempotent**: Running twice produces same result
**4. Versioned**: Pipeline config in version control

## GitHub Actions Patterns

### Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      DATABASE_URL:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Use in another workflow
# .github/workflows/main.yml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '18'
    secrets:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Matrix Strategy

```yaml
# Test across multiple versions
jobs:
  test:
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Custom Actions

```yaml
# .github/actions/deploy/action.yml
name: 'Deploy Application'
description: 'Deploy to specified environment'
inputs:
  environment:
    description: 'Target environment'
    required: true
  api-key:
    description: 'Deployment API key'
    required: true

runs:
  using: 'composite'
  steps:
    - run: |
        echo "Deploying to ${{ inputs.environment }}"
        ./deploy.sh ${{ inputs.environment }}
      env:
        API_KEY: ${{ inputs.api-key }}
      shell: bash

# Usage
jobs:
  deploy:
    steps:
      - uses: ./.github/actions/deploy
        with:
          environment: production
          api-key: ${{ secrets.DEPLOY_KEY }}
```

### Conditional Execution

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - name: Deploy to production
        run: ./deploy.sh production

  notify:
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - name: Send failure notification
        uses: slack/notify@v2
        with:
          message: 'Build failed!'
```

## Infrastructure as Code (Terraform)

### Project Structure

```
terraform/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
└── global/
    └── s3/
        └── main.tf
```

### VPC Module Example

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.environment}-public-${count.index + 1}"
  }
}

# modules/vpc/variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}
```

### Using Modules

```hcl
# environments/prod/main.tf
terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "../../modules/vpc"

  environment          = "prod"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones  = ["us-east-1a", "us-east-1b"]
}

module "eks" {
  source = "../../modules/eks"

  cluster_name    = "prod-cluster"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.public_subnet_ids
  node_count      = 3
  node_instance_type = "t3.large"
}
```

## Docker Best Practices

### Multi-Stage Builds

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Layer Optimization

```dockerfile
# ✅ GOOD - Dependencies cached separately
FROM node:18-alpine

WORKDIR /app

# Copy package files first (rarely change)
COPY package*.json ./
RUN npm ci

# Copy source code (changes frequently)
COPY . .
RUN npm run build

# ❌ BAD - Everything in one layer
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm ci && npm run build
# Cache invalidated on every source change
```

### Security Best Practices

```dockerfile
# ✅ Use specific versions
FROM node:18.17.1-alpine

# ✅ Run as non-root user
RUN addgroup -g 1001 nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# ✅ Use .dockerignore
# .dockerignore:
node_modules
.git
.env
*.md
.github

# ✅ Scan for vulnerabilities
# docker scan myapp:latest

# ✅ Use minimal base images
FROM node:18-alpine  # Not node:18 (full)

# ✅ Don't include secrets
# Use build args or runtime env vars
ARG API_KEY
ENV API_KEY=${API_KEY}
```

### Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - '3000:3000'
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    ports:
      - '5432:5432'
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

volumes:
  postgres_data:
```

## Kubernetes Patterns

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
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
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

### ConfigMap and Secrets

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: info
  MAX_CONNECTIONS: "100"

# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0BkYjU0MzIvbXlkYg==
  api-key: c2tfbGl2ZV9hYmMxMjN4eXo=
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:2.0.0

---
# Service (switch by changing selector)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
  ports:
  - port: 80
    targetPort: 3000
```

### Canary Deployment

```yaml
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable

---
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary

---
# Service routes to both
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp  # Matches both stable and canary
  ports:
  - port: 80
    targetPort: 3000
```

### Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max 2 extra pods during update
      maxUnavailable: 1  # Max 1 pod unavailable during update
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:2.0.0
```

## Database Migration Strategies

### Forward-Only Migrations

```typescript
// ✅ GOOD - Backwards compatible
// Step 1: Add new column (nullable)
await db.schema.alterTable('users', (table) => {
  table.string('phone_number').nullable();
});

// Step 2: Populate data
await db('users').update({
  phone_number: db.raw('contact_info'),
});

// Step 3: Make non-nullable (separate deployment)
await db.schema.alterTable('users', (table) => {
  table.string('phone_number').notNullable().alter();
});

// Step 4: Drop old column (separate deployment)
await db.schema.alterTable('users', (table) => {
  table.dropColumn('contact_info');
});
```

### Zero-Downtime Migrations

```typescript
// Rename column without downtime

// Migration 1: Add new column
await db.schema.alterTable('users', (table) => {
  table.string('email_address').nullable();
});

// Update application code to write to both columns
class User {
  async save() {
    await db('users').update({
      email: this.email,
      email_address: this.email, // Write to both
    });
  }
}

// Migration 2: Backfill data
await db.raw(`
  UPDATE users
  SET email_address = email
  WHERE email_address IS NULL
`);

// Migration 3: Update app to read from new column
class User {
  get email() {
    return this.email_address; // Read from new column
  }
}

// Migration 4: Drop old column
await db.schema.alterTable('users', (table) => {
  table.dropColumn('email');
});
```

## Environment Management

### Environment Configuration

```typescript
// config/environments.ts
interface EnvironmentConfig {
  database: {
    host: string;
    port: number;
    name: string;
  };
  api: {
    baseUrl: string;
    timeout: number;
  };
  features: {
    enableNewFeature: boolean;
  };
}

const environments: Record<string, EnvironmentConfig> = {
  development: {
    database: {
      host: 'localhost',
      port: 5432,
      name: 'myapp_dev',
    },
    api: {
      baseUrl: 'http://localhost:3000',
      timeout: 30000,
    },
    features: {
      enableNewFeature: true,
    },
  },
  staging: {
    database: {
      host: 'staging-db.example.com',
      port: 5432,
      name: 'myapp_staging',
    },
    api: {
      baseUrl: 'https://staging-api.example.com',
      timeout: 10000,
    },
    features: {
      enableNewFeature: true,
    },
  },
  production: {
    database: {
      host: process.env.DB_HOST!,
      port: parseInt(process.env.DB_PORT!),
      name: 'myapp_prod',
    },
    api: {
      baseUrl: 'https://api.example.com',
      timeout: 5000,
    },
    features:  {
      enableNewFeature: false,
    },
  },
};

export const config = environments[process.env.NODE_ENV || 'development'];
```

## Monitoring

### Prometheus Metrics

```typescript
import prometheus from 'prom-client';

// Create metrics
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
});

const httpRequestTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

// Middleware to track metrics
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode.toString())
      .observe(duration);

    httpRequestTotal
      .labels(req.method, req.route?.path || req.path, res.statusCode.toString())
      .inc();
  });

  next();
});

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(await prometheus.register.metrics());
});
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      }
    ]
  }
}
```

### Log Aggregation

```typescript
// Winston logger with JSON format
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'myapp',
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Structured logging
logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
});
```

## Disaster Recovery

### Backup Strategy

```bash
#!/bin/bash
# backup-database.sh

# Configuration
DB_HOST="${DB_HOST}"
DB_NAME="${DB_NAME}"
BACKUP_DIR="/backups"
S3_BUCKET="s3://my-backups"
RETENTION_DAYS=30

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Dump database
pg_dump -h "${DB_HOST}" -U postgres "${DB_NAME}" | gzip > "${BACKUP_FILE}"

# Upload to S3
aws s3 cp "${BACKUP_FILE}" "${S3_BUCKET}/"

# Remove local backup
rm "${BACKUP_FILE}"

# Delete old backups from S3
aws s3 ls "${S3_BUCKET}/" | while read -r line; do
  FILE_DATE=$(echo "$line" | awk '{print $1}')
  FILE_NAME=$(echo "$line" | awk '{print $4}')

  FILE_EPOCH=$(date -d "$FILE_DATE" +%s)
  CURRENT_EPOCH=$(date +%s)
  DAYS_OLD=$(( (CURRENT_EPOCH - FILE_EPOCH) / 86400 ))

  if [ $DAYS_OLD -gt $RETENTION_DAYS ]; then
    aws s3 rm "${S3_BUCKET}/${FILE_NAME}"
  fi
done
```

### Recovery Plan

```markdown
## Disaster Recovery Plan

### RTO (Recovery Time Objective): 4 hours
### RPO (Recovery Point Objective): 1 hour

### Recovery Steps:

1. **Assess the situation**
   - Identify scope of failure
   - Notify stakeholders

2. **Restore database**
   ```bash
   # Download latest backup
   aws s3 cp s3://my-backups/latest.sql.gz /tmp/

   # Restore database
   gunzip -c /tmp/latest.sql.gz | psql -h new-db -U postgres myapp
   ```

3. **Deploy application**
   ```bash
   # Deploy to new infrastructure
   kubectl apply -f k8s/production/

   # Update DNS
   aws route53 change-resource-record-sets ...
   ```

4. **Verify recovery**
   - Run smoke tests
   - Check monitoring dashboards
   - Verify critical features

5. **Post-mortem**
   - Document incident
   - Identify root cause
   - Create action items
```

## When to Use This Skill

Use this skill when:
- Setting up CI/CD pipelines
- Deploying applications
- Managing infrastructure
- Implementing deployment strategies
- Configuring monitoring
- Planning disaster recovery
- Containerizing applications
- Orchestrating with Kubernetes
- Automating workflows
- Scaling infrastructure

---

**Remember**: DevOps is about automation, reliability, and continuous improvement. Invest in your infrastructure and deployment processes to enable faster, safer releases.
