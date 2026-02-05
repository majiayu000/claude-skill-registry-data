---
name: table-config
description: 表字段配置规范。建表后配置 ts 文件时使用。
---

# 表配置规范

## 默认值（无需配置）

| 字段/类型 | 默认行为 |
|-----------|----------|
| `lbl` | width/align/require/search 已有默认 |
| `*_id`/`*_ids` | foreignKey 自动推断 |
| 数字类型 | align:right, width:100 |
| date/datetime | width:160 |
| decimal | width:100 |
| rem | width:280 |
| `*_province_code` | 自动识别省份 |
| `isFluentEditor` | noList 默认 true |

## 需要配置的情况

### 外键数据量大

```typescript
{
  COLUMN_NAME: "usr_id",
  foreignKey: {
    selectType: "selectInput",  // 弹框选择
  },
  search: true,
  isSearchByLbl: true,  // 按标签搜索
}
```

### 聚合关系

```typescript
ec_order: {
  opts: {
    inlineForeignTabs: [{
      mod: "ec",
      table: "order_detail",
      label: "订单明细",
      column: "order_id",
    }],
    detailCustomDialogType: "medium",  // 字段多时用
    detailFormCols: 3,  // 表单列数
  }
}
```

## 审计字段

大部分表需要：
```typescript
{ COLUMN_NAME: "create_usr_id" },
{ COLUMN_NAME: "create_time" },
{ COLUMN_NAME: "update_usr_id" },
{ COLUMN_NAME: "update_time" },
```
