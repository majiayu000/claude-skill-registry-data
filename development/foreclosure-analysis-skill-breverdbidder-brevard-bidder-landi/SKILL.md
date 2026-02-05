---
name: foreclosure-analysis-skill
description: Execute 12-stage Everest Ascent pipeline for foreclosure auction analysis from discovery to disposition
---

# Foreclosure Analysis Skill

Executes the complete 12-stage Everest Ascent™ methodology for foreclosure auction intelligence.

## When to Use This Skill

- Analyzing upcoming foreclosure auctions
- Processing new auction listings
- Generating investment recommendations
- Creating property reports for bidding decisions

## The Everest Ascent™ Pipeline

### Stage 1: Discovery
- Monitor RealForeclose.com for new listings
- Extract: case number, plaintiff, property address, auction date
- Filter: Brevard County only, exclude tax deeds
- Output: candidate_properties list

### Stage 2: Scraping
- **BCPAO Scraper:** Property details, valuations, photos
- **RealForeclose Scraper:** Auction specifics, judgment amount
- **AcclaimWeb Scraper:** Mortgages, liens, legal descriptions
- **RealTDM Scraper:** Tax certificates, delinquencies
- **Census API:** Demographics, neighborhood data

### Stage 3: Title Search
- Parse legal description
- Identify all recorded instruments
- Build chain of title
- Flag gaps or issues

### Stage 4: Lien Priority Analysis
**CRITICAL STAGE - Use lien-discovery-skill**
- Identify lien positions (1st, 2nd, 3rd+)
- Detect HOA foreclosures (senior mortgage survives)
- Calculate lien satisfaction amounts
- Determine what buyer inherits

### Stage 5: Tax Certificates
- Check RealTDM for outstanding certificates
- Calculate tax debt
- Verify redemption status
- Add to cost basis

### Stage 6: Demographics
- Census API: median income, vacancy rate
- Neighborhood score: rental demand, appreciation potential
- Target zips: 32937, 32940, 32953, 32903
- Flag: optimal for Third Sword MTR strategy

### Stage 7: ML Prediction
- XGBoost model: third-party purchase probability (64.4% accuracy)
- Features: plaintiff, property type, judgment amount, location
- Output: probability score 0-1
- Brand as "BrevardBidderAI ML" in reports

### Stage 8: Max Bid Calculation
**Use max-bid-calculator-skill**
- Formula: (ARV×70%) - Repairs - $10K - MIN($25K, 15%×ARV)
- ARV: After-repair value from BCPAO + comps
- Repairs: Conservative estimate based on age/condition
- Holding costs: $10K standard
- Profit buffer: $25K or 15% ARV (whichever less)

### Stage 9: Decision Logic
- Calculate bid/judgment ratio
- **BID:** Ratio ≥ 75% (strong value)
- **REVIEW:** Ratio 60-74% (marginal, needs human review)
- **SKIP:** Ratio < 60% (insufficient value)
- **DO_NOT_BID:** HOA foreclosure with senior mortgage

### Stage 10: Report Generation
- One-page DOCX format
- BrevardBidderAI branding (NOT Property360)
- Include: property details, BCPAO photo, max bid, decision, rationale
- ML prediction prominently displayed
- Lien analysis summary

### Stage 11: Disposition Tracking
- Log to Supabase auction_results table
- Fields: property_id, decision, max_bid, actual_bid, outcome
- Track: won/lost/skipped
- Calculate: actual ROI vs predicted

### Stage 12: Archive
- Store all data in Supabase historical_auctions
- Preserve: scraper outputs, ML predictions, decisions
- Enable: backtesting, model improvements, pattern analysis

## Data Sources & APIs

**RealForeclose:** brevard.realforeclose.com (auction listings)
**BCPAO:** gis.brevardfl.gov/gissrv/rest/services/Base_Map/Parcel_New_WKID2881/MapServer/5
**AcclaimWeb:** Search by case number, parcel ID
**RealTDM:** Tax certificate search by parcel
**Census:** api.census.gov/data (demographics)

## Decision Rules

**Auto-BID if:**
- Bid/judgment ≥ 75%
- No HOA foreclosure issues
- Clean title chain
- Target zip code (optional boost)

**Flag REVIEW if:**
- Bid/judgment 60-74%
- Minor title issues
- Unusual property characteristics
- High repair uncertainty

**Auto-SKIP if:**
- Bid/judgment < 60%
- Insufficient margin
- High risk factors

**DO_NOT_BID if:**
- HOA foreclosure + senior mortgage survives
- Title defects
- Legal complications

## Output Format

```json
{
  "property_id": "2024-CA-001234",
  "address": "123 Main St, Melbourne FL 32940",
  "decision": "BID",
  "max_bid": 285000,
  "judgment": 320000,
  "bid_ratio": 0.89,
  "ml_probability": 0.72,
  "lien_analysis": "Clean 1st position",
  "reasoning": "Strong equity position, target zip, clean title"
}
```

## Example Usage

```
"Analyze the December 3rd foreclosure auction using foreclosure-analysis-skill"

"Process new RealForeclose listings with the Everest Ascent pipeline"
```

## Integration Points

- Triggers lien-discovery-skill at Stage 4
- Triggers max-bid-calculator-skill at Stage 8
- Uses bcpao-data-extraction-skill throughout
- Logs to Supabase at Stages 11-12

## Best Practices

1. **NO GUESSING:** Always use actual recorded documents
2. **Verify Everything:** Don't trust automated data blindly
3. **Conservative Repairs:** Better to overestimate than underestimate
4. **Document Reasoning:** Every decision needs clear rationale
5. **Track Performance:** Log actual vs predicted outcomes
