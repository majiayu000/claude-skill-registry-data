---
name: deploy-guide
description: "Guide user through actual deployment steps for their application. This skill should be used when a project is ready to deploy to production. Walks through pre-deployment checks, deployment execution, and post-deployment verification. Supports VPS/Docker, Cloudflare Pages, fly.io, and Hostinger Shared Hosting."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
  - WebFetch
---

# deploy-guide

<purpose>
Guide the user step-by-step through deploying their application to the chosen hosting target. Performs pre-deployment checks, provides deployment commands, and verifies successful deployment. Creates deployment documentation for future reference.
</purpose>

<role>
BUILDER role with GUIDE approach. Executes deployment steps with user confirmation.
- WILL run deployment commands (with user approval)
- WILL perform pre-deployment checks
- WILL verify deployment success
- WILL create deployment documentation
- WILL troubleshoot common deployment issues
</role>

<output>
- Deployed application
- .docs/deployment-log.md (deployment record and runbook)
- Post-deployment verification results
</output>

---

<workflow>

<phase id="0" name="gather-context">
<action>Understand deployment target and project state.</action>

<check-handoff-docs>
Read .docs/deployment-strategy.md if it exists to understand:
- Chosen deployment target
- Deployment workflow
- Environment configuration

If not present, gather information conversationally.
</check-handoff-docs>

<when-handoff-exists>
"I can see from your deployment strategy that you're deploying to {target}.

Let me verify your project is ready for deployment, then we'll proceed step by step."
</when-handoff-exists>

<when-handoff-missing>
"I don't see .docs/deployment-strategy.md. No problem - let me understand your deployment target.

Where are you deploying?
1. **VPS with Docker** - Your Hostinger VPS using Docker Compose
2. **Cloudflare Pages** - Static/JAMstack deployment
3. **Fly.io** - Containerized full-stack deployment
4. **Hostinger Shared Hosting** - PHP + MySQL deployment

Which target? [1/2/3/4]"
</when-handoff-missing>

<gather-additional-info>
Based on target, gather:
- VPS: Hostname/IP, SSH username, project path
- Cloudflare: Project name, build command, output directory
- Fly.io: App name, region preference
- Shared: FTP/SSH credentials, remote path
</gather-additional-info>
</phase>

<phase id="1" name="pre-deployment-checks">
<action>Verify project is ready for deployment.</action>

<checklist>
Pre-deployment Verification:

**Code Readiness:**
- [ ] All changes committed to git
- [ ] Working branch merged to main (or deploy branch)
- [ ] No uncommitted changes
- [ ] Build passes locally

**Configuration:**
- [ ] Environment variables documented
- [ ] Production config separate from development
- [ ] Secrets not committed to git

**Testing (if applicable):**
- [ ] Tests passing
- [ ] No critical bugs open

**Infrastructure:**
- [ ] Target environment accessible
- [ ] Required services running (database, etc.)
- [ ] DNS configured (if first deployment)
</checklist>

<verification-commands>
```bash
# Check git status
git status

# Verify on correct branch
git branch --show-current

# Check build passes
{build_command}

# Verify tests pass (if configured)
{test_command}
```
</verification-commands>

<prompt-to-user>
Running pre-deployment checks...

{checklist_results}

**Issues Found:** {count}
{issue_details}

Ready to proceed with deployment? [yes/no/fix issues]
</prompt-to-user>
</phase>

<phase id="2" name="deploy">
<action>Execute deployment based on target.</action>

<deployment-targets>

<vps-docker>
<name>VPS with Docker (Hostinger)</name>

<pre-steps>
1. Ensure Docker Compose file is ready
2. Verify SSH access to VPS
3. Confirm project directory exists on VPS
</pre-steps>

<deployment-process>
**Step 1: Connect to VPS**
```bash
ssh {username}@{host}
```

**Step 2: Navigate to project**
```bash
cd /var/www/{project_name}
```

**Step 3: Pull latest code**
```bash
git pull origin main
```

**Step 4: Build and restart containers**
```bash
docker compose pull
docker compose up -d --build
```

**Step 5: Verify containers running**
```bash
docker compose ps
```

