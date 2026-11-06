---
name: xiaohongshu-note-acquire
description: "小红书作品笔记获取工具。根据关键词获取小红书作品数据，支持按最多点赞、最多评论、最多收藏排序，支持按日期范围筛选，支持单次最多1w条笔记，结果以结构化数据展示。当用户需要获取小红书作品、查询小红书高赞内容、搜索xhs收藏笔记、爬取rednote评论笔记、搜索小红书爆款笔记时使用。触发词：小红书获取、小红书作品、小红书爆款、小红书搜索、小红书热门、小红书笔记查询、小红书高赞、小红书收藏、小红书评论。"
license: MIT
version: "1.2.1"
category: 数据分析
homepage: https://www.guaikei.com
metadata:
  openclaw:
    emoji: "📕"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins: ["node"]
    env: ["GUAIKEI_API_TOKEN"]
  env_desc:
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通。"
  keywords:
    - "小红书"
    - "小红薯"
    - "xhs"
    - "rednote"
    - "小红书搜索"
    - "小红书笔记"
    - "小红书评论"
    - "小红书博主"
    - "爆款选题"
    - "竞品分析"
    - "KOL筛选"
    - "评论舆情"
    - "xiaohongshu"
  category:
    - "Integrations"
    - "Research"
    - "Creative"
    - "内容创作"
    - "数据分析"
    - "商业运营"
  tags:
    - "小红书"
    - "小红书搜索"
    - "小红书笔记"
    - "小红书评论"
    - "小红书博主"
    - "小红书运营"
    - "小红书数据分析"
    - "爆款选题"
    - "竞品分析"
    - "KOL筛选"
    - "评论舆情分析"
    - "内容选题调研"
    - "趋势洞察"
    - "种草营销"
    - "新媒体运营"
    - "关键词搜索"
    - "评论分析"
    - "选题调研"
    - "爆款挖掘"
    - "小红书内容创作"
    - "小红书营销"
  schemas:
    - name: "输出信封"
      file: "assets/output_envelope.schema.json"
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "详情入参"
      file: "assets/detail_cli_req.schema.json"
    - name: "详情出参"
      file: "assets/detail_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
  examples:
    - "帮我找最近一周小红书『露营装备』的高赞图文笔记 → node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --time 2 --limit 20"
    - "这条小红书笔记评论区在吐槽什么 → node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 20"
    - "看这个小红书博主最近 30 条作品发什么 → node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 30"
    - "分析这篇小红书爆款笔记为什么火 → node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
    - "监控『多巴胺穿搭』最新动态 → node src/xiaohongshu/search-cli.js --keyword '多巴胺穿搭' --sort 1 --time 1 --limit 40"
    - "这个小红书博主多少粉丝 → node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx' --limit 0"
    - "只要这篇笔记近 30 天的评论 → node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx' --expired_at 30 --limit 20"
---

# 小红书笔记作品数据获取

> ✨ **一句话**：「小红书笔记作品数据获取」按关键词或笔记/博主链接，拿回结构化的小红书公开数据——笔记详情、评论、博主作品与粉丝获赞收藏，直接喂给选题分析、竞品对比和舆情归纳。不登录，不发布；结果是一份 JSON，AI 可直接接着用。

> ✨ **解决什么问题**：小红书运营最费时间的不是写内容，是「先搞清楚该写什么」。人工翻 50 条笔记记录点赞收藏要一小时，本工具一条命令返回结构化数据，AI 直接接着做归纳。

| 你要做的事 | 用哪个命令 | 你拿到什么 |
| --- | --- | --- |
| 🔍 找选题、看高赞 | `search-cli.js` | 笔记数组。点赞、收藏、评论、分享都是字符串 |
| 📰 看一篇笔记的正文 | `detail-cli.js` | 一个笔记对象。不含评论 |
| 💬 看评论区 | `comment-cli.js` | 评论数组 |
| 📸 看博主作品 | `post-cli.js --limit 大于 0` | `results.note` 笔记数组，以及可能有的 `results.user` |
| 👥 看粉丝、获赞、收藏 | `post-cli.js`，不传 `--limit` 或 `--limit 0` | `results.user`。`fans` 粉丝，`liked` 获赞，`collected` 收藏，`interaction` 获赞与收藏 |

**🔥 适合放进 Agent 的原因**

