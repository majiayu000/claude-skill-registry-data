---
name: organize-z80
description: Map Z80 ownership and dependencies, design boundaries, or plan and apply an approved reorganization. Use for structural work and persistent project maps in ASM/C, z88dk/SDCC, banked or overlay projects while preserving behavior, ABI, memory, and timing.
---

# Organize Z80

Design the smallest sustainable organization justified by the current project.
Treat source structure, runtime placement, ownership, and dependency direction as
separate decisions: on Z80, a tidy directory tree can still produce a worse
binary, extra calls, bank switches, duplicated state, or an unsafe memory map.
Cover applications, ROMs, games, tools, and drivers, including RAM, rendering,
storage, input, audio, protocols, hardware, resources, and application logic.
Preserve binary, storage, and multi-target contracts without imposing a framework.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, agent topology, dispatch, repair,
verification, and integration; this skill owns organization modes, evidence,
the S–V domain flow, persistent-map rules, and mutation permissions. A workflow
route never widens those permissions or bypasses the apply gate. If the sibling
skill is unavailable, report the exact limitation and continue directly
without claiming delegated execution.

## Modes

- `help`: explain modes, demand, evidence required, and the smallest safe next
  step; do not inspect or propose a target structure.
- `map`: establish current topology, ownership, placement, and risks; do not
  prescribe moves or a target tree; keep it read-only unless the user explicitly
  requests the persistent-map exception below.
- `design` (default): define proportional boundaries and their rationale; do
  not order migration work, edit source, or imply approval.
- `plan`: turn an approved or clearly stated design into reversible slices;
  do not edit source.
- `apply`: execute exactly one approved slice; do not widen scope, redesign,
  combine behavior changes, or start without all apply gates.
- `review`: assess an existing architecture or proposal against this skill's
  contracts; do not edit or silently turn findings into a migration plan.

## Domain Demand

Classify after the initial map and pass the result to `$workflow` when it is in
`auto`:

- **Focused**: one component, state owner, dependency cycle, memory region, or
  proposed move. Analyze only the affected boundary; light is normally enough.
- **Standard**: several coupled components or one cross-cutting responsibility.
  Map the relevant execution and data paths before designing; medium can own a
  cohesive multi-file slice.
- **Deep**: whole project, several targets, mixed C/ASM, interrupts, banking,
  overlays, generated assets, or a requested migration. Heavy can split
  independent surfaces; cover every active responsibility and runtime placement
  class, or state what remains unmapped.

An explicit workflow level wins. Do not turn a small project into a layered
framework. A single file with clear sections and contracts may be the correct
organization.

## Routing and progressive disclosure

Except in `help` mode, read `references/hard-contract.md` first. Read
`references/project-model.md` when mapping more than a named local boundary.
Load only the references selected by the following signals:

| Signal | Read |
| --- | --- |
| Target boundaries, dependency direction, or layout | `references/organization-patterns.md` |
| Planned or applied move, split, include change, or validation | `references/migration-and-validation.md` |
| C/ASM, z88dk, SDCC, assembler scope, linker, CRT, or toolchain seam | `references/toolchain-layout.md` |
| Persistent current, recommended, final, or stale project map | `references/persistent-project-map.md` |
| Formal/durable deliverable, or Standard/Deep report | `references/reporting.md` |

Use these workflow steps, stopping once the selected mode and demand are
satisfied: **S** scope; **B** baseline; **E** execution map; **M** state,
placement, and dependency map; **C** seam/contract; **D** design; **P** one-way
slice plan; **V** verify and report.

| Mode | Focused | Standard | Deep |
| --- | --- | --- | --- |
| `help` | Explain S–V only | Explain S–V only | Explain S–V only |
| `map` | S, local M, report | S, E/M/C, report | S/B/E/M/C, report gaps |
| `design` | S, local M/C/D | S/E/M/C/D | S/B/E/M/C/D across active classes |
| `plan` | S/B/C/P/V gate | S/B/E/M/C/D/P/V gate | S/B/E/M/C/D/P/V by approved phases |
| `apply` | S/B/C, one P slice, V | S/B/C, one P slice, V | S/B/C, one P slice, V; never the whole plan |
| `review` | S, local M/C, report | S/E/M/C, report | S/B/E/M/C, report gaps |

Do not build merely to decorate a read-only proposal. For `Focused`, inspect
only the affected boundary. For `Standard`, map coupled execution and data
paths. For `Deep`, cover every active responsibility and placement class or
name the unmapped remainder.

For a non-durable `Focused` result, do not load `references/reporting.md`.
Return only the decision or finding, its current anchor, the preserved boundary,
the narrow check or next step, and material residual risk.

## Apply gate

Enter `apply` only when all conditions hold:

1. Receive an explicit request to edit.
2. Freeze a relevant baseline, including repository state when available and
   the cheapest applicable build, map, symbol, artifact, emulator, or hardware
   evidence.
3. Have an approved design or boundary contract.
4. Name one phase or slice, its acceptance gate, and its rollback point.

If any condition is absent, remain read-only and state the missing gate.

## Persistent project map

When a canonical project map already exists, read the sections relevant to the
requested ownership, dependencies, placement, or migration. For a named local
boundary, do not load the full map unless unresolved dependencies or an explicit
project requirement make it necessary. In `help`, do not load it. Verify volatile
claims used in the answer against current source; routed context is not proof.
Create or update it only after an explicit request. A map-only write may edit
the approved map and routing pointer without authorizing source, build, or
configuration changes. Follow `references/persistent-project-map.md` for its
location, lifecycle, drift rules, and current/recommended/final contract.

## Decision Rules

- Split by ownership and reason to change, not file length or noun count.
- Keep one authoritative owner for mutable state; expose operations or snapshots
  instead of writable globals.
- Point dependencies from application orchestration toward capabilities and
  from capabilities toward explicit platform adapters. Keep hardware-specific
  details at the edge unless timing or placement requires deliberate colocation.
- Keep memory layout authoritative in one place even when data users live in
  several modules.
- Keep generated files derivative. Edit their source, generator, schema, or
  manifest rather than the generated output.
- Preserve a stable boundary across targets; isolate target differences behind
  assembly-time selection or narrow adapters only when multiple variants exist.
- Prefer direct calls and explicit data over factories, registries, service
  locators, generic managers, or function-pointer frameworks.
- Accept duplication when sharing would introduce bank traffic, long calls,
  unstable ABI, lifetime coupling, or larger linked output; record the reason.
- Reject a move whose only benefit is aesthetic and whose runtime or validation
  cost is material.

## Relationship to Other Z80 Skills

- Use `audit-z80` separately when the map exposes a correctness, ABI, ISR,
  memory-corruption, or hardware-risk question.
- Use `shrink-z80` separately for size claims and `optimize-z80` separately for
  speed, RAM, rendering, latency, or multi-objective claims.
- Do not claim that reorganization improves bytes or cycles without fresh local
  evidence. Maintainability evidence may justify a design even when runtime
  metrics remain neutral.

## Core Rules

- Preserve behavior, public APIs, file and wire formats, target support, build
  entry points, and user data unless the user explicitly authorizes a break.
- Never mix unrelated modernization, renaming, formatting, optimization, or bug
  fixes into a structural migration.
- Never infer safety from compilation alone; validate runtime placement and
  hidden contracts appropriate to the changed boundary.
- Produce no empty directories, placeholder modules, speculative interfaces, or
  abstractions for hypothetical future targets.
- State `NO REORGANIZATION NEEDED` when current ownership and dependencies are
  already proportionate to the project.
