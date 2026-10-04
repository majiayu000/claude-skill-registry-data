---
name: si
description: "Supernal Interface CLI for test generation, contract scanning,
  story system, and MCP setup. Use when: (1) scanning Next.js routes/components
  for contracts, (2) generating tests from @Tool decorators, (3)
  recording/validating story-based tests, (4) setting up MCP integration, (5)
  validating contracts. NOT for: task management (use sc), orchestration (use
  orch), or CLI/API generation patterns (use universal-command)."
---


# si - Supernal Interface CLI

Test generation, contract scanning, story-based testing, and MCP setup for web applications.

## Installation

```bash
npm install -g @supernal/interface
```

## Quick Reference

### Contract Generation & Scanning

```bash
# Scan Next.js pages → generate route contracts
si scan-routes
si scan-routes -p ./src/pages -o ./src/routes/Routes.ts
si scan-routes --framework nextjs --watch        # Watch mode
si scan-routes --git-commit                      # Auto-commit

# Scan components → generate name contracts (data-testid)
si scan-names
si scan-names -c ./src/components -o ./src/names/Components.ts
si scan-names --flat                             # Components.Header vs Header.submitButton

# iOS-specific scanning
si scan-ios-views      # SwiftUI views → component names
si scan-ios-routes     # SwiftUI navigation → route contracts
si scan-ios-names      # Swift accessibility identifiers
```

### Validation

```bash
si validate --all                    # Validate everything
si validate --routes <file>          # Validate route contracts
si validate --names <file>           # Validate name contracts
si validate --tools                  # Validate @Tool decorators
si validate --no-cache               # Force refresh

si validate-graph                    # Detect broken links, orphan routes
```

### Test Generation

```bash
# From @Tool decorators
si generate-tests
si generate-tests --tools src/tools/index.ts
si generate-tests --include-e2e      # Add Playwright E2E tests
si generate-tests -f jest            # Framework: jest (default)

# From Gherkin feature files
si generate-story-tests <path>       # Multi-platform test generation
```

### Story System (BDD Testing)

```bash
# Record story videos
si story record <story-file>         # Record .story.ts execution

# Test without video
si story test <feature-file>         # Run Gherkin scenarios

# Validate before running
si story validate <feature-file>     # Check syntax, steps, components

# List available steps
si story list-steps                  # Show allowed Gherkin patterns
si list-steps                        # Alias
```

### Testing Commands

```bash
# Graph-based testing (routes graph)
si test graph                        # All modes: visual, perf, a11y, SEO
si test graph --modes visual,performance
si test graph --start-url /dashboard

# Shortcuts
si test visual                       # Visual regression (screenshots)
si test performance                  # Core Web Vitals, Lighthouse
si test a11y                         # WCAG compliance (axe-core)

# Record test video
si test record <test-file>           # Playwright video capture
si record <test-file>                # Alias
```

### Project Setup

```bash
# Initialize in Next.js project
si init                              # Current directory
si init ./my-project                 # Specific directory
si init --scan-only                  # Report only, no generation
si init --inject                     # Inject data-testid into components
si init --migrate                    # Migrate imports to contracts
si init --dry-run                    # Preview changes
si init --revert                     # Restore from backups

# Route migration
si migrate-routes                    # Migrate hardcoded strings → Routes
```

### MCP Setup

```bash
# Fully automated MCP setup (zero manual steps)
si setup-mcp                         # Configure IDE + create server
si setup-mcp --force                 # Overwrite existing
si setup-mcp --skip-test             # Skip server startup test
si setup-mcp --manual                # Create files only, skip IDE config

# Claude Code integration
si setup-claude                      # Install skills + agents
```

### Utilities

```bash
si cache-tools <file>                # Cache @Tool decorators
si benchmark-cache                   # Test caching performance
si feedback                          # File GitHub issue
```

## Common Patterns

### New Project Setup

```bash
cd my-nextjs-project
si init
si scan-routes
si scan-names
si setup-mcp
```

### Pre-PR Validation

```bash
si validate --all
si test visual                       # Check for visual regressions
si test a11y                         # Accessibility compliance
```

### Story-Driven Development

```bash
# 1. Write Gherkin feature
echo 'Feature: Login
  Scenario: Valid credentials
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard' > login.feature

# 2. Validate
si story validate login.feature

# 3. Create story implementation (.story.ts)
# 4. Record demonstration
si story record login.story.ts

# 5. Generate tests
si generate-story-tests login.feature
```

### Contract-First Development

```bash
# Generate contracts from existing code
si scan-routes --git-commit
si scan-names --git-commit

# Validate contracts stay in sync
si validate --routes ./src/routes/Routes.ts
si validate --names ./src/names/Components.ts
```

## Integration with Other Tools

| Tool | Relationship |
|------|--------------|
| `sc` | Task management, project health — use sc for dev workflow |
| `orch` | Agent orchestration — si focuses on testing/contracts |
| `universal-command` | si uses universal-command pattern internally for CLI/API/MCP |

## Environment

- **Routes file**: `./src/routes/Routes.ts` (default)
- **Names file**: `./src/names/Components.ts` (default)
- **Tests output**: `./tests/generated/` (default)
- **Framework**: Next.js (default), React Router supported
