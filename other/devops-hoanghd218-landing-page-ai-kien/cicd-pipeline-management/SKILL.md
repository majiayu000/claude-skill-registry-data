---
name: CI/CD Pipeline Management
description: GitLab CI/CD pipeline optimization, Docker image building, caching strategies, and 3-stage deployment workflow
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# CI/CD Pipeline Management

Understand and optimize GitLab CI/CD pipeline for PCR Card application.

## When to Use

- Understanding CI/CD pipeline architecture
- Troubleshooting pipeline failures
- Optimizing build performance
- Planning pipeline improvements
- Reviewing pipeline configuration

## Current Pipeline Status

**Status**: ✅ WORKING | ⚡ Optimization Available (4-6 min savings)

**Performance**:
- Current build time: ~11-12 minutes
- Optimized build time: ~3-4 minutes (with custom Docker image)
- Potential savings: 7-8 minutes per run (60-65% faster)

## Pipeline Architecture

### 3-Stage Pipeline

| Stage | Duration | Purpose | Jobs |
|-------|----------|---------|------|
| **validate** | ~10s | Project structure validation | validate-structure |
| **build** | 11-12min | Install dependencies, compile, build assets | build-app |
| **deploy** | Manual | Staging deployment via Deployer | deploy-staging |

**Total**: 5-8 minutes for automated stages, manual deploy to staging

## Build Stage Breakdown

### What Happens (11-12 minutes total)

```yaml
build-app:
  stage: build
  image: php:8.3

  before_script:
    # 1. Initialize git submodules (~30s)
    - git submodule update --init --recursive

    # 2. Install system libraries (~1 min)
    - apt-get update
    - apt-get install -y libzip-dev libpng-dev libjpeg-dev libfreetype6-dev

    # 3. Compile PHP extensions from source (~2-3 min) ⚡ OPTIMIZATION TARGET
    - docker-php-ext-install pdo_mysql zip exif pcntl bcmath
    - docker-php-ext-configure gd --with-freetype --with-jpeg
    - docker-php-ext-install gd

    # 4. Install Composer (~30s)
    - curl -sS https://getcomposer.org/installer | php
    - mv composer.phar /usr/local/bin/composer

    # 5. Install Node.js 22.x (~1 min)
    - curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    - apt-get install -y nodejs

  script:
    # 6. Install PHP dependencies (~2-3 min)
    - composer install --prefer-dist --no-interaction --optimize-autoloader --no-dev

    # 7. Install Node dependencies (~1 min)
    - npm ci

    # 8. Build frontend assets (~4-5 min)
    - npm run build

    # 9. Create Laravel caches (~10s)
    - php artisan config:cache
    - php artisan route:cache
    - php artisan view:cache
```

**Bottleneck**: PHP extensions compile from source every run

## Caching Strategy

### Three-Layer Caching

**1. APT Packages** (`apt-cache-v1`)

```yaml
cache:
  key: apt-cache-v1
  paths:
    - apt-cache/
```

Saves: ~1 minute per run (system dependencies)

**2. Node Modules** (keyed by `package-lock.json`)

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

Saves: ~1 minute if package-lock.json unchanged

**3. Composer Vendor** (keyed by `composer.lock`)

```yaml
cache:
  key:
    files:
      - composer.lock
  paths:
    - vendor/
```

Saves: ~2 minutes if composer.lock unchanged

**Total Cache Savings**: ~4 minutes (when cache hits)

## Optimization Path

### Custom Docker Image

**Current**: Base `php:8.3` image (compiles extensions every run)
**Optimized**: Custom image with pre-compiled extensions

### Performance Gain

| Stage | Current | Optimized | Savings |
|-------|---------|-----------|---------|
| PHP extensions | 2-3 min | 0s | 2-3 min |
| System libs | 1 min | 0s | 1 min |
| Composer install | 30s | 0s | 30s |
| Node install | 1 min | 0s | 1 min |
| **Build stage** | **11-12 min** | **3-4 min** | **7-8 min** |

**Overall**: 60-65% faster pipeline

### Custom Dockerfile

**Location**: `.gitlab/Dockerfile`

```dockerfile
FROM php:8.3-cli

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install PHP extensions (pre-compiled!)
RUN docker-php-ext-install \
    pdo_mysql \
    zip \
    exif \
    pcntl \
    bcmath

RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install Node.js 22.x
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /builds/overmindllc/pcrcard
```

### Implementation Steps

**1. Build Custom Image** (one-time setup)

```bash
# Build image
docker build -f .gitlab/Dockerfile -t registry.gitlab.com/overmindllc/pcrcard-ci:latest .

# Push to GitLab Container Registry
docker push registry.gitlab.com/overmindllc/pcrcard-ci:latest
```

**2. Update `.gitlab-ci.yml`**

