---
name: od-dashboard
description: 制作带侧边栏的数据看板或管理后台首页，含关键指标卡片与图表区域。用户提到后台、仪表盘、数据面板时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-dashboard

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-dashboard` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。
- 桌面宽屏布局：左侧导航 + 顶栏 + 主内容区。
- 主区含 KPI 数字卡片 3–6 个、至少 1 个图表或表格占位（标明示例数据）。
- 信息层级清晰，适合运营/管理者快速扫读。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
