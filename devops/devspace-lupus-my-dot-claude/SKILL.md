---
name: devspace
description: Guide for working with DevSpace, a Kubernetes development tool that automates building, deploying, and developing applications. Use when users need to create or modify devspace.yaml configuration files, build and deploy images to Kubernetes, manage multi-environment deployments with profiles, upload files to pods, or troubleshoot DevSpace workflows. Includes patterns for CI/CD integration, image tagging strategies, and secret management.
---

# DevSpace

## Overview

DevSpace is a Kubernetes development tool that automates the complete lifecycle of building container images, deploying to Kubernetes, and developing applications. This skill provides guidance for working with DevSpace non-interactively in automation scenarios, avoiding common pitfalls and following best practices.

## Core Principle

**Always work through `devspace.yaml` configuration rather than applying Kubernetes manifests directly.** DevSpace manages the complete lifecycle including image building, tagging, and deployment coordination.

## When to Use This Skill

Use this skill when:
- Creating or modifying `devspace.yaml` configuration files
- Building and deploying container images to Kubernetes via DevSpace
- Setting up multi-environment deployments with DevSpace profiles
- Uploading files or creating secrets dynamically in Kubernetes pods
- Troubleshooting DevSpace-related image tag mismatches or deployment issues
- Integrating DevSpace into CI/CD pipelines
- Converting manual `kubectl` workflows to DevSpace-managed workflows

## Critical Understanding

### The Image Tag Problem

**Problem:** DevSpace builds images with dynamic, random tags (e.g., `abc123`) and automatically replaces image references in manifests during deployment. Applying manifests manually with `kubectl apply` bypasses this replacement, causing deployments to fail with "image not found" errors.

**Solution:** Always use `devspace deploy` or `devspace build` + `devspace deploy --skip-build`. Never manually `kubectl apply` files from the k8s folder.

### DevSpace v2 Architecture

DevSpace v2 uses a pipeline-based approach with three main sections:

```yaml
version: v2beta1
name: my-project

# Define what images to build
images:
  backend:
    image: myregistry/backend
    dockerfile: ./Dockerfile
    context: ./

# Define build and deploy pipelines
pipelines:
  build: |-
    build_images --all

  deploy: |-
    build_images --all
    create_deployments --all

# Define what to deploy
deployments:
  backend:
    kubectl:
      manifests:
        - k8s/
```

## Common DevSpace Workflows

### 1. Build and Deploy

```bash
# Build all images and deploy
devspace deploy

# Deploy without rebuilding (use existing images)
devspace deploy --skip-build

# Force rebuild all images
devspace deploy --force-build

# Deploy with specific profile
devspace deploy -p production
```

### 2. Build Images Only

```bash
# Build all images
devspace build

# Build with specific tag
devspace build --tag v1.0.0

# Build and tag multiple versions
devspace build --tag v1.0.0 --tag latest
```

### 3. Non-Interactive Deployment

```bash
# Specify namespace explicitly
devspace deploy -n my-namespace

# Specify Kubernetes context
devspace deploy --kube-context=my-cluster

# Override variables
devspace deploy --var REGISTRY=production.io --var TAG=v1.0.0

# Wait for deployment to be ready
devspace deploy --wait --timeout=300
```

### 4. Configuration Validation

```bash
# Validate and show rendered configuration
devspace print

# Validate with specific profile
devspace print -p production

# List deployments
devspace list deployments

# List profiles
devspace list profiles
```

### 5. Cleanup

```bash
# Remove all deployments
devspace purge

# Remove specific deployment
devspace purge --deployments=backend
```

## Configuration Patterns

### Minimal Configuration

```yaml
version: v2beta1
name: simple-app

images:
  app:
    image: myregistry.io/app
    dockerfile: ./Dockerfile
    context: ./

deployments:
  app:
    kubectl:
      manifests:
        - k8s/

pipelines:
  deploy: |-
    build_images --all
    create_deployments --all
```

### Production-Ready Configuration

```yaml
version: v2beta1
name: production-app

vars:
  - name: REGISTRY
    source: env
    default: dev.registry.io
  - name: VERSION
    value: $(git describe --always)
  - name: NAMESPACE
    source: env
    default: development

images:
  backend:
    image: ${REGISTRY}/backend
    tags:
      - ${VERSION}
      - latest
    rebuildStrategy: default

deployments:
  backend:
    namespace: ${NAMESPACE}
    kubectl:
      manifests:
        - k8s/deployment.yaml
        - k8s/service.yaml

profiles:
  - name: production
    patches:
      - op: replace
        path: vars.REGISTRY.value
        value: prod.registry.io
      - op: add
        path: deployments.backend.kubectl.patches
        value:
          - op: replace
            path: spec.replicas
            value: 5

pipelines:
  deploy: |-
    build_images --all
    create_deployments --all

  verify: |-
    kubectl wait --for=condition=available deployment/backend \
      -n ${NAMESPACE} --timeout=300s
```

