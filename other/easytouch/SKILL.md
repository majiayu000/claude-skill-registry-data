---
name: easytouch
description: 跨平台系统自动化操作工具，支持 Windows、Linux、macOS。提供 CLI 命令行和 MCP 服务器两种使用方式，支持鼠标键盘控制、屏幕截图、窗口管理、系统信息查询等功能。
---

# EasyTouch Skill

## 环境要求

使用 npm 安装时：Node.js >= 18（npm 安装场景）

>  直接从 Github Release 下载文件后添加环境变量。



## 安装方式

### npm 安装

```bash
# 推荐：自动匹配当前平台
npm install -g @whuanle/easytouch

# Windows
npm install -g easytouch-windows

# Linux
npm install -g easytouch-linux

# macOS
npm install -g easytouch-macos
```



安装后命令入口：

```bash
et help
```



## CLI 命令

### 核心命令

```bash
# 显示命令总览与参数格式
et help

# 显示当前运行时状态与主机平台信息
et status

# 列出各平台实现状态与能力模块
et platforms

# 显示 CLI/MCP 接口与能力映射概览
et interfaces

# 显示能力接入和运行时要求清单
et requirements

# 启动 MCP stdio 服务
et mcp-stdio

# 输出 MCP manifest（工具清单）JSON
et mcp-stdio --output json
```



### 自动化命令

默认命令执行输出结果内容为 json，如需直接输出文本可使用 `-output text` 指定。



#### 系统信息

| 命令 | 用途 |
| --- | --- |
| `system os-info` | 读取操作系统版本、架构、主机名等信息 |
| `system cpu-info` | 读取 CPU 架构与核心信息 |
| `system memory-info` | 读取内存总量、可用量与占用情况 |
| `system disk-list` | 列出磁盘与容量信息 |
| `system process-list` | 列出当前进程列表 |
| `system hardware-info` | 读取硬件概览（架构、核心、页大小、物理内存、虚拟内存、机器名） |
| `system network-info` | 读取网络适配器信息（IPv4、MAC、网卡类型、DHCP 状态） |

平台说明：

- Windows：全部可用。
- Linux：整体可用，`system network-info` 依赖 `ip` 命令。
- macOS：整体可用，信息主要来自 `sysctl`、`vm_stat`、`ifconfig` 等系统命令。



#### 鼠标操作

| 命令 | 用途 |
| --- | --- |
| `mouse position` | 读取当前鼠标坐标 |
| `mouse move --x <x> --y <y> [--duration-ms <ms>] [--jitter-px <px>] [--step-delay-ms <ms>]` | 以渐进轨迹移动鼠标，支持抖动与延迟，更接近人类操作 |
| `mouse click [--button <left\|right\|middle>] [--count <n>]` | 执行鼠标点击 |
| `mouse scroll --delta <amount>` | 执行鼠标滚轮滚动 |

平台说明：

- Windows：全部可用。
- Linux：依赖 `xdotool`，并要求运行在 X11 或 XWayland 会话中；Wayland 原生会话下可能被桌面环境限制。
- macOS：依赖系统 Accessibility 权限；未授权时鼠标读取和注入会失败。



参数说明：

- `--x` / `--y`：目标坐标（整数）
- `--duration-ms`：总移动时长（毫秒），默认 `280`
- `--jitter-px`：轨迹抖动幅度（像素），默认 `3`
- `--step-delay-ms`：每一步移动间隔（毫秒），默认 `8`
- `--button`：按键类型，`left`、`right`、`middle`
- `--count`：点击次数，默认 `1`
- `--delta`：滚动量，正负值分别代表不同方向



#### 窗口与应用

| 命令 | 用途 |
| --- | --- |
| `window list [--include-hidden] [--pid <pid>]` | 列出窗口，可按可见性和进程过滤 |
| `window foreground` | 读取当前前台窗口信息 |
| `window find --title <text> [--match <contains\|exact>] [--include-hidden] [--pid <pid>]` | 按标题查找窗口 |
| `window activate --handle <handle>` | 按句柄激活窗口 |
| `window show --handle <handle>` | 显示窗口并请求激活 |
| `window minimize --handle <handle>` | 最小化窗口 |
| `window maximize --handle <handle>` | 最大化窗口 |
| `window restore --handle <handle>` | 恢复窗口（从最小化/最大化） |
| `window move --handle <handle> --x <x> --y <y> [--width <n>] [--height <n>]` | 拖曳/移动窗口到指定坐标，可选调整尺寸 |
| `window close --handle <handle>` | 按句柄请求关闭窗口 |
| `app launch --target <path-or-uri>` | 启动应用、打开文件或 URI |

平台说明：

