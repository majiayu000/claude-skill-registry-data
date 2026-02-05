---
name: dashboard-auto-generation-client
description: Generate professional, client-ready dashboards from data files with clean design (no CURV branding). Detects patterns, creates visualizations, provides insights. Perfect for client presentations and professional reporting.
---

# Dashboard Auto-Generation (Client Edition)

## Core Principle

**Show first, refine later.** Never ask "what do you want to see?" - analyze the data, detect patterns, and build a professional dashboard immediately.

**Client-Ready Design:** Clean, professional styling with neutral colors and universal branding. No CURV-specific elements. Ready to share directly with clients.

## When to Activate

Activate this skill when user:
- Uploads a data file (CSV, Excel, JSON, TSV)
- Says "analyze this data"
- Asks for a "dashboard" or "report"
- Wants to "visualize" or "understand" data
- Mentions PPC, sales, analytics, or business metrics
- Requests "client-friendly" or "professional" dashboard
- Wants to share analysis with external stakeholders

**Do NOT ask questions** - just build the best dashboard you can from the data.

## Modern Design System (Actual n8n Tokens)

### CRITICAL: Complete CSS Variables (Copy Exactly)

**Every dashboard MUST start with these exact n8n design tokens in the `<style>` tag:**

```css
:root {
  /* n8n colors - extracted from n8n.io */
  --color-crow: rgba(25, 9, 24, 0.94);
  --color-dr--white: rgba(250, 249, 251, 0.75);
  --color-new-love: rgb(196, 187, 211);
  --color-ink-black: rgba(31, 25, 42, 0.7);
  --color-ink-black-2: rgba(31, 25, 42, 0.5);
  --color-ink-black-3: rgba(31, 25, 42, 0.3);
  --color-ink-black-4: rgb(31, 25, 42);
  --color-white: rgba(255, 255, 255, 0.16);
  --color-white-2: rgba(255, 255, 255, 0.1);
  --color-white-3: rgba(255, 255, 255, 0.3);
  --color-white-4: rgb(255, 255, 255);
  --color-white-5: rgba(255, 255, 255, 0.8);
  --color-white-6: rgba(255, 255, 255, 0.93);
  --color-narwhale-grey: rgba(12, 8, 28, 0.43);
  --color-narwhale-grey-2: rgba(13, 10, 25, 0.28);
  --color-narwhale-grey-3: rgb(14, 9, 24);

  /* n8n typography */
  --font-family: geomanist, ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --font-family-book: geomanist-book, ui-sans-serif, system-ui, sans-serif;

  /* n8n spacing */
  --vspace-sm: 0.5rem;
  --vspace-md: 1rem;
  --vspace-lg: 1.5rem;
  --vspace-xl: 2rem;
  --vspace-xxl: 3rem;

  --hspace-sm: 0.5rem;
  --hspace-md: 1rem;
  --hspace-lg: 1.5rem;
  --hspace-xl: 2rem;

  /* n8n border radii */
  --border-radius-sm: 8px;
  --border-radius-md: 16px;
  --border-radius-lg: 20px;
  --border-radius-xl: 1.5rem;

  /* n8n shadows - glassmorphic effects */
  --shadow-card: rgba(255, 255, 255, 0.05) 0px 4px 12px 0px inset, rgba(0, 0, 0, 0.23) 0px 4px 16px -8px;
  --shadow-card-hover: rgb(196, 187, 211) 0px 0px inset, rgba(14, 9, 24, 0.44) 0px 4px 4px, rgb(0, 0, 0) 0px 13px 16px -8px, rgba(255, 255, 255, 0.05) 0px 4px 12px inset;
  --shadow-glow: rgba(196, 187, 211, 0.3) 0px 0px 20px;
}
```

### Base Styles Using n8n Tokens

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    background: var(--color-narwhale-grey-3);
    color: var(--color-white-4);
    line-height: 1.6;
    padding: var(--vspace-xl);
    min-height: 100vh;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
}

