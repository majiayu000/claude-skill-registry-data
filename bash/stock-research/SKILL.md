---
name: stock-research
description: "个股深度研究（多 Agent 编排版）— 多角色分析师并行编排（技术/新闻/资金情绪/基本面/市场 5 分析师并行 → 多空辩论 → 研究经理汇总），数据全部走 QuantMind 本地（QuantDB + PG 新闻富集 + Huntly），新闻双通道（自家 FinBERT 量化情绪 + 实时搜索补充）。用户说「深度研究」「个股深度研究」「研究某只股票」「多角度分析」时使用：跑 research_data.py 取数 → 并行分析师 → 辩论 → 汇总报告 → PDF → 落盘深度分析目录。触发词：深度研究、个股研究、研究600519、多角度分析、全面分析某股"
---

> ⚙️ 本技能遵循公共运行环境契约（最高优先级，先于本文其余内容执行）：
> 详见 [_shared/env-contract.md](../_shared/env-contract.md)，执行前先读它。

# stock-research — 个股深度研究（多 Agent 框架版）

把多角色投研编排落地到 QuantMind：**数据 100% 走本地**（QuantDB parquet + PG 新闻富集 + Huntly），**新闻双通道**（自家 FinBERT 情绪量化 + WebSearch 实时补充），输出研报级 MD + PDF，落盘深度分析目录（报告管理页 → A股市场 → {股票名}）。

与 [[stock-deep-research]]（智能体自主版深度投研）**不冲突，互为补充**：
- 本 skill = 5 分析师并行编排的「多 Agent 框架版」，流程更重、结构化更强；
- [[stock-deep-research]] = 轻量自主版（特征快照 → 多空子代理辩论 → 综合研判），任何大模型可跑；
- 两者**数据同源**（QuantDB + PG），本 skill 额外整合了**模型推理分数**（engine_signal_scores）与**新闻类型分布**；
- 结论冲突时以数据为准：每个数字都可在数据包溯源，也可读归档目录下已有报告（`A股市场/{股票名}/`）交叉验证。

## 架构

```
Phase 1（并行 5 分析师，各读同一份数据包的不同切片）：
  技术面 → 趋势/均线/指标/量价
  新闻面 → 自家 FinBERT 情绪（主）+ WebSearch 实时新闻（辅）
  资金情绪 → L2 主力资金流 + 换手/量能
  基本面 → 估值 + 财务三表核心科目
  市场面 → 大盘背景 + 所属行业强弱 + 板块资金流
Phase 2（并行）：多头研究员 vs 空头研究员（基于 facts 辩论，禁编数据）
Phase 3：研究经理汇总 → 结论（评级/目标区间/风险/跟踪信号）
输出 → md → PDF → 落盘
```

## ⚠️ 数据铁律（最高优先级，所有 Agent 必须遵守）

1. **禁止伪造数据**：所有价格/PE/财务/资金流数字必须来自数据包 JSON，严禁编造
2. **数据包是唯一数据源**：先跑 `research_data.py` 拿到 `{symbol}_{date}.json`，各分析师只读该文件对应切片；WebSearch 只允许补充**新闻面**的时效性（不得用于取行情/财务）
3. **过期标注**：数据包 generated_at 距今 >5 个交易日时，报告开头标注 `⚠️ 数据截止 {generated_at}`；财报报告期为上季度时注明
4. **单位口径**：amount 万元、市值元（估值 JSON 已原样给出，报告统一 亿元=÷1e8）、L2 资金流脚本已转亿元、技术指标 pct_change 为 %
5. **数据缺失不跳过**：某段数据为空时在报告「数据可用性」注明，不得用推断值充数
6. **Symbol 格式**：内部统一后缀格式（600036.SH）；输入任意格式（600036/SH600036/招商银行）由脚本归一化

## 执行流程（每次 7 步）

### 第 1 步：跑数据脚本（容器内）

