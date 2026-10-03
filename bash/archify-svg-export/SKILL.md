---
name: archify-svg-export
description: 把 archify 生成的图表 HTML 无头导出为 SVG（复用成品页内置的 Archify.exportMenu.run()，产物与人工点 Export 一致，含深浅双主题），需本地已装 Chrome/Chromium。默认不自动触发，仅在用户显式点名本 skill 时生效。
---

# Archify 图表导出 SVG

## 概述

**目的**：补上 archify 的"最后一公里"。archify 交付的是独立可交互 HTML，导出功能只存在于 Viewer 的 Export 菜单里，必须人工开浏览器点。本 skill 让 AI 在无人值守下直接产出官方 SVG 文件。

**功能**：
- 复用成品 HTML 内置的官方导出代码 `Archify.exportMenu.run('svg')`，**不重写** `serializeSvg()`，产物与人工导出字节一致，含浅色/深色双主题
- 输入两种形态：已交付的 `*.html`，或 archify 规范 `*.json`（自动先渲染再导出）
- 自带产物校验：文件名取自 CDP 事件而非猜目录，并校验文件头，避免命中陈旧文件或读到半截写入
- 缺 Chrome 时给出明确指引，不静默失败

**适用条件**（仅在被显式调用后判断，不用于自动触发）：
- 已存在 archify 产物（`*.html` 或规范 `*.json`），需要把它导出为 SVG 文件
- 导出后交给用户自行嵌入文档；本 skill **不负责**嵌入动作

> 本 skill 是 archify 的**无头配套**，不是替代品：archify 负责生成图表，本 skill 只把已生成的图表导出为文件。

---

## 触发方式：仅显式调用

**本 skill 默认不自动触发。** 不要根据语义相似度自行判断"该不该用我"——只有在以下情况才生效：

1. 用户用 `@command://archify-svg-export` 之类的显式指令调用
2. 用户点名要求"用 archify-svg-export 这个 skill"

不触发的典型情况（即使语义相关）：

| 用户输入 | 是否启用本 skill | 说明 |
|---|---|---|
| "把 archify 图导出成 SVG" | ❌ | 除非显式指定；这类语义交由 archify skill 处理 |
| "用 archify 画个架构图" | ❌ | 生成图表属 `archify` 职责 |
| "archify 怎么导出" | ❌ | 未显式指定本 skill |

**为什么这样设计**：archify 官方 skill 的 description 里已含 "SVG export"，若本 skill 也按语义自动触发，两者会撞车，导致用户要导出时反而选中生成向的 archify skill。改为显式调用后，触发责任完全交给用户，不存在歧义。

---

## 前置条件

| 条件 | 说明 |
|---|---|
| archify 产物 | 已有 `*.html`（archify 交付的成品），或规范 `*.json`（须含 `diagram_type` 字段） |
| Chrome / Chromium | **必需**。官方导出代码依赖 `getComputedStyle`、`canvas` 等浏览器 API，纯 Node 无法实现 |

### 前置检测：archify 是否已安装

**执行导出前必须先检测 archify skill 是否存在。不存在时只提示用户自行安装，绝不自动安装。**

检测依据（命中任一即视为已安装）：

1. 环境变量 `ARCHIFY_HOME` 指向的目录下存在 `bin/archify.mjs`
2. `~/.codebuddy/skills/archify/bin/archify.mjs` 存在

未检测到 → **停止执行**，并提示用户自行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/HACK-WU/skills/master/scripts/skill-install.sh | \
  bash -s -- --repo tt-a1i/archify
```

> 安装器已下载到本地时可改为 `bash scripts/skill-install.sh --repo tt-a1i/archify`。

已安装但不在默认位置时，用 `ARCHIFY_HOME` 指定（输入为规范 JSON 时用它渲染 HTML）：

```bash
export ARCHIFY_HOME=/path/to/archify-skill   # 该目录下须有 bin/archify.mjs
```

脚本按以下顺序定位浏览器：

1. 环境变量 `ARCHIFY_CHROME`（与 archify 官方约定的同一个变量）
2. `/usr/bin/google-chrome`、`/usr/bin/google-chrome-stable`、`/usr/bin/chromium`、`/usr/bin/chromium-browser`

装在非标准路径时用环境变量指定：

```bash
export ARCHIFY_CHROME=/path/to/chrome
```

---

## 运行契约

- **WHEN**：用户**显式指定**本 skill 时（不是根据语义自动判断，见"触发方式"）
- **SEE**：archify 产物路径（HTML 或 JSON）、期望的输出位置
- **DO**：确认有 Chrome → 执行导出脚本 → 校验产物
- **CHECK**：退出码为 0，且产物文件头是 `<svg` 或 `<?xml`
- **STOP**：以下情况停止并明确告知用户，**绝不自行安装任何东西**
  - 未检测到 archify skill → 提示用户自行安装（见"前置检测"）
  - 无 Chrome / Chromium → 提示用户自行安装
  - 输入不是 archify 产物 → 确认输入文件

---

## 导出

```bash
node scripts/export.mjs <artifact.html> svg [out.svg]
node scripts/export.mjs <spec.json> svg [out.svg]
```

第三个参数两种写法都支持：

- **以 `.svg` 结尾** → 视为输出**文件路径**（脚本会在导出后重命名到位）
- **其他** → 视为输出**目录**，文件名由 archify 的 `diagramFilename()` 决定

省略时输出到产物同目录。

示例：

```bash
export ARCHIFY_CHROME=/path/to/chrome
node scripts/export.mjs docs/pipeline.html svg docs/pipeline.svg
```

成功输出：

```
SVG  /abs/path/archify.svg  886x660, 57330 bytes
     via Archify.exportMenu.run('svg') in chrome-headless-shell
```

| 退出码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 运行失败（产物缺失、Chrome 异常等） |
| 2 | 参数错误（用法不对） |
| 3 | 未检测到 archify skill（已打印安装提示，未做任何安装动作） |

---

## 失败处理

| 现象 | 含义 | 处理 |
|---|---|---|
| `ARCHIFY_CHROME points to a missing file: X` | 环境变量指向了不存在的路径 | 修正路径，或取消该变量改用标准路径 |
| `Chrome/Chromium not found` | 未安装，或不在标准路径 | **提示用户自行安装**，并告知可用 `ARCHIFY_CHROME` 指定路径；不要自行下载安装 |
| `Archify.exportMenu.run never became available` | 输入不是 archify 产物，或 archify 版本不兼容 | 确认输入文件 |
| `export ran but no completed svg file appeared` | 导出已触发但文件未落盘 | 检查输出目录写权限与磁盘空间 |

---

## 边界

- **只覆盖 SVG**。脚本底层同一个调用也支持 png / jpeg / webp / webm / share-card，但本 skill 不覆盖这些格式，也不涉及"导出后如何嵌入文档"
- **依赖内部 API**：`Archify.exportMenu.run` 是上游 archify 的内部实现，非公开契约。archify 大版本升级后若失效，需重新确认入口
- **文件名默认不可控**：不指定输出文件路径时，文件名由 archify 的 `diagramFilename()` 决定（实测通常是 `archify.svg`）；`svg` 格式可用 `.svg` 结尾的第三参自定义
- **同名文件会被覆盖**：这是预期行为，不是错误

---

## 更多资源

- 导出脚本：[scripts/export.mjs](scripts/export.mjs)
