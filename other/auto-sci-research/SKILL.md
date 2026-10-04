---
name: auto-sci-research
description: "总领型自动科研 Agent skill。用于统筹地理学+体育学研究中的科研自动化、长期记忆、文献库建设、idea 生成、方法设计、数据分析、机器学习、地理空间/遥感、综述与文献计量、SCI 写作、审稿回复、进化档案维护。触发于 auto-sci-research、Auto-sci-research、agent-auto-sci、自动化科研、科研 Agent、跨项目记忆、skill 总控、科研工作流编排、进化档案、AutoSci/OmegaWiki 思路迁移、K-Dense scientific-agent-skills 精简封装等任务。"
---

# Auto-sci-research

This is the umbrella skill for the user's local scientific-agent system. It replaces the earlier public label `agent-auto-sci` while keeping that phrase as a legacy trigger. It does not replace domain skills. It routes work to the right subskill, preserves reusable knowledge, and requires every major improvement to leave a visible evolution record.

Core idea:

`sources -> structured memory -> idea and method design -> data/geo/ML analysis -> manuscript or review -> critique/rebuttal -> evolution archive`

For full paper projects, use the expanded route:

`intake -> topic -> SMART question -> literature search -> literature matrix -> data plan -> processing/code -> analysis -> figures/tables -> draft -> internal review -> formatting/submission -> rebuttal -> evolution record`

## Routing

Use this skill first when the task spans multiple research stages or asks to improve the user's local skills.

### Deliverable-first precedence

Route by the current deliverable, not by topic keywords alone. Green exposure, heat exposure, urban health, spatial equity, accessibility, and SHAP can occur in either a literature review or an empirical manuscript, so they do not select the writing owner by themselves.

- External literature synthesis, review corpus construction, paper-level extraction, Evidence Trace, cross-paper synthesis, conflicting evidence, heterogeneity, literature gaps, review coding, or review drafting routes to `sport-geography-review-bibliometric`. If the review type or domain route is still undecided, place `urban-exposure-review-radar-workflow` before it.
- The user's own data/method/results manuscript drafting or revision routes to `sport-geography-sci-writing`. Add geospatial, ML, data-viz, methodology, or scicomm helpers only when the immediate deliverable requires them.
- For mixed tasks, choose the owner for the current handoff. A frozen empirical Results/Discussion remains owned by `sport-geography-sci-writing` even when it cites literature; review skills may be helpers and must not take over. Do not load both domain owners merely because the topic contains literature and empirical terms; make a later handoff explicit when the deliverable changes.
- If the immediate deliverable is only review evidence structure and explicitly says not to write prose, do not add `sport-geography-sci-writing`, `scipilot-writing-skill`, or `agent-auto-sci-scicomm` as primary owners.

### Academic prose quality-control handoff

Any route that produces manuscript prose, Discussion, Introduction, Conclusion, Abstract, review synthesis prose, rebuttal prose, or substantial academic interpretation must invoke the shared `agent-auto-sci-scicomm/references/academic_prose_style_guard.md` after claims and evidence are stable. This is a writing QC handoff, not a primary research router; it preserves causal, conditional, uncertainty, null, conflicting, and reviewer-relevant boundaries while reducing repetitive defensive contrast.

