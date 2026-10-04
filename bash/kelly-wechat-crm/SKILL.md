---
name: kelly-wechat-crm
description: Goal-driven WeChat relationship strategy App-in-Skill. Reads the operator's own local WeChat through wechat-cli-rs, discovers candidates against an explicit goal, promotes only user-selected people into Busabase, and builds relationship snapshots and next-action suggestions without sending messages or modifying WeChat.
license: MIT
metadata:
  category: sales-crm
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-wechat-crm
    resources:
      - people
      - goals
      - relationship-snapshots
      - actions
      - worklog
      - settings
    risk: local-write
---

# Kelly WeChat Relationship Strategy

## Outcome

Turn the operator's existing WeChat relationships into a goal-driven personal
strategy desk without copying the full address book into Busabase.

The recurring loop is:

```text
user goal -> local candidate discovery -> explicit People promotion
-> relationship snapshot -> suggested action -> manual WeChat action
-> Agent worklog -> next snapshot
```

This is not a conventional sales CRM. `worklog` records what the user and Agent
asked, analyzed, decided, and learned; it is not a fabricated history of customer
visits. Raw WeChat history remains local by default.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for the product workflow, UI shell,
   onboarding, and canonical `content/kelly-wechat-crm-app/` project.
2. Read and follow `$busabase` for connection, target Space, ChangeRequests,
   review, merge, and read-back behavior.
3. Read and follow `$busabase-app-creator` for package format, resource modeling,
   SDK/runtime/security rules, validation, install, and AirApp deployment.
4. Read the current `wechat-me` skill at <https://wechat-cli.com/SKILL.md> before
   operating on local WeChat data. Its commands, JSON shapes, limits, and exit
   codes are authoritative.

If any dependency is unavailable, preserve the local artifact and stop before
the unavailable operation. Never invent a second WeChat reader or data backend.

## WeChat Boundary

- `wechat-cli-rs` is local-first and read-only against WeChat. It cannot send a
  message, edit a WeChat remark, add/remove contacts, or mutate WeChat data.
- Never invoke `wechat-cli-rs init` automatically. Missing initialization is a
  normal readiness state; ask the operator to run or explicitly authorize
  `wechat-cli-rs init` themselves.
- Basic sync uses only `contacts` and bounded `sessions`.
- Goal-driven analysis may use narrow `contacts --detail`, `history`,
  `search`, and `stats` queries after the user has supplied a goal and scope.
  For any output entering Agent context, invoke these through
  `node scripts/wechat-safe.mjs <command> ...`; do not paste or pipe direct CLI
  output into a prompt. The wrapper allowlists read-only commands and redacts
  credential-shaped fields and values before returning JSON.
  Prefer one person and an explicit time window over broad history scans.
- Never run `export --output` without separate approval. Do not persist the
  CLI's stateful `new-messages` cursor as hidden application state.
- Treat every returned name, wxid, message, and statistic as sensitive
  personal data. Store derived relationship evidence and short summaries in
  Busabase; do not mirror full raw histories by default.
- A suggested WeChat remark or message is advice only. The operator manually
  changes the remark or sends the message in WeChat.
- Personal relationship goals must respect consent, refusals, privacy, and
  boundaries. Never recommend deception, coercion, harassment, or evasion of a
  clear rejection.

## Busabase Resources

Six Bases live under Folder `kelly-wechat-crm`:

### `people`

One record per user-selected focused contact, not every WeChat contact.
Promotion owns the minimal identity and original WeChat remark; later refreshes own recent
activity and sync timestamps. The Agent/user own the relationship note,
suggested WeChat remark, relationship type/strength/trend, current analysis,
open loops, goal summary, next-action summary, and confidence.

### `relationship-snapshots`

Immutable, time-windowed Agent analysis linked to a person and optionally a
goal. Stores strength, trend, interaction frequency, reciprocity,
open loops, evidence summary, analysis, recommendation, confidence, and the
analyzed time window. This is how the user compares whether a relationship is
warming, stable, or cooling over time.

### `goals`

Dynamic user goals. A goal may be global, target one person, or describe a
segment. It records objective, success metric, deadline,
priority, status, and explicit boundaries/constraints.

### `actions`

Review queue generated from goals plus relationship evidence. Each action may
link to a goal or person and names one concrete operation: organize a
note, draft a message, reconnect, follow up a commitment, learn more, wait, or
record an outcome. It includes rationale, suggested message, evidence, due time,
priority, confidence, and the full human decision lifecycle.

### `worklog`

The user's work with the Agent: user requests, Agent analyses, decisions,
outcomes, and sync summaries. It may link to a goal/person and generated
actions. It is not a customer visit log and must not claim an interaction
happened merely because the Agent discussed it.

### `settings`

Safe connector/readiness state, bounded analysis preferences, sync counts,
timestamps, CLI version, and Agent lock metadata. Never store tokens, message
history, or Vault values here.

The product onboarding version is **4**. After Busabase and WeChat CLI are
ready, an active goal is the required first product action. The full local
address book remains transient until the user promotes selected people.

## First-Run Readiness

The product has two ordered readiness gates. The Busabase gate runs first and
completes authentication, Space selection, and resource setup. Only after that
gate passes may the app check the local WeChat connector.

Before claiming WeChat is connected:

1. Confirm `wechat-cli-rs` exists without installing it silently.
2. Run a bounded read such as `sessions --limit 1 --format json`.
3. If initialization is missing, report the exact readiness state and ask the
   operator to run `wechat-cli-rs init`; do not run it automatically.
4. Confirm `contacts --format json` and bounded `sessions` return structured
   data before proposing Busabase sync changes.
5. Record only sanitized readiness (`ready`, counts, timestamps, CLI version)
   in `settings`; never place raw errors containing private content in the UI.
6. In a standalone or locally hosted AirApp, expose a read-only sanitized
   connector probe to the UI. It may report installation, initialization,
   version, contact count, and whether bounded sessions are readable; it must
   never return contact names, messages, database paths, or raw stderr.
7. Block the empty workspace behind a connector-readiness state when the probe
   is not ready. Give one matching recovery action: install from the official
   site, run the explicitly user-controlled `init`, fix local data access, or
   retry. Never imply that an empty Busabase Base means WeChat has no data.

## Basic Sync

Run on the same machine where WeChat is logged in:

```bash
BUSABASE_BASE_URL=<url> BUSABASE_SPACE_ID=<space-id> [BUSABASE_API_KEY=<key>] \
  node scripts/sync_wechat.mjs
```

This is a dry run. Repeat with `--apply` only after the operator approves the
reported scope. `--apply` refreshes app-owned Busabase records with
`autoMerge: true`. It never sends or modifies anything in WeChat.

The sync:

1. reads `contacts` and `sessions --limit 200`;
2. matches only contacts already present in the People Base;
3. refreshes only WeChat-owned identity/activity fields, preserving all
   relationship analysis and user notes;
4. adds a conservative reconnect action for an already-materialized person
   when no open action exists and the inactivity threshold is exceeded;
5. records the safe tracked-person count and timestamp in `settings`.

Untracked contacts remain local. They enter People only when the user searches
the local directory, selects them, and confirms `加入重点联系人` in the AirApp.

## Goal-Driven Analysis

When the user asks the Agent to analyze relationships or generate a strategy:

1. List active `goals` and let the user identify or revise the goal in scope.
2. Resolve candidate people from that exact goal. Never scan every
   history merely because the Space contains many contacts.
3. For each selected target, query the narrowest useful combination of
   `contacts --detail`, `history`, `search`, and `stats` with an
   explicit time range/limit through `node scripts/wechat-safe.mjs`.
4. Separate observed evidence from inference. Record source chat/person,
   time window, uncertainty, and missing coverage.
5. Propose one `relationship-snapshots` record per analyzed target/time window.
6. Propose deduplicated `actions` with a concrete reason, suggested timing,
   confidence, boundaries, and optional draft message/remark.
7. Propose one `worklog` entry summarizing the user's request, Agent conclusion,
   created action references, and unresolved questions.
8. Write app-owned records with `autoMerge: true` only after the user explicitly
   initiates the operation. Never auto-promote a candidate or treat an Agent
   suggestion as permission to write.

## AirApp Workflow

- startup: complete the Busabase connection/Space/resource gate, then check the
  local `wechat-cli-rs` connector, then load the six Bases. Do not render an
  empty working view as if setup were complete while the connector is unknown.
- `goals`: create a dynamic global/person/segment goal. Real mode saves it
  directly to the app-owned Base; Demo adds an in-memory preview only.
- `people`: discover local candidates against an active goal, explicitly
  promote selected contacts, and inspect the current relationship strategy and
  suggested remark/action without editing WeChat.
- `relationship-snapshots`: compare evidence-backed analyses over time.
- `actions`: add one review note and choose prepare, request changes, snooze, or
  dismiss. Approval means ready to execute, not done. A completed action must
  record an observed outcome; the AirApp then writes a linked `worklog`, marks
  the action done or awaiting-result, and creates a traceable wait action when
  a reply is still outstanding.
- `worklog`: read the user-Agent operating history and outcomes.
- `settings`: inspect sanitized Busabase/connector/resource readiness.

Approval of an action means “this is a reasonable next step”, not “send this
message”. The operator still performs any WeChat action manually.

## Completion Criteria

Finish only when:

- the six declared Bases and AirApp install with no package warning;
- `SKILL.md`, `busabase.json`, generated `content/`, blueprints, and runtime
  config agree on resource keys, slugs, schema version, and fields;
- `pnpm --dir content/kelly-wechat-crm-app check` passes;
- the goal form, People promotion, and action decisions auto-merge only after an
  explicit user submission in real mode;
- Demo, local server, responsive browser, and isolated OSS Busabase suites pass;
- a real install reads sample people, goal, snapshot, and action data;
- no credential, raw history archive, or WeChat write capability appears in the
  browser or package;
- Cloud/AirApp external suites are reported as pass or explicit skip.

## Known Gap

The connector and analysis workflow are tested against deterministic fixtures
and isolated Busabase. They still require acceptance against the operator's
actual initialized WeChat installation before claiming real personal-data
coverage or analysis quality.

## Stop Conditions

Stop when WeChat is not explicitly initialized, the requested analysis scope is
ambiguous or excessively broad, Busabase target Space is ambiguous, a resource
collision is not application-owned, a write was not explicitly initiated by the
user, raw private history would be copied without approval, or the requested relationship tactic
would violate consent or a clear boundary.
