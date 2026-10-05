---
name: publisher-wechatsync
description: Use when the user has a finished blog master draft and wants to publish it to multiple content platforms (知乎/掘金/CSDN/公众号 等) via the @wechatsync/cli tool. Handles pre-flight auth checks, platform selection, dry-run preview, and the actual sync. Do NOT use for writing, rewriting, compliance rewriting, or topic selection — this skill only publishes existing drafts as-is.
---

# Publisher Wechatsync

这个 skill 只负责一件事：把已经写完的博客母稿通过 `@wechatsync/cli` 发到多个平台的草稿箱。

边界很明确：

- 负责：预检、平台选择、dry-run、真正同步、结果汇报
- 不负责：改写正文
- 不负责：大陆合规脱敏
- 不负责：生成平台版标题、摘要、封面图
- 不负责：替换母稿里的外链
- 不负责：删除或修改源文件

一句话原则：这一层只做"把现有 md 送到各家草稿箱"这一段,改写是另一个 skill 的事。

## Working Scope

适用场景:

- 用户说"把这篇发到知乎和掘金"
- 用户说"同步到公众号草稿箱"
- 用户说"这篇母稿写完了,帮我发出去"
- 用户说"先 dry-run 一下看看能发到哪里"

不适用场景:

- 用户说"帮我改成公众号风格"
- 用户说"过一下合规"
- 用户说"帮我补摘要/封面/标题"
- 用户说"从 URL 抓取正文"

以上任意一种都不在这个 skill 的边界内。停住,告诉用户"发布 skill 不做改写,这是另一段流程"。

## Required Inputs

每次执行前至少要拿到:

1. **源文件路径**:一个已写完的 `.md` 文件路径(例如 `path/to/your-article.md`)
2. **目标平台列表**:逗号分隔的平台名(例如 `zhihu,juejin,csdn`)

可选补充:

- `--title`:显式覆盖标题(默认从 frontmatter 或首个 `#` 提取)
- `--cover`:封面图 URL 或本地路径(知乎/公众号/小红书需要)

## Preconditions

开始前必须先确认这 3 件事:

1. **CLI 已安装**
   - 执行 `which wechatsync` 能拿到路径
   - 执行 `wechatsync --version` 不报错
   - 如果没装,告诉用户运行 `npm install -g @wechatsync/cli` 再回来
2. **Chrome 扩展已连通**
   - 用户需要安装 Wechatsync Chrome 扩展,并开启「同步桥接 / MCP Connection」
   - 扩展里会显示一个 Token
   - 用户把 Token 写进环境变量:`export WECHATSYNC_TOKEN="xxx"`
   - 端口默认 9527,如果占用,用 `SYNC_WS_PORT` 覆盖
3. **目标平台已登录**
   - 用户需要先在 Chrome 里登录目标平台(知乎、掘金、CSDN 等)的网页版
   - 扩展用的是当前浏览器的 Cookie,没登录就发不了
   - 用 `wechatsync platforms -a` 查各平台登录状态

如果上面任何一条没满足,停住报错,不要试图绕过。

## Output Contract

这个 skill 的标准输出:

1. 预检报告(CLI 版本、Token 是否配置、目标平台登录状态)
2. dry-run 预览(将要发到哪几个平台、文件路径、标题)
3. 用户确认后的真正同步结果(每个平台是否成功、草稿链接或 id)
4. 一句总结,告诉用户下一步要去哪些平台后台审核

不生成任何中间文件。不修改源文件。不写入仓库任何位置。

## Workflow

### Step 1: 接收输入并自检

先做这几件事:

1. 读 `CLAUDE.md` / `AGENTS.md`,确认当前仓库流程允许发布
2. 确认用户要发的文件确实存在
3. 运行 `which wechatsync`,确认 CLI 可用
4. 运行 `echo $WECHATSYNC_TOKEN | wc -c`,确认 Token 非空

任意一条失败就停住,别继续。

### Step 1.5: 规整化图片路径(预处理)

Obsidian 写出的 markdown 默认会把图片路径 URL 编码(空格变 `%20`,中文字符也被编码),wechatsync CLI **不会自动 decode**,直接发会导致图片全部跳过。

每次发布前**必须**先跑预处理:

```bash
python3 scripts/normalize_image_paths.py "<md 文件路径>" --dry-run
```

看预览:

- 如果 `找不到: 0`,跑一次去掉 `--dry-run` 的版本,原地修正
- 如果 `找不到` 大于 0,停住,先排查图片文件到底在哪。不要带着 broken 图去发
- 如果 `已修复: 0`,说明这篇不需要预处理,直接进下一步

脚本做的事:
- URL decode 所有 markdown 图片链接
- 解析到实际文件(先按相对路径,再按仓库根)
- 重写为 markdown 文件所在目录的相对路径
- 外链(http/https/data)不动

