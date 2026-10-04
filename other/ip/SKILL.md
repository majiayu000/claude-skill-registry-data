---
name: jisu-ip
description: 使用极速数据 IP 查询 API，根据 IP 地址查询归属地和运营商类型信息。
metadata: { "openclaw": { "emoji": "📡", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据 IP 查询（Jisu IP）

基于 [IP 查询 API](https://www.jisuapi.com/api/ip/) 的 OpenClaw 技能，
根据 IP 地址查询其归属地与运营商类型。

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/ip/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/ip/ip.py`

## 使用方式

### 查询 IP 归属地与运营商

```bash
python3 skills/ip/ip.py '{"ip":"122.224.186.100"}'
```

请求 JSON 示例：

```json
{
  "ip": "122.224.186.100"
}
```

## 请求参数

| 字段名 | 类型   | 必填 | 说明   |
|--------|--------|------|--------|
| ip     | string | 是   | IP 地址 |

## 返回结果示例

脚本直接输出接口的 `result` 字段，结构与官网示例一致（参考 [`https://www.jisuapi.com/api/ip/`](https://www.jisuapi.com/api/ip/)）：

```json
{
  "area": "浙江省杭州市",
  "type": "电信"
}
```

当出现错误（如没有该 IP 信息）时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据 IP 文档](https://www.jisuapi.com/api/ip/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 在 OpenClaw 中的推荐用法

1. 用户提供 IP：「查一下 IP `122.224.186.100` 是哪里的」。  
2. 代理构造 JSON：`{"ip":"122.224.186.100"}` 并调用：  
   `python3 skills/ip/ip.py '{"ip":"122.224.186.100"}'`  
3. 从返回结果中读取 `area` 和 `type` 字段，为用户总结 IP 所在的省市及运营商类型。  

