---
name: artifact-investigation
description: "Opaque binary or artifact investigation: structure first, script second, agent last."
allowed-tools: ["Read", "Bash", "Glob", "Grep", "Agent"]
---

# Artifact Investigation (phase 2: gated)

Investigate an opaque artifact (a PE or .NET binary, a stripped executable, a vendor bundle) in
cost order: structure, then script, then agent judgment. The caller holds the artifact store; no
stage here copies the artifact's bytes into a repo. Cost order is
`coordinator/docs/wiki/coordinator-tripwires/cost-order-is-agent-tokens-then-wall-time-then-cpu.md`.

## When not to use

Ordinary source repos: read the code. This skill is for artifacts with no readable source.

## Stages, in order

1. **Parse and ingest, by script, no agent.** PE and .NET structural parsing (roadmap cluster C16,
   project-rag); Ghidra program-facts ingest (cluster C5, engine).
2. **Query the structural index.** Ask the target's indexed facts a ranked question before spending
   an agent (cluster C4, project-rag).
3. **Record claims and unknowns through the one writer** (cluster C3, engine), using the
   field names of cluster C2 (`coordinator/pipelines/deep-research/evidence-unknowns-ledger-schema.md`).
4. **Agent only on judgment** the earlier stages could not settle.

A blocker on any stage: read `references/stage-map.md` (stage to owning plane and cluster). Read it
at no other time.

## Degraded mode

No stage is wired to a sibling tool yet; each sibling primitive wires in as it lands. For every
stage whose sibling primitive has not landed, the run record writes `coverage: unknown` for that
stage, labelled provisional, and the investigation's conclusions name that stage as unchecked.
`coverage: unknown` is a provisional label, not a record shape: project-rag owns the record shape
for unknowns and claims. A stage is never reported covered because it was skipped.

## Gates (phase 2)

One run folder per investigation; layout in `references/run-folder.md`. Each stage writes its file
there and the next stage reads it. Between stages, run in order:

1. `python <skill>/scripts/claim_filter.py <run> <stage>` drops claims with no `source_link`.
2. `python <skill>/scripts/sweep_gate.py <run> <stage>` exits 1 and writes `sweep.json` until the
   stage is clean; do not start the next stage on exit 1.
3. After the last stage, `python <skill>/scripts/coverage_scorer.py <run>` writes `coverage.json`.

4. For a native binary, run `python <engine-root>/scripts/ghidra_ingest.py <binary>`
   (`ghidra_ingest.cmd` on Windows). It needs Ghidra 11.x via `GHIDRA_INSTALL_DIR` or `--ghidra`,
   analyses statically, and records functions, xrefs, imports and strings through
   `rea_ledger.write` itself. A missing script or Ghidra install leaves this stage at
   `coverage: unknown`.
5. Record what survived through the one writer:
   `coordinator-invoke rea_ledger.write '{"kind": "<claim|evidence_record|unknown_revision>", "records": [...]}'`.
   Each record is a JSON string in canonical form: keys sorted at every level, `,` and `:`
   separators, raw UTF-8, no trailing newline. A non-canonical record refuses the whole batch and
   nothing is written. An unknown revision N>1 carries the digest of revision N-1.

An unlanded stage records `coverage: unknown` with `provisional: true`, never a score.
