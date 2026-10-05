---
name: engineer-literature
description: Read, search, verify, and synthesize English frontier literature for engineering research and Chinese academic writing. Use when the user asks to read a paper, DOI, arXiv preprint, PDF, abstract, figure legends, related-work cluster, or research topic in engineering, AI, control, simulation, robotics, materials, energy, mechanics, signal processing, or similar domains; especially when they need Chinese explanations, paper cards, literature matrices, research gaps, method comparisons, citation-ready claim support, or material for a Chinese thesis/manuscript introduction, related work, methods, discussion, or figure planning.
---

# Engineer Literature

## Operating stance

Read literature as engineering research support, not as a generic summary. The goal is
to help the user understand English frontier work and convert it into Chinese academic
thinking: problem framing, technical route, evidence, limitations, research gaps, and
writing-ready comparisons.

Use Chinese as the default output language. Keep key technical terms in English with
Chinese explanations when useful, for example `model predictive control (模型预测控制)`.

Do not invent citations, DOIs, paper titles, venues, datasets, metrics, or claims. If the
user asks for recent/frontier/latest literature, verify with search or academic sources
before naming papers. If only a pasted abstract or partial text is available, say what is
known from the provided text and what still needs source verification.

## Workflow

1. Identify the task type: single-paper reading, paper comparison, topic frontier scan,
   citation support for a claim, or writing conversion for a Chinese manuscript.
2. Verify the source when needed. For DOI/arXiv/title/latest/frontier requests, prefer
   primary sources such as publisher pages, arXiv, Crossref, PubMed when relevant, IEEE,
   ACM, Springer, Elsevier, official lab/project pages, or the provided PDF.
3. Classify the paper's role: foundation, method, system, benchmark, dataset, review,
   application validation, negative result, or limitation/risk paper.
4. Extract engineering content: problem setting, assumptions, system model, algorithm or
   architecture, variables/equations, experimental setup, datasets, baselines, metrics,
   quantitative results, ablations, failure cases, and reproducibility details.
5. Convert the paper into Chinese research value: what gap it fills, what can be cited,
   what can be borrowed for method design, what can inspire figures, and what limitation
   can motivate the user's work.
6. Produce the requested output shape. For underspecified requests, default to a concise
   Chinese paper card plus a writing-use section.

## Output modes

- **快速读文献**: Use for abstracts, paper triage, and "is this useful for me?" Read
  `references/reading-workflow.md`.
- **深度精读**: Use for full papers, PDFs, methods, equations, or experiments. Read
  `references/reading-workflow.md`.
- **前沿检索与引用支撑**: Use for topic scans, latest work, or citation support. Read
  `references/search-and-citation.md`.
- **中文论文写作转化**: Use when the user asks for introduction, related work, discussion,
  novelty, comparison, or claim-support wording. Read `references/writing-bridge.md`.

## Default paper card

When the user has not specified a format, answer with:

1. 这篇文章解决什么问题
2. 核心方法/系统路线
3. 关键实验和证据
4. 和已有工作的区别
5. 局限性与可攻击点
6. 对中文论文写作的可用价值
7. 可进一步追的关键词和相邻文献

For multiple papers, use a comparison matrix with columns for `problem`, `method`,
`data/system`, `metrics`, `main finding`, `limitation`, and `how to cite/use`.

## Guardrails

- Separate source facts from your interpretation. Mark inference as inference.
- Keep claims proportionate to the evidence in the paper.
- Do not turn one paper into a field-wide conclusion.
- Do not provide a full-paper translation unless the user explicitly asks for full
  translation or side-by-side reading.
- When the task becomes full-paper bilingual translation with figure/table placement,
  use a dedicated paper-reader workflow if available, but keep this skill's engineering
  writing lens for interpretation and reuse.

