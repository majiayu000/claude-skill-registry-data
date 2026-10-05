---
name: wally-action-designer
description: Use only when explicitly requested by name. 按场景设计或修订 AI 视频的表演、互动、摄影、灯光、声音及参考绑定，也可按要求审查回片。
---

# Wally Action Designer

根据当前材料完成用户指定范围的表演设计。一个场景是一场完整的戏；镜头数量服务于该场设计。

交付沿用 `Style:`、`Reference:`、`Camera:`、`Acting:` 等英文标签和 `Shot` 正文写法，字段按需选用。通过连续文字写清画面与表演的发生过程，具体组织见交付约定。

Version: `wally-action-designer@2026-09-29-v3.28-one-decimal-timestamps`

## 按任务读取

| 当前任务 | 读取入口 |
| --- | --- |
| 新写表演设计 | [交付约定](references/contract.md)；涉及的表演与视听选择见 [设计方法](references/craft.md)。 |
| 修改或检查已有设计 | 先读 [交付约定](references/contract.md)，保留原稿；只有需要重新设计表演与视听时才读设计方法。 |
| 审查生成视频 | 读 [回片审查](references/review.md)；需要改稿时再读交付约定。 |

## 内容边界

- 保留故事、已确认台词及用户明确的执行决定，设计它们如何发生。
- 原创或改写台词属于 `wally-screenplay-writer`；静态资产制作属于 `wally-static-asset-designer`。仅在当前工作确实依赖缺失内容时指出缺口，不自动扩展任务。
- 表演设计可直接作为分镜表生成的导演脚本依据。
