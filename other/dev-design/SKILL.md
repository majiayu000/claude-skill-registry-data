---
name: dev-design
description: 开发设计 — 含 FSD + 数据模型 + 开发设计说明书 + 设计回测 + 任务复盘,合并原 9 阶段中的 7/8/8.4/8.5 子流程。PRD 已签字、需输出技术设计方案时调用。
disable-model-invocation: true
version: 4.0.0
requires: [no-field-guessing, no-self-invent, sql-dialect-discipline, stage-gate, doc-numbering]

---

# Dev-Design — 开发设计(7 件套)

## Contract

- 输入: 已签字的 `05-产品需求文档 PRD.md` 与 `paths/knowledge-path.md`、`paths/tech-stack-path.md`、`paths/doc-naming-path.md`
- 输出: `AGENTS.md`、`02-功能规格说明书 FSD.md`、`03-数据模型设计.md`、`06-开发设计说明书.md`、`08-设计回测报告.md`、可选 `RETRO_任务复盘汇总.md`
- 门控: 字段对齐通过;SQL 方言检查通过;设计回测通过;用户签字
- Required rules: `stage-gate`, `no-field-guessing`, `no-self-invent`, `sql-dialect`, `doc-numbering`, `context-pointer`, `goal-boundary`
- Required paths: `knowledge-path`, `tech-stack-path`, `doc-naming-path`
- 下一步: `/qa-audit`

## 适用场景

- PRD 已签字
- 需要把产品需求翻译成技术实现方案
- 含数据模型、接口契约、前后端实现细节

## 流程步骤

### §1. AGENTS.md(项目级 AI 助手配置)

- 加载 `templates/AGENTS.md`
- 在项目根生成,内容:
  - 项目约束
  - 文档索引
  - 分层架构规则
  - 关键纪律引用(no-field-guessing / stage-gate 等)
- **渐进式披露**:地图而非手册

### §2. FSD(功能规格说明书)

加载 `templates/FSD.md`,生成 `02-功能规格说明书 FSD.md`:

- 模块清单
- 功能详述(输入/输出/业务规则/边界条件/异常路径)
- 接口契约(REST/RPC/消息,含入参出参错误码)
- 状态机(关键业务对象的状态流转)
- 数据模型概览
- 业务错误码字典

### §3. 数据模型设计

加载 `templates/数据模型设计.md`,生成 `03-数据模型设计.md`:

- 表清单(新增 / 扩展)
- 表结构(字段、类型、可空、默认值、注释、索引)
- 序列定义
- 字段对齐验证(与知识库核对)
- 初始化数据
- 迁移脚本(如适用)

### §4. 开发设计说明书(代码实现版)

加载 `templates/开发设计说明书.md`,生成 `06-开发设计说明书.md`:

- 架构设计(分层、关键依赖)
- 后端分层(Controller / Service / Repository / Entity / Mapper XML / DTO/VO)
- 事务与异常处理
- **前端组件**(PC + APP,按需)
- 联调说明(接口清单、步骤、Mock 数据)
- 错误码映射
- Checklist

**关键纪律**:
- 严禁只写后端(必须含前端 + 联调 + Mock)
- 严禁降级为伪代码 / TODO 列表
- 字段名 / 表名 / 状态码必须与知识库一致

### §5. 设计回测(HARD GATE)

**触发条件**(满足任一即必做):
- 数据模型有新增/扩展表
- 业务规则新增/修改
- 状态机新增/修改
- `field-alignment-check.py` 报错
- 合规相关变更

**4 大类回测**(详见 `rules/stage-gate.md`):
1. 数据模型回测 — 跑历史样本验证 DDL / 索引 / 查询
2. 业务规则回测 — 关键场景样本手工重跑
3. 状态机回测 — 历史单据状态变化回放
4. 字段对齐回测 — 文档 vs 知识库 vs 生产库

**输出**:`08-设计回测报告.md`

**HARD GATE**:回测不通过(❌)禁止进入阶段 8。

### §6. 子流程门控清单(可选实施扩展)

加载 `templates/开发设计说明书.md` §六,记录:

| 子流程 | 状态 | 签字 / 时间 |
|---|---|---|
| brainstorming 设计稿 | ⬜ | |
| spec 自检 | ⬜ | |
| writing-plans 完成 | ⬜ | |
| TDD RED 测试 | ⬜ | |
| 全部子任务 GREEN | ⬜ | |

> 仅在用户明确进入实施扩展模式(走 `/using-superpowers` 之后)才需要填。

### §7. 任务复盘汇总

每个子任务完成后,按 `rules/stage-gate.md` 的 5 问复盘写到 commit / PR。
此处汇总关键沉淀到 `RETRO_任务复盘汇总.md`(可选)。

## 调用的 rule

- `rules/no-field-guessing` — 字段名必须查知识库
- `rules/no-self-invent` — 严禁自创字段/表名
- `rules/sql-dialect` — SQL 方言对齐 Target_DB
- `rules/stage-gate` — 3 层门控 + 设计回测 + 任务复盘方法
- `rules/doc-numbering` — 文档编号 02/03/06/08

## 输出

- `AGENTS.md`(项目根)
- `02-功能规格说明书 FSD.md`
- `03-数据模型设计.md`
- `06-开发设计说明书.md`
- `08-设计回测报告.md`
- `RETRO_任务复盘汇总.md`(可选,实施扩展模式才需要)

## 结束条件

- [ ] 5 件核心文档齐(AGENTS / FSD / 数据模型 / 开发设计 / 设计回测)
- [ ] 设计回测结论 ✅ / ⚠️(❌ 必须回 §2-§4 修复)
- [ ] Checklist 全部勾选
- [ ] `field-alignment-check.py` 通过
- [ ] `sql-dialect-check.py` 通过
- [ ] 用户签字进入 `/qa-audit`

## 反模式

- ❌ 只写后端,缺前端/联调/Mock — 6 文档必齐(AGENTS/FSD/数据模型/开发设计/设计回测/任务复盘)
- ❌ 降级为伪代码/TODO — FSD 必须含字段映射表、状态机、接口契约
- ❌ 跳过设计回测(4 大类必跑) — ❌ 必须回 §2-§4 修复后才能签字
- ❌ 自创字段名(无知识库依据) — 严格走 `field-alignment-check.py` 校验,严禁瞎编
- ❌ SQL 方言混用(Oracle `NVL` + PG `COALESCE`) — `sql-dialect-check.py` 必过
- ❌ 整数除法不写 `1.0/3` — Oracle 1/3=0,必须标 `1.0/3`
- ❌ 主键用自增 ID — 必须每表配 SEQUENCE,严禁 `IDENTITY`/`SERIAL`(WMOS 原生约束)
