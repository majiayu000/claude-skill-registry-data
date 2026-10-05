---
name: onboard
description: "Generates a comprehensive codebase onboarding guide by scanning the project structure, detecting the stack, mapping architecture, and identifying key entry points. Use when joining a new project or onboarding teammates."
argument-hint: "[optional: specific area to focus on]"
allowed-tools: Read, Grep, Glob, Bash
---

# Codebase Onboarding

## Auto-Scan
!`find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -not -path "*/__pycache__/*" -not -path "*/target/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/.next/*" 2>/dev/null | wc -l`

## Project Files
!`ls package.json requirements.txt pyproject.toml go.mod Cargo.toml *.csproj *.sln Gemfile composer.json mix.exs Makefile Dockerfile docker-compose* 2>/dev/null`

## Directory Structure
!`tree -L 2 -I "node_modules|.git|vendor|__pycache__|target|dist|build|.next" 2>/dev/null || find . -type d -maxdepth 2 -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null`

## README
!`cat README.md 2>/dev/null | head -50`

## Git Activity
!`git log --oneline -20 2>/dev/null`
!`git shortlog -sn --no-merges 2>/dev/null | head -10`

---

## Onboarding Guide Generation

### Section 1: Project Overview
- What this project does (from README + code analysis)
- Who maintains it (from git history)
- How active it is (recent commits, contributors)

### Section 2: Tech Stack
Detect and document:
- Language(s) and version(s)
- Framework(s)
- Database(s)
- Package manager
- Test framework
- Build tools
- CI/CD system

### Section 3: Directory Map
Annotated directory tree:
```
src/
├── components/   # UI components
├── services/     # Business logic
├── utils/        # Shared utilities
├── types/        # Type definitions
└── config/       # Configuration
```

### Section 4: Key Entry Points
- Application entry point (main file, index, app)
- API routes / endpoints
- Database schema / models
- Configuration files
- Environment variables needed

### Section 5: How to Run
- Prerequisites (runtime versions, tools)
- Installation steps
- Development server command
- Test command
- Build command

### Section 6: Architecture Patterns
- Code organization pattern (MVC, hexagonal, feature-based, etc.)
- State management approach
- Data flow (request lifecycle)
- Error handling strategy
- Authentication/authorization approach

### Section 7: Where to Start
Based on the codebase analysis:
- "If you need to fix a bug, start here: ..."
- "If you need to add a feature, start here: ..."
- "If you need to understand the data model, look at: ..."

### Section 8: Gotchas & Tribal Knowledge
- Non-obvious conventions found in the code
- Common pitfalls (from error handling patterns and comments)
- Areas with tech debt (complex, undocumented, or heavily modified files)

## Rules
- Base everything on actual code — don't assume
- Flag areas that lack documentation
- Be honest about code quality and tech debt
- Include exact file paths for every reference
