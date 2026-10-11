---
name: gui-plan
description: >-
  Atom Game GUI 开发 pipeline 的第 1 阶段（入口）。当用户要「开发/新增/修改一个 GUI 界面、
  panel、面板」或说「跑 gui pipeline / 做 GUI 需求」时使用。先确认用户已提供本次 run 的
  panelId 和需求描述，缺少任一项时先向用户询问；随后进入 Claude Code 原生 plan mode：
  只读探索资源 + 用已注入的知识库坑点 + 向用户提问澄清需求，写计划并 ExitPlanMode 等人类审批；
  审批通过后把计划高度精炼成需求契约 GUI_PLAN.md 落盘，并初始化 pipeline 运行状态。
  随后（由 /dev-gui-plugin:run 编排）顺序触发 gui-draft → gui-prefab → gui-config → gui-review →
  gui-improve → gui-learn。
---

# Phase 1: gui-plan — plan mode 交互确认需求 + 人类审批

**职责**：进入 plan mode，只读定位资源、向用户澄清需求、写计划并**等人类审批**；审批通过后产出
**高度精炼**的需求契约 `GUI_PLAN.md`，并初始化 run state。**控制：需求理解漂移。**

> **这是整条 pipeline 唯一的交互 + 人类审批关卡。** 本阶段**零写操作**（plan mode 内只读）；所有
> 写操作（建目录 / state / GUI_PLAN.md / 哨兵）都发生在**审批通过之后**。审批一过，pipeline 转入
> 全自动，从 gui-draft 起不再向用户提问。

## 路径约定（所有阶段共用）

- 工具：`${CLAUDE_PLUGIN_ROOT}/tools/`
- 契约：`${CLAUDE_PLUGIN_ROOT}/shared-references/`
- 知识库种子（只读）：`${CLAUDE_PLUGIN_ROOT}/gui-knowledge-seed/`
- **私有知识库（持久化、可写、个人）**：`${CLAUDE_PLUGIN_DATA}/gui-knowledge/`
- **公共知识库（项目共享、团队维护、走 p4）**：`${CLAUDE_PROJECT_DIR}/.claude/dev-gui-knowledge/`
  —— 两库内容都要参考；若有矛盾，以公共库为准。
- **本次运行产物（项目本地、gitignored）**：`${CLAUDE_PROJECT_DIR}/.claude/dev-gui-runs/<panelId>__<sessionId>/`

## 流程

### A. plan mode（只读 + 交互 + 审批）—— 零写操作

1. **入口参数前置检查（必须最先执行）**：在进入 plan mode、读取仓库或执行其他动作之前，先检查
   用户是否已明确提供本次 run 的 **panelId** 和**需求描述**。缺少任一项时，用 `AskUserQuestion`
   一次性询问所有缺失项（只缺一项则只问该项），并等待用户回答；**不得从仓库推断 panelId、不得使用
   占位值或 TODO 绕过此检查**。两项齐全后才继续。
2. **进入 plan mode**：若会话尚未处于 plan mode，`EnterPlanMode`（已在则跳过）。
3. **只读定位资源**：`Read` `code/LuaScripts/client/data/ui_data.lua`，按 panelId 定位 Prefab 路径、
   Panel 脚本路径、ViewModel 类型。找不到 → 在计划里标「待确认」。
4. **用已注入的知识库坑点**：两库 query_pack 已由 SessionStart hook 注入到上下文（**无需现场读文件
   或 init**）。提取与本需求相关的历史坑点/组件技巧；两库矛盾以公共库为准。
5. **查代码自答，无法确定必须提问**：在 panelId 和需求描述已通过入口检查后，如仍有其他需求缺口，
   **先穷尽代码仓库**——读 `ui_data.lua`、同目录现有 panel/View/ViewModel、`shared-references`、已注入的
   query_pack。凡能从仓库推断的（Prefab 路径、ViewModel 字段惯例等）一律自己定，**不问用户**；
   **无法从代码确定的、需要用户确认的，必须向用户提问澄清，不得用
   `**[TODO: 待人工确认]**` 占位绕过**。用 `AskUserQuestion` **一次性**问完所有此类
   问题（不逐条追问）。此阶段无 autorun 哨兵，可自由停顿。
