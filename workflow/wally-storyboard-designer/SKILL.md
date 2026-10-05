---
name: wally-storyboard-designer
description: Use only when explicitly requested by name. 设计或修订分镜脚本，提供固定绘图提示词，按场景在 ChatGPT Web 生成故事板或分镜表；经确认后裁切并制作图文成品。
---

# Wally Storyboard Designer

Provide on-demand storyboard-domain functions for the user's supplied story, scene, or shot material.
This skill is the test layer of the Wally pipeline；按用户当前要求设计、生成或修订，用户审查叙事与视觉效果。

Current version: `wally-storyboard-designer@2026-09-14-v3.20-selected-versions`

## 共用规则

- Accept scene-divided scripts, tables, images, partial artifacts, conflicting drafts, existing director scripts or performance designs, or any mixture. 输入和交付形式不固定；只处理当前要求，不为执行工具重写材料。
- 按源稿已有场景组织工作，保留原场景名称、顺序及镜号。按场景提取完整材料；网格与图数只决定该场镜头怎样分页。
- Preserve the latest explicit or approved `作品定义` as source authority. 保留适用的全局风格、灯光、音效、台词、参考绑定和前后衔接；无依据的内容不补写。
- 生成分镜表时，表演设计等同于导演脚本，直接作为镜头依据，无需转换格式或重写。
- Keep the fixed storyboard and shot-table prompt templates verbatim. Do not insert a scene title or make any other runtime substitution. 场景与镜号范围另行说明；固定正文仅按明确的模板修改请求调整。
- Do not offer returned-board review as a product. 用户审查故事与视觉质量；Agent 核对图像、镜号、资产和交付完整性，按用户观察定向修订。
- 原创剧本、静态资产、表演与声音设计、视频提示词分别由对应专业 skill 处理；本 skill 保留并传递已有内容。

## 按任务读取

只读取当前任务对应的入口，后续步骤到达时再读其说明。历史版本、脚本实现和测试无需默认加载。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 分镜脚本或定向修订 | [导演脚本合同](references/director-script-output-contract.md)；生成已有稿件的图片时无需读取或套用该写作格式。 |
| 新建场景布局 SVG | 用户明确发起时读 [场景布局规则](references/scene-layout-svg-rules.md)。 |
| 提示词污染检查 | 用户明确要求时读 [污染检查](references/pollution-check.md)。 |
| 只要固定提示词 | 按产品读 [故事板模板](templates/storyboard-prompt-template.md) 或 [分镜表模板](templates/shot-table-prompt-template.md)，展示其中两个正文块。 |
| 执行网页生成 | [ChatGPT Web 流程](references/chatgpt-web-visual-test-workflow.md)，生成时再读所选模板。 |
| 裁切或制作完整成品 | 确认用户已授权这项后续工作后，读 [裁切与图文成品](references/paginated-review.md)。 |
