---
name: claude-md
description: Create and maintain CLAUDE.md files for Claude Code projects. Use when users want to create a new CLAUDE.md, improve an existing one, audit CLAUDE.md quality, set up Claude Code configuration for a repository, or optimize agent context for monorepos. Triggers on requests like "create CLAUDE.md", "improve my CLAUDE.md", "set up Claude Code", "optimize agent context", or "audit my project documentation for Claude".
---

# CLAUDE.md Skill

Create effective CLAUDE.md files that transform Claude Code from a general-purpose assistant into a specialized tool for specific codebases.

## Core Philosophy

CLAUDE.md is Claude Code's "constitution" - it provides persistent context automatically loaded at conversation start. Every token counts because CLAUDE.md competes for context window space with conversation history, file contents, and tool results.

**Golden Rule:** Document what Claude gets wrong, not everything Claude might need. Start small, expand based on friction.

## CLAUDE.md Hierarchy

Claude Code loads CLAUDE.md files from multiple locations (all are merged):

| Location | Purpose | Git Status |
|----------|---------|------------|
| `~/.claude/CLAUDE.md` | Personal preferences across all projects | N/A |
| `repo/CLAUDE.md` | Team-shared project context | Commit |
| `repo/CLAUDE.local.md` | Personal project overrides | .gitignore |
| `repo/subdir/CLAUDE.md` | Subdirectory-specific context (monorepos) | Commit |

## Creation Workflow

### 1. Analyze the Codebase

Before writing, understand what Claude will struggle with:

```bash
# Identify key files and structure
find . -maxdepth 3 -type f -name "*.md" | head -20
ls -la package.json pyproject.toml Makefile 2>/dev/null

# Check for existing documentation
cat README.md 2>/dev/null | head -50

# Identify build/test commands
grep -E "scripts|test|build|dev" package.json 2>/dev/null
```

### 2. Structure Template

Use this proven structure (adapt sections as needed):

```markdown
# CLAUDE.md

[One-line project description]

## Quick Start

```bash
[Package manager] install
[Dev command]
[Test command]
```

## Architecture

[2-3 sentences on structure, key patterns, main technologies]

### Key Directories
- `src/` - [purpose]
- `tests/` - [purpose]

## Code Standards

- [Style rule with example if non-obvious]
- [Critical pattern to follow]
- [Common mistake to avoid → correct approach]

## Critical Rules

**MUST:**
- [Non-negotiable requirement]

**MUST NOT:**
- [Common mistake that breaks things]

## Common Commands

| Command | Purpose |
|---------|---------|
| `cmd` | Description |
```

### 3. Content Priorities

Include (in order of importance):

1. **Build/test/lint commands** - What Claude types most often
2. **Critical gotchas** - Things that break silently or waste time
3. **Architecture overview** - How components connect
4. **Code patterns** - Non-obvious conventions
5. **Workflow rules** - Branch naming, commit format, PR process

Exclude:

- Information Claude already knows (language syntax, common libraries)
- Verbose explanations (prefer examples)
- Comprehensive API docs (link to them instead)
- Anything unchanged from project defaults

## Writing Guidelines

### Conciseness Patterns

**Bad (verbose):**
```markdown
When you are writing TypeScript code in this project, you should always 
make sure to use strict mode and avoid using the 'any' type because it 
defeats the purpose of TypeScript's type system.
```

**Good (concise):**
```markdown
- TypeScript strict mode - no `any` types
```

### Negative Rules Need Alternatives

**Bad:**
```markdown
- Never use npm
```

**Good:**
```markdown
- Use pnpm (not npm) - monorepo requires pnpm workspaces
```

### Reference External Docs (Don't Embed)

**Bad:**
```markdown
[500 lines of API documentation]
```

**Good:**
```markdown
For complex widget usage or FooBarError, see docs/widgets.md
```

### Emphasis for Critical Items

```markdown
**IMPORTANT:** RLS policies auto-filter by user_id - don't add redundant .eq('user_id', userId)
```

## Monorepo Strategy

For large codebases, use hierarchical CLAUDE.md files:

