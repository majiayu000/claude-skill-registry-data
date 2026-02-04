---
name: fia-product-analyzer
description: Comprehensive analysis framework for Fixed Indexed Annuities (FIAs). Use when analyzing, comparing, or evaluating FIA products including surrender charges, index options, crediting methods, riders, commissions, and suitability. Creates detailed product profiles with 40-question suitability assessments and LLM-friendly scoring methodology. Use for internal product analysis, client suitability determination, or when building product comparison documents.
---

# Fixed Indexed Annuity Product Analyzer

This skill provides a complete framework for analyzing fixed indexed annuities (FIAs), creating comprehensive product profiles, and determining client suitability through structured assessment.

## When to Use This Skill

Use this skill when:
- Analyzing a specific FIA product (e.g., "Analyze the Allianz Benefit Control FIA")
- Creating product comparison documents
- Determining if an FIA is suitable for a prospect/client
- Building internal product knowledge base
- Evaluating product features, rates, and structures
- Running suitability assessments with incomplete client data

## Core Workflow

### Step 1: Data Collection

Gather comprehensive product information across these categories:

**Essential Data Points:**
1. **Basic Product Information**
   - Product name and issuer
   - Product type (FIA, RILA, etc.)
   - Contract term/surrender period
   - Minimum premium requirements
   - Premium payment options

2. **Surrender Charges & Fees**
   - Surrender charge schedule (by year)
   - Market Value Adjustment (MVA) provisions
   - Allocation charges (current and maximum)
   - Rider fees (if applicable)
   - Free withdrawal provisions

3. **Index Options**
   - All available indexes with descriptions
   - Index characteristics (volatility-controlled, diversified, etc.)
   - Affiliated indexes (note relationships like PIMCO-Allianz)

4. **Crediting Methods**
   - Annual point-to-point (cap/participation rate)
   - Multi-year point-to-point options
   - Monthly averaging/sum options
   - Fixed rate allocation
   - Minimum guaranteed rates

5. **Current Rates** (if available)
   - Caps by index and crediting method
   - Participation rates by index and crediting method
   - Fixed interest rates
   - Note: Rates change frequently - always include disclaimer

6. **Riders & Benefits**
   - Built-in riders (no cost)
   - Optional riders (with costs)
   - Lifetime income provisions
   - Long-term care benefits
   - Death benefits
   - Withdrawal percentages by age

7. **Special Features**
   - Unique product differentiators
   - Bonus structures
   - Index lock capabilities
   - Other innovative features

8. **Commission Structure**
   - Typical commission ranges
   - Industry standards for similar products

9. **Company Information**
   - Issuing company name
   - Parent company (if applicable)
   - Financial strength ratings
   - Years in business
   - Market position

**Data Collection Methods:**
- Use web_search for current product information
- Use web_fetch to retrieve full product pages and rate sheets
- Search for: "[product name] rates features", "[product name] surrender charges", "[product name] index options"
- Always verify information from multiple sources when possible

### Step 2: Document Creation

Create two output formats:

#### A. Markdown Document (LLM-Friendly)
Structure the analysis as follows:

