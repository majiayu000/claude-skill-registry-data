---
name: urban-exposure-review-radar-workflow
description: "用于地理学、体育学、城市健康和遥感交叉研究的综述与前沿雷达全流程 skill。触发于绿色暴露、热暴露、体育公园/体育设施暴露、公园/绿地可达性、城市健康、空间公平、遥感热环境、LCZ、Geospatial AI、CV-to-RS、系统综述、范围综述、文献计量+批判性综述、医学公开数据库连接、SCS/Cities/Environment International/Health & Place/Urban Forestry & Urban Greening 投稿路线，以及需要结合 Academic Research Suite/ARS、ars-plan、ars-lit-review、ars-reviewer、论文写作、同行评审、引用核查和完整科研管线的任务。"
---

# Urban Exposure Review Radar Workflow

This skill turns a broad geography + sport + urban health idea into a reproducible review, frontier radar, or review-informed empirical research plan.

It combines two transferable patterns:

- review workflow discipline: project structure, search, screening, extraction, synthesis, drafting, audit, citation export;
- research radar discipline: current-source scanning, remote-sensing / CV transfer analysis, ranked reading queues, publishable idea generation.

## Output Contract

For every substantial request, return these blocks unless the user asks for a smaller answer:

1. `研究定位`: review type, target journal route, contribution boundary.
2. `流程路线`: staged workflow with inputs, outputs, and checkpoints.
3. `检索/雷达策略`: formal databases and, when needed, frontier sources.
4. `提取与编码`: variables, coding fields, quality or bias checks.
5. `分析与图表`: bibliometric, evidence-map, spatial, remote-sensing, or health-linkage outputs.
6. `写作与门控`: manuscript structure, claim-evidence audit, citation and genre checks.
7. `风险与下一步`: failure modes, fallback, and the next concrete action.

If the user asks for an executable setup, create or recommend a project scaffold using `scripts/create_review_radar_scaffold.py`.

## Workflow

1. **Classify the task**
   - Choose exactly one primary route: narrative review, systematic review, scoping review, bibliometric + critical review, frontier radar, empirical study design, or hybrid.
   - If the route is ambiguous, stop at a checkpoint and ask the user to choose.
   - Read `references/workflow_playbook.md`.

2. **Set the journal and contribution boundary**
   - SCS / Cities: emphasize urban governance, planning mechanism, spatial equity, sustainability, policy agenda.
   - Health & Place / Environment International / Environmental Research: emphasize exposure validity, health outcome definition, confounding, causal caution.
   - Urban Forestry & Urban Greening / Landscape and Urban Planning: emphasize green infrastructure, landscape planning, ecosystem and social benefits.
   - Nature-family urban/health outlets: require strong conceptual novelty, data credibility, mechanism, and generalizable contribution.

3. **Separate formal review search from frontier radar**
   - Formal review search uses reproducible databases, queries, dates, filters, deduplication, and screening reasons.
   - Frontier radar uses current sources such as arXiv, OpenReview, CVF, GitHub, Papers with Code, Hugging Face, benchmark pages, and conference workshops.
   - Do not merge radar items into a systematic review corpus unless they pass the same inclusion criteria.

4. **Build the evidence structure**
   - For reviews: design screening table, extraction table, coding framework, evidence map, and claim-evidence map.
   - For bibliometrics: stabilize scope before CiteSpace, VOSviewer, or bibliometrix analysis.
   - For remote sensing: record sensor, spatial resolution, temporal window, index/model, validation data, uncertainty, and scale.
   - For health linkage: record outcome definition, exposure window, confounders, spatial linkage unit, population strata, ethics and privacy limits.

5. **Synthesize by argument, not by paper order**
   - Organize by concept, measurement, method, population, exposure pathway, equity dimension, and planning implication.
   - Use bibliometric maps and radar scans as supporting evidence, not as the sole contribution.
   - Once a formal review corpus or evidence-synthesis route is selected, hand off to `sport-geography-review-bibliometric`; do not hand off to `sport-geography-sci-writing` merely because the topic concerns green/heat exposure, urban health, or spatial equity.
   - Keep `sport-geography-sci-writing` for the separate empirical-manuscript route based on the user's own data, methods, and results.

