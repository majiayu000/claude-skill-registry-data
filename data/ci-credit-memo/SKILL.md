---
name: ci-credit-memo
description: "Generate comprehensive Commercial & Industrial (C&I) loan credit memos for banking demos. Interviews bankers, gathers data from Morningstar/S&P/Aiera/LSEG, handles file uploads, tracks citations, and produces standardized credit approval documents. Use when a banker needs to create a credit memo for a C&I loan application."
---

# C&I Credit Memo Generator Skill

## Overview

This skill helps commercial bankers create comprehensive credit memos for Commercial & Industrial (C&I) loan applications. It automates the data gathering, financial analysis, and memo writing process while maintaining proper citations and allowing for demo scenarios.

## When to Use This Skill

- When a banker says "I need to create a credit memo"
- When preparing loan approval documents for C&I transactions
- When analyzing a company for a commercial loan
- When the user mentions "credit memo", "loan approval", "underwriting", or "C&I loan"

## Workflow Overview

The skill follows a structured 5-phase approach:

1. **Interview Phase** - Gather initial information from banker
2. **Data Collection Phase** - Source information from multiple channels with citation tracking
3. **Analysis Phase** - Calculate ratios, assess risks, benchmark against industry
4. **RAROC Pricing Phase** - Calculate risk-adjusted returns and pricing recommendation
5. **Memo Generation Phase** - Create formatted, cited credit memo with RAROC analysis

---

## PHASE 1: INTERVIEW & INFORMATION GATHERING

### Memo Detail Level Selection

Before beginning the interview, determine the appropriate level of detail:

**Ask the banker:**
"What stage is this credit request at? This helps me calibrate how much detail we need now vs. later:

1. **Screening Memo** - Quick 3-5 page assessment for initial deal viability
   - I'll use reasonable defaults liberally and flag all assumptions
   - Good for: Initial pipeline discussion, go/no-go decision

2. **Draft Credit Memo** (most common) - Full 15-25 page memo with some placeholders
   - I'll ask key questions, suggest defaults for minor items
   - Marks '[TBD]' where critical data is missing
   - Good for: Banker/analyst collaboration, preliminary credit committee review

3. **Final Credit Memo** - Complete, submission-ready document
   - I'll require answers to all material questions before proceeding
   - No assumptions on key deal terms
   - Good for: Final credit committee approval

Which level fits your needs?"

**Behavior by Level:**

| Aspect | Screening | Draft | Final |
|--------|-----------|-------|-------|
| Missing financials | Estimate from available data | Flag gaps, suggest sources | Require before proceeding |
| Deal structure | Suggest based on deal type | Present options, confirm | Require banker input |
| Pricing | Use pricing matrix defaults | Present with rationale, allow override | Require confirmed pricing |
| Pro formas | High-level sensitivity table | Detailed with flagged assumptions | Verified projections only |
| Covenants | Standard package for risk rating | Propose and discuss | Finalized terms |

### Initial Questions to Ask

Start by gathering these critical details from the banker:

**Basic Information:**
1. **Company Name**: What is the name of the borrower/company?
2. **Industry**: What industry/sector is the company in?
3. **Public or Private**: Is this a publicly traded or private company?
4. **Loan Type**: What type of loan? (Line of credit, term loan, equipment financing, etc.)
5. **Loan Amount**: How much is the loan request?
6. **Loan Purpose**: What will the funds be used for? (Working capital, equipment purchase, expansion, acquisition, etc.)
7. **Loan Terms**: What are the proposed terms?
   - Interest rate
   - Maturity/term length
   - Amortization schedule
   - Collateral offered

**Borrower Details:**
8. **Management Team**: Who are the key executives? Any relevant background?
9. **Years in Business**: How long has the company been operating?
10. **Ownership Structure**: Who owns the company? Any guarantors?

**Available Data:**
11. **Financial Statements**: Do you have financial statements available? (If yes, ask them to upload)
12. **Tax Returns**: Years available?
13. **Other Documents**: Any other relevant documents? (Business plan, projections, customer contracts, etc.)

### Interview Format

Use a conversational approach:
- Ask 2-3 questions at a time, not all at once
- Adapt follow-up questions based on responses
- If they don't know something, note it and move on
- Be prepared for "demo mode" responses like "just make it up" or "use placeholder data"

**Example Opening:**
```
I'll help you create a credit memo for this C&I loan. Let me gather some information about the deal.

First, can you tell me:
1. What is the company name?
2. What industry are they in?
3. Is this a publicly traded or private company?
```

### Smart Defaults with Confirmation Pattern

When key deal parameters are not provided, DO NOT silently assume values. Instead, present suggested defaults with rationale and ask for confirmation.

**Template for Presenting Defaults:**

"Based on [what I know], here's what I'd suggest for [category]. Please confirm, modify, or say 'proceed with defaults':

| Parameter | Suggested Value | Rationale |
|-----------|-----------------|-----------|
| [Param 1] | [Value] | [Why this makes sense] |
| [Param 2] | [Value] | [Why this makes sense] |

**To proceed:**
- Type 'confirm' to use these values
- Or tell me what to change (e.g., 'change rate to SOFR + 350')
- Or 'skip' to leave as [TBD] placeholders"

**Example - Loan Structure Defaults:**

"Based on the $100M request split between equipment ($70M) and working capital ($30M), here's what I'd suggest:

**Equipment Facility:**
| Parameter | Suggested Value | Rationale |
|-----------|-----------------|-----------|
| Rate | SOFR + 325 bps | Risk Rating 6, secured equipment, per pricing matrix |
| Term | 7 years | Matches typical equipment useful life |
| Amortization | 7-year straight-line | Standard for equipment financing |
| Advance Rate | 80% of FMV | Standard for industrial equipment |

**Revolver:**
| Parameter | Suggested Value | Rationale |
|-----------|-----------------|-----------|
| Rate | SOFR + 300 bps | 25 bps tighter (shorter tenor, liquid collateral) |
| Term | 3 years | Standard revolver tenor |
| A/R Advance | 85% eligible | Standard for commercial A/R |
| Inventory Advance | 50% eligible | Conservative for manufactured goods |

Confirm, modify, or skip?"

**When to Use Smart Defaults:**
- Loan pricing and structure
- Covenant levels
- Collateral advance rates
- RAROC inputs (PD, LGD based on risk rating)
- Pro forma growth assumptions

**When to REQUIRE Input (No Defaults):**
- Loan amount (must be provided by banker)
- Borrower name and industry
- Loan purpose
- New contract values (if contract-based financing)
- Known collateral issues or exceptions

---

## PHASE 1B: DATA COMPLETENESS CHECKPOINT

Before proceeding to data collection, summarize what is known vs. unknown and get direction on how to handle gaps.

**Template:**

"Before I build the credit memo, here's what I have vs. what I need:

### ✓ KNOWN (from documents/interview):
- [List items with source]
- [List items with source]

### ⚠ UNKNOWN - Need Your Input:
For each unknown, I'll suggest a default. Tell me to use it, override it, or leave as TBD.

