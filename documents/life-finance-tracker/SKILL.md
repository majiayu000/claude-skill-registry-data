---
name: life-finance-tracker
description: 管理个人财务记录 — 查看净值状态、从 Numbers 同步月度快照、分析资产变动趋势。Use when the user says "净值", "财务状态", "sync finances", "net worth", or after a monthly snapshot lands. NOT for investment strategy or relocation-portability questions (use life-strategic-advisor) or day-to-day expense capture (the expense app).
---

# 个人财务跟踪

管理个人资产负债表，跟踪净值变化。**主编辑在 Numbers，自动同步到 Obsidian。**

## 文件位置

- **MOC 索引**: `20_Areas/Finances/net-worth/_净值跟踪.md`
- **快照文件**: `20_Areas/Finances/net-worth/净值-YYYY-MM-DD.md`
- **CSV 数据**: `20_Areas/Finances/net-worth/data/`
- **更新模板**: `20_Areas/Finances/net-worth/templates/净值快照模板.md`
- **Numbers 源文件**: `/Users/kb/Library/Mobile Documents/com~apple~Numbers/Documents/`

## 命令

### 1. 查看最新财务状态

**触发词**: 「最新财务状态」「我的净值」「财务概览」「净值多少」

执行步骤：
1. 读取最新的 `净值-YYYY-MM-DD.md` 文件
2. 显示概览表格：
   - 总净值
   - 总资产（流动 + 固定）
   - 总债务（长期 + 短期）
3. 如用户需要，展开资产/债务明细

### 2. 同步最新财务（从 Numbers）

**触发词**: 「同步财务」「更新财务」「同步 Numbers」「记录这个月财务」

执行步骤：
1. 列出 Numbers 文件夹中最新的净值文件
2. 询问用户确认要同步哪个文件
3. 使用 Python + numbers-parser 提取数据：
   - 概览 sheet → 总净值/资产/债务
   - 资产 sheet → 流动资产、固定资产明细
   - 债务 sheet → 短期、长期债务明细
4. 生成 `净值-YYYY-MM-DD.md` Markdown 文件
5. 追加数据到对应年份的 CSV 文件
6. 更新 `_净值跟踪.md` 最新快照链接
7. 显示同步结果摘要

**Python 提取代码片段：**
```python
from numbers_parser import Document

SOURCE_DIR = "/Users/kb/Library/Mobile Documents/com~apple~Numbers/Documents/"

def extract_from_numbers(filename):
    doc = Document(f"{SOURCE_DIR}/{filename}")
    data = {'overview': {}, 'assets': [], 'debts': []}

    for sheet in doc.sheets:
        if sheet.name == "概览":
            # 提取 总净值、总资产、总债务 表格
        elif sheet.name == "资产":
            # 提取 流动资产、固定资产、个人项目 表格
        elif sheet.name == "债务":
            # 提取 短期债务、长期债务 表格

    return data
```

### 3. 净值趋势分析

**触发词**: 「净值趋势」「资产变化」「对比上月」「今年变化」

执行步骤：
1. 读取 `data/净值概览-YYYY.csv`
2. 计算并显示：
   - 本月 vs 上月变化
   - 今年累计变化
   - 同比去年（如有数据）
3. 用简单图表展示趋势

### 4. 查看资产/债务明细

**触发词**: 「资产明细」「债务明细」「银行余额」「信用卡欠款」

执行步骤：
1. 读取最新快照或指定日期快照
2. 展示对应明细表格

## 数据结构

### Numbers 文件结构（3个 Sheets）
- **概览**: 总净值表、总资产表、总债务表
- **资产**: 流动资产、固定资产、个人项目
- **债务**: 短期债务、长期债务

### CSV 文件
| 文件 | 内容 |
|------|------|
| 净值概览-YYYY.csv | 日期,总资产,流动资产,固定资产,总债务,长期债务,短期债务,净值 |
| 资产明细-YYYY.csv | 日期,类别,账户,金额,币种 |
| 债务明细-YYYY.csv | 日期,类别,项目,金额,备注 |
| 净值变动-YYYY.csv | 月度净值变动历史 |

## 工作流

```
┌─────────────┐     「同步财务」     ┌─────────────┐
│   Numbers   │  ───────────────▶  │  Obsidian   │
│  (主编辑)    │    Claude Code     │  (查看/存档) │
└─────────────┘                    └─────────────┘
```

**每月流程：**
1. 月初在 Numbers 更新上月末数据
2. 对 Claude Code 说「同步最新财务」
3. 自动生成 Markdown + 更新 CSV
4. 在 Obsidian 查看、搜索、关联

## 汇率说明

- 主货币：人民币 (¥)
- 澳币账户在"备注"列显示 AUD 原值
- 汇率转换已在 Numbers 中完成

## 示例对话

**用户**: 最新财务状态
**Claude**: 读取 净值-2025-11-30.md，显示概览表格

**用户**: 同步这个月的财务
**Claude**: 检测到最新文件 `净值 2026-01-03.numbers`，是否同步？
**用户**: 是
**Claude**: 提取数据，生成 Markdown，更新 CSV，显示结果

**用户**: 对比上个月
**Claude**: 读取 CSV，计算变化，显示趋势
