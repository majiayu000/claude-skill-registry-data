---
name: web-projects
description: Guidelines for web development projects using JavaScript/TypeScript frameworks. Activate when working with web projects, package.json, npm/yarn/pnpm, React, Next.js, Vue, Angular, Svelte, or other web frameworks, frontend components, or Node.js applications.
---

# Web Projects

**Auto-activate when:** Working with `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `tsconfig.json`, `.eslintrc*`, `vite.config.*`, `next.config.*`, `*.jsx`, `*.tsx`, `*.vue`, `*.svelte`, or when user mentions React, Next.js, Vue, Angular, Svelte, npm, yarn, pnpm, or frontend development.

Guidelines for modern JavaScript/TypeScript web projects.

## Project Structure Recognition

### Package Managers
- Check `package.json` for dependencies and scripts
- Detect from lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`

### Framework Detection
Look for framework-specific configuration files:
- **Next.js**: `next.config.js`, `next.config.ts`
- **Vite**: `vite.config.js`, `vite.config.ts`
- **React**: Check `package.json` dependencies
- **Vue**: `vue.config.js`, `vite.config.ts` with Vue plugin
- **Angular**: `angular.json`
- **Svelte**: `svelte.config.js`

## Development Workflow

### Package Manager Usage
Respect the project's package manager:
- **npm**: `npm install`, `npm run`, `npm test`
- **yarn**: `yarn install`, `yarn`, `yarn test`
- **pnpm**: `pnpm install`, `pnpm run`, `pnpm test`

**Detection:** Lock file or config (`.npmrc`, `.yarnrc`, `pnpm-workspace.yaml`)

### Common Scripts
Check `package.json` "scripts" section for:
- `dev` or `start` - Development server
- `build` - Production build
- `test` - Run tests
- `lint` - Linting
- `format` - Code formatting

## Code Patterns

### Component Patterns
- **Respect existing patterns** - Don't change established structure
- Check naming conventions and import/export patterns
- Review existing components directory

### Testing Setup
- **Respect existing test framework** - Jest, Vitest, Testing Library, Cypress, Playwright
- Check config in `package.json` or dedicated files
- Follow established patterns and naming (`.test.js`, `.spec.ts`, etc.)

### Styling Approach
Identify and follow the project's styling method:
- CSS Modules (`.module.css`)
- Styled Components / Emotion
- Tailwind CSS (`tailwind.config.js`)
- SASS/SCSS (`.scss` files)
- Plain CSS

## Configuration Files

### Common Config Files
- `tsconfig.json` - TypeScript configuration
- `.eslintrc` - Linting rules
- `.prettierrc` - Code formatting
- `jest.config.js` or `vitest.config.ts` - Test configuration
- `.env.local`, `.env.development` - Environment variables

## Quick Reference

**Common mistakes to avoid:**
- ❌ Mixing package managers
- ❌ Changing test framework without discussion

---

**Note:** Web projects vary greatly - always check the project's specific configuration and patterns before making assumptions.
