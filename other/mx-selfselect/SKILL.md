---
name: mx_selfselect
description: 妙想自选股管理工具，基于东方财富通行证账户数据，管理个人自选股列表。当用户提到自选股相关操作时必须使用此技能，包括：查询我的自选股列表、查看自选股行情、添加股票到自选股、把某只股票加入自选、从自选股中删除/移除某只股票。只要涉及"自选股"、"我的股票列表"、"加自选"、"删自选"等个人股票收藏管理操作，都应触发此技能。
---

# 妙想自选股管理 (mx_selfselect)

通过**自然语言**查询或操作东方财富通行证账户下的自选股，支持查询、添加、删除三种操作。

## API 说明

**认证**：从环境变量 `MX_APIKEY` 读取，若未设置则使用内置默认值。

### 接口一：查询自选股列表

**接口**：`POST https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get`（无请求体）

```bash
APIKEY="${MX_APIKEY:-mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE}"

curl -s -X POST \
  'https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get' \
  --header 'Content-Type: application/json' \
  --header "apikey: ${APIKEY}"
```

### 接口二：添加或删除自选股

**接口**：`POST https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage`

```bash
APIKEY="${MX_APIKEY:-mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE}"

curl -s -X POST \
  'https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage' \
  --header 'Content-Type: application/json' \
  --header "apikey: ${APIKEY}" \
  --data "{\"query\": \"${USER_QUERY}\"}"
```

## 问句示例

| 操作 | query 示例 |
|------|-----------|
| 查询 | （无需 query，调用 get 接口即可） |
| 添加 | 把贵州茅台添加到我的自选股列表 |
| 删除 | 把贵州茅台从我的自选股列表删除 |

## 操作路由规则

根据用户意图选择接口：

- 用户想**查看/列出**自选股 → 调用 `/get` 接口（无请求体）
- 用户想**添加**某只股票 → 调用 `/manage` 接口，query 填写添加指令
- 用户想**删除/移除**某只股票 → 调用 `/manage` 接口，query 填写删除指令

## 返回数据解析

### 查询接口返回

```python
result = resp.json()
# 数据路径
inner = result["data"]["allResults"]["result"]
columns  = inner["columns"]   # 列定义（title, key, unit 等）
datalist = inner["dataList"]  # 自选股数据行

# 构建列名映射
col_map = {col["key"]: col["title"] for col in columns}
```

**`dataList[]` 核心字段**：

| 键 | 含义 |
|----|------|
| `SECURITY_CODE` | 股票代码 |
| `SECURITY_SHORT_NAME` | 股票简称 |
| `MARKET_SHORT_NAME` | 市场（SH/SZ） |
| `NEWEST_PRICE` | 最新价（元） |
| `CHG` | 涨跌幅（%） |
| `PCHG` | 涨跌额（元） |
| `010000_TOAL_MARKET_VALUE...` | 总市值 |
| `010000_PE_D...` | 动态市盈率（倍） |
| `010000_PB...` | 市净率（倍） |

### 管理接口返回

检查 `status == 0` 且 `message == "ok"` 即表示操作成功。

## 输出规范

**查询自选股**：
1. 以 Markdown 表格输出全部自选股，至少包含：股票代码、简称、最新价、涨跌幅
2. 在表格前注明查询时间
3. 若 `dataList` 为空，提示用户前往东方财富 App 查看

**添加/删除**：
1. 告知用户操作结果（成功/失败）
2. 操作成功后，建议用户可通过"查询自选股"确认最新列表
3. 若接口报错，告知错误信息并提示前往东方财富 App 操作
