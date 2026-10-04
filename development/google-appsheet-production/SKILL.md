---
name: google-appsheet-production
description: Use when designing, building, modifying, securing, automating, integrating, testing, deploying, reviewing, or troubleshooting a Google AppSheet application. Produces a source-grounded implementation pack or makes verified editor changes, with data modeling, expressions, security filters, automation, performance, release, rollback, and operations gates based on live official AppSheet Help.
version: 1.0.0
author: Yash Kavaiya
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [appsheet, google-workspace, no-code, automation, security, production]
    related_skills: [computer-use, google-workspace, systematic-debugging]
---

# Google AppSheet Production Engineering

## Overview

Build AppSheet systems as production software, not as editor demos. Start from requirements and identity boundaries, model durable data, enforce row-level access with security filters, design idempotent automations, test against live-data hazards, run the deployment check, and leave monitoring plus rollback instructions.

AppSheet changes quickly. Treat official AppSheet Help as the authority and refresh the relevant pages during every substantial task. The curated map in `references/official-docs-map.md` is an index, not a substitute for a live fetch.

## When to Use

Use this skill for:

- New AppSheet apps, prototypes that must become production apps, and app rebuilds
- Data source, table, key, Ref, slice, view, action, expression, or offline/sync design
- Bots, events, processes, tasks, templates, files, email, webhooks, Apps Script, or API integrations
- Authentication, sharing, security filters, app-user versus app-creator access, governance, or licensing
- Test, deployment, version, upgrade, monitoring, performance, incident, and recovery work
- Architecture or security reviews of an existing AppSheet app

Do not use it for generic Google Workspace administration that does not involve AppSheet. For a simple conceptual answer, apply the source-freshness and security rules without generating the full delivery pack.

## Non-Negotiable Rules

1. **Official-source gate.** Before giving plan-, limit-, API-, UI-, or feature-specific instructions, fetch the relevant official page from `https://support.google.com/appsheet`. Record the page title, URL, and fetch date. If a mapped URL is gone, search again instead of guessing.
2. **No false completion.** A specification is not a built app. If the user asked to build or modify the app, make the changes in the AppSheet editor and verify them. If access is blocked, deliver an implementation pack and label it `NOT APPLIED`.
3. **Never handle credentials.** Do not type passwords, API keys, OAuth tokens, or payment details. Let the user complete sign-in and secret entry. Stop at permission, billing, destructive production-data, or broad-sharing prompts.
4. **Security is not presentation.** Slices, views, `Show_If`, `Editable_If`, and hidden actions do not establish row-level confidentiality. Use sign-in, restricted sharing, security filters, and source-level controls.
5. **No live-data surprises.** App preview is a live app and preview edits persist. Use a test copy or disposable test records unless the user explicitly authorizes production data changes.
6. **No unstated edition assumptions.** Features and limits vary by subscription and Workspace entitlement. Capture the plan and verify it against current official docs before relying on a feature.
7. **Fail closed.** Unknown identity, missing ownership data, unverified event behavior, ambiguous delete rules, and untested external responses block deployment.

## Operating Modes

Choose one mode and state it in the work log.

| Mode | Deliverable | Completion criterion |
|---|---|---|
| Blueprint | Complete implementation pack | Every required artifact exists, assumptions are explicit, and the pack validator passes |
| Editor implementation | Working AppSheet app plus implementation pack | Changes are saved, tested with representative personas/devices, deployment checks are addressed, and evidence is recorded |
| Review | Findings and remediations | Every finding includes severity, evidence, risk, exact fix, and retest |
| Incident | Root cause and recovery | Reproduction or logs identify cause, mitigation is verified, and rollback/monitoring is documented |

If the user asks to "build" without supplying editor access, begin in Blueprint mode and move to Editor implementation as soon as the signed-in editor is available.

## Phase 1 — Frame the Production Contract

Capture the following before choosing tables or views:

- Business outcome and measurable success condition
- Personas, identity provider, internal/external status, and row/action permissions
- Data classification: public, internal, confidential, regulated, or residency constrained
- System of record, data owners, expected rows now and in 12 months, write concurrency, and retention
- Devices, browser/mobile mix, connectivity, offline duration, and attachment sizes
- Required workflows, approval states, notifications, documents, integrations, and service-level expectations
- AppSheet/Workspace subscription, organization/team ownership, deployment region, and support owner
- Recovery objectives, acceptable data loss, maintenance window, and change approvers

Use `templates/app-spec.md`. Do not ask a long questionnaire when repository files, an existing app, or official documentation can answer the question. Mark unresolved items as `TBD-BLOCKING` or `TBD-NONBLOCKING`.

