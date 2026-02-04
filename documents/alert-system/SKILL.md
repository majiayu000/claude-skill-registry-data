---
name: alert-system
description: |
  Automated alert system for key events in drug discovery. Use for tracking
  competitor milestones, clinical trial updates, regulatory decisions, and
  publications of interest.

  Keywords: alerts, monitoring, tracking, notifications, competitive intelligence
category: Intelligence
tags: [alerts, monitoring, notifications, tracking]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - clinicaltrials-api
  - fda-api
  - pubmed-api
---

# Alert System Skill

Automated monitoring and alerting for drug discovery intelligence.

## Quick Start

```
/alerts --create --target "EGFR inhibitors" --events clinical,fda
/alerts --list
/alerts --check my-alert
```

## What's Included

| Alert Type | Description | Sources |
|------------|-------------|---------|
| Clinical Updates | Trial status changes | ClinicalTrials.gov |
| Regulatory | FDA/EMA decisions | FDA, EMA |
| Publications | New papers on target | PubMed |
| Competitor | Pipeline updates | Press releases |
| Patent | New patent filings | USPTO, EPO |
| Conference | Meeting abstracts | ASCO, ESMO |

## Alert Configuration

```yaml
name: EGFR Competitive Alerts
description: Monitor EGFR inhibitor landscape

targets:
  - EGFR
  - Exon 19 deletion
  - T790M
  - C797S

competitors:
  - AstraZeneca
  - Johnson & Johnson
  - Roche

events:
  - clinical_trial_updates
  - regulatory_approvals
  - publications
  - patent_filings

filters:
  phase: [2, 3]
  countries: [US, EU, CN, JP]
  minimum_significance: high

notifications:
  email: user@example.com
  frequency: weekly
  format: summary
```

## Output Structure

```markdown
# Alert Report: EGFR Landscape (Weekly)

## Summary
| Alert Type | New | Total |
|------------|-----|-------|
| Clinical Updates | 3 | 127 |
| Publications | 12 | 456 |
| Regulatory | 1 | 23 |
| Patent Filings | 5 | 89 |

## Clinical Trial Updates

### New Trials
| NCT ID | Sponsor | Phase | Indication | Status |
|--------|---------|-------|------------|--------|
| NCT01234567 | AstraZeneca | 3 | NSCLC | Recruiting |
| NCT01234568 | Johnson & Johnson | 2 | NSCLC | Not recruiting |

### Status Changes
| NCT ID | Previous | Current | Date |
|--------|----------|---------|------|
| NCT07890123 | Recruiting | Active, not recruiting | 2024-12-10 |

## Key Publications

1. **Fourth-generation EGFR inhibitors targeting C797S**
   - Journal: Nature Cancer
   - Date: 2024-12-08
   - Authors: Zhang et al.
   - Impact: Novel scaffold for resistance

2. **Combination therapy: EGFR + MET inhibition**
   - Journal: Lancet Oncology
   - Date: 2024-12-05
   - Authors: Smith et al.
   - Impact: Positive Phase 2 results

## Regulatory Updates

### FDA Actions
| Date | Sponsor | Action | Drug |
|------|---------|--------|------|
| 2024-12-12 | AstraZeneca | Approval | Tagrisso (adjuvant) |

## Patent Filings

### New Patents
| Date | Assignee | Title | Patent No. |
|------|----------|-------|------------|
| 2024-12-10 | Merck | EGFR C797S inhibitors | US2024/XXX |
| 2024-12-08 | Roche | Antibody-drug conjugate | EPXXX |

## Recommendations

**Action Items**:
1. Review new C797S inhibitor paper - assess differentiation
2. Monitor AstraZeneca adjuvant approval impact
3. Investigate Merck's new patent - potential FTO issue
```

## Event Types

| Event | Description | Priority |
|-------|-------------|----------|
| Clinical trial starts | New trial initiated | Medium |
| Clinical trial completes | Primary endpoint reached | High |
| Regulatory approval | Drug approval | High |
| Regulatory rejection | CRL, rejection | High |
| Key publication | High-impact paper | Medium |
| Competitor deal | M&A, licensing | High |
| Patent granted | New patent issued | Medium |
| Patent expiry | Patent expires | Low |

## Running Scripts

```bash
# Create new alert
python scripts/alert_system.py --create my-alert --target "EGFR"

# Check for updates
python scripts/alert_system.py --check my-alert

# List all alerts
python scripts/alert_system.py --list

# Export alert history
python scripts/alert_system.py --export my-alert --format csv
```

## Requirements

```bash
pip install requests schedule

# For persistence
pip install sqlalchemy
```

## Reference

- [reference/alert-types.md](reference/alert-types.md) - Alert type reference
- [reference/data-sources.md](reference/data-sources.md) - Data source configuration
- [reference/notifications.md](reference/notifications.md) - Notification setup

## Best Practices

1. **Set specific targets**: Narrower = fewer false positives
2. **Use appropriate frequency**: Daily for high-priority, weekly for others
3. **Review regularly**: Alerts need human interpretation
4. **Adjust filters**: Refine based on signal-to-noise
5. **Document actions**: Track alert-driven decisions

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many alerts | Narrow target/event filters |
| False positives | Add confidence filters |
| Alert fatigue | Adjust frequency and thresholds |
| Missing context | Include summary with links |
| No action tracking | Document response to alerts |

## Alert Frequency Guidelines

| Priority | Check Frequency | Notification |
|----------|-----------------|--------------|
| Critical | Hourly | Immediate |
| High | Daily | Daily digest |
| Medium | Weekly | Weekly summary |
| Low | Monthly | Monthly report |
