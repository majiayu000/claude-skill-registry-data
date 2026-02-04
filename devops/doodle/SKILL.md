---
name: doodle
description: Create and manage experimental features in the Doodle project. Use this skill when user requests creating a new doodle, adding features to the features folder, or mentions working on a specific language-based experimental project. Handles both new feature creation and continuation of existing features.
---

# Doodle Feature Creator

## Overview

This skill enables creating and managing experimental features in the Doodle project. The Doodle project is a feature-based, language-agnostic experimental playground where each feature lives in its own folder under `features/` and can use any appropriate programming language.

**Core Philosophy**: Flexibility over rigidity. Features adapt to their needs rather than conforming to strict templates.

## When to Use This Skill

Invoke this skill when the user:

1. **Explicitly mentions "doodle"**
   - "calculator doodle 만들어줘"
   - "Create a new doodle for..."

2. **Requests adding to features folder**
   - "features/에 새 프로젝트 추가"
   - "Add a new feature to the project"

3. **Specifies a language for experimental work**
   - "Python으로 웹스크래퍼 만들어줘"
   - "Go로 CLI 도구 구현하고 싶어"

4. **Continues work on existing features**
   - "hellojava에 기능 추가해줘"
   - "calculator-js 개선하자"

## Quick Start Workflow

When a user requests a new feature:

1. **Check for existing feature**
   ```bash
   ls features/ | grep feature-name
   ```
   - If exists: Continue working in that folder
   - If new: Create appropriate structure

2. **Determine language and structure**
   - From explicit user request: "in Python", "using Go"
   - From feature name suffix: "calculator-js", "algorithms-python"
   - Default: Ask user or infer from context

3. **Create feature folder**
   - Naming: `{feature-name}-{language}` (e.g., `web-server-go`)
   - Java often omits suffix: `hellojava`, `collections-utils`

4. **Start with TDD**
   - Write test files first
   - Define expected behavior
   - Implement to make tests pass

5. **Create comprehensive README**
   - Follow structure in `references/project_conventions.md`
   - Include language, purpose, usage, tests

## Core Capabilities

### 1. Feature Folder Management

When creating or working with features:

**Check if feature exists:**
```bash
# Look for existing feature folder
ls features/ | grep {feature-name}
```

**If exists:**
- Inform user: "Feature folder already exists, continuing work..."
- Work within existing structure
- Add or modify files as needed

**If new:**
- Create folder with appropriate naming
- Set up language-specific structure
- Initialize with tests and README

### 2. Language-Specific Structure Creation

Adapt structure based on language. Reference `references/project_conventions.md` for patterns:

**JavaScript**:
- `package.json` with test script
- Implementation file(s)
- `test.js` with custom runner
- Minimal dependencies

**Python**:
- `test_{feature}.py` (often combined impl + tests)
- No external dependencies preferred
- Use stdlib for simplicity

**Go**:
- `go.mod` with module path
- Package directory structure
- `*_test.go` test files
- Standard Go testing

**Java/Gradle**:
- Multi-module Gradle project
- `settings.gradle.kts`, `app/build.gradle.kts`
- Standard `src/main/java` and `src/test/java` layout
- JUnit 5 for testing

**Key Principle**: Consult `references/language_examples.md` for concrete examples, but adapt as needed for the specific feature.

### 3. TDD Implementation

Always follow Test-Driven Development:

1. **Write tests first**
   - Define what the feature should do
   - Create test cases for expected behavior
   - Include edge cases

2. **Implement functionality**
   - Make tests pass
   - Keep implementation simple
   - Follow language idioms

3. **Refactor**
   - Improve code quality
   - Keep tests green
   - Document as you go

### 4. README Generation

Every feature must have a comprehensive README. Use this structure:

```markdown
# Feature Name (Language)

**Language**: {Language}
**Purpose**: {Brief description}
**Status**: 🚧 In Progress / ✅ Complete

## Overview
{What this feature does and why}

## Features
- [ ] Feature 1
- [ ] Feature 2

## Quick Start
### Prerequisites
- {Language version, tools}

### Installation
```bash
cd features/{feature-name}
{install commands}
```

### Running Tests
```bash
{test command}
```

### Usage
{Code examples}

## Test Coverage
{Description of tests}

## Project Structure
```
{feature-name}/
├── ...
```

## Future Plans
- [ ] ...

## Development Notes
{Any special considerations}
```

