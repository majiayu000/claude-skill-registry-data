---
name: research-innovation-explorer
description: Build literature-grounded research-question candidate landscapes by collecting papers, generating A+B matrices, and dynamically reviewing combinations with traceable evidence, uncertainty, and next checks. Use when an AI agent needs to explore a field, screen research questions, compare paper combinations, inspect prior art, or prepare a provisional shortlist for researcher review.
---

# Research Innovation Explorer

## Purpose

Help a researcher decide which literature-grounded questions deserve more attention. Search broadly, structure a paper pool, generate an A+B matrix, and review selected candidates against source evidence.

Stop the default workflow at a provisional candidate landscape. Do not present matrix rankings as novelty, feasibility, publishability, or expected research success. Expand a researcher-selected candidate into theory framing, an experiment plan, or a publication-oriented report only when requested.

Use this skill as a host-neutral contract. Adapt search and browsing actions to the tools available in the current environment.

## Default Workflow

1. Clarify the topic, resource constraints, available data or code, and the desired breadth of the candidate landscape.
2. Read `references/search-playbook.md`, create a working `search-log.csv`, and generate a starter query pack with `scripts/build_search_queries.py`.
3. Build a 20-50 paper pool and normalize each paper into tasks, mechanisms, strengths, weaknesses, benchmarks, and implementation signals. Read `references/workflow.md` for intake rules.
4. Run `scripts/build_idea_matrix.py` to generate `idea-matrix.csv`. The script rejects duplicate paper identifiers and orders papers by identifier so each pair has stable A/B roles.
5. Treat matrix scores only as queue-priority signals. Build the review queue from the ten highest-ranked unique pairs, up to five coverage-increasing pairs, and every researcher-requested pair.
6. Read `references/post-matrix-review.md` and `references/scoring-rubric.md`. Copy `assets/templates/candidate-review.yaml` for each candidate under review.
7. Complete both entries under `direction_checks`. Select a direction only after both `A -> B` and `B -> A` have been assessed.
8. In each review round, identify the single uncertainty most likely to change the recommendation. Perform one focused action, then update facts, inferences, the relevant direction check, decision-linked inference identifiers, status, confidence, and the next check.
9. Validate each populated review with `scripts/validate_candidate_review.py` before including it in the candidate landscape.
10. Stop when further searching mainly repeats known information, a status is adequately supported, or the next decision requires researcher input. Preserve unresolved uncertainty in the record.
11. Produce a candidate landscape using `references/reporting-and-visualization.md` and `assets/templates/analysis-report-template.md`.

## Candidate Review Rules

- Verify source facts before interpreting a pairing.
- Preserve the canonical `paper_a_id`, `paper_b_id`, and `candidate_id` defined by the matrix order.
- Record observed facts separately from agent inferences.
- Give every observed fact a stable source URL and a section, page, figure, table, or repository location.
- Link every inference to the fact identifiers that support it.
- Link each non-unknown direction assessment, selected direction, and decisive research status to inference identifiers.
- Use `unknown` only for direction or dimension fields. Use `needs_check` or `conflicting` for research status when evidence warrants them.
- Keep matrix score and qualitative review judgment separate. Do not calculate a second aggregate score.
- Reopen any research judgment when new evidence changes the basis.
- Stop review on broken input data and resume after the data is repaired.

## Default Deliverables

- `search-log.csv`
- `paper-pool.csv`
- `idea-matrix.csv`
- one `candidate-review.yaml` per reviewed candidate
- one candidate-landscape Markdown document covering promising, unresolved, parked, weak, and excluded candidates
- optional screening figures when visual comparison is useful

## Optional Expansion

After the researcher selects a candidate:

- read `references/framing-and-theory.md` for a framing note
- read `references/experiment-plan.md` and use `assets/templates/experiment-plan.md` for a validation plan
- use `scripts/build_research_figures.py` for screening visualizations
- use `scripts/build_markdown_report.py` only as a matrix-overview scaffold, then add the candidate-review evidence manually

Keep all claims proportional to the available evidence. Read `references/ethics-boundaries.md` whenever wording about novelty, theory, or expected results becomes stronger than the sources support.

## Resources

- `references/workflow.md`: paper intake, matrix generation, queue construction, and default outputs
- `references/search-playbook.md`: search objectives, source selection, logging, and stopping rules
- `references/post-matrix-review.md`: dynamic review loop, evidence records, statuses, and failure handling
- `references/scoring-rubric.md`: qualitative dimensions and state assignment
- `references/reporting-and-visualization.md`: candidate-landscape reporting rules
- `references/framing-and-theory.md`: optional framing guidance for selected candidates
- `references/experiment-plan.md`: optional experiment planning guidance
- `references/ethics-boundaries.md`: claim and evidence boundaries
- `assets/templates/candidate-review.yaml`: stable review record interface
- `assets/templates/analysis-report-template.md`: researcher-facing candidate landscape
- `scripts/validate_candidate_review.py`: deterministic candidate identity and evidence-link validation
