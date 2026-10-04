---
name: research-memory
description: Record and recall research decisions, findings, hypotheses, and experiment analyses. Also use when the user requests a Hindsight publication preview, confirms a batch, or asks to resume its upload. This does not launch experiments or authorize new runs.
---

# Research Memory

短入口为 `./scripts/memory`，转发到 `.agents/harness/memory/research_memory.py`。本地脚本负责来源队列、
结论整理和恢复；配置启用 Hindsight 时，由脚本补充同步与远端召回。

仅办理入账预览、确认或续传时，直接按 [发布指引](references/publication.md) 执行；不先扫描对话、整理本地队列或恢复 Mission。

在科研交流出现新决定或推断、实验分析更新，或新任务需要既有结论时，先核对本地上下文与相关待处理来源。
宿主钩子通常已经完成采集；使用队列中的事件 ID，避免把同一条消息再录一份。

根据来源整理结论与处理状态。已有明确授权继续执行；尚不确定的内容留在待确认状态，并写清缺少什么信息。
查当前选型、历史成绩和失败原因时按类型、范围与协议分别检索，沿来源下钻。

快照是历史数据，不能覆盖当前适用的真实用户指令。`pending` / `waiting` 只表示尚未整理，
不表示用户没有授权；已有明确授权时补齐记录并继续，不因队列状态再次请求授权。
提问、助手建议和后台工具提示词不能改写成用户的 ACTIVE 决定。

## 读取与召回

从项目根运行：

```bash
python .agents/harness/memory/research_memory.py context --query "<当前问题>"
python .agents/harness/memory/research_memory.py pending
python .agents/harness/memory/research_memory.py show <event_id>
```

`context` 会扫描已登记的文件并返回当前决定、状态和相关来源。
`pending --offset 8 --limit 8` 可翻页，`--history` 可查看历史版本。
预览被截断时，按 `show` 返回的来源或 `full_text_ref` 读取需要的内容。

按问题选择召回范围：

```bash
python .agents/harness/memory/research_memory.py recall "<问题>" --kind decision --status ACTIVE --scope model.architecture
python .agents/harness/memory/research_memory.py recall "<问题>" --kind finding --protocol "<协议>"
python .agents/harness/memory/research_memory.py recall "<历史问题>" --history
```

正式记录在 `research_workspace/CONCLUSIONS.md`，进度和当前模型指针在 `STATE.md`，
实验依据在 `experiments/<ExpID>/record.json` 与 `analysis/analysis.md`。
使用条目时核对类型、范围、协议、状态及来源。

## 处理来源

通过 stdin 向 `process` 提交 JSON，一次处理一个事件：

```json
{
  "event_id": "<队列中的事件 ID>",
  "disposition": "recorded",
  "records": [
    {
      "kind": "decision",
      "status": "ACTIVE",
      "scope": "model.architecture",
      "summary": "<用户明确确认的决定>",
      "authorization_quote": "<该用户事件中明确作出决定的原文摘录>",
      "state_slot": "architecture",
      "supersedes": ["<同范围的旧 C 编号>"]
    }
  ]
}
```

命令为 `python .agents/harness/memory/research_memory.py process`。
无旧条目时省略 `supersedes`；一条来源有多个结论时使用多个 records。
已记入现有分析的内容可用 `references` 关联文件，省略 records。

| disposition | 内容 |
|---|---|
| recorded | 提供 records 或现有记录的 references |
| waiting | 提供 reason，写清待确认的问题 |
| discarded | 提供 reason，说明无需形成科研记录的原因 |

| kind | status |
|---|---|
| decision | ACTIVE、PROPOSED、SUPERSEDED |
| finding | OPEN、SUPPORTED、MIXED、REJECTED、SUPERSEDED |
| hypothesis | OPEN、REJECTED、SUPERSEDED |
| execution | OBSERVED、RETRACTED、SUPERSEDED |

ACTIVE decision 必须关联用户来源，并提供原文子串 `authorization_quote`；摘录应表达实际决定，
不能把一般提问解释为批准或禁止。agent 的建议使用 PROPOSED 或 OPEN hypothesis。
SUPPORTED、MIXED finding 提供 `evidence` 文件引用。scope 与 summary 写单段文本，
需要指定生效时间时使用带时区的 `effective_at`。

