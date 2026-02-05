---
name: memory-generator
description: Generate CLAUDE.md project memory files by exploring codebases. Use when user asks to "generate memory", "create CLAUDE.md", "document this project", "understand this codebase", or starts work on a new/unfamiliar repository. Triggers on new project onboarding and documentation requests.
---

# Memory Generator Skill

Generate comprehensive CLAUDE.md project memory files by exploring and analyzing codebases.

## When to Use

Invoke this skill when:
- Starting work on a new/unfamiliar project
- A project lacks CLAUDE.md documentation
- User asks to "create memory" or "generate context" for a project
- Beginning exploration of a repository

## Exploration Process

### Phase 1: Project Structure Analysis

1. **Identify project root markers**:
   - `.git/` directory
   - `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.
   - `Makefile`, `CMakeLists.txt`, `build.gradle`

2. **Map directory structure**:
   ```bash
   tree -L 3 -d --dirsfirst
   # Or for large projects:
   find . -type d -maxdepth 3 | head -50
   ```

3. **Identify key directories**:
   - Source code: `src/`, `lib/`, `app/`, `pkg/`
   - Tests: `tests/`, `test/`, `__tests__/`, `spec/`
   - Config: `config/`, `.github/`, `.vscode/`
   - Docs: `docs/`, `doc/`, `documentation/`

### Phase 2: Technology Detection

1. **Language detection**:
   ```bash
   # Count files by extension
   find . -type f -name "*.py" | wc -l
   find . -type f -name "*.go" | wc -l
   find . -type f -name "*.rs" | wc -l
   find . -type f -name "*.ts" -o -name "*.tsx" | wc -l
   ```

2. **Framework detection**:
   - Python: Django, Flask, FastAPI, pytest
   - JavaScript: React, Vue, Next.js, Express
   - Go: Gin, Echo, standard library patterns
   - Rust: Actix, Axum, Tokio

3. **Dependency analysis**:
   - Read `requirements.txt`, `pyproject.toml`
   - Read `package.json`, `package-lock.json`
   - Read `Cargo.toml`, `go.mod`

### Phase 3: Pattern Recognition

1. **Architecture patterns**:
   - Monolith vs microservices
   - MVC, clean architecture, hexagonal
   - Module organization

2. **Code conventions**:
   - Naming patterns (snake_case, camelCase)
   - File naming conventions
   - Import organization

3. **Testing patterns**:
   - Test file naming (`test_*.py`, `*_test.go`)
   - Fixture patterns
   - Mock usage

### Phase 4: Entry Point Discovery

1. **Application entry points**:
   - `main.py`, `app.py`, `index.ts`
   - `cmd/`, `bin/` directories
   - `Makefile` targets

2. **Build/run commands**:
   - npm scripts
   - Makefile targets
   - Docker compose services

### Phase 5: Documentation Review

1. **Existing documentation**:
   - README.md content
   - API documentation
   - Architecture docs
   - Contributing guides

## Output: CLAUDE.md Template

```markdown
# [Project Name]

## Overview
[1-2 sentence project description based on README or package metadata]

## Tech Stack
- **Language**: [Primary language and version]
- **Framework**: [Main framework if applicable]
- **Key Dependencies**: [Important libraries]
- **Testing**: [Test framework]
- **Build Tool**: [npm, cargo, make, etc.]

## Project Structure
```
[Simplified tree showing key directories]
```

### Key Directories
- `src/` - [Description]
- `tests/` - [Description]
- [Other important directories]

## Development Commands

```bash
# Install dependencies
[command]

# Run tests
[command]

# Run application
[command]

# Build
[command]
```

## Architecture

### Code Organization
[Brief description of how code is organized - modules, packages, layers]

### Key Patterns
- [Pattern 1]: [Where/how it's used]
- [Pattern 2]: [Where/how it's used]

### Entry Points
- [Main entry point and what it does]
- [Other important entry points]

## Conventions

### Naming
- Files: [convention]
- Functions/methods: [convention]
- Classes/types: [convention]

### Code Style
- [Formatter used]
- [Linter used]
- [Key style rules]

### Testing
- Test files: [naming pattern]
- Fixtures: [location/pattern]
- Running: [command]

## Important Files

| File | Purpose |
|------|---------|
| [file1] | [purpose] |
| [file2] | [purpose] |

## Notes for Claude

- [Important context about how to work with this codebase]
- [Any quirks or non-obvious patterns]
- [Preferred approaches for this project]
```

## Customization

Tailor the generated CLAUDE.md based on:

### For ML/AI Projects
- Add sections on:
  - Model architecture locations
  - Training scripts
  - Dataset handling
  - Experiment tracking

### For Web Applications
- Add sections on:
  - API endpoints
  - Frontend structure
  - Database schema location
  - Authentication flow

### For Libraries/Packages
- Add sections on:
  - Public API surface
  - Versioning approach
  - Breaking change policy
  - Example usage

### For Monorepos
- Add sections on:
  - Package/workspace structure
  - Shared dependencies
  - Inter-package relationships
  - Build order

## Usage Example

When user says:
- "Generate memory for this project"
- "Create CLAUDE.md for this repo"
- "Help me understand this codebase"

Execute exploration process and generate CLAUDE.md:

```bash
# Step 1: Basic structure
ls -la
tree -L 2 -d --dirsfirst 2>/dev/null || find . -type d -maxdepth 2

# Step 2: Detect language/framework
cat package.json 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -30
cat Cargo.toml 2>/dev/null | head -30
cat go.mod 2>/dev/null

# Step 3: Read existing docs
cat README.md 2>/dev/null | head -100

# Step 4: Sample source files to understand patterns
# Find representative files and read them

# Step 5: Generate CLAUDE.md
```

## Output Location

- Primary: `./CLAUDE.md` (project root, version controlled)
- Alternative: `./.claude/CLAUDE.md` (claude-specific directory)
- Private: `./CLAUDE.local.md` (gitignored, personal notes)

Ask user preference if unclear.