---
name: ha:challenge
description: Challenge mode reviews - rigorous questioning before approving changes. Use when you want thorough scrutiny of coordinator/registry changes, Lit events / websocket messages, coordinator/service designs, or PR readiness.
effort: high
argument-hint: coordinator | lit | pr
---

# Challenge Mode Reviews

Rigorous, critical review patterns inspired by Boris Cherny's "Grill me" approach. Push beyond first solutions to ensure quality.

## Iron Laws - Never Violate These

1. **No approval without verification** - Don't approve until all concerns addressed
2. **Assume bugs exist** - Look for edge cases, race conditions, missing handlers
3. **Question everything** - Even "obvious" code can hide issues
4. **Demand proof** - Ask for tests, show state transitions, verify behavior

## Adversarial Lenses (Apply to ALL Modes)

1. **"What Would Break This?"** — Runtime failure modes under load, during reloads, on reconnect, with unexpected device data
2. **"Assumption Stress Test"** — List every assumption; which are most fragile?
3. **"Contradictions Finder"** — Find contradictions between tests/implementation, docs/behavior, or within the diff

## Challenge Modes

### Coordinator & Registry Challenge (`/ha:challenge coordinator`)

Grill the developer on coordinator, registry, and config-entry changes:

**Migration Safety**

- Will this config-entry migration run on every existing entry without data loss (`async_migrate_entry` with a `minor_version`/`version` bump)?
- What happens to entries created before the new key existed?
- Is the migration idempotent, and does it handle a downgrade gracefully (an entry from a newer version)?
- Are there any unsafe operations (removing an entity, changing an entity's `unique_id` without an entity-registry migration, dropping a supported feature)? These are breaking changes (PR3).

**Update Performance**

- Have you introduced any blocking I/O on the event loop — sync calls in `async def`, imports or `Path.exists()` as I/O (P4)?
- Are executor jobs batched into one `hass.async_add_executor_job` rather than run in a loop?
- Will this scale as the device count grows? Is `update_interval` a sensible constant (not user-configurable — PS6), and does the poll avoid hammering the device/API?

**Data Integrity**

- Are unique IDs stable, immutable identifiers (serial, `format_mac()`, burned-in ID) — never host/port/name/URL (P7)?
- What happens during a reload (old entities present, new coordinator data)? Are listeners and subscriptions torn down in `async_unload_entry`?
- Is unknown state modelled as `None`, never a sentinel (`-1`, `""`, `0`) or a stale last value (P8)?

**Backward Compatibility**

- Will existing automations, dashboards, and entity IDs keep working after this change?
- Are there breaking changes to entities or service actions? If so: breaking-change section, migration, and a deprecation period (PR3)?

### Lit & WebSocket Challenge (`/ha:challenge lit`)

Prove the ha-frontend Lit component and its data subscriptions handle all cases:

**Event Coverage**

- List every Lit event listener (`@click`, custom `CustomEvent` handlers) and every hass/websocket subscription, with the expected component/`hass` state for each
- What happens if a reactive property (`@state`/`@property`) is `undefined` when an event fires?
- Are there race conditions between user-triggered events and server-pushed state changes (`hass.states` updates)?

**Subscription & Dispatcher Handling**

- List every frontend subscription (`this.hass.connection.subscribeEvents`/`subscribeMessage`) and, on the backend, every dispatcher listener (`async_dispatcher_connect`) plus the entity subscriptions set up in `async_added_to_hass` (PS4)
- Do all `async_dispatcher_send(...)` calls have a corresponding `async_dispatcher_connect` listener? Does every websocket command have a registered handler?
- What happens if a message arrives before the component's `connectedCallback`/`firstUpdated` completes, or before the entity finishes `async_added_to_hass`?

**State Transitions**

- Show the event → handler → state transition table
- Are all error states handled gracefully (rejected websocket promises, connection lost / reconnect)?
- What's the recovery path from each error state?

**Memory & Performance**

- Are large lists rendered with Lit's `repeat()` directive using stable keys (or `@lit-labs/virtualizer` for very large lists)?
- Is transient/large data kept out of `@state` (to avoid triggering unnecessary re-renders), using plain instance fields — and are no objects/arrays/schemas/functions created inside `render()` (F2)?
- What's the memory footprint per subscription (dispatcher listeners removed on unload, websocket subscriptions unsubscribed on `disconnectedCallback`)?

### PR Challenge (`/ha:challenge pr`)

Senior engineer review checklist:

**Must Pass**

- [ ] No protocol/transport/parsing in the integration — it lives in a published PyPI library; entities read `coordinator.data` (P11)
- [ ] Coordinator owns the fetch; entity state properties do no I/O and return `None` for unknown (P8)
- [ ] Config flow uses voluptuous schemas + selectors and validates the connection before creating the entry (P16, PS15)
- [ ] No dynamic attribute access (`getattr`/`setattr`/`hasattr`) or `cast`/`# type: ignore` to silence typing (P5)
- [ ] Error cases handled — correct HA exception with a `translation_key` (P3), never log-and-raise (P2), never a bare/broad `except` outside the config flow (P1)
- [ ] Tests cover new functionality, black-box via the core API (P13)

**Performance**

- [ ] No blocking I/O on the event loop — imports and file-exists checks included (P4)
- [ ] Lit `repeat()` with keys (or virtualization) for lists > 100 items
- [ ] Executor jobs batched; `update_interval` a sane constant

**Coordinator/Service**

- [ ] Coordinator raises `UpdateFailed` on fetch errors; setup raises `ConfigEntryNotReady`/`ConfigEntryAuthFailed` (P3, P16)
- [ ] Service actions registered in `async_setup` (a `services.py` module) with strict schemas — no `vol.ALLOW_EXTRA` (P18)
- [ ] No unbounded task spawning or runaway coordinator reschedules

**Security & Correctness**

- [ ] Unique IDs are stable, immutable identifiers — never host/port/name (P7)
- [ ] Secrets/tokens are never logged; credentials come from the config entry, not hard-coded
- [ ] Everything user-facing is translated with reusable keys (P9)

## Prior Findings Deduplication (MANDATORY)

CRITICAL: Prevents re-discovering identical issues across consecutive runs.

1. **Search** `.claude/plans/*/reviews/` and `.claude/reviews/` for prior findings
2. **Read ALL** prior findings before analyzing code
3. **Check each finding** against priors:
   - Fixed → **SKIP** | Still present → **PERSISTENT** (one line) | New → **NEW** (full analysis) | Reintroduced → **REGRESSION**
4. **Present**: NEW first (full), then PERSISTENT (one-line), then REGRESSION

## Example Challenge Output

```markdown
## Challenge: Coordinator — Acme unique-ID migration

### FINDING 1: Unstable unique ID (HIGH)
The config entry's unique ID is derived from `CONF_HOST` (config_flow.py:38).
A DHCP lease change orphans every entity and breaks the already-configured abort.
**Proof needed**: Read the `async_set_unique_id` call — if it uses the host, IP,
or any user-entered value, switch to a stable identifier (device serial /
`format_mac()`), and migrate existing entries via `async_migrate_entry` plus an
entity-registry `_attr_unique_id` update (P7).

### FINDING 2: Blocking import in async setup (MEDIUM)
`__init__.py:12` imports the vendor library inside `async_setup_entry`, causing
I/O on the event loop (P4).
**Action**: Move the import to module top-level (or, if it must be lazy, run it
via `hass.async_add_executor_job`).

### Status: BLOCKED — 2 unresolved findings
```

## Usage

Run `/ha:challenge [mode]` to initiate a rigorous review. The reviewer will not approve until all concerns are addressed with evidence.

Example workflow:

1. Run `/ha:challenge coordinator` after coordinator or registry changes
2. Answer each question with code references or test results
3. Address all concerns before proceeding to PR