**Step 6: Check application logs**
```bash
docker compose logs --tail=50
```

**Step 7: Clean up**
```bash
docker system prune -f
```
</deployment-process>

<first-deployment-extras>
For first-time deployment:

1. Create project directory:
   ```bash
   sudo mkdir -p /var/www/{project_name}
   sudo chown {username}:{username} /var/www/{project_name}
   ```

2. Clone repository:
   ```bash
   cd /var/www/{project_name}
   git clone {repo_url} .
   ```

3. Create production .env:
   ```bash
   cp .env.example .env
   nano .env  # Configure production values
   ```

4. Configure Caddy (reverse proxy):
   ```
   {domain} {
       reverse_proxy localhost:{port}
   }
   ```

5. Reload Caddy:
   ```bash
   sudo systemctl reload caddy
   ```
</first-deployment-extras>
</vps-docker>

<cloudflare-pages>
<name>Cloudflare Pages</name>

<pre-steps>
1. Ensure Cloudflare account connected
2. Verify build configuration
3. Confirm project name
</pre-steps>

<deployment-process>
**Option A: Git-Connected (Automatic)**

If connected to GitHub:
1. Push to main branch
2. Cloudflare automatically deploys
3. Monitor build in Cloudflare dashboard

**Option B: Direct Deploy (Manual)**

Using Wrangler CLI:
```bash
# Install/update Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Build project
{build_command}

# Deploy
wrangler pages deploy {output_dir} --project-name={project_name}
```
</deployment-process>

<first-deployment-extras>
For first-time deployment:

1. Create project in Cloudflare Pages dashboard
2. Connect to GitHub repository (recommended)
3. Configure build settings:
   - Build command: `npm run build`
   - Build output directory: `out` or `dist` or `.next`
4. Set environment variables in dashboard
</first-deployment-extras>
</cloudflare-pages>

<fly-io>
<name>Fly.io</name>

<pre-steps>
1. Ensure fly.toml exists
2. Verify Fly CLI installed and authenticated
3. Confirm app created
</pre-steps>

<deployment-process>
**Step 1: Verify fly.toml**
Ensure fly.toml is configured correctly.

**Step 2: Deploy**
```bash
flyctl deploy
```

**Step 3: Monitor deployment**
```bash
flyctl logs
```

**Step 4: Verify running**
```bash
flyctl status
```

**Step 5: Open application**
```bash
flyctl open
```
</deployment-process>

<first-deployment-extras>
For first-time deployment:

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Authenticate:
   ```bash
   flyctl auth login
   ```

3. Create app:
   ```bash
   flyctl apps create {app_name}
   ```

4. Create fly.toml (or use `flyctl launch`)

5. Set secrets:
   ```bash
   flyctl secrets set DATABASE_URL="..."
   flyctl secrets set SECRET_KEY="..."
   ```

6. Create database (if needed):
   ```bash
   flyctl postgres create
   flyctl postgres attach
   ```
</first-deployment-extras>
</fly-io>

<hostinger-shared>
<name>Hostinger Shared Hosting</name>

<pre-steps>
1. Ensure FTP/SSH credentials available
2. Verify remote path
3. Confirm PHP version compatibility
</pre-steps>

<deployment-process>
**Option A: Using Git (if SSH available)**

```bash
# SSH to server
ssh {username}@{host}

# Navigate to public_html
cd ~/public_html/{subdirectory}

# Pull latest code
git pull origin main

# Install dependencies (if composer)
composer install --no-dev --optimize-autoloader
```

**Option B: Using rsync**

```bash
rsync -avz --delete \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='node_modules' \
  ./ {username}@{host}:~/public_html/{subdirectory}/
```

**Option C: Using FTP**

Use FileZilla or similar:
1. Connect to FTP server
2. Navigate to public_html
3. Upload files (excluding .env, node_modules, .git)
</deployment-process>

<first-deployment-extras>
For first-time deployment:

1. Create subdirectory (if not root):
   ```bash
   mkdir -p ~/public_html/{subdirectory}
   ```

2. Create .htaccess (for PHP routing):
   ```
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule ^(.*)$ index.php [QSA,L]
   ```

