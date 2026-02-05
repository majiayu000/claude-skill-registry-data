---
name: target-competition
description: |
  Analyze target competitive landscape including existing drugs, pipeline companies,
  differentiation opportunities, and market maturity assessment.

  Keywords: target competition, landscape, differentiation, pipeline analysis, market share
category: Competitive Intelligence
tags: [competition, landscape, pipeline, differentiation, market]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - drugbank
  - chembl
  - pharma-projects
  - citeline
---

# Target Competition Skill

Comprehensive competitive landscape analysis for targets.

## Quick Start

```
/target-compete EGFR --full
/competition "KRAS G12C" --include pipeline,patents,market
/landscape --target "PD-1" --by-phase
```

## Competition Dimensions

### 1. Approved Drugs

| Metric | Analysis |
|--------|----------|
| Number approved | Competitive intensity |
| Classes/mechanisms | Differentiation opportunities |
| First-in-class | Innovation level |
| Generics/biosimilars | Erosion risk |
| Market share leaders | Key competitors |

### 2. Pipeline Drugs

| Metric | Analysis |
|--------|----------|
| Phase 3 | Near-term competition |
| Phase 2 | Mid-term competition |
| Phase 1 | Future competition |
| Novel mechanisms | Innovation potential |

### 3. Company Coverage

| Metric | Analysis |
|--------|----------|
| Big Pharma | Institutional interest |
| Biotech | Innovation sources |
| Emerging markets | Global competition |

### 4. Patent Landscape

| Metric | Analysis |
|--------|----------|
| Active patents | IP barriers |
| Expiration timeline | FTO timeline |
| White space | Opportunity areas |

## Output Structure

```markdown
# Target Competition: KRAS G12C

## Competitive Landscape Summary

| Dimension | Assessment |
|-----------|------------|
| Approved drugs | 2 (Sotorasib, Adagrasib) |
| Pipeline drugs | 15 |
| Active companies | 18 |
| Patent density | Medium |
| Market maturity | Early-growth |

**Overall Competition**: Medium-High

## Approved Drugs

| Drug | Company | Approval Year | Sales (2023) | Market Share |
|------|---------|--------------|---------------|--------------|
| Sotorasib | Amgen | 2021 | $0.8B | 45% |
| Adagrasib | Mirati | 2022 | $0.2B | 15% |
| Others (off-label) | Various | - | $0.5B | 40% |

## Pipeline Analysis

### Phase 3

| Drug | Company | Differentiation | Timeline |
|------|---------|-----------------|----------|
| GDC-6036 | Gilead | CNS-penetrant | 2025 |
| JDQ443 | J&J | Combination | 2026 |

### Phase 2

| Drug | Company | Differentiation |
|------|---------|-----------------|
| RMC-6236 | Revolution | Oral macrocycle |
| BI 1701963 | Boehringer | Pan-KRAS |

### Phase 1

| Drug | Company | Novel Mechanism |
|------|---------|-----------------|
| 4 compounds | Various | Degraders |
| 3 compounds | Various | Allosteric |

## Company Analysis

### Big Pharma Activity

| Company | Pipeline | Strategy |
|----------|----------|----------|
| Amgen | 2 assets | Market leader |
| Mirati | 2 assets | Innovation |
| J&J | 3 assets | Multiple approaches |
| Roche | 2 assets | Combinations |

### Biotech Activity

| Company | Pipeline | Focus |
|----------|----------|-------|
| Revolution Medicine | 2 assets | Oral macrocycle |
| Kura Oncology | 1 asset | Selective inhibitor |
| BridgeBio | 2 assets | Different indications |

## Patent Landscape

| Metric | Value |
|--------|-------|
| Active patents (US) | 45 |
| Key patents expiring | 2033-2037 |
| Freedom to operate | Challenging |
| White space | Allosteric, degraders |

## Differentiation Opportunities

### Unmet Needs

1. **CNS penetration**: Current drugs don't reach brain mets
2. **Resistance mutations**: G12D, Y96D emerging
3. **Combination therapy**: With SHP2, SOS1
4. **Pan-KRAS**: Beyond G12C

### White Space

| Area | Competition | Opportunity |
|------|-------------|------------|
| CNS-penetrant | Low | High |
| G12D inhibitors | Medium | Medium |
| Pan-KRAS | Medium | Medium |
| Degraders | Low | High (early) |
| Allosteric | Low | Medium |

## Market Dynamics

### Market Evolution

```
2020: No approved drugs
2021: Sotorasib approval (first-in-class)
2022: Adagrasib approval (second-in-class)
2023-2025: Generics, biosimilars enter
2026+: Next-generation launch (CNS, combinations)
```

### Future Outlook

| Year | Event | Impact |
|------|--------|--------|
| 2025 | GDC-6036 launch | CNS opportunity |
| 2027 | Key patents expire | Generic entry |
| 2028 | Multiple 4th-gen | Market fragmentation |

## Strategic Recommendations

### For New Entrants

**Avoid**: Me-too G12C inhibitors (crowded)

**Consider**:
- CNS-penetrant molecules
- Resistance mutation coverage
- Novel mechanisms (degraders, covalent allosteric)
- Combination approaches

**Differentiation Strategies**:
1. **CNS penetration**: Brain metastasis indication
2. **Pan-KRAS**: Broad mutation coverage
3. **Combination-first**: Co-develop with SHP2/SOS1
4. **Resistance-focused**: Target emerging mutations
```

## Competition Scoring

### Market Maturity Index

| Score | Description | Strategy |
|-------|-------------|----------|
| 1 | Novel target, no competition | First-in-class opportunity |
| 2 | Early competition | Fast follow opportunity |
| 3 | Multiple approved | Differentiation needed |
| 4 | Crowded, generics | Avoid or niche focus |

### Competitive Intensity

| Dimension | Weight | Score |
|-----------|--------|-------|
| Approved drugs | 30% | 3/5 |
| Pipeline diversity | 25% | 4/5 |
| Patent density | 20% | 3/5 |
| Company interest | 15% | 5/5 |
| Innovation rate | 10% | 4/5 |

**Overall**: 3.8/5 (High competition)

## Running Scripts

```bash
# Full competitive analysis
python scripts/target_competition.py KRAS --full

# Pipeline only
python scripts/target_competition.py EGFR --pipeline

# Patent landscape
python scripts/target_competition.py ALK --patents

# Company breakdown
python scripts/target_competition.py BRAF --companies
```

## Reference

- [reference/pipeline-analysis.md](reference/pipeline-analysis.md) - Pipeline analysis methods
- [reference/patent-landscape.md](reference/patent-landscape.md) - Patent landscape reference

## Best Practices

1. **Include off-label**: Approved drugs used in other indications
2. **Track discontinued**: Why did programs fail?
3. **Assess innovation quality**: Not all Phase 1s equal
4. **Monitor startups**: Often most innovative
5. **Check conference abstracts**: Early pipeline visibility

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Ignoring off-label use | Include real-world usage |
| Over-counting pipeline | Track active programs only |
| Missing discontinued | Check for terminated trials |
| Late-stage blind spot | Monitor conference abstracts |
| Geographic bias | Include China, Japan, EU
