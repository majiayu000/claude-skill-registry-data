---
name: typescript-configuration
description: TypeScript configuration (tsconfig.json) for MetaSaver projects with no-barrel architecture support. Use when creating or auditing tsconfig.json files to ensure proper path aliases (baseUrl, paths with #/* mapping), compiler options, and module resolution for direct module imports.
---

# TypeScript Configuration Skill

Provides tsconfig.json validation logic for TypeScript configuration with no-barrel architecture support.

## Purpose

Configure TypeScript compiler options, path aliases, and module resolution to support:

- Direct module imports via `#/*` path alias
- Proper baseUrl and paths configuration
- Type checking and compilation settings
- Module resolution for ESM

## The 5 TypeScript Configuration Standards

| Rule | Requirement              | Details                                                      |
| ---- | ------------------------ | ------------------------------------------------------------ |
| 1    | Compiler options         | target: "ES2022", module: "ESNext", moduleResolution: "node" |
| 2    | Path alias configuration | baseUrl: ".", paths with "#/_": ["./src/_"]                  |
| 3    | Type generation          | declaration: true, declarationMap: true                      |
| 4    | Strict mode              | strict: true                                                 |
| 5    | Output configuration     | outDir: "./dist", rootDir: "./src"                           |

### Rule 1: Compiler Options

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Rule 2: Path Alias Configuration (No-Barrel Architecture)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "#/*": ["./src/*"]
    }
  }
}
```

**Critical**: `baseUrl` MUST be present when using `paths`. The `#/*` alias enables direct module imports without barrel files.

### Rule 3: Type Generation

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true
  }
}
```

### Rule 4: Strict Mode

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### Rule 5: Output Configuration

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

## Validation

Validation checks (pseudo-code):

```typescript
// Rule 1: Compiler options
validate(config.compilerOptions?.target === "ES2022");
validate(config.compilerOptions?.module === "ESNext");
validate(config.compilerOptions?.moduleResolution === "node");

// Rule 2: Path alias configuration (No-Barrel Architecture)
if (config.compilerOptions?.paths) {
  if (!config.compilerOptions?.baseUrl) {
    errors.push("Rule 2: baseUrl must be present when using paths");
  }
  if (!config.compilerOptions?.paths?.["#/*"]) {
    errors.push("Rule 2: Missing paths['#/*'] for no-barrel imports");
  } else {
    const pathMapping = config.compilerOptions.paths["#/*"];
    if (!Array.isArray(pathMapping) || pathMapping[0] !== "./src/*") {
      errors.push("Rule 2: paths['#/*'] must point to ['./src/*']");
    }
  }
}

// Rule 3: Type generation
validate(config.compilerOptions?.declaration === true);
validate(config.compilerOptions?.declarationMap === true);

// Rule 4: Strict mode
validate(config.compilerOptions?.strict === true);

// Rule 5: Output configuration
validate(config.compilerOptions?.outDir === "./dist");
validate(config.compilerOptions?.rootDir === "./src");
```

## Common Violations

| Violation                 | Issue                               | Remediation                                     |
| ------------------------- | ----------------------------------- | ----------------------------------------------- |
| Missing baseUrl           | paths defined without baseUrl       | Add "baseUrl": "." to compilerOptions           |
| Missing #/\* path mapping | No path alias for no-barrel imports | Add "paths": { "#/_": ["./src/_"] }             |
| Incorrect path mapping    | #/\* points to wrong directory      | Update paths["#/*"] to ["./src/*"]              |
| Missing declaration       | No type generation configured       | Add "declaration": true, "declarationMap": true |
| Non-strict mode           | TypeScript not in strict mode       | Add "strict": true                              |

## Best Practices

1. Always set `baseUrl` when using `paths`
2. Use `#/*` alias for no-barrel architecture
3. Enable strict mode for type safety
4. Generate declaration files for library packages
5. Re-audit after making changes

## Integration

- Repository type: Use `/skill scope-check` if not provided
- Workflow: `/skill audit-workflow`
- Remediation: `/skill remediation-options`
- Related: `root-package-json-config`, `vitest-config`, `vite-config`
