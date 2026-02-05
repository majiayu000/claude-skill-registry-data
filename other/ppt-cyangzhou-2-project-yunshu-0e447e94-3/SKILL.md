---
id: ppt
name: ppt生成大师
version: 1.0.0
author: Yunshu
description: 可以直接通过大模型生成ppt文件。支持从 Markdown 大纲自动转换为 PowerPoint 演示文稿。
icon: 📊
color: "#D04423"
tags: [custom, office, productivity]
entry_point: tools.SkillTools
workspace_root: ../../../Data
input:
  - name: markdown_content
    type: textarea
    label: PPT内容大纲 (Markdown)
    placeholder: "# 标题\n## 子标题\n- 第一页要点1\n- 第一页要点2\n\n# 第二页标题\n- 内容..."
    required: true
    default: ""
  
  - name: filename
    type: text
    label: 文件名
    placeholder: "presentation.pptx"
    required: false
    default: "output.pptx"
---

# ppt生成大师

本技能可以将 Markdown 格式的大纲直接转换为 PowerPoint (.pptx) 文件。

## 使用说明
1. **准备内容**：在输入框中粘贴您的 PPT 大纲。
   - 使用一级标题 `#` 作为每一页的标题。
   - 使用列表 `-` 作为页面的正文内容。
2. **生成**：点击执行，系统将自动生成 PPT 文件。

## Markdown 格式示例
```markdown
# 2024年度工作汇报
- 汇报人：张三
- 部门：技术部

# 项目进展概览
- 完成了核心模块开发
- 性能提升 30%
- 修复了 50+ Bug

# 下一步计划
- 启动二期工程
- 优化用户体验
```
