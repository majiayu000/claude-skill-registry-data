---
name: research-collector
description: Use when the user wants to collect research material for an article or topic by gathering YouTube videos and web articles into a NotebookLM notebook, then running analysis queries and saving results as markdown. Best for "收集素材"、"给我找这个话题的相关视频和文章"、"整理成 NotebookLM 分析" type requests. Combines yt-dlp YouTube search, NotebookLM `nlm` CLI research, and markdown report output.
---

# Research Collector

这个 skill 只做一件事:

- 为某个主题批量收集 YouTube 视频 + 网页文章,喂进 NotebookLM,跑分析查询,把结果落地到本地目录(默认 `./research/<topic>/`,可配置)

不负责:

- 写成品文章(交给你自己的写作工具 / skill)
- 选主标题
- 下载视频(交给本仓库里的 `yt-dlp-direct` skill)
- 发布到多平台(交给本仓库里的 `publisher-wechatsync` skill)

一句话原则:用户说"帮我收集 X 话题的素材"或"拉一批 YouTube + 文章到 NotebookLM",就走这条固定流水线,不要每次重新设计。

## When To Use

适用场景:

- 用户要为某个话题写推荐/测评/观点文,需要先做背景研究
- 用户说"帮我找 X 的热门 YouTube 视频和文章"
- 用户说"收集到 NotebookLM 里分析"
- 用户说"给我整理一份 X 话题的素材研究"

不适用场景:

- 用户已经有明确素材清单,只想要总结 → 直接跑 `nlm notebook query`
- 用户要做的是实时对话研究,不需要持久化到 notebook → 用 WebSearch + WebFetch
- 用户只要下载单个视频 → 用 `yt-dlp-direct`

## Preconditions

开始前必须确认:

1. `nlm` CLI 已安装且登录:`nlm login --check`
2. `yt-dlp` 在 PATH 中:`which yt-dlp`
3. 用户明确说明了主题和角度
4. 输出目录可写(默认 `./research/<topic>/`,可以通过 `RESEARCH_OUTPUT_DIR` 环境变量或对话里直接指定其他路径)

前置不满足时:

- `nlm login --check` 失败 → 让用户跑 `nlm login`,session 有效期 ~20 分钟
- `yt-dlp` 没装 → 停止并告诉用户

## Working Rules

- 先和用户对齐主题、角度、量级,再动手
- 每轮 ytsearch 默认 15 条,可以根据需要调整
- NotebookLM deep research 一次只能跑一个任务,不能并发
- 添加 source 时每条之间 sleep 2 秒,避免限流
- 所有产出(原始 JSON + 汇总 markdown)落到 `./research/<topic>/` 下(或用户指定的目录)
- 这个 skill 只负责收集和分析,不要擅自接着写成品文章
- 不要删 notebook,用户后面可能还要回去跑 query

## Core Workflow

### Phase 0: 对齐目标

在动手前必须和用户明确:

1. **主题是什么**(要一句话能喂给 ytsearch 的关键词)
2. **角度**(比如"最常用 + 个人创作" vs "最新发布 + 技术细节")
3. **笔记本命名**(默认 `<主题> 素材`)
4. **量级**(默认:15 油管 + deep research 自动 ~40 网页)

### Phase 1: 创建笔记本 + 设 alias

```bash
nlm notebook create "<话题> 素材"
# 从输出提取 ID,然后:
nlm alias set <short-name> <notebook-id>
```

alias 取短名,比如 `skills-research`、`vps-2026`,后续所有命令都用 alias。

### Phase 2: yt-dlp ytsearch 找热门 YouTube

并行跑 2-3 个不同角度的搜索,每个 15 条:

```bash
yt-dlp --simulate --print "%(title)s|%(webpage_url)s|%(view_count)s|%(uploader)s" \
  "ytsearch15:<关键词 A>"
yt-dlp --simulate --print "%(title)s|%(webpage_url)s|%(view_count)s|%(uploader)s" \
  "ytsearch15:<关键词 B>"
```

输出里的 JS runtime warning 可以忽略。

从结果里按以下规则筛 top 15:

- 去重(同一视频出现在多个搜索里)
- 优先官方账号(比如 Anthropic、OpenAI 等)
- 按 view count 从高到低,但要留 2-3 个垂直向角度的中腰部视频,避免全是爆款通稿
- 每个角度至少保留 5 条

### Phase 3: 把 YouTube 加为 source

用 bash 循环逐条加,每次 sleep 2 秒:

```bash
cat > /tmp/yt_urls.txt <<'EOF'
https://www.youtube.com/watch?v=XXX1
https://www.youtube.com/watch?v=XXX2
...
EOF

while IFS= read -r url; do
  echo "=== Adding: $url ==="
  nlm source add <alias> --url "$url" 2>&1 | tail -5
  sleep 2
done < /tmp/yt_urls.txt
```

偶尔会遇到单条失败(视频不公开、区域限制),忽略继续,最后报告成功率。

### Phase 4: 跑 NotebookLM deep research 发现网页文章

```bash
nlm research start "<英文查询,适合 web 研究>" \
  --notebook-id <alias> --mode deep
```

deep 模式 ~5 分钟,返回 ~40 条网页源。

**关键:一个 notebook 同一时间只能有一个 research 任务在跑**。如果要跑第二轮,必须等第一轮 import 完或 --force。

等待完成:

```bash
nlm research status <alias> --max-wait 360
```