h1, h2, h3 {
    font-family: var(--font-family-book);
    font-weight: 500;
}

.dashboard-title {
    font-size: 54px;
    font-weight: 500;
    color: var(--color-white-4);
    letter-spacing: -2px;
    line-height: 54px;
}

.metric-value {
    font-size: 48px;
    font-weight: 500;
    color: var(--color-new-love);
    line-height: 1;
}

.metric-label {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--color-dr--white);
    font-weight: 400;
}
```

### Header (Modern n8n-Style)

```html
<!-- ========== MODERN GRADIENT HEADER ========== -->
<header class="modern-header">
    <div class="header-background"></div>
    <div class="header-content">
        <h1 class="dashboard-title">[Dashboard Name]</h1>
        <p class="dashboard-subtitle">[Description of data - e.g., "30-Day Performance Analysis | Aug 11 - Sep 9, 2025"]</p>
        <p class="dashboard-metadata">Generated: [Date] | [Data Point Count] records analyzed</p>
    </div>
</header>
```

**Required CSS for Header (Using n8n Tokens):**
```css
.modern-header {
    text-align: center;
    margin-bottom: var(--vspace-xxl);
    padding: var(--vspace-xxl) var(--hspace-xl);
    background: var(--color-ink-black);
    border-radius: var(--border-radius-lg);
    position: relative;
    overflow: hidden;
    border: 1px solid var(--color-ink-black-3);
    box-shadow: var(--shadow-card);
}

.header-background {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, var(--color-narwhale-grey) 0%, transparent 70%);
    animation: pulseGlow 8s ease-in-out infinite;
}

@keyframes pulseGlow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.1); }
}

.header-content {
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}

.dashboard-title {
    font-size: 54px;
    font-weight: 500;
    color: var(--color-white-4);
    letter-spacing: -2px;
    margin: 0 0 var(--vspace-md) 0;
    line-height: 54px;
}

.dashboard-subtitle {
    font-size: 20px;
    color: var(--color-white-5);
    margin: 0 0 var(--vspace-sm) 0;
    font-weight: 400;
    line-height: 30px;
}

.dashboard-metadata {
    font-size: 14px;
    color: var(--color-dr--white);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 400;
}

/* Responsive header */
@media (max-width: 768px) {
    .modern-header { padding: var(--vspace-xl) var(--hspace-lg); }
    .dashboard-title { font-size: 36px; line-height: 36px; }
    .dashboard-subtitle { font-size: 16px; }
}
```

### Footer (Modern Design)

```html
<!-- ========== MODERN FOOTER ========== -->
<footer class="modern-footer">
    <div class="footer-content">
        <p class="footer-credits">Produced By Danny McMillan | A Seller Sessions Production | &copy; 2025</p>
    </div>
</footer>
```

**Required CSS for Footer (Using n8n Tokens):**
```css
.modern-footer {
    text-align: center;
    padding: var(--vspace-xl) var(--hspace-lg);
    margin-top: var(--vspace-xxl);
    border-top: 1px solid var(--color-ink-black-3);
    background: var(--color-ink-black-2);
}

.footer-content {
    max-width: 900px;
    margin: 0 auto;
}

.footer-credits {
    font-size: 14px;
    color: var(--color-dr--white);
    margin: 0;
    letter-spacing: 0.04em;
    font-weight: 400;
    line-height: 21px;
}
```

### Panel Design (Glassmorphic Cards - n8n Style)

```css
.panel {
    background: var(--color-ink-black);
    backdrop-filter: blur(20px);
    border: 1px solid var(--color-ink-black-3);
    border-radius: var(--border-radius-lg);
    padding: var(--hspace-xl);
    box-shadow: var(--shadow-card);
    transition: box-shadow 0.5s ease, border-color 0.5s ease, transform 0.3s ease;
    position: relative;
    overflow: hidden;
}

.panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--color-new-love), transparent);
    opacity: 0.3;
}

.panel:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-card-hover);
    border-color: var(--color-new-love);
}
```

### Button Styles (Professional)

```css
.btn-primary {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 32px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(37, 99, 235, 0.25);
}

.btn-outline {
    background: transparent;
    color: #2563eb;
    border: 2px solid #2563eb;
    border-radius: 8px;
    padding: 10px 28px;
}
```

### Tab Navigation (Modern n8n Style)

```html
<div class="tab-nav">
    <button class="tab active">OVERVIEW</button>
    <button class="tab">EXPLORER</button>
    <button class="tab">FUNNEL</button>
    <button class="tab">INSIGHTS</button>
</div>
```

**Tab Styling (Using n8n Tokens):**
```css
.tab-nav {
    display: flex;
    gap: var(--hspace-sm);
    margin-bottom: var(--vspace-xl);
    padding: var(--hspace-sm);
    background: var(--color-ink-black-2);
    border-radius: var(--border-radius-md);
    border: 1px solid var(--color-ink-black-3);
}

.tab {
    background: transparent;
    color: var(--color-dr--white);
    border: none;
    border-radius: var(--border-radius-sm);
    padding: var(--vspace-md) var(--hspace-lg);
    font-size: 14px;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: box-shadow 0.5s ease, border-color 0.5s ease, background 0.3s ease;
    position: relative;
    line-height: 21px;
}

.tab.active {
    color: var(--color-white-4);
    background: var(--color-ink-black);
    border: 1px solid var(--color-new-love);
    box-shadow: var(--shadow-glow);
}

.tab:hover:not(.active) {
    color: var(--color-white-5);
    background: var(--color-white-2);
}
```

## Auto-Detection Patterns

### 1. PPC / Advertising Data

**Detect columns like:**
- Placement, Campaign, Ad Group, Keyword, Search Term
- Impressions, Clicks, Spend, Cost Per Click (CPC)
- Sales, Revenue, ROAS, ACOS, CTR, Conversion Rate
- Orders, Units, Add-to-Cart, Cart Adds

**Auto-generate tabs:**
1. **OVERVIEW** - 6 key metrics + top performers table
2. **EXPLORER** - Searchable/filterable table with all campaigns/keywords
3. **FUNNEL** - Impressions → Clicks → Cart Adds → Purchases (with CVR)
4. **INSIGHTS** - Key findings, opportunities, recommendations

### 2. Sales / E-commerce Data

**Detect columns like:**
- Date, Product, SKU, Category, ASIN
- Units, Revenue, Profit, Price
- Orders, Customers, Sessions
- Returns, Refunds

**Auto-generate tabs:**
1. **OVERVIEW** - Revenue, units, AOV, profit metrics
2. **EXPLORER** - Product performance table with filters
3. **FUNNEL** - Sessions → Views → Cart → Purchase (if session data)
4. **INSIGHTS** - Low stock, high return rate, underperformers

### 3. Analytics / Traffic Data

**Detect columns like:**
- Date, Source, Medium, Campaign, Keyword
- Sessions, Users, Pageviews, Bounce Rate
- Conversion Rate, Goal Completions, Events
- Avg Session Duration, Pages per Session

**Auto-generate tabs:**
1. **OVERVIEW** - Sessions, users, CVR, bounce rate
2. **EXPLORER** - Source/medium breakdown with filters
3. **FUNNEL** - Landing → Engagement → Conversion
4. **INSIGHTS** - High bounce sources, conversion opportunities

### 4. Financial / Business Data

**Detect columns like:**
- Date, Account, Category, Transaction Type
- Amount, Debit, Credit, Balance
- Vendor, Customer, Invoice

**Auto-generate tabs:**
1. **OVERVIEW** - Total income, expenses, profit, cash flow
2. **EXPLORER** - Transaction table with filters
3. **NO FUNNEL** - Not applicable
4. **INSIGHTS** - Top expenses, late invoices, cash flow issues

## Tab System (When to Use)

### Use Tabs When:
- Dataset has >100 rows (need explorer for search/filter)
- Data supports funnel visualization (impressions→clicks→conversions)
- Multiple insight types exist (opportunities, trends, recommendations)

### Single Page When:
- Dataset <50 rows (all fits on overview)
- Simple report with few metrics
- No funnel or exploration needed

## Overview Tab (Always Required)

### Structure:
1. **Performance Summary Section** (4-6 large metric cards)
2. **Top Performers Table** (top 10 by primary metric)
3. **Key Insights Section** (3-5 bullet points)

### Metric Cards (Modern n8n Style - 3 Columns):

```html
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-content">
            <p class="metric-label">IMPRESSIONS</p>
            <p class="metric-value">50.9K</p>
            <p class="metric-detail">Brand share: 1.8%</p>
        </div>
        <div class="metric-footer">
            <span class="percentage positive">+12.5%</span>
            <span class="period">vs last period</span>
        </div>
    </div>
    <!-- Repeat for other metrics -->
