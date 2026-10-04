---
name: error-hierarchy
description: Implement a structured error class hierarchy with actionable messages, proper exit codes, debug mode via env var, and bug report hints on unexpected errors. Generic pattern for any CLI tool or Node.js application.
---

# Structured Error Handling

## Goal

Build a structured error hierarchy with actionable messages, consistent exit codes, and good DX for debugging.

## Error Class Hierarchy

```ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly exitCode: number = 1,
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class UserError extends AppError {
  constructor(message: string) {
    super(message, 2)
    this.name = 'UserError'
  }
}

export class ConfigError extends UserError {
  constructor(
    message: string,
    public readonly filePath: string,
  ) {
    super(`${filePath}: ${message}`)
    this.name = 'ConfigError'
  }
}

// Add domain-specific error subclasses as needed, e.g.:
// export class ProviderError extends AppError { ... exitCode = 3 }
```

## Exit Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 0    | Success                                |
| 1    | Unexpected/internal error              |
| 2    | User error (bad input, missing config) |
| 3+   | Domain-specific errors                 |
| 130  | Interrupted (SIGINT)                   |

## Actionable Error Messages

Every error message must tell the user what happened AND what to do:

```text
Bad:  "No environment selected"
Good: "No environment selected. Run 'mycli env select <env>' or pass --env <env>."

Bad:  "Config not found"
Good: "Config file not found at /path/config.yaml. Run 'mycli init' to create one."

Bad:  "Invalid option"
Good: "Invalid format 'xml'. Expected one of: default, table, json"
```

## Debug Mode via Environment Variable

Support a debug env var (e.g., `MY_CLI_DEBUG=1`) in addition to `--verbose`:

```ts
const isDebug = () => process.env['MY_CLI_DEBUG'] === '1' || process.env['MY_CLI_VERBOSE'] === '1'
```

Use in the global error handler to show stack traces.

## Bug Report Hint

On unexpected errors (non-UserError), print actionable debug info:

```ts
function formatUnexpectedError(error: Error, command: string): string {
  const version = getPackageVersion()
  return [
    'Unexpected internal error',
    '',
    'This is a bug. Please report it at:',
    'https://github.com/YOUR_ORG/YOUR_REPO/issues/new',
    '',
    'Include the following:',
    `  Version: ${version}`,
    `  Node.js: ${process.version}`,
    `  OS: ${process.platform} ${process.arch}`,
    `  Command: ${command}`,
    '',
    error.stack ?? error.message,
  ].join('\n')
}
```

## SIGINT Handling

Ensure clean exit on Ctrl+C:

```ts
process.on('SIGINT', () => {
  process.exit(130)
})
```

## Global Error Handler Pattern

```ts
async function main() {
  try {
    await runCli()
  } catch (error) {
    if (error instanceof UserError) {
      console.error(`Error: ${error.message}`)
      process.exit(error.exitCode)
    }
    // Unexpected error
    console.error(formatUnexpectedError(error, process.argv.slice(2).join(' ')))
    process.exit(1)
  }
}
```
