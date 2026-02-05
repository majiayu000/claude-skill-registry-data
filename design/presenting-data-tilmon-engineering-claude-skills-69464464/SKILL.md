---
name: presenting-data
description: Component skill for creating compelling data-driven presentations and whitepapers using marp and pandoc with proper citations and reproducibility
---

# Presenting Data

## Purpose

This component skill guides creation of professional data-driven presentations and whitepapers. Use it when:
- Communicating analysis findings to stakeholders
- Creating executive summaries and detailed technical reports
- Documenting reproducible research with proper citations
- Building a presentation hierarchy: slides → whitepapers (drill-in capability)
- Referenced by process skills for final deliverables

**Supports two complementary formats:**
- **Presentations (marp)** - Slide decks for meetings, pitches, and executive summaries
- **Whitepapers (pandoc)** - Comprehensive documents with citations, cross-references, and academic formatting

## Prerequisites

- Analysis completed with clear findings
- Query results documented and interpreted (use `interpreting-results` skill)
- Visualizations prepared (use `creating-visualizations` skill)
- Understanding of data sources, queries, and reproducibility requirements
- Clear communication goal and target audience identified

## Data Presentation Process

Create a TodoWrite checklist for the 5-phase presentation process:

```
Phase 1: Analyze Audience & Purpose - pending
Phase 2: Structure Narrative - pending
Phase 3: Create Content - pending
Phase 4: Add Citations & Reproducibility - pending
Phase 5: Generate Outputs - pending
```

Mark each phase as you complete it. Document all presentation materials in your analysis directory.

---

## Phase 1: Analyze Audience & Purpose

**Goal:** Understand who will consume your presentation and what decisions they need to make.

### Identify Your Audience

**Executive Stakeholders:**
- Format: Slide presentation (5-10 slides)
- Focus: Key findings, business impact, recommendations
- Detail Level: High-level metrics, visual emphasis
- Tool: **marp** for quick, visual presentations

**Technical Peers:**
- Format: Whitepaper or technical report (20-50 pages)
- Focus: Methodology, reproducibility, detailed analysis
- Detail Level: SQL queries, statistical methods, data quality notes
- Tool: **pandoc** for comprehensive documentation

**Mixed Audience:**
- Format: Both (presentation + supporting whitepaper)
- Focus: Slides for overview, whitepaper for drill-in details
- Detail Level: Presentation hierarchy allowing progressive disclosure
- Tools: **marp** for slides, **pandoc** for backing documents

### Define Communication Goals

**What decisions will this presentation support?**
- Strategic planning (high-level trends and forecasts)
- Operational changes (specific process improvements)
- Technical validation (methodology and reproducibility)
- Policy changes (compliance, risk, standards)

**What actions should the audience take?**
- Approve/reject a proposal
- Allocate budget or resources
- Change operational procedures
- Investigate further (drill into details)

**CHECKPOINT:** Before proceeding to Phase 2, you MUST have:
- [ ] Target audience identified (executive, technical, or mixed)
- [ ] Primary communication goal defined
- [ ] Desired audience action articulated
- [ ] Output format selected (presentation, whitepaper, or both)

---

## Phase 2: Structure Narrative

**Goal:** Organize findings into a compelling narrative that guides the audience to your conclusions.

### Use the 3-Paragraph Essay Structure

**→ See [frameworks/3-paragraph-essay.md](./frameworks/3-paragraph-essay.md) for detailed guidance**

The classic essay structure adapts perfectly to data presentations:

1. **Introduction & Thesis**
   - State the question or problem
   - Present your key finding or recommendation
   - Preview supporting evidence

2. **Body & Supporting Arguments**
   - Present data findings that support your thesis
   - Use visualizations to make patterns clear
   - Address alternative explanations
   - Cite data sources and methodology

3. **Conclusion & Next Steps**
   - Restate key findings
   - Articulate implications and recommendations
   - Identify limitations and follow-up questions

4. **Bibliography & Supporting Documentation**
   - Data sources and SQL queries
   - Reproducibility information (versions, timestamps)
   - References to prior research or methodology
   - Links to detailed whitepapers or repositories

