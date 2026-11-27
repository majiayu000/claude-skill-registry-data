---
name: xiaohongshu-yunying-zhushou
description: "一站式小红书运营工具，融合选题灵感、数据分析模块。支持爆款标题、热点选题、粉丝分析等，覆盖小红书运营数据获取场景。支持四大能力：(1) 关键词搜索笔记/视频，可按点赞数、评论数、收藏数、发布时间、内容类型筛选排序；(2) 博主作品抓取，按主页链接获取博主的互动数据（粉丝量、点赞量或收藏量等）或公开作品列表；(3) 笔记（视频）详情，获取详情数据及互动数据等；(4) 笔记评论分析，按笔记链接获取评论内容与互动数据。用户提到小红书/xhs/rednote 且需要查数据、做选题、竞品监控、KOL筛选、评论舆情分析时调用；给关键词或链接即可，无需登录账号"
license: MIT
version: 1.2.3
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

# 📊 小红书运营分析助手

> 一站式小红书运营工具，融合选题灵感、数据分析模块。支持爆款标题、热点选题、粉丝分析等，覆盖小红书运营数据获取场景。

> 💡 给一个关键词或一条链接，拿回小红书公开笔记、评论和博主数据。不登录，不发布。结果是一份 JSON，AI 可以直接接着做选题、竞品和舆情。

| 你要做的事 | 用哪个命令 | 你拿到什么 |
| --- | --- | --- |
| 🔍 找选题、看高赞 | `search-cli.js` | 笔记数组。点赞、收藏、评论、分享都是字符串 |
| 📰 看一篇笔记的正文 | `detail-cli.js` | 一个笔记对象。不含评论 |
| 💬 看评论区 | `comment-cli.js` | 评论数组 |
| 📸 看博主作品 | `post-cli.js --limit 大于 0` | `results.note` 笔记数组，以及可能有的 `results.user` |
| 👥 看粉丝、获赞、收藏 | `post-cli.js`，不传 `--limit` 或 `--limit 0` | `results.user`。`fans` 粉丝，`liked` 获赞，`collected` 收藏，`interaction` 获赞与收藏 |

**🔥 适合放进 Agent 的原因**

- **🔒 只读**：不登录小红书账号，无发布、点赞、评论、关注
- **💪 一次最多 1 万条**：互动数是字符串，空字符串和数字 0 可能不返回
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

## 1. ⚠️ 执行前置（每次必过）

1. **先 `cd` 到本 SKILL.md 所在目录**，再执行 `node src/xiaohongshu/*.js`（或用绝对路径，见 [faq.md](references/faq.md)）。
2. **确认 `GUAIKEI_API_TOKEN` 已配置**。未配置 → 不执行，走 `AUTH_REQUIRED`（见 §7 / [errors.md](references/errors.md)），禁止先跑「试试看」。
3. **一次只跑一条命令，等进程自己结束**。查询最多约 20 次退避，只算等待大约 15 分钟。stderr「处理中」不是失败。**未退出前不要判定失败，不要并发/重复同一命令。**
4. **必填参数不齐先追问**（话术见 [ask.md](references/ask.md)），禁止猜测关键词或链接。
5. **Windows 拼参：cmd 只用双引号**包含空格/中文/URL 的参数；不要用 bash 单引号。引号仍拆坏 → 改用 `--json-args`（[faq.md](references/faq.md)）。Windows / 弱模型优先 `--json-args`。

