---
name: gcp-nodejs-cicd
description: Generate CI/CD pipelines for Node.js and Angular applications on GCP with Cloud Build and GKE deployment. Use when creating or updating deployment pipelines for Node.js services, Express APIs, NestJS applications, or Angular frontends targeting Google Cloud Platform.
---

# GCP Node.js CI/CD Pipeline Generation

This Skill generates production-ready CI/CD pipelines for Node.js and Angular applications deployed to Google Kubernetes Engine (GKE) via Cloud Build.

## When to Use This Skill

- Creating new Node.js or Angular services
- Setting up deployment pipelines
- Configuring multi-environment deployments (dev, staging, production)
- Implementing security scanning and quality gates
- Deploying containerized applications to GKE

## Organizational Context

### Build Standards
- **Node.js versions**: 18.x, 20.x (LTS only)
- **Package manager**: npm (lock file required)
- **Build process**: Multi-stage Docker builds
- **Test coverage**: Minimum 80% for production deployments
- **Linting**: ESLint with organizational config

### Security Requirements
- **Dependency scanning**: Snyk (0 critical vulnerabilities allowed)
- **Container scanning**: Trivy (no high/critical CVEs)
- **SAST**: SonarQube (Quality Gate must pass)
- **SBOM**: Generate and upload to Artifact Registry
- **Secrets**: Must use GCP Secret Manager (never hardcoded)

### Deployment Strategies
- **Development**: Auto-deploy on commit
- **Staging**: Manual approval required
- **Production**: Canary deployment (5% → 50% → 100%)
- **Rollback**: Automatic on health check failures or error rate >5%

## Instructions

### Step 1: Analyze Service Context

First, determine the service type and requirements by checking:

```bash
# Check package.json for framework
cat package.json | jq '.dependencies'

# Identify service type
if [ -f "angular.json" ]; then
  SERVICE_TYPE="angular"
elif grep -q "express" package.json; then
  SERVICE_TYPE="express"
elif grep -q "@nestjs" package.json; then
  SERVICE_TYPE="nestjs"
else
  SERVICE_TYPE="nodejs-generic"
fi
```

### Step 2: Generate Cloud Build Configuration

Use the appropriate template from `templates/cloudbuild/`:

**For Node.js services:**
```yaml
# See templates/cloudbuild/nodejs-service.yaml
steps:
  - name: 'node:${NODE_VERSION}'
    entrypoint: npm
    args: ['ci']
  
  - name: 'node:${NODE_VERSION}'
    entrypoint: npm
    args: ['run', 'build']
  
  - name: 'node:${NODE_VERSION}'
    entrypoint: npm
    args: ['test']
    
  # Security scanning - see templates/security/
  # Docker build - see templates/docker/
  # GKE deployment - see templates/kubernetes/
```

**For Angular applications:**
```yaml
# See templates/cloudbuild/angular-app.yaml
# Includes ng build with optimization flags
# Static asset handling
# Environment-specific configurations
```

### Step 3: Implement Security Scanning

Always include all three security scans:

```yaml
# Snyk dependency scan
- name: 'snyk/snyk:node'
  entrypoint: 'sh'
  args:
    - '-c'
    - 'snyk test --severity-threshold=high || exit 1'
  secretEnv: ['SNYK_TOKEN']

# Trivy container scan
- name: 'aquasec/trivy'
  args: ['image', '--severity', 'HIGH,CRITICAL', '${IMAGE_NAME}']

# SonarQube SAST
- name: 'sonarsource/sonar-scanner-cli'
  args: ['sonar-scanner', '-Dsonar.qualitygate.wait=true']
```

Use validator at `validators/security-policy.rego` to verify all scans are present.

### Step 4: Generate Kubernetes Manifests

Create deployment, service, and HPA configurations:

```yaml
# See templates/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  template:
    spec:
      containers:
      - name: ${SERVICE_NAME}
        image: ${IMAGE_NAME}
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
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Step 5: Configure Multi-Environment Deployment

Set up deployment strategy per environment:

**Development:**
- Auto-deploy on every commit
- No approval required
- Rolling update strategy

**Staging:**
- Manual approval required (team lead)
- Smoke tests must pass
- Rolling update strategy

**Production:**
- Two approvals required (team lead + platform lead)
- Canary deployment strategy
- Automated rollback on metrics degradation

### Step 6: Add Monitoring and Observability

Include Cloud Monitoring configuration:

```yaml
# Metrics to collect
metrics:
  - http_requests_total
  - http_request_duration_seconds
  - http_errors_total
  
# Alerts to configure
alerts:
  - error_rate_high (>5% for 5 minutes)
  - latency_p99_high (>2s for 5 minutes)
  - pod_restart_frequent (>3 in 10 minutes)
```

### Step 7: Generate Documentation

Create comprehensive documentation:

```markdown
# Service Name

## CI/CD Pipeline

This service uses the following deployment pipeline:
- Build: Multi-stage Docker with Node.js ${VERSION}
- Test: Unit tests with 80%+ coverage
- Security: Snyk + Trivy + SonarQube
- Deploy: Canary to GKE with automated rollback

## Deployment

**Development:**
- Auto-deployed on commit to main
- URL: https://dev.example.com

**Production:**
- Requires 2 approvals
- Canary deployment (5% → 50% → 100%)
- URL: https://api.example.com

## Rollback

If deployment fails:
```bash
platform-cli rollback payment-api --to-version previous
```
```

## Validation Rules

Before completing generation, validate using `validators/security-policy.rego`:

```rego
# Validation checks
package cloudbuild

# Rule: Security scans required
deny[msg] {
  not input.steps[_].name == "snyk/snyk:node"
  msg = "Snyk dependency scan is required"
}

deny[msg] {
  not input.steps[_].name == "aquasec/trivy"
  msg = "Trivy container scan is required"
}

# Rule: Secrets must be in Secret Manager
deny[msg] {
  input.steps[_].args[_] contains "password"
  msg = "Hardcoded secrets detected. Use Secret Manager."
}

# Rule: Production requires approval
deny[msg] {
  input.environment == "production"
  not input.approvals
  msg = "Production deployments require approval"
}
```

## Examples

For complete working examples, see:
- `examples/payment-service/` - Express API with PCI compliance
- `examples/user-api/` - NestJS service with authentication
- `examples/frontend-app/` - Angular SPA with SSR

## Troubleshooting

**Build fails with "npm ci" error:**
- Ensure package-lock.json is committed
- Check Node.js version matches package.json engines

**Security scan fails:**
- Review Snyk dashboard for vulnerabilities
- Update dependencies to patch CVEs
- Request exception if no patch available

**Deployment fails:**
- Check GKE cluster has sufficient resources
- Verify namespace exists
- Confirm image was pushed to Artifact Registry

**Canary rollback triggered:**
- Check Cloud Monitoring for error rates
- Review logs in Cloud Logging
- Validate health check endpoints

## Additional Resources

- [Cloud Build Docs](https://cloud.google.com/build/docs)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Organizational Build Standards](context/build-standards.yaml)
- [Security Requirements](context/security-requirements.yaml)
