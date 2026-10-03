---
name: to-brd
description: 生成业务需求文档(BRD)— 含业务流程图、角色职责、功能模块、字段映射表。业务需求需正式文档化交付给团队评审时调用本 skill,把 TASK_CONFIRM 翻译为 9 节齐备的 BRD。
disable-model-invocation: true
version: 4.0.0
requires: [ascii-flowchart, no-field-guessing, doc-numbering, stage-gate]

---

# To-BRD — 业务需求文档生成

## Contract

- 输入: 已签字的 `TASK_CONFIRM_*.md`、`REVIEW_需求确认书.md`、`REVIEW_字段对齐分析.md`、`paths/knowledge-path.md`
- 输出: `01-业务需求文档 BRD.md`、ASCII 流程图、可选 `业务流程图.drawio`
- 门控: BRD 必备章节齐全;字段映射与知识库核对;用户签字
- Required rules: `stage-gate`, `no-field-guessing`, `ascii-flowchart`, `doc-numbering`, `goal-boundary`
- Required paths: `knowledge-path`, `doc-naming-path`
- 下一步: `/compliance-review`

## 适用场景

- TASK_CONFIRM 和字段对齐分析已通过
- 需要把业务需求整理成 BRD 交给团队评审
- 需要画业务流程图 / 状态流转图

## 流程步骤

### 1. 加载模板

- `templates/BRD.md`(9 节必备章节)

### 2. 填充内容

按 BRD 模板逐节生成:

| 章节 | 内容来源 |
|---|---|
| 一、项目概述 | TASK_CONFIRM §1-3 |
| 二、角色与职责 | 业务调研 |
| 三、业务流程 | ASCII 流程图 / drawio |
| 四、功能模块 | TASK_CONFIRM §功能描述 |
| 五、数据要求 | 字段对齐分析 + 知识库 |
| 六、合规要点 | 预留,阶段 4 填 |
| 七、非功能需求 | 性能/可靠性/安全/可维护性 |
| 八、风险与约束 | 团队约束 + 外部依赖 |
| 九、上线计划 | 团队节奏 |

### 3. 画流程图

- 状态流转图:**ASCII**(参考 `rules/ascii-flowchart.md`)
- 业务流程图:简单用 ASCII,复杂用 drawio
- 泳道图:ASCII(角色分工清晰)

### 4. 字段映射表

把字段对齐分析里的 ✅ 项固化到 BRD §五.3:

| 业务概念 | 字段 | 备注 |
|---|---|---|
| ASN 单号 | `ASN.TC_ASN_ID` | ❌ 严禁用 ASN_NBR |

### 5. DB 验证(如涉及)

- 仅允许 `SELECT` 查询
- 用 `desc table_name` 验证字段定义
- **严禁** 任何 DDL/DML 写操作

## 输出

- `01-业务需求文档 BRD.md`
- `业务流程图-状态流转.txt`(ASCII)
- `业务流程图-收货流程.txt`(如需要,泳道图)
- `业务流程图.drawio`(可选,用于可视化)

## 调用的 rule

- `rules/ascii-flowchart` — 流程图规范
- `rules/no-field-guessing` — 字段名必须查知识库
- `rules/doc-numbering` — 文档编号 01

## 结束条件

- [ ] BRD 9 个必备章节齐
- [ ] ASCII 流程图 + 状态流转图
- [ ] 字段映射表通过 `field-alignment-check.py`
- [ ] 用户签字进入阶段 4

## 反模式

- ❌ 用 Mermaid 写流程图 — 必须 ASCII(参考 rules/ascii-flowchart.md);可视化交付经 `flow-to-mermaid.py --ascii-strict`
- ❌ 泳道图回流箭头散乱 — 必须汇聚到同一目标节点(回流闭环强制)
- ❌ 字段映射表缺知识库来源 — 每条字段必须标"WMOS 知识库/XX 章"或"项目侧 schema"
- ❌ 9 章节缺一 — `brd-check.py --strict` 必须 exit 0
- ❌ 写完不跑 `field-alignment-check.py` — 应在签字前自动跑一遍,errors=0 才签字
- ❌ 流程图用真实人名/客户名 — 用角色占位(仓管员/客户/系统)
