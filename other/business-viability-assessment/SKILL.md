---
name: business-viability-assessment
description: Assess the commercial and financial viability of a software product, startup idea, MVP, repository, PRD, requirements folder, or concept. Use when the user asks whether a project is worth building or wants demand, competitors, MVP scope, development and operating costs, unit economics, scenarios, risks, validation experiments, or a GO, VALIDATE_FIRST, PIVOT, or NO_GO verdict. Default to a quick advisory answer in chat; create analysis files only when the user explicitly requests artifacts.
---

# Business Viability Assessment

Produce a grounded decision, not a pitch.

## Operating contract

- Treat project claims as hypotheses until evidence supports them.
- Distinguish facts, calculations, assumptions, and judgment.
- Label material assumptions and confidence. Prefer ranges over false precision.
- Use current public sources for prices, market data, competitors, and regulations. Cite claims near their use and include access dates.
- If current research is unavailable, mark external claims unverified and list exact research gaps.
- Never invent statistics, prices, competitors, customer behavior, or sources.
- Keep product source code unchanged.
- Create analysis files only when the user explicitly asks for a saved report, model, or other artifacts.
- Never overwrite an existing assessment unless the user explicitly asks to update it.

## Choose the mode

- **Advisory**: Use by default. Give a concise quick assessment in chat and create no files. Read [references/quick-assessment.md](references/quick-assessment.md).
- **Quick artifacts**: Use only when the user explicitly requests a short saved report. Read the quick reference and the artifact-path rules below.
- **Standard**: Use when the user explicitly requests a complete saved assessment. Read [references/assessment-contract.md](references/assessment-contract.md).
- **Deep**: Use when the user requests investor-grade research, deeper sensitivity analysis, or a reproducible model beyond standard depth. Read the full assessment contract.

Use the smallest mode that satisfies the request. Do not infer artifact authorization from a request for advice.

## Resolve inputs and artifact paths

Capture supplied paths, target customers and markets, currency, forecast horizon, founder context, budget, launch date, and technical constraints. Infer missing values only when the inference is low risk; label it.

For artifact modes:

1. Use a user-specified output path when provided.
2. Otherwise create `analysis/business-viability/<project-slug>-<UTC-timestamp>/`.
3. Sanitize the slug to lowercase letters, digits, and hyphens.
4. If the path exists, add a numeric suffix. Do not reuse or clear it.
5. Record the resolved path, currency, horizon, mode, and source scope in the report.

## Inspect with bounded coverage

Read repository instructions and relevant project, documentation, configuration, schema, deployment, and source files. Ignore generated dependencies, vendor folders, builds, caches, binaries, `.git`, and `node_modules` unless the request specifically requires them.

Do not claim exhaustive coverage. In chat, summarize inspected and skipped scope. In artifact modes, create `coverage-manifest.md` with:

- supplied roots and selection rules;
- files inspected or sampled;
- ignored, binary, generated, inaccessible, or out-of-scope files;
- contradictions and unresolved evidence gaps.

## Run the assessment

1. Summarize the problem, product, users, buyers, value proposition, revenue model, MVP, architecture, contradictions, and unsupported assumptions.
2. Define the core business hypothesis and refusal-to-pay risk.
3. Evaluate demand, alternatives, competitors, differentiation, market access, and realistic market size.
4. Reduce the MVP to the cheapest test of problem importance, repeated use, and willingness to pay.
5. Estimate development, infrastructure, marketing, sales, support, and founder time.
6. Model pessimistic, base, and optimistic economics using the requested currency and horizon.
7. Define risks, validation experiments, pass/fail thresholds, and kill criteria.
8. Return exactly one verdict enum: `GO`, `VALIDATE_FIRST`, `PIVOT`, or `NO_GO`.

Do not derive confidence from a numeric score alone. Weight demonstrated demand and willingness to pay above technical feasibility.

## Validate saved assessments

For quick artifacts, run the bundled validator after writing the report:

```text
python scripts/validate_assessment.py <report-directory> --mode quick --horizon <months> --currency <code>
```

For standard and deep artifacts, validate the required files, horizon, currency,
scenario coverage, and derived financial formulas:

```text
python scripts/validate_assessment.py <report-directory> --mode standard --horizon <months> --currency <code>
```

Invoke it from this skill directory or use the equivalent absolute script path. Use `--mode deep` for deep reports. Fix every reported artifact error before handoff. If no Python 3 runtime is available, report that deterministic validation remains pending.

## Progress and handoff

Send concise host-native progress updates for long assessments: scope, research, model, validation, and handoff. Do not print a fixed progress script when the host has a different update mechanism.

For advisory mode, return the verdict, confidence, strongest evidence for and against, dominant financial assumption, cheapest validation step, and inspected scope.

For artifact modes, also report the collision-safe output path, currency, horizon, validation command and result, skipped scope, and remaining research gaps.
