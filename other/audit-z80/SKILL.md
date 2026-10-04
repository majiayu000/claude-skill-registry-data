---
name: audit-z80
description: Evidence-first, read-only review of mixed Z80 ASM/C projects, especially ZX Spectrum code built with z88dk or SDCC. Use for preventive or broad bug audits involving ABI, stack/register/flag clobbers, ISR/shared state, memory maps, banks/overlays, firmware, generated code, toolchain behavior, hardware timing, or regression risk. Do not use for root-cause diagnosis of one observed failure. Uses the shared workflow skill to scale execution while preserving Z80-specific evidence and safety gates.
---

# Audit Z80

Use this file as a lean dispatcher. Load only references selected by the current
scope. Prefer context-efficient reads, searches, and shell output when the
runtime provides them.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, agent topology, dispatch, repair,
verification, and integration; this skill owns audit modes, evidence gates,
domain lanes, reporting, and its read-only contract. A workflow route never
widens that contract. If the sibling skill is unavailable, report the exact
limitation and continue directly without claiming delegated execution.

## Runtime Portability

- Resolve `SKILL_DIR` as the directory containing this file before invoking a
  bundled script.
- Use the Python 3 interpreter exposed by the host or explicitly provided by
  the user; never assume a platform-specific path.
- Invoke bundled scripts as `"$SKILL_DIR/scripts/<name>.py"` (or an equivalent
  absolute path), never as a project-relative `scripts/<name>.py`.

## Modes

- `help`: summarize modes from this file and stop.
- `preflight`: run the relevant profile scripts, report escalation signals, and
  stop.
- `auto` (default): preflight, then choose focused, standard, or deep demand.
- `full` / `diverge`: force broad category coverage; depth still adapts to the
  evidence and available agent capacity.
- Focused modes: `asm`, `c`, `abi`, `isr`, `memory`, `spectrum-hw`, `esxdos`,
  `toolchain`, `copt`, `map`.

For every real audit, read `references/hard-contract.md`,
`references/dispatcher.md`, and `references/preflight.md`. Read
`references/agent-orchestration.md` only when more than one independent
investigation lane is useful.

## Domain Demand

Classify after preflight and pass the result to `$workflow` when it is in
`auto`:

- **Focused**: explicit files/functions, one boundary, and a concrete question.
  A light route is normally sufficient.
- **Standard**: two or more interacting domains, a fuzzy symptom, or a material
  evidence gap. A medium route can isolate the highest-value uncertainty.
- **Deep**: broad/full scope, high-impact corruption or timing risk, mixed
  source/generated evidence, several targets, contradictory artifacts, or an
  explicit exhaustive request. A heavy route can investigate independent lanes.

An explicit workflow level wins. Missing agents reduce parallelism, not evidence
standards. In `auto`, stop after risk-prioritized lanes cease changing the
result. In explicit `full`, cover every applicable lane or state that the audit
is incomplete.

## First Actions

1. Resolve the skill directory before invoking bundled scripts.
2. Parse scope and mode; narrow only on an explicit user limit.
3. Build one project profile and one evidence digest.
4. Select domain references from `references/dispatcher.md`.
5. Select domain lanes from `references/agent-orchestration.md` and pass their
   briefs to `$workflow` when demand is standard or deep.
6. Read `references/external-research.md` only when a research trigger in
   `references/dispatcher.md` fires.
7. Treat scripts, agents, prior knowledge, and web sources as candidate
   generators. The main agent verifies every promoted finding.

## Reference Map

- Evidence and sandbox rules: `references/hard-contract.md`
- Preflight and profile: `references/preflight.md`
- Routing and scripts: `references/dispatcher.md`
- Domain lanes for delegated analysis: `references/agent-orchestration.md`
- External discovery: `references/external-research.md`
- Promotion: `references/promotion-gate.md`
- Reporting: `references/reporting.md`
- Domain checks: `references/asm-abi.md`, `references/c-memory.md`,
  `references/isr-map.md`, `references/sdcc-z88dk-quirks.md`,
  `references/spectrum-hardware-esxdos.md`,
  `references/promotion-gate.md`

## Core Rules

- Findings first; except for `preflight` mode, place profile and coverage context
  after findings. Never edit project code during an audit.
- Hand one observed failure with unresolved causality to `$debug-z80`; keep a
  requested preventive or broad correctness review here.
- Promote only current-code or fresh-artifact evidence.
- Verify reachability, ABI, stack, flags, registers, interrupt state, memory
  layout, generated-code reality, and target constraints as applicable.
- If no finding survives, say so and identify the strongest residual risk.
