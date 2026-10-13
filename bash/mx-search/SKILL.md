---
name: mx_search
version: 1.1.0
description: "基于东方财富妙想搜索能力，用于获取涉及时效性信息或特定事件信息的任务，包括新闻、公告、研报、政策、交易规则、具体事件、各种影响分析等。支持多 API Key 自动轮询 Fallback。"
author: User
---

# 妙想资讯搜索 (mx_search)

基于东方财富妙想搜索能力的金融资讯搜索 Skill，基于金融场景进行信源智能筛选，避免AI搜索时参考到非权威、过时的信息。

## 新功能：多 Key Fallback（v1.1.0）

✅ **支持多 API Key 自动轮询** - 当一个 Key 配额耗尽时自动切换到备用 Key

## Overview

妙想资讯搜索提供：
- **个股资讯** - 最新研报、机构观点
- **板块/主题资讯** - 近期新闻、政策解读
- **宏观/风险资讯** - 汇率风险、政策影响分析
- **综合解读** - 大盘异动原因、资金流向解读

## Prerequisites

### API Key 配置

需要在环境变量中配置妙想 API Key：

```bash
# 单 Key 模式（兼容旧版）
export MX_APIKEY="your_api_key_here"

# 多 Key 模式（推荐，自动 Fallback）
export MX_APIKEYS="key1,key2,key3"
```

或在运行时传入。

### API 端点

- **搜索接口**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search`
- **请求方式**: POST
- **Content-Type**: application/json
- **配额限制**: 50 次/天/Key

## Usage

### Python 调用方式

```python
from scripts.mx_search_client import MxSearchClient

# 单 Key 模式（兼容旧版）
client = MxSearchClient(api_key="your_key")

# 多 Key 模式（自动 Fallback）
client = MxSearchClient(api_keys=["key1", "key2"])

# 从环境变量读取（MX_APIKEYS 逗号分隔）
client = MxSearchClient()

# 搜索个股资讯
result = client.search("格力电器最新研报")
print(result)

# 查看配额统计
stats = client.get_quota_stats()
print(f"剩余配额: {stats['total_remaining']} 次")
```

### 多 Key Fallback 示例

```python
from scripts.mx_search_client import MxSearchClient

# 配置两个 Key，当 key1 配额耗尽时自动切换到 key2
client = MxSearchClient(api_keys=[
    "mkt_xxxxxxxxxxxx",  # 主 Key
    "mkt_yyyyyyyyyyyy"   # 备用 Key
])

# 正常调用，无需关心配额管理
for stock in ["茅台", "宁德时代", "比亚迪", "腾讯"]:
    try:
        result = client.search(f"{stock}最新研报")
        # 结果中包含配额信息
        meta = result.get('_meta', {})
        print(f"使用 Key: {meta.get('api_key_masked')}, 剩余: {meta.get('quota_remaining')}")
    except Exception as e:
        print(f"搜索失败: {e}")
```

### 命令行调用

```bash
# 搜索个股资讯
python3 scripts/mx_search_client.py --query "贵州茅台机构观点"