Bash 工具默认 timeout 120 秒,必须加 `timeout: 400000`(即 400 秒)。

### Phase 5: 导入 research 结果

研究完成后从输出里拿 task-id,然后:

```bash
nlm research import <alias> <task-id> --timeout 600
```

Bash 工具加 `timeout: 700000`。

**注意**:用户有时会说"素材够了,不用再导入",要停下来直接进 Phase 6。

### Phase 6: 跑 3 个分析查询

默认跑 3 个角度,命令直接重定向到文件避免输出过大:

```bash
mkdir -p "./research/<topic>"

nlm notebook query <alias> "<问题 1 的中文提示>" \
  > "./research/<topic>/query1-<slug>-raw.json" 2>&1

nlm notebook query <alias> "<问题 2 的中文提示>" \
  > "./research/<topic>/query2-<slug>-raw.json" 2>&1

nlm notebook query <alias> "<问题 3 的中文提示>" \
  > "./research/<topic>/query3-<slug>-raw.json" 2>&1
```

**每个 query 的 Bash 调用要加 `timeout: 240000`。**

默认 3 个查询模板(按需改关键词):

1. **Top 清单**:"基于所有 source,请列出被最多来源推荐的 Top 10 X。对每个 X 说明:(1) 名称 (2) 具体做什么 (3) 主要使用场景 (4) 推荐它的来源数量 (5) 类型分类。按推荐频率从高到低,用中文输出。"
2. **目标读者向**:"我要写一篇面向 <读者画像> 的文章。请筛选出对 <读者> 最有帮助的 Top 8 X,每个说明:(1) 名称 (2) 具体痛点 (3) 典型用法一句话 (4) 类型 (5) 最具体的来源编号。去掉不相关的,聚焦 <场景>,用中文。"
3. **入门 + 坑**:"针对 <读者> 使用 X 时,请总结:(1) 最快入门方式 (2) 去哪里获取 (3) 最容易踩的 5 个坑 (4) 什么时候其实不需要 (5) 最新的重要更新。每点配来源编号,用中文。"

### Phase 7: 抽取 answer 字段,生成汇总 markdown

原始输出是 JSON 包含 answer + citations,用 Python 抽 `value.answer` 字段:

```bash
python3 <<'PY'
import json, pathlib
base = pathlib.Path("./research/<topic>")
files = [
    ("query1-<slug>-raw.json", "## Query 1:<标题>"),
    ("query2-<slug>-raw.json", "## Query 2:<标题>"),
    ("query3-<slug>-raw.json", "## Query 3:<标题>"),
]
out = ["# <话题> 素材研究", "",
       "> 基于 NotebookLM 笔记本 `<notebook-name>` 的分析结果", "",
       "---", ""]
for fname, heading in files:
    out.append(heading)
    out.append("")
    raw = (base/fname).read_text()
    try:
        data = json.loads(raw)
        out.append(data.get("value",{}).get("answer",""))
    except Exception as e:
        out.append(f"(解析失败: {e})")
    out.append("")
    out.append("---")
    out.append("")
(base/"素材研究汇总.md").write_text("\n".join(out))
print("Written:", (base/"素材研究汇总.md").stat().st_size, "bytes")
PY
```

## Output Contract

执行完要给用户报告:

1. Notebook 名字 + alias + 实际 source 数量
2. 3 份 raw JSON 和 1 份汇总 markdown 的落盘路径
3. 失败/跳过的 source(如果有)
4. 汇总文件的头部预览(前 20 行左右)
5. 建议的下一步(交给用户决定下游怎么用,本 skill 到此结束)

## Safety and Boundaries

- 不要默认跑 audio/video/slides 生成,这些费配额,用户没要就不碰
- 不要自动跑第二轮 research,一轮够用绝大多数场景
- 不要覆盖已有的 `素材研究汇总.md`,如果存在先追加 `-v2`
- 研究查询里不要塞用户私密信息(notebook 是可搜索的)

## Troubleshooting

### nlm login 失效

```bash
nlm login --check  # 会告诉你是否有效
nlm login          # 重新登录
```

session 有效期约 20 分钟。

### yt-dlp 搜索结果没输出

先看版本:

```bash
yt-dlp --version
```

如果太旧提示用户更新。JS runtime / ffmpeg 的警告可以忽略,不影响 `--simulate` 模式。

### research 超时或卡住

单独查状态(不阻塞):

```bash
nlm research status <alias> --max-wait 0
```

如果 status 一直是 in_progress 超过 10 分钟,用 `--force` 重开:

```bash
nlm research start "..." --notebook-id <alias> --mode deep --force
```

### query 输出太大无法直接看

所有 query 都重定向到文件,再用 Python 抽 answer,不要尝试在终端直接打印大 JSON。

### source add 连续失败

- 检查是否有限流 → 增大 sleep 到 3-5 秒
- 检查 URL 格式(YouTube 要用 `watch?v=` 标准格式,不用 shorts/live)
- 检查登录态 → `nlm login --check`

## References

- NotebookLM CLI 完整指引:`notebooklm-mcp-cli`(pip 包,作者 jacob-bd)随附的 nlm-skill,或上游 README https://github.com/jacob-bd/notebooklm-mcp-cli
- yt-dlp 命令库:同仓库 `../yt-dlp-direct/SKILL.md`
- 项目自身约定:如果你的工作目录有 `CLAUDE.md` / `AGENTS.md`,本 skill 不强依赖,可选阅读
