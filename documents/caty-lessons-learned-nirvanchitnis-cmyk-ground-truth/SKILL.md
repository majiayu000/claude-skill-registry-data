---
name: caty-lessons-learned
description: North star principles from CATY equity research project - professional HTML standards, external source citations, audit-grade documentation, and target profile frameworks that work for Big 4 audiences
version: 1.0.0
author: Nirvan Chitnis (PWC Audit Staff)
date: 2025-10-25
reference_project: https://github.com/nirvanchitnis-cmyk/caty-equity-research-live
---

# CATY Lessons Learned: North Star Principles

## Purpose

This skill captures proven design patterns, documentation standards, and quality principles from the CATY (Cathay General Bancorp) equity research project. CATY serves as the **target profile framework** - a template that worked so well it became the standard for all future company analysis.

**Use this skill when**:
- Building HTML pages for professional/Big 4 audiences
- Documenting financial analysis or audit intelligence
- Creating target company profiles
- Designing data visualizations for partners
- Ensuring audit-grade provenance and citations

---

## Core Principles

### 1. Professional Visual Standards (No Clanker Slop)

**CATY Standard**: Off-white backgrounds, clean typography, subtle colors

**What to DO**:
- ✅ **Backgrounds**: Off-white (#F9F9F9, #FAFAFA), light grays (#F5F5F5)
- ✅ **Text colors**: Dark gray (#333, #2C3E50), not pure black
- ✅ **Accent colors**: Professional blues (#3498DB), greens (#27AE60), muted oranges (#E67E22)
- ✅ **Typography**: System fonts (-apple-system, BlinkMacSystemFont), Inter, Roboto
- ✅ **Spacing**: Generous padding (2-3rem between sections)
- ✅ **Borders**: Subtle (1px solid #DDD), rounded corners (border-radius: 8px)

**What to AVOID**:
- ❌ **Purple gradients** (screams "AI-generated slop")
- ❌ **Neon colors** (unprofessional)
- ❌ **Pure white backgrounds** (#FFF too stark)
- ❌ **Comic Sans or decorative fonts** (never)
- ❌ **Excessive animations** (distracting)
- ❌ **Stock photos of people in suits pointing at screens** (cringe)

**CATY Example**:
```css
body {
  background-color: #F9F9F9;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
  line-height: 1.6;
  padding: 2rem;
}

.section {
  background: white;
  border: 1px solid #DDD;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

h1 {
  color: #2C3E50;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.highlight {
  background-color: #FFF3CD; /* Subtle yellow, not neon */
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
```

---

### 2. External Source Citations (Audit-Grade Provenance)

**CATY Standard**: Every claim has a traceable source with URL + date

**Citation Format**:
```html
<p>
  CATY's total assets were $26.1B as of December 31, 2024
  <sup><a href="https://www.sec.gov/..." target="_blank">[1]</a></sup>.
</p>

<!-- Footnotes section -->
<div class="sources">
  <h3>Sources</h3>
  <ol>
    <li>
      <a href="https://www.sec.gov/Archives/edgar/data/..." target="_blank">
        SEC 10-K Filing, Cathay General Bancorp, December 31, 2024
      </a>
    </li>
  </ol>
</div>
```

**Why This Matters**:
- ✅ **Audit trail**: Partners can verify every fact
- ✅ **Regulatory compliance**: SEC/PCAOB require source documentation
- ✅ **Credibility**: Shows rigor, not just ChatGPT output
- ✅ **Reproducibility**: Anyone can re-pull the same data

**CATY Practice**:
- Every financial metric has SEC EDGAR URL
- Every industry statistic has FDIC/HMDA/regulatory source
- Every market comparison has peer company 10-K citation
- SHA-256 checksums on all downloaded files (ground-truth extends this)

---

### 3. Target Profile Framework (Reusable Template)

**CATY Innovation**: Built a company profile structure so good it works for ANY company

**Sections** (in order):
1. **Executive Summary** (1-page, C-suite friendly)
2. **Business Model** (revenue streams, customer segments, competitive position)
3. **Financial Performance** (5-year trends, peer benchmarks, profitability analysis)
4. **Risk Factors** (regulatory, market, operational, credit risks)
5. **Critical Audit Matters** (if public company, extracted from 10-K)
6. **Valuation** (DCF, comparables, sensitivity analysis)
7. **Investment Thesis** (bull case, bear case, recommendation)
8. **Appendices** (detailed financials, methodology, sources)

**Why This Works**:
- ✅ **Big 4 teams recognize this structure** (mirrors audit planning memos)
- ✅ **Partners can skim or deep-dive** (executive summary vs appendices)
- ✅ **Modular**: Drop sections not relevant to use case
- ✅ **Scalable**: Apply to 1 company or 1,000

**Ground-Truth Application**:
- Use this structure for each extracted company
- Generate HTML pages automatically (like CATY site)
- Partners navigate company profiles, not JSON files

---

### 4. Data Visualization Best Practices

**CATY Standard**: Charts are clean, readable, and tell a story

**Chart Design Principles**:
- ✅ **Simple color palette**: Max 4-5 colors per chart
- ✅ **Clear labels**: Axis titles, legends, data point values
- ✅ **Trends over time**: Line charts for 5-year revenue/earnings
- ✅ **Peer comparisons**: Grouped bar charts for benchmarking
- ✅ **Responsive**: Charts scale on mobile
- ✅ **Accessible**: High contrast, no red/green only (colorblind friendly)

**What to AVOID**:
- ❌ **3D charts** (distort data, look dated)
- ❌ **Pie charts with >5 slices** (unreadable)
- ❌ **Default Excel colors** (ugly)
- ❌ **Missing axis labels** (confusing)
- ❌ **Overfitted trendlines** (misleading)

**CATY Example** (using Chart.js):
```javascript
// 5-Year Revenue Trend
const ctx = document.getElementById('revenueChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['2020', '2021', '2022', '2023', '2024'],
    datasets: [{
      label: 'Revenue ($M)',
      data: [1200, 1350, 1500, 1680, 1820],
      borderColor: '#3498DB',
      backgroundColor: 'rgba(52, 152, 219, 0.1)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'CATY Revenue Growth (2020-2024)',
        font: { size: 16, weight: '600' }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => '$' + value + 'M'
        }
      }
    }
  }
});
```

---

### 5. Interactive Elements (User Experience)

**CATY Standard**: Pages are navigable, searchable, and responsive

**Interactive Features**:
- ✅ **Table of contents** (sticky sidebar, jump to section)
- ✅ **Search functionality** (Ctrl+F works, or custom search)
- ✅ **Collapsible sections** (expand/collapse for long content)
- ✅ **Hover tooltips** (definitions for jargon)
- ✅ **Mobile menu** (hamburger icon, responsive nav)
- ✅ **Print-friendly** (CSS @media print rules)

**CATY Example** (Collapsible Section):
```html
<details>
  <summary><h3>Risk Factors (click to expand)</h3></summary>
  <div class="risk-content">
    <p>Interest rate risk: CATY's net interest margin is sensitive to...</p>
    <!-- Full risk factors content -->
  </div>
</details>

<style>
summary {
  cursor: pointer;
  padding: 1rem;
  background: #F9F9F9;
  border-radius: 4px;
}
summary:hover {
  background: #F0F0F0;
}
</style>
```

---

### 6. Documentation Philosophy

**CATY Mindset**: Document failures with more rigor than successes

**What to Document**:
- ✅ **Assumptions**: "We assume CATY's loan loss reserve is adequate..."
- ✅ **Limitations**: "This analysis does not include off-balance-sheet items..."
- ✅ **Data gaps**: "HMDA data not available for 2024 yet"
- ✅ **Methodology changes**: "Switched from DCF to P/E multiples because..."
- ✅ **Failure modes**: "CAM extraction returned 0 results - regex issue documented in..."
- ✅ **Lessons learned**: "Next time, validate balance sheet reconciliation earlier"

**Why This Matters**:
- ✅ **Audit teams trust transparent analysis** (vs black box)
- ✅ **Reproducibility**: Others can replicate and improve
- ✅ **Continuous improvement**: Learn from mistakes

**Ground-Truth Application**:
- `MILESTONE_01_PFSI_SUCCESS.md` documents bug fix (XBRL period consistency)
- `HANDOFF.md` lists known limitations (CAM parser low yield, validation missing from batch)
- `open_items/` directory tracks incomplete features

---

### 7. Mobile Responsiveness (Non-Negotiable)

**CATY Standard**: Partners review on iPad/iPhone, not just desktop

**Responsive Design Checklist**:
- ✅ **Viewport meta tag**: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- ✅ **Breakpoints**: 768px (tablet), 480px (mobile)
- ✅ **Flexible grids**: CSS Grid or Flexbox
- ✅ **Readable font sizes**: Min 16px on mobile
- ✅ **Touch-friendly buttons**: Min 44px × 44px
- ✅ **No horizontal scroll**: Content fits screen width

**CATY Example**:
```css
/* Desktop */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Tablet */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  h1 {
    font-size: 2rem; /* Smaller on tablet */
  }
}

/* Mobile */
@media (max-width: 480px) {
  .container {
    padding: 0.5rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .stats {
    flex-direction: column; /* Stack stats vertically */
  }
}
```

---

## CATY-to-Ground-Truth Translation

### What Ground-Truth Inherits from CATY

1. **Professional HTML standards** → `ARCHITECTURE_DEMO.html` uses off-white, clean typography
2. **External citations** → Every fact has SEC URL + SHA-256
3. **Target profile framework** → Each extracted company gets standardized structure
4. **Data visualization** → Charts for CAM trends, ICFR failure rates, sector benchmarks
5. **Interactive elements** → Collapsible sections, search, mobile-friendly
6. **Transparent documentation** → `MILESTONE_01` documents bug fix, not just success
7. **Mobile responsiveness** → Demo page works on all devices

### What Ground-Truth Extends Beyond CATY

1. **SHA-256 provenance** → CATY had URLs, ground-truth adds cryptographic verification
2. **RAG integration** → CATY was static HTML, ground-truth adds natural language queries
3. **Skills architecture** → CATY was manual, ground-truth packages expertise as reusable skills
4. **Sector routing** → CATY was one company, ground-truth handles banking/mortgage/tech with intelligent dispatch
5. **Validation framework** → CATY had manual checks, ground-truth has automated gates (balance sheet, EPS, data quality)

---

## Anti-Patterns (What NOT to Do)

### 1. Purple Gradient Syndrome
**Bad**: `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);`
**Why**: Screams "I used a template from CodePen" (not professional)
**CATY Fix**: Solid off-white or subtle gray gradients only

### 2. Unsourced Claims
**Bad**: "CATY is the largest bank in California"
**Why**: No citation = no credibility
**CATY Fix**: "CATY is the 12th largest bank in California by deposits<sup>[1]</sup>" + FDIC source

### 3. Wall of Text
**Bad**: 10-paragraph executive summary with no headings
**Why**: Partners won't read it
**CATY Fix**: Use bullet points, subheadings, bold key takeaways

### 4. Broken Links
**Bad**: Link to 10-K that returns 404
**Why**: Destroys trust instantly
**CATY Fix**: Verify all links before publishing, use SEC EDGAR permanent URLs

### 5. "Trust Me Bro" Methodology
**Bad**: "We valued CATY using DCF" (no details)
**Why**: Not reproducible, not auditable
**CATY Fix**: Full methodology section with assumptions, formulas, sensitivity analysis

---

## Quick Reference Checklist

When building professional HTML/docs, ensure:

**Visual Design**:
- [ ] Off-white background (#F9F9F9 or similar)
- [ ] System fonts or Inter/Roboto
- [ ] No purple gradients or neon colors
- [ ] Generous spacing (2rem+ between sections)
- [ ] Subtle borders and shadows

**Citations**:
- [ ] Every fact has source URL
- [ ] Sources section at bottom with numbered footnotes
- [ ] External links open in new tab (`target="_blank"`)
- [ ] Dates included (e.g., "as of December 31, 2024")

**Structure**:
- [ ] Executive summary first (1-page, skimmable)
- [ ] Clear section headings (H1, H2, H3 hierarchy)
- [ ] Table of contents for long documents
- [ ] Appendices for detailed data/methodology

**Interactivity**:
- [ ] Mobile-responsive (test on iPhone/iPad)
- [ ] Collapsible sections for long content
- [ ] Search functionality (or good Ctrl+F support)
- [ ] Print-friendly CSS

**Documentation**:
- [ ] Assumptions stated upfront
- [ ] Limitations acknowledged
- [ ] Methodology explained
- [ ] Failure modes documented

---

## Examples from CATY Project

### Example 1: Financial Performance Section
```html
<section id="financials">
  <h2>Financial Performance (2020-2024)</h2>

  <div class="metric-cards">
    <div class="card">
      <h3>Total Assets</h3>
      <p class="big-number">$26.1B</p>
      <p class="change positive">+12.3% YoY</p>
      <p class="source">
        <a href="https://www.sec.gov/..." target="_blank">Source: 10-K</a>
      </p>
    </div>

    <div class="card">
      <h3>Net Income</h3>
      <p class="big-number">$412M</p>
      <p class="change positive">+8.7% YoY</p>
      <p class="source">
        <a href="https://www.sec.gov/..." target="_blank">Source: 10-K</a>
      </p>
    </div>
  </div>

  <canvas id="revenueChart"></canvas>

  <details>
    <summary><h3>Methodology</h3></summary>
    <p>All financial data sourced from SEC EDGAR 10-K filings. YoY calculations based on fiscal year-end figures. Peer comparisons use median of 5 largest California banks by assets.</p>
  </details>
</section>
```

### Example 2: Risk Factors Extraction
```html
<section id="risks">
  <h2>Risk Factors</h2>

  <div class="risk-category">
    <h3>Credit Risk</h3>
    <p>
      CATY's loan portfolio is concentrated in commercial real estate (42% of total loans), exposing the bank to downturns in the California property market
      <sup><a href="https://www.sec.gov/..." target="_blank">[1]</a></sup>.
    </p>
    <p><strong>Mitigation:</strong> Diversified geographic footprint across Southern California, conservative underwriting standards.</p>
  </div>

  <div class="risk-category">
    <h3>Regulatory Risk</h3>
    <p>
      As a $20B+ bank, CATY is subject to enhanced prudential standards under Dodd-Frank
      <sup><a href="..." target="_blank">[2]</a></sup>.
    </p>
    <p><strong>Impact:</strong> Higher capital requirements, stress testing obligations, increased compliance costs.</p>
  </div>
</section>
```

---

## Reference Files

**CATY Project** (North Star):
- GitHub: https://github.com/nirvanchitnis-cmyk/caty-equity-research-live
- Live site: (if deployed to GitHub Pages)
- Key files: `index.html`, `CATY_05_nim_decomposition.html`, `CATY_16_coe_triangulation.html`

**Ground-Truth Application**:
- `ARCHITECTURE_DEMO.html` — Uses CATY visual standards
- `README.md` — Uses CATY documentation philosophy
- `MILESTONE_01_PFSI_SUCCESS.md` — Documents failures (XBRL bug) with same rigor as successes

---

## Notes

**CATY Timeline**: Built October 18, 2025 (1 week before ground-truth)

**CATY Achievement**: Established the canonical target profile framework — so good that it became the template for all future company analysis

**CATY Legacy**: Proved the 3-agent workflow (Claude ideates, Nirvan directs, Codex executes) on a hard bank analysis

**Ground-Truth Evolution**: Takes CATY's proven design patterns and adds:
- RAG natural language queries
- Automated extraction (vs manual research)
- SHA-256 provenance chain
- Skills-based domain expertise packaging

**Philosophy**: CATY is the north star because it **worked** — Big 4 teams understood it, partners could navigate it, and the analysis held up to scrutiny. Ground-truth inherits this DNA.

---

## When to Apply This Skill

**Use CATY principles when**:
- Building HTML pages for PWC/Big 4 audiences
- Documenting financial analysis or audit findings
- Creating company profiles or target assessments
- Designing data dashboards for partners
- Writing reports that will be reviewed by regulators (SEC, PCAOB)

**Don't force CATY patterns when**:
- Internal dev docs (Markdown is fine)
- Quick prototypes (perfection not needed)
- Non-financial content (different audience expectations)

**Remember**: CATY succeeded because it respected the audience (Big 4 partners) and delivered what they needed (professional, sourced, navigable analysis). Ground-truth does the same for audit intelligence.
