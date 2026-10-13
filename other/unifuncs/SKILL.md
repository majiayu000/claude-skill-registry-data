---
name: unifuncs
version: 1.0.0
description: "Unifuncs Deep Research API 集成 - 获取A股市场深度研究报告、热门板块分析、涨停股预测等"
author: StanleyChanH
---

# Unifuncs Deep Research 🔬

**By StanleyChanH**

专业的A股市场深度研究 API 集成技能，支持热门板块分析、涨停股预测、市场深度研究等功能。

## Overview

Unifuncs Deep Research API 提供：
- **深度研究报告** - 基于AI分析的市场研究报告
- **热门板块分析** - 实时识别A股热门板块
- **涨停股预测** - 分析涨停股连板概率
- **市场情绪分析** - 综合市场情绪判断

## Prerequisites

### API Key Configuration

API Key 已配置在技能脚本中：
```
sk-gCxXKluzZeZEjUvvyc35efFBjOa6SUcR7gDDG9giUPG3Aetg
```

### API 端点

- **创建任务**: `POST /v1/create_task`
- **查询任务**: `GET /v1/query_task`
- **Base URL**: `https://api.unifuncs.com/deepresearch`

## Usage

### Python 调用方式

```python
from scripts.unifuncs_client import UnifuncsClient

# 初始化客户端
client = UnifuncsClient()

# 创建研究任务
task_id = client.create_task(
    output_prompt="今天A股热门板块哪几个？所有涨停股中，哪3个涨停股在下一个交易日继续涨停的概率最大？"
)

# 轮询获取结果
result = client.query_task(task_id)
print(result)
```

### 命令行调用

```bash
# 创建研究任务
openclaw unifuncs create --prompt "今天A股热门板块哪几个？"

# 查询任务结果
openclaw unifuncs query --task-id "3aff2a91-7795-4b73-8dab-0593551a27a1"

# 一键获取报告（自动创建并等待结果）
openclaw unifuncs report --prompt "分析今日市场情绪和热门板块"
```

### 典型应用场景

#### 1. 热门板块分析
```python
client = UnifuncsClient()
result = client.get_report(
    "今天A股热门板块哪几个？分析各板块的领涨股和资金流向"
)
```

#### 2. 涨停股预测
```python
result = client.get_report(
    "所有涨停股中，哪3个涨停股在下一个交易日继续涨停的概率最大？给出理由"
)
```

#### 3. 市场深度分析
```python
result = client.get_report(
    "分析今日北向资金流向、主力资金动向，预测明日市场走势"
)
```

## API 详细说明

### create_task - 创建任务

提交研究需求后立即返回 task_id，后端在后台执行。

**请求参数:**
| 参数 | 类型 | 必选 | 描述 |
| --- | --- | --- | --- |
| model | str | Y | 模型类型，固定为 "u2" |
| messages | array | Y | 消息数组，格式见示例 |
| output_type | str | N | 输出类型: "summary" (摘要) 或 "full" (完整) |
| output_prompt | str | Y | 研究问题/提示词 |
| reference_style | str | N | 引用风格: "hidden" 或 "visible" |

**返回示例:**
```json
{
  "task_id": "3aff2a91-7795-4b73-8dab-0593551a27a1",
  "status": "pending"
}
```

### query_task - 查询任务

轮询任务状态，完成后返回研究结果。

**请求参数:**
| 参数 | 类型 | 必选 | 描述 |
| --- | --- | --- | --- |
| task_id | str | Y | 任务ID |

**返回示例:**
```json
{
  "task_id": "3aff2a91-7795-4b73-8dab-0593551a27a1",
  "status": "completed",
  "result": {
    "summary": "今日热门板块包括...",
    "answer": "详细分析结果..."
  }
}
```

**状态说明:**
- `pending` - 任务排队中
- `processing` - 任务执行中
- `completed` - 任务完成
- `failed` - 任务失败

## Integration with T01 Task

本技能专为 T01 Task（A股龙头选股策略系统）设计，可提供：

1. **板块热度分析** - 识别当前市场热点板块
2. **龙头股筛选** - 从热门板块中筛选龙头股
3. **连板预测** - 预测涨停股的连板概率
4. **资金流向分析** - 分析主力资金动向

### 与 Tushare 配合使用

```python
# 1. 使用 Tushare 获取涨停股列表
from tushare_client import TushareClient
ts = TushareClient()
limit_stocks = ts.get_limit_up_list()

# 2. 使用 Unifuncs 分析涨停股连板概率
from unifuncs_client import UnifuncsClient
uf = UnifuncsClient()
analysis = uf.get_report(
    f"以下涨停股哪3个在下一个交易日继续涨停的概率最大？{limit_stocks}"
)
```

## Best Practices

### 轮询间隔
- 建议轮询间隔：3-5秒
- 最大等待时间：120秒
- 超时后可重新创建任务

### 提示词优化
```python
# 好的提示词示例
good_prompt = """
请分析以下内容：
1. 今日热门板块及其领涨股
2. 各板块的资金净流入情况
3. 预测明日可能延续强势的板块

请给出具体数据和理由。
"""

# 不好的提示词示例
bad_prompt = "分析股市"
```

### 错误处理
```python
try:
    result = client.get_report(prompt, timeout=120)
except TimeoutError:
    print("任务超时，请稍后重试")
except APIError as e:
    print(f"API错误: {e.message}")
```

## Troubleshooting

### API Key 无效
```
错误: 401 Unauthorized
解决: 检查 API Key 是否正确配置
```

### 任务超时
```
错误: TimeoutError
解决: 增加等待时间或重新创建任务
```

### 任务失败
```
错误: status = "failed"
解决: 检查提示词是否合理，重新提交任务
```

## 相关链接

- API 文档: https://api.unifuncs.com/deepresearch
- 支持邮箱: support@unifuncs.com

---

**Note**: API Key 已内置配置，可直接使用。建议合理控制调用频率，避免频繁请求。