```bash
docker cp <repo>/skills/stock-research/scripts/research_data.py quantmind:/tmp/
docker exec quantmind python3 /tmp/research_data.py --symbol 600036.SH
# 输出: /data/reports/stock_research/600036_SH_YYYYMMDD.json（容器内）
docker cp quantmind:/data/reports/stock_research/600036_SH_YYYYMMDD.json /tmp/
```

数据包含：quote（120 日 K 线/60日高低/20-60日涨幅）、indicators（量纲无关指标：rsi/kdj/macd/乖离率/量能/波动率/return 系列；均线由 K 线计算）、valuation（pe_ttm/pb/ps/市值）、l2_flow（近 10 日主力净流入）、financials（三表最新报告期）、sector（CSRC 一级行业）、market_context（5 指数 + 行业涨幅榜 + 板块资金流 1/5/10 日 + 所属行业）、news（近 60 天 FinBERT 情绪事件 + 来源/标签统计 + **类型分布**）、model_score（最新推理 run 的融合/轻量/TFT 分数 + 信号方向 + 预期价 + 全市场分位）。

### 第 2 步：创建报告目录

```bash
mkdir -p /tmp/stock-research/{symbol}/reports
```

### 第 3 步：Phase 1 并行启动 5 个分析师（Agent tool，各自独立）

每个 Agent 的 prompt = `prompts/{role}.md` 内容 + 数据包路径 + 输出路径。**并行**（同一消息多个 Agent 调用）。输出各自 `reports/{role}.md`。

- `technical.md` — 技术面
- `news.md` — 新闻面（双通道：自家情绪统计为主 + WebSearch 实时为辅）
- `sentiment.md` — 资金情绪（L2 主力资金流）
- `fundamentals.md` — 基本面（估值 + 财务）
- `market.md` — 市场面（大盘 + 行业 + 板块资金）

### 第 4 步：Phase 2 多空辩论（并行）

`bull.md` / `bear.md`：基于 5 份分析师报告 + 数据包，各自构建最强多/空逻辑链。**必须引用具体数据，不得空泛**。

### 第 5 步：Phase 3 研究经理汇总（串行）

`research_manager.md`：读全部 7 份报告，输出最终研究报告（结论/目标区间/风险/跟踪信号）。

### 第 6 步：md → PDF → 落盘深度分析目录

```bash
# PDF（研报风管线，QwenPaw 本地直接执行：扩展镜像已内置 reportlab + 中文字体）
python3 /app/backend/scripts/md_to_pdf_report.py /tmp/stock-research/{symbol}/reports/final.md /tmp/ma_report.pdf

# 落盘（A股市场/{股票名}/，与深度分析报告同列表）
# /data 为 QwenPaw 与 quantmind 共享挂载，直接写入即可被「报告档案」页实时列出
mkdir -p '/data/reports/stock_reports/A股市场/{股票名}'
cp /tmp/stock-research/{symbol}/reports/final.md '/data/reports/stock_reports/A股市场/{股票名}/{股票名}{代码}_2026-08-29_深度研究分析报告.md'
cp /tmp/ma_report.pdf '/data/reports/stock_reports/A股市场/{股票名}/{股票名}{代码}_2026-08-29_深度研究分析报告.pdf'
```

文件名约定：`{股票名}{代码}_{日期}_深度研究分析报告.pdf`（与现有深度学习分析报告同格式，便于排序）。

### 第 7 步：聊天回复速览

3-5 行：结论评级、关键数据（现价/PE/资金/情绪）、主要风险、报告路径。

## 支持的分析师独立运行

用户指定单个分析师时只跑该角色（如"技术面分析 600519"）：步骤 1 + 3（单 Agent）+ 直接输出该角色报告。

## 已知边界

- 财务为最新报告期（季度），非实时；估值/技术指标为最新交易日
- 新闻情绪依赖 FinBERT 富集（PG），Huntly 断流时新闻段降级为空并在报告中标注
- 仅支持 A 股（QuantDB 主库）；港股/美股个股研究走其他 skill
- 报告落盘目录为容器 root，宿主机不可写，统一容器内操作
