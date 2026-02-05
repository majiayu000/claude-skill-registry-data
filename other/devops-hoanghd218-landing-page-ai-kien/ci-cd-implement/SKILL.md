---
name: ci-cd-implement
description: "Analyze a project and implement CI/CD pipelines tailored to its tech stack and deployment target. This skill should be used when a project is ready for automated testing and/or deployment. Generates GitHub Actions workflows, deployment scripts, and secrets documentation. Works as a standalone utility on any project."
---

# ci-cd-implement

<purpose>
Analyze an existing project's structure, tech stack, and deployment target to generate production-ready CI/CD pipelines. Provides GitHub Actions workflows for continuous integration (testing, linting, building) and continuous deployment to supported hosting targets.
</purpose>

<output>
- .github/workflows/ci.yml (if CI requested)
- .github/workflows/deploy.yml (if CD requested)
- scripts/deploy.sh (for VPS/manual deployment targets)
- scripts/rollback.sh (for VPS deployments)
- CICD-SECRETS.md (documentation of required secrets)
</output>

---

<workflow>

<phase id="0" name="analyze-project">
<action>Scan project to understand tech stack, existing configuration, and deployment target.</action>

<project-analysis>
Look for and analyze:

1. Package/dependency files:
   - package.json (Node.js/frontend)
   - requirements.txt / pyproject.toml (Python)
   - composer.json (PHP)
   - go.mod (Go)
   - Cargo.toml (Rust)

2. Existing CI/CD:
   - .github/workflows/ (existing GitHub Actions)
   - Dockerfile, docker-compose.yml

3. Test configuration:
   - Test commands in package.json scripts
   - pytest.ini, jest.config.js, vitest.config.ts
   - phpunit.xml

4. Linting/formatting:
   - .eslintrc, .prettierrc
   - ruff.toml, pyproject.toml [tool.ruff]
   - phpcs.xml

5. Type checking:
   - tsconfig.json (TypeScript)
   - mypy.ini, pyrightconfig.json (Python)

6. Build configuration:
   - next.config.js, vite.config.ts
   - Build scripts in package.json

7. Deployment hints:
   - .docs/deployment-strategy.md (from workflow)
   - fly.toml (Fly.io)
   - wrangler.toml (Cloudflare)
   - Caddyfile references
</project-analysis>

<extract-information>
From analysis, determine:
- Primary language/framework
- Test command (e.g., npm test, pytest, phpunit)
- Lint command (e.g., npm run lint, ruff check)
- Type check command (e.g., npx tsc --noEmit)
- Build command (e.g., npm run build)
- Deployment target (cloudflare-pages, fly-io, vps-docker, hostinger-shared)
- Database type (if any)
- Environment variables needed
</extract-information>

<check-deployment-strategy>
Read .docs/deployment-strategy.md if it exists to understand:
- Chosen deployment target
- Deployment workflow
- Environment configuration
</check-deployment-strategy>
</phase>

<phase id="1" name="gather-preferences">
<action>Ask user what pipelines to generate.</action>

<prompt-to-user>
I've analyzed your project. Before generating pipelines, what would you like?

**Pipeline Options:**

1. **CI only** - Automated testing, linting, and builds on every push/PR
   Best for: Projects not ready for automated deployment, or deploying manually

2. **CD only** - Automated deployment to your hosting target
   Best for: Projects with existing CI, or simple projects where you trust manual testing

3. **Both CI + CD** - Complete pipeline from code push to deployment
   Best for: Most production projects

Which would you like? [1/2/3]
</prompt-to-user>

<store-preference>
Record user choice as: ci_only, cd_only, or both
</store-preference>
</phase>

<phase id="2" name="determine-complexity">
<action>Assess project complexity to determine environment strategy.</action>

<complexity-indicators>
Simple project (production only):
- Single developer
- Low traffic expectations
- No sensitive data
- Personal or small public project
- No existing staging setup

Complex project (staging + production):
- Multiple contributors
- Higher traffic expectations
- Handles user data or payments
- Existing staging/production separation
- deployment-strategy.md indicates professional uptime needs
</complexity-indicators>

<environment-decision>
Based on indicators:
- Simple: Generate single production deployment
- Complex: Generate staging + production with promotion workflow

