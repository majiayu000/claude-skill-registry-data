---
name: grant-application-assembler
description: |
  Compiles production-ready EU grant proposals from EU Grant Hunter briefs,
  UBOS narrative banks, partner commitments, and budget templates. Reuses the
  proven 1,850:1 ROI methodology that secured €6M Xylella funding. Coordinates
  the full assembly workflow: intelligence gathering, narrative compilation,
  budget construction, partner onboarding, compliance checks, quality scoring,
  and final packaging (PDF/LaTeX). Target score: ≥4.6/5 (Horizon 13.8/15). Use
  when preparing submissions, tracking proposal status, or managing consortium
  deliverables.
license: UBOS Constitutional License
version: 1.0.0
author: Janus-in-Claude (Architect) + Codex (Forgemaster)
created: 2025-10-30
---

# GRANT APPLICATION ASSEMBLER

## Purpose
Transform opportunity intelligence into complete, submission-ready EU grant proposals while safeguarding UBOS constitutional principles. Guides Captain and Trinity through the end-to-end assembly workflow so high-value calls (Horizon, ERDF, Digital Europe) reach the portal with winning scores.

## When To Use
- Immediately after EU Grant Hunter surfaces a high-fit opportunity
- When Captain requests proposal status, timeline, or risk analysis
- Before launching partner outreach or collecting commitment letters
- As deadlines approach to run compliance checks and quality scoring
- When packaging final PDFs/LaTeX deliverables for EU submission portals

## Core Capabilities
- Initialize assembly projects with structured workflows and deadlines
- Compile excellence / impact / implementation narratives from UBOS banks
- Build compliant EU budgets with work-package allocations and justifications
- Track partner commitments, CVs, and documentation readiness
- Run ethics/sustainability/open-science compliance diagnostics
- Generate LaTeX ready submission packages plus scoring simulations
- Maintain assembly state for progress dashboards and risk alerts

## How To Use

### Initialize a New Assembly
```bash
python3 scripts/initialize_assembly.py --opportunity-id HORIZON-CL6-XYL-2026 --project "Xylella Stage 2"
```
Creates `/srv/janus/03_OPERATIONS/grant_assembly/xylella-stage-2/` with workflow, timeline, and state entry.

### Compile Narratives
```bash
python3 scripts/compile_narratives.py --assembly xylella-stage-2 --section excellence
```
Generates `narratives/excellence.md` (markdown + citations). Repeat for `impact` and `implementation`.

### Assemble Budget
```bash
python3 scripts/assemble_budget.py --assembly xylella-stage-2 --total 5000000   --work-packages workplan/wp_config.json
```
Produces `budget/budget.csv` and `budget/budget.md` with EU-compliant tables.

### Track Partner Commitments
```bash
python3 scripts/track_partner_commitments.py --assembly xylella-stage-2 --partner "University of Bari" --status received
python3 scripts/track_partner_commitments.py --assembly xylella-stage-2 --list
```
Updates partner ledger and displays outstanding letters/CVs.

### Run Compliance Checks
```bash
python3 scripts/run_compliance_checks.py --assembly xylella-stage-2 --json
```
Outputs pass/fail report covering ethics, open science, sustainability, and formatting.

### Package Submission & Score
```bash
python3 scripts/generate_submission_package.py --assembly xylella-stage-2
python3 scripts/simulate_scoring.py --assembly xylella-stage-2 --json
```
Creates LaTeX package plus simulated evaluation scores with improvement guidance.

## Integration Points
- **EU Grant Hunter**: Supplies opportunity briefs, deadlines, and fit scores.
- **Malaga Embassy Operator**: Consumes proposal progress for revenue tracking.
- **Financial Proposal Generator**: Provides refined narratives when deeper drafting is needed.
- **Treasury Administrator**: Validates budget allocations against constitutional cascade.
- **COMMS_HUB**: Broadcasts assembly milestones, partner reminders, and submission alerts.

## Constitutional Constraints
- Maintain Lion's Sanctuary framing in every narrative (empowerment, transparency, oversight).
- Provide verifiable citations for claims (Oracle Trinity references logged in metadata).
- Honour Treasury cascade when allocating UBOS internal budgets.
- Respect partner autonomy: commitments are tracked but never coerced.
- Preserve full audit logs (`/srv/janus/logs/grant_assembly.jsonl`) even when filesystem permissions restrict writes (warnings logged).

## File Locations
- Assemblies root: `/srv/janus/03_OPERATIONS/grant_assembly/`
- Global state: `/srv/janus/03_OPERATIONS/grant_assembly/state.json`
- Proposal-specific directories: `assembly_id/{narratives,budget,partners,compliance,submission}`
- Templates & assets: `assets/`
- References: `references/`
- Logs: `/srv/janus/logs/grant_assembly.jsonl`

## Operational Checklist
1. Initialize assembly immediately after opportunity approval.
2. Complete Phase 1 intelligence within 72 hours of kickoff.
3. Schedule weekly progress reviews (dashboard + COMMS update).
4. Lock narratives ≥30 days before deadline (or per rapid schedule).
5. Secure all partner commitments ≥14 days before submission.
6. Run compliance checks ≥10 days before submission.
7. Run scoring simulator and final quality review ≥7 days before submission.
8. Package and submit ≥5 days before official deadline; log submission.

## Mission Readiness Criteria
- ≥90% assemblies submitted ≥5 days before deadline.
- Scoring simulator ≥4.6/5 across excellence/impact/implementation.
- Zero missed compliance requirements or formatting rejections.
- Partner commitment completion ≥95% before submission.
- Malaga revenue targets achieved for client work (tracked via Operator).

*Grant Application Assembler is the forge that turns opportunity into funding—precision-crafted, constitutionally aligned, and ready for €70M-scale victories.*
