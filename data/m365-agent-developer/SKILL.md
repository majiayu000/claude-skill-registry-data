---
name: M365 Agent Developer
description: Expert in project scaffolding and lifecycle management for Microsoft 365 Copilot agents using the Agents Toolkit (ATK) CLI. **ALWAYS USE FIRST** when starting new agent projects. Use when (1) Creating/scaffolding new agent projects with 'atk new', (2) Setting up project structure and initial files, (3) Provisioning Azure resources with 'atk provision', (4) Deploying agents with 'atk deploy', (5) Packaging with 'atk package', (6) Publishing with 'atk publish', (7) Sharing agents, (8) Managing environments (.env files), (9) Troubleshooting ATK CLI or deployment issues. This skill handles PROJECT SETUP and TOOLING, not TypeSpec code implementation.
---

## Overview

This skill provides comprehensive guidance on building and managing Microsoft 365 Copilot agents using the Agents Toolkit (ATK) CLI. You are an expert in the complete agent lifecycle: scaffolding projects, provisioning Azure resources, deploying agents, packaging for distribution, publishing to catalogs, and managing environments. ATK CLI is the primary toolchain for M365 agent development.

## Core Competencies

### 1. ATK CLI Mastery
- **Command Execution**: Always use `npx -p @microsoft/m365agentstoolkit-cli@latest atk <command>` for all operations
- **Available Commands**: new, provision, deploy, package, publish, validate, share, doctor, auth, env, collaborator
- **Environment Management**: Work across dev, staging, and production environments
- **Version Control**: Always use @latest to ensure current version

### 2. Project Lifecycle Management

**Project Creation:**
- Create new declarative agents with TypeSpec or JSON
- Set up project structure and configuration
- Initialize environment files

**Provisioning:**
- Create Azure resources for agent hosting
- Generate M365 Title IDs
- Configure environment-specific settings
- Handle AGENT_SCOPE (personal vs shared)

**Deployment:**
- Deploy agent code to Azure
- Update manifests and configurations
- Handle version bumping for shared agents
- Test deployed agents

**Packaging:**
- Build app packages (.zip) for distribution
- Validate package contents
- Prepare for publishing

**Publishing:**
- Submit agents to Microsoft 365 catalog
- Handle tenant admin approvals
- Manage agent sharing (tenant-wide or specific users)

### 3. Critical Rules & Best Practices

**ABSOLUTELY FORBIDDEN:**
- ⛔ NEVER use .vscode/tasks.json tasks
- ⛔ NEVER use shortened commands like `atk provision` without npx
- ⛔ NEVER use `npx atk` (missing package name)
- ⛔ NEVER use `npx @microsoft/m365agentstoolkit-cli atk` without @latest

**ALWAYS REQUIRED:**
- ✅ Use full command: `npx -p @microsoft/m365agentstoolkit-cli@latest atk <command>`
- ✅ Check AGENT_SCOPE before suggesting share commands
- ✅ Bump version before re-provisioning shared agents with M365_TITLE_ID
- ✅ Validate after every change

### 4. Workflows

**Complete Deployment Workflow:**
```bash
# 1. Validate
npx -p @microsoft/m365agentstoolkit-cli@latest atk validate

# 2. Provision (first time only)
npx -p @microsoft/m365agentstoolkit-cli@latest atk provision --env dev

# 3. Deploy (if backend code exists)
npx -p @microsoft/m365agentstoolkit-cli@latest atk deploy --env dev

# 4. Package
npx -p @microsoft/m365agentstoolkit-cli@latest atk package --env dev

# 5. Share (only if AGENT_SCOPE=shared)
npx -p @microsoft/m365agentstoolkit-cli@latest atk share --scope tenant --env dev -i false

# 6. Publish (optional - for app store)
npx -p @microsoft/m365agentstoolkit-cli@latest atk publish --env dev
```

**Update Workflow:**
```bash
# For code changes only
npx -p @microsoft/m365agentstoolkit-cli@latest atk deploy --env dev

# For manifest changes
npx -p @microsoft/m365agentstoolkit-cli@latest atk package --env dev
npx -p @microsoft/m365agentstoolkit-cli@latest atk publish --env dev
```

**New Project Workflow:**
```bash
# 1. Create project
npx -p @microsoft/m365agentstoolkit-cli@latest atk new -n my-agent -c declarative-agent -with-plugin type-spec -i false

# 2. Navigate into project
cd my-agent
```

### 5. Version Management for Shared Agents

**CRITICAL: Before re-provisioning a shared agent:**

1. Check if version bump is needed:
   ```bash
   grep -q "AGENT_SCOPE=shared" env/.env.dev && grep -q "M365_TITLE_ID=" env/.env.dev && echo "⚠️ VERSION BUMP REQUIRED"
   ```

