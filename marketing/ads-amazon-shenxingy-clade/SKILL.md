---
name: ads-amazon
description: "Amazon Ads deep analysis covering Sponsored Products, Sponsored Brands (incl. Sponsored Brands Video), Sponsored Display (audiences + contextual), and basic Amazon DSP. Evaluates campaign structure, ACOS/TACOS targets, search-term harvesting, negative keyword discipline, Brand Analytics signals, day-parting, bid management, auto vs manual campaign mix, ASIN targeting, and DSP retargeting. Use when user says Amazon Ads, Amazon advertising, Amazon PPC, Amazon search ads, Sponsored Products, Sponsored Brands, Sponsored Display, Amazon DSP, ACOS, TACOS, retail media audit, Amazon Marketing Services, AMS, or Amazon seller advertising."
user_invocable: false
tested_date: 2026-05-17
tested_with: claude-code v2.x
---

# Amazon Ads Deep Analysis

Amazon owns ~80% of US retail media (~$56B in 2025). This sub-skill audits
the three Sponsored ad types plus basic DSP visibility for sellers and
vendors. Detailed Amazon DSP audit (programmatic / Twitch / Fire TV / Freevee
/ Prime Video) is queued for Wave 3 in `ads-retail-media`.

> **Note:** This is a leaf sub-skill. The thresholds and rules below live
> inline. In Wave 3, once `ads-walmart` ships and the `ads-retail-media`
> orchestrator extracts the shared retail-media logic, a dedicated
> `retail-media-specs.md` reference file will replace these inline rules
> (planned, not yet created — do not link to it from other files).

## Process

1. Collect Amazon Advertising export: Search Term Report (last 60 days),
   Campaign Performance Report, Targeting Report, Placement Report, Bulk
   Operations file
2. Collect Brand Analytics if available (Brand-Registered sellers / vendors):
   Search Terms, Repeat Purchase Behavior, Item Comparison
3. Verify Seller / Vendor Central context (vendor strategy differs from
   seller strategy on portfolio, coupons, and Sponsored Brands video)
4. Read `ads/references/benchmarks.md` for Amazon-specific benchmarks
5. Read `ads/references/scoring-system.md` for weighted scoring
6. Evaluate checks per category
7. Calculate Amazon Ads Health Score (0-100)
8. Generate findings report with action plan

## What to Analyze

### Campaign Structure & Portfolios (15% weight)

- **Portfolio organization** — campaigns grouped by funnel stage (Awareness /
  Consideration / Conversion) or by product line, not ad-hoc
- **Campaign naming convention** consistent (e.g.,
  `SP_Brand_Exact_USD_Conv` / `SB_NonBrand_HSA_Video_USD_Cons`)
- **Auto vs Manual mix**: Sponsored Products has ≥1 Auto campaign per ASIN
  cluster for search-term harvesting (auto-mining workflow)
- **ASIN-level coverage**: every priority ASIN appears in ≥1 SP campaign
  (Exact, Phrase, or Broad) AND ≥1 Auto campaign
- **Targeting type mix in SP**: Manual Keyword + Manual Product (ASIN
  targeting) + Auto (for harvesting). Pure Auto is a learning-only state
- **Sponsored Brands**: at least one HSA (Headline Search Ad) campaign per
  brand storefront; SB Video tested for high-AOV products
- **Sponsored Display**: separate Audience (retargeting + lookalike) and
  Contextual (product / category targeting) campaigns — don't mix in one

### Search-Term Harvesting & Negatives (25% weight)

- **Auto → Manual harvest cadence** weekly or bi-weekly: pull converting
  search terms from Auto, promote winners to Manual Exact in their target
  campaign, add as negatives to the Auto so spend redirects
- **Negative keyword coverage**: every Auto campaign has Manual campaign
  ASINs as negatives (prevents Auto cannibalizing Manual placements)
- **Negative product targeting**: irrelevant ASINs added at campaign level
  (prevents Sponsored Display contextual targeting from showing your ad
  next to incompatible products)
- **Search Term Report harvested last 7 days** — any high-spend, zero-
  conversion terms above $10 / 30 days should be negatives
- **Brand defense**: branded search terms are isolated in a separate
  campaign with exact-match brand keywords and competitor-name negatives
- **Top-of-search visibility** — branded search auction CPC vs default; flag
  if competitor bid is above your brand-defense bid

### ACOS / TACOS Discipline (20% weight)

- **ACOS targets set per portfolio** based on contribution margin (target
  ACOS = (1 - contribution_margin) × buffer). Sloppy "30% across the board"
  ACOS targets cap performance
