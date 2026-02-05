---
name: carbon.report.gen
description: Automate creation of structured carbon reports by pulling data from Carbon ACX datasets and formatting per template (monthly, quarterly, compliance, executive).
---

# carbon.report.gen

## Purpose

This skill enables Claude to automatically generate complete, professional carbon accounting reports by:

- Querying Carbon ACX data using `carbon.data.qa` skill (or directly from CSVs)
- Populating report templates with data, charts, and analysis
- Generating visualizations using matplotlib or plotly
- Ensuring all reports include units, sources, and provenance
- Following brand guidelines and formatting standards

Reports are saved as Markdown files (with optional PDF export) and include structured sections for executive summaries, key metrics, trends, and recommendations.

## When to Use

**Trigger Patterns:**
- "Generate a monthly carbon report for [month/year]"
- "Create a quarterly emissions summary"
- "I need a compliance report for [period]"
- "Prepare an executive carbon briefing"
- "Automate our carbon reporting"

**Do NOT Use When:**
- User asks analytical questions (use `carbon.data.qa` instead)
- User wants to write code (use `acx.code.assistant` instead)
- User wants custom reports not matching templates (may require template modification)

## Allowed Tools

- `read_file` - Read templates, data CSVs, existing reports
- `write_file` - Write generated report files
- `python` - Pull data, generate charts, populate templates
- `bash` - File system operations (create directories, check paths)

**Access Level:** 2 (File Modification - can create report files in designated output directory)

**Tool Rationale:**
- `read_file`: Required to load templates and source data
- `write_file`: Required to save generated reports
- `python`: Needed for data querying, chart generation (matplotlib), template rendering
- `bash`: Helpful for creating output directories and verifying paths

**Explicitly Denied:**
- `web_fetch` - No external data sources (use internal data only)
- `edit_file` - Templates should not be modified during report generation

## Expected I/O

**Input:**
- Type: Report request with parameters
- Format: Natural language or structured parameters
- Required Parameters:
  - Report type: monthly | quarterly | compliance | executive
  - Date range: "January 2025", "Q1 2024", "2024 annual", etc.
  - Optional: Focus areas, specific layers/sectors to highlight
- Example:
  ```
  "Generate a monthly carbon report for February 2025 focusing on digital infrastructure"
  ```

**Output:**
- Type: Markdown file (and optionally PDF)
- Format: Structured report following template
- Location: `reports/` directory (or user-specified path)
- Filename: `{report_type}_{period}_{timestamp}.md`
  - Example: `monthly_2025-02_20251015.md`
- Requirements:
  - All data must include units (tCO2e, kgCO2e, etc.)
  - Charts embedded as images (PNG/SVG)
  - Sources cited for all emission factors
  - Data provenance section at end
  - Executive summary at beginning

**Validation:**
- Report contains all required sections (see templates)
- All numeric values have units
- Charts have titles, axis labels, legends
- Data sources cited
- No placeholder/TODO text in final report

## Dependencies

**Required:**
- Python 3.11+ with pandas, matplotlib or plotly, jinja2
- Access to Carbon ACX `data/` directory
- Report templates in `.claude/skills/project/carbon-report-gen/templates/`
- Optionally: `carbon.data.qa` skill for data queries

**Data Dependencies:**
- `data/activities.csv`
- `data/emission_factors.csv`
- `data/sources.csv`
- `calc/outputs/` (derived artifacts, if available)

**Optional:**
- Pandoc for PDF generation
- Brand guidelines/logo files (if customization needed)

## Examples

### Example 1: Monthly Report Generation

**User:** "Generate a monthly carbon report for March 2025"

**Claude Process:**
1. Invoke `carbon.report.gen` skill
2. Load monthly report template from `templates/monthly_report.md.template`
3. Query data for March 2025 (or latest available data)
4. Calculate key metrics:
   - Total emissions by layer
   - Top 10 activities by emission intensity
   - Month-over-month changes (if previous month available)
5. Generate charts:
   - Emissions by layer (bar chart)
   - Top activities (horizontal bar)
   - Trend line (if historical data exists)
6. Populate template with data
7. Write to `reports/monthly_2025-03_20251018.md`

**Output File Structure:**
```markdown
# Monthly Carbon Report — March 2025

**Report Generated:** 2025-10-18
**Data Version:** v1.2
**Reporting Period:** March 2025

## Executive Summary

This report covers carbon accounting data for March 2025...

[Key findings bullet points]

## Key Metrics

| Metric | Value | Change from Feb 2025 |
|--------|-------|----------------------|
| Total Emissions | 145.2 tCO2e | +2.3% |
| ...

## Charts

![Emissions by Layer](./charts/monthly_2025-03_by_layer.png)

## Data Sources

All emission factors sourced from Carbon ACX dataset v1.2...
```

### Example 2: Quarterly Compliance Report

**User:** "Create a quarterly compliance report for Q1 2024"

**Claude Process:**
1. Load compliance report template
2. Aggregate data for Q1 (Jan-Mar 2024)
3. Calculate required compliance metrics
4. Generate detailed tables for regulatory reporting
5. Include data quality indicators (% with sources, vintage coverage)
6. Populate template
7. Save to `reports/compliance_2024-Q1_20251018.md`

**Output Sections:**
- Compliance Summary
- Scope 1/2/3 Breakdown (if applicable)
- Activity-Level Detail Table
- Verification Status
- Data Quality Metrics
- Attestation Section (placeholder for signature)

