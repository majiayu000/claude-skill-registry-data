---
name: pino
description: Pino fast JSON logger for Node.js. Covers log levels, child loggers, transports, and redaction. Triggers on pino, logger, log.info, log.error.
triggers: ["pino", "logger", "log\\.info", "log\\.error", "log\\.warn", "log\\.debug"]
---

<objective>
Implement structured logging using Pino - the fastest Node.js JSON logger. Configure log levels, child loggers, and transports for different environments.
</objective>

<mcp_first>
**CRITICAL: Fetch Pino documentation before implementing.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_octocode__githubSearchCode" })
```

```typescript
// Pino configuration
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["pino", "logger", "transport"],
  owner: "pinojs",
  repo: "pino",
  path: "lib",
  mainResearchGoal: "Understand Pino logger configuration",
  researchGoal: "Find logger setup patterns",
  reasoning: "Need current API for Pino setup"
})

// Transports
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["pino-pretty", "transport", "destination"],
  owner: "pinojs",
  repo: "pino",
  path: "docs",
  mainResearchGoal: "Understand Pino transports",
  researchGoal: "Find transport configuration patterns",
  reasoning: "Need current API for log transports"
})
```
</mcp_first>

<quick_start>
**Basic setup:**

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
});

logger.info("Server started");
logger.error({ err }, "Database connection failed");
logger.debug({ userId }, "User authenticated");
```

**With pretty printing (development):**

```typescript
import pino from "pino";

const logger = pino({
  level: "debug",
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      translateTime: "HH:MM:ss",
      ignore: "pid,hostname",
    },
  },
});
```

**Child loggers:**

```typescript
const requestLogger = logger.child({ requestId: req.id });
requestLogger.info("Processing request");
// Output: {"level":30,"requestId":"abc123","msg":"Processing request"}
```
</quick_start>

<log_levels>
| Level | Value | Use Case |
|-------|-------|----------|
| `fatal` | 60 | App crash |
| `error` | 50 | Error conditions |
| `warn` | 40 | Warning conditions |
| `info` | 30 | Normal operations |
| `debug` | 20 | Debug information |
| `trace` | 10 | Detailed tracing |
</log_levels>

<patterns>
**Structured logging:**

```typescript
// Good - structured data
logger.info({ userId, action: "login" }, "User logged in");

// Bad - string interpolation
logger.info(`User ${userId} logged in`);
```

**Error logging:**

```typescript
try {
  await riskyOperation();
} catch (error) {
  // Pass error as `err` property for proper serialization
  logger.error({ err: error, context: "riskyOperation" }, "Operation failed");
}
```

**Request logging middleware:**

```typescript
function requestLogger(req, res, next) {
  const start = Date.now();
  const log = logger.child({ requestId: req.id });

  res.on("finish", () => {
    log.info({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - start,
    }, "Request completed");
  });

  req.log = log;
  next();
}
```

**Redaction (hide sensitive data):**

```typescript
const logger = pino({
  redact: ["password", "creditCard", "*.secret", "users[*].token"],
});

logger.info({ password: "secret123" }); // password: "[Redacted]"
```
</patterns>

<transports>
**Multiple transports:**

```typescript
import pino from "pino";

const logger = pino({
  transport: {
    targets: [
      {
        target: "pino-pretty",
        options: { colorize: true },
        level: "debug",
      },
      {
        target: "pino/file",
        options: { destination: "./app.log" },
        level: "info",
      },
    ],
  },
});
```

**Custom transport:**

```typescript
const logger = pino({
  transport: {
    target: "./my-transport.js",
    options: { customOption: true },
  },
});
```
</transports>

<constraints>
**Best practices:**
- Use structured data (objects) not string interpolation
- Pass errors as `err` property
- Use child loggers for context
- Redact sensitive fields
- Set appropriate log level per environment

**Performance:**
- Pino is async by default
- Use `pino.destination()` for sync in critical paths
- Avoid logging in hot paths
</constraints>

<success_criteria>
- [ ] Logger configured with appropriate level
- [ ] Structured logging (not string interpolation)
- [ ] Errors passed as `err` property
- [ ] Sensitive data redacted
- [ ] Pretty printing in development only
</success_criteria>
