---
name: moat-analysis
description: Use this skill to evaluate economic moat sources, durability, evidence, competitive advantages, switching costs, scale economies, network effects, brand, regulation, or cost advantages. Trigger when business quality and defensibility must be judged.
---

# Moat Analysis Skill

## Purpose

Assess the depth, durability, and competitive threats of an economic moat with auditable evidence. For L1+ public-company analysis, include compact quantitative moat checks when data is available; for quick checks, private companies, early-stage loss makers, or non-comparable assets, state what is blocked or deferred.

## Applicability and Depth

Use the smallest useful moat packet:

| Analysis depth | Required treatment |
|---|---|
| L0 quick check | 1-2 sentence moat view; flag missing data |
| L1 standard report | Compact moat table with ROIC spread, inferred moat category, trend, and key threat |
| L2+ full memo | Full multi-method assessment, peer benchmark, and evidence trail |
| Data-blocked / not comparable | Mark as `blocked`, `low-confidence`, or `not applicable`; do not invent scores |

## Combined Moat Evidence Framework

### 1. ROIC Spread / AFOS Test

```
ROIC Spread = ROIC - WACC
AFOS (Asset Franchise Spread) = ROIC - Cost of Capital

Default criteria:
- > 15%      : Wide Moat (Extremely Deep)
- 10%-15%    : Narrow Moat+ (Deep)
- 5%-10%     : Narrow Moat (Moderate)
- < 5%       : Weak or No Moat
```

ROIC spread and AFOS are the same economic spread lens. They may use different naming conventions, but they should not be counted as two independent cross-validation methods.

### 2. Inferred Moat Classification

Do not claim an official Morningstar rating unless an official Morningstar source is provided. Otherwise label the result as `Morningstar-style inferred moat classification`.

| Rating | Meaning | Moat Period | ROIC Characteristic |
|--------|---------|-------------|---------------------|
| Wide Moat | Extremely deep moat | 20+ years | ROIC > WACC + 10% |
| Narrow Moat | Moderate moat | 10-20 years | ROIC > WACC + 5-10% |
| No Moat | No moat | < 10 years | ROIC ≈ WACC |

**Five Moat Sources (select one or more):**
1. Intangible Assets (brand, patents, licenses)
2. Switching Costs (customer lock-in)
3. Network Effects (user/ecosystem stickiness)
4. Cost Advantage (economies of scale, process optimization)
5. Efficient Scale (market structure barriers)

### 3. Competitive Advantage Period

```
Rating Criteria:
- A+ : AFOS > 20%, competitive advantage period > 20 years
- A  : AFOS 15-20%, competitive advantage period 15-20 years
- B+ : AFOS 10-15%, competitive advantage period 10-15 years
- B  : AFOS 5-10%, competitive advantage period 5-10 years
- C  : AFOS < 5%, competitive advantage period < 5 years
```

### 4. Moat Trend Assessment

| Trend | Criteria |
|-------|----------|
| Widening | ROIC rising for 3 consecutive years, or gross margin consistently improving |
| Stable | ROIC maintained at stable high level, competitive landscape stable |
| Narrowing | ROIC declining for 3 consecutive years, new entrant threats increasing, or pricing power weakening |

### 5. Porter's Five Forces Composite Score

Score each force as risk to the company's moat: `1 = moat-friendly / low risk`, `10 = moat-hostile / high risk`.

| Five Forces Dimension | Core Question | Score (1-10) |
|----------------------|---------------|--------------|
| Threat of New Entrants | How high are barriers to entry? Economies of scale required? | 1=Extremely high barriers, 10=Very easy entry |
| Threat of Substitutes | How easy to find substitutes? Customer willingness to switch? | 1=Difficult to substitute, 10=Easy to substitute |
| Supplier Bargaining Power | Supplier concentration? Difficulty of alternative suppliers? | 1=Suppliers have no power, 10=Suppliers are powerful |
| Buyer Bargaining Power | Buyer concentration? Product differentiation? | 1=Buyers have no power, 10=Buyers are powerful |
| Industry Rivalry | Intensity of competition? Degree of differentiation? | 1=Highly differentiated, 10=Commoditized competition |

