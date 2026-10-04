---
name: seed-data-and-fixtures
description: Use when creating demo data, test fixtures, seed scripts, or factory functions, when preparing for a sales demo and the screenshots are full of "John Doe", when test data is missing edge cases, or when seed scripts crash on a second run.
---

# Seed Data and Fixtures

## Overview

Produce realistic data for demos, dev environments, and tests — *before* lorem ipsum makes it to a screenshot. Output is `.forge/seed-data.md` (the entity inventory, distributions, demo scenarios, and the factory contract) plus the seed scripts themselves. Seeds must be **realistic** (real-feeling names, plausible timestamps, domain-appropriate content), **comprehensive** (edge cases included), **reproducible** (seeded RNG), and **idempotent** (re-runnable without dupes). Consumed by `incremental-implementation` (factories for tests), `demo-narrative` (demo scenes), and `testing-strategy` (golden-test fixtures).

## When to Use

- A new dev environment is being set up and there's no seed data
- A demo is coming up and the screenshots have lorem ipsum or "Test User"
- Test fixtures are inconsistent across the test suite — every test rebuilds its own data
- A bug only reproduces with specific data and no seed covers that case
- Multiple developers are stepping on each other's seed data in shared dev DB

## When NOT to Use

- Production data migration — that's `database-design` + a one-off backfill ADR
- Schema design — that's `database-design`
- Loading anonymized production data for analytics — separate concern, distinct safety rules

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Lorem ipsum is fine for now" | Lorem ipsum in a demo makes the product look fake. The buyer notices in 4 seconds and you've already lost the deal. |
| "Just use 'Test User'" | Homogeneous seed data hides bugs that only appear with real-world variance — long names, accents, no last name, multi-byte chars, all-caps. |
| "Seeds don't need to be idempotent" | Non-idempotent seeds crash on the second run and corrupt the dev DB. Every developer ends up with a different shape. |
| "Edge cases in seed data are overkill" | The bug you ship is always in the edge case you didn't seed. Empty list, single item, 10k items, missing optional field, deleted-but-referenced. |
| "We can use production data, it's anonymized" | Anonymization is not a checkbox. Re-identification from indirect identifiers is trivial. Use synthesized data. |
| "Timestamps don't matter, just use now()" | All-now() timestamps hide ordering bugs, time-based logic bugs, and "what does this look like with a year of history" bugs. |

## Red Flags

- Lorem ipsum visible in a screenshot, demo, or recording
- Every seeded user named "John Doe", "Test User", or `user1` / `user2`
- All `created_at` timestamps within seconds of each other
- A seed script that errors on a second run (unique constraint violation)
- No edge-case scenarios: no empty states, no overflow, no missing-optional-field
- Production PII (real emails, names, phone numbers) checked into the seed file
- A demo that requires the demo-runner to "set up the data manually first"
- Factories that don't allow overrides — every test gets the same default user

## Core Process

### Step 1: Inventory entities needing seed

Read `.forge/architecture.md` and `.forge/database-design.md`. List every entity that needs seed data, with the minimum count for a realistic dev environment (e.g., 50 users, 200 tasks per user, 20 organizations, 5k events).

### Step 2: Define realistic distributions per field

For each entity, decide what "realistic" means:

| Field | Naive | Realistic |
|---|---|---|
| Name | "John Doe" | A pool of 200+ first + last names spanning cultures, lengths (1 char to 30+), with hyphens, apostrophes, multi-byte chars |
| Email | `user1@test.com` | `firstname.lastname@<plausible-domain>` with the same distribution as names |
| Timestamp | `now()` | Spread across the last 90 days with a realistic curve (more recent = denser) |
| Status | All `active` | Weighted: 70% active, 15% pending, 10% archived, 5% suspended |
| Content | "lorem ipsum" | Domain-appropriate (e.g., task titles like "Review Q3 budget", "Onboard new hire", "Fix flaky integration test") |
| Count fields | All 0 or all 100 | Long-tail distribution: many users with 1-5 items, a few with 50+, one with 500+ |

### Step 3: Write factories with overrides

Every entity has a factory: `createUser(overrides?: Partial<User>): User`. Defaults from the distribution; overrides allow tests and demos to pin specific fields.

```ts
const user = createUser({ email: "demo@example.com", status: "active" });
const power = createUser({ taskCount: 500 });  // edge case
```

Factories use a seeded RNG (e.g., `seedrandom`) so the same seed produces the same data — critical for reproducible demos.

### Step 4: Write demo-specific scenarios

For each demo scene in `.forge/demo-narrative.md` (or for each test-needed shape):

- **Happy path scenario** — the buyer-facing flow
- **Empty state scenario** — fresh user, no data
- **Single-item scenario** — one of everything
- **Overflow scenario** — long names, long content, many items
- **Error state scenario** — failed payment, expired card, locked account

Each scenario is a named function: `seedDemoOnboardingScene()`, `seedDemoPowerUserScene()`. The demo script runs the named scene.

### Step 5: Make idempotent

Seeds upsert by a **stable key** — typically a slug or a UUIDv5 derived from a deterministic input. Re-running the script reconciles: missing rows are inserted, existing rows are updated, drift is corrected.

```ts
upsert("users", { stable_id: "demo:onboarding:alex" }, { ... });
```

The seed script can be run before every demo with confidence.

### Step 6: Version + document in `.forge/seed-data.md`

- Inventory of entities + counts
- Distribution rules per field
- Factory API summary
- Named demo scenarios
- The stable-key naming convention
- The PII safety rule (no production data, ever)

## Verification

- [ ] `.forge/seed-data.md` written
- [ ] Zero lorem ipsum anywhere in seed output (grep verified)
- [ ] No `John Doe`, `Test User`, or `user1` in any seeded user
- [ ] Names span cultures, lengths, and character sets
- [ ] Timestamps spread across a realistic window with a realistic curve
- [ ] Every demo scene in `.forge/demo-narrative.md` has a corresponding `seedDemo<Scene>()` function
- [ ] Edge cases seeded: empty list, single item, overflow, error state
- [ ] Seed script runs twice without errors (idempotency tested in CI)
- [ ] No production PII (real emails, names, phone numbers) checked into the seed file
- [ ] Factories accept overrides for every field