### Example 3: Executive Briefing

**User:** "Prepare an executive carbon briefing for the board"

**Claude Process:**
1. Load executive template (high-level, concise)
2. Query latest data across all layers
3. Calculate top-level KPIs
4. Identify 3-5 key insights
5. Generate executive-friendly visualizations (simplified charts)
6. Limit to 2-page equivalent
7. Save to `reports/executive_brief_2025-10-18.md`

**Output Focus:**
- One-paragraph summary
- 3-5 key metrics with visual indicators (↑↓)
- Single summary chart
- Top recommendations (3-5 bullets)
- No technical details

## Limitations

**Known Edge Cases:**
- Cannot generate reports for periods with no data
- Chart generation may fail if data is sparse or missing
- Templates are fixed - custom layouts require template modification
- PDF generation requires pandoc installation
- Large reports (100+ pages) may be slow to generate

**Performance Constraints:**
- Report generation: typically 10-30 seconds
- Chart generation: 2-5 seconds per chart
- Large dataset aggregations may take up to 1 minute

**Scope Limitations:**
- Only supports predefined template types
- Cannot perform predictive analysis or forecasting
- Does not provide compliance advice (data reporting only)
- Does not handle multi-organization consolidated reporting

**Data Quality Constraints:**
- Reports reflect data quality issues (missing EFs, sources)
- No automatic imputation of missing data
- Flags data gaps in quality section

## Validation Criteria

**Success Metrics:**
- ✅ Report file created in `reports/` directory
- ✅ All required sections present per template
- ✅ All numeric values have explicit units
- ✅ Charts have proper titles, axis labels, units, legends
- ✅ Data sources cited in References section
- ✅ No TODO or placeholder text in final report
- ✅ Calculations are correct and traceable
- ✅ Report is readable markdown (renders correctly)

**Failure Modes:**
- ❌ Missing required sections → REJECT
- ❌ Charts without labels/units → REJECT
- ❌ Numeric values without units → REJECT
- ❌ Placeholder text like "[INSERT DATA]" → REJECT
- ❌ Calculations with errors → REJECT
- ❌ Sources not cited → WARN

**Quality Checks:**
- Verify all charts saved to `reports/charts/` directory
- Verify markdown syntax is valid
- Verify all data matches source CSV files
- Verify date ranges match request

**Recovery:**
- If data missing for period: Note in report and use latest available
- If chart generation fails: Include data table instead
- If template missing: Ask user which template to use or use default

## Related Skills

**Dependencies:**
- `carbon.data.qa` - Can use this skill to query data before populating report

**Composes With:**
- Generate report → User reviews → Use `acx.code.assistant` to modify template if needed

**Alternative Skills:**
- For ad-hoc data queries: `carbon.data.qa`
- For code generation: `acx.code.assistant`

## Report Templates

### Available Templates

1. **Monthly Report** (`templates/monthly_report.md.template`)
   - Monthly emissions summary
   - Month-over-month trends
   - Top activities
   - 4-6 pages typical

2. **Quarterly Report** (`templates/quarterly_report.md.template`)
   - Quarterly aggregation
   - Quarter-over-quarter comparison
   - Sector/layer breakdowns
   - 8-12 pages typical

3. **Compliance Report** (`templates/compliance_report.md.template`)
   - Regulatory reporting format
   - Detailed activity-level tables
   - Data quality metrics
   - Verification sections
   - 15-25 pages typical

4. **Executive Brief** (`templates/executive_brief.md.template`)
   - High-level summary
   - Key metrics only
   - Minimal charts
   - 2-3 pages maximum

### Template Variables

All templates support Jinja2 variables:

- `{{ report_title }}` - Report title
- `{{ reporting_period }}` - Date range
- `{{ generation_date }}` - When report was generated
- `{{ data_version }}` - Carbon ACX dataset version
- `{{ total_emissions_tco2e }}` - Total emissions
- `{{ by_layer }}` - Emissions breakdown by layer (dict/table)
- `{{ by_sector }}` - Emissions breakdown by sector
- `{{ top_activities }}` - Highest emission activities (list)
- `{{ charts }}` - Dictionary of chart file paths
- `{{ sources }}` - List of data sources
- `{{ data_quality }}` - Data quality metrics

## Chart Specifications

See `reference/chart_specs.md` for detailed chart styling guidelines.

**Standard Charts:**
- Emissions by Layer (bar chart)
- Emissions by Sector (pie chart)
- Top 10 Activities (horizontal bar)
- Trend Over Time (line chart)
- Scope Breakdown (stacked bar)

**Chart Requirements:**
- Size: 800x600 px (standard), 1200x800 (executive)
- Format: PNG (embedded) or SVG (for vector scaling)
- Font: Sans-serif, minimum 10pt
- Colors: Consistent palette (see `reference/chart_specs.md`)
- Units: Always on axis labels
- Legend: Include when multiple series
- Title: Descriptive, includes units and period

## Maintenance

**Owner:** ACX Team
**Review Cycle:** Monthly (align with dataset releases)
**Last Updated:** 2025-10-18
**Version:** 1.0.0

**Maintenance Notes:**
- Update templates when reporting requirements change
- Add new template types as needed
- Keep chart specs synchronized with brand guidelines
- Review example reports quarterly for quality
- Update when data schema changes
