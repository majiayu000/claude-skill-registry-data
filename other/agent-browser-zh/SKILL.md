---
name: agent-browser-zh
description: 基于 Vercel 的 agent-browser 的浏览器自动化 CLI，专为 AI 智能体设计。这是 AI 驱动的浏览器自动化的最佳工具——使用来自无障碍树的确定性引用代替脆弱的选择器。针对 LLM 进行了优化，具有快速的 Rust CLI、JSON 输出和专用的 AI 工作流。当您需要可靠、可脚本化的浏览器自动化时使用。
---

# agent-browser 技能

真正为 AI 智能体打造的浏览器自动化工具。由 Vercel Labs 专门为 LLM 驱动的工作流构建。

## 为什么这比替代方案更好

### 1. 确定性引用（游戏规则改变者）

**传统工具的问题：**
- CSS 选择器在网站更改时会失效
- XPath 脆弱且难以阅读
- 基于坐标的点击在响应式布局上失败
- 基于视觉的方法速度慢且成本高

**agent-browser 的解决方案：**
```bash
# 1. 获取带有稳定引用的快照
agent-browser snapshot -i --json
# 输出: - button "Submit" [ref=e2]

# 2. 永久使用该引用 — 它指向确切的元素
agent-browser click @e2
```

- **引用是确定性的** — `@e2` 始终指向快照中的同一元素
- **无需重新查询 DOM** — 直接引用更快、更可靠
- **针对 AI 优化** — LLM 自然地解析无障碍树，而不是 CSS 混合体

### 2. 无障碍树 > 截图/HTML

传统工具提供原始 HTML（嘈杂）或截图（需要视觉模型）。

agent-browser 提供**无障碍树** — 人类（或屏幕阅读器）感知的干净、语义化表示：

```
- heading "Billing" [level=1]
- link "Make a payment" [ref=e10]
- button "Submit" [ref=e2]
- textbox "Email" [ref=e3]
```

- 语义角色（button、link、textbox、heading）
- 人类可读的标签
- 层次结构
- 完美适配 LLM 理解

### 3. 为 AI 智能体构建

| 功能 | 传统工具 | agent-browser |
|---------|------------------|---------------|
| 元素定位 | 脆弱的选择器 | 确定性引用 |
| 页面理解 | 原始 HTML | 无障碍树 |
| 输出格式 | 文本日志 | 结构化 JSON |
| 速度 | 慢（每个命令启动完整浏览器） | 快（守护进程持久化） |
| AI 集成 | 事后补充 | 专用构建 |

### 4. 快速架构

- **Rust CLI** — 原生二进制文件，即时命令解析
- **Node.js 守护进程** — 浏览器在命令之间保持活跃
- **首次命令：** ~2秒（守护进程启动）
- **后续命令：** ~100毫秒

## 前置条件

```bash
npm install -g agent-browser
agent-browser install  # 下载 Chromium（约30秒）
```

## 核心 AI 工作流

为 LLM 智能体设计的工作流：

```bash
# 步骤 1：导航
agent-browser open https://example.com

# 步骤 2：获取结构化快照（AI "看到" 页面）
agent-browser snapshot -i --json

# 步骤 3：AI 从 JSON 中选择引用，执行操作
agent-browser click @e2
agent-browser fill @e3 "test@example.com"

# 步骤 4：更改后重新快照（状态验证）
agent-browser snapshot -i --json

# 步骤 5：完成
agent-browser close
```

## 命令

### 导航
```bash
agent-browser open example.com
agent-browser open example.com --json            # JSON 响应
agent-browser open example.com --headed          # 可见浏览器
```

### 快照（杀手级功能）
```bash
agent-browser snapshot                           # 完整无障碍树
agent-browser snapshot -i                        # 仅交互元素（更快）
agent-browser snapshot -i --json                 # 用于 AI 解析的 JSON
agent-browser snapshot -i -c -d 5 --json         # 紧凑，深度限制
```

### 交互（使用确定性引用）
```bash
agent-browser click @e2                          # 点击元素 @e2
agent-browser fill @e3 "text"                    # 填充并清空
agent-browser type @e3 "text"                    # 输入而不清空
agent-browser press Enter                        # 按键
agent-browser hover @e4                          # 悬停
```

