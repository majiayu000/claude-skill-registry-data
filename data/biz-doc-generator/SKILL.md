---
name: biz-doc-generator
description: Word, Excel, PPT, PDF 등 기업용 문서를 생성하고, 결과를 docs/exports에 저장하며 임시파일을 자동 정리합니다.
---

# 비즈니스 문서 생성기 (Biz Doc Generator)

이 워크플로우는 **Template-First** 접근 방식을 사용하여 코드로 문서를 그리는 대신, 데이터 주입에 집중합니다.

## 1. 기획 및 스펙 정의 (Phase 1: Design)
1.  **Load Standard**: `this document`를 읽어 Golden Stack을 로드합니다.
2.  **Analyze Request**: 사용자의 요청에서 문서 타입과 필요한 데이터(Context)를 식별합니다.
3.  **Define Spec**: `templates/context-spec-template.md`를 사용하여 변수 명세를 작성합니다.
4.  **Check Template**:
    - 사용할 템플릿 파일이 존재하는지 확인합니다.
    - **없다면**: "기본 템플릿 생성" 단계를 먼저 수행할 것을 제안합니다.

## 2. 코드 구현 (Phase 2: Implementation)
1.  **Select Library**:
    - Word: `docxtpl`
    - Excel: `openpyxl`
    - PPT: `python-pptx`
    - PDF: `WeasyPrint`
2.  **Prepare Environment**:
    - 출력 폴더 `docs/exports`가 없으면 생성합니다.
3.  **Generate Code**: 데이터 컨텍스트를 주입하는 Python 코드를 작성합니다.
    - **스타일 주의**: 하드코딩된 스타일 대신 템플릿의 스타일을 따르도록 합니다.
    - **PDF 주의**: 한글 폰트 설정 코드를 반드시 포함합니다.

## 3. 실행 및 검증 (Phase 3: Execution)
1.  **Run Script**: 작성된 파이썬 스크립트를 실행합니다.
2.  **Verify Output**:
    - 파일이 생성되었는지 확인합니다 (`ls -l`).
    - 파일 크기가 0이 아닌지 확인합니다.
3.  **Delivery**: 
    - 생성된 파일의 절대 경로(`docs/exports/...`)를 사용자에게 알립니다.
    - **Cleanup**: 생성에 사용된 임시 스크립트와 템플릿 파일을 삭제합니다.


---

## Standards & Rules

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
    > Refer to [`STANDARD_TEMPLATE_SPEC.md`](resources/STANDARD_TEMPLATE_SPEC.md) for Layout Indices and Cleanup rules.
    ```python
    from pptx import Presentation
    
    TEMPLATE_PATH = "resources/templates/standard_biz_template.pptx" 
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
