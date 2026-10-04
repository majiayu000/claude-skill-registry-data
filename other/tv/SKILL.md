---
name: jisu-tv
description: 使用极速数据电视节目预告 API 查询指定频道某日的电视节目单，并支持获取全部电视频道列表。
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据电视节目预告（Jisu TV）

基于 [电视节目预告 API](https://www.jisuapi.com/api/tv/) 的 OpenClaw 技能，支持：

- **电视节目查询**（`/tv/query`）
- **电视节目频道列表**（`/tv/channel`）

可用于对话中回答「今晚 CCTV-3 有什么节目」「帮我看明天湖南卫视的晚间综艺」「有哪些可用频道及 ID」等问题。

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/tv/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/tv/tv.py`

## 使用方式

### 1. 获取频道列表（channel）

```bash
python3 skills/tv/tv.py channel
```

返回值为频道数组，每项包含：

- `tvid`：电视频道 ID  
- `name`：电视频道名称  
- `parentid`：上级 ID  
- `istv`：是否为电视频道（1 是，0 否）  

### 2. 查询某频道在某日的节目单（query）

```bash
python3 skills/tv/tv.py query '{"tvid":435,"date":"2015-10-19"}'
```

## 请求参数

### /tv/query

| 字段名 | 类型   | 必填 | 说明           |
|--------|--------|------|----------------|
| tvid   | int    | 是   | 电视频道 ID     |
| date   | string | 是   | 日期，格式 `YYYY-MM-DD` |

### /tv/channel

无请求参数。

## 返回结果示例

### /tv/query

脚本直接输出接口的 `result` 字段，例如（节选自官网示例）：

```json
{
  "tvid": "435",
  "name": "CCTV-3（综艺）",
  "date": "2015-08-09",
  "program": [
    {
      "name": "综艺喜乐汇",
      "starttime": "01:18"
    },
    {
      "name": "2014中国梦-我梦最美",
      "starttime": "03:55"
    }
  ]
}
```

字段说明：

| 字段名    | 类型     | 说明           |
|-----------|----------|----------------|
| tvid      | int      | 电视频道 ID     |
| name      | string   | 电视频道名称    |
| date      | string   | 日期           |
| program   | array    | 节目列表        |
| program[].name | string | 节目名称    |
| program[].starttime | string | 开始时间 |

### /tv/channel

返回数组，每项形如：

```json
{
  "tvid": "2381",
  "name": "中国美食",
  "parentid": "4",
  "istv": "1"
}
```

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "电视节目频道为空"
}
```

## 常见错误码

来源于 [极速数据电视节目预告文档](https://www.jisuapi.com/api/tv/)：

| 代号 | 说明           |
|------|----------------|
| 201  | 电视节目频道为空 |
| 202  | 电视节目频道错误 |
| 203  | 没有信息       |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无请求此数据权限、104 请求超过次数限制、105 IP 被禁止、106 IP 请求超过限制、107 接口维护中、108 接口已停用。

## 在 OpenClaw 中的推荐用法

1. 用户：「今晚 8 点有什么好看的综艺？」→ 先通过 `channel` 找到相关卫视或 CCTV 综艺频道的 `tvid`，再用 `query` 拉取当天节目单，根据时间筛选并用自然语言总结。  \n
2. 用户：「列出下周湖南卫视的晚间节目」→ 使用 `channel` 获取湖南卫视 `tvid`，对未来一周的日期依次调用 `query`，抽取 19:00–24:00 时段的节目并按日期分组展示。  \n
3. 用户：「支持哪些频道？」→ 直接调用 `channel`，罗列 `name` 与 `tvid`，便于后续对话中用频道 ID 精确查询。  \n