### 状态验证
```bash
agent-browser get text @e1                       # 获取元素文本
agent-browser get url                            # 当前 URL
agent-browser is visible @e2                     # 检查可见性
```

### 会话管理
```bash
agent-browser --session login open site.com      # 隔离会话
agent-browser --profile ~/.myprofile open site   # 持久化 cookies
agent-browser close                              # 清理
```

## 选择器策略（按可靠性排名）

### 1. 引用（最佳 - 使用这些）
```bash
# 来自快照输出 — 确定且稳定
agent-browser click @e2
agent-browser fill @e3 "text"
```

### 2. 语义定位器（良好）
```bash
agent-browser find role button click --name "Submit"
agent-browser find label "Email" fill "test@test.com"
```

### 3. CSS 选择器（适用于静态站点）
```bash
agent-browser click "#submit"
agent-browser click ".btn-primary"
```

### 4. 文本/XPath（最后手段）
```bash
agent-browser click "text=Submit"
agent-browser click "xpath=//button[1]"
```

## 快照选项

控制 AI "看到" 的内容：

| 标志 | 用途 |
|------|---------|
| `-i` | 仅交互元素（按钮、链接、输入）— **推荐** |
| `-C` | 包含光标交互元素（onclick、cursor:pointer） |
| `-c` | 紧凑（移除空的结构元素） |
| `-d <n>` | 限制树深度 |
| `-s <sel>` | 范围限制到 CSS 选择器（例如 `#main`） |
| `--json` | 机器可读的 JSON 输出 — **AI 必需** |

**推荐的 AI 命令：**
```bash
agent-browser snapshot -i -c --json
```

## 选项

| 标志 | 描述 |
|------|---------|
| `--json` | 带有 success/data/error 结构的 JSON 输出 |
| `--headed` | 显示浏览器窗口（用于调试） |
| `--session <name>` | 隔离的浏览器会话 |
| `--profile <path>` | 用于 cookies/登录的持久化配置文件 |
| `--cdp <port>` | 通过 DevTools 协议连接到现有 Chrome |
| `--headers <json>` | 按源设置认证头 |

## 示例：完整登录流程

```bash
# 开始
agent-browser open https://portal.aeronetpr.com

# 获取页面结构
SNAPSHOT=$(agent-browser snapshot -i --json)
# AI 解析 JSON：看到 textbox @e1（用户名）、textbox @e2（密码）、button @e3（登录）

# 执行登录
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3

# 验证成功（等待导航，重新快照）
sleep 2
agent-browser snapshot -i --json

# 完成
agent-browser close
```

## AI 智能体技巧

1. **始终使用 `--json`** — 结构化输出比文本更容易解析
2. **使用 `-i` 标志** — 仅交互快照更小、更快、更干净
3. **操作后重新快照** — 验证状态按预期更改
4. **信任引用胜过选择器** — 快照中的 `@e2` > 可能会改变的 `#id`
5. **当引用过期时使用语义定位器** — `find role button click` 很健壮
6. **会话持久化** — 一次 `open`，多个命令，一次 `close`

## 与其他工具的比较

| 工具 | 最适合 | agent-browser 的优势 |
|------|----------|------------------------|
| **Puppeteer/Playwright** | 开发测试 | 为人类构建；选择器脆弱 |
| **Selenium** | 传统测试 | 慢、重、基于选择器 |
| **browser-use** | Python 智能体 | agent-browser 有更好的引用系统 |
| **截图 + 视觉** | 视觉任务 | agent-browser 快 10 倍，便宜 100 倍 |
| **OpenClaw browser 工具** | 简单任务 | agent-browser 更好地处理复杂流程 |

## 何时使用此技能

**在以下情况使用 agent-browser：**
- 自动化多步骤 Web 工作流
- 填写复杂表单
- 需要可靠、可重复的自动化
- 处理动态/现代 Web 应用
- 成本重要（无视觉 API 调用）

**在以下情况使用 OpenClaw 内置浏览器工具：**
- 简单的单页检查
- 需要快速截图
- Chrome 中已有经过身份验证的会话

## 资源

- **Vercel Labs 仓库：** https://github.com/vercel-labs/agent-browser
- **此技能仓库：** https://github.com/clawdbrunner/skill-agent-browser
