---
name: dockerize-app
description: Use when asked to dockerize or containerize an app, write or fix a Dockerfile or docker-compose.yml, shrink a large Docker image, speed up slow Docker builds, or run an app with its database locally in containers — Node, Python, Java, Go and others.
---

# Dockerize App

## Overview

Produce a small, secure, fast-building image that runs the app exactly as it runs today. Read how the project builds and starts before writing a line, and prove the result by building and running it.

## Method

1. **Discover:** runtime and version (`.nvmrc`, `engines`, `python_requires`, `pom.xml`, `go.mod`), package manager and lockfile, build command, start command, port, required environment variables (`.env.example`), and services it needs (database, cache).
2. **Write the Dockerfile** with the rules below. Templates per stack are in [templates.md](templates.md).
3. **Write `.dockerignore`** before the first build.
4. **Write `docker-compose.yml`** if the app needs services, with health checks and named volumes.
5. **Build and run to verify:** `docker build -t app .`, `docker run --rm -p <port>:<port> --env-file .env app`, then hit the health or home route. Report image size (`docker images app`).

## Rules

| Rule | Why |
|---|---|
| Multi-stage build: build stage with dev tools, slim runtime stage | Smaller, fewer vulnerabilities |
| Pin base image versions (`node:22-alpine`, not `node:latest`) | Reproducible builds |
| Copy lockfile and install dependencies before copying source | Dependency layer stays cached |
| Use the lockfile install command (`npm ci`, `pip install -r`, `mvn -B package`) | Exact versions |
| Run as a non-root user | Container escape is less damaging |
| No secrets in the image or build args; pass them at runtime | Images get shared and pushed |
| One process per container; `CMD` in exec form (`["node", "server.js"]`) | Correct signal handling and shutdown |
| `HEALTHCHECK` or a compose healthcheck | Orchestrators know when it is ready |
| `.dockerignore` excludes `node_modules`, `.git`, `.env`, build output, tests | Faster context, no leaked files |

## Output

The Dockerfile, `.dockerignore`, optional `docker-compose.yml`, then:

```
Build: docker build -t <name> .
Run:   docker run --rm -p 3000:3000 --env-file .env <name>
Image size: <size>   Verified: <route> returned <status>
```

If Docker is not available to run, say the files are unverified.

## Common mistakes

- `COPY . .` before installing dependencies, so every code change reinstalls everything.
- Copying `.env` into the image.
- Using a full OS image (`node:22`) for runtime when `-slim` or `-alpine` works.
- App listening on `localhost` inside the container; it must bind to `0.0.0.0`.
- Compose `depends_on` without a healthcheck, so the app starts before the database is ready.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
