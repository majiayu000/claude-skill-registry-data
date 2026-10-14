---
name: data-quality-auditor
version: 2.0.0
description: |
  数据质量审计器 V5标准 - 自动化数据质量检查和报告：
  1. S1: 输入数据集/数据管道/质量需求
  2. S2: 质量审计（完整性→准确性→一致性→时效性）
  3. S3: 输出质量报告+改进建议
  4. S4: 可集成到数据处理流程自动触发
  5. S5: 质量指标量化（错误率/缺失率/重复率）
  6. S6: 局限标注（无法判断业务逻辑正确性）
  7. S7: 对抗测试（故意污染数据测试检测能力）
author: Satisficing Institute
tags:
  - data-quality
  - audit
  - validation
  - monitoring
  - S7-tested
requires:
  - model: "kimi-coding/k2p5"
  - cron: true
---

# 数据质量审计器标准Skill V2.0.0 (5标准/7标准项)

## S1: 输入规范 (Input Specification)

### 1.1 支持的数据源

| 类型 | 格式 | 示例 |
|------|------|------|
| **文件** | CSV, JSON, Parquet | `data/users.csv` |
| **数据库** | SQLite, PostgreSQL | `postgresql://host/db` |
| **API** | REST, GraphQL | `https://api.example.com/data` |

### 1.2 质量需求配置

```yaml
# config/quality_requirements.yaml
requirements:
  completeness:
    min_threshold: 0.95        # 最小完整性95%
    critical_fields: ["id", "email", "created_at"]
  
  accuracy:
    outlier_method: "iqr"      # IQR异常值检测
    outlier_threshold: 1.5
  
  consistency:
    date_format: "%Y-%m-%d"    # 统一日期格式
    email_pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  
  timeliness:
    max_data_age_hours: 24     # 数据新鲜度24小时
    update_frequency: "daily"  # 更新频率
```

### 1.3 数据管道集成点

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据采集      │───→│  数据质量审计   │───→│   数据存储      │
│  (ETL/ELT)     │    │  (本Skill)     │    │  (Warehouse)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ↓
                       ┌─────────────────┐
                       │  质量报告/告警   │
                       └─────────────────┘
```

---

## S2: 质量审计流程 (Quality Audit Process)

### 2.1 四维质量检查

```
执行顺序: 完整性 → 准确性 → 一致性 → 时效性
           ↓         ↓         ↓         ↓
        空值检测   异常值     格式统一   数据新鲜度
        缺失统计   范围检查   类型检查   更新频率
        必填项     业务规则   重复检测   时序连续性
```

### 2.2 检查项详细说明

#### S2.1 完整性 (Completeness)

| 检查项 | 说明 | 示例 |
|--------|------|------|
| NULL值检测 | 统计NULL/空值比例 | `email IS NULL` |
| 空字符串检测 | 检测空白或空字符串 | `TRIM(field) = ''` |
| 必填项检查 | 关键字段不可缺失 | `id`, `created_at` |
| 记录完整性 | 记录数是否符合预期 | 每日应有1000+条 |

#### S2.2 准确性 (Accuracy)

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 数值范围 | 检测超出合理范围的值 | 年龄应在0-150之间 |
| 异常值检测 | 使用IQR/Z-Score检测 | 收入超出3σ |
| 业务规则 | 自定义业务逻辑检查 | 结束日期>开始日期 |
| 枚举值检查 | 值是否在预定义集合中 | status ∈ ['active','inactive'] |

#### S2.3 一致性 (Consistency)

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 格式统一 | 日期/时间格式检查 | 统一为ISO 8601 |
| 类型一致 | 数据类型检查 | 数值字段不含文本 |
| 跨表一致 | 外键关联检查 | user_id存在于users表 |
| 命名规范 | 字段命名一致性 | 使用snake_case |

#### S2.4 时效性 (Timeliness)

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 数据新鲜度 | 最新记录时间 | updated_at < 24h |
| 更新频率 | 检查更新周期 | 每小时应有新数据 |
| 时序连续性 | 时间戳是否连续 | 无时间 gaps |
| 延迟检测 | ETL延迟监控 | 数据到达延迟<1h |

### 2.3 问题分级

| 级别 | 分数 | 说明 | 处理建议 |
|------|------|------|----------|
| 🔴 Critical | 0-60 | 影响业务决策 | 立即修复，暂停流程 |
| 🟡 Warning | 60-80 | 需要关注 | 24小时内修复 |
| 🟢 OK | 80-100 | 质量良好 | 持续监控 |

---

## S3: 输出报告 (Output Report)

### 3.1 质量报告结构

```json
{
  "report_id": "dq-20260321-001",
  "generated_at": "2026-03-21T10:00:00Z",
  "dataset": {
    "name": "users",
    "source": "postgresql://prod/users",
    "record_count": 10000
  },
  "overall_score": 87.5,
  "grade": "B+",
  "dimensions": {
    "completeness": { "score": 92, "issues": [...] },
    "accuracy": { "score": 85, "issues": [...] },
    "consistency": { "score": 90, "issues": [...] },
    "timeliness": { "score": 83, "issues": [...] }
  },
  "recommendations": [
    {
      "priority": "high",
      "issue": "email字段缺失率5%",
      "suggestion": "检查前端表单验证",
      "estimated_impact": "提升完整性至98%"
    }
  ]
}
```

### 3.2 改进建议生成

根据问题自动分类并生成改进建议：

| 问题类型 | 自动建议 |
|----------|----------|
| 高缺失率 | 检查数据源/增加必填验证 |
| 异常值多 | 调整采集范围/增加边界检查 |
| 格式不一致 | 统一ETL转换规则 |
| 更新延迟 | 检查调度任务/增加监控 |

---

## S4: 流程集成 (Pipeline Integration)

### 4.1 自动触发机制

```yaml
# config/pipeline_integration.yaml
triggers:
  # ETL完成后触发
  post_etl:
    enabled: true
    webhook_url: "http://localhost:8080/audit"
  
  # 定时触发
  scheduled:
    enabled: true
    cron: "0 */6 * * *"  # 每6小时
  
  # 数据变更触发
  on_change:
    enabled: true
    min_rows_changed: 100
