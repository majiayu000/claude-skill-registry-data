---
name: browser-use-zh-remote-browser
description: 从沙箱远程机器控制本地浏览器。当代理在沙箱中运行（无 GUI）时，需要导航网站、与网页交互、填写表单、截图或通过隧道暴露本地开发服务器时使用。
allowed-tools: Bash(browser-use:*)
---

# 沙箱代理的浏览器自动化

此技能适用于在**沙箱远程机器**（云虚拟机、CI、编码代理）上运行的代理，这些代理需要控制无头浏览器。

## 前置条件

```bash
browser-use doctor    # 验证安装
```

安装详情请参见 https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## 核心工作流程

1. **导航**: `browser-use open <url>` — 如需要则启动无头浏览器
2. **检查**: `browser-use state` — 返回可点击元素及其索引
3. **交互**: 使用 state 返回的索引（`browser-use click 5`、`browser-use input 3 "text"`）
4. **验证**: `browser-use state` 或 `browser-use screenshot` 确认结果
5. **重复**: 浏览器在命令之间保持打开
6. **清理**: 完成后使用 `browser-use close`

## 浏览器模式

```bash
browser-use open <url>                                    # 默认：无头 Chromium
browser-use cloud connect                                 # 配置云浏览器并连接
browser-use --connect open <url>                          # 通过 CDP 自动发现运行中的 Chrome
browser-use --cdp-url ws://localhost:9222/... open <url>  # 通过 CDP URL 连接
```

## 命令

```bash
# 导航
browser-use open <url>                    # 导航到 URL
browser-use back                          # 后退
browser-use scroll down                   # 向下滚动（--amount N 指定像素数）
browser-use scroll up                     # 向上滚动
browser-use switch <tab>                  # 按索引切换标签页
browser-use close-tab [tab]              # 关闭标签页（不指定则关闭当前标签页）

# 页面状态 — 始终先运行 state 获取元素索引
browser-use state                         # URL、标题、可点击元素及索引
browser-use screenshot [path.png]         # 截图（不指定路径返回 base64，--full 截取整页）

# 交互 — 使用 state 返回的索引
browser-use click <index>                 # 按索引点击元素
browser-use click <x> <y>                 # 按像素坐标点击
browser-use type "text"                   # 在聚焦元素中输入文本
browser-use input <index> "text"          # 点击元素后输入文本
browser-use keys "Enter"                  # 发送键盘按键（也支持 "Control+a" 等）
browser-use select <index> "option"       # 选择下拉菜单选项
browser-use upload <index> <path>         # 上传文件到文件输入框
browser-use hover <index>                 # 悬停在元素上
browser-use dblclick <index>              # 双击元素
browser-use rightclick <index>            # 右键点击元素

# 数据提取
browser-use eval "js code"                # 执行 JavaScript，返回结果
browser-use get title                     # 页面标题
browser-use get html [--selector "h1"]    # 页面 HTML（或限定到选择器范围）
browser-use get text <index>              # 元素文本内容
browser-use get value <index>             # 输入框/文本域的值
browser-use get attributes <index>        # 元素属性
browser-use get bbox <index>              # 边界框（x, y, width, height）

# 等待
browser-use wait selector "css"           # 等待元素（--state visible|hidden|attached|detached，--timeout 毫秒）
browser-use wait text "text"              # 等待文本出现

# Cookie 管理
browser-use cookies get [--url <url>]     # 获取 Cookie（可按 URL 过滤）
browser-use cookies set <name> <value>    # 设置 Cookie（--domain, --secure, --http-only, --same-site, --expires）
browser-use cookies clear [--url <url>]   # 清除 Cookie
browser-use cookies export <file>         # 导出为 JSON
browser-use cookies import <file>         # 从 JSON 导入

# Python — 持久会话，可访问浏览器
browser-use python "code"                 # 执行 Python（变量在调用之间持久保存）
browser-use python --file script.py       # 运行文件
browser-use python --vars                 # 显示已定义的变量
browser-use python --reset                # 清除命名空间

# 会话管理
browser-use close                         # 关闭浏览器并停止守护进程
browser-use sessions                      # 列出活跃会话
browser-use close --all                   # 关闭所有会话
```

Python 的 `browser` 对象提供：`browser.url`、`browser.title`、`browser.html`、`browser.goto(url)`、`browser.back()`、`browser.click(index)`、`browser.type(text)`、`browser.input(index, text)`、`browser.keys(keys)`、`browser.upload(index, path)`、`browser.screenshot(path)`、`browser.scroll(direction, amount)`、`browser.wait(seconds)`。

## 隧道

通过 Cloudflare 隧道将本地开发服务器暴露给浏览器。

```bash
browser-use tunnel <port>                 # 启动隧道（幂等操作）
browser-use tunnel list                   # 显示活跃隧道
browser-use tunnel stop <port>            # 停止隧道
browser-use tunnel stop --all             # 停止所有隧道
```

## 命令链接

命令可以使用 `&&` 链接。浏览器通过守护进程持久存在，因此链接是安全高效的。

```bash
browser-use open https://example.com && browser-use state
browser-use input 5 "user@example.com" && browser-use input 6 "password" && browser-use click 7
```

当不需要中间输出时可以链接命令。当需要解析 `state` 来发现索引时，应分别运行。

## 常见工作流程

### 暴露本地开发服务器

```bash
python -m http.server 3000 &                      # 启动开发服务器
browser-use tunnel 3000                            # → https://abc.trycloudflare.com
browser-use open https://abc.trycloudflare.com     # 浏览隧道
```

隧道独立于浏览器会话，在 `browser-use close` 后仍然存在。

## 全局选项

| 选项 | 说明 |
|------|------|
| `--headed` | 显示浏览器窗口 |
| `--connect` | 通过 CDP 自动发现运行中的 Chrome |
| `--cdp-url <url>` | 通过 CDP URL 连接（`http://` 或 `ws://`） |
| `--session NAME` | 指定命名会话（默认："default"） |
| `--json` | 输出为 JSON 格式 |

## 提示

1. **始终先运行 `state`** 以查看可用元素及其索引
2. **会话持久存在** — 浏览器在命令之间保持打开，直到你关闭它
3. **隧道独立存在** — 在 `browser-use close` 后仍然保留
4. **`tunnel` 是幂等的** — 对同一端口再次调用会返回已有的 URL

## 故障排除

- **浏览器无法启动？** 先 `browser-use close` 再重试。运行 `browser-use doctor` 检查。
- **找不到元素？** 先 `browser-use scroll down` 再 `browser-use state`
- **隧道不工作？** 用 `which cloudflared` 检查，用 `browser-use tunnel list` 查看活跃隧道

## 清理

```bash
browser-use close                         # 关闭浏览器会话
browser-use tunnel stop --all             # 停止隧道（如果有）
```
