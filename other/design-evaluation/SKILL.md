---
name: design-evaluation
description: "Evaluate one design or a user-approved maturity-mapped batch through a transparent evidence-based rubric. Classify each work, score design quality and presentation, identify Critical risks, report evidence confidence, and optionally shortlist works within separate maturity tracks. Use when a user asks to judge, score, critique, review, diagnose, batch-evaluate, or rank designs by evidence-aligned evaluation score. Do not use this skill to retrieve winners, choose an award, produce a redesign, audit submission-file compliance, simulate an official jury, or predict winning probability."
---

# Design Evaluation

## Purpose

Evaluate design quality consistently without pretending that a score is an award outcome. Keep design quality, presentation quality, and evidence confidence separate. Require the user to choose the maturity track.

## Scope Boundary

- Evaluate the supplied design and supplied presentation materials.
- Classify one primary discipline, one primary sector, and optional secondary labels and focus tags.
- Build an evidence ledger before scoring.
- Score the general rubric and report Critical findings separately.
- Apply an optional award-aligned lens only when the user already names a target award.
- Batch-evaluate a fixed corpus only after the user approves the maturity mapping for every included record.
- Produce score-based shortlists within each maturity track; never cross-rank Student Concept and Mature Work.

Do not:

- infer or change the work maturity;
- retrieve award winners inside this skill;
- recommend which award to enter;
- turn findings into a full redesign proposal;
- audit upload limits, filenames, declarations, licences, or portal compliance;
- call the result an official iF, Red Dot, or other jury decision;
- estimate an exact probability of winning.
- label a rank percentile, top-decile membership, or score as a winning probability.

Route winner retrieval to `$design-award-search`, award selection to `$design-award-match`, concrete redesign work to `$design-optimization` when available, and final package compliance to `$design-submission-check`.

## Required User Input

Accept images, a PDF, project text, a portfolio page, video frames, prototype evidence, test records, or a structured brief.

Maturity is mandatory and must come from the user. Accept exactly:

- `Student Concept` / `学生概念`
- `Mature Work` / `成熟作品`

If maturity is absent, ask exactly one question and stop scoring:

`请选择作品成熟度：“学生概念”或“成熟作品”。`

Never infer maturity from the author's identity, image finish, prototype appearance, commercial branding, or supplied metadata. If evidence conflicts with the selected maturity, preserve the user's selection and record `Maturity evidence mismatch`.

For a batch, an explicit user-approved mapping rule counts as user selection for every record matched by that rule. Reject unmatched values rather than inferring them. Record the mapping rule and `maturity_source: user` in the batch manifest.

Offer this template when the user asks how to use the skill:

```text
Project: {name}
Maturity: Student Concept | Mature Work  # selected by the user
Primary function: {what it does}
Target user: {who uses it}
Use context: {where and when}
Materials: {attachments or links}
Evaluation mode: General | optional named award-aligned lens
```

## Evaluation Workflow

For batch work, first read [references/batch-evaluation.md](references/batch-evaluation.md). Use `scripts/batch_evaluation.py` for deterministic scoring, failure isolation, and separate-track shortlisting. Use a project adapter for private database access; never bundle database rows, images, signed URLs, or credentials in the public Skill.

### 1. Confirm the user-selected maturity

Record:

```yaml
maturity: student_concept | mature_work
maturity_source: user
```

Do not proceed with a numeric score when `maturity_source` is missing or is not `user`.

### 2. Build the evaluation profile

Read [references/classification-policy.md](references/classification-policy.md) and `references/profiles/classification.json`.

Extract:

- primary function, target user, use context, and claimed outcome;
- one primary design discipline and up to two secondary disciplines;
- one primary application sector and up to one secondary sector;
- zero or more focus tags;
- supplied material types and obvious material limitations.

The classification confidence is separate from evaluation confidence. Ask no additional question when a reasonable classification can be stated as an assumption.

### 3. Build the evidence ledger

Read [references/evidence-policy.md](references/evidence-policy.md). For every scored dimension, assign exactly one evidence state:

- `Verified`
- `Supported`
- `Claimed`
- `Missing`

Attach concise evidence references and distinguish observable facts from author claims and evaluator inference.

### 4. Load the rubric

Read [references/evaluation-framework.md](references/evaluation-framework.md).

Load:

1. `references/profiles/core.json`;
2. the user-selected maturity profile;
3. the relevant classification overlay in `references/profiles/sector-overlays.json`;
4. an optional aggregate benchmark context resolved by `scripts/benchmark_profiles.py`;
5. an optional file from `references/profiles/award-lenses/` when the user names that target.

Award lenses produce a separate alignment section. Never replace or mathematically blend the general score with an award-aligned result.

For the main iF context, read [references/if-benchmark-methodology.md](references/if-benchmark-methodology.md). Resolve an exact normalized category profile first, then its mapped discipline profile, then the core fallback.

For iF Student context, read [references/if-student-benchmark-methodology.md](references/if-student-benchmark-methodology.md). Load it only after the user has selected `student_concept`. Reject it for `mature_work`. Treat its 15 SDG categories as issue themes, never as evidence of product, communication, interface, spatial, or other design discipline. Resolve a high-sample SDG theme first and otherwise use the competition-wide student profile.