### Apply Narrative Structure for Data Stories

**→ See [frameworks/narrative-structure.md](./frameworks/narrative-structure.md) for storytelling patterns**

Data presentations follow narrative arcs:
- **Setup**: Establish business context and question
- **Conflict**: Present the data challenge or pattern
- **Resolution**: Show findings and recommendations
- **Call to Action**: Define next steps

### Outline Your Presentation

Create outline document: `analysis/[session-name]/presentation-outline.md`

**For Presentations (Marp):**
```markdown
# Presentation Outline

## Slide 1: Title & Context
- Analysis question
- Time period and data sources

## Slide 2-3: Key Findings (Thesis)
- 3-5 bullet points with metrics
- Visual emphasis

## Slide 4-7: Supporting Evidence (Body)
- One finding per slide
- Include visualizations
- Reference methodology

## Slide 8: Conclusions & Recommendations
- Restate key findings
- Next steps
- Questions

## Slide 9: Reproducibility Notes (Appendix)
- Data sources
- Query locations
- Validation status
```

**For Whitepapers (Pandoc):**
```markdown
# Whitepaper Outline

## Introduction (2-3 pages)
- Business context and objectives
- Research question
- Thesis statement

## Methodology (5-10 pages)
- Data sources and collection methods
- SQL queries and transformations
- Analysis frameworks used
- Data quality assessment

## Results (10-20 pages)
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data
- Visualizations and tables

## Discussion (5-10 pages)
- Interpretation of findings
- Comparison to prior research
- Limitations and caveats
- Alternative explanations

## Conclusions (2-3 pages)
- Summary of key findings
- Recommendations
- Future research directions

## References
- Bibliography (BibTeX format)
- Appendix: SQL queries
- Appendix: Data validation notes
```

**CHECKPOINT:** Before proceeding to Phase 3, you MUST have:
- [ ] Narrative structure selected (essay-based or story-based)
- [ ] Presentation outline created with sections identified
- [ ] Key findings and supporting evidence mapped
- [ ] Introduction, body, conclusion, and bibliography sections defined

---

## Phase 3: Create Content

**Goal:** Write presentation content using appropriate tools (marp for slides, pandoc for documents).

### Creating Slide Presentations with Marp

**→ See [tools/marp.md](./tools/marp.md) for detailed CLI usage and syntax**

Marp transforms Markdown into professional slide decks. Use for:
- Executive summaries (5-10 slides)
- Meeting presentations
- Quick stakeholder updates

**Basic Marp Syntax:**
```markdown
---
theme: gaia
paginate: true
footer: "DataPeeker Analysis"
---

# Q4 Sales Analysis
## Key Findings

---

## Data Source
- Database: `analytics_prod.sales_metrics`
- Query Date: 2025-11-25
- Period: 2024-10-01 to 2024-12-31

---

## Finding 1: Revenue Growth

- Total Revenue: $1.2M
- YoY Growth: +23%
- Top Region: West Coast

![width:600px](revenue-chart.png)

---

## Methodology

\```sql
SELECT
  DATE_TRUNC('month', date) as month,
  SUM(amount) as revenue
FROM sales_metrics
WHERE date BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY month
\```

---

## Conclusions

- Revenue exceeded target by 15%
- West Coast expansion successful
- Recommend continued investment

---

## Reproducibility

- Queries: `queries/q4_analysis.sql`
- Data validated: 2025-11-25
- Full report: [Technical Whitepaper](./whitepaper.pdf)
```

**Generate Presentation:**
```bash
marp presentation.md -o presentation.pdf
```

### Creating Whitepapers with Pandoc

**→ See [tools/pandoc.md](./tools/pandoc.md) for detailed CLI usage and citations**

Pandoc creates publication-quality documents. Use for:
- Technical reports (20-50 pages)
- Comprehensive analysis documentation
- Academic papers with citations and cross-references

