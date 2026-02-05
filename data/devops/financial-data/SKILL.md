---
name: financial-data
description: |
  金融数据处理技能：交易数据导入、持仓数据管理、风险指标计算。
  Use when: 需要处理交易记录、导入持仓数据、计算风险指标、数据清洗验证。
  Triggers: "交易", "持仓", "导入", "数据", "IBKR", "风险", "净值", "回撤"
category: data-processing
---

# Financial Data (金融数据处理)

> 💰 **核心理念**: 金融数据是投资决策的基础，必须确保数据准确性、完整性和一致性。垃圾进，垃圾出。

## 🔴 第一原则：数据验证优先

```
❌ 错误做法: 直接导入数据，假设数据正确
✅ 正确做法: 导入 → 验证 → 清洗 → 再验证 → 存储

❌ 错误做法: "这是券商数据，应该没问题"
✅ 正确做法: 任何外部数据都要经过完整验证流程
```

## When to Use This Skill

使用此技能当你需要：
- 从 IBKR、Gmail、Google Drive 导入交易数据
- 处理持仓快照数据
- 计算风险指标（VaR、回撤、夏普比率等）
- 数据清洗和格式转换
- 验证数据完整性和一致性
- 处理多币种数据转换

## Not For / Boundaries

此技能不适用于：
- 实时行情数据获取（参考 api-integration skill）
- AI 分析和建议生成（参考 agent 相关代码）
- 数据库 schema 变更（参考 database-migration skill）

---

## Quick Reference

### 🎯 数据处理工作流

```
数据源 → 获取原始数据 → 格式验证 → 数据清洗 → 业务验证 → 存储 → 确认
   ↓                                                    ↓
 IBKR/Gmail/Drive                                    失败 → 记录错误 → 人工处理
```

### 📋 数据导入前必问清单

| 问题 | 目的 |
|------|------|
| 1. 数据源是什么？ | 确定解析格式（XML/CSV/JSON） |
| 2. 数据时间范围？ | 避免重复导入或遗漏 |
| 3. 币种是什么？ | 确定汇率转换需求 |
| 4. 有没有已存在的数据？ | 决定是覆盖还是增量更新 |
| 5. 数据量有多大？ | 评估是否需要分批处理 |

### ✅ 数据质量检查清单

| 检查项 | 说明 | 严重程度 |
|--------|------|----------|
| 必填字段完整 | ticker, date, quantity 等 | 🔴 阻断 |
| 数值范围合理 | 价格 > 0, 数量 ≠ 0 | 🔴 阻断 |
| 日期格式正确 | YYYY-MM-DD | 🔴 阻断 |
| 币种有效 | USD/HKD/CNY | 🟡 警告 |
| 无重复记录 | 同一交易不重复 | 🟡 警告 |
| 数据连续性 | 无缺失日期 | 🟢 提示 |

---

## 数据源集成指南

### 1. IBKR Flex Query 导入

IBKR 是主要数据源，通过 Flex Query API 获取数据。

**配置要求：**
```typescript
// 环境变量
VITE_CORS_PROXY_URL=https://your-proxy.workers.dev

// Flex Query 配置
const IB_TOKEN = "your_token";
const IB_QUERY_ID = "your_query_id";
```

**数据获取流程：**
```
1. 请求生成报表 (SendRequest)
2. 等待报表生成 (轮询 GetStatement)
3. 解析 XML 响应
4. 提取各类数据：
   - EquitySummaryByReportDateInBase → 账户摘要
   - OpenPosition → 持仓数据
   - Trade → 交易记录
   - ChangeInNAV → 净值变化
   - CashReportCurrency → 多币种现金
```

**关键代码位置：**
- `client/src/services/ibkrFlexQuery.ts` - IBKR 数据获取
- `client/src/services/ibkrData.ts` - IBKR 数据处理

### 2. Gmail 导入（交易确认邮件）

从券商确认邮件中提取交易数据。

**支持的邮件格式：**
- IBKR 交易确认
- 富途牛牛交易确认
- 老虎证券交易确认

**解析流程：**
```
1. 通过 Gmail API 获取邮件
2. 解析邮件正文（HTML/纯文本）
3. 使用正则表达式提取交易信息
4. 验证并格式化数据
```

### 3. Google Drive 导入（CSV/Excel）

从 Google Drive 导入历史数据文件。

**支持的文件格式：**
- CSV（推荐）
- Excel (.xlsx)

**CSV 格式要求：**
```csv
date,ticker,action,quantity,price,fee,currency,notes
2025-01-15,AAPL,BUY,100,185.50,1.00,USD,加仓
2025-01-16,AAPL,SELL,50,188.00,1.00,USD,止盈
```

---

## 数据验证规则

### 交易记录验证

```typescript
// 必填字段验证
const requiredFields = ['date', 'ticker', 'action', 'quantity', 'price'];

// 数值范围验证
const validations = {
  price: (v: number) => v > 0,
  quantity: (v: number) => v !== 0,
  fee: (v: number) => v >= 0,
};

// 枚举值验证
const validActions = ['BUY', 'SELL', 'SHORT', 'COVER', 'DEPOSIT', 'WITHDRAW'];
const validCurrencies = ['USD', 'HKD', 'CNY'];
const validMarkets = ['US', 'HK', 'CN'];
```

