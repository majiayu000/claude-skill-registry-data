---
name: dw-etl
description: 数仓 ETL 开发流程，适用于生成 ODPS/MaxCompute 建表 DDL、INSERT SQL 和 SR 建表语句，并配合 hooks 自动校验 SQL 规范。直接调用命令：/dw-etl。
---

# Step 3: ETL 开发

## 执行流程

1. 根据技术设计生成建表 DDL
2. 生成 Insert SQL
3. 生成 SR 建表语句（如需）
4. PostToolUse hook 自动触发 SQL 规范检查

## 产出文件

| 文件名 | 用途 |
|--------|------|
| `ddl_[表名].sql` | ODPS 建表语句 |
| `insert_[表名].sql` | Insert SQL |
| `ddl_sr_[表名].sql` | SR 建表语句 |

## 强制规范

- INSERT 用 OVERWRITE 模式
- PARTITION 子句必须包含 partition_dt
- 金额字段类型 DECIMAL(20,4)
- 禁止 SELECT *
- 金额字段单位继承上游（如千元），不做转换
- 注释三段式：业务含义 + 数据来源 + 计算逻辑

## DDL 模板

```sql
CREATE TABLE IF NOT EXISTS [表名] (
    [字段名] [类型] COMMENT '[业务含义|数据来源|计算逻辑]',
    ...
    partition_dt STRING COMMENT '分区日期|系统生成|yyyyMMdd格式'
)
PARTITIONED BY (partition_dt STRING)
COMMENT '[表注释]'
LIFECYCLE [天数];
```

## Insert 模板

```sql
INSERT OVERWRITE TABLE [表名] PARTITION (partition_dt = '[日期]')
SELECT
    [字段列表]
FROM [来源表]
WHERE partition_dt = '[日期]'
[AND 其他条件];
```

## 自动护栏

写入 .sql 文件后，PostToolUse hook 自动检查：
- 发现 SELECT * → exit 2 阻断
- 缺少 PARTITION → exit 2 阻断
- 金额字段用 DOUBLE → exit 2 阻断
- Claude 收到 stderr 错误信息后自动修正