| Task | Use |
|---|---|
| Full workflow from topic selection to final manuscript | Start here, then read `references/08_full_research_to_manuscript_pipeline.md` |
| Large task that should be split into role-specific agents | Read `references/09_subagent_composition_matrix.md` |
| Reusing academic prompt libraries without copying copyrighted text | Read `references/10_prompt_workflow_from_academic_pdf.md` |
| Integrating Sportpark writing/figure memories or deduplicating local skills | Read `references/11_sportpark_skill_integration_notes.md` |
| Build or update the overall research-agent workflow | `agent-auto-sci-automation` |
| Machine learning, AI model design, SHAP, model evaluation | `agent-auto-sci-ai-ml` |
| Upstream K-Dense ML/AI technical playbooks: scikit-learn, PyTorch Lightning, Transformers, SHAP, time-series ML, GNN, UMAP | `kdense-ml-ai-selected` |
| EDA, statistics, publication figures, tables, dashboards | `agent-auto-sci-data-viz` |
| Upstream K-Dense EDA/statistics/visualization playbooks: matplotlib, seaborn, scientific visualization, NetworkX, Polars, Dask | `kdense-data-viz-selected` |
| Data figure advisor, chart selection, journal-ready plotting, CJK font setup, visual QA | `scipilot-figure-skill` |
| GIS, spatial accessibility, remote sensing, spatial ML | `agent-auto-sci-geospatial` |
| Upstream K-Dense geospatial and remote-sensing playbooks: geomaster, GeoPandas | `kdense-geospatial-rs-selected` |
| Manuscript argument, slides, posters, peer review, journal strategy, rebuttal | `agent-auto-sci-scicomm` |
| Academic polishing, translation, de-AI/humanizing, cover letter, response-to-reviewers, writing lint | `scipilot-writing-skill` |
| Geography and remote-sensing SCI writing: inversion, spatiotemporal change, exposure/accessibility IMRAD sections | `geors-sci-writing-adapter` |
| Upstream K-Dense scientific communication playbooks: writing, peer review, citations, literature review, slides, posters, schematics | `kdense-scicomm-selected` |
| Hypothesis, research design, critical appraisal, evidence grading | `agent-auto-sci-methodology` |
| Urban exposure review workflow, systematic/scoping review, bibliometric + critical review, remote-sensing frontier radar, CV-to-RS idea generation, public health database linkage | `urban-exposure-review-radar-workflow` |
| Sport geography empirical SCI manuscript writing | `sport-geography-sci-writing` |
| Sport geography review, systematic review, bibliometrics | `sport-geography-review-bibliometric` |
| Web-based autonomous deep research | `gpt-researcher` |
| Full academic research suite and ARS workflows | `academic-research-suite` |
| Long-running improve/verify loops | `codex-autoresearch` |
| Local PDF library reading and HTML notes | `codex-paper-reader` |
| Persona or thinking-framework skill distillation | `huashu-nuwa` |
| Academic-writing prompt reuse | `awesome-ai-research-writing` |
| External academic skill selection | `codex-academic-skills-index` |

Read `references/02_subskill_registry.md` when choosing among skills.

## Operating Contract

1. Keep the user's research project persistent. Do not treat a task as a one-off answer if it creates reusable knowledge.
2. Convert useful external repositories into local workflows, not blind copies.
3. Separate memory, workflow, scripts, data, manuscripts, figures, and review feedback.
4. Record failed attempts, rejected ideas, weak evidence, and reviewer objections as first-class knowledge.
5. Never store secrets in skill files, HTML, markdown logs, or committed examples.
6. Every major skill change must update the evolution archive HTML.

### QC visibility protocol

Keep quality control strict internally and quiet externally. Run routine checks—citation and terminology consistency, basic causal-language review, figure/table alignment, routine support checks, style lint, and minor uncertainty checks—silently; do not list each check or announce that work must “pass a gate.” Report a finding only when it could change the current scientific interpretation, estimand, sample, result, or conclusion. Pause for author input only when safe continuation is impossible or a material scientific choice belongs to the author. Present ordinary work in the order `answer -> evidence -> interpretation -> material limitation -> next step`, not as a gate or warning log.

Once a boundary has been stated for the current task, do not repeat it unless new evidence changes it, the current section must independently contain it, or the user requests a full audit.

Treat a result file that conflicts with `CURRENT_STATE` on effect direction or another conclusion-determining fact as a blocking issue: stop interpretation and ask the author to resolve the authoritative value before proceeding.

## Workflow

1. **Scope the task**
   - Identify whether this is literature, idea, method, data, spatial, ML, writing, review, or skill-evolution work.
   - Decide which subskill owns the task and which existing sport-geography skill is relevant.
   - Read `references/00_system_architecture.md`.

2. **Load project memory**
   - Check local project notes, previous skill references, and the evolution archive.
   - For sport geography, reuse the established narrative: public problem -> spatial inequity -> measurement gap -> evidence -> mechanism -> planning implication.

3. **Run the smallest reliable workflow**
   - Prefer reproducible scripts and structured tables when the task repeats.
   - Prefer clear markdown references when the task is judgment-heavy.
   - Use external APIs only when their value justifies setup and security cost.
   - For full manuscript projects, progress phase by phase and keep handoffs explicit.
   - For large tasks, compose subagents instead of creating new standalone skills by default.

4. **Check quality**
   - Verify files, scripts, outputs, citations, figures, and assumptions.
   - For manuscripts, run claim-evidence checks and reviewer-risk scans internally; surface only findings that materially affect interpretation or require author judgment.
   - For data or models, run EDA, leakage checks, baselines, sensitivity, and reproducibility checks.

