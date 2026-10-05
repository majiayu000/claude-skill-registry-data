---
name: od-poster-hero
description: 制作竖版宣传海报或朋友圈分享长图（强视觉冲击、要点列表、品牌与二维码区）。用户提到海报、活动图、分享图时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-poster-hero

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-poster-hero` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- **主视觉先生图**：图片 API 可用时先 `generate_image`（约 1 次）落盘同目录 PNG（如 `hero.png`），再写 `index.html` 用 `<img>` 引用；**禁止**首轮用 CSS/SVG 渐变冒充主视觉。用户明确要官图时走官图阶梯，禁止 AI 冒充官图。
- 竖版比例（约 9:16，如 1080×1920 展示）。
- 主标题醒目，副标题一句话。
- 3–5 条核心要点（图标+短句）。
- 底部品牌或二维码占位。
- 使用用户提供的活动名、时间、地点，不虚构。

## 资源

- 上游：OpenDesign/skills/poster-hero
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
