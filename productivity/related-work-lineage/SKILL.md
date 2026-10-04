---
name: related-work-lineage
description: Use when the user wants a related-work survey, technical lineage, task timeline, or paper-map around a baseline paper, research task, benchmark, or project direction.
argument-hint: "[workspace path] [project id] [round id]"
---

# Related Work Lineage

Build a paper-only related-work lineage map. For baseline-paper requests, the baseline paper is a **field-scope detector**, not a method-component seed.

## Boundary

This workflow maps papers only. Dataset, benchmark, method, theory, survey, and system are paper roles, not graph nodes.

This is not Project Understanding Graph truth. Do not append graph events, create D* proposals, mutate Zotero, or mark sources project-core/global-core.

## Core Rule

When user provides a baseline paper:

1. Read the baseline paper first.
2. Extract its primary problem, input/output, benchmarks/datasets, evaluation setting, method/evaluation setting, and claimed contribution.
3. Infer the broader research field structure around that problem.
4. Do not build route lanes from method internals used by the paper.

Wrong:

```text
Baseline uses module X and architecture Y, so lanes are module X internals and architecture Y variants.
```

Right:

```text
Baseline solves problem P, so lanes are broad field-structure positions extracted from
the baseline paper and exploratory search.
```

Method-internal routes are allowed only when the user explicitly asks for method motivation lineage.

## Field Ontology First

In baseline-paper mode, choose route lanes from the field's natural ontology before using the baseline paper's novelty claim.

Ask:

```text
What kinds of problems, target settings, outputs, benchmarks, or paper traditions does this field contain if the baseline paper is removed?
```

Do not ask first:

```text
What components, cues, modules, backbones, losses, or fusion steps does the baseline combine?
```

Prefer candidate lane axes in this order:

1. object of study or target setting;
2. task formulation or output/evaluation object;
3. benchmark/dataset community;
4. application or deployment context;
5. field tradition/problem-position;
6. method/evidence source, only when papers in the field are actually organized that way;
7. baseline method components, forbidden unless `input_mode` is `method_motivation`.

If a candidate lane axis mostly restates the baseline's claimed novelty, demote it to `non_lane_axes` unless the user explicitly asks for method motivation.

## Required Context

Read:

```text
$WORKSPACE/wiki/projects/$PROJECT/overview.md
$WORKSPACE/wiki/projects/$PROJECT/project-query-pack.md
$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/
$WORKSPACE/wiki/projects/$PROJECT/papers/
$WORKSPACE/wiki/_system/workflows/related-work-lineage.md
```

If a path is absent, continue with available context and record the missing path in the artifact.

## Input Modes

### Baseline-Paper Field Survey

Default when user provides one or more anchor/baseline papers.

Before artifact creation, create 3-6 candidate lane axes. For each candidate, record:

- axis name;
- candidate lanes;
- source in baseline paper, project context, or exploratory search;
- why it is field-native rather than baseline-method-native;
- weakness or risk;
- checks for baseline-removal, neighbor-paper fit, project-intent fit, and non-component status;
- decision: `selected` or `rejected`.

Select one lane axis using this rubric:

- it matches project overview/query-pack intent;
- it captures the field's task ontology or paper traditions;
- it organizes neighboring papers without forcing them;
- it remains meaningful if the baseline paper is removed;
- it does not merely restate the baseline contribution.

Required first output before artifact creation if scope or lane-axis selection is ambiguous:

- primary problem;
- input/output;
- benchmark/dataset names;
- evaluation setting;
- candidate lane axes and decisions;
- inferred field-structure lane axis;
- selected field-structure lanes;
- non-lane axes and their visual encoding;
- exclusion rules.

Search field-first, not method-component-first. Run enough distinct searches to cover every derived taxonomy axis plus benchmark/latest and calibration checks.

Do not use a fixed search template such as supervision categories, openness, modality, or architecture families. First derive 3-6 taxonomy axes from the baseline paper:

- categories named in related work;
- groups used in comparison tables;
- datasets/benchmarks and metrics;
- input/output variants;
- field positions or adjacent problem settings;
- limitation/gap language in the introduction and conclusion.

Then generate searches from those derived axes:

- field/problem definition and benchmark query;
- one query per derived taxonomy axis;
- one benchmark/latest query per major dataset or benchmark;
- one survey/SOTA calibration query;
- adjacent-branch queries only when the baseline paper or field boundary supports them.

Record every query in `search_log` with `derived_from`. If a query type could apply to only one domain family, it is probably too hard-coded. Six searches is a common floor for non-trivial topics, not a fixed rule.

### Coarse Direction

When no baseline paper exists, first produce 3-5 candidate field/problem routes with 1-2 baseline papers each. Ask user to choose before creating the lineage map.

### Method Motivation

Use only when user explicitly asks how a method's components evolved. Route lanes may then be method families, model internals, architectures, or representation probes. Mark `route_narrowing.input_mode` as `method_motivation`.

## Artifact Paths

Write/update:

```text
$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/<round>/related-work-lineage.json
$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/<round>/related-work-lineage.md
```

## Artifact Requirements

Baseline-paper field surveys must include:

- `baseline_paper_field_scope`;
- `axis_candidates`;
- `search_log`;
- `routes` as field-structure/problem-position lanes, not method-component lanes;
- `papers` with `field_position`, `method_setting`, and `artifact_type`;
- `survey_catalog`;
- `timeline_tracks`;
- `major_trends`;
- `notable_forks`;
- `explicit_edges`;
- `positioning_note` explaining where the baseline paper sits in field history.

Max 20 papers per artifact. If the field needs more, split rounds by field position, adjacent problem setting, time window, or another derived taxonomy axis.
If a map would exceed that cap, ask the user to narrow or split maps before expanding scope.
Always exclude low-signal follow-ups that only restate the same method or benchmark position without changing the field structure.

## Commands

Create:

```bash
python3 "$PLUGIN_ROOT/tools/related_work_lineage_cli.py" create --repo "$WORKSPACE" --project "$PROJECT" --round "$ROUND" --title "$TITLE" --direction "$DIRECTION" --baseline-paper "$BASELINE" --json
```

Validate:

```bash
python3 "$PLUGIN_ROOT/tools/related_work_lineage_cli.py" validate --path "$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/$ROUND/related-work-lineage.json" --json
```

Render summary:

```bash
python3 "$PLUGIN_ROOT/tools/related_work_lineage_cli.py" render-summary --path "$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/$ROUND/related-work-lineage.json" --output "$WORKSPACE/wiki/projects/$PROJECT/literature-rounds/$ROUND/related-work-lineage.md"
```

## Stop Point

Stop after artifact creation, validation, or summary rendering. Graph updates belong to separate human-gated workflows.