**[Category 1: e.g., Contract Terms]**
| Item | My Suggested Assumption | Basis for Assumption |
|------|-------------------------|----------------------|
| Contract value Year 1 | $[X]M | Based on [rationale] |
| Gross margin | [X]% | Based on company's current [segment] margin |
| Contract duration | [X] years | Typical for this industry |

**[Category 2: e.g., Guarantor Strength]**
| Item | My Suggested Assumption | Basis for Assumption |
|------|-------------------------|----------------------|
| Guarantor liquidity | Adequate for proposed guarantees | Management provided guarantees during crisis |
| PFS available | No | Will note as condition to closing |

**[Category 3: e.g., Collateral]**
| Item | My Suggested Assumption | Basis for Assumption |
|------|-------------------------|----------------------|
| Property value | $[X]M | Purchase price from [year] |
| Equipment liquidation | 50-60% of cost | Standard for specialized industrial equipment |

### How would you like to proceed?
1. **Answer the unknowns now** - I'll wait for your input
2. **Use my suggestions** - I'll clearly flag each assumption in the memo
3. **Leave as TBD** - I'll insert placeholders for follow-up
4. **Mix** - Tell me which to assume, which to wait for, which to TBD"

---

## PHASE 2: DATA COLLECTION WITH CITATION TRACKING

### Citation Tracking System

**CRITICAL**: Every piece of data must be tracked with its source. Create an internal citations object throughout data collection:

```javascript
citations = {
  "Company financials (2024)": "Morningstar Direct API - Retrieved [date]",
  "Revenue $45M": "Uploaded financial statement: ABC_Corp_2024_Financials.pdf, page 3",
  "Industry growth rate 8.5%": "S&P Capital IQ Industry Report - Manufacturing Sector 2025",
  "Management commentary on expansion": "Aiera earnings call transcript Q3 2024",
  "Stock price $42.50": "LSEG Real-time data - Retrieved [date]",
  "Debt-to-equity industry average 2.1x": "Web search: Industry benchmarks manufacturing sector",
  "EBITDA $6.2M (estimated)": "DEMO DATA - For demonstration purposes only"
}
```

### Data Sourcing Strategy

#### For Public Companies:

**1. Company Financials (Morningstar)**
- Query Morningstar MCP for:
  - Income statements (3-5 years)
  - Balance sheets (3-5 years)
  - Cash flow statements (3-5 years)
  - Key ratios
- **Citation format**: "Morningstar Direct - [Company Name] financials as of [date]"

**2. Credit Ratings & Research (S&P)**
- Query S&P MCP for:
  - Credit ratings (if available)
  - Industry research and benchmarks
  - Peer comparisons
  - Capital IQ data
- **Citation format**: "S&P Capital IQ - [specific report/data point] accessed [date]"

**3. Management Commentary (Aiera)**
- Query Aiera MCP for:
  - Recent earnings call transcripts
  - Management outlook and strategy
  - Q&A with analysts
  - Forward guidance
- **Citation format**: "Aiera - [Company Name] [Event Type] [Date]"

**4. Market Data (LSEG)**
- Query LSEG MCP for:
  - Stock price and performance
  - Market capitalization
  - Trading volume and liquidity
  - Analyst estimates
- **Citation format**: "LSEG Refinitiv - [Data point] as of [date]"

**5. Supplementary Web Search**
- Use WebSearch for:
  - Recent news about the company
  - Industry trends and outlook
  - Competitor information
  - Market conditions
- **Citation format**: "Web source - [Article title] - [URL] - [Date]"

#### For Private Companies:

**1. Financial Statement Upload**
- Prompt: "Since this is a private company, please upload the company's financial statements (PDF or Excel format). I need at least 2-3 years of historical financials."
- Process uploaded files:
  - If PDF: Extract text and tables
  - If Excel: Read directly
- **Citation format**: "Uploaded document: [filename] - page [X] or sheet [Y]"

**2. Industry Research (S&P/Web)**
- Even without company data, gather industry benchmarks
- Query S&P for industry averages
- Web search for industry trends
- **Citation format**: Standard citation per source type above

**3. Management Interview Data**
- Information provided verbally during interview
- **Citation format**: "Provided by [Banker name] during credit interview [date]"

#### Special Module: Contract-Based Financing

When the loan purpose involves financing a new customer contract, the contract economics are CRITICAL to the credit analysis. Use this structured approach:

**Trigger:** Loan purpose mentions "contract," "new customer," "project financing," or similar

**Contract Information Questionnaire:**

"This financing is tied to a new contract. To build accurate pro formas, I need to understand the contract economics:

**Contract Status:**
- [ ] Executed/Signed
- [ ] In final negotiation
- [ ] LOI/Term sheet stage
- [ ] Verbal/preliminary discussions

**Required Information (please provide or confirm my assumptions):**

| Question | Your Answer | If Unknown, I'll Assume |
|----------|-------------|-------------------------|
| Customer name | [Required] | Cannot assume |
| Total contract value | $_______ | Cannot assume - need at least a range |
| Contract duration | _____ years | 3 years (typical) |
| Year 1 revenue | $_______ | 30% of total (ramp-up) |
| Year 2 revenue | $_______ | 35% of total |
| Year 3 revenue | $_______ | 35% of total |
| Expected gross margin | _____% | Company's current blended margin for similar products |
| Payment terms | Net ___ days | Net 45 (typical commercial) |
| Performance milestones | Yes/No | No |
| Cancellation provisions | Describe | Standard mutual termination |

**If contract details are preliminary:**
I can build a sensitivity analysis showing how credit metrics change across scenarios:

| Scenario | Year 1 Revenue | Pro Forma DSCR | Pro Forma Leverage |
|----------|----------------|----------------|-------------------|
| Conservative | $[X]M | [X]x | [X]x |
| Base Case | $[X]M | [X]x | [X]x |
| Optimistic | $[X]M | [X]x | [X]x |

Would a sensitivity approach be helpful while contract terms are being finalized?"

#### Demo Mode vs. Draft Mode Distinction

**Important:** Distinguish between "demo mode" (fake company) and "draft mode" (real company, incomplete data).

**Demo Mode Triggers:**
- "Make up a company"
- "Use fake data"
- "This is just for training"
- "Create a sample memo"

**Draft Mode Triggers (NOT demo mode):**
- "I don't have all the details yet"
- "Use your best guess for now"
- "We're still negotiating terms"
- Real company name with incomplete data

**Demo Mode Response:**
"Understood - I'll create a fully simulated credit memo with realistic but fictional data. The memo will be clearly marked as DEMONSTRATION throughout.

To make it useful, what scenario should I model?
1. Strong credit - easy approval
2. Moderate risk - standard deal
3. Marginal credit - requires mitigants
4. Decline scenario - for training purposes"

**Draft Mode Response:**
"Got it - this is a real deal with incomplete information. I'll:
1. Use actual data where available
2. Present suggested assumptions for missing items (you can confirm or override)
3. Clearly flag all assumptions in the memo
4. NOT mark this as a 'demo' since it's a real credit

