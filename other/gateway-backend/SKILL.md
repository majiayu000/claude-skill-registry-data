---
name: gateway-backend
description: Route backend tasks to the right library skill. Detects intent and returns specific skill file paths to load.
type: gateway
tier: core
domains: [backend, api, services]
trigger: "backend logic, server-side code, Node.js, Go, Python, Express, FastAPI, Rust, service layer, business logic"
---

## Purpose

You are the Backend Gateway. Your job is to detect intent from the current task and return the exact library skill paths that should be loaded. Do NOT execute the task — only route to the right knowledge.

## Intent Detection → Skill Routing

Read the task description and match against these patterns:

| Intent Keywords | Load Skill |
|---|---|
| `tdd`, `test-driven`, `red-green`, `failing test first` | `skills/library/backend/developing-with-tdd/SKILL.md` |
| `debug`, `diagnose`, `trace`, `investigate`, `root cause` | `skills/library/backend/debugging-systematically/SKILL.md` |
| `auth`, `jwt`, `oauth`, `session`, `token`, `login` | `skills/library/backend/implementing-auth/SKILL.md` |
| `middleware`, `interceptor`, `pipeline`, `chain` | `skills/library/backend/writing-middleware/SKILL.md` |
| `cache`, `redis`, `memcache`, `invalidate` | `skills/library/backend/caching-strategies/SKILL.md` |
| `queue`, `worker`, `job`, `background task`, `async` | `skills/library/backend/async-job-queues/SKILL.md` |
| `websocket`, `realtime`, `socket.io`, `sse` | `skills/library/backend/realtime-connections/SKILL.md` |
| `error handling`, `exception`, `retry`, `circuit breaker` | `skills/library/backend/error-handling-patterns/SKILL.md` |
| `rate limit`, `throttle`, `ddos` | `skills/library/security/rate-limiting/SKILL.md` |

## Output Format

Return ONLY this — no prose:

```
GATEWAY_BACKEND:
Domain: backend
Skills to load:
  - [absolute/path/to/SKILL.md]
  - [absolute/path/to/SKILL.md]

Instructions: Read the above skill files before proceeding with your task.
```

If no specific skill matches, return:
```
GATEWAY_BACKEND:
Domain: backend
Skills to load: none (proceed with general backend patterns)
```
