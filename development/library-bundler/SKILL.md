---
name: library-bundler
description: Configure build systems, optimize bundle size, manage exports for ESM/CJS/UMD, and publish packages to NPM with proper versioning
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Library Bundler

Expert skill for building, bundling, and publishing component libraries to NPM. Specializes in modern build tools (tsup, Vite, Rollup), bundle optimization, multi-format exports, and package publishing workflows.

## Core Capabilities

### 1. Build System Configuration
- **tsup**: Fast TypeScript bundler with zero config
- **Vite**: Modern build tool with HMR and optimization
- **Rollup**: Powerful module bundler for libraries
- **esbuild**: Extremely fast JavaScript bundler
- **Webpack**: Full-featured bundler (when needed)

### 2. Bundle Optimization
- Tree-shaking for dead code elimination
- Code splitting for optimal loading
- Minification (Terser, esbuild)
- Compression (gzip, brotli)
- Bundle size analysis
- Dependency externalization
- Chunk optimization

### 3. Multi-Format Support
- **ESM** (ES Modules): Modern standard
- **CJS** (CommonJS): Node.js compatibility
- **UMD** (Universal Module Definition): Browser globals
- **IIFE**: Self-executing browser bundles
- Dual package support (ESM + CJS)

### 4. TypeScript Integration
- Type declaration generation (.d.ts)
- Declaration maps for IDE navigation
- Type checking during build
- Multiple tsconfig.json support
- Path aliasing resolution

### 5. Package Publishing
- NPM registry publishing
- Semantic versioning (semver)
- Changelog generation
- Git tagging
- Pre-publish validation
- Scoped packages (@org/package)
- Package provenance

### 6. Development Workflow
- Watch mode for rapid iteration
- Source maps for debugging
- Hot Module Replacement (HMR)
- Build caching
- Parallel builds
- Incremental compilation

## Workflow

### Phase 1: Build Configuration Setup
1. **Analyze Project Structure**
   - Entry points (index.ts, components/)
   - Output formats needed (ESM, CJS, UMD)
   - External dependencies
   - Target environments (browsers, Node.js)

2. **Choose Build Tool**
   - **tsup**: Best for simple TS libraries
   - **Vite**: Best for modern ESM-first libraries
   - **Rollup**: Best for maximum control
   - **esbuild**: Best for raw speed

3. **Configure package.json**
   - Entry points (main, module, types, exports)
   - Build scripts
   - Files to include
   - Peer dependencies

### Phase 2: Optimization
1. **Tree-Shaking Setup**
   - Mark side effects in package.json
   - Use ESM imports/exports
   - Avoid namespace imports
   - Test tree-shaking effectiveness

2. **Bundle Size Analysis**
   - Use bundle analyzer tools
   - Identify large dependencies
   - Consider alternatives
   - Externalize heavy deps

3. **Code Splitting**
   - Split by route/feature
   - Shared chunk optimization
   - Dynamic imports where beneficial

### Phase 3: Publication Preparation
1. **Version Management**
   - Follow semantic versioning
   - Update package.json version
   - Create git tag
   - Generate changelog

2. **Pre-publish Checks**
   - Run tests
   - Build all formats
   - Verify type declarations
   - Check bundle sizes
   - Test in consuming projects

3. **Publish to NPM**
   - npm login
   - npm publish (or publish:dry-run)
   - Verify on npmjs.com
   - Test installation

## Build Tool Configurations

### tsup Configuration
```typescript
// tsup.config.ts
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  treeshake: true,
  minify: true,
  external: ['react', 'react-dom'],
  esbuildOptions(options) {
    options.banner = {
      js: '"use client"', // For React Server Components
    }
  },
})
```

### Vite Library Mode
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import dts from 'vite-plugin-dts'

