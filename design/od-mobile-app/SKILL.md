---

name: od-mobile-app

description: 制作手机应用界面示意，可单屏或多屏并排（含手机外框）。用户提到 App 界面、手机页面、移动端产品时使用。先读取 open-design 总控流程，再按本技能清单执行。

---



# od-mobile-app



## 使用方式



1. 若用户已说明 App 名称、屏数、风格（如「世界杯观赛指南、三屏、FIFA 风格」），**跳过问卷**，直接交付。

2. **第一步必做**：调用 `scaffold_mobile_mockup`（不要 read_file `skills/` 路径，租户项目读不到）：

   - `slug`: 如 `world-cup-2026`

   - `preset`: `fifa-world-cup`（世界杯/FIFA）或 `blank`（通用占位）

   - `screens`: 1–3，默认 3

3. 按需 `edit_file` 各 `screen-N.html` 微调文案；**禁止**在对话里贴 ` ```html ` 整页代码。

4. 读清单：`read_skill` skillName=`od-mobile-app` relativePath=`references/checklist.md`（勿 read_file）。

5. 交付：只回复 `artifacts/task-*/<slug>/index.html` 路径 + 一两句说明。



## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。



- 比例接近真实手机（约 390×844），外框在 `index.html` 三列 iframe。

- 每屏一个主任务；多屏横向并排，每屏有 label 标注。

- UI 由产品内「页面预览」展示；勿把 HTML 当代码块贴在回复里。



## 禁止



- ❌ 在助手回复中用 ` ```html ` 贴整页代码

- ❌ 单文件堆全部三屏 CSS（会截断失败）

- ❌ `read_file` 仓库 `skills/` 或 `references/`（用 `read_skill` + `relativePath`）

- ❌ 用户要求已完整时仍 `ask_user_question` 反复问卷



## 资源



- 工具：`scaffold_mobile_mockup`（首选）

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）

- 渲染流程：open-design `references/render-workflow.md`（经 read_skill relativePath 读取）

