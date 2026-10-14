---
name: craft-job
description: Crafting Jobs. Queue orchestration, not business logic.
---

# Skill: Craft Job

> "Jobs are just another way of exposing business functionality to the outside world."

## The Standard

1. **Application Layer**: Jobs belong in App, not Domain. Like controllers.
2. **Delegate to Actions**: Business logic lives in Actions. Jobs orchestrate.
3. **Queue Configuration**: Jobs manage retries, delays, chaining—workflow, not logic.
4. **Prefer Queueable Actions**: For simple cases, skip the job class entirely.

## The Anti-Patterns

| ❌ Don't                     | ✅ Do                              | Why                          |
|-----------------------------|-----------------------------------|------------------------------|
| Business logic in `handle()` | Call `Action->execute()`          | Jobs aren't domain code      |
| One job per action          | `Action::onQueue()->execute()`    | Eliminates boilerplate       |
| Complex job chains          | Orchestrator action               | Testable, debuggable         |
| Domain namespace            | App\Jobs namespace                | Respects layer boundary      |

## Real-World Examples

See [examples.md](examples.md).
