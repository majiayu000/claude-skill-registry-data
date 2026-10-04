---
name: mdrgnb-meta
description: "Staged v6.1 closure workflow for the adult MDR-GNB current-state diagnostic prediction-model review. Use to screen diagnostic model branches, extract or recover source-verified evidence without conflating missingness, classify algorithms at model level, build bilingual manuscript and supplementary outputs, repair legacy NR/NA and dual-schema workbooks, merge A/B/third/final overlays without cross-entity borrowing, appraise models, maintain the closed 41-report audit pool and 39-report primary diagnostic set, run updates, or execute reproducible release QA."
---

# MDR-GNB diagnostic prediction-model review v6.1

Released v6.1 (closure freeze 2026-08-07). Preserve source artifacts and migrate legacy batches through explicit
crosswalks/change logs; never rewrite a frozen branch. When any v5.9.2 or older package,
incremental overlay, generated workbook, or suspicious bulk `NR`/`NA` is present, read
`references/release-v60-completion-overlay.md`.
For any current screening, extraction, synthesis, manuscript, or handoff task, also read
`references/closure-v61-20260807.md`; it supersedes all older fixed-count and age-sensitivity
statements.

## Declare one phase

- `SCREENING`: read `references/eligibility-protocol-v5.md`,
  `references/regression-cases-v5.md`, `references/pool-governance-v5.md`, and
  `references/closure-v61-20260807.md`.
- `EXTRACTION_SCORING`: read `references/extraction-and-units-v5.md`,
  `references/extraction-data-contract-v56.md`,
  `references/semantic-key-v1.md`, `references/scoring-protocol-v5.md`, and
  `references/execution-and-qa-v5.md`, plus `references/analysis-set-and-taxonomy-v55.md`
  `references/algorithm-taxonomy-v58.md`, and
  `references/supplementary-material-schema-v60.md`.
  Read `references/closure-v61-20260807.md` before using any fixed report count or age rule.
  Read `references/schema-migration-v54.md` when importing
  any v5.3 batch. Read `references/schema-recovery-v57.md` whenever old/new schemas,
  branch overlays, companion tables, or suspicious bulk `NR`/`NA` are present.
- `SYNTHESIS_REPORTING`: read `references/extraction-data-contract-v56.md`,
  `references/synthesis-protocol-v5.md`,
  `references/pool-governance-v5.md`, `references/execution-and-qa-v5.md`, and
  `references/analysis-set-and-taxonomy-v55.md`, plus
  `references/algorithm-taxonomy-v58.md` and
  `references/supplementary-material-schema-v60.md`, and
  `references/release-v60-completion-overlay.md`, then
  `references/closure-v61-20260807.md` last.
- `MIXED`: freeze phases in the order above. Later performance must never influence eligibility.

The v5-series references remain historical implementation building blocks. The v6.0 overlay,
`analysis-set-and-taxonomy-v55.md`,
`algorithm-taxonomy-v58.md`,
`supplementary-material-schema-v60.md`,
`schema-recovery-v57.md`, and
`extraction-data-contract-v56.md` implement protocol v6.0. The v6.0 overlay supersedes
earlier export, placeholder-cleaning, same-entity inheritance, and worksheet-layout defaults.
The v5.8 algorithm taxonomy
supersedes the v5.5 algorithm-family definitions whenever an algorithm field or subgroup is
created. The v5.6 data contract supersedes
earlier missingness, whole-document extraction, merge, and arbitration defaults.
The v6.1 closure overlay is the final authority for active pool cardinality, STU-041,
age handling, screening closure, and current file locations.
Legacy v3/v4 rules, a known-organism
secondary stratum, TRIPOD 2015, and PROBAST 2019 are not active.

## Project identity and sources

Use the user-specified sources:

- locked list: `<USER_HOME>/Desktop/报告ID.xlsx`;
- reports: `D:/下载/mdrgnb/python/pdf_downloads2/纳入/`;
- supplements: `D:/下载/mdrgnb/python/pdf_downloads2/纳入/补充材料/`;
- workflow: `<PRIVATE_WORKSPACE>/mdrgnb/提取工作流_2026-07-20/`;
- v5.4 identity checkpoint:
  `<PRIVATE_WORKSPACE>/mdrgnb/outputs/mdrgnb-first10-v45-2026-07-21/`
  `MDRGNB_诊断预测模型_标准化数据提取表_v4.5_前10篇统一颗粒度_2026-07-21.xlsx`.