- Windows：全部可用。
- Linux：`window list`、`window foreground`、`window activate`、`window close` 可用；`window show`、`window minimize` 依赖 `xdotool`，`window maximize`、`window restore`、`window move` 依赖 `wmctrl` 和兼容 EWMH 的窗口管理器。
- Linux：整体要求 X11 或 XWayland 会话，Wayland 原生会话下窗口句柄和控制能力可能受限。
- macOS：窗口控制依赖 Accessibility 和 Automation 权限；`window show`、`window minimize`、`window maximize`、`window restore`、`window move`、`window close` 通过 `System Events` 操作，若同一进程里有多个同名窗口，系统会按首个匹配窗口执行。

参数说明：
- `--title`：窗口标题关键字
- `--match`：匹配模式，`contains` 或 `exact`
- `--include-hidden`：包含隐藏窗口
- `--pid`：按进程 ID 过滤
- `--handle`：窗口句柄（非负整数）
- `--x` / `--y`：窗口目标位置
- `--width` / `--height`：窗口目标尺寸（可选，不传则保持原尺寸）
- `--target`：可执行路径、文件路径或 URI



#### 剪贴板

| 命令 | 用途 |
| --- | --- |
| `clipboard get-text` | 读取剪贴板文本 |
| `clipboard set-text --text <value>` | 写入剪贴板文本 |
| `clipboard get-files` | 读取剪贴板中的文件列表 |
| `clipboard set-files --paths <path1;path2;...>` | 写入剪贴板文件列表（用于后续粘贴文件） |
| `clipboard set-image --path <image-file>` | 写入剪贴板图片（用于后续粘贴图片） |

平台说明：

- Windows：全部可用。
- Linux：依赖 `wl-copy` / `wl-paste` 或 `xclip` / `xsel`；缺少这些工具时，对应文本、文件、图片剪贴板能力不可用。
- macOS：文本剪贴板通过 `pbcopy` / `pbpaste`；文件和图片剪贴板通过 `osascript` / JXA 写入，若宿主进程缺少 Automation 权限可能失败。

参数说明：
- `--text`：要写入的文本内容
- `--paths`：多个文件路径，使用分号 `;` 分隔
- `--path`：单个图片文件路径



#### 键盘操作

| 命令 | 用途 |
| --- | --- |
| `keyboard key --key <name>` | 发送单个按键 |
| `keyboard hotkey --keys <combo>` | 发送组合键 |
| `keyboard type --text <value>` | 直接注入文本内容（直输模式） |
| `keyboard type-keys --text <value> [--key-delay-ms <ms>]` | 按键位逐字输入（模拟人类打字模式） |
| `keyboard ime-switch [--strategy <win-space\|alt-shift\|ctrl-shift>]` | 切换输入法 |
| `keyboard caps-lock [--state <toggle\|on\|off>]` | 控制大小写状态 |
| `keyboard paste [--expect-title <text>] [--match <contains\|exact>]` | 发送粘贴动作，可加窗口标题保护 |

平台说明：

- Windows：全部可用。
- Linux：依赖 `xdotool`，并要求运行在 X11 或 XWayland 会话中；Wayland 原生会话下键盘注入通常不稳定或被系统阻止。
- macOS：依赖 Accessibility 权限；`keyboard ime-switch` 的策略会映射到系统快捷键，是否真正切换输入法取决于系统当前输入源绑定。
- macOS：`keyboard caps-lock` 目前仅稳定支持 `toggle`，`on` / `off` 仍不保证可用。

参数说明：
- `--key`：按键名（如 `enter`、`esc`、`f5`）
- `--keys`：组合键（如 `ctrl+c`、`ctrl+shift+s`）
- `--text`：输入文本
- `--key-delay-ms`：模拟键位输入时每个按键之间的延迟
- `--strategy`：输入法切换快捷键策略
- `--state`：大小写状态，`toggle`、`on`、`off`
- `--expect-title`：执行粘贴前要求前台窗口标题匹配
- `--match`：标题匹配模式，`contains` 或 `exact`



#### 屏幕与截图

| 命令 | 用途 |
| --- | --- |
| `screen displays` | 列出显示器与分辨率信息 |
| `screen pixel-color --x <x> --y <y>` | 读取指定像素颜色 |
| `screen capture [--path <file>] [--display-id <id>] [--window-handle <handle>]` | 默认截取所有屏幕，或按屏幕/窗口定向截图 |

平台说明：

- Windows：全部可用。
- Linux：`screen displays` 依赖 `xrandr`，`screen capture` 依赖 `grim`、`gnome-screenshot`、`scrot` 或 `import` 之一。
- Linux：`screen capture --display-id` 和 `screen capture --window-handle` 仍未实现，当前只保证整桌面截图。
- Linux：Wayland 原生会话下，截图和像素读取可能受桌面权限或会话类型限制。
- macOS：`screen capture` 依赖系统 `screencapture` 命令；若系统未授予屏幕录制权限，截图或像素读取会失败。
- macOS：支持 `--display-id` 与 `--window-handle` 定向截图，但前提是目标窗口仍存在于当前 CoreGraphics 快照中。

