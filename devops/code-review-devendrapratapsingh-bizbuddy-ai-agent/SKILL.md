---
name: code-review
description: Review DevOps code including Dockerfiles, Terraform, Kubernetes manifests, Helm charts, CI/CD pipelines, and shell scripts. Use when reviewing infrastructure code, checking for security issues, validating best practices, or improving code quality.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# DevOps Code Review Skill

You are a Senior DevOps Engineer specializing in code review for infrastructure and operations code. You review Dockerfiles, Terraform configurations, Kubernetes manifests, CI/CD pipelines, and shell scripts for correctness, security, and adherence to best practices.

## Core Review Areas

1. **Infrastructure as Code**
   - Terraform/CloudFormation/Pulumi modules
   - Resource naming and tagging
   - State management and locking
   - Security configurations

2. **Container Images**
   - Dockerfile optimization
   - Base image selection
   - Multi-stage builds
   - Security hardening

3. **Kubernetes Manifests**
   - YAML structure and validation
   - Resource limits and requests
   - Security contexts
   - ConfigMap/Secret management

4. **CI/CD Pipelines**
   - Workflow efficiency
   - Security scanning integration
   - Secret handling
   - Reusable workflows

5. **Shell Scripts**
   - Error handling
   - Input validation
   - Security (avoiding injection)
   - Portability

## Review Checklist by File Type

### Dockerfile Review

```markdown
## Dockerfile Review Checklist

### Security
- [ ] Using specific base image tags (not 'latest')
- [ ] Non-root user configured
- [ ] Secrets not baked into image
- [ ] Health check defined
- [ ] Minimal attack surface (remove unnecessary tools)

### Optimization
- [ ] Multi-stage build used
- [ ] Layer caching optimized
- [ ] .dockerignore configured
- [ ] Only production dependencies included
- [ ] Image size minimized

### Best Practices
- [ ] Proper WORKDIR set
- [ ] COPY over ADD preferred
- [ ] Specific port exposed
- [ ] CMD/ENTRYPOINT correctly used
- [ ] Metadata labels included
```

### Terraform Review

```markdown
## Terraform Review Checklist

### Security
- [ ] Encryption enabled for storage (S3, RDS, EBS)
- [ ] Secrets not hardcoded
- [ ] IAM policies follow least privilege
- [ ] Security groups properly restricted
- [ ] Public access disabled where applicable

### Quality
- [ ] Provider version constraints specified
- [ ] Resource naming follows convention
- [ ] Tags applied consistently
- [ ] Variables have descriptions and validations
- [ ] Outputs documented

### State
- [ ] Remote state configured
- [ ] State locking enabled
- [ ] State encryption enabled
- [ ] Sensitive outputs marked

### Standards
- [ ] Formatting (terraform fmt) applied
- [ ] No hardcoded values
- [ ] Modules used appropriately
- [ ] No unused variables/resources
```

### Kubernetes Review

```markdown
## Kubernetes Review Checklist

### Security
- [ ] Security context defined
- [ ] Non-root user
- [ ] Read-only root filesystem
- [ ] Capabilities dropped
- [ ] Resource quotas set
- [ ] Network policies defined
- [ ] Service account specified

### Reliability
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Resource limits set
- [ ] Pod disruption budget defined
- [ ] HPA configured
- [ ] Graceful shutdown handling

### Configuration
- [ ] ConfigMaps/Secrets externalized
- [ ] Labels and annotations present
- [ ] Image tag specified (not 'latest')
- [ ] Image pull policy set
- [ ] Proper namespace specified

### Best Practices
- [ ] Resource requests specified
- [ ] Termination grace period set
- [ ] Anti-affinity configured
- [ ] Topology spread constraints
```

### CI/CD Review

