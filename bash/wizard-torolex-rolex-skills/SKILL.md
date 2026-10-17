---
name: wizard
description: 生成一个交互式 bash wizard，引导人类一步步完成只有他们能执行的步骤。用于开通基础设施、设置凭据或 CI secrets、在一个不熟悉的第三方 dashboard 中操作，或运行一次性迁移或切换。不要为 agent 自己能执行的步骤调用它。
---

# Wizard

**wizard** 是一个 bash 脚本，一步步引导人类完成一个手工操作流程，这个流程手工做很繁琐，而且每次都要向 AI 重新解释一遍也很繁琐。它打开每个 URL，准确说出要点击和复制什么，捕获值，把它们写到该去的地方（`.env`、GitHub secrets），在每个阶段确认，并显示还剩多少。它可能配置第三方服务、运行一次性迁移，或把项目从一个状态移到另一个状态。

令人愉悦的 UX 已经由 [template.sh](template.sh) 解决了：逐 stage 的进度、确认门、跨平台 URL 打开（包括 WSL）、隐藏的 secret 输入、幂等的 `.env` upsert、`gh secret`/`gh variable` 写入，以及收尾摘要。**你的工作只是界定操作流程并编写它的 stages。** `STAGES` 标记上方的库在每个 wizard 中都是相同的；这种一致性正是重点：永远不要手工编辑它。

wizard 默认是一次性的：为单次运行构建，保存到 scratch 或 `scripts/` 路径，工作完成后删除。只有当用户想要一个应该存在于仓库中的可重复 setup 路径时才提交它。

## 流程

### 1. 界定操作流程

弄清人类必须采取的每个手工步骤，以及沿途捕获的每个值。先读仓库，不要凭空问：

- 对于 setup：`.env`、`.env.example`、`.env.*`、`README`、`docker-compose*`、框架配置，以及 `.github/workflows/*`（每个 `secrets.*` / `vars.*` 引用都是一个 wizard 必须产出的值）。
- 对于迁移或转换：当前状态、目标状态，以及它们之间不可逆的动作。

然后向用户展示有序的 stage 列表以及每个产生的值，并确认：他们可能添加、删除或重新排序。

**完成条件：** 每个 stage 都已按顺序命名，并且对于每个捕获的值，你知道（a）人类从哪里得到它，（b）它被写到哪里（`.env`、GitHub secret、两者，或哪里都不写；有些 stage 是纯动作），以及（c）它是否是 secret（隐藏输入）还是公开的。

### 2. 映射每个 stage 的旅程

对于每个 stage，写下人类遵循的精确路径：打开哪个 URL、在那里做什么、值在哪里显示、它填充哪个变量：例如 "Dashboard → Developers → API keys → Reveal test key → copy"。在你实际上不知道当前 UI 或确切命令的地方，说出来并询问用户或查阅文档：永远不要编造可能不存在的步骤。

**完成条件：** 每个 stage 都追溯到陌生人能跟随的具体指令。

### 3. 编写 wizard

把 `template.sh` 复制到目标路径。用每个步骤一个 `stage` 替换示例 stage，按依赖顺序排列。使用库中的 helper：`stage`、`say`/`step`、`open_url`、`ask`/`ask_secret`、`write_env`、`set_secret`/`set_var`、`pause`/`confirm`。把 `TOTAL_STAGES` 设为你写的 stage 数量。

保持模板设定的标准：在询问值之前先打开 URL，任何 secret 都用 `ask_secret`，每个持久化的值都 `write_env`，只 `set_secret` CI 真正需要的值，任何不可逆动作前都 `confirm`。每个 `stage` 清屏，所以只有当前步骤可见：让一个 stage 保持一个聚焦任务，这样人类需要的东西不会滚出屏幕。不要碰标记上方的库。

### 4. 验证并交接

- `bash -n <script>`；如果有 `shellcheck` 就运行它。
- `chmod +x <script>`。
- 不要自己端到端运行它：它打开浏览器并阻塞在人类输入上。改为静态跟踪：第 1 步的每个值都被捕获并落在第 1 步所说的位置，并且每个 `set_secret` 名称都精确匹配 CI 中的一个 `secrets.*` 引用。
- 告诉用户如何运行它。如果这是一个可重复的 setup 路径，提交它并从 README 链接，这样下一个人运行脚本而不是询问 AI。