6. **Gate before writing**
   - Confirm enough evidence exists for the selected route.
   - Confirm every planned figure answers a research question.
   - Confirm causal language is supported by study design.
   - Confirm target journal route fits the evidence.

7. **Write and audit**
   - Draft section by section from extraction notes or verified source material.
   - Run claim-evidence audit for numbers, datasets, methods, effect directions, and policy claims.
   - Run genre audit: narrative, systematic, scoping, and bibliometric reviews use different language.
   - Run citation audit before Word/Pandoc/Zotero export.

## Route Decision Table

Use this table before producing a plan. If two rows fit equally well, ask the user to choose before proceeding.

| User intent | Primary route | Required evidence | Main output |
|---|---|---|---|
| "热点、知识图谱、CiteSpace、VOSviewer、bibliometrix" | Bibliometric + critical review | Stable WoS/Scopus records plus manual coding | Search protocol, bibliometric plan, coding framework, policy agenda |
| "严格综述、PRISMA、健康影响证据" | Systematic review | Reproducible database search, screening reasons, extraction and bias/risk checks | Protocol, PRISMA table, extraction schema, evidence synthesis |
| "这个领域有哪些研究、范围和空白" | Scoping review | Broad transparent search and charting table | Evidence map, concept/method taxonomy, research agenda |
| "写一篇高水平综述但不做穷尽统计" | Narrative / critical review | Curated high-quality literature and explicit inclusion logic | Argument map, conceptual framework, critical synthesis |
| "最近有什么新方法、新论文、新项目" | Frontier radar | Current web sources with dates and source links | Ranked candidates, deep dives, CV-to-RS transfer notes, ideas |
| "设计实证论文/基金选题" | Review-informed empirical design | Literature gap plus feasible data and method path | Hypothesis, data plan, method, validation, target journal |

## Journal Evidence Gate

Bind evidence standard to the target journal before writing.

| Journal route | Minimum contribution | Evidence risks to audit | Required writing emphasis |
|---|---|---|---|
| Sustainable Cities and Society / Cities | Urban governance, planning mechanism, sustainability or equity agenda | Descriptive maps without policy mechanism; weak city-scale implication | Explain how exposure/accessibility evidence changes planning decisions |
| Environment International / Environmental Research | Valid exposure-health linkage and confounding control | Ecological fallacy, temporal mismatch, over-causal language | Define exposure window, outcome, model, confounders, uncertainty |
| Health & Place | Place-health mechanism and population heterogeneity | Thin spatial theory; generic health claims | Connect place, social inequality, behavior, and health pathways |
| Urban Forestry & Urban Greening / Landscape and Urban Planning | Green infrastructure or landscape planning contribution | Green quantity treated as quality; weak design implication | Separate exposure, quality, use, and planning levers |
| Nature-family urban/health journals | Generalizable conceptual or empirical advance | Local descriptive case without broader mechanism | State transferable theory, data credibility, mechanism, and limits |

## Direction Modules

Use the relevant module from `references/workflow_playbook.md`:

- `M1`: bibliometric + critical review.
- `M2`: systematic review.
- `M3`: scoping review.
- `M4`: green exposure / sports park exposure.
- `M5`: green park / sports facility accessibility.
- `M6`: remote-sensing heat exposure.
- `M7`: heat-green compound exposure.
- `M8`: urban exposure + public health or medical databases.
- `M9`: geospatial AI / CV-to-remote-sensing frontier radar.

## Academic Research Suite Subskill

When the request needs a general academic research pipeline beyond the urban-exposure domain workflow, use the vendored subskill at `subskills/academic-research-suite/SKILL.md`.

Use this subskill for:

- deep research, literature review, systematic review, meta-analysis, or fact-checking beyond the domain route table;
- paper outlining, abstract drafting, revision planning, citation checking, disclosure wording, LaTeX/DOCX/PDF formatting guidance;
- peer-review simulation, editorial decision support, reviewer-response roadmaps, or re-review after revision;
- full research-to-paper pipelines, integrity gates, Material Passport style provenance, or experiment planning/validation;
- Claude-style ARS aliases such as `/ars-plan`, `ars-plan`, `/ars-lit-review`, `/ars-reviewer`, `/ars-citation-check`, `/ars-revision`, and `/ars-full`.

