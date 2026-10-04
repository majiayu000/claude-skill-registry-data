---
name: healthcheck
description: Verify whether the second brain can retrieve current context, reach important sources, execute useful workflows, and support recurring behavior.
---

# Healthcheck

This is a verification review, not a score-chasing exercise.

Read `SYSTEM.md`, the core workspace files, source registry, decision journal, installed skills, and recent healthcheck reports if present.

Create a new report under:

`reviews/healthcheck-YYYY-MM-DD-HHMM.md`

## Review areas

Assess five areas using only these statuses:

- `PASS` — directly verified with current evidence.
- `PARTIAL` — some useful behavior works, but meaningful coverage is missing.
- `UNKNOWN` — documented but not verified.
- `FAIL` — a required route or behavior is demonstrably broken.

### 1. Core context
Can a fresh session answer:
- who this is for,
- what matters now,
- who is served,
- important working preferences,
without relying on this chat?

### 2. Retrieval
Run four realistic retrieval probes tied to the user's actual work:
- current objective or commitment,
- an active project or deliverable,
- a prior decision or lesson,
- an important original file or external record.

For each probe, record the declared route, evidence found, and whether fallback search was needed.

### 3. Source access
For each important source in `workspace/sources.md`, record:
- what it is authoritative for,
- access method,
- last successful read or dated evidence,
- known limitations.

Configuration alone is not proof of access.

### 4. Workflow execution
Select up to three workflows that matter to current objectives. Look for:
- clear trigger,
- inputs,
- useful output,
- validation,
- failure handling,
- evidence of an actual run.

### 5. Recurring behavior
Inspect any schedules, hooks, automations, or explicit human routines. Distinguish:
- documented intent,
- enabled trigger,
- evidence that the expected output actually happened.

## Report format

Start with a one-paragraph conclusion.

Then include:
1. status table for the five areas,
2. four retrieval probes,
3. source access table,
4. up to three workflow checks,
5. concrete issues grouped as:
   - broken,
   - unverified,
   - optional improvement,
6. up to three next actions with a clear completion test.

Do not manufacture problems to fill the report.
