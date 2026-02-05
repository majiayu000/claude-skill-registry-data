---
name: clinical-intelligence
description: |
  Deep analysis of clinical trials including design, enrollment, outcomes,
  and competitive positioning. Use for trial monitoring, landscape analysis,
  and competitive intelligence.

  Keywords: clinical, trials, NCT, enrollment, phase, outcomes, study design
category: Clinical Intelligence
tags: [clinical, trials, intelligence, fda, nmpa]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - clinicaltrials-database
  - fda-database
  - ema-database
---

# Clinical Intelligence Skill

Comprehensive clinical trial analysis for drug development and competitive intelligence.

## Quick Start

```
/clinical NCT03704547
/clinical-intelligence EGFR inhibitors --phase 3
Analyze all trials for KRAS G12C inhibitors
Compare NSCLC trial designs across companies
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| Trial Overview | NCT ID, title, status, dates | ClinicalTrials.gov |
| Study Design | Phase, type, arms, endpoints | ClinicalTrials.gov |
| Enrollment | Target, actual, rate, sites | ClinicalTrials.gov |
| Eligibility | Inclusion/exclusion criteria | ClinicalTrials.gov |
| Outcomes | Primary/secondary endpoints | ClinicalTrials.gov, publications |
| Competitive Map | Similar trials comparison | Aggregated |
| Timeline | Milestones and readouts | Estimated |

## Output Structure

```markdown
# Clinical Trial Analysis: NCT03704547

## Executive Summary
FLAURA2 study evaluating osimertinib ± chemotherapy in first-line
EGFR-mutated NSCLC. **Status**: Active, not recruiting. **Results**: Positive PFS benefit.

## Trial Overview
| Field | Value |
|-------|-------|
| NCT ID | NCT03704547 |
| Title | Osimertinib With or Without Chemotherapy in EGFR-Mutated NSCLC |
| Status | Active, not recruiting |
| Phase | Phase 3 |
| Start Date | November 2018 |
| Primary Completion | October 2022 |
| Sponsor | AstraZeneca |

## Study Design
**Type**: Randomized, double-blind, placebo-controlled

**Arms:**
| Arm | Intervention | N |
|-----|--------------|---|
| Arm A | Osimertinib + chemotherapy | 279 |
| Arm B | Osimertinib + placebo chemo | 278 |

**Primary Endpoint:** Progression-free survival (PFS)
**Key Secondary:** Overall survival (OS), ORR, DoR

## Enrollment
| Metric | Value |
|--------|-------|
| Target Enrollment | 557 |
| Actual Enrollment | 557 |
| Enrollment Rate | On target |
| Sites | 150+ centers |
| Countries | 25+ countries |

## Key Results
- **PFS HR**: 0.62 (95% CI: 0.44-0.89)
- **Median PFS**: 25.5 vs 16.7 months
- **ORR**: 82% vs 74%
- **OS**: Mature (68% events)

## Competitive Landscape
| Trial | Drug | Phase | Status | Readout |
|-------|------|-------|--------|--------|
| NCT03704547 | Osimertinib + chemo | III | Positive | 2023 ESMO |
| NCT04035486 | Lazertinib + amivantamab | III | Recruiting | 2025 |
| NCT04887080 | Furmonertinib + chemo | III | Recruiting | 2025 |

## Site Distribution
| Region | Sites | Patients |
|--------|-------|----------|
| North America | 45 | 180 |
| Europe | 60 | 210 |
| Asia Pacific | 45 | 167 |
```

## Examples

### Trial Lookup
```
/clinical NCT03704547
/clinical-intelligence NCT01234567
```

### By Target/Drug
```
/clinical EGFR trials --phase 3
/clinical "sotorasib" studies
Analyze all KRAS G12C clinical trials
```

### Competitive Analysis
```
Compare osimertinib trials vs competitors
/clinical NSCLC --company AstraZeneca
Map phase III trials in EGFR-mutated NSCLC
```

### Enrollment Analysis
```
/clinical NCT03704547 --focus enrollment
Compare enrollment rates across similar trials
Analyze site distribution for KRAS trials
```

## Running Scripts

```bash
# Fetch trial data
python scripts/fetch_trial_data.py NCT03704547 --output trial.json

# Search for trials by condition
python scripts/fetch_trial_data.py --condition "NSCLC" --phase 3 -o results.json

# Search by drug/intervention
python scripts/fetch_trial_data.py --intervention osimertinib -o osimertinib.json

# Competitive trial mapping
python scripts/fetch_trial_data.py --target EGFR --phase 2-3 --map-competition
```

## Requirements

```bash
pip install requests pandas
```

## Additional Resources

- [ClinicalTrials.gov API](reference/clinicaltrials-api.md)
- [Trial Fields Reference](reference/trial-fields.md)
- [FDA Database Links](reference/fda-resources.md)

## Best Practices

1. **Use NCT ID**: Most precise way to look up trials
2. **Specify phase**: Narrow down to relevant trials
3. **Check status**: Trials may be terminated/suspended
4. **Verify enrollment**: Actual vs target enrollment matters
5. **Cross-reference**: Check publications for results

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many results | Add phase, status, or date filters |
| Outdated status | Trial status changes, verify current |
| Missing results | Results may be in publications only |
| Duplicate trials | Same study may have multiple NCTs |
| Terminated trials | Check why before analysis |