```yaml
build-app:
  stage: build
  image: registry.gitlab.com/overmindllc/pcrcard-ci:latest  # ← Use custom image

  before_script:
    # ✅ Keep these (still needed)
    - git submodule update --init --recursive

    # ❌ Remove these (already in image)
    # - apt-get update && apt-get install...
    # - docker-php-ext-install...
    # - curl -sS https://getcomposer.org/installer...
    # - curl -fsSL https://deb.nodesource.com/setup_22.x...

  script:
    - composer install --prefer-dist --no-interaction --optimize-autoloader --no-dev
    - npm ci
    - npm run build
    - php artisan config:cache
    - php artisan route:cache
    - php artisan view:cache
```

**3. Test Pipeline**

```bash
# Push changes
git add .gitlab-ci.yml
git commit -m "ci: optimize pipeline with custom Docker image"
git push origin main

# Monitor pipeline at:
# https://gitlab.com/overmindllc/pcrcard/-/pipelines
```

**Setup Time**: 30 minutes (one-time)

## Deployment Stage

### Staging Deployment

**Trigger**: Manual (button click in GitLab UI)
**Script**: Uses Laravel Deployer via `./scripts/staging.sh deploy`
**Duration**: ~2-3 minutes

```yaml
deploy-staging:
  stage: deploy
  when: manual
  environment:
    name: staging
    url: https://staging.pcrcard.com

  script:
    - php vendor/bin/dep deploy staging

  only:
    - main
```

### Production Deployment

**Trigger**: Git tag creation
**Process**: Create release tag → GitLab triggers production deploy

```bash
# Create release
DRY_RUN=false ./scripts/release.sh full patch

# GitLab auto-deploys to production on tag push
```

## Git Submodules Integration

### Auto-Initialization

Every build initializes forked package submodules:

```yaml
before_script:
  - git submodule update --init --recursive
```

**Why**: Ensures `packages/nova-menus` and `packages/nova-medialibrary-bounding-box-field` are available for Composer VCS path repositories.

**Impact**: +30 seconds per build (necessary)

## Common Pipeline Issues

### Issue 1: PHP Extension Compilation Failure

**Symptom**: Build fails during `docker-php-ext-install`

```
configure: error: Package requirements (libpng) were not met
```

**Solution**: Missing system library

```dockerfile
# Add missing library to Dockerfile
RUN apt-get install -y libpng-dev
```

### Issue 2: Composer Package Not Found

**Symptom**: `Package pcrcard/nova-menus not found`

**Cause**: Git submodules not initialized

**Solution**: Verify submodule initialization

```yaml
before_script:
  - git submodule update --init --recursive
  - ls -la packages/  # Verify packages exist
```

### Issue 3: npm ci Failure

**Symptom**: `package-lock.json out of sync`

**Solution**: Regenerate package-lock.json locally

```bash
rm package-lock.json
npm install
git add package-lock.json
git commit -m "fix: regenerate package-lock.json"
```

### Issue 4: Build Timeout

**Symptom**: Build exceeds 1-hour timeout

**Solution**: Increase timeout or optimize

```yaml
build-app:
  timeout: 2h  # Increase timeout
```

Or implement custom Docker image (removes 7-8 min)

## Pipeline Configuration

### .gitlab-ci.yml Location

**File**: `.gitlab-ci.yml` (project root)

### Key Sections

```yaml
# Global settings
stages:
  - validate
  - build
  - deploy

# Variables
variables:
  COMPOSER_CACHE_DIR: "$CI_PROJECT_DIR/.composer-cache"

# Validate stage
validate-structure:
  stage: validate
  image: alpine:latest
  script:
    - echo "Validating project structure..."
    - test -f composer.json
    - test -f package.json

# Build stage
build-app:
  stage: build
  image: php:8.3
  # ... (see Build Stage Breakdown above)

# Deploy stage
deploy-staging:
  stage: deploy
  when: manual
  # ... (see Deployment Stage above)
```

## Monitoring Pipeline

### GitLab UI

**Pipeline URL**: https://gitlab.com/overmindllc/pcrcard/-/pipelines

**View**:
- Pipeline status (success/failed)
- Stage durations
- Job logs
- Cache hit rates
- Artifacts

### Pipeline Metrics

**Track**:
- Average build time
- Success rate
- Cache hit rate
- Deployment frequency
- Time to recovery

## Documentation Links

- **Optimization Guide**: `docs/ci-cd/pipeline/OPTIMIZATION-GUIDE.md` (comprehensive, foolproof instructions)
- **CI/CD Hub**: `docs/ci-cd/README.md` (navigation to 15 guides)
- **Deployment Guide**: `docs/deployment/DEPLOYMENT-GUIDE.md`
- **Deployment Checklist**: `docs/deployment/DEPLOYMENT-CHECKLIST.md`
- **GitLab CI/CD Docs**: https://docs.gitlab.com/ee/ci/
