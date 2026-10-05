---
name: chrono-pm-portfolio
version: 3.5.1
schema_version: 0.7.0
workspace_schema: 0.10.0
updated_at: 2026-08-20
description: 给项目集/组合经理用的只读 Skill。跨多个项目 ai 目录归集检索进度、风险、合同、周报。禁止写入成员项目事实源。触发：项目集、组合、跨项目、汇总周报、进度总览、人员排期、跨项目风险、门禁、P&L、合同去重、建议更新清单、挂载、健康巡检、ChronoPM-Portfolio。
---
# ChronoPM-Portfolio — 只读项目集归集

## 1. 定位
**写归 Project，读归 Portfolio。** 日常录入、待办、日报、风险问题只发生在各成员项目的 ChronoPM-Project 对话；本包只做跨项目归集、检索、汇总、预警。
本包 **零事实源**：一切结论实时读成员项目得出。无 init 脚本；联邦骨架由 AI 按模板创建，登记须确认。

## 2. 工作模式
仅 **viewer**：对 `ai/projects/*/ai/**` 只读禁写；可写范围仅 `ai/portfolio/**`。
跨项目变更一律输出「建议更新清单」，由对应项目的 ChronoPM-Project 对话执行。

## 3. 联邦工作区
```
{集工作区}/
└── ai/
    ├── .skill-version.json          # 集级版本（skillName=chrono-pm-portfolio）
    ├── portfolio/                   # 唯一集级区（本包可写）
    │   ├── context/project-index.md # 成员登记（指针，权威索引）
    │   ├── reports/                 # 派生产物（须 generated_from+updated+stale）
    │   ├── resources/               # 共享人力/流转只读指针索引（可选）
    │   └── logs/
    └── projects/                    # 挂载区（本包只读）
        └── {项目名}/ai/             # 完整单项目工作区（可打包带走）
```
`projects/{名}/ai/` 内部结构 = ChronoPM-Project 单项目工作区。解压即识别。
**防套娃**：`projects/{名}/ai` 内禁止再出现 `portfolio/` 或 `projects/`。发现即告警，拒绝聚合。

## 4. 只读契约（五条，安全底线）
1. 对任何成员项目 `projects/*/ai` **只读**，禁止创建/修改/删除其中任何文件。
2. 允许写入的**仅限** `portfolio/`（索引维护 + reports/ 派生产物）。
3. 集经理意图变更成员项目实体 → 只输出「建议更新清单」（目标项目 + 目标文件 + 建议内容），不代写。
4. 聚合视图全部实时计算，禁止把聚合结果落盘为数据源；落盘仅限当期报告快照，且必须带 `generated_from:` + `updated:` + stale 失效规则。
5. 跨项目「人的视图」实时遍历其参与项目的待办聚合，**不落盘**。

## 5. 进入工作区（先做）
1. 读集级 `ai/.skill-version.json` → 比本包 `VERSION`。Skill < 工作区 → 提示升级本包 + 只读降级。见 `06-version-health-rules.md`。
2. **V-1 动态感知**：扫描 `projects/` 一级目录 vs `portfolio/context/project-index.md`。未登记→提示登记（须确认）；索引有而目录无→提示清理失效路径。见 `03-mount-awareness-rules.md`。
3. **V-10 健康巡检**：双包版本、反向校验、孤儿路径、防套娃、配置漂移。见 `06-version-health-rules.md`。
4. 查询一律按 project-index **已登记且校验通过** 的一级成员项目自动路由；未登记目录不参与聚合。

联邦骨架缺失时：按 `assets/templates/project-index-template.md` 创建 `portfolio/context/project-index.md` 与空 `projects/`，询问集经理后登记，不扫描即当正式成员。

