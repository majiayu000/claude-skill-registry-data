---
name: devops
description: Expert guidance for deploying, managing, and scaling GabeDA infrastructure on Railway (backend) and Render (frontend). Handles environment configuration, CORS setup, troubleshooting, monitoring, and production optimizations. Use when deploying services, fixing deployment issues, configuring infrastructure, or scaling production systems.
---

# GabeDA DevOps Expert

## Purpose

Provide expert guidance for deploying, managing, and troubleshooting GabeDA's full-stack infrastructure across Railway (backend) and Render (frontend). Handle environment configuration, CORS setup, deployment automation, monitoring, and production optimizations.

**Key Capabilities:**
- Deploy backend (Django/PostgreSQL/Redis) to Railway
- Deploy frontend (React/Vite) to Render
- Configure environment variables and secrets
- Debug CORS, build failures, and connectivity issues
- Set up monitoring and logging
- Implement continuous deployment workflows
- Scale services and optimize performance

## When to Invoke

**Use this skill when:**
- Deploying backend or frontend to production
- Fixing deployment failures (CORS, build errors, 404s)
- Configuring environment variables or secrets
- Troubleshooting production issues
- Setting up monitoring or alerts
- Implementing continuous deployment
- Scaling services or optimizing costs
- Need deployment best practices

**Input required:** Service to deploy (backend/frontend), issue description, or infrastructure task

## GabeDA Infrastructure Overview

### Current Stack

**Backend (Railway):**
- Platform: Railway Hobby Plan ($5/month)
- URL: https://gabedabe-production.up.railway.app
- Framework: Django 5.1 + Django REST Framework
- Database: PostgreSQL (Railway-managed)
- Cache: Redis (Railway-managed)
- Workers: Celery (for async tasks)
- Python: 3.11

**Frontend (Render):**
- Platform: Render Free Tier (Static Site)
- URL: https://gabedabe-frontend.onrender.com
- Framework: React 18 + TypeScript + Vite
- Build: npm run build → dist/
- Node: 22.x

**Repositories:**
- Backend: https://github.com/Brownbull/gabeda_backend
- Frontend: https://github.com/Brownbull/gabeda_frontend

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Render (Frontend - Static Site)                            │
│  https://gabedabe-frontend.onrender.com                     │
│  ├─ React SPA (built with Vite)                             │
│  ├─ Environment: VITE_API_URL                               │
│  └─ Auto-deploy on git push                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │ API Calls (CORS-enabled)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Railway (Backend - Web Service)                            │
│  https://gabedabe-production.up.railway.app                 │
│  ├─ Django REST API                                         │
│  ├─ Gunicorn (2 workers)                                    │
│  ├─ Environment: DJANGO_SETTINGS_MODULE=production          │
│  └─ Auto-deploy on git push                                 │
└───────────┬──────────────────────────┬──────────────────────┘
            │                          │
            ▼                          ▼
    ┌───────────────┐          ┌──────────────┐
    │  PostgreSQL   │          │    Redis     │
    │  (Railway)    │          │  (Railway)   │
    └───────────────┘          └──────────────┘
```

---

## Deployment Workflows

### 1. Backend Deployment (Railway)

#### Prerequisites
- Railway account with Hobby plan ($5/month)
- Railway CLI installed: `npm install -g @railway/cli`
- Backend code pushed to GitHub

#### Initial Deployment Steps

```bash
# 1. Navigate to backend folder
cd C:/Projects/play/gabeda_backend

# 2. Initialize Railway project (first time only)
railway init

# 3. Add PostgreSQL
railway add --plugin postgresql

# 4. Add Redis
railway add --plugin redis

# 5. Set environment variables
railway variables --set DJANGO_SETTINGS_MODULE="config.settings.production"
railway variables --set DEBUG="False"
railway variables --set SECRET_KEY="your-secret-key-here"
railway variables --set ALLOWED_HOSTS="gabedabe-production.up.railway.app"
railway variables --set CORS_ALLOWED_ORIGINS="http://localhost:5173,https://gabedabe-frontend.onrender.com"

# 6. Deploy
railway up
```

#### Configuration Files Required

**railway.toml:**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
```

**runtime.txt:**
```
python-3.11
```

**Procfile:**
```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
worker: celery -A config worker --loglevel=info --concurrency=2
```

#### Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | Load production settings |
| `SECRET_KEY` | Random 50-char string | Django secret key |
| `DEBUG` | `False` | Disable debug mode |
| `ALLOWED_HOSTS` | `gabedabe-production.up.railway.app` | Allowed hostnames |
| `DATABASE_URL` | Auto-provided by Railway | PostgreSQL connection |
| `REDIS_URL` | Auto-provided by Railway | Redis connection |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,https://gabedabe-frontend.onrender.com` | CORS whitelist |

---

### 2. Frontend Deployment (Render)

#### Prerequisites
- Render account (free tier)
- Frontend code pushed to GitHub

#### Deployment Steps

**Via Render Dashboard:**

1. Go to https://dashboard.render.com/
2. Click "New +" → "Static Site"
3. Connect to GitHub repo: `Brownbull/gabeda_frontend`
4. Configure:
   - **Name:** gabedabe-frontend
   - **Branch:** main
   - **Build Command:** `npm run build`
   - **Publish Directory:** `dist`
5. Add environment variable:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://gabedabe-production.up.railway.app/api`
6. Click "Create Static Site"

#### Configuration Files Required

**render.yaml** (optional, for infrastructure-as-code):
```yaml
services:
  - type: web
    name: gabedabe-frontend
    env: static
    buildCommand: npm run build
    staticPublishPath: ./dist
    envVars:
      - key: VITE_API_URL
        value: https://gabedabe-production.up.railway.app/api
```

**public/_redirects** (for React Router):
```
/*    /index.html   200
```

#### Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `VITE_API_URL` | `https://gabedabe-production.up.railway.app/api` | Backend API URL |
| `VITE_APP_NAME` | `GabeDA` | Application name |

**Important:** Vite injects environment variables at build time, so any changes require a rebuild!

---

## Troubleshooting Guide

### Backend Issues

#### Issue: CORS Errors

**Symptom:** Browser console shows "blocked by CORS policy"

**Diagnosis:**
```bash
# Test CORS preflight
curl -v -X OPTIONS https://gabedabe-production.up.railway.app/api/accounts/auth/register/ \
  -H "Origin: https://gabedabe-frontend.onrender.com" \
  -H "Access-Control-Request-Method: POST"
```

**Expected:** `Access-Control-Allow-Origin: https://gabedabe-frontend.onrender.com`

**Fixes:**
1. **Check CORS_ALLOWED_ORIGINS:**
   ```bash
   railway variables
   # Should show: CORS_ALLOWED_ORIGINS=http://localhost:5173,https://gabedabe-frontend.onrender.com
   ```

2. **Update if incorrect:**
   ```bash
   railway variables --set CORS_ALLOWED_ORIGINS="http://localhost:5173,https://gabedabe-frontend.onrender.com"
   ```

3. **Common mistakes:**
   - Trailing slashes (❌ `https://example.com/`)
   - Missing `http://` or `https://`
   - Spaces in comma-separated list
   - Typos in domain name

4. **Wait 30 seconds** for Railway auto-redeploy after variable change

**See:** [references/cors_troubleshooting.md](references/cors_troubleshooting.md)

---

#### Issue: Build Failures

**Symptom:** Railway build fails with errors

**Common Causes:**

1. **Python version mismatch:**
   - Ensure `runtime.txt` specifies `python-3.11`
   - Check `requirements.txt` for Python 3.12+ incompatibilities

2. **Missing dependencies:**
   ```bash
   # Test locally first
   pip install -r requirements.txt
   python manage.py check
   ```

3. **Database migration failures:**
   - Check if models changed without migrations
   - Run locally: `python manage.py makemigrations`

**Fix:**
```bash
# Update requirements
pip freeze > requirements.txt
git add requirements.txt runtime.txt
git commit -m "fix: update dependencies"
git push
```

---

#### Issue: 500 Internal Server Error

**Symptom:** API returns HTTP 500

**Diagnosis:**
1. Check Railway logs: https://railway.com
2. Look for Python tracebacks
3. Check for missing environment variables

**Common fixes:**
- SECRET_KEY not set
- DATABASE_URL not connected
- Missing migrations: `python manage.py migrate`

---

### Frontend Issues

#### Issue: Build Fails on Render

