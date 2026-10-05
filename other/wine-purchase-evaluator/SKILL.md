---
name: wine-purchase-evaluator
description: Disciplined wine purchase evaluation framework for building a learning-focused cellar with limited storage. Use this skill when evaluating wine purchases from any source (retailers, flash sales, screenshots, PDFs, marathons). Triggers include requests to evaluate/assess/analyze wine purchases, make buy/pass decisions, review flash sales, or compare multiple wine offers. Provides structured BUY/CONSIDER/PASS verdicts with scoring, market analysis, and cellar fit assessment.
---

# Wine Purchase Evaluator

This skill uses preferences from `references/preferences.md` if available. If no preferences file exists, apply the framework with reasonable defaults and ask the user about their specific constraints.

This skill provides a rigorous, storage-aware framework for evaluating wine purchases with a focus on educational value, quality-to-price ratio (QPR), and cellar discipline.

## Core Philosophy

**Default stance: PASS**

Every wine must earn its place against:
- Limited storage (fridge + cabinet + racks)
- Budget constraints
- Your learning priorities
- Existing cellar inventory

**Guiding principles:**
- Discipline beats curiosity
- Rotation beats accumulation
- Learning value trumps status/prestige
- True market price matters, not claimed retail
- Half bottles are educational dead-ends
- Known producers over marketing hype

## Evaluation Workflow

### 1. Auto-Detect Evaluation Type

Determine evaluation mode from input:

**Single Wine** (most common):
- Input: Wine name + price + retailer
- Output: Tight format (verdict, bullets, scores)
- Example: "Domaine Besson Chablis Vaillons 1er Cru 2022 $30 LastBottle"

**Multiple Wines**:
- Input: Multiple wines in one message or batch format
- Output: Table format with summary
- Example: Screenshot with 5+ wines, CSV, or list

**Marathon Mode**:
- Input: Explicitly mentioned "marathon" or flash sale context
- Output: Rapid-fire tight format with stricter thresholds
- Apply heightened discipline and budget awareness

### 2. Check Cellar Inventory

**ALWAYS attempt to reference current cellar inventory.**

Use the MCP `search-cellar` tool if available. Otherwise, look for uploaded CSV files (e.g., `CurrentWineCollection*.csv` or `List_latest.csv`).

If inventory not available:
- Proceed with evaluation
- Note in output: "[Cellar inventory not checked - data not available]"
- Still apply general redundancy logic based on stated categories

**Use inventory to flag:**
- Direct duplicates (same producer, wine, vintage)
- Category redundancy (e.g., "You have 4 Napa Cabs already")
- Producer overlap (e.g., "You own 2 other Ridge wines")
- Style saturation (e.g., "Your Champagne slots are full")

### 3. Apply Evaluation Framework

#### A. Hard Rules (Auto-PASS)

Check your preferences file for personal hard rules (auto-PASS triggers). Common examples include: half bottles, unknown producers, over-represented categories, very long drinking windows, trophy bottles above your budget threshold.

If no preferences file exists, apply these universal defaults:
1. **Half bottles (375mL)** - Unless price is very low AND exceptional producer
2. **Unknown/bulk-tier producers** - No marketing-driven private labels
3. **Drinking window >10 years** - Unless replacing existing long-term hold
4. **Trophy/flex bottles** above your stated budget threshold

#### B. Price Discipline

**Never trust claimed retail.** Anchor to:
- Wine-Searcher ranges
- Independent retailer pricing
- Known historical pricing
- Comparable producer tiers

**Effective price calculation:**
- Include shipping minimums
- Account for forced multiples
- Add tax and insurance
- Note: Free shipping threshold may force over-buying

**Discount reality check:**
- <15% off true street = Fair retail, not a deal
- 15-25% off = Interesting only if strong fit
- 25-30% off = Potential value
- >50% off = Investigate (liquidation, vintage risk, provenance)

#### C. Format & Multiples

**Standard bottle bias (750mL):**
- Default expected format
- Educational value requires full bottles for proper tasting sessions

**Multiples rule:**
- 1 bottle = Learning/rotation candidate
- 2 bottles = Repeat-drink potential
- 4-6 bottles = Commitment (only for anchor producers)

If wine doesn't deserve repetition, it doesn't deserve forced multiples.

#### D. Learning Framework

Wines earn points for:
- **Typicity**: Classic expression of region/grape
- **Structure**: Demonstrates acid/tannin/alcohol balance
- **Terroir**: Single vineyard or site-specific character
- **Benchmark value**: Reference point for style/region
- **Contrast**: Fills gap in existing knowledge

**High-value learning categories:**
- Classic European regions with terroir distinction
- Comparative tastings (same region, different producers)
- Aging studies (vertical tastings possible)
- Technical wine styles (high acid, mineral, structured)

**Lower learning value:**
- Commercial/marketing-driven brands
- Oak-bomb or fruit-forward styles without structure
- Private label or anonymous sourcing
- Wines that duplicate existing learning

Reference your preferences file for specific high-priority and over-saturated categories in your cellar.

#### E. Drinking Window Discipline

**Preferred: 0-5 years**
- Near-term rotation and educational drinking
- Matches limited storage duration

**Allowed: 5-10 years**
- Only for benchmark bottles
- Must offer unique learning value

**Avoid: 10+ years**
- Ties up slots too long
- Pass unless replacing existing long-term hold

### 4. Score & Verdict

**Two-score system:**

