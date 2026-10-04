---
name: crew-init
description: Analyzes a project codebase, builds 3-layer index, generates project profile, and auto-configures the agent team with relevant skills. The main initialization skill for CodeCrew.
---

# Crew Init - Project Analysis & Team Setup

Full project initialization that transforms any codebase into a CodeCrew workspace with indexed code, profiled architecture, and a configured agent team.

## When to Activate

- User runs `/crew init`
- User runs `/crew` with `init` argument
- First time using CodeCrew in a project

## Initialization Pipeline

### Phase 1: Project Discovery

Scan the project to understand what we're working with:

**1.1 Detect project type and languages:**
```
Use Glob to check for:
- package.json, tsconfig.json → Node.js / TypeScript
- requirements.txt, pyproject.toml, setup.py → Python
- go.mod → Go
- Cargo.toml → Rust
- pom.xml, build.gradle → Java / Kotlin
- Gemfile → Ruby
- composer.json → PHP
- Makefile, CMakeLists.txt → C/C++
- pubspec.yaml → Dart/Flutter
- *.sln, *.csproj → .NET/C#
```

**1.2 Detect frameworks:**
```
Read package.json (or equivalent) for:
- react, next, vue, angular, svelte → Frontend framework
- express, fastify, koa, django, flask, gin, actix → Backend framework
- playwright, jest, pytest, mocha → Testing framework
- eslint, prettier, black, gofmt → Linting/formatting
- docker, kubernetes → Container/orchestration
```

**1.3 Map project structure:**
```
Use Glob for directory layout:
- src/, lib/, app/ → Source code
- test/, tests/, __tests__, spec/ → Tests
- docs/, doc/ → Documentation
- .github/, .gitlab-ci.yml → CI/CD
- Dockerfile, docker-compose.yml → Docker
- scripts/, bin/ → Build/deploy scripts
```

**1.4 Read existing context:**
- Read CLAUDE.md if it exists (project-specific instructions)
- Read README.md for project description
- Check git log for recent activity areas (if git repo)

### Phase 2: Build Codebase Index

Invoke the **codebase-index** skill in full-build mode:

1. Discover all source files (excluding node_modules, dist, build, etc.)
2. For each file: read, hash, extract metadata (exports, imports, functions, classes, line count)
3. Build call graph from import/export relationships
4. Write `.claude/crew-index.json` (Layer 1 - compact)
5. Write `.claude/crew-symbols.json` (Layer 2 - symbols)

This enables the Index-First Protocol for all future agent interactions.

### Phase 3: Generate Project Profile

Write `.claude/crew-profile.md` with:

```markdown
# Crew Profile: {project-name}

## Overview
- **Type**: {web-app | api | cli | library | scraper | mobile | etc.}
- **Languages**: {detected languages}
- **Frameworks**: {detected frameworks}
- **Size**: {total files} files, {total lines} lines

## Architecture
- **Entry Point**: {main file}
- **Pipeline/Flow**: {data flow description}
- **Patterns**: {MVC, pipeline, event-driven, microservice, etc.}

## Key Directories
- **Source**: {src paths}
- **Tests**: {test paths}
- **Config**: {config files}
- **Docs**: {doc paths}

## Tech Stack
- **Runtime**: {node, python, go, etc.}
- **Package Manager**: {npm, pip, cargo, etc.}
- **Testing**: {jest, pytest, etc.}
- **Linting**: {eslint, prettier, etc.}
- **CI/CD**: {github actions, gitlab ci, etc.}
- **Deployment**: {docker, k8s, vercel, etc.}

## Index Status
- **Files Indexed**: {count}
- **Symbols Mapped**: {count}
- **Last Indexed**: {timestamp}
- **Index Files**: .claude/crew-index.json, .claude/crew-symbols.json
```

### Phase 4: Configure Agent Team

Based on detected stack, determine which agents are active and what skills they need.

Write `.claude/crew-team.json`:

