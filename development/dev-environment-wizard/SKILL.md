---
name: dev-environment-wizard
description: Interactive setup wizard for development environments. ALWAYS trigger first when users want to set up, create, or initialize a new development environment. Asks discovery questions about tech stack, services, and preferences, then coordinates other skills (zero-to-running, database-seeding, git-hooks, local-ssl, env-manager) to generate a customized environment.
---

# Development Environment Wizard

Interactive wizard that discovers requirements and orchestrates other skills to create a perfectly tailored development environment.

## When to Trigger

This skill should ALWAYS be the first one triggered when users request:
- "Set up a development environment"
- "Create dev environment for my project"
- "I need a local development setup"
- "Help me initialize my development workflow"
- Any variation of setting up/creating/initializing a dev environment

## Discovery Process

### Step 1: Project Understanding

Ask these questions to understand the project:

**Required Questions:**
1. What's your tech stack?
   - Frontend framework? (React, Vue, Angular, Svelte, Next.js, None)
   - Backend framework? (Node/Express, FastAPI, Django, Rails, Go, Java Spring, .NET, None)
   - Database? (PostgreSQL, MySQL, MongoDB, SQLite, None)
   - Cache/Queue? (Redis, Memcached, RabbitMQ, None)

2. What services do you need running?
   - List all services (API, Frontend, Database, Cache, etc.)
   - Any additional services? (Elasticsearch, S3-compatible storage, etc.)

3. Do you already have a project, or are we starting fresh?
   - Existing project → Adapt to existing structure
   - New project → Generate full structure

**Optional Questions (ask based on needs):**
4. Do you need HTTPS for local development?
   - OAuth/payment testing?
   - Service worker testing?
   - Subdomain testing?

5. Do you want realistic test data?
   - User profiles, posts, comments, etc.?
   - How much data? (dozens, hundreds, thousands)

6. Code quality automation?
   - Pre-commit linting?
   - Pre-push testing?
   - Commit message standards?

7. Multiple environments?
   - Dev/test/staging profiles?
   - Different configurations per environment?

### Step 2: Technology Detection

Based on answers, determine:
- **Container orchestration**: Docker Compose (default) or Kubernetes
- **Language-specific needs**: Node.js versions, Python versions, etc.
- **Port defaults**: Standard ports or custom
- **Volume mounts**: What needs hot reload

### Step 3: Skill Coordination

Based on discovery, coordinate these skills:

```typescript
interface EnvironmentPlan {
  core: {
    useSkill: 'zero-to-running',
    config: {
      services: string[],
      ports: Record<string, number>,
      orchestration: 'docker-compose' | 'kubernetes',
      healthChecks: boolean,
    }
  },
  optional: {
    ssl?: {
      useSkill: 'local-ssl',
      domains: string[],
    },
    seeding?: {
      useSkill: 'database-seeding',
      models: string[],
      recordCounts: Record<string, number>,
    },
    hooks?: {
      useSkill: 'git-hooks',
      preCommit: string[],
      prePush: string[],
    },
    environments?: {
      useSkill: 'env-manager',
      profiles: string[],
    }
  }
}
```

## Orchestration Logic

### 1. Generate Core Environment (Always)

Use **zero-to-running** skill to generate:
- docker-compose.yml with specified services
- Makefile with all commands
- .env.example with discovered variables
- Health check scripts
- Startup/teardown scripts
- DEVELOPER_SETUP.md

