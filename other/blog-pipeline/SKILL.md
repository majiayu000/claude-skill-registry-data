---
name: blog-pipeline
description: Route one Paperclip child stage of the PLE new-content routine, producing hash-verifiable evidence and a fail-closed handoff.
---

# Blog pipeline stage router

Read `references/eo-blog-routine/execution-contract.md` completely before acting. That contract defines the only valid stage order, data policy, cadence, publish authority, and failure behavior.

This skill operates one assigned Paperclip child stage. It does not run the whole article, spawn subagents, create the next stage, wake another agent, call paid SEO/research APIs, or publish unless the assigned stage is Stage 10 in `quality_gated_live` and every prior receipt validates.

## Procedure

1. Read the child description and identify `runKey`, `slug`, `parentIssueId`, stage number, mode, accepted inputs, and output paths. If any are absent, fail closed with `INVALID_TASK_ENVELOPE`.
2. Read the exact required skill instructions listed for the stage in the execution contract. Compute each instruction file’s SHA-256.
3. Hash all accepted inputs before work.
4. Perform only the assigned stage. Do not silently repair or rerun an accepted predecessor; return `restartStage` when upstream evidence is invalid.
5. Run the deterministic gates named by the stage. Record exact commands, exit codes, and results.
6. Hash every output and write `content-pipeline/stage-receipts/{runKey}/{stage}.json` using the canonical schema.
7. Validate the receipt’s paths and hashes. A skill may be listed only if its instruction was read and its use changed a decision or produced a named artifact. Record non-applicability explicitly.
8. Post a structured handoff with disposition, receipt path, accepted outputs, exact next or restart stage, and public-publish count. Close the child `done`.

## Fail-closed dispositions

- `PASS`: all required skills, artifacts, and gates are verifiable.
- `NO_PUBLISH_DATA_REQUIRED`: exact external Ahrefs evidence is missing or conflicting. Write one exact data-request artifact and close; do not leave the issue active.
- `NO_PUBLISH_QUARANTINED`: the same producing gate failed twice. Preserve accepted predecessors and close.
- `PREVIEW_ONLY_COMPLETE`: Stage 10 preview validation passed with public-publish count 0.
- `PUBLISHED_VERIFIED`: live mode only; CMS mutation and every rendered-page check passed.
- `PUBLISH_FAILED`: a public mutation or rendering check failed. Never mislabel this PASS.

## Required checks by stage

- 01: provenance, freshness, schema, conflict detection, intent, product fit, Course Formula, vulnerability, cannibalization, and kill rules.
- 02: SERP-derived intent, named weak pages, backlink reality, BEAT SPEC, authoritative sources, and a concrete information-gain asset.
- 03: current product proof, Feature Fit Matrix, author voice, named byline, author/profile/CMS mapping.
- 04: answer-first outline, Article Promise, internal-link destinations, visual roles, Contagious and Oversubscribed applicability.
- 05: critique v1 and produce substantive v2; no thin template compliance.
- 06: verify or remove material claims; confirm citations and links support their sentences; scrub placeholders/internal terms.
- 07: useful original cover/OG and in-article visuals; verify files, dimensions, alt text, product proof, and manifest consistency.
- 08: adversarial comparison, policy, author, product, claims, links, visuals, information gain, and deterministic score. PASS requires >=85; BORDERLINE stops.
- 09: preview plus CMS payload dry-run; no public mutation. Run the contract validator in preview mode.
- 10: in preview mode, record zero-publish completion. In live mode, run the live validator before mutation, publish once, then verify the rendered page exactly as the execution contract requires.

Prose, comments, and self-attestation never substitute for a receipt or deterministic gate result.
