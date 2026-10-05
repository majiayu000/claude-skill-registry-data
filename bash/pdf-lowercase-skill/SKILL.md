---
name: pdf-case-converter
description: 将 PDF 文件的内容转换为小写 (PDF to Lowercase)
allowed-tools: Bash
---

# PDF Case Converter Skill

## Description
这是一个用于处理 PDF 文件的工具，专门用于将 PDF 中的文本内容转换为小写。它通过调用本地的 Python 脚本来完成转换。

## Instructions
当用户请求将某个 PDF 文件的内容转换为小写时，请遵循以下步骤：

1.  **检查文件路径**：确认用户提供的输入文件路径存在。
2.  **构建输出路径**：如果用户没有指定输出路径，默认在原文件名后加上 `_lower` 后缀（例如 `input.pdf` -> `input_lower.pdf`）。
3.  **执行脚本**：
    在当前文件所在的目录下，使用 `Bash` 工具运行以下命令：
    ```bash
    python3 scripts/pdf_lowercase.py <输入文件路径> <输出文件路径>
    ```
4.  **验证结果**：脚本执行完成后，检查输出文件是否生成成功，并向用户报告结果。

## Examples
**User:** "把 document.pdf 里的字都变成小写。"
**Assistant:** (Executing Bash from this file's directory) `python3 scripts/pdf_lowercase.py document.pdf document_lower.pdf`