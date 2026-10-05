---
name: cd-pipeline-generator
description: Generates continuous deployment pipelines for GitHub Actions, GitLab CI, Jenkins, and ArgoCD with deployment strategies, environment promotion, and rollback.
---

# CD Pipeline Generator

Specialized skill for generating production-grade continuous deployment pipelines across major CI/CD platforms. This skill produces complete, ready-to-use pipeline configurations that implement industry-standard deployment strategies, environment promotion workflows, secret management, health checks, and automated rollback triggers. Rather than providing generic templates, it tailors each pipeline to the target platform's idioms and best practices while maintaining consistent deployment safety guarantees.

## When to Use This Skill

Use this skill for:

- Generating a new continuous deployment pipeline from scratch for any major platform
- Converting an existing CI-only pipeline into a full CI/CD workflow with deployment stages
- Implementing blue-green, canary, or rolling deployment strategies in pipeline configuration
- Setting up environment promotion chains (dev, staging, production) with approval gates
- Configuring secret injection and credential management within deployment pipelines
- Adding health check verification and automated rollback triggers to existing pipelines
- Creating multi-environment deployment matrices for microservice architectures
- Integrating ArgoCD GitOps workflows with existing CI pipelines

**Trigger phrases**: "deployment pipeline", "CD pipeline", "continuous deployment", "deploy to production", "blue-green deployment", "canary deployment", "rolling update pipeline", "environment promotion", "deployment gates", "ArgoCD pipeline", "GitOps deployment", "deploy workflow"

## What This Skill Does

This skill follows a structured methodology to produce deployment pipelines:

1. **Platform Assessment**: Identifies the target CI/CD platform and its native deployment primitives (GitHub Environments, GitLab environments, Jenkins stages, ArgoCD Application resources).

2. **Strategy Selection**: Matches the deployment strategy (blue-green, canary, rolling) to the infrastructure target (Kubernetes, cloud VMs, serverless, static hosting) and produces the appropriate configuration.

3. **Environment Chain Design**: Builds a promotion workflow where artifacts flow through dev, staging, and production with configurable gates (manual approval, automated tests, metric thresholds) at each transition.

4. **Secret Integration**: Wires platform-native secret stores (GitHub Secrets, GitLab CI variables, Jenkins credentials, Kubernetes Secrets, Vault) into the pipeline without exposing values in logs or artifacts.

5. **Health Verification**: Adds post-deployment health checks (HTTP probes, smoke tests, metric queries) that feed into automated rollback decisions.

6. **Rollback Configuration**: Implements automatic rollback triggers based on health check failures, error rate thresholds, or manual intervention, ensuring every deployment can be reversed safely.

7. **Output Generation**: Produces complete pipeline files with inline comments explaining each decision, plus a companion README section documenting how to operate the pipeline.

## Instructions

### Step 1: Gather Deployment Requirements

Before generating any pipeline configuration, collect the following information:

```
Target Platform:        [GitHub Actions | GitLab CI | Jenkins | ArgoCD]
Infrastructure Target:  [Kubernetes | AWS ECS | Azure App Service | GCP Cloud Run | VMs | Static]
Deployment Strategy:    [Blue-Green | Canary | Rolling | Recreate]
Environments:           [dev | staging | production] (list all)
Approval Gates:         [manual | automated | metric-based] per environment
Container Registry:     [GHCR | ECR | GCR | ACR | DockerHub | self-hosted]
Secret Store:           [platform-native | HashiCorp Vault | AWS Secrets Manager | Azure Key Vault]
Health Check Type:      [HTTP probe | smoke test | metric query | all]
Rollback Trigger:       [health check failure | error rate | latency | manual]
```

### Step 2: Generate the Pipeline Skeleton

Start with the platform-appropriate file structure:

**GitHub Actions** (`.github/workflows/deploy.yml`):

```yaml
name: Continuous Deployment

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options:
          - dev
          - staging
          - production
      skip_approval:
        description: "Skip manual approval (dev only)"
        required: false
        type: boolean
        default: false

permissions:
  contents: read
  packages: read
  deployments: write
  id-token: write

concurrency:
  group: deploy-${{ inputs.environment || 'dev' }}
  cancel-in-progress: false

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

**GitLab CI** (`.gitlab-ci.yml` deployment stages):

```yaml
stages:
  - build
  - test
  - publish
  - deploy-dev
  - verify-dev
  - deploy-staging
  - verify-staging
  - approve-production
  - deploy-production
  - verify-production
  - rollback

