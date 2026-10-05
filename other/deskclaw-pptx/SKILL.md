---
name: deskclaw-pptx
slug: deskclaw-pptx
version: 4.0.0
displayName: PPT 演示文稿生成器（DeskClaw PPTX）
summary: DeskClaw 自研 PPT 全能工具。支持从零创建（PptxGenJS 高精度渲染）、模板编辑（OOXML unpack/pack）、内容分析三大工作流。内置 18 种配色方案、5 种幻灯片类型、完整设计系统，跨平台兼容。
description: "Generate, edit, and read PowerPoint presentations. Create from scratch with PptxGenJS (cover, TOC, content, section divider, summary slides), edit existing PPTX via XML unpack/pack workflows, or extract text with markitdown. Includes 18 color palettes, 4 style recipes, 5 slide types, and full design system. Triggers: PPT, PPTX, PowerPoint, presentation, slide, deck, slides, 演示文稿, 幻灯片."
author: DeskClaw
tags: office, pptx, presentation, slides, design-system, charts, templates, powerpoint
---

# PPT 演示文稿生成器

## 工作流选择

| 用户需求 | 走哪条路 | 关键命令 |
|----------|---------|---------|
| **创建新 PPT** | PptxGenJS 工作流 | 写 JS → `python scripts/compile.py slides/ output.pptx` |
| **编辑现有 PPT** | OOXML 工作流 | `unpack.py` → 编辑 XML → `pack.py` |
| **查看 PPT 内容** | markitdown | `python -m markitdown file.pptx` |

**执行须知 (减少不必要的工具调用):**
- `python bootstrap.py` 只需执行一次，它会自动检测已安装的依赖并跳过，输出所有可用路径
- `compile.py` 会自动创建输出目录，不需要提前 mkdir
- `write_file` 直接写文件即可，不需要先 ls 检查或 mkdir 创建目录
- 简单任务不需要读 reference 文件，SKILL.md 本身包含足够的示例

## 命令速查表

| 任务 | 命令 |
|------|------|
| **安装依赖** | `python bootstrap.py` |
| **提取文本** | `python -m markitdown presentation.pptx` |
| **生成缩略图** | `python scripts/thumbnail.py presentation.pptx` |
| **解包 PPTX** | `python scripts/office/unpack.py input.pptx unpacked/` |
| **打包 PPTX** | `python scripts/office/pack.py unpacked/ output.pptx --original input.pptx` |
| **复制幻灯片** | `python scripts/add_slide.py unpacked/ slide2.xml` |
| **清理孤立文件** | `python scripts/clean.py unpacked/` |
| **验证 XML** | `python scripts/office/validate.py unpacked/ --original input.pptx` |
| **编译 JS→PPTX** | `python scripts/compile.py slides/ output.pptx` |

| 参数 | 值 |
|------|---|
| **幻灯片尺寸** | 10" x 5.625" (LAYOUT_16x9) |
| **颜色格式** | 6 位 hex，无 # 前缀 (如 `"FF0000"`) |
| **中文字体** | Microsoft YaHei (微软雅黑) |
| **英文字体** | Arial (默认)，或 Georgia/Calibri/Cambria |
| **页码位置** | x: 9.3", y: 5.1" |
| **theme 键** | `primary`, `secondary`, `accent`, `light`, `bg` |

---

## 参考文档 (按需读取)

根据任务需要选择读取对应文件，不需要全部读。

| 文件 | 何时读 | 内容摘要 |
|------|--------|---------|
| [pptxgenjs-basic.md](references/pptxgenjs-basic.md) | **总是** | 文本、列表、形状的 JS API — 写 slide JS 必读 |
| [pptxgenjs-data.md](references/pptxgenjs-data.md) | 需要表格或图表时 | addTable、addChart API |
| [pptxgenjs-media.md](references/pptxgenjs-media.md) | 需要图片或图标时 | addImage、react-icons 用法 |
| [colors.md](references/colors.md) | 用户要求设计感/配色时 | 18 套色彩方案查找表 |
| [styles.md](references/styles.md) | 用户要求特定风格时 | 4 种风格 (Sharp/Soft/Rounded/Pill) 的间距和圆角参数 |
| [fonts-chinese.md](references/fonts-chinese.md) | 生成中文内容时 | 中文字体、字号、行高规则 |
| [slide-cover.md](references/slide-cover.md) | 需要精美封面时 | 封面页布局方案 |
| [slide-content.md](references/slide-content.md) | 需要丰富布局时 | 内容页 6 种子类型 |
| [slide-toc-divider.md](references/slide-toc-divider.md) | 超过 8 页时 | 目录页 + 分隔页 |
| [slide-summary.md](references/slide-summary.md) | 需要精美结尾时 | 总结页布局 |
| [color-scales.md](references/color-scales.md) | 极少 | Platinum 主题完整色阶 |
| [pitfalls.md](references/pitfalls.md) | QA 阶段 | 常见错误 + PptxGenJS 陷阱 |
| [editing.md](editing.md) | 编辑现有 PPT 时 | OOXML 模板编辑工作流 |

