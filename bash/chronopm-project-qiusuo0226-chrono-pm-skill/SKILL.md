---
name: chrono-pm-project
version: 3.5.1
schema_version: 0.10.0
updated_at: 2026-08-20
description: Markdown 驱动的单项目 AI 项目管理技能。覆盖需求、待办、进度、风险问题、里程碑、成本、日报周报、会议纪要、决策、复盘、初始化向导、计划、完整性巡检、历史计划导入、词库、PM 偏好。录入只发生在本项目 ai 目录。跨项目归集/检索请使用伴生技能 ChronoPM-Portfolio（只读）。触发：项目管理、日报、周报、风险登记册、需求追踪、里程碑、ChronoPM、记录/更新/归档/入库/评审/验收、会议纪要、合同登记、初始化项目、倒排、待办、完整性巡检、词库、偏好。支持主动变更+人工确认：写入即标记待确认并登记 pending-changes，确认后生效。
---
# ChronoPM-Project — 单项目 Markdown 项目管理技能

## 1. 概述
本技能以项目文件夹下的 `ai/` 目录为载体，以 Markdown 为项目记忆，以 AI 为副手，以人工确认为最终控制点。
**核心理念**：事实源文件是唯一真相；日报/纪要是输入，不能替代事实源。
**待办单一数据源**：执行状态 = `todos/{date}/{owner}.md`；PLAN = 唯一计划编排事实源（§3 只引用 WP）；WP 独立文件 = `wps/WP-NNN.md`；WP 进度 / 日周计划 / todo 索引 / WP 索引均为派生或加速器。
**v3.0.0**：本包仅单项目。旧 portfolio 录入口废弃。跨项目只读归集见 ChronoPM-Portfolio。

## 2. 工作模式
仅 **single**：全部管理文档在本项目 `ai/`。无 portfolio 模式。
若工作区是联邦集工作区中的 `ai/projects/{项目名}/ai/`，本包仍按单项目读写该目录，禁止写兄弟项目，禁止写 `portfolio/`。
跨项目查询/汇总周报/挂载感知 → 换 ChronoPM-Portfolio 对话。

## 3. 工作区结构
```
project-root/
└── ai/
    ├── context/          # project-context、pm-profile、project-rules、词库等
    ├── templates/
    ├── todos/{date}/{owner}.md
    ├── requirements/     # 登记册 + {type}-source/ 拆解产物（本项目一套）
    ├── plans/  wps/  risks/  issues/  decisions/
    ├── resources/        # 本项目人员（建议建；含他项目名指针）
    ├── reports/          # 项目日报按需生成（存根，可能不存在）+ 周报；个人日报在 todos
    ├── meetings/  reviews/  logs/  outputs/
    ├── pending-changes.md
    └── .skill-version.json
```
联邦集工作区（Portfolio 使用，本包不创建）：`ai/portfolio/` + `ai/projects/{名}/ai/`（内部即上图）。项目 ai 内禁止再出现 `portfolio/` 或 `projects/`。

## 4. 事实源（须确认后生效；主动变更先写后确认）
写入即 `Confirmed By: 待确认`、登记 `pending-changes.md`，确认前不进已完成统计、不参与超期判定。

| 文件 | 对象 |
|------|------|
| `todos/{date}/{owner}.md` | 待办与人员快照/进出组/能耗 |
| `todos/{date}/_index.md` | 当日人员绑定 |
| `pending-changes.md` | 待确认变更 |
| `risks/` `issues/` `decisions/` | 风险/问题/决策 |
| `plans/PLAN-*.md` `progress-plan.md` `budget.md` | 计划/进度/预算（PLAN §3 = WP 引用简表） |
| `wps/WP-*.md` `wps/_index.md` | 独立 WP 文件 + 查找加速器（存在性以文件为准） |
| `requirements/requirement-register.md` `change-log.md` `contract-register.md` `source-type-registry.md` | 需求与合同（本项目） |
| `resources/resource-register.md` `transfer-log.md` | 本项目人员 |

过程记录：`reports/daily/project/**`、`reports/weekly/**`、`meetings/**` 不能当事实源结论。

## 5. 核心工作流
### 5.1 初始化
```bash
python "scripts/init_workspace.py" --project-root <根目录> --mode single --project-name "项目名称"
```
无 `--mode portfolio`。向导见 `18-init-wizard-rules.md`（含成本核算方式必填）。
### 5.1b 版本检查（进入工作区先做）
读 `ai/.skill-version.json` → 比 Skill `VERSION`。Skill < 工作区版本 → 提示升级 Skill + 只读降级。见 `20-workspace-version-rules.md`。
### 5.2 日报
先 §1.0 录入归属判定 → 存档 §2 → 映射待办。个人日报落 `todos/{date}/{owner}.md`（§2 存档 + §3 工作日志），禁止写入 `reports/daily/`。项目日报为按需生成的存根（`reports/daily/project/`，可能不存在）。疑似他项目：拆分+分流，禁代写。见 `01-daily-report-rules.md`。
### 5.3 查询
本项目事实源。跨项目用 Portfolio。待办清单输出见 05 号新节（默认未办结；未确认终态仍可见）。日报内容（含「昨天日报风险点/问题」）默认先读 `todos/{date}/*.md` §2+§3，禁止先探测 `reports/daily/`；仅用户明确要项目日报文件时才读 `reports/daily/project/`（目录不存在=未生成，不报错）。
### 5.4 其他
需求变更 08；结转 22（含 Step 0.5 共享人力提示）；历史计划 15。时间线报/月报（自然月）见 01 号 §4a：懒建 `reports/timeline/`，判重四案，非精确重合整段从 todos 重汇聚。

