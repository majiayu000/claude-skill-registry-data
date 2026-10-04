---
name: evidence-synthesis-docs
description: Create structured, evidence-backed synthesis documents from large crawled or collected information corpora. Use when Codex needs to turn many raw or processed sources such as JSON, CSV, Markdown notes, social posts, comments, transcripts, web captures, OCR, or research exports into coherent reports, playbooks, matrices, taxonomies, evidence tables, or follow-up research plans. Especially useful when the user wants common patterns, concrete examples, actionable requirements, source-year labeling, confidence levels, or multiple documents with clearly different purposes.
---

# Evidence Synthesis Docs

## Overview

Use this skill to transform a messy evidence corpus into a small set of high-cohesion documents. Optimize for traceable claims, concrete examples, clear document roles, and structures selected from the data distribution and the user's intended use.

For detailed output patterns, read `references/document-structures.md` when the task involves creating or reorganizing substantial documents.

## Core Rule

Do not summarize by source order. Summarize by the user's decision problem.

Create multiple documents only when each document has a distinct job. Good splits:

- Understanding report: explains patterns, cases, mechanisms, caveats, and evidence.
- Execution playbook: converts findings into actions, timing, deliverables, risks, and acceptance criteria.
- Evidence matrix: preserves structured records for filtering, checking, and reuse.
- Gap plan: lists missing evidence, contradictions, and next crawl or interview targets.

Bad splits:

- One document per source unless the user asked for an archive.
- One document per year when year is only metadata.
- Separate documents that repeat the same conclusions with different formatting.
- A playbook that is just a shortened essay.

## Workflow

1. Inventory the corpus.
   - Identify raw files, processed files, existing reports, tables, and generated artifacts.
   - Preserve provenance fields: source file, record id, URL or note id, author if available, publication time, extracted year, source title, and evidence strength.
   - Inspect schemas before synthesizing. Prefer structured CSV/JSON over re-parsing prose when both exist.

2. Diagnose data distribution.
   - Find dense themes, sparse themes, repeated examples, unique high-value cases, time or year clusters, source-type clusters, and contradiction points.
   - Separate direct evidence from inferred patterns, weak signals, predictions, and user assumptions.
   - Mark where evidence is absent rather than filling gaps with generic advice.

3. Diagnose user intent.
   - If the user wants to understand a domain, produce an explanation-centered report.
   - If the user wants to prepare, operate, decide, or execute, produce an action playbook or matrix.
   - If the corpus will be reused or audited, produce a structured evidence table.
   - If the next step is more crawling, produce a gap-driven collection plan.

4. Design the document set.
   - Choose the fewest documents that cover the intent.
   - Give every document a one-sentence role before writing it.
   - Put cross-cutting evidence in tables, not duplicated paragraphs.
   - Keep top-level sections high cohesion: each section should answer one stage, question, audience need, or decision type.

5. Synthesize from concrete evidence upward.
   - Start with cases, records, quotes or paraphrased source claims, and observed distributions.
   - Then derive patterns, requirements, methods, risks, and templates.
   - For each major conclusion, attach source ids or an evidence table reference.
   - Label year or period whenever time matters.

6. Validate the output.
   - Check that every major claim is traceable.
   - Check that abstract advice is backed by at least one concrete example or explicit inference.
   - Check that each document has a non-overlapping purpose.
   - Check that years, confidence, predictions, and weak evidence are labeled.
   - Check that the result is useful without requiring the reader to inspect the raw corpus.

## Evidence Model

When creating or updating structured data, prefer records with these fields:

- `record_id`
- `source_id`
- `source_file`
- `source_title`
- `source_type`
- `url_or_note_id`
- `author`
- `published_at`
- `year_or_period`
- `topic`
- `subtopic`
- `claim`
- `concrete_detail`
- `evidence_strength`
- `confidence`
- `inference_level`
- `supports_output_section`

Use `inference_level` values such as `direct`, `paraphrase`, `synthesis`, `weak_signal`, or `prediction`.

## Writing Rules

- Prefer concrete cases before general conclusions.
- Replace vague statements with actor, context, action, evidence, and outcome.
- Include counterexamples and discarded options when they improve decision quality.
- Do not present predictions as historical facts.
- Do not hide uncertainty. Label weak, sparse, conflicting, or indirect evidence.
- Do not overfit to the loudest source. Weight repeated independent signals and high-detail records more heavily.
- Keep operational documents terse, table-heavy, and acceptance-criteria driven.
- Keep understanding documents explanatory, example-rich, and caveat-aware.

## Common Output Set

For a large crawl-to-report task, a strong default is:

1. `*_synthesis_report.md`: understanding document with patterns, cases, taxonomy, and caveats.
2. `*_action_playbook.md`: execution document with stage-by-stage actions, deliverables, risks, and checks.
3. `*_evidence_matrix.csv` or `.json`: structured evidence supporting both documents.

Only create all three when the corpus and user intent justify them. Otherwise create the smallest complete set.
