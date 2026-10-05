---
name: dw-dqc
description: 数仓 SLA/DQC 规则配置流程，适用于生成完整性、准确性、一致性和时效性质量规则 JSON。直接调用命令：/dw-dqc。
---

# Step 8: SLA/DQC

## 执行流程

1. 基于表结构和业务规则生成 9 类 DQC 规则
2. 配置 SLA 产出时间
3. 输出 DQC 配置 JSON

## 9 类 DQC 规则

### 完整性规则 (3 类)
1. **主键非空**: 主键字段不允许 NULL
2. **分区数据量**: 分区行数在合理范围内（波动 ≤ 30%）
3. **必填字段完整**: 核心业务字段不允许 NULL

### 准确性规则 (2 类)
4. **金额字段容差**: 核心金额字段与上游差异 ≤ 0.01%
5. **数值范围检查**: 字段值在业务合理范围内

### 一致性规则 (2 类)
6. **联动逻辑**: 如 is_perform 与 perform_flag 的对应关系
7. **上下游一致性**: 汇总值与明细汇总一致

### 时效性规则 (2 类)
8. **产出时间 SLA**: 数据产出时间 ≤ 次日 8:00
9. **数据新鲜度**: 最大分区日期与当前日期差值 ≤ 1 天

## 推荐提示词

```
为 [表名] 生成 DQC 规则配置：
- 核心金额字段: [字段列表]
- 主键: [字段]
- SLA: 次日 8:00
输出 DQC 配置 JSON。
```

## 输出格式

```json
{
  "table_name": "[表名]",
  "sla": "08:00",
  "rules": [
    {
      "type": "completeness",
      "name": "主键非空",
      "field": "[字段名]",
      "condition": "IS NOT NULL",
      "severity": "critical"
    },
    {
      "type": "accuracy",
      "name": "金额容差",
      "field": "[金额字段]",
      "threshold": "0.01%",
      "compare_with": "[上游表]",
      "severity": "critical"
    },
    {
      "type": "timeliness",
      "name": "产出时间",
      "sla": "08:00",
      "severity": "warning"
    }
  ]
}
```
