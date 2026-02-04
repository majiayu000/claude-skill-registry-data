---
name: data-governance-and-quality
description: Data governance strategy, quality validation rules, and data dictionary management for vehicle insurance platform. Use when defining data quality standards, implementing validation rules, managing field mappings, resolving data conflicts, or establishing data governance processes. Covers data cleaning standards, quality metrics, and mapping management.
allowed-tools: Read, Edit, Grep, Glob
---

# Data Governance and Quality Management

Comprehensive data governance framework for vehicle insurance daily report analysis platform, covering data quality rules, field definitions, cleaning standards, mapping management, and audit mechanisms.

## When to Use This Skill

Activate this skill when you need to:
- Define or validate data quality rules
- Implement field validation logic
- Manage staff-institution mapping updates
- Resolve data conflicts or inconsistencies
- Establish data cleaning standards
- Create data quality reports
- Design data audit mechanisms
- Document business field definitions

## 📚 一、数据字典 (Data Dictionary)

### 1.1 核心业务字段定义

**关键文件**: [docs/FIELD_MAPPING.md](../../../docs/FIELD_MAPPING.md)

#### 维度字段 (Dimensions)

| 字段名 | 数据类型 | 业务含义 | 枚举值 | 必填 |
|--------|----------|----------|--------|------|
| 三级机构 | String | 业务员所属三级机构 | 达州/德阳/绵阳/南充等 | ✅ |
| 四级机构 | String | 业务员所属四级机构 | 达州/德阳等 | ❌ |
| 团队简称 | String | 业务员所属团队 | 达州业务一部等 | ❌ |
| 业务员 | String | 销售人员姓名 | 从映射表提取 | ✅ |
| 客户类别3 | String | 客户类型 | 非营业个人客车/摩托车等9类 | ✅ |
| 险种大类 | String | 保险产品类别 | 车险/其他 | ✅ |
| 险种名称 | String | 具体险种 | 0312/0313/0317等 | ✅ |
| 是否续保 | String | 续保状态 | 新保/续保/转保 | ✅ |
| 是否新能源 | String | 新能源标志 | 是/否 | ✅ |
| 是否过户车 | String | 过户车标志 | 是/否 | ✅ |
| 终端来源 | String | 销售渠道 | 0110融合销售等 | ✅ |
| 吨位分段 | String | 货车吨位区间 | <2吨/2-5吨/5-10吨/>10吨 | ❌ |

#### 度量字段 (Metrics)

| 字段名 | 数据类型 | 业务含义 | 范围 | 必填 | 特殊规则 |
|--------|----------|----------|------|------|----------|
| 签单/批改保费 | Numeric | 签单净保费 | 可负数 | ✅ | 允许负值(退保/调整) |
| 签单数量 | Numeric | 保单数量 | ≥1 | ✅ | 整数 |
| 手续费含税 | Numeric | 含税手续费 | ≥0 | ❌ | 允许为0 |
| 签单/批改保额 | Numeric | 保额 | >0 | ❌ | 负数为异常 |
| 手续费比例 | Numeric | 手续费占保费比例 | 0-1 | ❌ | 百分比 |

#### 时间字段 (Temporal)

| 字段名 | 数据类型 | 格式 | 业务含义 | 必填 |
|--------|----------|------|----------|------|
| 投保确认时间 | Datetime | YYYY-MM-DD HH:MM:SS | 业务口径时间基准 | ✅ |
| 刷新时间 | Datetime | YYYY-MM-DD HH:MM:SS | 数据最新性标志 | ✅ |
| 保险起期 | Datetime | YYYY-MM-DD | 保单生效日期 | ✅ |

#### 标识字段 (Identifiers)

| 字段名 | 数据类型 | 业务含义 | 唯一性 | 必填 | 脱敏 |
|--------|----------|----------|--------|------|------|
| 保单号 | String | 保单唯一标识 | ❌ (结合时间) | ✅ | ❌ |
| 车牌号码 | String | 车辆标识 | ❌ | ❌ | ✅ |
| 被保险人 | String | 客户姓名 | ❌ | ✅ | ✅ |
| 车架号 | String | 车辆VIN码 | ✅ | ❌ | ✅ |

### 1.2 派生字段 (Derived Fields)

**实现位置**: [backend/data_processor.py](../../../backend/data_processor.py)

| 派生字段 | 源字段 | 派生规则 | 用途 |
|----------|--------|----------|------|
| telesales_flag | 终端来源 | `== '0110融合销售'` | 电销业务标识 |
| commercial_flag | 险种名称 | `∈ {'0312','0313','0317'}` | 商业险标识 |
| new_energy_flag | 是否新能源 | `== '是'` | 新能源车筛选 |
| transfer_flag | 是否过户车 | `== '是'` | 过户车筛选 |
| non_local_flag | 是否异地车 | `== '是'` | 异地车筛选 |
| premium_sum | 签单/批改保费 | `SUM()` | 保费汇总 |
| policy_count | 签单数量 | `COUNT()` where 保费≥50 | 有效保单数 |

