---
name: od-team-okrs
description: 制作团队 OKR / 目标跟踪页（季度横幅、目标、关键结果进度条、负责人与状态）。用户提到 OKR、关键结果时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-team-okrs

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-team-okrs` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 季度横幅 + 至少 3 个 Objective，每个含 Key Results 进度条。
- 负责人头像占位、状态胶囊（进行中 / 风险 / 完成）。
- 侧栏或底部「本季度一览」摘要。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