**Basic Pandoc Structure:**
```yaml
---
title: "Q4 Sales Performance Analysis"
author: "DataPeeker Team"
date: "2025-11-25"
institute: "Tilmon Engineering"
abstract: |
  This analysis examines Q4 2024 sales data, revealing 23% YoY growth
  driven primarily by West Coast expansion. Methodology, findings, and
  recommendations are presented with full reproducibility documentation.
keywords: "sales analysis, SQL, data analysis, reproducibility"
toc: true
lof: true
lot: true
---

# Introduction

This analysis addresses the question: What factors drove Q4 2024
sales performance? Using DataPeeker to analyze production database
records, we identify key growth drivers and provide actionable
recommendations.

# Methodology

## Data Collection

Data was extracted from `analytics_prod.sales_metrics` using:

\```sql
SELECT
  transaction_id,
  customer_id,
  region,
  amount,
  transaction_date
FROM sales_metrics
WHERE DATE(transaction_date) BETWEEN '2024-10-01' AND '2024-12-31'
ORDER BY transaction_date
\```

## Analysis Framework

Analysis followed established data quality frameworks [@jones2024]
and reproducibility standards [@smith2023].

# Results

![Q4 Revenue by Region](revenue-by-region.png){#fig:revenue}

Figure @fig:revenue demonstrates clear regional patterns.

# Discussion

Our findings align with previous research on seasonal trends
[@williams2024] while revealing new patterns in customer behavior.

# Conclusions

Three key findings emerge from this analysis:
1. West Coast growth exceeded projections
2. Customer acquisition accelerated in Q4
3. Average transaction value increased 12%

# References
```

**Generate Whitepaper:**
```bash
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  --csl ieee.csl \
  -F pandoc-crossref \
  -s -V geometry:margin=1in \
  --toc \
  --number-sections \
  -o whitepaper.pdf
```

### Integrating Visualizations

**Use `creating-visualizations` component skill** to create charts and diagrams:

**Terminal visualizations:**
- Use `creating-visualizations` terminal formats for inline code examples
- Include ASCII charts in whitepaper appendices
- Show sparklines for trend indicators

**Image-based visualizations:**
- Use `creating-visualizations` image formats (Kroki) for slides and whitepapers
- Generate Mermaid flowcharts for methodology sections
- Create GraphViz diagrams for data lineage
- Use Vega-Lite for statistical charts

**Best Practices:**
- Export visualizations as PNG/SVG for marp presentations
- Reference figure numbers in pandoc documents
- Include chart source data or generation code
- Document visualization choices in methodology

**CHECKPOINT:** Before proceeding to Phase 4, you MUST have:
- [ ] Presentation/whitepaper content drafted in Markdown
- [ ] Visualizations created and embedded
- [ ] SQL queries and code snippets included
- [ ] Narrative structure followed (introduction, body, conclusion)

---

## Phase 4: Add Citations & Reproducibility

**Goal:** Document data sources, queries, and methodology to enable reproducibility and proper attribution.

### Citing Data Sources and Queries

**→ See [formats/citations.md](./formats/citations.md) for BibTeX and CSL formats**

Proper citation enables:
- Traceability to original data sources
- Validation of methodology
- Reproducibility by others
- Academic and professional credibility

**Citation Types for Data Analysis:**
1. **Data Sources** - Databases, APIs, file systems
2. **SQL Queries** - Specific queries used in analysis
3. **Analysis Tools** - Software and versions (DataPeeker, Python, R)
4. **Prior Research** - Published papers or internal reports
5. **Methodology References** - Statistical methods or frameworks

**Example BibTeX Entries:**
```bibtex
@misc{production_database_2025,
  author = {Tilmon Engineering},
  title = {Production Sales Metrics Database},
  year = {2025},
  url = {analytics_prod.sales_metrics},
  note = {Query timestamp: 2025-11-25 14:30 UTC}
}

@software{datapeeker_2025,
  author = {Tilmon Engineering},
  title = {DataPeeker: SQL Analysis Tool},
  year = {2025},
  version = {2.1.0},
  url = {https://github.com/tilmon/datapeeker}
}
```

### Documenting Reproducibility

**→ See [formats/reproducibility.md](./formats/reproducibility.md) for comprehensive checklist**

