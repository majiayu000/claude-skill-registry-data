---
name: faker-data
description: Generate realistic, correctly-linked Frappe/ERPNext test records for any DocType using the `bench faker` CLI, then roll them back when done. Use when a test, demo, or local repro needs seed data and the site is missing it — e.g. "I need some Sales Orders", "seed data so I can test this API", "create test Employees in Chennai", or "populate the database to test this endpoint".
---

# Frappe Faker — Generate Test Data from the CLI

Use this skill when you need realistic, linked Frappe/ERPNext test records for a specific DocType. Faker resolves the full dependency graph, generates all linked records via LLM, and inserts them in FK-safe order. Every run produces a **Faker Batch** ID that you can use to delete all generated records when testing is done.

## Prerequisites

- The Frappe Faker app must be installed on the site
- Faker Settings must have a configured AI provider (check `/app/faker-settings`)
- The RQ background worker is **not** needed — CLI runs synchronously in the terminal

## Workflow

### 1. Inspect dependencies first

```bash
bench --site <site> faker plan --doctype "<DocType>"
```

This shows the full dependency tree without generating anything. Look for:
- `[Has data — will skip]` — existing records will be reused; no generation needed
- `[Cyclic]` — cycle detected; generation will still proceed
- `[Target]` — the DocType you requested

Example output:
```
Dependency plan for: Salary Slip

Salary Slip  [Target]
  Salary Structure Assignment
    Employee
      Department  [Has data — will skip]
    Company  [Has data — will skip]
  Salary Structure
```

### 2. Generate records

```bash
bench --site <site> faker generate \
  --doctype "<DocType>" \
  --count <N> \
  --instructions "<free-text requirements>"
```

Options:
- `--count` / `-n` — number of target doctype records (dependencies get `min(count, 5)`)
- `--skip` — comma-separated list of DocTypes to skip (e.g. `--skip "Employee,Company"`)
- `--instructions` — natural language constraints passed to the LLM
- `--no-fast-insert` — use standard `doc.insert()` path (runs Python hooks; slower)

Example:
```bash
bench --site demo.localhost faker generate \
  --doctype "Salary Slip" --count 3 \
  --instructions "Employees are software engineers in Bangalore, monthly salary 80k-120k INR, use existing company"
```

Output:
```
Generating 3 record(s) for Salary Slip...

Batch: abc123def456  |  Created: 12  |  Failed: 0
  Department: 0 created  (skipped — has data)
  Employee: 3 created
  Salary Structure: 3 created
  Salary Structure Assignment: 3 created
  Salary Slip: 3 created
```

### 3. Run your tests

Use the generated records for whatever testing or API calls you need.

### 4. Clean up

```bash
bench --site <site> faker cleanup --batch <batch_id>
```

This deletes all records from the batch in reverse dependency order (FK-safe). Use the batch ID printed by `faker generate`.

```bash
bench --site demo.localhost faker cleanup --batch abc123def456
# → Deleted 12 record(s). Status: Rolled Back
```

## Tips

- **Use `--instructions` liberally** — the LLM respects free-text constraints like dates, locations, salary ranges, roles, and relationships between records
- **Skip doctypes with existing data** — if your site already has Employees, use `--skip "Employee"` to reuse them and avoid duplication
- **Check for errors** — if `Failed > 0`, re-run with a lower count or simpler instructions; per-record errors are logged in the output
- **Batch rollback is partial-crash-safe** — if generation crashes mid-way, the batch still tracks all successfully inserted records; `cleanup` will roll back only what was tracked

## Rollback from the UI

Open the Frappe Faker web app at `/faker`, go to **History**, click a run row, and use the **Rollback** button in the detail dialog to delete that batch's records without touching the terminal.
