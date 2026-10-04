---
name: design-award-match
description: "Match a design project to supported design-award programs, tracks, and entry categories; apply structural eligibility gates; verify current official rules; compare published criteria and cautiously described winner trends; and output fit, evidence confidence, and submission priority. Use when a user asks which award or category to enter, compares awards, or requests an award-fit analysis. Supports iF, iF Student, Red Dot Product, Red Dot Design Concept, IDEA, DIA, K-Design, GOOD DESIGN AWARD Japan, Core77, James Dyson, and EPDA. Do not use for winner retrieval alone, detailed submission-file compliance, general design evaluation, optimization, or winning-probability prediction."
---

# Design Award Match

## Purpose

Identify the most defensible award, program, track, and category for a design project. Treat fit scores as transparent decision aids, never as probabilities of winning.

## Scope

- Extract decision-relevant project facts.
- Pre-filter the configured award allowlist with stable eligibility gates.
- Verify all dynamic requirements on current official pages.
- Compare project evidence with published criteria and observable winner trends.
- Score, rank, and explain strategic fit.
- Stop after recommendation; do not audit every submission file or redesign the project.

Use `$design-award-search` for verified same-category winners. Route file format, size, naming, declarations, and upload completeness to `$design-submission-check`.

## Input Contract

Accept a brief, images, PDF, portfolio page, or structured JSON. Extract or request only facts that can change the recommendation:

- primary function, target user, and use context;
- innovation and supporting evidence;
- project state and completion, launch, or release date;
- applicant type, student status, country or region;
- candidate awards, intended cycle, budget, and geographic constraints.

Use the canonical values in [references/category-crosswalk.json](references/category-crosswalk.json). If the primary function is unclear, ask one short question. If an eligibility fact is missing, continue with `Eligibility: Unknown`; never assume a pass.

Offer this template when the user asks how to use the skill:

```text
Project: {name and one-sentence description}
Primary function: {job performed or problem solved}
Target user / context: {optional}
Innovation and evidence: {optional}
Development status / launch date: {optional}
Applicant: {student, individual, studio, company; country/region}
Candidate awards: {optional; omit to search the supported allowlist}
Submission cycle / constraints: {optional year, region, budget}
```

## Workflow

### 1. Build the project profile

Read [../design-judge-shared/category-taxonomy.md](../design-judge-shared/category-taxonomy.md) and [references/category-crosswalk.json](references/category-crosswalk.json). Classify by primary function before appearance. Record one canonical category, no more than two adjacent categories, project state, applicant type, evidence, timing, and constraints. Label material inferences.

For command-line pre-filtering, prepare JSON like [examples/project-profile.example.json](examples/project-profile.example.json).

### 2. Validate and load the supported award set

Read [references/awards/index.json](references/awards/index.json) and [references/award-profile-guide.md](references/award-profile-guide.md). Analyze only the programs in the allowlist. Treat Red Dot Product and Red Dot Design Concept as separate programs. If a requested award is absent, return `Unsupported` rather than researching and silently adding it.

When a shell is available, validate configuration before analysis:

```powershell
python scripts/validate_award_profiles.py --pretty
```

Build a focused candidate set, normally three to five routes:

```powershell
python scripts/build_candidate_set.py examples/project-profile.example.json --limit 5 --pretty
```

Use `--award` repeatedly to restrict candidates. Award ids and declared aliases are accepted.

### 3. Apply stable gates

Use each selected profile's `routes`, `required_project_fields`, and `stable_constraints`. When needed, run:

```powershell
python scripts/filter_eligible_awards.py examples/project-profile.example.json --include-ineligible --pretty
```

Assign:

- `Eligible`: all stable and current official gates pass.
- `Ineligible`: a confirmed rule excludes the entry.
- `Unknown`: a project fact is missing or any live gate remains unchecked.

Exclude `Ineligible` routes from ranking but state the exact reason. Keep `Unknown` routes conditional.