---

## 两个核心工作流

### 工作流 A: 从零创建 (PptxGenJS)

用于没有现成模板的场景。用 JavaScript 生成原生 PPTX 文件。

### 工作流 B: 模板编辑 (OOXML)

用于基于现有演示文稿的场景。解包 PPTX 为 XML，直接编辑后重新打包。

---

## 工作流 A: 从零创建

### 第 1 步: 理解需求

了解主题、受众、用途、风格基调和内容深度。

### 第 2 步: 选择色彩方案与字体

从 [色彩方案](references/design-system.md#color-palette-reference) 中选择匹配主题的方案。
从 [字体配对](references/design-system.md#font-reference) 中选择字体组合。

色彩方案应该为这个特定主题而选择。如果把你的颜色换到一个完全不同的演示中还能"成立"，说明选择不够具体。

### 第 3 步: 选择设计风格

从 [风格配方](references/design-system.md#style-recipes) 中选择视觉风格:
- **Sharp & Compact**: 数据密集、财务报告
- **Soft & Balanced**: 企业商务、通用场景
- **Rounded & Spacious**: 产品介绍、营销
- **Pill & Airy**: 品牌发布、高端展示

### 第 4 步: 规划幻灯片大纲

将每张幻灯片归类为 [5 种页面类型](references/slide-types.md) 之一:

| 类型 | 用途 | 数量 |
|------|------|------|
| **封面 (Cover)** | 开场，定调 | 1 张 |
| **目录 (TOC)** | 导航，设预期 | 0-1 张 |
| **分隔页 (Section Divider)** | 章节过渡 | 按章节数 |
| **内容页 (Content)** | 主体内容 (6 种子类型) | 占大部分 |
| **总结页 (Summary)** | 收尾，行动号召 | 1 张 |

内容页 6 种子类型: 文字型、图文混排、数据可视化、对比型、时间线/流程、图片展示。

确保视觉多样性 — 不要在多张幻灯片上重复同一布局。

### 第 5 步: 生成幻灯片 JS 文件

每张幻灯片一个 JS 文件 (`slides/slide-01.js`, `slides/slide-02.js`, ...)。

每个文件必须导出同步 `createSlide(pres, theme)` 函数。不需要 require pptxgenjs — `pres` 对象由 compile.js 传入:

```javascript
// slides/slide-01.js
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addText("标题", {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, align: "center"
  });

  return slide;
}

module.exports = { createSlide };
```

### 第 6 步: 编写 compile.js 并编译

在 `slides/` 目录下创建 `compile.js`，汇编所有幻灯片:

```javascript
// slides/compile.js
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const theme = {
  primary: "2b2d42",    // 深色，标题和背景
  secondary: "8d99ae",  // 次深色，正文和装饰
  accent: "ef233c",     // 强调色
  light: "edf2f4",      // 浅色调
  bg: "ffffff"           // 背景色
};

// 按顺序加载所有幻灯片 (修改数量以匹配实际幻灯片数)
for (let i = 1; i <= 3; i++) {
  const num = String(i).padStart(2, '0');
  require(`./slide-${num}.js`).createSlide(pres, theme);
}

// 输出路径由 compile.py 通过环境变量传入
const output = process.env.PPTX_OUTPUT || './output.pptx';
pres.writeFile({ fileName: output });
```

编译命令 (compile.py 自动处理 node 路径和模块查找):
```bash
python scripts/compile.py slides/ ~/Desktop/testout/deskclaw-pptx/output.pptx
```

### 第 7 步: QA 质量检查

详见 [QA 流程](references/pitfalls.md#qa-process)。

输出结构:
```
slides/
├── slide-01.js ... slide-NN.js
├── imgs/
└── compile.js
→ python scripts/compile.py slides/ <目标路径>.pptx
```

---

## Theme 对象协议 (必须遵守)

所有幻灯片通过 compile.js 接收同一个 theme 对象，包含且仅包含以下 5 个键:

| 键 | 用途 | 示例 |
|----|------|------|
| `theme.primary` | 最深色，用于标题和背景 | `"22223b"` |
| `theme.secondary` | 次深色，正文和装饰 | `"4a4e69"` |
| `theme.accent` | 中间色调，强调 | `"9a8c98"` |
| `theme.light` | 浅色调，轻装饰 | `"c9ada7"` |
| `theme.bg` | 背景色 | `"f2e9e4"` |

不要使用其他键名 (如 `background`, `text`, `muted`)，因为编译脚本只传递这 5 个键。

---

## 页码徽章 (非封面页必须添加)

除封面外的所有幻灯片都必须在右下角添加页码。

位置: x: 9.3", y: 5.1"。只显示当前页号 (如 `3` 或 `03`)，不显示 "3/12"。

```javascript
// 圆形徽章
slide.addShape(pres.shapes.OVAL, {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fill: { color: theme.accent }
});
slide.addText("3", {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fontSize: 12, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

---

## 工作流 B: 模板编辑

详见 [editing.md](editing.md) 的完整工作流。

简要步骤:

1. **分析**: `python scripts/thumbnail.py template.pptx` + `python -m markitdown template.pptx`
2. **解包**: `python scripts/office/unpack.py template.pptx unpacked/`
3. **操作**: 在 `ppt/presentation.xml` 的 `<p:sldIdLst>` 中删除/复制/重排幻灯片
4. **编辑**: 修改各 `slide{N}.xml` 中的文本和元素
5. **清理**: `python scripts/clean.py unpacked/`
6. **打包**: `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`
7. **验证**: `python scripts/office/validate.py unpacked/ --original template.pptx`

---

## 设计原则

### 不要做无聊的幻灯片

白色背景加项目符号是最低标准。每张幻灯片都应该有视觉元素 — 图片、图表、图标或形状。

### 排版规范

| 元素 | 字号 |
|------|------|
| 幻灯片标题 | 36-44pt 加粗 |
| 章节标题 | 20-24pt 加粗 |
| 正文 | 14-16pt (中文 16-18pt) |
| 注释/来源 | 10-12pt |
| 数据突出显示 | 60-72pt |

正文左对齐 (不要居中)。标题可以居中。中文正文不加粗 — 粗体仅用于标题。

### 布局建议

- 双栏布局 (文字左，图片右)
- 图标 + 文字行 (图标在彩色圆圈中)
- 2x2 或 2x3 网格
- 半出血图片 + 内容叠加
- 大数字标注 (60-72pt 数字 + 小标签)

### 常见错误 (必须避免)

- 不要在多张幻灯片上重复同样的布局
- 不要居中正文 — 正文左对齐
- 不要使用 `#` 前缀的 hex 颜色 (会导致文件损坏)
- 不要把透明度写进 8 位 hex 颜色字符串 — 用 `opacity` 属性
- 不要在 createSlide() 中使用 async/await — 必须同步
- 不要复用选项对象 — PptxGenJS 会原地修改，用工厂函数代替
- 不要在标题下加装饰线 — 这是 AI 生成幻灯片的明显标志
- 不要使用低对比度的文字或图标

---

## QA 检查 (必须执行)

假设第一次渲染有问题。你的任务是找到它们。

### 内容检查

```bash
python -m markitdown output.pptx
```

检查内容缺失、错别字、顺序错误。

模板编辑时检查残留占位文本:
```bash
python -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert"
```

### 验证循环

1. 生成 → markitdown 检查内容
2. 列出发现的问题
3. 修复
4. 重新验证
5. 重复直到无新问题

---

## 图标 (react-icons)

使用 react-icons 将 SVG 图标栅格化为 PNG，提升视觉效果。

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

图标库: `react-icons/fa` (Font Awesome), `react-icons/md` (Material), `react-icons/hi` (Heroicons)。

注意: 图标渲染是异步的，应该在 createSlide() 之前预处理好，将 base64 数据传入同步函数。

---

## 中文本地化

生成中文内容时:
- 字体: 微软雅黑 (Microsoft YaHei)
- 正文字号: 16-18pt (比英文大 2pt)
- 行高: 1.5-1.8x
- 每行中文字符: 15-20 个
- 中英文/数字之间加半角空格: `会议有 12 位参与者`

---

## 依赖安装

运行 `python bootstrap.py` 自动安装所有依赖。

手动安装:
```bash
# Python
pip install "markitdown[pptx]" Pillow defusedxml lxml -i https://pypi.tuna.tsinghua.edu.cn/simple

# Node.js
npm install pptxgenjs react-icons react react-dom sharp --registry=https://registry.npmmirror.com
```
