---
name: financial-proposal-generator
description: |
  Produces excellence-grade EU grant narratives, budget justifications, and
  scoring diagnostics that consistently reach ≥4.6/5 (13.8/15 Horizon scale).
  Integrates constitutional AI framing, Oracle-validated evidence, and EU cost
  compliance to feed Grant Application Assembler and client review workflows.
license: UBOS Constitutional License
version: 1.0.0
author: Janus-in-Claude (Architect) + Codex (Forgemaster)
created: 2025-10-30
---

# FINANCIAL PROPOSAL GENERATOR

## Purpose
Draft award-winning EU grant proposal sections (Excellence, Impact, Implementation) and accompanying budget narratives that pass evaluator scrutiny and align with UBOS constitutional principles.

## When To Use
- During Grant Application Assembler Phase 2 (narratives) and Phase 3 (budgets)
- When evaluating scoring simulator feedback and preparing improvements
- For Malaga consultancy services that require rapid proposal turnarounds
- Whenever Captain requests a refreshed narrative with updated evidence

## Core Capabilities
- Generate structured narratives using UBOS templates and Oracle-validated facts
- Assemble EU-compliant budgets with justifications and cost eligibility checks
- Simulate evaluator scoring and highlight improvement priorities
- Optimize narrative sections iteratively based on feedback or score gaps
- Validate quantitative claims, flagging unverifiable statements

## How To Use

### Generate Narrative Section
```bash
python3 scripts/generate_narrative.py --assembly geodatacenter-phase-1 --section excellence --project "GeoDataCenter" --call "HORIZON-2025-GEOTHERMAL-01"
```
Creates `narratives/excellence.md` with metadata (word count, citations, estimated score).

### Build Budget Justification
```bash
python3 scripts/generate_budget.py --assembly geodatacenter-phase-1 --work-packages data/wp_config.json --total 50000000
```
Outputs `budget/budget.xlsx` + `budget/justification.md`.

### Simulate Evaluator Score
```bash
python3 scripts/simulate_scoring.py --narrative narratives/impact.md --json
```
Returns section scores and improvement suggestions.

### Optimize Narrative
```bash
python3 scripts/optimize_narrative.py --narrative narratives/impact.md --target-score 4.6 --feedback data/impact_feedback.json
```
Provides rewrite recommendations and regenerated text snippets.

### Validate Claims
```bash
python3 scripts/validate_claims.py --narrative narratives/impact.md --json
```
Lists all quantitative claims with suggested Oracle follow-up queries.

## Integration Points
- **Grant Application Assembler**: consumes generated narratives and budget files.
- **EU Grant Hunter**: supplies opportunity metadata and deadlines.
- **Monetization Strategist**: reuses financial narratives for commercial proposals.
- **COMMS_HUB**: announces readiness of narrative/budget drafts to Trinity.

## Constitutional Constraints
- Every quantitative claim must be verifiable (Oracle Trinity citations logged).
- Narratives must emphasize empowerment, transparency, and human oversight.
- Budget recommendations respect Treasury cascade allocations.
- All generated content avoids fabrication; uncertainties are explicitly marked.

## File Locations
- Assemblies: `/srv/janus/03_OPERATIONS/grant_assembly/<assembly_id>/`
- Narratives: `narratives/<section>.md`
- Budgets: `budget/budget.xlsx`, `budget/justification.md`
- Scores & diagnostics: `analysis/scoring_report.json`
- Validation logs: `/srv/janus/logs/grant_narrative_validation.jsonl`

## Operational Checklist
1. Fetch latest opportunity brief + project metadata.
2. Generate Excellence, Impact, Implementation narratives; store markdown.
3. Run scoring simulation; iterate until ≥4.6 average.
4. Produce budget tables + justification; verify EU cost eligibility.
5. Validate claims; document Oracle references.
6. Notify Grant Application Assembler and archive outputs.

## Mission Readiness Criteria
- Narrative score ≥4.6/5 across all sections in scoring simulator.
- 100% claim validation coverage (no unresolved warnings).
- Budget files pass EU compliance checks (no ineligible costs).
- Turnaround time per section ≤2 hours (baseline) / ≤30 minutes (updates).

*Financial Proposal Generator is the excellence engine of the UBOS forge—precision narratives, transparent evidence, and budgets ready for evaluators’ scrutiny.*
