---
name: briefbound-performance-engineering
description: "Use when an explicit performance goal, measurable regression, unresolved hot path, large workload, concurrency/cache/streaming decision, or latency/throughput/CPU/memory/I/O/bundle budget needs profiling and evidence-backed optimization; do not use for routine development, speculative cleanup, competition score iteration, or an already-located N+1/local inefficiency whose batch fix and deterministic count verification are clear to the current owner."
license: MIT
---

# Briefbound 性能工程

## 目标

用最小测量找到真正限制结果的瓶颈，只保留收益超过噪声与复杂度成本的优化。普通开发不经过本 skill。

## Briefbound task contract

- Context Boundary: 已确认的性能目标或强信号、代表性负载、owning surface、现有指标/benchmark/profile、正确性契约和允许写入范围。
- Output Contract: baseline、主要瓶颈、最小优化、同负载对比、取舍、正确性验证和必要的回归保护。
- Allowed Action: 读取相关代码和运行证据，执行有界 benchmark/profile，修改已授权 scope 并运行相关验证；不自动安装全局工具、不压测生产、不扩大产品行为。
- Success Evidence: 相同负载下有可比较的 before/after，收益超过测量噪声或目标已满足，且正确性验证通过。
- Stop Condition: 没有性能强信号、无法建立安全负载、瓶颈不在可改范围、需要高风险架构取舍、收益不足以抵偿复杂度，或目标已经满足。
- Route Out: 当前开发 owner、`briefbound-bug-review`、`briefbound-pr-review`、`briefbound-development-cleanup`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回最具体 owner。用户可见内容默认中文，保留指标、命令、路径、API 和工具名。
- Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。
- 不把性能工程变成固定开发阶段，也不要求用户逐步确认已授权的测量、优化和验证。

## 三档边界

Briefbound Router 使用 `FAST / CHECK / PROFILE`：

- `FAST`：低频、低规模、机械修改，直接开发和验证，不输出性能检查。
- `CHECK`：当前 owner 静默处理已定位的 N+1、循环 I/O、重复全量计算、隐藏高阶复杂度和无界增长；批量修复及查询/调用次数断言仍是确定性验证，不加载本 skill、不建 benchmark，也不因“发现问题”切到 bug owner。只有存在已观察到的故障、正确性回归或待诊断根因时才路由 `briefbound-bug-review`。
- `PROFILE`：明确性能目标/回归，或功能进入高频热路径、大数据量、并发、缓存、批处理、流式 I/O、持久化、包体/启动关键面时，才进入本 skill。

文件多、描述长、可能“以后会扩展”或一般性最佳实践不触发 `PROFILE`。PR/diff 审查仍由 `briefbound-pr-review` 主责，本 skill 只在需要性能测量证据时作为 support。

## 最小测量循环

1. 锁定一个主指标和代表性负载：延迟分位、吞吐、CPU、内存、I/O、查询/请求次数、包体或启动时间。没有目标阈值时，以当前回归或稳定 baseline 为比较点。
2. 优先复用现有 benchmark、trace、日志、query plan 或 profiler；选择能区分方案的最小 probe。确定性调用次数、查询数或复杂度证据足够时，不制造负载测试。
3. 找一个主要限制点，区分算法/重复工作、数据库/网络、分配/序列化、锁/队列、缓存、下游依赖和环境噪声；不做全仓性能扫描。
4. 实施一个最小修改。优先消除无效工作和改进算法/数据访问，再考虑批处理、缓存或并发；微优化最后。缓存、线程池和并行不能凭直觉加入。
5. 在相同负载下复测并运行正确性检查。记录方差或至少重复结果；延迟敏感链路优先看 p95/p99，不只看平均值。
6. 收益达到目标或明显超过噪声且复杂度合理时保留；否则只撤销本轮自己的优化。只有测量稳定、回归代价高时才增加性能 guard，避免把脆弱时间阈值塞进普通单元测试。

目标达到即停止。进一步优化进入 Deferred，不自动扩展范围。

## 低噪声约束

- 不默认生成性能报告、规划文档、TASK_GRAPH、worktree 或子 Agent。
- 不因缺少专用工具阻塞；先用项目已有能力，安装依赖或长时间压测需要明确收益和权限。
- 不用代码审美代替测量，也不把微小 benchmark 改善包装成用户价值。
- 性能变化破坏行为、数据、安全或可维护性时，不接受该优化。

## 输出

```text
性能结果:
- 指标与负载: ...
- Baseline: ...
- 瓶颈与最小修改: ...
- After 与取舍: ...
- 正确性验证/剩余风险: ...
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```

只有维护本 skill 或核对来源许可时读取 `references/sources.md`；执行性能任务不加载它。
