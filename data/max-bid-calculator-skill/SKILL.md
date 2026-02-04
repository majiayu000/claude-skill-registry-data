---
name: max-bid-calculator-skill
description: Calculate maximum bid using BidDeed formula and bid/judgment ratios to determine BID/REVIEW/SKIP decisions
---

# Max Bid Calculator Skill

Calculates maximum bid amount and decision recommendation using BidDeed.AI proprietary formula.

## When to Use This Skill

- Stage 8 of Everest Ascent pipeline
- After ARV and repair estimates determined
- Before generating final report
- Any time evaluating auction opportunity

## The BidDeed Formula

```
MAX_BID = (ARV × 70%) - Repairs - Holding - MIN(Profit_Buffer, 15% × ARV)

Where:
- ARV: After-Repair Value
- Repairs: Conservative repair estimate
- Holding: $10,000 (standard carrying costs)
- Profit_Buffer: LESSER of $25,000 OR 15% of ARV
```

## Formula Breakdown

### Component 1: ARV × 70%
**Purpose:** Conservative purchase price ceiling
**Reasoning:** Industry standard for value investors
**Example:** ARV $400K → Max $280K (70%)

### Component 2: Repairs
**Sources:**
- Property age/condition assessment
- BCPAO photos inspection
- Drive-by evaluation
- Comparable properties
**Conservative Approach:** Round up, not down
**Example:** Estimate $15-20K → Use $20K

### Component 3: Holding Costs
**Fixed Amount:** $10,000
**Covers:**
- Property taxes (6-12 months)
- Insurance
- HOA fees if applicable
- Utilities during renovation
- Carrying costs

### Component 4: Profit Buffer
**Formula:** MIN($25,000, 15% × ARV)
**Examples:**
- ARV $150K → 15% = $22.5K → Use $22.5K
- ARV $200K → 15% = $30K → Use $25K (capped)
- ARV $500K → 15% = $75K → Use $25K (capped)

**Reasoning:** Guarantees minimum profit while capping risk

## Complete Examples

### Example 1: Lower-Value Property
```
ARV: $180,000
Repairs: $15,000
Holding: $10,000
Profit Buffer: MIN($25K, 15% × $180K) = MIN($25K, $27K) = $25K

MAX_BID = ($180K × 70%) - $15K - $10K - $25K
        = $126K - $15K - $10K - $25K
        = $76,000
```

### Example 2: Higher-Value Property
```
ARV: $450,000
Repairs: $35,000
Holding: $10,000
Profit Buffer: MIN($25K, 15% × $450K) = MIN($25K, $67.5K) = $25K

MAX_BID = ($450K × 70%) - $35K - $10K - $25K
        = $315K - $35K - $10K - $25K
        = $245,000
```

### Example 3: Heavy Repairs
```
ARV: $300,000
Repairs: $60,000
Holding: $10,000
Profit Buffer: MIN($25K, 15% × $300K) = MIN($25K, $45K) = $25K

MAX_BID = ($300K × 70%) - $60K - $10K - $25K
        = $210K - $60K - $10K - $25K
        = $115,000
```

## Bid/Judgment Ratio Analysis

After calculating max bid, compare to judgment amount:

```
RATIO = MAX_BID / JUDGMENT_AMOUNT
```

### Decision Rules

**BID (Ratio ≥ 0.75):**
- Strong equity cushion
- Proceed with confidence
- Auto-approve for bidding

**REVIEW (Ratio 0.60 - 0.74):**
- Marginal opportunity
- Human review required
- Flag for Ariel's approval

**SKIP (Ratio < 0.60):**
- Insufficient margin
- Not worth risk
- Auto-reject

## Example Ratio Calculations

### Scenario 1: Strong BID
```
Max Bid: $245,000
Judgment: $280,000
Ratio: $245K / $280K = 0.875 (87.5%)
→ Decision: BID
→ Reasoning: 87.5% ratio = strong value
```

### Scenario 2: Marginal REVIEW
```
Max Bid: $175,000
Judgment: $260,000
Ratio: $175K / $260K = 0.673 (67.3%)
→ Decision: REVIEW
→ Reasoning: Close to threshold, needs human judgment
```

### Scenario 3: Clear SKIP
```
Max Bid: $130,000
Judgment: $285,000
Ratio: $130K / $285K = 0.456 (45.6%)
→ Decision: SKIP
→ Reasoning: Insufficient equity, too risky
```

## Output Format

```json
{
  "arv": 400000,
  "repairs": 35000,
  "holding_costs": 10000,
  "profit_buffer": 25000,
  "max_bid": 245000,
  "judgment_amount": 320000,
  "bid_ratio": 0.766,
  "decision": "REVIEW",
  "reasoning": "76.6% ratio - marginal opportunity, human review recommended"
}
```

## Integration with Pipeline

```python
# Stage 8: Max Bid Calculation
calc_result = max_bid_calculator_skill.calculate(
    arv=arv_estimate,
    repairs=repair_estimate,
    judgment=auction_judgment
)

if calc_result['decision'] == 'BID':
    # Proceed to report generation
    generate_report(calc_result)
elif calc_result['decision'] == 'REVIEW':
    # Flag for Ariel's review
    flag_for_human_review(calc_result)
else:  # SKIP
    # Log and move on
    log_skip(calc_result)
```

## Decision Logging

Every calculation must be logged to Supabase:

```python
supabase.table('auction_decisions').insert({
    'property_id': case_number,
    'arv': arv,
    'repairs': repairs,
    'max_bid': max_bid,
    'judgment': judgment,
    'ratio': ratio,
    'decision': decision,
    'timestamp': datetime.now(),
    'reasoning': reasoning
})
```

## Conservative Adjustments

**When to Add Safety Margin:**
- Unknown property condition → +$5K repairs
- No interior access → +$10K repairs
- Older property (>50 years) → +$15K repairs
- Complex title issues → Reduce ARV by 5%

**Example with Safety Margin:**
```
Base Repairs: $25,000
Unknown condition: +$5,000
Old property: +$10,000
Total Repairs: $40,000 (conservative)
```

## Example Usage

```
"Use max-bid-calculator-skill to calculate bid for property with ARV $350K, repairs $30K, judgment $280K"

"Calculate max bid: ARV $180K, repairs $15K, judgment $150K"
```

## Critical Reminders

1. **Always Use Formula:** Don't deviate from calculation
2. **Conservative Repairs:** Round up, not down
3. **Log Everything:** Track all decisions in Supabase
4. **Respect Ratios:** Don't override threshold decisions
5. **Profit Buffer Caps:** Remember $25K maximum
