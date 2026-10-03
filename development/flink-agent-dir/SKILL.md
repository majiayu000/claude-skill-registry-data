---
name: flink-agent-dir
description: 为 Flink 项目（CDC 同步作业 / Flink 流计算作业，多作业单仓库或多仓库）生成或维护 `.agent/` 目录——多 Agent 共享的渐进式披露项目上下文：每个作业一个目录按生命周期分文件（README 接入/plan 规划/dev 开发/test 测试/acceptance 验收/changelog 迭代），加全局代码目录规范、任务看板、决策/调试/交接知识库、公共工具沉淀。Use when the user asks to create, scaffold, initial or update a `.agent` directory (or .agent 目录, agent 协作目录, 多 agent 上下文, progressive disclosure docs) for a Flink project, or asks to organize Flink project conventions for multiple coding agents (Codex/Claude/Cline/Cursor), shared task context, code layout conventions, or common utility settlement, or wants to remove tool-specific rules files (like CLAUDE.md) and consolidate everything into the .agent directory.
---

# flink-agent-dir

为 Flink 项目生成共享的 `.agent/` 协作目录：多 Agent（Codex / Claude Code / Cline / Cursor 等）在同一份渐进式披露上下文上协作，工具无关、不依赖任何特定产品的根规范文件。

## 设计内核（生成时必须贯彻）

1. **渐进式披露**: 每次会话唯一必读 `INDEX.md`；其余按主题与生命周期分层读取——接任务读 `jobs/<入口类>/README` + TASKS（顶部含「当前交接」）；动手前读 CONVENTIONS（含 Part C 归属）；找代码读 CODE_MAP；全景/踩坑读 CONTEXT。**禁止"必须先读完全部文件"。**
2. **每作业一目录、按生命周期分文件**: `jobs/<入口类>/`（目录名 = Flink 主程序入口类）下 README/plan/dev/test/acceptance/changelog/decisions/debug-log 八个文件——单作业渐进式披露 + 全生命周期追踪；公共设施与源码改造同样配齐 plan/decisions/debug-log/test。
3. **SSOT 单一事实源**: 一类信息只在一个文件维护；作业级变更只记作业 changelog，全局 CHANGELOG 只记跨作业/公共设施。
4. **工具无关**: 不为任何特定 Agent 产品留根文件；可选一个极薄根 `AGENTS.md` 只作指针（跨工具通用入口约定），全部规范与上下文收束 `.agent/`。
5. **代码目录规范是核心资产**: 四类代码（Job/Bean/Function/基础设施）唯一落点 + 归属裁决 + 查找指引（防散落、防重复造工具）。
6. **知识按作用域就近沉淀**: 决策（decisions.md 增量）/ 调试（debug-log.md 增量）按主题落在 jobs/<入口类>/、shared/、sourcerefact/ 各自目录；项目级交接叙事并入 TASKS.md 顶部「当前交接」块（覆盖式，禁放清单）。
7. **发布 SOP 与凭据指针**: 发布/回滚唯一 SOP 在 shared/deploy.md；外部凭据只在 CONTEXT 留非敏感「去哪拿」指针，敏感值不落任何文档。
8. **成品参照是老师**: 先读 `examples/flink-demo/.agent/`（虚构业务、full 档的 sanitized 完整示例）理解填充质量，再用 `assets/templates/` 骨架生成。

## 触发场景

- 为某 Flink 项目生成/初始化 `.agent` 目录；把散落文档收敛为多 Agent 共享上下文
- 移除 CLAUDE.md 等工具专属文件、统一收束到 `.agent/`
- 制定代码目录规范、任务看板、协作规范

## 生成流程（交互 + 扫描）

### 第 1 步：确认范围（最多 6 问）

1. **项目形态**: 单仓库多作业/多仓库？CDC 同步、流计算、SQL 作业各几条？
2. **作业清单**: 每个作业的名称、上游→下游、源/汇系统、入口 main 类。
3. **外部系统**: 存储/消息/编排平台（VVP/K8s...）、配置形态（文件/配置库/参数）。
4. **现有规范**: 已有 CLAUDE.md / AGENTS.md / README / docs 的处理策略——默认：规范吸收进 `.agent/CONVENTIONS.md`（Part A 代码写法 / Part B 协作 / Part C 代码组织与归属）、知识按作用域归类；**未经确认不修改原项目任何文件**。
5. **任务看板现状**: 进行中任务、backlog、编号体系（已有 R/D 编号则沿用，保证与决策文档连续）。
6. **包结构事实**: 无则跳过，直接扫描。

### 第 2 步：扫描目标项目（只读）

