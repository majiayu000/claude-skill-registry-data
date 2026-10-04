---
name: tdd-guard
description: "Strict test-first owner policy only when explicitly requested or required by repository rules; delegates the workflow to original Superpowers TDD."
---

# Test-First Owner Policy

Use only when the user or repository explicitly requires a strict test-first
gate. The author workflow is `superpowers.test-driven-development`; resolve it
with `be skills route superpowers.test-driven-development --json` and read the
complete exposed author skill and required references. Reuse compatible native
providers or install the missing reviewed dependency through the selected
profile. Report pending exposure instead of replacing it with a local summary.

Bible owns the explicit gate: preserve the first failing command and raw result
as evidence before implementation, and report the actual validation outcome.
An exception requires an explicit user instruction or applicable repository
rule; state its reason, alternative evidence and residual risk. An unrun check
does not satisfy this gate.

This policy does not install Claude Code hooks or claim runtime enforcement.
Hook tooling, if requested, must be separately reviewed and configured through
the host. Keep author content unchanged and personal exceptions in this layer.