### 4. Verify dynamic rules live

Read only the selected award profiles under `references/awards/`. For every `dynamic_gate` and relevant `dynamic_field`, verify current official pages at request time:

- cycle status and absolute deadlines;
- applicant, geography, age, enrollment, and graduation rules;
- completion, publication, distribution, or launch windows;
- exact track and category labels;
- current judging criteria;
- enough material and physical-delivery requirements to assess feasibility;
- fees and mandatory winner obligations when they affect priority.

Record direct URL and `checked on: YYYY-MM-DD`. Profile category hints are routing aids only; current official labels control. Never rely on stored dates, fees, category numbers, or remembered requirements.

### 5. Compare criteria and winner evidence

Read [references/evidence-policy.md](references/evidence-policy.md) and [references/criteria-crosswalk.json](references/criteria-crosswalk.json). Display each award's official criterion name; use normalized dimensions only for cross-award comparison.

Map every criterion to concrete project evidence using `Strong`, `Partial`, `Weak`, or `Unknown`. Do not award alignment for generic claims.

Past winners are optional evidence. Use `$design-award-search` or a small verified official-source sample. State sample size, years, category, and limitations. Describe observable `past-winner trends`, never hidden jury preferences.

### 6. Score and rank

Read [references/matching-framework.md](references/matching-framework.md). Score five dimensions from 0 to 5 with one evidence sentence per rating. Prepare input using [examples/match-input.example.json](examples/match-input.example.json), then run:

```powershell
python scripts/score_award_matches.py examples/match-input.example.json --pretty
```

Keep separate:

- `Fit score`: weighted strategic compatibility, 0–100.
- `Evidence confidence`: High, Medium, or Low.
- `Eligibility`: Eligible, Unknown, or Ineligible.

Do not change the numeric fit because confidence is low. Cap `Unknown` at `Conditional`.

### 7. Report

Follow [references/output-template.md](references/output-template.md). Lead with the primary target and reason. Include:

1. project profile and assumptions;
2. ranked shortlist;
3. criterion alignment for top options;
4. eligibility, timing, fee, and mandatory-obligation risks;
5. winner trends only when sufficiently supported;
6. actions that resolve uncertainty or strengthen fit;
7. official sources with checked dates.

Prefer one primary target, one secondary target, and one conditional or stretch option.

## Decision Rules

- Exact program, track, and category fit outranks brand prestige.
- Confirmed ineligibility overrides any fit score.
- Current official rules override profiles, archived pages, third-party summaries, and memory.
- Published criteria control criteria alignment.
- Winner trends may refine but never replace published criteria.
- An open brief such as James Dyson has no exact product-category match; score its category relation as broad.
- A missing universal rubric, as with Core77, lowers criteria-evidence confidence; do not invent criteria.
- If candidates are within five points, prefer higher confidence and fewer unresolved gates.
- A high fit score is not a forecast of winning.

## Fallback and Compliance

- Without live web access, use only user-supplied official documents and mark every dynamic gate unverified.
- If no official category fits, report `No defensible match`.
- If fewer than three comparable winners are verified, omit trends or label them anecdotal.
- Distinguish `current cycle closed` from structural ineligibility.
- Use public pages without login; do not crawl or mirror galleries.
- Store no official images, full descriptions, raw payloads, or content-derived embeddings.
- For James Dyson, use only public official sources; do not reintroduce removed private records.
- Quote minimally and avoid legal, financial, or contractual certainty.

## Example Invocations

- `使用 $design-award-match，基于附件匹配最合适的设计奖、赛道和类别，并输出适配度、资格风险和申报优先级。`
- `使用 $design-award-match，比较 iF、Red Dot、IDEA、DIA 和 Core77 中哪个项目路径最适合这个学生概念。`
- `Use $design-award-match to rank the supported award routes for this project and list every unresolved live eligibility gate.`