预处理对 Obsidian 完全兼容 —— Obsidian 既接受编码路径也接受未编码路径,改完继续在 Obsidian 里看没问题。

### Step 2: 列出并确认目标平台

如果用户没指定平台,默认只发 `zhihu,juejin` 两个技术平台:

- 知乎、掘金的合规门槛最低
- CSDN 需要手动过审,可以加
- 公众号需要提前准备封面图和摘要,要单独确认
- 小红书、头条对标题和封面要求更硬,单独确认

推荐分组:

- `tech-min`: `zhihu,juejin` — 默认,合规成本最低
- `tech-full`: `zhihu,juejin,csdn,segmentfault,oschina` — 技术平台全家桶
- `with-wechat`: 在上面基础上加 `wechat`,但要同时传 `--cover` 和确认标题
- `social`: `xiaohongshu,weibo,toutiao` — 社交向,注意平台对风格差异敏感

跑一次 `wechatsync platforms -a` 把当前登录状态调出来,不要直接假设。

### Step 3: 先跑 dry-run

**必须先 dry-run,不允许直接实跑。**

```bash
wechatsync sync "path/to/your-article.md" -p zhihu,juejin --dry-run
```

把 dry-run 输出完整贴给用户,让用户确认:

- 解析到的标题对不对
- 目标平台列表对不对
- 文件路径没搞错

只要用户说"不对",停住,别修正后直接跑。先问清楚问题在哪。

### Step 4: 用户确认后实跑

用户明确说"可以"或"发"之后,去掉 `--dry-run` 再跑一次同样的命令:

```bash
wechatsync sync "path/to/your-article.md" -p zhihu,juejin
```

如果要传封面或自定义标题:

```bash
wechatsync sync "path/to/your-article.md" \
  -p zhihu,juejin,wechat \
  -t "可能改过的标题" \
  --cover "path/to/cover.png"
```

### Step 5: 汇报结果

同步完成后,按每个平台列一行结果:

- ✓ 成功:平台名 + 草稿 id 或链接
- ✗ 失败:平台名 + 错误原因

错误最常见的几类:

- `未登录`:让用户去那个平台网页版登录后重试
- `超时`:Chrome 扩展掉线,重启扩展或重开浏览器
- `图片上传失败`:正文里有外链图片,某些平台拉不到
- `内容超长/过短`:平台有字数限制

### Step 6: 收尾提示

给用户一句收尾话:

- 告诉用户每个平台的草稿箱在哪里手动审核
- 提醒这是草稿,需要在平台后台预览 → 配封面 → 手动点发布
- **不要替用户去点「发布」按钮**

## Hard Constraints

- **禁止**未经用户确认就跑非 dry-run
- **禁止**跳过 Step 1.5 的图片路径预处理
- **禁止**发布前改写正文(那是另一个 skill 的事)
  - 注意:预处理只改图片路径,不算改写正文
- **禁止**自动补合规脱敏
- **禁止**替用户在平台后台点「发布」
- **禁止**跳过 `wechatsync platforms -a` 就假设平台已登录
- **禁止**把失败结果悄悄吞掉,要完整透传错误

## Reference Commands

```bash
# 安装
npm install -g @wechatsync/cli

# 版本检查
wechatsync --version

# 平台列表(带登录状态)
wechatsync platforms -a

# 查某个平台登录状态
wechatsync auth zhihu

# 预览(dry-run,不实跑)
wechatsync sync article.md -p zhihu,juejin --dry-run

# 实跑
wechatsync sync article.md -p zhihu,juejin

# 带标题和封面
wechatsync sync article.md -p zhihu,juejin,wechat -t "自定义标题" --cover ./cover.png

# 从当前浏览器页面反向抽取(不常用)
wechatsync extract -o out.md
```

## Environment Variables

- `WECHATSYNC_TOKEN`:和 Chrome 扩展里的 Token 保持一致,**必填**
- `SYNC_WS_PORT`:WebSocket 端口,默认 9527,只有端口冲突时才改

## Troubleshooting

| 报错 | 原因 | 解法 |
|---|---|---|
| `已有实例正在运行但 Chrome Extension 未连接` | 扩展没开同步桥接 | 打开扩展 → 启用 MCP Connection → 确认 Token |
| `连接超时` | 扩展挂了 / Token 不一致 | 重启扩展,重新导出 Token,重新 `export` |
| `未登录 zhihu` | 当前 Chrome 没登录 | 去 zhihu.com 登录后,再跑 `wechatsync auth zhihu -r` 刷新 |
| `图片上传失败` | 正文外链图片拉不到 | 图片先本地化到 `assets/`,再重跑 |

## Workflow Position

- 上游:一份已经写完、改完、确认可发的 `.md` 母稿(写作工具不限)
- 本层:只做同步,不改写
- 下游:用户到各平台后台手动点「预览 → 发布」

一句话定位:**这是创作链路的终点,不是终稿的润色层**。
