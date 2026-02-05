---
name: turbo
description: Turborepo monorepo build system with task pipelines, caching, and package management. Triggers on turbo, turbo.json, monorepo.
triggers: ["turbo", "turbo\\.json", "monorepo", "workspace"]
---

<objective>
Configure Turborepo for efficient monorepo builds with task pipelines, remote caching, and proper package dependencies.
</objective>

<mcp_first>
**CRITICAL: Always fetch Turborepo documentation for current configuration.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_context7__query-docs" })
```

```typescript
// Task configuration
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/vercel/turborepo",
  topic: "tasks dependsOn outputs inputs"
})

// Caching
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/vercel/turborepo",
  topic: "cache outputs remote caching"
})

// Filtering
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/vercel/turborepo",
  topic: "filter workspace package"
})
```
</mcp_first>

<quick_start>
**turbo.json:**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**Key concepts:**

- `^build` - Run `build` in dependencies first
- `outputs` - Files to cache
- `inputs` - Files that affect cache key
- `cache: false` - Disable caching for dev tasks
- `persistent: true` - Long-running tasks
</quick_start>

<task_patterns>
**Build pipeline:**

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "inputs": ["src/**", "package.json", "tsconfig.json"]
    }
  }
}
```

**Test after build:**

```json
{
  "tasks": {
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

**Parallel independent tasks:**

```json
{
  "tasks": {
    "lint": {
      "outputs": []
    },
    "typecheck": {
      "outputs": []
    }
  }
}
```
</task_patterns>

<commands>
```bash
turbo build                    # Build all packages
turbo build --filter=@org/app  # Build specific package
turbo build --filter=./apps/*  # Build apps only
turbo build --filter=...@org/lib  # Package and dependents
turbo build --force            # Ignore cache
turbo build --dry-run          # Preview what will run
```
</commands>

<constraints>
**Required:**
- Define `outputs` for cacheable tasks
- Use `^` prefix for dependency ordering
- Set `cache: false` for dev tasks
- Use `persistent: true` for long-running tasks

**Best practices:**
- Keep `inputs` specific to avoid cache misses
- Use workspace filters for targeted builds
- Enable remote caching for CI
</constraints>

<success_criteria>
- [ ] Context7 docs fetched for current config
- [ ] Tasks have proper `dependsOn`
- [ ] `outputs` defined for cacheable tasks
- [ ] Dev tasks have `cache: false`
- [ ] Pipeline is efficient (parallel where possible)
</success_criteria>
