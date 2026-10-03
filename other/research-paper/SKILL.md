---
name: research-paper
description: Generate journal or top-conference research-paper drafts with literature grounding, novelty framing, evaluation planning, reproducibility, ethics disclosure, and LaTeX-ready structure.
triggers:
  - research_paper
  - 科研论文
  - 期刊论文
  - 顶会论文
  - LaTeX
domain: academic_writing
version: "1.0"
created_at: "2026-05-25"
---

# Research Paper Drafting

Use this skill when the target artifact is a scholarly research-paper draft rather than a generic essay or thesis.

## Output Contract

- Produce an article-style manuscript, not a project plan.
- Default structure: Abstract, Introduction, Related Work, Problem Formulation, Methodology, Experimental Design and Evaluation, Discussion / Limitations / Ethics, Conclusion.
- Keep references outside the section loop; the assembly layer renders the bibliography.
- State the research gap, contribution claims, and assumptions explicitly.
- If no real experiment data is supplied, write an evaluation protocol and reproducibility plan instead of fabricating results.
- Mark datasets, benchmarks, metrics, ablations, and statistical tests as author-supplied requirements when evidence is missing.

## Quality Bar

- Novelty: make the contribution distinguishable from representative prior work.
- Related work: compare methods and research streams, not just list papers.
- Method clarity: define system components, algorithms, protocols, and assumptions.
- Evaluation rigor: specify datasets, baselines, metrics, ablation plan, and statistical checks.
- Reproducibility: include implementation details, data availability expectations, and parameter / prompt disclosure needs.
- Ethics: disclose AI assistance, data privacy constraints, bias risks, dual-use concerns, and limits of generated evidence.
- Citation integrity: every concrete prior-work claim must be tied to retrieved evidence.

## LaTeX Readiness

- Prefer section titles and prose that can be converted directly into LaTeX.
- Use LaTeX math delimiters for formulas.
- Do not emit fake BibTeX keys; use citation ids from the shared citation snapshot.