## 6. 提示词路由表（最小规则集）
21 号在所有输出场景自动加载。WF-8 新建待办 = 00+22+21+06；04/07/08 仅关键词命中才加载。

| 场景 | 必须加载 | 可选 |
|------|----------|------|
| 初始化向导 | 00+06+18 | — |
| 完整性巡检 | 00+06+19 | 01/02/04-08 |
| 日报 | 00+01+06+17 | 04、07、10 |
| 会议纪要 | 00+02+06+17 | 04、07、08 |
| 需求评审/变更 | 00+07+08+06 | — |
| 待办文件更新 | 00+06 | 10 |
| 待办创建 WF-8 | 00+22+21+06 | 01、02、07、08、10 |
| WP 创建/查询 | 00+06 | 05、07、14 |
| 待办状态 WF-1 | 00+01+04+06+10 | 17 |
| 关联待办 WF-Linked | 00+22 | 01 |
| 风险评估 | 00+04 | — |
| 本项目查询 | 00+05+17 | 按问题 |
| 跨源范围判定 | 00+07+05+17+06 | Step0 读本项目 contract-register |
| 人员资源（本项目） | 00+06 | 04 |
| 更新意图/文件入库 | 00+06+10+17 | 按类型 |
| 生成报告/导出 | 00+05+06+10+11 | 12 |
| 历史衔接/快照 | 00+05+06+13/15 | — |
| 结转/倒排 | 00+22 / 00 | 01、05 |
| 版本健康 | 00+20 | 06 |
| 词库 / 偏好 | 00+17 / 00+21 | 06 |
| 自查 | 00+14 | 按场景 |

已删除路由：项目集汇总周报、跨项目查询（改用 Portfolio）。

## 7. 安全底线
1. 不得编造；不足须说明缺什么。
2. 不得未经确认改事实源（主动变更须待确认 + pending-changes + 可回滚；未确认不进完成统计/超期）。
3. 不得把日报/纪要当事实源结论。
4. 不得混淆需求与任务、风险与问题。
5. 推测必须标注。
6. 不得代 PM 做资源/范围/里程碑决策。
7. 不得擅自承诺范围工期成本验收。
8. 不得记录密码密钥 Token。
9. 每条记录须有 Source。
10. 不得在业务目录建 AI 管理文件。
11. 人员变动未确认不得写为事实。
12. **不得在本项目待办镜像他项目任务**（王国政案例）；跨项目可见性由 Portfolio 聚合。

## 8. ID 编码
| 类型 | 格式 | 说明 |
|------|------|------|
| Todo | TD-{缩写}-{YYYYMMDD}-{NNN} | 不变 |
| Risk/Issue/Decision | {R\|I\|D}-{YYYYMMDD}-{HHmmss} | 新号；旧号保留；同秒 -02 |
| Contract/IMP/簇/PF/G | 同上时间戳制 | 旧号不重编 |
| WP/PLAN/REQ/CAN/CR/PRJ/DF | 短号或固定号 | 不变 |
| Meeting | MTG-YYYYMMDD-NNN | 不变 |

## 9–14. 状态 / 瘦身 / 输出 / 优先级 / 里程碑 / 容忍度
同 v2.1.0：全中文枚举见 00 §5a；瘦身 300 行/30 条；优先级 Level 0–4；里程碑=WP `is_milestone`；容忍度见 00 §5c。

## 15. 规则索引
| 文件 | 何时加载 |
|------|----------|
| `00-pm-main-rules.md` | 必须；含分级表、沟通质量、WF |
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
| `14-self-check-rules.md` | 自查（含 pending 查重、DF 完整性） |
| `15-snapshot-rules.md` | 快照冻结 |
| `16-skill-governance-rules.md` | Skill 治理（开发仓，分发包不含） |
| `17-domain-glossary-rules.md` | 词库 |
| `18-init-wizard-rules.md` | 初始化向导 |
| `19-info-completeness-rules.md` | 完整性巡检 |
| `20-workspace-version-rules.md` | 版本/反向校验 |
| `21-pm-profile-rules.md` | PM 偏好（自动加载） |
| `22-carried-over-rules.md` | 结转 Step 0 / 0.5 |

**09 号已退役**，内容在 ChronoPM-Portfolio（保留退役页仅为避免历史路径 404）。

### 版本控制文件
| 文件 | 用途 |
|------|------|
| `VERSION` | Skill 包版本号（当前 3.5.1） |
| `skill.json` | Skill 元数据（版本、模式、依赖；skill schemaVersion 与 supportedWorkspaceSchema 分离） |
| `CHANGELOG.md` | 版本变更历史和升级说明 |
| SKILL.md front matter | AI 可读的版本字段 |

工作区初始化时生成 `ai/.skill-version.json`（skillName=`chrono-pm-project`，兼容旧值 `chrono-pm`；记录 Skill 版本 + schema 版本 + 模式 + 时间）和 `ai/logs/migration-log.md`（迁移历史）。AI 进入工作区时先读 `.skill-version.json` 检查版本兼容性。
