---
name: kpi-calculation
description: KPI指标计算技能，包括目标拆解、达成率、增长率、时间进度等核心业务计算
license: MIT
version: 1.0.0
category: business-logic
---

# KPI Calculation Skill

## 能力概述
此技能提供车险经营 KPI 指标的完整计算引擎，包括目标拆解、达成率、增长率、时间进度等核心业务逻辑，支持多种口径和计算模式。

## 核心计算功能

### 1. 年度目标拆解为月度目标

#### 线性时间进度（linear）
将年度目标平均分配到 12 个月：

```typescript
// 公式
月度目标 = 年度目标 / 12

// 示例
年度目标: 120000 万元
月度目标: 120000 / 12 = 10000 万元/月
```

#### 权重时间进度（weighted）
使用 `allocation_rules.json` 中的预设权重分配：

```typescript
// 公式
月度目标[i] = 年度目标 × 权重[i]

// 示例
年度目标: 120000 万元
权重: [0.05, 0.06, 0.08, 0.09, 0.10, 0.11, 0.10, 0.09, 0.08, 0.08, 0.08, 0.08]
1月目标: 120000 × 0.05 = 6000 万元
2月目标: 120000 × 0.06 = 7200 万元
```

#### 2025 实际权重（actual2025）
基于 2025 年实际数据计算贡献度权重：

```typescript
// 公式
权重[i] = 2025年月度实际[i] / 2025年总计

// 示例
2025年总计: 95000 万元
1月实际: 4000 万元 → 权重: 4000/95000 ≈ 0.042
2月实际: 5000 万元 → 权重: 5000/95000 ≈ 0.053
```

### 2. 动态未来目标计算

当已过月份有实际数据时，动态调整剩余月份目标：

```typescript
// 公式
剩余目标 = 年度目标 - YTD实际
未来月份目标[i] = 剩余目标 × 该月权重比例

// 示例
年度目标: 120000 万元
当前月份: 3月
YTD实际: 25000 万元
剩余目标: 120000 - 25000 = 95000 万元
未来月份权重归一化后分配 95000 万元
```

### 3. 达成率计算

#### 月度达成率
```typescript
// 公式
月度达成率 = 月度实际 / 月度目标

// 示例
月度实际: 8500 万元
月度目标: 10000 万元
月度达成率: 8500 / 10000 = 85%

// 边界处理
- 目标为 0 时返回 null
- 实际为 null 时返回 null
```

#### 年累计达成率（YTD）
```typescript
// 公式
YTD达成率 = YTD实际 / YTD目标

// 示例（截至 6 月）
YTD实际: 58000 万元
YTD目标: 60000 万元
YTD达成率: 58000 / 60000 = 96.67%

// YTD 计算
YTD实际 = sum(1月实际, 2月实际, ..., n月实际)
YTD目标 = sum(1月目标, 2月目标, ..., n月目标)
```

### 4. 增长率计算

#### 同比增长率
```typescript
// 公式
同比增长率 = (当前期 - 基期) / 基期

// 示例（当月同比）
当期（2026年3月）: 10500 万元
基期（2025年3月）: 8000 万元
同比增长率: (10500 - 8000) / 8000 = 31.25%

// 边界处理
- 基期为 0 时返回 null
- 基期数据缺失时返回 null
- 当期数据缺失时返回 null
```

#### 增量（绝对差值）
```typescript
// 公式
增量 = 当前期 - 基期

// 示例
增量 = 10500 - 8000 = 2500 万元
```

### 5. 季度聚合计算

#### 月度转季度
```typescript
// 公式
季度值 = sum(该季度3个月度值)

// 示例（Q1 = 1月+2月+3月）
Q1保费 = 8500 + 9200 + 10500 = 28200 万元
Q2保费 = 9800 + 10200 + 10600 = 30600 万元
```

#### 季度达成率
```typescript
// 公式
季度达成率 = 季度实际 / 季度目标

// 季度目标 = sum(该季度3个月度目标)
// 季度实际 = sum(该季度3个月度实际)
```

## 计算模式切换

### 时间进度口径（progressMode）

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `linear` | 线性时间进度，每月平均 | 业务稳定，无季节性波动 |
| `weighted` | 权重时间进度，按预设权重 | 有明显季节性特征 |
| `actual2025` | 2025实际权重，基于历史数据 | 需要延续历史趋势 |

### 示例：切换时间进度口径
```
用户请求：切换到权重时间进度模式

AI 处理流程：
1. 读取 allocation_rules.json 中的权重配置
2. 重新计算 12 个月度目标
3. 使用新权重重新计算达成率
4. 更新图表和 KPI 卡片显示
5. 记录切换操作日志
```

## 四舍五入与回补策略

### 问题场景
```typescript
// 原始计算
年度目标: 100 万元
权重: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
月度目标原始值: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

// 四舍五入后
月度目标四舍五入: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10] ✓

// 问题场景（非平均权重）
权重: [0.0833, 0.0833, ...] (1/12 的精确值)
月度目标原始值: [8.33, 8.33, 8.33, ...]
四舍五入后: [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
总和: 96 万元（误差 4 万元）✗
```

