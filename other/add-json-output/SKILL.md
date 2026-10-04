---
name: add-json-output
description: Add --json flag to CLI commands for machine-readable output on stdout. Generic pattern for any CLI tool, enabling piping to jq and CI/CD integration while keeping human-readable output on stderr.
---

# Add JSON Output Mode

## Goal

Add `--json` flag to commands that produce output, writing structured JSON to stdout for programmatic consumption.

## Convention

- **stdout**: JSON output (only when `--json` is passed)
- **stderr**: Human-readable output (logs, progress, errors) — always

This allows: `mycli show --json | jq '.items'` to work while the user still sees progress on stderr.

## Implementation

### 1. Add --json Option to Commands

```ts
program
  .command('show')
  .option('--json', 'Output in JSON format')
  .action(async (options) => {
    const result = await buildResult()
    if (options.json) {
      process.stdout.write(JSON.stringify(result, null, 2) + '\n')
    } else {
      displayHumanReadable(result)
    }
  })
```

### 2. Define Result Types

Define typed interfaces for each command's JSON output:

```ts
interface ShowResult {
  items: Array<{
    name: string
    status: string
    // ... domain-specific fields
  }>
}
```

### 3. Suppress Decorative Output in JSON Mode

When `--json` is active, suppress spinners and progress bars on stderr:

```ts
if (options.json) {
  logger.setLevel('warn') // Only show warnings and errors
}
```

### 4. Error Output in JSON Mode

On error with `--json`, still output JSON to stdout:

```ts
if (options.json) {
  process.stdout.write(
    JSON.stringify(
      {
        success: false,
        error: {
          type: error.name,
          message: error.message,
          exitCode: error instanceof AppError ? error.exitCode : 1,
        },
      },
      null,
      2,
    ) + '\n',
  )
}
process.exit(exitCode)
```

### 5. Testing

```ts
test('show --json outputs valid JSON to stdout', async () => {
  const { stdout, stderr } = await runCli(['show', '--json'])
  const result = JSON.parse(stdout)
  expect(result.items).toBeInstanceOf(Array)
  // stderr may still have log output
})
```

## Which Commands

Add `--json` to any command that displays data:

- List/show commands
- Status commands
- Execution result commands
- Config display commands
