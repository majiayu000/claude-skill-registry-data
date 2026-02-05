---
name: map-growth-norms-2025
description: NWEA MAP Growth 2025 Norms technical reference for student/school achievement and growth percentile calculations. Use this skill when implementing MAP norm comparisons, calculating student percentile ranks from RIT scores, computing growth percentiles, interpreting seasonal achievement data, or building norm-referenced reporting dashboards. Covers Mathematics, Reading, Language Usage (G2-G11), and Science (G2-G10) with Fall/Winter/Spring seasonal data.
---

# MAP Growth 2025 Norms

## Overview

Official 2025 NWEA MAP Growth normative data derived from 116M+ test events across 13.8M students in 29,720 US public schools (2022-2024). Provides achievement and growth norms for student and school-level comparisons.

## Coverage

| Subject | Student Grades | School Grades |
|---------|----------------|---------------|
| Mathematics | K-12 | K-12 |
| Reading | K-12 | K-12 |
| Language Usage | 2-11 | 2-11 |
| Science | 2-10 | 2-10 |

## Key Concepts

### Achievement Norms
Cross-sectional RIT performance at specific time points. Answers: "How does this score compare to peers?"

### Growth Norms
Change between two assessments. **Conditional** on starting RIT score. Answers: "Is this growth typical for students who started at this level?"

### Seasonal Timing (Weeks from District Start)
- **Fall**: Week 4 (0-12 weeks)
- **Winter**: Week 20 (13-28 weeks)
- **Spring**: Week 32 (29+ weeks)

## Percentile Calculations

### Achievement Percentile

```typescript
function calculateAchievementPercentile(
  ritScore: number,
  mean: number,
  sd: number
): number {
  const z = (ritScore - mean) / sd;
  // Standard normal CDF approximation
  const p = 0.5 * (1 + Math.sign(z) * Math.sqrt(1 - Math.exp(-2 * z * z / Math.PI)));
  return Math.round(p * 100);
}
```

### Growth Percentile (Conditional) - Technical Manual Section 3.3.3

Growth percentiles are **conditional on starting RIT**. Higher starting scores have lower expected growth (regression to mean effect).

```typescript
function calculateGrowthPercentile(
  startRit: number,
  endRit: number,
  normData: GrowthNormData
): number {
  const observedGrowth = endRit - startRit;
  // Conditional mean adjusted for starting RIT (Section 3.3.2)
  const expectedGrowth = normData.meanGrowth +
    normData.regressionCoeff * (startRit - normData.startMean);
  const z = (observedGrowth - expectedGrowth) / normData.conditionalSD;
  return normalCDF(z) * 100;
}
```

→ See: `lib/map/conditional-growth.ts` for full implementation

## Reference Files

See `references/` for complete norm tables:

- **achievement-norms.md**: Mean and SD by grade/subject/season (Student & School)
- **achievement-percentiles.md**: RIT-to-percentile lookup tables
- **growth-norms.md**: Mean and SD for within-year and between-year growth

## Quick Lookup Examples

### Student Achievement (Reading, G4, Spring)
- Mean: 202.09
- SD: 17.74
- A RIT of 210 → ~68th percentile

### Student Achievement (Language Usage, G3, Fall)  
- Mean: 184.42
- SD: 17.37
- A RIT of 195 → ~73rd percentile

## Integration Notes

1. **Always use conditional growth norms** - Marginal growth (ignoring starting RIT) produces misleading percentiles
2. **School norms have smaller SD** - Aggregation reduces variance
3. **Week timing matters** - Norms assume standard seasonal weeks (4/20/32)
4. **EISA concordance applied** - 2025 norms aligned to enhanced item-selection algorithm scores
