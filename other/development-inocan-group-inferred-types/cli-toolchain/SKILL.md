---
name: cli-toolchain
description: "Apply modern CLI development toolchain patterns: Commander.js (default), oclif, Ink for Node.js command-line tools. Use when building CLI applications, choosing CLI frameworks, or discussing terminal UX."
---

# CLI Toolchain

Modern command-line application development with Node.js and TypeScript.

## Recommended Stack: Commander.js (Default)

**Why Commander.js (2025):**
- Lightweight library (not a framework)
- Unopinionated (full control over structure)
- Standard in Node.js ecosystem (24M+ downloads/week)
- Excellent TypeScript support
- Simple API for argument parsing and subcommands
- Battle-tested (used by Vue CLI, Create React App, etc.)

```bash
# Install
npm install commander

# Create CLI entry point
```

```typescript
// bin/cli.ts
#!/usr/bin/env node
import { Command } from 'commander'
import { version } from '../package.json'

const program = new Command()

program
  .name('my-cli')
  .description('CLI tool for awesome things')
  .version(version)

program
  .command('create <name>')
  .description('Create a new project')
  .option('-t, --template <type>', 'Project template', 'default')
  .action((name, options) => {
    console.log(`Creating project: ${name}`)
    console.log(`Template: ${options.template}`)
  })

program.parse()
```

### When to Use Commander.js
✅ Standard CLIs with subcommands and options
✅ Want lightweight, minimal overhead
✅ Need full control over implementation
✅ Simple argument parsing requirements
✅ Most use cases (90%+)

## Alternative: oclif

**Enterprise-grade CLI framework:**
- Full framework (not just parsing)
- Plugin system
- Auto-generated documentation
- Testing utilities
- Used by Salesforce, Heroku CLIs

```bash
# Create new CLI with oclif
npx oclif generate my-cli

# Structure enforced by framework
my-cli/
├── src/
│   ├── commands/       # Command files
│   └── hooks/          # Lifecycle hooks
├── test/
└── package.json
```

### When to Use oclif
✅ Large CLIs with many commands (20+)
✅ Need plugin architecture
✅ Auto-documentation required
✅ Enterprise/team projects
✅ Want opinionated structure

## Alternative: Ink

**React for CLIs:**
- Build interactive UIs with React components
- Flexbox layout for terminal
- Rich, interactive experiences (dashboards, progress, forms)

```bash
# Install
npm install ink react

# Create interactive CLI
```

```tsx
// bin/ui.tsx
import React from 'react'
import { render, Box, Text } from 'ink'

const App = () => (
  <Box flexDirection="column">
    <Text color="green">✓ Task completed</Text>
    <Text>Processing...</Text>
  </Box>
)

render(<App />)
```

### When to Use Ink
✅ Rich interactive UI needed (dashboards, loaders)
✅ Complex terminal layouts
✅ Team familiar with React
⚠️ Overkill for simple CLIs (use Commander.js)

## Toolchain Comparison

| | Commander.js | oclif | Ink |
|---|---|---|---|
| **Type** | Library | Framework | UI Library |
| **Setup** | Minimal | Scaffold | Manual |
| **Use Case** | General purpose | Large/complex | Interactive UI |
| **Learning Curve** | Low | Medium | Medium (React) |
| **Bundle Size** | Small | Large | Medium |
| **Flexibility** | High | Medium | High |
| **Documentation** | Good | Excellent | Good |

## Project Structure (Commander.js)

```
my-cli/
├── src/
│   ├── commands/           # Command implementations
│   │   ├── create.ts
│   │   ├── build.ts
│   │   └── deploy.ts
│   ├── utils/              # Shared utilities
│   │   ├── logger.ts
│   │   ├── config.ts
│   │   └── spinner.ts
│   ├── types/              # TypeScript types
│   └── index.ts            # Main CLI entry
├── bin/
│   └── cli                 # Executable (symlink to dist)
├── package.json
└── tsconfig.json
```

## Essential Patterns

### Subcommands

```typescript
// src/index.ts
import { Command } from 'commander'
import { createCommand } from './commands/create'
import { buildCommand } from './commands/build'

const program = new Command()

program
  .addCommand(createCommand)
  .addCommand(buildCommand)

program.parse()
```

```typescript
// src/commands/create.ts
import { Command } from 'commander'

export const createCommand = new Command('create')
  .description('Create a new project')
  .argument('<name>', 'Project name')
  .option('-t, --template <type>', 'Template type', 'default')
  .action(async (name, options) => {
    console.log(`Creating: ${name}`)
    // Implementation
  })
```

### Arguments & Options

```typescript
program
  .command('deploy')
  // Required argument
  .argument('<app>', 'Application to deploy')
  // Optional argument with default
  .argument('[environment]', 'Environment', 'production')
  // Boolean option
  .option('-d, --dry-run', 'Dry run mode')
  // Option with value
  .option('-r, --region <region>', 'Deployment region', 'us-east-1')
  // Option with choices
  .option('-l, --log-level <level>', 'Log level', 'info')
  .choices(['debug', 'info', 'warn', 'error'])
  // Variadic option (multiple values)
  .option('-e, --env <pairs...>', 'Environment variables')
  .action((app, environment, options) => {
    console.log({ app, environment, ...options })
  })
```

