---
name: creating-modules
description: Creates new modules within existing packages following project conventions. Handles file structure, barrel exports, namespace files, package.json imports/exports, and internal import patterns.
---

# Creating Modules

## Steps

1. **Create module directory**: `packages/<pkg>/src/<module-name>/`

2. **Create implementation files**: `<module-name>.ts` or split across multiple files

3. **Create barrel file** `__.ts`:
   ```typescript
   export * from './implementation.js'
   export type * from './types.js'
   ```

4. **Create namespace file** `_.ts`:
   ```typescript
   export * as ModuleName from './__.js'
   ```

5. **Add to package.json imports**:
   ```json
   {
     "imports": {
       "#module-name": "./build/module-name/_.js",
       "#module-name/*": "./build/module-name/*.js"
     }
   }
   ```

6. **Add to package.json exports**:
   ```json
   {
     "exports": {
       "./module-name": "./build/module-name/__.js"
     }
   }
   ```

7. **Sync tsconfig paths** (run `syncing-tsconfig-paths` skill script)

8. **Add to main exports** in `src/index.ts`:
   ```typescript
   export * from '#module-name'
   ```

## Reference

### Module Structure

```
src/module-name/
├── _.ts              # Namespace file - exports the namespace
├── _.test.ts         # Module tests
├── __.ts             # Barrel file - exports all functions/types
└── *.ts              # Implementation files
```

### Import System

Use `#` imports for internal module references within a package:

```typescript
// Correct - use # imports
import { Fn } from '#fn'
import { Obj } from '#obj'

// Incorrect - don't use relative or package imports internally
import { Fn } from '../fn/_.js'
import { Obj } from '@kitz/core/obj'
```

### Naming

- **Directory**: kebab-case (`group-by/`)
- **Namespace export**: PascalCase (`GroupBy`)
- **Functions**: camelCase, no namespace prefix (`by`, not `groupBy`)

## Notes

- Each package defines its own `#` imports in package.json
- Cross-package `#` imports are not valid - use package name imports