# 搜索板块资讯
python3 scripts/mx_search_client.py --query "新能源政策解读"
```

### 典型应用场景

#### 1. 个股资讯搜索
```python
client = MxSearchClient()
result = client.search("立讯精密最新研报")
```

#### 2. 板块资讯搜索
```python
result = client.search("商业航天板块近期新闻")
```

#### 3. 宏观风险分析
```python
result = client.search("A股具备自然对冲优势的公司 汇率风险")
```

#### 4. 综合解读
```python
result = client.search("今日大盘异动原因")
```

## API 详细说明

### 请求参数

| 参数 | 类型 | 必选 | 描述 |
|------|------|------|------|
| query | str | Y | 搜索问句 |

### 请求示例

```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
--header 'Content-Type: application/json' \
--header 'apikey: your_api_key' \
--data '{"query":"立讯精密的资讯"}'
```

### 返回字段说明

| 字段路径 | 简短释义 |
|----------|----------|
| `title` | 信息标题，高度概括核心内容 |
| `secuList` | 关联证券列表，含代码、名称、类型等 |
| `secuList[].secuCode` | 证券代码（如 002475） |
| `secuList[].secuName` | 证券名称（如立讯精密） |
| `secuList[].secuType` | 证券类型（如股票 / 债券） |
| `trunk` | 信息核心正文 / 结构化数据块，承载具体业务数据 |
| `_meta` | 元数据（仅多Key模式），包含使用的Key和剩余配额 |

### _meta 字段说明

```python
{
    "_meta": {
        "api_key_masked": "mkt_m3...y8",  # 脱敏显示的Key
        "quota_remaining": 45,              # 该Key剩余配额
        "quota_total": 50                   # 每日配额上限
    }
}
```

## Best Practices

### 多 Key 配置策略

**推荐做法**：
1. **主从模式**：配置 2 个 Key，主 Key 耗尽后自动切换备用 Key
2. **负载均衡**：多个 Key 轮流使用，延长总可用时间
3. **环境变量管理**：生产环境使用 `MX_APIKEYS` 配置，避免硬编码

```bash
# .bashrc 或 .env 文件
export MX_APIKEYS="mkt_primary_key,mkt_backup_key"
```

### 配额监控

```python
from scripts.mx_search_client import MxSearchClient

client = MxSearchClient()

# 查看配额统计
stats = client.get_quota_stats()
print(f"总 Key 数: {stats['total_keys']}")
print(f"总剩余配额: {stats['total_remaining']}")
print(f"Key 详情: {stats['key_stats']}")
```

### 问句优化

**好的问句示例**:
```python
# 个股
"格力电器最新研报"
"贵州茅台机构观点"

# 板块
"商业航天板块近期新闻"
"新能源政策解读"

# 宏观/风险
"A股具备自然对冲优势的公司 汇率风险"
"美联储加息对A股影响"

# 综合解读
"今日大盘异动原因"
"北向资金流向解读"
```

### 错误处理

```python
from scripts.mx_search_client import MxSearchClient, MxSearchError

# 多 Key 模式 - 配额超限会自动切换，无需手动处理
client = MxSearchClient(api_keys=["key1", "key2"])

try:
    result = client.search("格力电器最新研报")
    print(f"使用 Key: {result['_meta']['api_key_masked']}")
    print(f"剩余配额: {result['_meta']['quota_remaining']}")
except MxSearchError as e:
    if "配额已耗尽" in e.message:
        print("所有 Key 配额已用完，请明日再试或添加更多 Key")
    else:
        print(f"搜索失败: {e.message}")
```

## Troubleshooting

### API Key 无效
```
错误: 401 Unauthorized
解决: 检查环境变量 MX_APIKEY 或 MX_APIKEYS 是否正确配置
```

### 请求超时
```
错误: TimeoutError
解决: 增加超时时间或检查网络连接
```

### 无返回数据
```
错误: 返回空结果
解决: 检查问句是否清晰，或更换关键词重试
```

### 配额超限（多 Key Fallback）
```
错误: 所有 API Key 配额已耗尽
解决: 
  1. 确认已配置多个 Key（MX_APIKEYS=key1,key2）
  2. 检查 quota_stats 查看使用情况
  3. 等待次日配额重置（每日0点）
  4. 或添加更多 API Key
```

### 配额统计查看
```python
from scripts.mx_search_client import MxSearchClient

client = MxSearchClient()
stats = client.get_quota_stats()

# 输出示例：
# {
#     'total_keys': 2,
#     'quota_per_key': 50,
#     'key_stats': {'mkt_m3...y8': {'used': 45, 'remaining': 5, 'total': 50}},
#     'total_remaining': 55
# }
```

## 版本更新

### v1.1.0 (2026-03-20)
- ✅ 新增多 Key Fallback 支持
- ✅ 配额管理器自动追踪每日使用
- ✅ 配额超限时自动切换备用 Key
- ✅ 新增 `get_quota_stats()` 方法查看配额统计
- ✅ 兼容旧版单 Key 配置

## 相关链接

- 东方财富官网: https://www.eastmoney.com/

---

**Note**: 需要先在妙想 Skills 页面获取 API Key 后才能使用。
