---
name: docker-and-deployment-fix
description: Diagnose and fix container, build, runtime, environment, networking, reverse proxy, TLS, and deployment problems. Use when Codex needs to handle Docker build failures, crashing containers, unreachable apps, missing environment variables, VPS deployment failures, reverse proxy issues, HTTPS/TLS problems, wrong port mappings, database connection failures, frontend-backend production URL issues, CORS deployment failures, Docker Compose service networking, static file serving, health checks, volume paths, runtime logs, CI/VPS build command failures, localhost binding inside containers, restart loops, and deployment behavior that differs from local development.
---

# Docker and Deployment Fix

Use this skill when an application works locally but fails in Docker, on a VPS, behind a reverse proxy, or after deployment.

## Core Rule

Diagnose from evidence before editing. Inspect logs and configuration, identify the root cause, apply the smallest safe fix, and verify with concrete commands.

## Workflow

1. Understand the deployment problem:
   - what fails, where it fails, build/startup/runtime/network/proxy layer, local/staging/production environment, command run, logs, expected behavior, and actual behavior
2. Classify the issue:
   - build, startup, runtime, networking, port, environment, database, reverse proxy, TLS/HTTPS, frontend deployment, backend deployment, volume/file, health check, CI/CD, or service readiness
3. Inspect Dockerfile:
   - base image, workdir, dependency install, copy order, build command, runtime command, exposed port, permissions, env vars, multi-stage artifact copy, `.dockerignore`, and start command
4. Inspect Docker Compose:
   - service names, build context, Dockerfile path, image, ports, environment, `.env`, volumes, networks, `depends_on`, health checks, restart policy, command override, database service, and proxy labels/network
5. Inspect build logs:
   - first meaningful error, missing packages, runtime versions, TypeScript/build failures, dependency conflicts, lockfile mismatches, missing system dependencies, permission errors, missing files, and env vars required at build time
6. Inspect runtime logs:
   - app crash, missing env vars, import errors, DB connection failure, port bind errors, permission errors, migration errors, CORS/static file issues, external service failures, and health check failures
7. Inspect environment variables:
   - `.env.example`, real env location, compose env block, deployment platform variables, CI secrets, Docker ARG vs ENV, frontend build-time variables, backend runtime variables, and secret exposure risk
8. Inspect ports and binding:
   - internal app port, `EXPOSE`, compose `ports`/`expose`, proxy upstream port, firewall/security group, bind address, and platform `$PORT`
9. Inspect service networking:
   - service names, network names, database/Redis hosts, frontend API URL, reverse proxy network, internal vs external ports, and container DNS
10. Inspect database connection and startup:
   - host, port, database name, credentials variables, connection string, SSL, migrations, readiness, volumes, network access, seeds, pools, and retry/wait behavior
11. Inspect reverse proxy:
   - Caddy/Nginx/Traefik config, domain, upstream service/port, HTTPS, WebSockets, forwarded headers, path routing, static/API routing, cert behavior, redirects, upload limits, and timeouts
12. Inspect frontend deployment:
   - build command/output, static server, SPA fallback, API base URL, env variables, asset paths, base path, source maps, CORS, mixed content, and route refresh behavior
13. Inspect backend deployment:
   - runtime command, host binding, port, workers, env vars, DB, migrations, static/media, CORS origins, auth secrets, file storage, logs, health endpoint, workers/jobs, and scheduler
14. Inspect volumes, file permissions, health checks, and persistent data risks.
15. Identify root cause with evidence:
   - connect logs/config to the actual failure instead of stating a vague deployment problem
16. Apply the smallest safe fix:
   - command, port, service hostname, env reference, build path, SPA fallback, proxy upstream, DB readiness, volume, health endpoint, CORS origin, or Dockerfile copy/start fix
17. Verify the fix:
   - run or provide commands such as `docker compose config`, build, up, ps, logs, curl health/domain, proxy logs, and network probes
18. Check production safety:
   - secrets, debug mode, CORS, HTTPS, DB persistence, logs, health checks, restart policy, env docs, backups, and no destructive volume/database actions
19. Summarize problem, scope, evidence, root cause, fix, files, verification, safety notes, risks, and follow-up recommendations.

Read `references/deployment-fix-checklist.md` for layer-specific checks, common root causes, verification commands, production safety review, and the final report format.

## Non-Negotiable Rules

- Do not guess deployment fixes without checking logs or config.
- Do not print real secrets.
- Do not commit real `.env` files.
- Do not use `localhost` between containers unless it is intentionally inside the same container.
- Do not expose database ports publicly unless necessary and secured.
- Do not disable CORS or security just to make the app work.
- Do not run destructive volume or database commands without explicit approval.
- Do not remove persistent volumes casually.
- Do not rewrite the whole deployment when a small fix is enough.
- Do not claim deployment works without verification or clear limitation.
- Do not ignore health checks.
- Do not ignore reverse proxy logs when proxying fails.
- Do not ignore production differences from local development.
- Keep deployment changes safe, minimal, and documented.

## Output Contract

When using this skill, provide:

1. Deployment problem and environment/scope.
2. Evidence found from logs/config/commands.
3. Root cause.
4. Fix applied.
5. Files changed.
6. Verification commands and real result.
7. Production safety notes: secrets, CORS, HTTPS, DB persistence, health checks, logs.
8. Remaining risks.
9. Recommended follow-up.