```json
{
  "project": "project-name",
  "configured": "2026-04-04T12:00:00Z",
  "agents": {
    "ceo": {
      "model": "opus",
      "active": true,
      "role": "Task triage, decomposition, delegation, architecture decisions"
    },
    "vp-engineering": {
      "model": "sonnet",
      "active": true,
      "role": "Tech decisions, architecture review, complex planning"
    },
    "vp-quality": {
      "model": "sonnet",
      "active": true,
      "role": "Quality gates, test strategy, review coordination"
    },
    "senior-dev": {
      "model": "sonnet",
      "active": true,
      "role": "Complex implementation, multi-file changes"
    },
    "junior-dev": {
      "model": "haiku",
      "active": true,
      "role": "Simple fixes, formatting, small changes"
    },
    "code-reviewer": {
      "model": "sonnet",
      "active": true,
      "role": "Code review, quality assessment"
    },
    "debugger": {
      "model": "sonnet",
      "active": true,
      "role": "Bug investigation, root cause analysis"
    },
    "security-analyst": {
      "model": "sonnet",
      "active": false,
      "activateWhen": "security-related tasks or pre-deploy review"
    },
    "devops-engineer": {
      "model": "haiku",
      "active": false,
      "activateWhen": "Docker/CI/CD/deployment tasks detected"
    },
    "doc-writer": {
      "model": "haiku",
      "active": true,
      "role": "Documentation, comments, READMEs"
    },
    "test-engineer": {
      "model": "sonnet",
      "active": false,
      "activateWhen": "test directory detected or testing tasks"
    }
  },
  "activationRules": {
    "hasDocker": ["devops-engineer"],
    "hasTests": ["test-engineer"],
    "hasSecurity": ["security-analyst"],
    "always": ["ceo", "vp-engineering", "senior-dev", "junior-dev", "code-reviewer", "debugger", "doc-writer"]
  }
}
```

Activate conditional agents based on detected stack:
- Found `Dockerfile` or `docker-compose.yml` → activate `devops-engineer`
- Found `test/` or testing framework → activate `test-engineer`
- Found `.env` or security configs → activate `security-analyst`

### Phase 5: Suggest Custom Agents

Based on Phase 1 detection results (languages, frameworks, tools), suggest project-specific custom agents that extend the built-in team. The number of suggestions is **dynamic** — more frameworks/tools detected = more suggestions.

#### Step 0: Detect Project Domain

Analyze available project signals to classify the project domain:

1. **Project directory name** — check for keywords (e.g., "trading", "shop", "health", "game")
2. **README.md** — read first 50 lines for project description keywords
3. **package.json / pyproject.toml** — check `description` and `keywords` fields
4. **Directory names** — scan for domain-specific folders (e.g., `strategies/`, `orders/`, `cart/`, `patients/`)
5. **Import patterns** — check for domain-specific libraries (e.g., `ccxt`, `alpaca-trade-api`, `stripe`, `hl7`)

Classify into ONE primary domain:

| Domain | Detection Signals |
|--------|------------------|
| `trading/finance` | "trading", "bot", "strategy", "backtest", "portfolio", "hedge", "quant", ccxt, alpaca, binance, ta-lib, quantlib |
| `e-commerce` | "shop", "store", "cart", "checkout", "product", stripe, shopify, woocommerce, snipcart |
| `healthcare` | "patient", "health", "medical", "clinical", "ehr", hl7, fhir, dicom |
| `education` | "course", "student", "learning", "lms", "quiz", "classroom" |
| `gaming` | "game", "player", "score", "level", "sprite", phaser, unity, godot, pixi.js |
| `ai-ml` | "model", "training", "inference", "prediction", tensorflow, pytorch, scikit-learn, transformers, langchain |
| `iot` | "sensor", "device", "mqtt", "firmware", "embedded", mqtt.js, johnny-five, raspberry |
| `media` | "stream", "video", "audio", "media", "content", ffmpeg, hls, webrtc |
| `saas` | "tenant", "subscription", "billing", "dashboard", "admin", "onboarding", "workspace" |
| `devtools` | "cli", "plugin", "extension", "lint", "compiler", "bundler", "sdk" |
| `data-pipeline` | "pipeline", "etl", "ingest", "warehouse", "transform", airflow, prefect, dagster, dbt |
| `social` | "chat", "message", "feed", "notification", "real-time", "presence", socket.io, pusher |
| `general` | No strong domain signals detected |

If domain is `general`, skip domain-specific suggestions. Otherwise, include domain-specific agents in Step 1 below.

#### Step 1: Match Detected Stack + Domain to Suggested Agents

Check Phase 1 results and Step 0 domain against these mappings. Only include agents whose detection conditions match:

```
JavaScript/TypeScript:
  - react-specialist (sonnet)     → if React or Next.js detected
    "Expert in React component architecture, hooks, state management, and performance optimization"
  - nextjs-specialist (sonnet)    → if Next.js detected
    "Expert in Next.js App Router, server components, API routes, and SSR/SSG strategies"
  - vue-specialist (sonnet)       → if Vue detected
    "Expert in Vue 3 composition API, Pinia state management, and component patterns"
  - angular-specialist (sonnet)   → if Angular detected
    "Expert in Angular modules, services, dependency injection, and RxJS patterns"
  - node-api-specialist (sonnet)  → if Express/Fastify/Koa detected
    "Expert in Node.js API design, middleware patterns, route handling, and request validation"
  - styling-specialist (haiku)    → if Tailwind/styled-components/CSS modules detected
    "Expert in styling architecture, responsive design, and CSS optimization"

Python:
  - django-specialist (sonnet)    → if Django detected
    "Expert in Django models, views, serializers, middleware, and ORM optimization"
  - flask-specialist (sonnet)     → if Flask detected
    "Expert in Flask blueprints, extensions, request handling, and API design"
  - fastapi-specialist (sonnet)   → if FastAPI detected
    "Expert in FastAPI endpoints, Pydantic models, dependency injection, and async patterns"
  - data-engineer (sonnet)        → if pandas/numpy/scipy detected
    "Expert in data pipelines, DataFrame operations, data cleaning, and transformation"
  - ml-engineer (sonnet)          → if tensorflow/pytorch/sklearn detected
    "Expert in ML model architecture, training pipelines, and inference optimization"

Go:
  - go-api-specialist (sonnet)    → if Gin/Echo/Fiber detected
    "Expert in Go HTTP handlers, middleware, routing, and concurrent request processing"

Rust:
  - rust-systems (sonnet)         → if Actix/Tokio detected
    "Expert in Rust async patterns, ownership semantics, and systems-level optimization"

Database (any language):
  - database-specialist (sonnet)  → if Prisma/Sequelize/SQLAlchemy/TypeORM/Drizzle detected
    "Expert in database schema design, query optimization, migrations, and ORM patterns"

Mobile:
  - mobile-specialist (sonnet)    → if React Native/Flutter detected
    "Expert in mobile UI patterns, navigation, platform-specific APIs, and performance"

Monorepo:
  - monorepo-specialist (haiku)   → if Turborepo/Nx/Lerna detected
    "Expert in monorepo architecture, workspace dependencies, and shared package management"
```

Domain-Based Suggestions (from Step 0 domain detection):

trading/finance:
  - quant-expert (sonnet)
    "Expert in trading algorithms, market data processing, order execution, risk calculations, and financial modeling"
  - risk-analyst (sonnet)
    "Expert in risk assessment, portfolio analysis, compliance checks, and financial regulations"

e-commerce:
  - payment-specialist (sonnet)
    "Expert in payment gateway integration, checkout flows, cart logic, and order management"
  - catalog-specialist (haiku)
    "Expert in product catalog management, search/filter, inventory, and pricing logic"

healthcare:
  - compliance-specialist (sonnet)
    "Expert in HIPAA compliance, patient data handling, audit trails, and healthcare regulations"
  - ehr-specialist (sonnet)
    "Expert in electronic health record systems, patient data models, and clinical workflows"

education:
  - lms-specialist (sonnet)
    "Expert in learning management systems, course structures, grading logic, and student progress tracking"

gaming:
  - game-logic-specialist (sonnet)
    "Expert in game state management, physics, rendering pipelines, and multiplayer sync"

ai-ml:
  - ml-pipeline-expert (sonnet)
    "Expert in training pipelines, model serving, feature engineering, and experiment tracking"

iot:
  - device-specialist (sonnet)
    "Expert in device communication protocols, sensor data processing, firmware updates, and telemetry"

media:
  - media-pipeline-specialist (sonnet)
    "Expert in media processing, transcoding, streaming protocols, and content delivery"

saas:
  - auth-specialist (sonnet)
    "Expert in authentication flows, RBAC, multi-tenancy, and session management"
  - billing-specialist (sonnet)
    "Expert in subscription billing, usage metering, invoice generation, and payment processing"

data-pipeline:
  - etl-specialist (sonnet)
    "Expert in data extraction, transformation, loading, scheduling, and pipeline orchestration"

social:
  - realtime-specialist (sonnet)
    "Expert in WebSocket connections, message queuing, presence systems, and notification delivery"

devtools:
  - plugin-architect (sonnet)
    "Expert in plugin/extension architecture, API design, CLI patterns, and developer experience"
```

If no frameworks/tools AND no domain detected (domain is `general`), skip this phase entirely and proceed to Phase 6.

#### Step 2: Present Agent Catalogue

Display all matched suggestions (both stack-based and domain-based) in a numbered table:

```
Suggested Custom Agents for This Project:

Based on your stack ({detected frameworks}) and domain ({detected domain}), these specialized agents can improve task routing:

  #  | Agent                  | Model  | Source  | Specialization
  1  | react-specialist       | Sonnet | Stack   | React component architecture, hooks, state management
  2  | node-api-specialist    | Sonnet | Stack   | Node.js API design, middleware, route handling
  3  | database-specialist    | Sonnet | Stack   | Database schema design, query optimization, ORM patterns
  4  | quant-expert           | Sonnet | Domain  | Trading algorithms, market data, order execution
  5  | risk-analyst           | Sonnet | Domain  | Risk assessment, portfolio analysis, compliance

These agents extend the built-in team with project-specific expertise.
Custom agents are automatically considered by the task router when their specialization matches a task.
```

#### Step 3: Ask User to Select

Present selection options and wait for user response:

```
Which agents would you like to add?
  a) All — add all suggested agents
  b) None — skip, use only built-in agents
  c) Select by number — e.g. "1,3" or "1-3"
