---
name: scaffold-library
description: Setup library project structure with src, build config, exports, and tests
type: scaffold
project_types: [library]
trigger: "create library, setup package, init library"
inputs:
  - name: name
    description: Library/package name
    required: true
  - name: runtime
    description: Target runtime (node, browser, universal)
    required: false
    default: "universal"
  - name: format
    description: Output format (esm, cjs, both)
    required: false
    default: "both"
---

## Context

You will create a library "{{input.name}}" targeting {{input.runtime}}.
Output format: {{input.format}}.

## Instructions

1. **Setup package.json**
   - name, version, description, license
   - main (CJS), module (ESM), types
   - exports field for dual package
   - scripts: build, test, lint, prepublishOnly
   - peerDependencies (not dependencies) for shared libs

2. **Setup TypeScript config**
   - `tsconfig.json` for source
   - `tsconfig.build.json` for build output
   - Strict mode enabled
   - Declaration files enabled

3. **Setup build tool**
   - tsup or unbuild (simple, near-zero-config)
   - Config for ESM + CJS output
   - Source maps
   - DTS generation

4. **Create source structure**
   ```
   src/
   ├── index.ts          # Public API exports
   ├── types.ts           # Shared types
   └── [modules]/         # Feature modules
   ```

5. **Setup testing**
   - Vitest config
   - Example test file
   - Coverage config

6. **Setup linting**
   - ESLint config (if not already present)
   - Prettier config (if not already present)

7. **Create README stub**
   - Installation
   - Quick start
   - API reference placeholder

8. **Setup CI** (if jonggrang.json ci.provider != none)
   - Build + test on PR
   - Publish on tag/release

## Script

```bash
#!/bin/bash
# Initialize if no package.json
if [ ! -f "package.json" ]; then
  npm init -y
fi

# Install dev dependencies
npm install -D typescript tsup vitest @types/node
```

## Validation

- [ ] `npm run build` succeeds
- [ ] `npm run test` passes
- [ ] Output files generated (dist/)
- [ ] Types generated (.d.ts)
- [ ] ESM import works
- [ ] CJS require works (if format includes cjs)
- [ ] Exports field correct in package.json