- **🔒 只读**：不登录小红书账号，无发布、点赞、评论、关注
- **💪 双上限**：技能硬上限 10000（按量 Token）；**包月**搜索最多 40、作品最多 30、评论最多 20。互动数是字符串，空字符串和数字 0 可能不返回
- **🎛️ 参数说了算**：类型、排序、时间、数量越界就失败，不会偷偷改成默认值
- **🤖 一份 JSON**：成功、无结果、失败都是同一份信封，字段以 `assets/*.schema.json` 为准

在本技能目录下执行 `node src/xiaohongshu/*.js`。先确认环境变量 `GUAIKEI_API_TOKEN` 已配置。

查询过程中 stderr 出现「处理中」表示任务还在跑，等进程退出后再读 stdout。向用户只说 `message` 和关键字段，不要念 stderr，也不要把整份 JSON 贴回去。

执行时记住这几条：

- 没有关键词或链接就先问，不要编造，也不要改成别的词再偷偷重跑
- 搜索不传 `--limit` 是 **20** 条；博主命令不传 `--limit` 是 **0**，只有博主信息，没有作品列表
- 互动数全是字符串。比较、排序、算比值之前先转成数字。空字符串和数字 0 可能不出现
- `status=empty` 且退出码 0 是「没有结果」，不是命令失败

按这个顺序执行：

1. 先确认 `GUAIKEI_API_TOKEN` 已配置。没有配置时不要先跑一遍试探。
2. 按第 2 节选择命令。没有关键词或链接就问，不要编造。
3. 按第 3 节填写参数。`-t` 是内容类型，`-i` 才是发布时间。含空格的关键词写成一个引号参数，不要拆成两个位置参数。
4. 在技能目录执行。stderr 的「处理中」不是失败。查询最多 20 次，间隔从 2 秒起增加，之后每次 60 秒，只算等待大约 15 分钟。每次请求本身还有最多 20 秒超时。宿主如果更早结束进程，按超时处理，不要立刻用同一组参数连打。
5. 只读 stdout 的 JSON 信封。
6. 向用户只说结论和关键字段。

同一组参数再次执行时，笔记搜索、作品和评论大约 20 分钟内会复用已有任务，详情大约 19 分钟内复用。评论还要 `expired_at` 相同。等到 `TIMEOUT` 后再立刻重跑，详情的窗口可能已经过去。

## 1. ✅ 什么时候调用

### 1.1 🎯 满足任一条件即调用

- 用户提到「小红书」「小红薯」「xhs」「rednote」，并要求查看、搜索或分析内容
- 用户要做关键词搜索、选题、竞品、评论、博主作品、KOL 筛选或舆情
- 用户给了关键词、笔记链接、博主主页、`xiaohongshu.com` / `xhslink.com` / `xhslink.cn` 链接、24 位作品 id，或 24 / 29 位博主 id

### 1.2 🚫 不要调用

- 只让写文案、起标题、改脚本，没要求查数据
- 平台是抖音、快手、B 站、微博、公众号
- 要求登录、私密笔记、草稿、仅粉丝可见、创作者后台或商业化数据
- 没有关键词也没有可识别链接，且目标不明确

### 1.3 👀 意图模糊时先问

不要编造关键词或链接。例如「做竞品分析」要确认：是某个账号还是某个关键词，看最新还是高赞，看多少条。

## 2. 🔀 路由

| 用户给了什么 | 命令 | 最少要有 |
| --- | --- | --- |
| 🔍 关键词，没有链接 | `node src/xiaohongshu/search-cli.js` | `--keyword` |
| 📰 笔记链接或笔记 id，要正文 | `node src/xiaohongshu/detail-cli.js` | `--url` |
| 💬 笔记链接或笔记 id，只要评论 | `node src/xiaohongshu/comment-cli.js` | `--url` |
| 👥 博主主页或 user_id | `node src/xiaohongshu/post-cli.js` | `--url` |

按这个顺序判断，命中即停：

1. 💬 要评论、留言、舆情，且对象是一篇笔记 → `comment-cli.js`
2. 👥 要作品、主页、账号、博主、粉丝、获赞 → `post-cli.js`
3. 📰 要一篇笔记的标题、正文、图片、互动 → `detail-cli.js`
4. 🔍 有关键词，且没有上面三类信号 → `search-cli.js`
5. 🤔 以上都不明确 → 先追问