### Interactive Prompts

```bash
# Install prompts library
npm install inquirer @types/inquirer
```

```typescript
import inquirer from 'inquirer'

program
  .command('init')
  .action(async () => {
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'projectName',
        message: 'Project name:',
        default: 'my-app',
      },
      {
        type: 'list',
        name: 'template',
        message: 'Choose template:',
        choices: ['React', 'Vue', 'Vanilla'],
      },
      {
        type: 'confirm',
        name: 'useTypeScript',
        message: 'Use TypeScript?',
        default: true,
      },
    ])

    console.log('Creating project with:', answers)
  })
```

### Progress & Spinners

```bash
npm install ora chalk
```

```typescript
import ora from 'ora'
import chalk from 'chalk'

async function deploy() {
  const spinner = ora('Deploying application...').start()

  try {
    await performDeploy()
    spinner.succeed(chalk.green('Deployed successfully!'))
  } catch (error) {
    spinner.fail(chalk.red('Deployment failed'))
    console.error(error)
    process.exit(1)
  }
}
```

### Configuration Files

```typescript
// src/utils/config.ts
import { cosmiconfigSync } from 'cosmiconfig'

export function loadConfig() {
  const explorer = cosmiconfigSync('my-cli')
  const result = explorer.search()

  if (!result) {
    return {} // Default config
  }

  return result.config
}

// Looks for:
// - .my-clirc
// - .my-clirc.json
// - .my-clirc.yaml
// - my-cli.config.js
// - "my-cli" field in package.json
```

## Essential Libraries

```bash
# Argument parsing (if not using Commander.js)
npm install yargs

# Interactive prompts
npm install inquirer

# Terminal styling
npm install chalk

# Progress indicators
npm install ora cli-progress

# Tables
npm install cli-table3

# File system utilities
npm install fs-extra

# Configuration loading
npm install cosmiconfig
```

## Testing Strategy

```bash
npm install --save-dev vitest @types/node
```

```typescript
// src/commands/create.test.ts
import { describe, it, expect, vi } from 'vitest'
import { execSync } from 'child_process'

describe('create command', () => {
  it('creates project with default template', () => {
    const output = execSync('node dist/index.js create test-app')
    expect(output.toString()).toContain('Creating project: test-app')
  })

  it('uses specified template', () => {
    const output = execSync('node dist/index.js create test-app --template react')
    expect(output.toString()).toContain('Template: react')
  })
})
```

## Publishing to npm

```json
// package.json
{
  "name": "my-cli",
  "version": "1.0.0",
  "bin": {
    "my-cli": "./dist/index.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  }
}
```

```bash
# Build
npm run build

# Test locally
npm link
my-cli --version

# Publish
npm publish
```

## Quality Gates Integration

```yaml
# .github/workflows/cli-ci.yml
name: CLI CI

on: [pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [20, 22]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm run build
      - run: npm test

  publish:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Error Handling

```typescript
import chalk from 'chalk'

program
  .command('risky-operation')
  .action(async () => {
    try {
      await performOperation()
    } catch (error) {
      console.error(chalk.red('Error:'), error.message)

      if (process.env.DEBUG) {
        console.error(error.stack)
      }

      process.exit(1)
    }
  })

// Global error handler
program.exitOverride((err) => {
  if (err.code === 'commander.unknownCommand') {
    console.error(chalk.red('Unknown command. See --help for available commands.'))
    process.exit(1)
  }
  throw err
})
```

## Performance Optimization

```typescript
// Lazy load heavy dependencies
program
  .command('build')
  .action(async () => {
    // Only import when command is used
    const { build } = await import('./commands/build')
    await build()
  })

// Use dynamic imports for optional features
if (options.analyze) {
  const { analyze } = await import('./utils/analyzer')
  await analyze()
}
```

## UX Best Practices

- **Clear help text**: Use `.description()` liberally
- **Sensible defaults**: Minimize required options
- **Consistent naming**: Use kebab-case for flags
- **Progress feedback**: Show spinners for long operations
- **Color sparingly**: Red for errors, green for success, yellow for warnings
- **Respect --quiet**: Suppress non-critical output
- **Support --help**: Always implement comprehensive help
- **Version info**: Include `--version` flag

## Recommendation Flow

```
New CLI tool:
├─ Standard commands/options → Commander.js ✅
├─ Large enterprise CLI (20+ commands) → oclif
└─ Rich interactive UI needed → Ink

Combine approaches:
├─ Commander.js + Ink → Interactive commands when needed
└─ Commander.js + inquirer → Simple prompts
```

When agents design CLI tools, they should:
- Default to Commander.js for most use cases
- Use inquirer for interactive prompts
- Apply chalk sparingly for colored output
- Show ora spinners for long operations
- Load config with cosmiconfig
- Apply quality-gates skill for testing/CI
- Test on multiple OS (Linux, macOS, Windows)
- Publish to npm with proper bin configuration
- Lazy load heavy dependencies for performance
- Provide comprehensive --help documentation
