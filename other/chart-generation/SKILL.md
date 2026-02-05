---
name: chart-generation
description: 生成专业金融图表（K线图、技术指标图）。适用于数据可视化、技术分析展示、报告生成等场景。支持多种图表类型（basic、comprehensive）和自定义样式（深色、浅色主题）。
license: MIT
allowed-tools:
  - generate_candlestick_chart
  - generate_comprehensive_chart
metadata:
  version: "1.0.0"
  author: "YFOOOO"
  chart_library: "mplfinance"
  supported_themes:
    - dark
    - light
---

# Chart Generation Skill

专业的金融图表生成工具，基于 mplfinance 库。

## Overview

本 Skill 提供以下核心功能：
1. **基础K线图** - 经典的蜡烛图（Candlestick Chart）
2. **综合技术图** - K线图 + 技术指标（MA、MACD、成交量）
3. **主题定制** - 深色/浅色主题，专业美观

所有图表支持保存为 PNG 文件或在 Jupyter Notebook 中直接显示。

## Quick Start

### 1. 准备数据

图表生成需要 OHLCV 数据（开盘、最高、最低、收盘、成交量）。
通常先调用 `financial-data-fetch` Skill 获取数据。

如需技术指标图表，还需调用 `technical-indicators` Skill 计算指标。

### 2. 选择图表类型

- **基础K线图** → `generate_candlestick_chart`（仅蜡烛图 + 成交量）
- **综合技术图** → `generate_comprehensive_chart`（K线 + MA + MACD + 成交量）

### 3. 调用工具

```python
# 示例：生成综合技术图
result = generate_comprehensive_chart(
    data=stock_data,        # 包含 OHLCV 和技术指标的 DataFrame
    symbol="000001",        # 股票代码
    title="平安银行技术分析", # 图表标题
    theme="dark",           # 主题（dark/light）
    save_path="chart.png"   # 保存路径（可选）
)
```

## Chart Types

### 1. Basic Candlestick Chart

**Tool**: `generate_candlestick_chart`

**Purpose**: 生成经典的蜡烛图，适用于：
- 快速查看价格走势
- 技术形态识别（如十字星、锤子线）
- 简洁报告展示

**Parameters**:
- `data` (DataFrame, required): 包含 OHLCV 数据
  - 必需列：日期（索引）、开盘、收盘、最高、最低、成交量
- `symbol` (str, optional): 股票代码（用于标题）
- `title` (str, optional): 自定义标题
- `theme` (str, optional): 主题（"dark" or "light"，默认"dark"）
- `save_path` (str, optional): 保存路径（如 "output/chart.png"）

**Returns**: Dict with:
- `success` (bool): 是否成功
- `message` (str): 结果描述
- `saved_path` (str): 保存路径（如果指定）

**Example**:
```python
result = generate_candlestick_chart(
    data=stock_data,
    symbol="000001",
    theme="dark",
    save_path="candlestick.png"
)
# 生成纯净的K线图 + 成交量副图
```

### 2. Comprehensive Chart

**Tool**: `generate_comprehensive_chart`

**Purpose**: 生成综合技术分析图表，适用于：
- 专业技术分析
- 多指标联合判断
- 详细报告生成

**Chart Layout**:
```
┌─────────────────────────────┐
│  主图: K线 + MA(5/10/20/60) │  ← 蜡烛图 + 移动平均线
├─────────────────────────────┤
│  副图1: MACD               │  ← DIF/DEA/BAR柱状图
├─────────────────────────────┤
│  副图2: 成交量              │  ← 柱状图（红绿分色）
└─────────────────────────────┘
```

**Parameters**:
- `data` (DataFrame, required): 包含 OHLCV + 技术指标数据
  - 必需列：日期、开盘、收盘、最高、最低、成交量
  - 可选列：MA_5, MA_10, MA_20, MA_60（移动平均线）
  - 可选列：MACD_DIF, MACD_DEA, MACD_BAR（MACD指标）
- `symbol` (str, optional): 股票代码
- `title` (str, optional): 自定义标题
- `theme` (str, optional): 主题（"dark" or "light"）
- `save_path` (str, optional): 保存路径

**Returns**: 同 Basic Chart

