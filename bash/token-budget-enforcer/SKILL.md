---
name: token-budget-enforcer
version: 2.1.0
description: |
  Token预算强制执行器 - 5标准完整实现：
  1. 全局考虑：覆盖人/事/物/环境/外部集成/边界情况
  2. 系统考虑：预算→消耗→预警→熔断→报告完整闭环
  3. 迭代机制：PDCA循环，版本历史，反馈收集
  4. Skill化：标准SKILL.md格式，可安装可调用
  5. 自动化：实时监控+cron报告+自动熔断
  6. 认知谦逊：预算预估置信度/局限标注(S6增强)
  7. 对抗验证：预算耗尽等失效场景测试(S7增强)
author: Satisficing Institute
tags:
  - token
  - budget
  - enforcement
  - monitoring
  - circuit-breaker
requires:
  - model: "kimi-coding/k2p5"
  - local_tools: ["python3", "pyyaml"]
---

# Token预算强制执行器 Skill V2.1.0

## 快速开始

```bash
# 查看预算看板
python3 scripts/enforcer_runner.py budget

# 预估任务消耗
python3 scripts/enforcer_runner.py estimate "撰写技术报告"

# 生成日报
python3 scripts/enforcer_runner.py report daily

# 运行对抗测试
python3 scripts/enforcer_runner.py test
```

---

## S1: 输入规范 (Input Standards)

### 1.1 Token预算输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 总日预算 | int | config/budgets.yaml | 默认50,000 tokens |
| 预算池分配 | dict | config/budgets.yaml | 战略30%/运营50%/创新20% |
| 任务类型 | string | 自动识别 | 基于关键词分类 |
| 上下文长度 | int | 运行时传入 | 影响预估 |

### 1.2 任务队列输入

```yaml
task_input:
  task_id: "T-001"           # 任务唯一标识
  description: "任务描述"     # 自然语言描述
  task_type: "auto"          # 自动识别或指定
  priority: "p1"             # p0/p1/p2/p3
  pool: "operational_budget" # 指定预算池
  estimated_tokens: null     # 如已知可指定
```

### 1.3 消耗预测输入

| 预测类型 | 置信度 | 方法 |
|----------|--------|------|
| 标准任务 | ±15% | 历史平均+关键词匹配 |
| 新类型任务 | ±30% | 参考相似任务 |
| 复杂任务 | ±50% | 最坏情况预估 |
| 实验性任务 | 范围估计 | 最小-最大区间 |

---

## S2: 预算执行 (Execution)

### 2.1 执行闭环流程

```
任务请求 → 预算检查 → 消耗预估 → 预扣预算 → 任务执行 → 实际扣减 → 效率评估
    ↑                                                              ↓
    └──────────── 策略优化 ← 趋势分析 ← 报告生成 ← 监控告警 ←──────┘
```

### 2.2 监控→预警→熔断→调整→报告

| 阶段 | 组件 | 触发条件 | 动作 |
|------|------|----------|------|
| 监控 | monitor.py | 每5秒/每次API调用 | 实时跟踪消耗 |
| 预警 | monitor.py | 使用率>70% | 控制台通知 |
| 熔断 | circuit_breaker.py | 消耗>200%预估 | 阻断任务 |
| 调整 | allocator.py | 日终/手动 | 预算再分配 |
| 报告 | reporter.py | 每日18:37 | 生成效率报告 |

### 2.3 熔断机制详细规则

```yaml
circuit_breaker:
  soft_limit: 150%        # 预警但不阻断
  hard_limit: 200%        # 触发熔断
  emergency_limit: 300%   # P0任务上限
  cooldown: 300s          # 熔断冷却时间
  
  actions:
    soft_breach:
      - 控制台警告
      - 记录审计日志
    hard_breach:
      - 阻断任务
      - 通知相关人员
      - 进入冷却期
    p0_override:
      - 允许通过(需<300%)
      - 强制审计标记
```

---

## S3: 输出规范 (Output Standards)

### 3.1 预算报告输出

**日报格式示例：**
```
============================================================
[Token效率日报 - 2026-03-21]
============================================================

📊 概览:
  总预算: 50,000 tokens
  已使用: 15,000 tokens (30.0%)
  剩余: 35,000 tokens
  任务数: 15
  效率评分: 82%

💰 预算池状态:
  🟢 strategic_reserve:
     已用: 0 / 15,000
     使用率: 0.0%
  🟡 operational_budget:
     已用: 12,000 / 25,000
     使用率: 48.0%
  🟢 innovation_fund:
     已用: 3,000 / 10,000
     使用率: 30.0%

⚠️ 告警:
  🟡 预算使用超过70%，请注意

💡 建议:
  ✅ 预算使用正常，继续保持

✅ 准确性验证:
  ✓ pool_allocation_sum: 预算池分配正确
  ✓ consumption_consistency: 消耗统计一致
  ✓ data_completeness: 数据完整
```

