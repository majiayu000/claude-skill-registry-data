---
name: design-html
preamble-tier: 4
version: 1.0.0
description: |
  把批准后的设计稿转成 Pretext-native HTML。支持设计分析、智能 API 路由、
  前端框架检测、live reload、验证截图与 refinement loop。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /design-html

这个 skill 负责把 `/design-shotgun` 的批准结果，变成真正能跑、能 resize、文本会 reflow 的 HTML，而不是死板截图还原。

## 核心流程

1. `Input Detection`：识别用户给的是截图、设计稿、现有页面，还是一组选定 mockup。
2. `Design Analysis`：分析版式、层级、内容密度、视觉重心。
3. `Smart Pretext API Routing`：根据设计类型决定该走哪条生成路径。
4. `Framework Detection`：识别 React / Svelte / Vue 等宿主框架。
5. `Generate Pretext-Native HTML`：生成 HTML，并处理 Pretext wiring patterns。
6. `Live Reload Server`：启动预览服务。
7. `Preview + Refinement Loop`：通过验证截图和迭代修正，让成品逼近目标。
8. `Save & Next Steps`：抽取 design tokens、保存 metadata、给出后续接入建议。

## 关键规则

- 重点是“可生产、可响应、文本真实重排”，不是像素级硬编码。
- 要尽量复用宿主框架结构，不凭空发明额外壳层。