This gives you a working draft that's easy to update as details are finalized.

Let me summarize what I know vs. what I'll need to assume..."

**Demo Mode - Additional Steps:**

**1. Acknowledge and Confirm:**
```
Understood - I'll generate realistic demo data for this credit memo.
This will be clearly marked as "DEMO DATA" in the final memo and all
citations will indicate these are placeholder values for demonstration purposes.

To make the demo realistic, what loan characteristics should I focus on?
- Strong credit profile?
- Moderate risk?
- Challenging situation that needs mitigation?
```

**2. Generate Realistic Data:**
- Create plausible financials based on industry and loan size
- Ensure ratios are internally consistent
- Make data appropriate for the loan decision (approval or conditional)

**3. Citation Format for Demo Data:**
- **Citation**: "DEMO DATA - Simulated for demonstration purposes only. Not based on actual company financials."

**4. Add Prominent Disclaimer:**
Include this in the memo header:
```
⚠️ DEMONSTRATION CREDIT MEMO ⚠️
This credit memo contains simulated data for demonstration purposes only.
All financial figures, ratios, and analysis are placeholder values and
should not be used for actual credit decisions.
```

### Data Validation Checkpoint

After attempting to gather data, present a summary to the banker:

```
Here's what I've gathered so far:

✓ Company financials (2022-2024) - Source: Morningstar
✓ Credit rating: BBB - Source: S&P
✓ Recent earnings call Q4 2024 - Source: Aiera
✓ Industry benchmarks - Source: S&P Industry Reports
⚠ Missing: Detailed A/R aging report
⚠ Missing: Equipment appraisal for collateral

Would you like to:
1. Upload additional documents for missing items?
2. Have me search for alternative data sources?
3. Proceed with available data and note gaps in the memo?
4. Use demo/placeholder data for missing items?
```

---

## PHASE 3: FINANCIAL ANALYSIS

### Calculate Key Ratios

Using gathered data, calculate and interpret these critical ratios:

#### Liquidity Ratios

**Current Ratio = Current Assets / Current Liabilities**
- Target: 1.2 - 2.0
- Interpretation: Company's ability to pay short-term obligations
- **Flag if**: < 1.0 (concerning) or > 3.0 (inefficient use of assets)

**Quick Ratio = (Current Assets - Inventory) / Current Liabilities**
- Target: 0.8 - 1.5
- Interpretation: Liquidity without relying on inventory sales

**Working Capital = Current Assets - Current Liabilities**
- Interpretation: Absolute liquidity cushion
- Compare to industry norms

#### Leverage Ratios

**Debt-to-Tangible Net Worth = Total Liabilities / (Net Worth - Intangibles)**
- Target: < 3.0 - 4.0x
- Interpretation: Financial leverage and solvency
- **Flag if**: > 4.0x (high leverage)

**Debt-to-EBITDA = Total Debt / EBITDA**
- Target: < 3.0 - 4.0x
- Interpretation: Time to repay all debt from operating earnings

**Total Liabilities to Total Assets**
- Target: < 0.60 (60%)
- Interpretation: Percentage of assets financed with debt

#### Coverage Ratios

**Debt Service Coverage Ratio (DSCR) = EBITDA / Annual Debt Service**
- **MINIMUM: 1.25x** (most critical ratio for loan approval)
- Target: > 1.50x (comfortable)
- Interpretation: Ability to service debt from operating cash flow
- **FLAG if**: < 1.25x (requires strong mitigants to approve)

**Interest Coverage Ratio = EBITDA / Interest Expense**
- Target: > 3.0x
- Interpretation: Ability to cover interest payments

#### Profitability Ratios

**Gross Profit Margin = (Revenue - COGS) / Revenue**
- Compare to industry average
- Look for trends (improving vs declining)

**Operating Profit Margin = Operating Income / Revenue**
- Compare to industry average
- Indicates operational efficiency

**Return on Assets (ROA) = Net Income / Total Assets**
- Measures asset efficiency

**Return on Equity (ROE) = Net Income / Shareholders' Equity**
- Measures returns to owners

#### Trend Analysis

For each ratio, analyze 3-5 year trends:
- **Improving**: Positive indicator
- **Stable**: Acceptable if within targets
- **Declining**: Concern - investigate cause

### Industry Benchmarking

Compare company ratios to industry averages (from S&P or web search):

```
Ratio Comparison Table:
                          Company    Industry Avg    Assessment
Current Ratio             1.85          1.50         Above Average ✓
Debt-to-Worth            2.1x          2.8x         Below Average ✓
DSCR                     1.45x         1.30x        Above Average ✓
Operating Margin         12.5%         10.2%        Above Average ✓
```

### Risk Assessment

Identify top 3-5 risks and rate severity (High/Medium/Low):

**Common C&I Loan Risks:**
1. **Cash Flow Risk**: Insufficient or inconsistent cash flow
2. **Industry Risk**: Declining industry or heavy competition
3. **Management Risk**: Inexperienced team or key person dependency
4. **Collateral Risk**: Inadequate or hard-to-liquidate collateral
5. **Customer Concentration**: Over-reliance on few customers
6. **Market Risk**: Economic downturn impact
7. **Regulatory Risk**: Industry-specific regulations
8. **Covenant Risk**: Potential for covenant violations

**For Each Risk, Document:**
- **Risk Description**: What could go wrong?
- **Severity**: High/Medium/Low
- **Probability**: High/Medium/Low
- **Mitigating Factors**: What reduces this risk?
- **Proposed Covenants/Conditions**: How to monitor/control this risk?

### Stress Testing

Perform "what if" scenarios:

**Revenue Decline Scenario:**
- What if revenue drops 10-20%?
- Does DSCR stay above 1.25x?
- Does company violate covenants?

**Margin Compression Scenario:**
- What if gross margin declines by 200-300 bps?
- Impact on EBITDA and debt coverage?

**Interest Rate Scenario:**
- If variable rate, what if rates increase 200-300 bps?
- Impact on debt service coverage?

---

## ASSUMPTION TRACKING

### Continuous Assumption Logging

Throughout the memo creation process, maintain a running registry of all assumptions made. Surface this to the banker at key checkpoints.

**After each major section, present:**

"**Assumptions made in this section:**
| ID | Assumption | Value Used | Basis | Confirmed? |
|----|------------|------------|-------|------------|
| A1 | [Description] | [Value] | [Source/rationale] | ⏳ Pending |
| A2 | [Description] | [Value] | [Source/rationale] | ✓ Confirmed |

Running total: [X] assumptions made | [Y] confirmed | [Z] pending

Would you like to confirm or modify any of these before I continue?"

**Final Memo Assumption Summary:**

Include this table in the memo appendix:

"## APPENDIX: ASSUMPTION SUMMARY

This credit memo includes the following assumptions. Items marked 'Unconfirmed' should be verified before final credit approval.