### 3.2 预警通知输出

| 级别 | 触发条件 | 通知方式 | 内容 |
|------|----------|----------|------|
| info | - | 日志 | 常规监控信息 |
| warning | 使用率>70% | 控制台+日志 | 预算注意提醒 |
| critical | 使用率>90% | 控制台+日志+告警 | 预算紧急警告 |
| emergency | 使用率>=100% | 全渠道 | 预算耗尽警报 |

### 3.3 调整建议输出

| 场景 | 建议类型 | 建议内容 |
|------|----------|----------|
| 预算紧急 | 即时行动 | "立即启用极简模式，非P0任务暂停" |
| 预算注意 | 策略调整 | "考虑减少非必要任务，优先高价值产出" |
| 效率偏低 | 优化建议 | "审查任务类型，优化高频Skill" |
| 预估偏差大 | 模型校准 | "重新校准预估模型" |

---

## S4: 实时监控自动触发

### 4.1 监控架构

```
┌─────────────────────────────────────────────────────┐
│                 TokenMonitor                        │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────┐   │
│  │ Budget Check │  │ Task Check  │  │ Efficiency │   │
│  │   (5s)      │  │  (Event)    │  │  (Event)   │   │
│  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘   │
│         └─────────────────┼─────────────────┘        │
│                           ↓                          │
│                    ┌─────────────┐                   │
│                    │ Alert Queue │                   │
│                    └──────┬──────┘                   │
│                           ↓                          │
│              ┌────────────────────────┐              │
│              │  Console / Log / File  │              │
│              └────────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

### 4.2 自动触发机制

| 监控项 | 检查频率 | 自动动作 |
|--------|----------|----------|
| 预算使用率 | 每5秒 | 超阈值触发告警 |
| 单次任务消耗 | 实时 | 超200%触发熔断 |
| 效率指标 | 任务完成时 | 低于阈值生成审计 |
| 预估偏差 | 任务完成时 | 超50%记录校准需求 |

### 4.3 监控API

```python
monitor = TokenMonitor()

# 启动持续监控
monitor.start_monitoring()  # 后台线程

# 单次检查
alert = monitor.check_budget_usage()

# 获取状态
status = monitor.get_status()
# {
#   "running": true,
#   "current_usage_percent": 30.0,
#   "alert_count_last_hour": 0
# }
```

---

## S5: 预算核算准确性验证

### 5.1 验证检查项

| 检查项 | 验证内容 | 通过标准 |
|--------|----------|----------|
| pool_allocation_sum | 各池分配之和=总预算 | 误差<1token |
| consumption_consistency | 各池消耗之和=总消耗 | 误差<1token |
| forecast_accuracy | 预测vs实际偏差 | <50%为可接受 |
| data_completeness | 必填字段存在 | 无缺失字段 |

### 5.2 验证报告示例

```json
{
  "accuracy_validation": {
    "status": "valid",
    "checks": [
      {
        "check": "pool_allocation_sum",
        "status": "pass",
        "message": "预算池分配正确"
      },
      {
        "check": "consumption_consistency",
        "status": "pass",
        "message": "消耗统计一致"
      },
      {
        "check": "forecast_accuracy",
        "status": "pass",
        "message": "预测准确率: 85.0%"
      },
      {
        "check": "data_completeness",
        "status": "pass",
        "message": "数据完整"
      }
    ],
    "errors": []
  }
}
```

### 5.3 自动化验证

验证在每次生成报告时自动执行：
- 日报：每日18:37生成时验证
- 异常时：熔断触发后验证
- 手动：通过脚本调用验证

---

## S6: 局限标注 (Limitations)

### 6.1 预算预估置信度

| 预估类型 | 置信区间 | 说明 |
|----------|----------|------|
| 标准任务 | ±15% | 历史数据充足 |
| 新类型任务 | ±30% | 参考相似任务 |
| 复杂任务 | ±50% | 不确定性高 |
| 实验性任务 | 范围估计 | 最小-最大 |

### 6.2 已知局限性

```yaml
budget_limitations:
  estimation:
    description: "基于历史平均，实际可能有偏差"
    mitigation: "标注置信度，大偏差触发模型校准"
    
  external_factors:
    description: "第三方API计费变化未纳入"
    mitigation: "定期审查API提供商计费策略"
    
  model_changes:
    description: "模型更新可能影响token计算"
    mitigation: "模型切换时重新校准预估模型"
    
  concurrent_tasks:
    description: "并发任务预估存在竞争条件"
    mitigation: "预扣机制防止超支"
    
  sudden_large_tasks:
    description: "无法预测突发大任务"
    mitigation: "战略储备(30%)应对突发"
    severity: "HIGH"
