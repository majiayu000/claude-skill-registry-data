---
name: dashboard-auto-generation
description: Automatically convert uploaded data (CSV, Excel, JSON) into complete interactive dashboards with zero user input required. Detects patterns in PPC reports, sales data, analytics exports, and business metrics - then generates insights, recommendations, and visualizations instantly. Works seamlessly with CURV design system for on-brand outputs with tabs, funnels, filters, and multi-view layouts.
---

# Dashboard Auto-Generation

## Core Principle
**Show first, refine later.** Never ask "what do you want to see?" - analyze the data, detect patterns, and build a professional dashboard immediately.

## When to Activate

Activate this skill when user:
- Uploads a data file (CSV, Excel, JSON, TSV)
- Says "analyze this data"
- Asks for a "dashboard" or "report"
- Wants to "visualize" or "understand" data
- Mentions PPC, sales, analytics, or business metrics

**Do NOT ask questions** - just build the best dashboard you can from the data.

## CURV Design System Integration (CRITICAL - ALWAYS INCLUDE)

**⚠️ MANDATORY REQUIREMENT: Every dashboard MUST include the complete CURV header and footer exactly as shown below.**

**NEVER skip the header or footer. If you generate a dashboard without both, the output is incorrect and must be regenerated.**

### Header (MANDATORY - Copy this exact structure)

```html
<!-- ========== CURV HEADER (REQUIRED) ========== -->
<header class="curv-header">
    <!-- Rotating background shape -->
    <div class="header-shape"></div>

    <!-- Header content -->
    <div class="header-content">
        <h1 class="hero-title">[Dashboard Name]</h1>
        <p class="hero-subtitle">[Description of data - e.g., "30-Day Amazon Advertising Analysis | Aug 11 - Sep 9, 2025"]</p>
        <p class="powered-by">POWERED BY CURV</p>
    </div>
</header>
```

**Required CSS for Header:**
```css
.curv-header {
    text-align: center;
    margin-bottom: 40px;
    padding: 40px;
    background: rgba(3, 12, 27, 0.6);
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1.5px solid rgba(157, 78, 221, 0.5);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CRITICAL: Rotating background shape animation */
.header-shape {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 600px;
    height: 600px;
    background: linear-gradient(135deg,
        rgba(157, 78, 221, 0.15) 0%,
        rgba(157, 78, 221, 0.05) 50%,
        transparent 100%);
    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
    transform: translate(-50%, -50%);
    animation: headerRotate 30s linear infinite;
    opacity: 0.3;
    z-index: 0;
}

@keyframes headerRotate {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

.header-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    position: relative;
    z-index: 1;
    max-width: 800px;
}

.hero-title {
    font-size: 72px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -2px;
    text-align: center;
    text-shadow: 0 0 25px rgba(255, 255, 255, 0.6),
                 0 0 50px rgba(255, 255, 255, 0.4),
                 0 0 100px rgba(157, 78, 221, 0.4);
    margin: 0;
}

.hero-subtitle {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.8);
    text-align: center;
    margin: 0;
    max-width: 600px;
}

.powered-by {
    font-size: 14px;
    color: rgb(157, 78, 221);
    letter-spacing: 1px;
    text-align: center;
    text-transform: uppercase;
    font-weight: 500;
    margin-top: 0.5rem;
}

/* Responsive header */
@media (max-width: 768px) {
    .hero-title { font-size: 48px; }
    .hero-subtitle { font-size: 16px; }
}
```

### Footer (MANDATORY - Copy this exact structure)

```html
<!-- ========== CURV FOOTER (REQUIRED) ========== -->
<footer class="curv-footer">
    <div class="footer-title">[Dashboard Name]</div>
    <div class="footer-subtitle">Advanced [Data Type] Analytics for Amazon Sellers</div>
    <div class="footer-credits">Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025</div>
</footer>
```

**Required CSS for Footer:**
```css
.curv-footer {
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(157, 78, 221, 0.2);
    color: rgba(255, 255, 255, 0.5);
}

.footer-title {
    font-size: 16px;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.footer-subtitle {
    font-size: 12px;
    opacity: 0.7;
    margin-bottom: 1rem;
    color: rgba(255, 255, 255, 0.7);
}

.footer-credits {
    font-size: 11px;
    opacity: 0.5;
    color: rgba(255, 255, 255, 0.7);
    letter-spacing: 0.5px;
}
```