5. **Update evolution records**
   - Update `<project-root>/agent_auto_sci/evolution_archive/evolution_data.json`.
   - Run `<project-root>/agent_auto_sci/evolution_archive/update_evolution_html.py`.
   - Mention the generated HTML path in the final response.
   - Read `references/04_evolution_archive_protocol.md`.

## Reference Map

- `references/00_system_architecture.md`: total architecture and how AutoSci/OmegaWiki is adapted.
- `references/01_source_learning_notes.md`: what was learned from AutoSci and K-Dense Scientific Agent Skills.
- `references/02_subskill_registry.md`: current local subskill inventory and routing.
- `references/03_api_config_and_security.md`: API configuration, provider roles, and secret-handling rules.
- `references/04_evolution_archive_protocol.md`: how to maintain the HTML evolution archive.
- `references/05_project_routes.md`: current sport-geography review and empirical-manuscript routes.
- `references/06_external_skill_coverage_audit.md`: coverage matrix for AutoSci and K-Dense skills, including what is preserved, adapted, and intentionally excluded.
- `references/07_external_skills_deployment_20260601.md`: 2026-06-01 deployment record for gpt-researcher, nuwa-skill, ARS, autoresearch, paper reader, Codex Academic Skills, and AI writing prompts.
- `references/08_full_research_to_manuscript_pipeline.md`: end-to-end research pipeline from topic selection, literature, data/code, analysis, figures, drafting, review, formatting, and rebuttal.
- `references/09_subagent_composition_matrix.md`: role-specific subagent combinations and handoff schema.
- `references/10_prompt_workflow_from_academic_pdf.md`: private PDF-derived prompt workflow structure, adapted without copying long text.
- `references/11_sportpark_skill_integration_notes.md`: Sportpark writing/figure lessons, duplicate handling, and Darwin-style evaluation boundary.
- `../urban-exposure-review-radar-workflow/references/workflow_playbook.md`: route-specific workflow for reviews, bibliometrics, urban exposure, remote sensing radar, and health database linkage.
- `../kdense-ml-ai-selected/SKILL.md`: selected K-Dense ML/AI package and upstream subskills.
- `../kdense-data-viz-selected/SKILL.md`: selected K-Dense data analysis and visualization package.
- `../kdense-geospatial-rs-selected/SKILL.md`: selected K-Dense geospatial and remote-sensing package.
- `../kdense-scicomm-selected/SKILL.md`: selected K-Dense scientific communication package.
- `../scipilot-figure-skill/SKILL.md`: SciPilot scientific figure advisor and visual QA workflow.
- `../scipilot-writing-skill/SKILL.md`: SciPilot writing, polishing, de-AI/humanizing, cover letter, and rebuttal workflow.
- `../geors-sci-writing-adapter/SKILL.md`: original geography/remote-sensing SCI writing adapter for inversion, spatiotemporal change, exposure, accessibility, and urban-health manuscripts.

## Local Project Files

- `<project-root>/agent_auto_sci/00_AGENT_AUTO_SCI_总览与变更记录.md`
- `<project-root>/agent_auto_sci/evolution_archive/agent-auto-sci-evolution.html`
- `<project-root>/agent_auto_sci/evolution_archive/evolution_data.json`
- `<local-skill-workspace>/external_repos/latest/AutoSci`
- `<local-skill-workspace>/external_repos/latest/scientific-agent-skills`
- `<local-skill-workspace>/external_repos/latest/gpt-researcher`
- `<local-skill-workspace>/external_repos/latest/nuwa-skill`
- `<local-skill-workspace>/external_repos/latest/academic-research-skills-codex`
- `<local-skill-workspace>/external_repos/latest/codex-autoresearch`
- `<local-skill-workspace>/external_repos/latest/Codex-Academic-Skills`
- `<local-skill-workspace>/external_repos/latest/codex-paper-reader`
- `<local-skill-workspace>/external_repos/latest/awesome-ai-research-writing-STRYXTN`

## Must Not Do

- Do not install all third-party skills blindly.
- Do not copy external workflows that require unavailable infrastructure without marking them as optional.
- Do not expose API keys, tokens, private PDFs, unpublished data, or reviewer-sensitive material in HTML.
- Do not copy long text from private prompt PDFs into public skill files.
- Do not create a new subskill when an existing subskill can be extended cleanly.
- Do not skip the HTML evolution archive after a meaningful skill change.
