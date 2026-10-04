---
name: develop-z80
description: Develop a complete Z80/ZX/Next product or deliberate vertical slice from an explicit initiative, or resume its SDD dossier and milestones. Do not use for routine bug fixes, isolated repository features, or Spectranext cartridge consumer ports.
---

# Develop Z80

Lead the user from idea to verified code without requiring SDD knowledge or
workflow commands. Keep one source of truth and stop scope growth at playable or
otherwise inspectable product checkpoints.

## Activation Boundary

Enter this lifecycle only for an explicit product initiative or an existing
develop dossier, or an explicit develop-z80 invocation. This covers applications,
games, demos, tools, and generic ports from idea through specification, milestones,
implementation, and verification. Repository language, a Z80 target, or generic
verbs such as plan, design, implement, feature, and verify are
not sufficient activation. Routine bug fixes, isolated features, refactors,
reviews, build/test
or documentation fixes, and internal architecture proposals stay outside this
lifecycle unless explicitly placed under an active product dossier.
Route ordinary maintenance and bounded repository changes through `$workflow`;
use `audit-z80`, `organize-z80`, `shrink-z80`, or `optimize-z80` only when their
specialist question is the requested result.

Once explicitly activated for a product, keep this skill as the product
contract across its dossier and milestones. Execute its individual engineering
steps through `$workflow` without treating each fix or proposal as a fresh
develop-z80 activation.

An existing ZX program's consumer port to the Spectranext cartridge has its own
external fail-closed lifecycle. Route it to `port-spectranext`; do not run two
product state machines over the same port.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, dispatch, repair, verification, and
integration; this skill owns SDD stages, evidence, the dossier, Z80 decisions,
and mutation gates. A workflow route never widens those gates. If the sibling
skill is unavailable, report the limitation and continue directly without
claiming delegated execution.

## Runtime Portability

- Canonicalize the catalog path to this `SKILL.md` while following symlinks and
  Windows junctions, then set `SKILL_DIR` to its parent.
- Use the Python 3 interpreter exposed by the host or explicitly provided by
  the user; never assume a platform-specific executable or path.
- Resolve `RUNNER` from canonical `SKILL_DIR` as
  `"$SKILL_DIR/../../scripts/run_in_worktree.py"` and verify that it is a file
  before any disposable command. Invoke it by absolute path.

## Modes

- `auto` (default): infer the earliest incomplete stage and progress to the
  current authorization ceiling.
- `idea`: shape the concept and smallest convincing product slice.
- `spec`: define behavior, constraints, and acceptance criteria.
- `plan`: choose technical direction, milestones, risks, and validation.
- `tasks`: produce the ready backlog for the active milestone.
- `implement`: execute one authorized task or the active milestone.
- `verify`: reconcile an implementation with its acceptance criteria.
- `help`: explain the lifecycle, mutation boundary, and a minimal invocation;
  do not inspect or edit a project.

Treat a named mode as a ceiling, not a step the user must operate. In `auto`,
never ask the user to choose a mode, stage, methodology, or next task.

## Routing

For every real task, read `references/hard-contract.md` first. Then load only
the references selected by current evidence:

| Signal | Read |
| --- | --- |
| Idea, spec, plan, tasks, or implementation sequencing | `references/lifecycle.md` |
| Create, resume, revise, or persist the source of truth | `references/dossier.md` |
| Target, CPU, video, memory, timing, I/O, delivery, or toolchain decision | `references/platform-profile.md` |
| Baseline, implementation, milestone gate, emulator/hardware check, or final reconciliation | `references/verification.md` |

Infer the earliest incomplete stage from the request, repository, dossier, and
current evidence. Ask one focused question only when a missing product decision
would materially change scope, architecture, compatibility, or visible behavior;
otherwise label the assumption and continue.

## Domain Demand

Classify after the initial concept and project inspection, then pass the signal
to `$workflow` when project route policy permits automatic selection:

- **Focused**: one bounded task or milestone already governed by the active
  product dossier, with one target. Light normally suffices.
- **Standard**: one vertical slice crossing several components or one material
  platform unknown. Medium can own one cohesive stream.
- **Deep**: a greenfield product spanning several domains or milestones,
  multiple targets, banking/MMU, ISR/timing, or a material generated-asset
  pipeline. Heavy can investigate independent evidence lanes while keeping
  implementation slices bounded.

An explicit workflow level and project route instructions win. Reduced agent
capacity reduces parallelism, not evidence or checkpoint requirements.

## Product-Code Apply Gate

Use the mutation boundary and product-code entry conditions in
`references/hard-contract.md`; use `references/dossier.md` for specification
acceptance state and `references/verification.md` for milestone checkpoints.
Product-code edits still require explicit authorization for the named behavior
or bounded slice. The first greenfield mutation still requires explicit user
acceptance of the presented scope, non-goals, active criteria, and first
milestone; broad authorization reaches only the first playable slice unless the
current session explicitly grants more.

## Handoffs

- Hand correctness, ABI, ISR, corruption, or hardware-risk investigation to
  `audit-z80` before implementation when it can veto the slice.
- Hand ownership, dependency direction, source layout, or runtime placement to
  `organize-z80` when topology is the primary risk; consume its approved design
  rather than creating a competing one.
- Hand size-only decisions to `shrink-z80` and competing size/speed/RAM/rendering
  decisions to `optimize-z80` before promoting those claims into the spec.

Keep the dossier and acceptance IDs authoritative across handoffs. Other skills
supply evidence or approved decisions; they do not silently change product scope
or authorize implementation.

## Output Contract

For idea, specification, or planning work, return the decision artifact, current
stage/scope, acceptance state, evidence or open decisions, dossier/task status,
and next step. Do not load verification guidance just to format this response.
For implementation or verification, use the closing record in
`references/verification.md` with checks, checkpoint, residual risk, and rollback.

Prefer the smallest idea, dossier, task set, and implementation that proves the
intended experience. Never weaken criteria or widen the active milestone merely
to obtain a pass.
