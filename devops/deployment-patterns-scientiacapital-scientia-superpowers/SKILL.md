---
name: deployment-patterns
description: Deploy projects to Vercel, Railway, or Docker with platform-specific best practices. Use when deploying applications, configuring deployment settings, debugging deployment failures, or setting up CI/CD pipelines. Triggers on "deploy to vercel", "railway deployment", "docker build", "deployment failed", "configure vercel.json".
---

# Deployment Patterns for Scientia Stack

Deploy to Vercel, Railway, or Docker following proven patterns from 98+ projects.

## Platform Selection

Choose based on project type:

| Project Type | Platform | Reason |
|--------------|----------|--------|
| Next.js frontend | Vercel | Native support, edge functions |
| Python backend | Railway | Nixpacks, health checks |
| ML/GPU workloads | RunPod | GPU access, vLLM |
| Local development | Docker | Consistent environment |

## Vercel Deployment (19 projects)

### Standard vercel.json for Monorepo

```json
{
  "framework": "nextjs",
  "installCommand": "cd frontend && npm install",
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next"
}
```

### Environment Variables

1. Set in Vercel Dashboard or CLI:
   ```bash
   vercel env add VITE_SUPABASE_URL production
   vercel env add VITE_SUPABASE_ANON_KEY production
   ```

2. For preview deployments, use `preview` scope.

### SPA Routing

Add to `frontend/vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

### Deploy Command

```bash
# Production
vercel --prod

# Preview
vercel
```

## Railway Deployment (2 projects)

### Standard railway.json

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "poetry install --no-dev"
  },
  "deploy": {
    "startCommand": "poetry run python -m src.vozlux.main",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### Environment Variables

Railway requires manual dashboard configuration for sensitive vars:
- Go to: https://railway.com/project/{project-id}/settings
- Add each variable under "Variables" tab

Common variables for Python backends:
```
SUPABASE_URL
SUPABASE_SERVICE_KEY
ANTHROPIC_API_KEY
GOOGLE_API_KEY
DEEPSEEK_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
```

### Health Check Endpoint

Always implement `/health`:
```python
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

## Docker Deployment (5 projects)

### Multi-stage Dockerfile

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry export -f requirements.txt > requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

### docker-compose.yml for Development

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./src:/app/src
```

## Pre-Deployment Checklist

Before any deployment:

1. [ ] All tests passing (`npm test` or `pytest`)
2. [ ] No hardcoded API keys (grep for patterns)
3. [ ] Environment variables documented in `.env.example`
4. [ ] CLAUDE.md updated with deployment status
5. [ ] Build succeeds locally (`npm run build` or `poetry build`)

## Debugging Deployment Failures

### Vercel Failures

1. Check build logs: `vercel logs`
2. Common issues:
   - Missing env vars → Check Vercel dashboard
   - Build timeout → Increase in project settings
   - Module not found → Check package.json dependencies

### Railway Failures

1. Check logs in dashboard
2. Common issues:
   - Health check timeout → Increase `healthcheckTimeout`
   - Missing env vars → Must set manually in dashboard
   - Poetry lock issues → Delete poetry.lock and regenerate

### Docker Failures

1. Build locally first: `docker build -t test .`
2. Run with logs: `docker run -it test`
3. Check for missing system dependencies

## CI/CD Integration

For GitHub Actions, use:

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```
