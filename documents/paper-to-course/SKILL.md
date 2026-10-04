---
name: paper-to-course
description: 将学术论文转换为交互式 HTML 课程 + Markdown 文档 + PPTX 演示文稿，一键生成全部三种输出
---

# Paper-to-Course Skill

将任意学术论文转换成交互式 HTML 课程 + Markdown 文档 + PPTX 演示文稿，**一次调用自动生成全部三种输出**。

## 使用方法

用户调用 skill 时传入 PDF 路径，skill 自动完成以下全部工作：

```
paper-to-course: /path/to/paper.pdf
```

**无需额外指令，HTML + Markdown + PPTX 全部自动生成。**

## 自动输出（三种同时生成）

| 输出 | 文件 | 说明 |
|------|------|------|
| HTML 课程 | `index.html` | 交互式单页，含时间线、对比表、公式拆解、对话动画、测验 |
| Markdown 文档 | `README.md` | 纯文本版，保留表格/公式/代码 |
| PPTX 演示文稿 | `slides.pptx` | 16 页组会汇报幻灯片 |

## 完整工作流（每次调用自动执行）

### Step 0 — 验证论文内容（必须！）

**在生成任何内容前，必须先读取 PDF 并验证论文主题。**

这一步至关重要——如果论文主题与预期不符（如把自动驾驶安全论文误读成 CNN 架构论文），后续所有内容都会错误。

读取 PDF 后，必须提取并确认：
- **标题**：论文原标题
- **作者/机构**：论文作者和所属机构（可判断领域）
- **Abstract**：摘要内容（核心发现一句话）
- **关键词/CCS Concepts**：论文的关键词（可判断研究领域）

然后向用户确认：
```
📄 论文主题确认
标题：<论文原标题>
作者：<作者>
摘要：<摘要前2-3句>
领域：<判断领域，如 CV/NLP/RL/安全等>

以上信息是否正确？如果论文主题不符，请告知我。
```

**只有在用户确认或未提出异议后，才继续生成内容。**

### Step 1 — 读取论文

读取用户提供的 PDF 文件，提取论文内容：
- Abstract / Introduction / Related Work / Method / Experiments / Conclusion
- 核心贡献、方法细节、实验数据、对比方法

### Step 2 — 生成课程目录结构

在课程目录（`paper-to-course/[论文名]/`）创建以下结构：

```
course-name/
├── _base.html          ← HTML 模板头部（从 references/ 复制）
├── _footer.html        ← HTML 模板尾部（从 references/ 复制）
├── build.sh           ← 打包脚本
├── slides-config.json ← PPTX 幻灯片配置（必须同时生成！）
├── modules/
│   ├── module-01.html  ← 问题与动机
│   ├── module-02.html  ← 发展脉络
│   ├── module-03.html  ← 主流方法对比
│   ├── module-04.html  ← 本文方法详解
│   ├── module-05.html  ← 实验与验证
│   └── module-06.html  ← 局限与展望
├── styles.css          ← 从 references/ 复制
└── main.js             ← 从 references/ 复制
```

### Step 3 — 生成 HTML 模块

为每个模块生成 HTML 文件，使用设计系统 CSS class（禁止内联样式）。

6 个模块内容要点：

**Module 1: 问题与动机**
- 背景问题与重要性
- 现有方法的瓶颈（3-4 个具体问题）
- 核心研究问题
- 为什么这个问题值得研究

**Module 2: 发展脉络**
- Literature Timeline 时间线（领域关键节点，含年份、方法、突破）
- 与其他方法的关键区别

**Module 3: 主流方法对比**
- Comparison Table（可交互，悬停显示详情）
- 各方法优缺点卡片
- 方法"对话"动画（Method Chat）

**Module 4: 本文方法详解**
- Architecture Diagram（可点击组件查看描述）
- 核心公式 Formula Breakdown（逐行通俗解释）
- 关键组件协作对话

**Module 5: 实验与验证**
- 主实验结果表格（数字精确到个位）
- Ablation Diagram（消融实验可视化）
- 分类型性能数据

**Module 6: 局限与展望**
- 当前局限性（3-4 条）
- 未来研究方向（3-5 条）
- 核心贡献总结
- 最终理解测验

### Step 4 — 生成 PPTX 配置（必须！）

在课程目录生成 `slides-config.json`，内容为 16 页幻灯片配置：

