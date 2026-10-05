---
name: init-next-logging
description: Initializes production-ready logging for a Next.js project using Pino + pino-roll with file output and log rotation. Use when setting up a new Next.js project, adding logging infrastructure, or when the user asks to initialize Next.js logging with log rotation and file output.
---

# Init Next.js Logging

## Overview

This skill scaffolds a production-ready logging system for Next.js using **Pino** (high-performance, async-first) + **pino-roll** (log rotation) with file output. It handles both server-side (Node.js) and client-side environments.

## Prerequisites

- Next.js project (App Router recommended)
- Node.js 18+
- Package manager: npm / pnpm / yarn

## Workflow

### Step 1: Confirm deployment target

Ask the user which environment they are deploying to:

- **Self-hosted / VPS** (Node.js server) → full file logging with rotation
- **Vercel / Serverless** (filesystem read-only or ephemeral) → console + external log service only

If Vercel/serverless, skip file transport setup and point to external log services instead.

### Step 2: Install dependencies

Run the appropriate install command:

```bash
# npm
npm install pino pino-roll

# pnpm
pnpm add pino pino-roll

# yarn
yarn add pino pino-roll
```

### Step 3: Create the logger module

Create `lib/logger.ts` in the project root. Follow the [Pino + pino-roll reference](REFERENCE.md) for the full implementation.

Key decisions to confirm with the user:

- Log level: `info` (default) or `debug` (verbose)
- Rotation strategy: `frequency: 'daily'` (time-based) or `size: '10m'` (size-based)
- Max files to retain: default `14`

### Step 4: Create the log wrapper with request context

Create `lib/withLogger.ts` — a middleware-style wrapper that injects `requestId`, `method`, `url`, `duration` into every log entry automatically.

See the [reference](REFERENCE.md) for the complete implementation.

### Step 5: Wire up `instrumentation.ts`

If the project does not have `instrumentation.ts` at the project root, create it to capture unhandled exceptions and unhandled promise rejections. This is the only way to catch server-side crashes in Next.js.

```typescript
// instrumentation.ts
import logger from './lib/logger';

export async function register() {
    if (process.env.NEXT_RUNTIME === 'nodejs') {
        process.on('uncaughtException', error => {
            logger.fatal({ err: error }, 'Uncaught Exception');
            process.exit(1);
        });

        process.on('unhandledRejection', reason => {
            logger.fatal({ reason: String(reason) }, 'Unhandled Promise Rejection');
        });
    }
}
```

If `instrumentation.ts` already exists, merge the logger initialization into the existing `register()` function instead of creating a duplicate file.

### Step 6: Update `next.config.js`

Add the instrumentation hook configuration:

```js
// next.config.js
module.exports = {
    experimental: {
        instrumentationHook: true,
    },
};
```

If `experimental` is not present, add it. If it already exists with other keys, merge the `instrumentationHook: true` into the existing object.

### Step 7: Create the logs directory and update `.gitignore`

```bash
mkdir -p logs
touch logs/.gitkeep
```

Add to `.gitignore`:

```gitignore
logs/
*.log
```

### Step 8: Verify

1. Run `npm run dev` (or `pnpm dev` / `yarn dev`)
2. Visit any page or trigger an API route
3. Confirm that:
    - `logs/app.log` is created
    - Log entries are written in JSON format with `level`, `time`, `msg`, and context fields
    - When the file exceeds the size threshold, a numbered backup is created (e.g., `logs/app.log.0`, `logs/app.log.1.gz`)

## Output Summary

After setup, the project will have:

```
lib/
  logger.ts       # Core Pino + pino-roll logger
  withLogger.ts   # Request context wrapper / middleware
instrumentation.ts  # Global exception/rejection capture
logs/
  .gitkeep        # Placeholder to ensure directory is tracked
next.config.js    # instrumentationHook: true added
.gitignore        # logs/ and *.log excluded
```

## Quick Reference

| Topic               | Detail                                                |
| ------------------- | ----------------------------------------------------- |
| Log level           | Controlled by `LOG_LEVEL` env var; defaults to `info` |
| Rotation trigger    | `frequency: '1d'` (daily) or `size: '10m'`            |
| File format         | JSON (Pino default) — structured for log aggregation  |
| Uncaught exceptions | Captured via `instrumentation.ts`                     |
| Vercel/serverless   | Use LogLayer + DataDog/Logtail transport instead      |

For detailed code references, see [REFERENCE.md](REFERENCE.md).