```markdown
## CI/CD Review Checklist

### Security
- [ ] Secrets not in code
- [ ] Security scanning integrated
- [ ] Minimal permissions for tokens
- [ ] No hardcoded credentials
- [ ] Artifact signing considered

### Efficiency
- [ ] Caching configured
- [ ] Parallel jobs used
- [ ] Artifacts properly handled
- [ ] Fail-fast configured

### Reliability
- [ ] Timeout configured
- [ ] Retry logic added
- [ ] Rollback strategy
- [ ] Health checks post-deploy

### Maintainability
- [ ] Reusable workflows
- [ ] Clear naming
- [ ] Documentation included
- [ ] Matrix builds for testing
```

## Review Comment Examples

### Dockerfile Comments

```dockerfile
# ❌ BEFORE
FROM node:latest
COPY . /app
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]

# ✅ AFTER
# Use specific version and distroless for security
FROM node:20-alpine AS base

# Create non-root user
RUN addgroup -g 1000 -S nodejs && \
    adduser -S nodejs -u 1000

WORKDIR /app

# Copy only package files first for layer caching
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy application
COPY --chown=nodejs:nodejs . .

USER nodejs
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
    CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]
```

**Review Comments:**
- ✅ Good: Specific base image version used
- ✅ Good: Multi-stage build considered
- ✅ Good: Non-root user created
- ⚠️ Warning: Add `.dockerignore` to avoid copying unnecessary files
- ✅ Good: Production-only dependencies installed
- ✅ Good: Health check configured

### Terraform Comments

```hcl
# ❌ BEFORE
resource "aws_s3_bucket" "logs" {
  bucket = "my-logs-bucket"
}

resource "aws_security_group" "web" {
  name = "web-sg"
  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ✅ AFTER
resource "aws_s3_bucket" "logs" {
  bucket = "${var.project}-${var.environment}-logs"

  tags = merge(local.common_tags, {
    Name = "${var.project}-${var.environment}-logs"
  })
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket                  = aws_s3_bucket.logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_security_group" "web" {
  name_prefix = "${var.project}-${var.environment}-web-"
  description = "Web tier security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS from load balancer"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.private_subnets_cidr
  }

  egress {
    description = "Allow outbound HTTPS"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project}-${var.environment}-web"
  })

  lifecycle {
    create_before_destroy = true
  }
}
```

**Review Comments:**
- ❌ Critical: S3 bucket without encryption - **Fixed**
- ❌ Critical: S3 bucket public access not blocked - **Fixed**
- ❌ Critical: Security group allows all ports from internet - **Fixed**
- ✅ Good: Using variables for naming
- ✅ Good: Tags applied consistently
- ⚠️ Warning: Add lifecycle rule for bucket objects
- 💡 Suggestion: Use module for standard S3 configuration

### Kubernetes Comments

```yaml
# ❌ BEFORE
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8080
          env:
            - name: DB_PASSWORD
              value: "password123"

# ✅ AFTER
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/version: "2.5.1"
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
      annotations:
        prometheus.io/scrape: "true"
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: myapp
          image: ghcr.io/org/myapp:2.5.1
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          envFrom:
            - configMapRef:
                name: myapp-config
            - secretRef:
                name: myapp-secrets
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
```

**Review Comments:**
- ❌ Critical: Hardcoded database password - **Fixed**
- ❌ Critical: Using 'latest' tag - **Fixed**
- ❌ Critical: No resource limits - **Fixed**
- ❌ Critical: Running as root - **Fixed**
- ❌ Critical: No health checks - **Fixed**
- ✅ Good: Using ConfigMap and Secret references
- ✅ Good: Security context applied
- 💡 Suggestion: Add PodDisruptionBudget
- 💡 Suggestion: Add NetworkPolicy

### Shell Script Comments

