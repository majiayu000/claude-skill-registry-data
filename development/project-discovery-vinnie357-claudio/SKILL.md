---
name: project-discovery
description: Activate when analyzing codebases to understand project structure, technology stack, dependencies, and development workflows
license: MIT
---

# Project Discovery

Guide for systematically analyzing codebases to identify technology stack, development tools, dependencies, and recommend relevant integrations like MCPs.

## When to Use This Skill

Activate when:
- Analyzing a new codebase to understand its structure
- Identifying technology stack and frameworks
- Discovering development tools and configuration
- Recommending MCPs or integrations based on project needs
- Understanding project dependencies and their purposes
- Planning project onboarding or documentation

## Discovery Process

### Phase 1: Project Structure Analysis
1. Examine root directory files (README, package.json, Cargo.toml, mix.exs, etc.)
2. Identify primary language(s) and frameworks
3. Map directory structure and conventions
4. Detect configuration files and their purposes

### Phase 2: Dependency Analysis
1. Parse package/dependency files
2. Categorize dependencies (runtime, dev, testing, build)
3. Identify version constraints and compatibility requirements
4. Flag potential security or maintenance concerns

### Phase 3: Tool Detection
1. Scan for configuration files of common tools
2. Examine scripts in package.json, Makefile, etc.
3. Identify CI/CD configurations
4. Detect database schemas and migration files

### Phase 4: MCP Recommendations
Based on discoveries, recommend MCPs such as:
- **Database MCPs**: postgres, mysql, sqlite, mongodb
- **Cloud MCPs**: aws, gcp, azure for deployment
- **Development MCPs**: docker, kubernetes for containerization
- **API MCPs**: github, gitlab for repository management

## Tool Identification Categories

### Package Managers
- npm, yarn, pnpm (JavaScript/TypeScript)
- pip, poetry, pipenv (Python)
- cargo (Rust)
- mix/hex (Elixir)
- go mod (Go)
- bundler (Ruby)

### Build Systems
- webpack, vite, esbuild (JavaScript)
- gradle, maven (Java)
- make, cmake (C/C++)
- mix (Elixir)

### Testing Frameworks
- jest, mocha, vitest (JavaScript)
- pytest, unittest (Python)
- cargo test (Rust)
- ExUnit (Elixir)

### Linting and Formatting
- eslint, prettier (JavaScript)
- black, ruff, flake8 (Python)
- clippy, rustfmt (Rust)
- credo, mix format (Elixir)

## Elixir-Specific Discovery

### AGENTS.md Processing
When discovering Elixir projects:
1. Search for `AGENTS.md` in project root (community standard)
2. Check for `usage-rules.md` as alternative
3. Scan `deps/*/` for library-specific AGENTS.md files
4. Extract AI-specific guidance and conventions

### Framework Detection
- **Phoenix**: config/, lib/, priv/ structure with Phoenix dependencies
- **LiveView**: Phoenix.LiveView dependencies and live view modules
- **OTP**: Application modules and supervision trees
- **Ecto**: Database schemas, migrations, repository patterns

## Analysis Report Structure

```markdown
# Project Discovery Report

## Project Overview
- **Name**: [Project Name]
- **Primary Language(s)**: [Languages]
- **Framework(s)**: [Frameworks]
- **Project Type**: [web app, CLI tool, library, etc.]

## Technology Stack
### Frontend
- [Framework/Library and version]
- [Build tools]

### Backend
- [Runtime/Framework]
- [Database(s)]

### Development Tools
- **Package Manager**: [npm, yarn, pip, etc.]
- **Build System**: [webpack, vite, etc.]
- **Testing**: [jest, pytest, etc.]
- **Linting**: [eslint, prettier, etc.]

## Recommended MCPs
Based on analysis, consider:
1. **[MCP Name]**: For [specific use case]
2. **[MCP Name]**: For [specific use case]

## Setup Instructions
[Quick start commands]
```

## Key Principles

- **Systematic Exploration**: Start with root files, then explore directories
- **Prioritize Important Discoveries**: Lead with most significant findings
- **Actionable Recommendations**: Provide specific MCP recommendations with installation commands
- **Flag Issues**: Identify potential problems or missing configurations
- **Context-Aware**: Tailor recommendations to project type and stack
