---
name: foreclosure-analysis
description: Expert skill for analyzing Florida foreclosure auction properties using The Everest Ascent™ 12-stage methodology. Use when analyzing properties, calculating max bids, researching liens, or making bid/skip decisions for Brevard County foreclosure auctions.
---

# Foreclosure Analysis Skill

Expert methodology for analyzing foreclosure auction properties in Brevard County, Florida using The Everest Ascent™ systematic approach.

## When to Use This Skill

- Analyzing foreclosure auction properties
- Calculating maximum bid amounts
- Researching title and lien priority
- Making BID/REVIEW/SKIP recommendations
- Generating property analysis reports
- Evaluating exit strategies (wholesale, retail, rental)

## The Everest Ascent™ 12-Stage Pipeline

### Stage 1: Discovery
- Scrape auction listings from RealForeclose (brevard.realforeclose.com)
- Extract: case number, property address, plaintiff, defendant, judgment amount, auction date
- Filter for in-person Titusville courthouse auctions vs online tax deed sales
- Initial data validation and deduplication

### Stage 2: Scraping & Enrichment
**Data Sources (Priority Order):**
1. BCPAO API (gis.brevardfl.gov/gissrv/rest/services/Base_Map/Parcel_New_WKID2881/MapServer/5)
   - Property details: lot size, living area, year built, zoning
   - Photos: masterPhotoUrl field (format: https://www.bcpao.us/photos/{prefix}/{account}011.jpg)
   - Tax values: just value, market value, assessed value
   
2. RealForeclose
   - Case details, auction status, sale date
   - Historical auction results
   
3. Zillow/Redfin (for residential properties)
   - Beds, baths, square footage (BCPAO GIS lacks these)
   - Recent sales comps
   - Market trends

**Critical:** BCPAO provides property data but NOT beds/baths for residential. Must use Zillow/Redfin for complete residential analysis.

### Stage 3: Title Search
- Search BECA (Brevard County Clerk) for recorded documents
- Identify all mortgages, liens, judgments in chronological order
- **NEVER GUESS** - only use actual recorded documents

### Stage 4: Lien Priority Analysis
**Florida Foreclosure Law - Lien Priority:**

1. **First Position Mortgage Foreclosure (most common):**
   - Senior mortgage forecloses
   - Wipes out junior liens (2nd mortgages, HELOCs, mechanic's liens)
   - Buyer gets clean title except for:
     - Property taxes (always survive)
     - HOA assessments recorded BEFORE the foreclosing mortgage
     - Code enforcement liens (sometimes)

2. **HOA Foreclosure (CRITICAL SCENARIO):**
   - HOA forecloses for unpaid assessments
   - Senior mortgage SURVIVES
   - Buyer inherits the senior mortgage debt
   - **AUTOMATIC DO_NOT_BID** unless bid covers: HOA judgment + senior mortgage balance + your profit
   - Detection: Plaintiff is HOA/condo association, mortgage still on title

3. **Tax Certificate Foreclosure:**
   - County sells tax lien certificates
   - After 2 years, certificate holder can foreclose
   - Wipes out ALL liens including mortgages
   - Very clean title for buyer

**AcclaimWeb Search Pattern:**
```
1. Search property address
2. Download all mortgages (OR book/page references)
3. Download all liens, judgments, lis pendens
4. Check recording dates vs foreclosing lien date
5. Flag if HOA plaintiff + senior mortgage exists
```

**Detection Logic:**
- If plaintiff contains: "HOA", "Homeowners Association", "Condo Association", "POA"
- AND mortgage recorded BEFORE HOA lien
- → Senior mortgage survives
- → DO_NOT_BID

### Stage 5: Tax Certificate Check
- Search RealTDM for outstanding tax certificates
- Check redemption status
- Tax certificates < 2 years: owner can still redeem
- Tax certificates ≥ 2 years: holder can foreclose

### Stage 6: Demographics & Market Analysis
**Census API Data:**
- Median household income (target: $78-82K)
- Population trends
- Vacancy rates (target: 5-6%)
- Age demographics

**Optimal Zip Codes (ML-validated):**
- 32937 Satellite Beach (income: $82K, vacancy: 5.2%)
- 32940 Melbourne/Viera (income: $80K, vacancy: 5.8%)
- 32953 Merritt Island (income: $78K, vacancy: 6.1%)
- 32903 Indialantic (income: $81K, vacancy: 5.4%)

**Red Flags:**
- High crime zip codes: 32901, 32904, 32935
- Declining population trends
- Vacancy rates > 8%

### Stage 7: ML Probability Score
**XGBoost Model (64.4% accuracy):**
- Predicts: Third-party purchase probability, estimated sale price
- Features: judgment amount, property value, zip code, plaintiff type, time on market
- Output: Probability score 0-100%

**Plaintiff Risk Profiles (28 tracked):**
- Wells Fargo: 72% third-party purchase (aggressive bidders)
- Bank of America: 65% third-party purchase
- US Bank: 58% third-party purchase
- Local credit unions: 45% third-party purchase (bank often bids)

### Stage 8: Maximum Bid Calculation
**Formula:**
```
Max Bid = (ARV × 70%) - Repairs - $10,000 - MIN($25,000, 15% × ARV)
```

**Components:**
- **ARV (After Repair Value):** Zillow/Redfin comps, BCPAO market value
- **Repairs:** Estimate from photos, property age, condition
  - $0-5K: Good condition, cosmetic only
  - $10-25K: Moderate rehab (kitchen, baths, flooring)
  - $30-50K: Major rehab (roof, HVAC, structural)
  - $60K+: Gut rehab or structural issues
- **$10K buffer:** Holding costs, closing, surprises
- **MIN($25K, 15% ARV):** Profit margin

**Example:**
```
ARV: $350,000
Repairs: $20,000
Max Bid = ($350,000 × 0.70) - $20,000 - $10,000 - MIN($25,000, $52,500)
Max Bid = $245,000 - $20,000 - $10,000 - $25,000
Max Bid = $190,000
```

### Stage 9: Decision Logic
**Bid/Judgment Ratio:**
```
Ratio = Max Bid ÷ Judgment Amount
```

**Decision Rules:**
- **Ratio ≥ 0.75 (75%):** BID - Strong deal, bid up to max
- **Ratio 0.60-0.74 (60-74%):** REVIEW - Marginal deal, need more analysis
- **Ratio < 0.60 (<60%):** SKIP - Insufficient margin

**Additional BID Criteria:**
- Clean title (no HOA foreclosure with senior mortgage)
- Repairs < 30% of ARV
- Property in target zip code
- Exit strategy viable (flip, rental, wholesale)

**Additional SKIP Criteria:**
- HOA foreclosure + senior mortgage survives
- Code violations > $10K
- Structural issues (foundation, severe water damage)
- Environmental issues (mold, asbestos, underground tanks)
- Title clouds (unresolved liens, boundary disputes)

### Stage 10: Report Generation
**One-Page DOCX Format:**
- **Header:** BidDeed.AI branding (navy #1E3A5F)
- **Property Photo:** BCPAO masterPhotoUrl
- **Key Metrics:**
  - Address, case number, auction date
  - Judgment amount, max bid, bid/judgment ratio
  - ARV, repair estimate, profit margin
  - ML probability score
- **Decision Box:**
  - BID (green #E8F5E9)
  - REVIEW (orange #FFF3E0)
  - SKIP (red #FFEBEE)
- **Exit Strategy:** Wholesale, flip, rental with projected returns
- **Lien Summary:** Clean or issues flagged
- **Risk Factors:** HOA, code violations, structural issues

**NEVER include:**
- Property360 references
- Mariam Shapira references
- Everest Capital of Brevard LLC (use "Everest Capital USA" or "BidDeed.AI")

### Stage 11: Disposition Tracking
- Record actual auction outcome
- Track: winning bid, buyer, bank credit bid
- Compare predicted vs actual results
- Update ML model with ground truth data

### Stage 12: Archive & Learning
- Save all analysis to Supabase `auction_results` table
- Document lessons learned
- Update decision thresholds based on actual results
- Refine repair estimates from actual rehab costs

## Data Sources & APIs

**BCPAO API:**
```
Base: https://gis.brevardfl.gov/gissrv/rest/services/Base_Map/Parcel_New_WKID2881/MapServer/5
Query: /query?where=PARCEL_ID='...'&outFields=*&f=json
Photo: https://www.bcpao.us/photos/{prefix}/{account}011.jpg
```

**Census API:**
```
Base: https://api.census.gov/data/2021/acs/acs5
Key: Public (no auth needed for basic queries)
```

**AcclaimWeb:**
- Manual search (no API)
- Search by: address, name, book/page
- Download PDFs of mortgages/liens

**RealForeclose:**
- Scrape auction listings
- Use async httpx, anti-detection headers
- Respect rate limits

**Supabase:**
```
Project: mocerqjnksmhcjzxrewo.supabase.co
Tables: auction_results, historical_auctions, insights
```

## Critical Rules

1. **NEVER guess about liens** - only use recorded documents from BECA
2. **ALWAYS check for HOA foreclosures** - senior mortgage survival is deal killer
3. **Use ACTUAL property data** - no fake comps or estimated values
4. **BCPAO lacks beds/baths** - must use Zillow/Redfin for residential
5. **One-page reports only** - BidDeed.AI branding, DOCX format
6. **Fair Housing compliance** - NO race/ethnicity/familial status in analysis
7. **Conservative estimates** - better to skip than overbid

## Exit Strategies

**Wholesale (Fastest):**
- Target: 65-70% ARV
- Timeline: 7-30 days
- Profit: $10-25K
- Best for: Clean properties, quick capital return

**Retail Flip (Highest Profit):**
- Target: 70-75% ARV + repairs
- Timeline: 3-6 months
- Profit: $40-80K
- Best for: Nice neighborhoods, cosmetic repairs

**Mid-Term Rental (Third Sword):**
- Target zip codes: 32937, 32940, 32953, 32903
- Timeline: Hold 1-3 years
- Cash flow: $800-1,500/month
- Best for: Furnished rentals, traveling professionals

## Common Pitfalls to Avoid

1. **Bidding on HOA foreclosures without checking senior mortgages**
2. **Trusting BCPAO beds/baths for residential** (often inaccurate/missing)
3. **Underestimating repairs** (always add 20% buffer)
4. **Ignoring code violations** (can delay closing/sale)
5. **Overbidding due to auction fever** (stick to max bid)
6. **Skipping title search** (hidden liens can destroy deal)

## Pro Tips

- Attend auctions to observe bidding patterns
- Build relationships with title companies
- Pre-arrange financing for quick closes
- Visit properties before auction (exterior only)
- Track competitor bidding patterns
- Keep $50-100K liquid for quick acquisitions

## Example Analysis Workflow

```
1. Property discovered in RealForeclose scrape
2. BCPAO API pull → property data + photo
3. Zillow scrape → beds/baths/comps (if residential)
4. AcclaimWeb search → title/lien documents
5. Lien priority analysis → HOA check
6. Census API → demographics
7. ML model → probability score
8. Max bid calculation → ARV × 70% formula
9. Decision logic → BID/REVIEW/SKIP
10. Generate DOCX report → BidDeed.AI branded
11. Save to Supabase → auction_results table
```

This skill encodes 10+ years of Brevard County foreclosure investing experience into a systematic, repeatable process that maximizes ROI while minimizing risk.
