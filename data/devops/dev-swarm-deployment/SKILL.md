---
name: dev-swarm-deployment
description: Deploy application to staging/production environments, setup CD pipelines, manage cloud infrastructure, and configure monitoring. Use when user asks to deploy application, setup production environment, or configure automated deployment.
---

# AI Builder - Deployment

This skill handles the deployment of applications to various environments (staging, production), sets up CD pipelines, manages cloud infrastructure, and configures monitoring and logging systems.

## When to Use This Skill

- User asks to deploy the application
- User wants to setup production or staging environment
- User needs CD pipeline configuration
- User wants to configure cloud infrastructure (AWS, Azure, GCP, etc.)
- User needs to setup monitoring, logging, or alerting
- User wants to configure domain names and SSL certificates
- When application is ready for production deployment
- When `09-sprints/` development is complete and ready for release

## Your Roles in This Skill

- **Deployment Engineer**: Execute and manage application deployments to various environments. Identify the best deployment strategy (blue-green, canary, rolling updates) based on project requirements and ensure zero-downtime deployments.
- **Cloud Infrastructure Architect**: Design and implement scalable, cost-effective cloud infrastructure solutions. Make decisions on cloud provider selection, infrastructure as code approach, and resource optimization.
- **DevOps Engineer**: Setup and maintain CI/CD pipelines for automated testing and deployment. Ensure proper integration between development, testing, and production environments.
- **SysOps Engineer**: Provision and manage cloud resources (compute, storage, networking). Configure web servers, load balancers, and security groups. Implement system-wide logging, monitoring, and alerting. Manage infrastructure security and scaling strategies. Ensure high availability and disaster recovery. Optimize cloud costs and resource utilization.
- **Site Reliability Engineer (SRE)**: Implement monitoring, logging, and alerting systems. Ensure application reliability, performance, and quick incident response. Define and track SLIs, SLOs, and error budgets. Implement automated remediation and incident response procedures.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `09-sprints/` folder exists (recommended):**
   - If found: Read to understand:
     - Development progress and readiness
     - Features completed

2. **Check if `07-tech-specs/` folder exists (mandatory):**
   - If NOT found: Inform user they need to define tech specs first, then STOP
   - If found: Read all files to understand:
     - Technology stack chosen
     - Infrastructure requirements
     - Deployment needs

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand all files

