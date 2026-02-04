---
name: loading-insurance-data
description: 加载并预处理保险保单周度数据，支持智能周期检测、多周数据加载、数据验证和清洗。在开始任何保险数据分析任务时使用。
---

# 保险数据加载器

## 核心功能

处理保险业务周度CSV数据的完整加载流程：

- ✅ 智能检测可用周次
- ✅ 灵活周期范围设置
- ✅ 多年度数据支持（2024/2025）
- ✅ 数据质量验证
- ✅ 标准化预处理

## 立即使用

```python
from pathlib import Path
import pandas as pd

# 1. 检测可用周次
def detect_available_weeks(data_folder="2025年保单"):
    import re
    available = set()

    for file in Path(data_folder).glob("*保单第*周*.csv"):
        match = re.search(r'第(\d+)周', file.name)
        if match:
            available.add(int(match.group(1)))

    return sorted(available)

# 2. 加载单周数据
def load_week_data(week, data_folder="2025年保单"):
    pattern = f"*保单第{week}周*.csv"
    files = list(Path(data_folder).glob(pattern))

    if not files:
        return None

    df = pd.read_csv(files[0], encoding='utf-8-sig')
    df['week_number'] = week
    return df

# 3. 批量加载
weeks = detect_available_weeks()
print(f"可用周次: {weeks}")

data = {}
for week in weeks:
    df = load_week_data(week)
    if df is not None:
        data[week] = df
        print(f"✅ 第{week}周: {len(df):,}行")
```

## 数据文件结构

### 文件命名规范

```
{YEAR}保单第{WEEK}周变动成本明细表.csv

示例:
- 2025保单第28周变动成本明细表.csv
- 2025保单第43周变动成本明细表.csv
```

### 关键字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `policy_start_year` | int | 保单年度 |
| `third_level_organization` | str | 三级机构 |
| `business_type_category` | str | 业务类型 |
| `is_new_energy_vehicle` | bool | 是否新能源车 |
| `signed_premium_yuan` | float | 签单保费 |
| `matured_premium_yuan` | float | 满期保费 |
| `reported_claim_payment_yuan` | float | 已报告赔款 |
| `expense_amount_yuan` | float | 费用金额 |
| `claim_case_count` | int | 赔案件数 |
| `policy_count` | int | 保单件数 |

## 数据处理流程

### 步骤1: 周期检测

```python
# 自动扫描目录
available_weeks = detect_available_weeks()

# 确定分析周期
start_week = 28
end_week = 43
analysis_weeks = list(range(start_week, end_week + 1))

# 检查缺失
missing = [w for w in analysis_weeks if w not in available_weeks]
if missing:
    print(f"⚠️  缺失周次: {missing}")
```

### 步骤2: 数据加载

```python
loaded_data = {}

for week in analysis_weeks:
    if week in available_weeks:
        df = load_week_data(week)
        if df is not None:
            loaded_data[week] = df
```

### 步骤3: 数据清洗

```python
def preprocess_data(df):
    """标准化数据处理"""
    # 过滤本部
    df = df[df['third_level_organization'] != '本部'].copy()

    # 提取保单年度
    df['policy_year'] = df['policy_start_year'].astype(str).str.extract(r'(202[45])')[0]

    # 数值型字段转换
    numeric_cols = [
        'signed_premium_yuan',
        'matured_premium_yuan',
        'reported_claim_payment_yuan',
        'expense_amount_yuan',
        'claim_case_count',
        'policy_count'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df

# 应用清洗
for week in loaded_data:
    loaded_data[week] = preprocess_data(loaded_data[week])
```

### 步骤4: 数据验证

```python
def validate_data(df, week):
    """数据质量检查"""
    issues = []

    # 检查空数据
    if len(df) == 0:
        issues.append("数据为空")

    # 检查关键字段
    required = ['signed_premium_yuan', 'third_level_organization']
    missing = [col for col in required if col not in df.columns]
    if missing:
        issues.append(f"缺失字段: {missing}")

    # 检查负值
    if 'signed_premium_yuan' in df.columns:
        if (df['signed_premium_yuan'] < 0).any():
            issues.append("存在负保费")

    if issues:
        print(f"⚠️  第{week}周问题: {', '.join(issues)}")
        return False

    return True
```

## 数据输出结构

### 按年度分组

```python
def group_by_year(loaded_data):
    """按保单年度分组"""
    grouped = {'2024': {}, '2025': {}}

    for week, df in loaded_data.items():
        for year in ['2024', '2025']:
            year_df = df[df['policy_year'] == year]
            if len(year_df) > 0:
                grouped[year][week] = year_df

    return grouped

# 使用示例
data_by_year = group_by_year(loaded_data)
print(f"2024保单周次: {list(data_by_year['2024'].keys())}")
print(f"2025保单周次: {list(data_by_year['2025'].keys())}")
```

## 常见问题

### Q1: 文件编码错误

**问题**: `UnicodeDecodeError`

**解决**: 使用 `encoding='utf-8-sig'`

```python
df = pd.read_csv(file, encoding='utf-8-sig')
```

### Q2: 周次文件缺失

**问题**: 第32周、第38周等文件不存在

**解决**: 自动跳过并记录

```python
if week not in available_weeks:
    print(f"⚠️  第{week}周: 文件不存在，跳过")
    continue
```

### Q3: 数据类型错误

**问题**: 保费字段被识别为字符串

**解决**: 强制数值转换

```python
df['signed_premium_yuan'] = pd.to_numeric(
    df['signed_premium_yuan'],
    errors='coerce'
).fillna(0)
```

### Q4: 内存占用过大

**问题**: 加载多周数据内存不足

**解决**: 按需加载或只读取必要列

```python
# 只读取需要的列
usecols = [
    'policy_year',
    'third_level_organization',
    'signed_premium_yuan',
    'matured_premium_yuan',
    'reported_claim_payment_yuan'
]
df = pd.read_csv(file, usecols=usecols, encoding='utf-8-sig')
```

## 性能优化

### 批量加载优化

```python
from concurrent.futures import ThreadPoolExecutor

def load_weeks_parallel(weeks, data_folder):
    """并行加载多周数据"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(load_week_data, week, data_folder): week
            for week in weeks
        }

        results = {}
        for future in futures:
            week = futures[future]
            try:
                df = future.result()
                if df is not None:
                    results[week] = df
            except Exception as e:
                print(f"❌ 第{week}周加载失败: {e}")

        return results
```

### 内存管理

```python
import gc

# 加载和处理后释放内存
for week in weeks:
    df = load_week_data(week)
    processed = preprocess_data(df)
    # ... 使用数据 ...
    del df, processed
    gc.collect()
```

## 参考资源

脚本工具:
- `scripts/quick_load.py` - 快速数据加载工具
- `scripts/data_validator.py` - 数据质量检查工具

参考文档:
- `reference/data_schema.md` - 完整字段说明
- `reference/data_quality_rules.md` - 数据质量标准

## 更新日志

- v1.0 (2025-11-04): 初始版本
  - 基础加载功能
  - 智能周期检测
  - 数据验证和清洗
  - 多年度支持
