---
name: laohan-luping
description: 口播稿转录屏脚本（CLI+浏览器），自动生成ffmpeg录制脚本并输出MP4。Use when 用户说"录屏""录制教程""录视频""录一段""screen record""补录""口播稿转录屏""浏览器录屏""录网页"或提到录制Claude Code画面或浏览器操作。
version: "1.2.0"
---

# 录屏自动化：口播稿 → 录屏脚本 → MP4

> **边界（2026-09-20治理P2-20）**：本工具不进入episode生产合同。episode内的录屏只响应⑨冻结的`LOCAL_CAPTURE`请求（Prompt 08 / local-capture-mvp），无请求时为`NOT_NEEDED`；勿在episode上下文用本工具发起录屏。独立研究、demo或Jeffrey明确要求的自由录屏不受此限。

输入一篇口播稿（或录屏指示），自动生成 bash 录屏脚本。脚本编排 CLI 操作（tmux+Claude Code）和浏览器操作（Playwright headed），ffmpeg 录物理屏幕，输出 1080p MP4。

## 核心理念

**口播稿即脚本蓝图。** 每段口播对应一个屏幕操作（CLI 命令/浏览器导航/静态等待），从口播稿里提取出操作序列和时长，填入录制模板。

**看到什么录什么。** ffmpeg 录物理屏幕，tmux 前台显示终端，Playwright headed 显示浏览器。两种"演员"按口播稿交替出场。

**录屏是素材，不是生产。** 录制过程中的临时文件全部自动清理，只保留最终 MP4。

## 工作流

### 1. 输入口播稿

接收用户提供的：
- 口播稿文件路径（`script.md`）
- 或录屏指示文件路径（`录屏指示.md`）
- 或直接描述要录制什么

如果用户提供了口播稿但没有录屏指示 → 根据口播稿内容自动推断每段对应的操作。
如果用户提供了录屏指示 → 直接用指示里的操作序列。

- **完成条件：** 拿到完整的操作序列和每步时长

### 2. 解析口播稿→操作序列

从口播稿/录屏指示中提取。操作分为三种类型：

**CLI 操作**（tmux + Claude Code）：

| 口播段落 | 屏幕操作 | 脚本动作 |
|---------|---------|---------|
| "说「抓今天的AI精选」" | 执行命令 | `send_cmd "抓今天的AI精选"` |
| "说「帮我写口播稿」" | 执行命令 | `send_cmd "帮我写口播稿"` |
| "展示 output/ 文件夹" | 查看命令 | `send_cmd "ls output/"` |

**浏览器操作**（Playwright headed）：

| 口播段落 | 屏幕操作 | 脚本动作 |
|---------|---------|---------|
| "打开 GitHub 项目页" | 导航到 URL | `browser_goto "https://github.com/..."` |
| "看一下 README" | 页面滚动 | `browser_scroll 500` |
| "点击安装文档" | 点击链接 | `browser_click "a[href='docs']"` |
| "展示项目截图" | 静态展示 | `browser_wait 3000` |

**静态操作**（纯等待）：

| 口播段落 | 屏幕操作 | 脚本动作 |
|---------|---------|---------|
| 开场白/过渡/结尾 | 静态画面 | `sleep N` |

提取规则：
- 引号里的内容（「」或""）→ 直接作为 send_cmd 的参数
- 提到 URL / GitHub / 网站 / 文档 → 浏览器操作
- 提到终端/命令/CLI → CLI 操作
- 纯叙述段落 → 按口播时长估算 sleep 秒数（正常语速约 3 字/秒）
- CLI 命令需要等 Claude 完成的 → 加 `wait_for_claude`
- 浏览器页面需要阅读时间的 → 加 `browser_wait`

- **完成条件：** 生成结构化的操作列表，每条含类型（cli/browser/static）、内容、等待方式、标签

### 3. 环境检测

