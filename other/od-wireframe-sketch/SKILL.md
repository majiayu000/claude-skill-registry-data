---
name: od-wireframe-sketch
description: 制作灰块线框示意页，用于先确认页面结构与模块位置，再细化视觉。用户提到线框、草图、先搭结构时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-wireframe-sketch

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-wireframe-sketch` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 手绘或灰盒风格，低饱和度，无精美插画。
- 模块用矩形+短标注（如「轮播」「定价」「页脚」）。
- 标注信息架构与优先级，非最终视觉稿。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