- **TACOS (Total ACOS) trending down** quarter-over-quarter — TACOS measures
  total ad spend / total revenue including organic; downward trend means
  paid is lifting organic, not replacing it
- **ROAS reported alongside ACOS** for the team that thinks in ROAS
- **Coupon + Lightning Deal stacking** — when on, ACOS targets relaxed to
  capture lift; auto-flag campaigns that need temporary ACOS uplift
- **Day-parting**: bid adjustments by hour for ASINs where add-to-cart
  hours differ from purchase hours (frequent for high-AOV electronics)

### Bid & Budget Management (15% weight)

- **Dynamic bidding strategy**: `Up and Down` for Manual Exact converting
  campaigns; `Down Only` for Auto campaigns or Sponsored Display contextual
  (avoid bid escalation in learning campaigns)
- **Placement bid multipliers**: Top-of-search placement adjusted based on
  ROAS by placement (Placement Report); often +50-100% for top-of-search,
  -30% for product page placements
- **Budget caps appropriate** — no campaigns capped at <2x current daily
  spend (caps strangle algorithm learning)
- **Bulk bid adjustments** — bid optimization runs weekly via Bulk
  Operations not ad-hoc in the UI

### Sponsored Brands (10% weight)

- **HSA (Headline Search Ad)**: brand logo + 3-product showcase + landing
  page (Store, custom URL, or product list)
- **SB Video**: 6-45s; 15-30s sweet spot. Hook within 2s. Captions on.
  Required for high-AOV products
- **Brand Store linked** as landing destination where available (higher
  CVR than product detail page)
- **Negative keywords on SB** include competitor brand names if you don't
  want top-of-funnel competitor traffic; remove if you do

### Sponsored Display (10% weight)

- **Audience targeting**: Views Remarketing, Purchase Remarketing, Cross-
  Sell, and Lookalike audiences each scaled with appropriate bids
- **Contextual targeting**: relevant categories AND specific ASIN targeting
  (your own complementary products + competitor ASINs you can win)
- **Display creative quality**: at minimum, the default product creative;
  custom creative tested for top SKUs
- **Off-Amazon Sponsored Display** (Twitch, IMDb, third-party sites) audited
  separately — different CPC dynamics, different attribution windows

### Brand Analytics & Reporting (5% weight)

- **Brand Analytics** accessed (Brand-Registered only): Top Search Terms,
  Item Comparison, Repeat Purchase Behavior
- **Top Search Terms report** used to identify share-of-voice gaps vs
  competitors on category keywords
- **Repeat Purchase Behavior** informs subscription / replenishment ad
  strategy
- **Amazon Attribution** (off-Amazon traffic) tracked if running external
  ads driving to Amazon listings

## Key Thresholds

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| ACOS (vs target) | Within ±10% of target | 10-25% over | >25% over |
| TACOS trend (90d) | Decreasing | Flat | Increasing |
| Auto / Manual mix | Both active per ASIN | Only Manual or only Auto | Single campaign / ASIN |
| Negative keywords on Auto | Manual ASIN keywords added | Some missing | None |
| Search term harvest cadence | Weekly | Monthly | Ad-hoc |
| Branded campaign ACOS | <5% | 5-15% | >15% |
| Dynamic bidding strategy | Up-and-Down on converters, Down-Only on learners | Mixed inconsistently | All campaigns same strategy |
| Sponsored Brands video tested | Active on top 10 ASINs | Active on 1-3 ASINs | Not tested |
| Brand Analytics accessed | Weekly | Monthly | Never |

## Output

### Amazon Ads Health Score

```
Amazon Ads Health Score: XX/100 (Grade: X)

Campaign Structure:     XX/100  ████████░░  (15%)
Search-Term Harvesting: XX/100  ██████████  (25%)
ACOS / TACOS Discipline:XX/100  █████████░  (20%)
Bid & Budget Mgmt:      XX/100  ████████░░  (15%)
Sponsored Brands:       XX/100  ███████░░░  (10%)
Sponsored Display:      XX/100  ███████░░░  (10%)
Brand Analytics:        XX/100  █████░░░░░  (5%)
```

### Deliverables

- `AMAZON-ADS-REPORT.md`: Full per-category findings
- Search-term harvest plan: keywords to promote to Manual + keywords to
  add as negatives, ranked by spend recovery $
- ACOS-by-ASIN matrix highlighting unprofitable SKUs
- Sponsored Brands video opportunity list (top 10 ASINs without SB Video)
- Pre-launch checklist when entering a new product category
- Amazon DSP entry recommendation (yes / no based on total monthly spend
  and audience size)
