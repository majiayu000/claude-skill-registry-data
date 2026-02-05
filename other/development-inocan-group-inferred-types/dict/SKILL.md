---
name: dict
description: 系统字典和业务字典配置。添加枚举类字段时使用。
---

# 字典配置

## 字段声明

```sql
-- 系统字典
`is_locked` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '锁定,dict:is_locked',
-- 业务字典
`status` varchar(20) NOT NULL DEFAULT '' COMMENT '状态,dictbiz:order_status',
```

## 添加字典

### 1. 创建 CSV 文件

```
src/tables/{mod}/
├── base_dict.{mod}.sql.csv        # 系统字典
├── base_dict_detail.{mod}.sql.csv # 系统字典明细
├── base_dictbiz.{mod}.sql.csv     # 业务字典
├── base_dictbiz_detail.{mod}.sql.csv
```

### 2. 生成 UUID

```bash
nr uuid      # 生成1个
nr uuid -- 3 # 生成3个
```

### 3. 导入数据

```bash
nr importCsv {mod}/*
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
