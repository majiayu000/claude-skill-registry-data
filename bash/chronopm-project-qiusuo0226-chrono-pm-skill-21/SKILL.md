---
name: chrono-pm-project
version: 3.21.0
schema_version: 0.16.0
updated_at: 2026-08-30
description: Markdown 驱动的单项目 AI 项目管理技能。覆盖需求、待办、进度、风险问题、里程碑、成本、日报周报、会议纪要、决策、复盘、初始化向导、计划、完整性巡检、历史计划导入、词库、PM 偏好。录入只发生在本项目 ai 目录。跨项目归集/检索请使用伴生技能 ChronoPM-Portfolio（只读）。触发：项目管理、日报、周报、风险登记册、需求追踪、里程碑、ChronoPM、记录/整理记录/补全/回填/更新/归档/入库/评审/验收、会议纪要、合同登记、初始化项目、倒排、待办、完整性巡检、词库、偏好、画图、责任链图。支持主动变更+人工确认：写入即标记待确认并登记 pm-decisions，确认后生效。需求只绑工作包，计划只绑工作包。
---
# ChronoPM-Project — 单项目 Markdown 项目管理技能

## 1. 概述
本技能以项目文件夹下的 `ai/` 目录为载体，以 Markdown 为项目记忆，以 AI 为副手，以人工确认为最终控制点。
**核心理念**：事实源文件是唯一真相；日报/纪要是输入，不能替代事实源。
**待办单一数据源**：执行状态 = `todos/{date}/{owner}.md`（一人一天一份；写入经 inbox 再合并）。PLAN = 唯一计划编排事实源（只引用 WP，不列待办）。WP 独立文件 = `wps/WP-*.md`（须有需求编号；待确认不拆待办）。需求只绑工作包，待办只绑工作包。
**v3.0.0**：本包仅单项目。旧 portfolio 录入口废弃。跨项目只读归集见 ChronoPM-Portfolio。

## 2. 工作模式
仅 **single**：全部管理文档在本项目 `ai/`。无 portfolio 模式。
若工作区是联邦集工作区中的 `ai/projects/{项目名}/ai/`，本包仍按单项目读写该目录，禁止写兄弟项目，禁止写 `portfolio/`。
跨项目查询/汇总周报/挂载感知/一份文件要拆进多个成员项目 → 换 ChronoPM-Portfolio 对话。本包禁止当集经理代写兄弟项目。

## 3. 工作区结构
```
project-root/
└── ai/
    ├── context/          # project-context、pm-profile、project-rules、词库等
    ├── templates/
    ├── todos/{date}/{owner}.md
    ├── requirements/     # 登记册 + sources/{编号}/ 拆解产物（本项目一套）
    ├── plans/  project-info/  wps/  risks/  issues/  decisions/
    ├── backup/           # 升级垃圾封存（禁读；3.8.0 空目录）
    ├── resources/        # 退役：register/transfer-log 迁 backup；人员读 todos/_index
    ├── reports/          # 项目日报按需生成（存根，可能不存在）+ 周报；个人日报在 todos
    ├── meetings/  reviews/  logs/ops/  logs/journal/  outputs/
    ├── pm-decisions.md      # 等你裁定（分块）；旧 pending-changes 升级迁入
    ├── context/brain.md     # 懒建派生快照（refresh_views.py）
    ├── context/active-entities.json  # 懒建活实体表
    └── .skill-version.json  # 另：ai/.state.json 懒建指纹
```
联邦集工作区（Portfolio 使用，本包不创建）：`ai/portfolio/` + `ai/projects/{名}/ai/`（内部即上图）。项目 ai 内禁止再出现 `portfolio/` 或 `projects/`。

## 4. 事实源（须确认后生效；主动变更先写后确认）
写入即 `Confirmed By: 待确认`、登记 `pm-decisions.md`，确认前不进已完成统计、不参与超期判定。