| ID | Category | Assumption | Value | Basis | Impact if Wrong | Status |
|----|----------|------------|-------|-------|-----------------|--------|
| A1 | Revenue | Pepe's Y1 revenue | $40M | Banker estimate | High - affects all coverage ratios | ⏳ Unconfirmed |
| A2 | Margin | Contract gross margin | 42% | Blended HW/SW margin | Medium - affects profitability | ⏳ Unconfirmed |
| A3 | Structure | Equipment term | 7 years | Industry standard | Low - structural only | ✓ Confirmed |
| A4 | Pricing | Base rate spread | +325 bps | Pricing matrix, RR6 | Medium - affects RAROC | ✓ Confirmed |

**Assumption Categories:**
- **High Impact:** Changes would materially affect credit decision
- **Medium Impact:** Changes would affect terms/conditions but not approval
- **Low Impact:** Structural/administrative assumptions"

### Assumption Confirmation Prompts

At minimum, pause for confirmation at these points:
1. After deal structure is proposed
2. After pro forma projections are built
3. After RAROC is calculated
4. Before generating final memo

---

## PHASE 4: RAROC PRICING ANALYSIS

### Overview

This bank uses **Risk-Adjusted Return on Capital (RAROC)** as the primary framework for loan pricing. Every credit memo must include a complete RAROC analysis demonstrating that the proposed pricing creates shareholder value.

**Reference Document:** See `resources/RAROC_METHODOLOGY.md` for complete methodology, formulas, and examples.

### Required RAROC Components

#### Step 1: Determine Risk Parameters

Based on the financial analysis from Phase 3, determine:

1. **Internal Risk Rating** (1-10 scale)
   - Based on DSCR, leverage, liquidity, management quality, industry risk
   - See UNDERWRITING_STANDARDS.md for rating criteria

2. **Probability of Default (PD)**
   - Map from risk rating (see RAROC_METHODOLOGY.md)
   - Example: Risk Rating 5 → PD of 1.00-2.00%

3. **Loss Given Default (LGD)**
   - Based on collateral type and quality
   - Senior Secured - Strong: 25-35%
   - Senior Secured - Standard: 35-45%
   - Senior Unsecured: 45-60%

4. **Exposure at Default (EAD)**
   - Typically the full loan amount
   - For lines of credit, apply utilization factor

5. **Economic Capital Allocation**
   - Map from risk rating (see RAROC_METHODOLOGY.md)
   - Example: Risk Rating 5 → 4-8% of EAD

#### Step 2: Generate Pricing Inputs with Pricing Matrix

**NEW WORKFLOW:** Use the `pricing-matrix.js` tool to automatically generate RAROC calculator inputs based on your risk rating and loan amount.

**Location:** `resources/pricing-matrix.js`

**What It Does:**
- Takes risk rating and loan amount as inputs
- Automatically determines appropriate pricing based on bank assumptions
- Generates interest rate from target spreads by risk rating
- Determines fees (origination, annual) based on loan size and risk
- Calculates operating costs based on loan amount
- Sets collateral LGD based on collateral type
- Estimates relationship value (deposits, treasury fees)
- Outputs a complete RAROC calculator command ready to run

**Usage:**
```bash
# Step 2a: Generate pricing inputs
node resources/pricing-matrix.js \
  --risk-rating 5 \
  --loan-amount 5000000 \
  --borrower-name "ABC Manufacturing" \
  --collateral-type senior-secured-standard

# The output will include a complete RAROC calculator command
```

**Example Output:**
```
═══════════════════════════════════════════════════════════
           PRICING MATRIX - RAROC INPUT BUILDER
═══════════════════════════════════════════════════════════

BORROWER: ABC Manufacturing
LOAN DETAILS:
  Loan Amount:              $5,000,000
  Risk Rating:              5
  Hurdle Rate:              15%

PRICING INPUTS (Generated):
  Interest Rate:            7.25% (calculated from 275 bps spread)
  Collateral LGD:           40%
  Operating Costs:          50 bps ($25,000)
  Origination Fee:          0.75% ($37,500)
  Annual Fees:              $5,000
  Average Deposits:         $1,750,000 (35% of loan)
  Treasury Mgmt Fees:       $15,000
  Other Fee Income:         $5,000

─────────────────────────────────────────────────────────
RAROC CALCULATOR COMMAND:
─────────────────────────────────────────────────────────

node resources/raroc-calculator.js \
  --loan-amount 5000000 \
  --interest-rate 7.25 \
  --risk-rating 5 \
  --lgd 0.40 \
  --funding-cost 4.50 \
  --operating-cost-bps 50 \
  --origination-fee-pct 0.75 \
  --annual-fees 5000 \
  --avg-deposits 1750000 \
  --deposit-cost 0.50 \
  --deposit-reinvestment-rate 4.50 \
  --treasury-mgmt-fees 15000 \
  --other-fees 5000
```

**Step 2b: Review and Adjust Inputs**

The pricing matrix uses bank-specific assumptions from `resources/BANK_ASSUMPTIONS.md`. Review the generated inputs and adjust for deal-specific factors:

**Adjustments to Consider:**
1. **Interest Rate:**
   - Competitive pressure may require lower rate
   - Relationship value may justify tighter pricing
   - If overriding, document reason (competitive match, relationship exception, etc.)

2. **Deposits:**
   - Replace default (35% of loan) with actual committed deposits
   - Require documentation: deposit agreements, historical balances, board resolution
   - Be conservative - use contracted/committed amounts only

3. **LGD:**
   - Adjust for specific collateral package quality
   - Consider advance rates and coverage ratios
   - Factor in collateral monitoring and control

4. **Fees:**
   - May need adjustment for competitive reasons
   - Large relationships may negotiate fee reductions
   - Document any fee waivers or reductions

**Override Example:**
```bash
# If you need to override the calculated rate (e.g., competitive match)
node resources/pricing-matrix.js \
  --risk-rating 5 \
  --loan-amount 5000000 \
  --interest-rate 6.75 \
  --avg-deposits 2500000 \
  --collateral-type ar-standard
```

**Step 2c: Run RAROC Calculator**

**CRITICAL:** Use the deterministic `raroc-calculator.js` script to perform all RAROC calculations. DO NOT calculate manually.

**Option A: Copy-Paste Command**
Copy the RAROC calculator command from the pricing matrix output and run it.

**Option B: Pipe Directly**
```bash
node resources/pricing-matrix.js \
  --risk-rating 5 \
  --loan-amount 5000000 \
  --output-command | bash
```

This generates the pricing inputs AND runs the RAROC calculator in one step.

**RAROC Calculator Output:**
The calculator provides a comprehensive report including:
- Risk parameters (PD, LGD, Expected Loss, Economic Capital)
- Revenue and cost breakdowns
- Stand-alone RAROC vs. hurdle rate
- Relationship RAROC (with deposits and fees)
- Three stress test scenarios
- Decision recommendation

