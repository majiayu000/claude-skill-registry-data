---
name: nick-schema-designer
description: Supabase-first database schema design for Nick's app stack. Generate production-ready Postgres schemas, Supabase SQL migrations, RLS policies, TypeScript types, seed data, role-aware access patterns, and schema checklists from plain English requirements. Use when starting any new project database, designing or reviewing schemas, adding tables, planning migrations, or turning product requirements into Supabase-ready data models. Bias toward product-led schema design, MVP discipline, core-workflow-first modeling, and avoiding premature table/role sprawl.
---

# Nick Schema Designer

Use this as the default database design skill for Nick's projects.

## Core job

Turn product strategy into a schema that supports the real workflow without overbuilding the backend.

Do not optimize for theoretical completeness. Optimize for:
- the core workflow
- trust-sensitive data handling
- clear ownership and permissions
- MVP-speed buildability
- future extension without premature complexity
- monetization and operational visibility where it actually matters

## Strategy-first schema inputs

When available, anchor schema design to:
- ICP / buyer
- end user vs economic buyer
- core workflow
- product wedge
- activation moment
- monetization model
- trust / compliance sensitivity
- MVP boundaries

If these are unclear, state assumptions and keep the schema narrow.

## Default output

Generate what is justified by the product stage. Usually include:
- Supabase SQL migration structure
- table definitions
- foreign keys and indexes
- RLS policies for exposed/user-facing tables
- role-aware access model when roles are real
- TypeScript type definitions
- seed data / seed strategy
- migration / rollout notes

Do not force complexity just to check boxes.

## Non-negotiables

- Always account for access control intentionally.
- Never leave a user-facing table without explicit policy guidance.
- Prefer Supabase SQL migrations over ORM-specific abstractions.
- Design around actual app roles, not imagined enterprise roles.
- Account for auth/bootstrap/profile flows when users exist.
- Flag multi-tenant needs explicitly.
- Call out dangerous schema decisions early.
- Model for real UI and operator flows, not abstract purity alone.
- Do not over-model v1 just because future expansion is imaginable.

## Product-led schema rules

### Model the core workflow first
Start with:
- what objects the user creates, views, changes, or acts on
- what ownership or membership rules matter
- what records prove value delivery
- what records matter for trust, auditability, or monetization

If a table does not support the core workflow, challenge whether it belongs in v1.

### Prefer narrow schemas for MVPs
For v1, usually prefer:
- one clear tenant model or no tenant model
- one clean profile/bootstrap pattern
- one role system only if required
- a small set of core business entities
- minimal support tables

Push out unless justified:
- complex role matrices
- generic workflow engines
- abstract event buses as schema tables
- extensive audit/event models with no consumer
- deep settings/preferences tables
- broad notification tables before notification behavior exists
- enterprise-style extensibility layers

### Model monetization only where it matters
Include monetization-relevant records when the product needs them, such as:
- subscriptions / plans
- usage or quota records
- billable actions
- leads / conversions / demos / requests
- operator actions tied to revenue outcomes

Do not add monetization tables by default if the current product stage does not need them.

### Design permissions from reality, not optimism
Separate clearly when relevant:
- unauthenticated visitor
- signed-in user
- operator / manager
- admin / owner
- organization member roles

If the app only needs one or two roles in v1, do not invent five.

## Default workflow

1. Read the product requirements.
2. Identify the core workflow and value-producing actions.
3. Identify users, roles, and permissions that actually matter.
4. Identify tenant model if relevant.
5. Identify the minimum core entities and relationships.
6. Design normalized schema with pragmatic denormalization where useful.
7. Add indexes and constraints intentionally.
8. Write RLS policies table by table where applicable.
9. Generate TypeScript types.
10. Generate realistic seed data or a seed strategy.
11. Provide rollout/testing notes and call out assumptions.

## Required design sections

For each schema design, include:
- Product summary
- Core workflow summary
- User roles
- Main entities
- Relationships
- Tables
- RLS / access plan
- Migration SQL
- TypeScript types
- Seed strategy
- Risk / edge-case notes
- Policy test notes
- Migration ordering / rollout notes
- Storage policy notes if uploads exist

## Supabase defaults

- `auth.users` is the source of authenticated identity
- app profile/bootstrap table should be explicit when needed
- use UUIDs unless there is a strong reason otherwise
- use `created_at` and `updated_at` on app tables by default
- use `deleted_at` only when soft delete is truly needed
- use RLS intentionally, not mechanically
- separate public client access from privileged/service-role operations
- design for real UI flows and operational workflows

## When not to over-model

Challenge or remove these unless the product clearly needs them now:
- separate tables for every future concept
- role tables when a simple enum/member pattern works
- audit tables with no actual audit consumer
- elaborate billing models before billing exists
- multiple tenancy modes in v1
- complex state machines without real workflow pressure
- settings tables for preferences that can live elsewhere for now

## Access and RLS rules

When writing policies, define explicitly:
- who can read
- who can insert
- who can update
- who can delete
- whether access is row-owned, tenant-scoped, role-scoped, or admin-scoped

Prefer policies that are easy to reason about and test.

If policy logic becomes complicated, question whether the schema or role design is too complex for the current stage.

## Seed data rules

Seed enough data to test:
- the main happy path
- role-specific visibility when applicable
- filters, sorting, and empty states
- realistic operator/admin views
- monetization or workflow states if relevant

Do not generate toy seed data that fails to exercise the real product.

## Output style

When designing or reviewing a schema, structure the response around:

### Product frame
- user / buyer
- core workflow
- MVP boundary

### Data model
- core entities
- relationships
- ownership / tenant model

### Access model
- roles
- row-level visibility / write rules
- admin/operator exceptions

### Migration plan
- table order
- bootstrap assumptions
- rollout cautions

### Risks
- over-modeling risk
- policy complexity risk
- trust/compliance risk
- scaling assumptions that may be premature

## Quality bar

A strong schema response should:
- map tightly to the real product workflow
- include enough structure to ship confidently
- avoid premature table and role sprawl
- support trust-sensitive and monetization-relevant flows where needed
- make policies understandable and testable

## References

Read these as needed:
- `references/schema-workflow.md` for the end-to-end process
- `references/rls-patterns.md` when writing access policies
- `references/table-template.md` when structuring table specs
- `references/common-patterns.md` for auth/profile/tenant defaults
- `references/review-checklist.md` before finalizing schema output
- `references/multi-role-planning.md` when multiple roles actually matter
- `references/migration-conventions.md` when sequencing changes matters
- `references/policy-test-template.md` for RLS verification structure
- `references/storage-patterns.md` when uploads/storage are part of the product

## Bundled scripts

- `scripts/init_schema_design.sh` — create a schema design stub
- `scripts/generate_table_spec.sh` — create a table spec stub
- `scripts/generate_migration_checklist.sh` — create rollout/test checklist
- `scripts/generate_policy_test_checklist.sh` — create an RLS verification checklist for a table
- `scripts/generate_seed_plan.sh` — create a realistic seed-data planning stub
- `scripts/generate_storage_policy_stub.sh` — create a Supabase Storage policy stub
