---
name: auto-deploy
description: "One-click deployment to multiple platforms (Vercel, Netlify, AWS, Docker). Includes CI/CD setup, environment management, and rollback support."
triggers:
  - "deploy to vercel"
  - "deploy to production"
  - "一键部署"
  - "自动部署"
  - "CI/CD setup"
---

# Auto Deploy

One-click deployment to multiple platforms with CI/CD integration.

## Supported Platforms

| Platform | Type | Auto-SSL | CDN | Cost |
|----------|------|----------|-----|------|
| Vercel | Serverless | ✅ | ✅ | Free tier |
| Netlify | Static/JAMstack | ✅ | ✅ | Free tier |
| AWS | Full stack | Manual | Manual | Pay-as-you-go |
| Docker | Self-hosted | Manual | Manual | Server cost |
| Railway | Full stack | ✅ | ✅ | $5/mo |

## Usage

### Deploy to Vercel

```bash
# Auto-detect framework and deploy
hermes deploy --platform vercel

# With custom settings
hermes deploy --platform vercel \
  --env production \
  --domain myapp.com
```

### Deploy to Docker

```bash
# Generate Dockerfile and deploy
hermes deploy --platform docker \
  --registry ghcr.io \
  --server user@production.com
```

### Multi-Platform Deploy

```bash
# Deploy to multiple platforms
hermes deploy --platforms vercel,netlify,docker
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Auto Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: clowlove/hermes-deploy@v1
        with:
          platform: vercel
          token: ${{ secrets.VERCEL_TOKEN }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - hermes deploy --platform vercel
  only:
    - main
```

## Environment Management

### Environment Variables

```bash
# Set environment variables
hermes env set DATABASE_URL="postgres://..." --env production
hermes env set API_KEY="sk-..." --env production

# List all variables
hermes env list --env production

# Import from .env file
hermes env import .env.production --env production
```

### Secrets Management

```bash
# Store encrypted secrets
hermes secrets set DB_PASSWORD="..." --platform vercel
hermes secrets set AWS_KEY="..." --platform aws
```

## Rollback Support

```bash
# List deployments
hermes deploy list

# Rollback to previous version
hermes deploy rollback --to deployment-id

# Rollback to specific commit
hermes deploy rollback --commit abc123
```

## Configuration

```yaml
# hermes-deploy.yml
project:
  name: my-app
  framework: next.js

platforms:
  vercel:
    domain: myapp.com
    env:
      - DATABASE_URL
      - API_KEY
  
  docker:
    registry: ghcr.io
    image: my-app
    ports:
      - "3000:3000"

ci:
  provider: github
  auto_deploy: true
  branches: [main, staging]
```

## Pitfalls

1. **Build Errors** — Always test build locally before deploying
2. **Environment Variables** — Double-check all required vars are set
3. **Domain DNS** — Allow 24-48h for DNS propagation
4. **Rollback** — Keep at least 3 deployment versions for rollback
5. **Cost Monitoring** — Set up billing alerts for cloud platforms
