---
name: bend-proof
description: Prove selected properties of Bend modules when a plan has chosen Bend proof work, the user explicitly requests it, or an existing project proof contract needs maintenance. Mathematical or pure-function labels alone do not trigger this skill.
---

# Bend Proof

Use Bend proofs to supplement independent review and necessary tests. Keep the
target project's laws, proofs, implementation, and tests together. For a first
example or command setup, read [the verified minimal example](references/minimal-example.md).

## Bind the claim

Recover the selected properties, preconditions, domain, allowed edits, protected
property files, gate IDs, budget, and unfinished-work handling from the plan or
existing project contract. If these leave a material ambiguity, stop the affected
step and resolve it through plan revision. Explicit proof requests still need
a bounded claim before implementation.

Trace proof imports through laws to the actual implementation and inspect
whether the properties capture the requested behavior. For a sorter, ordering
alone permits an always-empty result; preserving the input elements also
matters. Preserve agreed laws: a property change needs explicit plan revision.
Keep proof files without a runtime entry point and runtime examples in tests.

## Check and record

Use the project's pinned tools and commands. The reference was verified with
Bend 2.0.38 and Lean 4.34.0. `bend PROOF.bend` gives quick feedback;
`bend PROOF.bend --verdict` is the formal proof gate. Record both separately.
In this release, `--verdict` uses BendTT, an independent checking kernel built
from the release's `bendtt.lean` with Lean 4.34.0 on first use, or selected by
`BENDTT`. Record the kernel's source/build identity or the supplied binary's
provenance, along with any `BEND_DIR` override. A cache hit is not proof evidence.

Before claiming success, verify tool versions (`bend version`, `lean --version`
when used), checked files and transitive imports, exit status, and diagnostics.
`ALL PROOFS CHECK` alone is insufficient: the ordinary checker prints it too.
Confirm the expected properties were checked against the delivered code, not
an unrelated file. Check runtime examples against their expected values.

Bind results to the current candidate and environment in the existing gate
ledger: record commands/cwd, file identities, tool/kernel identities, exit
status, output, and elapsed time. Changes to properties, imports, implementation,
commands, tools, or relevant environment invalidate affected evidence. Reuse
unchanged evidence only with an explicit mapping to the current delivery.

On failure, distinguish a property counterexample from syntax/import errors,
infrastructure failures, and budget exhaustion. Preserve diagnostics and leave
the gate unsatisfied using the existing STOP/report procedure. Keep the agreed
properties, imports, and gate strength; do not edit them just to obtain a pass.
Respect the task's budget; this skill supplies no universal attempt/time limit.

## State the coverage

The verdict checks the translated BendTT terms. Bend-to-BendTT translation
and correspondence to the intended Bend source remain a trust boundary;
the independent kernel does not establish that translation's correctness.
State what the claim excludes:

- A separate reference model proves that model's properties, not an existing
  Rust/TypeScript implementation. A correspondence argument needs its own evidence.
- FFI, IO, external services, and runtime effects are outside a pure module
  claim unless explicitly modeled and connected to the delivered behavior.
- Mathematical equalities do not establish floating-point error bounds or
  machine arithmetic behavior without the relevant semantics and assumptions.
- A source-level verdict does not prove compiler backends, generated binaries,
  hardware, or the deployed runtime environment correct.

Report these limits and unproved behavior to the reviewer; a verdict never
replaces review of property sufficiency or implementation correspondence.
Do not automatically migrate a project to Bend or install dependencies.
Tool preparation requires task-specific authority; the reference experiment's
temporary-tool authorization does not grant installation rights elsewhere.
