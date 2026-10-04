---
name: laohan-douyinsousuo
description: 抖音关键词搜索与结构化取证 adapter，只使用已安装且已登录的 OpenCLI；独立回答搜索请求，或为真人口播①写本期抖音证据，不决定最终选题。Use when 用户说"抖音搜索""搜一下抖音""抖音上搜""抖音关于""抖音上有什么""douyin搜索"，或 bianpai/选题流程要求抖音关键词验证。
version: "3.3.0"
---

# 抖音搜索

这是工作流里的抖音搜索编排接口。只使用宿主已安装且已登录的 OpenCLI，不自带爬虫、浏览器、cookie 复制、独立 profile 或 Python runtime。

## 输入

- `query`：必填，搜索关键词。
- `limit`：可选，1—30，默认 10。
- `episode`：可选，本期 `episodes/<slug>` 路径；只允许写 `00-抖音搜索证据.json` 与 `.md`，不得写 candidates、source-health 或 `00-选题.*`。

## 执行

### 1. 预检

```bash
opencli doctor
opencli douyin whoami -f json
```

Browser Bridge 可连接且 `logged_in=true` 时执行搜索。任一预检失败时，episode 模式仍写出 `UNAVAILABLE` 证据与原始错误供①继续判断；独立搜索请求则如实报告当前不可用。不要抽取或复制 Chrome cookie，也不要安装新工具。

### 2. 搜索

Episode 模式用确定性包装器一次执行 1—3 个短名单查询并原子写 JSON/Markdown：

```bash
node ~/Documents/laohan-skills/laohan-douyinsousuo/scripts/search-evidence.mjs \
  --episode episodes/<slug> \
  --query "关键词一" \
  --query "关键词二" \
  --limit 10
```

独立单查询可直接执行：

```bash
opencli douyin search "$QUERY" --limit "$LIMIT" -f json
```

结果必须是 JSON 数组，并逐条保留 OpenCLI 返回的 `rank`、`desc`、`author`、`url`、`aweme_id`、发布时间及可用互动字段。稳定 id 优先使用 `aweme_id` 或 URL 中的 `/video/<id>`；两者都没有时才用 `sha256(url + desc)[:12]`。排名不得参与稳定 id；不要按缺失字段重排，也不要把 OpenCLI 的结果顺序描述成“按点赞排行”。

### 3. 失败降级

按顺序执行，成功即停：

1. 同一命令加 `--trace retain-on-failure`，使用 OpenCLI autofix 修复现有 adapter；总尝试最多 3 次。
2. 若 `opencli doctor` 仍正常但 adapter 持续失败，使用 `opencli browser douyin-search bind` 绑定用户当前已登录的抖音标签页，仅做读取和取证。执行浏览器降级前说明会操作当前标签页。
3. 仍失败则记录失败层级和原始错误。episode 模式标记平台数据 `UNAVAILABLE` 并返回证据文件，不把它升级为①的卡点；独立搜索请求报告本次未取得结果。不得临时安装 DrissionPage、Playwright、浏览器或自制爬虫。

## 输出与判断

先展示搜索健康状态和实际返回条数，再展示结果表：

| # | 作者 | 点赞 | 标题 | 链接 |
|---|------|------|------|------|
| 1 | author | likes/不可用 | desc | url |

- 互动字段缺失写 `null` 并在 `field_availability` 标记 `false`；实际返回数字 `0` 则保留 0 并标记 `true`，不得混为一谈。
- 返回空数组时写 `EMPTY_OR_FIELD_UNAVAILABLE`；不能据此断言抖音上没有相关内容。
- 当前已安装 OpenCLI 1.8.6 的 `douyin search` 只提供搜索结果样本，卡片通常只有点赞字段；`douyin hashtag hot` 可提供全站热点，已由 laohan-xuanti 的 discovery route 使用。`douyin hashtag search` 当前接口实测失败，`hashtag hot --keyword` 也不能可靠按关键词过滤。因此搜索量、供给总量、增长速度和官方内容缺口默认均为 `UNAVAILABLE`；以后只有 OpenCLI 实际返回这些字段时才使用，不从结果条数或点赞反推。
- 事实性结论必须回到原视频或权威来源核验；搜索结果只能作为发现证据。
- 用户单独要求搜索分析时，可总结结果中可见的内容类型和重复角度；不得决定工作流最终选题，不得补造搜索结果未提供的事实。
- 指定 `episode` 时必须使用 runtime-locked 包装器，先写机器真源 `00-抖音搜索证据.json`，再从它生成 `.md`；Markdown 不得新增 JSON 没有的结论。

Episode JSON 最小合同：

```json
{
  "schema_version": 1,
  "collected_at": "ISO-8601",
  "executor": {
    "name": "opencli",
    "version": "实际版本",
    "doctor_status": "PASS|FAILED",
    "logged_in": true,
    "availability_status": "AVAILABLE|UNAVAILABLE"
  },
  "queries": [{
    "query": "关键词",
    "command": "opencli douyin search ... -f json",
    "attempted_at": "ISO-8601",
    "status": "OK|EMPTY_OR_FIELD_UNAVAILABLE|FAILED",
    "result_count": 1,
    "results": [{"id":"稳定id","rank":1,"desc":"原字段","author":"原字段","url":"https://..."}]
  }]
}
```

`OK` 必须 `result_count > 0` 且等于 results 长度；`EMPTY_OR_FIELD_UNAVAILABLE` 必须为 0 和空数组；FAILED 必须为 0、空数组并有 `error`。全部查询 FAILED 或预检失败时写 `availability_status: UNAVAILABLE`，仍完成 episode 证据落盘；①不得据此推断平台没有需求。

## 边界

- 下载视频、博主作品列表：用 `/laohan-xiazai`。
- 评论、发布、账号运营：用 `/laohan-yunying` 或对应 OpenCLI adapter。
- 禁止 DrissionPage、`browser_cookie3` cookie 注入、独立 user-data-dir、额外 Chrome/Chromium、后台自动发布或回复。