### Tab Navigation (When Multiple Views)
```html
<div class="tab-nav">
    <button class="tab active">📊 OVERVIEW</button>
    <button class="tab">🔍 EXPLORER</button>
    <button class="tab">📈 FUNNEL</button>
    <button class="tab">💎 OPPORTUNITIES</button>
</div>
```

**Styling:**
- Inactive: Dark background `rgba(255, 255, 255, 0.05)`, white text
- Active: Purple background `rgb(157, 78, 221)`, white text
- Border radius: 12px
- Padding: 12px 24px

### Color System
```css
/* Backgrounds */
--bg-primary: rgb(3, 12, 27);              /* Main background */
--bg-header: linear-gradient(180deg, rgb(18, 11, 41) 0%, rgb(13, 18, 41) 40%, rgb(4, 16, 32) 70%, rgb(3, 12, 27) 100%);
--bg-panel: rgba(255, 255, 255, 0.03);     /* Glassmorphic panels */

/* Accents */
--accent: rgb(157, 78, 221);               /* CURV Purple */
--accent-hover: rgb(177, 98, 241);
--accent-border: rgba(157, 78, 221, 0.5);

/* Status Colors */
--success: rgb(34, 197, 94);               /* Green - Top Growing */
--warning: rgb(234, 179, 8);               /* Yellow - Hidden Gem */
--danger: rgb(239, 68, 68);                /* Red - Drop-off/Critical */
--info: rgb(59, 130, 246);                 /* Blue - Clicks/CTR */

/* Text */
--text-primary: #ffffff;
--text-muted: rgba(255, 255, 255, 0.7);
--text-dim: rgba(255, 255, 255, 0.5);
```

### Typography
```css
/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: rgb(3, 12, 27);
    color: #ffffff;
}

.hero-title {
    font-size: 72px;
    font-weight: 700;
    letter-spacing: -2px;
    text-shadow: 0 0 25px rgba(255, 255, 255, 0.6),
                 0 0 50px rgba(255, 255, 255, 0.4),
                 0 0 100px rgba(157, 78, 221, 0.4);
}

.metric-value {
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -1px;
}

.metric-label {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255, 255, 255, 0.7);
}
```

### Glassmorphic Panel Template
```css
.panel {
    background: linear-gradient(135deg, rgba(18, 11, 41, 0.6), rgba(13, 18, 41, 0.6));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(157, 78, 221, 0.3);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

### Button Styles
```css
.btn-primary {
    background: linear-gradient(135deg, rgb(157, 78, 221), rgb(177, 98, 241));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(157, 78, 221, 0.4);
}

