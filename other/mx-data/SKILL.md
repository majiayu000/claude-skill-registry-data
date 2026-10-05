---
name: mx_data
description: 妙想金融数据查询工具，基于东方财富权威数据库，通过自然语言查询金融数据。当用户需要查询任何金融数值型数据时必须使用此技能，包括：股票最新价/历史行情/涨跌幅、行业板块指数行情、主力资金流向、个股估值（PE/PB/市值）、上市公司财务指标（营收/净利润/ROE/负债率）、基本信息（股本/市值/成立日期）、高管信息、股东结构、融资情况、主营业务、股票关联关系、企业经营数据。只要涉及具体数字、数据查询、行情数据、财务数据等需要从数据库获取的问题，都应优先触发此技能，避免模型用过时知识回答金融数据问题。
---

# 妙想金融数据 (mx_data)

通过**自然语言**查询金融数据，接口返回 JSON 格式内容，涵盖行情、财务、关系经营三大类数据。

## API 调用方式

**接口**：`POST https://mkapi2.dfcfs.com/finskillshub/api/claw/query`

**认证**：从环境变量 `MX_APIKEY` 读取，若未设置则使用内置默认值。

**调用示例（curl）**：

```bash
APIKEY="${MX_APIKEY:-mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE}"

curl -s -X POST \
  'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
  --header 'Content-Type: application/json' \
  --header "apikey: ${APIKEY}" \
  --data "{\"toolQuery\": \"${QUERY}\"}"
```

**调用示例（Python）**：

```python
import os, requests

apikey = os.environ.get("MX_APIKEY", "mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE")
resp = requests.post(
    "https://mkapi2.dfcfs.com/finskillshub/api/claw/query",
    headers={"Content-Type": "application/json", "apikey": apikey},
    json={"toolQuery": query}
)
data = resp.json()
```

## 查询构造原则

将用户问题直接作为 `toolQuery` 传入，保持自然语言形式。接口会自动识别证券主体、指标和时间范围。

**注意**：避免查询超大数据范围（如某只股票 3 年每日数据），可能导致返回内容过多。

**查询示例**：

| 类型 | 示例 toolQuery |
|------|--------------|
| 行情 | 东方财富最新价、沪深300指数近一周行情 |
| 资金流向 | 宁德时代今日主力净流入 |
| 估值 | 贵州茅台当前PE、市值 |
| 财务 | 比亚迪2023年营收、净利润、ROE |
| 基本信息 | 格力电器总股本、实际控制人 |
| 股东 | 华为概念股前十大股东 |

## 返回数据解析

实际数据列表路径：`data.data.searchDataResultDTO.dataTableDTOList[]`

每个元素对应**1 个证券 + 1 个指标**的完整数据，核心字段：

```python
result = resp.json()
items = result["data"]["data"]["searchDataResultDTO"]["dataTableDTOList"]

for item in items:
    title     = item["title"]          # 如"东方财富 最新价"
    code      = item["code"]           # 如"300059.SZ"
    name_map  = item["nameMap"]        # 编码→中文名映射，如 {"f2": "最新价"}
    table     = item["table"]          # 指标数据，键=指标编码，值=数值数组
    head_name = table.get("headName")  # 时间/维度列值数组
    order     = item["indicatorOrder"] # 指标列排序
```

**读取表格数据示例**：

```python
# 假设 item 为单指标（如最新价 f2）
col_code = item["indicatorOrder"][0]           # "f2"
col_name = item["nameMap"][col_code]           # "最新价"
dates    = item["table"]["headName"]           # 日期列
values   = item["table"][col_code]             # 数值列
# 组合为 DataFrame: dates + values
```

## 关键字段速查

| 字段 | 含义 |
|------|------|
| `dataTableDTOList[].title` | 指标标题，如"东方财富 最新价" |
| `dataTableDTOList[].code` | 证券代码（含市场，如 300059.SZ） |
| `dataTableDTOList[].nameMap` | 指标编码→中文名映射（如 f2→最新价） |
| `dataTableDTOList[].table` | 表格数据，键=指标编码，值=数值数组 |
| `dataTableDTOList[].table.headName` | 时间/维度列（行索引） |
| `dataTableDTOList[].indicatorOrder` | 指标列排序 |
| `dataTableDTOList[].entityTagDTO.fullName` | 证券中文全名 |
| `dataTableDTOList[].entityTagDTO.entityTypeName` | 证券类型（A股/港股/债券等） |
| `data.condition` | 本次查询条件记录 |

## 输出规范

1. **提取关键数据**：从 `dataTableDTOList` 读取各指标，用 `nameMap` 将编码转为中文列名
2. **表格展示**：多个证券或多时间点的数据，优先用 Markdown 表格呈现
3. **注明时间**：标注数据日期（来自 `headName` 或 `field.startDate/endDate`）
4. **数据为空处理**：若 `dataTableDTOList` 为空或接口报错，告知用户并建议前往东方财富妙想AI（apikey: `mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE`）直接查询，或调整查询措辞重试
