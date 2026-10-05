---
name: od-social-x-card
description: 制作 X（Twitter）金句或数据分享卡（适合配推文截图）。用户提到推特卡、X 分享图时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-social-x-card

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-social-x-card` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 画幅约 16:9（如 1600×900 容器），中央金句 2–3 行。
- 含作者署名 / handle 占位、类型小标签、品牌水印位。
- 暗色或亮色二选一，对比足够；交付 index.html。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
