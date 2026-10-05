---
name: stock-analysis-integrator
description: 集成股票分析能力，使用 Yahoo Finance 获取精确行情数据，本地计算技术指标（MA/MACD/RSI/100分评分），使用 Tavily 搜索新闻舆情，使用混元大模型（hunyuan-chat-integrator）生成智能分析报告。当应用需要股票分析功能时使用此 Skill。触发场景：股票分析、行情数据获取、技术指标计算、投资决策支持。输出 Markdown 格式报告，支持 Web App 展示。
_meta_type: sdk
---

# 股票分析 SDK 集成

## 适用场景

- **个股分析**：获取精确行情数据，计算技术指标（MA/MACD/RSI），搜索最新新闻，由混元大模型生成智能决策仪表盘报告
- **技术指标分析**：均线排列判断、乖离率计算、量能分析、MACD 金叉死叉信号、RSI 超买超卖分析、100分制评分系统
- **新闻舆情分析**：搜索并分析股票相关新闻，提取风险警报和利好催化
- **智能分析报告**：将结构化数据送入混元大模型，生成深度分析的 Markdown 决策仪表盘报告

**不适用于：**
- 高频交易或实时逐笔数据
- 基于历史数据集的回测（请使用专用回测工具）
- 投资组合管理或多股批量分析

## 架构说明

```
用户输入股票代码
  → Yahoo Finance (yahoo-finance2)    获取精确 OHLCV 历史数据
  → 本地计算                          MA5/10/20/60, MACD, RSI, 100分评分
  → Tavily (@tavily/core)             搜索最新新闻舆情
  → 混元大模型 (hunyuan-chat)         将结构化数据+7条交易规则 → 生成智能分析报告
  → 输出 Markdown 报告                Web App 展示
```

## 安装配置

### 1. 安装依赖

```bash
npm install yahoo-finance2 @tavily/core tencentcloud-sdk-nodejs-hunyuan @uiw/react-markdown-preview
```

> - `yahoo-finance2`：获取精确历史 K 线和实时行情
> - `@tavily/core`：新闻搜索
> - `tencentcloud-sdk-nodejs-hunyuan`：混元大模型（分析报告生成）
> - `@uiw/react-markdown-preview`：Markdown 渲染组件

### 2. 拷贝 SDK 封装

读取本 Skill 中的 `lib/stock-analysis.ts` 并复制到项目中。

同时需要 `hunyuan-chat-integrator` 的 `lib/hunyuan-chat.ts`，确保两个文件在同一目录下。

### 3. 确保依赖 Skill 已配置

本 Skill 依赖以下 Skill：

- **`web-search-integrator`**：提供 Tavily 搜索能力（Genie 环境零配置）
- **`hunyuan-chat-integrator`**：提供混元大模型能力（Genie 环境零配置）

## 配置说明

### 零配置（默认）

Genie 环境提供默认的零配置支持：
- Tavily 通过 `tavily.auth-proxy.local` 代理
- 混元通过 `hunyuan.tencent_cloud.auth-proxy.local` 代理
- 无需设置任何环境变量

```typescript
import { createStockAnalyzer } from './lib/stock-analysis';
const analyzer = createStockAnalyzer();
```

### 自定义配置（可选）

如需使用自有凭证：

```env
# Tavily API Key（可选）
TAVILY_WEB_SEARCH_API_KEY=tvly-your-api-key-here

# 腾讯云凭证（可选，混元大模型）
TENCENTCLOUD_SECRET_ID=your-secret-id
TENCENTCLOUD_SECRET_KEY=your-secret-key
```

## 快速上手

### 分析单只股票

