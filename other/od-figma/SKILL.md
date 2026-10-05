---
name: od-figma
description: 通过已配置的 Figma MCP 工具读取文件结构、提取设计信息并执行自动化操作。
---

# Figma 自动化（MCP）

当用户提到「Figma」「设计稿」「节点」「批量修改组件」等需求时，优先检查是否存在 `mcp__figma__*` 工具并调用。

## 使用建议
- 先列出可用 Figma 工具，再执行读取或写入动作。
- 先读后改，避免盲改。
- 输出时说明改动范围、受影响页面与节点。

## 配置提醒
- 需要在 `~/.pilotdeck/mcp.json` 或项目 `.pilotdeck/mcp.json` 中配置 Figma MCP（命令、参数、TOKEN）。
- 未配置时，提示用户先补齐 MCP 配置。
