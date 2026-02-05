---
name: vite-config
description: Vite configuration templates and validation logic for React web apps. Includes 5 required standards (correct plugins for React, required path alias #src to ./src, build configuration with sourcemaps and manual chunks, server configuration with strictPort, required dependencies). Use when creating or auditing vite.config.ts files.
---

# Vite Configuration Skill

This skill provides vite.config.ts templates and validation logic for Vite build configuration.

## Purpose

Manage vite.config.ts configuration to:

- Configure correct plugins for React projects
- Set up path aliases and build options
- Configure development server settings

## Usage

This skill is invoked by the `vite-agent` when:

- Creating new vite.config.ts files
- Auditing existing Vite configurations
- Validating Vite configs against standards

## Templates

Standard templates are located at:

```
templates/vite-standalone.template.ts      # React web apps
```

## The 5 Vite Standards

### Rule 1: Correct Plugins for React Projects

All React projects must have:

- `@vitejs/plugin-react`

### Rule 2: Required Path Alias

Must include `#src` alias pointing to `./src`:

```typescript
resolve: {
  alias: {
    '#src': path.resolve(__dirname, './src'),
  },
}
```

### Rule 3: Required Build Configuration

Must include:

```typescript
build: {
  outDir: 'dist',
  sourcemap: true,
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom'],
      },
    },
  },
}
```

### Rule 4: Required Server Configuration

Must include:

```typescript
server: {
  port: 5173,  // Or assigned port from registry
  strictPort: true,
  host: true,
}
```

### Rule 5: Required Dependencies

Must have in package.json devDependencies:

- `vite`
- `@vitejs/plugin-react`

## Validation

To validate a vite.config.ts file:

1. Read package.json to get `metasaver.projectType`
2. Check that vite.config.ts exists
3. Parse config and check plugins array
4. Verify path alias configuration
5. Check build and server configuration
6. Verify required dependencies
7. Report violations

### Validation Approach

```typescript
// Rule 1: Check plugins for React
const hasReact = plugins.some((p) => p.name.includes("vite:react"));
if (!hasReact) {
  errors.push("Rule 1: Missing @vitejs/plugin-react");
}

// Rule 2: Check path alias
if (!config.resolve?.alias?.["#src"]) {
  errors.push("Rule 2: Missing path alias '#src' → './src'");
}

// Rule 3: Check build configuration
if (!config.build?.outDir) {
  errors.push("Rule 3: Missing build.outDir");
}
if (!config.build?.sourcemap) {
  errors.push("Rule 3: Missing build.sourcemap");
}

// Rule 4: Check server configuration
if (!config.server?.port) {
  errors.push("Rule 4: Server port not set");
}
if (config.server?.strictPort !== true) {
  errors.push("Rule 4: Server strictPort must be true");
}

// Rule 5: Check dependencies
const deps = packageJson.devDependencies || {};
if (!deps.vite) errors.push("Rule 5: Missing vite in devDependencies");
if (!deps["@vitejs/plugin-react"]) {
  errors.push("Rule 5: Missing @vitejs/plugin-react in devDependencies");
}
```

## Project Type Detection

Extract from package.json:

```json
{
  "metasaver": {
    "projectType": "web-standalone"
  }
}
```

## Port Registry

Check package.json for assigned port:

```json
{
  "metasaver": {
    "port": 5173
  }
}
```

## Repository Type Considerations

- **Consumer Repos**: Must strictly follow all 5 standards unless exception declared
- **Library Repos**: May have custom Vite config for component library builds

### Exception Declaration

Consumer repos may declare exceptions in package.json:

```json
{
  "metasaver": {
    "exceptions": {
      "vite-config": {
        "type": "custom-build-plugins",
        "reason": "Requires vite-plugin-svg-icons for icon generation"
      }
    }
  }
}
```

## Best Practices

1. Place vite.config.ts at workspace root (where package.json is)
2. Use standalone template for React projects
3. Path alias must match tsconfig.json paths
4. Port must be unique across monorepo
5. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `typescript-agent` - Ensure path aliases match tsconfig.json
- `package-scripts-agent` - Ensure dev/build scripts exist
