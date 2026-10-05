---
name: od-finance-report
description: 制作财务 / 经营摘要报告页（指标卡、图表区、说明）。用户提到财务报告页、经营看板摘要时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-finance-report

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-finance-report` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 至少 4 个 KPI 卡片 + 1 个趋势或构成图（可用 SVG/简易 Chart）。
- 数字用示例数据并标注「示例」；勿伪造真实公司财报。
- 附简短解读段落。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
