---
name: cui-javascript-project
description: JavaScript project structure, package.json configuration, dependency management, and Maven integration standards for consistent project setup and builds
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JavaScript Project Structure and Build Standards

## Overview

This skill provides comprehensive standards for JavaScript project setup, structure, dependencies, and Maven integration in CUI projects. It covers directory layouts, package.json configuration, semantic versioning strategies, security management, ES module configuration, and frontend-maven-plugin integration for reproducible builds.

## Prerequisites

To effectively use this skill, you should have:

- Understanding of npm package management
- Knowledge of Maven build lifecycle
- Familiarity with project structure conventions
- Experience with Node.js development

## Standards Documents

This skill includes the following standards documents:

- **project-structure.md** - Directory layouts, file naming conventions, package.json structure, git ignore requirements
- **dependency-management.md** - Semantic versioning, security management, dependency updates, conflict resolution, ES module configuration
- **maven-integration.md** - Frontend Maven Plugin configuration, Maven phase integration, SonarQube integration, build environment standards

## What This Skill Provides

### Project Structure Standards
- **Directory Layouts**: Standard Maven, Quarkus DevUI, NiFi extension, standalone project structures
- **File Naming**: Kebab-case conventions, framework-specific prefixes (qwc-, nf-)
- **Package.json Configuration**: Essential structure, required fields, npm scripts
- **Configuration Files**: Location and naming for ESLint, Prettier, Jest, etc.
- **Git Ignore Requirements**: Essential exclusions for Node.js and Maven artifacts

### Dependency Management
- **Semantic Versioning**: Caret ranges vs exact versions, version update strategies
- **Security Management**: Vulnerability scanning, response timeframes, resolution strategies
- **Deprecated Packages**: Common replacements, handling deprecation warnings
- **Dependency Conflicts**: Peer dependency resolution, npm overrides
- **ES Module Configuration**: "type": "module" setup, configuration file syntax requirements
- **Update Management**: Regular update schedules, breaking change handling

### Maven Integration
- **Frontend Maven Plugin**: Required plugin setup, configuration parameters
- **Phase Integration**: Mapping npm scripts to Maven lifecycle phases
- **Node.js Management**: Version management, installation directory strategies
- **Script Integration**: Required npm scripts, execution order
- **SonarQube Integration**: Coverage reporting, quality gate configuration
- **Build Environment**: Reproducible builds, CI/CD integration
- **Project Adaptations**: Configuration for different project types

## When to Activate

This skill should be activated when:

1. **Setting Up New Project**: Creating new JavaScript project with Maven integration
2. **Configuring Project Structure**: Establishing directory layout and file organization
3. **Managing Dependencies**: Adding, updating, or resolving dependency issues
4. **Security Issues**: Addressing npm vulnerabilities or deprecated packages
5. **Maven Integration**: Configuring frontend-maven-plugin or build pipeline
6. **Build Issues**: Troubleshooting Maven/npm integration problems
7. **Updating Node.js**: Changing Node.js or npm versions
8. **SonarQube Setup**: Configuring JavaScript coverage analysis
9. **Project Type Adaptation**: Adapting structure for Quarkus, NiFi, or multi-module projects
10. **Best Practice Review**: Ensuring project follows CUI standards

## Workflow

When this skill is activated:

### 1. Identify Project Requirement
- Determine if new project setup or modification to existing
- Identify specific concern (structure, dependencies, Maven, security)
- Check current project type (Maven, Quarkus DevUI, NiFi, standalone)

### 2. Apply Project Structure Standards
- Use **project-structure.md** for directory layout selection
- Choose appropriate structure for project type
- Configure package.json with required fields and scripts
- Set up configuration files (.prettierrc.js, eslint.config.js, etc.)
- Create .gitignore with essential exclusions

### 3. Configure Dependency Management
- Reference **dependency-management.md** for version strategies
- Set up security audit scripts
- Configure semantic versioning (caret ranges for dev, exact for critical)
- Enable ES module support ("type": "module")
- Plan update management schedule

