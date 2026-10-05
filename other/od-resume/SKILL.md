---
name: od-resume
description: 制作个人求职简历页面（经历、技能、项目、联系方式）。用户提到简历、求职、个人介绍页时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-resume

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-resume` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 一页或两页屏高内可读完的简历版式。
- 区块：姓名与定位、经历（倒序）、技能、项目 2–3 个、教育、联系。
- 仅使用用户提供的信息；缺失处标注「待补充」而非虚构公司。

## 资源

- 上游：OpenDesign/skills/resume-modern
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
