---
name: playwright-browser
description: >
  完整浏览器自动化（Playwright 驱动，无需 Chrome 扩展）：截图、截屏、网页截图、打开网页、点击按钮、填写表单、输入文字、下拉选择、提取网页内容、滚动采集、多步骤自动化流程、登录保持、执行JS、批量操作。
  Use when：用户提到截图、截屏、screenshot、网页截图、打开网页看看、浏览器自动化、点击、填表、批量截图、批量抓取、爬虫、scrape、无头浏览器、headless。也可在内置 browser 工具不可用时作为替代。
  NOT for：简单的纯文本网页内容获取（用 web_fetch）、API 调用。
  注意：本 Skill 通过 exec 执行 python3 脚本驱动本地 Chrome，不需要 Chrome 扩展，不需要内置 browser 工具。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌐"
    os: ["darwin", "linux"]
    requires:
      bins: ["python3"]
---

# 浏览器自动化

> **Playwright 驱动的完整浏览器自动化。只使用 exec 工具执行 bash 命令。不要调用 browser 工具。**

## 调用方式

```bash
python3 {{SKILL_DIR}}/scripts/browser.py <命令> '<JSON参数>'
```

当参数包含中文或特殊字符时，用文件传参：

```bash
cat > /tmp/browser_args.json << 'BROWSEREOF'
{"url": "https://example.com", "selector": "#search"}
BROWSEREOF
python3 {{SKILL_DIR}}/scripts/browser.py click @/tmp/browser_args.json
```

## 前置检查

每次首次使用前，先检查环境：

```bash
python3 {{SKILL_DIR}}/scripts/browser.py check '{}'
```

如果返回 `"status": "issues"`：
- 如果缺 playwright → 执行 `python3 {{SKILL_DIR}}/scripts/browser.py install '{}'`
- 如果缺浏览器 → 告知用户安装 Chrome（https://www.google.cn/chrome/）

本 Skill 直接使用系统已安装的 Chrome/Edge/Chromium，**不需要翻墙，不需要额外下载浏览器**。

**检查点**：`check` 返回 `"browser_available": true`。如果为 false，停止并告知用户具体问题。

## 🔒 必须执行的命令（非建议）

### 命令 1：环境检查

```bash
python3 {{SKILL_DIR}}/scripts/browser.py check '{}'
```

### 命令 2：打开网页

```bash
python3 {{SKILL_DIR}}/scripts/browser.py navigate '{"url": "https://example.com"}'
```

可选参数：
- `wait_for`：等待指定 CSS 选择器出现
- `timeout`：超时毫秒数（默认 30000）
- `session_file`：加载已保存的登录状态

### 命令 3：截图

```bash
python3 {{SKILL_DIR}}/scripts/browser.py screenshot '{"url": "https://example.com", "output": "/tmp/page.png"}'
```

可选参数：
- `full_page`：true 截取整个可滚动页面
- `wait_for`：等待指定元素出现后再截图

### 命令 4：点击元素

```bash
python3 {{SKILL_DIR}}/scripts/browser.py click '{"url": "https://example.com", "selector": "#submit-btn"}'
```

可选参数：
- `screenshot_after`：点击后截图保存路径
- `wait_for`：点击前等待指定元素

### 命令 5：输入文字

```bash
python3 {{SKILL_DIR}}/scripts/browser.py input '{"url": "https://example.com", "selector": "#search-box", "text": "搜索内容"}'
```

可选参数：
- `clear`：true（默认）先清空再输入，false 追加输入
- `press_enter`：true 输入后按回车
- `screenshot_after`：输入后截图

### 命令 6：提取页面内容

```bash
python3 {{SKILL_DIR}}/scripts/browser.py extract '{"url": "https://example.com", "mode": "text"}'
```

mode 选项：
- `text`：提取纯文本（默认）
- `html`：提取 HTML
- `all_links`：提取所有链接
- `table`：提取表格数据

可选参数：
- `selector`：指定提取区域（默认 body）

