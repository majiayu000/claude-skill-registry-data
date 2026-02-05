---
name: project-analyzer
description: Systematically analyze a codebase to understand its structure, purpose, technologies, and architecture. Use this skill when users ask to "analyze this project", "explain this codebase", "what does this project do", or need a comprehensive overview of repository contents.
---

# Project Analyzer

This skill helps you systematically analyze and understand codebases by following a structured approach to gather key information about the project.

## When to Use This Skill

Activate this skill when:
- User asks "what does this project do?"
- User requests "analyze this codebase" or "explain this repo"
- User wants to understand project structure or architecture
- You need to provide a comprehensive overview of an unfamiliar codebase
- User asks about the technologies or stack used in a project

## Analysis Process

Follow these steps systematically:

### 1. Project Overview
- Read `README.md`, `README.txt`, or similar documentation files
- Check `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent manifest files
- Look for `LICENSE` file to understand licensing
- Review `.git/config` or check remote URLs to understand the repository source

### 2. Technology Stack Detection
Identify the primary languages and frameworks by checking for:
- `package.json` → Node.js/JavaScript/TypeScript project
- `requirements.txt`, `pyproject.toml`, `setup.py` → Python project
- `Cargo.toml` → Rust project
- `go.mod` → Go project
- `pom.xml`, `build.gradle` → Java project
- `Gemfile` → Ruby project
- `.csproj`, `.sln` → .NET/C# project
- `composer.json` → PHP project

### 3. Project Structure Analysis
- Use `Glob` to identify key directories (`src/`, `lib/`, `tests/`, `docs/`, etc.)
- Look for configuration files (`.env.example`, `config/`, `.github/`, etc.)
- Identify entry points (`main.py`, `index.js`, `main.go`, `app.py`, etc.)
- Check for build/tooling files (`Makefile`, `Dockerfile`, CI/CD configs)

### 4. Code Architecture
- Identify main modules/packages using directory structure
- Look for architectural patterns (MVC, microservices, monolith, etc.)
- Check for API definitions (`openapi.yaml`, `schema.graphql`, route files)
- Review database schemas or models if present

### 5. Dependencies & Integrations
- List major dependencies from manifest files
- Identify external services (databases, APIs, cloud services)
- Note testing frameworks and tooling
- Check for containerization (Docker, Kubernetes)

## Output Format

Present your analysis in this structure:

```markdown
# Project Analysis: [Project Name]

## Overview
[Brief description of what the project does]

## Technology Stack
- **Language(s)**: [Primary languages]
- **Framework(s)**: [Main frameworks]
- **Runtime/Platform**: [Node.js, Python 3.x, etc.]

## Project Structure
[Key directories and their purposes]

## Architecture
[High-level architecture description]

## Key Features
[Main functionality and capabilities]

## Dependencies
[Notable dependencies and integrations]

## Entry Points
[Main files to start understanding the code]

## Development Setup
[How to build/run the project based on available documentation]
```

## Best Practices

- **Start with documentation**: Always read existing docs first
- **Use the right tools**: Prefer `Glob` for file searches, `Read` for reading files
- **Be thorough but concise**: Cover all important aspects without overwhelming detail
- **Provide context**: Explain why certain patterns or technologies are used
- **Highlight entry points**: Help users know where to start reading code
- **Note gaps**: If documentation is missing or unclear, mention it

## Examples

### Example 1: Web Application
```
User: "What does this project do?"
Assistant: [Activates project-analyzer skill]
[Reads README.md, package.json]
[Analyzes src/ structure]
[Provides comprehensive analysis]
```

### Example 2: Library/Package
```
User: "Explain this codebase to me"
Assistant: [Activates project-analyzer skill]
[Checks for setup.py or Cargo.toml]
[Reviews lib/ and tests/]
[Explains library purpose and API]
```

### Example 3: Microservices
```
User: "Analyze this repository"
Assistant: [Activates project-analyzer skill]
[Identifies multiple service directories]
[Checks docker-compose.yml]
[Explains microservice architecture]
```

## Anti-Patterns to Avoid

- Don't make assumptions without checking files
- Don't skip reading the README if it exists
- Don't provide generic descriptions without specific details
- Don't analyze every single file (focus on key files)
- Don't ignore configuration and tooling files
