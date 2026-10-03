---
name: leeway-automation-fabric
description: Govern and integrate LeeWay automation across Runtime Fabric, Formula F8, n8n, Home Assistant, Device Bridge, agents/workers and future robotics without making any provider the authority.
---

# LeeWay Automation Fabric

Use this skill when designing, integrating, executing or verifying LeeWay automation.

## Authority

LeeWay Automation Harness is the domain authority. Runtime Fabric owns execution lifecycle/adapters. Formula governs eligibility/routing/automation state. External engines are replaceable providers.

## Provider roles

- native Runtime Fabric automation: canonical durable jobs/schedules/queues
- n8n: deterministic workflow provider
- Home Assistant: environment/device aggregation provider
- Device Bridge: physical device capability authority
- robotics adapters: future physical actuation/sensing routes

## Default route

1. Normalize intent/event/schedule.
2. Recover current state/context.
3. Resolve authorization.
4. Apply Formula governance/automation gates when materially required.
5. Select the minimum qualified automation adapter.
6. Execute.
7. Observe post-state.
8. Run Veritas.
9. Write receipt.
10. Promote repeated verified procedures into deterministic skills/workflows.

## No-LLM preference

Prefer deterministic rules, Formula, verified skills and workflow engines. Use lightweight ML/LoRA for learned classification/routing when evidence supports it. Escalate to an LLM only for ambiguity, novel planning or semantic synthesis that deterministic capability cannot close.

## Physical actions

For Device Bridge/Home Assistant/robotics, API success is not physical proof. Require fresh device/sensor state where observable. Fail closed when authorization, safe operating bounds or post-state proof is missing.

## Formula boundary

F8 currently has a documented empty-condition policy gap. Never infer zero-condition automation as safe.

Domain Formula adapters must use calibrated measurements and the centralized evaluator. No invented Q69 state.

## External developer boundary

Automation Fabric may be consumed independently through its contracts. Consumers do not need Agent Lee or the full Sensory Harness.
