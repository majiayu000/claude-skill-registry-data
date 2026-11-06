---
name: science-campaign-design
description: Use when a research goal is too large for one agent turn and must be split into schedulable work — when planning a campaign across S0–S11, when deciding how fine a shard should be (literature, statistics, figures, writing), when setting gates and vote counts so parallel results can be trusted, or when a batch plan produced duplicates, idle workers or unusable outputs.
---

# Campaign 设计：从研究问题到可分片的任务

## 四层拆解

```
Campaign（一个课题的一次冲顶）
  └─ Workstream（S0–S11 中的一段，有独立 gate）
       └─ Task（一个可验收的交付，有 owner 与 gate）
            └─ Shard（一次模型调用能做完的最小单元）
```

- **Campaign** 与课题一一对应，有唯一 `campaignId`；跨课题不复用。
- **Workstream** 必须有 `stage`（S0…S11）与 `gate`；没有 gate 的 Workstream 不允许存在。
- **Task** 是派单单位，必须有唯一 owner（L2 岗位）与 `acceptance`。
- **Shard** 是执行单位，必须有稳定 `idempotencyKey`，同一 key 重跑不得产生第二份产物。

## 拆到哪一层为止

判断标准只有一条：**这一层能否单独验收**。

- 能验收 → Task。
- 不能验收，但能并行 → 继续拆到 Shard。
- 拆完还说不清"什么叫做完" → 不是粒度问题，是目标没定义，回 S0。

## 分片粒度经验值

| 分片类型 | 一片的量 | 理由 |
| --- | --- | --- |
| 文献 | 50–200 条记录/片 | 低于 50 上下文浪费；高于 200 单次摘要质量下降 |
| 全文精读 | 3–8 篇/片 | 需要逐段引用时按篇切，不要按段落切 |
| 统计 | 1 个检验/片 | 假设检查与效应量必须同片，拆开就对不上 |
| 作图 | 1 张图/片 | 尺寸、字号、误差棒说明是整图属性 |
| 写作 | 1 节/片 | 引言/方法/结果/讨论各自风格不同，混写必串味 |
| 写作-润色 | 800–1500 字/片 | 超过就要拆，否则一致性无法检查 |
| 代码执行 | 1 个命令/片 | 便于定位失败与重跑 |

**不许按"平均分"切**。1000 条文献分 5 片是 200 条/片，分 20 片是 50 条/片，都合法；
分 50 片是 20 条/片，属于过度分片，协调成本超过收益。

## Shard 的最小字段

```json
{
  "shardId": "lit-0031",
  "taskId": "task-lit-map",
  "role": "shard-worker",
  "kind": "literature",
  "input": { "query": "...", "window": "2019-2026", "offset": 150, "limit": 200 },
  "acceptance": { "minRecords": 150, "requireDoi": true },
  "idempotencyKey": "task-lit-map:2019-2026:150:200",
  "maxAttempts": 3,
  "votes": 1
}
```

`idempotencyKey` 由 `taskId + 分片输入指纹` 组成，不含时间戳、不含随机数。
包含时间戳的 key 等于没有幂等。

## Gate 怎么设

一个 Task 的 gate 必须满足三条：

1. **可机器判**：来自工具输出，不是"读起来还行"。例如 `science_stats` 返回了
   效应量与 CI、`science_manuscript_lint` 无 block、`science_paper_audit` 无 blocking。
2. **可失败**：写得出反例。写不出反例的 gate 是装饰。
3. **有归属**：谁判、判不过谁修。判 gate 的人不能是产出该产物的人。

常用 gate：

| 产物 | gate 工具 | 通过条件 |
| --- | --- | --- |
| 统计分析 | `science_stats` | 有假设检查结论、效应量、CI |
| 稿件结构 | `science_manuscript_lint` | 无 block 级问题 |
| 投稿前门禁 | `science_paper_audit` | 无 blocking |
| 复现包 | `science_provenance` | 代码/数据/环境/seed 齐全 |

## votes 怎么定

- **默认 3 票**，`voteThreshold` 0.66：三个独立分片跑同一输入，至少两票一致才采用。
- 只有**结论型**产物需要多票：筛选判定、新颖性判断、审稿意见分级、字段抽取。
- **抽取型/确定性**产物用 1 票：跑统计、出图、格式转换。多票只会烧预算，不会更准。
- 票数超过 5 没有额外收益；分歧应先回查输入定义，而不是加票。
- 票不一致时**报分歧，不报多数**：把三份结果与差异点一起交上去，由 L2 裁决。

## 预算与失败

- `maxShardsPerBatch` 2000、`maxShardsPerCampaign` 50000。超限先合并分片，不要拆更细。
- `defaultMaxAttempts` 3：三次失败后 Task 转 blocked，必须带最后一次的错误摘要与事件 id。
- 一个 Workstream 的失败率超过 30%，停下来查输入定义，不要继续加并发。

## 反模式

| 反模式 | 后果 | 正确做法 |
| --- | --- | --- |
| 按 token 数切分片 | 语义被切断，结果无法合并 | 按记录/检验/图/节切 |
| 所有分片共用 votes=3 | 预算翻三倍，确定性任务毫无收益 | 只对结论型产物投票 |
| gate 写成"质量合格" | 无法判定，实际永远通过 | 绑定具体工具字段与阈值 |
| Task 没有 owner | 卡住时无人认领 | 每个 Task 指定唯一 L2 岗位 |
| Workstream 跨多个 stage | gate 语义混乱 | 一个 Workstream 只对应一个 stage |
| 用时间戳做幂等键 | 重跑必然重复 | 用输入指纹 |

## 交付前自检

- [ ] 每个 Workstream 都有 stage 与 gate
- [ ] 每个 Task 都有唯一 owner 与 acceptance
- [ ] 每个 Shard 都有 idempotencyKey 与 maxAttempts
- [ ] 文献/统计/图/写作四类分片粒度落在经验区间
- [ ] votes 只在结论型产物上大于 1
- [ ] 分片总数未超 `maxShardsPerBatch`，超了先合并