**Moat Resilience Score = 55 - Five Forces Risk Total**
Range is 5-50. Higher is better.

- 40-50: Extremely wide moat
- 30-39: Wide moat
- 20-29: Moderate moat
- < 20: Weak moat

### 6. Buffett Moat Checklist

| Question | Yes=1, No=0 |
|----------|--------------|
| 1. Can you sell at a higher price than competitors without losing customers? | |
| 2. Are customers dependent on this product/service? | |
| 3. Is the competitive advantage strengthening over time? | |
| 4. Can the company maintain its competitive position without excessive maintenance capex? | |
| 5. Do you have pricing power (can raise prices during inflation)? | |
| 6. Will the company be stronger in 10 years than now? | |

**Score ≥ 4 = Strong Moat**

---

## Moat and Margin of Safety Linkage

Use this as a starting threshold, then adjust for cyclicality, leverage, data confidence, and valuation uncertainty.

| Inferred Moat Rating | Starting Minimum Margin of Safety |
|------------------------|----------------------------------|
| Wide Moat | 20% |
| Narrow Moat | 35% |
| No Moat | 50% or Do Not Recommend |

---

## Inputs

- Target (analysis subject)
- Market
- Industry
- Available data
- User requested depth
- Prior assumptions, if any

## Outputs

### Moat Quantitative Assessment Report

```
0. Status
   - Usable / Low confidence / Blocked / Not applicable
   - Reason if blocked or low confidence: XX

1. ROIC Spread / AFOS Test
   - ROIC: XX%
   - WACC: XX%
   - ROIC Spread: XX% (ROIC - WACC)
   - Rating: [Extremely Wide/Wide/Moderate/Weak]

2. Inferred Moat Classification
   - Overall Rating: [Wide/Narrow/No] Moat
   - Label: [Official Morningstar / Morningstar-style inferred]
   - Moat Sources: [Intangibles/Switching Costs/Network Effects/Cost Advantage/Efficient Scale]
   - Confidence: [High/Medium/Low]

3. Competitive Advantage Period
   - AFOS Value: XX%
   - Rating: [A+/A/B+/B/C]
   - Competitive Advantage Period: XX years

4. Moat Trend
   - Trend: [Widening/Stable/Narrowing]
   - Evidence: [List specific metric changes]

5. Porter's Five Forces Composite Score
   - Risk Total: XX/50
   - Moat Resilience Score: XX/50
   - Strongest Moat Source: XX
   - Largest Competitive Threat: XX

6. Buffett Checklist
   - Total Score: X/6
   - Core Moat: [Description]

7. Margin of Safety Requirement
   - Starting MOS based on moat rating: XX%
   - Adjustments for uncertainty/cyclicality/leverage: XX%
   - Final required MOS: XX%
   - Does current valuation meet requirement: [Yes/No]
```

## Rules

1. **Evidence Required**: Do not state "has moat" or "strong moat" without supporting metrics, peer evidence, or structural evidence.
2. **Avoid False Precision**: Use score ranges and confidence labels when inputs are estimated or stale.
3. **Independent Checks**: Do not count ROIC spread and AFOS as independent methods; pair spread analysis with peer comparison, source-of-moat evidence, and industry structure.
4. **Trend Priority**: Companies with narrowing moats require higher margin-of-safety thresholds.
5. **Peer Benchmark Rule**: When a credible same-industry benchmark exists, compare against the company with the deepest moat, not automatically the largest company.
6. **Conservative Assumption**: When data is insufficient, default to lower moat confidence or block the rating.
7. **Auditability**: Maintain traceability; evidence must support conclusions.
