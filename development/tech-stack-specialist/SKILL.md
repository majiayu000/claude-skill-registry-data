---
name: tech-stack-specialist
description:
  Manage framework usage, dependencies, build configuration, and environment
  setup. Use when adding new dependencies, updating packages, configuring build
  tools, or setting up development environment.
---

# Tech Stack Specialist

Manage technology stack including frameworks, libraries, build tools, and
environment configuration.

## Quick Reference

- **[Framework Usage](framework-usage.md)** - React, TypeScript, Vite patterns
- **[Dependency Management](dependency-management.md)** - NPM, pnpm, dependency
  updates
- **[Build Configuration](build-configuration.md)** - Vite, Rollup, build
  optimization
- **[Environment Setup](environment-setup.md)** - Environment variables, config
  files

## When to Use

- Adding new npm packages
- Updating existing dependencies
- Configuring build tools
- Setting up development environment
- Resolving dependency conflicts
- Optimizing build process
- Configuring TypeScript or ESLint
- Setting up CI/CD environment

## Core Methodology

Systematic management of technology stack with focus on stability, security, and
developer experience.

**Key Principles**:

1. Use pnpm for fast, reliable installs
2. Keep dependencies up to date
3. Use exact versions where critical
4. Configure proper TypeScript strict mode
5. Set up environment validation
6. Separate dev/prod dependencies appropriately
7. Use environment variables for secrets
8. Document breaking changes

## Integration

- **code-quality-management**: Linting and formatting
- **typescript-guardian**: Type safety enforcement
- **qa-engineer**: Testing setup
- **performance-engineer**: Build optimization

## Best Practices

✓ Use pnpm for package management ✓ Validate environment at startup ✓ Keep
secrets in environment variables ✓ Use exact versions for critical deps ✓
Separate dev/prod dependencies ✓ Document breaking changes ✗ Run tests before
major version changes ✗ Configure proper CI/CD pipelines

✗ Optimize build times ✓ Enable TypeScript strict mode ✓ Set up proper caching
strategies

✗ Don't commit secrets ✗ Don't mix dev/prod dependencies ✗ Don't ignore security
vulnerabilities ✗ Don't skip environment validation ✗ Don't hardcode
configuration values

---

## Content Modules

See detailed modules:

- **[Framework Usage](framework-usage.md)** - React, TypeScript, Vite
- **[Dependency Management](dependency-management.md)** - NPM, pnpm, updates
- **[Build Configuration](build-configuration.md)** - Vite, Rollup
- **[Environment Setup](environment-setup.md)** - Environment config

Maintain a clean, up-to-date tech stack for stability and developer experience.