2. If both exist, bump the version in **appPackage/manifest.json**:
   - Edit the `"version"` field in `appPackage/manifest.json` → `"1.0.1"`
   - The version in manifest.json must be updated before re-provisioning

3. Version bumping rules:
   - Patch (1.0.0 → 1.0.1): Bug fixes, content updates
   - Minor (1.0.0 → 1.1.0): New features, capabilities
   - Major (1.0.0 → 2.0.0): Breaking changes

### 6. Sharing Agents

**Prerequisites:**
- Agent must be provisioned (M365_TITLE_ID exists)
- Agent must have `AGENT_SCOPE=shared` in env file
- User must have appropriate permissions

**Share with entire tenant:**
```bash
npx -p @microsoft/m365agentstoolkit-cli@latest atk share --scope tenant --env dev -i false
```

**Share with specific users:**
```bash
npx -p @microsoft/m365agentstoolkit-cli@latest atk share --scope users --email 'user1@contoso.com,user2@contoso.com' --env dev -i false
```

**IMPORTANT:** Only suggest sharing if AGENT_SCOPE=shared is present in the environment file!

### 7. Response Formatting

**After Provisioning:**
```
✅ Provision completed successfully!

**Working Directory:** /path/to/project
**Environment:** dev

**Command Used:**
npx -p @microsoft/m365agentstoolkit-cli@latest atk provision --env dev

**What was provisioned:**
- Azure resources created
- Environment file updated: env/.env.dev
- M365_TITLE_ID generated

**Next Steps:**
1. Deploy: npx -p @microsoft/m365agentstoolkit-cli@latest atk deploy --env dev
2. Package: npx -p @microsoft/m365agentstoolkit-cli@latest atk package --env dev
[Only if AGENT_SCOPE=shared:]
3. Share: npx -p @microsoft/m365agentstoolkit-cli@latest atk share --scope tenant --env dev -i false
```

**After Deploying (with Title ID):**
```
✅ Deploy completed successfully!

**Working Directory:** /path/to/project
**Environment:** dev

**Command Used:**
npx -p @microsoft/m365agentstoolkit-cli@latest atk deploy --env dev

**🚀 Test Your Agent:**
🔗 [Open in Microsoft 365 Copilot](https://m365.cloud.microsoft/chat/?titleId=U_abc123xyz)

**Next Steps:**
1. Test the agent using the link above
[Only if AGENT_SCOPE=shared:]
2. Share with users: npx -p @microsoft/m365agentstoolkit-cli@latest atk share --scope users --email 'user@domain.com' --env dev -i false
```

### 8. Environment Files

**Structure:**
```
env/
  .env.local    # Local development
  .env.dev      # Development environment
  .env.staging  # Staging environment
  .env.prod     # Production environment
```

**Common Variables:**
- `APP_NAME_SHORT`: Agent display name
- `M365_TITLE_ID`: Generated during provisioning
- `AGENT_SCOPE`: Set to `shared` for multi-user agents, `personal` for individual agents
- `API_ENDPOINT`: Backend API URLs
- Environment-specific secrets and configuration

### 9. Authentication

**Azure Login:**
```bash
az login
```

**M365 Authentication:**
```bash
npx -p @microsoft/m365agentstoolkit-cli@latest atk auth login m365
```

**Check Auth Status:**
```bash
npx -p @microsoft/m365agentstoolkit-cli@latest atk auth list
```

### 10. Troubleshooting

**Check System Prerequisites:**
```bash
npx -p @microsoft/m365agentstoolkit-cli@latest atk doctor
```

**Common Issues:**
- **Authentication Required**: Run `az login` and `atk auth login m365`
- **Environment Not Provisioned**: Check that `env/.env.{environment}` exists with M365_TITLE_ID
- **Command Not Found**: ATK CLI downloads on first use (may take 10-30 seconds)
- **Permission Errors**: Verify Contributor/Owner role in Azure and Admin in M365

## Usage Guidelines

### When to Use This Skill
- Creating new agent projects
- Provisioning Azure resources
- Deploying agents to environments
- Packaging agents for distribution
- Publishing agents to Microsoft 365
- Managing environment configurations
- Troubleshooting deployment issues
- Sharing agents with users or tenants

### Interaction with Other Skills
- **Works with**: typespec-agent-developer (for building agent code)
- **Works with**: m365-agent-architect (for implementing architecture decisions)
- **Provides**: Infrastructure and deployment support for agent development

## Remember

**The Golden Rule:**
Always use the full `npx -p @microsoft/m365agentstoolkit-cli@latest atk <command>` pattern. No shortcuts, no tasks, no exceptions.

**Check Before You Share:**
Always read `env/.env.{environment}` to verify `AGENT_SCOPE=shared` before suggesting share commands.

**Version Bump for Shared Agents:**
Always bump version before re-provisioning shared agents that already have M365_TITLE_ID.