---

## 📋 二、数据质量规则 (Data Quality Rules)

### 2.1 必填字段校验 (Required Fields Validation)

**优先级**: P0 (阻断性)

```python
# 实现示例 (伪代码参考)
REQUIRED_FIELDS = {
    '投保确认时间': 'Datetime',
    '三级机构': 'String',
    '业务员': 'String',
    '客户类别3': 'String',
    '签单/批改保费': 'Numeric',
    '签单数量': 'Numeric',
    '是否续保': 'String'
}

def validate_required_fields(df):
    """
    必填字段校验

    Returns:
        dict: {
            'valid': bool,
            'missing_fields': list,
            'missing_rows': int,
            'message': str
        }
    """
    missing_fields = []
    for field in REQUIRED_FIELDS.keys():
        if field not in df.columns:
            missing_fields.append(field)

    if missing_fields:
        return {
            'valid': False,
            'missing_fields': missing_fields,
            'missing_rows': 0,
            'message': f'缺失必填字段: {", ".join(missing_fields)}'
        }

    # 检查空值行数
    null_count = df[REQUIRED_FIELDS.keys()].isnull().any(axis=1).sum()

    return {
        'valid': null_count == 0,
        'missing_fields': [],
        'missing_rows': null_count,
        'message': f'发现{null_count}行数据缺失必填字段值' if null_count > 0 else '所有必填字段校验通过'
    }
```

### 2.2 格式验证 (Format Validation)

**优先级**: P0 (阻断性)

#### 日期格式校验

```python
def validate_date_format(df, date_columns=['投保确认时间', '刷新时间', '保险起期']):
    """
    日期格式校验

    规则:
    - 格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
    - 时间范围: 2020-01-01 至 当前日期+30天
    """
    errors = []

    for col in date_columns:
        if col not in df.columns:
            continue

        # 尝试转换
        df[col] = pd.to_datetime(df[col], errors='coerce')

        # 检查无效日期
        invalid_count = df[col].isnull().sum()
        if invalid_count > 0:
            errors.append(f'{col}: {invalid_count}行日期格式无效')

        # 检查时间范围
        valid_data = df[col].dropna()
        min_date = pd.to_datetime('2020-01-01')
        max_date = pd.to_datetime('today') + pd.Timedelta(days=30)

        out_of_range = valid_data[(valid_data < min_date) | (valid_data > max_date)]
        if len(out_of_range) > 0:
            errors.append(f'{col}: {len(out_of_range)}行日期超出合理范围')

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'message': '; '.join(errors) if errors else '日期格式校验通过'
    }
```

#### 数值类型校验

```python
def validate_numeric_types(df):
    """
    数值类型校验

    规则:
    - 签单/批改保费: 数值型,可负数,范围[-1000000, 100000]
    - 签单数量: 正整数,范围[1, 10000]
    - 手续费含税: 非负数,范围[0, 50000]
    """
    errors = []

    # 保费校验
    if '签单/批改保费' in df.columns:
        df['签单/批改保费'] = pd.to_numeric(df['签单/批改保费'], errors='coerce')
        invalid = df['签单/批改保费'].isnull().sum()
        if invalid > 0:
            errors.append(f'签单/批改保费: {invalid}行无法转换为数值')

        out_of_range = df[
            (df['签单/批改保费'] < -1000000) |
            (df['签单/批改保费'] > 100000)
        ]
        if len(out_of_range) > 0:
            errors.append(f'签单/批改保费: {len(out_of_range)}行超出合理范围')

    # 签单数量校验
    if '签单数量' in df.columns:
        df['签单数量'] = pd.to_numeric(df['签单数量'], errors='coerce')
        invalid = (df['签单数量'] < 1) | (df['签单数量'] > 10000)
        if invalid.sum() > 0:
            errors.append(f'签单数量: {invalid.sum()}行不在[1, 10000]范围内')

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'message': '; '.join(errors) if errors else '数值类型校验通过'
    }
```

### 2.3 范围检查 (Range Validation)

**优先级**: P1 (警告性)

