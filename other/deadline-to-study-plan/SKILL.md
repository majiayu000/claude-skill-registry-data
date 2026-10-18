---
name: deadline-to-study-plan
description: 当学生说"下个月要考 IB 大考不知道怎么安排"、"这几个 DDL 撞在一起了"、"帮我排一下复习计划"时使用。从一个或多个截止日倒推出到期之前的可执行安排：先读清楚已有事项，直接按合理假设排出第一版有交付物的节点，同时把只有本人知道的岔路口（每天多少时间、哪些天动不了）一次问完，拿到答案后修订并提案进日程。不排满、不编造截止日、不给"每天学两小时"这种无法验收的任务。
category: study-planning/planning
version: 0.2.1
status: draft
priority: P0
compatible_agents:
  - claude-code
  - nestudy
  - generic-llm-agent
display_name: 从截止日倒推计划
capabilities:
  - get_events
  - get_profile
  - propose_events
optional_capabilities:
  - resolve_deadline
  - ask_user
outputs:
  - event
max_rounds: 24
suggest_hint: 有几个截止日快到了，用「从截止日倒推计划」把它拆成这周能动手的几件事
---

# 从截止日倒推计划 / Deadline to Study Plan

给定一个或多个截止日，倒推出到期之前该做什么、什么时候做，并提案进学生的日程。

这个 skill 存在的理由是：**学生知道 DDL，也知道该复习，卡住的是中间那一段**——
把"5 月 8 日 IB 物理大考"翻译成"这周三之前把电磁学的错题重做一遍"。

## 何时使用 / When to use

- 学生给出一个明确的截止日，问怎么安排
- 几个 DDL 撞在一起，需要判断先后
- 学生已有的计划落后了，要重排剩下的时间

**不适用于** / Not for：

- 复盘上一周做得怎么样 —— 那是 `weekly-study-review`
- 整理已经发生过的活动经历 —— 那是 `activity-profile-builder`
- 排一整年的申请节点 —— 那是 `application-timeline-builder`

## 需要的输入 / Inputs

| 输入 | 必填 | 说明 |
|---|---|---|
| 截止日 | 是 | 具体日期。学生只说"下个月"就问清楚，**不要挑一个日期替他定** |
| 已有事项 | 是 | 先读一遍。不知道那几天已经排了什么，排出来的计划必然打架 |
| 每天实际可用时间 | 是 | 决定整个计划的形状。**先按 2 小时排出骨架，同一轮用 `ask_user` 问真实值**，拿到之后重排 |
| 学生档案 | 否 | 课程体系与在读科目，用来判断这门课的复习该按什么粒度拆 |

**可用时间这一项最后必须落实。** 按"高中生每天应该能学三小时"排出来又不告诉学生的计划，
第一周就会崩，然后学生会认为是自己不行。所以做法不是"问到了才动手"，而是
**先给一版并把假设写在最上面**——他看着具体的日程说"我哪有 2 小时"，比凭空回答准得多。

## 流程 / Process

1. **读现状**：取回已有事项（尤其是截止日前后那段时间的短期事项）与学生档案。
2. **先排出第一版**：不要停下来等信息。按"每天 2 小时、周末 3 小时"倒推，
   把假设明写在最前面。截止日本身没说清楚是唯一的例外——日期不确定就整份计划都建在沙子上，
   那种情况把日期作为第一个问题问出来，先别排。
3. **同一轮把该问的一次问完**：调 `ask_user`，最多 4 问，问那些**只有他本人知道、
   而且会改变计划形状**的事。典型的两问：

   | 问什么 | 给什么选项 |
   |---|---|
   | 每天实际能拿出多少 | 1 小时以内 / 1–2 小时 / 2–3 小时 / 3 小时以上 |
   | 这段时间有没有动不了的安排 | 周末有课外班 / 有比赛或考试 / 有家庭安排 / 没有 |

   不要问"要不要我帮你排"、"这样可以吗"——第一版已经在他眼前，他会直接说哪里不对。