**Important Notes:**
- The pricing matrix uses bank assumptions from `BANK_ASSUMPTIONS.md`
- The RAROC calculator uses bank-approved formulas and policy constants
- PD (Probability of Default) is automatically determined from risk rating
- Economic Capital allocation is automatically determined from risk rating
- All calculations are deterministic and verifiable
- Stress testing is automatically performed
- **Workflow:** Pricing Matrix → generates inputs → RAROC Calculator → produces analysis

#### Step 3: Document Calculator Inputs and Results

In your credit memo, document the inputs you provided to the calculator and the results:

**RAROC Calculator Inputs:**
```
Loan Amount:             $5,000,000
Risk Rating:             5 (Moderate Risk)
Proposed Rate:           6.25%
Term:                    5 years
LGD:                     40% (senior secured - standard collateral)
Funding Cost:            4.50%
Operating Cost Rate:     0.50%
Origination Fee:         $50,000 (1.0%)
Annual Fees:             $5,000

Relationship Components:
  Average Deposits:      $2,000,000
  Deposit Cost:          0.50%
  Reinvestment Rate:     4.50%
  Treasury Fees:         $15,000
  Other Fees:            $5,000
```

**RAROC Calculator Results:**
```
Risk Parameters:
  PD (Probability of Default):  1.50%
  Expected Loss:                $30,000
  Economic Capital:             $250,000 (5.0% of EAD)

Stand-Alone Analysis:
  Total Revenue:                $367,500
  Total Costs:                  $280,000
  Net Income:                   $87,500
  Stand-Alone RAROC:            35.0%
  Hurdle Rate:                  15.0%
  Spread to Hurdle:             +20.0%

Relationship Analysis:
  Loan Net Income:              $87,500
  Deposit Value:                $80,000
  Fee Income:                   $20,000
  Total Relationship Income:    $187,500
  Relationship RAROC:           75.0%

Decision: EXCEEDS HURDLE - Approved ✓
```

**Copy the full calculator output into the credit memo's RAROC section.**

#### Step 4: Interpret Results and Provide Recommendation

Based on the calculator output, provide your interpretation and recommendation:

**Key Metrics from Calculator:**
- Stand-Alone RAROC: [X.X]%
- Hurdle Rate: [XX]%
- Spread to Hurdle: [±X.X]%
- Relationship RAROC: [X.X]%
- Stress Test Overall Assessment: [Acceptable/Marginal/Fails]

### Pricing Recommendation

Based on RAROC analysis, provide clear pricing recommendation:

#### Scenario A: RAROC Exceeds Hurdle

```
✓ RECOMMENDED PRICING

Proposed Rate:           6.25%
Stand-Alone RAROC:       35.0%
Hurdle Rate:             15.0%
Spread to Hurdle:        +20.0%

Conclusion: Proposed pricing significantly exceeds hurdle rate and
creates substantial shareholder value. RECOMMEND APPROVAL at proposed terms.
```

#### Scenario B: RAROC Below Hurdle (No Relationship Value)

```
⚠ PRICING REQUIRES ADJUSTMENT

Proposed Rate:           5.50%
Stand-Alone RAROC:       12.0%
Hurdle Rate:             15.0%
Spread to Hurdle:        -3.0%

Required Rate for Hurdle: 5.95%
Alternative: Reduce loan amount to improve returns

Conclusion: Proposed pricing destroys shareholder value. RECOMMEND:
- Increase rate to 5.95% minimum, OR
- Reduce loan amount by $1M, OR
- DECLINE if customer won't accept adjusted terms
```

#### Scenario C: Relationship Value Justifies Exception

```
✓ APPROVED WITH RELATIONSHIP VALUE

Proposed Rate:           5.50%
Stand-Alone RAROC:       12.0% (below 15% hurdle)
Relationship RAROC:      22.0% (exceeds hurdle)

Relationship Components:
- Committed Deposits:    $3,000,000 (documented)
- Deposit Value:         $120,000 annually
- Fee Income:            $30,000 annually

Conclusion: While stand-alone RAROC is below hurdle, full relationship
profitability exceeds hurdle rate. RECOMMEND APPROVAL contingent on:
1. Executed deposit agreement for $3M minimum balance
2. Treasury management services adoption within 90 days
3. Annual relationship review to validate profitability
```

### Banker's Pricing Exception Request

**When requesting pricing below calculated rate**, banker must provide:

#### A. Relationship Commitment Documentation

```
Current Deposits:        $[Amount]
Committed Deposits:      $[Amount] - [Attach signed commitment letter]
Expected Growth:         $[Amount] over [timeframe]
Fee Income Breakdown:
  - Treasury Management: $[Amount]
  - Wire Transfers:      $[Amount]
  - Other Services:      $[Amount]
Total Relationship Value: $[Amount] annually

Relationship RAROC:      [X.X]% (must exceed hurdle)
```

#### B. Competitive Justification

```
Competitor Name:         [Bank Name]
Competitor Rate:         [X.XX]%
Our Calculated Rate:     [X.XX]%
Requested Rate:          [X.XX]%
Rate Reduction:          [XX] basis points

RAROC at Requested Rate: [X.X]%
vs. Hurdle Rate:         [X.X]%

Justification: [Specific reason why match is strategically important]
```

#### C. Strategic Value Documentation

```
Strategic Importance:
- [ ] Market share in target segment
- [ ] Industry expertise building
- [ ] Future growth potential (quantify)
- [ ] Defensive pricing (prevent attrition)
- [ ] Other: [Specify]

Expected Future Value:
- Year 1: $[Amount] additional business
- Year 2: $[Amount] additional business
- Year 3: $[Amount] additional business

Risk Assessment at Reduced Pricing:
- Stressed RAROC remains above: [X]%
- Acceptable given: [Risk mitigants]
```

### Fair Lending Compliance Note

**CRITICAL:** All pricing decisions and exceptions must be:
1. **Documented** with specific business justification
2. **Approved** at appropriate authority level
3. **Tracked** in centralized exception database
4. **Reviewable** to ensure consistent, non-discriminatory application

Generic justifications like "good customer" or "relationship value" without specific documentation are **NOT acceptable** and create compliance risk.

### RAROC Stress Testing

Test RAROC under adverse scenarios:

**Scenario 1: Credit Downgrade**
```
Risk Rating: 5 → 7
PD: 1.50% → 3.50%
Expected Loss: Doubles
Economic Capital: Increases 50%
New RAROC: [Calculate]

Assessment: [Does loan remain above cost of equity (12%)?]
```

**Scenario 2: Loss of Deposits**
```
Deposits Decline: 50%
Deposit Value: Reduced by half
New Relationship RAROC: [Calculate]

Assessment: [Does relationship remain profitable?]
```

**Scenario 3: Rate Compression**
```
Market Rates: Compress 50 bps
Revenue: Decreases by $[Amount]
New RAROC: [Calculate]

Assessment: [Impact on profitability]
```

**Requirement:** Stressed RAROC should remain ≥ bank's cost of equity (12%).

### RAROC Section Format for Credit Memo

