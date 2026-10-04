---
name: generating-synthetic-test-data
description: Generate realistic synthetic data for testing data pipelines — deterministic seeded fixtures, referential integrity across tables, edge cases (nulls, duplicates, late/out-of-order events), volume for load tests, and privacy-safe stand-ins for production. Use when creating test data for pipeline/dbt tests, seeding dev environments, load testing, or replacing PII with safe synthetic data.
---

# Generating Synthetic Test Data

## When to use

- Creating fixtures for pipeline/dbt unit and integration tests.
- Seeding dev/staging with realistic, privacy-safe data instead of copying prod.
- Load-testing with high volume, or crafting edge cases on purpose.
- Do NOT use for production data generation or ML training data augmentation.

## Workflow

```
- [ ] Seed the generator for deterministic, reproducible output
- [ ] Preserve referential integrity (child keys reference generated parents)
- [ ] Include edge cases: nulls, duplicates, boundaries, late/out-of-order events
- [ ] Match production distributions where behavior depends on them
- [ ] Scale volume for load tests; keep small fixtures for unit tests
```

1. **Deterministic + seeded.** Fix the random seed so tests are reproducible;
   flaky data makes flaky tests. Small, fixed fixtures for unit tests.
2. **Referential integrity.** Generate parents first, then children referencing
   real parent keys — otherwise join/relationship tests are meaningless.
3. **Edge cases on purpose.** Include nulls, duplicate keys, boundary values,
   empty batches, and late/out-of-order timestamps so pipelines are tested against
   what actually breaks them.
4. **Realistic distributions** where logic depends on them (skew, seasonality) —
   uniform random data hides skew bugs.
5. **Privacy-safe.** Synthetic stand-ins let you test without copying PII
   (pairs with `masking-pii-data`).

## Patterns

**Deterministic, referentially-consistent generation (Python + Faker):**

```python
from faker import Faker
fake = Faker(); Faker.seed(42)                 # reproducible

customers = [{"customer_id": i, "email": fake.email()} for i in range(1000)]
orders = [{
    "order_id": n,
    "customer_id": fake.random_int(0, 999),    # references a real customer
    "amount": round(fake.random.uniform(0, 500), 2),
    "ordered_at": fake.date_time_this_year(),
} for n in range(10000)]
```

**Inject edge cases explicitly** — append rows with a null email, a duplicate
`order_id`, a zero/negative amount, and a far-future timestamp so quality checks
and dedup logic are exercised.

**dbt seeds / unit-test fixtures** — commit small CSV seeds or inline `unit_tests`
rows for deterministic model tests (`testing-dbt-projects`).

## Common pitfalls

- **Unseeded randomness** — non-reproducible, flaky tests; always seed.
- **Broken referential integrity** — orphan foreign keys make relationship tests
  pass or fail meaninglessly.
- **Only happy-path data** — the pipeline breaks on nulls/dupes/late events you
  never generated; add them deliberately.
- **Uniform distributions** — hide skew and performance issues that real,
  skewed data would surface in load tests.
- **Copying production "just this once"** — leaks PII; generate synthetic instead.
- **Giant fixtures for unit tests** — slow and hard to reason about; keep unit
  fixtures tiny, reserve volume for load tests.
