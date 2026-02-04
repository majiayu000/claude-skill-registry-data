---
name: managing-claude-memory
description: Expert guidance for creating, updating, and maintaining CLAUDE.md memory files following best practices for hierarchical memory, structure, content organization, and team collaboration
---

# Managing Claude Memory (CLAUDE.md Files)

## Overview

CLAUDE.md files are persistent memory documents that help Claude understand codebases, preferences, and working patterns across sessions. They serve as a bridge between sessions, maintaining context and enforcing guidelines.

## File Locations and Hierarchy

Claude searches for CLAUDE.md files in a **hierarchical memory system** with four levels (highest to lowest priority):

1. **Enterprise Policy** (`/etc/claude-code/CLAUDE.md` on Linux, `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS)
   - Organization-wide security policies and compliance
   - Managed by IT teams
   - Cannot be overridden by users

2. **Project Memory** (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
   - Team-shared guidelines stored in version control
   - Architecture and coding standards
   - Project-specific workflows and conventions
   - **Most commonly used**

3. **User Memory** (`~/.claude/CLAUDE.md`)
   - Personal preferences applying across all projects
   - Global working style and guidelines
   - Cross-project defaults

4. **Project Memory (Local)** (`./CLAUDE.local.md`)
   - Personal overrides for specific project
   - Added to .gitignore (not committed)
   - Use for personal preferences that differ from team

### Import Syntax

CLAUDE.md supports importing other files using `@path/to/import` syntax:

```markdown
## Architecture
@./docs/architecture-guide.md

## Testing Standards
@./specs/testing-requirements.md
```

**Features:**
- Up to 5 levels of recursive imports allowed
- Better multi-worktree support
- Allows breaking CLAUDE.md into logical sections

## Structure Guidelines

### Recommended Section Order

```markdown
# [Project Name]

[One-sentence description]

## Quick Reference (Optional: for files >150 lines)
## Commands
## Project Structure
## Code Style
## Architecture Patterns
## Critical Rules
## Environment Variables
## Common Pitfalls
## Testing
## Additional Resources
```

### Standard Conventions

- Use **Markdown headings** (`#`, `##`, `###`) to organize information
- Keep information **concise and actionable** (respect token budget)
- Use **bullet points** for lists
- Include **code blocks with inline comments** for commands
- Add **emphasis markers** (IMPORTANT, ALWAYS, NEVER) for critical rules
- Group related guidelines under logical sections

## Content Guidelines

### What SHOULD Go in CLAUDE.md

1. **Model Preferences**
   - Which Claude model to use for planning vs execution
   - When to use extended thinking or other features

2. **Project Structure Rules**
   - Where to place files and folders
   - Required directory organization
   - Naming conventions

3. **Code & Architecture Standards**
   - Design patterns to follow or avoid
   - Code organization principles
   - Technology stack constraints
   - Import/export conventions

4. **Commands with Context**
   - Development, testing, build commands
   - Inline comments explaining when to use each

5. **Environment Variables**
   - Required vs optional variables
   - Security notes (NEVER commit)
   - Default values

6. **Common Pitfalls**
   - ❌/✅ examples showing wrong vs right approaches
   - Project-specific mistakes to avoid

7. **Testing Conventions**
   - Framework and coverage requirements
   - Test file locations
   - Testing patterns

8. **Important Restrictions**
   - Things Claude must NOT do without explicit approval
   - Security or compliance requirements

9. **Documentation References**
   - @ file references to related docs
   - Links to detailed specifications

### What Should NOT Go in CLAUDE.md

1. **Sensitive Data** - NEVER include API keys, passwords, tokens, secrets
   - Use settings.json deny rules instead
   - Store secrets in .env files

2. **Large Code Blocks** - Keep concise
   - Reference files instead of embedding large code

3. **Frequently Changing Information**
   - Use task files or planning documents instead
   - CLAUDE.md should contain stable, long-term guidance

4. **Tool Configurations**
   - Use `.claude/settings.json` instead
   - Permissions, hooks, MCP servers, environment variables

5. **Verbose Paragraphs**
   - Use bullet points and short declarative statements
   - Every line consumes tokens on every request

6. **Obvious Explanations**
   - Folder named "components" doesn't need explanation
   - Focus on non-obvious conventions and rules

## Best Practices

### 1. Token Efficiency

**Rule:** Keep CLAUDE.md files concise. Every line consumes tokens on every request.

❌ **Too verbose:**
```markdown
This project uses TypeScript with strict mode enabled, which means that
all code must be properly typed and we don't allow the use of the 'any'
type anywhere in the codebase because it defeats the purpose.
```

✅ **Concise:**
```markdown
- **TypeScript strict mode** - No implicit any, strict null checks
- **No any types** - Use `unknown` if type is truly unknown
```

### 2. Critical Rules with Emphasis

**Rule:** Use emphasis markers (IMPORTANT, ALWAYS, NEVER, MUST) for critical rules.

**Example:**
```markdown
## Critical Rules

- **IMPORTANT:** All imports MUST include `.js` extension (ES modules)
- **NEVER delete users** - Use `active: false` for soft delete
- **ALWAYS validate requests** with Zod schemas before controllers
```

### 3. Common Pitfalls with Visual Examples

**Rule:** Document mistakes with ❌ (wrong) and ✅ (correct) code examples.

**Example:**
```markdown
### Import Extensions
❌ `import { User } from './models/user'`
✅ `import { User } from './models/user.js'`

### Error Handling
❌ `throw 'User not found'`
✅ `throw new NotFoundError('User not found')`
```

### 4. Command Blocks with Inline Comments

**Rule:** Group commands by purpose with comments explaining when to use.

**Example:**
```markdown
### Development
```bash
npm run dev          # Start server with hot reload on port 4000
npm run typecheck    # Type check without emit (run before commits)
npm run lint:fix     # Auto-fix linting issues
```
```

### 5. Hierarchical Structure for Monorepos

**Rule:** Root CLAUDE.md provides overview, subdirectory files provide specifics.

**Example:**
```markdown
## Monorepo Structure

**Directory-specific guidance:**
- See `client/CLAUDE.md` for React/Vite patterns
- See `server/CLAUDE.md` for Express/Node patterns
- See `shared/CLAUDE.md` for shared library development
```

### 6. Quick Reference Section

**Rule:** For complex projects (>150 lines), start with Quick Reference.

**Example:**
```markdown
## Quick Reference

**Full Documentation:**
- **API Reference:** `README.md` (1,663 lines)
- **Migration Guide:** `docs/MIGRATION.md` (1,051 lines)

**Package:** `@app-master/auth@0.1.0`
**Test Coverage:** 96.73% (329 passing tests)
```

### 7. @ File References for Discovery

**Rule:** Use @path/to/file syntax to help Claude discover related docs.

**Example:**
```markdown
## Common Workflows

- **Modify AI Behavior**: @server/systemInstructions/CLAUDE.md
- **Add New Tags**: @docs/tag-system.md
- **Database Schema**: @docs/database.md
```

### 8. User vs Project Level Separation

**User-level (`~/.claude/CLAUDE.md`):**
- Model selection preferences
- Universal code style preferences
- Documentation conventions (if truly universal)
- Git commit preferences

**Project-level (`./CLAUDE.md`):**
- Project overview and tech stack
- Project-specific patterns
- Critical business rules
- Team coding standards

**Rule:** Never duplicate content. Keep project-specific rules at project level only.

## Templates

### Template 1: Minimal (<50 lines)

**Use when:** Small projects, prototypes, POCs, simple utilities

```markdown
# [Project Name]

[One-sentence description]

## Tech Stack
- [Framework/Language with version]
- [Key dependencies]

## Commands

### Development
```bash
[start command]    # [Description]
[test command]     # [Description]
```

## Project Structure
```
[directory tree with brief descriptions]
```

## Code Style
- [Import style]
- [Naming conventions]
- [File organization]

## Critical Rules
- **IMPORTANT:** [Critical constraint]
- **NEVER** [Common mistake to avoid]
- **ALWAYS** [Essential practice]
```

### Template 2: Standard (100-200 lines)

**Use when:** Most full-featured applications, team projects

```markdown
# [Project Name]

[2-3 sentence description including purpose and key features]

## Tech Stack
- [Framework versions]
- [Key dependencies]

## Commands

### Development
```bash
[commands with inline comments]
```

### Testing
```bash
[test commands]
```

### Production
```bash
[build/deploy commands]
```

## Project Structure
```
[directory tree with purpose explanations]
```

**Key Files:**
- `[file]` - [Purpose]
- `[file]` - [Purpose]

## Code Style

### Import/Export
- [Style with examples]

### Naming Conventions
- [Pattern] - [Use case]

### TypeScript/Type System
- [Key rules]

## Architecture Patterns

### [Pattern Category 1]
[Brief explanation with code example]

### [Pattern Category 2]
[Brief explanation]

## Critical Rules
- **IMPORTANT:** [Critical rule]
- **NEVER** [Anti-pattern]
- **ALWAYS** [Best practice]

## Environment Variables

### Required
- `[VAR]` - [Description]

### Optional
- `[VAR]` - [Description with default]

## Common Pitfalls

### [Category]
❌ [Wrong way with code]
✅ [Right way with code]

## Testing
- **Framework:** [Tool]
- **Coverage:** [Target]
- **Commands:** [Key commands]

## Additional Resources
- **[Doc Category]:** [Path] - [Description]
```

### Template 3: Monorepo Root

**Use when:** Multiple related projects in one repository

```markdown
# [Monorepo Name]

[Description of overall system]

## Monorepo Structure

```
project-root/
├── [package1]/       - [Description] (see [package1]/CLAUDE.md)
├── [package2]/       - [Description] (see [package2]/CLAUDE.md)
└── [shared]/         - [Description] (see [shared]/CLAUDE.md)
```

**Directory-specific guidance:**
- See `[package1]/CLAUDE.md` for [topic]
- See `[package2]/CLAUDE.md` for [topic]

## Development

### Terminal Setup
```bash
# Terminal 1: [Service]
[command]

# Terminal 2: [Service]
[command]
```

### Testing
```bash
# Test [package1]
[command]

# Test [package2]
[command]
```

## Cross-Cutting Patterns
- **[Pattern]** - [Description]

## Monorepo Conventions

### Package Management
- **[Approach]** - [Explanation]

## Critical Business Rules
- **NEVER** [Global rule]
- **ALWAYS** [Global rule]

## Git Workflow
- **Main branch:** [branch]
- **Feature branches:** [pattern]

## Common Pitfalls

### Monorepo Management
❌ [Wrong approach]
✅ [Right approach]
```

### Template 4: Shared Library

**Use when:** Reusable packages/libraries consumed by multiple projects

```markdown
# [Library Name]

[One-line description of library purpose]

## Quick Reference

**Full Documentation:**
- **API Reference:** `README.md` - [Brief description]

**Package:** `[package-name]@[version]`
**Test Coverage:** [percentage]

## Installation

### Build the Library
```bash
[build commands]
```

### Add to Consuming Project
```json
{
  "dependencies": {
    "[package-name]": "[path or version]"
  }
}
```

## Common Usage Patterns

### [Pattern Category]
```typescript
[Code example with explanation]
```

## Library Structure
```
src/
├── [module]/    - [Purpose]
```

## Common Patterns

### Backend
```typescript
[Example]
```

### Frontend
```typescript
[Example]
```

## Testing
- **Framework:** [Tool]
- **Coverage:** [Target]
- **Commands:** [List]

## Critical Rules
- **IMPORTANT:** [Key rule]
- **NEVER** [Anti-pattern]
- **ALWAYS** [Best practice]

## Common Pitfalls

### [Category]
❌ **WRONG:** [Code example]
✅ **CORRECT:** [Code example]

## Performance
- [Bundle size info]
- [Tree-shaking guidance]
```

### Template 5: User-Level

**Use when:** Personal preferences across all projects

```markdown
# Personal Claude Code Preferences

## Model Usage

### Planning Mode
[Preferred model]

### Execution Mode
[Preferred model]

## Project Structure Conventions

- [Universal folder patterns]
- [Backup file locations]

## Code Style

- [Naming preferences]
- [Comment style]
- [Import organization]

## Documentation Guidelines

### When to Create Documentation
- **NEVER** create documentation files unless explicitly requested
- Only create when user specifically asks

### Documentation Structure
- [Folder organization if you create docs]

## Design Principles

- [Your coding philosophy]
- [Simplicity vs complexity preferences]

## Git Conventions

- [Commit message style]
- [Never commit without explicit instruction]
```

### Template 6: Training/Tutorial Repository

**Use when:** Educational repositories, course materials, learning resources

```markdown
# [Course/Tutorial Name]

[Description of learning objectives]

## Repository Structure

### Core Directories
- `[dir]/` - [Purpose and what learners do]
  - `[subdir]/` - [Purpose]

### Key File Patterns
- `[filename]` - [What it demonstrates]

## Development Setup

### Environment Setup
```bash
[Setup commands with explanations]
```

### [Technology] Server
[How to run required services]

## Common Development Commands

### [Task Category]
```bash
[command] # [Explanation]
```

## [Technology] Architecture Patterns

### Core Components
- **[Component]** - [What it does and how to use it]

## Dependencies

Key packages:
- `[package]` - [Purpose]

## Development Environment

This repository works with:
- **[Environment 1]** - [Special notes]
- **[Environment 2]** - [Special notes]
```

## Good Examples

### Example 1: Monorepo Root Overview

```markdown
# App Master - Internal user and application management system

Monorepo with React frontend and Express backend.

## Monorepo Structure

```
project-root/
├── client/          - React 19 + Vite + TypeScript (port 3000)
├── server/          - Express + TypeScript + MongoDB (port 4000)
└── docs/            - PRD and documentation
```

**Directory-specific guidance:**
- See `client/CLAUDE.md` for React/Vite patterns
- See `server/CLAUDE.md` for Express/Node patterns

## Critical Business Rules

- **NEVER delete users/applications** - Set `active: false` for soft delete
- **NEVER commit .env files** - Use .env.sample templates
- **ALWAYS validate inputs** - Both frontend and backend
```

**Why this is good:**
- Clear project identity
- Visual structure
- Hierarchical navigation
- Critical rules emphasized

### Example 2: Backend Code Style

```markdown
## Code Style

### Import/Export
- **ES modules only** - All imports require `.js` extension
- **Path aliases** - Use `@/` for `src/`
- **No default exports** - Use named exports

### Error Handling
- **Use AppError classes** - NotFoundError, ValidationError, etc.
- **Wrap async routes** - Use `asyncHandler()`
- **Never throw strings** - Always throw Error instances

## Common Pitfalls

### Import Extensions
❌ `import { User } from './models/user'`
✅ `import { User } from './models/user.js'`

### Async Routes
❌ `router.get('/users', async (req, res) => { ... })`
✅ `router.get('/users', asyncHandler(async (req, res) => { ... }))`
```

### Example 3: Library Quick Reference

```markdown
## Quick Reference

**Full Documentation:**
- **API Reference:** `README.md` (1,663 lines)
- **Migration Guide:** `docs/MIGRATION.md` (1,051 lines)

**Package:** `@app-master/auth@0.1.0`
**Test Coverage:** 96.73% (329 passing tests)

## Common Usage Patterns

### Subpath Imports (Recommended for Tree-Shaking)

**IMPORTANT:** Use subpath imports to minimize bundle size

```typescript
// Types
import { User, UserRole } from '@app-master/auth/types';

// Validation schemas
import { loginSchema } from '@app-master/auth/schemas';
```

## Common Pitfalls

### Importing Entire Package

❌ **WRONG (imports everything):**
```typescript
import { User, loginSchema } from '@app-master/auth';
```

✅ **CORRECT (granular imports):**
```typescript
import { User } from '@app-master/auth/types';
import { loginSchema } from '@app-master/auth/schemas';
```
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Duplicating User-Level File

**Problem:**
```markdown
# Project CLAUDE.md that duplicates user-level content

# Model usage
## Planning mode
Opus when available
## Execution mode
Sonnet
[... exact copy of user-level CLAUDE.md ...]
```

**Why this is bad:**
- Creates maintenance burden
- Unclear which file takes precedence
- Wastes tokens

**Correct approach:**
```markdown
# Project Name

[Only project-specific content here]
# User-level CLAUDE.md already provides model selection
```

### Anti-Pattern 2: Project-Specific Rules at User Level

**Problem:**
```markdown
## Project Structure [in ~/.claude/CLAUDE.md]

- Place all test files in 'test-ground' folder at root
```

**Why this is bad:**
- Forces all projects to use this structure
- Not appropriate for all project types

**Correct approach:**
- Move to project-level CLAUDE.md
- Keep only universal preferences at user level

### Anti-Pattern 3: Vague References

**Problem:**
```markdown
- Follow project-specific CLAUDE.md in backend/ subdirectory
```

**Why this is bad:**
- Doesn't help discovery
- No indication what's in that file

**Correct approach:**
```markdown
- **Backend:** @backend/CLAUDE.md - FastAPI patterns, Burr workflows
```

### Anti-Pattern 4: "To Be Created" Markers

**Problem:**
```markdown
- `src/api/client.ts` - Axios instance (to be created)
```

**Why this is bad:**
- Creates uncertainty
- Claude may assume files exist

**Correct approach:**
```markdown
**Planned (Not Yet Implemented):**
- `src/api/client.ts` - Axios instance with httpOnly cookies
```

### Anti-Pattern 5: Missing Code Style

**Problem:**
- Commands documented but no code conventions
- Claude doesn't know project patterns

**Correct approach:**
- Always include import style, naming conventions, file organization

## Validation Checklist

Before committing CLAUDE.md, verify:

**Structure & Organization:**
- [ ] File is concise (<200 lines unless complex system requires more)
- [ ] Quick Reference section at top (for files >150 lines)
- [ ] Sections organized logically
- [ ] Subdirectory files referenced (monorepos only)

**Content Quality:**
- [ ] All commands include inline comments
- [ ] Critical rules use emphasis markers (IMPORTANT, ALWAYS, NEVER)
- [ ] Common pitfalls section with ❌/✅ examples
- [ ] Code examples included (not just prose)
- [ ] @ file references used for related docs

**Technical Accuracy:**
- [ ] No hardcoded secrets or credentials
- [ ] Environment variables clearly marked (required/optional)
- [ ] Tech stack versions specified
- [ ] No "to be created" markers

**Token Efficiency:**
- [ ] No verbose paragraphs (bullet points preferred)
- [ ] No redundant information
- [ ] No obvious explanations

**Security:**
- [ ] No API keys, passwords, or secrets
- [ ] Environment variable security noted
- [ ] Security practices documented if applicable

**Completeness:**
- [ ] Development commands included
- [ ] Testing commands included
- [ ] Project structure explained
- [ ] Code style guidelines present

**Hierarchy:**
- [ ] Project-specific content only (not duplicating user-level)
- [ ] References to subdirectory files (monorepos)

## Quick Tips

### Adding Memories During Sessions
- Press `#` key during conversation
- Select which CLAUDE.md file to update
- Claude will add it automatically

### Bootstrapping New Project
- Use `/init` command for auto-generation
- Provides starter template
- Customize based on project type

### Editing Memory Files
- Use `/memory` command
- Shows all applicable memory files
- Allows selection and editing

### Iterative Improvement
- Treat CLAUDE.md like any frequently used prompt
- Refine based on what works
- Remove outdated guidance
- Add new patterns as discovered
