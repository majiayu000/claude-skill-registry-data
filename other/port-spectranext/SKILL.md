---
name: port-spectranext
description: Orchestrate starting, resuming, implementing, diagnosing, validating, and handing off an existing ZX program port to the Spectranext cartridge through its canonical external consumer pipeline. Use when explicitly invoked or selected by route-z80 for a Spectranext cartridge port. Do not use for ZX Spectrum Next targets, generic ZX ports, or development of the Spectranext backend itself.
---

# Port Spectranext

Drive one consumer port through the Spectranext repository's fail-closed
pipeline. Keep the consumer checkout as the active project and treat the
external pipeline, manifest schema, and cartridge documentation as authority.
Do not copy their logic or create a competing lifecycle.

## Activation Boundary

Use this skill for an existing ZX program gaining a build for the **Spectranext
cartridge**. The spelling identifies the product; it is not the ZX Spectrum
Next platform. Route a generic Spectrum Next product or port to `develop-z80`
when it needs a product lifecycle, or to `$workflow` for bounded engineering.

Work on the Spectranext driver, tools, firmware contract, or generic pipeline
is platform work, not part of the consumer seam. Keep it in the Spectranext
repository and in its own commit. When the live external canon grants standing
escalation for a bounded generic repair, use that authorization and continue
without asking the user to repeat it.

## Workflow Core

Apply the sibling `$workflow` skill at `../workflow/SKILL.md` as the execution
control plane. Workflow owns effort, dispatch, repair routing, verification,
and integration; this skill owns the port state, external authority, consumer
boundary, hardware evidence, and mutation gates. A workflow route never widens
those gates. If the sibling skill is unavailable, report the limitation and
continue directly without claiming delegated execution.

## Authority Discovery

For every real task, read `references/hard-contract.md` first.

1. Resolve the Spectranext repository from an explicit user or project path,
   then from bounded workspace candidates. Never bake a machine-specific path
   into the skill or search the entire filesystem.
2. Verify that the candidate contains `AGENTS.md`, `docs/porting.md`, and the
   platform-appropriate `tools/dev` or `tools/dev.cmd` entry point. If no
   verified checkout exists, ask only for its path.
3. Read the external `AGENTS.md` and `docs/porting.md` at the start of every
   real task. They are binding and may have changed since this skill was
   published.
4. Load only the external surface documents required by the manifest and the
   current blocker. Within the same task, reuse a read only after verifying the
   authority files are unchanged; refresh them when canonical state or the
   blocker changes. Follow `AGENTS.md` routing rules and keep no cross-task or
   plugin cache.

The consumer repository root is always the command working directory. Invoke
the verified development entry point by absolute path.

## Canonical Entry

Route every request to start, resume, continue, or diagnose a consumer port
through the external `port request` gate before port-specific edits. Treat its
reported authority, manifest, state, and next command as current evidence.

If the manifest is absent, perform intake only when the user requested starting
or implementing the port. If it exists, follow the emitted state instead of
inferring progress from file names or remembered output. Never reorder the
commit, gate run, hardware validation, push, and handoff sequence defined by
the external canon.

Do not maintain a second state file, copy another consumer implementation, or
reinterpret the manifest schema in prose. The external command owns mechanical
validation; this skill owns the decisions and authorization around it.

## Demand

Pass the smallest sufficient signal to `$workflow`:

- **Focused**: explain state, run the read-only request/check gate, or resolve
  one bounded intake question.
- **Standard**: one consumer port with known seams and one ordered
  implementation/verification stream.
- **Deep**: the port exposes multiple independent backend, storage, packaging,
  or hardware blockers that need separate evidence lanes.

An explicit workflow level and repository instructions win. Reduced agent
capacity reduces parallelism, not gates or required evidence.

## Handoffs

- Keep this skill primary across the canonical port lifecycle. Do not compose
  `develop-z80` as a second state machine.
- Hand one unresolved observed failure to `debug-z80` only when causal
  investigation is a material blocker; return its verified result to the same
  port state.
- If the declared seam cannot preserve protected product behavior, stop the
  port. Keep a product change separate from the port seam. Route a required
  generic Spectranext repair through the live authority policy instead of
  widening the manifest; perform it immediately when that policy grants
  standing authorization.
- After a passing gate report, read
  `references/evidence-and-handoffs.md` before hardware or final handoff work.

## Output Contract

Return a decision artifact, not a transcript:

- verified Spectranext and consumer roots;
- current canonical state and exact next command;
- effective mutation boundary and authorized seam;
- manifest capabilities and external references loaded;
- checks as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`, with current evidence;
- artifact/commit binding, hardware evidence state, and residual risk;
- any separate authorization or physical action required from the user.
