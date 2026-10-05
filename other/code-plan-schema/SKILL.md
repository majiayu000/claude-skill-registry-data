---
name: code-plan-schema
description: Design database schemas, ORM models, migrations, and data relationships. Use when asked to plan schema or persistence changes.
---

Generate an actionable schema design plan based on task analysis and research.

## Process

### Step 1 - Identify Context

- Inspect changed files with `jj diff -s`; restrict with `jj diff -- path`.
- Focus on user-specified entities, tables, models, migrations, or relationships.
- Identify the database, ORM/framework, migration tooling, and existing data model.

### Step 2 - Research and Scout

Apply a scout lens to analyze existing schema artifacts for {task} (schema definitions, migrations, models, query code, tests, persistence conventions):

- Map relevant files, conventions, and call paths; cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs; stay read-only and task-relevant.

Apply a researcher lens to research official database/ORM documentation relevant to {task} (migration constraints, performance, security):

- Prefer official documentation over blog posts; cite sources with URLs.
- Separate confirmed facts from plausible interpretations; note version requirements.
- Lead with the single most actionable recommendation.

- For schemas affecting data flow or cross-module boundaries, apply an architect lens to analyze data flow, ownership, dependency direction, and migration shape for {task}:
  - Map current boundaries, ownership, and dependency direction first.
  - Recommend the smallest architecture/schema that preserves invariants.
  - Avoid speculative generality.

Apply a planner lens to design a minimal schema plan for {task} (relationships, indexes, constraints, migrations, alternatives, tradeoffs):

- Prefer simple, boring solutions; preserve existing project patterns.
- Make tradeoffs and assumptions explicit; scope to the current problem.

Apply a reviewer lens to review the proposed schema for correctness, data integrity, security, performance, simplicity, and project-convention risks:

- Ground findings in file paths and line numbers; prioritize the requested lens.
- Distinguish confirmed findings from speculative risks; explain why each issue matters.

### Step 3 - Adjudicate Decisions

- For high-impact or conflicting schema decisions, apply an oracle lens to adjudicate the conflicting schema recommendations for {task}:
  - Identify the decision; state assumptions and constraints.
  - Pick the smallest safe path that preserves future options.
  - Note what evidence would change the recommendation.

### Step 4 - Audit

- For production-bound schema changes, apply an auditor lens to audit the schema plan for {task} for production risks:
  - Data loss, migration hazards, rollback safety, and contract compatibility.
  - Flag only material risk; this is a final gate, not iterative style review.

### Step 5 - Validate Findings

- Read relevant code yourself and validate findings.

### Step 6 - Design Schema

- Define only required tables, entities, and fields; avoid generic or over-flexible schemas.
- Account for indexes, constraints, migrations, normalization, and N+1 query risks.
- When mapping objects to tables or modeling relationships, read the `martin-fowler-eaa-patterns` reference and apply its O/R structural and metadata patterns: choose Single/Class/Concrete Table Inheritance for hierarchies, Association Table Mapping for many-to-many, Embedded Value for small owned objects, and Identity Field for object identity; consider Lazy Load and Identity Map for N+1 and consistency.
- Identify security and privacy risks for stored data.

### Step 7 - Report

1. **Context Analysis** — existing schema/model structure, query patterns, integration points.
2. **Security Considerations** — data exposure, tenant boundaries, privacy, integrity risks.
3. **Documentation & Best Practices** — database/ORM constraints; common migration pitfalls.
4. **Simplicity Constraint** — minimal required entities and fields; over-engineering risks.
5. **Schema Design** — tables/entities/fields, relationships, indexes and constraints, migration/backfill considerations.
6. **Implementation Plan** — numbered concrete steps, file targets, verification strategy.

Prioritize actionable, specific guidance over abstract advice.
