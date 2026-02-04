---
name: project-understanding
description: Analyzes codebases to map architecture, dependencies, complexity metrics, and data flows for rapid onboarding. Use when exploring new repos, understanding project layout, analyzing dependencies, measuring code complexity, or preparing codebase documentation.
---

# Project Understanding

Comprehensive codebase analysis for architecture mapping, dependency understanding, complexity analysis, and rapid developer onboarding.

## Quick Start

**Summarize a project:**
```
Analyze and summarize this project's structure, identifying key components and technologies.
```

**Map dependencies:**
```
Show me the dependency graph for this project, highlighting critical and outdated packages.
```

**Analyze complexity:**
```
Calculate complexity metrics for the core modules and identify high-risk areas.
```

## Capabilities

### 1. Directory Structure Analysis

Scan and summarize project layout:

```
1. Identify project type (monorepo, library, application, etc.)
2. Map top-level directories and their purposes
3. Locate entry points (main, index, app files)
4. Identify configuration files and their roles
5. Note test locations and documentation
```

**Output format:**
```markdown
## Project: {name}
**Type:** {monorepo|library|application|service|cli}
**Stack:** {primary technologies}

### Structure
- `src/` - Main source code
- `tests/` - Test suites
- `docs/` - Documentation
...

### Entry Points
- Main: `src/index.ts`
- CLI: `bin/cli.js`

### Key Files
- Config: `tsconfig.json`, `.eslintrc`
- CI: `.github/workflows/`
```

### 2. Dependency Analysis

Analyze package dependencies for health and risk:

**For Node.js projects:**
```bash
# Check outdated packages
npm outdated --json

# Audit for vulnerabilities
npm audit --json

# Analyze bundle size impact
npx bundle-phobia-cli package-name
```

**For Python projects:**
```bash
# List installed with versions
pip list --format=json

# Check for updates
pip list --outdated --format=json

# Security check
pip-audit --format=json
```

**Dependency categories:**
| Category | Description | Action |
|----------|-------------|--------|
| Critical | Security vulnerabilities | Update immediately |
| Outdated | Major version behind | Plan upgrade |
| Deprecated | No longer maintained | Find replacement |
| Heavy | Large bundle impact | Consider alternatives |
| Duplicate | Multiple versions | Deduplicate |

See [references/dependency-analysis.md](references/dependency-analysis.md) for language-specific patterns.

### 3. Architecture Mapping

Identify architectural patterns and boundaries:

**Detection patterns:**
- **MVC**: Look for `models/`, `views/`, `controllers/`
- **Clean/Hexagonal**: Look for `domain/`, `infrastructure/`, `application/`
- **Feature-based**: Look for `features/` or `modules/` with self-contained units
- **Layered**: Look for `api/`, `service/`, `repository/`, `entity/`

**Mapping process:**
1. Identify module boundaries
2. Trace import/require graphs
3. Find circular dependencies
4. Locate shared utilities
5. Map external integrations (DB, APIs, queues)

**Output: Architecture diagram (text-based)**
```
+-------------+     +-------------+
|   Web UI    |---->|   API       |
+-------------+     +------+------+
                           |
                    +------v------+
                    |  Services   |
                    +------+------+
                           |
              +------------+------------+
              v            v            v
        +---------+  +---------+  +---------+
        |   DB    |  |  Cache  |  |  Queue  |
        +---------+  +---------+  +---------+
```

### 4. Code Complexity Metrics

Analyze code complexity for maintainability assessment.

#### Cyclomatic Complexity

Measures the number of independent paths through code:

| Score | Risk Level | Action |
|-------|------------|--------|
| 1-10 | Low | Acceptable |
| 11-20 | Moderate | Consider refactoring |
| 21-50 | High | Refactor recommended |
| 50+ | Very High | Refactor required |

**Calculation tools:**
```bash
# JavaScript/TypeScript
npx escomplex src/ --format json

# Python
radon cc src/ -a -j

# Go
gocyclo -over 10 ./...

# General (multi-language)
lizard src/
```

#### Cognitive Complexity

Measures how difficult code is to understand (mental effort):

**High cognitive complexity indicators:**
- Deeply nested conditionals (>3 levels)
- Multiple loop breaks/continues
- Complex boolean expressions
- Switch statements with fallthrough
- Recursion without clear base case