### 2.1 🗣️ 口语对应哪个参数

| 用户说 | 应该传 |
| --- | --- |
| 爆款、高赞、什么火 | `search-cli.js --sort 2` |
| 最新、刚发的、今天 | `search-cli.js --sort 1 --time 1` |
| 这周、近期 | `search-cli.js --sort 1 --time 2` |
| 收藏多 | `search-cli.js --sort 4` |
| 评论多、讨论度高 | `search-cli.js --sort 3` |
| 图文、文案 | `--type 2` |
| 视频 | `--type 1` |
| 多少粉丝、获赞、收藏 | `post-cli.js --limit 0` |
| 最近发了什么、近 N 条作品 | `post-cli.js --limit N`。没说条数就问，不要省略 |
| 评论区、舆情 | `comment-cli.js`。没说条数用默认 10；要归纳观点再加大 `--limit`（包月勿超 20） |
| 近 30 天的评论 | `--expired_at 30` |
| 只要正文、为什么火 | `detail-cli.js`。它不带评论 |

这些数字不是天数。`--time 2` 是一周内，`--sort 2` 是最多点赞。

链接类型：

- `xiaohongshu.com/user/profile/{user_id}` 只能给 `post-cli.js`
- `xiaohongshu.com/explore/{id}` 只能给 `detail-cli.js` 或 `comment-cli.js`
- `xiaohongshu.com/discovery/item/{id}` 给 `detail-cli.js` 或 `comment-cli.js`
- 24 位十六进制 id：详情和评论把它当作品 id，作品命令也可以把它当博主 id。用户只丢了一个 24 位 id 时，先问是笔记还是博主
- 29 位十六进制 id 只是博主 id，只能给 `post-cli.js`
- `xhslink.com` 与 `xhslink.cn` 的 `/m/*`、`/o/*` 三种命令都接受，前缀后面必须还有一段 id。只拿到短链、又没说明是笔记还是主页时，先问，不要两个命令都试
- 不带 `www` 的 `xiaohongshu.com` 会补成 `www.xiaohongshu.com`。`http://` 会改成 `https://`。协议和主机名不区分大小写，笔记 id、短链 id 和 query 保持原样

`detail-cli.js` 不返回评论。正文和评论都要时，先详情，再 `comment-cli.js`。

打开搜索或作品列表里的一条笔记：有 `id` 时用 `https://www.xiaohongshu.com/explore/{id}`；有 `xsec_token` 时再接 `?xsec_token=`。程序不会另造 `url` 字段。博主主页优先用 `user.share_link`。

选题可以先 `search-cli.js --sort 2 --time 2 --limit 30`，再对挑出的笔记跑详情。竞品看作品时必须显式 `--limit`，例如 30；不传时只有博主信息。评论数、点赞数、收藏数是字符串，做比值前先转成数字。空字符串和数字 0 可能不出现。

## 3. 🧺 参数

枚举和数量不在允许范围内时，命令直接失败（退出码 2，`INVALID_ARGS`），不会改成默认值再请求。四个命令都支持 `--help` / `-h`：帮助打在 stderr，退出码 0，stdout 为空。`-t` 是内容类型，`-i` 才是发布时间。关键词以 `-` 开头时写成 `--keyword=-AI`，或 `node src/xiaohongshu/search-cli.js -- -AI`。完整字段见 `assets/*_cli_req.schema.json` 与 [references/options.md](references/options.md)。

### 3.1 🔍 关键词搜索

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--keyword` `-k` | 是 | 1–50 个字符，不能是链接，不含 `< > " '` | — |
| `--type` `-t` | 否 | `0` 全部 / `1` 视频 / `2` 图文 | `0` |
| `--sort` `-s` | 否 | `0` 综合 / `1` 最新 / `2` 最多点赞 / `3` 最多评论 / `4` 最多收藏 | `0` |
| `--time` `-i` | 否 | `0` 全部 / `1` 一天内 / `2` 一周内 / `3` 半年内 | `0` |
| `--limit` `-l` | 否 | 整数 1–10000（**包月 Token 实际最多 40**） | `20` |

