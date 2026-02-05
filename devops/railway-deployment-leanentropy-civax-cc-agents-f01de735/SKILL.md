---
name: railway-deployment
description: Railway.app deployment patterns, environment management, and production best practices. Applied automatically when working with Railway deployments.
---

# Railway Deployment Knowledge Base

## Railway Platform Overview

Railway is a modern PaaS that deploys applications from Git repositories with automatic builds and deployments.

### Key Concepts
- **Project**: Container for all services and environments
- **Service**: Individual deployable unit (backend, frontend, database)
- **Environment**: Isolated deployment target (staging, production)
- **Deployment**: Specific version of code running in an environment

## Auto-Deploy Configuration

Railway automatically deploys when you push to configured branches:

| Branch | Environment | Trigger |
|--------|-------------|---------|
| `develop` | Staging | Push to develop |
| `main` | Production | Push to main |

### Setting Up Auto-Deploy

1. Go to Railway Dashboard → Project → Settings
2. Under "Deployments", configure:
   - Source branch for each environment
   - Build command (auto-detected usually)
   - Start command

## Project Structure Patterns

### Monorepo (Multiple Services)
```
project/
├── frontend/
│   ├── Dockerfile
│   └── package.json
├── backend/
│   ├── Dockerfile
│   └── requirements.txt
└── railway.json
```

### Single Service
```
project/
├── Dockerfile (or detected runtime)
├── package.json / requirements.txt
└── railway.json (optional)
```

## railway.json Configuration

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

## Dockerfile Best Practices for Railway

```dockerfile
# Multi-stage build for smaller images
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Python Example
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Environment Variables

### Railway-Provided Variables
```
RAILWAY_ENVIRONMENT=production
RAILWAY_SERVICE_NAME=backend
RAILWAY_PROJECT_ID=xxx
PORT=<assigned port>
```

### Common Application Variables
```
ENVIRONMENT=production
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
API_KEY=xxx
CORS_ORIGINS=https://myapp.com
```

## Health Checks

Railway performs health checks to ensure your app is running:

```python
# FastAPI example
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

```javascript
// Express example
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});
```

## Networking

### Internal Networking
Services within the same project can communicate via internal DNS:
```
http://backend.railway.internal:8000
```

### External Access
- Railway provides `*.up.railway.app` domains
- Custom domains can be configured in settings

## Logging

### Viewing Logs
```bash
# Via CLI
railway logs
railway logs --environment production
railway logs -n 100  # Last 100 lines

# Via Dashboard
Project → Service → Logs tab
```

### Structured Logging Best Practices
```python
import logging
import json

logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)

def log_json(level, message, **kwargs):
    log_entry = {"message": message, **kwargs}
    getattr(logging, level)(json.dumps(log_entry))
```

## Scaling

### Horizontal Scaling
```json
// railway.json
{
  "deploy": {
    "numReplicas": 3
  }
}
```

### Resource Limits
Configure in Railway Dashboard:
- Memory limit
- CPU limit
- Instance count

## Database Connections

### Connection Pooling
For production, use connection pooling:

```python
# SQLAlchemy with pool
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
```

## Deployment Monitoring

### Key Metrics to Watch
- Build time
- Deployment status
- Memory usage
- CPU usage
- Response times
- Error rates

### Alerts
Configure alerts in Railway Dashboard for:
- Deployment failures
- High memory usage
- Service crashes

## Rollback Procedures

### Quick Rollback
1. Go to Railway Dashboard
2. Select service → Deployments
3. Click "Rollback" on previous healthy deployment

### Git-Based Rollback
```bash
git revert HEAD
git push origin main
# Railway auto-deploys reverted code
```

## Cost Optimization

- Use multi-stage Docker builds (smaller images)
- Set appropriate resource limits
- Use sleep/hibernation for staging if not needed 24/7
- Monitor usage in Railway Dashboard

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Build fails | Dockerfile syntax, dependencies |
| Deploy hangs | Health check endpoint, startup time |
| 502 errors | App not binding to PORT env var |
| Slow performance | Resource limits, database queries |
| Missing env vars | Railway Dashboard → Variables |
