---
name: cicd-patterns
version: "1.0"
description: >
  Implement CI/CD pipelines with GitHub Actions and Cloud Build for GCP deployments.
  PROACTIVELY activate for: (1) setting up GitHub Actions workflows for GCP, (2) configuring Cloud Build pipelines, (3) implementing Workload Identity federation.
  Triggers: "cicd", "github actions", "cloud build"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# CI/CD Patterns Skill

## Metadata (Tier 1)

**Keywords**: cicd, github actions, cloud build, pipeline, workflow, automation, deploy

**File Patterns**: .github/workflows/*.yml, cloudbuild.yaml, .gitlab-ci.yml

**Modes**: deployment

---

## Instructions (Tier 2)

### Standard Pipeline Stages

1. **Lint & Format** - Code quality validation
2. **Test** - Unit and integration tests
3. **Security Scan** - Vulnerability detection
4. **Build** - Container image creation
5. **Image Scan** - Container vulnerability scan
6. **Deploy Staging** - Automated deployment
7. **Deploy Production** - Manual approval + deployment

### GitHub Actions with Workload Identity

#### Setup Workload Identity (One-time)
```bash
gcloud iam workload-identity-pools create "github-pool" \
  --project=PROJECT --location=global

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project=PROJECT --location=global \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"
```

#### Workflow Authentication
```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
    service_account: 'deployer@PROJECT.iam.gserviceaccount.com'
```

#### Deploy Step
```yaml
- uses: google-github-actions/deploy-cloudrun@v2
  with:
    service: my-service
    region: us-central1
    image: ${{ env.IMAGE }}
```

### Cloud Build Pipeline

```yaml
steps:
- id: 'test'
  name: 'python:3.13'
  entrypoint: 'pytest'
  args: ['--cov=src']

- id: 'build'
  name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', '$_IMAGE', '.']

- id: 'scan'
  name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: 'bash'
  args:
  - '-c'
  - |
    gcloud artifacts docker images scan $_IMAGE --remote
    # Check for CRITICAL vulnerabilities

- id: 'deploy'
  name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  args:
  - 'run'
  - 'deploy'
  - '$_SERVICE'
  - '--image=$_IMAGE'
  - '--region=$_REGION'

images: ['$_IMAGE']
```

### Security Best Practices

- Use Workload Identity (no service account keys)
- Scan images for vulnerabilities
- Run tests before deployment
- Use least-privilege service accounts
- Store secrets in Secret Manager
- Enable branch protection on main
- Require approvals for production

### Anti-Patterns
- Service account keys in secrets
- No vulnerability scanning
- No test stage
- Direct push to production without validation
- Secrets in environment variables