variables:
  REGISTRY: $CI_REGISTRY
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA
  KUBE_NAMESPACE_DEV: app-dev
  KUBE_NAMESPACE_STAGING: app-staging
  KUBE_NAMESPACE_PROD: app-prod
```

**Jenkins** (`Jenkinsfile`):

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Target deployment environment')
        booleanParam(name: 'SKIP_APPROVAL', defaultValue: false, description: 'Skip manual approval for dev')
        string(name: 'IMAGE_TAG', defaultValue: '', description: 'Override image tag (defaults to build number)')
    }

    environment {
        REGISTRY = 'ghcr.io'
        IMAGE_NAME = 'org/app'
        IMAGE_TAG = "${params.IMAGE_TAG ?: env.BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig')
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Validate') {
            steps {
                script {
                    echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} to ${params.ENVIRONMENT}"
                }
            }
        }
    }
}
```

**ArgoCD** (`argocd/application.yaml`):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: deployments
    notifications.argoproj.io/subscribe.on-sync-failed.slack: deployments
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/org/app-manifests.git
    targetRevision: main
    path: overlays/production
    kustomize:
      images:
        - ghcr.io/org/app
  destination:
    server: https://kubernetes.default.svc
    namespace: app-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 1m
  revisionHistoryLimit: 10
```

### Step 3: Implement Deployment Strategies

#### Blue-Green Deployment

Blue-green uses two identical environments. Traffic switches atomically from the current (blue) to the new (green) after verification.

**GitHub Actions (Kubernetes)**:

```yaml
  deploy-green:
    runs-on: ubuntu-latest
    environment:
      name: production-green
      url: https://green.example.com
    steps:
      - name: Configure kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: "v1.29.0"

      - name: Deploy green environment
        run: |
          # Deploy to the inactive color
          ACTIVE_COLOR=$(kubectl get svc myapp-active -n production \
            -o jsonpath='{.spec.selector.color}' 2>/dev/null || echo "blue")

          if [ "$ACTIVE_COLOR" = "blue" ]; then
            TARGET_COLOR="green"
          else
            TARGET_COLOR="blue"
          fi

          echo "Active: $ACTIVE_COLOR, Deploying to: $TARGET_COLOR"
          echo "TARGET_COLOR=$TARGET_COLOR" >> "$GITHUB_ENV"

          kubectl set image deployment/myapp-${TARGET_COLOR} \
            app=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
            -n production

          kubectl rollout status deployment/myapp-${TARGET_COLOR} \
            -n production --timeout=300s

      - name: Run smoke tests against green
        run: |
          GREEN_URL="http://myapp-${TARGET_COLOR}.production.svc.cluster.local:8080"
          for i in $(seq 1 10); do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$GREEN_URL/health")
            if [ "$STATUS" = "200" ]; then
              echo "Health check passed (attempt $i)"
              break
            fi
            if [ "$i" -eq 10 ]; then
              echo "Health check failed after 10 attempts"
              exit 1
            fi
            sleep 5
          done

      - name: Switch traffic to green
        run: |
          kubectl patch svc myapp-active -n production \
            -p "{\"spec\":{\"selector\":{\"color\":\"${TARGET_COLOR}\"}}}"
          echo "Traffic switched to $TARGET_COLOR"

      - name: Verify live traffic
        run: |
          sleep 10
          LIVE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://app.example.com/health")
          if [ "$LIVE_STATUS" != "200" ]; then
            echo "Live verification failed, initiating rollback"
            ROLLBACK_COLOR=$( [ "$TARGET_COLOR" = "green" ] && echo "blue" || echo "green" )
            kubectl patch svc myapp-active -n production \
              -p "{\"spec\":{\"selector\":{\"color\":\"${ROLLBACK_COLOR}\"}}}"
            exit 1
          fi
```

#### Canary Deployment

Canary gradually shifts traffic to the new version, monitoring metrics at each step before proceeding.

**GitHub Actions (with Flagger on Kubernetes)**:

```yaml
  deploy-canary:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Update canary image
        run: |
          kubectl set image deployment/myapp \
            app=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
            -n production

      - name: Monitor canary progression
        run: |
          # Flagger manages the canary automatically; we poll for completion
          TIMEOUT=600
          INTERVAL=15
          ELAPSED=0

          while [ $ELAPSED -lt $TIMEOUT ]; do
            STATUS=$(kubectl get canary myapp -n production \
              -o jsonpath='{.status.phase}')

            case "$STATUS" in
              "Succeeded")
                echo "Canary promotion succeeded"
                exit 0
                ;;
              "Failed")
                echo "Canary promotion failed, automatic rollback triggered"
                exit 1
                ;;
              "Progressing")
                WEIGHT=$(kubectl get canary myapp -n production \
                  -o jsonpath='{.status.canaryWeight}')
                echo "Canary progressing: ${WEIGHT}% traffic"
                ;;
            esac

            sleep $INTERVAL
            ELAPSED=$((ELAPSED + INTERVAL))
          done

          echo "Canary timed out after ${TIMEOUT}s"
          exit 1