### 持仓数据验证

```typescript
// 持仓一致性检查
function validatePositions(positions: Position[], transactions: Transaction[]) {
  // 1. 计算交易累计数量
  const calculatedQty = calculateFromTransactions(transactions);
  
  // 2. 与持仓数量对比
  for (const pos of positions) {
    const expected = calculatedQty[pos.ticker] || 0;
    if (pos.quantity !== expected) {
      console.warn(`持仓不一致: ${pos.ticker} 实际=${pos.quantity} 计算=${expected}`);
    }
  }
}
```

### 净值数据验证

```typescript
// 净值连续性检查
function validateNetWorthHistory(records: NetWorthRecord[]) {
  const sorted = records.sort((a, b) => a.date.localeCompare(b.date));
  
  for (let i = 1; i < sorted.length; i++) {
    const prev = sorted[i - 1];
    const curr = sorted[i];
    
    // 检查日期连续性（工作日）
    const daysDiff = getBusinessDaysDiff(prev.date, curr.date);
    if (daysDiff > 1) {
      console.warn(`净值数据缺失: ${prev.date} 到 ${curr.date}`);
    }
    
    // 检查异常波动（单日变化超过 10%）
    const changePercent = (curr.netWorth - prev.netWorth) / prev.netWorth * 100;
    if (Math.abs(changePercent) > 10) {
      console.warn(`异常波动: ${curr.date} 变化 ${changePercent.toFixed(2)}%`);
    }
  }
}
```

---

## 数据清洗最佳实践

### 1. 股票代码标准化

```typescript
// 统一股票代码格式
function normalizeSymbol(symbol: string, market: Market): string {
  switch (market) {
    case 'HK':
      // 港股：补齐到 5 位数字
      return symbol.replace(/^0+/, '').padStart(5, '0');
    case 'CN':
      // A股：保持 6 位数字
      return symbol.padStart(6, '0');
    case 'US':
    default:
      // 美股：大写字母
      return symbol.toUpperCase().replace(/[^A-Z]/g, '');
  }
}
```

### 2. 日期格式标准化

