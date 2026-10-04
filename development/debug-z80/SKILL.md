---
name: debug-z80
description: Evidence-bounded root-cause debugging for observed Z80, ZX Spectrum, or ZX Spectrum Next failures whose cause is unresolved. Use for reproducible crashes, wrong output, build or link failures, nondeterminism, regressions, hardware or emulator divergence, and failed fixes. Do not use for known-cause fixes, speculative audits, routine reviews, green refactors, or optimization without a failing behavior.
---

# Debug Z80

Find one causal owner and, only when requested, apply one verified root-cause
repair. Do not turn a local failure into a repository audit.

## Entry Gate

For `help`, explain this gate and stop without loading references or workflow.
Otherwise evaluate the request first. If it fails, state `NOT_DEBUGGING` and
continue through the receiving route, loading its instructions only.

Enter only when all conditions hold:

1. There is an observed failure: an exact diagnostic, wrong output, crash,
   hang, nondeterministic symptom, regression, hardware/emulator difference,
   or reproducible budget violation.
2. The causal owner is genuinely unknown, competing explanations remain, or a
   supported fix failed.
3. The requested result is diagnosis or diagnosis plus repair, not a broad
   correctness audit or general improvement search.

Preserve modality. Diagnose without editing when the user asked only for a
cause, explanation, or report. An original request to diagnose and fix is
sufficient repair authorization once the repair gate is met.

Do not debug merely because a task contains the words bug, failure, regression,
or test. If the cause already made a prediction confirmed by a discriminating
check, hand the known-cause fix to `$workflow`. Route preventive or broad
read-only correctness review to `$audit-z80`; route acceptable behavior that
only needs better size, speed, RAM, rendering, or latency to the matching
optimization specialist.

## Workflow Core

After the entry gate passes, apply the sibling `$workflow` skill at
`../workflow/SKILL.md` as the execution control plane. Workflow owns effort,
agent topology, dispatch, repair coordination, verification, and integration;
this skill owns Z80 evidence, the causal loop, repair gate, and output contract.
A workflow route never widens the mutation boundary. If the sibling is
unavailable, report the limitation and continue directly without claiming
workflow execution.

Read [references/hard-contract.md](references/hard-contract.md) before
reproducing, building, instrumenting, or editing.

## Runtime Portability

- Canonicalize the catalog path to this `SKILL.md` while following symlinks and
  Windows junctions, then set `SKILL_DIR` to its parent.
- Use the Python 3 interpreter exposed by the host or explicitly provided by
  the user; never assume a platform-specific executable or path.
- Resolve `RUNNER` from canonical `SKILL_DIR` as
  `"$SKILL_DIR/../../scripts/run_in_worktree.py"` and verify that it is a file
  before any disposable command. Invoke it by absolute path.

## Demand Signal

After the entry gate, pass one signal to `$workflow` in `auto`:

- **Focused**: stable narrow reproduction, one target, and one likely boundary.
  Light is normally sufficient.
- **Standard**: several interacting boundaries, mixed C/ASM, or one material
  evidence gap. Medium can follow the dependency chain in one ordered stream.
- **Deep**: nondeterminism, corruption, hardware timing, cross-process tools,
  hardware/emulator divergence, or a failed evidence-supported repair. Heavy
  is useful only when at least two independent investigations exist.

An explicit workflow level wins. Deep evidence does not by itself authorize
parallelism or edits.

## Causal Method

After the entry gate passes, read
[references/causal-method.md](references/causal-method.md). Apply its causal
loop and only the first symptom discriminator that fits. Do not load it for
`NOT_DEBUGGING` requests.

## Repair Gate

Repair only when the user authorized a fix and the evidence identifies the
owner, violated invariant, predicted effect, and narrow acceptance check.

- Patch the owner, not every caller. Preserve public ABI, registers, flags,
  stack, interrupt state, bank state, memory placement, firmware contracts,
  formats, targets, and timing unless the user authorizes a contract change.
- Reject retries, delays, swallowed errors, timeout increases, defensive bounds,
  and blanket state resets unless evidence proves that behavior is the intended
  policy.
- Exercise the candidate in a disposable worktree before applying it to the
  primary tree when the check builds, writes artifacts, instruments code, or
  depends on runtime behavior.
- Apply only the proven minimal change to the primary tree. Mirror that scoped
  change into a fresh disposable check when final verification would otherwise
  dirty the primary tree.
- Repeat the narrow check once. Use a safe, cheap negative control when it
  discriminates causality; otherwise name the equivalent evidence and why the
  control was unavailable.
- After two failed repairs against the same acceptance check, stop editing and
  reassess the reproduction, assumptions, and ownership.

Add a regression test only when it protects a durable invariant at lower cost
than recurrence. Remove temporary probes and disposable worktrees before
handoff.

## Outcomes

- `NOT_DEBUGGING`: no observed failure, causality already established, or a
  narrower domain owns the request. Name the receiving route.
- `READY_TO_FIX`: cause, causal evidence, owner, and narrow check are known, but
  repair was not authorized or cannot be applied here.
- `NEEDS_EVIDENCE`: name one missing fact and one next command or observation.
- `EXTERNAL`: evidence places the cause outside local ownership; name the
  smallest safe workaround or upstream/environment owner.
- `FIXED`: the authorized root-cause change passed the narrow causal check and
  any required broader gate.

Return one compact block:

```text
Outcome:
Observed:
Causal evidence or missing fact:
Owner or handoff:
Action and narrow check:
Residual risk:
```

## Attribution

Causal workflow adapted for this Z80 plugin from the MIT-licensed
`systematic-debugging` skill by NousResearch Hermes Agent, itself adapted from
obra/superpowers. This adaptation uses the plugin's existing workflow and
disposable-worktree contracts rather than copying its generic capture helper.
