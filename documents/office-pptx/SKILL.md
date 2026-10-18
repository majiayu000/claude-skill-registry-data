---
name: office-pptx
description: 制作和修改 PowerPoint 演示，检查页数与内容，导出 PDF 和幻灯片预览。
---

# PowerPoint 演示

先调用 `load_workspace_dependencies`，使用随包 Python 与 `python-pptx`。在工作目录保存制作脚本，通过 `run_command` 执行。

## 制作和修改

默认 16:9，一页围绕一个明确结论。统一标题、正文、图表、留白和页码，正文不挤成小字；图表标签应带单位和来源。使用真实图片或清晰示意，不能用空占位框冒充完成成果。

修改时使用 `Presentation(input_path)`，调整原有文字、图片、表格和图表后另存为新文件。普通文本和布局支持直接修改；复杂动画、SmartArt 或嵌入对象必须在交付时说明实际兼容情况。

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

deck = Presentation()
deck.slide_width, deck.slide_height = Inches(13.333), Inches(7.5)
slide = deck.slides.add_slide(deck.slide_layouts[6])
title = slide.shapes.add_textbox(Inches(.6), Inches(.5), Inches(12), Inches(.7))
title.text = '季度工作进展'
paragraph = title.text_frame.paragraphs[0]
paragraph.font.name = 'Noto Sans CJK SC'
paragraph.font.size = Pt(30)
data = CategoryChartData()
data.categories = ['第一月', '第二月', '第三月']
data.add_series('完成量', [12, 18, 25])
slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(.8), Inches(1.8), Inches(10), Inches(4.6), data)
deck.save(output_path)
```

## 验证和交付

用 `checkOffice` 检查实际 PPTX 的文字和页数：`--contains TEXT --count N`。通过 `render_document` 导出 PDF 或生成选定幻灯片 PNG。可识图模型读取每种主要版式的预览，检查重叠、裁切、文字大小和图表标签；发现问题修改源文件并重渲染对应页面。

最终 PPTX 使用 `register_artifact` 登记，PDF 和预览由 `render_document` 登记。未完成视觉检查时明确说明。
