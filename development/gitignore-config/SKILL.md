---
name: gitignore-config
description: Git ignore configuration patterns for MetaSaver monorepos. Includes 10 required pattern categories (dependencies, build outputs, environment files with security-critical .env and .npmrc exclusions, logs, testing, IDE, OS, database, cache, temporary files). Use when creating or auditing .gitignore files to prevent secret leakage and repository pollution.
---

# Gitignore Configuration Skill

This skill provides the canonical .gitignore patterns for MetaSaver monorepos.

## Required Pattern Categories

### 1. Dependencies

```gitignore
# Dependencies
node_modules
.pnpm-store
.yarn
.npm
```

### 2. Build Outputs

```gitignore
# Build outputs
dist
build
out
.turbo
.next
*.tsbuildinfo
```

### 3. Environment Files (CRITICAL - Security)

```gitignore
# Environment files - CRITICAL: prevent secret leakage
.env
.env.*
!.env.example
!.env.template

# NPM configuration - may contain auth tokens
.npmrc
!.npmrc.template
```

### 4. Logs

```gitignore
# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*
```

### 5. Testing and Coverage

```gitignore
# Testing
coverage
.nyc_output
test-results
playwright-report
```

### 6. IDE and Editor

```gitignore
# IDE/Editor (note: .vscode often committed, exclude only if needed)
.idea
*.swp
*.swo
*~
*.sublime-workspace
```

### 7. Operating System

```gitignore
# OS files
.DS_Store
Thumbs.db
desktop.ini
```

### 8. Database (Prisma/SQLite)

```gitignore
# Database
*.db
*.db-journal
```

### 9. Cache

```gitignore
# Cache
.cache
.eslintcache
.stylelintcache
*.cache
```

### 10. Temporary Files

```gitignore
# Temporary
tmp
temp
*.tmp
*.temp
```

## Complete Template

```gitignore
# ========================================
# Dependencies
# ========================================
node_modules
.pnpm-store
.yarn
.npm
jspm_packages

# ========================================
# Build outputs
# ========================================
dist
build
out
.turbo
.next
.nuxt
.cache
.parcel-cache
*.tsbuildinfo

# ========================================
# Environment files - SECURITY CRITICAL
# ========================================
.env
.env.*
!.env.example
!.env.template
.npmrc
!.npmrc.template

# ========================================
# Logs
# ========================================
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# ========================================
# Testing and coverage
# ========================================
coverage
.nyc_output
test-results
playwright-report
*.lcov

# ========================================
# IDE and editor files
# ========================================
.idea
*.swp
*.swo
*~
*.sublime-workspace
.project
.classpath
.settings

# ========================================
# Operating system files
# ========================================
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# ========================================
# Database files
# ========================================
*.db
*.db-journal
*.sqlite
*.sqlite3

# ========================================
# Cache files
# ========================================
.cache
.eslintcache
.stylelintcache
.prettiercache
*.cache

# ========================================
# Temporary files
# ========================================
tmp
temp
*.tmp
*.temp
*.bak
*.backup
*.orig
```

## Validation Logic

```typescript
const REQUIRED_PATTERNS = {
  critical: [".env", ".env.*", "!.env.example", ".npmrc", "!.npmrc.template"],
  high: ["node_modules", "dist", "build", ".turbo", "*.log", "coverage"],
  medium: [".next", "out", ".cache", ".eslintcache", "*.tsbuildinfo"],
  low: [".DS_Store", "Thumbs.db", "desktop.ini", "*.db", "tmp"],
};

function validateGitignore(content: string): ValidationResult {
  const lines = content.split("\n").map((l) => l.trim());
  const violations = [];

  for (const [priority, patterns] of Object.entries(REQUIRED_PATTERNS)) {
    for (const pattern of patterns) {
      if (!lines.includes(pattern)) {
        violations.push({
          pattern,
          priority,
          message: `Missing ${priority} pattern: ${pattern}`,
        });
      }
    }
  }

  return {
    valid: violations.filter((v) => v.priority === "critical").length === 0,
    violations,
  };
}
```

## Best Practices

1. **Security First**: Always include .env and .npmrc exclusions with template whitelists
2. **Organized Structure**: Group patterns by category with clear comments
3. **No Duplicates**: Avoid redundant patterns
4. **Complete Coverage**: Don't miss any build output directories
5. **Cross-Platform**: Include both Unix and Windows OS-specific files
6. **Whitelist Templates**: Use `!` pattern to allow template files

## Consumer vs Library Repos

Both use the same patterns. The .gitignore is repository-agnostic - all monorepos need the same exclusions.

## Common Mistakes

1. **Forgetting .npmrc**: Auth tokens can leak
2. **Missing .turbo**: Turborepo cache pollutes repo
3. **No .env exclusion**: Secrets in version control
4. **Incomplete whitelists**: Template files get ignored
5. **Missing OS files**: .DS_Store creates noise in PRs
