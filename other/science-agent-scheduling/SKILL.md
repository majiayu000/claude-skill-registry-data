---
name: science-agent-scheduling
description: Use when a campaign is running and work must be dispatched, retried or throttled — when a shard sits in running with no heartbeat, when a lease expired and the result was duplicated, when retries storm the source APIs, when budget or concurrency must be cut mid-campaign, or when someone wants to fix a stuck task by editing state directly.
---

# 任务调度：租约、幂等与背压

## 一条总原则

**调度器是唯一能改状态的人。** 模型、脚本、人都不直接写 task 状态；
所有状态变化只由 `science_campaign_run` 的动作（claim / heartbeat / complete / fail /
release）产生。手工改 state 会让事件流与状态表对不上，之后每一次重跑都不可信。

## 租约（lease）

- 领取任务即获得租约，`leaseMs` 默认 120000（2 分钟）。
- 租约不是所有权，是**临时独占**；到期未续，任务自动回到 pending，任何人可再领。
- 领取前必须写 `owner`、`leaseUntil`、`attempt`。三项缺一，这次领取无效。
- 续租用 `heartbeat`，间隔取 `leaseMs/3`（约 40 秒）。不要等到快到期才续。
- **不要在长任务里省心跳**。一次 LLM 调用超过 2 分钟就该拆片，而不是把租约调长。

## 心跳

心跳要带三样：`taskId`、`attempt`、`progress`（已完成/总数）。
只发空心跳会被判为僵尸——有租约没进展，与没心跳等价。

| 现象 | 判断 | 动作 |
| --- | --- | --- |
| 有心跳、progress 在涨 | 正常 | 继续 |
| 有心跳、progress 不动超过 2 个周期 | 卡住 | 记录事件，下一轮换策略 |
| 无心跳、租约未到期 | 可能正在长调用 | 等到期，不要抢 |
| 无心跳、租约已到期 | 僵尸 | 允许重新领取，attempt+1 |

## 幂等键

- 每个 shard 的 `idempotencyKey` 必须只由输入决定：`taskId + 输入指纹`。
- 写入产物前先按键查一次：已存在且校验通过 → 直接返回旧结果，不重算。
- 重试沿用同一个 key。**重试换 key 是最常见的重复产物来源。**
- 部分失败（50 条里成了 30 条）按子键续跑，不要整片重来；子键同样是输入指纹。

## 退避

失败后按 attempt 指数退避，并在抖动区间内随机：

```
delay = min(base * 2^(attempt-1), cap) * (0.5 + random()*0.5)
base = 2s, cap = 120s
```

- `429` / 限流 / 超时 → 退避，属于可重试。
- `401` / `403` / 参数非法 / 数据不存在 → 不退避，直接 fail 并写原因。
- `defaultMaxAttempts` 3。第三次失败后转 blocked，附最后一次错误摘要与事件 id。
- 同一源连续 3 次 429，触发该源的熔断，改用备用源，不要继续打。

## 背压

- 全局并发受 `llmConcurrency`（默认 6）约束；单片内并发不要再叠。
- 队列积压超过在跑数的 5 倍，说明分片过细或下游太慢：先停派单，再合并分片。
- 上游产出速率低于下游消费速率时，**降并发而不是加机器**；加机器只会更快把队列打空。
- 某一类分片长期 pending 而其他类型空闲，是路由问题，不是容量问题。

## 预算熔断

- 进 Campaign 前设总预算与单价上限；每次调用后累计，不靠事后对账。
- 达到 80% 预算：只允许收尾类任务（合并、校验、出报告），停止新分片。
- 达到 100%：熔断，所有未领取任务置 paused，已领取的允许跑完并落库。
- 熔断不是失败。报告里写清"跑到哪、花了多少、还差什么"，不要假装完成。

## 失败时先看事件流

排查顺序固定，不要跳步：

1. `science_campaign_status` 看统计：pending / running / done / failed / blocked 各多少。
2. 取一个失败样本，读它的事件流：`claimed → heartbeat* → failed(reason)`。
3. 看 `attempt` 与 `leaseUntil`：是没领到、领了没续、还是续了没产出。
4. 看错误分类：可重试 / 不可重试 / 输入非法 / 上游缺依赖。
5. 只有以上都排除了，才怀疑调度器本身。

**不要**用"再跑一次看看"代替排查——重跑会污染 attempt 计数与事件流。

## 禁止清单

| 禁止 | 原因 |
| --- | --- |
| 手工 UPDATE 任务状态 | 状态与事件流脱钩，无法复盘 |
| 重试时更换 idempotencyKey | 产生重复产物 |
| 把 leaseMs 调到几十分钟 | 掩盖"任务太大"的真实问题 |
| 失败后立刻全量重跑 | 打爆源配额，且丢掉已成功分片 |
| 用加并发解决积压 | 加重下游与限流 |
| 在报告里把 blocked 写成 done | 后续 gate 全部失真 |

## 收尾检查

- [ ] 所有 done 的分片都有产物指纹
- [ ] 所有 failed / blocked 都有原因与事件 id
- [ ] attempt 分布正常（没有大量 3 次打满）
- [ ] 预算消耗与分片数对得上
- [ ] 未有手工改 state 的痕迹
