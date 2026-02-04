---
name: digest-content
description: 对文章/转录/报告文本做结构化摘要，归档到主题档案（可选）并写入 U1 的长期记忆（mem0-memory）。
allowed-tools:
  - mem0-memory
  - video_pipeline
  - tasks
  - glm_router
  - workspace
  - shell
  - python
---

# 触发条件

当用户提供或指向以下内容时使用本技能：

- 一段粘贴文本（文章/观点/讨论）
- 一个本地文件路径（Markdown/纯文本/转录）
- 一个 URL（若无法获取正文，先让用户提供转录/正文或使用 web_search 获取公开内容）

# 目标

1. 生成结构化 digest（Markdown），并保存到：
   - 若提供 `topic_id`：`archives/topics/<topic_id>/digests/`
   - 否则：`exports/digests/`
2. 抽取“长期价值结论候选”，写入 mem0（`user_id=U1_USER_ID`）
3. （可选但推荐）为投研/研究用途生成 Claim Ledger，并对“高影响未核验”项创建 tasks

# 操作步骤（SOP）

1. **确定输入**
   - 若用户给的是路径：读取文件内容。
   - 若是 URL：优先尝试获取公开内容；若不可得，提示用户提供正文/转录。
   - 若是视频：
     - 若已存在转录文本：按“路径”处理转录即可；
     - 若提供的是本地视频路径且已配置 `video_pipeline` MCP：先调用 `video_pipeline.analyze_video` 生成 `evidence_compact.md`，再对该文件做 digest（避免把全量转写/OCR 原样喂给模型）。
     - 若提供的是 B 站 URL（UP 主页或单条视频 URL）：先用 `scripts/bilibili_up_batch.py` 下载到 `imports/content/videos/`，再走 `video_pipeline`。

2. **生成结构化摘要（按模板）**
   - 若已启用 `glm_router` MCP：
     - **优先用 `glm_router.glm_router_write_file` 直接写入目标文件**（低成本、且不把长文作为 tool result 回到 Codex 上下文）。
       - 推荐：先 `allow_paid=false`；若失败/限流/输出不符合约束，再按需重试 `allow_paid=true`（质量优先，其次成本）。
       - 建议设置 `validate.must_have_substrings=["## 核心观点","## Claim Ledger"]` 并给出 `max_chars`，让校验失败时在 MCP 内部自动重试。
     - 仅当你需要“把输出拿回当前上下文做二次推理/改写”时，才用 `glm_router.glm_router_chat` 生成短输出或片段。
   - 使用 `templates/digest.md` 的结构生成：
     - 核心观点（3–7 条）
     - 关键证据/数据点
     - 反驳点/局限性
     - 对主题框架的影响（若关联 topic）
     - 建议写入 mem0 的长期结论候选（可选）
     - Claim Ledger（断言清单，优先给出来源/证据指针）
   - 外部事实需要来源标注（链接/出处）+ 不确定性提示（见 `spec.md` 信息源策略）。

3. **落盘**
   - 生成文件名：`YYYY-MM-DD_<source_slug>.md`
   - 写入目标目录（topic 优先）。
   - 若已用 `glm_router_write_file` 直接写入：此步只需检查文件是否存在、结构是否完整（必要时抽查 1–2 段）。

4. **写入 mem0（U1）**
   - 只写入“长期价值”部分（不要写长文全文）。
   - 调用 `mem0-memory.add_memory(user_id=U1_USER_ID, kind=topic_insight|investing_thesis|personal_principle|reflection, topic=<topic_id或自定>)`。

5. **（可选）创建核验 tasks**
   - 对 Claim Ledger 里 `核验状态=unverified` 且“影响范围高”的条目，创建 `tasks.create_task`：
     - `category=investing|tech`
     - `topic_id=<topic_id>`（如有）
     - `source=digest_content`
     - title 建议以“核验/找官方口径/读原文”为主

6. **对用户反馈**
   - 返回：
     - digest 文件路径
     - 写入 mem0 的条目摘要（kind/topic）
     - （如有）创建的 tasks 列表
   - 若提供了 `topic_id`：提示用户下一步可用 `topic-ingest` skill 更新 `sources.md/timeline.md`

# 输出格式

- `digest_path`: `<path>`
- `mem0_updates`: 列表（`kind`, `topic`, `summary`）
- `tasks_created`: 列表（`id`, `title`）
