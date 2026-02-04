---
name: dict
description: 系统字典和业务字典配置。建表需要枚举字段或给表添加枚举类字段时使用
---

# 字典配置

## 字段声明

```sql
-- 系统字典
`is_locked` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '锁定,dict:is_locked',
-- 业务字典, 字典编码格式: {mod}_{table}_{column}
`status` varchar(20) NOT NULL DEFAULT '' COMMENT '状态,dictbiz:ec_order_status',
```

## 添加字典

### 1. 创建 CSV 文件

```
src/tables/{mod}/
├── base_dict.{mod}.sql.csv        # 系统字典
├── base_dict_detail.{mod}.sql.csv # 系统字典明细
├── base_dictbiz.{mod}.sql.csv     # 业务字典
├── base_dictbiz_detail.{mod}.sql.csv # 业务字典明细
```

#### `base_dictbiz.{mod}.sql.csv` 中:
- `id` 使用 `nr uuid` 生成唯一 ID
- `lbl` 为: `{table_comment}-{column_comment}`, 例: `订单-状态`
- `type` 一般为: `string`, 或 `number`
- `tenant_id` 固定为: `ZDbZlC1OT8KaDg6soxMCBQ` (默认租户)
- `is_sys` 一般为: `1` 代表是否 `系统记录`, 系统记录禁止用户修改/删除
- `is_add` 一般为: `0` 代表是否允许用户新增字典明细
- `order_by` 从1开始依次递增
- 例如:
```csv
id,code,lbl,type,order_by,tenant_id,is_sys,is_add
l4V3aK5XRCOqSWsc/59GEw,exh_booking_order_state,订单-状态,string,1,ZDbZlC1OT8KaDg6soxMCBQ,1,0
```

#### `base_dictbiz_detail.{mod}.sql.csv` 中:
- `id` 使用 `nr uuid` 生成唯一 ID
- `dictbiz_id` 为业务字典 ID, 对应 `base_dictbiz.{mod}.sql.csv` 中对应业务字典的 ID
- `_dictbiz_lbl` 为业务字典标签, 对应 `base_dictbiz.{mod}.sql.csv` 中对应业务字典的 `lbl` 字段
- `lbl` 字段为字典明细标签
- `val` 字段为字典明细值
- `order_by` 此业务字典从1开始依次递增
- `tenant_id` 固定为: `ZDbZlC1OT8KaDg6soxMCBQ` (默认租户)
- `is_sys` 一般为: `1` 代表是否 `系统记录`, 系统记录禁止用户修改/删除
- 多个字典明细之间可以留空行, 方便阅读
- 例如:
```csv
id,dictbiz_id,_dictbiz_lbl,lbl,val,order_by,tenant_id,is_sys
QudgQBmlTtGBastzn2jpwA,l4V3aK5XRCOqSWsc/59GEw,订单-状态,未支付,unpaid,1,ZDbZlC1OT8KaDg6soxMCBQ,1
23GjMKTwRKeUvIZvTCwHSg,l4V3aK5XRCOqSWsc/59GEw,,已支付,paid,2,ZDbZlC1OT8KaDg6soxMCBQ,1
```

### 2. 生成 UUID

```bash
nr uuid      # 生成1个
nr uuid -- 3 # 生成3个
```

### 3. 导入业务字典

```bash
nr importCsv {mod}/base_dictbiz.{mod}.sql.csv
```

## 内置系统字典

| 编码 | 用途 |
|------|------|
| is_deleted | 删除标记 |
| is_locked | 锁定 |
| is_enabled | 启用 |
| is_default | 默认 |
| yes_no | 是否 |

## is_sys 字段

```sql
`is_sys` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '系统记录,dict:is_sys',
```

`is_sys=1` 时：
- 自动生成枚举类型
- 禁止用户修改/删除
