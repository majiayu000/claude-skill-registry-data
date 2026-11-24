---
name: "tech-hiring-data-science"
description: "Data scientists extract insights from data to inform product and business decisions. They range from analyst-adjacent (SQL, dashboards, A/B testing) to research-adjacent (statistical modelling, experimental design, ML). Define the profile c"
---

# Data Science — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Data Science

### What This Role Does
Data scientists extract insights from data to inform product and business decisions. They range from analyst-adjacent (SQL, dashboards, A/B testing) to research-adjacent (statistical modelling, experimental design, ML). Define the profile carefully before sourcing — "data scientist" is one of the most inconsistently used titles in tech.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Junior Data Scientist, Data Analyst (with ML focus), Associate Data Scientist |
| Mid | Data Scientist, Applied Scientist, Quantitative Analyst |
| Senior | Senior Data Scientist, Lead Data Scientist, Quantitative Researcher |
| Staff+ | Staff Data Scientist, Principal Scientist, Head of Data Science |
| Specialist | Growth Data Scientist, Product Data Scientist, Research Scientist |

### Skill Tiers

**Tier 1 — Must-have:**
- Python: pandas, NumPy, scikit-learn, scipy
- SQL: complex queries, window functions, CTEs — non-negotiable
- Statistical fundamentals: hypothesis testing, p-values, confidence intervals, A/B testing
- Data visualisation: matplotlib, seaborn, Plotly, or equivalent
- Jupyter notebooks / collaborative notebook environments

**Tier 2 — Differentiator:**
- Experiment design: power analysis, multi-armed bandits, holdout methodology
- ML fundamentals: regression, classification, clustering, cross-validation, bias-variance
- Business communication: can translate findings to non-technical stakeholders
- BI tools: Looker, Tableau, Superset, Mode
- Cloud data environments: BigQuery, Redshift, Snowflake

**Tier 3 — Bonus:**
- R (for statistical rigour signal)
- Causal inference: difference-in-differences, instrumental variables, propensity scoring
- ML in production (not just notebooks)
- Research publications or public analysis work (Kaggle, blog, papers)

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("data scientist" OR "applied scientist" OR "quantitative analyst") (Python OR SQL OR "machine learning" OR "statistical modelling") -recruiter -talent

# Product/growth focused
site:linkedin.com/in/ ("data scientist" OR "product analyst") ("A/B testing" OR experimentation OR "growth") -recruiter

# Kaggle — active practitioners
site:kaggle.com "joined * ago" python ("machine learning" OR "data science") -course -competition

# GitHub
site:github.com "joined on" "data scientist" (Python OR "jupyter" OR pandas) followers:>10
```

### Seniority Signals

- **Junior → Mid:** Can run an A/B test end-to-end without hand-holding; communicates results clearly
- **Mid → Senior:** Pushes back on poorly designed experiments; identifies what question *should* be asked, not just the one they were given
- **Senior → Staff:** Builds the analytics infrastructure and culture; defines measurement frameworks across product teams
- **Watch:** Many "data scientists" are actually data analysts. Ask: "Describe the last model you built and deployed." If they can't answer, you have an analyst.

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| Technical screen | SQL test (medium complexity) + 20 min stats questions | Fundamentals — non-negotiable |
| Take-home analysis | Real (anonymised) dataset, open-ended question, 3–4 hours | Problem framing, methodology, communication |
| Presentation | Walk through take-home findings to the team | Can they explain to a PM? Do they know the limits of their analysis? |
| Depth interview | Whiteboard: design an A/B test for [specific scenario] | Experimental rigour, edge case thinking |
| Behavioural | STAR questions on influencing without authority | Most DS work requires persuading PMs and engineers |

### Red Flags
- "I build models in scikit-learn" but cannot explain what cross-validation is
- Treats p < 0.05 as the only signal of significance — no understanding of effect size or power
- Has never shipped anything to production or influenced a real business decision
- Cannot write SQL fluently — a senior data scientist who struggles with window functions is a problem
- Notebooks are messy, undocumented, and non-reproducible

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $90k – $130k |
| Mid | $130k – $175k |
| Senior | $155k – $225k |
| Staff | $200k – $280k |
| Principal | $240k – $330k+ |
