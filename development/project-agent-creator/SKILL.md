---
name: project-agent-creator
description: Use when setting up project-specific agents via /cc:setup-project or when user requests custom agents for their codebase - analyzes project to create specialized, project-aware implementer agents that understand architecture, patterns, dependencies, and conventions
---

# Project Agent Creator

## Overview

**Creating project-specific agents transforms generic implementers into specialists who understand YOUR codebase.**

This skill analyzes your project and creates dedicated agents (e.g., `project-python-implementer.md`) that extend generic agents with project-specific knowledge: architecture patterns, dependencies, conventions, testing approaches, and codebase structure.

**Core principle:** Project-specific agents are generic agents + deep project context.

## When to Use

Use this skill when:
- User runs `/cc:setup-project` command
- User requests "create custom agents for my project"
- You need agents that understand project-specific architecture
- Generic agents need project context to be effective
- Setting up a new development environment

Do NOT use for:
- One-off implementations (use generic agents)
- Projects without clear patterns
- Quick prototypes or experimental code

## Project Analysis Workflow

### Phase 1: Project Detection

Detect project type and structure:

**1. Language/Framework Detection**

Check for language indicators in project root:
- Python: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
- TypeScript/JavaScript: `package.json`, `tsconfig.json`
- Go: `go.mod`, `go.sum`
- Rust: `Cargo.toml`
- Java: `pom.xml`, `build.gradle`

**2. Architecture Analysis**

Identify architecture patterns:
- Check directory structure (e.g., `src/`, `lib/`, `core/`, `app/`)
- Look for architectural markers:
  - `repositories/`, `services/`, `controllers/` → Repository/Service pattern
  - `domain/`, `application/`, `infrastructure/` → Clean Architecture
  - `api/`, `worker/`, `web/` → Microservices
  - `components/`, `hooks/`, `pages/` → React patterns

**3. Dependency Analysis**

Scan dependencies for key libraries:
- Web frameworks: FastAPI, Django, Flask, Express, NestJS
- Testing: pytest, Jest, Vitest, Go testing
- Database: SQLAlchemy, Prisma, TypeORM
- Async: asyncio, aiohttp, async/await patterns

**4. Convention Discovery**

Find existing patterns in codebase:
- Import patterns (check 5-10 files)
- Class/function naming conventions
- File organization
- Testing patterns (check `tests/` or `__tests__/`)
- Error handling approaches

### Phase 2: Interactive Presentation

**CRITICAL: Always present findings to user before generating agents.**

Create a summary showing:

```markdown
## Project Analysis Results

**Project Type:** Python with FastAPI
**Architecture:** Clean Architecture (domain/application/infrastructure)
**Key Dependencies:**
- FastAPI for API endpoints
- SQLAlchemy for database
- pytest for testing
- Pydantic for validation

**Patterns Discovered:**
- Repository pattern in `core/repositories/`
- Service layer in `core/services/`
- Dependency injection via FastAPI Depends
- Type hints throughout (mypy strict mode)
- Async/await for all I/O

**Testing Approach:**
- pytest with async support
- Fixtures in `tests/conftest.py`
- Integration tests with test database

**Agent Recommendation:**
I recommend creating `project-python-implementer.md` that:
- Understands your Clean Architecture structure
- Uses repository pattern from `core/repositories/`
- Follows your async patterns
- Knows your testing conventions
```

Ask user: "Should I create this project-specific agent?"

### Phase 3: Agent Generation

**Agent Structure:**

```yaml
---
name: project-{language}-implementer
model: sonnet
description: {Language} implementation specialist for THIS project. Understands {project-specific-patterns}. Use for implementing {language} code in this project.
tools: Read, Write, MultiEdit, Bash, Grep
---
```

**Agent Content Template:**

