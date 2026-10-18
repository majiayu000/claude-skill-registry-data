---
name: application-timeline-builder
description: 当学生说"申请季怎么安排"、"ED 之前要做完哪些事"、"帮我排一下今年的申请节点"时使用。从各校截止日往回推出整个申请季的时间线：推荐信什么时候要请老师、文书初稿什么时候出、标化什么时候送分，全部换算成北京时间直接排出来落进日程，只把"走哪一轮"这类只有本人能定的岔路口做成选择题一次问完。截止日只用核实过的，本地数据没核实的一律让学生去官网确认后再排。
category: study-planning/admissions
version: 0.2.2
status: draft
priority: P0
compatible_agents:
  - claude-code
  - nestudy
  - generic-llm-agent
display_name: 申请季时间线
capabilities:
  - get_applications
  - get_school_requirements
  - resolve_deadline
  - propose_events
optional_capabilities:
  - get_test_dates
  - get_profile
  - propose_application
  - ask_user
outputs:
  - event
max_rounds: 40
suggest_hint: 申请季快开始了，用「申请季时间线」把各校截止日往回推成这几个月的具体节点
---

# 申请季时间线 / Application Timeline Builder

从各校的截止日往回推，排出整个申请季的节点，并落进学生的日程。

申请季真正杀人的不是文书难写，是**有些事必须提前很久启动**：
推荐信要给老师留几周、送分要留处理时间、成绩单要走学校流程。
学生通常在 10 月底才发现这些事该在 9 月做。

## 何时使用 / When to use

- 申请季开始前，学生想知道整体节奏
- 学生已经定了几所学校和轮次，要排具体节点
- 中途加了一所学校，要看会不会跟已有安排撞车

**不适用于** / Not for：

- 只想换算一个截止日到北京时间 —— 直接用 `resolve_deadline`（没有这个工具就只跑下文降级一节的换算命令），不必起 skill
- 压缩活动栏文案 —— 那是 `activity-list-optimizer`
- 评估现有材料的成色 —— 那是 `admissions-reader`

## 需要的输入 / Inputs

| 输入 | 必填 | 说明 |
|---|---|---|
| 申请清单 | 是 | 哪些学校、走哪一轮。清单空着才问，问就用 `ask_user` 给选项 |
| 各校截止日 | 是 | 优先用申请清单里已有的；没有再查 `get_school_requirements` |
| 学生档案 | 否 | 年级与课程体系，用来判断标化与成绩单的节奏 |

## 截止日的可信度 —— 这一节不能跳

`get_school_requirements` 返回的学校分两种：

- **`verified: true`** —— 有 `deadlines`，核对过官网，可以直接用
- **`verified: false`** —— **没有 `deadlines` 字段**，本地一个日期都没存

看到 `verified: false` 时：

1. **不要把"字段缺席"读成"这所学校没有早申"**
2. **不要凭印象填一个日期。** "藤校 ED 都是 11 月 1 日"这个印象本身就是错的——
   同一年里有学校是 11 月 1 日、有学校因为撞上周末顺延到 11 月 2 日
3. 把该校的 `requirementsUrl` 给学生，请他去官网抄下截止日再回来
4. 拿到之后用 `propose_application` 记进申请清单，这样下次不用再查

返回里的 `unverifiedWarning` 要转述给学生，不要私自吞掉。

## 流程 / Process

1. **读清单**：`get_applications` 拿到已有申请（返回里已经带好北京时间与倒计时，不必再算一遍）。
2. **补缺口**：清单里没有的学校查 `get_school_requirements`；查不到或未核实的按上一节处理。
3. **换算**：所有截止日过 `resolve_deadline` 换成北京时间。
   **`warnings` 里凡是提到夏令时切换的，必须转述**——11 月初 ET 从 EDT 切回 EST，
   北京时间会整整差一小时，而 ED/EA 的截止日正好压在那几天。