```markdown
# [Product Name] Fixed Indexed Annuity
## Product Analysis & Suitability Assessment

---

## Executive Summary
[Brief overview - 2-3 paragraphs covering product type, target audience, key features]

## Product Overview
### Core Product Features
[Bullet points of main features]

### Premium Structure
[Initial premium, additional premiums, payment options]

---

## Detailed Data Points

### Surrender Charges & Fees
[Table with year-by-year surrender charges]
[Additional fees: allocation charges, MVA, rider fees]
[Free withdrawal provisions]

### Index Options
[Numbered list with each index: name, description, crediting methods, characteristics]

### Crediting Methods
[Description of each method type with how it works, limitations, advantages]

### Special Features
[Unique features like Index Lock, bonus structures, etc.]

### Riders & Benefits
**Built-In Riders (No Additional Cost)**
[List each with details]

**Optional Riders (Additional Cost)**
[List each with costs and details]

### Lifetime Withdrawal Provisions
[Table with withdrawal percentages by age for single/joint life]

### Commission Structure
[Typical ranges and industry standards]

### Death Benefits
[Standard and alternative death benefit structures]

### Tax Considerations
[Tax advantages, liabilities, qualification status]

### Realistic Return Expectations
[Conservative estimates with factors affecting returns]

---

## Suitability Analysis

### Who This Product Is a GOOD FIT For
[8-10 categories with specific characteristics under each]

### Who This Product Is NOT a GOOD FIT For
[8-10 categories with specific disqualifying characteristics]

---

## Suitability Questionnaire for LLM Analysis

### Instructions for LLM Use
**Answering Questions:**
- Answer YES or NO to each question based on available prospect/client data
- If insufficient data exists to answer a specific question, mark it as "UNABLE TO ANSWER" or "N/A"
- **Important:** Only include questions you CAN answer in the scoring calculation

**Scoring Formula:**
```
Suitability Score = (Total YES answers ÷ Total Answerable Questions) × 100
```

**Where:**
- Total YES answers = Count of questions answered YES
- Total Answerable Questions = Count of questions answered YES or NO (excludes N/A)

**Scoring Interpretation:**
- 80-100%: Highly Suitable
- 60-79%: Suitable (with discussion of concerns)
- 40-59%: Marginal Fit (detailed discussion required)
- Below 40%: Not Suitable

### Questionnaire (40 Questions)

**Financial Capacity & Commitment (5 questions)**
1. Does the client have at least [minimum premium] available to invest?
   - YES / NO / N/A
2. Can the client commit these funds for at least [contract term] years?
   - YES / NO / N/A
3. Does the client have adequate emergency funds (3-6 months expenses) outside this investment?
   - YES / NO / N/A
4. Will this annuity represent less than 50% of the client's total investable assets?
   - YES / NO / N/A
5. Can the client afford surrender charges if early access is needed?
   - YES / NO / N/A

**Age & Time Horizon (3 questions)**
6. Is the client at or above minimum age for income withdrawals?
   - YES / NO / N/A
7. Is the client in the optimal age range for this product?
   - YES / NO / N/A
8. Does the client expect to live long enough to benefit from lifetime income?
   - YES / NO / N/A

**Investment Objectives (5 questions)**
9. Is the client's primary goal retirement income (rather than accumulation)?
   - YES / NO / N/A
10. Is the client seeking principal protection from market downturns?
    - YES / NO / N/A
11. Is the client comfortable with expected returns in the realistic range?
    - YES / NO / N/A
12. Is the client seeking tax-deferred growth?
    - YES / NO / N/A
13. Does the client want guaranteed lifetime income?
    - YES / NO / N/A

**Risk Tolerance (4 questions)**
14. Would the client describe their risk tolerance as conservative or moderate?
    - YES / NO / N/A
15. Is the client uncomfortable with stock market volatility?
    - YES / NO / N/A
16. Does the client prioritize safety over maximum growth?
    - YES / NO / N/A
17. Is the client willing to accept limited upside in exchange for downside protection?
    - YES / NO / N/A

**Liquidity Needs (3 questions)**
18. Does the client NOT anticipate needing large lump-sum withdrawals?
    - YES / NO / N/A
19. Is the client comfortable with structured lifetime withdrawal percentages?
    - YES / NO / N/A
20. Does the client have other liquid assets for unexpected expenses?
    - YES / NO / N/A

**Understanding & Complexity (4 questions)**
21. Does the client understand this is NOT a direct market investment?
    - YES / NO / N/A
22. Is the client comfortable with complexity of multiple index options?
    - YES / NO / N/A
23. Does the client understand bonus/income value limitations?
    - YES / NO / N/A
24. Does the client understand surrender charges and fees?
    - YES / NO / N/A

**Health & Long-Term Care (3 questions)**
25. Is the client in good health with no immediate terminal diagnoses?
    - YES / NO / N/A
26. Does the client value long-term care benefits (if applicable)?
    - YES / NO / N/A
27. Is the client concerned about outliving their assets?
    - YES / NO / N/A

**Tax Situation (3 questions)**
28. Will the client benefit from tax-deferred growth?
    - YES / NO / N/A
29. Does the client understand tax treatment of withdrawals?
    - YES / NO / N/A
30. If under 59½, is client willing to wait or accept early withdrawal penalty?
    - YES / NO / N/A

**Alternative Options (3 questions)**
31. Has the client rejected direct stock investing due to risk concerns?
    - YES / NO / N/A
32. Has the client compared this to alternatives (MYGAs, SPIAs, other FIAs)?
    - YES / NO / N/A
33. Does the client understand commission structure and potential conflicts?
    - YES / NO / N/A

**Specific Product Features (4 questions)**
34. Is the client interested in product-specific unique features?
    - YES / NO / N/A
35. Does the client want flexibility in income start timing?
    - YES / NO / N/A
36. Is the client attracted to bonus features (if applicable)?
    - YES / NO / N/A
37. Does the client value combination of accumulation and income features?
    - YES / NO / N/A

**Disqualifying Factors (3 questions)**
38. Does the client NOT need aggressive growth (8-10%+ annually)?
    - YES / NO / N/A
39. Is the client NOT planning major purchases requiring lump sums in near term?
    - YES / NO / N/A
40. Does the client NOT view this as their entire retirement portfolio?
    - YES / NO / N/A

---

## Score Interpretation & Recommendations

**90-100% (Highly Suitable)**
- Strong alignment with product features
- Proceed with application
- Discuss specific allocation selections

**75-89% (Suitable)**
- Good overall fit with minor concerns
- Address any NO answers before proceeding
- Ensure client fully understands limitations

**60-74% (Moderately Suitable)**
- Mixed fit - significant considerations required
- Deep dive into NO answers
- Explore alternative products
- Only proceed if concerns resolved

**40-59% (Marginal/Not Suitable)**
- More NO than YES answers
- Significant misalignment
- Recommend alternatives
- Should NOT proceed without major changes

**Below 40% (Not Suitable)**
- Strong misalignment
- Do NOT recommend this product
- Explore other options
- Document reasons for non-recommendation

---

## Critical Considerations

### Important Disclosures
[Standard disclosures: not bank products, guarantees, index performance, complexity]

### Company Information
[Issuer details, financial strength, contact information]

### Summary Recommendation Framework
**Proceed with Confidence If:** [criteria list]
**Proceed with Caution If:** [criteria list]
**Do NOT Proceed If:** [criteria list]

---

## Document Version & Updates
**Document Created:** [Date]
**Product Information Current As Of:** [Date]
**Important:** Rates and features subject to change. Always verify current information.

---

## Disclaimer
This analysis is for informational and internal use only. Not a prospectus or offering document. Verify all information with current product materials. Consult licensed professionals for advice.

---
```