If unclear from analysis, default to production-only for first implementation.
Note in output that staging can be added later.
</environment-decision>
</phase>

<phase id="3" name="generate-ci">
<action>Create GitHub Actions CI workflow if requested.</action>

<skip-condition>If user selected cd_only, skip to phase 4.</skip-condition>

<ci-components>
Include based on project analysis:
- Checkout code
- Set up language runtime (Node.js, Python, PHP, etc.)
- Install dependencies
- Run linting (if detected)
- Run type checking (if detected)
- Run tests (if detected)
- Run build (if detected)
- Cache dependencies for speed
</ci-components>

<ci-workflow-template>
```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Language-specific setup inserted here

      - name: Install dependencies
        run: {install_command}

      # Conditional steps based on detection:

      - name: Lint
        run: {lint_command}

      - name: Type check
        run: {typecheck_command}

      - name: Test
        run: {test_command}

      - name: Build
        run: {build_command}
```
</ci-workflow-template>

<language-setup-templates>

<nodejs>
```yaml
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
```
</nodejs>

<python>
```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
```
</python>

<php>
```yaml
      - name: Set up PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          tools: composer
```
</php>

</language-setup-templates>
</phase>

<phase id="4" name="generate-cd">
<action>Create deployment workflow and scripts based on deployment target.</action>

<skip-condition>If user selected ci_only, skip to phase 5.</skip-condition>

<deployment-targets>

<cloudflare-pages>
<description>Static/JAMstack deployment via Wrangler CLI</description>

<workflow-template>
```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy {build_output_dir} --project-name={project_name}
```
</workflow-template>

<secrets-needed>
- CLOUDFLARE_API_TOKEN: API token with Pages edit permissions
- CLOUDFLARE_ACCOUNT_ID: Your Cloudflare account ID
</secrets-needed>
</cloudflare-pages>

<fly-io>
<description>Containerized deployment via Fly.io CLI</description>

<workflow-template>
```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Fly.io CLI
        uses: superfly/flyctl-actions/setup-flyctl@master

      - name: Deploy to Fly.io
        run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```
</workflow-template>

<secrets-needed>
- FLY_API_TOKEN: Fly.io API token (flyctl tokens create deploy)
</secrets-needed>

<prerequisites>
- fly.toml must exist in project root
- App must be created: flyctl apps create {app-name}
</prerequisites>
</fly-io>

<vps-docker>
<description>Docker deployment to VPS via SSH</description>

<workflow-template>
```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USERNAME }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /var/www/{project_name}
            git pull origin main
            docker compose pull
            docker compose up -d --build
            docker system prune -f
```
</workflow-template>

<secrets-needed>
- VPS_HOST: VPS IP address or hostname
- VPS_USERNAME: SSH username (e.g., john)
- VPS_SSH_KEY: Private SSH key for authentication
</secrets-needed>

<deploy-script>
Also generate scripts/deploy.sh for manual deployment:

```bash
#!/bin/bash
set -e

echo "Deploying {project_name} to VPS..."

# SSH to VPS and deploy
ssh {username}@{host} << 'EOF'
  cd /var/www/{project_name}
  git pull origin main
  docker compose pull
  docker compose up -d --build
  docker system prune -f
  echo "Deployment complete!"
EOF
```
</deploy-script>

<rollback-script>
Generate scripts/rollback.sh:

```bash
#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./scripts/rollback.sh <commit-hash>"
  exit 1
fi

echo "Rolling back to $1..."

ssh {username}@{host} << EOF
  cd /var/www/{project_name}
  git fetch origin
  git checkout $1
  docker compose up -d --build
  echo "Rolled back to $1"
EOF
```
</rollback-script>
</vps-docker>

<hostinger-shared>
<description>PHP deployment via rsync/FTP</description>

<workflow-template>
```yaml
name: Deploy to Shared Hosting

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy via rsync
        uses: burnett01/rsync-deployments@6.0.0
        with:
          switches: -avzr --delete --exclude='.git' --exclude='.github' --exclude='.env'
          path: ./
          remote_path: ${{ secrets.REMOTE_PATH }}
          remote_host: ${{ secrets.FTP_HOST }}
          remote_user: ${{ secrets.FTP_USERNAME }}
          remote_key: ${{ secrets.SSH_KEY }}
```
</workflow-template>

