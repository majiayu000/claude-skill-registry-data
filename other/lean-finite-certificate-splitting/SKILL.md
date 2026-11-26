---
name: lean-finite-certificate-splitting
description: "Reduce Lean kernel replay memory for finite literal matrix certificates by splitting ordinary decide goals and assembling them symbolically. Use after a measured memory failure; it does not replace mathematical validation."
---

# Schiitlispalter (lean-finite-certificate-splitting)

*Split finite kernel certificates*

Preserve the statement and exact literal data while changing proof granularity. A resource failure rejects an execution shape under its bound, not the mathematical identity.

Read the failed receipt and raw output first. If all axiom prints were at the end, absence of output does not identify the failing declaration. Even an earlier checkpoint can be lost through buffering on an abort. Do not promote a localization hypothesis into a confirmed cause.

For matrix equality, inspect the pinned finite-function equality instance. In the tested Mathlib route, equality uses `Fintype.decidablePiFintype`; deciding a whole matrix nests finite decisions. Try a demanding fixed row before the whole matrix. If a row still exceeds the bound, use one scalar dot-product entry as the next discriminator. Prefer a final literal index or nontrivial row over the all-ones row, but do not claim it is the worst case without evidence.

Keep data in one accepted module where practical. Give each small equality a named theorem and print its axioms immediately. Assemble rows and matrices with `funext`, `Fin.cases`, `congrFun`, and the named proofs; do not reintroduce a whole-table `decide` in the assembly. A standalone test module repeating the data namespace must not be imported alongside the production data module.

Bind source, literal transcription, compiler, explicit imports and resulting objects. Changing imports as well as proof granularity confounds attribution: a successful combined change establishes feasibility, not which change reduced memory. Cached-object existence alone does not establish elaboration. Use ordinary kernel-checked proofs, not `native_decide`, placeholders or new axioms.

Use the current task's measured resource limit. Lean `-M` is not a hard RSS cap. A sampled process-group watchdog is also not a hard cap: record sample spacing, observed peak, termination and surviving-group check. Target only the owned process group. Preserve the failed run and choose a new bounded phase; do not silently restart it or raise limits.

A passing scalar proves only that entry. A passing row proves only that row. Promote a full identity only after all required leaves and the symbolic assembly compile, with permitted axiom reports and unchanged bindings. Integration into a semantic theorem and independent consumer review are separate checks.

Row splitting does not always suffice. Measure each split before relying on it.
