---
name: create-table
description: 将已有 SQL 接入到数据栈的某一层（ODS/DIM/DWD/ADS）。当用户需要添加新表、接入数据源、配置数据层时使用。支持配置 sources、table_dependencies、创建 migration 文件。
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Create Table Skill

帮助您将已有的 SQL 接入到 The Nomad Data Stack 的某一层。

## 项目架构

本项目使用 **Airflow + DuckDB + MinIO** 架构：
- 数据分层：`raw` → `ods` → `dwd` → `dim` → `ads`
- 存储格式：Parquet + Hive 分区（dt=YYYY-MM-DD）
- 查询引擎：DuckDB 视图
- 调度：Apache Airflow

## ⚠️ 表命名规范（必须遵守）

**所有表名必须使用以下后缀之一**，以确保数据栈的一致性和可维护性：

| 后缀 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `_full` | 全量快照表 | 每次全量覆盖，存储当前完整数据快照 | `dim_etf_universe_whitelist_full` |
| `_inc` | 增量表 | 仅存储增量变更数据 | `dwd_stock_price_inc` |
| `_zip` | 拉链表 | 记录数据历史状态变化，支持时间旅行 | `dim_customer_zip` |

**命名规则**：
- 格式：`{layer}_{业务描述}_{类型后缀}`
- 示例：
  - ✅ `dim_trade_calendar_full` （DIM 层交易日历全量表）
  - ✅ `dwd_order_detail_inc` （DWD 层订单明细增量表）
  - ✅ `dim_customer_zip` （DIM 层客户拉链表）
  - ❌ `dim_trade_calendar` （缺少类型后缀）

**类型选择指南**：
- 使用 `_full`：数据需要每日全量快照，或者数据量不大且需要查询当前全量
- 使用 `_inc`：数据量大，只需要存储增量变更（通常配合流式处理）
- 使用 `_zip`：需要追踪历史状态变化，支持任意时间点查询

## 两种接入场景

### 场景 A：接入到 ODS 层

**前提**：数据已经在 `lake/raw/daily/{target}` 目录（CSV 格式）

#### 步骤 1：配置数据源

在 `dags/dw_config.yaml` 添加配置：

```yaml
sources:
  ods_{table_name}:
    path: "lake/raw/daily/{target}"
    format: "csv"
```

#### 步骤 2：创建 SQL 文件

在 `dags/ods/` 目录创建 `ods_{target}.sql`：

```sql
SELECT
  field1,
  field2,
  CAST(STRPTIME(CAST(date_field AS VARCHAR), '%Y%m%d') AS DATE) AS trade_date,
  '${PARTITION_DATE}' AS dt
FROM tmp_ods_{target};
```

**关键点**：
- 文件名必须包含 `ods_` 前缀（例如 `ods_fund_etf_spot.sql`）
- 从 `tmp_ods_{target}` 读取（Airflow 自动创建的临时表）
- 进行字段类型转换
- 添加 `${PARTITION_DATE}` 作为分区列

#### 步骤 3：创建 Migration 文件

在 `catalog/migrations/` 创建 `{number}_ods_{target}_table.sql`

参考示例中的 Migration 文件格式，包含：
- Schema 定义宏
- Seed parquet 初始化
- DuckDB 视图定义
- 分区查询宏

#### 步骤 4：完成

- Airflow 会自动识别新文件
- 运行 `dw_ods` DAG 即可

---

### 场景 B：接入到 DIM/DWD/ADS 层

**前提**：SQL 查询语句已准备好

#### 步骤 1：分析同层依赖

检查 SQL 是否依赖同层的其他表。

**示例**：如果 SQL 中使用了 `dim.other_table`，则需要配置同层依赖。

#### 步骤 2：创建 SQL 文件

在 `dags/{layer}/` 目录创建 `{layer}_{table_name}_{type}.sql`

**⚠️ 重要**：表名必须包含类型后缀（`_full`、`_inc` 或 `_zip`）

```sql
SELECT
  field1,
  field2,
  '${PARTITION_DATE}' AS dt
FROM ods.ods_source_table;
```

**关键点**：
- 使用标准 SQL 从下层读取
- 添加 `${PARTITION_DATE}` 作为分区列
- SQL 中使用的表即为依赖
- **表名格式**：`{layer}_{业务描述}_{类型后缀}`

