---
name: github-api-rate-limits
description: >-
  gh / GitHub API：发 API 请求前使用，尤其分页、循环或批量调用（含脚本与
  workflow）；遇到 403/429、RATE_LIMITED 或 Retry-After 时也用。
---

# 遵守 GitHub API 的 rate limits

GitHub 有两个独立的 primary rate limit 预算（bucket）：

- REST（`core` bucket）：按请求数计。
- GraphQL：按 query cost 计——cost 由 query 申请的字段及其数量决定，随 `first:`/`last:` 页长放大；准确值以 query 返回的 `rateLimit.cost` 为准，不要凭 nodes 数估算。

两个 bucket 预算独立、reset 时钟各自独立；REST 的 reset 时刻在 `rate_limit` 响应里是 epoch 秒（`reset`），GraphQL 里是 ISO 8601 字符串（`resetAt`），比较时先统一。Secondary limits（每分钟上限、并发上限）同时横跨两个 API——把负载分摊到两个 primary budget 上仍可能撞 secondary。

## 流程

### 1. 预检（分页、循环、批量请求之前）

```bash
gh api rate_limit --jq '{ core: .resources.core, graphql: .resources.graphql }'
```

读到目标 bucket 的 `remaining` 与 reset 时刻（本次路径用哪个 bucket 就查哪个，另一个 bucket 的余量与本次无关），估算下一批请求的消耗（REST 按请求数、GraphQL 按上一次同型 query 的 `cost`）。余量不足下一批消耗：停下，等该 bucket 的 reset 时刻，或改走另一个 bucket。

### 2. 选 API（预算感知路由）

默认规则：同一数据有 REST endpoint 可得时走 REST；满足以下任一条件才改走 GraphQL——REST 拼齐同样数据需要 3 次以上请求，或需要把多个端点的读取合并进一次往返。选用时写明选了哪条路、为什么。

### 3. 执行并监控

- GraphQL query 内嵌 `rateLimit { limit cost remaining resetAt }`，按查询自监控 cost：

  ```graphql
  gh api graphql -f query='
  query {
    viewer {
      repositories(first: 5) {
        pageInfo { hasNextPage endCursor }
        nodes { nameWithOwner }
      }
    }
    rateLimit { limit cost remaining resetAt }
  }'
  ```

- 只选取本任务需要的字段（最小字段集）。
- 分页用 `pageInfo.endCursor` 游标推进，用小页长，不用巨型 `first:`/`last:`。
- 相关读取合并进一个 GraphQL query，减少 round-trip。

### 4. 限流恢复

- Primary 限流：等刚才超支那个 bucket 的 reset 时刻（另一个 bucket 的 reset 与此无关）。响应带 `Retry-After` header 时，把它作为最短等待秒数。
- Secondary 限流（429 或消息含 "secondary rate limit"）：有 `Retry-After` 就按它等待；没有则从 60s 起步、每次翻倍地退避。
- 恢复后重新预检，确认余量满足下一批消耗才继续；重试最多 3 次，仍被限流就停下，报告 header 与消息原文，等人决定是否等 reset 后续跑。

### 5. 汇报

昂贵操作（批量、循环、大量分页）结束后，报告本次消耗（REST 请求数 / GraphQL cost）与两个 bucket 的 `remaining`、`resetAt`，让人看到预算水位。