4. **Check if this stage should be skipped:**
   - Check if `10-deployment/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 10 (deployment) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed anyway?"
     - **If user says yes:**
       - Delete SKIP.md and continue with this skill
     - **If user says no:**
       - Exit the skill

5. **Check if `10-deployment/` folder exists:**
   - If exists: Read all existing files to understand current deployment state
   - If NOT exists: Will create new structure

6. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

7. **Assess Current State:**
   - Verify build process works (`npm run build`, `docker build`, etc.)
   - Check if tests pass
   - Review tech specs from `07-tech-specs/` for deployment requirements
   - Check if application has production configuration files
   - Look for existing cloud configurations (AWS, Azure, GCP credentials)
   - Check for infrastructure as code files (Terraform, CloudFormation, etc.)
   - Review existing deployment scripts or CI/CD configurations
   - Look for `src/.github/workflows/` (GitHub Actions)
   - Check for other CI/CD configurations (Jenkins, GitLab CI, CircleCI, etc.)

8. **Analyze Deployment Requirements:**

   Based on the tech stack (from `07-tech-specs/`) and project requirements:

   - Determine deployment needs:
     - **L2 Tools/Skills**: Deploy to `dev-swarm/py_scripts`, `dev-swarm/js_scripts`, or `dev-swarm/skills`.
     - **Hosting Platform**: Static hosting (Netlify, Vercel), PaaS (Heroku, Railway), IaaS (AWS EC2, Azure VMs), Container (ECS, Kubernetes), Serverless (Lambda, Cloud Functions)
     - **Database Hosting**: Managed database service vs self-hosted
     - **Storage**: Object storage (S3, Azure Blob), CDN requirements
     - **Compute**: Serverless, containers, or VMs
     - **Environments**: Development, staging, production (number of environments needed)

   - Identify complexity level:
     - **Basic**: Simple static sites or single PaaS deployment
     - **Standard**: Multi-environment setup with managed services, basic CI/CD
     - **Complex**: Multi-region deployment, microservices, advanced CI/CD, infrastructure as code, auto-scaling

   - Determine CD requirements:
     - Automated testing before deployment
     - Deployment approval process
     - Rollback strategy
     - Deployment frequency and schedule

   - Identify monitoring and observability needs:
     - Application performance monitoring (APM)
     - Error tracking and logging
     - Uptime monitoring
     - Alerting channels (email, Slack, PagerDuty)
     - Analytics and metrics

9. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first based on previous stage results, get user approval, then create deployment plan files.**

1. **Analyze information from previous stages:**
   - Read `07-tech-specs/` to understand technology stack and infrastructure needs
   - Consider cost-budget constraints for deployment
   - Assess application readiness from Step 0

2. **Create or update 10-deployment/README.md with refined requirements:**
   - **For L2 projects:** Create a simple README (just several lines) indicating the project level and the target deployment directory (e.g., `dev-swarm/py_scripts` or `dev-swarm/skills`).
   - **For L3+ projects:** List deliverables explicitly in README (typical: infrastructure-plan.md, cd-pipeline.md, deployment-strategy.md, monitoring-logging.md, environment-config.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Deployment Engineer (lead), DevOps Engineer, SysOps Engineer, Site Reliability Engineer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What deployment will include:**
     - For L2: Deployment to local script/skill directories (`deployment.md`)
     - Infrastructure setup (hosting, database, storage)
     - **CD strategy options (with checkboxes):**
       - [ ] Release to GitHub
       - [ ] Deploy to Cloud
       - [ ] Publish Package
     - CD pipeline configuration
     - Deployment strategy (blue-green, rolling, canary)
     - Monitoring and logging setup
     - Environment configurations
   - **Methodology:**
     - How infrastructure will be provisioned
     - How CD will be configured
   - **Deliverables planned:**
     - List of files that will be created (deployment.md for L2; infrastructure-plan.md, cd-pipeline.md, etc. for L3+)
   - **Budget allocation for deployment** (from cost-budget.md)
   - **Status:** In Progress (update to "Completed" after deployment)

3. **Present README to user:**
   - Show the deployment approach and what will be configured
   - Show what setup files will be created
   - Explain cost implications of chosen infrastructure
   - Ask: "Does this deployment plan look good? Should I proceed with creating deployment configurations?"

4. **Wait for user approval:**
   - **If user says yes:** Proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again

### Step 2: Create Deployment Plan Files

**Only after user approves the README:**

**IMPORTANT**: These files serve dual purposes:
1. **Initially**: Deployment plans/instructions for user approval
2. **Finally**: Documentation of the actual deployment setup (source of truth for future updates)

1. **Create folder structure:**
   ```
   10-deployment/
   ├── README.md
   ├── deployment-info.md (if independently runnable package/MCP server)
   ├── infrastructure-plan.md
   ├── cd-pipeline.md
   ├── deployment-strategy.md
   ├── monitoring-logging.md
   └── environment-config.md
   ```

2. **Create deployment plan files with proposed configurations:**

**10-deployment/README.md:**
- Specify the owner: Deployment Engineer
- Specify attendances: Cloud Infrastructure Architect, DevOps Engineer, Site Reliability Engineer (SRE)
- Overview of deployment stage
- Links to all deployment documentation files
- Current deployment status (will be updated after execution)
- Quick links to deployed environments

**deployment.md (Deployment Plan - For L2 Projects):**
Write as a deployment plan with:
- **Target Location**: `dev-swarm/py_scripts`, `dev-swarm/js_scripts`, or `dev-swarm/skills`.
- **Files to Deploy**: List of source files to copy/move.
- **Dependencies**: Any dependencies that need to be packaged or installed in the target.
- **Configuration**: Any config changes needed for the target environment.
- **Step-by-Step Instructions**: How to perform the deployment.

**deployment-info.md (Deployment Plan - For Independently Runnable Packages/MCP Servers):**
Write as a deployment plan with:
- **Project Type**: Independently runnable package or MCP server
- **Publishing Strategy**: Publish to GitHub as a release with version number
- **Installation Commands for End Users:**
  - For Node.js projects:
    - `pnpm dlx github:username/repo-name#v1.0.0 [command] [options]`
    - `npx github:username/repo-name@latest [command] [options]`
  - For Python projects:
    - `uvx --from 'git+https://github.com/username/repo-name.git@v1.0.0' package-name [command] [options]`
  - Use these as examples and tailor to the actual project