Completion criterion: there is a signed-off scope boundary, a persona list, a data classification, and a named owner for the app and each production data source.

## Phase 2 — Refresh Official Documentation

Run the bundled helper from the skill directory:

```bash
python scripts/appsheet_docs.py search "security filters"
python scripts/appsheet_docs.py fetch 10104488 --format markdown
python scripts/appsheet_docs.py check-catalog references/official-docs.json
```

For a substantial task, fetch at least one official source for every applicable area:

- Data/modeling
- Security/sharing
- Expressions or UX behavior
- Automation/integration
- Performance/offline behavior
- Testing/deployment/monitoring
- Licensing, limits, AI, or residency when applicable

Cite the exact pages in the implementation pack. Do not use a search-result snippet as final evidence; open the article. Community posts may help diagnose symptoms but never override official Help for security, licensing, limits, or supported behavior.

Completion criterion: `source-register.md` lists all material claims with live official URLs and a fetch date, and every link used for a blocking decision returned an article rather than a 404 page.

## Phase 3 — Design the Data Model

Follow `references/architecture-and-data.md` and produce `data-model.md`.

1. Identify the system of record for each entity. Do not create parallel truth without an explicit synchronization owner.
2. Normalize repeating groups into child tables. Model many-to-many relationships with a junction table.
3. Give every table a stable, unique, immutable key. Prefer a natural key only when immutability and uniqueness are guaranteed; otherwise use a generated ID. Never use row number as a production key.
4. Define `Ref` relationships and ownership semantics. Record whether child rows are independent or composition-owned.
5. Declare each column's type, requiredness, default/initial value, formula, validation, editability, sensitivity, and index/filter role.
6. Define lifecycle states and permitted transitions. Treat delete as a business decision; use soft delete when auditability or references require it.
7. Estimate the per-user working set. AppSheet caches working data locally; reduce the set before optimizing cosmetic UX.
8. Choose the data source based on scale, concurrency, governance, locality, backup, and plan limits—not convenience alone.
9. Plan schema migration and rollback. Regenerate table structure after source schema changes and retest expressions, automations, and integrations.

Completion criterion: every Ref resolves to a stable key; every sensitive table has an ownership/access rule; every state transition has an actor; and projected working-set size has a mitigation if large.

## Phase 4 — Build the Security Model Before UX

Use `templates/security-matrix.csv` and `references/security-governance.md`.

1. Require sign-in for confidential data or any reliable user distinction.
2. Restrict sharing to explicitly authorized users, domains, or supported groups. Public access is forbidden for internal or sensitive apps.
3. Define security filters per table using authenticated identity and trusted ownership/membership data. Test both allowed and denied rows.
4. Use slices only to shape views and permitted actions after security filtering. Never call a slice a security boundary.
5. Choose app-creator or app-user data-source access deliberately. Document what the setting exposes and which source credentials are used.
6. Protect sensitive operations at the underlying data source and integration layer. A security filter is not a complete security solution.
7. Restrict add/update/delete at both table and slice levels, then add `Editable_If`/action conditions for business rules—not secrecy.
8. Keep secrets out of expressions, template bodies, URLs, screenshots, logs, and source files. Prefer authorization headers and managed secret entry where supported.
9. Define onboarding, offboarding, ownership transfer, lost-device, cached/offline data, and emergency revocation procedures.
10. If organization governance is available, map policies for sign-in, sharing, data sources, attachments, deletion, and deployment.

Completion criterion: each persona/table/action cell in the security matrix is explicit; a denied persona cannot sync protected rows; and source-level access plus offboarding have been tested or are blocking findings.

## Phase 5 — Implement in Dependency Order

Build in this order so later behavior rests on stable foundations:

1. Data sources, tables, keys, Refs, and column types
2. Required, initial value, app formula, `Valid_If`, `Editable_If`, and `Show_If` expressions
3. Security filters and update modes
4. Slices and views
5. Actions and state transitions
6. Bots, events, processes, tasks, templates, and external calls
7. Offline/sync settings, branding, localization, and navigation
8. Monitoring, documentation, and deployment settings

For editor work, use the current editor labels visible in the UI. Official pages may describe both current and legacy navigation; do not silently mix them. After each structural change, save and resolve consistency errors before continuing.

### Editor execution protocol

