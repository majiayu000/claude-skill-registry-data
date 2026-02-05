---
name: Commander.js Patterns
description: Commander.js CLI framework patterns including Command class, options, arguments, nested subcommands, and Option class usage. Use when building Node.js CLIs, implementing Commander.js commands, creating TypeScript CLI tools, adding command options/arguments, or when user mentions Commander.js, CLI commands, command options, or nested subcommands.
allowed-tools: Read, Write, Bash, Edit
---

# Commander.js Patterns Skill

Provides comprehensive Commander.js patterns, templates, and examples for building robust Node.js CLI applications with TypeScript support.

## Overview

Commander.js is the complete solution for Node.js command-line interfaces. This skill provides battle-tested patterns for:
- Command class instantiation and configuration
- Options with flags, choices, and defaults
- Arguments (required, optional, variadic)
- Nested subcommands and command hierarchies
- Option class with advanced validation
- Action handlers and middleware
- Error handling and validation

## Instructions

### Basic Command Setup

1. **Create program instance:**
   ```typescript
   import { Command } from 'commander';
   const program = new Command();

   program
     .name('mycli')
     .description('CLI description')
     .version('1.0.0');
   ```

2. **Add simple command:**
   ```typescript
   program
     .command('init')
     .description('Initialize project')
     .action(() => {
       // Command logic
     });
   ```

3. **Parse arguments:**
   ```typescript
   program.parse();
   ```

### Command with Options

Use options for named flags with values:

```typescript
program
  .command('deploy')
  .description('Deploy application')
  .option('-e, --env <environment>', 'target environment', 'dev')
  .option('-f, --force', 'force deployment', false)
  .option('-v, --verbose', 'verbose output')
  .action((options) => {
    console.log('Environment:', options.env);
    console.log('Force:', options.force);
    console.log('Verbose:', options.verbose);
  });
```

### Command with Arguments

Use arguments for positional parameters:

```typescript
program
  .command('deploy <environment>')
  .description('Deploy to environment')
  .argument('<environment>', 'target environment')
  .argument('[region]', 'optional region', 'us-east-1')
  .action((environment, region, options) => {
    console.log(`Deploying to ${environment} in ${region}`);
  });
```

### Option Class Usage

For advanced option configuration:

```typescript
import { Command, Option } from 'commander';

program
  .command('deploy')
  .addOption(
    new Option('-m, --mode <mode>', 'deployment mode')
      .choices(['fast', 'safe', 'rollback'])
      .default('safe')
      .makeOptionMandatory()
  )
  .addOption(
    new Option('-r, --replicas <count>', 'replica count')
      .argParser(parseInt)
      .default(3)
  )
  .action((options) => {
    console.log(`Mode: ${options.mode}, Replicas: ${options.replicas}`);
  });
```

### Nested Subcommands

Create command hierarchies:

```typescript
const config = program
  .command('config')
  .description('Manage configuration');

config
  .command('get <key>')
  .description('Get config value')
  .action((key) => {
    console.log(`Config ${key}:`, getConfig(key));
  });

config
  .command('set <key> <value>')
  .description('Set config value')
  .action((key, value) => {
    setConfig(key, value);
    console.log(`✓ Set ${key} = ${value}`);
  });

config
  .command('list')
  .description('List all config')
  .action(() => {
    console.log(getAllConfig());
  });
```

### Variadic Arguments

Accept multiple values:

```typescript
program
  .command('add <items...>')
  .description('Add multiple items')
  .action((items) => {
    console.log('Adding items:', items);
  });

// Usage: mycli add item1 item2 item3
```

### Custom Argument Parsing

Transform argument values:

```typescript
program
  .command('wait <delay>')
  .description('Wait for specified time')
  .argument('<delay>', 'delay in seconds', parseFloat)
  .action((delay) => {
    console.log(`Waiting ${delay} seconds...`);
  });
```

### Global Options

Options available to all commands:

```typescript
program
  .option('-c, --config <path>', 'config file path')
  .option('-v, --verbose', 'verbose output')
  .option('--no-color', 'disable colors');

program
  .command('deploy')
  .action((options, command) => {
    const globalOpts = command.parent?.opts();
    console.log('Config:', globalOpts?.config);
    console.log('Verbose:', globalOpts?.verbose);
  });
```

### Error Handling

```typescript
program
  .command('deploy <environment>')
  .action((environment) => {
    if (!['dev', 'staging', 'prod'].includes(environment)) {
      throw new Error(`Invalid environment: ${environment}`);
    }
    // Deploy logic
  });

program.exitOverride();
try {
  program.parse();
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
```

## Available Scripts

- **validate-commander-structure.sh**: Validates Commander.js CLI structure and patterns
- **generate-command.sh**: Scaffolds new command with options and arguments
- **generate-subcommand.sh**: Creates nested subcommand structure
- **test-commander-cli.sh**: Tests CLI commands with various inputs
- **extract-command-help.sh**: Extracts help text from CLI for documentation

## Templates

### TypeScript Templates
- **basic-commander.ts**: Minimal Commander.js setup
- **command-with-options.ts**: Command with various option types
- **command-with-arguments.ts**: Command with required/optional arguments
- **nested-subcommands.ts**: Multi-level command hierarchy
- **option-class-advanced.ts**: Advanced Option class usage
- **full-cli-example.ts**: Complete CLI with all patterns
- **commander-with-inquirer.ts**: Interactive prompts integration
- **commander-with-validation.ts**: Input validation patterns

### JavaScript Templates
- **basic-commander.js**: ES modules Commander.js setup
- **commonjs-commander.js**: CommonJS Commander.js setup

