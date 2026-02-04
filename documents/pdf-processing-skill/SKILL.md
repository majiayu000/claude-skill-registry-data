---
name: pdf-processing          # Skill唯一标识（小写+连字符，必选）
description: 提取PDF文件中的文本，并按标题/段落结构化输出。适用于文档总结、数据提取等场景。 # Skill功能描述（必选）
---

# PDF文本提取技能

## 概述
本Skill用于从PDF文件中提取文本，并按照“标题→子标题→段落”的层级结构化输出。支持处理多页PDF，自动忽略页眉/页脚。

## 工作流程
1. **上传PDF**：用户将PDF文件上传至Claude Code或Claude.ai；
2. **提取文本**：调用`scripts/extract_text.py`脚本，提取PDF中的所有文本；
3. **结构化处理**：按换行符和标题层级（如“# 标题”“## 子标题”）拆分内容；
4. **输出结果**：根据`templates/output_template.md`生成结构化Markdown文档。

## 使用示例
输入：上传一份“2024年年度报告.pdf”  
输出：生成包含“1. 公司概况→1.1 业务范围→段落”的结构化总结。

## 依赖说明
- Python库：PyPDF2（用于PDF文本提取），需提前安装（`pip install pypdf2`）。