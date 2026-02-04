---
name: higher-ed-fred-analysis
description: "Create sophisticated economic data analyses and visualizations for higher education stakeholders using FRED (Federal Reserve Economic Data). Use this skill when users request: (1) Analysis of student loan debt, unemployment by education level, or earnings data, (2) Dashboard or visual presentations of higher ed economic indicators, (3) Narrative reports on higher education ROI or economic value, (4) Data-driven communications for institutional stakeholders (trustees, enrollment management, financial aid offices), or (5) Integration of FRED API data into interactive visualizations."
---

# Higher Education FRED Analysis

Create data-driven analyses and visualizations of higher education economic indicators using the Federal Reserve Economic Data (FRED) API.

## Overview

This skill enables creation of professional, evidence-based economic analyses for higher education institutions. It combines FRED API data access, sophisticated visual design, and stakeholder-focused narrative frameworks to produce compelling dashboards and reports about student debt, employment outcomes, and earnings differentials by educational attainment.

## Core Workflow

### 1. Determine Analysis Type

**Interactive Dashboard**: Use when stakeholders need real-time, explorable data visualizations
**Narrative Report**: Use when stakeholders need written analysis with supporting data
**Combined Approach**: Most effective for comprehensive stakeholder communications

### 2. Identify Relevant FRED Series

Read `references/fred-series-guide.md` for complete catalog. Common series:
- **Student Debt**: SLOAS (Student Loans Owned and Securitized)
- **Unemployment by Education**: LNS14027662 (Bachelor's+), LNS14027660 (HS), LNS14027659 (No HS)
- **Earnings by Education**: LEU0252918500A (Bachelor's+), LEU0252917300A (HS only)

### 3. Fetch and Process Data

Use `scripts/fetch_fred_data.py` for consistent data retrieval with error handling:
```bash
python scripts/fetch_fred_data.py --series SLOAS LNS14027662 --api-key YOUR_KEY
```

Or implement in-artifact fetching for interactive dashboards (see template).

### 4. Create Visualizations

**For interactive dashboards**: 
- Copy and customize `assets/dashboard-template.html`
- Implements React + Chart.js with FRED API integration
- Includes CORS proxy pattern for client-side POCs

**For narrative reports**: 
- Follow structure in `references/narrative-templates.md`
- Integrate visualizations as needed

Apply consistent design system from `references/design-system.md`:
- Dark sophisticated theme (primary: #1a2332, accent: #d4af37)
- Typography: Playfair Display (headers), IBM Plex Mono (data), Inter (body)
- Chart styling configurations provided

### 5. Craft Stakeholder-Appropriate Narratives

Read `references/stakeholder-personas.md` for audience-specific strategies. Match tone and depth to audience:
- **Trustees/Board**: Executive summary focus, strategic implications
- **Financial Aid**: Debt contextualization, ROI analysis
- **Enrollment Management**: Student recruitment value propositions
- **Faculty/Academic Affairs**: Discipline-specific outcomes when possible

## Key Principles

**Evidence-Based**: Ground all claims in FRED data with proper attribution and source citations
**Context-Rich**: Never present debt/cost data without employment/earnings context - the ROI story matters
**Balanced**: Acknowledge limitations (correlation ≠ causation, individual variation, field differences)
**Actionable**: Conclude with strategic implications for institutional decision-making

## Common Analysis Patterns

**ROI Analysis**: Combine debt (SLOAS), unemployment (LNS series), and earnings (LEU series) data to show net value
**Trend Analysis**: Use 5-10 year windows for meaningful trend identification; avoid cherry-picking
**Comparative Analysis**: Always show education level differentials, not absolute values alone
**Crisis Impact**: Layer recession periods (2008, 2020) to highlight higher ed's stabilizing effect

## Technical Notes

### FRED API Access
- Requires free registration at research.stlouisfed.org
- Rate limits: 120 requests per minute
- Returns JSON observations with dates and values
- Handle "." values (missing data) gracefully

### Implementation Approaches
- **Client-side (POC)**: Use CORS proxy (corsproxy.io) - note security limitations
- **Production**: Backend API calls recommended for key management and caching
- **Hybrid**: Client-side with pre-fetched data embedded in artifact

### Data Update Frequencies
- Unemployment: Monthly
- Earnings: Annual
- Student Debt: Quarterly
- Plan analysis refresh cycles accordingly

### Important Considerations
- All monetary values are nominal; consider CPI adjustments for multi-decade comparisons
- Seasonal adjustments vary by series; check FRED metadata
- Education categories may not align perfectly across different BLS surveys

## Bundled Resources

### Scripts
- `scripts/fetch_fred_data.py` - Python utility for fetching FRED data with error handling and caching

### References
- `references/fred-series-guide.md` - Comprehensive catalog of higher ed relevant FRED series
- `references/design-system.md` - Visual design specifications and Chart.js configurations
- `references/narrative-templates.md` - Report structures and writing guidelines
- `references/stakeholder-personas.md` - Audience-specific communication strategies

### Assets
- `assets/dashboard-template.html` - Complete React dashboard boilerplate with FRED API integration
