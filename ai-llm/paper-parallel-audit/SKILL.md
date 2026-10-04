---
name: paper-parallel-audit
description: |
  在执行 ≥ 30 条目的批量核查 / 批量修改任务（引用核查、术语一致性检查、格式统一、文献元数据补齐）时，
  必须采用"派多个 Agent 并行 + 每个 Agent 输出 JSON + 主进程汇总落盘 + 分批断点续跑"的标准模式，
  不得在主会话里串行单线程跑全量。
  Use when 任务规模 ≥ 30，涉及对独立条目的同质操作（每个条目处理逻辑相同、之间无依赖）。
---

# paper-parallel-audit：大批量核查的并行 Agent 模式

## 核心理念

156 篇引用串行核查 ≈ 5 小时 + 中间挂了从头来。
3 个 Agent 并行 + 每个 50 篇 + JSON 落盘 ≈ 1 小时 + 任意一个挂了只重跑那一个。

> 批量任务的瓶颈不是 AI 的速度，是"挂了从头来"的恐惧。
> 并行 + 落盘 = 把恐惧拆成可控的小块。

---

## 触发条件

满足全部 → 触发：

- 任务规模 ≥ 30（条目 / 引用 / 文件 / 段落）
- 各条目之间**无依赖**（核查 A 的结论不影响 B 的核查）
- 操作是**同质的**（每条用的方法 / 标准都一样）
- 已经通过 `paper-pilot-before-batch` 跑过样本，逻辑确认无误

任意一条不满足 → 不并行，老老实实串行 + 落盘（仍然要落盘）。

---

## 标准模式（4 个组件，缺一不可）

### 组件 1：分片

```
total = 156 条
shard_size = 50（按 Agent 数倒推）
shards = [0:50, 50:100, 100:156]
```

### 组件 2：每个 Agent 独立输出 JSON

每个 Agent 处理自己的分片，输出：

```json
{
  "shard_id": "0-50",
  "total": 50,
  "results": [
    {"item_id": 1, "status": "pass", "issue": null},
    {"item_id": 2, "status": "fail", "issue": "作者名拼写错误", "suggestion": "..."}
  ],
  "completed_at": "<ISO 8601 timestamp>"
}
```

### 组件 3：主进程汇总 + 落盘

```bash
# 等所有 Agent 返回后
python merge_shards.py shard-*.json > audit_report.json
```

### 组件 4：断点续跑

- 每个 Agent 跑完立即落盘 JSON 到磁盘
- 任何一个挂了，只重跑那个分片
- 主进程读已有 JSON，跳过已完成

---

## 强制流程

```
检测到 ≥ 30 条目的同质批量任务
        │
        ▼
确认已经跑过 paper-pilot-before-batch
        │
        ▼
分片：N 个 Agent，每个 ≤ 50 条
        │
        ▼
告诉用户：「派 N 个 Agent 并行，每个负责 [区间]，
各自落盘 JSON。预计 [时间]，挂了只重跑挂掉的分片。」
        │
        ▼
用 Task 工具派 Agent（subagent_type 选 general-purpose）
单条消息里多个 Task 调用 = 真正并行
        │
        ▼
等所有 Agent 返回 → 汇总 JSON → 给用户报告
```

---

## 派 Agent 的标准 prompt 模板

```
你是引用核查 Agent，负责本批 [分片区间]。

任务：核查每条引用的 [核查标准列表]。
输入：[引用列表 / 文件路径]
输出：JSON 文件，路径 `shard-<分片 ID>.json`，格式：
  {
    "shard_id": "...",
    "total": N,
    "results": [
      {"item_id": ..., "status": "pass|fail", "issue": "...", "suggestion": "..."}
    ],
    "completed_at": "..."
  }

完成后只返回一句话：「分片 X 完成，pass M 条，fail K 条，已落盘 shard-X.json」。
不要把详细结果写在回复里——一律只在 JSON 里。
```

---

## ❌ 反例（书 §10.2）

用户：「把这 156 条引用核查一遍。」

**错误做法**：在主会话里串行跑——

- 跑到第 80 条 rate limit 了
- claude --continue 接续，但中间结果在内存里没存
- 重跑要么从头来，要么人工记到第几条
- 用户的耐心已经磨没了

**正确做法**：分 3 片 → 派 3 个 Agent → 各自 JSON 落盘 → 主进程汇总 → 用户拿到完整报告。

---

## "不要并行" 的情况

- 条目之间有依赖（B 用 A 的结论）→ 串行 + 落盘
- 任务规模 < 30 → 直接串行更省心
- 操作不同质（每条要不同处理）→ 一个 Agent 全包

---

## Rationalization Table

| 念头 | 现实 |
|---|---|
| "派 Agent 太重，自己串行更直接" | 串行第 80 条挂掉时你会回来读这个表 |
| "我能边跑边把结果记在脑子里" | 你不能。这是惨案 9 的根因 |
| "JSON 太麻烦，纯文本 markdown 就行" | 汇总时要 dedupe / 排序 / filter，markdown 干不了 |
| "派 1 个 Agent 跑 156 条也是并行" | 不是，那只是把串行搬到了子进程里，还是从头来 |
| "落盘的 JSON 占空间" | 一个 shard JSON 几 KB，挂了能省小时级时间 |

---

## Red Flags

- 你正打算 for 循环 156 次 Edit → 停
- 你想"主会话直接核查，写个 todo 记进度" → todo 不是落盘
- 你跑到第 N 条挂了，想凭记忆接着第 N+1 条 → 不行，从最近一次落盘点重启
- 多个 Task 调用分散在多条消息里 → 不是并行，重写成单消息多调用

---

## 配套 skill

- 触发前必须先 `paper-pilot-before-batch`
- 修改性操作还要 `paper-protect-terminology`
- 完成后用 `paper-verify-before-handoff` 自查报告

---

## 来源

《Claude Code 科研手记》§4.2「批量文献核查」、§10.2「引用核查的并行实战」