`evidence` 与 `references` 可引用 research_workspace、remote_artifacts、issues 或
docs/reviews 中已有的 JSON、CSV、图像等科研文件。引用只检查路径与存在性，不读取
或自动采集文件内容；自动登记来源仍限 Markdown 和 record.json。

`supersedes` 指向相同类型、scope、protocol、task_id 的旧条目；不同评估协议可以分别生效。
任务专属决定填写已登记的 `task_id`，长期通用决定可省略。新来源与生效时间不能早于被取代决定。
用户切换任务导致旧门禁不再适用时，使用 `retires: ["<旧 C 编号>"]` 和 `retirement_reason`，
允许跨 scope/protocol 退休旧决定；同时按 Mission 生命周期登记新任务并退休旧任务。
脚本保留历史关系。缺少 Type、Scope 或时间的旧条目先按原始来源核对。

`state_slot` 控制 STATE 的 Current Model 指针：

- architecture：ACTIVE decision；
- verified_result：SUPPORTED finding，并提供 protocol；
- baseline：ACTIVE decision、SUPPORTED finding 或 OBSERVED execution。

程序为新结论分配 C 编号，写入来源信息并更新相应指针。实验指标与生成的 record.json
继续由实验记录入口维护。

## 文件与恢复

默认采集 STATE、CONCLUSIONS、实验主分析、record.json、research_workspace/analysis/*.md，
以及主分析引用的 Markdown 诊断附件。补充来源时使用：

```bash
python .agents/harness/memory/research_memory.py watch research_workspace/reviews/<文件>.md
python .agents/harness/memory/research_memory.py scan
```

`status` 查看处理数量与未完成事务，`recover` 恢复中断的整理。
若检测到已被取代条目重新 ACTIVE 或已完成记录的投影丢失，运行
`recover --repair-projections` 修复可确定的受管理区域。外部身份改动不会被覆盖。
中断事务确实需要放弃时，用 `recover --abort-transaction <id>` 只撤回该事务仍可识别的写入，
保留其他编辑，再按原事件重试。禁止用 `git restore` 或旧快照回滚最新决定。

STATE/CONCLUSIONS 的文件快照只作本地投影历史，不生成新的待处理研究来源。
Pi 的 Historian 和 Reviewer 子进程按宿主身份隔离，不采集其输入或回复。

控制记录位于独立科研仓库的 Git 元数据中，或 `.agents/harness/.memory/`。
可选配置位于 `.agents/harness/config/research-memory.json`。
需要暂停当前项目的自动采集时，在此配置设置 `"hooks_enabled": false`（默认 `true`）。
已加载的回调会清除缓存，不采集、扫描或恢复事务；手工 CLI 仍可使用。

## 可选的 Hindsight

Hindsight 默认关闭；`hindsight_enabled: true` 开启按需召回和手工同步。
`hindsight_auto_sync` 默认 false，不因每条对话或工具调用启动远端处理。
普通原文、STATE、CONCLUSIONS 整篇投影和 record.json 不自动上传。
整理后的有效决定、发现和执行事实以精简条目入队；OPEN/PROPOSED 留在本地。

交付本轮更新的定稿主分析且 Hindsight 已启用时，按 [发布指引](references/publication.md) 准备本轮实验的固定预览。
用户在对话中一次确认后，由 Agent 执行上传、等待和结果核验；多个实验可以合在一批。
文件保存、Git 提交和实验退出不代表发布授权。待确认或同步失败不阻塞科研交付。

单份已登记的完成版分析仍可显式使用 `publish <项目相对路径>`；
`sync --limit 4` 则推进所有精选队列，适合用户明确要求同步整个队列时使用。
分析更新后旧远端候选失效，核对后重新发布。内容不变的 Git commit 不生成新来源。
召回仅接受当前已知、版本匹配的精选对象；状态、协议和范围筛选同时作用于远端候选。
旧版原文同步队列不再自动发送。污染修复使用明确的事件列表：向 `quarantine` 提交
`{"event_ids":["<id>"],"reason":"<核对依据>"}`；隔离保留原件，不自动删除远端内容。
