---
name: google-ads-keywordplanner
description: "Use when planning Google Ads keywords: keyword discovery, evaluating intent/volume/bid, match-type selection."
metadata:
  source: "prompts/skills/google_ads/keywordPlanner"
---

# Google Ads Keyword Planner Protocol

## When to Use Keyword Planner

**Rule:** If a decision depends on search volume, CPC (top-of-page bid), or competition → Keyword Planner MUST be used.
**If Keyword Planner is not used → Stop recommendations.**

## Tools

- **`google_ads_keyword_discover`**: Discover new keyword ideas from seed keywords or URLs. Returns suggestions with volume, competition, bid estimates.
- **`google_ads_keyword_metrics`**: Get historical metrics + forecasts for specific keywords. Returns volume, competition, bid ranges, trend data.

## When Keyword Planner is REQUIRED

### 1. Keyword Research / Discovery
**Triggers:**
- "Do keyword research"
- "Suggest keywords"
- "Find buyer keywords"
- "What keywords should we target?"

**Action:** Invoke `google_ads_keyword_discover` → Discover New Keywords

### 2. Keyword Validation / Filtering
**Triggers:**
- "Are these keywords good?"
- "Which keywords should I keep?"
- "Which keywords should I remove?"

**Action:** Invoke `google_ads_keyword_metrics` → Search volume + forecasts

### 3. Keyword Comparison / Prioritization
**Triggers:**
- "Which keyword is better?"
- "Prioritize these keywords"
- "High intent vs high volume keywords"

**Action:** Invoke `google_ads_keyword_metrics` for all compared keywords

### 4. New Search Campaign Creation
**Triggers:**
- "Create a new search campaign"
- "Launch Google Search ads"

**Action:** Run `google_ads_keyword_discover` (research) → `google_ads_keyword_metrics` (validate) BEFORE proposing structure

### 5. Market / Geo Expansion
**Triggers:**
- "Expand to a new country"
- "Test a new region"
- "International Google Ads"

**Action:** Invoke Keyword Planner with new `location_ids` + `language_id`

### 6. Budget-Based Decisions
**Triggers:**
- "Can we scale?"
- "What keywords fit this budget?"
- "What CPCs should we expect?"

**Action:** Invoke `google_ads_keyword_metrics` → Top-of-page bids (use `forecast` parameter)

## When Keyword Planner is NOT Required

Allowed without Keyword Planner:

1. **Creative**
   - RSA headlines
   - Descriptions
   - Ad strength improvements
2. **Structure**
   - Match type explanations
   - Campaign naming
   - Account audits (unless keyword changes are suggested)
3. **Post-Performance Analysis**
   - CPA / ROAS analysis
   - Search term mining (use Search Terms Report)

## Guardrail

If Keyword Planner data is required but unavailable:
- Do NOT generate keywords
- Do NOT estimate volume or CPC

---

## How to Use Keyword Planner

### STEP 1: Generate Candidate Keywords

Generate keywords only using buyer-intent patterns.

**Approved Patterns:**
- [service] + agency
- [service] + management
- [service] + pricing
- [service] + cost
- [service] + consultant
- [software] + for + [industry]
- [competitor] + alternative

**Disallowed Patterns:**
- how to
- what is
- guide
- tips
- tutorial
- free
- examples

### STEP 2: Evaluate Each Keyword

| Criterion | Rule |
|-----------|------|
| **Intent** | Buyer intent must be explicit in the keyword text. Unclear → REJECT. |
| **Search Volume** | Volume < 50 → REJECT. Volume ≥ 50 → PASS. |
| **Top-of-Page Bid** | High → STRONG APPROVE. Medium → APPROVE. Low → APPROVE only if intent is very strong. Zero / Missing → REJECT. |
| **Competition** | Use only as a tie-breaker. Never reject solely due to high competition. |

### STEP 3: Final Keyword Decision Rule

```
IF
  - Buyer intent = YES
  - Volume ≥ 50
  - Top-of-page bid ≠ Low / Zero
THEN
  - APPROVE
ELSE
  - REJECT
```

### STEP 4: Match Type

For approved keywords only:

| Match Type | When to Use |
|------------|-------------|
| Exact | Very strong intent, specific wording |
| Phrase | Core scalable keywords |
| Broad | Do NOT suggest by default |

### STEP 5: Output Format

```
Keyword:
Match Type:
Volume:
Top of Page Bid:
Competition:
Decision:
Reason:
```

**Example:**
```
Keyword: google ads agency for ecommerce
Match Type: Phrase
Volume: 90
Top of Page Bid: High
Competition: Medium
Decision: APPROVE
Reason: Clear buyer intent + active advertiser bidding
```

---

## Final Rules

1. Intent > Volume (always)
2. Top-of-page bid = strongest commercial signal
3. Informational keywords = auto-reject
4. Fewer correct keywords > many random ones

## Tool Call Examples

**Discovery:**
```
Tool: google_ads_keyword_discover
Parameters:
  customer_id: "1234567890"
  keywords: ["google ads agency", "ppc management"]
  location_ids: ["2840"]   # US
  language_id: "1000"      # English
  page_size: 100
```

**Validation with forecast:**
```
Tool: google_ads_keyword_metrics
Parameters:
  customer_id: "1234567890"
  keywords: ["google ads agency for ecommerce"]
  location_ids: ["2840"]
  language_id: "1000"
  forecast:
    daily_budget_micros: 500000000   # $500/day
    max_cpc_bid_micros: 5000000      # $5 max CPC
    forecast_period_days: 30
```
