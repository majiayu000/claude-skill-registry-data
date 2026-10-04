---
name: wiring-audit
description: Post-build integration gate and diagnostic scan for disconnected ChefFlow work. Use after every build, when user says /wiring-audit, "wire audit", "what's disconnected", "find orphans", "dead code check", or before marking feature/page work done.
---

# WIRING-AUDIT

## Purpose

Make every build prove it is connected to the ChefFlow nervous system before anyone says done.

This is the single post-build closeout skill. It subsumes the old build-completion triad:

1. Page X-Ray
2. Dinner Circles wiring
3. Universal Rail Intelligence wiring

It also checks the other integration domains that commonly get missed.

## Required After Every Build

Run this after any code build, feature change, page change, route change, UI workflow change, server action change, resolver change, or domain integration change.

Do not wait for the developer to ask. Builders, Codex, Claude main sessions, and sub-agents must include this in done-when criteria.

## Phase 1: Mechanical Scan

Run:

```bash
node scripts/wiring-audit.mjs
```

Read `scripts/wiring-audit-results.json`, especially:

- `orphans`
- `weak`
- `post_build_domain_matrix.changed_files`
- `post_build_domain_matrix.affected_routes`
- `post_build_domain_matrix.domains`

The matrix ranks which integration domains are relevant to the build based on changed files and domain keywords.

## Phase 2: Page X-Ray

For each affected route from the matrix:

- Existing page: run `/page-xray {route} --delta`
- New page: run `/page-xray {route} --quick`
- Rail-heavy page: add `--rail-only`
- Security-sensitive page: add `--security-only`

If a route changed but has no X-Ray record, create one. Page X-Ray findings are build evidence, not optional notes.

## Phase 3: Domain Relevance Matrix

For every domain ranked `high` or `medium`, answer the checks below with evidence or a clear N/A reason.

| Domain                            | Trigger examples                                             | Required wiring proof                                                               |
| --------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Page X-Ray                        | `app/`, page, route, layout, UI surface                      | X-Ray run, open findings handled or recorded                                        |
| Universal Rail Intelligence       | page, route, intel, resolver, rail profile                   | `lib/discovery/rail-profiles.ts` profile and resolver coverage                      |
| Dinner Circles                    | event, inquiry, client, guest, staff, recurring, hub, circle | `ensure*Circle()`, `create*Circle()`, or circle feed hook at relationship formation |
| Priority Queue and Action Graph   | next action, waiting, blocker, urgency, queue                | surfaced task/action with source, urgency, due state, deep link                     |
| Commitment UI and Completion      | quote, booking, deposit, readiness, confirmed, accepted      | commitment/completion state updated and visible                                     |
| Client Intelligence               | client, household, preference, repeat, dietary               | client intelligence ledger or summary receives relevant facts                       |
| Menu Intelligence                 | menu, recipe, dish, approval, dietary                        | menu intelligence surface receives decisions, risks, and approvals                  |
| PIE and Pricing Intelligence      | ingredient, recipe cost, quote, margin, procurement          | PIE used or explicit non-applicable reason, no fake zero pricing                    |
| Communications and Notifications  | message, email, SMS, inbox, reply, notification              | correct party notified or feed/inbox updated without duplicates                     |
| Event Lifecycle and FSM           | event status, transition, lifecycle, handoff                 | canonical transition path and dependent surfaces updated                            |
| Ledger, Finance, Payments         | payment, invoice, billing, Stripe, revenue                   | immutable ledger/payment records and finance summaries updated                      |
| Remy, Navigation, Command Surface | new route, action, nav, shortcut, Remy                       | discoverable entry point or justified local-only action                             |
| Automation and CIL                | signal, automation, insight, continuous intelligence         | durable signal, automation hook, freshness, suppression rules                       |

If the matrix misses an obvious domain, add it manually. The script is a first pass, not an excuse.

## Phase 4: Orphan and Reachability Audit

Use the route audit results:

- `ORPHAN`: route has no inbound references. Add a nav, command, Remy, redirect, rail, or local workflow entry if the route is meant to be live.
- `WEAK`: route has only one weak reference. Verify this is intentional.
- Uncalled server actions, unmounted components, and exported utilities with no consumers must be classified as live gap, WIP, test-only, tooling-only, or future.

Never delete orphaned code during audit. Wire clear live gaps, queue unclear work, or record why it is intentionally unwired.

## Phase 5: Finish Criteria

A build can only be called done when:

- Page X-Ray ran for affected routes or the proof pack explains why no route was affected.
- Every `high` or `medium` matrix domain has evidence, a fix, a queued follow-up, or a clear N/A reason.
- Dinner Circles, Universal Rail, Priority Queue, commitment/completion, Menu Intelligence, PIE, and Client Intelligence were explicitly considered when relevant.
- No live route remains orphaned without a reason.
- The proof pack or final closeout lists wire-audit results, affected routes, relevant domains, remaining gaps, and verification commands.

If any required wiring is missing and the correct connection is obvious, fix it before closeout. If it needs product judgment, add or update a queue item instead of pretending it is done.