```
monorepo/
├── CLAUDE.md              # Shared: package manager, CI, overall arch
├── apps/
│   ├── web/CLAUDE.md      # Frontend-specific context
│   └── api/CLAUDE.md      # Backend-specific context
├── packages/
│   └── shared/CLAUDE.md   # Shared library context
```

**Root CLAUDE.md** should contain:
- Monorepo tooling (pnpm/nx/turborepo commands)
- Cross-package patterns
- CI/CD workflows
- Shared conventions

**Subdirectory CLAUDE.md** should contain:
- Package-specific commands
- Local testing patterns
- Package-specific gotchas

**Size targets:**
- Root: <500 lines, <10k words
- Subdirectories: <200 lines each
- Total loaded context: <15k tokens

## Quality Audit Checklist

Run this audit on existing CLAUDE.md files:

- [ ] **Actionable:** Every item helps Claude do something concrete
- [ ] **Non-obvious:** Excludes things Claude already knows
- [ ] **Current:** Reflects actual project state (not aspirational)
- [ ] **Tested:** Commands actually work when copied
- [ ] **Minimal:** Each line earns its token cost
- [ ] **Alternatives:** Every "don't" has a "do instead"
- [ ] **Scannable:** Uses tables/bullets, not paragraphs
- [ ] **Examples:** Critical patterns show code, not just describe

## Anti-Patterns to Fix

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Comprehensive manual | Context bloat | Keep <500 lines, link to docs |
| `@-file` references | Loads entire file at startup | Use path + "see X for Y" |
| Only negatives | Claude gets stuck | Add alternatives |
| Stale commands | Broken workflows | Test all commands |
| Obvious info | Wastes tokens | Remove if Claude knows it |
| No structure | Hard to scan | Use headers, tables, bullets |

## Iteration Workflow

CLAUDE.md improves through use:

1. **During coding:** Press `#` in Claude Code to add memories
2. **After sessions:** Review what Claude struggled with
3. **Add sparingly:** Only document repeated friction points
4. **Prune regularly:** Remove outdated or unused content

## Post-Task Maintenance

**After completing significant tasks, update CLAUDE.md:**

### What to Add

| Trigger | Add to CLAUDE.md |
|---------|------------------|
| Claude used wrong command | Correct command in Quick Start |
| Claude broke a pattern | Pattern in Code Standards |
| Claude missed a gotcha | Gotcha in Critical Rules |
| New workflow established | Steps in Common Commands |
| Documentation outdated | Updated paths/commands |

### What to Update

- **New dependencies** - Add install commands
- **New scripts** - Document in commands table
- **Architecture changes** - Update directory descriptions
- **Deprecated patterns** - Remove or mark as legacy

### Maintenance Checklist

After each significant task:

- [ ] Did Claude struggle with anything? → Document it
- [ ] Did I discover a new pattern? → Add to Code Standards
- [ ] Did commands change? → Update Quick Start
- [ ] Is anything now outdated? → Remove it

### Learn from Mistakes

When Claude makes errors:

```markdown
## Critical Rules

**MUST NOT:**
- Use `npm install` (breaks pnpm lockfile)  ← Added after Claude broke deps
- Import from `@/old-path` (migrated to `@/new-path`)  ← Added after refactor
```

**Golden Rule:** If you corrected Claude, future Claude should know too.

## Advanced Patterns

### Machine-Readable State

For complex projects, add parseable metadata:

```markdown
## Project State
<!-- machine-readable -->
Version: 1.2.0
Status: development
Last migration: 0016_search_analytics
```

### Conditional Workflows

```markdown
## Workflow

**Creating new feature?**
1. Create branch from main
2. Implement with tests
3. Run full suite before PR

**Fixing bug?**
1. Write failing test first
2. Implement fix
3. Verify only that test changes
```

### Performance Targets

```markdown
## Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Cold start | <200ms | Measure with `time cmd` |
| API p95 | <500ms | Check after changes |
```

## Output Requirements

When creating CLAUDE.md:

1. Analyze codebase first (don't guess structure)
2. Keep total length under 500 lines
3. Test all commands before including
4. Use markdown tables for reference data
5. Save to `/mnt/user-data/outputs/CLAUDE.md`

When auditing CLAUDE.md:

1. Report issues with specific line references
2. Provide concrete fixes, not vague suggestions
3. Prioritize by impact (token waste vs. broken workflows)