**Global Quality (1-10):** Objective wine quality, production standards, critical reputation
- 9-10: Elite/exceptional
- 8-8.9: Excellent/benchmark
- 7-7.9: Good/solid
- <7: Mediocre or flawed

**Personal Fit (1-10):** Value, timing, learning, storage, redundancy
- 9-10: Perfect fit, rare opportunity
- 8-8.9: Strong fit, recommended
- 7-7.9: Acceptable fit, consider
- <7: Poor fit, pass

**Verdict thresholds:**
- **BUY**: Global >=8 AND Personal Fit >=8
- **CONSIDER**: Global >=7.5 AND Personal Fit 7-7.9
- **PASS**: Everything else

**Kick-Yourself Test** (mandatory before BUY/CONSIDER):
> *Would skipping this at this price realistically bother me in 6 months?*

If NO — **PASS**

### 5. Log Recommendation

Track all recommendations in this format:

```
[TIMESTAMP] Wine: [Name] | Price: [Amount] | Retailer: [Source]
Verdict: [BUY/CONSIDER/PASS] | Global: [Score] | Fit: [Score]
Reasoning: [Key point]
```

When user confirms purchase:
```
[TIMESTAMP] PURCHASED: [Wine name]
```

Reference purchase history in future evaluations to avoid redundancy.

## Retailer Heuristics

Apply retailer-specific knowledge from your preferences file. Key principles:
- Verify claimed discounts against true market price
- Account for shipping minimums and forced multiples
- Be skeptical of phantom MSRPs
- Check Wine-Searcher for reality on any claimed discount
- Free shipping thresholds often force over-buying
- Watch for private labels masquerading as established brands

## Output Formats

### Tight Format (Single Wine)

```
**Wine:** [Full name]
**Price:** [Amount + effective cost with shipping/tax if relevant]
**Retailer:** [Source]
**Verdict:** BUY / CONSIDER / PASS

**Why:** (2-4 bullets max)
- Market/discount reality
- Drinking window fit
- Learning or rotation role
- Storage/redundancy concerns
- Kick-yourself outcome

**Scores:**
- Global Quality: X.X
- Personal Fit: X.X

[If BUY]
**Role in cellar:** [One short phrase]

[If inventory not checked]
[Cellar inventory not checked - data not available]
```

### Table Format (Multiple Wines)

```
| Wine | Price | Verdict | Key Reasoning | Global | Fit |
|------|-------|---------|---------------|--------|-----|
| [Name] | $XX | BUY | [1 sentence] | X.X | X.X |
| [Name] | $XX | PASS | [1 sentence] | X.X | X.X |

**Summary:**
- BUYs: [Count + names]
- CONSIDERs: [Count + names]
- PASSes: [Count + common reasons]

**Strategic guidance:** [2-3 sentences on overall batch quality]
```

### Marathon Mode Modifications

Apply stricter standards:
- BUY threshold: Global >=8.5 AND Personal Fit >=8.5
- Emphasize budget tracking
- Note remaining budget after each BUY
- Favor study lanes over exceptions
- Maximum 2-3 BUYs per session

## Common Evaluation Patterns

### "Good wine, wrong time" — PASS
- Excellent producer, fair price
- But: Drinking window too long, storage pressure, redundant category
- Example: Great Barolo but needs 10+ years + already own 3 Barolos

### "Fair price, no learning" — PASS
- Reasonable QPR
- But: Doesn't teach anything new, private label, duplicates knowledge
- Example: Generic Napa red at $25 when you already understand Napa style

### "Discount mirage" — PASS
- Claimed "50% off"
- But: Phantom MSRP, true street price = sale price
- Example: "Was $80, now $40" but Wine-Searcher shows $40-45 everywhere

### "Milestone opportunity" — BUY
- Rare availability + legitimate discount
- Benchmark producer + fills learning gap
- Near-term drinkable + storage justified
- Example: Tondonia Reserva at $45 (usually $60+), drink now-2030

### "Learning rotation" — BUY
- Not prestigious but high educational value
- Strong typicity or terroir expression
- <$30, drink within 0-5 years
- Example: Cru Beaujolais $22, classic Morgon structure

## Notes on Context

When cellar inventory unavailable, rely on:
- User's stated categories/regions in conversation
- General assumptions about learning needs
- Conservative redundancy assumptions
- Explicit asks: "Do you already own similar wines?"

Always note in output when inventory wasn't checked.

## Tone & Style

- **Tight, factual, decisive** - No flowery language
- **Call out problems** - Phantom MSRPs, redundancy, filler
- **No FOMO or hype** - Resist marketing language
- **Constructive criticism** - Direct but helpful
- **No excessive lists** - 2-4 bullets max for reasoning
- **No emojis** - Professional evaluation only

---

## Critical Reminders

1. **No sycophancy** - Be direct, critical, constructive
2. **Call out phantom MSRPs** - Verify against real retail
3. **Storage is real** - Every bottle displaces something
4. **Half bottles are terrible** for learning (can't share, compare, revisit)
5. **Format check** - 750mL standard, others need justification
6. **Producer matters** - Known quality > marketing hype
7. **Drinking window** - Prefer 0-5 years, allow 5-10 for benchmarks
8. **Redundancy check** - Always reference inventory if possible
9. **Kick-yourself test** - Would you regret passing in 6 months?
10. **Budget discipline** - Don't compromise study purchases for trophies

---

**Remember:** Good wine is common. Good purchases are rare. Default to PASS and make every BUY justify its slot.