> 开通[小红书运营分析助手](https://www.guaikei.com) TOKEN。配 TOKEN / 落盘 / FAQ → [faq.md](references/faq.md)。

## 2. 💎 价值与典型场景（10 秒判断该不该用）

| 你是谁 | 你要做的事 | 用哪个命令 |
| --- | --- | --- |
| 创作者 / 运营 | 找爆款选题、看高赞图文共同点 | `search-cli.js --sort 2` |
| 品牌 / 投放 | 监控已知博主发文与互动 | `post-cli.js`（要作品须显式 `--limit`） |
| 内容分析 | 看一篇笔记正文、图片、互动 | `detail-cli.js` |
| 舆情 / 客服 | 评论区在吐槽还是在夸 | `comment-cli.js` |
| MCN / 商务 | 看粉丝、获赞、收藏 | `post-cli.js --limit 0` |

**何时用**：用户提小红书/小红薯/xhs/rednote，并要搜、看、分析公开数据；或给了笔记/主页/短链/id。

**何时不用**：只写文案不查数；平台是抖音/快手/B 站/微博/公众号；要登录、私密、草稿、创作者/商业化后台。

**为什么用它**：只读、不登录；零第三方依赖；按量单次最多 1 万条；stdout 纯 JSON、日志走 stderr。

> **合规**：调用会把关键词/链接发到 `www.guaikei.com`。不上传本地文件。仅公开数据，限个人/团队内部分析。

## 3. 🎯 识别卡（选命令，命中即停）

| 用户要什么 | 命令 | 最少要有 |
| --- | --- | --- |
| 搜笔记、爆款、选题 | `node src/xiaohongshu/search-cli.js` | `--keyword` |
| 一篇笔记的正文 / 为什么火 | `node src/xiaohongshu/detail-cli.js` | 笔记链接或 24 位笔记 id |
| 一篇笔记的评论 / 舆情 | `node src/xiaohongshu/comment-cli.js` | 笔记链接或 24 位笔记 id |
| 博主作品、粉丝、获赞 | `node src/xiaohongshu/post-cli.js` | 主页链接或 24/29 位 `user_id` |

- 正文和评论都要：先 `detail-cli`，再 `comment-cli`。
- 24 位 id / 短链类型不明：先追问（[ask.md](references/ask.md)），禁止两个命令都试。
- App 分享文案可整段粘贴给 `--url`，命令会自动抽链（保留 `xsec_token`）。

## 4. 🛠️ 命令一行例（详参下沉）

> **详参 / 枚举**：需要确认取值时再读 [options.md](references/options.md) 。**不要每次都读。**  
> 注意：`-t` = 内容类型，`-i` = 发布时间。`--time 2` = 一周内；`--sort 2` = 最多点赞。  
> **Windows**：cmd **只用双引号**；PowerShell 含空格也优先双引号。仍拆坏或弱模型 → `--json-args`。双壳例 → [faq.md](references/faq.md)。

```bash
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20
node src/xiaohongshu/search-cli.js --keyword "多巴胺穿搭" --sort 1 --time 1 --limit 40
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx" --limit 20
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx" --expired_at 30 --limit 20
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx" --limit 30
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx" --limit 0
```

**Windows 双壳（同一条搜索，先 cd 到技能目录）**：

```bat
REM cmd —— 参数必须用双引号，不要用单引号
node src\xiaohongshu\search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20
```

```powershell
# PowerShell —— 含空格/中文同样用双引号
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20
```

**数量 / 套餐**：搜索默认 **20**；评论默认 **10**；博主不传 `--limit` 默认 **0**（只有博主信息）。不要擅自抓 10000。技能硬上限 10000（按量）。**包月**超限 → `PLAN_LIMIT`：搜索 ≤40，作品 ≤30，评论 ≤20；详情无此条数限制。

口语 → flag 对照 → [routing.md](references/routing.md)。

## 5. 🔀 意图路由（按序命中即停）

```
1. 评论/留言/舆情 + 对象是一篇笔记 → comment-cli
2. 作品/主页/账号/博主/粉丝/获赞 → post-cli
3. 一篇笔记的标题/正文/图片/互动 → detail-cli
4. 有关键词且无以上信号 → search-cli
5. 都不明确 → 先追问（ask.md）
```

消歧：`/user/profile/` → 只能 post；`/explore/` 或 `/discovery/item/` + 评论 → comment，+ 正文 → detail，都没说 → 追问。选题可先 `search --sort 2 --time 2 --limit 30`，再对挑出的笔记跑详情。竞品看作品必须显式 `--limit`。

## 6. 📜 输出（摘要）

- stdout = 统一 JSON 信封；stderr = 日志。向用户**只摘关键字段**，勿整份粘贴。取数成功/empty 时信封顶层可能有 `cost`（花费估算，见 [contract.md](references/contract.md)）。
- `status=empty` + `NO_MATCH` 退出码 0，**不是失败**。
- `results`：搜/评论 = 数组；详情 = 单对象；作品 = `{note,user}`。
- 互动数是字符串；比较前先转数字。

完整信封与形态 → [contract.md](references/contract.md)。Schema 在 `assets/`。

## 7. 🚨 错误应对（摘要）

| error_code | 退出码 | Agent |
| --- | --- | --- |
| `AUTH_*` | 3 | **禁止重试**；引导官网配 TOKEN |
| `PLAN_LIMIT` | 1 | **禁止同参重试**；降 limit 须用户同意（搜≤40 / 作品≤30 / 评论≤20） |
| `INSUFFICIENT_BALANCE` / `DAILY_LIMIT` | 1 | **禁止同参重试**；充值或明日/调限额 |
| `RATE_LIMITED` | 1 | **禁止立即重试** |
| `INVALID_*` | 1/2 | 换词/换链/按 help 改一次；禁止擅自改默认再跑 |
| `NO_MATCH` | 0 | 如实无结果 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 同参续等最多 1 次（搜/作品/评论约 20 分钟、详情约 19 分钟复用）；禁止改参「重做」 |

全表 → [errors.md](references/errors.md)。

## 8. 🛑 硬性禁止

- 不得编造数据；不得把空结果说成有结果。
- 不得未征得同意就自动改搜索条件重试；不得编造关键词或链接。
- `AUTH_*` / `PLAN_LIMIT` / `INSUFFICIENT_BALANCE` / `RATE_LIMITED` / `DAILY_LIMIT` 后不得同参或立即重试。
- 不得把 stderr 原文转述给用户；不得整份 JSON 贴回对话。
- 不得做登录态/私密获取或任何写操作。
- 不得在未 cd 到技能目录时执行 `node src/xiaohongshu/*.js`。
- 24 位 id / 短链类型不明时，不得两个命令都试。

## 9. 📚 何时读 references（入口总表）

| 时机 | 打开 |
| --- | --- |
| 确认枚举/参数取值 | [options.md](references/options.md) |
| 口语指令 → flag / 链接消歧 | [routing.md](references/routing.md) |
| 信封 / `results` 形态 | [contract.md](references/contract.md) |
| 完整错误表 | [errors.md](references/errors.md) |
| 缺参追问话术 | [ask.md](references/ask.md) |
| 环境 / FAQ | [faq.md](references/faq.md) |
| 逐步排障问答 | [troubleshooting.md](references/troubleshooting.md) |
| 版本变更 | [changelog.md](references/changelog.md) |
| 技术人员总览 | [readme.md](readme.md) |
| 机器可校验 Schema | `assets/*.schema.json` |
