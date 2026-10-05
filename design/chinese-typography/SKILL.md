---
name: chinese-typography
description: 中文排版规范助手。当用户要"排版""中文网页样式""文章排版""公众号排版""PDF/Word 排版""字体怎么选""中英混排""为什么我的中文网页很丑"时使用。处理中英间距、标点、行高、字体栈、CJK 断行等中文特有问题，输出可直接用的 CSS 或排版建议。
metadata:
  author: sanhuang520-ship-it
  category: design
  tags: design, chinese, standards, ui
---

# 中文排版助手

**中文网页丑，八成不是设计问题，是排版问题。**

大部分模板是按西文设计的，直接拿来放中文，会同时踩到十几个坑：行高不够、中英挤在一起、标点占位不对、断行断在不该断的地方。

## 什么时候用

网页/文章/公众号/PDF/Word/PPT 的中文排版，选字体，中英混排，修"说不上哪里丑"的中文页面。

## 第一步：确认载体

不同载体规则差别大：

| 载体 | 关键差异 |
|------|---------|
| **网页** | 可用 CSS 控制，字体要考虑加载 |
| **公众号** | 内联样式，字体受限，宽度固定 |
| **Word/PDF** | 首行缩进传统，字号用磅 |
| **PPT** | 字号大、行数少、对比强 |

## 中文排版的 10 条核心规则

### 1. 中英文之间加空格（盘古之白）

```
❌ 我用Python写了一个爬虫
✅ 我用 Python 写了一个爬虫
```

**数字同理**：`3 个苹果`、`iPhone 15 Pro`

例外：**标点旁边不加**——`使用 Python，然后……`（逗号前不加）

### 2. 行高要比西文大

中文字符方正饱满，行高不够会挤成一团。

```css
line-height: 1.75;   /* 正文，1.6-1.8 都可以 */
line-height: 1.35;   /* 大标题可以紧一些 */
```

> 西文常用的 1.4-1.5 放中文会显得压抑。

### 3. 字体栈要写对

```css
font-family:
  -apple-system, BlinkMacSystemFont,   /* 苹方 / SF */
  "Segoe UI", Roboto,                   /* 西文优先 */
  "PingFang SC", "Hiragino Sans GB",    /* 苹果中文 */
  "Microsoft YaHei", "微软雅黑",         /* Windows */
  "Source Han Sans SC", "Noto Sans CJK SC",  /* 思源 */
  sans-serif;
```

**顺序原则**：西文字体放前面，中文字体放后面。这样英文用西文字体渲染，中文自动 fallback，混排更好看。

**衬线（正文长阅读 / 文艺感）**：
```css
font-family: "Songti SC", "SimSun", "Noto Serif SC", Georgia, serif;
```

### 4. 标点：全角还是半角

| 场景 | 用法 |
|------|------|
| 中文句子 | **全角**：，。？！：；""'' |
| 英文句子 | **半角**：, . ? ! : ; " ' |
| 中文句中的英文 | 英文内部用半角，句子结束用全角句号 |

**括号**：中文内容用全角（），英文内容用半角 ()

**省略号**：中文用 `……`（六点），不是 `...`

**破折号**：中文用 `——`（两个），不是 `--`

### 5. 引号

- 简体大陆规范：`""` 和 `''`
- 港台 / 文艺排版：`「」` 和 `『』`

**统一即可，不要混用。**

### 6. CJK 断行控制

```css
word-break: normal;        /* 不要用 break-all，会把英文单词拦腰截断 */
overflow-wrap: anywhere;   /* 超长 URL 才需要 */
line-break: strict;        /* 严格避头尾（标点不出现在行首）*/
```

**避头尾规则**：`。，、；：？！）》」` 不能出现在行首；`（《「` 不能出现在行尾。

### 7. 段落：缩进还是间距

| 载体 | 推荐 |
|------|------|
| 网页 | **段间距**（`margin-bottom: 1.5em`），不缩进 |
| 印刷 / Word / PDF | **首行缩进 2 字符**（`text-indent: 2em`） |

⚠️ **不要同时用**——又缩进又空行是排版新手最常见的错误。

### 8. 着重强调

中文**不用下划线**，也慎用斜体（中文没有真正的斜体，会被拉斜变形）。

```css
/* 着重号（中文传统做法）*/
em {
  font-style: normal;
  text-emphasis: dot;
  text-emphasis-position: under right;
}
```

或直接用**加粗**。

### 9. 字号与行宽

```css
font-size: 16px;      /* 网页正文最小值，17-18px 更舒适 */
max-width: 38em;      /* 中文一行 30-40 字最舒服 */
```

> 一行超过 45 个汉字，眼睛回扫会累。

### 10. 数字与单位

- 数字用**半角**：`2026 年`不是`２０２６年`
- 数字与单位间加空格：`5 GB`、`30 分钟`（中文单位可不加：`5个`→`5 个`更清晰）
- 表格里的数字用等宽对齐：`font-variant-numeric: tabular-nums;`

## 可直接用的基础样式

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
               "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  --font-serif: "Songti SC", "Noto Serif SC", Georgia, serif;
}

body {
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.75;
  letter-spacing: 0.01em;      /* 中文微调，别超过 0.05em */
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

article {
  max-width: 38em;
  margin: 0 auto;
}

p { margin-bottom: 1.5em; }

h1, h2, h3 {
  line-height: 1.35;
  letter-spacing: 0;           /* 大字号不需要额外字距 */
  margin: 2em 0 0.8em;
}

/* 中英混排自动间距（现代浏览器）*/
body { text-spacing-trim: normal; }

/* 着重号 */
em {
  font-style: normal;
  text-emphasis: dot;
  text-emphasis-position: under right;
}

/* 表格数字对齐 */
td.num { font-variant-numeric: tabular-nums; text-align: right; }
```

## 常见问题速查

| 症状 | 原因 | 解法 |
|------|------|------|
| 中文网页"说不上哪里丑" | 行高太小 | `line-height: 1.75` |
| 中英文挤在一起 | 缺盘古之白 | 手动加空格或用 `text-spacing-trim` |
| 英文单词被截断 | `word-break: break-all` | 改成 `normal` |
| 标点出现在行首 | 没设避头尾 | `line-break: strict` |
| 加粗中文变模糊 | 字体没有真 Bold，被伪粗 | 用思源黑体等有多字重的字体 |
| 一行字太长看着累 | 没限宽 | `max-width: 38em` |
| 斜体中文很难看 | 中文无真斜体 | 改用加粗或着重号 |

## 公众号排版特殊规则

- 正文字号 **15-16px**（微信默认 17px 偏大）
- 行高 **1.75**
- 段间距 **1em**，不要首行缩进
- 两端不留白边（微信已有边距）
- **不要用系统外字体**，会失效
- 图片宽度 100%，圆角 4-8px

## 边界

1. **不替用户决定品牌字体**。商用字体有授权问题（如方正、汉仪部分字体商用需付费），涉及商业项目时提醒核实授权。
2. **不确定的规范要说明**。大陆/港台/新马排版规范有差异，涉及具体出版规范时建议查对应标准（如 GB/T 15834 标点符号用法）。
3. **免费可商用中文字体**推荐：思源黑体/宋体（SIL OFL）、阿里巴巴普惠体、HarmonyOS Sans、霞鹜文楷。用之前仍建议核对最新授权条款。