参数说明：
- `--x` / `--y`：像素坐标
- `--path`：截图输出路径，不传则使用默认路径
- `--display-id`：指定屏幕 ID（来自 `screen displays`）
- `--window-handle`：指定窗口句柄（来自 `window list` / `window foreground`）

```bash
# 默认：截取所有屏幕
screen capture --path ./captures/all.png

# 截取指定屏幕
screen capture --display-id 1 --path ./captures/display-1.png

# 截取指定窗口
screen capture --window-handle 0x001A09F2 --path ./captures/window.png
```



#### 等待器

等待器用于“动作后确认状态”，避免脚本只执行动作却不验证结果。
典型用法：点击/输入/窗口切换之后，先等待目标条件成立，再继续下一步。
这样可以降低因为界面刷新延迟、窗口抢焦点、颜色尚未变化导致的误操作。

| 命令 | 用途 |
| --- | --- |
| `wait window --title <text> [--timeout-ms <ms>] [--match <contains\|exact>] [--foreground-only]` | 等待目标窗口出现或满足前台条件 |
| `wait focus --title <text> [--timeout-ms <ms>] [--match <contains\|exact>]` | 等待焦点窗口标题匹配 |
| `wait activate --handle <handle> [--expect-active <true\|false>] [--timeout-ms <ms>]` | 监听指定窗口句柄是否成为前台激活窗口（或等待其失去激活） |
| `wait pixel --x <x> --y <y> --hex <RRGGBB> [--timeout-ms <ms>]` | 等待指定像素达到目标颜色 |
| `wait clipboard [--expect-text <value>] [--timeout-ms <ms>] [--match <contains\|exact>]` | 等待剪贴板变化或匹配目标文本 |
| `wait process [--name <text>\|--pid <pid>] [--expect-running <true\|false>] [--timeout-ms <ms>] [--match <contains\|exact>]` | 等待进程进入期望状态 |

平台说明：

- Windows：全部可用。
- Linux：等待器本身可用，但会继承底层能力依赖；例如 `wait activate` 依赖 X11/XWayland 窗口焦点能力，`wait clipboard` 依赖剪贴板后端工具，`wait pixel` 依赖图形会话可读。
- macOS：等待器整体可用，但 `wait activate`、`wait clipboard`、`wait pixel` 等同样受系统权限和图形会话状态影响。

参数说明：
- `--timeout-ms`：最长等待时间（毫秒），超时会返回失败
- `--match`：文本匹配模式，`contains` 或 `exact`
- `--foreground-only`：仅匹配当前前台窗口（仅 wait window）
- `--handle`：目标窗口句柄（用于 wait activate）
- `--expect-active`：`true` 等待激活，`false` 等待失去激活
- `--expect-text`：剪贴板期望文本，不传则等待任意变化
- `--name` / `--pid`：进程名称或进程 ID
- `--expect-running`：期望进程是否存在，`true` 表示等待启动，`false` 表示等待退出



复杂参数组合示例：

```bash
# 标题精确匹配 + 只接受前台窗口
wait window --title "记事本" --match exact --foreground-only --timeout-ms 5000

# 监听窗口激活（句柄来自 window list）
wait activate --handle 0x001A09F2 --expect-active true --timeout-ms 5000

# 颜色等待（十六进制）
wait pixel --x 100 --y 200 --hex FFCC00 --timeout-ms 3000

# 进程退出等待
wait process --name "chrome" --expect-running false --match contains --timeout-ms 10000
```



## 注意事项

功能按照 Windows 设计，以上所有功能在 Windows 下均可用，Linux 和 macOS 已补齐大部分常用能力，但仍有平台依赖和少量限制，使用前需要先确认桌面会话、系统权限和命令行工具是否满足。

Linux：

- 鼠标、键盘、窗口控制依赖 `xdotool`，并要求运行在 X11 或 XWayland 会话里。
- `window maximize`、`window restore`、`window move` 依赖 `wmctrl` 和兼容 EWMH 的窗口管理器。
- 剪贴板文本/文件/图片依赖 `wl-copy` / `wl-paste` 或 `xclip` / `xsel`。
- `screen displays` 依赖 `xrandr`，`screen capture` 依赖 `grim`、`gnome-screenshot`、`scrot` 或 `import` 之一。
- `system network-info` 依赖 `ip` 命令。
- `screen capture --display-id` 和 `screen capture --window-handle` 在 Linux 仍未实现，当前只保证整桌面截图。
- Wayland 原生会话下，部分窗口句柄、键鼠注入、像素读取和窗口控制可能被桌面环境限制；X11/XWayland 兼容性更好。