#### B. PDF Document (Professional Format)
Use reportlab to create formatted PDF with:
- Title page with product name and key details
- Table of contents (optional for longer documents)
- Professional styling (consistent fonts, colors, headers)
- Tables for surrender charges and withdrawal percentages
- Clear section breaks
- Page numbers
- Company branding (if applicable)

**PDF Creation Example:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Define custom styles for consistency
title_style = ParagraphStyle('CustomTitle', fontSize=24, textColor=colors.HexColor('#003366'))
heading1_style = ParagraphStyle('CustomHeading1', fontSize=16, textColor=colors.HexColor('#003366'))
# ... etc

# Create document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)
story = []

# Build content
story.append(Paragraph("Product Name", title_style))
# ... add all content sections

doc.build(story)
```

### Step 3: Output Delivery

1. **Save both formats** to `/mnt/user-data/outputs/`:
   - Markdown: `[product_name]_analysis.md`
   - PDF: `[product_name]_analysis.pdf`

2. **Provide links** to both files:
   - [View Markdown](computer:///mnt/user-data/outputs/[product_name]_analysis.md)
   - [View PDF](computer:///mnt/user-data/outputs/[product_name]_analysis.pdf)

3. **Brief summary** of findings (2-3 sentences)

## Best Practices

### Data Quality
- **Always search for current rates** - they change frequently
- **Verify from multiple sources** when possible
- **Include disclaimers** about rate changes
- **Note data limitations** when information is unavailable

### Suitability Assessment
- **Be objective** - present both pros and cons
- **Consider the whole profile** - not just one factor
- **Explain reasoning** in good/not good fit sections
- **Account for missing data** - use N/A scoring properly

### Documentation
- **Be comprehensive but concise** - avoid unnecessary repetition
- **Use tables for numerical data** - easier to scan
- **Include examples** - especially for complex features
- **Provide context** - explain industry norms and comparisons

### LLM-Friendly Formatting
- **Markdown structure** - clear hierarchy with headers
- **Consistent formatting** - makes parsing easier
- **Explicit instructions** - don't assume understanding
- **Scoring methodology** - detailed and unambiguous

## Common Pitfalls to Avoid

❌ **Don't:**
- Make up rates or data points
- Guarantee future performance
- Ignore surrender charges or fees
- Oversimplify complex features
- Score without adequate data
- Copy marketing language verbatim
- Recommend without understanding client needs

✅ **Do:**
- State when data is unavailable
- Emphasize realistic expectations
- Highlight all fees and charges
- Explain features in plain language
- Use N/A for missing data points
- Provide balanced analysis
- Focus on suitability match

## Product-Specific Adaptations

While the framework is standard, adapt these elements for each product:

1. **Questionnaire customization**
   - Adjust age ranges based on product minimums
   - Include/exclude questions based on available features
   - Modify dollar amounts for premium requirements

2. **Good/Not Good Fit categories**
   - Emphasize product-specific strengths
   - Highlight unique disqualifiers
   - Match to target market

3. **Special features section**
   - Focus on differentiators
   - Explain proprietary features
   - Compare to industry norms

## Example Usage

**User Request:** "Analyze the Nationwide Peak 10 FIA for me"

**Response Flow:**
1. Search for Nationwide Peak 10 product information
2. Gather surrender charges, index options, crediting methods, riders
3. Create markdown document with all sections
4. Generate professional PDF
5. Output both files to `/mnt/user-data/outputs/`
6. Provide links and brief summary

## Handling Incomplete Information

When data is unavailable:

1. **In the document:**
   - Note: "Current rates not publicly available - contact issuer"
   - State: "Information on [feature] could not be verified"
   - Include: "As of [date], the following information was available..."

2. **In scoring:**
   - Questions without data are marked N/A
   - Only answerable questions count in denominator
   - Document lists which questions couldn't be answered

3. **In recommendations:**
   - Acknowledge limitations
   - Suggest additional research needed
   - Recommend verification with licensed professional

## Skill Output Quality Standards

A complete analysis should include:

✅ All major sections populated with data
✅ At least 6 index options documented (or all available)
✅ Full 10+ year surrender charge schedule
✅ 40-question suitability assessment
✅ Both markdown and PDF formats
✅ Realistic return expectations stated
✅ Critical disclosures included
✅ Professional formatting and styling
✅ Links provided to user
✅ Clear scoring methodology explained

## Updates and Maintenance

This skill framework should be updated when:
- Industry standards change significantly
- New product types emerge (e.g., new hybrid structures)
- Regulatory requirements affect disclosures
- User feedback suggests improvements
- Common data sources become unavailable

---

**Remember:** The goal is to provide objective, comprehensive analysis that helps determine product-client fit while being transparent about limitations, fees, and realistic expectations.