## Image Tagging Strategies

### Static Tags

```yaml
images:
  backend:
    image: myregistry/backend
    tags:
      - latest
      - v1.0.0
```

### Dynamic Tags from Git

```yaml
images:
  backend:
    image: myregistry/backend
    tags:
      - $(git describe --always)
      - latest
```

### Runtime Variables for Image References

Use runtime variables in inline manifests to reference built images:

```yaml
deployments:
  backend:
    kubectl:
      inlineManifest: |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: backend
        spec:
          template:
            spec:
              containers:
              - name: backend
                image: ${runtime.images.backend.image}:${runtime.images.backend.tag}
```

Available runtime variables:
- `${runtime.images.IMAGE_NAME.image}` - Full image name with tag
- `${runtime.images.IMAGE_NAME.tag}` - Just the tag
- `${runtime.images.IMAGE_NAME.imageName}` - Just the image name (no tag)

## Variables and Configuration

### Variable Types

**Static Variables:**
```yaml
vars:
  - name: REGISTRY
    value: myregistry.io
```

**Environment Variables:**
```yaml
vars:
  - name: CI_COMMIT_SHA
    source: env
  - name: NAMESPACE
    source: env
    default: default
```

**Command Variables:**
```yaml
vars:
  - name: GIT_COMMIT
    command: git
    args: ["rev-parse", "HEAD"]

  # Shorthand
  - name: GIT_BRANCH
    value: $(git rev-parse --abbrev-ref HEAD)
```

**AVOID in Automation - Interactive Variables:**
```yaml
# DON'T USE THIS - prompts user
vars:
  - name: MYSQL_VERSION
    question: "Which MySQL version?"
    options: ["5.7", "8.0"]
```

### Predefined Variables

DevSpace provides built-in variables:
- `${DEVSPACE_NAMESPACE}` - Current namespace
- `${DEVSPACE_CONTEXT}` - Current kube context
- `${DEVSPACE_PROFILE}` - Active profile name
- `${DEVSPACE_RANDOM}` - Random 6-char string
- `${DEVSPACE_TIMESTAMP}` - Current UNIX timestamp

## Profiles for Multi-Environment Deployments

Profiles allow different configurations for dev, staging, production:

```yaml
vars:
  - name: ENV
    source: env
    default: development

profiles:
  - name: staging
    patches:
      - op: replace
        path: images.backend.image
        value: staging.registry.io/backend
      - op: add
        path: deployments.backend.kubectl.patches
        value:
          - op: replace
            path: spec.replicas
            value: 2

  - name: production
    activation:
      - vars:
          ENV: production
    patches:
      - op: replace
        path: images.backend.image
        value: prod.registry.io/backend
      - op: add
        path: deployments.backend.kubectl.patches
        value:
          - op: replace
            path: spec.replicas
            value: 5

# Use with: devspace deploy -p production
# Or auto-activate: ENV=production devspace deploy
```

## Uploading Files to Pods

DevSpace provides hooks for uploading files to containers after deployment.

### Option 1: Command-based Variables (Recommended)

```yaml
vars:
  - name: CONFIG_PATH
    source: command
    command: |
      if [ -f ~/.config/app/config.json ]; then
        echo ~/.config/app/config.json
      elif [ -f ./config/app.json ]; then
        echo ./config/app.json
      else
        echo "config-not-found"
      fi

hooks:
  - upload:
      localPath: ${CONFIG_PATH}
      containerPath: /app/config/config.json
    container:
      imageSelector: myregistry/app:tag
    events: ["after:deploy:my-deployment"]
    name: "upload-config"
```

### Option 2: Config Expressions

```yaml
hooks:
  - upload:
      localPath: $!(./scripts/find-config.sh)
      containerPath: /app/config/config.json
    container:
      labelSelector:
        app: my-app
    events: ["after:deploy:my-deployment"]
    name: "upload-config"
```

### Multiple Files