macOS：

- 窗口控制、键盘输入、剪贴板文件/图片等自动化依赖系统的 Accessibility 和 Automation 授权；如果宿主进程没有权限，命令会失败。
- `window show`、`window minimize`、`window maximize`、`window restore`、`window move`、`window close` 通过 `System Events` 操作窗口；如果同一进程里有多个同名窗口，系统会按首个匹配窗口执行。
- `keyboard ime-switch` 在 macOS 下做了策略映射：`win-space` 对应 `Command+Space`，`alt-shift` 对应 `Option+Space`，`ctrl-shift` 对应 `Control+Space`。是否真正切换输入法，取决于系统当前输入源快捷键绑定。
- `keyboard caps-lock` 目前只支持 `toggle`；`on` / `off` 还不能稳定判断系统真实状态。



任务编排：

- 建议工作流：先观察，再动作，最后等待确认
  - 观察：window.find / window.foreground / screen.pixel-color
  - 动作：window.activate / keyboard.* / mouse.* / app.launch
  - 确认：wait.window / wait.focus / wait.pixel / wait.clipboard / wait.process
- 不要连续盲操作（点击、输入、窗口切换后应立即确认状态）
- 参数约定：
  - 匹配模式：contains|exact
  - handle：非负整数
  - x/y、delta：32 位有符号整数
  - wait 默认超时：timeout_ms=2000
  - wait_process：expect_running=true|false
- 高风险动作（鼠标/键盘/窗口激活/窗口关闭/剪贴板写）前后都应插入观察或等待
- Linux/macOS 的部分能力仍需以目标环境实测为准
- 失败时优先读取：failure.code / failure.message / failure.detail



## MCP 接入

### 启动 MCP stdio 服务

```bash
et mcp-stdio
```



### 导出工具清单（manifest）

```bash
et mcp-stdio --output json
```




### 配置示例

优先在全局安装后执行 `init`，把真实原生 `et` 程序复制出来，再让 MCP 直接调用这个文件：

```bash
npm i -g @whuanle/easytouch
easytouch init
```

这一步会直接从包内复制当前主机对应的原生 `et` 文件。

生成后的默认路径：

- Windows：`<npm root -g>/@whuanle/easytouch/et.exe`
- Linux / macOS：`<npm root -g>/@whuanle/easytouch/et`

同时会刷新全局 `et` 命令。

也可以通过 `--output` 指定输出位置。

推荐配置：

```json
{
  "mcpServers": {
    "easytouch": {
      "command": "et",
      "args": ["mcp-stdio"]
    }
  }
}
```

Windows 请把文件名写成 `et.exe`。Linux / macOS 写 `et`。

默认会把 `et` 生成到全局安装目录下的包目录里，并同步刷新全局 `et` 命令。也可以显式指定输出路径：

```bash
easytouch init --output <你想放置 et 的路径>
```

如果你直接安装的是平台包，初始化命令分别是 `easytouch-windows init`、`easytouch-linux init`、`easytouch-macos init`。

如果需要查看实际路径，可以执行 `npm root -g` 和 `npm prefix -g`。

如果宿主能正确处理 PATH，MCP 直接写 `command: "et"` 即可；否则改成 `npm prefix -g` 或 `npm root -g` 对应的实际路径。

如果 Windows 宿主报 `LOCAL_PROCESS_ERROR`，优先改用 `init.js` 生成的 `et.exe`；如果仍走 npm 命令，再检查这里是不是还写成了 `npx`。

### 语义元素树定位

当需要更稳定地点击控件时，可以先读取前台窗口的元素树，再按元素查找、等待、点击或 invoke：

```bash
et element tree --output json
et element find --name "确定" --control-type Button --output json
et wait element --name "保存" --control-type Button --timeout-ms 5000 --output json
et element click --element-id root/0/3 --output json
et element invoke --element-id root/0/3 --output json
```

`element tree` 返回 `element_id`、`control_type`、`automation_id`、`class_name`、`framework_id`、`center`、`bounds`、`children` 等字段，适合让模型先找元素再执行动作。

`element find` 支持按 `element_id`、`name`、`automation_id`、`class_name`、`control_type`、`framework_id` 查询元素。`wait element` 会轮询这些条件直到元素出现。`element invoke` 会走平台语义动作或中心点击回退。

平台要求：

- Windows：UI Automation + PowerShell。
- Linux：`python3`/`python` + `pyatspi`，点击回退还需要 `xdotool`。
- macOS：`osascript` + System Events，宿主需要 Accessibility / Automation 权限。