`01_Source_Report_Index` in the explicitly frozen workbook and its SHA-256 are the only
report/study mapping authority. Never reconstruct IDs from row order, filenames, or minimum row.
The historical locked source list contains 41 source rows/40 unique reports; the two CRAB-VAP
records are one report. The active closure audit adds STU-041 and therefore contains 41 unique
reports. The primary diagnostic set contains 39 reports after STU-005 and STU-006 remain excluded.

## Eligibility boundary

Include patient/episode-level multivariable models that classify a currently present eligible
MDR-GNB infection, colonization/carriage, positive specimen, or resistant etiology while the
current causative organism is unknown at model use.

Assess eligibility at `report × cohort × outcome × fixed/provisional model branch × T0`.
A report may contain included, excluded, and pending branches. Keep every branch in the audit
inventory, but allow only finally eligible fixed diagnostic branches into synthesis pools.

Exclude a branch when:

- its target is future acquisition, death, recurrence, deterioration, or another future event;
- it uses the known current GNB/Enterobacterales/genus/species/resistance result at T0;
- its analytic cohort is restricted to a known current GNB/Enterobacterales/genus/species;
- it is association-only, laboratory/isolate-only, ineligible phenotype, pediatric-only or
  inseparable, non-human, non-original, or lacks any usable prediction performance.

Keep the known-organism-input and organism-restricted-cohort exclusions separate. Prior
colonization/infection history is not knowledge of the organism causing the current episode.
Culture/AST becoming available after T0 does not make a current hidden state prognostic.
Leakage, absent formula, poor performance, and absent calibration affect appraisal/usability,
not eligibility.

Age scope includes explicit adults, author-defined adults without contrary evidence, no evidence
of pediatric enrollment, and the user-approved >=16 cohort (`ADULT_ACCEPTED_16PLUS`). Treat all
of these as adult in the primary analysis. Do not create a strict-18-year adult sensitivity set.

## Atomic and synthesis architecture

The atomic unit is:

`report × study × cohort × outcome × model × dataset × metric × analysis population × subgroup/timepoint/threshold context`.

Do not equate an atomic row with an independent effect. Assign `independent_cohort_id`,
`dependent_effect_cluster_id`, `model_family_id`, and `synthesis_group_id` explicitly.
Use `SEMKEY_V1` from `references/semantic-key-v1.md` for all 41 active audit reports; retain raw branch keys
and map A/B/third/final entities through `semantic_key_crosswalk.tsv`.

Maintain two pools:

1. immutable historical `AUDIT_POOL_40` plus the append-only STU-041 closure addition, exported
   as active `AUDIT_POOL_41` at report level;
2. versioned diagnostic analysis sets at branch/performance level. The active primary diagnostic
   report set contains 39 reports. There is no active strict-adult sensitivity set.

An excluded report remains in the audit pool. Pending, future-event, known-organism-input,
organism-restricted, inventory-only, or unresolved effects cannot enter a synthesis pool.

## Model algorithm taxonomy

For every fixed eligible or candidate model, apply `references/algorithm-taxonomy-v58.md`.
Algorithm is a model-level entity, never a predictor-domain value. Store the source label,
normalized algorithm, family, superclass, binary traditional-versus-ML code, regularization,
ensemble status, mother-model/derived-score relation, author-designated final status, model role,
and dependency cluster. A point score inherits the algorithm of its fitted mother model; LASSO,
ridge, and elastic-net regression remain traditional statistical models with a separate
regularization label. Data-trained trees, forests, boosting, SVM/KNN, neural/deep models, and
stacked/voting ensembles are machine learning.

Do not select the best AUC from each algorithm family. Multiple algorithms evaluated on the same
participants are dependent effects. The binary traditional-versus-ML subgroup is secondary and
must use either one prespecified effect per independent cohort or a multilevel/cluster-robust
model with `dependent_effect_cluster_id`.

## Manuscript and supplementary-material views

Apply `references/supplementary-material-schema-v60.md`. The workbook is a compact generated view
of long-form facts, not a substitute fact store. Absorb supplement fields into the existing study,
dataset, model, predictor, performance, calibration, appraisal, and limitation sheets. Keep
`03_模型` and `03_预测因子` as separate generated views linked by model and model-family IDs.
Do not create one worksheet per Liu table. Predictor-frequency and other supplementary result
tables are generated later from the adjudicated long-form facts.