<secrets-needed>
- FTP_HOST: Shared hosting server hostname
- FTP_USERNAME: FTP/SSH username
- SSH_KEY: Private key for SSH access (or use FTP credentials)
- REMOTE_PATH: Path on server (e.g., /home/user/public_html)
</secrets-needed>

<alternative-ftp>
If SSH not available, use FTP action instead:

```yaml
      - name: Deploy via FTP
        uses: SamKirkland/FTP-Deploy-Action@v4.3.4
        with:
          server: ${{ secrets.FTP_HOST }}
          username: ${{ secrets.FTP_USERNAME }}
          password: ${{ secrets.FTP_PASSWORD }}
          local-dir: ./
          server-dir: ${{ secrets.REMOTE_PATH }}
```
</alternative-ftp>
</hostinger-shared>

</deployment-targets>

<staging-production>
If complexity warrants staging + production:

<staging-workflow>
Deploy to staging on push to dev branch:
```yaml
on:
  push:
    branches: [dev]
```
Use staging-specific secrets (STAGING_* prefix).
</staging-workflow>

<production-workflow>
Deploy to production on push to main branch:
```yaml
on:
  push:
    branches: [main]
```
Use production secrets.
</production-workflow>

<promotion-note>
Document in README: "To promote staging to production, merge dev into main."
</promotion-note>
</staging-production>
</phase>

<phase id="5" name="document-secrets">
<action>Create CICD-SECRETS.md documenting all required secrets.</action>

<secrets-template>
```markdown
# CI/CD Secrets Configuration

This document lists the secrets required for the CI/CD pipelines.

## GitHub Actions Secrets

Add these secrets in your repository settings:
**Settings -> Secrets and variables -> Actions -> New repository secret**

### Required Secrets

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
{secrets_table}

## Setup Instructions

{target_specific_instructions}

## Verification

After adding secrets, trigger a workflow run to verify configuration:

```bash
git commit --allow-empty -m "test: verify CI/CD pipeline"
git push
```

Check the Actions tab for workflow results.
```
</secrets-template>

<target-instructions>

<cloudflare-instructions>
### Cloudflare Pages Setup

1. Log in to Cloudflare Dashboard
2. Go to **My Profile -> API Tokens -> Create Token**
3. Use "Edit Cloudflare Workers" template or create custom with Pages permissions
4. Copy the token as CLOUDFLARE_API_TOKEN
5. Find Account ID in dashboard URL or **Workers & Pages -> Overview** sidebar
</cloudflare-instructions>

<fly-instructions>
### Fly.io Setup

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Authenticate: `flyctl auth login`
3. Create deploy token: `flyctl tokens create deploy -x 999999h`
4. Copy the token as FLY_API_TOKEN
</fly-instructions>

<vps-instructions>
### VPS (Hostinger) Setup