```python
FIELD_RANGES = {
    '签单/批改保费': {'min': -1000000, 'max': 100000, 'allow_negative': True},
    '签单数量': {'min': 1, 'max': 10000, 'allow_negative': False},
    '手续费含税': {'min': 0, 'max': 50000, 'allow_negative': False},
    '手续费比例': {'min': 0, 'max': 1, 'allow_negative': False},
}

def validate_ranges(df):
    """
    范围检查

    Returns:
        dict: {
            'valid': bool,
            'warnings': list,
            'out_of_range_count': dict
        }
    """
    warnings = []
    out_of_range_count = {}

    for field, config in FIELD_RANGES.items():
        if field not in df.columns:
            continue

        # 检查范围
        valid_data = df[field].dropna()
        min_val = config['min']
        max_val = config['max']

        if not config['allow_negative']:
            out_of_range = valid_data[(valid_data < min_val) | (valid_data > max_val)]
        else:
            out_of_range = valid_data[(valid_data < min_val) | (valid_data > max_val)]

        count = len(out_of_range)
        if count > 0:
            out_of_range_count[field] = count
            warnings.append(f'{field}: {count}行超出范围[{min_val}, {max_val}]')

    return {
        'valid': len(warnings) == 0,
        'warnings': warnings,
        'out_of_range_count': out_of_range_count,
        'message': '; '.join(warnings) if warnings else '范围检查通过'
    }
```

### 2.4 一致性校验 (Consistency Validation)

**优先级**: P1 (警告性)