Adapt sections based on feature complexity and language.

### 5. Naming Conventions

Follow established patterns from `references/project_conventions.md`:

**Feature Folders:**
- Lowercase kebab-case
- Language suffix: `-js`, `-python`, `-go`
- Java often plain: `hellojava`, `collections-utils`
- Examples: `calculator-js`, `ascii-art-go`, `algorithms-python`

**Files:**
- JavaScript: camelCase or snake_case for files
- Python: snake_case for everything
- Go: lowercase package names
- Java: PascalCase for classes, match package structure

**Packages/Modules:**
- Go: `github.com/homveloper/doodle/features/{feature-name}`
- Java: Match folder name (no hyphens): `hellojava`, `collectionsutils`

### 6. CI/CD Awareness

Be aware of GitHub Actions testing:

**Currently Supported:**
- Node.js: 18.x, 20.x, 22.x
- Python: 3.9, 3.10, 3.11, 3.12

**Can Be Added:**
- Go testing
- Java/Gradle testing

When appropriate, suggest adding CI/CD support for new languages.

## Workflow

When handling a feature request:

1. **Understand the request**
   - What feature?
   - Which language? (explicit or infer)
   - New or existing?

2. **Check existing features**
   - Look in `features/` folder
   - Check for similar or same-named features
   - Decide: new feature or continue existing

3. **Determine structure**
   - Consult `references/project_conventions.md` for patterns
   - Look at `references/language_examples.md` for similar examples
   - Adapt based on feature requirements

4. **Create files**
   - Start with test files (TDD)
   - Create implementation files
   - Add configuration files (package.json, go.mod, etc.)
   - Generate comprehensive README

5. **Verify setup**
   - Ensure test commands work
   - Check file structure makes sense
   - Confirm README is complete

6. **Communicate clearly**
   - Tell user what was created
   - Show file structure
   - Explain next steps
   - Provide test command

## Best Practices

### Flexibility First
- Don't force rigid templates
- Adapt to feature needs
- Use references as guides, not rules
- Each feature is an experiment

### TDD Always
- Tests define behavior
- Write tests before implementation
- Keep tests simple and clear
- Run tests frequently

### Minimal Dependencies
- Prefer standard library
- Zero dependencies ideal for simple features
- Document why external deps are needed
- Keep it simple

### Complete Documentation
- README is mandatory
- Include usage examples
- Document prerequisites
- Explain design decisions

### Language Idioms
- Follow language-specific conventions
- Use established patterns
- Write idiomatic code
- Respect language best practices

## Common Scenarios

### Scenario 1: Brand New Feature

```
User: "Go로 HTTP 서버 doodle 만들어줘"

Steps:
1. Check features/http-server-go doesn't exist
2. Create features/http-server-go/
3. Create go.mod
4. Create server/ package with server.go and server_test.go
5. Write tests first (TDD)
6. Implement basic HTTP server
7. Create comprehensive README
8. Test: go test -v
```

### Scenario 2: Existing Feature

```
User: "hellojava에 Result 패턴 추가해줘"

Steps:
1. Confirm features/hellojava exists
2. Add Result.java to src/main/java/hellojava/
3. Update existing code to use Result
4. Add tests in src/test/java/hellojava/
5. Update README with new feature
6. Test: ./gradlew test
```

### Scenario 3: Ambiguous Request

```
User: "calculator 만들어줘"

Steps:
1. Ask for language preference or infer from context
2. Check if features/calculator-* already exists
3. Once language determined, proceed with creation
4. Follow language-specific patterns
```

## Resources

### references/project_conventions.md

Comprehensive guide to Doodle project conventions:
- Feature naming patterns
- Language-specific structures
- README requirements
- TDD approach
- CI/CD integration
- Best practices

**Use this as primary reference** for understanding project patterns and conventions.

### references/language_examples.md

Concrete examples for each supported language:
- Complete working examples
- JavaScript string utilities
- Python math utilities
- Go file utilities
- Java collections utilities

**Use this for specific implementation patterns** when creating new features. Adapt examples to fit the specific feature being created.

---

**Remember**: The goal is experimentation and learning. Be flexible, follow TDD, document well, and adapt to each feature's unique needs.
