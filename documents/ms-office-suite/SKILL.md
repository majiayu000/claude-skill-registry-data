---
name: ms-office-suite
description: >
  Generate professional Excel workbooks, Word documents, PowerPoint decks, and PDFs,
  including CPA-grade financial reports, cost analyses, ROI projections, executive
  summaries, budgets, and break-even reports. Uses python-docx, openpyxl, python-pptx,
  reportlab, weasyprint, and Markdown. Use when asked to generate a report, spreadsheet,
  PDF, pitch deck, presentation, financial projection, cloud-cost analysis, or other
  Microsoft Office-style deliverable.
---

# MS Office Suite — Document Generation Skill

Generate professional-grade documents: Excel workbooks, Word docs, PowerPoint decks, and PDFs. Optimized for CPA-quality financial reports.

## Dependencies

Install per-project in `pyproject.toml` (or standalone venv):

```toml
[project.optional-dependencies]
reports = [
    "python-docx>=1.1.0",
    "openpyxl>=3.1.0",
    "python-pptx>=0.6.23",
    "reportlab>=4.0",
    "weasyprint>=62.0",
    "matplotlib>=3.8.0",
    "markdown>=3.6",
]
```

Standalone install: `uv pip install python-docx openpyxl python-pptx reportlab weasyprint matplotlib markdown`

## Output Conventions

- Reports go to `<project>/reports/` directory
- Filename: `<project>-<report-type>-<YYYY-MM-DD>.{pdf,xlsx,docx,pptx}`
- Always generate both source format AND PDF (e.g., XLSX + PDF)
- Include generation timestamp in document footer

## Excel Workbooks (openpyxl)

### Cost Comparison Matrix

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

def create_cost_workbook(project_name: str, data: dict) -> str:
    """Generate a multi-sheet cost comparison workbook.

    Args:
        project_name: e.g. "sample-app"
        data: {
            "tiers": ["Starter", "Growth", "Scale"],
            "providers": ["AWS", "Azure", "GCP", "OCI", "Hetzner"],
            "costs": {
                "Starter": {"AWS": {"compute": 25, "db": 15, "storage": 5, ...}, ...},
                ...
            },
            "revenue": {"conservative": 500, "base": 2000, "optimistic": 5000}
        }
    """
    wb = Workbook()

    # Style constants
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    money_fmt = '#,##0.00'
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # Sheet 1: Summary comparison
    ws = wb.active
    ws.title = "Summary"
    # ... build summary with totals per tier per provider

    # Sheet per tier: detailed line items
    for tier in data["tiers"]:
        ws = wb.create_sheet(title=tier)
        # Row headers: cost categories (compute, db, storage, network, CDN, DNS, SSL, monitoring, backup)
        # Columns: one per provider
        # Bottom rows: monthly total, annual total, break-even months

    # Sheet: ROI Analysis
    ws = wb.create_sheet(title="ROI Analysis")
    # Three scenarios: conservative, base, optimistic
    # Rows: monthly revenue, monthly cost (per tier), net margin, break-even month
    # Charts: bar chart comparing tiers, line chart for cumulative P&L

    # Sheet: Hidden Costs
    ws = wb.create_sheet(title="Hidden Costs")
    # Data transfer, DNS, SSL certs, log retention, backup storage, support plans

    path = f"reports/{project_name}-cloud-cost-{date.today()}.xlsx"
    wb.save(path)
    return path
```

### Key openpyxl Patterns

```python
# Conditional formatting — highlight cheapest provider per row
from openpyxl.formatting.rule import CellIsRule
ws.conditional_formatting.add(
    f"B2:{get_column_letter(col_count)}{row_count}",
    CellIsRule(operator="equal", formula=["MIN($B2:$F2)"],
              fill=PatternFill(bgColor="C6EFCE"))
)

# Auto-fit column widths (approximate)
for col in ws.columns:
    max_len = max(len(str(cell.value or "")) for cell in col)
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 30)

# Freeze panes (headers always visible)
ws.freeze_panes = "B2"

# Number formatting
for row in ws.iter_rows(min_row=2, min_col=2):
    for cell in row:
        cell.number_format = money_fmt