export default defineConfig({
  plugins: [
    react(),
    dts({
      insertTypesEntry: true,
    }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLibrary',
      formats: ['es', 'cjs', 'umd'],
      fileName: (format) => `my-library.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    sourcemap: true,
    minify: 'esbuild',
  },
})
```

### Rollup Configuration
```typescript
// rollup.config.mjs
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import typescript from '@rollup/plugin-typescript'
import { terser } from 'rollup-plugin-terser'
import peerDepsExternal from 'rollup-plugin-peer-deps-external'
import postcss from 'rollup-plugin-postcss'

export default {
  input: 'src/index.ts',
  output: [
    {
      file: 'dist/index.cjs.js',
      format: 'cjs',
      sourcemap: true,
    },
    {
      file: 'dist/index.esm.js',
      format: 'esm',
      sourcemap: true,
    },
    {
      file: 'dist/index.umd.js',
      format: 'umd',
      name: 'MyLibrary',
      sourcemap: true,
      globals: {
        react: 'React',
        'react-dom': 'ReactDOM',
      },
    },
  ],
  plugins: [
    peerDepsExternal(),
    resolve(),
    commonjs(),
    typescript({
      tsconfig: './tsconfig.json',
      declaration: true,
      declarationDir: 'dist',
    }),
    postcss({
      extensions: ['.css'],
      minimize: true,
      inject: false,
      extract: 'styles.css',
    }),
    terser(),
  ],
  external: ['react', 'react-dom'],
}
```

## Package.json Configuration

### Modern Package.json (ESM-First)
```json
{
  "name": "@myorg/ui-library",
  "version": "1.0.0",
  "description": "Modern React component library",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./button": {
      "types": "./dist/button.d.ts",
      "import": "./dist/button.js",
      "require": "./dist/button.cjs"
    },
    "./package.json": "./package.json"
  },
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ],
  "sideEffects": false,
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "prepublishOnly": "npm run build && npm test",
    "publish:dry": "npm publish --dry-run"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "react": "^18.2.0",
    "tsup": "^8.0.0",
    "typescript": "^5.3.0"
  },
  "publishConfig": {
    "access": "public"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/myorg/ui-library"
  },
  "keywords": [
    "react",
    "components",
    "ui",
    "library"
  ],
  "author": "Your Name",
  "license": "MIT"
}
```

### Dual Package (ESM + CJS)
```json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  },
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts"
}
```

### Monorepo Package (Turborepo/Nx)
```json
{
  "name": "@myorg/ui-components",
  "private": false,
  "version": "1.0.0",
  "exports": {
    "./button": {
      "types": "./dist/button.d.ts",
      "import": "./dist/button.js"
    },
    "./input": {
      "types": "./dist/input.d.ts",
      "import": "./dist/input.js"
    }
  },
  "typesVersions": {
    "*": {
      "button": ["./dist/button.d.ts"],
      "input": ["./dist/input.d.ts"]
    }
  }
}
```

## TypeScript Configuration

### Library tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "removeComments": true,
    "strict": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.test.tsx"]
}
```

## Optimization Strategies

### 1. Tree-Shaking Optimization
```json
// package.json
{
  "sideEffects": false
}

// Or specify files with side effects
{
  "sideEffects": ["*.css", "*.scss"]
}
```

```typescript
// Use named exports (tree-shakeable)
export { Button } from './Button'
export { Input } from './Input'

// Avoid default exports for libraries
// ❌ export default { Button, Input }
```

### 2. Code Splitting Strategy
```typescript
// tsup.config.ts
export default defineConfig({
  entry: {
    index: 'src/index.ts',
    button: 'src/components/Button/index.ts',
    input: 'src/components/Input/index.ts',
  },
  format: ['esm', 'cjs'],
  splitting: true, // Enable code splitting
  dts: true,
})
```

### 3. Bundle Size Analysis
```bash
# Install bundle analyzer
npm install -D rollup-plugin-visualizer

# Add to rollup config
import { visualizer } from 'rollup-plugin-visualizer'

plugins: [
  visualizer({
    filename: './dist/stats.html',
    open: true,
  }),
]
```

### 4. External Dependencies
```typescript
// Don't bundle these (keep as peerDependencies)
external: [
  'react',
  'react-dom',
  'framer-motion',
  '@radix-ui/react-*',
]

// Regex pattern for dynamic externals
external: (id) => {
  return /^react/.test(id) || /^@radix-ui/.test(id)
}
```

### 5. Minification Options
```typescript
// esbuild (fastest)
minify: true

// Terser (best compression)
import { terser } from 'rollup-plugin-terser'

plugins: [
  terser({
    compress: {
      drop_console: true,
      drop_debugger: true,
    },
    format: {
      comments: false,
    },
  }),
]
```

## Publishing Workflow

### 1. Semantic Versioning
```bash
# Patch: Bug fixes (1.0.0 → 1.0.1)
npm version patch

# Minor: New features, backwards compatible (1.0.0 → 1.1.0)
npm version minor

# Major: Breaking changes (1.0.0 → 2.0.0)
npm version major

# Pre-release
npm version prerelease --preid=beta
# 1.0.0 → 1.0.1-beta.0
```

### 2. Changelog Generation
```bash
# Install conventional-changelog
npm install -D conventional-changelog-cli

# Generate changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

### 3. Pre-publish Script
```json
{
  "scripts": {
    "prepublishOnly": "npm run lint && npm test && npm run build",
    "prepack": "cp README.md LICENSE dist/"
  }
}
```

### 4. Publishing Commands
```bash
# Dry run (test without publishing)
npm publish --dry-run

# Publish to npm
npm publish

# Publish scoped package
npm publish --access public

# Publish with tag
npm publish --tag beta

# Publish specific folder
cd dist && npm publish
```

### 5. NPM Provenance (Recommended)
```bash
# Publish with provenance (requires GitHub Actions)
npm publish --provenance
```

### 6. GitHub Actions for Publishing
```yaml
# .github/workflows/publish.yml
name: Publish Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm test
      - run: npm run build
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Build Scripts

### Development Scripts
```json
{
  "scripts": {
    "dev": "tsup --watch",
    "build": "tsup",
    "build:analyze": "tsup && rollup-plugin-visualizer",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist"
  }
}
```

### CI/CD Scripts
```json
{
  "scripts": {
    "ci:build": "npm run clean && npm run build",
    "ci:test": "npm run type-check && npm test",
    "ci:publish": "npm run ci:test && npm run ci:build && npm publish"
  }
}
```

## Testing Build Output

### 1. Local Testing
```bash
# Create tarball
npm pack

# Install in test project
cd ../test-project
npm install ../my-library/my-library-1.0.0.tgz
```

### 2. Link for Development
```bash
# In library
npm link

# In consuming project
npm link my-library
```

### 3. Verify Exports
```typescript
// test.mjs
import * as lib from 'my-library'
console.log(Object.keys(lib))

// test.cjs
const lib = require('my-library')
console.log(Object.keys(lib))
```

## Monorepo Considerations

### Turborepo Configuration
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Workspace Package
```json
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}

// apps/docs/package.json
{
  "dependencies": {
    "@myorg/ui": "workspace:*"
  }
}
```

## Best Practices

### Package Design
1. **ESM-First**: Modern standard, better tree-shaking
2. **Dual Package**: Provide both ESM and CJS for compatibility
3. **Explicit Exports**: Use exports field for better control
4. **Tree-Shakeable**: Mark side effects, use named exports
5. **Small Bundles**: Externalize dependencies, optimize code

### Build Configuration
1. **Source Maps**: Always generate for debugging
2. **Type Declarations**: Essential for TypeScript users
3. **Declaration Maps**: Enable IDE navigation
4. **Minification**: For production builds
5. **Clean Output**: Clear dist/ before building

### Publishing
1. **Semantic Versioning**: Follow strictly
2. **Changelog**: Document all changes
3. **Git Tags**: Tag releases
4. **Pre-publish Tests**: Run comprehensive checks
5. **Provenance**: Use for supply chain security

### Performance
1. **Bundle Size**: Keep minimal
2. **Code Splitting**: Split by feature
3. **Tree-Shaking**: Maximize dead code elimination
4. **Compression**: Use gzip/brotli
5. **Lazy Loading**: Dynamic imports where beneficial

## Troubleshooting

### Common Issues

**Dual Package Hazard**
```typescript
// Ensure consistent resolution
// Use exports field properly
{
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  }
}
```

**Missing Type Declarations**
```typescript
// Check tsconfig.json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true
  }
}