Reproducible research requires documentation of:
- **Data**: Source, timestamp, version, schema
- **Queries**: Full SQL text, execution time, row counts
- **Environment**: Tool versions, dependencies, configuration
- **Process**: Step-by-step methodology
- **Validation**: Data quality checks, cross-validation results

**Reproducibility Section Template:**
```markdown
## Reproducibility Information

### Data Sources
- **Database**: `analytics_prod.sales_metrics`
- **Schema Version**: v2.3.1
- **Query Timestamp**: 2025-11-25 14:30:00 UTC
- **Records Examined**: 50,000 transactions
- **Time Period**: 2024-10-01 to 2024-12-31

### Analysis Environment
- **Tool**: DataPeeker v2.1.0
- **Python Version**: 3.11.5
- **Key Libraries**: pandas 2.1.0, plotext 5.2.8
- **Operating System**: macOS 14.6.0

### Query Repository
- **Location**: `github.com/tilmon/analysis/queries/q4_sales.sql`
- **Commit Hash**: abc123def456
- **Execution Time**: 3.2 seconds
- **Rows Returned**: 50,000

### Data Quality Validation
- **Null Values**: 0.02% (within tolerance)
- **Duplicates**: 0 detected
- **Outliers**: 12 identified and documented separately
- **Cross-Validation**: Results match source system aggregate queries

### Reproducibility Instructions
1. Clone repository: `git clone github.com/tilmon/analysis`
2. Install dependencies: `pip install -r requirements.txt`
3. Run analysis: `python scripts/q4_analysis.py`
4. View results: `analysis/q4-2024/01-findings.md`
```

**CHECKPOINT:** Before proceeding to Phase 5, you MUST have:
- [ ] BibTeX bibliography created with data sources
- [ ] SQL queries documented with execution details
- [ ] Reproducibility section added with environment info
- [ ] Citations inserted in text using [@citation_key] syntax

---

## Phase 5: Generate Outputs

**Goal:** Compile final presentation and whitepaper artifacts using marp and pandoc.

### Generate Slide Presentation (Marp)

**Basic PDF Output:**
```bash
marp presentation.md -o presentation.pdf
```

**HTML with Speaker Notes:**
```bash
marp presentation.md -o presentation.html
```

**PowerPoint (Editable):**
```bash
marp presentation.md --pptx -o presentation.pptx
```

**With Custom Theme:**
```bash
marp presentation.md --theme-set custom-theme.css -o presentation.pdf
```

**Watch Mode (Live Preview):**
```bash
marp -w -p presentation.md
```

### Generate Whitepaper (Pandoc)

**PDF with Citations:**
```bash
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  --csl ieee.csl \
  -s -V geometry:margin=1in \
  -o whitepaper.pdf
```

**PDF with Cross-References:**
```bash
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  -F pandoc-crossref \
  -s --toc --number-sections \
  -o whitepaper.pdf
```

**Word Document (Editable):**
```bash
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  --reference-doc=template.docx \
  -o whitepaper.docx
```

**HTML for Web Publishing:**
```bash
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  -s -c style.css \
  --self-contained \
  -o whitepaper.html
```

### Presentation Hierarchy (Slides → Whitepapers)

**Link from slides to detailed documentation:**
```markdown
# Conclusion

For detailed methodology and reproducibility:
→ [Technical Whitepaper](./whitepaper.pdf)
→ [GitHub Repository](https://github.com/tilmon/analysis)
```

**File Organization:**
```
analysis/
├── q4-2024/
│   ├── presentation.md (marp source)
│   ├── presentation.pdf (generated)
│   ├── whitepaper.md (pandoc source)
│   ├── whitepaper.pdf (generated)
│   ├── references.bib (bibliography)
│   ├── queries/
│   │   └── q4_analysis.sql
│   └── visualizations/
│       ├── revenue-chart.png
│       └── regional-breakdown.png
```

**Automation Script:**
```bash
#!/bin/bash
# generate_deliverables.sh

# Generate presentation
echo "Creating presentation..."
marp presentation.md -o presentation.pdf

# Generate whitepaper
echo "Creating whitepaper..."
pandoc whitepaper.md \
  --citeproc \
  --bibliography references.bib \
  --csl ieee.csl \
  -F pandoc-crossref \
  -s --toc --number-sections \
  -V geometry:margin=1in \
  -o whitepaper.pdf

echo "Deliverables created:"
echo "  - presentation.pdf (slides)"
echo "  - whitepaper.pdf (detailed report)"
```

