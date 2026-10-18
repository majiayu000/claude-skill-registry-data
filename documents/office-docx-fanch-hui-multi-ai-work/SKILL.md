---
name: office-docx
description: 制作、修改并检查 Word 文档，导出 PDF 和页面预览。
---

# Word 文档

先调用 `load_workspace_dependencies`，使用返回的 Python、检查脚本和字体路径。使用 `run_command` 执行工作目录中的脚本，命令和文件访问由 App 权限管理。

## 制作和修改

使用随包 `python-docx`。设置纸张、页边距、标题层级、正文样式、页眉页脚和表格列宽；图片按版心缩放，保持宽高比。中文字体可使用随包的 `Noto Sans CJK SC`。

修改已有文档先读取并检查原文档，使用 `Document(input_path)` 修改实际段落、表格、图片或节属性。默认另存为新文件，避免重建整个文档丢失现有内容。复杂对象不能保证保真，交付时说明实际发现的限制。

```python
from docx import Document
from docx.shared import Cm, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.top_margin = section.bottom_margin = Cm(2)
normal = doc.styles['Normal']
normal.font.name = 'Noto Sans CJK SC'
normal.font.size = Pt(11)
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'Noto Sans CJK SC')
doc.add_heading('工作报告', 0)
doc.add_paragraph('这里放经过核实的正文。')
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.rows[0].cells[0].text = '项目'
table.rows[0].cells[1].text = '结果'
doc.save(output_path)
```

## 验证和交付

执行 `[python, '-I', '-B', checkOffice, document, '--contains', expected_text]` 校验实际文件。需要可视预览时使用 `render_document`，PDF 导出选 `format: 'pdf'`，图片预览选 `format: 'png'` 和一开始的少量页码；按需继续查看其他页面。

将最终 DOCX 使用 `register_artifact` 登记。使用可识图模型读取预览成果，检查换行、表格、图片和页边距。结构检查通过不代表版式通过，未做视觉检查时如实说明。