Liu 2024 Table S1 and diagnostic predictor-frequency tables may be used only as field-coverage
references. Recompute all values from this review. Do not import its prognostic tables, old
PROBAST aggregate counts, mixed diagnostic/prognostic eligibility, predictor frequencies, or
correlations. Predictor-frequency views count one `report × minimal_construct` among eligible
development reports and retain report/model-family/model denominators separately.

For legacy workbook generation, harmonize old dataset-role aliases to the active controlled
vocabulary while retaining the raw code in the audit facts. A PERFORMANCE row stored as a sibling
of its EVALUATION_CONTEXT must be joined only through an exact context key (including a documented
`<performance_id>_CTX` legacy relation) or adjudicated crosswalk. Export must fail when an observed
performance value lacks model, dataset, or outcome links. Do not display these migration failures
as source non-reporting.

At export, reapply the v5.8 mother-model rule. LASSO/ridge/elastic-net labels are resolved before a
generic logistic-regression mapping; an original unpenalized model must remain separate from later
penalized updates. A regression-derived score, nomogram, or locked rule inherits the fitted mother
model's algorithm and regularization and must expose `mother_model_id`. Only a genuinely
expert-authored rule without a fitted mother remains `EXPERT_OR_HEURISTIC_RULE`.

Dataset views operate at `dataset × analysis population`, not one arbitrary analysis population
per dataset. When one physical development dataset has outcome-specific event counts, emit one
linked row per analysis population/outcome. Reuse counts across development/training/tuning role
instances only through the same physical cohort and an explicit generated link note.

The compact model view must expose, without creating extra worksheets, candidate/final parameter
counts, data modality, feature selection, missing-data handling, continuous-predictor handling,
class-imbalance handling, hyperparameter tuning, optimism correction, sample-size rationale,
intended user/input burden, workflow implementation, impact evaluation, and fairness assessment.
Threshold and calibration rows must also carry model/dataset/outcome links; an observed metric with
blank context is an export failure.

## Dataset role and appraisal

Use one dataset role from the controlled vocabulary in `references/extraction-and-units-v5.md`.
Keep temporal/geographic validation axis orthogonal to investigator relation. A tuning set is not
unbiased evaluation. Fitting and apparent performance on one physical cohort are linked role
instances, not independent cohorts.

Use TRIPOD+AI 2024 at report-component × item and PROBAST+AI 2025 Development per developed/
updated fixed model and Evaluation per model × outcome × dataset × analysis population/
performance context. Never calculate numeric PROBAST totals. Keep eligibility-scope foreign keys
so ineligible/pending branches cannot be merged into eligible appraisal scopes.

## Review and evidence contract

Use independent extraction A/B, TRIPOD A/B, and PROBAST A/B branches plus a third adjudicator for
material disagreements. Freeze branches before comparison. Store source file/hash, locator,
evidence span/cell, raw and normalized values, mapping rationale, reviewer/round/time/confidence,
and separate A/B/final evidence IDs. Use explicit missingness; blanks are invalid tracked facts.
A blank numeric workbook cell is permitted only when its linked fact has an explicit non-observed
status and a reader-facing explanation or audit link.

Extract in stages: source inventory and OCR/table QA, candidate-unit inventory, targeted
unit-specific extraction, numerical verification, independent A/B comparison, then adjudication.
Do not truncate a report or supplement to a fixed character limit and call absent downstream text
`NR`. Do not use one universal wide schema across unlike entities.

Use `OBSERVED`, `NR_SOURCE`, `NA_STRUCTURAL`, `NOT_CALCULABLE`, `NOT_RUN`, `NOT_CAPTURED`,
`UNCLEAR`, `PENDING_REVIEW`, `SOURCE_NOT_ACCESSIBLE`, and `CONFLICT` exactly as defined in the
v5.6 contract. A legacy `NR`, `NA`, or blank migrates to `NOT_CAPTURED` unless source-level or
structural evidence justifies a stronger code. Never use `row.get(field, "NR")` or equivalent.

