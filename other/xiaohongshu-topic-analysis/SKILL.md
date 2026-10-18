---
name: xiaohongshu-topic-analysis
description: 当用户需要做小红书选题、xhs内容选题、rednote笔记选题策划、爆款角度拆解、内容方向规划或选题素材整理时使用。面向内容运营、品牌调研和创作者。
license: MIT
version: 1.1.4
category: 数据分析
platforms: [WorkBuddy, Openclaw, QClaw, ima, Claude Code, Cursor]
homepage: https://github.com/um-why/xiaohongshu-openclaw-skill
metadata:
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins: ["node"]
    env: ["GUAIKEI_API_TOKEN"]
  env_desc:
    GUAIKEI_API_TOKEN: "小红书数据API访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通。"
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
  examples:
    - "帮我找最近一周小红书『露营装备』的高赞图文笔记 → node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --time 2 --limit 20"
    - "这条小红书笔记评论区在吐槽什么 → node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 200"
    - "看这个小红书博主最近 30 条作品发什么 → node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 30"
    - "分析这篇小红书爆款笔记为什么火 → node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
    - "监控『多巴胺穿搭』最新动态 → node src/xiaohongshu/search-cli.js --keyword '多巴胺穿搭' --sort 1 --time 1 --limit 50"
---

# 小红书选题分析

> ✨ **一句话**：给关键词或链接，拿回结构化的小红书公开数据——笔记、评论、博主作品，直接喂给后续的选题分析、竞品对比、舆情归纳。

> ✨ **解决什么问题**：小红书运营最费时间的不是写内容，是「先搞清楚该写什么」。人工翻 50 条笔记记录点赞收藏要一小时，本工具一条命令返回 50 条结构化数据，AI 直接接着做归纳。

| 你要做的事     | 这个技能给你什么                         | 省掉的动作             |
| -------------- | ---------------------------------------- | ---------------------- |
| 找选题方向     | 按点赞/收藏排序的笔记列表 + 完整互动数据 | 手动翻页、逐条记录数据 |
| 盯竞品账号     | 博主公开作品列表 + 发布时间 + 互动表现   | 每天手动刷对方主页     |
| 筛 KOL 真实性  | 点赞/评论/收藏三项原始数值               | 靠感觉判断数据是否注水 |
| 摸用户真实想法 | 单篇笔记的评论区全量数据                 | 手动往下翻评论         |
| 追热点         | 按「最新」+「一天内」筛出的实时内容      | 反复刷发现页           |

**🔥核心优势**

- **🔒 安全**：不登录你的小红书账号，零封号风险——这是爬虫方案给不了的
- **💪 强大**：单次最多拉取 **1 万条**数据，出参字段全面，可见即所得
- **🎛️ 精准**：内容类型 / 排序 / 时间范围 / 数量四维筛选，直出你要的那批数据
- **🪶 轻量**：零依赖、零部署，装好 Node.js 就能跑，Windows / macOS / Linux 通吃
- **🤖 为 AI 而生**：标准 JSON 出参 + 完整 SKILL.md，WorkBuddy / Openclaw / Claude Code / Cursor 等 Agent 开箱即用
- **📁 省心**：每次执行结果自动归档本地日志，写周报、做复盘直接翻记录

---

## 1. ✅ 什么时候应该调用这个技能

### 1.1 🎯 满足以下**任一**条件即调用

- 用户提到「小红书」「小红薯」「xhs」「rednote」并要求查看、搜索、分析内容
- 用户要做 **关键词搜索**、**爆款选题调研**、**竞品监控**、**评论洞察**、**博主作品追踪**、 **KOL/博主筛选**、**评论区舆情分析**、**关键词趋势跟踪**。
- 用户提供了小红书关键词、笔记链接或博主主页链接，希望拿到结构化数据。
- 用户给出 `xiaohongshu.com` 或 `xhslink.com` 开头的链接
- 用户说「帮我看看 XX 在小红书上的情况」这类需要真实数据支撑的判断
- 用户后续还要基于结果继续做总结、对比、筛选、报告生成。

### 1.2 🚫 以下情况**不要调用**

- 用户只让写文案、起标题、改脚本，没要求查数据
- 用户查询的平台是抖音、B站、微博、公众号
- 用户要求获取私密内容、登录态数据、隐藏数据或非公开信息。
- 用户既没有提供关键词，也没有提供可识别的小红书链接，且任务目标不明确。

### 1.3 👀 意图模糊时的追问模板

用户说「帮我做小红书竞品分析」——信息不足，按此追问：

> 需要确认三件事：1）竞品是具体某个账号（给我主页链接），还是某个品类关键词？2）关注最新动态还是历史高赞？3）大概看多少条？

拿到答案再执行。**不要自行编造关键词或链接。**

---

## 2. 🔀 四个能力与路由