```

### 6.3 失效场景声明

以下场景可能导致预算机制失效：

1. **突发超大任务**：超出战略储备的紧急任务
2. **预估系统性偏差**：连续多天预估准确率<50%
3. **熔断机制绕过**：通过拆分任务规避熔断
4. **数据损坏**：消耗记录文件损坏或丢失

---

## S7: 对抗测试 (Devil's Advocate)

### 7.1 测试场景覆盖

| 场景 | 测试内容 | 预期结果 |
|------|----------|----------|
| 预算耗尽 | 模拟全部预算用完 | 非P0任务被阻断 |
| 预估偏差 | 实际消耗远超预估 | 150%预警，200%熔断 |
| 熔断滥用 | 验证熔断审计记录 | 所有熔断被记录 |
| 并发超支 | 多任务同时申请预算 | 总消耗不超预算 |
| 异常峰值 | 5倍预估消耗 | 触发critical告警 |
| P0覆盖 | P0任务超200% | 允许通过但审计 |
| P0上限 | P0任务超300% | 即使P0也被阻断 |

### 7.2 运行对抗测试

```bash
python3 scripts/enforcer_runner.py test
# 或
python3 tests/adversarial_test.py
```

### 7.3 测试输出示例

```
============================================================
🛡️ Token预算对抗测试开始
============================================================

🧪 测试场景1: 预算耗尽场景
✅ Budget Exhaustion - Block Non-P0: PASS
✅ Budget Exhaustion - P0 Reserve Check: PASS

🧪 测试场景2: 预估偏差场景
✅ Soft Limit Warning: PASS
✅ Hard Limit Circuit Breaker: PASS
✅ P0 Emergency Override: PASS
✅ P0 Limit at 300%: PASS

🧪 测试场景3: 熔断滥用场景
✅ Circuit Breaker State Tracking: PASS
✅ Circuit Breaker Audit Trail: PASS
✅ Circuit Breaker Cooldown: PASS

...

============================================================
📊 测试结果汇总
============================================================
总计: 12
通过: 12 ✅
失败: 0 ❌
通过率: 100.0%

🎉 所有对抗测试通过！系统具备足够的鲁棒性。
```

---

## 目录结构

```
token-budget-enforcer/
├── SKILL.md                    # 本文件 (5标准完整文档)
├── _meta.json                  # 元数据
├── cron.json                   # 定时任务配置
├── config/
│   ├── budgets.yaml            # 预算池配置
│   ├── thresholds.yaml         # 阈值配置
│   └── rules.yaml              # 执行规则
├── scripts/
│   ├── enforcer_runner.py      # 主运行脚本
│   ├── allocator.py            # 预算分配器
│   ├── circuit_breaker.py      # 熔断器
│   ├── estimator.py            # 消耗预估器
│   ├── monitor.py              # 实时监控器
│   └── reporter.py             # 报告生成器
├── data/
│   ├── consumption.json        # 消耗记录
│   ├── forecasts.json          # 预测数据
│   └── reports/                # 报告存档
├── logs/
│   └── budget.log              # 运行日志
└── tests/
    └── adversarial_test.py     # 对抗测试
```

---

## 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `budget` | 查看预算看板 | `python3 scripts/enforcer_runner.py budget` |
| `estimate [task]` | 预估消耗 | `python3 scripts/enforcer_runner.py estimate "写报告"` |
| `report daily` | 生成日报 | `python3 scripts/enforcer_runner.py report daily` |
| `monitor status` | 监控状态 | `python3 scripts/enforcer_runner.py monitor status` |
| `check [pool] [amount]` | 检查可用性 | `python3 scripts/enforcer_runner.py check operational_budget 1000` |
| `test` | 运行对抗测试 | `python3 scripts/enforcer_runner.py test` |

---

## 版本历史

| 版本 | 日期 | 变更 | 标准 |
|------|------|------|------|
| v2.1.0 | 2026-03-21 | 5标准完整实现，添加对抗测试 | S1-S7 |
| v2.0.0 | 2026-03-21 | 5标准全覆盖 | S1-S6 |
| v1.1.0 | 2026-03-19 | 增加熔断机制 | S1-S3 |
| v1.0.0 | 2026-03-20 | 三级预算初始版 | S1-S2 |

---

*版本: v2.1.0*  
*更新日期: 2026-03-21*  
*作者: 满意解研究所*  
*标准级别: 5标准完整实现*
