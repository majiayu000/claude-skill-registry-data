---
name: cli-author
description: Write Node.js CLI tools with zero dependencies. Use when creating command-line tools, argument parsing, colored output, or interactive prompts.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# CLI Authoring Skill

Write professional Node.js command-line tools using zero-dependency patterns.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Zero Dependencies | Use Node.js built-ins only (util.parseArgs, readline, fs) |
| Fail Fast | Validate arguments early, exit with clear errors |
| Exit Codes | 0 = success, 1 = user error, 2 = system error |
| Respect Environment | NO_COLOR, TERM, CI detection |
| Unix Philosophy | Single purpose, composable with pipes |

## Argument Parsing with util.parseArgs

Node.js 18+ includes native argument parsing:

```javascript
import { parseArgs } from 'node:util';

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    output: { type: 'string', short: 'o' },
    verbose: { type: 'boolean', short: 'v' },
    help: { type: 'boolean', short: 'h' },
  },
  allowPositionals: true,
});

// values.output, values.verbose, values.help
// positionals = ['file1.js', 'file2.js']
```

### Option Types

| Type | Example | Notes |
|------|---------|-------|
| `boolean` | `--verbose`, `-v` | Flag, no value needed |
| `string` | `--output file.txt`, `-o file.txt` | Requires value |
| `string` (multiple) | `--tag a --tag b` | Use `multiple: true` |

### Error Handling

```javascript
try {
  const { values } = parseArgs({ args, options, strict: true });
} catch (error) {
  if (error.code === 'ERR_PARSE_ARGS_UNKNOWN_OPTION') {
    console.error(`Unknown option: ${error.message}`);
    printHelp();
    process.exit(1);
  }
  throw error;
}
```

## CLI Structure Patterns

### Simple (Single Action)

```javascript
#!/usr/bin/env node
import { parseArgs } from 'node:util';

const { values, positionals } = parseArgs({...});

if (values.help) {
  printHelp();
  process.exit(0);
}

if (positionals.length === 0) {
  console.error('Error: No files specified');
  process.exit(1);
}

await processFiles(positionals, values);
```

### Multi-Command (Git-style)

```javascript
#!/usr/bin/env node
const [command, ...rest] = process.argv.slice(2);

const commands = {
  init: () => import('./commands/init.js'),
  build: () => import('./commands/build.js'),
  help: () => import('./commands/help.js'),
};

if (!command || command === 'help' || command === '--help') {
  showHelp(commands);
  process.exit(0);
}

if (!commands[command]) {
  console.error(`Unknown command: ${command}`);
  console.error(`Run 'toolname help' for available commands`);
  process.exit(1);
}

const { run } = await commands[command]();
await run(rest);
```

### Interactive (Wizard)

```javascript
#!/usr/bin/env node
import { createInterface } from 'node:readline';

const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
});

const question = (q) => new Promise((resolve) => rl.question(q, resolve));

async function wizard() {
  const name = await question('Project name: ');
  const type = await question('Type (lib/app): ');

  rl.close();
  return { name, type };
}

const config = await wizard();
await scaffold(config);
```

## Help Text Convention

```
Usage: toolname [options] <command> [arguments]

Commands:
  init          Initialize a new project
  build         Build the project
  help          Show this help message

Options:
  -o, --output <path>    Output directory
  -v, --verbose          Enable verbose output
  -h, --help             Show help
  --version              Show version

Examples:
  toolname init my-project
  toolname build --output dist/
```

## Colored Output

```javascript
// ANSI color codes (respect NO_COLOR)
const useColor = process.stdout.isTTY && !process.env.NO_COLOR;

const colors = {
  red: useColor ? '\x1b[31m' : '',
  green: useColor ? '\x1b[32m' : '',
  yellow: useColor ? '\x1b[33m' : '',
  blue: useColor ? '\x1b[34m' : '',
  dim: useColor ? '\x1b[2m' : '',
  reset: useColor ? '\x1b[0m' : '',
};

// Status indicators
const success = (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`);
const error = (msg) => console.error(`${colors.red}✗${colors.reset} ${msg}`);
const warn = (msg) => console.warn(`${colors.yellow}⚠${colors.reset} ${msg}`);
```

## Exit Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 0 | Success | Normal completion |
| 1 | User Error | Invalid args, file not found, validation failed |
| 2 | System Error | Unexpected exception, crash |
| 130 | SIGINT | Ctrl+C (convention) |

```javascript
process.on('uncaughtException', (error) => {
  console.error('Unexpected error:', error.message);
  process.exit(2);
});

