---
slug: deskclaw-docx
version: 3.0.0
displayName: 官方 Word 文档操作（DeskClaw DOCX）
summary: "DeskClaw 自研 Word 全能工具。基于 docx-js 创建、python-docx 读取、OOXML unpack/repack 编辑、LibreOffice 校验与格式转换；支持红线审阅、评论、接受修订与中文排版规范。"
tags: office, docx, word, document, ooxml, tracked-changes, docx-js, redlining
name: deskclaw-docx
description: "专业 Word 文档（.docx）创建、编辑和排版。覆盖报告、公文、合同、备忘录、学术论文等场景。当用户要求生成、编辑、修改任何 Word 文档时使用此技能。即使用户没有明确说 docx，只要任务暗示需要可打印的正式文档，就应使用此技能。"
setup: bootstrap.py
---

# DeskClaw DOCX v3.0

创建、编辑和排版 Word 文档。创建用 docx-js（JavaScript），编辑用 unpack/XML/repack 工具链。

## 第零步：Bootstrap

```python
python bootstrap.py
```

幂等设计，已装跳过。Bootstrap 完成后会生成 `runtime/env.json`，包含当前环境的 Node.js 和 Python 路径。

检查是否就绪：

```python
import json
env = json.load(open("<SKILL_DIR>/runtime/env.json"))
print(env["node"])  # Node.js 路径
```

如果 `runtime/env.json` 不存在 → 先运行 `python bootstrap.py`。

## 命令速查表（Agent 必读）

> **关键**：先从 `runtime/env.json` 读取 `node` 和 `node_modules` 路径，不要硬编码。
> 运行 JS 脚本的模式：`NODE_PATH="<node_modules路径>" <node路径> script.js`

| 任务 | 方法 | 详细文档 |
|------|------|---------|
| 获取 node 路径 | 读取 `runtime/env.json` 中的 `node` 和 `node_modules` 字段 | — |
| 创建新文档 | 写 JS 脚本 → 用上面获取的 node 执行 | [creating_basics.md](references/creating_basics.md), [creating_extras.md](references/creating_extras.md) |
| 读取/分析 | `python -c "from docx import Document; ..."` | — |
| 编辑已有文档 | unpack → 编辑 XML → repack | [editing_xml.md](references/editing_xml.md) |
| 验证文档 | `python scripts/office/validate.py doc.docx` | — |
| 添加评论 | `python scripts/comment.py unpacked/ 0 "text"` | [editing_xml.md](references/editing_xml.md) |
| 接受修订 | `python scripts/accept_changes.py in.docx out.docx` | — |
| .doc → .docx | `python scripts/office/soffice.py --headless --convert-to docx file.doc` | — |
| 排版配方 | 根据文档类型选参数 | [recipes_common.md](references/recipes_common.md) |

## 创建新文档：最小可用模板

写 JavaScript 脚本，用 DeskClaw 的 Node 执行。**不要用 python-docx 创建新文档**——docx-js 支持 TOC、脚注、精确列表控制等 python-docx 做不到的功能。

```javascript
const fs = require("fs");
const os = require("os");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
        ImageRun } = require("docx");

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Microsoft YaHei", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, font: "Microsoft YaHei" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, font: "Microsoft YaHei" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1,
        children: [new TextRun("文档标题")] }),
      new Paragraph({ children: [new TextRun("正文内容...")] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(path.join(os.homedir(), "Desktop", "output.docx"), buffer);
  console.log("Saved");
});
```

运行方式（路径从 env.json 获取）：
```bash
# 先读路径
NODE=$(python -c "import json; print(json.load(open('<SKILL_DIR>/runtime/env.json'))['node'])")
NODE_MODULES=$(python -c "import json; print(json.load(open('<SKILL_DIR>/runtime/env.json'))['node_modules'])")
# 再执行
NODE_PATH="$NODE_MODULES" $NODE script.js
```

**完整的 docx-js API 模式（列表、表格、图片、页眉页脚、超链接、脚注、多栏、TOC 等）见：**
- [creating_basics.md](references/creating_basics.md) — 基础：Setup + 页面尺寸 + 样式 + 列表 + 表格
- [creating_extras.md](references/creating_extras.md) — 进阶：图片 + 超链接 + 脚注 + 多栏 + TOC + 硬规则

## 排版速查

### 中文文档默认值

| 属性 | docx-js 值 | 原因 |
|------|-----------|------|
| 字体 | `font: "Microsoft YaHei"` | 跨平台最安全 |
| 正文字号 | `size: 24` (12pt) | 中文需要较大字号 |
| 标题1 | `size: 32` (16pt), bold | 与正文比 ≥ 1.3:1 |
| 段间距 | `spacing: { after: 160 }` (8pt) | 段落分隔 |
| 页面 | A4: `width: 11906, height: 16838` | 中国标准 |
| 边距 | `margin: { top: 1440, ... }` (1 inch) | 通用 |

### 设计决策 6 条原则

1. **留白** 60-70% 覆盖率 2. **对比** 标题与正文 ≥ 1.5:1 3. **亲近** 相关内容间距小 4. **对齐** 网格对齐 5. **重复** 同级标题同样式 6. **层次** 3 秒看出层级

中英混排时，中文和英文/数字之间加半角空格：`中文 English 中文`。

## 参考文档索引

按需读取，不要一次全读。

| 需求 | 文件 |
|------|------|
| **docx-js 创建基础**（样式/列表/表格） | [creating_basics.md](references/creating_basics.md) |
| **docx-js 创建进阶**（图片/脚注/TOC/硬规则） | [creating_extras.md](references/creating_extras.md) |
| **编辑已有文档** / tracked changes / comments | [editing_xml.md](references/editing_xml.md) |
| 排版风格（5 种常用配方） | [recipes_common.md](references/recipes_common.md) |
| 更多学术/专业配方 | [recipes_extra.md](references/recipes_extra.md) |
| 留白和间距原则 | [design_space.md](references/design_space.md) |
| 对比和比例原则 | [design_contrast.md](references/design_contrast.md) |
| 对齐和一致性原则 | [design_structure.md](references/design_structure.md) |
| 视觉层次原则 | [design_hierarchy.md](references/design_hierarchy.md) |
| 西文字体/字号/行距 | [typo_fonts.md](references/typo_fonts.md) |
| 页面布局/表格/配色 | [typo_layout.md](references/typo_layout.md) |
| CJK 字体/字号名称 | [cjk_fonts.md](references/cjk_fonts.md) |
| CJK 标点/行距/GB/T 9704 | [cjk_rules.md](references/cjk_rules.md) |
