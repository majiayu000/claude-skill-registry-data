---
name: light-memory-pm
description: 上下文管理、记忆持久化与科研项目管理。当任务涉及长期项目、需要记住项目背景/进展/版本/偏好，或需要把项目拆成阶段任务时使用（常驻）。持续记住研究方向、已定 idea、数据、实验进度、论文/PPT/图表/代码版本、投稿记录、用户偏好、目标期刊。把项目拆成阶段任务并建立任务清单、时间线、里程碑、风险清单与版本记录。
user-invocable: false
---

# 上下文管理、记忆持久化与科研项目管理

## 记忆系统 SSOT 决策表（先查这里，再动手写）
两套记忆系统并存——**跨会话 Light 记忆文件**(user/feedback/project/reference + MEMORY.md 索引)与**项目库 db09**——极易把同一类信息写错地方或两头都写造成漂移。落盘前先按下表定位**唯一权威落点**(SSOT)，再决定是否需 MEMORY.md 索引双写。**铁律**：权威落点只有一个；MEMORY.md 只放**索引行**(指针)，绝不放权威正文。

### 表一：每类信息 → 唯一权威落点 + 是否双写

| 信息类别 | 唯一权威落点(SSOT) | 是否需 MEMORY.md 索引 | 反例(别写这) |
|---|---|---|---|
| 个人偏好(写作风格/工具/格式习惯) | Light **feedback 记忆**文件 | 是(索引行) | 别塞进 db09 project_card |
| 项目背景/进展/状态(idea/数据/实验/版本/投稿) | db09 **project_card.md**(14 字段) | 否(项目内事实不进 MEMORY) | 别写进 feedback/MEMORY 正文 |
| 跨项目过程教训(踩坑/被拒/复现失败/省时避雷) | db09 顶层 **lessons.md** | 否 | 别留在某项目 decision_log 当全局教训 |
| 方法选型事实(某方法适用条件/优劣/基线) | db03 **方法卡** | 否 | 别进 lessons.md(那是过程教训非方法事实) |
| 术语/指标/创新点定名 | db09 项目 **terminology.md** | 否 | 别散落各材料正文 |
| 重大决策时间线 | db09 项目 **decision_log.md** | 否 | 别只记在对话里 |
| 跨会话项目背景/参考资源(供新对话快速恢复) | Light **project/reference 记忆**文件 | 是(索引行) | 别只写 db09(新对话不会自动扫 db09 全库) |

### 表二：边界裁决(易混三对，照此切)

| 看似都能放 | 归属判据 | 落点 |
|---|---|---|
| 偏好 vs 教训 | "我习惯这么做"=偏好；"这么做导致被拒/复现失败"=过程教训 | feedback 记忆 / lessons.md |
| 教训 vs 方法事实 | "三模块纯串联当创新点会被拒"(对任意 CV/ML 成立)=教训；"OC-SORT 适合无 re-id 跟踪"=方法事实 | lessons.md / db03 |
| 项目内决策 vs 跨项目教训 | 带研究方向前提(如"白羊外观同质化弃 re-id")=项目内；剥离方向后仍成立=可上 lessons | decision_log.md / lessons.md(去偏科化后) |

> 写 lessons.md 须**去偏科化**(剥离研究方向前提，抽到对任意学科成立的层面)，a02 起草、归档点由用户拍板(详见下「跨项目教训回写」)。校验工具：`scripts/check_project_card.py`(日期/枚举/行格式/衔接链)、`scripts/version_tag_reconcile.py`(version_history↔git tag 对齐)。

## 持久化（用 Light 记忆系统 + 项目库 db09）
- 跨会话事实写入记忆文件(user/feedback/project/reference)，并在 MEMORY.md 加索引行。其中 **feedback 记忆槽的「跨项目过程教训」部分结构化落地为 db09 顶层 `lessons.md`**（与 `projects/` 平级，格式见下）；feedback 记忆文件本身仍存个人偏好类反馈。
- 项目级状态写入 db09 的 project_card：`project_name, goal, current_stage, confirmed_idea, data_status, method_status, experiment_status, paper_status, ppt_status, code_status, risk_list, next_actions, decision_log, version_history`。
- 相对日期一律转绝对日期再存。
- **两层记忆模型**（借 LangGraph checkpointer/Store 与 mem0 的作用域设计）：会话级状态(≈thread_id，短期、随会话压缩可丢)与项目级状态(≈跨会话的 Store/db09，长期、按"项目"namespace 持久)分开管理。关键事实即使能被自动抽取也要显式写入——自动记忆(mem0 式 LLM 抽取)会漏记，db09 是权威来源。

## 记忆写入机制（招牌功能，硬性定义）
四类记忆文件**存哪、什么格式、何时写、何时读**，照此执行，不得省略。