### 命令 7：滚动采集

```bash
python3 {{SKILL_DIR}}/scripts/browser.py scroll '{"url": "https://example.com", "selector": ".item", "times": 5, "delay": 1000}'
```

### 命令 8：下拉框选择

```bash
python3 {{SKILL_DIR}}/scripts/browser.py select '{"url": "https://example.com", "selector": "#city", "label": "北京"}'
```

### 命令 9：执行 JavaScript

```bash
python3 {{SKILL_DIR}}/scripts/browser.py evaluate '{"url": "https://example.com", "script": "document.title"}'
```

### 命令 10：保存登录状态

```bash
python3 {{SKILL_DIR}}/scripts/browser.py save_session '{"url": "https://example.com/login", "wait_seconds": 60}'
```

会打开有头浏览器，用户手动登录后自动保存 Cookie 到 `/tmp/browser_session.json`。

### 命令 11：多步骤自动化

```bash
cat > /tmp/steps.json << 'STEPSEOF'
{
  "steps": [
    {"action": "goto", "url": "https://www.baidu.com"},
    {"action": "input", "selector": "#kw", "text": "OpenClaw"},
    {"action": "press", "selector": "#kw", "key": "Enter"},
    {"action": "wait", "selector": "#content_left"},
    {"action": "screenshot", "output": "/tmp/search_result.png"},
    {"action": "extract", "selector": "#content_left"}
  ]
}
STEPSEOF
python3 {{SKILL_DIR}}/scripts/browser.py multi_step @/tmp/steps.json
```

multi_step 支持的 action：
- `goto`：打开 URL（参数：url）
- `click`：点击（参数：selector）
- `click_and_goto`：点击链接并跳转到目标页面（参数：selector）。自动处理新标签页打开和反爬跳转链接（如百度搜索结果），**点击链接时优先使用此 action 而不是 click**
- `input`：输入（参数：selector, text, clear）
- `press`：按键（参数：selector, key）
- `wait`：等待元素（参数：selector, state）
- `screenshot`：截图（参数：output, full_page）
- `extract`：提取文本（参数：selector）
- `select`：下拉选择（参数：selector, value/label）
- `scroll`：滚动到底部（参数：delay）
- `sleep`：等待（参数：seconds）
- `evaluate`：执行 JS（参数：script）

## 执行流程

### 第 1 步：环境检查

执行命令 1（check）。

- 如果 `browser_available` 为 true → 继续第 2 步
- 如果为 false → 执行 `install` 命令，再重新 check

### 第 2 步：判断使用哪个命令

**核心规则：每次 exec 都会启动一个全新的浏览器，操作完就关闭。所以多个操作之间状态不共享。**

| 场景 | 用哪个命令 | 原因 |
|------|----------|------|
| 只截图一个网页 | `screenshot` | 单步操作 |
| 只提取一个网页内容 | `extract` | 单步操作 |
| 打开网页 + 输入 + 搜索 + 截图 | **`multi_step`** | 多步操作，需要同一个浏览器 |
| 打开网页 + 点击链接 + 截图 | **`multi_step`** | 多步操作 |
| 搜索 + 提取结果 | **`multi_step`** | 多步操作 |
| 登录 + 后续操作 | `save_session` + 带 `session_file` 的命令 | 登录需要有头模式 |

**简单判断：如果用户的需求涉及 2 个以上浏览器操作（打开+输入、打开+点击、搜索+截图等），必须用 `multi_step`，不要拆成多次 exec。**

### 第 3 步：构造命令并执行

对于 `multi_step`，用文件传参：

```bash
cat > /tmp/steps.json << 'STEPSEOF'
{
  "steps": [
    {"action": "goto", "url": "https://www.baidu.com"},
    {"action": "input", "selector": "#kw", "text": "搜索词"},
    {"action": "press", "selector": "#kw", "key": "Enter"},
    {"action": "wait", "selector": "#content_left"},
    {"action": "screenshot", "output": "/tmp/result.png"},
    {"action": "extract", "selector": "#content_left"}
  ]
}
STEPSEOF
python3 {{SKILL_DIR}}/scripts/browser.py multi_step @/tmp/steps.json
```