</div>
```

**Metric Card Styling (3 Equal Columns - Using n8n Tokens):**
```css
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* EXACTLY 3 columns, equal width */
    gap: var(--hspace-lg);
    margin-bottom: var(--vspace-xxl);
}

@media (max-width: 1024px) {
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);  /* 2 columns on tablets */
    }
}

@media (max-width: 640px) {
    .metrics-grid {
        grid-template-columns: 1fr;  /* 1 column on mobile */
    }
}

.metric-card {
    background: var(--color-ink-black);
    backdrop-filter: blur(20px);
    border: 1px solid var(--color-ink-black-3);
    border-radius: var(--border-radius-lg);
    padding: var(--hspace-xl);
    box-shadow: var(--shadow-card);
    transition: box-shadow 0.5s ease, border-color 0.5s ease, transform 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--color-new-love), transparent);
    opacity: 0.4;
}

.metric-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-card-hover);
    border-color: var(--color-new-love);
}

.metric-content {
    margin-bottom: var(--vspace-lg);
}

.metric-label {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--color-dr--white);
    font-weight: 400;
    margin-bottom: var(--vspace-sm);
    line-height: 21px;
}

.metric-value {
    font-size: 48px;
    font-weight: 500;
    color: var(--color-new-love);
    margin: var(--vspace-sm) 0;
    line-height: 48px;
}

.metric-detail {
    font-size: 14px;
    color: var(--color-dr--white);
    margin-top: var(--vspace-sm);
    line-height: 21px;
}

.metric-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: var(--vspace-lg);
    border-top: 1px solid var(--color-ink-black-3);
}

.percentage {
    font-size: 14px;
    font-weight: 400;
    padding: var(--vspace-1) var(--hspace-sm);
    border-radius: var(--border-radius-sm);
    line-height: 21px;
}

.percentage.positive {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
}

.percentage.negative {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
}

.period {
    font-size: 14px;
    color: var(--color-white-3);
    font-weight: 400;
    line-height: 21px;
}
```

## Explorer Tab (When >100 Rows)

### Structure:
1. **Search Bar** (filter across all text columns)
2. **Performance Legend** (color-coded badges)
3. **Sortable Table** (click headers to sort)
4. **Pagination** (10/20/50 per page)

### Search Implementation:

```html
<div class="explorer-controls">
    <input type="text" id="search-input" placeholder="Search..." class="search-input">
    <select id="per-page" class="per-page-select">
        <option value="10">10 per page</option>
        <option value="20">20 per page</option>
        <option value="50">50 per page</option>
    </select>
    <span class="results-count">Showing <strong id="count">0</strong> results</span>
