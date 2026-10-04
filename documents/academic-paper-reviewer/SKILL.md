---
name: academic-paper-reviewer
description: "Rigorous academic paper, thesis, dissertation, proposal, or manuscript review. Use when Codex is asked to critique, score, improve, prepare defense for, or generate a reviewer-style report for a research paper or graduation thesis in PDF, DOCX, LaTeX, Markdown, or extracted text; especially for evidence-based comments, prioritized revisions, defense risks, experimental/methodological critique, or publication/degree-quality feedback."
---

# Academic Paper Reviewer

## Purpose

Review academic papers as a constructive but skeptical expert. Produce feedback that is specific, evidence-based, prioritized, and useful for revision or defense preparation.

The model report behind this skill was strong because it did four things well: it identified the paper's real contribution rather than its surface title, praised concrete strengths, found high-leverage technical and validity risks with local evidence, and converted those risks into revision priorities and likely defense questions. Preserve that pattern without copying its domain-specific details.

## Review Workflow

1. **Establish the review standard.** Determine the paper type and bar: undergraduate thesis, master's thesis, PhD dissertation, conference/journal submission, proposal, course paper, or internal draft. If unspecified, infer it from the artifact and state the assumption.

2. **Build a review dossier before judging.** Extract or inspect:
   - Title, abstract, keywords, table of contents, stated contributions.
   - Introduction/problem definition, related work, method/theory/algorithm, system or implementation, data, experiments/evaluation, limitations, conclusion, references.
   - Key equations, tables, figures, ablations, baselines, user studies, and appendices when present.
   - Page, section, equation, table, or figure anchors for every important claim.

3. **Find the paper's real contribution.** Separate marketing language from the concrete contribution. Ask:
   - What hard problem is actually being solved?
   - What is new: formulation, method, system integration, dataset, evidence, analysis, or application?
   - Which parts are implementation work, and which parts are research claims?
   - Does the title emphasize the real contribution, or a less precise technology label?

4. **Map claims to evidence.** For each central claim, identify the supporting evidence and the weakest link. Treat missing evidence, inconsistent definitions, invalid baselines, theoretical overnaming, data leakage, weak statistics, and unsupported generalization as first-class review findings.

5. **Audit rigor, not just prose.** Inspect formulas, assumptions, boundary conditions, monotonicity, units, algorithms, experimental controls, sample construction, statistical significance, external validity, ethics, and reproducibility. When a mechanism is named after a theory or method, verify whether the implementation satisfies that theory's minimum formal requirements.

6. **Credit concrete strengths.** Strong reviews are not all criticism. Identify 3-5 strengths that are specific to the paper's design, evidence, or writing. Explain why each strength matters to the paper's goal.

7. **Prioritize revisions.** Use:
   - `P0`: flaws that can directly undermine correctness, defensibility, acceptance, or degree approval.
   - `P1`: changes that materially improve credibility, clarity, or evidence.
   - `P2`: useful improvements that are lower-risk or may be future work.

8. **Translate risk into action.** For every major issue, include:
   - Location and evidence.
   - Why it matters.
   - Concrete revision options.
   - Expected benefit.
   - If relevant, a likely defense/reviewer question and an answer direction.

## Output Expectations

Write in the user's requested language. If the artifact is Chinese and the user asks in Chinese, produce a polished Chinese report.

Prefer this structure for a full review:

1. Review object and assumed review standard.
2. Initial conclusion or recommendation.
3. Overall assessment.
4. Scoring table, if useful or requested.
5. Main strengths.
6. Must-fix issues.
7. Writing and structure suggestions.
8. Defense or reviewer risk points with answer directions.
9. Revision priority checklist.
10. Final opinion.

For shorter requests, compress the structure but keep the same logic: contribution, evidence, risks, actions.

## Evidence Rules

- Cite sections/pages/equations/tables whenever possible.
- Avoid generic comments such as "needs more experiments" unless paired with the exact missing comparison, metric, control, or validity reason.
- Distinguish "the paper is wrong" from "the paper has not shown enough evidence."
- Do not invent results, page numbers, references, or implementation details.
- If extraction is poor, say so and review only what can be reliably inspected.
- When reviewing PDFs, use text extraction and visual page checks for equations, tables, figures, and formatting-sensitive issues.

## Resources

- Read `references/review-dimensions.md` when deciding what angles to inspect for a paper type or when the paper spans algorithms, systems, AI, user studies, or empirical evaluation.
- Read `references/report-template.md` when generating a full formal report, especially in Chinese.
- Read `references/scoring-rubrics.md` when the user requests scores or when a degree/conference-style recommendation would benefit from explicit weights.