3. Configure database in cPanel
4. Create production .env on server
5. Set correct file permissions:
   ```bash
   find . -type f -exec chmod 644 {} \;
   find . -type d -exec chmod 755 {} \;
   ```
</first-deployment-extras>
</hostinger-shared>

</deployment-targets>

<execution-approach>
For each deployment step:
1. Show the command about to run
2. Ask for confirmation before executing
3. Show output
4. Verify success before proceeding
5. Offer to stop if errors occur
</execution-approach>
</phase>

<phase id="3" name="post-deployment-verification">
<action>Verify deployment was successful.</action>

<verification-checks>
**Accessibility:**
- [ ] Application loads at expected URL
- [ ] No 500 errors on main pages
- [ ] Static assets loading correctly

**Functionality:**
- [ ] Authentication works (if applicable)
- [ ] Database connections working
- [ ] API endpoints responding

**Performance:**
- [ ] Reasonable load time
- [ ] No console errors
- [ ] SSL certificate valid
</verification-checks>

<verification-commands>
```bash
# Check HTTP response
curl -I https://{domain}

# Check SSL certificate
curl -vI https://{domain} 2>&1 | grep "SSL certificate"

# Check specific endpoints
curl https://{domain}/api/health
```
</verification-commands>

<prompt-to-user>
Verifying deployment...

{verification_results}

**Status:** {SUCCESS/ISSUES_FOUND}
{details}

{if success}
Your application is live at: https://{domain}

{if issues}
Issues detected. Would you like help troubleshooting? [yes/no]
</prompt-to-user>
</phase>

<phase id="4" name="create-deployment-log">
<action>Create .docs/deployment-log.md documenting the deployment.</action>

<deployment-log-template>
```markdown
# Deployment Log

## Latest Deployment

**Date:** {date}
**Target:** {deployment_target}
**Branch:** {branch}
**Commit:** {commit_hash}
**Deployed by:** {user}
**Status:** SUCCESS

### Pre-Deployment Checks
- [x] Code committed and pushed
- [x] Build passed locally
- [x] Tests passing
- [x] Environment configured

### Deployment Steps Executed
1. {step_1}
2. {step_2}
3. {step_3}

### Post-Deployment Verification
- [x] Application accessible
- [x] No errors in logs
- [x] Core functionality working

### URLs
- **Production:** https://{domain}
- **API:** https://{domain}/api

---

## Deployment Runbook

### Regular Deployment

```bash
{deployment_commands}
```

### Rollback Procedure

```bash
{rollback_commands}
```

### Environment Variables

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| {var_1} | {desc} | {location} |
| {var_2} | {desc} | {location} |

---

## Deployment History

| Date | Commit | Status | Notes |
|------|--------|--------|-------|
| {date} | {hash} | SUCCESS | Initial deployment |

---

## Troubleshooting

### Common Issues

**Application not loading:**
- Check container status: `docker compose ps`
- Check logs: `docker compose logs`
- Verify Caddy config

**Database connection failed:**
- Verify DATABASE_URL in .env
- Check database container running
- Test connection manually

**SSL certificate issues:**
- Caddy auto-generates certificates
- Check Caddy logs: `sudo journalctl -u caddy`
- Verify DNS pointing to server
```
</deployment-log-template>
</phase>

<phase id="5" name="summarize">
<action>Provide deployment summary and next steps.</action>

<summary-template>
## Deployment Complete

**Application:** {project_name}
**Target:** {deployment_target}
**URL:** https://{domain}
**Status:** SUCCESS

---

### Deployment Record

Created: .docs/deployment-log.md

This file contains:
- Deployment runbook for future deployments
- Rollback procedure
- Environment variables reference
- Troubleshooting guide

---

### Workflow Status

**TERMINATION POINT - MANUAL DEPLOYMENT**

Your application is deployed. You can stop here if you don't need CI/CD automation.

**Next Options:**
1. **Stop here** - Use .docs/deployment-log.md for future manual deployments
2. **Add CI/CD** - Use **ci-cd-implement** skill to automate deployments

---

### For Future Deployments

Quick deployment:
```bash
{quick_deploy_command}
```

