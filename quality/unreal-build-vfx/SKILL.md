---
name: unreal-build-vfx
description: Author and integrate Unreal Niagara effects with bounded simulation, explicit pooling, cancellation and target scalability evidence.
engines: [UNREAL]
---

# Unreal Build VFX

## When to use

Build or integrate Unreal Niagara effects, their runtime parameter adapters, pooling, bounds and scalability. Shared gameplay feedback design remains agnostic; this feature owns Niagara assets and native runtime integration.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-vfx` before writes or tool launches. Require effective engine `UNREAL` and `compatible: true`, with validated override/output scope when present. Skill selection never selects an engine.

Inspect engine version, selected Niagara plugin/modules, CPU/GPU simulation, renderer/platform support, required system assets, event sources, quality levels and effect budgets. Do not enable plugins, choose cloud media or install dependencies implicitly.

## Workflow

1. Specify each effect's semantic event, authority/prediction policy, owner, transform/attachment and completion/cancellation route. Deduplicate predicted/confirmed presentation without letting visual timing determine hits.
2. Author genuine Niagara systems/emitters, materials and parameter interfaces with native tools. Preserve source provenance and art direction; inspect parameter names/types against real assets.
3. Select CPU/GPU simulation, bounds, spawn/update rates, collision and data interfaces against target support. Declare world versus local space and explicit game/real/sequence clock behavior.
4. Choose component or system-spawn ownership and pool method deliberately. Configure parameters and bindings before activation, then retire handles safely; use the [Niagara runtime reference](references/niagara-runtime.md) for API and pool lifecycle decisions.
5. Stop loops and trails on cancellation, replacement, actor teardown or travel. Reset every owned parameter, attachment and delegate on reuse; never mutate a component after releasing it to the pool.
6. Use NiagaraEffectType/scalability and measured instance/particle/overdraw limits. Define how culling affects purely visual events and keep required gameplay information available through another channel.

## Verification

Test overlapping events, pool reacquisition, stale completion, actor removal, travel and all selected clocks. Inspect near/far views, bounds, pause, low frame rates and scalability tiers in native captures. Measure CPU/GPU, draw/overdraw and peak instance counts on the actual target. A finite CPU-emitter pool test does not certify GPU effects or appearance.

## Output

Native effect assets, typed parameter and event contracts, pool/reset/cancel rules, target budgets, lifecycle tests and native visual/performance findings. Record environment, expected/observed results and blocked/not-run checks under the active `.hephaera/.cache/tasks/` task.

## Boundaries

Preserve media, provenance, independent review and promotion controls. Headless success cannot certify effect readability, flashing safety, appearance or physical haptics.

## References

- [Niagara runtime](references/niagara-runtime.md): typed parameters, pooling, completion, scalability and acceptance.
