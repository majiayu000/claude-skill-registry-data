---
name: od-data-report
description: 制作数据汇报或分析摘要页面（结论先行、图表、建议行动）。用户提到数据报告、分析摘要、季度复盘时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-data-report

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-data-report` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 顶部 3–5 条核心结论或 KPI。
- 至少 2 个图表/表格区（示例数据须标注）。
- 结尾「建议下一步」3 条以内。
- 层级适合管理层快速浏览。

## 资源

- 上游：OpenDesign/skills/data-report
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