```

### Chart Generation

```python
# Bar chart comparing providers
chart = BarChart()
chart.type = "col"
chart.title = f"{tier} Tier — Monthly Cost by Provider"
chart.y_axis.title = "USD/month"
chart.y_axis.numFmt = '$#,##0'
data_ref = Reference(ws, min_col=2, max_col=col_count, min_row=1, max_row=row_count)
cats_ref = Reference(ws, min_col=1, min_row=2, max_row=row_count)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
chart.shape = 4
ws.add_chart(chart, "H2")
```

## Word Documents (python-docx)

### Executive Summary / Memo

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_memo(title: str, sections: list[dict]) -> str:
    """Generate a professional memo/report.

    sections: [{"heading": "...", "body": "...", "table": [[...]], "bullet_points": [...]}]
    """
    doc = Document()

    # Title
    title_para = doc.add_heading(title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadata line
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = meta.add_run(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | CONFIDENTIAL")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(128, 128, 128)

    doc.add_paragraph()  # spacer

    for section in sections:
        doc.add_heading(section["heading"], level=1)

        if "body" in section:
            doc.add_paragraph(section["body"])

        if "bullet_points" in section:
            for point in section["bullet_points"]:
                doc.add_paragraph(point, style="List Bullet")

        if "table" in section:
            rows, cols = len(section["table"]), len(section["table"][0])
            table = doc.add_table(rows=rows, cols=cols, style="Light Shading Accent 1")
            for i, row_data in enumerate(section["table"]):
                for j, cell_val in enumerate(row_data):
                    table.rows[i].cells[j].text = str(cell_val)

    # Footer
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = f"{title} — Page "
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    path = f"reports/{title.lower().replace(' ', '-')}-{date.today()}.docx"
    doc.save(path)
    return path
```

## PDF Generation

### Option 1: weasyprint (HTML/CSS → PDF) — best for styled reports

```python
from weasyprint import HTML

def html_to_pdf(html_content: str, output_path: str, css: str = None):
    """Convert HTML string to PDF. Supports full CSS3."""
    stylesheets = []
    if css:
        from weasyprint import CSS
        stylesheets = [CSS(string=css)]
    HTML(string=html_content).write_pdf(output_path, stylesheets=stylesheets)

# CPA report CSS
REPORT_CSS = """
@page { size: letter; margin: 1in; }
body { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 10pt; color: #333; }
h1 { color: #2F5496; border-bottom: 2px solid #2F5496; padding-bottom: 8px; }
h2 { color: #2F5496; margin-top: 24px; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; }
th { background: #2F5496; color: white; padding: 8px 12px; text-align: left; }
td { padding: 6px 12px; border-bottom: 1px solid #ddd; }
tr:nth-child(even) { background: #f8f9fa; }
.money { text-align: right; font-family: 'Courier New', monospace; }
.disclaimer { font-size: 8pt; color: #888; margin-top: 32px; border-top: 1px solid #ddd; padding-top: 8px; }
.conservative { color: #c0392b; font-weight: bold; }
.assumption { background: #fff3cd; padding: 8px; border-left: 4px solid #ffc107; margin: 12px 0; }
"""
```

### Option 2: reportlab — best for programmatic layouts with charts

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf_report(title: str, tables: list, charts: list, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(name='ReportTitle', parent=styles['Title'],
                              textColor=colors.HexColor('#2F5496'), fontSize=18))
    styles.add(ParagraphStyle(name='Disclaimer', parent=styles['Normal'],
                              textColor=colors.grey, fontSize=7))

    elements = [Paragraph(title, styles['ReportTitle']), Spacer(1, 12)]

    for table_data in tables:
        t = Table(table_data["rows"], colWidths=table_data.get("widths"))
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F5496')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    # Embed matplotlib charts as images
    for chart_path in charts:
        elements.append(Image(chart_path, width=6*inch, height=3*inch))
        elements.append(Spacer(1, 12))

    doc.build(elements)