4. **按答案重排**：调整每日负荷、避开动不了的日子，切成 3–6 个**有交付物的**阶段性节点。
   判据是"做完之后能拿出一个东西来"——一份错题整理、一套做完的真题、一版写完的提纲。
   "复习电磁学"不是交付物，"把电磁学近三年真题做完并订正"是。
5. **落到具体日期**：避开已有事项占满的日子，**在截止日前留出至少 1–2 天缓冲**。
   把最后一天排成"最终检查"而不是"继续赶工"。
6. **提案**：用 `propose_events` 逐条提案为短期事项，`startDate` 是该做完的那天。

跨时区的截止日（申请、境外考试报名）有 `resolve_deadline` 就用它换算；没有时跑下文「没有这些工具时（降级）」里的命令，
结果标「降级计算」。哪种情况都不要口算。

## 输出格式 / Output

第一版（与问题卡同一轮发出）：

```markdown
## 先按这个排了一版
截止：<日期>，距今 <N> 天，其中可用 <M> 天（已避开 <已有安排>）
**假设：每天 2 小时、周末 3 小时** —— 下面的问题答完我按你的实际情况重排

## 节点
1. <日期> —— <交付物>
2. <日期> —— <交付物>
...
<日期> —— 最终检查（不安排新内容）
```

拿到答案后给出修订版，然后调用 `propose_events` 出卡。
**不要先把计划列一遍再问"要不要保存"**，想清楚了就直接出卡。

## 没有这些工具时（降级） / Without these tools (degraded mode)

上面的流程按 nestudy 的工具写。在 Claude Code 或其他没有这些工具的环境里，流程、输出格式和边界都不变，
只把工具换成下表的做法，并在回复开头写明「降级：没有 nestudy 工具，已有安排来自你的描述」。

| 工具 | 没有时怎么做 |
|---|---|
| `get_events` | 读不到已有事项：第一版照常先排，把"还不知道你那几天已经排了什么"写进最上面的假设，同一轮的问题里请他列出截止日前已定的考试、比赛和固定安排 |
| `get_profile` | 从对话里取年级、课程体系和在读科目；没有就按科目本身拆，不为此单独追问 |
| `ask_user` | 在对话里直接问：同样最多 4 问、每问给选项，一次问完，然后停下等他回答 |
| `resolve_deadline` | 跑下面的命令；结果标「降级计算」，打印出的警告和「夏令时切换」行照样转述 |
| `propose_events` | 把修订后的节点写成一张 Markdown 卡片（日期、交付物；日期是该做完的那天），请学生自己存进日历；不说"已加入日程" |

每行一个截止日：`日期 时间 时区 标签`，时区写 IANA 名（ET → `America/New_York`，PT → `America/Los_Angeles`）。
北京时间的截止日也可以用它算「距今 N 天」，时区写 `Asia/Shanghai`。第一个参数是今天（北京时间）的日期，
省略就取本机当天。需要 Python 3.9 以上。