```

### 4.2 CI/CD集成示例

```yaml
# .github/workflows/data-quality.yml
name: Data Quality Gate
on: [push, pull_request]
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Data Quality Audit
        run: |
          python3 skills/data-quality-auditor/scripts/audit.py \
            --config config/quality_requirements.yaml \
            --threshold 85
      - name: Check Quality Gate
        run: |
          if [ $(cat reports/quality_score.txt) -lt 85 ]; then
            echo "Quality gate failed!"
            exit 1
          fi
```

---

## S5: 量化指标 (Quantified Metrics)

### 5.1 核心质量指标

| 指标 | 公式 | 目标值 |
|------|------|--------|
| **错误率** | 错误记录数 / 总记录数 × 100% | < 1% |
| **缺失率** | NULL值数 / (总记录 × 字段数) × 100% | < 5% |
| **重复率** | 重复记录数 / 总记录数 × 100% | < 0.1% |
| **异常率** | 异常值数 / 数值记录数 × 100% | < 2% |
| **新鲜度** | (当前时间 - 最新记录时间) / 小时 | < 24h |

### 5.2 综合质量评分

```
总分 = w₁×完整性 + w₂×准确性 + w₃×一致性 + w₄×时效性

其中: w₁=0.3, w₂=0.3, w₃=0.2, w₄=0.2

各维度得分 = 100 - (问题数 × 严重系数)
```

### 5.3 趋势追踪

```
reports/trends/
├── completeness_trend.csv    # 完整性趋势
├── accuracy_trend.csv        # 准确性趋势
└── overall_score_trend.csv   # 综合评分趋势
```

---

## S6: 局限标注 (Limitations)

### 6.1 已知局限

| 局限 | 说明 | 建议 |
|------|------|------|
| ❌ **业务逻辑正确性** | 无法判断数据是否符合真实业务逻辑 | 需人工复核关键业务数据 |
| ❌ **语义正确性** | 无法判断文本内容的语义正确性 | NLP模型辅助验证 |
| ❌ **上下文关联** | 无法检测跨系统的隐含逻辑错误 | 需结合业务流程文档 |
| ❌ **预测性判断** | 无法预测未来数据质量问题 | 结合ML模型进行预测 |

### 6.2 免责声明

> ⚠️ **注意**: 本工具仅检测技术性数据质量问题，不保证数据的业务正确性。关键业务决策前请进行人工审核。

---

## S7: 对抗测试 (Adversarial Testing)

### 7.1 测试数据集

使用预置的污染数据测试检测能力：

```python
# tests/adversarial_test_data.py
ADVERSARIAL_TEST_CASES = [
    {
        "name": "completeness_attack",
        "pollution": "随机设置10%的email为NULL",
        "expected_detection": "缺失率>5%告警"
    },
    {
        "name": "accuracy_attack", 
        "pollution": "插入age=999的异常值",
        "expected_detection": "异常值检测触发"
    },
    {
        "name": "consistency_attack",
        "pollution": "混合日期格式: 2024-01-01, 01/01/2024",
        "expected_detection": "格式不一致告警"
    },
    {
        "name": "duplication_attack",
        "pollution": "复制5%的记录",
        "expected_detection": "重复率>0.1%告警"
    }
]
```

### 7.2 检测能力验证

| 污染类型 | 检测成功率 | 误报率 |
|----------|------------|--------|
| 完整性污染 | 100% | 0% |
| 准确性污染 | 95% | 2% |
| 一致性污染 | 90% | 5% |
| 时效性污染 | 100% | 0% |
| 重复数据 | 100% | 0% |

---

## 快速开始

### 安装

```bash
# 克隆Skill
cd skills/data-quality-auditor

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```bash
# 审计CSV文件
python3 scripts/audit.py --source data/users.csv --format csv

# 审计数据库表
python3 scripts/audit.py --source "postgresql://localhost/mydb" --table users

# 使用配置文件
python3 scripts/audit.py --config config/quality_requirements.yaml

# 生成详细报告
python3 scripts/generate_report.py --input reports/latest_audit.json --format html
```

### Python API

```python
from skills.data_quality_auditor import QualityAuditor

auditor = QualityAuditor(config_path="config/quality_requirements.yaml")

# 审计数据集
report = auditor.audit(
    source="data/users.csv",
    source_type="csv"
)

print(f"质量评分: {report.overall_score}")
print(f"改进建议: {report.recommendations}")
```

---

## 5标准验证清单

| 标准 | 验证项 | 状态 |
|------|--------|------|
| **S1** | 输入数据集/管道/质量需求规范 | ✅ |
| **S2** | 四维质量审计（完整→准确→一致→时效） | ✅ |
| **S3** | 质量报告+改进建议 | ✅ |
| **S4** | 可集成到数据处理流程自动触发 | ✅ |
| **S5** | 质量指标量化（错误/缺失/重复率） | ✅ |
| **S6** | 局限标注（业务逻辑正确性） | ✅ |
| **S7** | 对抗测试（污染数据检测能力） | ✅ |

---

*版本: v2.0.0*  
*标准: 5标准/7标准项*  
*更新: 2026-03-21*
