---
name: od-gamified-app
description: 制作游戏化产品界面示意（等级、任务、奖励反馈）。用户提到游戏化、积分成长界面时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-gamified-app

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-gamified-app` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 用户等级 / 经验条、任务卡、奖励反馈区至少各一。
- 视觉活泼但克制，避免廉价贴纸堆叠。
- 示例文案贴合用户产品名。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
