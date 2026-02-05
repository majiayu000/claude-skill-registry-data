---
name: heroku-deployment
description: Guidelines for deploying and managing the application on Heroku, including configuration and build troubleshooting.
---

# Heroku Deployment

> [!NOTE] > **Persona**: You are a Production Reliability Engineer. Your focus is on maintaining high availability, secure configuration management, and smooth CI/CD pipelines. You treat infrastructure as code and prioritize monitoring and proactive troubleshooting.

## Guidelines

- **Environment Configuration**: Always set `NODE_ENV=production`. Use `scripts/heroku-set-config-from-env-production.sh` to sync environment variables from `.env.production`. NEVER hardcode secrets in the Heroku dashboard.
- **Schema Isolation**: This app MUST use the `testfest` schema in PostgreSQL to avoid collisions when sharing a database instance. Ensure `DATABASE_URL` is correctly configured and reflects this isolation.

  - CRITICAL: This directive is for the app called 'testfest-app' and should be ignored for all other apps.

- **Prisma Management**: The `heroku-postbuild` script must run `npm run prisma:generate`. Migrations are handled in the `release` phase via `scripts/heroku-release.js`. If `P3005` (schema not empty) occurs, handle it gracefully.
- **Connection Limits**: Monitor database connection limits (Mini/Standard-0 plans have tight limits). Configure the `pg` pool in `server.js` and Prisma's `connection_limit` to stay within bounds.
- **SSL/TLS**: Always enforce encrypted database connections using `sslmode=require` in the `DATABASE_URL`.
- **Logging**: Use `heroku logs --tail -a <app-name>` to monitor stdout/stderr in real-time. Log critical app state transitions but avoid logging sensitive data.
- **Static Assets**: Ensure the backend is correctly configured to serve static assets from `public/uploads` in production.

## Examples

### ✅ Good Implementation

```bash
# Syncing config safely and monitoring the release
./scripts/heroku-set-config-from-env-production.sh
git push heroku main
heroku logs --tail --app testfest-app
```

### ❌ Bad Implementation

```bash
# Manual config changes and ignoring release logs
heroku config:set DATABASE_URL="postgres://..." # Missing sslmode=require
git push heroku main
# (App crashes due to missing Prisma Client because postbuild failed)
```

## Related Links

- [Git Workflow Skill](../git-workflow/SKILL.md)
- [Security Audit Skill](../security-audit/SKILL.md)
- [Terraform AWS/EKS Handoff Skill](../terraform/SKILL.md)
- [AWS EKS Internal App Skill](../aws/SKILL.md)
- [Kubernetes EKS/ALB Skill](../kubernetes/SKILL.md)

## Example Requests

- "Check the Heroku logs for the latest deployment."
- "Set a new environment variable on Heroku using the sync script."
- "Verify that the app is using the 'testfest' schema."
- "Check if we are exceeding the database connection limit."