</div>
```

### Professional Table Design:

```css
.data-table {
    width: 100%;
    border-collapse: collapse;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.data-table thead {
    background: linear-gradient(135deg, #f8f9fa, #e5e7eb);
}

.data-table th {
    padding: 16px;
    text-align: left;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6b7280;
    font-weight: 700;
    border-bottom: 2px solid #2563eb;
}

.data-table td {
    padding: 16px;
    border-bottom: 1px solid #e5e7eb;
    color: #1f2937;
}

.data-table tr:hover {
    background: #f8f9fa;
}

.data-table th.sortable {
    cursor: pointer;
    user-select: none;
}

.data-table th.sortable:hover {
    color: #2563eb;
}
```

### Performance Badges (Professional):

```css
.badge {
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge.excellent {
    background: #d1fae5;
    color: #065f46;
}

.badge.good {
    background: #fef3c7;
    color: #92400e;
}

.badge.needs-work {
    background: #fee2e2;
    color: #991b1b;
}
```

## Funnel Tab (When Funnel Data Exists)

### When to Create Funnel:
**PPC Data:** Impressions → Clicks → Cart Adds → Purchases
**E-commerce:** Sessions → Views → Cart → Purchase
**Analytics:** Landing → Engagement → Goal Completion
**Support:** New → In Progress → Resolved

### Professional Funnel Visualization:

```html
<div class="funnel-container">
    <h2 class="funnel-title">Conversion Funnel Analysis</h2>
    <p class="funnel-subtitle">Track customer journey and identify conversion bottlenecks</p>

    <div class="funnel-visual">
        <!-- Stage 1 -->
        <div class="funnel-stage" style="width: 100%;">
            <div class="stage-header">
                <span class="stage-icon">👁️</span>
                <span class="stage-name">Impressions</span>
            </div>
            <div class="stage-metric">50,900</div>
            <div class="stage-detail">Starting point</div>
        </div>

        <!-- Drop-off -->
        <div class="funnel-drop">
            <span class="drop-rate">-94.9%</span>
            <div class="drop-arrow">↓</div>
        </div>

        <!-- Stage 2 -->
        <div class="funnel-stage" style="width: 85%;">
            <div class="stage-header">
                <span class="stage-icon">🖱️</span>
                <span class="stage-name">Clicks</span>
            </div>
            <div class="stage-metric">2,600</div>
            <div class="stage-detail">
                <span class="cvr">5.1% CVR</span>
            </div>
        </div>
        <!-- Continue for all stages -->
    </div>

    <div class="funnel-summary">
        <div class="summary-card">
            <p class="summary-value">0.62%</p>
            <p class="summary-label">Overall Conversion</p>
        </div>
        <div class="summary-card">
            <p class="summary-value alert">94.9%</p>
            <p class="summary-label">Largest Drop-off</p>
        </div>
        <div class="summary-card">
            <p class="summary-value">Impressions → Clicks</p>
            <p class="summary-label">Critical Stage</p>
        </div>
    </div>
</div>
```

**Professional Funnel Styling:**
```css
.funnel-visual {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    margin: 40px 0;
}

.funnel-stage {
    background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    border: 2px solid #2563eb;
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    transition: all 0.3s ease;
}

.funnel-stage:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);
}

.stage-metric {
    font-size: 36px;
    font-weight: 700;
    color: #1f2937;
    margin: 12px 0;
}

.funnel-drop {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 0;
}

.drop-rate {
    background: #fee2e2;
    color: #991b1b;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}

.cvr {
    background: #d1fae5;
    color: #065f46;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
```

## Insights Tab (Always Include)

### Structure:
1. **Key Findings** (3-5 bullet points with context)
2. **Opportunities** (sorted by impact)
3. **Recommendations** (actionable next steps)

### Professional Insight Cards:

```html
<div class="insights-section">
    <h2 class="section-title">📊 Key Findings</h2>
    <div class="insights-grid">
        <div class="insight-card success">
            <div class="insight-icon">✓</div>
            <div class="insight-content">
                <h3>Top Performing Segment</h3>
                <p class="insight-text">Product Pages deliver 5.84x ROAS vs 2.1x average</p>
                <p class="insight-recommendation">Recommendation: Increase budget allocation by 30%</p>
            </div>
        </div>
        <!-- More insights -->
    </div>
</div>
```

**Insight Card Styling:**
```css
.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.insight-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
}

.insight-card.success {
    border-left-color: #10b981;
}

.insight-card.warning {
    border-left-color: #f59e0b;
}

.insight-card.alert {
    border-left-color: #ef4444;
}

.insight-icon {
    font-size: 32px;
    margin-bottom: 16px;
}

.insight-text {
    font-size: 16px;
    color: #1f2937;
    margin-bottom: 12px;
    font-weight: 500;
}

.insight-recommendation {
    font-size: 14px;
    color: #6b7280;
    font-style: italic;
}
```

### Opportunity Cards (Professional):

```html
<div class="opportunities-section">
    <h2 class="section-title">💡 Opportunities</h2>
    <div class="opportunities-grid">
        <div class="opportunity-card high-impact">
            <div class="card-header">
                <span class="impact-badge high">HIGH IMPACT</span>
            </div>
            <h3 class="opportunity-title">Hidden Growth Potential</h3>
            <p class="opportunity-description">Low market share but high conversion rate</p>
            <div class="opportunity-metrics">
                <div class="metric-row">
                    <span>Impressions:</span>
                    <strong>15,420</strong>
                </div>
                <div class="metric-row">
                    <span>CVR:</span>
                    <strong class="positive">0.56%</strong>
                </div>
            </div>
            <button class="btn-outline">View Details</button>
        </div>
        <!-- More opportunities -->
    </div>
</div>
```

**Opportunity Styling:**
```css
.opportunity-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
}

.impact-badge {
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.impact-badge.high {
    background: #fee2e2;
    color: #991b1b;
}

.impact-badge.medium {
    background: #fef3c7;
    color: #92400e;
}

.impact-badge.low {
    background: #dbeafe;
    color: #1e40af;
}
```

## Search & Filter Implementation

```javascript
const searchInput = document.getElementById('search-input');
const tableBody = document.getElementById('table-body');
const resultsCount = document.getElementById('count');

searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = tableBody.querySelectorAll('tr');

    let visibleCount = 0;
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    resultsCount.textContent = visibleCount;
});
```

## Sortable Table Implementation

```javascript
document.querySelectorAll('.sortable').forEach(header => {
    header.addEventListener('click', () => {
        const column = header.getAttribute('data-column');
        const rows = Array.from(tableBody.querySelectorAll('tr'));
        const isAscending = header.classList.contains('asc');

        rows.sort((a, b) => {
            const aVal = a.querySelector(`[data-column="${column}"]`).textContent;
            const bVal = b.querySelector(`[data-column="${column}"]`).textContent;

            // Numeric sorting
            if (!isNaN(aVal) && !isNaN(bVal)) {
                return isAscending ? aVal - bVal : bVal - aVal;
            }
            // Text sorting
            return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });

        tableBody.innerHTML = '';
        rows.forEach(row => tableBody.appendChild(row));

        document.querySelectorAll('.sortable').forEach(h => h.classList.remove('asc', 'desc'));
        header.classList.add(isAscending ? 'desc' : 'asc');
    });
});
```

## File Naming Convention

```
[dashboard-name]-[client-name]-[date].html