See [references/complexity-metrics.md](references/complexity-metrics.md) for calculation methods.

#### Coupling Analysis

**Types of coupling (worst to best):**
1. **Content coupling**: Module modifies internal data of another
2. **Common coupling**: Shared global data
3. **Control coupling**: One module controls flow of another
4. **Stamp coupling**: Shared composite data structures
5. **Data coupling**: Only data parameters passed (best)

**Detection:**
```bash
# JavaScript - dependency-cruiser
npx dependency-cruiser --output-type dot src | dot -T svg > deps.svg

# Python - pydeps
pydeps src --cluster --max-bacon 2
```

### 5. API Surface Mapping

Map public interfaces and exports:

**Export analysis:**
```bash
# TypeScript/JavaScript
# Find all exports
grep -r "^export" src/ --include="*.ts"

# Find default exports
grep -r "export default" src/ --include="*.ts"
```

**Public API documentation:**
```markdown
## Public API Surface

### Exported Functions
| Function | Module | Parameters | Returns |
|----------|--------|------------|---------|
| `createUser` | `src/users.ts` | `(data: UserInput)` | `Promise<User>` |
| `validateEmail` | `src/utils.ts` | `(email: string)` | `boolean` |

### Exported Types
| Type | Module | Description |
|------|--------|-------------|
| `User` | `src/types.ts` | User entity interface |
| `Config` | `src/config.ts` | Configuration options |

### Breaking Change Risk
- High: `createUser` - used by 15 external modules
- Low: `validateEmail` - internal utility only
```

### 6. Data Flow Analysis

Map how data moves through the system:

**Data flow patterns:**
```
User Input --> Validation --> Business Logic --> Persistence --> Response
     |              |               |                |              |
     v              v               v                v              v
  [Forms]      [Validators]    [Services]       [Database]     [API Response]
```

**Trace data through layers:**
1. Entry points (API routes, event handlers)
2. Validation/transformation layers
3. Business logic services
4. Data access layer
5. External service calls
6. Response formatting

**Security-sensitive flows to identify:**
- Authentication data paths
- PII handling and storage
- Payment information
- Audit logging points

### 7. Integration Mapping

Map external service dependencies:

**Integration inventory:**
```markdown
## External Integrations

### Databases
| Type | Connection | Usage |
|------|------------|-------|
| PostgreSQL | `DATABASE_URL` | Primary data store |
| Redis | `REDIS_URL` | Session cache, job queue |

### Third-Party APIs
| Service | Purpose | Criticality |
|---------|---------|-------------|
| Stripe | Payments | Critical |
| SendGrid | Email | High |
| S3 | File storage | High |

### Internal Services
| Service | Protocol | Purpose |
|---------|----------|---------|
| Auth Service | gRPC | Authentication |
| Notification Service | HTTP | Push notifications |
```

### 8. License Compliance Scanning

Detect and analyze license usage:

```bash
# Node.js
npx license-checker --json > licenses.json
npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-3-Clause"

# Python
pip-licenses --format=json > licenses.json

# Go
go-licenses report ./...
```

**License compatibility matrix:**
| License | Commercial Use | Copyleft | Attribution |
|---------|---------------|----------|-------------|
| MIT | Yes | No | Yes |
| Apache-2.0 | Yes | No | Yes |
| GPL-3.0 | Yes | Yes (strong) | Yes |
| LGPL-3.0 | Yes | Yes (weak) | Yes |
| BSD-3-Clause | Yes | No | Yes |

See [references/license-scanning.md](references/license-scanning.md) for compliance guidance.

### 9. Tech Debt Estimation

Identify and quantify technical debt:

**Debt categories:**
| Category | Indicators | Impact |
|----------|------------|--------|
| Dependency Debt | Outdated packages, security vulnerabilities | Security risk, maintenance burden |
| Architecture Debt | Tight coupling, circular dependencies | Slow development, testing difficulty |
| Code Debt | High complexity, code smells | Bug risk, onboarding difficulty |
| Test Debt | Low coverage, missing tests | Regression risk |
| Documentation Debt | Missing/outdated docs | Onboarding friction |

