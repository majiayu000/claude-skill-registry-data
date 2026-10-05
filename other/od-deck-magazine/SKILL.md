---
name: od-deck-magazine
description: 制作杂志风横向翻页汇报或路演稿（多页、每页一屏、可键盘翻页）。用户提到演示稿、汇报幻灯片、路演时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-deck-magazine

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-deck-magazine` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 8–15 页，16:9 横屏，每页内容不超出视口（不页内滚动）。
- 版式偏杂志/墨水印刷感，非默认商务蓝模板。
- 结构建议：封面 → 问题 → 方案 → 亮点 → 数据 → 团队/计划 → 结尾。
- 支持方向键或点击翻页。

## 资源

- 上游：OpenDesign/skills/deck-guizang-editorial
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
