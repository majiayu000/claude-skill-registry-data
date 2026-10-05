---
name: od-pricing-page
description: 制作产品定价与套餐对比页面（多档价格、功能对比、常见问题）。用户提到定价、套餐、收费时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-pricing-page

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-pricing-page` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 2–4 个套餐卡片，推荐档视觉突出。
- 功能对比表或清单，差异点可读。
- 底部可附 3–5 条与付费相关的常见问题。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