1. Generate SSH key pair (if not exists):
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy"
   ```
2. Add public key to VPS:
   ```bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub john@your-vps-ip
   ```
3. Copy private key content as VPS_SSH_KEY
4. Set VPS_HOST to your VPS IP or hostname
5. Set VPS_USERNAME to your SSH username (john)
</vps-instructions>

<shared-instructions>
### Shared Hosting Setup

1. Get FTP/SSH credentials from Hostinger hPanel
2. Set FTP_HOST to the server hostname
3. Set FTP_USERNAME to your FTP username
4. For SSH: Generate and add key pair, copy private key as SSH_KEY
5. For FTP: Set FTP_PASSWORD (less secure than SSH)
6. Set REMOTE_PATH to your document root (e.g., /home/user/public_html)
</shared-instructions>

</target-instructions>
</phase>

<phase id="6" name="summarize">
<action>Present what was created and provide next steps.</action>

<summary-template>
## CI/CD Implementation Complete

**Project:** {project_name}
**Deployment Target:** {deployment_target}
**Pipelines Generated:** {ci_and_or_cd}

---

### Files Created

{files_list}

---

### Workflow Status

**WORKFLOW TERMINATION POINT - FULL AUTOMATION**

Your project now has complete CI/CD automation:
- Automated testing on every push/PR (if CI generated)
- Automated deployment to {target} (if CD generated)

This completes the Skills workflow.

---

### Next Steps

1. **Review generated workflows**
   - Check `.github/workflows/` files
   - Verify commands match your project

2. **Configure secrets**
   - Open `CICD-SECRETS.md` for instructions
   - Add secrets in GitHub repository settings

3. **Test the pipeline**
   ```bash
   git add .
   git commit -m "ci: add CI/CD pipeline"
   git push
   ```

4. **Monitor first run**
   - Go to repository -> Actions tab
   - Watch workflow execution
   - Debug any failures

{additional_notes}

---

Happy deploying!
</summary-template>

<additional-notes-options>
- For VPS: "Ensure /var/www/{project_name} exists and has correct permissions"
- For staging+production: "Staging deploys from dev branch, production from main"
- For first deployment: "You may need to manually deploy once to initialize the environment"
</additional-notes-options>
</phase>

</workflow>

---

<guardrails>

<must-do>
- Analyze project before generating anything
- Ask about CI/CD preference before generating
- Generate only what was requested (CI, CD, or both)
- Include secrets documentation for every deployment
- Use project-specific values (not placeholders) where detectable
- Make scripts executable (include shebang, set -e)
- Include rollback capability for VPS deployments
- Note prerequisites (fly.toml, initial app creation, etc.)
- Read .docs/deployment-strategy.md if it exists
</must-do>

<must-not-do>
- Generate pipelines for localhost deployment target
- Include actual secret values in generated files
- Skip project analysis phase
- Generate staging+production for simple projects without justification
- Assume deployment target without checking project
- Generate deployment to targets not in the supported list
</must-not-do>

</guardrails>

---

<workflow-status>
Phase 6 of 7: CI/CD Implementation (Final Phase)

Status:
  Phase 0: Project Brief (project-brief-writer)
  Phase 1: Tech Stack (tech-stack-advisor)
  Phase 2: Deployment Strategy (deployment-advisor)
  Phase 3: Project Foundation (project-spinup) <- TERMINATION POINT (localhost)
  Phase 4: Test Strategy (test-orchestrator) - optional
  Phase 5: Deployment (deploy-guide) <- TERMINATION POINT (manual deploy)
  Phase 6: CI/CD (you are here) <- TERMINATION POINT (full automation)
</workflow-status>

---

<user-context>

<infrastructure>
- Hostinger VPS8: 8 cores, 32GB RAM, 400GB storage
  - Docker/Docker Compose
  - SSH as user "john"
  - Caddy for reverse proxy
- Cloudflare DNS
- Backblaze B2 for storage
- GitHub for version control
</infrastructure>

<deployment-targets-supported>
1. hostinger-shared - PHP + MySQL via cPanel (rsync/FTP)
2. cloudflare-pages - Static/JAMstack (Wrangler)
3. fly-io - Containerized apps (flyctl)
4. vps-docker - Docker on Hostinger VPS (SSH + docker compose)

NOT supported: localhost (no CI/CD needed for localhost)
</deployment-targets-supported>

</user-context>

---

<integration-notes>

<workflow-position>
Phase 6 of 7 in the Skills workflow chain (final phase).
Expected input: Project structure, .docs/deployment-strategy.md (if exists)
Produces: .github/workflows/, scripts/, CICD-SECRETS.md

This is a TERMINATION POINT - workflow complete after this skill.
</workflow-position>

<flexible-entry>
This skill can be invoked standalone on any project with a deployment target. It analyzes the project structure to generate appropriate pipelines.
</flexible-entry>

<localhost-note>
If the project's deployment target is localhost (from .docs/deployment-strategy.md or user confirmation), inform the user that CI/CD is not applicable for localhost projects and the workflow is already complete.
</localhost-note>

<status-utility>
Users can invoke the **workflow-status** skill at any time to:
- See current workflow progress
- Check which phases are complete
- Get guidance on next steps
- Review all handoff documents

Mention this option when users seem uncertain about their progress.
</status-utility>

</integration-notes>