### 存哪（落盘路径）
全部存到 db09，每个项目一个独立目录（相对本技能目录为 `../../databases/db09-projects/projects/<project_name>/`）：
```
databases/db09-projects/projects/<project_name>/
├── project_card.md       项目卡：14 字段总览（next_actions 在此）
├── terminology.md        术语/指标/创新点统一定义表（供 a07）
├── decision_log.md       重大决策时间线
└── version_history.md    论文/PPT/图表/代码各版本记录
（可选子目录 literature/ reviews/ submissions/ 见 db09 README）
```
`<project_name>` 用短横线英文 slug（如 `dairygoat-detect-track`）。已存在实例可直接参考：`projects/dairygoat-detect-track/`（四文件齐全；version_history.md 在未出正式版本前只记当前态、不编造历史版本）。

### 什么格式（四文件确切结构，模板见 db09 `project_card_template.md`）
1. **project_card.md** — 顶部 YAML frontmatter（`project_name` / `created` 绝对日期），正文 `# 项目卡：<中文标题>`，再用一个 ```yaml 代码块装 14 字段：`project_name, goal, current_stage, confirmed_idea, data_status, method_status, experiment_status, paper_status, ppt_status, code_status, risk_list, next_actions`，末两字段写 `decision_log: 见 decision_log.md`、`version_history: 见 version_history.md`。多行字段用 `|` 块标量。
2. **terminology.md** — Markdown 表：`| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |`，类别取 方法/数据集/指标/创新点；创新点行标准措辞须与论文/PPT/软著一字对齐。
3. **decision_log.md** — 每行一条：`- [YYYY-MM-DD] 决策 — 理由 — 来源(m03/m04/m14…)`。只追加不改写，保留时间线。
4. **version_history.md** — 每行一条：`- [YYYY-MM-DD] 材料(论文/PPT/图/代码) vN — 变更摘要`，与 git tag 对齐（见下「管理工具映射」）。

## 该记什么
项目背景、研究问题、已确认 idea、数据情况、实验进度、论文/PPT/图表/代码各自版本、投稿与审稿记录、用户偏好(写作风格/工具/格式)、目标期刊、格式要求、重要决策(decision_log)。
**不记**：代码结构、git 历史、能从仓库直接看出的东西。

## 项目阶段拆解
把项目拆成：资料调研→idea 构思→方案确认→数据准备→实验实现→结果分析→论文写作→图表制作→投稿准备→答辩展示→成果转化。每阶段建：
- **任务清单**(可勾选)、**时间线/甘特**、**里程碑**、**风险清单**、**版本记录**。
- 落到工具时：一个阶段=一个里程碑(GitHub milestone，带 due 日期)，阶段内任务=带 `- [ ]` 复选框的条目，风险项打 `risk` 标记。`- [x]` 用于已完成项，便于自动统计进度。

## 管理工具映射（见 a09，具体用法/端点/参数见 references.md）
- **代码/文本/稿件版本→Git**：里程碑用带注释标签 `git tag -a v1.2.0`（注释标签才被 `git describe` 识别），遵循 SemVer，论文/PPT 也打 tag 并与 version_history 对齐；CHANGELOG 按 Keep a Changelog；大文件交 DVC；`git push --tags` 才上传。
- **数据/实验→DVC / MLflow / W&B**：DVC `dvc add` 生指针、`dvc.yaml` 定 stage、`dvc exp run`+`metrics diff`；MLflow `start_run`+`log_param/metric/artifact` 串 run_id；W&B `init/log`+Artifacts 血缘+Sweeps，记 run URL。data_status/experiment_status 挂对应 commit/run。
- **文献→Zotero**、**项目知识→Obsidian/Notion/Logseq/Markdown**、**进展→README+CHANGELOG**：各自的 API 基址、限流、字段映射见 references.md。

## 更新纪律（硬性）
每次完成：资料搜索、idea 修改、实验运行、论文修改、PPT 修改、投稿返修——**立即**更新 db09 对应字段与 decision_log，避免长期项目上下文丢失。

**触发→写入对照**：idea 定稿→改 `confirmed_idea` + 追加 decision_log；实验跑完→改 `experiment_status` + `next_actions`；论文/PPT/代码出新版→改对应 `*_status` + 追加 version_history（并打 git tag）；方案变更/取舍→追加 decision_log；新术语/指标/创新点定名→补 terminology.md。

**B-fact 引用三件套（硬性，禁裸写数值）**：写 decision_log/data_status 引用 **venue 计量(h_index/被引/分区) / 数据集许可/DOI / 外部数值** 时,不当 db09 自带权威,必带三件套——**快照值(可带 ≈) + `[snapshot YYYY-MM-DD, src=dbNN:文件#定位, 用前重核, 冲突信在线]`**(venue 回指 db01:venues.csv、数据集回指 db04 卡、色值回指 db05 DTCG;palette.json 是样板)。**读卡恢复状态时**:带 last_checked 的快照若超期(计量 >90 天/许可 >365 天)给"需重核"提示,不直接当当前值汇报,投稿/用前以在线(venue_signal.py)或官方源重核。

**跨项目教训回写（节制，避免噪声）**：仅当某决策产生了**可跨项目复用的过程教训**——踩坑、被审稿/导师否掉、复现失败、某流程显著省时/避雷——才在追加 decision_log 的**同时**回写一条 lesson 到 db09 顶层 `lessons.md`（格式：`- [YYYY-MM-DD] 阶段/场景 — 做法 — 结果(有效|失败) — 适用条件 — 来源项目slug`）。日常项目内决策**不强制**回写。边界：方法选型事实归 db03 方法卡，个人偏好归 feedback 记忆，二者不进 lessons.md。**去偏科化（回写时）**：lesson 须剥离研究方向前提、抽到对任意学科成立的层面(如"三模块纯串联当创新点会被拒,须有方法层 delta"对任何 CV/ML 成立=可上;"白羊外观同质化弃 re-id"带方向前提=留 decision_log 不上 lessons);a02 起草、归档确认点由用户拍板。

### 写入步骤示例（落地一次实验进展）
刚跑完检测 baseline（项目 `dairygoat-detect-track`）的五步：① **读现状**：Read project_card.md 看 `experiment_status`/`next_actions` 当前值；② **改项目卡**：Edit 把 `experiment_status` 改为带具体指标的实测描述（如「E1 baseline 已跑：YOLOv11@1280，mAP 0.71」），同步勾掉/替换 `next_actions` 首条；③ **追加决策日志**：decision_log.md 末尾加 `- [日期] 决策 — 理由 — 来源`；④ **记版本**：有可复现 tag 则 version_history.md 加行并 `git tag -a`；⑤ **跨会话索引**：涉用户长期偏好/项目背景则写 Light 记忆文件 + MEMORY.md 索引行。日期一律绝对日期（今天=系统 currentDate）。

## 会话开始时
先读项目库与记忆：定位 `databases/db09-projects/projects/<project_name>/project_card.md`，**优先读 `next_actions` 字段**确认"上次做到哪、下一步是什么"，必要时再读 decision_log 末几条与 version_history。会话长时被压缩后，靠 db09/记忆而非短期记忆恢复状态。

**跳过已归档项目**：罗列/恢复项目时跳过 project_card 带非空 `archived:` 字段的项目，只在活跃项目里恢复状态；除非用户点名该归档项目。完结项目按「项目归档协议」（见 `references.md`）加 `archived: 日期` + 回写终版 lessons，不删目录、不挪路径。

**复用历史教训**：新项目立项，或选定方法/投稿策略**前**，先 Grep db09 顶层 `lessons.md` 检索同类"阶段/场景"关键词（如 `方案确认`/`数据准备`/`投稿`）的历史有效做法；命中可复用的，在写 decision_log 时注明"复用自 lesson [日期]"。

## 会话衔接（主动交接）
本技能是会话衔接协议的执行者（全局纪律见 `CONVENTIONS.md §9`）。当上下文将尽或一段任务收尾时，**主动**给用户留种，让下一个对话零成本接上——区别于 orchestrator §0 的被动断点恢复（事后救火），这是事前留种。

**四类触发**（宁早勿晚，阶段边界默认触发）：T1 上下文水位（对话很长/已读大量文件/感知到压缩摘要/用户说"快不行了"）、T2 任务完成（收尾主动给"下一步"提示词）、T3 阶段切换（orchestrator 检查点通过前）、T4 用户索要（"给我衔接提示词/开新对话继续"）。注意：单纯"继续写这段/继续润色"是单技能续写，不触发交接。

**两件套产出**（触发时同时交付）：①衔接卡落盘 `.light/handoff/S<NN>-<slug>.md`（模板 `templates/handoff_card.md`，与 passport.yaml 同级，`<NN>` 两位递增）；②按 `templates/handoff_prompt.md` 填好具体值后**打印**一段中文启动提示词，用户复制→新开对话→粘贴即续。无项目目录的轻对话只打印提示词、不落卡（已知局限）。

**自包含 + 自传播**：每张卡独立可读，下一个 agent 只读最新卡即可续上；沿卡内 `parent_session` 链可追到任意上级对话。每个接手会话收尾必须再造下一张卡 + 提示词，协议才不断链。衔接卡 ≠ 当前事实：接手后仍按 orchestrator §5 刷新 git/passport/db09/CI 证据。

> 完整触发判据、落盘规则、与断点恢复的关系见 `references/session_handoff.md`。
> 特定客户端：Hermes 多会话/压缩主链恢复（查 `state.db` 的 `parent_session_id`/`archived`/`cwd` 复原完整会话链）见 `references/hermes_session_lineage_recovery.md`——通用协议优先，此为单客户端细节。

## 衔接
是所有技能的状态中枢：m01–m17 的产出都在此登记，a06 的目录与之对应。

---
各工具的真实端点/参数/已知坑见 `references.md`。
