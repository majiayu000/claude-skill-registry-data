---
name: agent-auto-sci-methodology
description: "研究方法论与批判性思维子 skill。用于研究问题 SMART 化、假设生成、机制框架、实验/准实验/观察研究设计、系统综述方法、证据质量评价、偏倚识别、因果边界、理论贡献、空间正义框架和审稿前风险扫描。触发于 hypothesis generation、research design、scientific critical thinking、evidence grading、bias audit、method critique 等任务。"
---

# Agent Auto Sci Methodology

Use this subskill when the research logic itself is uncertain or needs strengthening.

## Fast Workflow

1. Convert broad interests into answerable research questions.
2. Define concepts, constructs, variables, mechanisms, and scope.
3. Generate competing hypotheses or explanations.
4. Choose design: review, observational, quasi-experimental, modeling, or mixed methods.
5. Audit bias, confounding, validity, and evidence strength.
6. Convert critique into concrete changes.

Read `references/research_methodology_workflows.md`.

### Empirical support and exchangeability

Treat empirical support, positivity, and overlap as support-domain diagnostics: they identify where the observed data contain sufficiently comparable treatment variation. They do not by themselves establish conditional exchangeability. Strong overlap does not rule out unmeasured confounding, and rich covariate adjustment does not automatically prove exchangeability. Weak overlap limits which treatment contrasts are identifiable or transportable without extrapolation. Do not describe a local support screen as causal identification proof; causal interpretation also requires the design-specific identification assumptions to be credible.

For full paper projects, this skill owns topic selection, SMART research questions, hypothesis design, innovation diagnosis, feasibility, scope boundaries, conceptual framework, and reviewer-risk logic. When the task spans the whole manuscript lifecycle, coordinate through `auto-sci-research/references/08_full_research_to_manuscript_pipeline.md`.

For deeper K-Dense-style encapsulation:

- `references/k_dense_methodology_mapping.md`: how hypothesis generation, critical thinking, scholar evaluation, and peer-review logic are adapted.
- `references/sport_geography_methodology_playbook.md`: sport geography research questions, spatial justice, exposure mechanisms, bias, and evidence-grading playbook.

## Related Helper Skills

- `hypothesis-generation`
- `scientific-brainstorming`
- `scientific-critical-thinking`
- `scholar-evaluation`
- `statistical-analysis`
- `sport-geography-review-bibliometric`

## Must Not Do

- Do not turn a concept into a measurable variable without stating assumptions.
- Do not treat correlation, SHAP importance, or bibliometric co-occurrence as causal proof.
- Do not claim equity or justice from distribution maps alone.
- Do not hide uncertainty in policy language.

## QC Visibility

Apply routine validity, support, terminology, and causal-language checks silently. Report a methodological boundary when it could change the interpretation, estimand, sample, result, or conclusion. Pause for author input only when safe continuation is impossible or a material identification/design choice requires the author's judgment. Do not present routine checks as a gate log, and do not repeat a boundary already explained in the current task unless new evidence changes it, the section needs it independently, or the user requests a full audit.