**Symptom:** Render build logs show TypeScript or npm errors

**Diagnosis:**
```bash
# Test locally
cd C:/Projects/play/gabeda_frontend
npm run build
```

**Common Causes:**

1. **TypeScript errors:**
   - Unused imports
   - Type mismatches
   - Missing dependencies

2. **Environment variable issues:**
   - Missing VITE_API_URL
   - Typo in API URL

**Fix:**
```bash
# Fix TypeScript errors
npm run build  # See errors
# Fix issues in code
git add .
git commit -m "fix: typescript errors"
git push  # Render auto-rebuilds
```

---

#### Issue: API Calls Fail After Deployment

**Symptom:** Frontend works locally but fails in production

**Diagnosis:**
1. Open browser DevTools → Network tab
2. Check API call URLs
3. Look for CORS errors or wrong URLs

**Common Causes:**

1. **Wrong VITE_API_URL:**
   - Check Render environment variable
   - Ensure it ends with `/api` not `/ap` or `/`

2. **Needs rebuild:**
   - Vite bakes env vars at build time
   - After changing env var, trigger manual rebuild

**Fix:**
1. Go to Render dashboard
2. Environment → Update `VITE_API_URL`
3. Manual Deploy → "Clear build cache & deploy"
4. Wait 2-3 minutes for rebuild

---

#### Issue: 404 on Page Refresh

**Symptom:** Direct URL access returns 404

**Cause:** React Router needs all routes to serve `index.html`

**Fix:**
Create `public/_redirects`:
```
/*    /index.html   200
```

Commit and push:
```bash
git add public/_redirects
git commit -m "fix: add redirects for react router"
git push
```

---

## Monitoring & Logging

### Backend Monitoring (Railway)

**Access Logs:**
1. Go to https://railway.com
2. Select project → Service
3. View tabs:
   - **Deployments:** Build history
   - **Metrics:** CPU, Memory, Network
   - **Logs:** Real-time application logs

**Key Metrics:**
- Response time: <300ms target
- Error rate: <1% target
- Memory usage: <512MB target
- CPU usage: <50% average

**Log Filtering:**
```bash
# Railway CLI log streaming
railway logs --follow

# Filter for errors
railway logs | grep ERROR

# Filter by endpoint
railway logs | grep "/api/accounts"
```

---

### Frontend Monitoring (Render)

**Access Logs:**
1. Go to https://dashboard.render.com
2. Select service
3. View tabs:
   - **Events:** Deployment history
   - **Logs:** Build and deploy logs
   - **Metrics:** Bandwidth usage

**Key Metrics:**
- Build time: <3 minutes target
- Bundle size: <1MB target
- Bandwidth: <100GB/month (free tier limit)

---

### Browser Monitoring

**Chrome DevTools:**
1. Open DevTools (F12)
2. **Network tab:**
   - Monitor API calls
   - Check response times
   - Look for failed requests
3. **Console tab:**
   - Check for JavaScript errors
   - Look for CORS errors
4. **Application tab:**
   - Check localStorage (auth tokens)
   - Verify service worker status

---

## Continuous Deployment

### Automated Deployment Flow

**Both Railway and Render support auto-deploy on git push:**

```
Developer → git push → GitHub → Webhook → Platform → Deploy
```

**Current Configuration:**
- ✅ Backend: Railway auto-deploys on push to `main`
- ✅ Frontend: Render auto-deploys on push to `main`

**Workflow:**
1. Make changes locally
2. Test locally
3. Commit: `git commit -m "description"`
4. Push: `git push origin main`
5. Monitor deployment in platform dashboards
6. Verify in production

---

### Deployment Checklist

**Before pushing to production:**
- [ ] Code tested locally
- [ ] No TypeScript errors (`npm run build` for frontend)
- [ ] No Python errors (`python manage.py check` for backend)
- [ ] Environment variables documented
- [ ] Database migrations created (if schema changed)
- [ ] Tests passing (if implemented)

**After deployment:**
- [ ] Build succeeded in platform dashboard
- [ ] Health check passes (visit URLs)
- [ ] API endpoints work (test in browser)
- [ ] No errors in logs
- [ ] CORS works (test login/registration)

---

## Scaling & Optimization

### Backend Scaling (Railway)

