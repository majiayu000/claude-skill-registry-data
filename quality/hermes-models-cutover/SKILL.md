---
name: hermes-models-cutover
description: >-
  Cut over a Hermes fleet during provider outages, retirements or restores, or swap a model ID
  within one provider. Inventory live routes, migrate generated bindings and harnesses,
  prove the new routes, and keep rollback available.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development"
  targets: "hermes"
  summary: "cut over provider routes across Hermes homes and harnesses with live proof and rollback"
  summary_zh: "跨 Hermes home 与 harness 切换供应商路由，实时验证并保留回滚"
  kind: "mechanism"
---

# Hermes Models Fleet Cutover

## Gates

- Hidden is not authorization. Confirm the affected fleet and get authorization for writes,
  restarts, commits, pushes and rollback as applicable; never infer one from another.
- A provider outage is a fleet cutover, not a default change. Inventory every affected home,
  harness, cron store and binding first; report unenumerated surfaces as unverified. Keep
  deliberately different routes and retain the old provider entry for rollback.
- Back up before writes. Edit the generator's source, never a generated home. If another writer
  is active, stop before apply or commit; leave repository publication to the sync owner.
- Probe effort variants before editing. Reject stale, unknown and empty preset targets; validate
  every target and read the dry-run diff before apply. Never use a self-fallback.
- Never restart the gateway to finish a check. Use real traffic and per-home session rows first;
  restart only with explicit approval and no conflicting writer.
- Prove each changed surface with its own run record, not config alone. Include an untouched
  route as a control, re-check generated state and report missing hooks as unavailable.

Hermes does not honor `disable-model-invocation`; this mechanism stays listed there.
Install it together with `hermes-models` in the same skills root.

## 1. Scope and run the fleet cutover

For a provider outage, retirement or restore, follow the
[fleet cutover procedure](references/fleet-cutover.md). Move affected live routes together,
including generated bindings and harness effort metadata. Update the standing routing
instructions and facts that name the prior route. A same-provider ID swap changes live pins,
not the old catalog entry; follow [the ID-swap procedure](references/fleet-cutover.md#6-same-provider-id-swap-new-variant-of-an-existing-model).

## 2. Use one switch adapter

Resolve the install's adapter and presets as specified in
[switch adapter](references/switch-adapter.md). Run list/check and identify stale targets or
wrong-state presets. Obtain write authorization before correcting preset files. Review the dry run
before applying the authorized change, then verify. If there is no adapter, execute the
same inventory, validation, migration, live proof and rollback contract by hand. Keep comments
and layout intact, and use the owning repo's sync path to publish bindings.

## Proof

Use the [verification matrix](references/fleet-cutover.md#5-verification-matrix). In each switched
Hermes home, get a live reply, compare the two newest `sessions.model` rows in that home's
read-only `state.db` (new ID above old), and check `resolve_reasoning_config(load_config(), "<model>")`
in that home. The `sessions` table has no `provider` column; pair the live ID with the configured
provider or preset. Check each harness's own run record, not its settings. Keep the backup path,
scope, diff, unverified surfaces, rollback plan and any pending approval in the report.

For the runnable background probe and delegation transcript check, see the installed
`hermes-models` reference `references/model-switching.md#proof`.

## References

- [Fleet cutover](references/fleet-cutover.md): inventory, migration, ID swaps, proof and rollback.
- [Switch adapter](references/switch-adapter.md): configuration, presets, options and validation.