For Red Dot context, read [references/red-dot-benchmark-methodology.md](references/red-dot-benchmark-methodology.md). Keep Product Design, Brands & Communication Design, and Design Concept separate. Resolve an exact high-sample category first, then an explicitly supplied competition line, then the mapped evaluation discipline, then the core fallback. Never infer the Red Dot competition line from maturity.

For IDEA context, read [references/idea-benchmark-methodology.md](references/idea-benchmark-methodology.md). Resolve an exact high-sample category first, then a supplied or provisionally mapped discipline, then the program-wide context. Treat its discipline profiles as multi-label and non-additive. Load `Student Designs` only for `student_concept`, and never infer discipline from that category.

Treat every bundled benchmark profile as observed winner context with `score_effect: none`; use it to choose evidence questions and explain presentation coverage, never to change weights or predict an award result.

### 5. Score from evidence

Assign a raw score from 0 to 5 to all seven design dimensions and six presentation dimensions. Give one short reason for every score.

The general score allocates 50 points to design quality and 50 points to presentation quality.

Use `scripts/score_evaluation.py` for deterministic weighting and profile validation. The score is:

```text
weighted contribution = raw score / 5 * dimension weight
general score = design score + presentation score
```

Apply evidence caps from the framework. Evidence confidence does not otherwise add or subtract arbitrary points.

### 6. Identify findings

Separate:

- `Critical`: a fundamental contradiction, unverified safety-critical mechanism, serious harm risk, or a failure that invalidates a core claim;
- `Major`: materially reduces design quality or credibility but does not invalidate the whole proposal;
- `Minor`: local weakness with limited effect.

Critical findings cannot be cancelled by the average score. Evaluation findings describe the problem and its consequence; leave detailed redesign instructions to the optimization module.

### 7. Apply optional benchmark evidence

Consume either:

- a verified benchmark set supplied by the user or produced by `$design-award-search`; or
- the bundled aggregate iF context when the user targets iF or an iF category can be resolved; or
- the bundled aggregate iF Student context only when the user-selected maturity is `student_concept`.
- the bundled aggregate Red Dot context when Red Dot is the named target or its category and competition line are supplied.
- the bundled aggregate IDEA context when IDEA is the named target or an IDEA category is supplied.

For bundled iF context, run:

```text
python scripts/benchmark_profiles.py --category "{raw or normalized iF category}" --discipline "{evaluation discipline}" --pretty
```

For iF Student, run:

```text
python scripts/benchmark_profiles.py --source if_student_observed_winners --maturity student_concept --category "{raw or normalized SDG theme}" --pretty
```

For Red Dot, run:

```text
python scripts/benchmark_profiles.py --source red_dot_observed_winners --category "{raw or normalized Red Dot category}" --competition "{Product Design | Brands & Communication Design | Design Concept}" --discipline "{evaluation discipline}" --pretty
```

For IDEA, run:

```text
python scripts/benchmark_profiles.py --source idea_observed_recognized --maturity "{student_concept | mature_work}" --category "{raw or normalized IDEA category}" --discipline "{evaluation discipline}" --pretty
```

Do not run or load the iF Student benchmark for `mature_work`; the resolver must raise an error. Do not use an SDG theme to infer or replace the user's project discipline. For Red Dot, treat the competition line as explicit target context and never infer it from the project maturity. For IDEA, reject `Student Designs` when maturity is `mature_work`; its student category must not infer or replace project discipline.

State the matched profile, fallback used, sample size, years, review status, and limitations. Keep the benchmark section outside the numeric score calculation. Use it to explain differentiation, missing evidence, and presentation coverage, not hidden jury preferences or winning probability.

### 8. Present the result

Read [references/output-template.md](references/output-template.md). Lead with:

- user-selected maturity;
- classification;
- overall score, design score, presentation score;
- evidence confidence;
- Critical status.

Include the complete dimension table and evidence gaps. End with an explicit limitation statement.

## Scoring Guardrails

- Student Concept and Mature Work are separate tracks; do not rank them directly by total score.
- iF Student benchmark evidence is valid only in the Student Concept track.
- Do not reward unsupported claims because they sound plausible.
- Do not convert missing evidence into invented defects.
- Do not score an inaccessible or unreadable visual detail as observed.
- Keep category relevance and material coverage explicit.
- A high score means strong evidence-aligned design quality under this rubric, not an award forecast.
- Use the term `{award}-aligned assessment`, never `{award} official jury simulation`.
- Call batch output `evidence-aligned evaluation shortlist` or `within-track top decile`, never `award-probability shortlist`.
- Require all expected records to reach a terminal status before finalizing a corpus-wide shortlist; report failed and non-evaluable records separately.
- Exclude unresolved Critical findings and Low-confidence evaluations from the primary shortlist. Preserve them in review queues rather than deleting them.
- Resolve exact ties at the cutoff by including every work with the same total score; report when this makes the shortlist larger than the nominal ratio.

## Example Invocations

- `Use $design-evaluation on this fixed database snapshot. Apply my confirmed maturity mapping, score every evaluable work, and return the within-track top 10% evidence-aligned shortlist. Do not report award probability.`

- `使用 $design-evaluation 评价附件中的学生概念。成熟度由我确定为“学生概念”。`
- `Use $design-evaluation. Maturity: Mature Work. Evaluate the product photos, test summary, and entry boards.`
- `使用 $design-evaluation，以通用体系评价，并附加 iF-aligned 维度映射；不要预测获奖概率。`