```typescript
import { createStockAnalyzer } from './lib/stock-analysis';

const analyzer = createStockAnalyzer();

// 分析一只股票（支持 A 股、美股、港股）
const result = await analyzer.analyze('600519'); // 贵州茅台

// result.markdown 是混元大模型生成的智能分析报告
console.log(result.markdown);

// result.technicalAnalysis 是本地计算的精确技术指标
console.log(result.technicalAnalysis.signalScore);    // 评分 0-100
console.log(result.technicalAnalysis.buySignal);       // STRONG_BUY | BUY | HOLD | WAIT | SELL | STRONG_SELL
```

### 在 Web App 中展示

```tsx
import { createStockAnalyzer } from './lib/stock-analysis';
import MarkdownPreview from '@uiw/react-markdown-preview';

// React 组件中
const [report, setReport] = useState<string>('');

const handleAnalyze = async (stockCode: string) => {
  const analyzer = createStockAnalyzer();
  const result = await analyzer.analyze(stockCode);
  setReport(result.markdown);
};

// 渲染
<MarkdownPreview 
  source={report} 
  wrapperElement={{ "data-color-mode": "light" }}
/>
```

## 分析框架

### 数据层（本地精确计算）

| 数据源 | 内容 | 说明 |
|--------|------|------|
| **Yahoo Finance** | OHLCV 历史数据、实时报价、PE/PB | 精确数值，非搜索结果。支持速率限制重试机制 |
| **本地计算** | MA5/10/20/60、MACD(12,26,9)、RSI(6/12/24)、量比、乖离率 | 零延迟、100%精确 |
| **评分系统** | 100分制综合评分 | 基于 6 维度加权计算 |
| **Tavily** | 最新新闻、舆情 | 网络搜索最近一周新闻，自动过滤低质量来源（如 tipranks.com） |

### 评分系统（100分制）

| 维度 | 权重 | 满分条件 |
|------|------|----------|
| **趋势** | 30 分 | 强势多头（MA5>MA10>MA20，发散上行） |
| **乖离率** | 20 分 | MA5 偏离 < 2%（回踩买点区间） |
| **量能** | 15 分 | 缩量回调（洗盘特征） |
| **支撑** | 10 分 | 价格在 MA5/MA10 获得支撑 |
| **MACD** | 15 分 | 零轴上方金叉 |
| **RSI** | 10 分 | 超卖区间（RSI < 30） |

### 信号映射

| 评分区间 | 信号 | 操作建议 |
|----------|------|----------|
| 75-100 + 多头趋势 | 强烈买入 | 积极介入 |
| 60-74 + 多头/弱多头 | 买入 | 正常建仓 |
| 45-59 | 持有 | 维持仓位 |
| 30-44 | 观望 | 等待更好时机 |
| 0-29 或空头趋势 | 卖出 / 强烈卖出 | 退出仓位 |

### 分析层（混元大模型）

评分系统计算完成后，所有结构化数据（行情、技术指标、评分结果、新闻）被送入混元大模型，由 LLM 结合 **7 条核心交易规则** 生成深度分析报告：

1. **严进策略**：乖离率 > 5% → 严禁追高
2. **趋势交易**：仅在 MA5 > MA10 > MA20 时做多
3. **效率优先**：关注筹码集中度
4. **买点偏好**：缩量回踩 MA5/MA10 支撑为理想入场点
5. **风险排查**：减持公告、业绩预亏、监管处罚、解禁压力
6. **估值关注**：PE 明显偏高需在风险点中说明
7. **强势放宽**：强势多头趋势可将乖离率阈值放宽至 7.5%

## 报告结构

混元大模型输出结构清晰的 Markdown 报告（决策仪表盘）：

```markdown
# {股票名称}({代码}) 决策仪表盘
> 📅 日期 | 评分 **X/100** | 看多/震荡/看空 | **信号**

## 📊 核心结论 - 一句话判断 + 空仓/持仓建议表格
## 📈 趋势分析 - 均线系统表格 + 价格位置表格 + 量能特征
## 🔧 技术指标 - MACD表格 + RSI表格  
## 📰 舆情分析 - 情绪判断 + 1-3条相关新闻
## 🎯 操作计划 - 买卖点位表格 + 仓位建议 + 检查清单
## 📋 评分明细 - 综合评分 + 优势/风险
> ⚠️ 风险提示
```

