---
name: write-literature-review
description: Iterative literature-review workflow for a research topic. Use this skill to draft up to 10 search keywords, build a seed set from OpenAlex title-and-abstract matches, expand by backward and forward citations, screen candidates by title and abstract, repeat until no new relevant papers remain, rank the final set, inspect up to 30 full texts, build a concept-reference knowledge graph, and write a literature review grounded only in the final included references.
---

# Write Literature Review

## Overview

Use this skill when the user wants a serious literature review rather than a quick paper list. The workflow is intentionally iterative: search broadly, expand by citations, screen with judgment, repeat until saturation, then read deeply and synthesize.

Keep a separate execution log throughout the whole workflow at `logs/workflow_log.md`. Update it step by step as work happens. The log should record what you did, what inputs you used, what outputs you produced, what you learned, and what decision or next action followed.

## Workflow

Use `references/workflow.md` as the authoritative workflow.

At a high level, the agent should:

1. Clarify scope, confirm the citation format, and record the setup in `plan/review_plan.md`.
2. Draft up to 10 search keywords and save them in `search/seed_keywords.json`.
3. Build a seed set with `scripts/lit_review_pipeline.py search`.
4. Screen by title and abstract, then iteratively expand and rescreen until saturation.
5. Rank the final filtered set and inspect up to 30 full texts.
6. Build the knowledge graph artifacts.
7. Write `review/literature_review.md`, render the final deliverables, and finalize `logs/workflow_log.md`.

When there is any ambiguity about step order, stopping conditions, screening rules, or expected intermediate files, defer to `references/workflow.md`.

## Workspace Layout

Keep only three presentation files at the workspace root:

- `literature_review.pdf`
- `references.md`
- `knowledge_graph.png`

Put all editable or machine-readable files in shallow named folders:

- `plan/`: scope and planning notes
- `logs/`: step-by-step execution log and audit trail
- `search/`: keyword drafts, seed set, merged search pool, deduped search pool
- `screening/`: screening queue, filtered set, visited titles, screening log
- `expansion/`: raw backward and forward expansion outputs
- `fulltext/`: full-text discovery outputs and reading notes
- `review/`: editable markdown review source
- `graph/`: graph markdown, graph JSON, and graph DOT source
- `references/`: ranked reference artifacts and optional machine-readable reference exports

## Deliverables

Produce these files unless the user asks for a different format:

- `plan/review_plan.md`: scope, criteria, assumptions, and search boundaries.
- `logs/workflow_log.md`: step-by-step record of actions taken, outputs produced, and decisions made.
- `search/seed_keywords.json`: up to 10 drafted keywords.
- `search/seed_candidates.jsonl`: initial title-and-abstract seed set.
- `screening/screening_queue.jsonl`: newly expanded records awaiting LLM screening.
- `screening/visited_titles.jsonl`: all already visited article titles, including seeds and candidates.
- `screening/filtered_candidates.jsonl`: final title-and-abstract relevant set after iterative screening.
- `references/ranked_references.jsonl`: ranked final filtered list.
- `references/ranked_references.md`: readable ranking table.
- `fulltext/fulltext_hits.json`: discovery results for up to 30 deeper reads.
- `review/literature_review.md`: editable review source.
- `graph/knowledge_graph.md`: text version of the concept-reference graph.
- `graph/knowledge_graph.json`: structured graph nodes and edges.
- `graph/knowledge_graph.dot`: Graphviz source used to render the root PNG.
- `literature_review.pdf`: final review article at root.
- `references.md`: final reference list at root.
- `knowledge_graph.png`: final graph image at root.

## Subtasks

Use code-based subtasks for repeatable operations:

- Seed search by keyword: `scripts/lit_review_pipeline.py search`
- Backward and forward expansion: `scripts/lit_review_pipeline.py expand`
- Deduplication: `scripts/lit_review_pipeline.py dedupe`
- Reference ranking: `scripts/lit_review_pipeline.py rank`
- Full-text discovery: `scripts/lit_review_pipeline.py fulltext`
- Knowledge graph construction: `scripts/build_knowledge_graph.py`

Use prompt-based judgment for interpretation-heavy operations:

- Drafting the keyword list from the user topic.
- Screening title-and-abstract candidates for relevance.
- Deciding when saturation has been reached.
- Interpreting methods, concepts, findings, and limitations.
- Writing the final review.

## Screening Rules

- During iterative screening, judge relevance from title and abstract only.
- Prefer recall in early rounds and precision in later rounds.
- Keep borderline-but-possibly-useful papers unless the mismatch is clear.
- Track inclusion and exclusion decisions clearly enough that another reviewer could audit them.
- Never confuse "full text not found" with "not relevant."

## References

Read these files before running a substantial review:

- `references/workflow.md`: detailed iterative search, screening, and ranking rules.
- `references/workflow_logging.md`: format and expectations for the step-by-step workflow log.
- `references/review_writing.md`: template and instructions for the final literature review article.
- `references/citation format/`: style examples for common in-text citation and reference-list formats.
