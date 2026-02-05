---
name: package-json-scaffolder
description: Generate complete package.json files with appropriate dependencies, scripts, and configuration for Node.js projects of various types. Triggers on "create package.json", "generate package.json for", "npm init for", "node project setup".
---

# Package.json Scaffolder

Generate complete, production-ready `package.json` files with appropriate dependencies, scripts, and metadata for various Node.js project types.

## Output Requirements

**File Output:** `package.json`
**Format:** Valid JSON with 2-space indentation
**Compatibility:** npm, yarn, pnpm compatible

## When Invoked

Immediately generate a complete `package.json` with sensible defaults. Use current LTS versions for dependencies unless specified otherwise.

## JSON Structure

### Required Fields
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Project description",
  "main": "index.js",
  "scripts": {},
  "dependencies": {},
  "devDependencies": {}
}
```

### Recommended Fields
```json
{
  "author": "Author Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "keywords": ["keyword1", "keyword2"],
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Project Type Templates

### React Application (Vite)
```json
{
  "name": "react-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest",
    "test:coverage": "vitest run --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.55",
    "@types/react-dom": "^18.2.19",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "typescript": "^5.3.3",
    "vite": "^5.1.0",
    "vitest": "^1.2.0",
    "@vitest/coverage-v8": "^1.2.0"
  }
}
```

### Next.js Application
```json
{
  "name": "nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.55",
    "@types/react-dom": "^18.2.19",
    "eslint": "^8.56.0",
    "eslint-config-next": "14.1.0",
    "typescript": "^5.3.3",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.12",
    "jest-environment-jsdom": "^29.7.0"
  }
}
```

### Express API Server
```json
{
  "name": "express-api",
  "version": "1.0.0",
  "description": "Express REST API",
  "main": "dist/index.js",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "lint": "eslint src --ext .ts",
    "test": "jest",
    "test:watch": "jest --watch",
    "db:migrate": "prisma migrate dev",
    "db:generate": "prisma generate"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0",
    "dotenv": "^16.4.1",
    "zod": "^3.22.4",
    "@prisma/client": "^5.9.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "@types/morgan": "^1.9.9",
    "@types/node": "^20.11.0",
    "typescript": "^5.3.3",
    "tsx": "^4.7.0",
    "prisma": "^5.9.0",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.12",
    "ts-jest": "^29.1.2"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### CLI Tool
```json
{
  "name": "my-cli-tool",
  "version": "1.0.0",
  "description": "A command-line tool",
  "bin": {
    "mycli": "./dist/cli.js"
  },
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist"
  ],
  "scripts": {
    "dev": "tsx src/cli.ts",
    "build": "tsup src/index.ts src/cli.ts --format cjs,esm --dts",
    "lint": "eslint src --ext .ts",
    "test": "vitest",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "commander": "^12.0.0",
    "chalk": "^5.3.0",
    "ora": "^8.0.1",
    "inquirer": "^9.2.14"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/inquirer": "^9.0.7",
    "typescript": "^5.3.3",
    "tsx": "^4.7.0",
    "tsup": "^8.0.1",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "vitest": "^1.2.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "keywords": ["cli", "tool"]
}
```

### NPM Library Package
```json
{
  "name": "@scope/my-library",
  "version": "1.0.0",
  "description": "A reusable library",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "require": "./dist/index.js",
      "import": "./dist/index.mjs",
      "types": "./dist/index.d.ts"
    }
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts --clean",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src --ext .ts",
    "test": "vitest",
    "test:coverage": "vitest run --coverage",
    "prepublishOnly": "npm run lint && npm run test && npm run build"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.3.3",
    "tsup": "^8.0.1",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "vitest": "^1.2.0",
    "@vitest/coverage-v8": "^1.2.0"
  },
  "peerDependencies": {},
  "engines": {
    "node": ">=18.0.0"
  },
  "publishConfig": {
    "access": "public"
  },
  "keywords": [],
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "license": "MIT"
}
```

### Monorepo Root (Turborepo)
```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "turbo": "^1.12.0",
    "prettier": "^3.2.4",
    "eslint": "^8.56.0"
  },
  "packageManager": "pnpm@8.15.0",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Common Script Patterns

### Development
```json
{
  "dev": "tsx watch src/index.ts",
  "dev:debug": "tsx watch --inspect src/index.ts"
}
```

### Building
```json
{
  "build": "tsc",
  "build:watch": "tsc --watch",
  "clean": "rm -rf dist"
}
```

### Testing
```json
{
  "test": "vitest",
  "test:watch": "vitest --watch",
  "test:coverage": "vitest run --coverage",
  "test:e2e": "playwright test"
}
```

### Linting & Formatting
```json
{
  "lint": "eslint . --ext .ts,.tsx",
  "lint:fix": "eslint . --ext .ts,.tsx --fix",
  "format": "prettier --write .",
  "format:check": "prettier --check ."
}
```

### Database
```json
{
  "db:migrate": "prisma migrate dev",
  "db:push": "prisma db push",
  "db:generate": "prisma generate",
  "db:studio": "prisma studio",
  "db:seed": "tsx prisma/seed.ts"
}
```

## Validation Checklist

Before outputting, verify:
- [ ] Valid JSON syntax
- [ ] 2-space indentation
- [ ] Name is lowercase, no spaces (use hyphens)
- [ ] Version follows semver (x.y.z)
- [ ] Scripts are appropriate for project type
- [ ] Dependencies use `^` for minor version flexibility
- [ ] DevDependencies vs dependencies are correct
- [ ] Engine requirements specified if needed
- [ ] No duplicate dependencies

## Example Invocations

**Prompt:** "Create package.json for a React TypeScript project with testing"
**Output:** Complete `package.json` with Vite, React, TypeScript, Vitest configured.

**Prompt:** "Generate package.json for Express API with Prisma"
**Output:** Complete `package.json` with Express, Prisma, testing scripts.

**Prompt:** "Package.json for publishable npm library"
**Output:** Complete `package.json` with proper exports, types, and publish config.