```bash
which ffmpeg && which tmux && which node
ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep "Capture screen"
node -e "require('playwright')" 2>/dev/null && echo "playwright OK" || echo "playwright missing"
```

- 缺工具 → 提示安装
- 多屏幕 → 让用户确认索引
- 缺 Playwright → `npm install playwright`
- **完成条件：** 确认屏幕索引 + Playwright 可用（如需浏览器段）

### 4. 生成录制脚本

基于 `scripts/record_template.sh` 模板生成。模板包含：
- ffmpeg 录屏启动/停止
- tmux 会话管理（CLI 段）
- Playwright 浏览器控制（浏览器段）
- `send_cmd()`、`wait_for_claude()`、`browser_*()` 函数
- 1080p 转码 + 临时文件清理

填充内容：
- **CLI 段**：命令序列块（send_cmd + wait_for_claude）
- **浏览器段**：导航 JSON 文件（`browser_actions.json`）
- **切换时机**：口播稿段落顺序决定 CLI/浏览器交替

如果只有 CLI 段 → 纯 CLI 模式（不启动浏览器）。
如果只有浏览器段 → 纯浏览器模式（不启动 tmux）。
两者都有 → 混合模式。

生成脚本写到用户指定目录（或当前目录），文件名格式：`record_<教程名>.sh`

### 5. 交付+指导

输出：
1. 生成的 `record_xxx.sh` 脚本（含 `browser_actions.json` 如有浏览器段）
2. 运行命令：`bash record_xxx.sh`
3. 提醒：
   - 终端全屏（Cmd+Enter）
   - 开勿扰模式
   - 按回车后别碰键盘鼠标
   - Gate 确认框按回车继续

**不自动执行脚本** — 录屏需要用户手动在终端启动。

## 操作规则

- **口播稿驱动** — 每个操作都能追溯到口播稿的某一段
- **不自动执行录屏脚本** — 涉及屏幕接管，必须用户手动运行
- **屏幕索引需确认** — 不同机器配置不同，不能硬编码
- **CLI/浏览器交替自然** — 切换时加短暂 sleep（1-2s），模拟自然切换
- **浏览器滚动模拟真人** — 分段滚动 200-400px，间隔 500-800ms
- **静态段落用 sleep** — 开场/过渡/结尾等无操作段落，按口播字数÷3估算秒数
- **临时文件全部清理** — Claude 工作目录 + raw 文件 + browser JSON，只保留最终 MP4

## 不适用场景

- 录制桌面应用（非终端非浏览器） → 用 OBS
- 带声音解说 → 需额外配置音频输入
- 实时直播 → 这是录制方案不是直播方案
- 需要登录态的浏览器操作 → 用 opencli Browser Bridge

## 浏览器操作 JSON 格式

```json
{
  "viewport": { "width": 1920, "height": 1080 },
  "steps": [
    { "action": "goto", "url": "https://github.com/xxx", "label": "打开项目页" },
    { "action": "wait", "ms": 3000 },
    { "action": "scroll", "pixels": 600, "smooth": true },
    { "action": "wait", "ms": 2000 },
    { "action": "click", "selector": "a[href='/xxx/docs']", "label": "点击文档" },
    { "action": "wait", "ms": 3000 }
  ]
}
```

支持的 action：`goto`、`wait`、`scroll`、`click`。

## 踩坑速查

| 问题 | 原因 | 解决 |
|------|------|------|
| 录错屏幕 | 多显示器索引不对 | `ffmpeg -list_devices` 确认 |
| tmux 里 claude 立即退出 | 网络/初始化偶发问题 | 重跑 |
| 画面静止 | claude 等待输入 | 手动按回车 |
| 视频太大 | CRF 值太低 | 改 `-crf 23` |
| 命令没发完 | 超时 | 增大 `max_wait` |
| 浏览器窗口尺寸不对 | viewport 不匹配 | JSON 里设 viewport |
| Playwright 启动失败 | 未安装 | `npm install playwright` |