.btn-outline {
    background: transparent;
    color: rgb(157, 78, 221);
    border: 2px solid rgba(157, 78, 221, 0.5);
    border-radius: 12px;
    padding: 10px 28px;
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
4. **OPPORTUNITIES** - Hidden gems, bottlenecks, drop-offs

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
4. **OPPORTUNITIES** - Low stock, high return rate, underperformers

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
4. **OPPORTUNITIES** - High bounce sources, conversion opportunities

### 4. Accounting / Financial Data
**Detect columns like:**
- Date, Account, Category, Transaction Type
- Amount, Debit, Credit, Balance
- Vendor, Customer, Invoice

**Auto-generate tabs:**
1. **OVERVIEW** - Total income, expenses, profit, cash flow
2. **EXPLORER** - Transaction table with filters (vendor, category, date)
3. **NO FUNNEL** - Not applicable for accounting
4. **OPPORTUNITIES** - Top expenses, late invoices, cash flow issues

### 5. Support Tickets / CRM Data
**Detect columns like:**
- Ticket ID, Status, Priority, Category
- Created Date, Resolved Date, Response Time
- Agent, Customer, Satisfaction Score

**Auto-generate tabs:**
1. **OVERVIEW** - Total tickets, avg resolution time, satisfaction
2. **EXPLORER** - Ticket table with filters (status, agent, category)
3. **FUNNEL** - New → In Progress → Resolved
4. **OPPORTUNITIES** - Overdue tickets, low satisfaction, bottlenecks

## Tab System (When to Use)

### Use Tabs When:
- Dataset has >100 rows (need explorer for search/filter)
- Data supports funnel visualization (impressions→clicks→conversions)
- Multiple opportunity types exist (hidden gems, bottlenecks, drop-offs)

### Single Page When:
- Dataset <50 rows (all fits on overview)
- Simple report with few metrics
- No funnel or exploration needed

### Tab Structure
```html
<div class="dashboard-container">
    <div class="tab-nav">
        <button class="tab active" data-tab="overview">📊 OVERVIEW</button>
        <button class="tab" data-tab="explorer">🔍 EXPLORER</button>
        <button class="tab" data-tab="funnel">📈 FUNNEL</button>
        <button class="tab" data-tab="opportunities">💎 OPPORTUNITIES</button>
    </div>

    <div id="overview-tab" class="tab-content active">
        <!-- Overview content -->
    </div>

    <div id="explorer-tab" class="tab-content hidden">
        <!-- Explorer content -->
    </div>

    <div id="funnel-tab" class="tab-content hidden">
        <!-- Funnel content -->
    </div>

    <div id="opportunities-tab" class="tab-content hidden">
        <!-- Opportunities content -->
    </div>
</div>

<script>
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
            content.classList.add('hidden');
        });
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));

        // Show selected tab
        const tabName = tab.getAttribute('data-tab');
        document.getElementById(tabName + '-tab').classList.add('active');
        document.getElementById(tabName + '-tab').classList.remove('hidden');
        tab.classList.add('active');
    });
});
</script>
```

## Overview Tab (Always Required)

### Structure:
1. **Performance Summary Section** (4-6 large metric cards)
2. **Top Performers Table** (top 10 by primary metric)
3. **Insights Section** (3-5 key insights with "What this means" tooltips)

### Metric Cards with Icons:
```html
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-icon">👁️</div>
        <div class="metric-content">
            <p class="metric-value">50.9K</p>
            <p class="metric-label">IMPRESSIONS</p>
            <p class="metric-detail">total</p>
        </div>
        <div class="metric-footer">
            <span class="market-share">9.7%</span>
            <span class="label">Market Share</span>
        </div>
        <div class="tooltip-trigger">ℹ️ What this means</div>
    </div>
    <!-- Repeat for other metrics -->
</div>
```

**Icon mapping for PPC:**
- Impressions: 👁️
- Clicks: 🖱️
- Basket Adds: 🛒
- Purchases: 💰
- Spend: 💳
- Sales: 📈

### Tooltip Content:
```html
<div class="tooltip hidden">
    <p class="tooltip-text">[Explanation of metric]</p>
    <p class="tooltip-detail"><strong>Market Share:</strong> [Context about market share]</p>
</div>
```

## Explorer Tab (When >100 Rows)

### Structure:
1. **Search Bar** (filter across all text columns)
2. **Performance Score Legend** (color-coded badges)
3. **Sortable Table** (click column headers to sort)
4. **Pagination** (10/20/50 per page dropdown)

### Search Implementation:
```html
<div class="explorer-controls">
    <input type="text" id="search-input" placeholder="Search queries..." class="search-input">
    <select id="per-page" class="per-page-select">
        <option value="10">10 per page</option>
        <option value="20">20 per page</option>
        <option value="50">50 per page</option>
    </select>
    <span class="results-count">3 results</span>
</div>
```

### Performance Score Badges:
```html
<div class="performance-legend">
    <h3>Performance Score Legend</h3>
    <div class="legend-grid">
        <div class="legend-item">
            <span class="badge excellent">51-100%: Excellent</span>
        </div>
        <div class="legend-item">
            <span class="badge good">26-50%: Good</span>
        </div>
        <div class="legend-item">
            <span class="badge needs-work">0-25%: Needs Work</span>
        </div>
    </div>
</div>
```

**Badge colors:**
- Excellent (51-100%): Green `rgb(34, 197, 94)`
- Good (26-50%): Yellow `rgb(234, 179, 8)`
- Needs Work (0-25%): Red `rgb(239, 68, 68)`

### Sortable Table:
```html
<table class="data-table sortable">
    <thead>
        <tr>
            <th class="sortable" data-column="query">SEARCH QUERY ⬍</th>
            <th class="sortable" data-column="score">SCORE ⬍</th>
            <th class="sortable" data-column="impressions">IMPRESSIONS ⬍</th>
            <th class="sortable" data-column="clicks">CLICKS ⬍</th>
            <th class="sortable" data-column="ctr">CTR % ⬍</th>
            <th class="sortable" data-column="roas">ROAS ⬍</th>
        </tr>
    </thead>
    <tbody id="table-body">
        <!-- Rows populated dynamically -->
    </tbody>
</table>
```

### Classification Badges in Table:
```html
<td>
    <span class="badge stable-performer">✓ STABLE PERFORMER</span>
    <span class="badge-negative">↓ -24%</span>
</td>
```

**Badge types:**
- Rising Star: `⭐ RISING STAR` (purple)
- Stable Performer: `✓ STABLE PERFORMER` (blue)
- Needs Attention: `⚠️ NEEDS ATTENTION` (red)

## Funnel Tab (When Funnel Data Exists)

### When to Create Funnel:
**PPC Data:** Impressions → Clicks → Cart Adds → Purchases
**E-commerce:** Sessions → Views → Cart → Purchase
**Analytics:** Landing → Engagement → Goal Completion
**Support:** New → In Progress → Resolved

### Funnel Visualization:
```html
<div class="funnel-container">
    <h2>Customer Journey Funnel</h2>
    <p class="funnel-subtitle">Track your customer journey from first impression to final purchase. Spot bottlenecks instantly and discover growth opportunities.</p>

    <div class="funnel-visual">
        <!-- Stage 1 -->
        <div class="funnel-stage" style="width: 100%;">
            <div class="stage-label">
                <span class="stage-icon">👁️</span>
                <span class="stage-name">Impressions</span>
            </div>
            <div class="stage-metric">50.9K</div>
            <div class="stage-detail">9.7% market share</div>
        </div>

        <!-- Drop-off indicator -->
        <div class="funnel-drop">
            <span class="drop-badge critical">⬇ -94.9% drop-off</span>
            <div class="drop-arrow">↓</div>
        </div>

        <!-- Stage 2 -->
        <div class="funnel-stage" style="width: 85%; background: linear-gradient(90deg, rgba(59, 130, 246, 0.3), rgba(59, 130, 246, 0.1));">
            <div class="stage-label">
                <span class="stage-icon">🖱️</span>
                <span class="stage-name">Clicks</span>
            </div>
            <div class="stage-metric">2.6K</div>
            <div class="stage-detail">
                <span class="cvr-badge">5.1% CVR</span>
                <span class="drop-indicator critical">⚠️ Critical Drop-off</span>
            </div>
        </div>

        <!-- Continue for all stages -->
    </div>

    <div class="funnel-summary">
        <div class="summary-card">
            <p class="summary-value purple">0.62%</p>
            <p class="summary-label">Overall Conversion</p>
        </div>
        <div class="summary-card">
            <p class="summary-value red">94.9%</p>
            <p class="summary-label">Biggest Problem</p>
        </div>
        <div class="summary-card">
            <p class="summary-value yellow">Impressions → Clicks</p>
            <p class="summary-label">Critical Stage</p>
        </div>
        <div class="summary-card">
            <p class="summary-value green">2</p>
            <p class="summary-label">Issues to Fix</p>
        </div>
    </div>

    <div class="funnel-diagram">
        <h3>💡 Understanding Your Sales Funnel</h3>
        <div class="funnel-flow">
            <div class="flow-stage">
                <span class="flow-icon">👁️</span>
                <span class="flow-label">Impressions</span>
                <span class="flow-description">Shoppers see your product in search results</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-stage">
                <span class="flow-icon">🖱️</span>
                <span class="flow-label">Clicks</span>
                <span class="flow-description">Interested shoppers click to learn more</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-stage">
                <span class="flow-icon">🛒</span>
                <span class="flow-label">Cart Adds</span>
                <span class="flow-description">Convinced shoppers add to cart</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-stage">
                <span class="flow-icon">💰</span>
                <span class="flow-label">Purchases</span>
                <span class="flow-description">Final step: completed sales</span>
            </div>
        </div>
    </div>
</div>
```

### Funnel Styling:
```css
.funnel-visual {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    margin: 40px 0;
}

.funnel-stage {
    background: linear-gradient(90deg, rgba(157, 78, 221, 0.3) 0%, rgba(157, 78, 221, 0.1) 100%);
    border: 2px solid rgba(157, 78, 221, 0.5);
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    position: relative;
    transition: all 0.3s ease;
}

.funnel-drop {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 0;
}

.drop-badge {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgb(239, 68, 68);
    color: rgb(239, 68, 68);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}

.drop-badge.critical {
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.cvr-badge {
    background: rgba(34, 197, 94, 0.2);
    color: rgb(34, 197, 94);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
```

### Drop-off Severity:
- **Critical (>80%):** Red badge with pulse animation
- **Warning (50-80%):** Yellow/orange badge
- **Normal (<50%):** Muted display, no badge

## Opportunities Tab (Always Include)

### Structure:
1. **Opportunities Legend** (category badges)
2. **Impact Level Filter Buttons** (High/Medium/Low)
3. **Opportunity Cards** (sorted by impact)

### Opportunities Legend:
```html
<div class="opportunities-legend">
    <h3>Opportunities Legend</h3>
    <div class="legend-grid">
        <div class="legend-category">
            <span class="category-icon">💎</span>
            <span class="category-label">Hidden Gem</span>
            <span class="category-description">Low market share, high conversion</span>
        </div>
        <div class="legend-category">
            <span class="category-icon">⚠️</span>
            <span class="category-label">Funnel Bottleneck</span>
            <span class="category-description">High traffic, poor conversion</span>
        </div>
        <div class="legend-category">
            <span class="category-icon">📊</span>
            <span class="category-label">Share Opportunity</span>
            <span class="category-description">Strong metrics, growth potential</span>
        </div>
    </div>

    <h3>Impact Levels</h3>
    <div class="legend-grid">
        <div class="impact-level">
            <span class="badge high-impact">High Impact</span>
            <span>10,000+ impressions</span>
        </div>
        <div class="impact-level">
            <span class="badge medium-impact">Medium Impact</span>
            <span>3,000-10,000 impressions</span>
        </div>
        <div class="impact-level">
            <span class="badge low-impact">Low Impact</span>
            <span><3,000 impressions</span>
        </div>
    </div>
</div>
```

### Impact Filter Buttons:
```html
<div class="impact-filters">
    <p>💡 Hover over any opportunity card for detailed performance breakdown</p>
    <div class="filter-buttons">
        <button class="filter-btn active" data-impact="high">
            ⚠️ HIGH IMPACT <span class="count">4</span>
        </button>
        <button class="filter-btn" data-impact="medium">
            🎯 MEDIUM IMPACT <span class="count">1</span>
        </button>
        <button class="filter-btn" data-impact="low">
            ✓ LOW IMPACT <span class="count">0</span>
        </button>
    </div>
</div>
```

### Opportunity Cards:
```html
<div class="opportunities-grid">
    <div class="opportunity-card high-impact" data-impact="high">
        <div class="card-header">
            <span class="opportunity-icon">💎</span>
            <span class="impact-badge high">HIGH IMPACT</span>
        </div>
        <h3 class="opportunity-title">Hidden Gem</h3>
        <p class="opportunity-keyword">wireless headphones</p>
        <p class="opportunity-insight">Low market share but high conversion rate - untapped potential</p>

        <div class="opportunity-metrics">
            <div class="metric-row">
                <span class="metric-label">Impressions:</span>
                <span class="metric-value">15,420</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Clicks:</span>
                <span class="metric-value">892</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Purchases:</span>
                <span class="metric-value">87</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">CVR:</span>
                <span class="metric-value success">0.56%</span>
            </div>
        </div>

        <button class="btn-primary">EXPLORE INSIGHTS</button>
    </div>
    <!-- More cards -->
</div>
```

### Opportunity Detection Logic:

**Hidden Gem:**
- Market share <10% (impressions)
- CVR >0.4% or ROAS >3.0x
- Badge: Purple 💎

**Funnel Bottleneck:**
- High impressions (>10,000)
- Low CTR (<3%) OR low cart-to-purchase rate (<40%)
- Badge: Red ⚠️

**Share Opportunity:**
- All metrics above average
- Market share potential (CTR >5%, CVR >0.5%)
- Badge: Green 📊

**Priority Calculation:**
```
Impact Score = (Impressions / 1000) × CVR × ROAS
High Impact: >10
Medium Impact: 3-10
Low Impact: <3
```

## Search & Filter Implementation

### Search Functionality:
```javascript
const searchInput = document.getElementById('search-input');
const tableBody = document.getElementById('table-body');

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

    document.querySelector('.results-count').textContent = `${visibleCount} results`;
});
```

### Sortable Table:
```javascript
document.querySelectorAll('.sortable').forEach(header => {
    header.addEventListener('click', () => {
        const column = header.getAttribute('data-column');
        const rows = Array.from(tableBody.querySelectorAll('tr'));
        const isAscending = header.classList.contains('asc');

        rows.sort((a, b) => {
            const aVal = a.querySelector(`[data-column="${column}"]`).textContent;
            const bVal = b.querySelector(`[data-column="${column}"]`).textContent;

            // Handle numeric vs text sorting
            if (!isNaN(aVal) && !isNaN(bVal)) {
                return isAscending ? aVal - bVal : bVal - aVal;
            }
            return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });

        // Clear existing order
        tableBody.innerHTML = '';
        rows.forEach(row => tableBody.appendChild(row));

        // Toggle sort direction
        document.querySelectorAll('.sortable').forEach(h => h.classList.remove('asc', 'desc'));
        header.classList.add(isAscending ? 'desc' : 'asc');
    });
});
```

## Insight & Recommendation Cards

### Insight Cards with Tooltips:
```html
<div class="insights-section">
    <h2>📊 Key Insights</h2>
    <div class="insights-grid">
        <div class="insight-card success">
            <div class="insight-icon">✓</div>
            <div class="insight-content">
                <h3>Product Pages outperform all placements</h3>
                <p class="insight-metric">5.84x ROAS vs 2.1x average</p>
                <div class="insight-tooltip">
                    <span class="tooltip-trigger">💡 What this means</span>
                    <div class="tooltip-content hidden">
                        <p>Product Pages deliver nearly 3x better return than other placements. Every £1 spent generates £5.84 in sales.</p>
                        <p><strong>Recommendation:</strong> Increase budget allocation to Product Pages by 30%.</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- More insights -->
    </div>
</div>
```

### Recommendation Cards:
```html
<div class="recommendations-section">
    <h2>🎯 Actionable Recommendations</h2>
    <div class="recommendations-grid">
        <div class="recommendation-card">
            <div class="rec-number">1</div>
            <div class="rec-content">
                <h3>Reallocate 40% of "Rest of Search" budget to "Product Pages"</h3>
                <p class="rec-reason">Rest of Search shows 33.5% ACOS vs Product Pages at 17.1% ACOS</p>
                <div class="rec-impact">
                    <span class="impact-label">Expected Impact:</span>
                    <span class="impact-value success">Overall ACOS drops from 25.5% to ~22%</span>
                </div>
                <div class="rec-urgency high">🔴 High Priority</div>
            </div>
        </div>
        <!-- More recommendations -->
    </div>
</div>
```

## Performance Summary Cards

### Conversion Rate Cards (for Funnel):
```html
<div class="performance-summary">
    <h2>Performance Summary</h2>
    <p class="summary-subtitle">Conversion rates show how effectively you move customers through your sales funnel</p>

    <div class="conversion-cards">
        <div class="conversion-card blue">
            <p class="conversion-value">5.1%</p>
            <p class="conversion-label">CLICK RATE</p>
            <p class="conversion-description">How appealing your listing is compared to competitors</p>
        </div>
        <div class="conversion-card green">
            <p class="conversion-value">21.6%</p>
            <p class="conversion-label">ADD-TO-CART RATE</p>
            <p class="conversion-description">How convincing your product details and pricing are</p>
        </div>
        <div class="conversion-card yellow">
            <p class="conversion-value">56.1%</p>
            <p class="conversion-label">PURCHASE RATE</p>
            <p class="conversion-description">How well you convert cart additions to actual sales</p>
        </div>
        <div class="conversion-card purple">
            <p class="conversion-value">0.62%</p>
            <p class="conversion-label">OVERALL CVR</p>
            <p class="conversion-description">Your complete funnel: from impression to purchase</p>
        </div>
    </div>
</div>
```

## File Naming Convention

```
[dashboard-name]-[date].html

Examples:
- ppc-placement-dashboard-2025-10-19.html
- sales-performance-dashboard-2025-10-19.html
- website-analytics-dashboard-2025-10-19.html
```

## Quality Gates

**CRITICAL - Before delivering ANY dashboard, verify:**

**🚨 MANDATORY (Dashboard is INVALID without these):**
- ✅ CURV header with rotating background animation (`.header-shape` with `@keyframes headerRotate`)
- ✅ Hero title with white glow effect (`text-shadow: 0 0 25px...`)
- ✅ "POWERED BY CURV" text in purple (`rgb(157, 78, 221)`)
- ✅ CURV footer with three lines: title, subtitle, credits
- ✅ Footer credits: "Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025"

**⚠️ OUTPUT FORMAT REQUIREMENT:**
- ✅ Must be standalone HTML file (NOT React JSX, NOT component code)
- ✅ Complete `<!DOCTYPE html>` with `<head>` and `<body>`
- ✅ All CSS in `<style>` tag (no external stylesheets)
- ✅ All JavaScript in `<script>` tag (no external files)
- ✅ File opens directly in browser without build tools

**Standard Quality Checks:**
- ✅ Tab navigation (if >100 rows or funnel exists)
- ✅ All metric cards have icons and tooltips
- ✅ Funnel visualization (if applicable data)
- ✅ Opportunities tab with impact levels
- ✅ Search/filter working in Explorer tab
- ✅ Sortable table headers
- ✅ Color-coded badges (green/yellow/red)
- ✅ Purple accent color `rgb(157, 78, 221)` used consistently
- ✅ Dark background `rgb(3, 12, 27)`
- ✅ Responsive layout (works on mobile)
- ✅ JavaScript for tabs, search, sort included
- ✅ All tooltips functional (hover or click)

## Example Output Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PPC Placement Dashboard - CURV Tools</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* CURV Design System CSS */
        /* [Complete CSS from examples above] */
    </style>
</head>
<body>
    <!-- Hero Header -->
    <div class="hero-header">
        <h1 class="hero-title">PPC Placement Performance</h1>
        <p class="hero-subtitle">30-Day Analysis (Aug 11 - Sep 9, 2025) • 3,917 data points analyzed</p>
        <p class="powered-by">POWERED BY CURV</p>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-nav">
        <button class="tab active" data-tab="overview">📊 OVERVIEW</button>
        <button class="tab" data-tab="explorer">🔍 EXPLORER</button>
        <button class="tab" data-tab="funnel">📈 FUNNEL</button>
        <button class="tab" data-tab="opportunities">💎 OPPORTUNITIES</button>
    </div>

    <!-- Tab Content -->
    <div id="overview-tab" class="tab-content active">
        <!-- Overview content -->
    </div>

    <div id="explorer-tab" class="tab-content hidden">
        <!-- Explorer content -->
    </div>

    <div id="funnel-tab" class="tab-content hidden">
        <!-- Funnel content -->
    </div>

    <div id="opportunities-tab" class="tab-content hidden">
        <!-- Opportunities content -->
    </div>

    <!-- Footer -->
    <footer class="curv-footer">
        <p>PPC Placement Performance</p>
        <p>Advanced Search Performance Analytics for Amazon Sellers</p>
        <p>Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025</p>
    </footer>

    <script>
        /* JavaScript for tabs, search, sort, tooltips */
    </script>
</body>
</html>
```

## Success Criteria

This skill works correctly when:
- ✅ User uploads file → Complete tabbed dashboard generated automatically
- ✅ Header and footer match CURV production tools exactly
- ✅ Purple accent color used throughout
- ✅ Funnel visualization shows drop-offs with CVR
- ✅ Opportunities categorized by impact level
- ✅ Search and sort fully functional
- ✅ All tooltips provide useful context
- ✅ Dashboard is visually identical to SQPR Analyser style
- ✅ Zero questions asked before generation
- ✅ User can make immediate business decisions from output