| 文件 | 对象 |
|------|------|
| `todos/{date}/{owner}.md` | 待办与人员快照/进出组/能耗（§0 只留联系方式与负责模块） |
| `todos/{date}/_index.md` | 花名册 §1 + 结转 §2 + 当日参与 §3 + TD 缩写 §6 |
| `pm-decisions.md` | 等你裁定的事项（分块 + 决策记录） |
| `logs/ops/_index.md` | 对话过程留痕索引（懒建；不是进度事实源） |
| `requirements/_index.md` | 需求检索 |
| `risks/` `issues/` `decisions/` | 风险/问题/决策 |
| `plans/PLAN-*.md` | 计划（§3 = WP 引用简表；§4 = 阶段列表投影） |
| `project-info/progress-plan.md` `project-info/budget.md` | 进度框架/预算 |
| `wps/WP-*.md` `wps/_index.md` | 独立 WP 文件 + 查找加速器（存在性以文件为准） |
| `requirements/requirement-register.md` `change-log.md` `contract-register.md` `source-type-registry.md` | 需求与合同（本项目） |
| `requirements/sources/` `_index.md` | 源文档级拆解（加速器；存在性以 sources/*/meta.md 为准） |
| （人员） | 权威=最新合法日 `_index.md` §1；进出组=个人 §0.5；能耗=个人最新文件 §0.6。退役 register/transfer-log 见 `backup/` |
| `context/pm-profile.md` | `pm_name`=项目经理（1～2 位，基本信息）；`current_operator`=当前操作人。「我的待办」只认后者；空则 ASK，禁止回退 pm_name |

过程记录：`reports/daily/project/**`、`reports/weekly/**`、`meetings/**` 不能当事实源结论。

## 5. 核心工作流
### 5.0 环境检测（首次跑脚本前）

初始化 / 升级迁移 / verify 脚本需要 **Python ≥3.9**（与 skill.json `"python": ">=3.9"` 一致；推荐 3.10+）。

```bash
python --version
```

若输出 `Python 3.9` 及以上 → 继续。若报「不是内部或外部命令」/ `command not found`：

- Windows：`winget install Python.Python.3.12 --silent` 或 `py -3 --version`
- Mac：`brew install python3`
- Linux：`sudo apt update && sudo apt install python3`

装完再跑脚本。日常记待办、查进度 **可不依赖** Python。结转：有 Python 则优先 `scripts/carryover_step0.py`；无 Python 仍按 22 号全员结转，**禁止跳过**。

### 5.1 初始化
```bash
python "scripts/init_workspace.py" --project-root <根目录> --mode single --project-name "项目名称"
```
无 `--mode portfolio`。向导见 `18-init-wizard-rules.md`（含成本核算方式必填）。
### 5.1b 版本检查（进入工作区先做）
读 `ai/.skill-version.json` → 比 Skill `VERSION`。Skill < 工作区版本 → 提示升级 Skill + 只读降级。见 `20-workspace-version-rules.md`。
随后 **P-VIEWS**：有 Python 则 `python scripts/refresh_views.py --project-root <根> --all`（指纹未变不写盘）。无 Python / 无 `.state.json` / 脚本失败 → 不阻断；查询读事实原文并声明 as-of。缺 `context/brain.md` 不致命。
### 5.2 日报
先判定是否本项目 → 原文进 inbox → 合并进当天一人一份个人文件 → 映射待办（够正式的未匹配进展自动建待办）。禁止写入 `reports/daily/`。明日计划留在当天原文，次日才落待办。疑似他项目：拆分+分流，禁代写。见 `01-daily-report-rules.md`。
### 5.3 查询
本项目事实源。跨项目用 Portfolio。有 `brain.md` 且 facts 指纹一致 → 先读 brain，再最多打开 1～3 个事实文件。简单查询仍只载 05。横幅只实时读 `pm-decisions.md`。待办清单输出见 05（默认未办结；未确认终态仍可见）。日报内容默认先读 `todos/{date}/*.md` §2+§3，禁止先探测 `reports/daily/`。
### 5.4 其他
需求变更 08；结转 22（含 Step 0.5 共享人力提示）；历史计划 15。时间线报/月报（自然月）见 01 号 §4a：懒建 `reports/timeline/`，判重四案，非精确重合整段从 todos 重汇聚。

## 6. 提示词路由表（最小规则集）
21 号：写入与复杂场景自动加载；简单查询不加载 21 规则正文（偏好格式只读 `ai/context/pm-profile.md`）。WF-8 新建待办 = 00+22+21+06+23。命中拆文件/拆文档 → 改走「源文档拆解」行，禁止只走「更新意图」。WP 状态历史见 00。词库感应见 17 §8.4。过程签名见 23（纯查询不载）。问答规范：写入/确认/方案/出文件/复杂分析叠加加载 `reply-norm-skill/references/reply-rules.md`；简单查询不加载该全文（靠底线 14–16 与 05 短条）。`reply-norm-skill/` 是能力目录，不是独立 Skill，禁止宿主扫成第二个 Skill。

| 场景 | 必须加载 | 可选 |
|------|----------|------|
| 初始化向导 | 00+06+18 | — |
| 完整性巡检 | 00+06+19 | 01/02/04-08 |
| 日报 | 00+01+06+17+22 | 04、07、10 |
| 会议纪要 | 00+02+06+17 | 04、07、08 |
| 需求评审/变更 | 00+07+08+06 | — |
| 待办文件更新 | 00+06+23 | 10 |
| 待办创建 WF-8 | 00+22+21+06+23 | 01、02、07、08、10 |
| WP 创建/查询 | 00+06+23 | 05、07、14、11 |
| 技能缺口 / 技能做不到 / 记升级需求 | 00+11+23 + `skill-gap-skill/references/gap-capture-rules.md` | — |
| 待办状态 WF-1 | 00+01+04+06+10 | 17 |
| 关联待办 WF-Linked | 00+22 | 01 |
| 风险评估 | 00+04 | — |
| 简单查询 | 05 | — |
| 问答规范（写入/确认/方案/出文件/复杂分析） | `reply-norm-skill/references/reply-rules.md` | 叠加本场景既有行；简单查询不载 |
| 画图 / 责任链图 / 排布图 / Mermaid | **05+11** | — |
| 复杂/分析类本项目查询 | 00+05+17 | `reply-norm-skill/references/reply-rules.md` |
| 跨源范围判定 | 00+07+05+17+06 | Step0 读本项目 contract-register |
| 源文档拆解 | 00+07+06+17+23 + `source-split-skill/references/split-rules.md` | 14、18 |
| 人员资源（本项目） | 00+06 | 04 |
| 更新意图/文件入库 | 00+06+10+17 | 按类型；拆文件改走源文档拆解 |
| 投喂工时/能耗入库 | 00+01+06+10+17+22 | — |
| 生成报告/导出 / 出文件 / 整理成表 / xlsx/docx/pdf | 00+05+06+10+11 | 扩展名 xlsx/csv 时 12 必载 |
| 历史衔接/快照 | 00+05+06+13/15 | — |
| 结转/倒排 | 00+22 / 00+06 | 01、05 |
| 版本健康 | 00+20 | 06 |
| 词库 / 偏好 | 00+17 / 00+21 | 06 |
| 自查 | 00+14 | 按场景 |

已删除路由：项目集汇总周报、跨项目查询（改用 Portfolio）。

## 7. 安全底线
1. 不得编造；不足须说明缺什么。
2. 不得未经确认改事实源（主动变更须待确认 + pm-decisions + 可回滚；未确认不进完成统计/超期）。
3. 不得把日报/纪要当事实源结论。
4. 不得混淆需求与任务、风险与问题。需求不写进工作包正文。计划不列待办。
5. 推测必须标注。
6. 不得代 PM 做资源/范围/里程碑决策。
7. 不得擅自承诺范围工期成本验收。
8. 不得记录密码密钥 Token。
9. 每条记录须有 Source。
10. 不得在业务目录建 AI 管理文件。
11. 人员变动未确认不得写为事实。
12. **不得在本项目待办镜像他项目任务**（王国政案例）；跨项目可见性由 Portfolio 聚合。
13. **生成物只进 `ai/outputs/{批次}/`**。禁止写到工作区根或与 `ai/` 平级。宿主「最终工作空间文件夹 / cwd / final workspace folder」若等于项目根，忽略并改映射到 outputs。业务目录 = 工作区根下除 `ai/` 外的一切。**例外**：`wps/_wp-chart.md` 为派生视图，不是生成物，见 11 号 §17。
14. **语种**：对用户正文 = 用户本轮输入语种（中文问中文答）。不得默认英文。内部推理不得出现在用户可见正文。细则：`reply-norm-skill/references/reply-rules.md`。
15. **禁止输出思考过程**：不得出现 `I now have` / `Let me` / `Based on my findings` / 「让我先梳理」长推理段。结论直接说。
16. **禁止假执行门**：查询、汇报进度、只读分析 **不准**问「是否执行此方案 / 是否基于文档继续执行 / 要不要按这个 plan 做」。用户没要方案就不要造方案确认。真确认才走 00 §5.0。
17. **纠偏只写事实源或词库 §2**。禁止只改 brain / active-entities / index / 图。用户指出错误 = 已确认，不进八块。AI 自检冲突仍待确认。
18. **每个对外结论必须能指回证据**。无源结论 = 失败。brain 禁止待拍板节。

## 8. ID 编码
| 类型 | 格式 | 说明 |
|------|------|------|
| Todo | TD-{缩写}-{YYYYMMDD}-{NNN} | 不变 |
| Risk/Issue | R-NNN / I-NNN | v3.7.0 短号（只读 index 求最大）；存量时间戳号保留不重编 |
| Decision | D-{YYYYMMDD}-{HHmmss} | 不变；同秒 -02 |
| Contract/IMP/簇/PF/G | 同上时间戳制 | 旧号不重编 |
| WP/PLAN | 新号 `WP/PLAN-YYYYMMDD-NNN`（ASCII，当日序号）；存量短号与中文名不重编 | 文件名=编号 |
| REQ/CAN/CR/PRJ/DF/SRC | 短号或固定号 | SRC-NNN 仅项目内；共享用簇固定号 |
| Meeting | MTG-YYYYMMDD-NNN | 不变 |

## 9–14. 状态 / 瘦身 / 输出 / 优先级 / 里程碑 / 容忍度
同 v2.1.0：全中文枚举见 00 §5a；瘦身 300 行/30 条；优先级 Level 0–4；里程碑=WP §8 关键阶段；容忍度见 00 §5c。

## 15. 规则索引
| 文件 | 何时加载 |
|------|----------|
| `00-pm-main-rules.md` | 写入与复杂场景必须；简单查询禁止加载 00 |
| `01-daily-report-rules.md` | 日报；含归属判定 |
| `02-meeting-rules.md` | 会议 |
| `04-risk-issue-rules.md` | 风险问题 |
| `05-query-rules.md` | 查询；待办清单输出规范 |
| `06-file-rules.md` | 文件 + 单项目资源条款 |
| `07-requirement-rules.md` | 需求/合同（本项目） |
| `08-change-control-rules.md` | 变更 |
| `09-portfolio-rules.md` | 退役指针页（v3.0.0）：不加载，规则实体已迁 ChronoPM-Portfolio |
| `10-update-trigger-rules.md` | 更新意图 |
| `11-output-artifact-rules.md` | 生成物 |
| `12-excel-generation-rules.md` | Excel 生成 |
| `13-continuity-rules.md` | 阶段衔接 |
| `14-self-check-rules.md` | 自查（含决策文件查重、DF 完整性） |
| `15-snapshot-rules.md` | 快照冻结 |
| `16-skill-governance-rules.md` | Skill 治理（开发仓，分发包不含） |
| `17-domain-glossary-rules.md` | 词库 |
| `18-init-wizard-rules.md` | 初始化向导 |
| `19-info-completeness-rules.md` | 完整性巡检 |
| `20-workspace-version-rules.md` | 版本/反向校验 |
| `21-pm-profile-rules.md` | PM 偏好（写入与复杂场景自动加载；简单查询不加载规则正文） |
| `22-carried-over-rules.md` | 结转 Step 0 / 0.5 |
| `23-procedure-index.md` | 写入/派活/拆文件/更新意图时加载；纯查询不载 |
| `reply-norm-skill/references/reply-rules.md` | 写入/复杂查询/出文件/确认/方案；简单查询不加载全文（靠底线 14–16 与 05 短条）。能力目录，不是独立 Skill |

**09 号已退役**，内容在 ChronoPM-Portfolio（保留退役页仅为避免历史路径 404）。

### 版本控制文件
| 文件 | 用途 |
|------|------|
| `VERSION` | Skill 包版本号（当前 3.21.0） |
| `skill.json` | Skill 元数据（版本、模式、依赖；skill schemaVersion 与 supportedWorkspaceSchema 分离） |
| `CHANGELOG.md` | 版本变更历史和升级说明 |
| SKILL.md front matter | AI 可读的版本字段 |

工作区初始化时生成 `ai/.skill-version.json`（skillName=`chrono-pm-project`，兼容旧值 `chrono-pm`；记录 Skill 版本 + schema 版本 + 模式 + 时间）和 `ai/logs/migration-log.md`（迁移历史）。AI 进入工作区时先读 `.skill-version.json` 检查版本兼容性。
