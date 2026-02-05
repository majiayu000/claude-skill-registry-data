---
name: Codebase Analysis
description: This skill should be used when the user asks about "analyzing codebase", "understanding project structure", "code exploration", "architecture discovery", "codebase patterns", or needs to systematically analyze and document a codebase's organization and conventions.
version: 1.0.0
---

# Codebase Analysis Skill

This skill provides systematic approaches to analyzing and understanding codebases of any size and complexity.

## Analysis Strategy by Project Size

```
Small (<50 files):     Comprehensive scan of all files
Medium (50-500 files): Representative sampling per category
Large (>500 files):    Strategic sampling of key areas
```

## Parallel Analysis Tracks

Run these tracks concurrently for efficiency:

### Track 1: Product Understanding
```bash
# Files to examine:
- README.md, README*.md
- package.json "description" field
- docs/ or documentation/ folder
- Main entry points (index.ts, main.ts, app.ts)
- API documentation
```

### Track 2: Technical Stack Discovery
```bash
# Configuration files:
- package.json (dependencies, devDependencies, scripts)
- tsconfig.json / jsconfig.json
- Build configs: vite.config.*, webpack.config.*, rollup.config.*
- Test configs: jest.config.*, vitest.config.*
- Linter configs: .eslintrc.*, eslint.config.*
- Formatter configs: .prettierrc.*, prettier.config.*
```

### Track 3: Structure Mapping
```bash
# Analyze:
- Top-level directories (src/, lib/, packages/, apps/)
- 2-3 representative files per major directory
- Naming conventions (kebab-case, camelCase, PascalCase)
- Module organization patterns
- Index/barrel files
```

### Track 4: Convention Detection
```bash
# Patterns to identify:
- Export style: named vs default exports
- Component patterns: functional vs class, HOCs
- State management: Redux, Zustand, Context
- Testing patterns: unit, integration, e2e
- Error handling: try/catch, Result types, error boundaries
```

## Analysis Output Templates

### Package Analysis
```markdown
## Package: {name}

**Purpose**: {description}
**Type**: Library | Application | CLI | Framework
**Entry**: {main entry point}

### Dependencies
- Production: {count} packages
- Development: {count} packages
- Key deps: {list critical dependencies}

### Scripts
| Script | Command | Purpose |
|--------|---------|---------|
| dev | {cmd} | Development server |
| build | {cmd} | Production build |
| test | {cmd} | Run tests |
```

### Directory Analysis
```markdown
## Directory: {path}

**Purpose**: {description}
**Pattern**: {naming convention}
**File Count**: {count}

### Structure
{tree representation, 2-3 levels}

### Key Files
| File | Purpose |
|------|---------|
| {file} | {purpose} |
```

### Convention Analysis
```markdown
## Detected Conventions

### Confirmed Patterns
- {Pattern}: {evidence} (found in X% of files)

### Inconsistencies
⚠️ {Pattern}: {variant1} ({X%}) vs {variant2} ({Y%})
   Recommendation: Standardize on {recommended}
```

## Monorepo Analysis

For monorepos (pnpm workspaces, yarn workspaces, nx, turborepo):

```markdown
## Monorepo Structure

### Workspace Configuration
- Tool: {pnpm/yarn/npm/nx/turborepo}
- Config: {workspace config file}

### Packages
| Package | Type | Dependencies |
|---------|------|--------------|
| {name} | {lib/app} | {internal deps} |

### Build Order
1. {package1} (no deps)
2. {package2} (depends on 1)
3. {package3} (depends on 1, 2)

### Shared Configuration
- TypeScript: {shared tsconfig}
- Testing: {shared test config}
- Linting: {shared lint config}
```

## Error Patterns to Flag

```markdown
## Issues Detected

### Critical
❌ {issue}: {description}
   Location: {file:line}
   Impact: {impact}

### Warning
⚠️ {issue}: {description}
   Location: {file:line}
   Recommendation: {fix}

### Info
ℹ️ {observation}
```

## Integration with Steering Workflow

When used during `/steering`:

1. **Phase 2** uses this skill for systematic codebase exploration
2. **Product track** extracts README and documentation
3. **Tech track** discovers dependencies and build tools
4. **Structure track** maps directories and patterns
5. **Convention track** identifies code style rules

## Best Practices

1. **Sample Strategically**: Don't read every file; pick representative samples
2. **Parallel Execution**: Run independent analyses concurrently
3. **Evidence-Based**: Document where patterns were observed
4. **Mark Uncertainty**: Use ⚠️ for unclear or conflicting patterns
5. **Actionable Output**: Focus on patterns AI agents need to follow