**Vertical Scaling:**
```bash
# Upgrade plan for more resources
# Railway Hobby: $5/month base + usage
# Includes: 512MB RAM, shared CPU
```

**Horizontal Scaling:**
```bash
# Add more Gunicorn workers (in railway.toml)
startCommand = "... gunicorn ... --workers 4"  # Increase from 2
```

**Database Optimization:**
- Enable connection pooling
- Add database indexes
- Use `select_related()` and `prefetch_related()`
- Monitor slow queries

**Caching:**
- Redis already configured
- Add view-level caching
- Cache expensive computations

---

### Frontend Optimization (Render)

**Bundle Size Reduction:**
```bash
# Analyze bundle
npm run build -- --analyze

# Code splitting
# Use React.lazy() for route-based splitting
```

**Performance Improvements:**
- Lazy load routes
- Optimize images (WebP format)
- Enable compression (Render does this automatically)
- Add service worker for offline support

---

## Security Best Practices

### Backend Security

**✅ Already Implemented:**
- HTTPS enforced (Railway provides SSL)
- CORS properly configured
- JWT authentication
- Password validation
- SQL injection protection (Django ORM)
- XSS protection (Django templates)

**🔄 TODO:**
- [ ] Add rate limiting
- [ ] Implement API key rotation
- [ ] Add request logging for audit trail
- [ ] Set up automated security scanning
- [ ] Configure CSP headers
- [ ] Add IP-based throttling

---

### Frontend Security

**✅ Already Implemented:**
- HTTPS enforced (Render provides SSL)
- Environment variables not exposed
- XSS protection (React)
- Secure token storage (localStorage)

**🔄 TODO:**
- [ ] Add Content Security Policy headers
- [ ] Implement subresource integrity
- [ ] Add rate limiting on auth forms
- [ ] Implement session timeout
- [ ] Add CAPTCHA on registration

---

## Cost Management

### Current Costs

**Backend (Railway):**
- Base: $5/month (Hobby plan)
- Includes: PostgreSQL, Redis, 512MB RAM
- Additional: Pay-as-you-go for excess usage
- **Estimate:** $5-10/month for development

**Frontend (Render):**
- Static Site: **FREE**
- Includes: 100GB bandwidth/month
- No credit card required

**Total:** ~$5-10/month

---

### Cost Optimization Tips

**Backend:**
- Use Redis caching to reduce database queries
- Optimize Gunicorn workers (don't over-provision)
- Monitor Railway usage dashboard
- Set up billing alerts

**Frontend:**
- Optimize bundle size to reduce bandwidth
- Use image CDN for large assets
- Monitor bandwidth usage in Render dashboard

---

## Reference Documentation

**Detailed guides in `references/` folder:**

- [deployment_checklist.md](references/deployment_checklist.md) - Pre/post deployment checklist
- [cors_troubleshooting.md](references/cors_troubleshooting.md) - CORS error diagnosis
- [environment_variables.md](references/environment_variables.md) - Complete env var reference
- [railway_commands.md](references/railway_commands.md) - Railway CLI command reference
- [render_configuration.md](references/render_configuration.md) - Render setup guide
- [monitoring_setup.md](references/monitoring_setup.md) - Logging and metrics
- [disaster_recovery.md](references/disaster_recovery.md) - Backup and restore procedures

**Quick links:**
- Railway Dashboard: https://railway.com
- Render Dashboard: https://dashboard.render.com
- Backend URL: https://gabedabe-production.up.railway.app
- Frontend URL: https://gabedabe-frontend.onrender.com

---

## Quality Standard

DevOps operations must meet the **DEVOPS_STANDARD.md** criteria:

✅ **Reliability (25%)** - Services deployed successfully with <1% error rate
✅ **Security (25%)** - Proper secrets management, CORS, HTTPS enabled
✅ **Observability (20%)** - Logging and monitoring configured
✅ **Documentation (15%)** - Deployment steps documented and reproducible
✅ **Automation (15%)** - CI/CD pipelines configured

**Minimum score: 8.0/10** before marking deployment complete.

**See:** [DEVOPS_STANDARD.md](../standards/DEVOPS_STANDARD.md)

---

**Version:** 1.0.0
**Last Updated:** 2025-10-31
**Skill Type:** Infrastructure & Deployment Management
