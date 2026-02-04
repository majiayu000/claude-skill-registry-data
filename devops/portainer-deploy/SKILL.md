---
name: portainer-deploy
description: Setup automated deployment with GitHub Actions, ghcr.io, and Portainer webhooks. Supports Traefik reverse proxy and multi-service Docker Compose. Use when user wants to setup CI/CD, deployment, or Portainer integration.
---

# Portainer Deploy Skill

This skill helps set up automated deployment pipeline with:
- GitHub Container Registry (ghcr.io)
- GitHub Actions for CI/CD
- Portainer webhooks for automatic redeployment
- Traefik reverse proxy support
- Multi-service Docker Compose support

## When to Use This Skill

Use this skill when the user wants to:
- Set up automated deployment for their project
- Configure CI/CD with GitHub Actions
- Integrate with Portainer for container management
- Add Traefik reverse proxy with automatic HTTPS
- Deploy multi-service applications

## Deployment Process

### 1. Analyze Project Structure

First, understand the current project setup:

```bash
# Check for existing files
ls -la Dockerfile docker-compose.yml .github/workflows/
```

Determine:
- Is there a Dockerfile? (if not, this skill cannot help - Dockerfile is required)
- Is there a docker-compose.yml? (analyze or create)
- Are there existing GitHub Actions workflows?
- How many services does the project need? (single or multi-service)
- What is the main branch name? (main or master)

### 2. Interactive Questions

If uncertain, ask the user:

1. **Main branch**: "What is your main branch name? (main/master)"
2. **Services**: "Is this a single service or multi-service application?"
3. **Traefik**: "Do you want to use Traefik reverse proxy with automatic HTTPS? (yes/no)"
4. **Domain**: If Traefik - "What domain will you use? (can be configured via Portainer env vars)"
5. **Network**: If Traefik - "What is your Traefik network name? (can be configured via Portainer env vars)"
6. **Webhooks**: "How many Portainer stacks will you deploy? (usually 1, or 2+ for multi-stack)"

**Note:** Domain and network name can be provided via Portainer environment variables for flexibility across environments.

### 3. Generate or Update GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

**Key elements:**
- Trigger on push to main branch + workflow_dispatch
- Login to ghcr.io using GITHUB_TOKEN
- Build and push Docker image with **SHA tag ONLY** (NOT latest): `${{ github.sha }}`
- Checkout or create `deploy` branch using `git checkout -B deploy`
- Update docker-compose.yml with SHA tag using sed
- Commit changes to `deploy` branch
- Force push to `deploy` branch with `--force`
- Trigger Portainer webhook(s)

**CRITICAL:** Never use `:latest` tag in production deployments. Always use specific SHA tags for traceability.

**Template reference:** See `templates/github-workflow.yml`

