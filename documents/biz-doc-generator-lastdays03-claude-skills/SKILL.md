---
name: biz-doc-generator
description: Standards for generating enterprise documents (Word, Excel, PDF) using Template-First architecture.
---

# Business Document Generator Standards

## Core Principles
**"Template-First, Code-Second"**
We do NOT draw documents line-by-line with code. We inject data into pre-designed templates.

1.  **Separation of Concerns**: 
    - **Design**: Managed in `.docx` / `.xlsx` / `.html` files.
    - **Logic**: Managed in Python scripts using `Golden Stack` libraries.
2.  **Golden Tech Stack**:
    - **Word (.docx)**: **`docxtpl`** (Essential). use `{{ jinja2_tags }}` in Word.
    - **Excel (.xlsx)**: **`openpyxl`**. For preserving existing styles/formulas.
    - **PowerPoint (.pptx)**: **`python-pptx`**. Standard for slide generation.
    - **PDF**: **`WeasyPrint`** (HTML+CSS -> PDF). Best for styling and maintenance.
3.  **Output & Hygiene**:
    - **Output Path**: All final files MUST be saved to `docs/exports/`.
    - **Cleanup Policy**: All temporary scripts and templates MUST be deleted after successful generation (`rm script.py template.docx`).
3.  **Korean Font Safety 🇰🇷**:
    - Always strictly define fonts (e.g., NanumGothic) in CSS/Style to prevent `□□□` (tofu) errors.

## Quality Standards
- **Validation**: Generated files must be checked for existence and non-zero size.
- **Context-Aware**: The agent must clearly define the `context` dictionary before writing code.
- **Dependency Check**: Ensure libraries (`docxtpl`, `openpyxl`, `weasyprint`) are installed or prompted.

## Phase 1: Design & Spec 📝
- **Objective**: Define the "Contract" between Template and Code.
- **Action**:
    1.  Inspect User Request.
    2.  Define **Context Variables** (e.g., `user_name`, `total_revenue`, `item_list`).
    3.  Check if a template exists. If not, generate a "Base Template" creation script first.

## Phase 2: Implementation 💻
- **Word (`docxtpl`)**:
    ```python
    from docxtpl import DocxTemplate
    doc = DocxTemplate("template.docx")
    context = { 'key': 'value' }
    doc.render(context)
    doc.save("output.docx")
    ```
- **Excel (`openpyxl`)**:
    ```python
    import openpyxl
    wb = openpyxl.load_workbook("template.xlsx")
    ws = wb.active
    ws['B2'] = "New Value"
    wb.save("output.xlsx")
    ```
- **PDF (`WeasyPrint`)**:
    ```python
    from weasyprint import HTML
    HTML(string=html_content).write_pdf("docs/exports/output.pdf")
    ```
- **PowerPoint (`python-pptx`)**:
    > [!IMPORTANT]
    > Refer to [`STANDARD_TEMPLATE_SPEC.md`](.agent/references/biz-doc-generator/STANDARD_TEMPLATE_SPEC.md) for Layout Indices and Cleanup rules.
    ```python
    from pptx import Presentation
    
    TEMPLATE_PATH = ".agent/references/biz-doc-generator/templates/standard_biz_template.pptx" 
    prs = Presentation(TEMPLATE_PATH)
    
    # [CRITICAL] Remove existing instructional slides SAFELY
    # Must iterate backwards and drop relationships to prevent file corruption
    if len(prs.slides) > 0:
        for i in range(len(prs.slides) - 1, -1, -1):
            rId = prs.slides._sldIdLst[i].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[i]
        
    prs.save("docs/exports/output.pptx")
    ```

## Phase 3: Verification ✅
- **Self-Check**:
    - Did I use a template? (If I used `add_paragraph` loops, I failed).
    - Did I handle Korean fonts? (For PDF).
    - Is the output file saved correctly?

## Checklist
- [ ] **Stack Check**: Am I using `docxtpl` / `openpyxl` / `python-pptx` / `WeasyPrint`?
- [ ] **Path Check**: Is the output pointing to `docs/exports/`?
- [ ] **Cleanup**: Did I schedule deletion of temp files?
- [ ] **Template**: Is there a template available or being created?
- [ ] **Font**: (PDF only) Is a Korean font explicitly specified in CSS?
