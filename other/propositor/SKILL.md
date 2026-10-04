---
name: propositor
description: >-
  Commercial proposal generator requiring estimator output. Creates professional,
  client-adapted proposals with 5 templates (dev, refonte, TMA, audit, ao-public).
  Adapts tone to client type (startup/PME/grand-compte/public/GMS/industriel).
  Generates Mermaid Gantt charts and validates data coherence. Interactive workflow
  with checkpoints. Use when preparing quotes, responding to RFPs, formalizing offers,
  or user says "proposition commerciale", "propale", "offre", "devis".
  Not for estimation (use estimator first), invoicing, or contract legal review.
---

# Propositor — Commercial Proposal Generator

## Overview

Propositor generates professional commercial proposals from Estimator output through an interactive 4-phase workflow. Adapts content, tone, and structure to client type and project template.

## ⚠️ Critical Dependency

**Propositor requires Estimator output** — No standalone mode.

```
┌─────────────────────────────────────────────────────────────────┐
│  estimator output (Markdown)  ────►  PROPOSITOR  ────►  Proposal │
│         MANDATORY                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Data Retrieval

| Context | Mechanism |
|---------|-----------|
| Same conversation | Automatic detection of Estimator output |
| New conversation | Request file upload or paste content |

## Quick Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    What type of proposal?                        │
└─────────────────────────────────────────────────────────────────┘
                            │
    ┌───────────┬───────────┼───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼
┌───────┐  ┌────────┐  ┌────────┐  ┌───────┐  ┌──────────┐
│  DEV  │  │REFONTE │  │  TMA   │  │ AUDIT │  │ AO-PUBLIC│
└───┬───┘  └───┬────┘  └───┬────┘  └───┬───┘  └────┬─────┘
    │          │           │           │            │
    ▼          ▼           ▼           ▼            ▼
 New app   Migration   Maintenance  Technical   Public
 MVP/sprints  plan      SLA/process  review     tender
```

## Main Workflow (4 Phases)

### Phase 1: Client Qualification
**Goal**: Identify client type and calibrate template/tone

1. Retrieve and validate Estimator output
2. Ask client qualification questions
3. Auto-detect: template, tone, detail level
4. Verify data coherence

**📍 Checkpoint 1**: Confirm template + tone selection

→ See [workflow-details.md](references/workflow-details.md) for checkpoint format

### Phase 2: Structure & Outline
**Goal**: Define adapted table of contents

1. Select template structure
2. Identify customizable sections
3. Propose reference projects inclusion

**📍 Checkpoint 2**: Validate structure before writing

### Phase 3: Section-by-Section Writing
**Goal**: Generate content adapted to tone

1. Executive summary
2. Needs understanding
3. Proposed solution
4. Methodology
5. Planning (Gantt)
6. Team
7. Financial proposal
8. Conditions

**📍 Checkpoint 3** (optional): Validate critical sections

### Phase 4: Finalization
**Goal**: Assemble and verify

1. Complete document assembly
2. Final coherence check
3. Generate annexes if needed
4. Suggest critiquor review

**📍 Final Checkpoint**: Complete proposal ready for export

## Templates

| Template | Use Case | Key Sections |
|----------|----------|--------------|
| `dev` | New development | Architecture, sprints, MVP |
| `refonte` | Migration/refactoring | Existing analysis, migration plan |
| `tma` | Maintenance contract | SLA, intervention process |
| `audit` | Technical audit | Methodology, evaluation grid |
| `ao-public` | Public tender | DC1/DC2, technical memo, BPU |

→ See [templates.md](references/templates.md) for detailed structures

## Client Type Adaptation

| Client Type | Tone | Vocabulary | Detail Level |
|-------------|------|------------|--------------|
| Startup | Direct, modern | Tech assumed | Concise |
| PME | Professional, accessible | Simplified | Balanced |
| Grand compte | Corporate, formal | Business | Detailed |
| Public | Administrative, precise | Regulatory | Very detailed |
| GMS | Pragmatic, ROI | Retail business | Results-focused |
| Industriel | Technical, rigorous | Domain-specific | Technical |

→ See [tone-adaptation.md](references/tone-adaptation.md) for writing guidelines

## Commands Reference

### During Session

| Command | Action |
|---------|--------|
| `valider` | Confirm checkpoint |
| `modifier-section [name]` | Edit a section |
| `ajouter-reference [project]` | Add client reference |
| `changer-ton [formel/standard/direct]` | Adjust formality |
| `changer-template [name]` | Switch template |
| `regenerer [section]` | Regenerate specific section |
| `previsualiser` | Preview current document |
| `exporter` | Generate final document |
| `critiquor` | Launch quality review |
| `skip-checkpoints` | Disable optional checkpoints |

### Launch Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--template [name]` | Force template | Auto-detected |
| `--client-type [type]` | Force client type | Auto-detected |
| `--ton [level]` | Force tone level | Auto by client |
| `--with-gantt` | Include Gantt chart | ✅ if >30 JH |
| `--with-references` | Include references section | ✅ |
| `--with-cv` | Include team CVs | ❌ |
| `--validite [days]` | Offer validity period | 30 days |

## Coherence Validation

Propositor automatically checks:

| Check | Rule | Action if Failed |
|-------|------|------------------|
| Amounts | Lot total = Σ lines (±1%) | Alert + correction |
| Budget | Total = Σ lots | Blocking alert |
| Planning | Duration realistic vs JH | Informative alert |
| FCT refs | All FCT-xxx exist | Informative alert |
| Placeholders | No [XXX] remaining | Blocking alert |

## Output Format

Propositor generates structured Markdown with:
- Professional formatting
- Mermaid Gantt diagrams
- Tables for financial data
- Ready for PDF/DOCX conversion

→ See [output-format.md](references/output-format.md) for complete template

## Critical Rules

1. **Estimator mandatory** — Never generate without valid input
2. **Coherence validation** — Alert on detected issues
3. **Interactive workflow** — Checkpoints at key sections
4. **Tone adaptation** — Automatic per client type
5. **Gantt auto-generation** — From JH if >30 JH
6. **User's language** — Output in input language
7. **Suggest critiquor** — Always before final export

## Synergies

### Inputs From
- `estimator` → **MANDATORY** — Complete costing
- `brainstormer` → Report for "Needs Understanding"
- `planificator` (future) → Detailed planning

### Outputs To
- `critiquor` → Quality review before sending
- `negociator` (future) → Negotiation preparation
- `translator` (future) → International version
- `tracker` (future) → Signed proposal tracking

## Client References (Optional)

If file `references.md` exists in context:
- Propositor uses it for References section
- Format: standardized project cards
- If empty or absent: ask user preference

## Limitations

This skill does NOT handle:
- Cost estimation (use `estimator`)
- Price negotiation (see `negociator`)
- Translation (see `translator`)
- Invoicing or accounting
- Contract legal review (CGV provided by user)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-15 | Initial release |

## Current: v1.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