报告特点：
- **表格展示** - 数据清晰对比，使用 `@uiw/react-markdown-preview` 渲染
- **emoji 图标** - 增强可读性和视觉层次
- **分隔线** - 清晰划分各章节
- **引用块** - 突出核心结论和风险提示

## 架构集成

### 服务层模式（推荐）

```typescript
// src/services/stock-analysis.service.ts
import { createStockAnalyzer } from '../lib/stock-analysis';

export class StockAnalysisService {
  private analyzer = createStockAnalyzer();

  async analyzeStock(code: string) {
    return this.analyzer.analyze(code);
  }

  async getAnalysisMarkdown(code: string): Promise<string> {
    const result = await this.analyzer.analyze(code);
    return result.markdown;
  }
}
```

### Express 路由示例

```typescript
// src/routes/stock.routes.ts
import { Router } from 'express';
import { StockAnalysisService } from '../services/stock-analysis.service';

const router = Router();
const service = new StockAnalysisService();

// 获取分析结果（JSON 格式，包含 markdown 和结构化数据）
router.get('/analyze/:code', async (req, res) => {
  const result = await service.analyzeStock(req.params.code);
  res.json(result);
});

// 下载 Markdown
router.get('/analyze/:code/download/md', async (req, res) => {
  const markdown = await service.getAnalysisMarkdown(req.params.code);
  res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
  res.setHeader('Content-Disposition', `attachment; filename="${req.params.code}_analysis.md"`);
  res.send(markdown);
});
```

### React 组件示例

```tsx
// src/components/StockAnalysis.tsx
import React, { useState } from 'react';
import MarkdownPreview from '@uiw/react-markdown-preview';

export function StockAnalysis() {
  const [code, setCode] = useState('');
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    const res = await fetch(`/api/analyze/${code}`);
    const data = await res.json();
    setReport(data.markdown);
    setLoading(false);
  };

  return (
    <div>
      <input value={code} onChange={e => setCode(e.target.value)} placeholder="输入股票代码" />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? '分析中...' : '开始分析'}
      </button>
      {report && (
        <MarkdownPreview 
          source={report} 
          wrapperElement={{ "data-color-mode": "light" }}
        />
      )}
    </div>
  );
}
```

## 支持的市场

| 市场 | 代码格式 | 示例 |
|------|----------|------|
| A 股（沪深） | 6 位数字 | `600519`, `000001`, `300750` |
| 美股 | 字母 Ticker | `AAPL`, `TSLA`, `NVDA` |
| 港股 | 5 位数字 | `00700`, `09988`, `01810` |

## 安全最佳实践

1. **前端不暴露 API Key**：始终从后端发起分析请求
2. **使用环境变量**：将 API Key 存储在 `.env` 文件中
3. **实现速率限制**：防止过度调用 API（Tavily 和混元均有请求限制）
4. **校验股票代码**：在分析前对用户输入进行清洗和验证
5. **添加免责声明**：报告中始终包含投资风险提示

## 常见问题

**行情数据不完整**
- 确认股票代码正确
- Yahoo Finance 对部分新股/次新股数据可能不足20个交易日
- 非交易时段数据为上一交易日收盘数据

**新闻搜索结果为空**
- 确认 Tavily 连通性
- A 股可尝试使用中文名称
- 新上市股票可能暂无新闻

**混元大模型返回为空**
- 检查混元服务连通性
- Genie 环境默认通过 auth-proxy 连接，确认代理正常
- 自有凭证需确认已开通混元 API 权限

## 资源

- **SDK 封装源码**：`lib/stock-analysis.ts`
- **依赖 Skill**：`web-search-integrator`（Tavily 搜索）、`hunyuan-chat-integrator`（混元大模型）
- **分析框架参考**：基于 [daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 项目方法论
