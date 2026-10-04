---
name: finance-accounting
version: 1.0.0
description: "财务会计文书处理综合技能包 - 包含记账、对账、税务、报表等核心功能"
author: 天元 (⚡)
category: finance
tags: [accounting, finance, tax, document, invoice]
dependencies:
  - python>=3.11
  - pandas
  - openpyxl
  - reportlab
---

# 财务会计文书技能

## 概述
本技能包提供完整的财务会计文书处理功能，包括记账、对账、税务计算、报表生成等核心业务流程。

## 功能模块

### 1. 基础记账模块
- **流水账记录**: 收入、支出、转账记录
- **科目管理**: 会计科目设置和分类
- **凭证生成**: 自动生成会计凭证
- **余额计算**: 实时计算账户余额

### 2. 对账模块
- **银行对账**: 自动匹配银行流水
- **往来对账**: 客户/供应商对账
- **差异处理**: 自动识别和处理差异
- **对账报告**: 生成对账报告

### 3. 税务模块
- **增值税计算**: 自动计算增值税
- **所得税预缴**: 个人所得税/企业所得税
- **税务申报**: 生成税务申报表
- **税务规划**: 税务优化建议

### 4. 报表模块
- **资产负债表**: 自动生成资产负债表
- **利润表**: 生成利润表
- **现金流量表**: 现金流量分析
- **自定义报表**: 按需生成报表

### 5. 文档生成
- **发票生成**: 自动生成电子发票
- **对账单**: 客户对账单
- **税务报告**: 税务申报文档
- **审计报告**: 审计所需文档

## 使用方法

### 基本记账
```bash
# 记录收入
python finance.py record --type income --amount 1000 --category "销售收入" --date "2026-02-28"

# 记录支出
python finance.py record --type expense --amount 500 --category "办公用品" --date "2026-02-28"

# 查看余额
python finance.py balance
```

### 对账处理
```bash
# 导入银行流水
python finance.py reconcile import --file bank_statement.csv

# 自动对账
python finance.py reconcile auto

# 生成对账报告
python finance.py reconcile report --output reconciliation_report.pdf
```

### 税务计算
```bash
# 计算增值税
python finance.py tax vat --period 2026-02

# 生成税务申报表
python finance.py tax report --type vat --period 2026-02 --output vat_report.xlsx

# 税务规划建议
python finance.py tax plan --year 2026
```

### 报表生成
```bash
# 生成资产负债表
python finance.py report balance-sheet --period 2026-02 --output balance_sheet.pdf

# 生成利润表
python finance.py report income-statement --period 2026-02 --output income_statement.pdf

# 生成现金流量表
python finance.py report cash-flow --period 2026-02 --output cash_flow.pdf
```

## 配置文件

### 会计科目设置
```yaml
# config/accounts.yaml
accounts:
  assets:
    - code: 1001
      name: 现金
      type: current_asset
    - code: 1002
      name: 银行存款
      type: current_asset
  
  liabilities:
    - code: 2001
      name: 短期借款
      type: current_liability
  
  equity:
    - code: 3001
      name: 实收资本
      type: equity
  
  income:
    - code: 4001
      name: 主营业务收入
      type: revenue
  
  expenses:
    - code: 5001
      name: 办公费用
      type: expense
```

### 税务设置
```yaml
# config/tax.yaml
tax:
  vat_rate: 0.13  # 增值税率
  income_tax_rate: 0.25  # 企业所得税率
  tax_threshold: 300000  # 起征点
  
  declarations:
    vat: monthly  # 增值税申报周期
    income_tax: quarterly  # 所得税申报周期
```

## 数据格式

### 交易记录格式
```csv
date,type,account,amount,description,category
2026-02-28,income,4001,1000.00,销售产品,销售收入
2026-02-28,expense,5001,500.00,购买办公用品,办公费用
```

### 银行流水格式
```csv
date,description,amount,balance
2026-02-28,工资收入,10000.00,15000.00
2026-02-28,水电费支出,-500.00,14500.00
```

## 集成功能

### 与现有技能集成
- **github技能**: 版本控制财务数据
- **tavily-search技能**: 搜索税务法规
- **proactive-agent技能**: 自动执行定期任务

### 外部系统集成
- **银行API**: 自动获取银行流水
- **税务系统**: 电子申报接口
- **ERP系统**: 企业资源计划集成

## 安全注意事项

### 数据安全
- 财务数据加密存储
- 访问权限控制
- 操作日志记录

### 合规性
- 符合会计准则
- 遵守税务法规
- 审计追踪

## 故障排除

### 常见问题
1. **数据导入失败**: 检查文件格式和编码
2. **计算错误**: 验证会计科目设置
3. **报表生成失败**: 检查依赖库安装

### 日志查看
```bash
# 查看运行日志
tail -f logs/finance.log

# 查看错误日志
tail -f logs/error.log
```

## 更新计划

### 近期更新
- [ ] 添加更多报表模板
- [ ] 支持更多银行格式
- [ ] 优化税务计算算法

### 长期规划
- [ ] AI智能分析功能
- [ ] 预测和预算功能
- [ ] 多语言支持

---

**技能状态**: ✅ 就绪  
**最后更新**: 2026-02-28  
**维护者**: 天元 (⚡)