**Example**:
```python
# 先获取数据和计算指标
stock_data = fetch_stock_data(symbol="000001", days=60)
stock_data = calculate_all_indicators(stock_data)

# 生成综合图表
result = generate_comprehensive_chart(
    data=stock_data,
    symbol="000001",
    title="平安银行 - 60日技术分析",
    theme="dark",
    save_path="comprehensive.png"
)
```

## Themes

### Dark Theme (默认)

适用于：
- 现代化界面
- 夜间查看
- 专业演示

**特点**:
- 黑色背景
- 高对比度
- 护眼配色

### Light Theme

适用于：
- 打印输出
- 传统报告
- 明亮环境

**特点**:
- 白色背景
- 清晰线条
- 经典配色

### 自定义主题

主题配置文件位于 `assets/chart_styles/`：
- `dark_theme.json` - 深色主题配置
- `light_theme.json` - 浅色主题配置

可以编辑 JSON 文件自定义：
- 背景色、网格色
- 蜡烛颜色（涨/跌）
- 成交量颜色
- MA 线条颜色和样式

## Data Requirements

### Minimum Required Columns

| 列名 | 类型 | 说明 |
|------|------|------|
| 日期 | datetime | 必需，作为索引或列 |
| 开盘 | float | 必需 |
| 收盘 | float | 必需 |
| 最高 | float | 必需 |
| 最低 | float | 必需 |
| 成交量 | int/float | 必需 |

### Optional Columns (for Comprehensive Chart)

| 列名 | 类型 | 说明 |
|------|------|------|
| MA_5, MA_10, MA_20, MA_60 | float | 移动平均线 |
| MACD_DIF, MACD_DEA | float | MACD快慢线 |
| MACD_BAR | float | MACD柱状图 |

## Error Handling

### 1. 数据验证失败
```
错误：缺少必需列 ['开盘', '收盘', '最高', '最低']
```
**解决**: 确保数据包含所有必需的 OHLCV 列

### 2. 数据为空
```
错误：数据为空，无法生成图表
```
**解决**: 检查数据获取是否成功

### 3. 保存失败
```
错误：无法保存图表到 /invalid/path/chart.png
```
**解决**: 检查保存路径是否有效且有写入权限

### 4. 技术指标列缺失
```
警告：未找到 MA 指标列，将跳过均线绘制
```
**说明**: 不影响基础K线图生成，但综合图表会缺少对应指标

## Performance Notes

- **生成时间**: 通常 < 2秒（60条数据）
- **图片大小**: 约 100-200 KB（PNG格式）
- **分辨率**: 默认 1200x800 像素（高清）
- **内存使用**: < 50 MB

## Decision Tree

```
用户需求
    ├─ 仅查看价格走势？
    │   └─ 是 → generate_candlestick_chart
    │
    ├─ 需要技术指标分析？
    │   └─ 是 → generate_comprehensive_chart
    │
    └─ 选择主题
        ├─ 现代化/夜间 → theme="dark"
        └─ 打印/传统 → theme="light"
```

## Best Practices

### 1. 数据量建议
```python
# 推荐数据量
- 日K线: 30-120 条（1-6个月）
- 周K线: 50-200 条（1-4年）

# 避免过多数据
data = stock_data.tail(120)  # 只取最近120条
```

### 2. 标题规范
```python
# 清晰的标题格式
title = f"{stock_name}({symbol}) - {days}日K线"
# 示例: "平安银行(000001) - 60日K线"
```

### 3. 保存路径管理
```python
# 使用相对路径，按日期组织
from datetime import datetime
date_str = datetime.now().strftime("%Y%m%d")
save_path = f"outputs/{symbol}_{date_str}.png"
```

### 4. 错误处理
```python
result = generate_comprehensive_chart(...)
if not result['success']:
    print(f"图表生成失败: {result['error']}")
else:
    print(f"图表已保存: {result['saved_path']}")
```

## References

详细文档和配置说明见：
- [mplfinance 使用指南](references/mplfinance_guide.md)
- [主题配置](assets/chart_styles/)

## Script Implementation

图表生成逻辑实现在：
- `skill.py` - Skill 主类（复用 core/visualization.py）

复用项目中的 `core/visualization.py` 模块，确保代码一致性。
