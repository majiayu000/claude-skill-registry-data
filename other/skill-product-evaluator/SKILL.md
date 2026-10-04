---
name: skill-product-evaluator
description: Benchmark-grounded product-quality evaluation for Codex skills. Use when Codex needs to evaluate, harden, compare, or report on a skill beyond behavior tests by discovering public benchmarks or rubrics, creating realistic product-quality cases, running or reusing skill outputs and traces, and using a read-only LLM-as-a-judge subagent to score artifacts plus process evidence. Use for requests mentioning skill product quality, benchmark-driven eval, product-quality rubric, LLM-as-a-judge for skills, judge score, artifact/process scoring, or turning a skill eval workflow into a reusable report.
---

# Skill Product Evaluator

Use this skill to add a product-quality layer on top of normal skill behavior tests. It does not replace `skill-eval-optimizer`; it extends it with benchmark/source grounding, product-quality cases, judge-ready evidence bundles, and a final quality report.

## Core Rule

Evaluate real artifacts, not vibes. Prefer deterministic checks first, then use `skill_product_judge` as a read-only LLM-as-a-judge over sanitized evidence.

## Workflow

1. Define target and boundary.
   - Identify the target skill folder, users, promised artifacts, positive triggers, negative boundaries, required gates, and adjacent skills.
   - If normal behavior evals do not exist yet, use `skill-eval-optimizer` first.

2. Discover benchmark sources.
   - Use `$anysearch` for live public source discovery when benchmark or rubric grounding is needed.
   - Prefer official, university, standards, benchmark, or primary documentation sources over generic blogs.
   - Record source IDs and derived rubric dimensions in `benchmarks/sources.md`.
   - Read `references/benchmark-discovery.md` for source selection and external API closure.

3. Build a product case pack.
   - Create 8-20 cases in `product_cases.csv`.
   - Include direct positives, implicit triggers, negative controls, missing-evidence or safety gates, and benchmark-inspired product-quality cases.
   - Read `references/case-pack-design.md` before writing the pack.
   - Start from `assets/templates/product_cases.csv` when useful.

4. Run or reuse evidence.
   - Reuse existing behavior outputs when they are still valid and auditable.
   - Run only the new cases needed to cover product-quality gaps.
   - Save final responses, JSONL traces, stderr, style JSON, validation logs, and generated files under the eval directory.
   - Keep permissions minimal. Do not include secrets, cookies, tokens, or private personal data in judge bundles.

5. Build the judge input bundle.
   - Run:

```powershell
python <skill-dir>\scripts\build_judge_input_bundle.py --eval-dir <eval-dir>
```

   - The bundle should include validation evidence, benchmark mapping, case metadata, artifact excerpts, trace byte counts, stderr byte counts, and prior deterministic/style results.

6. Judge product quality.
   - Spawn `skill_product_judge` if available.
   - Give the judge the bundle or a concise evidence brief with real artifact excerpts and validator output.
   - The judge must stay read-only and must not browse, edit files, run commands, or call APIs.
   - Read `references/judge-workflow.md` for judge prompt shape and fallback rules.

7. Save reports.
   - Save the judge JSON to `artifacts/judge/suite_judge_result.json`.
   - Generate or write `product_quality_report.md` and `product_quality_summary.json`.
   - Run:

```powershell
python <skill-dir>\scripts\validate_product_eval.py --eval-dir <eval-dir>
python <skill-dir>\scripts\summarize_judge_result.py --judge-result <eval-dir>\artifacts\judge\suite_judge_result.json --out <eval-dir>\product_quality_report.md
```

## Recommended Layout

```text
evals/skill-eval/<skill-name>/
  benchmarks/
    sources.md
  product_cases.csv
  artifacts/
    validation/
    final/
    product-final/
    judge/
      judge_input_bundle.md
      suite_judge_result.json
  product_quality_report.md
  product_quality_summary.json
```

## Quality Gates

Do not call a skill product-stable unless:

- static validation passes;
- behavior regression cases pass or accepted exceptions are documented;
- benchmark sources are relevant and recorded;
- product-quality cases cover positive, negative, and edge conditions;
- judge has real artifacts or excerpts, not only summaries;
- overall score is at least 80 with no critical failures;
- product score is at least 80 on core cases;
- process score is at least 75 when trace evidence is available;
- residual risks and targeted fixes are written to the report.

## Output Shape

When closing a run, report:

- target skill and eval directory;
- benchmark source count and source families;
- case count and new/reused run split;
- judge score: overall/product/process/benchmark alignment;
- critical failures and noncritical gaps;
- key artifact paths;
- validation commands and any commands that could not run.

