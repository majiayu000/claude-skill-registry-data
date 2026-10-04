---
name: jisu-oil
description: 使用极速数据今日油价 API 查询各省市汽油、柴油实时价格，并支持获取全部省市列表。
metadata: { "openclaw": { "emoji": "⛽", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据今日油价（Jisu Oil）

基于 [今日油价 API](https://www.jisuapi.com/api/oil/) 的 OpenClaw 技能，支持：

- **省市油价查询**（`/oil/query`）
- **全部省市列表**（`/oil/province`）

适合在对话中回答「今天河南的 92 号油多少钱」「列一下支持查询油价的所有省份」等问题。

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/oil/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/oil/oil.py`

## 使用方式

### 1. 省市油价查询（query）

```bash
python3 skills/oil/oil.py query '{"province":"河南"}'
```

### 2. 全部省市列表（province）

```bash
python3 skills/oil/oil.py province
```

## 请求参数（/oil/query）

| 字段名    | 类型   | 必填 | 说明 |
|-----------|--------|------|------|
| province  | string | 是   | 省名（如：河南、浙江、北京） |

示例 JSON：

```json
{
  "province": "河南"
}
```

## 返回结果示例

### /oil/query

脚本直接输出接口的 `result` 字段，典型结构（节选自官网示例）：

```json
{
  "province": "河南",
  "oil89": null,
  "oil92": "7.98",
  "oil95": "8.52",
  "oil98": "9.17",
  "oil0": "7.62",
  "oil90": null,
  "oil93": "7.98",
  "oil97": "8.52",
  "updatetime": "2022-12-14 00:00:00"
}
```

字段含义：

| 字段名      | 类型   | 说明      |
|------------|--------|-----------|
| province   | string | 省名称     |
| oil89      | string | 89 号油价 |
| oil90      | string | 90 号油价 |
| oil92      | string | 92 号油价 |
| oil93      | string | 93 号油价 |
| oil95      | string | 95 号油价 |
| oil97      | string | 97 号油价 |
| oil98      | string | 98 号油价 |
| oil0       | string | 0 号柴油价 |
| updatetime | string | 更新时间   |

### /oil/province

返回值为字符串数组，每项为一个省/直辖市名称，例如：

```json
[
  "安徽",
  "北京",
  "广东",
  "浙江",
  "重庆"
]
```

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "省份为空"
}
```

## 常见错误码

来源于 [极速数据今日油价文档](https://www.jisuapi.com/api/oil/)：

| 代号 | 说明     |
|------|----------|
| 201  | 省份为空 |
| 202  | 没有信息 |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无权限、104 超过次数限制、105 IP 被禁止、106 IP 超限、107 接口维护中、108 接口已停用。

## 在 OpenClaw 中的推荐用法

1. 用户：「查一下浙江今天的 92 号油价」→ 构造 `query '{"province":"浙江"}'`，解析 `oil92` 并附带更新时间返回。  \n
2. 用户：「支持哪些省份的油价查询？」→ 调用 `province`，将数组直接展示或用于后续自动补全。  \n
3. 用户：「帮我对比一下河南和广东今天油价」→ 连续调用 `query` 两次，分别取出 `oil92`/`oil95`/`oil0` 等字段，按表格形式汇总给用户。

