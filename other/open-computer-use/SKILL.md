---
name: open-computer-use
description: Install and configure open-computer-use (macOS Computer Use via MCP) for Hermes Agent. Covers npm install, macOS permissions, hermes MCP config, and troubleshooting.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [MCP, Computer Use, macOS, Accessibility]
    related_skills: [native-mcp]
---

# Open Computer Use for Hermes

开源 macOS Computer Use 服务，基于 Accessibility API，通过 MCP 协议暴露给 AI Agent。

## 安装

```bash
npm i -g open-computer-use
```

若命令找不到：
```bash
npm config get prefix   # 检查全局路径
ls {prefix}/bin/open-computer-use
```

## macOS 权限（关键坑）

需授权**两个**权限，对象是 `.app` 包而非 Terminal：

| 权限 | 授权对象 |
|------|---------|
| 辅助功能 | `{npm_prefix}/lib/node_modules/open-computer-use/dist/Open Computer Use.app` |
| 屏幕录制 | 同上 |

**常见错误**：只授权 Terminal → `list-apps` 能用但 `get_app_state` 报 permissionDenied。

原因：`list-apps` 只需 Accessibility，`get_app_state` 需 Screen Recording，必须给 `.app` 本身授权。

### 授权步骤

1. 系统设置 → 隐私与安全性 → 辅助功能 → "+" → 导航到 `.app` 路径
2. 屏幕录制 → 同上
3. 重启终端

### 验证

```bash
open-computer-use doctor
open-computer-use list-apps
open-computer-use snapshot com.apple.finder
```

## 配置 Hermes MCP

参考 `native-mcp` 技能，在 hermes MCP 配置中添加 stdio server：

```yaml
mcp_servers:
  open-computer-use:
    command: "/full/path/to/open-computer-use"
    args: ["mcp"]
    timeout: 120
    connect_timeout: 60
```

路径获取：`npm config get prefix` → 拼接 `/bin/open-computer-use`。

重启 hermes 或执行 `/reload-mcp`。

## 可用 MCP 工具

| 工具 | 功能 |
|------|------|
| `get_app_state` | 截图 + accessibility 树（**必须首先调用**） |
| `click` | 点击元素/坐标 |
| `drag` | 拖拽 |
| `type_text` | 输入文字 |
| `press_key` | 按键/快捷键 |
| `scroll` | 滚动 |
| `set_value` | 设置输入框值 |
| `list_apps` | 列出运行中的应用 |
| `perform_secondary_action` | 执行辅助操作 |

工具名在 hermes 中自动加前缀：`mcp_open_computer_use_{tool}`

## 排错

- **command not found**：用完整路径
- **permissionDenied on get_app_state**：权限给了 Terminal 没给 `.app`
- **doctor 超时**：手动去系统设置授权
- **MCP tools 未出现**：检查配置缩进，重启 hermes
