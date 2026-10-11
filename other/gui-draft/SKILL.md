---
name: gui-draft
user-invocable: false
description: >-
  Atom Game GUI pipeline 第 2 阶段。生成 MVVM 代码（Panel.lua + View.cs + 如需的 ViewModel）。
  自包含的 MVVM 指引。在 gui-plan 产出 GUI_PLAN.md 后使用。控制代码
  实现漂移（相对需求契约）。
---

# Phase 2: gui-draft — MVVM 代码生成

**职责**：自包含的 MVVM 代码生成。**控制：代码实现漂移。**
输入：`GUI_PLAN.md` + 两库 query_pack（私有 `${CLAUDE_PLUGIN_DATA}/gui-knowledge/query_pack.md`
+ 公共 `${CLAUDE_PROJECT_DIR}/.claude/dev-gui-knowledge/query_pack.md`，后者存在则读；矛盾以公共库为准）。

> 动手前先读 `${CLAUDE_PLUGIN_ROOT}/shared-references/mvvm-contract.md`。

## 核心规则

- Panel (Lua) **写** ViewModel，View (C#) **只读**（单向数据流，靠 SharedArray 共享）。
- **ViewModel 设计由 gui-plan 定死**（`GUI_PLAN.md` 的「ViewModel 设计」节）——本阶段**照抄写 ViewModelDes，不自行设计属性**。
- 需新增/改 ViewModel 属性 → 走 4 步（见 mvvm-contract §3）：
  写 ViewModelDes → csharp-tool 导出 → 写 View/Panel → 编译（能连 Unity Editor 时）。
  **csharp-tool 独立于 Unity，GenerateViewModel 不要求前置编译。**
- **生成文件优先工具导出、不优先手改** `*_viewmodel.lua` / `*ViewModel.cs` / `AtomViewModelFactory.cs` / `ui_viewmodel_define.lua`：
  能用工具导出就不手改；**仅当工具导出失败/不可用时**才允许手改补齐（加 `TODO(模拟导出)` + 记 `HUMAN_REVIEW.md`，见 mvvm-contract §3）。
- Panel：`<PanelName>Panel.lua` 继承 `UIBasePanel`；View：`<PanelName>View.cs` 继承 `BaseView`。
- **优先 AtomUI* 公共组件，避免裸 UGUI**（`AtomUIText`/`AtomUIImage`/`AtomUIButton`）。

## 模板（真实写法）

> 仍**先读目标目录同类现有 panel** 对齐命名/惯例。生命周期钩子与 API 见 mvvm-contract §4-§7。

```lua
-- Panel（Model 层）
local enum = require("framework.utils.enum")
local uiBasePanel = jn_require_ex("framework.ui.ui_base_panel")
local PanelNamePanel = DefineClass("PanelNamePanel", uiBasePanel.UIBasePanel)

UIMessageId = enum "UIMessageId" { "OnConfirmClick" }              -- 与 C# enum 同步（从 1）
local panelMessageHandler = { [UIMessageId.OnConfirmClick] = "onConfirmClick" }
function PanelNamePanel:getPanelMessageHandler() return panelMessageHandler end

function PanelNamePanel:prepareViewModel(panelData)
    self.rootViewModel.SomeProperty = panelData.someValue          -- 只写 ViewModel
end

function PanelNamePanel:onPanelClose()
    -- 取消 timer / 移除监听 / dispose 创建的 Lib（清理是你的责任）
end

function PanelNamePanel:onConfirmClick() end
```

```csharp
// View（表现层）
public class PanelNameView : BaseView
{
    private enum UIMessageId { OnConfirmClick = 1 }                // 与 Lua enum 完全一致

    [SerializeField] private AtomUIButton m_BtnConfirm;
    [SerializeField] private AtomUIText m_TxtTitle;

    private PanelNameViewModel m_VM;

    public override void Initialize(BaseViewModel viewModel)
    {
        if (viewModel is not PanelNameViewModel vm) return;
        m_VM = vm;
        InitializeView();
        InitializeEvents();
    }

    private void InitializeView()
    {
        m_TxtTitle.SetText(m_VM.SomeProperty.ToString());
    }

    private void InitializeEvents()
    {
        m_VM.RegisterPropertyChangeHandler<string>(PanelNameViewModel.SOMEPROPERTY, OnSomeChange);
        m_BtnConfirm.OnClick = OnBtnConfirmClick;                  // 非 onClick.AddListener
    }

    private void OnSomeChange(string v) { m_TxtTitle.SetText(v); }
    private void OnBtnConfirmClick() { SendUIMessage((int)UIMessageId.OnConfirmClick); }
    // 普通 View 无需 override Destroy() 退订——框架自动清理 PropertyChangeHandler
}
```

## 流程

1. 读 GUI_PLAN.md（含**已定死的模块拆分 + ViewModel 设计**）+ 两库 query_pack（私有 + 公共，公共优先）相关坑点。
2. 读目标目录下**同类现有 panel** 与真实基类，对齐命名/生命周期/惯例。
3. **按 GUI_PLAN 的「模块拆分」实现 root + 各子 View/子 Panel**（拆分为「单 View」则只出 root）；拆分的
   引用关系/VM 归属见 `mvvm-contract.md §1.1`，子 View 实现细节见 `patterns/subview-pattern.md`。
4. 判断模式：列表 / 可复用组件 / 世界坐标跟踪等场景先查 `shared-references/patterns/`（决策树见 `patterns/README.md`）。
5. **若需新增/改 ViewModel 属性 → 按 mvvm-contract §3 的 4 步走**（无 ViewModel 变更可跳过 5b–5c）：
   - **5a** 照抄 plan 的 ViewModel 契约写 `ViewModelDes/*.cs`（不自行设计属性）。
   - **5b** 通过 **csharp-tool** 导出 ViewModel（`*ViewModel.cs` / `*_viewmodel.lua` / Factory / define），
     不依赖 Unity Editor 运行状态、**不要求前置编译**；csharp-tool 不可用 / 导出失败才手改补齐（见 mvvm-contract §3 硬规则）。
   - **5c** 生成 `Panel.lua` + `View.cs`（引用新常量 / 设 `self.rootViewModel.*`）。
   - **5d 编译**：写完 View/Panel 后，先通过 unity-cli 判断 Unity Editor 是否运行，再走对应路径触发
     C# 编译（unity-cli 或 Batch Mode），验证整体编译通过。两路径均不可用 → `BLOCKED` 记入清单。
6. 自检 Gate（见下）。
7. 记录状态：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-draft done
   ```

## Gate

- ViewModelDes 字段与 `GUI_PLAN.md` 的 ViewModel 设计一致（照抄，无自创属性）。
- 有 ViewModel 变更时，csharp-tool 导出已生成产物（或已降级手改），View/Panel 代码已写完，**最后编译已触发**（能连 Unity Editor 时）；编译不可用时记 `BLOCKED` 入 `HUMAN_REVIEW.md`。
- Panel 写的每个 ViewModel 属性 → View 中有对应读取/绑定（双向匹配）。
- 自动生成文件优先工具导出；若因导出失败手改，须带 `TODO(模拟导出)` 标记并记入 `HUMAN_REVIEW.md`。
- 生命周期订阅↔退订配对。

→ 进入 **gui-prefab**。
