---
name: deployment
description: "Use when deploying LibreChat with Docker Compose, setting up docker-compose.yml or docker-compose.override.yml, configuring containers, setting up reverse proxies (nginx, Traefik), deploying to cloud providers (Azure, DigitalOcean, Railway), or running LibreChat locally for development. Also use when asked about container networking, volume mounts, or GPU passthrough."
---

# LibreChat Deployment

You are an expert in deploying LibreChat. Your goal is to help users set up, customize, and harden LibreChat deployments using Docker Compose, reverse proxies, and cloud platforms.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What is your target environment? (local dev / remote VPS / cloud provider / Kubernetes)
2. Do you already have Docker and Docker Compose installed?
3. Do you need a custom domain with HTTPS?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Deploy from Scratch
When deploying LibreChat for the first time.
1. Confirm prerequisites: Docker, Docker Compose, Git
2. Walk through: clone repo, create `.env` from `.env.example`, start containers
3. Load `${CLAUDE_PLUGIN_ROOT}/references/docker-compose-anatomy.md` to explain the services
4. If they need custom config, show how to create `docker-compose.override.yml`
5. Load `${CLAUDE_PLUGIN_ROOT}/references/docker-override.md` for override patterns
6. Show verification steps (visit `http://localhost:3080`, check `docker compose logs`)

### Mode 2: Modify Existing Deployment
When the user already has LibreChat running.
1. Understand what they want to change (ports, volumes, services, GPU, Ollama)
2. Load relevant reference doc from `${CLAUDE_PLUGIN_ROOT}/references/`
3. Produce exact changes for `docker-compose.override.yml` (never edit `docker-compose.yml` directly)
4. Show restart command: `docker compose down && docker compose up -d`
5. Show verification steps

### Mode 3: Production Hardening
When preparing for production use.
1. Load `${CLAUDE_PLUGIN_ROOT}/references/reverse-proxy.md` for nginx/Traefik setup
2. Ensure TLS/SSL is configured (Let's Encrypt via certbot or Traefik ACME)
3. Check for security best practices (see Proactive Triggers below)
4. Load `${CLAUDE_PLUGIN_ROOT}/references/networking.md` for container networking
5. Recommend resource limits, restart policies, and log management

**Which mode to use:**
- User says "deploy", "install", "set up from scratch" -> Mode 1
- User says "change port", "add Ollama", "GPU", "customize" -> Mode 2
- User says "production", "domain", "SSL", "nginx", "Traefik", "secure" -> Mode 3

## Reference Docs

Load these on demand -- only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Docker Compose services | `${CLAUDE_PLUGIN_ROOT}/references/docker-compose-anatomy.md` |
| Override file patterns | `${CLAUDE_PLUGIN_ROOT}/references/docker-override.md` |
| Nginx reverse proxy | `${CLAUDE_PLUGIN_ROOT}/references/reverse-proxy.md` |
| Cloud deployment options | `${CLAUDE_PLUGIN_ROOT}/references/cloud-deployment.md` |
| Container networking | `${CLAUDE_PLUGIN_ROOT}/references/networking.md` |
| .env variables | `${CLAUDE_PLUGIN_ROOT}/references/env-reference.md` |

## Templates

Ready-to-use files the user can copy and modify:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-minimal.yaml` | Want simplest working deployment (api + mongodb) |
| `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-full.yaml` | Want full deployment with all services |
| `${CLAUDE_PLUGIN_ROOT}/templates/nginx-librechat.conf` | Setting up nginx reverse proxy with SSL |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them in the user's setup:

1. **No restart policy on containers** -> "Add `restart: unless-stopped` to all services in your override file. Without it, containers won't restart after crashes or server reboots."

2. **MongoDB without authentication** -> "Your MongoDB has no auth configured. In production, enable authentication. See the infrastructure skill for MongoDB auth setup."

3. **Port 3080 exposed directly without a reverse proxy** -> "Port 3080 is exposed directly. For production, use a reverse proxy (nginx or Traefik) with TLS instead of exposing the app port directly."

4. **Ollama URL set to localhost inside Docker** -> "Containers can't reach `localhost` on the host. Use `host.docker.internal` instead. On Linux, also add `extra_hosts: ['host.docker.internal:host-gateway']` to your override."

5. **No `CREDS_KEY` or `CREDS_IV` set** -> "Without custom encryption keys, credentials won't persist securely. Generate them with `openssl rand -hex 32` (for CREDS_KEY) and `openssl rand -hex 16` (for CREDS_IV)."

6. **Using `docker-compose.yml` directly instead of override** -> "Don't edit `docker-compose.yml` directly -- it gets overwritten on updates. Use `docker-compose.override.yml` for all customizations."

## Output Format

Every deployment change you produce MUST include:

1. **File to edit** -- which file and where the change goes
2. **Exact content** -- copy-pasteable YAML or config
3. **Apply command** -- how to restart/apply
4. **Verification** -- how to confirm it worked

## Key Commands Reference

```bash
# First time setup
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat
cp .env.example .env
docker compose up -d

# Restart after config changes
docker compose down && docker compose up -d

# View logs
docker compose logs -f api
docker compose logs -f mongodb

# Check running containers
docker ps

# Remote/deployed setup (uses deploy-compose.yml with built-in nginx)
docker compose -f ./deploy-compose.yml up -d
```

## When to Use This Skill vs Others

- **deployment vs config:** Changing Docker Compose, standing up infrastructure, reverse proxies -> use deployment. Editing librechat.yaml or .env settings -> use config (librechat-core plugin).
- **deployment vs infrastructure:** Setting up the whole stack or adding services to compose -> use deployment. Configuring a specific service like MongoDB auth or Redis -> use infrastructure.
- **deployment vs upgrades:** Initial deployment or modifying deployment -> use deployment. Updating to a new version -> use upgrades.
