---
name: auto-detect-ci
description: Add automatic CI/CD environment detection using ci-info package. Generic pattern for any CLI tool that needs to adapt behavior (prompts, output, integrations) based on whether it's running in CI.
---

# Auto-Detect CI Environment

## Goal

Automatically detect CI environments and adapt CLI behavior — removing the need for explicit flags in most cases.

## Install

```bash
pnpm add ci-info
```

## Implementation

### Detection Function

```ts
import ci from 'ci-info'

type RunMode = 'interactive' | 'non-interactive' | string

function detectRunMode(explicit?: string): RunMode {
  // Explicit flag always wins
  if (explicit) return explicit

  // CI environment detected
  if (ci.isCI) {
    // Add CI-specific modes as needed, e.g.:
    // if (ci.GITLAB) return 'gitlab'
    // if (ci.GITHUB_ACTIONS) return 'github-actions'
    return 'non-interactive'
  }

  // Local: check if terminal is interactive
  return process.stdout.isTTY ? 'interactive' : 'non-interactive'
}
```

### Integration Points

1. In Commander action handlers, use detection as default:

```ts
const mode = detectRunMode(options.mode)
```

2. Log the detected mode in verbose/debug:

```ts
if (isDebug()) {
  logger.debug(`Run mode: ${mode}${ci.isCI ? ` (detected: ${ci.name})` : ''}`)
}
```

### Behavior Matrix

| Environment                     | TTY | Explicit flag            | Result                        |
| ------------------------------- | --- | ------------------------ | ----------------------------- |
| Local terminal                  | yes | not set                  | `interactive`                 |
| Local pipe (`mycli show \| jq`) | no  | not set                  | `non-interactive`             |
| GitHub Actions                  | no  | not set                  | `non-interactive`             |
| GitLab CI                       | no  | not set                  | `non-interactive`             |
| Any CI                          | no  | `interactive` (explicit) | `interactive` (user override) |

### Where to Apply

- Commands with interactive prompts (confirmations, selections)
- Output formatting (spinners vs plain text)
- Approval flows (auto-approve in CI vs prompt in terminal)
- Any behavior that differs between human and automated usage

### Testing

```ts
test('detects CI from environment', () => {
  vi.mock('ci-info', () => ({ isCI: true, GITLAB: false, name: 'GitHub Actions' }))
  expect(detectRunMode()).toBe('non-interactive')
})

test('explicit flag overrides detection', () => {
  expect(detectRunMode('interactive')).toBe('interactive')
})
```