#### 步骤 3：配置同层依赖

在 `dags/dw_config.yaml` 添加配置：

```yaml
table_dependencies:
  {layer}:
    {table_name}: [dependency_table1, dependency_table2]
```

**示例**：
```yaml
table_dependencies:
  dim:
    dim_trade_calendar_full: [dim_other_table_full]
```

**如果没有同层依赖**，可以省略此步骤。

#### 步骤 4：创建 Migration 文件

在 `catalog/migrations/` 创建 `{number}_{table_name}_table.sql`

参考示例中的 Migration 文件格式，包含：
- Schema 定义宏
- Seed parquet 初始化
- DuckDB 视图定义
- 分区查询宏

#### 步骤 5：完成

- 跨层依赖由框架自动处理
- 运行对应的 `dw_{layer}` DAG

---

## 快速参考

### 文件位置

| 层级 | SQL 文件位置 | Migration 位置 |
|------|-------------|----------------|
| ODS  | `dags/ods/ods_{target}.sql` | `catalog/migrations/00XX_ods_{target}_table.sql` |
| DIM  | `dags/dim/dim_{table}_{type}.sql` | `catalog/migrations/00XX_dim_{table}_{type}_table.sql` |
| DWD  | `dags/dwd/dwd_{table}_{type}.sql` | `catalog/migrations/00XX_dwd_{table}_{type}_table.sql` |
| ADS  | `dags/ads/ads_{table}_{type}.sql` | `catalog/migrations/00XX_ads_{table}_{type}_table.sql` |

**注意**：`{type}` 是 `_full`、`_inc` 或 `_zip`，ODS 层除外。

### 配置文件

**`dags/dw_config.yaml`**：

```yaml
# ODS 数据源配置
sources:
  ods_fund_etf_spot:
    path: "lake/raw/daily/fund_etf_spot"
    format: "csv"

# 同层依赖配置（仅用于有同层依赖的情况）
table_dependencies:
  dim:
    dim_table_a_full: [dim_table_b_full]
  dwd:
    dwd_table_x_inc: [dwd_table_y_inc]
```

### Migration 命名规则

- 查找现有 migration：`ls catalog/migrations/`
- 使用下一个编号：如现有 `0006_*.sql`，新文件用 `0007_*.sql`
- 格式：`00XX_{table_name}_table.sql`

---

## 常见问题

### Q: 如何确定表应该使用什么类型后缀？
A:
- **`_full`**：每日全量快照，适合数据量不大或需要查询当前全量的场景（如维度表、配置表）
- **`_inc`**：仅存储增量数据，适合大数据量且只需要变更记录的场景（如日志、交易流水）
- **`_zip`**：需要追踪历史状态变化，支持任意时间点查询（如客户信息、账户状态）

### Q: 如何确定同层依赖？
A: 检查 SQL 中 `FROM` 或 `JOIN` 的表。如果引用了同层的表（如 `dim.xxx`），就是同层依赖。

### Q: 跨层依赖需要配置吗？
A: 不需要。框架通过 `layer_dependencies` 自动处理跨层依赖。

### Q: SQL 中必须有 `${PARTITION_DATE}` 吗？
A: 是的。所有表都是分区表，必须添加分区列。

### Q: 如果表名没有类型后缀会怎样？
A: 这会破坏数据栈的命名一致性，导致：
- 无法清晰识别表的更新策略
- 可能与全量/增量/拉链表混淆
- **必须在创建表时指定正确的类型后缀**

### Q: 如何测试新接入的表？
A:
1. 运行对应的 DAG
2. 查询验证：`SELECT * FROM {layer}.{table_name} LIMIT 10`

---

## 示例

查看完整示例：
- **ODS 接入完整流程**：`examples/ods_integration.md`
- **DIM 接入完整流程**：`examples/dim_integration.md`

**快速参考**：
- 命令速查、SQL 函数、数据类型等：`REFERENCE.md`

---

## 开始使用

告诉我：
1. 您要接入哪一层？（ODS/DIM/DWD/ADS）
2. SQL 是什么？（或者描述数据来源）
3. 有什么依赖关系？
4. **表类型是什么？**（全量 `_full` / 增量 `_inc` / 拉链 `_zip`）

我会引导您完成接入流程。