```yaml
vars:
  - name: APP_CONFIG
    source: command
    command: ./scripts/find-config.sh app
  - name: DB_CONFIG
    source: command
    command: ./scripts/find-config.sh database

hooks:
  - upload:
      localPath: ${APP_CONFIG}
      containerPath: /app/config/app.json
    container:
      imageSelector: myregistry/app
    events: ["after:deploy:my-app"]
    name: "upload-app-config"

  - upload:
      localPath: ${DB_CONFIG}
      containerPath: /app/config/database.json
    container:
      imageSelector: myregistry/app
    events: ["after:deploy:my-app"]
    name: "upload-db-config"
```

## Managing Secrets

Create Kubernetes secrets from environment variables using hooks.

### Basic Secret Creation

```yaml
vars:
  - name: API_KEY
    source: env
  - name: DATABASE_PASSWORD
    source: env

hooks:
  # Validate required secrets
  - command: |
      if [ -z "$API_KEY" ] || [ -z "$DATABASE_PASSWORD" ]; then
        echo "ERROR: API_KEY and DATABASE_PASSWORD must be set"
        exit 1
      fi
    events: ["before:deploy"]
    name: "validate-secrets"

  # Create secret
  - command: |
      kubectl create secret generic app-secrets \
        --from-literal=api-key="${API_KEY}" \
        --from-literal=db-password="${DATABASE_PASSWORD}" \
        --dry-run=client -o yaml | kubectl apply -f -
      echo "Application secrets created"
    events: ["before:deploy"]
    name: "create-secrets"

# Use in deployment
deployments:
  app:
    helm:
      componentChart: true
      values:
        containers:
          - image: myregistry/app
            env:
              - name: API_KEY
                valueFrom:
                  secretKeyRef:
                    name: app-secrets
                    key: api-key
```

### Dynamic Secret Detection from .env

```yaml
vars:
  - name: SECRET_DATA
    source: command
    command: |
      if [ -f .env ]; then
        cat .env | grep -v '^#' | grep -v '^$' | \
        awk -F= '{printf "--from-literal=%s=%s ", $1, $2}'
      fi

hooks:
  - command: |
      if [ ! -z "${SECRET_DATA}" ]; then
        kubectl create secret generic env-secrets \
          ${SECRET_DATA} \
          --dry-run=client -o yaml | kubectl apply -f -
      fi
    events: ["before:deploy"]
    name: "create-env-secrets"
```

## Dev Mode Initialization and Credential Mounting

DevSpace dev mode provides interactive development workflows with file sync and terminal access. However, it introduces challenges when applications need credential files mounted into directories they also write to.

### The Problem

**Challenge 1: Kubernetes subPath Mount Limitations**
- Applications often need credential files in directories where they create other files
- Kubernetes `subPath` mounts cannot mount files into directories where apps write other files
- Example: Mounting `credentials.json` into `~/.app/` fails if the app creates `~/.app/cache/` or other files

**Challenge 2: DevSpace Terminal Mode Bypasses Entrypoints**
- DevSpace dev mode with `terminal.enabled: true` replaces container commands
- Standard ENTRYPOINT and CMD are not executed
- Initialization logic in entrypoints does not run

### The Solution: DevSpace Hooks with once: true

DevSpace hooks with `once: true` are the official pattern for initialization tasks that run once per container lifecycle.

```yaml
hooks:
  - name: setup-credentials
    events: ["after:deploy"]
    command: |
      if [ -f /tmp/secrets/credentials.json ]; then
        ln -sf /tmp/secrets/credentials.json /home/user/.app/credentials.json
        echo "✓ Credentials symlinked"
      fi
    container:
      labelSelector:
        app: my-app
      containerName: main
      namespace: my-namespace
      once: true    # Only runs when container starts, not on every dev session
      wait: true
      timeout: 60
```

**Why This Works:**
- Hooks execute in the running container (not at build time)
- `once: true` ensures the hook only runs when the container first starts
- Runs after deployment, so the container and volumes are ready
- Does not interfere with DevSpace's terminal/entrypoint handling
- Subsequent `devspace dev` sessions do not re-trigger the hook

### Complete Example: Credential Mounting Pattern

```yaml
# In deployment manifest (k8s/deployment.yaml):
# Mount secret to separate directory (not the app's writable directory)
volumeMounts:
  - name: app-credentials
    mountPath: /tmp/secrets
    readOnly: true

volumes:
  - name: app-credentials
    secret:
      secretName: my-app-creds
      items:
        - key: credentials.json
          path: credentials.json

# In devspace.yaml:
hooks:
  - name: setup-app-credentials
    events: ["after:deploy"]
    command: |
      # Create target directory if needed
      mkdir -p ~/.app

      # Symlink credentials from read-only mount
      ln -sf /tmp/secrets/credentials.json ~/.app/credentials.json

      echo "✓ Application credentials configured"
    container:
      labelSelector:
        app: my-app
      containerName: main
      namespace: ${DEVSPACE_NAMESPACE}
      once: true
      wait: true
      timeout: 60
```