```

### Matplotlib Charts for PDF Embedding

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def cost_comparison_chart(providers: list, costs: dict, output_path: str):
    """Bar chart: providers on x-axis, cost categories stacked."""
    fig, ax = plt.subplots(figsize=(8, 4))
    categories = list(next(iter(costs.values())).keys())
    x = range(len(providers))
    bottom = [0] * len(providers)

    colors = ['#2F5496', '#4472C4', '#5B9BD5', '#A5C8E1', '#D6E4F0', '#ED7D31', '#FFC000']
    for i, cat in enumerate(categories):
        values = [costs[p][cat] for p in providers]
        ax.bar(x, values, bottom=bottom, label=cat, color=colors[i % len(colors)])
        bottom = [b + v for b, v in zip(bottom, values)]

    ax.set_xticks(x)
    ax.set_xticklabels(providers)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
    ax.set_ylabel('Monthly Cost (USD)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def breakeven_chart(months: range, revenue: dict, cost: float, output_path: str):
    """Line chart: cumulative revenue vs cost over time."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for scenario, monthly in revenue.items():
        cumulative = [monthly * m - cost * m for m in months]
        style = '--' if scenario == 'conservative' else '-' if scenario == 'base' else ':'
        ax.plot(months, cumulative, style, label=f'{scenario} (${monthly}/mo)')

    ax.axhline(y=0, color='red', linestyle='-', alpha=0.3)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
    ax.set_xlabel('Months')
    ax.set_ylabel('Cumulative Profit/Loss')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

## PowerPoint Decks (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_deck(title: str, slides_data: list[dict]) -> str:
    """Generate a presentation deck.

    slides_data: [
        {"layout": "title", "title": "...", "subtitle": "..."},
        {"layout": "content", "title": "...", "bullets": ["..."]},
        {"layout": "table", "title": "...", "table": [[...]]},
        {"layout": "chart", "title": "...", "chart_image": "path.png"},
    ]
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9
    prs.slide_height = Inches(7.5)

    for slide_data in slides_data:
        layout_idx = {"title": 0, "content": 1, "blank": 6}.get(slide_data["layout"], 1)
        slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])

        if "title" in slide_data and slide.shapes.title:
            slide.shapes.title.text = slide_data["title"]

        if slide_data["layout"] == "chart" and "chart_image" in slide_data:
            slide.shapes.add_picture(
                slide_data["chart_image"],
                Inches(1), Inches(1.5), Inches(11), Inches(5.5)
            )

        if slide_data["layout"] == "table":
            table_data = slide_data.get("table")
            if not table_data or not table_data[0]:
                raise ValueError("table slides require a non-empty 'table' matrix")

            column_count = len(table_data[0])
            if any(len(row) != column_count for row in table_data):
                raise ValueError("table slides require rows with equal column counts")

            table = slide.shapes.add_table(
                len(table_data),
                column_count,
                Inches(0.75),
                Inches(1.5),
                Inches(11.8),
                Inches(5.25),
            ).table
            for row_index, row_data in enumerate(table_data):
                for column_index, value in enumerate(row_data):
                    cell = table.cell(row_index, column_index)
                    cell.text = str(value)
                    if row_index == 0:
                        for run in cell.text_frame.paragraphs[0].runs:
                            run.font.bold = True

        if "bullets" in slide_data:
            tf = slide.placeholders[1].text_frame
            for i, bullet in enumerate(slide_data["bullets"]):
                if i == 0:
                    tf.text = bullet
                else:
                    p = tf.add_paragraph()
                    p.text = bullet

    path = f"reports/{title.lower().replace(' ', '-')}-{date.today()}.pptx"
    prs.save(path)
    return path
```

## CPA-Grade Financial Report Rules

These rules are NON-NEGOTIABLE for any financial document:

1. **Three-scenario projections**: Always show Conservative, Base, and Optimistic. Label which is which. Default to Conservative for headline numbers.

2. **Source every cost figure**: Include footnotes or inline citations. "AWS RDS db.t3.medium: $X/mo (us-east-1, on-demand, retrieved YYYY-MM-DD)"

3. **No vanity metrics**: No TAM/SAM/SOM unless backed by real data. No "if we capture just 1% of the market" reasoning.

4. **Unit economics first**: CAC (customer acquisition cost), LTV (lifetime value), gross margin, burn rate. If unknown, say "TBD — requires market testing."

5. **Hidden costs**: Always include data transfer, DNS, SSL, monitoring, logging, backups, support plans. These typically add 15-30% to base compute+DB costs.

6. **Self-hosted baseline**: For projects running on existing infrastructure, compare cloud cost to the marginal cost of self-hosting (compute + electricity costs at typical rates).

7. **Break-even analysis**: For each tier, show months to break-even at each revenue scenario. If break-even exceeds 24 months at base case, flag it.

8. **Assumptions box**: Every report gets a clearly labeled "Key Assumptions" section listing what was assumed and what could change.

9. **Conservative by default**: When in doubt, round costs UP and revenue DOWN. finance/CPA reviewers immediately spot optimistic bias.

10. **Currency and precision**: USD, two decimal places for per-unit costs, whole dollars for monthly/annual totals.

## Markdown to PDF

```python
import markdown
from weasyprint import HTML

def markdown_to_pdf(md_content: str, output_path: str):
    """Convert markdown to styled PDF via HTML intermediate."""
    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    full_html = f"""<!DOCTYPE html>
    <html><head><style>{REPORT_CSS}</style></head>
    <body>{html_body}</body></html>"""
    HTML(string=full_html).write_pdf(output_path)
```

## Quick Reference — When to Use What

| Need | Tool | Best For |
|------|------|----------|
| Multi-sheet data with formulas | openpyxl (Excel) | Cost comparisons, financial models |
| Styled narrative report | weasyprint (HTML→PDF) | Executive summaries, legal memos |
| Programmatic layout with charts | reportlab (PDF) | One-pagers with embedded charts |
| Client-facing document | python-docx (Word) | Editable deliverables |
| Presentation | python-pptx (PPT) | Pitch decks, board presentations |
| Quick report from markdown | weasyprint + markdown | Internal reports, research memos |