Customize based on:
- Detected languages (adjust Dockerfiles)
- Specified services (only include what's needed)
- Port preferences (use custom ports if specified)

### 2. Add Optional Features (If Requested)

**If SSL needed:**
- Use **local-ssl** skill
- Generate certificates for specified domains
- Update docker-compose.yml with cert mounts
- Update nginx config with HTTPS

**If test data needed:**
- Use **database-seeding** skill
- Generate seed factories for specified models
- Customize record counts
- Add seed scripts to package.json

**If code quality needed:**
- Use **git-hooks** skill
- Set up Husky + lint-staged
- Configure ESLint/Prettier for language
- Add pre-commit/pre-push hooks

**If multiple environments needed:**
- Use **env-manager** skill
- Generate .env.{dev,test,staging} files
- Create environment switcher script
- Add validation scripts

### 3. Integration & Testing

After generating all files:
1. Validate configuration consistency
2. Check for port conflicts
3. Ensure all scripts are executable
4. Generate integration documentation
5. Provide testing instructions

## Example Workflows

### Example 1: Simple React + Node App

**User**: "Set up a dev environment for my React and Node.js app"

**Wizard Questions**:
```
Q: What database do you need?
A: PostgreSQL

Q: Do you need a cache like Redis?
A: Yes

Q: Do you need HTTPS for local dev?
A: No

Q: Want realistic test data?
A: Yes, a few hundred users and posts

Q: Set up Git hooks for code quality?
A: Yes
```

**Generated Files** (using 4 skills):
- ✅ zero-to-running: docker-compose.yml, Makefile, scripts/
- ✅ database-seeding: seed-factory.ts, seed.ts
- ✅ git-hooks: .husky/, configs
- ❌ local-ssl: Not needed
- ❌ env-manager: Single environment sufficient

### Example 2: Full-Stack with Everything

**User**: "Create a production-like dev environment with all features"

**Wizard**: (Asks all questions)

**Generated Files** (using all 5 skills):
- ✅ zero-to-running: Full setup
- ✅ database-seeding: Complex seeds
- ✅ git-hooks: Strict quality checks
- ✅ local-ssl: HTTPS with trusted certs
- ✅ env-manager: Dev/test/staging profiles

### Example 3: Minimal Python API

**User**: "Simple FastAPI dev setup"

**Wizard Questions** (minimal):
```
Q: Database?
A: SQLite

Q: Any other services?
A: No
```

**Generated Files** (minimal zero-to-running):
- docker-compose.yml (just API service)
- Makefile (simplified)
- Basic scripts

## Decision Tree

```
User requests dev environment
    ↓
Wizard skill triggers FIRST
    ↓
Ask discovery questions
    ↓
Determine tech stack
    ↓
Plan skill usage
    ↓
Generate with zero-to-running (ALWAYS)
    ↓
Add optional features (IF REQUESTED):
    - database-seeding
    - git-hooks
    - local-ssl
    - env-manager
    ↓
Validate & integrate
    ↓
Provide files + instructions
```

## Communication Style

### Good Approach:
```
I'll help you set up your development environment! Let me ask a few 
questions to customize it for you:

1️⃣ Tech Stack:
   • Frontend framework? (React/Vue/Angular/other)
   • Backend framework? (Node/Python/Go/other)
   • Database? (PostgreSQL/MySQL/MongoDB/other)

2️⃣ Optional Features:
   • Need HTTPS locally? (y/n)
   • Want test data generation? (y/n)
   • Set up Git hooks? (y/n)
   • Multiple environments? (y/n)

I'll generate a customized setup based on your answers!
```

### Bad Approach:
```
Here's a generic docker-compose file. You'll need to modify it for your stack...
```

## Output Format

After discovery, provide:

1. **Summary of what will be generated**:
```
📋 Environment Plan:
✅ Core: React + Node.js + PostgreSQL + Redis
✅ Optional: HTTPS, Test Data, Git Hooks
📦 Using skills: zero-to-running, database-seeding, git-hooks, local-ssl

Generating your custom environment...
```

2. **Generated files with explanations**

3. **Setup instructions**:
```
🚀 Quick Start:
1. Copy these files to your project
2. Run: make dev
3. Access: http://localhost:3000

📚 Full documentation in DEVELOPER_SETUP.md
```

4. **Next steps**:
```
✨ You can now:
• make dev          - Start everything
• make db-seed      - Generate test data
• make ssl-setup    - Enable HTTPS
• make test         - Run tests

Need help? Check the troubleshooting section!
```

## Integration with Other Skills

This skill should:
1. **Never work alone** - Always use zero-to-running at minimum
2. **Coordinate, don't duplicate** - Reference other skills, don't reimplement
3. **Customize, don't boilerplate** - Adapt templates to actual needs
4. **Validate combinations** - Ensure skills work together
5. **Document integration** - Explain how pieces fit

## Best Practices

1. **Ask before assuming** - Don't guess the tech stack
2. **Start minimal** - Only add complexity if needed
3. **Explain choices** - Tell users why you're suggesting features
4. **Provide examples** - Show what each feature does
5. **Test mentally** - Ensure generated config will work
6. **Document everything** - No mystery files

## Error Prevention

Before generating:
- ✅ Validate port availability
- ✅ Check service compatibility
- ✅ Ensure scripts are platform-compatible
- ✅ Verify all referenced skills are available
- ✅ Test configuration consistency

## Special Cases

### Existing Project
If user has existing files:
- Ask to see current structure
- Adapt rather than replace
- Highlight what will change
- Offer backup suggestions

### Monorepo
If multiple services in one repo:
- Ask about service structure
- Generate per-service configs
- Create root orchestration
- Document monorepo patterns

### Non-Standard Stack
If technologies aren't in standard list:
- Ask for details
- Research best practices
- Generate custom Dockerfiles
- Document special setup

## Success Criteria

A successful wizard session should:
- ✅ Understand exact requirements
- ✅ Generate working configuration
- ✅ Include only requested features
- ✅ Provide clear setup instructions
- ✅ Enable `make dev` to work immediately
- ✅ Result in <10 minute setup time

## Anti-Patterns to Avoid

❌ Generating everything by default (bloat)
❌ Assuming tech stack (ask!)
❌ Copy-pasting without customizing
❌ Missing integration points
❌ No validation of generated config
❌ Unclear documentation

## Example Session

```
User: "Set up a dev environment for my app"

Wizard: "I'll create a customized development environment for you! 
Let me ask a few quick questions:

1. What's your tech stack?
   • Frontend: ?
   • Backend: ?
   • Database: ?

2. Which optional features do you want?
   • HTTPS for local development? (y/n)
   • Realistic test data generation? (y/n)
   • Automated code quality checks? (y/n)
   • Multiple environment profiles? (y/n)

Answer these and I'll generate everything!"

User: "Frontend is React, backend is Node/Express, database is 
PostgreSQL. Yes to all optional features."

Wizard: "Perfect! Generating your environment...

📋 Plan:
• Core: React + Node.js/Express + PostgreSQL + Redis
• HTTPS: mkcert with trusted certificates
• Test Data: Faker-based seed generation
• Code Quality: Git hooks with ESLint/Prettier
• Environments: Dev, Test, Staging profiles

Using 5 skills: zero-to-running, database-seeding, git-hooks, 
local-ssl, env-manager

[Generates all files...]

✅ Done! Your environment is ready.

🚀 Quick Start:
1. Copy generated files to your project root
2. Run: make dev
3. Access: https://localhost:3000

📚 See DEVELOPER_SETUP.md for full documentation

Need any adjustments?"
```