### Multi-File Credential Setup

```yaml
hooks:
  - name: setup-application-secrets
    events: ["after:deploy"]
    command: |
      # Create all required directories
      mkdir -p ~/.app ~/.config/app

      # Symlink multiple credential files
      ln -sf /tmp/secrets/credentials.json ~/.app/credentials.json
      ln -sf /tmp/secrets/api-key.txt ~/.config/app/api-key.txt
      ln -sf /tmp/secrets/client-secret.json ~/.app/client-secret.json

      # Set permissions if needed
      chmod 600 ~/.app/credentials.json

      echo "✓ All application credentials configured"
    container:
      labelSelector:
        app: my-app
      once: true
      wait: true
```

### Anti-Patterns to Avoid

**❌ Don't use dev.patches to force entrypoints (hacky):**
```yaml
# AVOID THIS
dev:
  my-app:
    patches:
      - op: replace
        path: spec.template.spec.containers[0].command
        value: ["/bin/sh", "-c", "/setup.sh && bash"]
```
This interferes with DevSpace's terminal handling and creates confusion.

**❌ Don't mount secrets with subPath into app-writable directories:**
```yaml
# AVOID THIS - will fail
volumeMounts:
  - name: app-credentials
    mountPath: /home/user/.app/credentials.json
    subPath: credentials.json  # Fails if app writes to ~/.app/
```

**❌ Don't use init containers for dev mode initialization:**
Init containers run before the main container starts, not when dev sessions restart. Hooks with `once: true` are the correct pattern.

**❌ Don't put initialization in .bashrc:**
```bash
# AVOID THIS in .bashrc
ln -sf /tmp/secrets/credentials.json ~/.app/credentials.json
```
This runs every shell session, not just on container start, and does not work for non-interactive containers.

### When to Use This Pattern

Use DevSpace hooks with `once: true` for:
- Mounting credential files into writable directories
- One-time setup tasks in dev mode
- Symlinking files from read-only mounts
- Database initialization scripts
- Certificate/key setup that should persist across dev sessions

### Container Selection Strategies

**By label selector (recommended):**
```yaml
container:
  labelSelector:
    app: my-app
    component: backend
```

**By image selector:**
```yaml
container:
  imageSelector: myregistry.io/my-app:${runtime.images.backend.tag}
```

**By container name:**
```yaml
container:
  containerName: main
  namespace: ${DEVSPACE_NAMESPACE}
```

### Debugging Initialization Hooks

**Check if hook executed:**
```bash
devspace logs --follow --container my-app
```

**Verify symlinks inside container:**
```bash
devspace enter
ls -la ~/.app/
cat ~/.app/credentials.json
```

**Re-run hook manually (for testing):**
```bash
devspace enter
ln -sf /tmp/secrets/credentials.json ~/.app/credentials.json
```

## CI/CD Integration

DevSpace works identically in CI/CD as it does locally:

```yaml
# GitHub Actions example
- name: Deploy to Kubernetes
  run: |
    devspace use namespace ${{ env.NAMESPACE }}
    devspace use context ${{ env.KUBE_CONTEXT }}
    devspace deploy --wait --timeout=300 --var VERSION=${{ github.sha }}
  env:
    REGISTRY: ghcr.io/myorg
    VERSION: ${{ github.sha }}
    NAMESPACE: production
```

**Key flags for CI/CD:**
- `--skip-build` - Skip image building
- `--skip-push` - Skip pushing images to registry
- `--force-build` - Force rebuild all images
- `--force-deploy` - Force redeploy all deployments
- `--wait` - Wait for deployments to be ready
- `--timeout` - Timeout for wait operations (default 120s)

## Common Pitfalls and Solutions

### Pitfall 1: Dynamic Image Tags Not Matching

**Error:** `Image "myregistry/backend:abc123" not found`

**Cause:** Manually applying manifests that reference images with DevSpace-generated tags.

**Solution:** Always use `devspace deploy` instead of `kubectl apply`.

### Pitfall 2: Image Built but Not Pushed

**Error:** Deployment fails because image doesn't exist in registry.