**套餐双上限（重要）**：技能侧硬上限为 10000（按量 Token）。**包月 Token** 超限会返回 `PLAN_LIMIT`（搜索/作品后端 errcode 14，评论为 16），不要当网络错误重试：搜索最多 **40**，作品最多 **30**，评论最多 **20**；详情无此条数限制。具体以官网与本次 `message` 为准。

这些数字不是天数。`--time 2` 是一周内，不是 2 天。`--sort 2` 是最多点赞，不是最新。

命令会先去掉控制字符和 emoji，再校验长度。纯 emoji 或纯符号洗完为空，会得到 `INVALID_KEYWORD`。

| 用户说 | 应该传 |
| --- | --- |
| 爆款、高赞、什么内容火 | `--sort 2` |
| 最新、刚发的、现在 | `--sort 1 --time 1` |
| 这周、近期 | `--sort 1 --time 2` |
| 收藏多、值得存 | `--sort 4` |
| 讨论度高、评论多 | `--sort 3` |
| 图文、文案 | `--type 2` |
| 视频 | `--type 1` |

未指定 `--limit` 时返回 20 条。用户说「全部 / 越多越好」再显式加大，不要自行抓 10000 条；**包月用户先确认套餐上限**，搜索勿超 40。超过约 1000 条时告诉用户数据量。

### 3.2 📰 笔记详情

只有 `--url` `-u`，必填，最长按接口为 255。支持：

- `https://www.xiaohongshu.com/explore/{id}`
- `https://www.xiaohongshu.com/discovery/item/{id}`
- `https://xhslink.com/o/*`、`https://xhslink.cn/o/*`
- `https://xhslink.com/m/*`、`https://xhslink.cn/m/*`
- 24 位笔记 id

`http://` 会改成 `https://`，不带 `www` 的域名会补上 `www`。主页链接不要传给本命令。短链前缀后面没有 id 时，按无效链接失败。

### 3.3 👥 博主作品

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 主页链接，或 24 / 29 位 `user_id`，最长按接口为 255 | — |
| `--limit` `-l` | 否 | 整数 0–10000（**包月最多 30**）。`0` 只要博主信息和互动数据；大于 0 取笔记列表 | `0` |

支持 `https://www.xiaohongshu.com/user/profile/{user_id}`、上面四类短链，以及 24 或 29 位 `user_id`。路径里的作品 id 必须是 24 位，博主 id 必须是 24 或 29 位。

不传 `--limit` 不会返回作品列表。用户要看最近发了什么，必须写出条数。包月勿超 30。

### 3.4 💬 笔记评论

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 笔记链接或 24 位笔记 id。含 `explore`、`discovery/item`、短链 | — |
| `--expired_at` `-e` | 否 | 正整数天数，或 `YYYY-MM-DD HH:mm:ss`。`--expire` 是同一参数 | 不传则按北京时间近 6 年换算成一个时间点 |
| `--limit` `-l` | 否 | 整数 1–10000（**包月最多 20**） | `10` |

`expired_at` 是时间过滤，不是分页。`limit=10000` 且 `expired_at=1` 也只返回近 1 天的评论。用户传入的天数或时间会原样出现在 `request.expired_at`。用户没传时，命令自己换成一个 `YYYY-MM-DD 00:00:00`，创建和查询用同一个值，这个值也会写进 `request.expired_at`。包月超 20 会 `PLAN_LIMIT`。

## 4. 📜 输出