See .docs/deployment-log.md for full runbook.

---

### Monitoring Recommendations

- Check logs regularly: `{log_command}`
- Monitor uptime with external service
- Set up alerts for errors

---

Congratulations on your deployment!
</summary-template>
</phase>

</workflow>

---

<troubleshooting>

<common-issues>

<docker-issues>
**Container won't start:**
```bash
# Check logs
docker compose logs {service_name}

# Rebuild from scratch
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Port already in use:**
```bash
# Find process using port
sudo lsof -i :{port}

# Kill process or change port in docker-compose.yml
```

**Out of disk space:**
```bash
# Clean up Docker
docker system prune -a --volumes
```
</docker-issues>

<networking-issues>
**Application not accessible:**
1. Check if container is running: `docker compose ps`
2. Test locally: `curl localhost:{port}`
3. Check Caddy/reverse proxy logs
4. Verify firewall allows traffic: `sudo ufw status`

**SSL certificate not working:**
1. Verify DNS points to server
2. Check Caddy logs: `sudo journalctl -u caddy -f`
3. Wait for certificate propagation (up to 15 minutes)
</networking-issues>

<database-issues>
**Connection refused:**
1. Check database container: `docker compose ps db`
2. Verify DATABASE_URL format
3. Check network: containers must be on same Docker network

**Permission denied:**
1. Verify user credentials in .env
2. Check database user has required permissions
</database-issues>

<cloudflare-issues>
**Build failed:**
1. Check build command matches local
2. Verify Node.js version in dashboard
3. Check build logs in Cloudflare dashboard

**Environment variables:**
1. Set in Cloudflare Pages dashboard
2. Redeploy after changing
</cloudflare-issues>

<fly-issues>
**Deploy failed:**
1. Check fly.toml configuration
2. Verify app name matches
3. Check resource limits (memory, CPU)

**App crashing:**
1. Check logs: `flyctl logs`
2. Verify health check endpoint
3. Check memory usage: `flyctl status`
</fly-issues>

</common-issues>

</troubleshooting>

---

<guardrails>

<must-do>
- Run pre-deployment checks before deploying
- Ask for confirmation before executing commands
- Verify deployment success
- Create deployment-log.md documentation
- Handle errors gracefully with troubleshooting guidance
- Provide rollback instructions
</must-do>

<must-not-do>
- Deploy without user confirmation
- Skip pre-deployment checks
- Leave failed deployment without troubleshooting help
- Expose sensitive credentials in logs or documentation
- Skip post-deployment verification
</must-not-do>

</guardrails>

---

<workflow-status>
Phase 5 of 7: Deployment

Status:
  Phase 0: Project Brief (project-brief-writer)
  Phase 1: Tech Stack (tech-stack-advisor)
  Phase 2: Deployment Strategy (deployment-advisor)
  Phase 3: Project Foundation (project-spinup) <- TERMINATION POINT (localhost)
  Phase 4: Test Strategy (test-orchestrator) - optional
  Phase 5: Deployment (you are here) <- TERMINATION POINT (manual deploy)
  Phase 6: CI/CD (ci-cd-implement) <- TERMINATION POINT (full automation)
</workflow-status>

---

<integration-notes>

<workflow-position>
Phase 5 of 7 in the Skills workflow chain.
Expected input: Deployable project, .docs/deployment-strategy.md (gathered conversationally if missing)
Produces: Deployed application, .docs/deployment-log.md

This is a TERMINATION POINT for projects not needing CI/CD automation.
</workflow-position>

<flexible-entry>
This skill can be invoked standalone on any deployable project. It gathers deployment target information conversationally if not available in handoff documents.
</flexible-entry>

<when-to-invoke>
- When project development is complete (or MVP ready)
- When user is ready to deploy to production
- For subsequent deployments (use deployment-log.md as runbook)
</when-to-invoke>

<status-utility>
Users can invoke the **workflow-status** skill at any time to:
- See current workflow progress
- Check which phases are complete
- Get guidance on next steps
- Review all handoff documents

Mention this option when users seem uncertain about their progress.
</status-utility>

</integration-notes>