6. **写计划 → 审批**：把需求写成计划（**偏需求侧**：要做什么 + 验收标准，而非详细实现步骤——实现是
   gui-draft 的职责）。**例外：以下两项设计属于契约，须在本阶段定死**（gui-draft 只照抄不再设计），
   且**必须按此顺序**：
   1. **先做模块拆分设计**：判断本界面是否需拆子 View / 子 Panel——多页签、多个高内聚低耦合模块、
      阶段流转、独立浮层 → 拆；单一职责小界面 → 不拆（root 单 View）。定好 root 与各子模块的划分、
      引用关系、命名。依据、引用关系与样例见 `${CLAUDE_PLUGIN_ROOT}/shared-references/mvvm-contract.md §1.1`
      （子 View 实现细节见 `patterns/subview-pattern.md`）。
   2. **再按拆分结果设计 ViewModel**：对 root + **每个子模块**分别定字段名/类型/是否 list/子 VM，
      组织成 ViewModel 树（root VM 持子 VM 列表，各子 View 绑各自 VM）。
   `ExitPlanMode` 等人类审批。被拒/要求改 → 回 plan mode 按反馈改，再 `ExitPlanMode`，循环直到通过。

### B. 审批通过后（已退出 plan mode）—— 落地写操作

> 在 `/dev-gui-plugin:run` 全自动编排下，这批写操作由 `commands/run.md` 步骤 2 承接（建目录 / start /
> run_meta / GUI_PLAN.md / 哨兵）；**单独调用本 skill** 时，由本 skill 执行到「写 GUI_PLAN.md + state」
> 为止，**不建哨兵、不自动进入 gui-draft**（哨兵与后续驱动是 /run 的职责）。

1. **初始化 run state**（只传裸 panelId，工具内部拼会话作用域 run_id）：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" start "${CLAUDE_PROJECT_DIR}" <panelId>
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-plan done
   ```
2. **产出 `GUI_PLAN.md`**（高度精炼的需求契约）到 run 目录。缺失项标 `**[TODO: 待人工确认] <缺什么>**`
   并汇总进 `HUMAN_REVIEW.md`。

## 输出格式 `GUI_PLAN.md`（高度精炼 —— 只留 gui-review 契约所需）

`GUI_PLAN.md` 是用户**已审批过的计划**原样落盘，供 gui-review 的独立审查者（全新上下文、Bias Guard）
读取当评分基准——**不是**让 AI 另写一份重量级 PRD。保持精炼，不写套话：

```markdown
# GUI PLAN: <panelId>   （用户已审批）

- panelId / Prefab 路径 / Panel 脚本路径 / ViewModel 类型

## 需求
- [几行 bullet：这个界面要做什么]

## 模块拆分（子 View / 子 Panel —— 先定这个，再设计下面的 ViewModel）
- 是否拆分：是/否 —— 一句理由（依据：多页签 / 模块高内聚低耦合 / 阶段流转 / 独立浮层）
- 拆分结构（**不拆则写「单 View，root 直接承载」并跳过下表**）：
  | 模块 | 子 View (C#) | Lua 侧 | 容器/触发 | 归属 VM |
  |------|-------------|--------|-----------|--------|
  | Root | `XxxView : BaseView` | `XxxPanel : UIBasePanel` | 用 `TableLib`/`TabView` 持子 | root VM（持子 VM 列表）|
  | <信息页> | `XxxInfoView : TabSheetView` | `xxx_info_view.lua : TableSheetLib` | 页签切换 | `XxxInfoViewModel` |
  | <独立浮层> | — | `xxx_tips_panel.lua`（独立 Panel）| `SendUIMessage` 触发 | 独立 VM |
- 命名/目录：Lua↔C# 文件名对称；子功能进子目录。详见 `mvvm-contract.md §1.1`。

## ViewModel 设计（数据契约 —— 按上面拆分，root + 每个子模块各一份；gui-draft 照抄写 ViewModelDes，不再自行设计）
- `<RootViewModel>`（`[ViewModel("group","lua_filename")]`）
  | 属性 | 类型 | 说明 |
  |------|------|------|
  | `SomeName` | `string` | … |
  | `HpList` | `IntList`（基础类型 list） | 变更后需 `update()` |
  | `Sheets` | 子 VM 列表（LIST） | 持各子 View 的 VM |
  | `SubInfo` | 子 VM `PlayerInfo` | `createViewModel` 创建 |
- `<每个子模块 ViewModel>`（拆分表里每个子模块各列一张同样的属性表）
- [属性名跟随同目录现有 panel 惯例；只列 Panel↔View 契约需要的字段，不含 Panel 私有字段]

## 验收标准
- [几行 bullet：review 据此判断是否达成]

## 相关历史坑点（可选，来自 query_pack）
- [涉及组件的已知坑点 / 类似界面曾出现的 bug]
```

> ViewModel 设计缺信息应在 plan 阶段问清；若仍有遗留 → 标 `**[TODO: 待人工确认]**`，不要在 gui-draft 现推。

## Gate

用户在 `ExitPlanMode` **审批通过** → 写 `GUI_PLAN.md` + 初始化 state → 进入 **gui-draft**。

> 审批之后整条 pipeline 无中途人工暂停；需人确认项最终统一收口到 `HUMAN_REVIEW.md`（gui-review 末）。