```json
{
  "title": "论文标题",
  "subtitle": "副标题 / 会议 / 年份",
  "slides": [
    { "type": "title", "title": "...", "subtitle": "...", "note": "" },
    { "type": "outline", "title": "汇报提纲", "items": ["...", "..."] },
    { "type": "content", "title": "研究背景", "layout": "cards-3", "cards": [...] },
    { "type": "timeline", "title": "发展脉络", "items": [...] },
    { "type": "table", "title": "Benchmark 对比", "headers": [...], "rows": [...], "highlightRows": [3] },
    { "type": "flow", "title": "方法流程", "steps": [...] },
    { "type": "bars", "title": "消融实验", "items": [...] },
    { "type": "stats", "title": "核心结果", "stats": [...] },
    { "type": "limitations", "title": "局限与展望", "limitations": [...], "futureWork": [...] },
    { "type": "summary", "title": "总结", "items": [...] }
  ]
}
```

**slides-config.json 支持的 slide type：**

| type | 说明 | 关键字段 |
|------|------|---------|
| `title` | 标题页 | `title`, `subtitle`, `note` |
| `outline` | 提纲 | `items[]` |
| `content` | 内容页 | `title`, `layout` (bullets/cards-2/cards-3/cards-4/steps/grid-2x2), `cards[]` 或 `items[]` |
| `flow` | 流程页 | `steps[]` (含 `num`, `title`, `subtitle`, `desc`) |
| `table` | 表格页 | `headers[]`, `rows[][]`, `highlightRows[]` |
| `bars` | 柱状图页 | `items[]` (含 `label`, `value`, `drop`) |
| `stats` | 大数字统计 | `stats[]` (含 `value`, `label`, `color`, `big`) |
| `formula` | 公式页 | `formula`, `lines[]` (含 `symbol`, `english`) |
| `timeline` | 时间线 | `items[]` (含 `year`, `title`, `desc`) |
| `summary` | 总结页 | `items[]` (含 `text`, `color`) |
| `limitations` | 双栏布局 | `limitations[]`, `futureWork[]` |

### Step 5 — 运行构建脚本

复制 CSS/JS 后执行：

```bash
cd paper-to-course/course-name
bash build.sh              # 生成 index.html
node scripts/build-all.js . # 自动生成 HTML + README.md + slides.pptx
```

## 设计规范

- 暖色调"开发者笔记本"美学：米白背景 (#FAF7F2) + 珊瑚红强调色 (#D94F30)
- 字体：Bricolage Grotesque (标题) + DM Sans (正文) + JetBrains Mono (公式/代码)
- 所有样式通过 CSS class 引用，禁止内联 style 属性
- 所有交互逻辑由 `main.js` 处理，模块 HTML 只写结构

## 文件结构

```
paper-to-course/
├── SKILL.md                     ← 本技能说明（本文档）
├── scripts/
│   ├── build-all.js           ← 统一流水线（HTML + MD + PPTX）
│   ├── generate-pptx.js       ← PPTX CLI 入口（通用，数据驱动）
│   ├── slides-builder.js      ← PPTX 核心构建器（支持所有 slide type）
│   └── html-to-md.js          ← HTML → Markdown 转换器
└── references/
    ├── styles.css              ← 完整设计系统
    ├── main.js                ← 交互引擎
    ├── _base.html             ← HTML 模板头部
    ├── _footer.html            ← HTML 模板尾部
    └── paper-elements.md       ← 7 种交互元素实现模式
```

## 交互元素参考

详见 `references/paper-elements.md`：

| 元素 | HTML class | 说明 |
|------|-----------|------|
| Formula Breakdown | `formula-block` | 公式逐行通俗解释 |
| Literature Timeline | `timeline-container` | 领域发展时间线动画 |
| Method Chat | `chat-window` / `group-chat` | 组件间"对话"动画 |
| Comparison Table | `comparison-table` | 可交互对比表格 |
| Ablation Diagram | `ablation-container` | 消融实验可视化 |
| Quiz | `quiz-container` | 选择题理解测验 |
| Glossary Tooltips | `term` | 术语悬停通俗解释 |

## PPTX 风格

- 背景：纯白 (#FFFFFF)
- 标题栏：深炭灰 (#36454F)
- 强调色：珊瑚红 (#D94F30)
- 卡片背景：浅灰 (#F0F0F0)
- 字体：Arial Black（标题）+ Calibri（正文）
- 布局：16:9 宽屏