Never promote a legacy blank/status token, old workbook cell, old evidence ID, generic statement,
or previous `NR_SOURCE` row directly to current `NR_SOURCE`. First rebuild the report source
manifest and verify the main article, every accessible supplement, and every accessible relevant
attachment by opening the real file and recomputing its SHA-256. Then perform a renewed field-specific targeted search
across all manifest files marked accessible and included in complete search. The final evidence
must contain one linked evidence row per searched file, each with its own page/table/section
locator and verified source identity/hash, plus a machine-readable search scope,
the full searched-file list, searched locations, reviewer, v6.0 review round, and rationale.
Absent any one of these, retain `NOT_CAPTURED` or another honest unresolved status. Use
`NA_STRUCTURAL` only with a versioned deterministic `status_rule_id`; free-text "not applicable"
or a legacy `NA` is insufficient. Appraisal-item `NA` remains a valid controlled response.
Declare one frozen source-package root per report and inventory every file under that root,
including files judged irrelevant or inaccessible. The release gate must scan the real directory
tree, reject unregistered files, and validate the inventory reviewer/completeness declaration.
Source IDs, paths, and hashes must be unique. Accessible main reports, supplements, appendices,
attachments, corrections, and registrations are mandatory search sources and cannot be excluded
by setting an include flag to zero.
Use the full fact identity
`report_id × study_id × entity_type × entity_id × field_code`. When historical and overlay facts
share that identity, require exactly one explicit `is_current_01=1`; never use row order, file
order, or "last row wins" as precedence.
For `NA_STRUCTURAL`, load the versioned rule table and evaluate the rule against the fact's
`context_json`; accept only the frozen, approved
`references/structural-rules-v60.tsv`. A merely nonempty or caller-invented rule ID never passes.
In release mode, reject unknown status codes and block `NOT_CAPTURED`, `UNCLEAR`,
`PENDING_REVIEW`, `SOURCE_NOT_ACCESSIBLE`, and `CONFLICT`. Use audit mode only for an explicitly
unfinished audit package, never for a manuscript-ready workbook.

An arbitration/API failure must remain `PENDING_REVIEW`; it must never silently adopt A, B, or
Round 1. Generate human questions only for genuine unresolved judgments, with evidence, a
recommended answer, mutually exclusive choices, and deterministic writeback coordinates.

Legacy recovery is field-level, never whole-row replacement. Resolve generated views in this order:
latest adjudicated v6.0 overlay, same-entity frozen fact, then same-entity legacy increment.
Never inherit a value from another model, dataset, outcome, analysis population, predictor, or
performance entity merely because it belongs to the same study. A narrow final or third-review
table cannot erase richer A/B facts. Header union is archival only; it cannot be called canonical
migration. Before any re-extraction, run `recover_schema_drift_v57.py` to recover mapped values and
materialize companion tables. A/B consensus may be recovered; conflicts and single-branch values
remain open. Identity is `report_id × study_id × entity_id`; unlinked, removed, ambiguous, or split
branch entities remain in the audit ledger and cannot inflate canonical views. Declare required
companion tables with `--require-companion` or `table_family_manifest.json`. Workbook export must
prove through `companion_coverage.tsv` that every observed final companion value is visible in a
generated view and is not displayed as missing. TRIPOD/PROBAST scoring and record-type companions
are part of this same gate. Any `FINAL` branch override requires a field-level adjudication-scope
row with evidence. After recovery, use `export_recovered_workbook_v57.py` or the project-specific
generated-view builder so the written XLSX is reopened and checked against every companion value.

At fact-ingestion time, clean legacy tokens. Literal `NR`, `NA`, `N/A`, `UNKNOWN`, status-code
strings, and blank legacy cells are never `OBSERVED` values. Preserve the legacy cell in the
migration/audit ledger, then materialize an empty typed value plus the justified status. Do not
hide a bad observed value by display-only string replacement. PROBAST/TRIPOD item response `NA`
remains a legitimate controlled answer and is not a legacy placeholder.

## Mandatory gates

Before freezing a batch, run:

```text
python scripts/qa_source_identity_v1.py ...
python scripts/qa_semantic_key_v1.py ...
python scripts/qa_eligibility_consistency_v1.py ...
python scripts/qa_pool_consistency_v1.py ...
python scripts/qa_full40_coverage_v1.py ...
python scripts/qa_extraction_package_v56.py ...
python scripts/qa_algorithm_taxonomy_v58.py --facts ... --mode freeze
python scripts/qa_completion_release_v60.py --facts ... --entities ... --evidence ... --source-manifest ... --mode release
python scripts/qa_schema_recovery_v57.py ...
python scripts/qa_real_recovery_smoke_v57.py ...
python scripts/regression_check.py
```

Run semantic/granularity and coverage QA cumulatively over the current batch plus every previously
adjudicated batch. A report closes only after unit, eligibility, evidence, scoring, dependency,
pool, writeback, and cross-report QA pass with no material open conflict.

## Framework sources

- TRIPOD+AI: https://doi.org/10.1136/bmj-2023-078378
- PROBAST+AI: https://doi.org/10.1136/bmj-2024-082505