```typescript
// 统一日期格式为 YYYY-MM-DD
function normalizeDate(dateStr: string): string {
  // 处理 IBKR 格式: 20250115
  if (/^\d{8}$/.test(dateStr)) {
    return `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;
  }
  
  // 处理 MM/DD/YYYY 格式
  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(dateStr)) {
    const [m, d, y] = dateStr.split('/');
    return `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
  }
  
  // 已经是标准格式
  return dateStr;
}
```

### 3. 金额和汇率处理

```typescript
// 汇率常量（应从实时数据获取）
const EXCHANGE_RATES = {
  USD_CNY: 7.04,
  HKD_CNY: 0.93,
};

// 转换为 CNY
function toCNY(amount: number, currency: Currency): number {
  switch (currency) {
    case 'USD':
      return amount * EXCHANGE_RATES.USD_CNY;
    case 'HKD':
      return amount * EXCHANGE_RATES.HKD_CNY;
    case 'CNY':
    default:
      return amount;
  }
}
```

### 4. 重复数据处理

```typescript
// 交易记录去重
function deduplicateTransactions(transactions: Transaction[]): Transaction[] {
  const seen = new Set<string>();
  
  return transactions.filter(tx => {
    // 生成唯一键：日期 + 股票 + 动作 + 数量 + 价格
    const key = `${tx.date}_${tx.ticker}_${tx.action}_${tx.quantity}_${tx.price}`;
    
    if (seen.has(key)) {
      console.warn(`发现重复交易: ${key}`);
      return false;
    }
    
    seen.add(key);
    return true;
  });
}
```

---

## 风险指标计算

### 核心风险指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 最大回撤 | (峰值 - 谷值) / 峰值 | 历史最大亏损幅度 |
| 夏普比率 | (收益率 - 无风险利率) / 波动率 | 风险调整后收益 |
| VaR (95%) | 历史分位数法 | 95% 置信度下的最大损失 |
| 胜率 | 盈利交易数 / 总交易数 | 交易成功率 |
| 盈亏比 | 平均盈利 / 平均亏损 | 风险回报比 |

### 计算示例

```typescript
// 计算最大回撤
function calculateMaxDrawdown(netWorthHistory: number[]): {
  maxDrawdown: number;
  maxDrawdownPercent: number;
  peakDate: string;
  troughDate: string;
} {
  let peak = netWorthHistory[0];
  let maxDrawdown = 0;
  let maxDrawdownPercent = 0;
  
  for (const value of netWorthHistory) {
    if (value > peak) {
      peak = value;
    }
    
    const drawdown = peak - value;
    const drawdownPercent = drawdown / peak;
    
    if (drawdownPercent > maxDrawdownPercent) {
      maxDrawdown = drawdown;
      maxDrawdownPercent = drawdownPercent;
    }
  }
  
  return { maxDrawdown, maxDrawdownPercent, peakDate: '', troughDate: '' };
}

// 计算夏普比率
function calculateSharpeRatio(
  returns: number[],
  riskFreeRate: number = 0.02
): number {
  const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
  const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
  const stdDev = Math.sqrt(variance);
  
  // 年化
  const annualizedReturn = avgReturn * 252;
  const annualizedStdDev = stdDev * Math.sqrt(252);
  
  return (annualizedReturn - riskFreeRate) / annualizedStdDev;
}
```

---

## 数据库表结构

详细的数据库 schema 定义请参考：
- `references/data-schemas.md` - 完整的数据结构定义

### 核心表概览

| 表名 | 用途 | 主键 |
|------|------|------|
| `transactions` | 交易记录 | uuid |
| `stock_positions` | 股票持仓快照 | bigserial |
| `option_positions` | 期权持仓快照 | bigserial |
| `dashboard_snapshots` | 每日驾驶舱快照 | bigserial |
| `risk_metrics` | 风险指标 | bigserial |
| `watchlist` | 观察列表 | uuid |

---

## Examples

### Example 1: 从 IBKR 导入数据

**Input:** "需要从 IBKR 导入最新的交易和持仓数据"

**Steps:**
1. 调用 `fetchIBKRFlexQuery()` 获取数据
2. 验证返回的数据完整性
3. 调用 `syncIBKRToSupabase()` 同步到数据库
4. 验证同步结果

**Expected Output:**
```typescript
import { syncIBKRToSupabase } from '@/services/ibkrFlexQuery';

const result = await syncIBKRToSupabase(true, (stage, progress) => {
  console.log(`[${progress}%] ${stage}`);
});

if (result.success) {
  console.log('同步成功:', result.data);
} else {
  console.error('同步失败:', result.message);
}
```

### Example 2: 验证持仓数据一致性

**Input:** "检查持仓数据是否与交易记录一致"

**Steps:**
1. 获取所有交易记录
2. 计算每个股票的累计持仓
3. 与当前持仓对比
4. 输出差异报告

**Expected Output:**
```typescript
// 获取数据
const transactions = await getTransactions();
const positions = await getPositions();

// 计算预期持仓
const expectedPositions = calculatePositionsFromTransactions(transactions);

// 对比
for (const pos of positions) {
  const expected = expectedPositions[pos.ticker] || 0;
  if (pos.quantity !== expected) {
    console.warn(`❌ ${pos.ticker}: 实际=${pos.quantity}, 预期=${expected}`);
  } else {
    console.log(`✅ ${pos.ticker}: ${pos.quantity}`);
  }
}
```

### Example 3: 计算风险指标

**Input:** "计算最近 30 天的风险指标"

**Steps:**
1. 获取净值历史数据
2. 计算日收益率
3. 计算各项风险指标
4. 存储到 risk_metrics 表

**Expected Output:**
```typescript
// 获取净值数据
const netWorthHistory = await getNetWorthHistory(30);

// 计算日收益率
const returns = calculateDailyReturns(netWorthHistory);

// 计算风险指标
const metrics = {
  maxDrawdown: calculateMaxDrawdown(netWorthHistory),
  sharpeRatio: calculateSharpeRatio(returns),
  var95: calculateVaR(returns, 0.95),
  volatility: calculateVolatility(returns),
};

// 存储
await saveRiskMetrics(metrics);
```

---

## 常见问题处理

### Q1: IBKR 数据获取失败

**可能原因：**
1. Token 过期
2. CORS 代理不可用
3. 网络问题

**解决方案：**
```typescript
// 1. 检查 Token 有效性
// 登录 IBKR 账户管理 → 报表 → Flex Queries → 检查 Token

// 2. 尝试备用代理
const FALLBACK_PROXIES = [
  'https://corsproxy.io/?',
  'https://api.allorigins.win/raw?url=',
];

// 3. 增加重试次数和超时时间
```

### Q2: 数据重复导入

**解决方案：**
```typescript
// 使用 upsert 而非 insert
const { error } = await supabase
  .from('transactions')
  .upsert(transactions, {
    onConflict: 'date,ticker,action,quantity,price',
    ignoreDuplicates: true
  });
```

### Q3: 汇率数据不准确

**解决方案：**
```typescript
// 1. 使用实时汇率 API
const rates = await fetchExchangeRates();

// 2. 或使用 IBKR 提供的汇率
const fxRate = trade.fxRateToBase;
```

---

## References

- `references/data-schemas.md`: 完整的数据结构定义
- `references/validation-rules.md`: 数据验证规则详解
- `references/import-templates.md`: 数据导入模板

---

## Maintenance

- **Sources**: 项目实际代码, IBKR API 文档, 金融数据处理最佳实践
- **Last Updated**: 2025-01-01
- **Known Limits**: 
  - IBKR Flex Query 有请求频率限制
  - 历史数据导入需要手动触发
  - 汇率数据可能有延迟