### 解决方案：回补到 12 月
```typescript
function applyRoundingAndBalance(
  monthlyRaw: number[],
  annual: number,
  mode: "none" | "2dp" | "integer"
): number[] {
  if (mode === "none") return monthlyRaw;

  // 逐月四舍五入
  const rounded = monthlyRaw.map(v => round(v, mode));
  const sum = rounded.reduce((a, b) => a + b, 0);
  const diff = round(annual - sum, mode);

  // 回补到 12 月
  const out = [...rounded];
  out[out.length - 1] = round(out[out.length - 1] + diff, mode);

  return out;
}

// 结果
[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 12] ✓ 总和: 100 万元
```

## 边界条件处理

### 1. 除零保护
```typescript
function safeDivide(
  numerator: number | null,
  denominator: number | null
): { value: number | null; reason?: string } {
  if (denominator === null) return { value: null, reason: "no_denominator" };
  if (denominator === 0) return { value: null, reason: "division_by_zero" };
  return { value: numerator === null ? null : numerator / denominator };
}
```

### 2. Null 值处理
```typescript
// 缺失数据不参与计算
const validData = data.filter(v => v !== null);
if (validData.length === 0) return null;
```

### 3. 异常值处理
```typescript
// 增长率超出合理范围（-100% ~ 1000%）
if (rate < -1 || rate > 10) {
  console.warn(`Unusual growth rate detected: ${(rate * 100).toFixed(1)}%`);
}
```

### 4. YTD 累计处理
```typescript
// 超出当前月份的累计值视为 0
const currentMonth = getCurrentMonth(); // 如 3
const ytd = monthlyData.slice(0, currentMonth).reduce((sum, v) => sum + (v ?? 0), 0);
```

## 使用示例

### 示例 1：计算月度达成率
```
用户请求：计算成都分公司车险 2026 年 3 月的达成率

AI 处理流程：
1. 读取成都分公司车险 3 月实际: 10500 万元
2. 计算 3 月目标（根据时间进度口径）:
   - linear: 120000 / 12 = 10000 万元
   - weighted: 120000 × 0.08 = 9600 万元
3. 计算达成率: 10500 / 10000 = 105%
4. 返回结果: 105%
```

### 示例 2：计算同比增长率
```
用户请求：分析成都分公司车险 2026 年 Q1 同比增长情况

AI 处理流程：
1. 计算 2026 年 Q1 实际: 8500 + 9200 + 10500 = 28200 万元
2. 计算 2025 年 Q1 实际: 6500 + 7000 + 7500 = 21000 万元
3. 计算同比增长率: (28200 - 21000) / 21000 = 34.29%
4. 计算增量: 28200 - 21000 = 7200 万元
5. 返回结果: 增长率 34.29%，增量 7200 万元
```

### 示例 3：动态调整未来目标
```
场景：截至 2026 年 3 月，成都分公司车险已完成 28000 万元，年度目标 120000 万元

AI 处理流程：
1. 计算 YTD 实际: 28000 万元
2. 计算剩余目标: 120000 - 28000 = 92000 万元
3. 读取 4-12 月权重，归一化
4. 重新分配 92000 万元到未来月份
5. 更新月度目标数组
```

## 性能优化

### 1. 缓存计算结果
```typescript
// 使用 Map 缓存已计算的结果
const cache = new Map<string, any>();

function getCacheKey(params: CalculationParams): string {
  return JSON.stringify(params);
}

function calculate(params: CalculationParams) {
  const key = getCacheKey(params);
  if (cache.has(key)) return cache.get(key);

  const result = doCalculate(params);
  cache.set(key, result);
  return result;
}
```

### 2. 批量计算
```typescript
// 一次计算多个机构的指标，避免重复计算
function calculateAllKPIs(
  orgs: Organization[],
  year: number
): Map<string, KPIResult> {
  const results = new Map();
  for (const org of orgs) {
    const kpi = calculateKPI(org, year);
    results.set(org.id, kpi);
  }
  return results;
}
```

## 依赖项

### 核心模块
- `src/domain/allocation.ts` (目标拆解)
- `src/domain/achievement.ts` (达成率)
- `src/domain/growth.ts` (增长率)
- `src/domain/time.ts` (时间进度)

### 配置文件
- `/public/data/allocation_rules.json` (权重规则)

## 最佳实践

1. **严格口径**：所有计算必须遵循业务规范文档
2. **空值处理**：缺失数据返回 null，严禁用 0 代替
3. **精度控制**：保费保留 2 位小数，百分比保留 1 位小数
4. **日志记录**：记录边界条件和异常情况
5. **单元测试**：所有计算函数必须有测试用例

## 参考文档
- @doc docs/business/业务指标计算.md
- @doc docs/business/权重分配规则.md
- @code src/domain/allocation.ts
- @code src/domain/achievement.ts
- @code src/domain/growth.ts
- @code src/domain/time.ts