Use this standard format in the credit memo:

```markdown
## RAROC ANALYSIS

### Risk Parameters
- Internal Risk Rating: [X] ([Risk Level Description])
- Probability of Default (PD): [X.XX]%
- Loss Given Default (LGD): [XX]%
- Exposure at Default (EAD): $[Amount]
- Expected Loss (EL): $[Amount] ([X.XX]% of EAD)
- Economic Capital: $[Amount] ([X.X]% of EAD)

### Profitability Analysis

**Revenue:**
| Component | Rate/Amount | Annual Income |
|-----------|-------------|---------------|
| Interest Income | [X.XX]% | $[Amount] |
| Origination Fee | [X.XX]% | $[Amount] |
| Annual Fees | - | $[Amount] |
| **Total Revenue** | | **$[Amount]** |

**Costs:**
| Component | Rate/Amount | Annual Cost |
|-----------|-------------|-------------|
| Funding Cost | [X.XX]% | $[Amount] |
| Operating Costs | [X.XX]% | $[Amount] |
| Expected Loss | - | $[Amount] |
| **Total Costs** | | **$[Amount]** |

**Net Income:** $[Amount]

### RAROC Calculation

**Stand-Alone RAROC:**
- RAROC = Net Income / Economic Capital
- RAROC = $[Amount] / $[Amount] = **[XX.X]%**
- Hurdle Rate: **[XX]%**
- Spread to Hurdle: **+/-[X.X]%**

**Assessment:** ✓ Exceeds Hurdle / ⚠ Below Hurdle

### Relationship Value

**Additional Income:**
| Component | Details | Annual Value |
|-----------|---------|--------------|
| Deposit Value | $[Amount] avg @ [X.X]% NIM | $[Amount] |
| Treasury Mgmt | [Details] | $[Amount] |
| Wire Transfers | [Details] | $[Amount] |
| Other Fees | [Details] | $[Amount] |
| **Total Additional** | | **$[Amount]** |

**Relationship RAROC:**
- Total Relationship Income: $[Amount]
- Total Economic Capital: $[Amount]
- Relationship RAROC: **[XX.X]%**
- Hurdle Rate: **[XX]%**
- Spread to Hurdle: **+[X.X]%**

**Assessment:** ✓ Exceeds Hurdle

### Pricing Recommendation

[Clear statement of recommendation with RAROC justification]

**Recommended Pricing:**
- Interest Rate: [X.XX]%
- Origination Fee: [X.XX]%
- Conditions: [Any pricing contingencies]

**Rationale:**
[2-3 sentences explaining how pricing creates shareholder value, supported by RAROC metrics]

### Stress Test Results

**Downside Scenarios:**
1. Credit Downgrade (Rating → [X]): RAROC = [XX]%
2. Deposit Loss (50% reduction): RAROC = [XX]%
3. Rate Compression (50 bps): RAROC = [XX]%

**Assessment:** [Do stressed scenarios remain above cost of equity?]
```

---

## PHASE 5: CREDIT MEMO GENERATION

### Interactive Review Checkpoints

After completing each major memo section, pause for banker input before proceeding.

**After Risk Assessment Section:**

"I've drafted the Risk Assessment with [X] key risks:

1. **[Risk 1]** - Severity: [H/M/L]
2. **[Risk 2]** - Severity: [H/M/L]
3. **[Risk 3]** - Severity: [H/M/L]

Before I continue:
- Did I miss any risks you're concerned about?
- Do my severity ratings match your view?
- Are the proposed mitigants realistic for your bank?

I've assigned **Risk Rating [X]** based on:
- [Key factor 1]
- [Key factor 2]
- [Key factor 3]

Does this rating feel right? Should I adjust for a [X-1] or [X+1]?"

**After RAROC Section:**

"RAROC analysis complete:
- Stand-alone RAROC: [X]% vs. [Y]% hurdle
- Relationship RAROC: [X]% vs. [Y]% hurdle
- Recommendation: [Exceeds/Meets/Below] hurdle

Key inputs used:
| Input | Value | Source |
|-------|-------|--------|
| Risk Rating | [X] | Credit analysis |
| PD | [X]% | Mapped from rating |
| LGD | [X]% | [Collateral type] |
| Funding Cost | [X]% | Bank standard |

Does the pricing feel right for this deal? Any competitive factors I should consider?"

**After Covenant Section:**

"Proposed covenant package:

| Covenant | Proposed Level | Current Actual | Cushion |
|----------|----------------|----------------|---------|
| Min DSCR | 1.25x | [X]x | [Y]% |
| Max Leverage | [X]x | [Y]x | [Z]% |
| Min Liquidity | $[X]M | $[Y]M | [Z]% |

Standard or aggressive for your credit policy?
Any covenants to add or remove based on specific deal dynamics?"

**After Complete Draft:**

"Draft memo complete. Before I finalize:

1. **Recommendation:** [APPROVED/APPROVED W/ CONDITIONS/DECLINED]
   - Does this match your view?

2. **Conditions:** [List key conditions]
   - Anything to add or remove?

3. **Assumptions:** [X] assumptions made, [Y] unconfirmed
   - Review assumption summary in appendix

4. **Gaps:** Missing [list items]
   - Should these be conditions to closing or obtained before committee?

Ready to generate final memo, or changes needed?"

### Memo Structure

Generate the credit memo using this standardized format (see MEMO_TEMPLATE.md for full template):

#### Header Section
```
CREDIT MEMORANDUM

[⚠️ DEMONSTRATION CREDIT MEMO ⚠️ - if demo mode]

Borrower: [Company Name]
Loan Amount: $[Amount]
Loan Type: [Type]
Purpose: [Purpose]
Date: [Current Date]
Prepared By: [Banker Name/AI Assistant]
Risk Rating: [Rating]
Recommendation: [APPROVED / APPROVED WITH CONDITIONS / DECLINED]
```

#### Table of Contents
1. Executive Summary
2. Loan Request
3. Borrower Analysis
4. Financial Analysis
5. Risk Assessment
6. Recommendation & Conditions
7. Appendices
8. Citations & Data Sources

#### 1. Executive Summary (1 page max)
- Brief company overview
- Loan request summary
- Key financial highlights
- Primary risks and mitigants
- Bottom-line recommendation

#### 2. Loan Request
- Loan amount and type
- Purpose/use of proceeds
- Proposed terms (rate, maturity, amortization)
- Collateral description and value
- Guarantees and personal support
- Pricing and estimated ROE

#### 3. Borrower Analysis

**Company Background:**
- Industry and business description
- Years in business
- Ownership structure
- Key products/services
- Customer base and market position

**Management Team:**
- Key executives and experience
- Management depth
- Succession planning

**Industry Analysis:**
- Industry trends and outlook
- Competitive position
- Market dynamics
- Growth prospects

#### 4. Financial Analysis

**Historical Performance (3-5 years):**
- Revenue trends with YoY growth rates
- Profitability trends
- Cash flow analysis
- Balance sheet strength