```markdown
You are a {LANGUAGE} implementation specialist for THIS specific project.

## Project Context

**Architecture:** {discovered architecture}
**Key Patterns:**
- {pattern 1}
- {pattern 2}
- {pattern 3}

**Directory Structure:**
- `{dir1}/` - {purpose}
- `{dir2}/` - {purpose}

## Critical Project-Specific Rules

### 1. Architecture Adherence
{Explain how to follow the project's architecture}

Example:
- **Repository Pattern:** All data access goes through repositories in `core/repositories/`
- **Service Layer:** Business logic lives in `core/services/`
- **Dependency Injection:** Use FastAPI's Depends() for all dependencies

### 2. Import Conventions
{Show actual import patterns from project}

Example from this project:
```python
from core.repositories.user_repository import UserRepository
from core.services.auth_service import AuthService
from domain.models.user import User
```

### 3. Testing Requirements
{Explain project testing approach}

Example:
- All services need unit tests in `tests/unit/`
- Use fixtures from `tests/conftest.py`
- Integration tests in `tests/integration/` with test database
- Async tests use `@pytest.mark.asyncio`

### 4. Error Handling
{Show project error handling pattern}

Example:
```python
# Project uses custom exception hierarchy
from core.exceptions import (
    ApplicationError,
    ValidationError,
    NotFoundError
)
```

### 5. Type Safety
{Explain type checking approach}

Example:
- mypy strict mode required
- All functions have type hints
- Use Pydantic models for validation

## Project-Specific Patterns

{Include 2-3 code examples from actual project showing preferred patterns}

### Pattern 1: Repository Usage
{Show actual repository code from project}

### Pattern 2: Service Implementation
{Show actual service code from project}

### Pattern 3: API Endpoint Pattern
{Show actual endpoint code from project}

## Quality Checklist

Before completing implementation:

Generic {language} checklist items:
- [ ] {standard language-specific checks}

PROJECT-SPECIFIC checks:
- [ ] Follows {project architecture} structure
- [ ] Uses {project pattern} from `{directory}/`
- [ ] Follows import conventions
- [ ] Tests match project testing patterns
- [ ] Error handling uses project exception hierarchy
- [ ] {Other project-specific requirements}

## File Locations

When implementing features:
- Models/Domain: `{actual path}`
- Repositories: `{actual path}`
- Services: `{actual path}`
- API endpoints: `{actual path}`
- Tests: `{actual path}`

**ALWAYS check these directories first before creating new files.**

## Never Do These (Project-Specific)

Beyond generic {language} anti-patterns:

1. **Never create repositories outside `{repo path}`** - Breaks architecture
2. **Never skip {project pattern}** - Required by our design
3. **Never use {anti-pattern found in codebase}** - Project is moving away from this
4. **{Other project-specific anti-patterns}**

{Include base generic agent content as fallback}
```

**Save Location:** `.claude/agents/project-{language}-implementer.md`

## Implementation Steps

**Use TodoWrite to create todos for each step:**

1. [ ] Detect project type (language, framework, architecture)
2. [ ] Analyze dependencies and key libraries
3. [ ] Discover patterns by reading sample files
4. [ ] Identify testing approach and conventions
5. [ ] Create analysis summary
6. [ ] Present findings to user interactively
7. [ ] Get user approval to generate agent
8. [ ] Generate agent using template + project context
9. [ ] Write agent to `.claude/agents/project-{language}-implementer.md`
10. [ ] Confirm agent creation with user

## Examples

### Example 1: Python FastAPI Project

**Input:** Python project with FastAPI, SQLAlchemy, Clean Architecture

**Analysis:**
- Detected: Python 3.11, FastAPI, SQLAlchemy, pytest
- Architecture: Clean Architecture (domain/application/infrastructure)
- Patterns: Repository pattern, dependency injection, async/await

**Generated Agent:** `project-python-implementer.md` that:
- Knows to use repositories from `core/repositories/`
- Understands service layer in `core/services/`
- Follows async patterns throughout
- Uses project's custom exception hierarchy

### Example 2: TypeScript React Project

**Input:** TypeScript project with React, Vite, TailwindCSS

**Analysis:**
- Detected: TypeScript 5.x, React 18, Vite, TailwindCSS
- Architecture: Component-based with custom hooks
- Patterns: Compound components, render props, context for state

**Generated Agent:** `project-typescript-implementer.md` that:
- Uses project component patterns
- Follows TailwindCSS conventions
- Knows custom hooks location
- Understands project state management approach

## Common Mistakes

### ❌ Generic Analysis
Creating agent without deep project understanding
**Fix:** Read actual code files to discover patterns

### ❌ Skipping User Approval
Generating agent without presenting findings
**Fix:** Always show analysis summary and get approval

### ❌ Too Generic
Agent doesn't include specific patterns from project
**Fix:** Include 2-3 actual code examples from codebase

### ❌ Missing Anti-Patterns
Not documenting what NOT to do
**Fix:** Note patterns project is moving away from

## Integration with writing-skills

**REQUIRED BACKGROUND:** Understanding `writing-skills` helps create better agents.

Agent creation follows similar principles:
- Test with real implementation tasks
- Iterate based on what agents struggle with
- Add explicit counters for common mistakes
- Include actual project code examples

## Quality Gates

Before considering agent complete:

- [ ] Agent includes actual code examples from project (not generic templates)
- [ ] Architecture patterns are specific and actionable
- [ ] File locations are exact paths from project
- [ ] Testing approach matches actual test files
- [ ] Import conventions match actual imports
- [ ] User has approved the agent
- [ ] Agent saved to correct location

## Naming Convention

**CRITICAL:** Use `project-{language}-implementer` naming:

- ✅ `project-python-implementer.md`
- ✅ `project-typescript-implementer.md`
- ✅ `project-go-implementer.md`
- ❌ `python-implementer-custom.md` (breaks convention)
- ❌ `my-python-agent.md` (unclear purpose)

The `project-` prefix ensures:
- No conflicts with generic agents
- Clear indication of project-specific knowledge
- Consistent discovery pattern
