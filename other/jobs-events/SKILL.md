---
model_tier: medium
name: jobs-events
description: "Use when creating Laravel jobs, queued workflows, events, or listeners. Covers clear responsibilities, safe serialization, and retry/failure handling."
domain: engineering
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# jobs-events

## When to use

Use when creating jobs, events, listeners, or queued workflows.

Do NOT use when:
- Artisan commands (use `artisan-commands` skill)
- Scheduling configuration (use `laravel-scheduling` skill)

## Procedure: Create a Job

### Step 0: Inspect

1. Check existing jobs — match naming, queue config, retry strategy, failure handling.
2. Determine sync vs. async — only queue work that is slow, retryable, or non-blocking.
3. Check queue driver: `.env` / `config/queue.php` (Redis, database, sync).
4. Check Horizon: `config/horizon.php` for queue names, supervisors, balancing.

### Step 1: Create the job class

1. Pass IDs or compact DTOs in constructor — not full models with relations.
2. Set queue via `$this->onQueue(Queue::NAME->value)`.
3. Add `tags()` for Horizon filtering.
4. Set `$maxExceptions`, `backoff()`, `$uniqueFor` as needed.

### Step 2: Implement handle()

1. Keep focused and readable.
2. Delegate complex logic to services/actions.
3. Design for idempotency — retries must not create duplicates.

### Step 3: Test

- `Bus::fake()`, `Queue::fake()`, `Event::fake()`.
- Test side effects, not just dispatch assertions.

## Procedure: Create an Event + Listener

### Step 1: Create event

- Past-tense naming: `OrderPlaced`, `ImportCompleted`.
- Keep payload focused.
- Laravel 11+: automatic discovery — no manual registration.

### Step 2: Create listener

- One responsibility per listener.
- Delegate large logic to services.
- Use `ShouldQueue` on listeners that do heavy work.

## Conventions

→ See guideline `php/jobs.md` for full conventions (serialization, idempotency, events, dispatching).

## Output format

1. Job/Event/Listener class(es) with proper serialization and retry config
2. Event registration in EventServiceProvider if needed

## Gotcha

- Without `ShouldQueue`, jobs run synchronously.
- Queued jobs serialize constructor args — don't pass loaded models.
- Listener exceptions block the event chain — queue heavy listeners.
- Set `$tries` and `$backoff` — unlimited retries overwhelm the queue.

## Do NOT

- Do NOT serialize Eloquent models with loaded relations into queued jobs.
- Do NOT ignore idempotency — retries must not create duplicates.
- Do NOT hide critical business flows behind deep listener chains.

## Auto-trigger keywords

- Laravel job
- queue
- event
- listener
- dispatch
- serialization
