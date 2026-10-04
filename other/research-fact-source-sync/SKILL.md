---
name: research-fact-source-sync
description: Sync research facts, experiment metrics, terminology, figures, and thesis/paper prose from authoritative source files. Use when Codex is asked to update a paper after code/data/benchmark changes, align claims with manifests, revise terminology across chapters, or prevent over-claiming from stale experiment results.
---

# Research Fact Source Sync

Use this skill to keep a research paper aligned with code, experiments, figures, and evidence.

## Workflow

1. Identify authoritative sources before editing prose:
   - claim manifest or result summary;
   - term mapping or glossary;
   - document hub or affected-file list;
   - figure manifest, evidence report, or run log.
2. Classify the change:
   - new fact or metric;
   - renamed term;
   - changed experiment status;
   - new boundary, failure case, or limitation;
   - figure/table replacement.
3. Update source-of-truth records first. If they do not exist, create a small manifest rather than scattering facts only in prose.
4. Do one long synchronized update across all affected paper locations.
5. Search for stale wording, old numbers, old model names, and over-claims.
6. Record verification evidence: grep output, compiled PDF status, rendered page paths, or review notes.

## Guardrails

- Do not let narrative prose become the only source of truth for numeric claims.
- Separate main experiments from pilots, pressure tests, and extension experiments.
- Separate complete coverage from manual correctness validation.
- Keep LLM-generated prose downstream of facts; do not let an LLM invent schools, scores, citations, or experimental metrics.
- Preserve failure cases and scope boundaries in the paper when they materially affect claims.

## Useful Resources

- Read `references/sync-checklist.html` for the detailed synchronization checklist.
- Use `assets/claim-manifest.html` as a starter page when a project lacks a claim manifest.