```bash
python3 -c 'import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
bj, utc = ZoneInfo("Asia/Shanghai"), timezone.utc
today = datetime.fromisoformat(sys.argv[1]).date() if len(sys.argv) > 1 else datetime.now(bj).date()
gap = lambda x: f"北京 = 当地 {(x.astimezone(bj).utcoffset() - x.utcoffset()) / timedelta(hours=1):+g} 小时"
for line in sys.stdin.read().splitlines():
    if not line.strip(): continue
    d, t, z, *label = line.split()
    tz = ZoneInfo(z)
    raw = datetime.fromisoformat(f"{d} {t}").replace(tzinfo=tz)
    loc = raw.astimezone(utc).astimezone(tz)
    b = loc.astimezone(bj)
    n = (b.date() - today).days
    print(" ".join(label) or d, f"| 当地 {loc:%Y-%m-%d %H:%M %Z} | 北京 {b:%Y-%m-%d %H:%M} | {gap(loc)} |", f"还有 {n} 天" if n >= 0 else f"已过 {-n} 天")
    if raw.replace(fold=1).utcoffset() != raw.utcoffset(): print("  警告：这个当地时间落在夏令时切换的那一小时里（不存在或出现两次），先向学校确认")
    u = loc.astimezone(utc).replace(minute=0, second=0, microsecond=0)
    prev = (u - timedelta(hours=505)).astimezone(tz)
    for h in range(-504, 505):
        x = (u + timedelta(hours=h)).astimezone(tz)
        if x.utcoffset() != prev.utcoffset(): print(f"  夏令时切换：{x:%Y-%m-%d %H:%M} 起 {prev.tzname()}→{x.tzname()}，在截止之" + ("前" if h <= 0 else "后") + f"；切换前 {gap(prev)}，切换后 {gap(x)}")
        prev = x' 2026-08-04 <<'EOF'
2026-11-06 23:59 America/Los_Angeles 竞赛报名
2026-09-05 23:59 Asia/Shanghai HL物理月考
EOF
```

上例的输出（命令会检查截止时刻前后 21 天内的夏令时切换）：

```text
竞赛报名 | 当地 2026-11-06 23:59 PST | 北京 2026-11-07 15:59 | 北京 = 当地 +16 小时 | 还有 95 天
  夏令时切换：2026-11-01 01:00 起 PDT→PST，在截止之前；切换前 北京 = 当地 +15 小时，切换后 北京 = 当地 +16 小时
HL物理月考 | 当地 2026-09-05 23:59 CST | 北京 2026-09-05 23:59 | 北京 = 当地 +0 小时 | 还有 32 天
```

连命令也跑不了时，把命令交给学生自己运行；拿到结果之前，计划里的北京时间和天数写「待换算」，不填估出来的数。

## 边界 / Boundaries

- **不编造截止日**：学生说不清就问，这是唯一值得先停下来的一问。
  替他假定一个日期，整个计划都建在沙子上。
- **假设必须写出来**：先做不等于替他决定。每一条被假定的前提都要摆在最上面，
  藏起来的假设才是有害的。
- **不排满**：每天排到极限的计划等于没有计划。留缓冲是设计的一部分，不是保守。
- **不给无法验收的任务**："每天学两小时"、"多刷题"、"保持状态"——这些不该出现在提案里。
- **不替学生做取舍**：几个 DDL 冲突且时间确实不够时，把冲突量化摆出来，
  用 `ask_user` 给出取舍选项让他选，不要私下决定哪门课可以放弃。
- **不假装了解学生的实际状态**：没问过的作息、没读到的安排，可以作为**声明过的假设**写进第一版，
  但不能当成已知条件陈述。

## Token 控制 / Token discipline

- 事项一次读齐（带 `withinDays` 覆盖到截止日之后几天即可），不要为每个节点单独去查
- 计划正文不复述读到的原始事项列表，只写会被避开或被依赖的那几条
- 节点控制在 6 个以内；再多学生不会看，也执行不了
- 问题一次问完。运行时对连续追问有硬上限，攒着分两次问只会把额度用光

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.2.1 | 2026-09-26 | 声明兼容 claude-code 却没有降级路径：补「没有这些工具时（降级）」，跨时区截止日无 `resolve_deadline` 时用 `zoneinfo` 命令换算并标「降级计算」，已有事项改为在同一轮问学生、提案改为 Markdown 卡片；"不要口算"改为有工具用工具、无工具跑命令 | patch |
| 0.2.0 | 2026-08-04 | 转向先产出：按声明过的假设直接排出第一版，同一轮用 `ask_user` 把可用时间与固定安排一次问完，不再等信息齐了才动手 | minor |
| 0.1.0 | 2026-08-04 | 初始草稿 | minor |
