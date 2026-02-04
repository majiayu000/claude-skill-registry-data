---
name: draw-diagram-skill
description: Expert guidance for creating syntactically correct and well-structured Mermaid diagrams following best practices. Use when creating flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, ER diagrams, data lineage visualizations, or any other Mermaid visualization.
allowed-tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash
---
# Mermaid 图生成 SKILL

本技能沉淀了在本仓库使用 Mermaid CLI（`mmdc`）将 `.mmd` 文本转为高分辨率 PNG 的标准流程。

## 适用场景
- 基于 Mermaid 流程/时序等图快速出图，随代码或脚本说明发布。
- 需要可重复、可修改的图源文件，避免手工绘制。

## 前置要求
- 已安装 `@mermaid-js/mermaid-cli` 并可调用 `mmdc`（本仓库曾使用 `nvm` 安装，路径通常在 `~/.nvm/.../bin/mmdc`）。
- 能够启动无沙箱的 Chromium（沙箱环境可能需要额外权限；在本仓库中使用过 `require_escalated` 执行）。

## 输入
- `input.mmd`：Mermaid 源文件，UTF-8 文本。
- 可选：缩放参数 `-s` 控制分辨率，默认示例用 `2.5`。

## 标准步骤
1) 准备源文件（示例）
   ```mermaid
   flowchart TD
     start([示例开始]) --> step1[步骤 1]
     step1 --> done([结束])
   ```
   保存为 `your-diagram.mmd`。

2) 本地生成 PNG
   ```bash
   mmdc -i your-diagram.mmd -o your-diagram.png -s 2.5
   ```
   - `-s` 越大，导出的图片越清晰；按需调整。
   - 如需 SVG，可将输出改为 `.svg`。

3) 版本化管理
   - 将 `.mmd` 与生成的产物（如需要）一并入库，保持可追溯。
   - 更新图时先改 `.mmd`，再重新导出。

## 故障排查
- 报错 “Failed to launch the browser process”：
  - 在受限环境中尝试关闭沙箱：`mmdc ... -p <config>`，其中配置可传 `{"args":["--no-sandbox","--disable-setuid-sandbox"]}`。
  - 若仍失败，需在有权限的环境执行，或使用 Kroki 等无头渲染服务。
- 找不到 `mmdc`：重新安装 `@mermaid-js/mermaid-cli` 或确保 PATH 包含其安装位置。

## 产出检查
- 确认节点/箭头与脚本逻辑一致。
- 放大查看 PNG 保证文字清晰；必要时增加 `-s` 或切换 SVG。