process.on('SIGINT', () => {
  console.log('\nCancelled');
  process.exit(130);
});
```

## Config File Loading

```javascript
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

function findConfig(startDir, filename) {
  let dir = resolve(startDir);
  while (dir !== dirname(dir)) {
    const configPath = resolve(dir, filename);
    if (existsSync(configPath)) {
      return JSON.parse(readFileSync(configPath, 'utf-8'));
    }
    dir = dirname(dir);
  }
  return null;
}

// Load from .toolrc or package.json
const config = findConfig(process.cwd(), '.mytoolrc')
  || loadPackageJsonConfig('mytool')
  || {};
```

## Progress Indicators

### Spinner (Simple)

```javascript
const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
let i = 0;

const spinner = setInterval(() => {
  process.stdout.write(`\r${frames[i++ % frames.length]} Processing...`);
}, 80);

await longOperation();

clearInterval(spinner);
process.stdout.write('\r✓ Done\n');
```

### Progress Bar

```javascript
function progressBar(current, total, width = 30) {
  const percent = current / total;
  const filled = Math.round(width * percent);
  const empty = width - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);
  return `[${bar}] ${Math.round(percent * 100)}%`;
}

// Usage
for (let i = 0; i <= 100; i++) {
  process.stdout.write(`\r${progressBar(i, 100)}`);
  await delay(50);
}
console.log();
```

## Testing CLI Tools

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { execSync } from 'node:child_process';

describe('mytool CLI', () => {
  it('should show help with --help', () => {
    const output = execSync('node bin/mytool.js --help', {
      encoding: 'utf-8',
    });
    assert.match(output, /Usage:/);
  });

  it('should exit 1 on invalid args', () => {
    try {
      execSync('node bin/mytool.js --invalid', {
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'pipe'],
      });
      assert.fail('Should have exited with error');
    } catch (error) {
      assert.strictEqual(error.status, 1);
    }
  });

  it('should process files correctly', () => {
    const output = execSync('node bin/mytool.js test.txt', {
      encoding: 'utf-8',
    });
    assert.match(output, /Processed/);
  });
});
```

## Stdin/Stdout Piping

```javascript
import { createInterface } from 'node:readline';

// Read from stdin if no files provided
if (positionals.length === 0 && !process.stdin.isTTY) {
  const rl = createInterface({ input: process.stdin });
  for await (const line of rl) {
    process.stdout.write(processLine(line) + '\n');
  }
} else if (positionals.length === 0) {
  console.error('Error: No input. Pipe data or provide files.');
  process.exit(1);
}
```

## Checklist

When writing CLI tools:

**Structure**
- [ ] Shebang line: `#!/usr/bin/env node`
- [ ] Entry point in `bin/` directory
- [ ] Main logic in `src/` (importable as library)
- [ ] JSDoc documentation for main functions

**Arguments**
- [ ] `--help` and `-h` show usage
- [ ] `--version` shows version from package.json
- [ ] Unknown options produce helpful error
- [ ] Required arguments validated early

**Output**
- [ ] Respect NO_COLOR environment variable
- [ ] Use stderr for errors, stdout for results
- [ ] Exit 0 on success, 1 on user error, 2 on system error
- [ ] Support `--quiet` or `--json` for scripting

**Robustness**
- [ ] Handle SIGINT (Ctrl+C) gracefully
- [ ] Catch uncaught exceptions
- [ ] Validate file paths before use
- [ ] Work correctly when piped

## Related Skills

- **javascript-author** - JavaScript coding patterns
- **unit-testing** - Testing with Node.js test runner
- **error-handling** - Error management patterns
- **nodejs-backend** - Server-side Node.js patterns