**Key Ratios Table:**
Present all calculated ratios in a clear table with:
- Company figures
- Industry benchmarks
- Assessment (Above/Below/In-line with target)

**The Five C's Analysis:**

**CHARACTER:**
- Credit history
- Payment record with suppliers/other lenders
- Business reputation
- Personal credit of guarantors

**CAPACITY:**
- Cash flow adequacy
- Debt service coverage analysis
- Working capital cycle
- Seasonality considerations
- Projected cash flows

**CAPITAL:**
- Net worth and equity position
- Owner's investment
- Liquidity reserves
- Contingency resources

**COLLATERAL:**
- Primary collateral details
- Valuation and loan-to-value
- Lien position
- Secondary collateral
- Collateral coverage ratio

**CONDITIONS:**
- Economic conditions
- Industry conditions
- Market trends
- Any special circumstances

**Stress Testing Results:**
- Summary of scenarios tested
- Results and covenant cushion
- Sensitivities

#### 5. Risk Assessment

**For Each Identified Risk (Top 3-5):**

**Risk #1: [Name]**
- **Description**: [What is the risk?]
- **Severity**: High/Medium/Low
- **Probability**: High/Medium/Low
- **Impact**: [What happens if it materializes?]
- **Mitigating Factors**: [What reduces this risk?]
- **Monitoring**: [How will we track this?]

[Repeat for all major risks]

**Overall Risk Rating**: [Low/Moderate/Satisfactory/Marginal/Substandard]

