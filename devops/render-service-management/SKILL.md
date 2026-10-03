---
name: render-service-management
description: >
  Use when managing Render platform services, configuring render.yaml,
  provisioning Render databases, or automating Render infrastructure.
  This skill provides Render-specific operational patterns.
---

# Render Service Management - Shared Skill

## Overview
This skill provides standardized patterns for managing Render platform services, including service provisioning, configuration management, and lifecycle operations.

## When to Use
- When creating new Render services
- When configuring render.yaml files
- When provisioning Render databases
- When managing service scaling
- When setting up auto-deployments
- When handling Render-specific deployments

## Core Procedures

### Service Creation
```yaml
# render.yaml - Web Service
services:
  - type: web
    name: my-service
    env: node  # or python, go, ruby, etc.
    region: oregon  # or frankfurt, singapore, etc.
    branch: main
    repo: https://github.com/org/repo
    plan: starter  # starter, pro, performance
    
    # Build & Run
    buildCommand: npm ci && npm run build
    startCommand: npm start
    healthCheckPath: /health
    
    # Auto-deploy
    autoDeploy: true
    
    # Scaling
    numInstances: 1
    
    # Environment
    envVars:
      - key: NODE_ENV
        value: production
      - key: API_KEY
        sync: false  # don't sync between environments
```

### Database Provisioning
```yaml
# render.yaml - PostgreSQL
databases:
  - name: my-database
    databaseName: myapp_db
    plan: starter  # starter, pro
    color: blue
    ipAllowList: []  # restrict access

# render.yaml - Redis
backgroundWorkers:
  - name: my-worker
    branch: main
    repo: https://github.com/org/repo
    buildCommand: pip install -r requirements.txt
    startCommand: python worker.py
    numInstances: 1
```

### Environment Variable Sync
```yaml
envVars:
  # Sync'd across all environments
  - key: COMMON_SETTING
    value: "value"
  
  # Environment-specific (not synced)
  - key: DATABASE_URL
    fromDatabase:
      name: my-database
      property: connectionString
  
  - key: API_KEY
    sync: false
```

### Custom Domain Configuration
```yaml
domains:
  - alias: www.example.com
    type: redirect
  - alias: app.example.com
    type: primary
```

## Service Scaling

### Auto-Scaling Configuration
```yaml
services:
  - type: web
    name: my-service
    env: node
    branch: main
    
    # Manual scaling
    numInstances: 2
    
    # Auto-scaling (Pro plan)
    autoScaling:
      minInstances: 1
      maxInstances: 5
      targetCPUPercent: 70
      targetMemoryPercent: 80
```

### Health Check Configuration
```yaml
healthCheckPath: /health

# Custom health check in code:
app.get('/health', (req, res) => {
  const healthy = checkDependencies();
  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'healthy' : 'unhealthy',
    timestamp: new Date().toISOString()
  });
});
```

## Deployment Patterns

### Branch-Based Deployment
```yaml
services:
  - type: web
    name: production
    branch: main
    autoDeploy: true
  
  - type: web
    name: staging
    branch: develop
    autoDeploy: true
```

### Environment Separation
```
Production: main branch → production service
Development: dev branch → dev service (or staging)
Preview: feature/* branches → preview services
```

## Monitoring & Logs

### Log Access
```bash
# Via CLI
render logs my-service

# Via Dashboard
# Render Dashboard → Service → Logs
```

### Metrics
```yaml
metrics_available:
  - CPU usage
  - Memory usage
  - Request count
  - Latency
  - Error rate

monitoring:
  - Render Dashboard
  - External: Datadog, New Relic, etc.
```

## Common Issues & Solutions

### Build Failures
```yaml
troubleshooting:
  - Check build logs in Render Dashboard
  - Verify Node version matches local
  - Ensure environment variables are set
  - Check for missing dependencies
```

### Slow Response
```yaml
solutions:
  - Upgrade plan for more CPU/memory
  - Increase instance count
  - Enable auto-scaling
  - Check database query performance
  - Add caching layer (Redis)
```

### Deployment Not Triggering
```yaml
checklist:
  - [ ] Auto-deploy enabled
  - [ ] Correct branch name
  - [ ] Valid GitHub repo connection
  - [ ] Push event occurred
```

## Pricing Reference

| Plan | Price | Instances | Custom Domain | Auto-Scale |
|------|-------|-----------|---------------|------------|
| Starter | Free | 1 | ✗ | ✗ |
| Pro | $25/mo | 3 | ✓ | ✗ |
| Pro Plus | $75/mo | 6 | ✓ | ✓ |
| Performance | $125/mo | 10+ | ✓ | ✓ |

## Best Practices

1. **Use render.yaml** for reproducible deployments
2. **Enable health checks** for auto-restart on failure
3. **Set up auto-scaling** for production services
4. **Use environment variables** for secrets, not in code
5. **Monitor logs** and set up alerting
6. **Test locally** before deploying to Render
7. **Use staging** for testing before production