**Solution:**
```bash
# Ensure push happens
devspace build  # Automatically pushes

# Or explicitly
devspace deploy --skip-push=false

# For local clusters only
devspace deploy --skip-push-local-kube=true
```

### Pitfall 3: Changes Not Reflected After Deploy

**Cause:** DevSpace skipped rebuild (no detected changes) or using cached image.

**Solution:**
```bash
# Force rebuild and redeploy
devspace deploy --force-build --force-deploy

# Or delete cache
rm -rf .devspace/
devspace deploy
```

### Pitfall 4: Interactive Prompts in Automation

**Cause:** Using variables with `question` field.

**Solution:** Use `source: env` with defaults or provide via command line:
```bash
devspace deploy --var REGISTRY=myregistry.io --var NAMESPACE=prod
```

### Pitfall 5: Wrong Namespace/Cluster

**Solution:**
```bash
# Set explicitly
devspace use context production-cluster
devspace use namespace production

# Or specify in command
devspace deploy --kube-context=production-cluster -n production
```

## Best Practices

### 1. Always Read devspace.yaml First

Before making changes:
```bash
cat devspace.yaml
devspace list deployments
devspace list profiles
```

### 2. Validate Configuration

```bash
# Validate configuration
devspace print

# Validate with specific profile
devspace print -p production
```

### 3. Test in Safe Environment First

```bash
# Create test namespace
kubectl create namespace test-${USER}

# Deploy there
devspace deploy -n test-${USER}

# Verify
devspace analyze -n test-${USER}

# Cleanup
devspace purge -n test-${USER}
kubectl delete namespace test-${USER}
```

### 4. Use Version Control

```bash
# Check current state
git diff devspace.yaml

# Create backup
cp devspace.yaml devspace.yaml.backup

# Make changes and validate
devspace print

# Commit if good
git add devspace.yaml
git commit -m "feat: add new service deployment"
```

### 5. Document Changes

Add comments to devspace.yaml when making changes:
```yaml
images:
  # Added 2024-01-15: New microservice for payment processing
  payments:
    image: myregistry.io/payments
    tags: ["${VERSION}"]
```

### 6. Handle Errors Gracefully

```bash
if devspace deploy; then
    echo "Deployment successful"
    devspace analyze
else
    echo "Deployment failed"
    kubectl get pods -n ${NAMESPACE}
    kubectl describe pods -n ${NAMESPACE}
    exit 1
fi
```

## Verification Checklist

After any change, verify:
- [ ] YAML syntax is valid (`devspace print`)
- [ ] Images are defined in `images` section
- [ ] Deployments reference correct manifests
- [ ] Variables have defaults or are provided
- [ ] No interactive prompts (no `question` fields)
- [ ] Namespace and context are explicit
- [ ] Image tags are managed by DevSpace
- [ ] No manual `kubectl apply` commands

## Quick Command Reference

```bash
# Build
devspace build                        # Build all images
devspace build --tag v1.0.0          # Build with specific tag
devspace build --force-build         # Force rebuild

# Deploy
devspace deploy                       # Build and deploy
devspace deploy --skip-build         # Deploy only
devspace deploy -p production        # Deploy with profile
devspace deploy --wait --timeout=300 # Wait for readiness

# Pipelines
devspace run-pipeline build          # Run custom pipeline
devspace run-pipeline deploy-backend # Run named pipeline

# Configuration
devspace print                        # Show rendered config
devspace print -p production         # With profile
devspace list deployments            # List deployments
devspace list profiles               # List profiles

# Validation
devspace analyze                      # Check namespace health
devspace analyze --patient           # Wait for pods to be ready

# Cleanup
devspace purge                        # Remove deployments
devspace purge --deployments=backend # Remove specific deployment

# Context management
devspace use context my-cluster      # Set cluster
devspace use namespace production    # Set namespace
```

## Resources

This skill includes additional reference documentation:

### references/

- `advanced_patterns.md` - Advanced DevSpace patterns including Helm deployments, Kustomize integration, deployment patches, and complex pipeline examples
- `troubleshooting.md` - Comprehensive troubleshooting guide for common DevSpace issues with diagnosis steps and solutions

**When to read references:**
- When implementing Helm or Kustomize deployments
- When creating complex multi-service pipelines
- When encountering deployment issues or errors
- When setting up advanced CI/CD workflows

**Note:** Start with the main SKILL.md for most DevSpace tasks. Load reference files when deeper knowledge is needed for specific advanced scenarios.