- **User Documentation Update**:
  - Update `src/README.md` with instructions on how to run the package without installation
  - Include usage examples and command-line options
  - Document all available commands and their purposes
- **Publishing Steps**:
  - Ask for explicit user approval before publishing or creating releases
  - Push code to GitHub remote
  - Use playwright-browser-* agent skills to open GitHub website
  - Create a new release with version number (e.g., v1.0.0) through GitHub UI
  - Verify installation works from GitHub release
- **Version Management**: How to create and manage releases through GitHub
- **Clear step-by-step instructions**

After user approves this plan, the `10-deployment/README.md` should reference this file to keep it clean and organized.

**infrastructure-plan.md (Deployment Plan):**
Write as a deployment plan with:
- Proposed cloud provider and services to use
- Infrastructure architecture diagram (text description)
- Resource specifications (compute, memory, storage)
- Network configuration (VPC, subnets, security groups)
- Database configuration and backup strategy
- Storage and CDN setup
- Domain name and DNS configuration
- SSL/TLS certificate setup
- Cost estimation
- Infrastructure as code approach (Terraform, CloudFormation, etc.)
- Clear step-by-step setup instructions
- Security considerations (IAM roles, secrets management)

**cd-pipeline.md (Deployment Plan):**
Write as a deployment plan with:
- CD platform to use (GitHub Actions, GitLab CI, etc.)
- Pipeline workflow diagram (text description)
- Build process steps
- Testing stages (unit, integration, e2e)
- Deployment stages (dev, staging, production)
- Approval gates and manual intervention points
- Environment variables and secrets management
- Deployment triggers (push, PR, manual, scheduled)
- Rollback procedures
- Pipeline configuration files to create
- Clear step-by-step setup instructions
Use `references/cd-pipeline.md` for CD-specific requirements and triggers.

**deployment-strategy.md (Deployment Plan):**
Write as a deployment plan with:
- Deployment approach (blue-green, canary, rolling, recreate)
- Zero-downtime deployment plan
- Database migration strategy
- Feature flags configuration (if applicable)
- Deployment checklist
- Pre-deployment steps
- Post-deployment verification steps
- Rollback plan and criteria
- Disaster recovery procedures
- Maintenance window planning
- Clear step-by-step deployment instructions

**monitoring-logging.md (Deployment Plan):**
Write as a deployment plan with:
- Monitoring tools to use (CloudWatch, Datadog, New Relic, etc.)
- Logging solution (CloudWatch Logs, ELK Stack, etc.)
- Error tracking (Sentry, Rollbar, etc.)
- Uptime monitoring (Pingdom, UptimeRobot, etc.)
- Performance metrics to track
- Alerting rules and thresholds
- Alert notification channels
- Dashboard configuration
- Log retention policies
- Clear step-by-step setup instructions

**environment-config.md (Deployment Plan):**
Write as a deployment plan with:
- Environment variables for each environment
- Secrets management strategy (AWS Secrets Manager, Vault, etc.)
- Configuration differences between environments
- API endpoints and service URLs
- Database connection strings (template)
- Third-party service credentials (template)
- Feature flags per environment
- Clear step-by-step configuration instructions

### Step 3: Get User Confirmation

1. Present all deployment plan files to the user
2. Explain what will be deployed and configured
3. Highlight cost implications if applicable
4. Ask user to review and confirm before proceeding
5. Make any adjustments based on user feedback
6. **DO NOT PROCEED** until user explicitly confirms

### Step 4: Execute Infrastructure Setup

**ONLY AFTER USER CONFIRMATION**, execute each setup:

1. **Execute Infrastructure Setup:**
   - Follow steps in `infrastructure-plan.md`
   - Create cloud accounts if needed (guide user)
   - Setup infrastructure as code (Terraform, CloudFormation, etc.)
   - Create and configure cloud resources
   - Setup VPC, subnets, security groups
   - Provision compute resources (servers, containers, serverless)
   - Setup databases and configure backups
   - Configure storage and CDN
   - Setup domain name and DNS records
   - Configure SSL/TLS certificates
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Document any manual steps user needs to complete

2. **Execute CD Pipeline Setup:**
   - Follow steps in `cd-pipeline.md`
   - Create CD configuration files
   - Configure build steps
   - Setup testing stages
   - Configure deployment stages for each environment
   - Setup secrets and environment variables in CD platform
   - Configure approval gates
   - Test pipeline with a sample deployment
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections
   - Document any manual approvals required

3. **Execute Monitoring and Logging Setup:**
   - Follow steps in `monitoring-logging.md`
   - Setup monitoring tools and agents
   - Configure logging aggregation
   - Setup error tracking service
   - Configure uptime monitoring
   - Create monitoring dashboards
   - Setup alerting rules
   - Configure notification channels
   - Test alerts and notifications
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections

4. **Configure Environments:**
   - Follow steps in `environment-config.md`
   - Setup environment variables in each environment
   - Configure secrets management
   - Store credentials securely
   - Configure feature flags
   - Verify configuration in each environment
   - **Fix any errors encountered during setup**
   - Retry failed steps with corrections

### Step 5: Initial Deployment

1. **For Independently Runnable Packages/MCP Servers:**
   - Follow deployment strategy from `deployment-info.md`
   - **Update src/README.md:**
     - Add installation instructions for end users
     - Include command examples (pnpm dlx, npx, or uvx --from)
     - Document all available commands and options
     - Add usage examples
   - **Push code to GitHub:**
     - Ask for explicit user approval before pushing
     - Ensure all changes are committed
     - Push code: `git push origin main` (or appropriate branch)
   - **Create GitHub Release:**
     - Ask for explicit user approval before opening the browser or creating the release
     - Use playwright-browser-* agent skills to automate browser interactions
     - Open GitHub repository releases page
     - Create a new release through the GitHub UI
     - Set version number (e.g., v1.0.0)
     - Add release notes describing the changes
     - Publish the release
   - **Verify installation:**
     - Test installation using the documented commands with the release version
     - Verify all commands work as expected
   - **Fix any errors encountered during deployment**
   - Document deployment completion
   - Update `deployment-info.md` with actual installation commands tested and release URL

2. **Deploy to Development/Staging First (For Cloud Deployments):**
   - Follow deployment strategy from `deployment-strategy.md`
   - Execute pre-deployment checklist
   - Trigger deployment via CD pipeline
   - Monitor deployment progress
   - Verify deployment success
   - Execute post-deployment verification
   - **Fix any errors encountered during deployment**
   - Adjust configuration as needed
   - Document any issues and resolutions

3. **Deploy to Production (if approved):**
   - Get explicit user confirmation for production deployment
   - Execute pre-deployment checklist
   - Trigger production deployment
   - Monitor deployment closely
   - Verify all services are running
   - Check monitoring dashboards
   - Verify application functionality
   - **Fix any errors encountered during deployment**
   - Be prepared to rollback if issues occur
   - Document deployment completion

### Step 6: Verification and Testing

For each deployed environment:

1. **Verify Infrastructure:**
   - All resources are running
   - Network connectivity is working
   - DNS resolution is correct
   - SSL certificates are valid
   - Security groups are properly configured
   - Backups are configured and working

2. **Verify Application:**
   - Application is accessible via public URL
   - All features are working correctly
   - Database connections are successful
   - API endpoints respond correctly
   - Static assets are served via CDN
   - Performance is acceptable

3. **Verify CD Pipeline:**
   - Pipeline executes successfully
   - Tests run and pass
   - Deployment completes without errors
   - Approval gates work correctly
   - Secrets are properly injected

4. **Verify Monitoring and Logging:**
   - Metrics are being collected
   - Logs are being aggregated
   - Errors are being tracked
   - Alerts are triggered correctly
   - Notifications are received
   - Dashboards display data correctly

### Step 7: Update Documentation Files