**Debt estimation output:**
```markdown
## Technical Debt Assessment

### High Priority (Address within 2 weeks)
- [ ] 3 critical security vulnerabilities in dependencies
- [ ] Circular dependency between auth and user modules

### Medium Priority (Address within quarter)
- [ ] 5 modules with cyclomatic complexity > 20
- [ ] Test coverage below 60% for payment module

### Low Priority (Track and address opportunistically)
- [ ] Outdated documentation for API endpoints
- [ ] Inconsistent error handling patterns
```

### 10. Monorepo Navigation

Guide for understanding monorepo structures:

**Common monorepo patterns:**
| Tool | Structure | Workspace Definition |
|------|-----------|---------------------|
| npm/yarn workspaces | `packages/*` | `package.json` workspaces |
| Lerna | `packages/*` | `lerna.json` |
| Nx | `apps/*`, `libs/*` | `nx.json`, `project.json` |
| Turborepo | `apps/*`, `packages/*` | `turbo.json` |
| pnpm | `packages/*` | `pnpm-workspace.yaml` |

**Navigation strategy:**
1. Find workspace configuration file
2. Identify shared packages (`libs/`, `packages/shared/`)
3. Map dependencies between packages
4. Locate build order/pipeline

### 11. First PR Guidance

Generate onboarding guide for new contributors:

```markdown
## First PR Guide for {Project}

### Quick Setup
1. Fork and clone the repository
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env`
4. Run tests: `npm test`
5. Start dev server: `npm run dev`

### Finding Your First Issue
- Look for issues labeled `good first issue` or `help wanted`
- Issues in `docs/` are great for getting familiar
- Small bug fixes help you understand the codebase

### Code Conventions
- Use TypeScript strict mode
- Follow ESLint configuration
- Write tests for new features
- Update documentation for API changes

### PR Process
1. Create branch: `feat/issue-123-description`
2. Make atomic commits with conventional commit messages
3. Run `npm test` and `npm run lint` before pushing
4. Create PR with description linking to issue
5. Address review comments
6. Squash merge when approved

### Getting Help
- Check existing documentation in `docs/`
- Ask questions in PR comments
- Join #dev-help channel on Slack
```

## Workflow: Full Project Analysis

```
1. Scan root directory for project type indicators
2. Read primary config files (package.json, etc.)
3. Map directory structure (exclude node_modules, .git, etc.)
4. Identify entry points and build outputs
5. Analyze dependencies for health/security
6. Calculate complexity metrics for core modules
7. Detect architectural patterns
8. Map data flows and integrations
9. Scan for license compliance
10. Generate summary with recommendations
```

## Hook Integration

Integrate project understanding with Claude Code hooks:

### SessionStart Hook - Auto Project Analysis

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "command": "claude-skill project-understanding --quick-summary"
    }]
  }
}
```

**Use case:** Automatically analyze project when Claude Code session starts in a new directory. Provides immediate context about project structure, key files, and technologies.

**Hook response pattern:**
```typescript
interface ProjectAnalysisHookResponse {
  projectType: 'monorepo' | 'library' | 'application' | 'service' | 'cli';
  stack: string[];
  entryPoints: string[];
  keyDirectories: Record<string, string>;
  warnings?: string[];
}
```

### PreToolUse Hook - Context Injection

Before file operations, inject relevant project context:
- Module boundaries when editing files
- Related test files when modifying source
- Documentation that may need updates

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Project Analysis
on:
  pull_request:
    types: [opened]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency Analysis
        run: |
          npm audit --json > audit.json
          npm outdated --json > outdated.json

      - name: Complexity Check
        run: |
          npx escomplex src/ --format json > complexity.json

      - name: License Check
        run: |
          npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-3-Clause"

      - name: Comment Results
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const audit = JSON.parse(fs.readFileSync('audit.json'));
            // Create PR comment with analysis results
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for high complexity in changed files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|js)$')

for file in $changed_files; do
  complexity=$(npx escomplex "$file" --format json | jq '.aggregate.cyclomatic')
  if [ "$complexity" -gt 20 ]; then
    echo "Warning: $file has high cyclomatic complexity: $complexity"
  fi
done
```

## Reference Files

- [references/dependency-analysis.md](references/dependency-analysis.md) - Language-specific dependency analysis patterns
- [references/architecture-patterns.md](references/architecture-patterns.md) - Common architecture pattern detection
- [references/complexity-metrics.md](references/complexity-metrics.md) - Complexity calculation patterns by language
- [references/license-scanning.md](references/license-scanning.md) - License detection and compliance guidance
