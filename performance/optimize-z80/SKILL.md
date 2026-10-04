---
name: optimize-z80
description: Read-only strategy engine for optimizing Z80 and ZX Spectrum projects across size, speed, RAM, rendering, latency, banking, overlays, data layout, C-to-ASM, z88dk/SDCC codegen, ABI, toolchain, and model-specific hardware constraints. Uses the shared workflow skill to scale execution, then ranks only project-local, policy-compliant candidates with explicit validation.
---

# Optimize Z80

Read `references/hard-contract.md` before any command or promoted candidate.
The primary project tree remains read-only during analysis.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, agent topology, dispatch, repair,
verification, and integration; this skill owns optimization modes, policy and
evidence gates, domain lanes, ranking, and mutation limits. A workflow route
never widens those limits. If the sibling skill is unavailable, report the
exact limitation and continue directly without claiming delegated execution.

## Runtime Portability

- Use the Python 3 interpreter exposed by the host or explicitly provided by
  the user; never assume a platform-specific path.
- Resolve canonical `SKILL_DIR`, bundled scripts, and the shared worktree runner
  exactly as required by `references/hard-contract.md`; invoke only verified
  absolute paths.
- `"$SKILL_DIR/scripts/preflight.py"` is the sole preflight entry point. Do not
  infer a preflight Markdown reference.

## Modes

- **Triage** (default): inspect current source/artifacts read-only; no build;
  stale artifacts cap confidence.
- **Measurement**: use a disposable worktree for a reproducible baseline build
  when real byte/cycle/latency deltas matter.
- **Experiment**: requires explicit user approval; apply and measure one
  candidate in a disposable worktree, then remove it unless the user explicitly
  asks to retain it.

Worktree setup, command routing, cleanup, and primary-tree contamination checks
are owned by `references/hard-contract.md`.

This skill ranks cross-metric optimization strategy. Use `shrink-z80` for an
exhaustive size-only harvest and `audit-z80` for correctness auditing; neither
skill's private references are normative dependencies here.

## Domain Demand

Classify after preflight and pass the result to `$workflow` when it is in
`auto`:

- **Focused**: one zone, bottleneck, file, or candidate. A light route is
  normally sufficient.
- **Standard**: multiple plausible mechanisms or a material uncertainty. A
  medium route can isolate the highest-value uncertainty.
- **Deep**: broad project, several active zones/targets, conflicting evidence,
  high-risk timing/banking/ABI work, or an explicit exhaustive request. A heavy
  route can investigate independent high-value lanes.

An explicit workflow level wins. Missing agents reduce parallelism, not
evidence or policy gates. A normal triage stops when new lanes cannot change
the ranking; an explicit exhaustive request covers all applicable lanes or
reports the limitation.

## Progressive Load

1. Always: `references/hard-contract.md`, then
   `references/project-policy.md` only when a policy file exists or constraints
   must be inferred.
2. Core decision: the matching section of
   `references/optimization-paths.md`.
3. Domain lanes: `references/multiagent-roles.md` only when more than one
   independent lane is useful; pass selected briefs to `$workflow`.
4. Commands/measurement: `references/terminal-blockers.md` and
   `references/measurement.md` only when executing or measuring.
5. Technique references only for observed zones:
   `references/profiles-and-zones.md`, then the relevant one of
   `references/z80-techniques.md`, `references/c-to-asm.md`,
   `references/z88dk-sdcc-abi.md`, `references/modern-spectrum-io.md`,
   `references/zx-spectrum-hardware.md`, or
   `references/zx-spectrum-models.md`.
6. Finalist risk only: `references/risk-matrix.md`,
   `references/z80-proof-obligations.md`, and `references/traps.md`.
7. Toolchain experiments only: `references/toolchain.md`.
8. `references/external-research.md` only when its trigger gate fires.
9. `references/usage-examples.md` only when the user requests examples.

For hot loops/data traversal, load `references/loops-and-data.md`; for math
hotspots, `references/arithmetic.md`. Use `references/technique-coverage.md`
only for catalogue audits or gaps in the normal route, then load the matching
entry. These references expand candidate discovery, not execution permissions
or the evidence required for promotion.

Bundled helpers are evidence-selective: start with
`"$SKILL_DIR/scripts/preflight.py"`; use the corresponding resolved paths for
`pattern_scan.py`, `asm_callgraph.py`, `map_hotspots.py`,
`contention_audit.py`, `tstate_estimate.py`, `bincompare.py`, and
`score_candidates.py` only for the matching signal. Scanner and static
timing/map estimates are candidate evidence, never `PROVEN` by themselves.
When ASM comments claim exact cycle costs, run `tstate_estimate.py
--audit-annotations`; a mismatch or unknown blocks promotion, while a match
still remains static candidate evidence until the relevant runtime gate passes.
Python 3.11+ is required whenever a TOML policy must be parsed or enforced;
`score_candidates.py --policy` rejects older runtimes. On Python 3.9–3.10,
run only policy-free paths or pass explicitly verified `--target` and
`--forbidden` overrides, enforce any remaining constraints before scoring, and
report that the TOML policy was not parsed.

## Workflow

1. Preflight target, policy, dirty state, toolchain, source mix, build recipe,
   artifacts, freshness, and dominant pressure.
2. Choose triage or measurement; do not claim measured deltas from stale
   artifacts.
3. Build a compact zone map and identify the actual bottleneck.
4. Select only useful analysis lanes from `references/multiagent-roles.md` and
   pass their briefs to `$workflow`.
5. Generate candidates with current anchors.
6. Apply policy/target vetoes before scoring.
7. Merge duplicates and rank globally for the active bottleneck.
8. Risk-audit the finalists.
9. Recommend at most three next experiments; measure one only with the required
   approval.
10. Clean the disposable worktree and verify the primary tree stayed unchanged.

## Candidate Contract

Each candidate states:

- current anchor and evidence freshness;
- bottleneck/zone and mechanism;
- expected size, cycles/latency, RAM/stack, and UX effect as applicable;
- risk, target applicability, forbidden-lane tags, rollback, and validation;
- confidence: `PROVEN`, `LIKELY`, or `SPECULATIVE`;
- why it outranks alternatives now.

External sources and subagents generate candidates only. `PROVEN` requires
current local evidence or a reproducible measurement.

## Output

- policy, target, profile, and artifact freshness;
- compact zone/coverage ledger;
- ranked candidates and rejected policy/target tricks;
- at most three next experiments;
- validation/measurement plan;
- short process traps only when they affected the result.

## Hard Rules

- Reject forbidden lanes and wrong-target candidates; do not merely demote them.
- Optimize the dominant wait or pressure, not the most interesting assembly.
- Multi-target candidates pass only when every declared target meets its own
  limits from a fresh artifact built from the same frozen source revision and
  configuration baseline.
- DI/EI, SP abuse, SMC, undocumented opcodes, floating bus, and hardware timing
  require explicit risk tags and target-specific validation.
- One failed command must change the next method.
