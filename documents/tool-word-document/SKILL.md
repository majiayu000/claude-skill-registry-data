---
name: tool-word-document
description: Read and write Microsoft Word (.docx) documents using python-docx — extract text and tables, create or edit documents. Use when the user says "read this docx", "make a Word doc", or "edit the .docx". NOT for PDFs (use tool-pdf-reader) or rendering styled PDFs from markdown (use the emptyos sdk/pdf.py profile).
---

# Word Document Skill

读写 Microsoft Word (.docx) 文档。

**依赖**: `python-docx` (pip install python-docx)

---

## 触发词

| User Says | Action |
|-----------|--------|
| "读取 Word" / "read docx" | 提取 Word 内容 |
| "导出 Word" / "export to Word" | 从 Markdown 创建 Word |
| "创建 Word 简历" | 生成格式化简历 |

---

## 1. 读取 Word 文档

### 提取所有文本（段落 + 表格）

```python
python -X utf8 << 'EOF'
from docx import Document

doc = Document(r"path/to/file.docx")

# 提取段落
print("=== 段落 ===")
for p in doc.paragraphs:
    if p.text.strip():
        print(p.text)

# 提取表格
print("\n=== 表格 ===")
for table in doc.tables:
    for row in table.rows:
        row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
        if row_text:
            print(" | ".join(row_text))
EOF
```

### 提取带格式信息

```python
python -X utf8 << 'EOF'
from docx import Document

doc = Document(r"path/to/file.docx")

for p in doc.paragraphs:
    if p.text.strip():
        style = p.style.name if p.style else "Normal"
        is_bold = any(run.bold for run in p.runs)
        print(f"[{style}] {'**' if is_bold else ''}{p.text}{'**' if is_bold else ''}")
EOF
```

---

## 2. 创建 Word 文档

### 基础模板

```python
python -X utf8 << 'EOF'
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

# 设置中文字体
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

# 标题
title = doc.add_paragraph()
title_run = title.add_run('文档标题')
title_run.bold = True
title_run.font.size = Pt(18)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 正文
doc.add_paragraph('这是正文内容。')

# 列表
doc.add_paragraph('列表项 1', style='List Bullet')
doc.add_paragraph('列表项 2', style='List Bullet')

# 表格
table = doc.add_table(rows=2, cols=3)
table.style = 'Table Grid'
table.rows[0].cells[0].text = '列1'
table.rows[0].cells[1].text = '列2'
table.rows[0].cells[2].text = '列3'

doc.save(r'output.docx')
print('文档已保存')
EOF
```

---

## 3. 常用格式操作

### 字体设置

```python
from docx.shared import Pt, RGBColor

run = paragraph.add_run('文本')
run.bold = True                          # 粗体
run.italic = True                        # 斜体
run.underline = True                     # 下划线
run.font.size = Pt(14)                   # 字号
run.font.color.rgb = RGBColor(255, 0, 0) # 颜色
run.font.name = '微软雅黑'                # 字体
```

### 段落对齐

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 居中
paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT    # 左对齐
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT   # 右对齐
```

### 页边距

```python
from docx.shared import Inches

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
```

---

## 4. 简历模板

专用于生成中文简历的完整代码：

```python
python -X utf8 << 'EOF'
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def create_resume(data, output_path):
    """
    data = {
        'name': '姓名',
        'title': '求职意向',
        'info': [['姓名', '值', '性别', '男'], ...],  # 4列表格
        'evaluation': ['评价1', '评价2', ...],
        'skills': [['类别', '技能'], ...],
        'work': [{'company': '', 'role': '', 'time': '', 'desc': ''}],
        'projects': [{'name': '', 'time': '', 'duties': []}],
        'education': {'school': '', 'time': '', 'major': '', 'degree': ''},
        'certs': ['证书1', ...],
        'clients': '客户列表文字'
    }
    """
    doc = Document()

    # 设置中文字体
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(11)
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    # 姓名标题
    title = doc.add_paragraph()
    title_run = title.add_run(data['name'])
    title_run.bold = True
    title_run.font.size = Pt(22)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 求职意向
    subtitle = doc.add_paragraph()
    subtitle_run = subtitle.add_run(f"求职意向：{data['title']}")
    subtitle_run.font.size = Pt(14)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ... 其他部分类似

    doc.save(output_path)
    return output_path

# 使用示例
# create_resume(data, 'resume.docx')
EOF
```

---

## 5. 注意事项

### Windows 路径

```python
# 使用原始字符串避免转义问题
path = r"{vault}\file.docx"

# 或使用正斜杠
path = "{vault}/file.docx"
```

### 中文编码

```bash
# 运行时加 -X utf8 避免编码错误
python -X utf8 script.py
```

### 字体兼容性

| 系统 | 推荐字体 |
|------|----------|
| Windows | 微软雅黑、宋体 |
| macOS | PingFang SC、华文黑体 |
| Linux | Noto Sans CJK SC |

---

## 6. 常见问题

### Q: 读取时乱码
A: 确保使用 `python -X utf8`，或设置环境变量 `PYTHONUTF8=1`

### Q: 字体不显示
A: 检查系统是否安装该字体，或使用系统默认字体

### Q: 表格边框不显示
A: 添加 `table.style = 'Table Grid'`

---

## 7. PDF 导出

**依赖**: `docx2pdf` (pip install docx2pdf) + Microsoft Word

```python
from docx2pdf import convert

# 单个文件
convert(r'D:\path\to\file.docx', r'D:\path\to\file.pdf')

# 整个文件夹
convert(r'D:\path\to\folder')
```

---

## 8. 双栏侧边栏布局（简历常用）

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement

doc = Document()

# 辅助函数：单元格背景色
def set_cell_shading(cell, color):
    """color: 6位16进制，如 '3D6B6B'"""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

# 辅助函数：段落背景色
def set_paragraph_shading(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    pPr.append(shd)

# 辅助函数：移除单元格边框
def remove_cell_borders(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'nil')
        tcBorders.append(border)
    tcPr.append(tcBorders)

# 创建双栏表格
main_table = doc.add_table(rows=1, cols=2)
main_table.autofit = False

left_cell = main_table.rows[0].cells[0]
right_cell = main_table.rows[0].cells[1]

# 设置列宽
left_cell.width = Cm(6.5)
right_cell.width = Cm(13.5)

# 左栏深色背景
remove_cell_borders(left_cell)
remove_cell_borders(right_cell)
set_cell_shading(left_cell, '3D6B6B')  # 深青色

# 垂直顶部对齐
left_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
right_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

# 左栏添加内容（白色文字）
p = left_cell.add_paragraph()
run = p.add_run('姓名')
run.font.color.rgb = RGBColor(255, 255, 255)

# 左栏分节标题（浅色背景条）
section = left_cell.add_paragraph()
sec_run = section.add_run(' 基本信息')
sec_run.bold = True
sec_run.font.color.rgb = RGBColor(0x3D, 0x6B, 0x6B)
set_paragraph_shading(section, 'E8F4F4')  # 浅青色

# 右栏正常内容
right_cell.add_paragraph('自我评价...')

doc.save('two_column_resume.docx')
```

**完整示例**: 见 `10_Projects/卞萱简历/generate_resume_v5.py`

---

## 相关 Skills

- `note-factory` - 创建 Markdown 笔记
- `obsidian-format` - Markdown 格式规范