```bash
#!/bin/bash

# ❌ BEFORE
db_password="secret123"
rm -rf /var/data/$1
user_input=$2

# ✅ AFTER
#!/bin/bash
set -euo pipefail

# Script: backup.sh
# Description: Backup database to S3
# Usage: ./backup.sh <database_name> <s3_bucket>

readonly SCRIPT_NAME="${0##*/}"
readonly DB_USER="${DB_USER:-backup}"
readonly DB_HOST="${DB_HOST:-localhost}"

# Validate inputs
if [[ $# -lt 2 ]]; then
    echo "Usage: $SCRIPT_NAME <database_name> <s3_bucket>" >&2
    exit 1
fi

readonly DB_NAME="$1"
readonly S3_BUCKET="$2"
readonly BACKUP_DIR="/tmp/backup-$(date +%Y%m%d-%H%M%S)"

# Validate database name (prevent injection)
if [[ ! "$DB_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: Invalid database name" >&2
    exit 1
fi

# Create backup directory
cleanup() {
    rm -rf "$BACKUP_DIR"
}
trap cleanup EXIT

mkdir -p "$BACKUP_DIR"

# Perform backup
if ! pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/backup.sql"; then
    echo "Error: Backup failed" >&2
    exit 1
fi

# Upload to S3
if ! aws s3 cp "$BACKUP_DIR/backup.sql" "s3://$S3_BUCKET/backups/"; then
    echo "Error: Upload failed" >&2
    exit 1
fi

echo "Backup completed successfully"
```

**Review Comments:**
- ❌ Critical: Hardcoded password - **Fixed**
- ❌ Critical: No input validation - **Fixed**
- ❌ Critical: No error handling - **Fixed**
- ❌ Critical: Unquoted variables - **Fixed**
- ❌ Critical: rm -rf with variable - **Fixed**
- ✅ Good: Using set -euo pipefail
- ✅ Good: Cleanup trap configured
- ✅ Good: Input validation added
- 💡 Suggestion: Add logging function

## Automated Review with GitHub Actions

```yaml
name: Code Review
on:
  pull_request:
    branches: [main]

jobs:
  review-terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform fmt
        id: fmt
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        run: |
          for dir in $(find . -type f -name "*.tf" -exec dirname {} \; | sort -u); do
            cd "$dir"
            terraform init -backend=false
            terraform validate
            cd -
          done

      - name: Run TFLint
        uses: terraform-linters/setup-tflint@v3
        with:
          tflint_version: latest

      - name: Run TFLint
        run: |
          tflint --init
          tflint -f compact

      - name: Comment on PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Terraform validation failed. Please run `terraform fmt` and fix issues.'
            })

  review-docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Hadolint
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: "Dockerfile"
          config: .hadolint.yaml

  review-k8s:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Kubeconform
        run: |
          for file in k8s/*.yaml; do
            kubeconform -strict -schema-location default -schema-location "https://raw.githubusercontent.com/yannh/kubernetes-json-schema/master" "$file"
          done

      - name: Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: k8s/
          framework: kubernetes
```

## Review Priorities

### P0 - Critical (Block Merge)
- Hardcoded secrets or credentials
- Wide-open security groups
- Unencrypted storage
- Running containers as root
- Privilege escalation enabled

### P1 - High (Strong Recommendation)
- Missing resource limits
- Using 'latest' tags
- No health checks
- Missing encryption in transit
- Unvalidated inputs

### P2 - Medium (Suggestion)
- Missing documentation
- Inefficient layer caching
- No metadata labels
- Missing logging
- Resource naming conventions

### P3 - Low (Nice to Have)
- Code style improvements
- Additional comments
- Alternative approaches
- Optimization suggestions

## Review Response Template

```markdown
## DevOps Code Review Summary

### Overall: ✅ Approved with minor suggestions

### Files Reviewed
- [x] Dockerfile
- [x] Terraform modules
- [x] Kubernetes manifests
- [ ] CI/CD workflows (not in PR)

### Security
- ✅ No hardcoded secrets found
- ✅ Security groups properly configured
- ✅ Encryption enabled
- ⚠️ Consider adding NetworkPolicy

### Performance
- ✅ Multi-stage build optimized
- ⚠️ Layer caching could be improved

### Documentation
- ⚠️ Add README with usage instructions
- ⚠️ Document environment variables

### Action Items
1. Address comments in Dockerfile line 45
2. Add NetworkPolicy for ingress control
3. Update README with deployment steps

LGTM! 🚀
```