- 规范文档（CLAUDE/AGENTS/README）提取技术栈、写法规范、防御底线；代码结构（`find src -name "*.java"`）得包级地图、入口、已有工具与补丁区；构建测试（pom/版本/测试布局）；配置（模板/脱敏/凭据状态）；评估目标项目自身已有的 docs/debug 等目录哪些值得迁移、哪些是垃圾不搬。

### 第 2.5 步：档位判定（lite / standard / full，扫描后与用户确认）

| 档位 | 适用 | 产出 | 说明 |
|------|------|------|------|
| `lite` | 单/双作业、无官方类补丁、规则文件少 | 根 `AGENTS.md` 单文件（对齐 agents.md 极简路线） | 不生成 `.agent/` 全套；项目长大后迁 `standard` |
| `standard` | 多作业常规项目（模板默认档） | 完整 `.agent/`：INDEX/TASKS/CONTEXT/CONVENTIONS/CODE_MAP/ROADMAP/CHANGELOG + `jobs/<入口类>/` 八件套 + `shared/` | `shared/` 按项目实际裁剪；无补丁不建 `sourcerefact/` |
| `full` | 深度改造型（多官方类补丁/多共享设施） | `standard` + `sourcerefact/`（patches/plan/decisions/debug-log/test） | `examples/flink-demo/`（sanitized 完整示例）即 full 档范式 |

> 判定依据：作业数、是否同包覆盖官方类、共享设施规模。模板始终只有一套，档位只决定"复制哪些、删除哪些"，不留空壳。

### 第 3 步：访谈式填充

复杂事实（链路拓扑、包边界、公共能力、已知坑）必须经用户确认再写；每个作业按 `assets/templates/jobs/_TEMPLATE/` 八文件填充（含 decisions/debug-log）。

### 第 4 步：生成 `.agent/`

```
.agent/
├── INDEX.md              # 唯一必读：分层读取、职责边界、作业责任表、协作流程
├── TASKS.md              # 全局看板（分组：公共设施/同步链路/计算任务/知识维护）+ 顶部「当前交接」叙事块
├── CONTEXT.md            # 按需深读：链路图、依赖纪律、外部系统、常见陷阱表
├── CONVENTIONS.md        # 落代码前读（唯一规范源）：Part A 代码写法 / Part B 协作 / Part C 代码组织与归属
├── CODE_MAP.md          # 代码地图：包级地图 + 查找指引（地图，按需查）
├── ROADMAP.md            # 远景规划（方向级，非任务清单）
├── CHANGELOG.md          # 全局极薄：跨作业/公共设施变更 + 各作业 changelog 索引
├── jobs/                 # 每作业一目录（名 = 入口类），八件套：README/plan/dev/test/acceptance/changelog/decisions/debug-log
│   ├── <入口类-1>/
│   ├── <入口类-2>/ …
│   └── _TEMPLATE/        # 八件套模板
├── shared/               # 公共设施：config/pipeline/storage/deploy/toolbox + plan/decisions/debug-log/test
└── sourcerefact/         # 官方类源码改造区：patches + plan/decisions/debug-log/test
```

- **根薄壳**（默认生成，来自 `assets/templates/shells/`，均可删）：`AGENTS.md`（Codex/Cursor/Cline）+ `CLAUDE.md`（Claude Code 入口）+ `.cursor/rules/000-read-index.mdc`（Cursor）。每个文件只允许 ≤3 行指针指向 `.agent/INDEX.md`，**禁止写实质规范**（SSOT 边界）。
- 按第 2.5 步档位从 templates 选用/删除模板（项目没有的能力删模板，不留空壳）。
- 迁移：旧规范吸收进 CONVENTIONS 三 Part；旧决策/调试/配置字典按作用域归类；路径引用统一改 `.agent/...`。

### 第 5 步：落地与验收

- 检查占位符全部填充、INDEX 文档地图与真实文件一一对应、每个链接可打开。
- [确认后] 提交 git；在 TASKS.md 顶部「当前交接」写明生成范围与下一步。

## 维护模式（已有 .agent）

- 认领任务照 INDEX 分层读取；任务细节进 `jobs/<入口类>/` 对应文件（含 decisions/debug-log），TASKS 只动状态行。
- 新增工具走 CONVENTIONS Part C 裁决 + CODE_MAP/toolbox 登记；新增作业按「新作业落地清单」（CONVENTIONS B3）成套落地。

## 注意事项

- 不臆造事实：没有依据标「待确认」，禁止编造链路/包/配置。
- 不迁移垃圾；敏感信息脱敏（`__FILL_IN_*__`），真实凭据不进任何新文件。
- 目标项目自身规范与 skill 冲突时以目标项目为准，并在 INDEX 记录该例外。
