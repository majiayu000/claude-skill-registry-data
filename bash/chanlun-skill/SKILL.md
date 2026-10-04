---
name: chanlun
version: "2026.3.13-1"
updated: "2026-03-13"
description: "缠论技术分析 Skill，用于 Solana Meme 币的 K 线结构分析、笔/线段/中枢识别、背驰判断和买卖点输出。当用户询问某个代币的技术面、买卖时机、趋势判断、是否有买点/卖点时使用。"
---

# 缠论 Skill

## 依赖

本 Skill 依赖 `bitget-wallet-skill` 提供 K 线数据和交易执行能力。

**启动时检查（每次加载 Skill 时执行）：**

```bash
# 检查 bitget-wallet-skill 是否存在（相对于本 Skill 的父目录）
ls ../bitget-wallet-skill/scripts/bitget_api.py
```

如果不存在，自动安装：

```bash
cd ..
git clone https://github.com/bitget-wallet-ai-lab/bitget-wallet-skill.git
```

安装完成后继续。如果 clone 失败（无网络/权限），告知用户手动执行上述命令。

**Python 依赖检查：**

```bash
pip install requests -q
```

---

## 使用方式

所有分析通过 `scripts/` 目录下的脚本执行，用户无需直接操作，由 Agent 在后台调用。

---

## 分析流程

### 第一步：获取并预处理 K 线

```bash
python3 scripts/bi.py --chain <chain> --contract <contract> --period <period> --size 300
```

**周期选择建议：**

| 市场状态 | 推荐周期 |
|---------|---------|
| Meme 币日内短线 | 1m / 5m |
| Meme 币波段 | 15m / 1h |
| SOL / 大盘币 | 1h / 4h |

**输出解读：**
- `原始K线 → 处理K线`：合并了多少包含关系
- 笔列表：每笔的方向、起止时间、价格、涨跌幅
- `进行中`：当前最新笔尚未被反向分型确认，仍在延伸

---

## 核心概念（Domain Knowledge）

### 包含关系
两根 K 线，若一根的 high/low 完全覆盖另一根，则存在包含关系，按方向合并为一根处理K线：
- 上涨方向：取两者中 high 较大、low 较大（向上合并）
- 下跌方向：取两者中 high 较小、low 较小（向下合并）

### 分型
- **顶分型**：连续三根处理K线，中间一根的 high 严格最高
- **底分型**：连续三根处理K线，中间一根的 low 严格最低

### 笔
- 一个顶分型 + 一个底分型（或反向）构成一笔
- 两个分型中心索引差 >= 3（中间至少有1根独立处理K线）
- 方向交替（不能连续两个同向分型构成笔）
- 同向分型竞争时，保留更极端的（更高的顶 / 更低的底）

### 判断当前走势
- **最新笔方向**：当前行情的短期方向
- **笔的序列**：连续多笔的高点/低点是否在抬升或下降
- **涨跌幅对比**：相邻同向笔的幅度是否收缩（背驰前兆）

---

## 常见任务

### 任务：分析某 token 是否有买点

1. 运行 bi.py 获取笔列表
2. 检查最新笔是否为向上笔（进行中）
3. 检查前几笔是否构成底部结构（连续下跌笔后出现向上笔）
4. 检查向下笔序列：如果下跌幅度逐笔收缩 → 底背驰前兆
5. 结合成交量（tx-info）：下跌笔成交量萎缩 → 更强烈的底部信号
6. 输出结论和建议入场区间

### 任务：扫描市场找机会

1. 调用 bitget-wallet-skill 的 rankings（topGainers / Hotpicks）获取候选列表
2. 对每个候选 token 运行 bi.py
3. 筛选：最新笔为向上笔 + 近期笔结构有底部形态 的 token
4. 输出候选列表供用户选择

### 任务：判断当前是否该卖

1. 运行 bi.py 获取笔列表
2. 检查最新笔是否为向下笔（进行中）
3. 检查向上笔序列：如果涨幅逐笔收缩 → 顶背驰前兆
4. 输出风险提示

---

## 脚本参考

### scripts/analyze.py — 完整分析主入口（P0+P1+P2 全流程）

```bash
python3 scripts/analyze.py \
  --chain <chain>       \  # sol / eth / bnb / base ...
  --contract <address>  \  # 合约地址，原生代币用空字符串 ""
  --period <period>     \  # 1m / 5m / 15m / 1h / 4h
  --size <n>            \  # K线数量，建议 200~300
  --symbol <name>          # 可选，代币符号（仅用于显示）
```

**输出包含：**
- K线预处理摘要
- 笔识别（最近5笔）
- 线段识别（最近4条）
- 中枢分析（ZG/ZD/位置/趋势）
- 背驰判断（是否顶/底背驰）
- 买卖点信号（一买/二买/三买/一卖/二卖/三卖）
- 综合结论（趋势 + 建议 + 止损位）

**这是 Agent 应优先调用的命令。**

---

### scripts/bi.py — P0 主入口（K线预处理 + 笔识别）

```bash
python3 scripts/bi.py \
  --chain <chain>       \  # sol / eth / bnb / base ...
  --contract <address>  \  # 合约地址，原生代币用空字符串 ""
  --period <period>     \  # 1m / 5m / 15m / 1h / 4h
  --size <n>               # K线数量，建议 200~300
```

**输出包含：**
- K线预处理摘要（原始/处理数量、合并数）
- 笔列表（方向、时间、价格、涨跌幅、是否进行中）

### scripts/kline_fetch.py — 直接获取 K 线数据

```bash
python3 scripts/kline_fetch.py \
  --chain sol --contract "" --period 5m --size 100
```

---

## 链标识速查

| 链 | 代码 |
|----|------|
| Solana | sol |
| Ethereum | eth |
| BNB Chain | bnb |
| Base | base |
| Arbitrum | arbitrum |

原生代币（SOL/ETH/BNB）使用空字符串 `""` 作为合约地址。

---

## 安全原则

- 本 Skill 仅做技术分析，不自动执行交易
- 买卖点判断仅供参考，实盘需结合安全审计（使用 bitget-wallet-skill 的 security 命令）
- 交易执行始终需要用户明确确认
