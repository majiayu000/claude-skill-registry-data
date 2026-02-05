---
name: project-implementation
description: Personal project implementation and modification guide. Use when creating or modifying Python 3.13 personal projects with FastAPI/Typer, pyproject.toml, and uv package manager.
---

# Project Implementation & Modification

Specialist in personal project implementation following modern Python development standards.

## Core Standards

### Python Version (MANDATORY)
- **Python 3.13 REQUIRED** for all personal projects
- Update from older Python 3.11 references
- Ensure compatibility with Python 3.13 features

### Project Structure
- Single `src/` directory for all source code
- `pyproject.toml` for modern project configuration
- `uv` package manager for fast dependency management
- **No `modules/` directory** (unlike BTDP Framework)

### Technology Stack
- **FastAPI**: Async API development with Pydantic validation
- **Typer**: CLI development with type hints
- **uv**: Fast, reliable dependency management

## Quality Gates (MANDATORY)

### Code Formatting
- **Black**: `black -l 120 src/` after ANY Python modifications
- Line length: 120 characters

### Quality Standards (Zero Tolerance)
- **Pylint**: 10/10 score required, NO rule disabling
- **Bandit**: Zero security issues, document any `# nosec`
- **Safety**: Zero dependency vulnerabilities, NO exceptions

### Code Standards
- **String handling**: f-strings for interpolation, % style for logging
- **Async/await**: Use `aiohttp` instead of `requests`
- **Import organization**: Standard library → Third-party → Local
- **DRY principle**: ZERO TOLERANCE for code duplication

## Quick Workflows

### Create New Project
```bash
mkdir my-project && cd my-project
# Create pyproject.toml with requires-python = ">=3.13"
mkdir -p src tests
uv sync
uv add fastapi uvicorn  # For API projects
uv add typer           # For CLI projects
```

### Add Feature
1. Update dependencies: `uv add <package>`
2. Implement feature following code standards
3. Format: `black -l 120 src/`
4. Quality check: `pylint src/ && bandit -r src/ && safety check`
5. Update documentation (README.md, CLAUDE.md)

### Modify Existing Project
1. Ensure Python 3.13 compatibility
2. Sync dependencies: `uv sync`
3. Apply DRY principle - eliminate duplication
4. Refactor to async/await if needed
5. Pass all quality gates
6. Update documentation

## Git Workflow

### Branch Naming
- `feat/STRYxxxxxxx/description` - New features
- `fix/STRYxxxxxxx/description` - Bug fixes
- `clean/STRYxxxxxxx/description` - Refactoring

### Commit Messages
Format: `[STRYxxxxxxx](type) Description`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`
- Signed commits: `git commit -S -m "[STRYxxxxxxx](feat) Description"`

### Pull Requests
- Feature/fix branches → develop (ALWAYS squash merge)
- Clear description with story/issue references

## Documentation Requirements

### README.md
- Project description and purpose
- Installation and usage instructions
- Configuration details
- Prerequisites and permissions

### CLAUDE.md
- Implementation guidance
- Architecture decisions
- Key patterns and workflows
- Troubleshooting tips

## Architecture Principles

### DRY (Don't Repeat Yourself)
- **ZERO TOLERANCE** for code duplication
- Create utility modules for shared functionality
- Extract common patterns to reusable components

### Object-Oriented Design
- Class-based design with clear separation of concerns
- Single Responsibility Principle
- Interface-based abstractions when beneficial

### Dependency Injection
- Centralize dependencies in `main()` or application entry point
- Use FastAPI dependency injection for APIs
- Pass dependencies explicitly, avoid global state

### Security
- Never store credentials in code
- Use environment variables for sensitive data
- Validate all user inputs with Pydantic models
- Use `.env` files (never commit to git)

## Response Style

- Focus on clean, maintainable code
- Prioritize security and quality
- Use modern Python 3.13 features when beneficial
- Document architectural decisions
- Keep it simple and readable

## Detailed References

For comprehensive guides on specific topics:
- **FastAPI patterns**: `references/fastapi-patterns.md`
- **Typer CLI development**: `references/typer-patterns.md`
- **Code quality standards**: `references/code-standards.md`
- **Project structure**: `references/project-structure.md`
- **Common workflows**: `references/common-workflows.md`
