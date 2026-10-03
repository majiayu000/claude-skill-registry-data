---
name: performance-investigation
description: Investigate measured latency, throughput, CPU, memory, or query-performance problems and verify an optimization with comparable before-and-after evidence. Use for a concrete slowdown or performance target; not for broad static code review.
---

# 性能问题调查与验证

针对一个具体的性能症状或目标，找出主要耗时或资源消耗来自哪里，并用同口径测量验证改动。用户只要求定位时保持只读；要求优化时只改已证实的瓶颈。

## 工作方式

1. **定义可比较的指标。** 确认操作、负载与数据规模、环境、版本、时间窗口和目标指标；延迟看适用的分位数与吞吐，资源问题看相应 CPU、内存、线程、I/O 或数据库指标。记录原始基线，区分真实测量、用户报告和推测。
2. **定位主导成本。** 用项目已有的监控、trace、profile、线程/堆证据、查询计划或可复现的基准定位热点。检查缓存冷热、连接池、并发、外部依赖和数据分布是否使样本不可比；不凭一段代码“看起来慢”就断定根因。
3. **提出可证伪的假设。** 对每个候选瓶颈写明支持证据、排除办法与预计影响，优先调查对目标指标贡献最大的部分。无法获取剖析数据时可做静态风险分析，但必须标记为未验证。
4. **按需做最小优化。** 用户要求修复时，一次改变一个主要因素，保持结果与错误语义正确；涉及索引或表结构时核对数据库迁移约定。运行相关正确性测试，再在尽可能相同的工作负载和环境中复测，报告测量波动与副作用。

交付基线、证据、瓶颈结论或当前最有力的假设、改动和前后测量、验证范围。没有可比结果时，不声称性能已经提升。生产压测、参数调整、扩容或其他会影响真实流量的动作需要相应授权。

## 边界

- 宽泛的静态性能代码审查：`code-review-deep-zh`。
- 数据库 schema 或数据迁移的实施：`database-migration`。
- 功能错误根因排查：`systematic-debugging`；若问题是测得的慢、卡顿或资源耗尽，使用本 skill。
- 压测脚本和持续集成中的业务流程测试：`integration-e2e-testing` 只负责功能流程，本 skill 负责性能基线与解释。
