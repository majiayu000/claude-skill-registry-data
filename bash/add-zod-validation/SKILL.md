---
name: add-zod-validation
description: Add zod schema validation for CLI options and YAML/JSON config files. Generic pattern for runtime validation with type-safe parsing and clear error messages in any Commander.js CLI.
---

# Add Zod Validation

## Goal

Add zod for runtime validation of CLI options and config files, providing type-safe parsing with clear error messages.

## Install

```bash
pnpm add zod
```

## CLI Option Validation

Create schemas for each command's options. Validate in the action handler before business logic.

### Pattern

```ts
import { z } from 'zod'

const commandOptionsSchema = z.object({
  format: z.enum(['default', 'table', 'json']).default('default'),
  env: z.string().min(1, 'Environment name cannot be empty').optional(),
  verbose: z.boolean().default(false),
  // Add command-specific options
})

type CommandOptions = z.infer<typeof commandOptionsSchema>

// In commander action:
.action(async (rawOptions: unknown) => {
  const result = commandOptionsSchema.safeParse(rawOptions)
  if (!result.success) {
    throw new UserError(formatZodError(result.error))
  }
  const options = result.data
  // ... typed and validated
})
```

### Error Formatting

```ts
import { ZodError } from 'zod'

function formatZodError(error: ZodError): string {
  return error.issues
    .map((issue) => {
      const path = issue.path.join('.')
      return path ? `--${path}: ${issue.message}` : issue.message
    })
    .join('\n')
}
```

## Config File Validation

### Example YAML Config Schema

```ts
const configSchema = z.object({
  // Adapt to your config file structure
  name: z.string().min(1),
  items: z.array(z.string()).min(1, 'At least one item required'),
  settings: z.record(z.unknown()).optional(),
  environments: z
    .record(
      z.object({
        vars: z.record(z.string()).optional(),
      }),
    )
    .optional(),
})
```

### Validate at Parse Time

```ts
import YAML from 'yaml'

function parseConfig(content: string, filePath: string) {
  const raw = YAML.parse(content)
  const result = configSchema.safeParse(raw)
  if (!result.success) {
    throw new ConfigError(formatZodError(result.error), filePath)
  }
  return result.data
}
```

## Best Practices

- Use `safeParse` (not `parse`) to throw custom errors (ConfigError, UserError)
- Keep schemas close to where they're used (colocate with the reader/handler)
- Export schemas for reuse in tests
- Use `z.coerce.number()` for CLI args that come as strings but need to be numbers