### 第 4 步：处理结果

- 截图 → 告知用户文件路径
- JSON 输出 → 整理成用户友好的格式
- 错误 → 按故障处理章节排查

## ✅ 完成定义（Definition of Done）

| 检查项 | 验证方式 |
|--------|---------|
| ✅ 执行了环境检查 | check 返回 browser_available: true |
| ✅ 使用了 browser.py | 执行了 `python3 {{SKILL_DIR}}/scripts/browser.py` |
| ✅ 产出了结果 | 截图文件存在 / 内容已输出 / 操作已完成 |
| ✅ 按格式汇报 | 使用了进度汇报格式 |

## ❌ 禁止行为（违反 = 任务失败）

```
❌ 不执行环境检查就直接使用命令
❌ 把 playwright-browser 当作 tool name 直接调用（必须用 exec 执行 python3 脚本）
❌ 编造浏览器输出结果
❌ 遇到错误直接放弃，不尝试故障处理
❌ 用 web_fetch 替代需要 JS 渲染的页面操作
```

## 工具列表

| 命令 | 说明 | 必填参数 | 可选参数 |
|------|------|----------|----------|
| `check` | 环境检查 | 无 | 无 |
| `install` | 安装 Playwright + Chromium | 无 | 无 |
| `navigate` | 打开网页 | `url` | `wait_for`, `timeout`, `session_file` |
| `screenshot` | 截图 | `url`, `output` | `full_page`, `wait_for` |
| `click` | 点击 | `selector` | `url`, `screenshot_after`, `wait_for` |
| `input` | 输入 | `selector`, `text` | `url`, `clear`, `press_enter`, `screenshot_after` |
| `extract` | 提取内容 | `url` | `mode`, `selector`, `wait_for` |
| `scroll` | 滚动采集 | `url` | `selector`, `times`, `delay`, `screenshot_after` |
| `select` | 下拉选择 | `selector` | `url`, `value`, `label` |
| `wait` | 等待元素 | `selector` | `url`, `state`, `timeout` |
| `evaluate` | 执行 JS | `script` | `url` |
| `save_session` | 保存登录 | `url` | `output`, `wait_seconds` |
| `multi_step` | 多步骤 | `steps` | `session_file`, `headless` |

## 约束

- 需要系统已安装 Chrome/Edge/Chromium（直接使用，无需额外下载）
- 无头模式下无法处理验证码，需要登录的场景用 `save_session`（有头模式）
- 截图文件建议存到 `/tmp/` 或 `~/Desktop/`
- `multi_step` 中每个 step 默认 `stop_on_error: true`，某步失败后续不执行

## 故障处理

### 浏览器未检测到
安装 Google Chrome：https://www.google.cn/chrome/（国内地址，无需翻墙）

### Playwright 未安装
```bash
python3 {{SKILL_DIR}}/scripts/browser.py install '{}'
```

### 元素找不到（Selector 超时）
1. 先用 `extract` 的 `all_links` 或 `html` 模式查看页面结构
2. 调整 selector
3. 加 `wait_for` 等待元素加载

### 页面加载超时
增加 timeout：
```bash
python3 {{SKILL_DIR}}/scripts/browser.py navigate '{"url": "https://slow-site.com", "timeout": 60000}'
```

### 被反爬拦截
使用 `save_session` 先手动登录，后续操作带 `session_file` 参数。

## 版本历史

### v1.0.0
- 初始版本
- 基于 Playwright，支持完整浏览器交互
- 13 个命令：navigate、screenshot、click、input、extract、scroll、select、wait、evaluate、save_session、multi_step、check、install
- 直接使用系统已安装的 Chrome/Edge/Chromium，无需翻墙，无需额外下载
- 支持多步骤自动化流程
