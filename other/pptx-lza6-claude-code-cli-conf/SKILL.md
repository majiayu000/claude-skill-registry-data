---
name: pptx
description: "当涉及 .pptx 文件（作为输入、输出或两者兼有）时，随时使用此 Skill。包括：创建幻灯片、演示文稿或演讲稿；读取、解析或从 .pptx 文件中提取文本；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板、布局、演讲者备注或批注。当用户提到\"幻灯片\"、\"演示文稿\"或引用 .pptx 文件名时触发。如果需要打开、创建或处理 .pptx 文件，使用此 Skill。"
license: "专有。完整条款请参见 LICENSE.txt"
---

# PPTX 技巧

## 快速参考

| 任务 | 指南 |
|------|--------|
| 阅读/分析内容 | `python -m markitdown 演示文稿.pptx` |
| 编辑或从模板创建 | 阅读 [editing.md](editing.md) |
| 从头开始创建 | 阅读 [pptxgenjs.md](pptxgenjs.md) |

---

## 阅读内容

```bash
# 文本提取
python -m markitdown presentation.pptx

# 视觉概览
python scripts/thumbnail.py presentation.pptx

# 原始 XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## 编辑工作流

**阅读 [editing.md](editing.md) 了解完整详情。**

1. 使用 `thumbnail.py` 分析模板
2. 解压 → 操作幻灯片 → 编辑内容 → 清理 → 打包

---

## 从头开始创建

**阅读 [pptxgenjs.md](pptxgenjs.md) 了解完整详情。**

当没有可用的模板或参考演示文稿时使用。

---

## 设计理念

**不要创建无聊的幻灯片。** 白色背景上的普通项目符号不会给任何人留下深刻的印象。为每张幻灯片考虑此列表中的想法。

### 开始之前

- **选择一个大胆的、内容丰富的调色板**：调色板应该感觉是专为这个主题设计的。如果将颜色交换为完全不同的演示文稿仍然"有效"，那么您还没有做出足够具体的选择。
- **支配平等**：一种颜色应占主导地位（60-70% 视觉权重），并有 1-2 个支撑色调和一种尖锐的强调色。永远不要给所有颜色同等的权重。
- **深色/浅色对比**：标题+结论幻灯片的深色背景，内容的浅色背景（"三明治"结构）。或者全身采用深色以获得高级感。
- **致力于视觉主题**：选择一个独特的元素并重复它 - 圆形图像框架、彩色圆圈图标、粗单边边框。将其放在每张幻灯片上。

### 调色板

选择与您的主题相匹配的颜色 - 不要默认为普通蓝色。使用这些调色板作为灵感：

| 主题 | 主色 | 辅色 | 强调色 |
|--------|---------|------------|--------|
| **午夜行政** | `1E2761`（海军蓝）| `CADCFC`（冰蓝色）| `FFFFFF`（白色）|
| **森林和苔藓** | `2C5F2D`（森林）| `97BC62`（苔藓）| `F5F5F5`（奶油色）|
| **珊瑚能源** | `F96167`（珊瑚）| `F9E795`（金色）| `2F3C7E`（海军蓝）|
| **温暖的赤土陶器** | `B85042`（赤土） | `E7E8D1`（沙子）| `A7BEAE`（鼠尾草）|
| **海洋渐变** | `065A82`（深蓝色）| `1C7293`（青色）| `21295C`（午夜）|
| **木炭最少** | `36454F`（木炭）| `F2F2F2`（灰白色）| `212121`（黑色）|
| **青色信托** | `028090`（青色）| `00A896`（海沫）| `02C39A`（翡翠）|
| **浆果和奶油** | `6D2E46`（浆果）| `A26769`（ dusty rose）| `ECE2D0`（奶油色）|
| **鼠尾草平静** | `84B59F`（鼠尾草）| `69A297`（桉树）| `50808E`（板岩）|
| **樱桃大胆** | `990011`（樱桃）| `FCF6F5`（灰白色）| `2F3C7E`（海军蓝）|

### 每张幻灯片

**每张幻灯片都需要一个视觉元素** - 图像、图表、图标或形状。纯文本幻灯片很容易被遗忘。

**布局选项：**
- 两栏（左侧为文字，右侧为插图）
- 图标+文本行（彩色圆圈中的图标，粗体标题，下面的说明）
- 2x2 或 2x3 网格（一侧为图像，另一侧为内容块网格）
- 带有内容叠加的半出血图像（完整的左侧或右侧）

**数据显示：**
- 大统计标注（大数字 60-72pt，下面带有小标签）
- 比较栏（之前/之后、优点/缺点、并排选项）
- 时间线或流程（编号步骤、箭头）

**视觉修饰：**
- 部分标题旁边的小彩色圆圈中的图标
- 关键统计数据或标语的斜体重音文本

### 字体排印

**选择有趣的字体配对** - 不要默认为 Arial。选择具有个性的标题字体，并将其与干净的正文字体配对。

| 标题字体 | 正文字体 |
|------------|------------|
| Georgia | Calibri |
| SimHei | SimSun |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Comic Sans MS | Calibri |
| Impact | SimSun |
| Palatino | Garamond |
| Consolas | Calibri |

| 元素 | 尺寸 |
|---------|------|
| 幻灯片标题 | 36-44pt 粗体 |
| 节标题 | 20-24pt 粗体 |
| 正文 | 14-16pt |
| 副标题 | 10-12pt 常规 |

### 间距

- 0.5" 最小边距
- 内容块之间 0.3-0.5"
- 留出呼吸空间——不要填满每一寸

### 避免（常见错误）

- **不要重复相同的布局** - 在幻灯片中改变列、卡片和标注
- **不要将正文居中** — 左对齐段落和列表；仅居中标题
- **不要吝惜大小对比** — 标题需要 36pt+ 才能从 14-16pt 正文中脱颖而出
- **不要默认为蓝色** — 选择反映特定主题的颜色
- **不要随机混合间距** — 选择 0.3 英寸或 0.5 英寸间隙并一致使用
- **不要设计一张幻灯片而让其余部分保持简单** - 完全承诺或保持简单
- **不要创建纯文本幻灯片** — 添加图像、图标、图表或视觉元素；避免简单的标题+项目符号
- **不要忘记文本框填充** - 将线条或形状与文本边缘对齐时，在文本框上设置"边距：0"或偏移形状以考虑填充
- **不要使用低对比度元素** - 图标和文本需要与背景形成强烈对比；避免在浅色背景上使用浅色文本或在深色背景上使用深色文本
- **切勿在标题下使用重音线** - 这是 AI 生成幻灯片的标志；使用空白或背景颜色代替

---

## 质量检查（必填）

**假设存在问题。你的工作就是找到它们。**

你的第一次渲染几乎从来都不正确。将 QA 视为 bug 搜寻，而不是确认步骤。如果你在第一次检查中未发现任何问题，说明你检查得不够仔细。

### 内容质量检查

```bash
python -m markitdown output.pptx
```

检查是否有内容缺失、拼写错误、顺序错误。

**使用模板时，检查剩余的占位符文本：**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

如果 grep 返回结果，请在声明成功之前修复它们。

### 视觉质量检查

**⚠️ 使用子代理**——即使是 2-3 张幻灯片。你一直在盯着代码，你会看到你期望看到的，而不是实际存在的。子代理有新鲜的视角。

将幻灯片转换为图像（请参阅[转换为图像](#转换为图像)），然后使用此提示：

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### 验证循环

1. 生成幻灯片 → 转换为图像 → 检查
2. **列出发现的问题**（如果没有发现，请更仔细地再看一遍）
3. 修复问题
4. **重新验证受影响的幻灯片** - 一项修复通常会产生另一个问题
5. 重复直到完整通过未发现新问题

**在至少完成一个修复和验证周期之前，不要宣布成功。**

---

## 转换为图像

将演示文稿转换为单独的幻灯片图像以进行目视检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

这将创建 `slide-01.jpg`、`slide-02.jpg` 等。

要在修复后重新渲染特定幻灯片：

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## 依赖项

- `pip install "markitdown[pptx]"` - 文本提取
- `pip install Pillow` - 缩略图网格
- `npm install -g pptxgenjs` - 从头开始创建
- LibreOffice (`soffice`) - PDF 转换（通过 `scripts/office/soffice.py` 自动配置沙盒环境）
- Poppler (`pdftoppm`) - PDF 到图像