- Work in the user's already signed-in browser session; never request or type credentials.
- Record the observed app name, app ID, owner, environment, and current version before changing anything.
- Use a test copy for structural, security, schema, or automation changes unless the user has explicitly approved direct production edits.
- Capture a before-state, make one coherent dependency-layer change, save, and verify the resulting editor state before proceeding.
- Do not use the AppSheet table REST API as if it authored the app definition; configure app objects in the supported editor/admin surfaces.
- Stop for new OAuth scopes, billing/subscription changes, ownership transfer, broad sharing, destructive source-data actions, or permission prompts. The authorized user must complete those steps.
- Record evidence by object name and observed result, with confidential rows and secrets redacted.

Completion criterion: no unresolved editor consistency errors; every implemented object maps to an item in the implementation pack; and names are stable and descriptive.

## Phase 6 — Engineer Expressions

Follow `references/expression-engineering.md`.

- State the evaluation context and required result type for every non-trivial expression.
- Distinguish an Initial value (computed when a row/form is initialized) from an App formula (recomputed as the row changes) and from a virtual column (computed, not stored).
- Test expressions in the Expression Assistant with normal, blank, boundary, unauthorized, and malformed cases.
- Avoid repeated scans such as broad `SELECT()` patterns in many rows. Prefer Refs/dereferences, stored values, database-side filtering, or precomputed aggregates when scale requires it.
- Keep authorization logic centralized in trusted tables and security filters. UI conditions may mirror the rule for feedback, but they do not replace enforcement.
- Document dependencies and whether a result is stored or device-local.

Completion criterion: each expression has test cases, no type warnings, and no security decision relies only on a display/edit condition.

## Phase 7 — Engineer Automations and Integrations

Use `templates/automation-inventory.csv` and `references/automation-integrations.md`.

For every bot record:

- Trigger type and exact event semantics
- Event condition, process input row, steps, tasks, and branching/wait behavior
- Idempotency key and duplicate-event behavior
- Synchronous/asynchronous choice and ordering when multiple bots can update the same row
- Retry behavior, timeout, rate/usage limit, and dead-letter/manual recovery path
- Service identity, least-privilege authorization, secret owner, and rotation procedure
- Request/response schema, status handling, correlation ID, and redacted logging
- Test fixture and monitoring owner

Do not assume direct edits to an external data source trigger an app data-change event. Verify the selected event type in current docs and with a real test. For webhooks, validate non-2xx responses, timeouts, duplicate delivery, malformed JSON, and return-value mappings. For AppSheet REST API work, verify plan support, current regional endpoint, access-key handling, URL encoding, action name, row schema, and HTTP status codes. Never expose the application access key in an artifact.

AI extraction/categorization is non-deterministic. Record current plan/credit/size/rate limits, validate output against schema and business rules, route low-confidence or unsafe cases to human review, and preserve the original input.

Completion criterion: happy path, duplicate, timeout, bad payload, denied authorization, and retry/recovery tests pass; monitor entries are visible; and no secret appears in evidence.

## Phase 8 — Design Offline, Sync, and Performance Behavior

- Decide what must work offline, what attachments must be cached, and how stale data may become.
- Test first launch online, airplane-mode read/write, queued changes, reconnect, conflicts, and revoked-user behavior.
- Treat per-user downloaded working set as a first-class budget. Security filters reduce exposure and may reduce transferred data; slices do not.
- Minimize unnecessary columns/rows, expensive virtual columns, repeated cross-table scans, and spreadsheet-side computation.
- Use an efficient data provider for the expected scale and concurrency. Verify current provider-specific behavior and limits.
- Measure with Audit History and the performance analyzer; do not declare performance from editor preview alone.

Completion criterion: sync time and working-set targets are measured on representative data/device/network conditions, and reconnect/conflict behavior is accepted by the product owner.

## Phase 9 — Test Like a Production System

Populate `templates/test-plan.csv`. At minimum cover:

- One case per persona, table, lifecycle transition, and destructive operation
- Allowed and denied row access for each security filter
- Blank, duplicate, malformed, boundary, and concurrent data changes
- Create/update/delete, Ref integrity, parent-child behavior, and schema migration
- Each view/action on phone, tablet, and browser when applicable
- Offline launch, offline changes, reconnect, and sync conflicts
- Bot condition true/false, duplicate, retry, timeout, bad response, and plan/limit failure
- API authentication, regional endpoint, encoding, status codes, and least privilege
- Accessibility, localization, dates/time zones, and attachment handling where relevant
- Performance on realistic data volume and slow network
- Backup restore, app-version restore, rollback, and ownership transfer

Use isolated test data. Remember that app preview writes to the live source. Capture evidence without secrets or sensitive rows.

Completion criterion: all critical/high cases pass; every failure has an owner and disposition; and blocked cases prevent deployment.

## Phase 10 — Deploy, Observe, and Roll Back