**CRITICAL**: Update all deployment files to reflect actual environment:

1. **Update deployment-info.md (if applicable):**
   - Change from "deployment plan" to "current deployment configuration"
   - Document actual version numbers released
   - Document actual installation commands tested and verified
   - Add links to GitHub releases page
   - Document the release creation process using playwright-browser-* agent skills
   - Document actual src/README.md updates made
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to create future releases using the browser automation approach

2. **Update infrastructure-plan.md:**
   - Change from "deployment plan" to "current infrastructure"
   - Document actual resources created with IDs/ARNs
   - Document actual costs (if available)
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to access and manage infrastructure

3. **Update cd-pipeline.md:**
   - Change from "deployment plan" to "current pipeline configuration"
   - Document actual pipeline setup and workflow
   - Add links to pipeline runs
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to trigger and monitor deployments

4. **Update deployment-strategy.md:**
   - Change from "deployment plan" to "current deployment process"
   - Document actual deployment steps executed
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document successful deployment timeline
   - Update rollback procedures based on actual setup

5. **Update monitoring-logging.md:**
   - Change from "deployment plan" to "current monitoring setup"
   - Document actual monitoring tools configured
   - Add dashboard URLs
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to access logs and metrics

6. **Update environment-config.md:**
   - Change from "deployment plan" to "current environment configuration"
   - Document actual environment variables (without sensitive values)
   - Document where secrets are stored
   - Add verification results
   - Add troubleshooting notes for any issues encountered
   - Document how to update configuration

7. **Update 10-deployment/README.md:**
   - Update current deployment status to "Deployed"
   - Add environment URLs for each deployed environment
   - Add summary of deployed infrastructure
   - Add links to monitoring dashboards
   - Add links to CD pipelines
   - Note date of deployment completion
   - Add quick troubleshooting guide

**These updated files now serve as the source of truth for:**
- Future deployments and updates
- Infrastructure modifications
- Troubleshooting deployment issues
- Onboarding new team members
- Disaster recovery procedures

### Step 8: Security and Compliance Check

1. **Security Review:**
   - Verify all secrets are stored securely
   - Check that no credentials are in code or logs
   - Verify SSL/TLS is configured correctly
   - Review security group rules
   - Check for unnecessary public access
   - Verify backup encryption

2. **Cost Optimization:**
   - Review actual costs vs estimates
   - Identify optimization opportunities
   - Setup cost alerts
   - Document cost breakdown

3. **Compliance:**
   - Document compliance requirements met
   - Verify data residency requirements
   - Check backup and retention policies

### Step 9: Final User Review

1. **Inform user that deployment is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files
   - Add **Deployment URLs** section with links to deployed environments

3. **Present completed work to user:**
   - Show the updated documentation showing actual deployment
   - Show verification results for all environments
   - Provide URLs to access deployed application
   - Share monitoring dashboard links
   - Confirm everything is working as expected
   - Provide handoff documentation for ongoing maintenance

4. Ask if they want any adjustments or additional configurations

### Step 10: Commit to Git

1. **Ask user if they want to commit the deployment documentation:**
   - Stage all changes in `10-deployment/`
   - Stage any infrastructure as code files created
   - Stage CD configuration files
   - Commit with message: "Setup deployment infrastructure and CD pipeline"

2. **Optionally push to remote**


## Key Principles

- **Dual-purpose documentation**: Deployment files serve as both initial plans and final documentation
- **Get confirmation first**: Always get user approval before executing deployment tasks
- **Security first**: Never expose credentials, always use secrets management
- **Cost awareness**: Keep user informed of infrastructure costs
- **Fix errors proactively**: When errors occur during deployment, fix them and retry automatically
- **Update documentation**: After execution, update files to reflect actual deployment state
- **Source of truth**: Final documentation becomes the authoritative reference for deployment management
- **Zero-downtime**: Prioritize deployment strategies that minimize service interruption
- **Monitoring first**: Ensure monitoring is in place before production deployment
- **Rollback ready**: Always have a tested rollback plan before deploying to production
- All configurations should be version-controlled
- Infrastructure as code should be preferred over manual configuration
- Deployment should be automated and repeatable
- Documentation should be clear for both humans and AI agents