stdout 只有一份信封。stderr 是日志，不要把它拼进 JSON，也不要原样念给用户。

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | INVALID_KEYWORD | INVALID_URL | INVALID_ARGS | AUTH_REQUIRED | AUTH_ERROR | TIMEOUT | NETWORK_ERROR | HTTP_5xx | ...",
  "message": "给人读的说明",
  "timestamp": "2026/10/22 15:16:11",
  "request": { "command": "search", "keyword": "露营装备", "limit": 20 },
  "metadata": {
    "skill_version": "1.2.1",
    "runtime_version": "22.x",
    "execution_time": 34210
  },
  "results": []
}
```

- `error` 和 `empty` 时 `results` 为 `null`。
- 搜索、评论成功时 `results` 是数组。
- 详情成功时 `results` 是一个笔记对象，没有评论数组。
- 作品成功时 `results` 是对象，含 `note` 和 `user`。`user.ipLocation` 是驼峰。
- 点赞、收藏、评论、分享、粉丝都是字符串。空字符串和数字 0 可能不返回。
- 向用户只摘标题、作者、互动数、时间和如何打开。图片和视频地址很多，不要把整份 JSON 贴回对话。
- 字段说明见 `assets/output_envelope.schema.json` 和 `assets/*_cli_resp.schema.json`。

成功结果还会写到系统临时目录下的 `xiaohongshu-guaikei/logs/当天日期/`。Windows 一般在 `%TEMP%`，macOS / Linux 在 `os.tmpdir()`。这里不是技能目录，系统清理临时文件后记录会消失。设置 `XHS_GUAIKEI_DISABLE_LOG=1` 可以关闭落盘。

## 5. 🚨 退出码

| error_code | 退出码 | 含义 | 怎么处理 |
| --- | --- | --- | --- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3 | TOKEN 未配置、格式不对，或接口拒绝 | 不要重试。让用户到[小红书笔记作品数据获取官网](https://www.guaikei.com)开通，并配置 `GUAIKEI_API_TOKEN`。格式为 16–256 位字母、数字、下划线或连字符 |
| `INVALID_KEYWORD` | 1 | 关键词长度、链接或特殊符号不合法 | 转述 `message`，请用户换词。不要自动改词再跑 |
| `INVALID_URL` | 1 | 链接或 id 无法识别，或命令和链接类型不一致 | 按第 2 节请用户给出对应链接 |
| `INVALID_ARGS` | 2 | 参数解析失败，或枚举、数量、`expired_at` 不合法 | 按 `--help` 改对后重试一次。不要改成默认值再跑 |
| `PLAN_LIMIT` | 1 | 套餐单次条数超限（常见于包月 Token；后端 14/16） | **禁止同参重试**。转述 `message`；可建议降低 `--limit`（搜索≤40，作品≤30，评论≤20）或到官网升级按量；**须用户同意后再跑** |
| `NO_MATCH`（`status=empty`） | 0 | 没有匹配内容，不是失败 | 如实说没有结果。可建议放宽条件，用户同意后再试 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 任务仍在处理，或网络、单次请求超时。处理中最长大约 15 分钟。搜索、作品、评论大约 20 分钟内会复用；详情大约 19 分钟，等满超时后再跑窗口可能已过 | 告诉用户后最多再试 1 次。不要在宿主刚杀掉进程后立刻连打 |
| `HTTP_429` | 1 | 频率限制 | 降低频率、减小 `--limit`，稍后重试，不要立刻连打 |
| `HTTP_5xx` | 1 | 服务端临时故障 | 等 1–2 分钟再试一次。持续失败就联系支持，并带上 `metadata.execution_time` 和 `request` |
| `"15"` 等其它数字字符串 | 1 | 接口业务错误，含义在 `message` | 按 `message` 说明。不要把所有业务码都当成笔记已删除，也不要原样反复重试 |

## 6. 💡 命令示例

```bash
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20

node src/xiaohongshu/search-cli.js --keyword "多巴胺穿搭" --sort 1 --time 1 --limit 40

node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"

node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/discovery/item/xxx"

node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 20

node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx" --expired_at 365 --limit 20

node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx" --expired_at "2026-10-01 12:00:00" --limit 20

node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 30

node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx" --limit 0
```

包月示例已压在套餐上限内。按量 Token 可加大 `--limit`（技能硬上限 10000）。

## 7. 🚧 不能做的事

能做的只有：搜索公开笔记、读公开详情、读公开评论、读博主公开作品和互动数据。

直接说不支持，不要变通：登录或写操作（发布、点赞、评论、关注、私信）；私密笔记、草稿、仅粉丝可见；创作者后台；用户个人身份信息；报价和聚光等商业化数据。

调用会把关键词或链接发到[小红书笔记作品数据获取](https://www.guaikei.com)。不上传本机文件。结果只供个人或团队内部分析。计费与单次上限以官网为准；**包月**超限为 `PLAN_LIMIT`，不是网络故障。

🎧 开通[小红书笔记作品数据获取 TOKEN](https://www.guaikei.com)。问题见 [GitHub Issues](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)。

参数细则见 [references/options.md](references/options.md)，排查见 [references/troubleshooting.md](references/troubleshooting.md)，更新记录见 [references/changelog.md](references/changelog.md)。