1. Save and resolve all consistency issues.
2. Run the AppSheet deployment check. Record each warning/error and disposition; the check is not proof that source permissions or row-security expressions are correct.
3. Confirm plan/license fit, user access, data-source permissions, ownership, privacy/terms information, and support contacts.
4. Freeze or back up the app definition and production data using separate supported mechanisms. App version history does not restore source data.
5. Choose the release mechanism supported by the current plan: direct latest version, stable-version rollout, or tested app upgrade/copy. Verify current docs before choosing.
6. Pilot with named users, watch sync, audit, performance, and automation monitors, then expand.
7. Execute post-deploy smoke tests as an end user, not only as the creator.
8. Record rollback thresholds and exact restoration steps.
9. For emergency shutdown, verify and use the current pause/stop mechanism. Do not assume that returning an app to prototype/undeployed status blocks end-user access.

Completion criterion: deployment check is clear or exceptions are signed off; pilot and smoke tests pass; monitors show expected events; and rollback has been rehearsed or verified on a test copy.

## Required Delivery Pack

Scaffold the complete pack from the bundled templates:

```bash
python scripts/scaffold_delivery.py path/to/appsheet-delivery --app-name "App Name" --mode Blueprint
```

The generated structure is:

```text
appsheet-delivery/
├── app-spec.md
├── source-register.md
├── data-model.md
├── security-matrix.csv
├── expressions.md
├── automation-inventory.csv
├── test-plan.csv
├── deployment-runbook.md
├── operations-runbook.md
└── evidence/
```

Run:

```bash
python scripts/validate_delivery.py path/to/appsheet-delivery
```

The final report must state:

- Mode and actual app status: `APPLIED`, `PARTIALLY APPLIED`, or `NOT APPLIED`
- App ID/name and environment only if directly observed
- Files created and checks performed
- Official sources and fetch date
- Tests run with pass/fail counts
- Deployment status and unresolved blockers
- Monitoring and rollback location

## Troubleshooting Discipline

1. Reproduce with a named user/app version/device and timestamp.
2. Preserve evidence: exact message, affected key, sync/audit/bot record, and correlation data—redacted.
3. Determine the failing boundary: device/app expression, AppSheet backend, data source, automation, external service, license/policy, or network.
4. Inspect Audit History, automation monitor, performance analyzer, source logs, and external service logs as applicable.
5. Form one hypothesis, run the smallest discriminating test, and record the result.
6. Fix root cause, repeat the original reproduction, then run regression and denied-access tests.

Never "fix" a sync or access problem by broadening sharing, removing sign-in, weakening a security filter, exposing source credentials, or disabling governance without explicit authorized approval.

## Common Pitfalls

1. **Using row numbers as keys.** Reordering or concurrent writes can target the wrong row. Use immutable unique keys.
2. **Treating slices as security filters.** Slices shape UX; protected rows must be excluded by security filters and protected at the source.
3. **Testing preview against production.** Preview writes persist. Use a test copy or controlled fixtures.
4. **Assuming an external source edit triggers a bot.** Event behavior depends on source/event type. Verify live docs and execute a test.
5. **Overusing virtual columns.** They are computed per row/device and can dominate sync time.
6. **Embedding credentials.** URLs, expressions, templates, and screenshots leak. Use supported secure configuration and redact evidence.
7. **Ignoring plan gates.** A configurable feature may not execute on a free or lower plan.
8. **Changing schema without migration tests.** Regenerate, repair dependent expressions/automation, and test rollback.
9. **Trusting latest-version edits in production.** Changes may reach users on sync. Use the plan-supported release strategy.
10. **Stopping at a successful bot run.** Test duplicates, partial failures, retries, side effects, and recovery.

## Verification Checklist

- [ ] Live official docs fetched and cited for every material feature/limit/UI claim
- [ ] App status is labeled without overstating what was applied
- [ ] Stable immutable keys and valid Refs defined
- [ ] Data classification, ownership, retention, and backup documented
- [ ] Sign-in, restricted sharing, security filters, and source protection tested
- [ ] Slices/UI conditions are not presented as security boundaries
- [ ] Expressions type-check and have boundary/blank/unauthorized tests
- [ ] Automations are idempotent, observable, and recovery-tested
- [ ] Secrets are absent from files, logs, screenshots, and URLs
- [ ] Offline/reconnect/conflict behavior tested when applicable
- [ ] Performance measured with realistic data and monitoring tools
- [ ] Preview/live-data risk controlled
- [ ] Deployment check, license fit, pilot, smoke test, and rollback complete
- [ ] Delivery validator passes and unresolved blockers are explicit
