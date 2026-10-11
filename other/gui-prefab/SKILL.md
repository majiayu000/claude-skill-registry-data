---
name: gui-prefab
user-invocable: false
description: >-
  Atom Game GUI pipeline 第 3 阶段。把 View.cs 挂到 Prefab 并绑定 [SerializeField] 引用。
  自包含的 Prefab 编辑指引，不依赖外部 edit-prefab skill。在 gui-draft 生成 View.cs 后使用。
  控制 Prefab 绑定漂移。
---

# Phase 3: gui-prefab — Prefab 编辑

**职责**：自包含的 Prefab 编辑。**控制：Prefab 绑定漂移。**
输入：gui-draft 输出的 `View.cs` + ui_data.lua 的 prefab 路径。

> **执行位置与并行**：本阶段**跑在主 agent**。gui-config（Phase 4）与本阶段**并行**——
> 若本需求涉及配置数据，由 orchestrator 把 gui-config **spawn 到 subagent** 与本阶段同时跑；
> 不涉及配置则直接 `skipped`。两阶段都落定后才进入 gui-review（编排细节见 `commands/run.md`）。

> 动手前先读 `${CLAUDE_PLUGIN_ROOT}/shared-references/prefab-binding-contract.md`。

## 编辑内容

- 把 `<PanelName>View.cs` 挂到 Prefab **根节点**。
- 绑定每个 `[SerializeField]` 引用（按钮、文本、图片、列表节点）。
- `StylesModule<TEnum>`：分组节点齐全 + 设默认 `m_SelectedIndex`。
- `ListModule`：Template 节点保持 **inactive**。
- 静态格式文本保留在 Prefab 文本节点。

## 工具使用（主动加载）

进入本阶段时，**主动通过 `ToolSearch` 搜索并加载** Prefab 相关能力（详见流程步骤 0），而非被动等待已加载：

- **优先使用搜到的 Prefab 专用 skill/tool**：用它读写 Prefab、读 hierarchy、校验绑定。
- **搜不到 Prefab 专用工具时，退而用 Unity Editor 交互能力**（编译、挂脚本、绑定 `[SerializeField]`）作为 fallback。
- **两者都没有** → 不臆造绑定；在 `HUMAN_REVIEW.md` 标注「需在 Unity 中人工挂脚本/绑定」，本阶段判降级，管线继续。

## 流程

0. **前置：主动加载 Prefab 相关 skill/tool（改 prefab 之前必做）**：
   - **优先**：使用 `ToolSearch` 搜索 Prefab 编辑相关能力（查询 `"prefab"` / `"prefab edit"` / `"prefab bind"` 等），
     获取 deferred tool schema——**搜到则优先使用**，用于读写 Prefab、读 hierarchy、校验绑定。
   - **fallback**：使用 `ToolSearch` 搜索 Unity Editor 交互能力（查询 `"unity editor"` / `"unity compile"` 等），
     获取编译/Editor 交互 tool schema——Prefab 专用工具搜不到时，退而用 Editor 交互能力编辑 Prefab
     （挂脚本、绑定 `[SerializeField]`）作为补充。
   - 搜索到的工具 schema 会展开在上下文中，后续步骤直接调用。
   - **两者都没有** → Prefab 编辑能力不可用，步骤 2–4 跳过，步骤 5 记 `BLOCKED` 入 `HUMAN_REVIEW.md`，不阻塞管线。

1. **前置：判断 Unity Editor 运行状态 + C# 编译（硬门，改 prefab 之前必做）**：
   - **先通过 unity-cli 判断 Unity Editor 是否正在运行。**
   - **Editor 运行中（unity-cli 可用）**：
     - 先查 PlayMode 状态；若处于 PlayMode 且需退出，**先征求用户确认**。
     - 通过 unity-cli 触发 C# 编译，让 gui-draft 产出的 `<PanelName>View.cs`（及本次新增/改动的 ViewModel）
       **进程序集**——只有编译通过、MonoScript 生成稳定 GUID 后，才能把 View 脚本挂到 Prefab 根节点、
       并让 `[SerializeField]` 字段在 Inspector 可见可绑。
     - 编译通过后可以继续编辑 Prefab（挂脚本、绑定 `[SerializeField]`）。
   - **Editor 未运行（unity-cli 不可用）**：
     - 可通过 Batch Mode 编译（`./unity/WindowsEditor/Unity.exe -projectPath ./client/ -batchmode -quit ...`），
       让 View/ViewModel 进程序集（`.meta` 文件由 csharp-tool 生成，不依赖 Unity 编译）。
     - **但 Batch Mode 无法编辑 Prefab**（不能挂脚本、不能绑定 `[SerializeField]`）→ Prefab 编辑本身判
       `BLOCKED`，记入 `HUMAN_REVIEW.md`「需在 Unity Editor 中人工挂脚本/绑定」。
   - **两路径均不可用（Editor 未开且无 Unity.exe）** → 编译门 + Prefab 编辑均判 `BLOCKED` 记入清单，不阻塞。
   - 编译报错 → 先按报错修 draft 产物再重编。**编译通过后才进入第 2 步**。
2. 列出 View.cs 中所有 `[SerializeField]` 字段（名称 + 类型）。
3. 对照 Prefab hierarchy 逐一绑定（或记录待人工绑定项）。
4. 校验 prefab-binding-contract 的清单（悬空字段 / 孤儿绑定 / 类型匹配 / 数量一致）。
5. 记录状态（**由 orchestrator 在主 agent 侧执行**）：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-prefab done
   ```

## Gate

- **前置工具加载门**：改 prefab 前已通过 `ToolSearch` 主动搜索 Prefab 专用工具（优先）及 Unity Editor
  交互能力（fallback）。Prefab 专用工具搜到 → 优先用于读写/校验 Prefab；搜不到 → 退而通过 unity-cli
  与 Editor 通讯完成 Prefab 编辑；unity-cli 也不可用（Editor 未运行）→ 步骤 1 仅剩 Batch Mode 编译，
  Prefab 编辑本身 `BLOCKED`；连 Unity.exe 都没有 → 编译门 + Prefab 编辑均 `BLOCKED`。
- **前置编译门**：改 prefab 前 C# 已编译通过（View/ViewModel 进程序集）。按两路径规则：Editor 运行中
  → unity-cli 编译后继续编辑 prefab；Editor 未运行 → Batch Mode 编译可过但 **Prefab 编辑本身 BLOCKED**
  （Batch Mode 无法操作 Prefab），记入 `HUMAN_REVIEW.md`；两路径均不可用 → BLOCKED。
- View.cs 中每个 `[SerializeField]` 在 Prefab 中都有对应绑定节点（数量一致）。
  缺 Prefab 能力时该 Gate → `BLOCKED`，记入清单，不阻塞。

→ gui-config（Phase 4）由 orchestrator **并行 spawn 于 subagent**（本需求不涉及配置则 `skipped`）。
**prefab 与 config 两阶段均落定后** → 进入 **gui-review**。
