---
name: deal-tracker
description: |
  Track pharmaceutical M&A, licensing, and investment deals. Use for competitive
  intelligence, market analysis, and identifying partnership opportunities.

  Keywords: deals, M&A, licensing, partnership, collaboration, acquisition, pharma deals
category: Business Intelligence
tags: [deals, manda, licensing, partnership, investment]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - sec-filings
  - press-releases
  - deal-databases
---

# Deal Tracker Skill

Track pharmaceutical industry deals, M&A, and partnerships.

## Quick Start

```
/deals --oncology --year 2024
/partnership --type licensing --target "EGFR"
/ma-summary --biotech --threshold 100M
```

## What's Included

| Section | Description | Source |
|---------|-------------|--------|
| Deal Feed | Recent announcements | Press releases, SEC |
| M&A Tracker | Acquisitions and mergers | SEC 8-K, 10-K |
| Licensing Deals | In-licensing, out-licensing | Company announcements |
| Partnerships | R&D collaborations | Press releases |
| Investment | Venture capital, IPO | SEC, exchanges |

## Output Structure

```markdown
# Deal Tracker: Oncology Targets (2024)

## Summary
| Metric | Count | Total Value |
|--------|-------|-------------|
| Total Deals | 127 | $45.2B |
| M&A | 12 | $28.5B |
| Licensing | 89 | $14.3B |
| Partnerships | 26 | $2.4B |

## Recent Deals (Last 30 Days)

### M&A
| Date | Acquirer | Target | Value | Type |
|------|----------|--------|-------|------|
| 2024-12-15 | Pfizer | Seagen | $43B | Acquisition |
| 2024-12-10 | BMS | Mirati | $4.8B | Acquisition |

### Licensing
| Date | Licensee | Licensor | Asset | Upfront | Milestones |
|------|----------|---------|-------|---------|------------|
| 2024-12-08 | AstraZeneca | Hengrui | KRAS G12D | $100M | $800M |
| 2024-12-05 | Merck | Daiichi Sankyo | ADC platform | $300M | $1.5B |

## By Target Class

| Target | Deals | Total Value | Avg Upfront |
|--------|-------|-------------|-------------|
| EGFR | 8 | $1.2B | $85M |
| KRAS | 12 | $2.8B | $120M |
| HER2 | 6 | $950M | $78M |

## By Deal Type

| Type | Count | Total Value | Trend |
|------|-------|-------------|-------|
| Acquisition | 12 | $28.5B | ↑ |
| Asset purchase | 45 | $8.2B | → |
| Platform license | 28 | $5.1B | ↑ |
| Co-development | 18 | $1.8B | → |
| Option agreement | 24 | $2.1B | ↓ |

## Key Observations
1. **M&A resurgence**: 12 biotech acquisitions in H2
2. **ADC momentum**: Antibody-drug conjugates dominate
3. **Early-stage focus**: 60% of deals at preclinical/Phase 1
4. **Oncology dominance**: 70% of deal value in oncology
```

## Deal Types

| Type | Description | Typical Structure |
|------|-------------|-------------------|
| Acquisition | Full company buyout | Cash + stock |
| Asset Purchase | Specific asset(s) | Upfront + milestones |
| Licensing | Rights to develop/sell | Upfront + royalties + milestones |
| Co-development | Joint development | Cost/revenue sharing |
| Collaboration | R&D partnership | Funded research |
| Option | Right to acquire later | Option fee + exercise price |
| Spin-off | Company separation | Share distribution |

## Valuation Ranges

| Stage | Typical Upfront | Total Deal |
|-------|-----------------|------------|
| Preclinical | $10-50M | $100-500M |
| Phase 1 | $30-100M | $200-800M |
| Phase 2 | $50-200M | $500M-2B |
| Phase 3 | $100-500M | $1B-5B |
| Approved | $200M-2B | $2B-10B+ |

## Running Scripts

```bash
# Recent deals feed
python scripts/deal_tracker.py --feed --days 30

# Filter by target
python scripts/deal_tracker.py --target EGFR --include licensing,manda

# Deal summary
python scripts/deal_tracker.py --summary --year 2024 --oncology

# Export to CSV
python scripts/deal_tracker.py --export --format csv --output deals.csv
```

## Requirements

```bash
pip install requests beautifulsoup4 pandas
```

## Reference

- [reference/deal-sources.md](reference/deal-sources.md) - Deal data sources
- [reference/deal-structures.md](reference/deal-structures.md) - Deal structure reference
- [reference/valuation-methods.md](reference/valuation-methods.md) - Valuation methodologies

## Best Practices

1. **Verify from multiple sources**: Cross-check deal values
2. **Track milestones: Monitor deal progression
3. **Understand structure**: Upfront vs milestones vs royalties
4. **Compare benchmarks**: Similar deals for reference
5. **Monitor regulatory**: FTC approval may be required

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Misreported values | Check SEC filings |
| Confusing announced vs closed | Track closing conditions |
| Ignoring milestones | Total value often optimistic |
| Currency confusion | Note USD vs local |
| Double counting | Verify unique deals |

## Limitations

- **Private deals**: Terms often undisclosed
- **Delayed reporting**: SEC filings lag announcements
- **Incomplete milestones**: Many undisclosed
- **Value estimates**: Some values are estimates
- **Geographic bias**: US deals better covered