Examples:
- performance-analysis-acme-corp-2025-10-19.html
- sales-dashboard-client-a-2025-10-19.html
- ppc-report-q4-2025-10-19.html
```

## Quality Gates

**Before delivering ANY client dashboard, verify:**

**MANDATORY Requirements:**
- Modern gradient header with pulsing glow animation
- Footer with exact text: "Produced By Danny McMillan | A Seller Sessions Production | © 2025"
- Responsive layout (mobile-friendly)
- All tabs functional (if multi-tab)
- Search and sort working in Explorer
- Color-coded performance indicators
- Modern n8n-inspired design (dark gradient background, purple/blue accents)
- 3 equal-width metric cards per row (grid-template-columns: repeat(3, 1fr))
- NO emoticons anywhere in the dashboard
- Glassmorphic cards with backdrop-filter blur

**⚠️ OUTPUT FORMAT:**
- Must be standalone HTML file
- Complete `<!DOCTYPE html>` with `<head>` and `<body>`
- All CSS in `<style>` tag
- All JavaScript in `<script>` tag
- Opens directly in browser without build tools

**Standard Quality:**
- Tab navigation (if >100 rows or funnel exists)
- Metric cards with icons
- Funnel visualization (if applicable)
- Insights with recommendations
- Search/filter functional
- Sortable table headers
- Professional badges (green/amber/red)
- Clean design throughout

## Example Output Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* Modern n8n-inspired design system CSS */
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #1e293b 100%);
            color: #ffffff;
            padding: 40px;
            margin: 0;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        /* ... rest of modern CSS ... */
    </style>
</head>
<body>
    <div class="container">
        <!-- Modern Gradient Header -->
        <header class="modern-header">
            <div class="header-background"></div>
            <div class="header-content">
                <h1 class="dashboard-title">Performance Analysis</h1>
                <p class="dashboard-subtitle">30-Day Report | Aug 11 - Sep 9, 2025</p>
                <p class="dashboard-metadata">Generated: Oct 19, 2025 | 1,344 records analyzed</p>
            </div>
        </header>

        <!-- Modern Tab Navigation -->
        <div class="tab-nav">
            <button class="tab active">OVERVIEW</button>
            <button class="tab">EXPLORER</button>
            <button class="tab">FUNNEL</button>
            <button class="tab">INSIGHTS</button>
        </div>

        <!-- Tab Content -->
        <div id="overview-tab" class="tab-content active">
            <!-- 3-column metric grid -->
            <div class="metrics-grid">
                <!-- Cards here -->
            </div>
        </div>

        <div id="explorer-tab" class="tab-content hidden">
            <!-- Explorer content -->
        </div>

        <div id="funnel-tab" class="tab-content hidden">
            <!-- Funnel content -->
        </div>

        <div id="insights-tab" class="tab-content hidden">
            <!-- Insights content -->
        </div>

        <!-- Modern Footer -->
        <footer class="modern-footer">
            <div class="footer-content">
                <p class="footer-credits">Produced By Danny McMillan | A Seller Sessions Production | &copy; 2025</p>
            </div>
        </footer>
    </div>

    <script>
        /* JavaScript for tabs, search, sort */
    </script>
</body>
</html>
```

## Success Criteria

This skill works correctly when:
- User uploads file → Complete tabbed dashboard generated automatically
- Modern n8n-inspired design with dark gradient background
- Purple/blue gradient accents throughout
- 3 equal-width metric cards per row (no emoticons)
- Glassmorphic cards with backdrop-filter blur effects
- Footer displays: "Produced By Danny McMillan | A Seller Sessions Production | © 2025"
- Funnel visualization with drop-off analysis
- Insights categorized by impact
- Search and sort fully functional
- Mobile-responsive layout (3 cols → 2 cols → 1 col)
- Zero questions asked before generation
- Smooth animations and hover effects
- Professional and cutting-edge appearance

## Integration with Other Skills

**Works with:**
- **mcp-response-optimization**: Ensures efficient data processing without token bloat
- **curv-design-system**: Alternative for internal Danny McMillan branded dashboards
- **dashboard-auto-generation**: CURV-branded version for internal use

**When to use this skill vs dashboard-auto-generation:**
- Use **dashboard-auto-generation-client**: For external clients, professional presentations, shareable reports
- Use **dashboard-auto-generation**: For internal CURV Tools, Seller Sessions content, Danny McMillan branded work