4. **直接倒推排完**，对每个已核实的截止日往回排。

   下面的提前量是**保守的排程默认值，不是平台承诺或统一行业标准**；学生、推荐人和学校的实际要求优先。
   最近核对：**2026-09-11**。流程依据：
   [Common App — First-year application guide](https://www.commonapp.org/apply/first-year-students)；
   [College Board — Sending SAT scores](https://satsuite.collegeboard.org/sat/scores/send-scores-to-colleges/sending-scores)。
   这些来源用于核对申请材料与送分流程，**不规定下表的统一提前天数**；表中区间是本 skill 的保守经验值。
   每个申请季开始前应复核这些来源和目标学校官网；若上游流程变化影响默认提前量，更新核对日期并发布 PATCH 版本。

   | 节点 | 相对截止日 | 为什么这么早 |
   |---|---|---|
   | 请老师写推荐信 | 提前 4–6 周 | 老师同时被十几个学生请托，最晚的那批质量最差 |
   | 主文书定稿 | 提前 3–4 周 | 留出补充文书的时间 |
   | 补充文书初稿 | 提前 2–3 周 | 每校一套，数量比想象中多 |
   | 送分 / 成绩单 | 提前 2–3 周 | 走机构与学校流程，不受你控制 |
   | 全部材料自查 | 提前 3–5 天 | 活动栏字符数、各篇文书字数对照上限再核一遍（活动栏交给 `activity-list-optimizer`） |

   **不要问"要不要我排"、"这个节奏可以吗"**——把时间线排出来给他看，他会直接说哪里不合适。
5. **合并同类**：多所学校共用的节点（主文书定稿、送分）合成一条，按**最早的那个截止日**排。
   十所学校排出十条"主文书定稿"是噪音。
6. **只问必须他定的**：清单为空、或某校的轮次不明时，用 `ask_user` 一次问完，给选项：

   > 「<校名> 你打算走哪一轮？」ED / EA / RD / 还没想好

   **ED 是有约束力的承诺，这个决定只能他自己做。** 但也仅此而已——
   提前量、节点粒度、要不要留缓冲这些不用问，按上表排就是。
7. **查冲突**：节点撞上已有的考试或大考月份时点出来，把取舍摆给他。
8. **提案**：`propose_events` 提案为短期事项，`category` 用 `application`，
   这样它们会和申请截止日排在同一条时间线上。

## 输出格式 / Output

```markdown
## 截止日（北京时间）
| 学校 | 轮次 | 当地 | 北京时间 | 剩余 | 来源 |
|---|---|---|---|---|---|
| <校名> | ED | 11-02 23:59 EST | 11-03 12:59 | 90 天 | 已核实 / **待你确认** |

<夏令时或其他 warning 的转述>

## 倒推节点
- <日期> —— <动作>（为了 <哪个截止日>）
...

## 需要你先确认的
- <校名>：本地没有核实过的截止日，去 <requirementsUrl> 抄一下告诉我
```

然后调 `propose_events` 出卡。**待确认的学校不要排节点**——建在假日期上的时间线比没有更危险。
已核实的那几所照排，不要因为有一所待确认就整份都不给。

## 没有这些工具时（降级） / Without these tools (degraded mode)

上面的流程按 nestudy 的工具写。在 Claude Code 或其他没有这些工具的环境里，流程、输出格式和边界都不变，
只把工具换成下表的做法，并在回复开头写明「降级：没有 nestudy 工具，截止日由你从官网抄来，时区由本地命令换算」。

| 工具 | 没有时怎么做 |
|---|---|
| `get_applications` | 请学生贴出申请清单：学校、轮次，以及官网写的截止日期、时间和时区 |
| `get_school_requirements` | 没有核实过的本地数据：每所学校都按上文 `verified: false` 那一路走，请学生去该校官网抄下截止日再排，来源一栏写「官网，学生抄录」。学生凭印象报的日期同样算待确认，不排节点 |
| `resolve_deadline` | 跑下面的命令，所有截止日一次算完；结果标「降级计算」，打印出的警告和「夏令时切换」行照样转述 |
| `get_test_dates`、`get_profile` | 请学生说出已经定下的考试日期、年级和课程体系；他没说的不排、不假设 |
| `ask_user` | 在对话里直接问：同样一次问完、每问给选项，然后停下等他回答 |
| `propose_events`、`propose_application` | 把倒推节点（日期、动作、为了哪个截止日）和已确认的截止日写成一张 Markdown 卡片，请学生自己存进日历；不说"已加入日程" |

每行一个截止日：`日期 时间 时区 标签`。时区写 IANA 名（ET → `America/New_York`，CT → `America/Chicago`，
MT → `America/Denver`，PT → `America/Los_Angeles`，英国 → `Europe/London`）；官网没写具体时间的按 23:59 算，
并注明这是默认值。第一个参数是今天（北京时间）的日期，省略就取本机当天。需要 Python 3.9 以上。

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
2026-11-02 23:59 America/New_York Duke ED
EOF
```

上例的输出（命令会检查截止时刻前后 21 天内的夏令时切换）：

```text
Duke ED | 当地 2026-11-02 23:59 EST | 北京 2026-11-03 12:59 | 北京 = 当地 +13 小时 | 还有 91 天
  夏令时切换：2026-11-01 01:00 起 EDT→EST，在截止之前；切换前 北京 = 当地 +12 小时，切换后 北京 = 当地 +13 小时
```

连命令也跑不了时，把命令交给学生自己运行；拿到结果之前，截止日表格里的北京时间一栏写「待换算」，
不填估出来的时间。

## 边界 / Boundaries

- **不编造截止日**。这是本 skill 最硬的一条。没有核实过的日期，宁可让时间线缺一块。
- **不按往年推**：申请截止日每年都可能动（撞周末就顺延），去年的日期不是今年的依据。
- **不心算时区**：有 `resolve_deadline` 就全部走它；没有时跑下文「没有这些工具时（降级）」里的命令，结果标「降级计算」。
  夏令时提示（工具的 `warnings`，或命令打印的警告与「夏令时切换」行）一律转述。
- **不替学生决定申哪些学校、走哪一轮**：ED 是有约束力的承诺，这个决定不属于 AI。
  用 `ask_user` 问，不要按"多数人会选 ED"排。
- **不承诺"按这个做就来得及"**：时间线是脚手架，实际进度取决于学生。
- **不排满**：申请季本来就有临时冒出来的事，每周留出空档。

## Token 控制 / Token discipline

- `get_applications` 一次读齐，它已经带了换算结果；只有清单外的学校才另外调 `resolve_deadline`
- `get_school_requirements` 按平台或校名取，不要无参数拉全量
- 表格里只放会用到的字段，不要把数据集原样倒出来
- 多所学校的轮次攒成一张卡问完；运行时对连续追问有硬上限

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.2.2 | 2026-09-26 | 声明兼容 claude-code 却没有降级路径：补「没有这些工具时（降级）」，截止日改由学生从官网抄录、时区用 `zoneinfo` 命令换算并标「降级计算」、写入改为 Markdown 卡片；"不自己算时区"改为有工具用工具、无工具跑命令；自查节点去掉学生在日程里用不了的 `check_activity_limits`、`count_essay_words`，改写成动作 | patch |
| 0.2.1 | 2026-09-11 | 标明倒推提前量是经验默认值，补充核对日期、流程来源与上游变化时发布 PATCH 的维护约定 | patch |
| 0.2.0 | 2026-08-04 | 转向先产出：已核实的学校直接排完整时间线，不再等所有信息齐；轮次选择改用 `ask_user` 一次问完 | minor |
| 0.1.0 | 2026-08-04 | 初始草稿 | minor |