## 6. 能力 V-1～V-10
| # | 能力 | 触发 | 实时读 | 输出 |
|---|---|---|---|---|
| V-1 | 成员登记 + 动态感知 | 进入工作区/查询前 | `projects/` + project-index | 候选登记/失效清理提示 |
| V-2 | 进度总览 | 「各项目进度」 | 各项目 `wps/_index.md`（3.5.0+ 加速器）+ PLAN §3 简表 + 待办聚合 | 项目×WP 进度表（含偏差） |
| V-3 | 人×项目视图 | 「某人/所有人这周干什么」 | 各项目 todos/{date}/ + resource-register | 人×项目×待办矩阵（T1 冲突提示） |
| V-4 | 跨项目风险/问题 | 「跨项目风险」 | 各项目 risk/issue-register（影响项目≥2） | 聚合清单 + 主归属 |
| V-5 | 集周报 | 「出集周报」 | **各项目周报**（不从日报现场拼） | `portfolio/reports/` 派生周报 |
| V-6 | 门禁最小值 | 「封板达成了吗」 | 各项目 PLAN 门禁 WP | 任一未完成=未完成 |
| V-7 | 整体 P&L | 「整体 P&L」 | 各项目 plans/budget.md | 合同额/成本/CPI 汇总 |
| V-8 | 合同去重归并 | 「集级合同全景」 | 各项目 contract-register + {type}-source/ | 簇 ID + 内容指纹；冲突提示版本差异 |
| V-9 | 建议更新清单 | 集经理意图变更 | — | 指向各项目，不代写 |
| V-10 | 健康巡检 | 进入工作区/定期 | 各项目 .skill-version.json + 结构抽查 | 版本/孤儿/套娃/漂移 |

**最小读取集**：V-1～V-10 一切聚合只读索引/摘要行（project-index、status 摘要、登记册表格行），不读全文。全文仅集经理点名某项目细节时才读。

**V-5 硬约束**：从各项目当期周报往上摘。无周报 → 提示「{项目} 周报未出，请先在该项目对话出周报」。PM **明确**指令「临时摘」才允许从该项目日报现场拼，且必须标注「临时摘要，非替代周报」。

待办聚合输出同 Project R18：默认仅未办结；未确认终态默认可见（禁止当已办结隐藏）。见 `02-aggregation-query-rules.md`。

## 7. 提示词路由表
| 场景 | 必须加载 |
|------|----------|
| 进入工作区 / 挂载 / 动态感知 | 03 + 06 |
| 进度总览 / 人×项目 / 风险 / 门禁 / P&L / 合同 | 01 + 02 |
| 待办跨项目查询 | 01 + 02 |
| 集周报 | 01 + 04 |
| 建议更新清单 / 意图变更 | 01 |
| 共享人力 / 流转 / 资源漂移 | 01 + 05 |
| 健康巡检 / 版本 / 防套娃 / 配置漂移 | 03 + 06 |
| 任意写入 portfolio/ | 01 |

细则不得跨包引用 Project `references/`。成员项目字段语义以该项目文件为准；本包只聚合。

## 8. 建议更新清单（V-9）
格式见 `assets/templates/suggested-update-list-template.md`。每条必须含：目标项目、目标文件路径（相对该项目 `ai/`）、建议内容、理由、优先级。可落 `portfolio/reports/` 或仅对话输出。**禁止**据此改 `projects/*/ai`。

## 9. 安全底线（重复只读五条）
1. 对 `projects/*/ai` 只读，禁止创建/修改/删除其中任何文件。
2. 只写 `portfolio/`。
3. 变更成员项目走建议更新清单，不代写。
4. 聚合不落盘为数据源；报告须 `generated_from` + `updated` + stale。
5. 人的视图实时聚合，不落盘。

另：不得编造；不足须说明缺什么。推测必须标注。不得代集经理做资源/范围/里程碑决策。不得记录密码密钥 Token。不得在业务目录建 AI 管理文件。

## 10. 规则与模板索引
| 文件 | 何时加载 |
|------|----------|
| `01-readonly-boundary-rules.md` | 写禁、建议更新清单、落盘规则 |
| `02-aggregation-query-rules.md` | V-2～V-8、待办 R18、合同去重 |
| `03-mount-awareness-rules.md` | 挂载、动态感知、防套娃、自动路由 |
| `04-portfolio-report-rules.md` | 集周报、缺周报降级、资源变动检测 |
| `05-resource-shared-rules.md` | 共享人力/transfer 只读聚合 |
| `06-version-health-rules.md` | 双包版本、反向校验、漂移比对 |

模板：`project-index-template.md`、`portfolio-weekly-template.md`、`suggested-update-list-template.md`。

### 版本文件
`VERSION` / `skill.json` / `CHANGELOG.md` / 本 front matter。集级 `ai/.skill-version.json`（skillName=`chrono-pm-portfolio`）。成员项目 `projects/{名}/ai/.skill-version.json`（skillName=`chrono-pm-project`，兼容 `chrono-pm`）。