### Configuration Templates
- **tsconfig.commander.json**: TypeScript config for Commander.js projects
- **package.json.template**: Package.json with Commander.js dependencies

## Examples

- **basic-usage.md**: Simple CLI with 2-3 commands
- **options-arguments-demo.md**: Comprehensive options and arguments examples
- **nested-commands-demo.md**: Building command hierarchies
- **advanced-option-class.md**: Option class validation and parsing
- **interactive-cli.md**: Combining Commander.js with Inquirer.js
- **error-handling-patterns.md**: Robust error handling strategies
- **testing-commander-cli.md**: Unit and integration testing patterns

## Commander.js Key Concepts

### Command Class
```typescript
new Command()
  .name('cli-name')
  .description('CLI description')
  .version('1.0.0')
  .command('subcommand')
```

### Option Types
- **Flag option**: `-v, --verbose` (boolean)
- **Value option**: `-p, --port <port>` (required value)
- **Optional value**: `-p, --port [port]` (optional value)
- **Negatable**: `--no-color` (inverse boolean)
- **Variadic**: `--files <files...>` (multiple values)

### Argument Types
- **Required**: `<name>`
- **Optional**: `[name]`
- **Variadic**: `<items...>` or `[items...]`

### Option Class Methods
- `.choices(['a', 'b', 'c'])`: Restrict to specific values
- `.default(value)`: Set default value
- `.argParser(fn)`: Custom parsing function
- `.makeOptionMandatory()`: Require option
- `.conflicts(option)`: Mutually exclusive options
- `.implies(option)`: Implies another option
- `.env(name)`: Read from environment variable

### Action Handler Signatures
```typescript
// No arguments
.action(() => {})

// With options only
.action((options) => {})

// With arguments
.action((arg1, arg2, options) => {})

// With command reference
.action((options, command) => {})
```

## Pattern Recipes

### Pattern 1: Simple CLI with Subcommands
Use template: `templates/basic-commander.ts`

### Pattern 2: CLI with Rich Options
Use template: `templates/option-class-advanced.ts`

### Pattern 3: Interactive CLI
Use template: `templates/commander-with-inquirer.ts`

### Pattern 4: CLI with Validation
Use template: `templates/commander-with-validation.ts`

### Pattern 5: Multi-level Commands
Use template: `templates/nested-subcommands.ts`

## Integration with Other Tools

### With Inquirer.js (Interactive Prompts)
```typescript
import inquirer from 'inquirer';

program
  .command('setup')
  .action(async () => {
    const answers = await inquirer.prompt([
      { type: 'input', name: 'name', message: 'Project name:' },
      { type: 'list', name: 'template', message: 'Template:', choices: ['basic', 'advanced'] }
    ]);
    // Use answers
  });
```

### With Chalk (Colored Output)
```typescript
import chalk from 'chalk';

program
  .command('deploy')
  .action(() => {
    console.log(chalk.green('✓ Deployment successful'));
    console.log(chalk.red('✗ Deployment failed'));
  });
```

### With Ora (Spinners)
```typescript
import ora from 'ora';

program
  .command('build')
  .action(async () => {
    const spinner = ora('Building...').start();
    await build();
    spinner.succeed('Build complete');
  });
```

## Best Practices

1. **Use Option class for complex options**: Provides better validation and type safety
2. **Keep action handlers thin**: Delegate to separate functions
3. **Provide clear descriptions**: Help users understand commands
4. **Set sensible defaults**: Reduce required options
5. **Validate early**: Check inputs before processing
6. **Handle errors gracefully**: Provide helpful error messages
7. **Use TypeScript**: Better type safety and IDE support
8. **Test thoroughly**: Unit test commands and options
9. **Document examples**: Show common usage patterns
10. **Version your CLI**: Use semantic versioning

## Common Patterns

### Pattern: Config Command Group
```typescript
const config = program.command('config');
config.command('get <key>').action(getConfig);
config.command('set <key> <value>').action(setConfig);
config.command('list').action(listConfig);
config.command('delete <key>').action(deleteConfig);
```

### Pattern: CRUD Commands
```typescript
program.command('create <name>').action(create);
program.command('read <id>').action(read);
program.command('update <id>').action(update);
program.command('delete <id>').action(deleteItem);
program.command('list').action(list);
```

### Pattern: Deploy with Environments
```typescript
program
  .command('deploy')
  .addOption(new Option('-e, --env <env>').choices(['dev', 'staging', 'prod']))
  .option('-f, --force', 'force deployment')
  .action(deploy);
```

## Troubleshooting

### Issue: Options not parsed
**Solution**: Ensure `program.parse()` is called

### Issue: Arguments not received
**Solution**: Check action handler signature matches argument count

### Issue: Subcommands not working
**Solution**: Verify subcommand is attached before `parse()`

### Issue: TypeScript errors
**Solution**: Install `@types/node` and configure tsconfig

### Issue: Help not showing
**Solution**: Commander.js auto-generates help from descriptions

## Success Criteria

✅ Command structure follows Commander.js conventions
✅ Options and arguments properly typed
✅ Help text is clear and descriptive
✅ Error handling covers edge cases
✅ CLI tested with various inputs
✅ TypeScript compiles without errors
✅ Commands execute as expected

## Related Skills

- `click-patterns` - Python Click framework patterns
- `typer-patterns` - Python Typer framework patterns
- `clap-patterns` - Rust Clap framework patterns

---

**Skill Type**: Framework Patterns + Code Templates
**Language**: TypeScript/JavaScript (Node.js)
**Framework**: Commander.js v12+
**Auto-invocation**: Yes (via description matching)