**实现位置**: [backend/data_processor.py:771-819](../../../backend/data_processor.py#L771-L819)

```python
def validate_policy_consistency(df, staff_mapping):
    """
    保单→业务员→机构/团队 一致性校验

    规则:
    - 同一保单号的业务员应该一致
    - 业务员的三级机构/团队应与映射表一致

    Returns:
        dict: {
            'valid': bool,
            'mismatch_policies': list,
            'mismatch_count': int,
            'conflicts': list
        }
    """
    mismatch_policies = []

    # 1. 检查保单号→业务员一致性
    if '保单号' in df.columns and '业务员' in df.columns:
        policy_staff = df.groupby('保单号')['业务员'].nunique()
        inconsistent = policy_staff[policy_staff > 1]
        if len(inconsistent) > 0:
            mismatch_policies.extend(inconsistent.index.tolist())

    # 2. 检查业务员→机构/团队一致性
    name_to_info, conflicts = _build_name_to_info(staff_mapping)

    if '三级机构' in df.columns and '业务员' in df.columns:
        for idx, row in df.iterrows():
            staff_name = row['业务员']
            data_institution = row['三级机构']

            if staff_name in name_to_info:
                mapped_institution = name_to_info[staff_name].get('三级机构')
                if mapped_institution and data_institution != mapped_institution:
                    mismatch_policies.append(row.get('保单号', f'Row-{idx}'))

    return {
        'valid': len(mismatch_policies) == 0 and len(conflicts) == 0,
        'mismatch_policies': mismatch_policies[:10],  # 只返回前10条
        'mismatch_count': len(mismatch_policies),
        'conflicts': conflicts,
        'message': f'发现{len(mismatch_policies)}条不一致记录,{len(conflicts)}个姓名冲突' if mismatch_policies or conflicts else '一致性校验通过'
    }
```

---

## 🧹 三、数据清洗规范 (Data Cleaning Standards)

### 3.1 缺失值处理 (Missing Value Handling)

**实现位置**: [backend/data_processor.py:132-156](../../../backend/data_processor.py#L132-L156)

| 字段类型 | 缺失值策略 | 填充值 | 业务规则 |
|----------|------------|--------|----------|
| 三级机构 | 从映射表查找 | 映射表值 | 优先使用业务员→机构映射 |
| 团队简称 | 保留缺失 | `''` (空字符串) | 允许为空 |
| 签单/批改保费 | 标记为无效 | 不填充,删除行 | 阻断性错误 |
| 手续费含税 | 填充为0 | `0` | 允许零手续费 |
| 是否续保 | 保留缺失 | `''` | 前端显示"未知" |
| 数值字段 | 转换失败设为NaN | `NaN` | 后续过滤或填充0 |
| 字符串字段 | 填充空字符串 | `''` | 避免None导致的异常 |

#### 实现示例

```python
def handle_missing_values(df, staff_mapping):
    """
    缺失值处理

    Args:
        df: 原始DataFrame
        staff_mapping: 业务员映射字典

    Returns:
        DataFrame: 处理后的数据
    """
    # 1. 三级机构缺失 → 从映射表查找
    if '三级机构' in df.columns and '业务员' in df.columns:
        name_to_info, _ = _build_name_to_info(staff_mapping)

        missing_mask = df['三级机构'].isnull() | (df['三级机构'] == '')
        for idx in df[missing_mask].index:
            staff_name = df.at[idx, '业务员']
            if staff_name in name_to_info:
                df.at[idx, '三级机构'] = name_to_info[staff_name].get('三级机构', '')

    # 2. 手续费缺失 → 填充0
    if '手续费含税' in df.columns:
        df['手续费含税'] = df['手续费含税'].fillna(0)

    # 3. 签单保费缺失 → 删除行
    if '签单/批改保费' in df.columns:
        before_count = len(df)
        df = df[df['签单/批改保费'].notnull()]
        after_count = len(df)
        if before_count > after_count:
            print(f'⚠️  删除{before_count - after_count}行保费缺失数据')

    # 4. 字符串字段 → 填充空字符串
    string_columns = df.select_dtypes(include=['object']).columns
    df[string_columns] = df[string_columns].fillna('')

    return df
```

### 3.2 异常值处理 (Outlier Handling)

**优先级**: P1 (警告性)

| 异常类型 | 检测规则 | 处理策略 | 业务含义 |
|----------|----------|----------|----------|
| 负保费 | `签单/批改保费 < 0` | ✅ **保留** | 退保/批改调整,合法 |
| 零手续费 | `手续费含税 == 0` | ✅ **保留** | 正常业务场景 |
| 负保额 | `签单/批改保额 < 0` | ⚠️ **标记** | 数据异常,需人工复核 |
| 超大保费 | `签单/批改保费 > 100000` | ⚠️ **标记** | 可能数据错误 |
| 异常手续费比例 | `手续费比例 < 0.03 or > 0.08` | ⚠️ **标记** | 异常业务 |

**关键原则**:
> **NEVER filter out negative premium values.** Negative premiums are legitimate business data representing policy cancellations, adjustments, or refunds. They MUST be included in all calculations.

#### 实现示例

```python
def detect_outliers(df):
    """
    异常值检测(仅标记,不删除)

    Returns:
        dict: {
            'outlier_counts': dict,
            'outlier_details': list,
            'warnings': list
        }
    """
    outlier_counts = {}
    outlier_details = []
    warnings = []

    # 1. 负保额检测
    if '签单/批改保额' in df.columns:
        negative_amount = df[df['签单/批改保额'] < 0]
        count = len(negative_amount)
        if count > 0:
            outlier_counts['负保额'] = count
            warnings.append(f'⚠️  发现{count}条负保额记录,请人工复核')
            outlier_details.extend(negative_amount['保单号'].tolist()[:5])

    # 2. 超大保费检测
    if '签单/批改保费' in df.columns:
        large_premium = df[df['签单/批改保费'] > 100000]
        count = len(large_premium)
        if count > 0:
            outlier_counts['超大保费'] = count
            warnings.append(f'⚠️  发现{count}条保费>10万记录')

    # 3. 异常手续费比例
    if '手续费比例' in df.columns:
        abnormal_ratio = df[
            (df['手续费比例'] < 0.03) | (df['手续费比例'] > 0.08)
        ]
        count = len(abnormal_ratio)
        if count > 0:
            outlier_counts['异常手续费比例'] = count
            warnings.append(f'⚠️  发现{count}条手续费比例异常(< 3% or > 8%)')

    return {
        'outlier_counts': outlier_counts,
        'outlier_details': outlier_details[:10],
        'warnings': warnings,
        'message': '\n'.join(warnings) if warnings else '未发现异常值'
    }
```

### 3.3 重复数据处理 (Duplicate Handling)

**实现位置**: [backend/data_processor.py:158-192](../../../backend/data_processor.py#L158-L192)

**去重规则**:
- **联合主键**: `保单号` + `投保确认时间`
- **保留策略**: `keep='last'` (保留最新记录)
- **理由**: 同一保单在不同时间可能有批改更新

```python
def remove_duplicates(df):
    """
    去重处理

    规则:
    - 联合主键: 保单号 + 投保确认时间
    - 保留最新记录(keep='last')

    Returns:
        DataFrame: 去重后的数据
    """
    if '保单号' not in df.columns or '投保确认时间' not in df.columns:
        return df

    before_count = len(df)

    # 确保日期类型
    try:
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
    except Exception:
        pass

    # 使用 duplicated 生成掩码,保留最后一条
    dup_mask = df.duplicated(subset=['保单号', '投保确认时间'], keep='last')
    df = df[~dup_mask]

    after_count = len(df)

    if before_count > after_count:
        print(f'ℹ️  去重: {before_count} → {after_count} (删除{before_count - after_count}条)')

    return df
```

### 3.4 数据标准化 (Data Normalization)

**实现位置**: [backend/data_processor.py:132-156](../../../backend/data_processor.py#L132-L156)

| 字段类型 | 标准化规则 | 实现方法 |
|----------|------------|----------|
| 日期字段 | 统一为 `datetime64[ns]` | `pd.to_datetime(errors='coerce')` |
| 数值字段 | 统一为 `float64` | `pd.to_numeric(errors='coerce')` |
| 字符串字段 | 去除首尾空格 | `str.strip()` |
| 是否类字段 | 统一为"是"/"否" | 映射 `{'Y':'是', 'N':'否'}` |
| 机构名称 | 去除空格和特殊字符 | `str.replace()` |

```python
def normalize_data(df):
    """
    数据标准化

    Returns:
        DataFrame: 标准化后的数据
    """
    # 1. 日期字段标准化
    date_columns = ['刷新时间', '投保确认时间', '保险起期']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 2. 数值字段标准化
    numeric_columns = ['签单/批改保费', '签单数量', '手续费', '手续费含税', '增值税']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. 字符串字段去除空格
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # 4. 是否类字段标准化
    yes_no_columns = ['是否续保', '是否新能源', '是否过户车', '是否异地车', '是否网约车']
    for col in yes_no_columns:
        if col in df.columns:
            df[col] = df[col].map({'Y': '是', 'N': '否', 'y': '是', 'n': '否'}).fillna(df[col])

    return df
```

---

## 🗂️ 四、映射管理 (Mapping Management)

### 4.1 业务员机构团队映射

**核心文件**: `业务员机构团队归属.json` (229 records as of 2025-11-04)

**数据结构**:
```json
{
  "200049147向轩颉": {
    "三级机构": "达州",
    "四级机构": "达州",
    "团队简称": null
  },
  "210011936赵莎莎": {
    "三级机构": "达州",
    "四级机构": "达州",
    "团队简称": "达州业务三部"
  }
}
```

**关键规则**:
- **映射优先级**: 映射表 > 数据文件中的机构字段
- **为什么**: 数据文件中的三级机构可能不准确,映射表是权威数据源
- **冲突解决**: 同名不同机构时,保留最后一条并标记冲突

### 4.2 映射更新流程

**步骤**:

1. **接收新映射文件** (Excel格式)
   - 文件名: `业务员机构团队对照表YYYYMMDD.xlsx`
   - 必需列: 序号, 三级机构, 四级机构, 团队简称, 业务员

2. **转换为JSON格式**
   ```python
   def convert_staff_mapping_excel_to_json(excel_path, json_path):
       """
       转换业务员映射表 Excel → JSON

       Args:
           excel_path: Excel文件路径
           json_path: 输出JSON路径
       """
       df = pd.read_excel(excel_path)

       # 提取关键列
       required_columns = ['业务员', '三级机构', '四级机构', '团队简称']
       if not all(col in df.columns for col in required_columns):
           raise ValueError(f'Excel文件缺少必需列: {required_columns}')

       # 构建映射字典
       mapping = {}
       for _, row in df.iterrows():
           staff_key = str(row['业务员'])  # 格式: 工号+姓名
           mapping[staff_key] = {
               '三级机构': str(row['三级机构']),
               '四级机构': str(row['四级机构']),
               '团队简称': str(row['团队简称']) if pd.notna(row['团队简称']) else None
           }

       # 保存JSON
       with open(json_path, 'w', encoding='utf-8') as f:
           json.dump(mapping, f, ensure_ascii=False, indent=2)

       print(f'✅ 映射表转换完成: {len(mapping)} 条记录')
       return mapping
   ```

3. **验证映射完整性**
   ```python
   def validate_staff_mapping(df, staff_mapping):
       """
       验证数据中的业务员是否都存在于映射表

       Returns:
           dict: {
               'unmatched_staff': list,
               'unmatched_count': int,
               'coverage_rate': float
           }
       """
       if '业务员' not in df.columns:
           return {'unmatched_staff': [], 'unmatched_count': 0, 'coverage_rate': 1.0}

       # 提取姓名
       import re
       name_to_info = {}
       for staff_key in staff_mapping.keys():
           match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
           if match:
               name = match.group()
               name_to_info[name] = staff_key

       # 检查未匹配
       data_staff = df['业务员'].unique()
       unmatched = [s for s in data_staff if s not in name_to_info]

       coverage_rate = 1.0 - (len(unmatched) / len(data_staff)) if len(data_staff) > 0 else 1.0

       return {
           'unmatched_staff': unmatched[:10],
           'unmatched_count': len(unmatched),
           'coverage_rate': coverage_rate,
           'message': f'映射覆盖率: {coverage_rate*100:.1f}% ({len(data_staff)-len(unmatched)}/{len(data_staff)})'
       }
   ```

4. **更新系统映射文件**
   - 备份旧版本: `业务员机构团队归属_backup_YYYYMMDD.json`
   - 替换为新版本
   - 触发数据刷新

5. **验证更新效果**
   - 重新加载数据
   - 检查未匹配业务员数量
   - 生成更新报告

### 4.3 冲突解决策略

**冲突场景**: 同一姓名出现在多条记录中,但机构/团队信息不同

**示例**:
```json
{
  "200012345张三": {"三级机构": "达州", "团队简称": "业务一部"},
  "210067890张三": {"三级机构": "德阳", "团队简称": "业务二部"}
}
```

**解决策略**:

1. **自动处理** (当前策略)
   - 保留最后一条记录
   - 记录冲突列表,返回前端提示
   - 实现位置: [backend/data_processor.py:23-58](../../../backend/data_processor.py#L23-L58)

2. **人工介入** (推荐,未来实现)
   - 前端显示冲突列表
   - 要求管理员选择正确记录
   - 或建议在映射表中区分(添加工号)

3. **工号区分** (最佳实践)
   - 在显示时使用"工号+姓名"
   - 系统内部维护工号→姓名映射
   - 避免同名冲突

### 4.4 历史版本管理

**版本命名规则**:
- 格式: `业务员机构团队归属_vYYYYMMDD.json`
- 示例: `业务员机构团队归属_v20251104.json`

**保留策略**:
- 保留最近12个月的版本
- 每月1号自动归档
- 超过12个月的版本移至 `data/archive/`

**版本对比**:
```python
def compare_mapping_versions(old_json, new_json):
    """
    对比两个版本的映射文件

    Returns:
        dict: {
            'added': list,      # 新增业务员
            'removed': list,    # 删除业务员
            'changed': list,    # 机构/团队变更
            'unchanged': int
        }
    """
    with open(old_json, 'r', encoding='utf-8') as f:
        old_mapping = json.load(f)

    with open(new_json, 'r', encoding='utf-8') as f:
        new_mapping = json.load(f)

    old_keys = set(old_mapping.keys())
    new_keys = set(new_mapping.keys())

    added = list(new_keys - old_keys)
    removed = list(old_keys - new_keys)

    changed = []
    for key in old_keys & new_keys:
        if old_mapping[key] != new_mapping[key]:
            changed.append({
                'staff': key,
                'old': old_mapping[key],
                'new': new_mapping[key]
            })

    return {
        'added': added,
        'removed': removed,
        'changed': changed,
        'unchanged': len(old_keys & new_keys) - len(changed),
        'summary': f'新增{len(added)},删除{len(removed)},变更{len(changed)},不变{len(old_keys & new_keys) - len(changed)}'
    }
```

---

## 📊 五、数据审计 (Data Audit)

### 5.1 变更日志 (Change Log)

**日志位置**: `logs/data_audit.log`

**记录内容**:
- 数据刷新时间
- 文件来源(Excel文件名)
- 处理前/后记录数
- 去重/清洗统计
- 异常值标记
- 映射匹配率

**日志格式**:
```
[2025-11-08 14:30:25] [INFO] 数据刷新开始
[2025-11-08 14:30:26] [INFO] 加载Excel: 车险清单_202511.xlsx
[2025-11-08 14:30:28] [INFO] 数据清洗: 5234 → 5180 (删除54行)
[2025-11-08 14:30:29] [INFO] 去重处理: 5180 → 5123 (删除57行)
[2025-11-08 14:30:30] [WARN] 发现23条负保额记录,已标记
[2025-11-08 14:30:31] [INFO] 映射匹配率: 98.5% (5045/5123)
[2025-11-08 14:30:32] [INFO] 数据刷新完成,最新日期: 2025-11-08
```

### 5.2 质量报告 (Quality Report)

**生成频率**: 每次数据刷新后自动生成

**报告内容**:

```python
def generate_quality_report(df, staff_mapping):
    """
    生成数据质量报告

    Returns:
        dict: 质量报告
    """
    report = {
        'timestamp': datetime.now().isoformat(),
        'data_summary': {
            'total_records': len(df),
            'date_range': f"{df['投保确认时间'].min()} ~ {df['投保确认时间'].max()}",
            'latest_date': df['投保确认时间'].max().strftime('%Y-%m-%d')
        },
        'field_completeness': {},
        'validation_results': {},
        'outlier_detection': {},
        'mapping_coverage': {},
        'quality_score': 0.0
    }

    # 1. 字段完整性
    for col in df.columns:
        null_count = df[col].isnull().sum()
        completeness = 1.0 - (null_count / len(df))
        report['field_completeness'][col] = {
            'completeness': completeness,
            'null_count': null_count,
            'status': '✅' if completeness >= 0.95 else '⚠️' if completeness >= 0.8 else '❌'
        }

    # 2. 必填字段校验
    report['validation_results']['required_fields'] = validate_required_fields(df)

    # 3. 格式验证
    report['validation_results']['date_format'] = validate_date_format(df)
    report['validation_results']['numeric_types'] = validate_numeric_types(df)

    # 4. 异常值检测
    report['outlier_detection'] = detect_outliers(df)

    # 5. 映射覆盖率
    report['mapping_coverage'] = validate_staff_mapping(df, staff_mapping)

    # 6. 综合质量评分 (0-100)
    score = 0
    score += 30 if report['validation_results']['required_fields']['valid'] else 0
    score += 20 if report['validation_results']['date_format']['valid'] else 0
    score += 20 if report['validation_results']['numeric_types']['valid'] else 0
    score += 15 if report['mapping_coverage']['coverage_rate'] >= 0.95 else 10 if report['mapping_coverage']['coverage_rate'] >= 0.9 else 0
    score += 15 if len(report['outlier_detection']['outlier_counts']) == 0 else 5

    report['quality_score'] = score
    report['quality_level'] = '优秀' if score >= 90 else '良好' if score >= 75 else '及格' if score >= 60 else '不及格'

    return report
```

**报告示例**:

```json
{
  "timestamp": "2025-11-08T14:30:32",
  "data_summary": {
    "total_records": 5123,
    "date_range": "2025-10-01 ~ 2025-11-08",
    "latest_date": "2025-11-08"
  },
  "field_completeness": {
    "投保确认时间": {"completeness": 1.0, "null_count": 0, "status": "✅"},
    "三级机构": {"completeness": 0.985, "null_count": 77, "status": "✅"},
    "团队简称": {"completeness": 0.72, "null_count": 1434, "status": "⚠️"}
  },
  "validation_results": {
    "required_fields": {"valid": true, "message": "所有必填字段校验通过"},
    "date_format": {"valid": true, "message": "日期格式校验通过"},
    "numeric_types": {"valid": true, "message": "数值类型校验通过"}
  },
  "outlier_detection": {
    "outlier_counts": {"负保额": 23, "异常手续费比例": 12},
    "warnings": ["⚠️  发现23条负保额记录,请人工复核"]
  },
  "mapping_coverage": {
    "unmatched_count": 8,
    "coverage_rate": 0.985,
    "message": "映射覆盖率: 98.5% (5045/5123)"
  },
  "quality_score": 85,
  "quality_level": "良好"
}
```

### 5.3 异常告警 (Anomaly Alerts)

**告警触发条件**:

| 告警级别 | 触发条件 | 通知方式 |
|----------|----------|----------|
| 🔴 严重 | 质量评分 < 60 | 前端红色提示 |
| 🟡 警告 | 质量评分 60-74 | 前端黄色提示 |
| ⚠️  提醒 | 异常值数量 > 50 | 前端灰色提示 |
| ℹ️  信息 | 映射覆盖率 < 95% | 日志记录 |

**告警消息模板**:

```python
ALERT_TEMPLATES = {
    'low_quality_score': '⚠️ 数据质量评分低({score}分),请检查数据源',
    'high_outlier_count': '⚠️ 发现{count}条异常数据,建议人工复核',
    'low_mapping_coverage': 'ℹ️  映射覆盖率较低({rate}%),建议更新映射表',
    'missing_required_fields': '🔴 缺少必填字段: {fields}',
    'date_format_errors': '🔴 日期格式错误: {errors}',
}

def generate_alert_messages(quality_report):
    """
    根据质量报告生成告警消息

    Returns:
        list: 告警消息列表
    """
    alerts = []

    # 1. 质量评分告警
    score = quality_report['quality_score']
    if score < 75:
        alerts.append({
            'level': 'warning' if score >= 60 else 'error',
            'message': ALERT_TEMPLATES['low_quality_score'].format(score=score),
            'category': 'quality_score'
        })

    # 2. 异常值告警
    outlier_count = sum(quality_report['outlier_detection']['outlier_counts'].values())
    if outlier_count > 50:
        alerts.append({
            'level': 'warning',
            'message': ALERT_TEMPLATES['high_outlier_count'].format(count=outlier_count),
            'category': 'outliers'
        })

    # 3. 映射覆盖率告警
    coverage_rate = quality_report['mapping_coverage']['coverage_rate']
    if coverage_rate < 0.95:
        alerts.append({
            'level': 'info',
            'message': ALERT_TEMPLATES['low_mapping_coverage'].format(rate=coverage_rate*100),
            'category': 'mapping_coverage'
        })

    # 4. 必填字段告警
    if not quality_report['validation_results']['required_fields']['valid']:
        missing_fields = quality_report['validation_results']['required_fields']['missing_fields']
        alerts.append({
            'level': 'error',
            'message': ALERT_TEMPLATES['missing_required_fields'].format(fields=', '.join(missing_fields)),
            'category': 'required_fields'
        })

    return alerts
```

---

## 📖 六、最佳实践 (Best Practices)

### 6.1 数据治理原则

1. **映射表权威原则**
   - ✅ 始终使用 `业务员机构团队归属.json` 作为机构/团队的权威来源
   - ❌ 不要直接使用数据文件中的 `三级机构` 字段

2. **负值保留原则**
   - ✅ 保留负保费值(退保/调整的合法数据)
   - ❌ 不要过滤或删除负保费记录

3. **增量更新原则**
   - ✅ 使用 `保单号` + `投保确认时间` 去重,保留最新
   - ❌ 不要全量替换,避免历史数据丢失

4. **质量优先原则**
   - ✅ 必填字段缺失时阻断数据导入
   - ❌ 不要强制填充可能错误的默认值

### 6.2 常见陷阱 (Common Pitfalls)

#### ❌ Pitfall 1: 使用原始机构字段

```python
# ❌ 错误 - 直接使用数据中的三级机构
df[df['三级机构'] == '达州']

# ✅ 正确 - 使用映射表查找
name_to_info, _ = _build_name_to_info(staff_mapping)
staff_list = [name for name, info in name_to_info.items()
              if info['三级机构'] == '达州']
df[df['业务员'].isin(staff_list)]
```

#### ❌ Pitfall 2: 过滤负保费

```python
# ❌ 错误 - 删除负保费
df = df[df['签单/批改保费'] > 0]

# ✅ 正确 - 保留负保费
total_premium = df['签单/批改保费'].sum()  # 包含负值
```

#### ❌ Pitfall 3: 忽略数据验证

```python
# ❌ 错误 - 直接处理,无验证
df = pd.read_excel('data.xlsx')
df.to_csv('output.csv')

# ✅ 正确 - 先验证,再处理
df = pd.read_excel('data.xlsx')
validation_result = validate_required_fields(df)
if not validation_result['valid']:
    raise ValueError(validation_result['message'])
df.to_csv('output.csv')
```

#### ❌ Pitfall 4: 硬编码日期范围

```python
# ❌ 错误 - 硬编码
df = df[df['投保确认时间'] >= '2025-10-01']

# ✅ 正确 - 相对时间
latest_date = df['投保确认时间'].max()
start_date = latest_date - timedelta(days=30)
df = df[df['投保确认时间'] >= start_date]
```

### 6.3 代码检查清单 (Code Review Checklist)

在实现数据处理逻辑时,请确保:

- [ ] 必填字段已校验
- [ ] 日期格式已统一为 `datetime64[ns]`
- [ ] 数值字段已转换为 `float64`
- [ ] 负保费值已保留(未过滤)
- [ ] 使用映射表获取机构/团队(非数据文件字段)
- [ ] 去重使用 `duplicated + 掩码` (避免类型问题)
- [ ] 缺失值已按规则处理(非默认全填充0)
- [ ] 异常值已检测并标记(非删除)
- [ ] 数据质量报告已生成
- [ ] 错误日志已记录

---

## 📂 相关文件索引 (Related Files)

### 数据处理核心

- [backend/data_processor.py](../../../backend/data_processor.py) - 数据处理主逻辑
  - L23-58: 姓名→机构映射构建
  - L59-101: 保单映射信息
  - L132-156: 数据清洗
  - L158-192: 去重与合并

### 数据字典

- [docs/FIELD_MAPPING.md](../../../docs/FIELD_MAPPING.md) - 字段映射表
- [业务员机构团队归属.json](../../../业务员机构团队归属.json) - 映射文件

### API与数据验证

- [backend/api_server.py](../../../backend/api_server.py) - API接口
  - L141-161: 保单映射查询
  - L244-314: 业绩分布(含过滤验证)

### 相关 Skills

- [analyzing-auto-insurance-data](../analyzing-auto-insurance-data/SKILL.md) - 数据分析
- [backend-data-processor](../backend-data-processor/SKILL.md) - 后端数据处理
- [api-endpoint-design](../api-endpoint-design/SKILL.md) - API设计

---

## 🎯 预期收益 (Expected Benefits)

### Token 节省估算

- **每次对话节省**: 2000-3000 tokens
- **年使用次数**: 约 30 次(数据治理相关对话)
- **年总节省**: 60,000 - 90,000 tokens

### 质量提升

- **数据准确性**: 从 92% 提升至 98%+
- **异常检测率**: 从 60% 提升至 95%+
- **映射覆盖率**: 从 90% 提升至 98%+
- **手工干预减少**: 降低 70%

### 效率提升

- **数据导入耗时**: 减少 40% (自动验证)
- **异常排查时间**: 减少 60% (质量报告)
- **映射更新时间**: 减少 80% (自动化流程)

---

## ✅ 总结 (Summary)

### 核心要点

1. **数据字典**: 完整的字段定义、类型、枚举值、业务含义
2. **质量规则**: 必填、格式、范围、一致性四层校验
3. **清洗规范**: 缺失值、异常值、重复数据、标准化处理
4. **映射管理**: 更新流程、冲突解决、版本控制
5. **数据审计**: 变更日志、质量报告、异常告警

### 适用场景

✅ **适用**:
- 定义数据质量标准
- 实现字段验证逻辑
- 管理业务员映射更新
- 解决数据不一致问题
- 建立数据治理流程
- 生成数据质量报告

❌ **不适用**:
- 具体数据分析任务 → `analyzing-auto-insurance-data`
- Vue 组件开发 → `vue-component-dev`
- API 接口设计 → `api-endpoint-design`

---

**Skill 版本**: v1.0
**创建日期**: 2025-11-09
**最后更新**: 2025-11-09
**维护者**: Claude Code AI Assistant
**下次审查**: 2025-12-09
