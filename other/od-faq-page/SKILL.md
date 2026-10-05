---
name: od-faq-page
description: 制作常见问题与帮助中心页面，支持搜索、分类与折叠展开。用户提到 FAQ、帮助中心、客服问答时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-faq-page

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-faq-page` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 页面标题与简短说明。
- 搜索框可过滤问题（前端脚本即可）。
- 3–4 个分类，每类 3–5 条真实问答（基于用户行业撰写，不编造政策细节）。
- 手风琴折叠，键盘可访问。
- 底部「还有问题？」联系或工单入口占位。

## 资源

- 上游：OpenDesign/skills/faq-page
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