> **Note:** 请先通过 [小红书选题分析官网](https://www.guaikei.com) 开通TOKEN，配置环境变量 `GUAIKEI_API_TOKEN` 后才能正常运行。

| 用户意图信号                          | 脚本                             | 必填        | 返回                                                 |
| ------------------------------------- | -------------------------------- | ----------- | ---------------------------------------------------- |
| 给的是**关键词**，无链接              | `src/xiaohongshu/search-cli.js`  | `--keyword` | 笔记列表 + 作者 + 互动数据 + 可点击 url              |
| 给的是**笔记链接**，要看正文/互动数据 | `src/xiaohongshu/detail-cli.js`  | `--url`     | 笔记详情 + 作者信息                                  |
| 给的是**笔记链接**，只要评论          | `src/xiaohongshu/comment-cli.js` | `--url`     | 评论内容 + 评论者 + 互动数据                         |
| 给的是**博主主页链接**                | `src/xiaohongshu/post-cli.js`    | `--url`     | 作品列表；`--limit 0` 时返回粉丝量、点赞量、收藏量等 |

### 2.1 🧭 路由细则

- 用户给的是 **关键词**，没有链接：走 **关键词搜索**。
- 用户给的是 `https://www.xiaohongshu.com/explore/...` 或可解析到笔记的短链：若只关心评论，走 **笔记评论查询**；若要笔记详情一起看，走 **笔记详情**。
- 用户给的是 `https://www.xiaohongshu.com/user/profile/...` 或可解析到主页的短链：走 **博主作品监控**。
- 如果用户同时给出多个目标，按用户目标拆分执行，不要把不同意图硬塞进一次命令。

### 2.2 ⚖️ detail 与 comment 的区别

- `detail-cli.js`：要笔记本身（标题、正文、图片、点赞收藏数）。
- `comment-cli.js`：只要评论区，不返回正文。

**同时需要正文和大量评论时**：调 `detail-cli.js` 拿正文，再调 `comment-cli.js --limit 500` 拿评论。

### 2.3 🧩 组合工作流

**选题调研**

```
search-cli --sort 2 --time 2 --limit 30    # 先拿一周高赞
→ 挑出前 5 条的 url
→ detail-cli 逐条看正文结构
→ 汇总标题公式 / 开头钩子 / 话题标签
```

**竞品监控**

```
post-cli --limit 30                        # 拿对方近 30 条
→ 按发布时间算更新频率
→ 按互动数据找出爆款
→ comment-cli 拉爆款的评论区看用户为什么买
```

**KOL 筛选**

```
post-cli --limit 20
→ 计算 评论数/点赞数、收藏数/点赞数 比值
→ 比值异常偏低 → 疑似刷量，标记风险
```

---

## 3. 🧺 输入规则

### 3.1 🔍 关键词搜索

| 参数             | 必填 | 取值                                                                       | 默认 |
| ---------------- | ---- | -------------------------------------------------------------------------- | ---- |
| `--keyword` `-k` | 是   | 2-50 字符，不能是链接                                                      | —    |
| `--type` `-t`    | 否   | 内容类型，`0` 全部 / `1` 视频 / `2` 图文                                   | `0`  |
| `--sort` `-s`    | 否   | 排序规则，`0` 综合 / `1` 最新 / `2` 最多点赞 / `3` 最多评论 / `4` 最多收藏 | `0`  |
| `--time` `-i`    | 否   | 发布时间，`0` 不限 / `1` 一天内 / `2` 一周内 / `3` 半年内                  | `0`  |
| `--limit` `-l`   | 否   | 返回数量，整数 1-10000                                                     | `10` |

**参数选择建议**（直接影响结果质量，请按意图选）：

| 用户说                             | 应该传              |
| ---------------------------------- | ------------------- |
| 「爆款」「高赞」「什么内容火」     | `--sort 2`          |
| 「最新」「刚发的」「实时」「现在」 | `--sort 1 --time 1` |
| 「这周趋势」「近期」               | `--sort 1 --time 2` |
| 「大家都在收藏什么」「值得存的」   | `--sort 4`          |
| 「讨论度高」「评论多」             | `--sort 3`          |
| 「文案怎么写」「图文笔记」         | `--type 2`          |
| 「视频怎么拍」                     | `--type 1`          |

`--limit` 建议：快速看一眼 `10`；正经做选题 `30-50`；批量分析 `200+`（注意返回体积，超过 1000 条时告知用户数据量）。

### 3.2 📰 笔记详情

至少要确认：

- `url`：小红书笔记链接。

适用链接示例：

- `https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`
- `https://xhslink.com/m/xxx`

如果用户给的是博主主页链接，不要误走详情脚本，先指出链接类型不匹配。

### 3.3 📡 博主作品监控

至少要确认：

- `url`：小红书博主主页链接。

可选参数：

- `limit`：返回作品数量上限；为 `0` 时返回该博主的互动数据（粉丝量、点赞量、收藏量等）。

适用链接示例：

- `https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy`
- `https://xhslink.com/m/xxx`

如果用户给的是笔记详情链接，不要误走博主脚本，先说明需要主页链接。

### 3.4 💬 笔记评论获取

至少要确认：

- `url`：小红书笔记链接。

可选参数：

- `expire`：有效评论天数筛选，整数 1-4745，不传时默认 2190，即近 6 年。
- `limit`：评论数量上限，整数 1-10000，不传时默认 10。

适用链接示例：

- `https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`
- `https://xhslink.com/m/xxx`

如果用户给的是博主主页链接，不要误走评论脚本，先指出链接类型不匹配。
与「笔记详情」的区别：本能力只取评论数据，不返回笔记正文 / 互动详情，适合只想做评论洞察、观点聚类或舆情分析的场景。

**👉 详细选项说明**, 可参阅 [完整选项说明](references/options.md)

---

## 4. 📜 执行原则

- **缺输入先问**：无关键词 → 追问；无链接 → 追问；链接类型不明 → 确认是笔记还是主页；无 TOKEN → 提醒配置。
- **成功输出**：目标 + 关键参数 + 结构化 JSON 结果，必要时补一小段摘要。
- **失败不编造**：token 无效、链接非法、结果为空、接口异常、超时——如实告知原因。空结果不是成功结论。
- **后续衔接**：结果可继续用于选题汇总、高赞对比、评论聚类、竞品风格总结、发文节奏分析、报告生成。

---

## 5. 🚫 反模式

| 错误做法                                | 后果                 | 正确做法                            |
| --------------------------------------- | -------------------- | ----------------------------------- |
| 主页链接传 `detail-cli` / `comment-cli` | 不返回数据           | 主页走 `post-cli`                   |
| 笔记链接传 `post-cli`                   | 不返回数据           | 笔记走 `detail-cli` / `comment-cli` |
| 关键词纯 emoji / 纯符号                 | 清洗后为空，校验失败 | 换有意义的文字关键词                |
| `--limit 20000`                         | 超上限回退为 10      | 上限 10000                          |
| 查抖音 / 微信                           | 无结果               | 明确告知不支持                      |

---

## 6. 💡 命令示例

```bash
# 关键词搜索：一周内图文，按点赞排序，取 20 条
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20

# 追最新：一天内，按最新排序
node src/xiaohongshu/search-cli.js --keyword "多巴胺穿搭" --sort 1 --time 1 --limit 50

# 笔记详情（不带评论，省 token）
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"

# 只拉评论，做舆情分析
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 200

# 获取一年内评论，剔除一年前无效评论
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 1000 --expire 365

# 博主近 30 条作品
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 30

# 博主互动数据（粉丝量、点赞量、收藏量等）
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 0
```

---

## 7. ❓ 错误速查

| 含义                       | 动作                        |
| -------------------------- | --------------------------- | ------------------------------------------------------------------------------------- |
| `401` / `403`              | TOKEN 未配置或无效          | 核对 `GUAIKEI_API_TOKEN`（16-256 位字母/数字/下划线/短横线），过期去 guaikei.com 重开 |
| `429`                      | 触发频率限制                | 降频、减小 `--limit`，稍后重试                                                        |
| `500` / `502` / `503`      | 服务端临时故障              | 等 1-2 分钟重试；持续失败联系支持                                                     |
| `ERRCODE_xxx`              | 业务错误（如笔记已删除）    | 换链接；重试无效，不要反复重试                                                        |
| `ETIMEDOUT` / `UNKNOWN`    | 网络超时                    | 查网络/代理，确认能访问 guaikei.com                                                   |
| 提示「链接格式无效」       | 链接类型或格式错误          | 见 §3.3 链接支持列表                                                                  |
| `--limit 10000` 只得 10 条 | limit 实际超了 10000 被回退 | 确认 limit 为 1-10000 整数                                                            |
| 搜索返回空且退出码 1       | search 把无结果视为失败     | 换宽泛关键词、放宽筛选；detail/comment 空数组属正常                                   |

排查细节见 [references/troubleshooting.md](references/troubleshooting.md)；完整选项说明见 [references/options.md](references/options.md)；更新记录见 [references/changelog.md](references/changelog.md)。

---

## 8. 🚧 能力边界与合规

**能做**：搜索公开笔记 / 读公开详情 / 读公开评论 / 读博主公开作品与互动数据。

**不能做（直接说不支持，不要变通）**：登录或写操作（发布/点赞/评论/关注/私信）；私密笔记、草稿、仅粉丝可见内容；创作者后台数据；用户个人身份信息；商业化数据（报价、聚光平台）。

**合规**：国内直连无需代理；数据流向 本机 → guaikei.com API → 返回，除查询参数外不上传本机数据；仅处理公开数据；结果限个人/团队内部分析，不得违规分发或用于违法用途。

---

## 9. 🎧 支持信息

- 官网 / TOKEN 开通：[小红书内容方向规划技能官网](https://www.guaikei.com)
- 问题反馈：https://github.com/um-why/xiaohongshu-openclaw-skill/issues