// Check package.json
{
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts"
    }
  }
}
```

**Large Bundle Size**
```bash
# Analyze bundle
npm run build:analyze

# Check for duplicate dependencies
npm dedupe

# Externalize peer dependencies
external: ['react', 'react-dom']
```

**CJS/ESM Compatibility**
```typescript
// Use conditional exports
{
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  }
}

// Add "type": "module" to package.json
// Name CJS files with .cjs extension
```

## When to Use This Skill

Activate this skill when you need to:
- Set up build configuration for a library
- Optimize bundle size
- Configure multi-format exports (ESM/CJS/UMD)
- Prepare package for NPM publishing
- Set up TypeScript declaration generation
- Configure tree-shaking
- Implement code splitting
- Create build scripts
- Set up CI/CD for publishing
- Troubleshoot build issues
- Migrate build tools
- Configure monorepo builds

## Output Format

When configuring builds, provide:
1. **Complete Configuration**: Build tool config files
2. **package.json Setup**: Proper entry points and scripts
3. **Build Instructions**: How to build and test
4. **Publishing Guide**: Step-by-step publishing process
5. **Optimization Report**: Bundle sizes and improvements
6. **Verification Steps**: How to verify build output

Always optimize for modern standards (ESM-first) while maintaining backwards compatibility where needed.
