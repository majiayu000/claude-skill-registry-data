---
name: xiaohongshu-mcp-zh
description: >
  Automate Xiaohongshu (RedNote) content operations using a Python client for the xiaohongshu-mcp server.
  Use for: (1) Publishing image, text, and video content, (2) Searching for notes and trends,
  (3) Analyzing post details and comments, (4) Managing user profiles and content feeds.
  Triggers: xiaohongshu automation, rednote content, publish to xiaohongshu, xiaohongshu search, social media management.
---

# 小红书 MCP 技能（含 Python 客户端）

通过内置的 Python 脚本自动化操作小红书内容运营，与 `xpzouying/xiaohongshu-mcp` 服务器（8.4k+ 星标）进行交互。

**项目地址：** [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)

## 1. 本地服务器部署

本技能需要在本地运行 `xiaohongshu-mcp` 服务器。

### 第一步：下载二进制文件

从 [GitHub Releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) 页面下载适合你系统的二进制文件。

| 平台 | MCP 服务器 | 登录工具 |
| -------- | ---------- | ---------- |
| macOS (Apple Silicon) | `xiaohongshu-mcp-darwin-arm64` | `xiaohongshu-login-darwin-arm64` |
| macOS (Intel) | `xiaohongshu-mcp-darwin-amd64` | `xiaohongshu-login-darwin-amd64` |
| Windows | `xiaohongshu-mcp-windows-amd64.exe` | `xiaohongshu-login-windows-amd64.exe` |
| Linux | `xiaohongshu-mcp-linux-amd64` | `xiaohongshu-login-linux-amd64` |

为下载的文件添加执行权限：
```shell
chmod +x xiaohongshu-mcp-darwin-arm64 xiaohongshu-login-darwin-arm64
```

### 第二步：登录（仅首次需要）

运行登录工具，会打开一个浏览器窗口显示二维码。使用小红书手机 App 扫码登录。

```shell
./xiaohongshu-login-darwin-arm64
```

> **重要提示：** 请勿在其他任何网页浏览器上登录同一个小红书账号，否则会导致服务器的登录会话失效。

### 第三步：启动 MCP 服务器

在单独的终端窗口中运行 MCP 服务器，它将在后台运行。

```shell
# 以无头模式运行（推荐）
./xiaohongshu-mcp-darwin-arm64

# 或者，以可见浏览器模式运行（用于调试）
./xiaohongshu-mcp-darwin-arm64 -headless=false
```

服务器将在 `http://localhost:18060` 上提供服务。

## 2. 使用技能

本技能包含一个 Python 客户端（`scripts/xhs_client.py`）用于与本地服务器交互。你可以直接通过命令行使用。

### 可用命令

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `status` | 检查登录状态 | `python scripts/xhs_client.py status` |
| `search <关键词>` | 搜索笔记 | `python scripts/xhs_client.py search "咖啡"` |
| `detail <id> <token>` | 获取笔记详情 | `python scripts/xhs_client.py detail "note_id" "xsec_token"` |
| `feeds` | 获取推荐信息流 | `python scripts/xhs_client.py feeds` |
| `publish <标题> <内容> <图片>` | 发布笔记 | `python scripts/xhs_client.py publish "标题" "内容" "url1,url2"` |

### 示例工作流：市场调研

1.  **检查状态**：首先确认服务器正在运行且已登录。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp-zh/scripts/xhs_client.py status
    ```

2.  **搜索关键词**：查找与调研主题相关的笔记。输出结果会包含下一步所需的 `feed_id` 和 `xsec_token`。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp-zh/scripts/xhs_client.py search "户外电源"
    ```

3.  **获取笔记详情**：使用搜索结果中的 `feed_id` 和 `xsec_token` 获取指定笔记的完整内容和评论。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp-zh/scripts/xhs_client.py detail "64f1a2b3c4d5e6f7a8b9c0d1" "security_token_here"
    ```

4.  **分析**：查看笔记的内容、评论和互动数据，收集有价值的洞察。
