---
name: turbo-config
description: Turbo.json configuration template and validation logic for Turborepo tasks. Use when creating or auditing turbo.json files to ensure correct task configuration, caching strategy, and the 7 required MetaSaver standards (schema, globalEnv, globalDependencies, required tasks by repo type, build requirements, persistent task cache, clean task cache).
---

# Turbo.json Configuration Skill

Provides turbo.json template and validation logic for Turborepo task configuration.

## Purpose

Manage turbo.json configuration to:

- Define monorepo build tasks
- Configure task dependencies and caching
- Set up persistent development servers
- Optimize build performance

## Template

The standard Turbo.json template is located at:

```
templates/turbo.template.json
```

## The 7 Turbo.json Standards

### Rule 1: $schema Reference

Must include Turborepo schema for IDE support:

```json
{
  "$schema": "https://turbo.build/schema.json"
}
```

### Rule 2: globalEnv Variables

Must declare environment variables available to all tasks:

```json
{
  "globalEnv": ["NODE_ENV", "CI"]
}
```

### Rule 3: globalDependencies

Must declare files that invalidate all task caches:

```json
{
  "globalDependencies": ["**/.env.*local", ".env"]
}
```

### Rule 4: Required Tasks (by repository type)

**Consumer Repos** (apps like metasaver-com, rugby-crm, resume-builder) require **15 tasks**:

- **Build**: `build`, `clean`
- **Development**: `dev`
- **Linting**: `lint`, `lint:fix`, `lint:tsc`
- **Formatting**: `prettier`, `prettier:fix`
- **Testing**: `test:unit`, `test:coverage`, `test:watch`
- **Database**: `db:generate`, `db:migrate`, `db:seed`, `db:studio`

**Library Repos** (producers like multi-mono) require **11 tasks**:

- **Build**: `build`, `clean`
- **Development**: `dev`
- **Linting**: `lint`, `lint:fix`, `lint:tsc`
- **Formatting**: `prettier`, `prettier:fix`
- **Testing**: `test:unit`, `test:coverage`, `test:watch`

Library repos do NOT require `db:*` tasks.

### Rule 5: Build Task Requirements

The `build` task must have:

```json
{
  "build": {
    "dependsOn": ["^build"],
    "env": ["NODE_ENV"],
    "outputs": ["dist/**", "build/**", ".next/**"]
  }
}
```

### Rule 6: Persistent Task Cache Config

Development and studio tasks must disable cache:

```json
{
  "dev": {
    "cache": false,
    "persistent": true
  },
  "db:studio": {
    "cache": false,
    "persistent": true
  }
}
```

### Rule 7: Clean Task Cache Disabled

The `clean` task must not cache:

```json
{
  "clean": {
    "cache": false
  }
}
```

## Validation

To validate a turbo.json file:

1. Check that file exists at repository root
2. Parse JSON and extract configuration
3. Verify $schema reference
4. Check globalEnv and globalDependencies
5. Verify required tasks exist (based on repo type)
6. Check build task configuration
7. Verify persistent tasks have cache: false
8. Report violations

### Validation Approach

```javascript
// Rule 1: Check schema
if (!config.$schema || !config.$schema.includes("turbo.build")) {
  errors.push("Rule 1: Missing or incorrect $schema reference");
}

// Rule 2: Check globalEnv
const requiredEnv = ["NODE_ENV", "CI"];
const missingEnv = requiredEnv.filter((e) => !config.globalEnv?.includes(e));
if (missingEnv.length > 0) {
  errors.push(`Rule 2: globalEnv missing: ${missingEnv.join(", ")}`);
}

// Rule 3: Check globalDependencies
const requiredDeps = [".env"];
const missingDeps = requiredDeps.filter(
  (d) => !config.globalDependencies?.some((dep) => dep.includes(d)),
);

// Rule 4: Check required tasks (Turborepo v2 uses "tasks" not "pipeline")
const baseTasks = [
  "build",
  "clean",
  "dev",
  "lint",
  "lint:fix",
  "lint:tsc",
  "prettier",
  "prettier:fix",
  "test:unit",
  "test:coverage",
  "test:watch",
];
const dbTasks = ["db:generate", "db:migrate", "db:seed", "db:studio"];

// Library repos: 11 tasks (baseTasks only)
// Consumer repos: 15 tasks (baseTasks + dbTasks)
const requiredTasks = isLibraryRepo ? baseTasks : [...baseTasks, ...dbTasks];

const missingTasks = requiredTasks.filter((t) => !config.tasks?.[t]);
if (missingTasks.length > 0) {
  errors.push(`Rule 4: Missing required tasks: ${missingTasks.join(", ")}`);
}

// Rule 5: Check build task requirements
const buildTask = config.tasks?.build;
if (!buildTask?.dependsOn?.includes("^build")) {
  errors.push("Rule 5: build must depend on ^build");
}
if (!buildTask?.outputs || buildTask.outputs.length === 0) {
  errors.push("Rule 5: build must have outputs defined");
}

// Rule 6: Check persistent tasks
const persistentTasks = isLibraryRepo ? ["dev"] : ["dev", "db:studio"];
persistentTasks.forEach((task) => {
  const taskConfig = config.tasks?.[task];
  if (taskConfig?.cache !== false) {
    errors.push(`Rule 6: ${task} must have cache: false`);
  }
  if (taskConfig?.persistent !== true) {
    errors.push(`Rule 6: ${task} must have persistent: true`);
  }
});

// Rule 7: Check clean task
if (config.tasks?.clean?.cache !== false) {
  errors.push("Rule 7: clean must have cache: false");
}
```

## Repository Type Considerations

| Repo Type    | Examples                                 | Required Tasks | db:\* Tasks  |
| ------------ | ---------------------------------------- | -------------- | ------------ |
| **Consumer** | metasaver-com, rugby-crm, resume-builder | 15             | Required     |
| **Library**  | multi-mono                               | 11             | Not required |

**Determining repo type:**

- Use `/skill scope-check` to identify repository type
- Consumer repos are applications that consume database services
- Library repos are package producers without database dependencies

## Best Practices

1. Place turbo.json at repository root only
2. Use template as starting point
3. Use `tasks` property (Turborepo v2), not `pipeline` (v1 deprecated)
4. Persistent tasks must disable cache
5. Build outputs must be specified for caching
6. Environment variables in globalEnv for all tasks
7. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `package-scripts-agent` - Ensure npm scripts match turbo tasks