**Explanation of Risk Rating:**
[Justify the rating based on the Five C's and identified risks]

#### 6. Recommendation & Conditions

**Recommendation**: APPROVED / APPROVED WITH CONDITIONS / DECLINED

**Rationale**: [2-3 paragraphs explaining the recommendation]

**Conditions of Approval** (if applicable):
- Satisfactory appraisal of equipment
- Receipt of landlord's waiver
- Personal guarantee from principals
- Insurance requirements
- Any other conditions precedent

**Covenants** (if applicable):
- Financial covenants (minimum DSCR, maximum debt-to-worth, etc.)
- Reporting requirements (frequency of financial statements)
- Negative covenants (no additional debt, maintain insurance, etc.)

**Pricing**:
- Interest rate and basis
- Fees
- Estimated ROE (return on equity)
- Comparison to risk-based pricing grid

#### 7. Appendices

List all supporting documents:
- Appendix A: Financial Statements (3-5 years)
- Appendix B: Tax Returns
- Appendix C: Accounts Receivable Aging
- Appendix D: Accounts Payable Aging
- Appendix E: Business Plan/Projections
- Appendix F: Credit Reports
- Appendix G: Collateral Appraisals
- Appendix H: Industry Research
- Appendix I: Customer Contracts (if relevant)

#### 8. Citations & Data Sources

**CRITICAL SECTION**: List every data source used in the memo

Format:
```
DATA SOURCES & CITATIONS

Company Financial Data:
• Income Statement (2022-2024): Morningstar Direct - ABC Corp financials retrieved 2025-12-02
• Balance Sheet (2022-2024): Morningstar Direct - ABC Corp financials retrieved 2025-12-02
• Credit Rating (BBB): S&P Capital IQ - Retrieved 2025-12-02

Industry Benchmarks:
• Manufacturing sector benchmarks: S&P Industry Reports - Manufacturing Sector 2025
• Industry growth rate (8.5%): IBISWorld Manufacturing Industry Report - December 2025

Management Commentary:
• Q4 2024 earnings call: Aiera transcript - ABC Corp Q4 2024 Earnings Call, January 15, 2025

Market Data:
• Stock price ($42.50): LSEG Real-time data - Retrieved 2025-12-02 at 2:30 PM EST

Uploaded Documents:
• 2024 Financial Statements: ABC_Corp_2024_Financials.pdf (uploaded by banker 2025-12-02)
• Equipment appraisal: Equipment_Appraisal_2025.pdf (uploaded by banker 2025-12-02)

Web Sources:
• Industry outlook article: "Manufacturing Sector Trends 2025" - Industry Week - https://www.industryweek.com/... - Nov 2025

[IF DEMO MODE]
⚠️ DEMONSTRATION DATA SOURCES ⚠️
The following data points are simulated for demonstration purposes only:
• Revenue figures ($45M, $48M, $52M)
• EBITDA margins (12.5%, 13.1%, 13.8%)
• All balance sheet figures
• Customer concentration metrics
• Management experience details

These simulated values are designed to create a realistic credit scenario but
should not be used for actual credit decisions.
```

---

## OUTPUT FORMATTING REQUIREMENTS

### Consistent Format

**1. Use Markdown Headers:**
- `#` for main sections
- `##` for subsections
- `###` for sub-subsections

**2. Use Tables for Financial Data:**
```markdown
| Year | Revenue | EBITDA | Net Income |
|------|---------|--------|------------|
| 2022 | $45.0M  | $5.6M  | $2.3M      |
| 2023 | $48.2M  | $6.3M  | $2.8M      |
| 2024 | $52.1M  | $7.2M  | $3.4M      |
```

**3. Use Bullet Points for Lists:**
- Key points
- Risk factors
- Conditions

**4. Use Callout Boxes for Critical Info:**
```markdown
**⚠️ KEY RISK**: Customer concentration - Top 3 customers represent 55% of revenue
```

**5. Use Consistent Currency Formatting:**
- Thousands: $X.XK (e.g., $125.5K)
- Millions: $X.XM (e.g., $45.2M)
- Billions: $X.XB (e.g., $1.3B)

**6. Use Consistent Ratio Formatting:**
- Multiple/X format: 2.5x, 1.45x
- Percentage format: 12.5%, 65.3%
- Always 1-2 decimal places

**7. Professional Tone:**
- Objective and analytical
- Avoid emotional language
- Present both positives and negatives
- Support conclusions with data
- Use banking industry terminology

### File Naming

Save the generated credit memo as:
`CreditMemo_[CompanyName]_[LoanAmount]_[Date].md`

Example: `CreditMemo_ABC_Manufacturing_2500K_20251202.md`

---

## SPECIAL CONSIDERATIONS

### When Data is Missing

If critical data cannot be obtained:

**Option 1: Note the Gap**
```
⚠️ DATA GAP: Accounts receivable aging report not available.
Unable to assess receivables quality and collection risk.
Recommend obtaining this prior to final credit approval.
```

**Option 2: Make Conservative Assumptions**
```
Note: Detailed customer concentration data not available.
Analysis assumes moderate concentration risk based on
industry norms for companies of this size.
```

**Option 3: Demo Mode**
```
DEMO DATA: Customer concentration simulated at 40% for
top 3 customers (moderate risk profile) - For demonstration only.
```

### When Banker Provides Conflicting Information

If MCP data conflicts with banker's statements:
```
Note: Banker indicated revenue of $50M, however Morningstar
data shows $48.2M. Analysis uses Morningstar figure.
Recommend clarifying discrepancy with borrower.
```

### When Deal is Declined

If the analysis indicates the loan should be declined:

**Be Direct but Professional:**
```
RECOMMENDATION: DECLINED

Based on the financial analysis, this credit request does not meet the
Bank's minimum underwriting standards. Key concerns include:

1. Debt Service Coverage Ratio of 0.95x is below the minimum 1.25x threshold
2. Declining revenue trend (down 15% YoY) with no clear turnaround plan
3. Negative working capital position of ($850K)
4. High customer concentration (80% from single customer under contract renewal)

While the management team has strong industry experience, the current
financial profile presents unacceptable credit risk without significant
additional support or restructuring of the request.

Alternative structures to consider:
- Reduced loan amount to improve coverage ratios
- Additional equity injection from owners
- Secured lending structure with stronger collateral position
```

### MCP Integration Notes

When the MCP servers are set up, the skill should:

**1. Detect Available MCP Servers:**
- Check if Morningstar MCP is available
- Check if S&P MCP is available
- Check if Aiera MCP is available
- Check if LSEG MCP is available

**2. Query Appropriately:**
- Use company ticker symbol or name to query
- Request specific data points (financials, ratings, transcripts, etc.)
- Handle API errors gracefully
- Fall back to alternative sources if MCP unavailable

**3. Parse and Structure Responses:**
- Extract relevant data from MCP responses
- Store in structured format for analysis
- Maintain citation information
- Handle missing data gracefully

---

## EXAMPLES & BEST PRACTICES

### Example: Opening the Interview

**Good:**
```
I'll help you create a comprehensive credit memo for this C&I loan.
Let me start by gathering some basic information:

1. What is the company name?
2. What industry/sector are they in?
3. Is this a public or private company?

We'll then dive into the loan details and financial information.
```

**Avoid:**
```
Please provide: company name, address, phone, fax, email, website,
EIN, state of incorporation, years in business, ownership structure,
management team names and titles, loan amount, loan type... [20 more questions]
```

### Example: Handling Demo Mode Request

**Banker**: "I don't have the actual financials yet, just make something up that looks realistic."

**Good Response:**
```
Understood! I'll create realistic demo data for this credit memo.
This will be clearly marked as simulated data throughout the document.

To make this realistic, what scenario should I model?
1. Strong borrower - solid financials, meets all underwriting guidelines
2. Moderate risk - acceptable but some areas of concern
3. Marginal deal - requires strong mitigants and conditions

Also, what's the approximate loan size and company revenue range you're thinking?
```

### Example: Data Gap Handling

**Good:**
```
I've gathered comprehensive data from Morningstar and S&P, but I'm
missing a few items:

⚠️ Not available: Detailed A/R aging report
⚠️ Not available: Equipment appraisal for collateral

Would you like to:
1. Upload these documents if you have them?
2. Proceed with the memo and note these as conditions of approval?
3. Use estimated/demo values for these items?
```

### Example: Citation in Text

**Good:**
```
The company reported revenue of $52.1M in 2024, representing 8.1%
growth over the prior year¹. This growth rate exceeds the industry
average of 5.2%², indicating strong competitive positioning.

¹Morningstar Direct - ABC Corp 10-K filing, March 2025
²S&P Capital IQ - Manufacturing Industry Report, Q4 2024
```

---

## ERROR HANDLING

### If Interview Stalls

If banker is unresponsive or provides minimal information:

**Prompt:**
```
I see we're missing some key information. Would you like to:
1. Continue the interview now?
2. Save progress and resume later?
3. Skip to demo mode with placeholder data?
4. Focus on a specific section first?
```

### If MCP Services Fail

If MCP queries return errors:

**Fallback Strategy:**
1. Try alternative MCP service (e.g., S&P if Morningstar fails)
2. Fall back to WebSearch
3. Request file upload from banker
4. Offer demo mode for that specific data point

**User Message:**
```
⚠️ I'm having trouble connecting to Morningstar for the financial data.
Let me try S&P Capital IQ instead... [or] Would you like to upload the
financial statements directly?
```

### If Calculations Don't Make Sense

If ratios are wildly out of range or data is inconsistent:

**Flag It:**
```
⚠️ DATA QUALITY CONCERN: The calculated current ratio of 0.15x
seems unusually low and may indicate missing or incorrect data.
Please verify the current assets ($150K) and current liabilities ($1.0M)
figures before proceeding.
```

---

## SUCCESS CRITERIA

A successful credit memo should:

✓ **Complete**: All sections filled out with relevant information
✓ **Cited**: Every data point has a clear source
✓ **Analyzed**: Financial ratios calculated and interpreted
✓ **Risk-Assessed**: Top risks identified with mitigants
✓ **Actionable**: Clear recommendation with supporting rationale
✓ **Professional**: Consistent formatting and banking terminology
✓ **Demo-Ready**: If in demo mode, clearly marked throughout

---

## FINAL NOTES

- **Always maintain professional banking tone**
- **Support every conclusion with data and citations**
- **Present balanced analysis (pros and cons)**
- **Be explicit about data quality and gaps**
- **Make demo data disclaimers prominent and clear**
- **Follow the template structure consistently**
- **Remember: The goal is to help the credit committee make an informed decision**

For detailed templates and reference materials, see:
- MEMO_TEMPLATE.md - Full credit memo template
- UNDERWRITING_STANDARDS.md - Ratio guidelines and thresholds
- INTERVIEW_GUIDE.md - Detailed interview questions by loan type

---

## APPENDIX: INTERACTIVE DECISION POINTS SUMMARY

Quick reference for when to pause and ask vs. proceed with defaults:

### ALWAYS ASK (Never Assume):
- Borrower name and basic info
- Loan amount
- Loan purpose
- Whether this is demo or real
- Contract value (if contract-based financing)
- Final recommendation (confirm before generating)

### ASK WITH SUGGESTED DEFAULT:
- Loan structure (term, amortization)
- Pricing (provide matrix-based suggestion)
- Covenant levels (provide risk-rating based suggestion)
- RAROC inputs (provide rating-mapped defaults)
- Pro forma growth rates (provide industry/historical basis)
- Collateral advance rates (provide standard rates)

### USE DEFAULT, FLAG IN MEMO:
- Funding costs (bank standard)
- Operating cost assumptions (bank standard)
- Tax rates (statutory or historical)
- Working capital cycle (historical)
- Depreciation lives (standard by asset class)

### CHECKPOINT MOMENTS:
1. After initial interview → Completeness check
2. After structure proposed → Confirm terms
3. After pro forma built → Validate assumptions
4. After risk assessment → Confirm rating
5. After RAROC → Validate pricing
6. After covenant package → Confirm terms
7. Before final generation → Full review

### RED FLAGS TO SURFACE IMMEDIATELY:
- DSCR below 1.25x
- Going concern in last 2 years
- Negative equity
- Customer concentration > 25%
- Single facility risk
- Covenant violations (current or recent)
- Fraud or character issues in background
- Related party transactions
