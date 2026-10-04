---
name: cli-ux-polish
description: Polish CLI user experience with @clack/prompts for interactive flows, update-notifier for version awareness, and enhanced Commander.js help text with examples and colors. Generic patterns for any Node.js CLI.
---

# CLI UX Polish

## Goal

Improve the interactive experience with polished prompts, update notifications, and better help text.

## 1. Interactive Prompts with @clack/prompts

### Install

```bash
pnpm add @clack/prompts
```

### Confirmation Flow

```ts
import * as p from '@clack/prompts'

async function promptConfirmation(message: string): Promise<boolean> {
  const result = await p.confirm({ message })

  if (p.isCancel(result)) {
    p.cancel('Operation cancelled.')
    process.exit(130)
  }

  return result
}
```

### Selection Flow

```ts
async function promptSelect<T extends string>(
  message: string,
  options: Array<{ value: T; label: string }>,
): Promise<T> {
  const result = await p.select({ message, options })

  if (p.isCancel(result)) {
    p.cancel('Operation cancelled.')
    process.exit(130)
  }

  return result as T
}
```

### Spinner

```ts
const s = p.spinner()
s.start('Processing...')
await doWork()
s.stop('Done')
```

### Important

- Only use @clack/prompts when `process.stdout.isTTY` is true (interactive terminal)
- In non-TTY / CI modes, skip prompts and auto-approve or fail with a clear message
- Always handle `p.isCancel()` — it returns a symbol when user presses Ctrl+C

## 2. Update Notifications

### Install

```bash
pnpm add update-notifier
```

### Usage

Add to the CLI entry point (before command parsing):

```ts
import updateNotifier from 'update-notifier'

const pkg = { name: 'your-package-name', version: currentVersion }
updateNotifier({ pkg }).notify()
```

This:

- Checks npm registry in the background (non-blocking)
- Caches the result for 24h
- Shows notification only when a new version exists
- Automatically respects `NO_UPDATE_NOTIFIER=1` and CI environments

## 3. Enhanced Help Text

### Add Examples to Commands

```ts
program
  .command('apply')
  .description('Apply changes')
  .addHelpText(
    'after',
    `
Examples:
  $ mycli apply --env staging
  $ mycli apply --env production --approve
  $ mycli apply --env dev --json`,
  )
```

### Global Help Epilog

```ts
program.addHelpText(
  'after',
  `
Documentation: https://github.com/YOUR_ORG/YOUR_REPO
Report bugs:   https://github.com/YOUR_ORG/YOUR_REPO/issues`,
)
```

### Colored Help (Optional)

```ts
import pc from 'picocolors'

program.configureHelp({
  formatHelp: (cmd, helper) => {
    const defaultHelp = helper.formatHelp(cmd, helper)
    if (process.stdout.isTTY) {
      return defaultHelp
        .replace(/^Usage:/m, pc.bold('Usage:'))
        .replace(/^Commands:/m, pc.bold('Commands:'))
        .replace(/^Options:/m, pc.bold('Options:'))
    }
    return defaultHelp
  },
})
```