### 4. Integrate with Maven Build
- Use **maven-integration.md** for frontend-maven-plugin setup
- Configure Node.js version (v20.12.2 LTS)
- Map npm scripts to Maven phases
- Set up environment variables (CI=true, NODE_ENV=test)
- Configure SonarQube integration for JavaScript coverage

### 5. Validate Configuration
- Run Maven build to verify integration works
- Check Node.js installation in target/
- Verify npm scripts execute in correct phases
- Test dependency installation without errors
- Validate SonarQube picks up JavaScript coverage

## Tool Access

This skill provides access to project standards through:
- Read tool for accessing standards documents
- Standards documents use Markdown format for consistency
- All standards are self-contained within this skill
- Cross-references between standards use relative paths

## Integration Notes

### Related Skills
For comprehensive frontend development, this skill works with:
- **cui-javascript-linting** skill - ESLint, Prettier, and StyleLint configuration
- **cui-javascript** skill - Core JavaScript development standards
- **cui-jsdoc** skill - JSDoc documentation standards
- **cui-javascript-unit-testing** skill - Jest testing standards

### Build Integration
Project standards integrate with:
- npm for package management and script execution
- Maven for build automation via frontend-maven-plugin
- Node.js v20.12.2 LTS for runtime environment
- SonarQube for quality analysis and coverage reporting
- Git for version control with proper .gitignore setup

### Project Types
Standards support multiple project structures:
- **Standard Maven**: src/main/resources/static/js/
- **Quarkus DevUI**: src/main/resources/dev-ui/
- **NiFi Extension**: src/main/webapp/js/
- **Standalone**: src/main/js/
- **Multi-Module**: Nested frontend module structures

## Best Practices

When setting up JavaScript projects for CUI:

1. **Follow project type conventions** - Use appropriate directory structure for Maven/Quarkus/NiFi/Standalone
2. **Use kebab-case naming** - Consistent file naming across all JavaScript files
3. **Configure "type": "module"** - Enable ES module support in package.json
4. **Commit package-lock.json** - Ensure reproducible builds across environments
5. **Never commit node_modules/** - Always gitignore dependencies
6. **Use caret ranges for dev dependencies** - Allow automatic updates within major version
7. **Use exact versions for critical deps** - Pin production dependencies with breaking change history
8. **Implement all required npm scripts** - lint, format, test, quality scripts
9. **Integrate with Maven properly** - Map scripts to correct lifecycle phases
10. **Set up security auditing** - Regular vulnerability scanning and response
11. **Use Node.js v20.12.2 LTS** - Consistent version managed by frontend-maven-plugin
12. **Configure SonarQube coverage** - JavaScript code quality and coverage analysis
13. **Handle deprecations promptly** - Replace deprecated packages before they become critical
14. **Document project-specific setup** - Update README.md with structure and setup instructions

## Common Issues and Solutions

### Project Structure Issues
- **Wrong directory layout**: Verify project type and use correct structure pattern
- **Files not found during build**: Check package.json script paths match structure
- **Tests failing to locate sources**: Update Jest testMatch patterns for directory layout

### Dependency Management Issues
- **npm install failures**: Clear cache, delete node_modules/, regenerate package-lock.json
- **Peer dependency conflicts**: Try npm overrides before using --legacy-peer-deps
- **Security vulnerabilities**: Run npm audit fix, update vulnerable packages
- **Deprecated packages**: Identify replacements and update package.json

### Maven Integration Issues
- **Node.js installation failures**: Check internet connectivity, proxy settings, disk space
- **npm scripts not found**: Verify scripts exist in package.json
- **Build phase ordering**: Ensure validate → generate-resources → compile → test
- **Test failures in CI**: Set CI=true, use test:ci-strict script
- **SonarQube not picking up coverage**: Verify lcov.info path matches SonarQube property

### Configuration Issues
- **ES module errors**: Set "type": "module" in package.json
- **Configuration files not loading**: Ensure .prettierrc.js, eslint.config.js use export default
- **Inconsistent builds**: Commit package-lock.json, use frontend-maven-plugin for Node.js

## Quick Reference

### Essential package.json Structure

```json
{
  "name": "project-name",
  "version": "1.0.0-SNAPSHOT",
  "description": "Brief project description",
  "private": true,
  "type": "module",
  "scripts": {
    "lint:js": "eslint src/**/*.js",
    "lint:js:fix": "eslint --fix src/**/*.js",
    "format": "prettier --write \"src/**/*.js\"",
    "format:check": "prettier --check \"src/**/*.js\"",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci-strict": "jest --ci --coverage --watchAll=false --maxWorkers=2",
    "quality": "npm run lint:js && npm run format:check",
    "quality:fix": "npm run lint:js:fix && npm run format"
  },
  "devDependencies": {
    "eslint": "^9.14.0",
    "@eslint/js": "^9.14.0",
    "prettier": "^3.0.3",
    "jest": "^29.7.0"
  }
}
```

### Directory Structure by Project Type

**Standard Maven**:
```
src/main/resources/static/js/    # JavaScript source
src/test/js/                      # JavaScript tests
```

**Quarkus DevUI**:
```
src/main/resources/dev-ui/       # Quarkus DevUI components (qwc-*.js)
src/test/js/                     # Component tests
```

**NiFi Extension**:
```
src/main/webapp/js/              # NiFi UI components (nf-*.js)
src/test/js/                     # Tests with NiFi mocks
```

**Standalone**:
```
src/main/js/                     # JavaScript source
src/test/                        # Tests
```

### Maven Frontend Plugin Configuration

```xml
<plugin>
  <groupId>com.github.eirslett</groupId>
  <artifactId>frontend-maven-plugin</artifactId>
  <version>1.15.1</version>
  <configuration>
    <nodeVersion>v20.12.2</nodeVersion>
    <npmVersion>10.5.0</npmVersion>
    <installDirectory>target</installDirectory>
  </configuration>
  <executions>
    <execution>
      <id>install-node-and-npm</id>
      <goals><goal>install-node-and-npm</goal></goals>
      <phase>validate</phase>
    </execution>
    <execution>
      <id>npm-install</id>
      <goals><goal>npm</goal></goals>
      <phase>validate</phase>
      <configuration>
        <arguments>install</arguments>
      </configuration>
    </execution>
    <execution>
      <id>npm-format-check</id>
      <goals><goal>npm</goal></goals>
      <phase>compile</phase>
      <configuration>
        <arguments>run format:check</arguments>
      </configuration>
    </execution>
    <execution>
      <id>npm-lint</id>
      <goals><goal>npm</goal></goals>
      <phase>compile</phase>
      <configuration>
        <arguments>run lint</arguments>
      </configuration>
    </execution>
    <execution>
      <id>npm-test</id>
      <goals><goal>npm</goal></goals>
      <phase>test</phase>
      <configuration>
        <environmentVariables>
          <CI>true</CI>
          <NODE_ENV>test</NODE_ENV>
        </environmentVariables>
        <arguments>run test:ci-strict</arguments>
      </configuration>
    </execution>
  </executions>
</plugin>
```

### Semantic Versioning Quick Guide

**Caret ranges** (allow compatible updates):
```json
{
  "devDependencies": {
    "eslint": "^9.14.0",    // Updates to 9.x.x
    "webpack": "^5.96.1"    // Updates to 5.x.x
  }
}
```

**Exact versions** (pin specific version):
```json
{
  "dependencies": {
    "lit": "3.2.0",         // Exact version, no updates
    "core-js": "3.39.0"     // Polyfills require exact versions
  }
}
```

### Security Audit Commands

```json
{
  "scripts": {
    "audit:security": "npm audit --audit-level=moderate",
    "audit:fix": "npm audit fix",
    "audit:licenses": "npx license-checker --summary",
    "update:check": "npx npm-check-updates --format group",
    "update:dependencies": "npx npm-check-updates --upgrade"
  }
}
```

### Essential .gitignore Patterns

```gitignore
# Node.js
node_modules/
target/node/

# npm
.npm/
npm-debug.log*

# Coverage
target/coverage/
coverage/

# Build outputs
target/dist/
dist/
```
