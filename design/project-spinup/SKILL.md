---
name: project-spinup
description: "Generate complete project foundations with personalized claude.md, Docker setup, and project structure. Supports Guided Setup or Quick Start."
---

# project-spinup

<purpose>
Generate a complete, ready-to-code project foundation tailored to development workflow, infrastructure, and chosen tech stack. Creates comprehensive claude.md for AI assistant context, Docker configuration, directory structure, and either guided learning prompts or full scaffolding.
</purpose>

<output>
Complete project foundation including:
- claude.md (comprehensive project context)
- docker-compose.yml (local development)
- Directory structure (src/, tests/, docs/)
- .env.example, .gitignore, README.md
- Guided setup prompts OR full scaffolding
- .docs/project-foundation-complete.md (handoff marker)
</output>

---

<workflow>

<phase id="0" name="check-prerequisites">
<action>Check for handoff documents and gather missing information conversationally.</action>

<expected-documents>
- .docs/PROJECT-MODE.md (workflow mode declaration)
- .docs/brief-*.md (project brief)
- .docs/tech-stack-decision.md (technology stack selection)
- .docs/deployment-strategy.md (deployment strategy)
</expected-documents>

<check-process>
1. Scan .docs/ for expected handoff documents
2. If found: Load context and summarize conversationally
3. If missing: Gather equivalent information through questions
4. Proceed with skill workflow regardless
</check-process>

<when-prerequisites-exist>
"I can see you've completed all prerequisite phases. You're in {MODE} mode, with {tech-stack} selected for deployment on {hosting-approach}.

Ready to generate your project foundation?"

Then proceed with the skill's main workflow.
</when-prerequisites-exist>

<when-prerequisites-missing>
"I don't see all the expected handoff documents. No problem - let me gather what I need.

To generate your project foundation, I need to understand:
1. **What's your project name?** (kebab-case preferred)
2. **What's your tech stack?** (Frontend, backend, database)
3. **Where will this deploy?** (Localhost, VPS, cloud platform)
4. **Learning or delivery focus?** (Affects scaffolding approach)

Once you share these, I can generate your project foundation."

Gather answers conversationally, then proceed with the skill's main workflow.
</when-prerequisites-missing>

<key-principle>
This skill NEVER blocks on missing prerequisites. It gathers information conversationally and proceeds.
</key-principle>

<spinup-approach-prompt>
For the project scaffolding, would you prefer:

1. **Guided Setup** - I'll create the foundation, then provide step-by-step prompts
   to build out the structure incrementally. You'll learn how each layer works.
   (Recommended if you're new to {tech stack})

2. **Quick Start** - I'll generate the complete project scaffolding immediately
   with all boilerplate code and configuration.
   (Recommended if you're familiar with {tech stack})

Which approach would you like?
</spinup-approach-prompt>

<mode-vs-spinup-distinction>
- PROJECT-MODE (LEARNING/BALANCED/DELIVERY): Governs advisory skills - exploration, discussion, checkpoints. Strategic learning.
- spinup_approach (Guided/Quick Start): Governs scaffolding style - step-by-step or all-at-once. Tactical implementation.

Key insight: You can be in LEARNING mode but use Quick Start if familiar with the stack. Or DELIVERY mode but use Guided Setup for a new framework.
</mode-vs-spinup-distinction>
</phase>

<phase id="1" name="gather-information">
<action>Confirm any missing inputs.</action>

<inputs-required>
1. project_name (kebab-case)
2. project_description
3. tech_stack (from tech-stack-decision.md or conversation)
4. hosting_plan (from deployment-strategy.md or conversation)
5. complexity_level (simple/standard/complex)
6. spinup_approach (guided/quick-start)
7. special_features (optional)
</inputs-required>
</phase>

<phase id="2" name="generate-core-files">
<action>Create foundation files regardless of spinup approach.</action>

<always-create>
1. claude.md - Comprehensive project context
2. docker-compose.yml - Local development environment
3. Directory structure - src/, tests/, docs/
4. .gitignore - Tech-stack-appropriate
5. README.md - Setup and development instructions
6. .env.example - Required environment variables
7. Git initialization guidance
8. .docs/project-foundation-complete.md - Handoff marker
</always-create>
</phase>

<phase id="3" name="apply-spinup-approach">

<guided-setup>
Generate foundation only, plus detailed "Next Steps" section in claude.md with:
- Step-by-step prompts to give Claude Code
- Explanation of what each step creates
- Learning objectives for each step
- Verification checkpoints
- Estimated time for each step

User incrementally asks Claude Code to build out the project.
</guided-setup>

<quick-start>
Generate complete scaffolding including:
- All tech-stack-specific configuration files
- Complete source file structure
- Starter/example code with comments
- Sample tests
- All middleware/utilities
- Initial git commit prepared
</quick-start>

</phase>

<phase id="4" name="create-handoff">
<action>Create .docs/project-foundation-complete.md handoff marker.</action>

<location>.docs/project-foundation-complete.md</location>

<handoff-content>
# Project Foundation Complete

**Project:** {project_name}
**Created:** {date}
**Tech Stack:** {tech_stack_summary}
**Deployment Target:** {hosting_approach}
**Spinup Approach:** {guided/quick-start}

## What Was Created
- claude.md (project context)
- docker-compose.yml (local development)
- Directory structure
- Configuration files
- README.md

## Workflow Status
This marks the completion of the PLANNING and SETUP phases.

[If Localhost:]
**WORKFLOW TERMINATION POINT**
Your localhost project is ready for development.
No further workflow phases needed.

[If Public Deployment:]
**Next Phases Available:**
- Phase 4: test-orchestrator (optional, when ready for testing infrastructure)
- Phase 5: deploy-guide (when ready to deploy)
- Phase 6: ci-cd-implement (optional, for automation)
</handoff-content>
</phase>

<phase id="5" name="provide-next-steps">
<action>Summarize what was created and provide clear next steps based on deployment target.</action>

<summary-includes>
- What was created
- How to start working
- How to run development environment
- Where to find documentation
- Workflow status with termination point guidance
- Git initialization commands
</summary-includes>
</phase>

</workflow>

---

<user-context>

<developer-profile>
- Name: John
- Experience: Hobbyist developer, beginner-to-intermediate
- Learning Goal: Deep understanding of full-stack, professional practices
- Reliance: Heavy use of Claude Code for implementation
</developer-profile>

<development-environment>
- Computers: MacBook Pro and Mac Mini
- Sync: iCloud, portable SSDs, GitHub
- IDE: VS Code with relevant extensions
- Git: main + dev branches, conventional commits
- Package Manager: Best for project
- Linting: Best for project
- Directory: src/, docs/, tests/
</development-environment>

<infrastructure>
- Hostinger VPS8: 8 cores, 32GB RAM, 400GB storage
  - Supabase (self-hosted), PocketBase, n8n, Ollama, Wiki.js, Caddy
  - All in Docker containers
- File Storage: Backblaze B2
- DNS: Cloudflare
- VPS Access: SSH as user "john"
- Deployment Options: Localhost, Shared Hosting, Cloudflare Pages, Fly.io, VPS Docker
</infrastructure>

<common-tasks>
- Feature implementation
- Debugging and troubleshooting
- Refactoring
- Testing (unit, integration, E2E)
- Deployment setup
- Performance optimization
- Security implementation
</common-tasks>

<standards>
- Security: OWASP awareness
- Testing: Framework-appropriate
- Code Style: Framework/language best practices
- Commits: Conventional commits format
</standards>

</user-context>

---

<claude-md-template>

<structure>
# {PROJECT_NAME}

> {PROJECT_DESCRIPTION}

**Status**: Active Development | **Developer**: John | **Philosophy**: Learning-Focused, Best Practices

---

## Developer Profile
{Experience level, learning goals, development approach, common tasks for Claude Code}

---

## Project Overview
{What project does, tech stack breakdown, architecture decisions}

---

## Development Environment
{Computers/sync, local setup, prerequisites, first-time setup commands}

---

## Infrastructure & Hosting
{Self-hosted infrastructure available, project-specific hosting, access/credentials}

---

## Development Workflow
{Git branching strategy, commit convention, development cycle, testing strategy}

---

## Code Conventions
{File organization, naming conventions, code style/linting}

---

## Common Commands
{Development, database, Docker commands}

---

## Project-Specific Notes
{Authentication, database schema, API endpoints, environment variables}

---

## Deployment
{Deployment workflow, checklist, rollback procedure}

---

## Resources & References
{Project docs, external resources, learning resources}

---

## Troubleshooting
{Common issues and solutions}

---

## Next Steps
{If Guided Setup: detailed step-by-step prompts}
{If Quick Start: immediate next actions}
</structure>

</claude-md-template>

---

<guided-setup-template>

<next-steps-section>
## Next Steps (Guided Setup)

You now have the project foundation. Complete the setup by asking Claude Code to build out the structure step-by-step.

### Learning Philosophy
Each step teaches about a specific part of the stack. Take your time, review what gets created, ask questions about why things are structured this way.

Estimated total time: {X hours}

---

### Step 1: Initialize {Framework} Structure
**Time:** ~{X} minutes | **Learning:** Project structure and configuration

**What you'll learn**: How {framework} projects are organized, what each config file does.

**Say to Claude Code**:
```
Set up the {Framework} structure with {specifics} as specified in claude.md. Please explain the purpose of each major file and directory.
```

**What will be created**: {list}

**Verification**: {command}

---

### Step 2: Configure Database Connection
**Time:** ~{X} minutes | **Learning:** Database configuration and connection patterns

**Say to Claude Code**:
```
Set up the database client configuration for {database} with environment variables as specified in claude.md.
```

---

### Step 3: Implement Authentication Scaffolding
**Time:** ~{X} minutes | **Learning:** Authentication patterns, security

**Say to Claude Code**:
```
Implement authentication using {auth approach} as specified in claude.md. Include registration, login, logout, and protected route examples.
```

---

### Step 4: Create Example CRUD Feature
**Time:** ~{X} minutes | **Learning:** Full-stack data flow, API design

**Say to Claude Code**:
```
Create a simple CRUD feature for {example entity} that demonstrates best practices. Include frontend form, API endpoints, database operations, and basic tests.
```

---

### Step 5: Add Testing Suite
**Time:** ~{X} minutes | **Learning:** Testing strategies

**Say to Claude Code**:
```
Set up the testing framework and write example tests for the CRUD feature. Include unit and integration tests.
```

---

### Step 6: Configure Docker Development Environment
**Time:** ~{X} minutes | **Learning:** Docker containerization

**Say to Claude Code**:
```
Review and enhance the docker-compose.yml. Explain how to use Docker for local development.
```

---

### Step 7: Document and Prepare for First Feature
**Time:** ~{X} minutes | **Learning:** Documentation practices

**Say to Claude Code**:
```
Help me document the project structure, update the README, and create a template for building new features.
```

---

### You're Ready to Build!

After completing these steps, you'll have:
- Complete {framework} project structure
- Database connected and configured
- Authentication working
- Example CRUD feature as template
- Testing framework ready
- Docker environment running
- Clear development workflow
</next-steps-section>

</guided-setup-template>

---

<tech-stack-templates>

<nextjs-supabase>
Default Configuration:
- Next.js 15 (App Router)
- TypeScript (strict mode)
- Tailwind CSS v4
- Supabase client (auth, database, storage)
- shadcn/ui components (optional)
- React Query / TanStack Query
- Zod for validation
- Jest or Vitest for testing

Files to generate (Quick Start):
- package.json, tsconfig.json, next.config.js
- tailwind.config.ts, postcss.config.js
- app/layout.tsx, app/page.tsx, app/api/
- lib/supabase/client.ts, lib/supabase/server.ts
- components/, middleware.ts
- .eslintrc.json, .prettierrc
- jest.config.js or vitest.config.ts
- tests/, docker-compose.yml
</nextjs-supabase>

<php-mysql>
Default Configuration:
- PHP 8.2+
- MySQL 8.0+
- Composer for dependencies
- Simple MVC structure
- PDO for database access
- PHPUnit for testing

Files to generate (Quick Start):
- composer.json, index.php
- src/Controllers/, src/Models/, src/Views/
- src/Router.php, src/Database.php
- config/database.php, config/config.php
- public/index.php, public/css/, public/js/
- tests/, docker-compose.yml (PHP, MySQL, phpMyAdmin)
</php-mysql>

<fastapi-postgresql>
Default Configuration:
- FastAPI
- PostgreSQL 15
- SQLAlchemy ORM
- Alembic for migrations
- Pydantic for validation
- pytest for testing
- uvicorn for ASGI server

Files to generate (Quick Start):
- requirements.txt, pyproject.toml, main.py
- app/__init__.py, app/models/, app/routers/
- app/schemas/, app/database.py, app/config.py
- tests/, alembic/
- docker-compose.yml
</fastapi-postgresql>

</tech-stack-templates>

---

<execution-summary-template>

<template>
## Project Foundation Created

**Project:** {project_name}
**Tech Stack:** {primary technologies}
**Spinup Approach:** {Guided Setup or Quick Start}
**Deployment Target:** {localhost / hosting approach}

---

### Workflow Status

**PLANNING PHASES - COMPLETE**
- Phase 0: project-brief-writer
- Phase 1: tech-stack-advisor
- Phase 2: deployment-advisor

**SETUP PHASE - COMPLETE**
- Phase 3: project-spinup (this skill)

[If Localhost:]
**WORKFLOW TERMINATION POINT**

Your localhost project is ready for development. No further workflow phases needed.

If you later decide to deploy publicly:
1. Re-run deployment-advisor to choose a hosting target
2. Continue with deploy-guide and optionally ci-cd-implement

[If Public Deployment:]
**DEVELOPMENT PHASE - START**

Build your features! When you're ready:
- Phase 4: test-orchestrator (optional - set up testing infrastructure)
- Phase 5: deploy-guide (deploy your application)
- Phase 6: ci-cd-implement (optional - automate deployments)

---

### Generated Files

- claude.md - Comprehensive project context
- docker-compose.yml - Local development environment
- Directory structure (src/, tests/, docs/)
- .env.example, .gitignore, README.md
- .docs/project-foundation-complete.md - Handoff marker
{If Quick Start: - Complete project scaffolding with starter code}

---

### Quick Start Commands

```bash
# Initialize git
cd {project_name}
git init
git checkout -b main
git add .
git commit -m "chore: initial project setup via project-spinup skill"
git checkout -b dev

# Start development
docker compose up -d  # or native commands
{dev server command}
```

Open http://localhost:{port} to see your application.

---

### Next Actions

{If Guided Setup:}
1. Open claude.md and read "Next Steps (Guided Setup)"
2. Copy the first prompt and paste it to Claude Code
3. Follow the guided steps incrementally
4. Ask questions as you go

{If Quick Start:}
1. Review generated code structure
2. Copy .env.example to .env.local and configure
3. Start building features!

Happy coding!
</template>

</execution-summary-template>

---

<guardrails>

<must-do>
- Load ALL handoff documents first (if they exist)
- Use handoff documents as primary source (if available)
- Gather missing information conversationally (never block)
- Ask about spinup approach with MODE-informed suggestion
- Adapt templates to tech stack
- Be comprehensive in claude.md
- Include user's context (workflow, infrastructure, learning goals)
- Respect user choice (Guided/Quick Start equally valid)
- Include testing setup and examples
- Always include docker-compose.yml
- Security-conscious (.env for secrets, .gitignore)
- Create .docs/project-foundation-complete.md handoff marker
- Show workflow status with termination point guidance
- Indicate clearly if this is a termination point (localhost)
</must-do>

<must-not-do>
- Skip reading handoff documents (if they exist)
- Use wrong templates for tech stack
- Assume spinup approach without asking
- Generate incomplete foundation
- Block on missing prerequisites (gather info instead)
- Treat localhost projects as incomplete workflows
</must-not-do>

</guardrails>

---

<workflow-status>
Phase 3 of 7: Project Foundation

Status:
  Phase 0: Project Brief (project-brief-writer)
  Phase 1: Tech Stack (tech-stack-advisor)
  Phase 2: Deployment Strategy (deployment-advisor)
  Phase 3: Project Foundation (you are here) <- TERMINATION POINT (localhost)
  Phase 4: Test Strategy (test-orchestrator) - optional
  Phase 5: Deployment (deploy-guide) <- TERMINATION POINT (manual deploy)
  Phase 6: CI/CD (ci-cd-implement) <- TERMINATION POINT (full automation)
</workflow-status>

---

<integration-notes>

<workflow-position>
Phase 3 of 7 in the Skills workflow chain.
Expected input: .docs/deployment-strategy.md (gathered conversationally if missing)
Produces: Project foundation + .docs/project-foundation-complete.md

This is a TERMINATION POINT for localhost/learning projects.
</workflow-position>

<flexible-entry>
This skill can be invoked standalone without prior phases. Missing context is gathered through conversation rather than blocking.
</flexible-entry>

<termination-points>
- If deployment target is localhost: Workflow terminates here
- If deployment target is public: Workflow continues to deploy-guide (Phase 5)
</termination-points>

<status-utility>
Users can invoke the **workflow-status** skill at any time to:
- See current workflow progress
- Check which phases are complete
- Get guidance on next steps
- Review all handoff documents

Mention this option when users seem uncertain about their progress.
</status-utility>

</integration-notes>
