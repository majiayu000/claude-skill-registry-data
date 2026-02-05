---
name: tsconfig-builder
description: Generate properly configured tsconfig.json files for TypeScript projects with appropriate compiler options for various project types. Triggers on "create tsconfig", "generate tsconfig.json", "typescript config for", "configure TypeScript".
---

# TSConfig Builder

Generate properly configured `tsconfig.json` files optimized for various TypeScript project types.

## Output Requirements

**File Output:** `tsconfig.json`
**Format:** Valid JSON with comments (JSONC)
**Compatibility:** TypeScript 5.x

## When Invoked

Immediately generate a complete `tsconfig.json` appropriate for the project type. Include comments explaining key options.

## Project Type Templates

### Node.js Backend (ES Modules)
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    // Language and Environment
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    // Output
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "resolveJsonModule": true,
    "isolatedModules": true,

    // Paths (optional)
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },

    // Skip type checking of node_modules
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Node.js Backend (CommonJS)
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "CommonJS",
    "moduleResolution": "Node",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### React Application (Vite)
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    // Bundler mode
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    // Strictness
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    // Paths
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Next.js Application
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts"
  ],
  "exclude": ["node_modules"]
}
```

### NPM Library Package
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    // Targets both CJS and ESM consumers
    "target": "ES2020",
    "lib": ["ES2020"],
    "module": "ESNext",
    "moduleResolution": "bundler",

    // Output
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationDir": "./dist",
    "declarationMap": true,
    "sourceMap": true,

    // Strictness (libraries should be strict)
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "skipLibCheck": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Monorepo Base Config
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "declaration": true,
    "declarationMap": true,
    "composite": true
  }
}
```

### Monorepo Package Config
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "composite": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"],
  "references": [
    { "path": "../shared" }
  ]
}
```

### Express API Server
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": false,
    "sourceMap": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@controllers/*": ["./src/controllers/*"],
      "@models/*": ["./src/models/*"],
      "@middleware/*": ["./src/middleware/*"],
      "@routes/*": ["./src/routes/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### CLI Tool
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true,
    // Important for CLI tools
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## Key Compiler Options Reference

### Module Systems
| Option | Use Case |
|--------|----------|
| `NodeNext` | Node.js with ESM support |
| `CommonJS` | Traditional Node.js |
| `ESNext` | Bundler (Vite, webpack) |
| `bundler` | Modern bundler resolution |

### Strictness Options
```json
{
  "strict": true,                          // Enable all strict checks
  "noUncheckedIndexedAccess": true,        // Add undefined to index signatures
  "noImplicitOverride": true,              // Require override keyword
  "noPropertyAccessFromIndexSignature": true, // Require bracket notation for index signatures
  "exactOptionalPropertyTypes": true,      // Distinguish undefined from optional
  "noFallthroughCasesInSwitch": true,      // Error on switch fallthrough
  "noImplicitReturns": true,               // Require return in all paths
  "noUnusedLocals": true,                  // Error on unused variables
  "noUnusedParameters": true               // Error on unused parameters
}
```

### Path Aliases
```json
{
  "baseUrl": ".",
  "paths": {
    "@/*": ["./src/*"],
    "@components/*": ["./src/components/*"],
    "~/*": ["./"]
  }
}
```

## Validation Checklist

Before outputting, verify:
- [ ] `$schema` property for IDE support
- [ ] `target` and `lib` are consistent
- [ ] `module` and `moduleResolution` are compatible
- [ ] `strict` is enabled (unless specific reason)
- [ ] `include` and `exclude` are set
- [ ] `outDir` specified if emitting
- [ ] Path aliases match project structure
- [ ] Comments explain non-obvious options

## Example Invocations

**Prompt:** "Create tsconfig for a React TypeScript project with Vite"
**Output:** Complete `tsconfig.json` with JSX support, bundler resolution, strict mode.

**Prompt:** "Generate tsconfig for Node.js Express API"
**Output:** Complete `tsconfig.json` with NodeNext module, path aliases, strict options.

**Prompt:** "TSConfig for publishable npm library"
**Output:** Complete `tsconfig.json` with declaration output, ES module target, strict settings.
