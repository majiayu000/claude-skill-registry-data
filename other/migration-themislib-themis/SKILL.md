---
name: svelte/migration
description: >-
  Route migration of shared Svelte writable/readable/derived stores and
  $state/$derived runes to Themis Redux and sagas, including assessment,
  components, and cleanup. Keep ephemeral UI state and DOM-local effects local.
type: lifecycle
requires:
  - svelte
  - core/core-policy
triggers:
  - migrate Svelte stores
  - convert Svelte stores to redux
  - replace svelte stores
  - Svelte migration
  - migrate writable
  - migrate derived
  - svelte store to redux
  - Svelte store migration plan
---
# Migrate Svelte Stores → Redux + Saga

## Agent Preflight Compliance Contract

Before editing code or docs under this skill:

- **MUST** read this skill plus every linked skill/doc that applies to the touched files.
- **MUST** cite the applicable skills/docs in the implementation plan or completion handoff, including the rules used.
- **MUST** include verifier-ready evidence: searches, tests, or diff checks proving the cited rules were followed.
- **MUST** keep the migrated app on the Svelte Store family described by this
  subtree.
- **SHOULD** stop and ask when rules conflict or scope is unclear.
- **NEVER** claim completion when a required skill/doc was skipped or the handoff lacks compliance evidence.

> Index for the migration playbook. Each step below links to a focused sub-skill; read them in order for a full slice migration.

## Migration Policy

Classify ownership before converting syntax. Shared/domain state moves to Redux;
ephemeral instance-local UI state and DOM-local focus, scroll, measurement, and
widget lifecycle stay with the component. Async syntax alone does not change that
boundary. Use `../../core/core-policy/SKILL.md` → **Setup — core rules** and
`./assessment/SKILL.md` → **Decision Framework** for the classification evidence.

Migrate small technical increments, simplest and most isolated first. Branches,
commits, and PR strategy come from the active task/repository instructions, not
this reusable skill; see `./cleanup/SKILL.md` → **Workflow ownership**. Keep the
old owner until verification succeeds, then apply **Remove Old Store Files** and
**Pass-Through Wrapper Guard** in `./cleanup/SKILL.md` for deletion/shim evidence.

For every migrated slice, apply pure/no-op reducer rules in
`../../core/reducers/SKILL.md` → **Do**, serializable value rules in
`../../core/state-serialization/SKILL.md` → **Do** and **Don't**, and domain-effect
conversion in `./side-effects/SKILL.md` → **Effect ownership boundary**.
Component reads/dispatch follow `../selector-lifecycle/SKILL.md` → **Call-mode map**.
Keep the app on the Svelte Store family throughout migration.

## Recommended Order

Run these sub-skills in order. Steps 3–6 repeat per slice; step 7 closes out each slice.

1. `./assessment/SKILL.md` → **Output of the Assessment** — Inventory stores/runes, record shared/domain vs local ownership, and choose the next leaf. Local-only findings need no Redux conversion.
2. `./setup/SKILL.md` → **Step 3 — Create the Store and Bootstrap It** — Complete pre-migration setup once with an empty app-owned reducer map; add registrations as slices land.
3. `./writable-stores/SKILL.md` → **State: `writable` / `$state` → Initial State** and **State Updates: `store.set` / `store.update` → `dispatch(action())`** — Convert shared mutable state and updates with immutable actions/reducers.
4. `./derived-stores/SKILL.md` → **Examples** — Convert shared derivations to named Store-bound selectors; compose upstream values rather than storing derived state.
5. `./side-effects/SKILL.md` → **Examples** and **Conversion Recipes** — Convert domain effects to saga workers, watchers, or channels, preserving explicit cancellation ownership.
6. `./component-migration/SKILL.md` → **Examples** and **Rollout Order Per Component** — Replace legacy imports, reads, and writes with selector readables and Store dispatch.
7. `./cleanup/SKILL.md` → **Rollback Strategy**, **Final Checklist Per Slice**, and **Cleanup Examples** — Verify before deleting the old owner; record zero references, wrappers/shims, and tests. Roll back the complete technical unit if needed.

## Primitive routing card

Only apply these routes after assessment classifies the state/effect as shared or
domain-owned. The linked leaves, not this index, own the conversion procedures.

| Source pattern | Canonical conversion owner |
| --- | --- |
| `writable`, `$state`, `.set`, `.update` | `./writable-stores/SKILL.md` → **State Updates: `store.set` / `store.update` → `dispatch(action())`** |
| `readable(value, start)` | State: `./writable-stores/SKILL.md` → **State: `writable` / `$state` → Initial State**; domain start/stop logic: `./side-effects/SKILL.md` → **Effect ownership boundary** |
| `derived`, `$derived` | `./derived-stores/SKILL.md` → **Examples** |
| `$store` reads and component writes | `./component-migration/SKILL.md` → **Rollout Order Per Component** |
| Domain `$effect`, fetch, persistence, timers, listeners/IPC | `./side-effects/SKILL.md` → **Conversion Recipes** |
| App saga startup formerly in `onMount` | `../store/SKILL.md` → **App saga lifetime**; mount-scoped startup cancels on unmount and restarts on remount, not automatically on Store creation |
| DOM-local lifecycle or instance-local visual state | `./assessment/SKILL.md` → **Decision Framework**; retain component ownership |

## Verification handoff

Record the assessment verdict and executed leaf routes in order. Attach the
per-slice evidence specified in `./cleanup/SKILL.md` → **Final Checklist Per Slice**
and **Cleanup Examples**; do not substitute this index for those checks.
