---
name: node-ops
description: Production Node.js operations advisor. Always use this skill when deploying or operating Node.js applications, handling graceful shutdown, SIGTERM, clustering, memory leaks, health checks, readiness probes, uncaught exceptions, or process management. Use when the user asks "how do I handle SIGTERM in Node.js", "graceful shutdown in Express", "how do I add health checks or readiness probes", "my Node app crashes and restarts", "uncaught exception handler", "should I use cluster mode", or "Node.js kubernetes". Read this before advising on any Node.js production or deployment topic.
---

# Production Node.js Operations

A Node.js app that works in development often has silent operational problems in production: it crashes on uncaught errors, drops in-flight requests during deploys, leaks memory over time, or gives load balancers no way to know it's ready. These are all fixable, and they should be addressed before the first production deploy, not after the first incident.

## Graceful shutdown

When a container or process manager sends `SIGTERM`, the app has a window to finish what it's doing before it's killed. If you don't handle it, the process exits immediately and drops every in-flight request.

```ts
const server = app.listen(3000);

process.on('SIGTERM', () => {
  server.close(() => {
    // connections drained — exit cleanly
    process.exit(0);
  });

  // Safety valve: force exit if drain takes too long
  setTimeout(() => process.exit(1), 10_000).unref();
});
```

`server.close()` stops accepting new connections and waits for existing ones to finish. The timeout prevents the app from hanging indefinitely if a connection never closes (e.g., a long-polling client).

For database connections, message consumers, or other resources: close them in the `SIGTERM` handler too, after the HTTP server has stopped accepting work.

## Handle uncaught exceptions and unhandled rejections

An uncaught exception or unhandled rejection leaves the process in an indeterminate state. The safest response is to log the error and exit: let the process manager restart you.

```ts
process.on('uncaughtException', (err) => {
  logger.error('Uncaught exception', err);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  logger.error('Unhandled rejection', reason);
  process.exit(1);
});
```

Don't try to continue after an uncaught exception. The state of the event loop and any in-flight work is unknown. Restart fast and restart clean.

## Liveness vs. readiness health checks

These are different endpoints with different semantics. Mixing them up causes deployment problems.

| Endpoint | Answers | Failure action |
|---|---|---|
| `GET /health/live` | "Is the process alive?" | Restart the container |
| `GET /health/ready` | "Can this instance serve traffic?" | Remove from load balancer rotation |

```ts
// Liveness: if this fails, something is fundamentally broken — restart
app.get('/health/live', (req, res) => res.sendStatus(200));

// Readiness: check dependencies before accepting traffic
app.get('/health/ready', async (req, res) => {
  try {
    await db.query('SELECT 1');
    res.sendStatus(200);
  } catch {
    res.sendStatus(503);
  }
});
```

The readiness check should fail during startup (before the DB connection is established) and during graceful shutdown (after `server.close()` is called). This prevents traffic from reaching instances that can't handle it.

## Clustering: when and how

Node.js runs on a single thread. A single instance won't saturate a multi-core machine. Options:

- **Multiple container instances** (preferred in Kubernetes/ECS): each container runs one Node process; the orchestrator handles distribution and restart. Simpler, easier to observe, and matches how most modern infra works.
- **Node cluster module**: spawns one worker per CPU core inside a single container. Works, but adds complexity: workers share no memory, IPC is manual, and a worker crash doesn't necessarily restart the master.
- **PM2 cluster mode**: wraps the cluster module with a process manager. Useful when you control the host but not the orchestrator.

In a containerized environment, prefer horizontal scaling over in-process clustering.

## Memory management

Node.js V8 has a default heap limit (around 1.5GB on 64-bit). If you need more: `NODE_OPTIONS='--max-old-space-size=4096'`. But first investigate whether you actually have a leak.

Common leak sources:
- **Event emitter listeners not removed**: `emitter.on()` without a corresponding `emitter.off()` or `{ once: true }`
- **Closures holding large objects**: a callback capturing a large request object that never gets freed
- **Unbounded caches**: in-memory maps that grow forever with no eviction
- **Timers not cleared**: `setInterval` holding a reference to objects that should be GC'd

Diagnose with `--inspect` and a heap snapshot in Chrome DevTools, or `clinic.js` for production-safe profiling.

## Environment configuration

Config belongs in environment variables, not in the repository or bundled into the process.

```ts
const config = {
  port: parseInt(process.env.PORT ?? '3000', 10),
  dbUrl: process.env.DATABASE_URL ?? throwMissing('DATABASE_URL'),
  jwtSecret: process.env.JWT_SECRET ?? throwMissing('JWT_SECRET'),
};

function throwMissing(name: string): never {
  throw new Error(`Required env var ${name} is not set`);
}
```

Fail fast at startup if required config is missing: don't let the app start and then crash on the first request that needs the config.

## Logging for production

- Use structured logging (JSON): log aggregators (Datadog, CloudWatch, Splunk) can parse and query it
- Include a correlation/request ID on every log line: essential for tracing a request across services
- Log at the right level: `error` for actionable failures, `warn` for degraded but functional, `info` for significant events, `debug` for local dev only
- Never log secrets, PII, or full request/response bodies by default

## What to watch for in code review

- No `SIGTERM` handler: process will drop in-flight requests on deploy
- `process.exit()` called without flushing logs or closing connections
- A single `/health` endpoint used for both liveness and readiness
- `uncaughtException` handler that catches and continues instead of exiting
- Large data structures cached in module scope with no eviction
- Required config accessed without validation at startup
