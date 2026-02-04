---
name: claim-ledger-to-tasks
description: 扫描 topic 的 digests Claim Ledger，把“未核验 + 数字高影响”条目转成 tasks（核验待办）。
allowed-tools:
  - tasks
  - workspace
  - shell
  - python
---

# 触发条件

当某个 topic 下已经批量产出了 digest（含 Claim Ledger），需要把“未核验的关键数字/口径”拆成可追踪的核验待办时使用。

# 目标

- 输入：`topic_id`
- 输出：在 `tasks` 中创建一批“核验”任务（默认 `status=pending`），并带上 `topic_id` 与 `bvid` 等标签，便于看板/筛选。

# SOP

1. **确认 topic**
   - `topic_id`：例如 `bili_up_414609825_touyanxianji`

2. **dry-run 预览（推荐）**
   - `python3 scripts/claim_ledger_to_tasks.py --topic <topic_id> --dry-run --max-total 20 --max-per-digest 2`

3. **正式创建 tasks**
   - `python3 scripts/claim_ledger_to_tasks.py --topic <topic_id> --max-total 80 --max-per-digest 2`
   - 输出 JSON 默认建议落到：`state/tmp/claim_tasks_created_*.json`（便于回溯）

4. **验证创建结果**
   - 可用 `tasks` MCP 或本地脚本查询：topic_id 过滤确认数量与标题是否合理。

# 过滤规则（当前实现）

- 只处理：`核验状态=unverified`
- 只挑选：包含“数字 + 单位/百分比”等紧凑数值事实，并结合关键词打分（每条 digest 取 TopN）
- 目的：降低 ASR 噪声导致的“泛泛而谈”任务污染

