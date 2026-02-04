---
name: robot-update-package
description: 将孩子对话摘要/日志输入后处理为“机器人变更包（JSON）”，供人工审核后应用（不自动应用）。
allowed-tools:
  - mem0-memory
  - workspace
  - shell
---

# 触发条件

当用户说“处理孩子对话日志/生成给机器人用的更新建议/给我育儿建议并输出变更包”等时使用本技能。

# 目标

- 输入：`imports/child/` 下的对话摘要/日志文件（上游 App 尚未稳定，schema 暂定）。
- 输出：`exports/robot-update-packages/*.json`
  - 必须满足：`review.status="pending"`（默认）；
  - **禁止自动应用**到机器人项目或孩子侧 mem0（必须人工审核后再应用）。

# 操作步骤（SOP）

1. **读取输入**
   - 读取一个或多个 `child_chat_bundle`（见 `robot-update-package-spec.md` 暂定 schema）。
   - 若输入格式不符合暂定 schema，先提示用户需要的最小字段（time_range/messages）。

2. **检索历史记忆（可选但推荐）**
   - 调用 `mem0-memory.search_memory(user_id=CHILD_USER_ID, query=...)` 获取相关画像/历史模式。
   - 调用 `mem0-memory.search_memory(user_id=U1_USER_ID, query=...)` 获取育儿原则（`parenting_guideline`）。

3. **生成变更包**
   - 以 `templates/robot-update-package.json` 为基础生成包体：
     - `inputs[]`：记录输入文件路径与 hash（如可得）。
     - `u1_advice[]`：给 U1 的建议（强调情绪价值与陪伴质量）。
     - `proposed_actions[]`：建议动作（mem0 写入建议、prompt patch 建议）。
     - `risks[]` / `open_questions[]`：风险与需要 U1 追问的问题。
   - 所有内容默认不包含逐字原文；只输出摘要化结论。

4. **落盘**
   - 写入 `exports/robot-update-packages/`，文件名建议：`YYYY-MM-DD_<CHILD_USER_ID>_<short_id>.json`。
   - `review.status` 固定为 `pending`。

5. **对用户反馈**
   - 返回生成的文件路径，并提示“需人工审核后再应用”。

# 输出格式

- `package_path`: `<path>`
- `summary`: 简要说明包含哪些建议（不泄露敏感原文）