```

#### Step 4: Create Selected Agents

For each selected agent:

1. Create `.claude/crew-agents/` directory if it doesn't exist
2. Generate the agent definition file `.claude/crew-agents/{name}.md` using the appropriate model template with **pre-filled responsibilities** specific to the framework (NOT generic placeholders)
3. Register in `.claude/crew-team.json` under the `agents` key with `"custom": true, "active": true`

**Sonnet custom agent template** (pre-filled example for react-specialist):

```markdown
---
name: crew-{name}
description: {description from mapping}
model: sonnet
---

You are the **{Name}** at CodeCrew. {description from mapping}.

## INDEX-FIRST PROTOCOL (MANDATORY)

**INDEX-FIRST**: Read `.claude/crew-index.json` → `crew-symbols.json` → then only specific lines from source files. Never read entire files.

## Your Responsibilities

1. {Framework-specific responsibility 1}
2. {Framework-specific responsibility 2}
3. {Framework-specific responsibility 3}
4. {Framework-specific responsibility 4}
5. Follow project conventions and patterns detected in the codebase
6. Coordinate with other agents when changes span beyond your specialization

## Output Format

When done, report:
- What you changed (file paths + summary)
- FILES_MODIFIED: {list}
- Confidence level: high | medium | low
- Any concerns or dependencies
```

**Haiku custom agent template:**

```markdown
---
name: crew-{name}
description: {description from mapping}
model: haiku
---

You are the **{Name}** at CodeCrew. {description from mapping}.

## INDEX-FIRST PROTOCOL (MANDATORY)

**INDEX-FIRST**: Read `.claude/crew-index.json` → `crew-symbols.json` → then only the lines you need. Never read entire files.

## Your Tasks

1. {Framework-specific task 1}
2. {Framework-specific task 2}
3. {Framework-specific task 3}
4. Follow project conventions detected in the codebase
5. If the task is too complex, report: "ESCALATE: Needs senior-dev or relevant sonnet specialist"

## Output

FILES_MODIFIED: {list}
CONFIDENCE: {high | medium | low}
```

Fill in the `{Framework-specific responsibility/task}` lines with real responsibilities relevant to the agent's specialization — do NOT leave them as generic placeholders. Use your knowledge of the framework to write 3-5 concrete responsibilities.

**crew-team.json registration** — add under `agents`:
```json
"custom-{name}": {
  "model": "{tier}",
  "active": true,
  "role": "{description}",
  "custom": true,
  "definitionPath": ".claude/crew-agents/{name}.md"
}
```

#### Step 5: Confirm

If agents were added:
```
Custom agents added: {n}
  {name} ({model}), {name} ({model}), ...

These agents will be auto-selected by the task router when tasks match their specialization.
Manage custom agents anytime with /crew agent list|remove
```

If user selected "None":
```
No custom agents added. You can add them later with /crew agent create
```

### Phase 6: Build Skill Catalog

Write `.claude/crew-skills.json` mapping all available ECC skills to categories:

```json
{
  "catalogVersion": 1,
  "totalSkills": 125,
  "relevantSkills": 45,
  "categories": {
    "always": [
      "strategic-compact",
      "context-budget",
      "verification-loop",
      "coding-standards",
      "iterative-retrieval",
      "search-first"
    ],
    "stack": {
      "javascript": ["typescript-patterns", "react-patterns", "nextjs-patterns", "backend-patterns"],
      "python": ["python-patterns", "django-patterns"],
      "go": ["golang-patterns"],
      "rust": ["rust-patterns"]
    },
    "taskType": {
      "bug-fix": ["iterative-retrieval", "deep-research", "codebase-onboarding"],
      "feature": ["architecture-decision-records", "agentic-engineering", "blueprint"],
      "test": ["tdd-workflow", "e2e-testing", "ai-regression-testing"],
      "security": ["security-scanning"],
      "docs": ["article-writing", "documentation-lookup"],
      "devops": ["deployment-patterns", "docker-patterns", "database-migrations", "git-workflow"],
      "review": ["verification-loop"],
      "refactor": ["architecture-decision-records", "backend-patterns"],
      "performance": ["cost-aware-llm-pipeline"]
    }
  },
  "detectedStack": ["javascript"],
  "activeSkills": ["typescript-patterns", "backend-patterns"]
}
```

### Phase 7: Report

Display initialization summary to the user:

```
CodeCrew ready — {project-name}
  {type} | {languages} | {count} files, {lines} lines
  Agents: {count}/{total} (Opus: 1, Sonnet: X, Haiku: Y) | Skills: {relevant}/{total}

Use /crew task "desc" to delegate work.
```