Routing rule:

1. First decide the urban-exposure route and journal evidence gate from this parent skill.
2. If ARS is needed, read only `subskills/academic-research-suite/SKILL.md` first.
3. Follow the ARS router there to load a single `WORKFLOW.md` under `subskills/academic-research-suite/ars/`.
4. Do not load the whole vendored suite unless the user explicitly asks for a package audit or update.
5. Keep domain-specific constraints from this parent skill in force: exposure/accessibility/use are not interchangeable, causal language must match study design, and formal review corpus rules remain separate from frontier radar.

Source and license:

- The subskill vendors the Codex-native package `Imbad0202/academic-research-skills-codex` v3.22.0, which is the Codex sibling distribution of `Imbad0202/academic-research-skills`.
- Upstream ARS content recorded in `subskills/academic-research-suite/manifest.json` tracks `Imbad0202/academic-research-skills@17c518b286e48bbcd19fa7d05ec4f7d2aeb01641`.
- The vendored package is licensed under CC BY-NC 4.0. Preserve `subskills/academic-research-suite/LICENSE`, attribution, non-commercial limitation, and modification notes when copying or sharing.

## Checkpoints

Stop and ask for user confirmation when:

- the task could be either systematic review, scoping review, narrative review, or bibliometric review;
- the target journal route changes the expected evidence standard;
- the corpus is too narrow for the claimed contribution;
- frontier radar results are being considered for formal systematic inclusion;
- health-effect language would imply causality from cross-sectional or ecological evidence;
- SAR, street-view, POI, mobile-phone, or medical data would change privacy, data access, or modality assumptions.

## Formal Corpus vs Frontier Radar Handoff

Use this handoff rule whenever radar results and formal review evidence appear in the same task:

1. Label each item as `formal-corpus`, `radar-candidate`, `background-method`, or `excluded`.
2. A `radar-candidate` can become `formal-corpus` only after it passes the same database/search, inclusion, deduplication, and screening rules.
3. If it is too new for WoS/Scopus indexing, use it only in the future agenda or method outlook, not in corpus counts.
4. Record the decision in a handoff table with: title, source, date, status, reason, and permitted manuscript use.

## Failure Modes and Fallbacks

| Failure | Required fallback |
|---|---|
| Database access unavailable | Produce a search protocol and ask the user to export records; do not invent counts |
| Non-OA PDFs missing | Mark as `manual download needed`; do not summarize unavailable full text as if read |
| Radar source changes quickly | Browse or ask for current links; report source dates |
| Too few sports-park papers | Broaden to parks, green/open space, active recreation infrastructure, and facility accessibility |
| Bibliometric maps are descriptive only | Add manual coding and policy/mechanism synthesis |
| Remote-sensing method has no exposure validity | Treat as technical background, not exposure evidence |
| Medical data linkage lacks individual location/time | Use area-level ecological framing and avoid individual causal claims |
| Citation match ambiguous | Ask for user confirmation or use DOI/title matching report |

## Must Not Do

- Do not present bibliometric software output as the main scientific contribution.
- Do not equate accessibility, exposure, availability, quality, and actual use.
- Do not equate green exposure or park proximity with health benefit.
- Do not call a review systematic if search, screening, and exclusion records are incomplete.
- Do not use exact corpus-count language in a narrative review.
- Do not infer health causality from ecological or cross-sectional exposure associations.
- Do not include private PDFs, local absolute paths, API keys, or unpublished reviewer comments in reusable skill files.
- Do not copy external skill text wholesale into the parent workflow. If a licensed upstream skill is vendored as a separate subskill, keep it isolated, preserve attribution and license files, and route through the subskill entrypoint.

## References

- `references/workflow_playbook.md`: route-specific workflow teaching and templates.
- `references/darwin_quality_gate.md`: 95-point quality gate used before merging into the public skill set.
- `references/darwin_ars_subskill_evaluation.md`: Darwin 9-dimension evaluation, test summary, project value, and packaging risk controls for the ARS subskill.
- `subskills/academic-research-suite/SKILL.md`: vendored Codex-native Academic Research Suite router for general research, writing, review, citation, integrity, and pipeline tasks.