```

**Flagger Canary Resource**:

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 8080
    targetPort: 8080
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 30s
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
    webhooks:
      - name: smoke-test
        type: pre-rollout
        url: http://flagger-loadtester.test/
        timeout: 60s
        metadata:
          type: bash
          cmd: "curl -s http://myapp-canary.production:8080/health | grep ok"
```

#### Rolling Update

Rolling update replaces pods incrementally, maintaining availability throughout the process.

**Kubernetes Deployment Configuration**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: "${IMAGE_TAG}"
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: app
          image: ghcr.io/org/app:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 5
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]
```

### Step 4: Configure Environment Promotion

Define the promotion chain with appropriate gates at each stage:

**GitHub Actions Environment Promotion**:

```yaml
jobs:
  deploy-dev:
    runs-on: ubuntu-latest
    environment:
      name: dev
      url: https://dev.example.com
    steps:
      - name: Deploy to dev
        uses: ./.github/actions/deploy
        with:
          environment: dev
          image_tag: ${{ needs.build.outputs.image_tag }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_DEV }}

  verify-dev:
    needs: deploy-dev
    runs-on: ubuntu-latest
    steps:
      - name: Run integration tests
        run: |
          npm run test:integration -- --base-url=https://dev.example.com

      - name: Run E2E tests
        run: |
          npm run test:e2e -- --base-url=https://dev.example.com

  deploy-staging:
    needs: verify-dev
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy to staging
        uses: ./.github/actions/deploy
        with:
          environment: staging
          image_tag: ${{ needs.build.outputs.image_tag }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

  verify-staging:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run performance tests
        run: |
          k6 run tests/performance/load-test.js \
            --env BASE_URL=https://staging.example.com \
            --out json=results.json

      - name: Check performance thresholds
        run: |
          python scripts/check_perf_thresholds.py results.json \
            --p95-latency 200 \
            --error-rate 0.01

  deploy-production:
    needs: verify-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Deploy to production
        uses: ./.github/actions/deploy
        with:
          environment: production
          image_tag: ${{ needs.build.outputs.image_tag }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
          strategy: blue-green
```

**Reusable Deploy Composite Action** (`.github/actions/deploy/action.yml`):

```yaml
name: "Deploy"
description: "Deploy application to a Kubernetes environment"

inputs:
  environment:
    description: "Target environment"
    required: true
  image_tag:
    description: "Container image tag to deploy"
    required: true
  kubeconfig:
    description: "Base64-encoded kubeconfig"
    required: true
  strategy:
    description: "Deployment strategy"
    required: false
    default: "rolling"

runs:
  using: "composite"
  steps:
    - name: Set up kubectl
      uses: azure/setup-kubectl@v4
      with:
        version: "v1.29.0"

    - name: Configure cluster access
      shell: bash
      run: |
        echo "${{ inputs.kubeconfig }}" | base64 -d > /tmp/kubeconfig
        echo "KUBECONFIG=/tmp/kubeconfig" >> "$GITHUB_ENV"

    - name: Apply manifests
      shell: bash
      run: |
        kustomize build "k8s/overlays/${{ inputs.environment }}" | \
          envsubst | kubectl apply -f -
      env:
        IMAGE_TAG: ${{ inputs.image_tag }}

    - name: Wait for rollout
      shell: bash
      run: |
        kubectl rollout status deployment/myapp \
          -n "app-${{ inputs.environment }}" \
          --timeout=300s

    - name: Verify deployment health
      shell: bash
      run: |
        RETRIES=12
        for i in $(seq 1 $RETRIES); do
          STATUS=$(kubectl get deployment myapp \
            -n "app-${{ inputs.environment }}" \
            -o jsonpath='{.status.conditions[?(@.type=="Available")].status}')
          if [ "$STATUS" = "True" ]; then
            echo "Deployment healthy"
            exit 0
          fi
          echo "Waiting for deployment health (attempt $i/$RETRIES)"
          sleep 10
        done
        echo "Deployment health check timed out"
        exit 1
```

### Step 5: Configure Secret Management

**GitHub Actions with OIDC and AWS Secrets Manager**:

```yaml
  deploy-with-secrets:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy
          aws-region: us-east-1

      - name: Fetch deployment secrets
        run: |
          # Retrieve secrets and create Kubernetes secret
          DB_PASSWORD=$(aws secretsmanager get-secret-value \
            --secret-id prod/db-password \
            --query SecretString --output text)

          API_KEY=$(aws secretsmanager get-secret-value \
            --secret-id prod/api-key \
            --query SecretString --output text)

          kubectl create secret generic app-secrets \
            --from-literal=db-password="$DB_PASSWORD" \
            --from-literal=api-key="$API_KEY" \
            -n production \
            --dry-run=client -o yaml | kubectl apply -f -
```

**GitLab CI with Vault**:

```yaml
deploy-production:
  stage: deploy-production
  image: alpine/k8s:1.29.0
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DATABASE_PASSWORD:
      vault: production/database/password@secret
      file: false
    API_KEY:
      vault: production/api/key@secret
      file: false
  script:
    - kubectl create secret generic app-secrets
        --from-literal=db-password="$DATABASE_PASSWORD"
        --from-literal=api-key="$API_KEY"
        -n $KUBE_NAMESPACE_PROD
        --dry-run=client -o yaml | kubectl apply -f -
    - kustomize build k8s/overlays/production | kubectl apply -f -
  environment:
    name: production
    url: https://app.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

### Step 6: Add Health Checks and Rollback Triggers

**Post-Deployment Health Verification Script** (`scripts/verify-deployment.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

ENDPOINT="${1:?Usage: verify-deployment.sh <endpoint> <namespace> <deployment>}"
NAMESPACE="${2:?Missing namespace}"
DEPLOYMENT="${3:?Missing deployment}"
MAX_RETRIES="${4:-20}"
RETRY_INTERVAL="${5:-15}"

echo "Verifying deployment: $DEPLOYMENT in $NAMESPACE"
echo "Health endpoint: $ENDPOINT"

# Phase 1: Kubernetes rollout status
echo "--- Phase 1: Rollout Status ---"
if ! kubectl rollout status "deployment/$DEPLOYMENT" -n "$NAMESPACE" --timeout=300s; then
  echo "FAIL: Rollout did not complete"
  kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE"
  exit 1
fi

# Phase 2: HTTP health checks
echo "--- Phase 2: HTTP Health Checks ---"
CONSECUTIVE_SUCCESS=0
REQUIRED_SUCCESSES=3

for i in $(seq 1 "$MAX_RETRIES"); do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$ENDPOINT/health" || echo "000")

  if [ "$HTTP_STATUS" = "200" ]; then
    CONSECUTIVE_SUCCESS=$((CONSECUTIVE_SUCCESS + 1))
    echo "Health check passed ($CONSECUTIVE_SUCCESS/$REQUIRED_SUCCESSES) [attempt $i]"
    if [ "$CONSECUTIVE_SUCCESS" -ge "$REQUIRED_SUCCESSES" ]; then
      echo "Health verification complete"
      break
    fi
  else
    CONSECUTIVE_SUCCESS=0
    echo "Health check returned $HTTP_STATUS [attempt $i/$MAX_RETRIES]"
  fi

  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "FAIL: Health checks did not pass after $MAX_RETRIES attempts"
    echo "Initiating automatic rollback"
    kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE"
    exit 1
  fi

  sleep "$RETRY_INTERVAL"
done

# Phase 3: Readiness probe verification
echo "--- Phase 3: Pod Readiness ---"
READY_PODS=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.status.readyReplicas}')
DESIRED_PODS=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}')

if [ "$READY_PODS" != "$DESIRED_PODS" ]; then
  echo "FAIL: Only $READY_PODS/$DESIRED_PODS pods ready"
  kubectl rollout undo "deployment/$DEPLOYMENT" -n "$NAMESPACE"
  exit 1
fi

echo "SUCCESS: All $READY_PODS/$DESIRED_PODS pods ready and healthy"
```

**GitHub Actions Rollback Job**:

```yaml
  rollback:
    if: failure() && needs.deploy-production.result == 'failure'
    needs: [deploy-production, verify-production]
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          kubectl rollout undo deployment/myapp -n production
          kubectl rollout status deployment/myapp -n production --timeout=300s

      - name: Notify rollback
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment rolled back",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Rollback* triggered for `${{ github.sha }}`\nPrevious version restored. <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View run>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_DEPLOY_WEBHOOK }}
```

### Step 7: Add Deployment Gates

**GitLab CI with Deployment Gate**:

```yaml
approve-production:
  stage: approve-production
  script:
    - echo "Production deployment approved by $GITLAB_USER_LOGIN"
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
      allow_failure: false

deploy-production:
  stage: deploy-production
  needs:
    - job: approve-production
    - job: verify-staging
  script:
    - ./scripts/deploy.sh production
  environment:
    name: production
    url: https://app.example.com
    on_stop: rollback-production
```

**GitHub Actions with Required Reviewers** (configured in repository settings, referenced in workflow):

```yaml
  deploy-production:
    needs: verify-staging
    runs-on: ubuntu-latest
    # The "production" environment must have required reviewers configured
    # in Settings > Environments > production > Required reviewers
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Record approval metadata
        run: |
          echo "Deployment approved at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          echo "Commit: ${{ github.sha }}"
          echo "Triggered by: ${{ github.actor }}"
```

## Best Practices

- **Immutable artifacts**: Build the container image once in CI and promote the same digest through every environment. Never rebuild for production.

- **Environment parity**: Keep dev, staging, and production as similar as possible. Differences in configuration should be limited to environment-specific values (URLs, replica counts, resource limits), not structural changes.

- **Concurrency control**: Use concurrency groups to prevent multiple deployments to the same environment from running simultaneously. This avoids race conditions and partial deployments.

- **Deployment metadata**: Tag every deployment with the git SHA, build number, and timestamp. Store this metadata in Kubernetes labels, cloud resource tags, or a deployment tracking system so you can always trace a running version back to its source.

- **Gradual rollout for production**: Even when using rolling updates, consider deploying to a subset of production infrastructure first (a single region or availability zone) before expanding globally.

- **Secret rotation compatibility**: Design pipelines so secrets are fetched at deploy time, not baked into images. This allows secret rotation without redeployment.

- **Timeout configuration**: Set explicit timeouts on every deployment step. A deployment that hangs indefinitely is worse than one that fails fast and triggers a rollback.

- **Notification integration**: Send deployment status notifications to the team's communication channel. Include the environment, version, deployer, and a link to the pipeline run.

- **Audit trail**: Log every deployment event (who approved it, when it started, when it completed, whether it succeeded or failed) to an immutable audit log for compliance and incident investigation.

- **Dry-run support**: Include a dry-run mode in your pipeline that shows what would be deployed without making changes. This is valuable for pre-deployment review and debugging.

## Common Pitfalls

- **Rebuilding artifacts per environment**: If you build a new container image for each environment, you are not deploying the same artifact you tested. This defeats the purpose of environment promotion and introduces risk.

- **Missing rollback path**: Every deployment strategy must have a tested rollback mechanism. If you have never practiced a rollback, it will fail when you need it most. Include rollback steps in your deployment runbook and test them regularly.

- **Hardcoded secrets in pipeline files**: Never place secrets directly in workflow files, even in private repositories. Use the platform's native secret management and inject values at runtime.

- **No concurrency control**: Without concurrency groups, two developers merging to main in quick succession can trigger overlapping deployments. The result is unpredictable: half-deployed versions, failed health checks, and confused rollback state.

- **Ignoring deployment timeouts**: A missing timeout means a stuck deployment blocks the pipeline indefinitely. Always set `--timeout` on `kubectl rollout status` and equivalent commands on other platforms.

- **Skipping health checks for speed**: Removing post-deployment verification to "speed up the pipeline" is a false economy. A broken deployment that reaches production undetected costs far more time than a 60-second health check.

- **Environment-specific logic in application code**: If your application contains `if (env === 'production')` branches, you are not testing in staging what runs in production. Use configuration injection, not code branches.

- **Manual deployment steps**: Any step that requires a human to run a command, copy a file, or click a button outside the pipeline is a step that will eventually be forgotten or done incorrectly. Automate everything except deliberate approval gates.

- **Overly broad rollback triggers**: Rolling back on any single failed health check can cause unnecessary rollbacks during transient issues. Use consecutive failure thresholds (for example, 3 failures in a row) to avoid false positives.

- **Neglecting pipeline maintenance**: Pipelines are code. They need testing, version control, and periodic review. Treat your deployment pipeline with the same rigor as your application code.
