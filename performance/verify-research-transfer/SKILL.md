---
name: verify-research-transfer
description: "Check whether a literature finding supports a proposed performance optimization. Read the primary figures and the implementation source, then run a cheap falsifier before writing code or benchmarks."
---

# Papiertiger (verify-research-transfer)

Use when a research report or model recommendation is about to guide a concrete optimization. Keep the user's chosen implementation and metric in scope. This skill grants no provider, publication or execution authority.

Bind the report, primary documents and target source revision. Preserve the original report when correcting it. Record publication and revision dates separately; a recent crawl is not a publication date. Use the existing Elicit research skill for API interaction rather than duplicating its client or storing a credential here.

Extract the few claims that determine whether to implement: workload eligibility, hardware support, exact arithmetic, intermediate storage, and measured versus predicted effects. For each decisive claim, find the primary section, figure or table. Read figures visually when their labels or comparison groups determine the answer.

Treat an assertion that evidence is absent as something to check directly. Search the paper for the relevant ISA, workload and experiment. Do not infer that unreported variants failed. A negative encoding-pool ablation is not necessarily a negative fusion experiment; a compressed scan using cache-resident vectors is not evidence of a register-only producer-consumer loop.

Map the technique to the actual code before proposing a measurement. Check whether the presumed input shape exists, whether the target already implements the suggested blocking or fusion, and which values remain live. Distinguish field equality from raw-word or serialized-proof equality. Keep source-derived eligibility separate from measured activation frequency.

Write one precise falsifier. Examples: the path has one sample point when the idea needs several; the removable phase is too small to reach the whole-program gate; required instruction support is unavailable; or the new representation changes required output bytes. Close only the tested mechanism. A failed eligibility check does not refute an adjacent optimization.

Preserve attribution through the project's existing research graph or knowledge system. Contributor measurements remain reports unless independently verified. If an ancestor endpoint fails but snapshot pagination works, reconstruct the relevant parent edges locally only after checking one stable snapshot, complete pagination, unique records, missing parents and cycles. Do not silently mix snapshots or turn an unavailable endpoint into missing research history.

Deliver a short corrected claim matrix and a source-specific next experiment or rejection. State the remaining evidence gap. Do not convert a paper's kernel throughput factor into an expected end-to-end speedup, or treat a model score as correctness or execution permission.