**CHECKPOINT:** Final verification before delivery:
- [ ] Presentation PDF generated and reviewed
- [ ] Whitepaper PDF generated with citations and cross-references
- [ ] All visualizations properly embedded and sized
- [ ] Bibliography and references correctly formatted
- [ ] Reproducibility information complete
- [ ] Links between presentation and whitepaper working
- [ ] Files organized in analysis directory structure

---

## Integration with Process Skills

Process skills reference this component skill when presenting findings:

```markdown
Use the `presenting-data` component skill to create professional
deliverables from your analysis:
- Executive presentations (marp) for quick communication
- Technical whitepapers (pandoc) for detailed documentation
- Both formats with proper citations and reproducibility
```

When presenting analysis results:
1. **Choose format** based on audience (Phase 1)
2. **Structure narrative** using essay or story patterns (Phase 2)
3. **Create content** with marp/pandoc (Phase 3)
4. **Add citations** and reproducibility documentation (Phase 4)
5. **Generate outputs** for delivery (Phase 5)

**Typical Usage Contexts:**
- `exploratory-analysis` → Use presenting-data for final report
- `guided-investigation` → Use presenting-data to document findings
- `hypothesis-testing` → Use presenting-data to publish results
- `comparative-analysis` → Use presenting-data for comparison reports

---

## Quality Checklist

Before considering presentation complete:

**Content Quality:**
- [ ] Clear thesis or key finding stated upfront
- [ ] Supporting evidence logically organized
- [ ] Visualizations effectively communicate patterns
- [ ] Conclusions tied directly to evidence
- [ ] Limitations and caveats acknowledged

**Reproducibility:**
- [ ] Data sources fully documented
- [ ] SQL queries included or referenced
- [ ] Tool versions and environment documented
- [ ] Execution timestamps recorded
- [ ] Reproducibility instructions provided

**Citation Quality:**
- [ ] All data sources cited in bibliography
- [ ] Prior research properly attributed
- [ ] Analysis tools and versions documented
- [ ] Citation style consistent throughout
- [ ] Links to repositories and queries working

**Technical Quality:**
- [ ] Presentation PDF renders correctly
- [ ] Whitepaper PDF has working cross-references
- [ ] Images embedded and properly sized
- [ ] Code blocks have syntax highlighting
- [ ] Math equations render correctly (if applicable)

**Narrative Quality:**
- [ ] Introduction establishes context and question
- [ ] Body presents evidence systematically
- [ ] Conclusion restates findings clearly
- [ ] Bibliography enables drill-in for details
- [ ] Overall flow guides audience to conclusions

**Presentation-Whitepaper Hierarchy:**
- [ ] Slides provide high-level overview
- [ ] Whitepaper provides comprehensive details
- [ ] Links between formats working
- [ ] Consistent terminology and metrics
- [ ] Both reference same data sources

---

## Best Practices

### DO:
✅ Start with audience analysis to choose format
✅ Use 3-paragraph essay structure for clear narrative
✅ Include SQL queries for reproducibility
✅ Cite data sources in bibliography
✅ Create both slides and whitepaper for mixed audiences
✅ Link from presentations to detailed whitepapers
✅ Document environment, versions, and timestamps
✅ Use `creating-visualizations` for charts and diagrams
✅ Version control both source markdown and generated PDFs
✅ Test reproducibility instructions before delivery

### DON'T:
❌ Skip audience analysis - format should match need
❌ Present findings without methodology documentation
❌ Forget to cite data sources and prior research
❌ Generate PDFs without reviewing output quality
❌ Mix presentation styles (stay consistent)
❌ Overcomplicate slides with too much detail
❌ Omit reproducibility information
❌ Assume audience can recreate analysis without documentation
❌ Ignore cross-references and internal links
❌ Deliver without validating bibliography formatting
