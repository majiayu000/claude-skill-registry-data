---
name: office-pdf
description: 将 Office 文档导出 PDF，读取 PDF 内容并生成页面预览以核查版式。
---

# PDF 导出与预览

有可编辑源文件时先制作或修改 DOCX、PPTX、XLSX，再使用 `render_document` 导出 PDF。简单 PDF 可以使用现有 `write_artifact`；不通过修改扩展名转换格式。

- Office 导出：`render_document({ artifactId, format: 'pdf' })`，或指定授权工作目录的 `path`。
- 页面预览：`render_document({ artifactId, format: 'png', pages: [1, 2] })`，适用于 PDF、Word 和 PowerPoint。
- Excel 预览：使用准确 `sheet` 名称和可选 A1 `range`；工作表不使用页码参数。
- PNG 成果使用 `read_artifact` 提供给可识图模型；查看实际文字、页边距、图表、换行和遮挡。
- 使用 `read_artifact` 或 `read_file` 提取 PDF 正文，核对关键内容。扫描 PDF 没有文本时，不声称已完成文字提取。

一次先检查少量代表性页面，再按内容继续检查。转换返回的缺失字体需要查看其实际排版影响。未完成视觉检查时明确标注；最终 PDF 与可编辑源文件一起交付。