**Important notes:**
- Use `ghcr.io/${{ github.repository_owner }}/${{ github.event.repository.name }}:${{ github.sha }}` for image tag
- The main branch keeps `:latest` as a placeholder (will be replaced in deploy branch)
- Portainer should watch the `deploy` branch, NOT the main branch
- Update ALL docker-compose files if multiple exist (e.g., main + bot-hoster)
- Add multiple webhook steps if deploying to multiple Portainer stacks
- Use `--force` when pushing to deploy branch (it's a CI-only branch)

### 4. Generate or Update docker-compose.yml

**Important:**
- Always use the actual repository path from `git remote get-url origin` instead of placeholder text
- In the **main branch**, use `:latest` as a placeholder (it will be replaced in the deploy branch)
- In the **deploy branch**, the image tag will be the specific SHA (updated by CI/CD)

**For single service with Traefik (main branch):**
```yaml
version: "3.8"

services:
  app:
    # The image tag will be replaced by GitHub Actions workflow in the deploy branch
    image: ghcr.io/owner/repo:latest  # Use actual owner/repo from git remote
    container_name: app-name
    networks:
      - traefik_network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`${HOSTNAME}`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=myresolver"
      - "traefik.http.services.app.loadbalancer.server.port=8080"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - ENV_VAR=${ENV_VAR}

networks:
  traefik_network:
    name: ${NETWORK_NAME:-traefik_network}  # Allow network name override via env var
    external: true
```

**Note:** The deploy branch will have the same structure but with `image: ghcr.io/owner/repo:abc123...` (full SHA)

**For multi-service:**
- Include all services (e.g., app + database + cache)
- Set up service dependencies with `depends_on`
- Use same image for multiple services with different `command` if needed
- Configure internal networks for inter-service communication

**Template reference:** See `templates/docker-compose-traefik.yml` and `templates/docker-compose-simple.yml`

### 5. Update Strategy

**If files exist:**

1. **GitHub Actions workflow exists:**
   - Check if it's similar to our pattern (build → push → update compose → webhook)
   - If similar: Update in place (fix image tags, add missing webhooks, etc.)
   - If different: Ask user if they want to replace or keep existing

2. **docker-compose.yml exists:**
   - Check if it has correct image format (ghcr.io/owner/repo:latest)
   - Check if Traefik labels are present (if user wants Traefik)
   - Update image tags to use ghcr.io format
   - Add Traefik labels if requested
   - Preserve existing environment variables and volumes

**If files don't exist:**
- Create new files from templates
- Customize based on project structure
- Get actual repository owner/repo from: `git remote get-url origin`
- Use actual values in docker-compose.yml image field

### 6. Remind About Secrets, Environment Variables, and Deploy Branch

After generating files, remind the user:

```
Important Setup Steps:

1. Add GitHub Secret:
   - Go to: https://github.com/OWNER/REPO/settings/secrets/actions
   - Click "New repository secret"
   - Name: PORTAINER_REDEPLOY_HOOK
   - Value: Your Portainer webhook URL (get from Portainer stack settings)

   If you have multiple stacks, add:
   - PORTAINER_REDEPLOY_HOOK_2 (for second stack)
   - PORTAINER_REDEPLOY_HOOK_BOT (for bot-hoster, etc.)

2. Configure Portainer Stack:
   - CRITICAL: Use the 'deploy' branch, NOT the main branch
   - The deploy branch contains SHA-tagged images (e.g., ghcr.io/owner/repo:abc123...)
   - This ensures you know exactly which version is deployed

   Portainer Environment Variables to Configure:
   - HOSTNAME: Your domain name (e.g., bot.example.com)
   - NETWORK_NAME: Traefik network name (optional, defaults to traefik_network)
   - Plus any application-specific environment variables

3. To get webhook URL from Portainer:
   - Open your stack in Portainer
   - Click on "Webhooks"
   - Copy the webhook URL

How it works:
- Push to main branch → CI builds and tags image with commit SHA
- CI updates deploy branch with the new SHA tag
- Portainer watches deploy branch and auto-updates
- You always know which exact commit is deployed
```

## Project Examples

Refer to these projects for patterns:

1. **virusgame** - Multi-service with WebSocket support
2. **madrookbot** - Multi-service (bot + qdrant + tool-api)
3. **countrycounter** - Single service with Traefik

## Troubleshooting

**Image tags not updating:**
- Check sed patterns in GitHub Actions workflow
- Verify all docker-compose files are included in sed commands

**Webhook not triggering:**
- Verify secret name matches in workflow and GitHub settings
- Check Portainer webhook URL is correct
- Test webhook manually with curl

**Traefik not routing:**
- Verify network exists: `docker network ls`
- Check Traefik labels syntax
- Ensure HOSTNAME environment variable is set

## Implementation Checklist

After running this skill, verify:

- [ ] `.github/workflows/deploy.yml` created/updated
- [ ] `docker-compose.yml` has correct image format
- [ ] Traefik labels added (if requested)
- [ ] User reminded about GitHub secrets
- [ ] All services defined in compose file
- [ ] Environment variables documented
- [ ] Volumes configured for persistence

## Next Steps for User

After setup:

1. Add PORTAINER_REDEPLOY_HOOK to GitHub secrets
2. Set up Portainer stack using the docker-compose.yml FROM THE DEPLOY BRANCH
3. Configure environment variables in Portainer
4. Test deployment: Push to main branch
5. Verify CI creates/updates deploy branch with SHA tag
6. Verify Portainer auto-updates the stack
