---
name: yargs-patterns
description: Advanced yargs patterns for Node.js CLI argument parsing with subcommands, options, middleware, and validation
tags: [nodejs, cli, yargs, argument-parsing, validation]
---

# yargs Patterns Skill

Comprehensive patterns and templates for building CLI applications with yargs, the modern Node.js argument parsing library.

## Overview

yargs is a powerful argument parsing library for Node.js that provides:
- Automatic help generation
- Rich command syntax (positional args, options, flags)
- Type coercion and validation
- Subcommands with isolated option namespaces
- Middleware for preprocessing
- Completion scripts for bash/zsh

## Quick Reference

### Basic Setup

```javascript
#!/usr/bin/env node
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('* <name>', 'greet someone', (yargs) => {
    yargs.positional('name', {
      describe: 'Name to greet',
      type: 'string'
    });
  }, (argv) => {
    console.log(`Hello, ${argv.name}!`);
  })
  .parse();
```

### Subcommands

```javascript
yargs(hideBin(process.argv))
  .command('init <project>', 'initialize a new project', (yargs) => {
    yargs
      .positional('project', {
        describe: 'Project name',
        type: 'string'
      })
      .option('template', {
        alias: 't',
        describe: 'Project template',
        choices: ['basic', 'advanced', 'minimal'],
        default: 'basic'
      });
  }, (argv) => {
    console.log(`Initializing ${argv.project} with ${argv.template} template`);
  })
  .command('build [entry]', 'build the project', (yargs) => {
    yargs
      .positional('entry', {
        describe: 'Entry point file',
        type: 'string',
        default: 'index.js'
      })
      .option('output', {
        alias: 'o',
        describe: 'Output directory',
        type: 'string',
        default: 'dist'
      })
      .option('minify', {
        describe: 'Minify output',
        type: 'boolean',
        default: false
      });
  }, (argv) => {
    console.log(`Building from ${argv.entry} to ${argv.output}`);
  })
  .parse();
```

### Options and Flags

```javascript
yargs(hideBin(process.argv))
  .option('verbose', {
    alias: 'v',
    type: 'boolean',
    description: 'Run with verbose logging',
    default: false
  })
  .option('config', {
    alias: 'c',
    type: 'string',
    description: 'Path to config file',
    demandOption: true  // Required option
  })
  .option('port', {
    alias: 'p',
    type: 'number',
    description: 'Port number',
    default: 3000
  })
  .option('env', {
    alias: 'e',
    type: 'string',
    choices: ['development', 'staging', 'production'],
    description: 'Environment'
  })
  .parse();
```

### Validation

```javascript
yargs(hideBin(process.argv))
  .command('deploy <service>', 'deploy a service', (yargs) => {
    yargs
      .positional('service', {
        describe: 'Service name',
        type: 'string'
      })
      .option('version', {
        describe: 'Version to deploy',
        type: 'string',
        coerce: (arg) => {
          // Custom validation
          if (!/^\d+\.\d+\.\d+$/.test(arg)) {
            throw new Error('Version must be in format X.Y.Z');
          }
          return arg;
        }
      })
      .option('replicas', {
        describe: 'Number of replicas',
        type: 'number',
        default: 1
      })
      .check((argv) => {
        // Cross-field validation
        if (argv.replicas > 10 && argv.env === 'development') {
          throw new Error('Cannot deploy more than 10 replicas in development');
        }
        return true;
      });
  }, (argv) => {
    console.log(`Deploying ${argv.service} v${argv.version} with ${argv.replicas} replicas`);
  })
  .parse();
```

### Middleware

```javascript
yargs(hideBin(process.argv))
  .middleware((argv) => {
    // Preprocessing middleware
    if (argv.verbose) {
      console.log('Running in verbose mode');
      console.log('Arguments:', argv);
    }
  })
  .middleware((argv) => {
    // Load config file
    if (argv.config) {
      const config = require(path.resolve(argv.config));
      return { ...argv, ...config };
    }
  })
  .command('run', 'run the application', {}, (argv) => {
    console.log('Application running with config:', argv);
  })
  .parse();
```

### Advanced Features

#### Conflicts and Implies

```javascript
yargs(hideBin(process.argv))
  .option('json', {
    describe: 'Output as JSON',
    type: 'boolean'
  })
  .option('yaml', {
    describe: 'Output as YAML',
    type: 'boolean'
  })
  .conflicts('json', 'yaml')  // Can't use both
  .option('output', {
    describe: 'Output file',
    type: 'string'
  })
  .option('format', {
    describe: 'Output format',
    choices: ['json', 'yaml'],
    implies: 'output'  // format requires output
  })
  .parse();
```

#### Array Options

```javascript
yargs(hideBin(process.argv))
  .option('include', {
    describe: 'Files to include',
    type: 'array',
    default: []
  })
  .option('exclude', {
    describe: 'Files to exclude',
    type: 'array',
    default: []
  })
  .parse();

// Usage: cli --include file1.js file2.js --exclude test.js
```

#### Count Options

```javascript
yargs(hideBin(process.argv))
  .option('verbose', {
    alias: 'v',
    describe: 'Verbosity level',
    type: 'count'  // -v, -vv, -vvv
  })
  .parse();
```

## Templates

See `templates/` directory for:
- `basic-cli.js` - Simple CLI with commands
- `advanced-cli.js` - Full-featured CLI with validation
- `config-cli.js` - CLI with configuration file support
- `interactive-cli.js` - CLI with prompts
- `plugin-cli.js` - Plugin-based CLI architecture

## Scripts

See `scripts/` directory for:
- `generate-completion.sh` - Generate bash/zsh completion
- `validate-args.js` - Argument validation helper
- `test-cli.sh` - CLI testing script

## Examples

See `examples/` directory for complete working examples.

## Resources

- [yargs Documentation](https://yargs.js.org/)
- [yargs GitHub](https://github.com/yargs/yargs)
- [yargs Best Practices](https://github.com/yargs/yargs/blob/main/docs/tricks.md)
