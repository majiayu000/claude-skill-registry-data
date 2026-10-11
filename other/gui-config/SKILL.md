---
name: gui-config
user-invocable: false
description: >-
  Atom Game GUI pipeline 第 4 阶段（按需，可跳过）。编辑 design/tables 下的 Excel 配置源表，
  并镜像改动到对应 *_data.lua（模拟导表，零人工中断）。自包含的配置表编辑指引，不依赖外部
  edit-excel skill。仅当功能涉及配置数据时使用。控制配置数据漂移。
---

# Phase 4: gui-config — 配置表编辑（按需，可跳过）

**职责**：自包含的配置表编辑。**控制：配置数据漂移（Excel 源表 vs lua data 不同步）。**

> **执行位置与并行**：本阶段**在 orchestrator 派发的 subagent 中执行**，与主 agent 的 gui-prefab（Phase 3）**并行**。
> 本 subagent **只做配表编辑**，把结果**结构化返回给 orchestrator**：`edited`（改了哪些 Excel/`*_data.lua`）
> / `skipped`（本需求不涉及配置）/ `blocked`（缺配表能力，需人工）+ 涉及的降级/TODO 说明。
> **run_state 由 orchestrator（主 agent）统一记账**——本 subagent **不自行写 `gui_run_state.py`**
> （会话作用域状态归主 agent，避免 subagent 缺 session env）。

若本需求不涉及配置数据 → 返回 `skipped`（由 orchestrator 记 `set <panelId> gui-config skipped`）。

## 规则（优先工具导表，导出失败才手改镜像；零人工中断）

1. 改 `design/tables/` 下的 **Excel 源表**（真正的真相源）。
2. **`*_data.lua` 优先用工具正式导出**：运行时若有可用的导表工具（GDE CLI / excel-config 等）→ 用它导出，**不手改**。
3. **导出工具不可用 / 失败 → 才允许手改镜像写入 `*_data.lua`**（降级兜底，模拟导表）：按行定位、同字段同值，
   严格对齐 GDE 导出格式，使运行期与后续阶段立即可见新配置；加 `-- TODO(模拟导出)` 标记并记入 `HUMAN_REVIEW.md`。
4. 区分两类「生成文件」，勿混淆——两者都**优先工具导出、导出失败才手改**：
   - `*_data.lua`（配表导出产物）—— 本阶段在导出失败时手改镜像写入，不是禁区。
   - `*_viewmodel.lua` / `*ViewModel.cs`（MVVM 生成）—— 同理优先工具导出，失败才手改（见 mvvm-contract §3）。

## 工具使用（不硬绑定 MCP）

- 运行时**已加载** excel-config / excel-mcp 等 → 用之读写 Excel 源表。
- **未加载** → 在 `HUMAN_REVIEW.md` 标出「需手工配表」，本阶段降级，管线继续。

## Gate

Excel 源表与对应 `*_data.lua` 改动**一致**（同字段、同值），运行期可读到新配置。

> ⚠ 若本次因导出失败而**手改镜像**了 `*_data.lua`：它是**模拟产物**，正式 GDE 导表会覆盖它。
> 故「确认 Excel 配置正确并正式导表」列入 `HUMAN_REVIEW.md`（gui-review 末），
> **绝不在管线中途停顿**。（若已用工具正式导出，则无此遗留项。）

编辑完成后 → **把结果返回 orchestrator**（`edited` + 改动文件 + 任何 `TODO(模拟导出)`/降级说明）。
orchestrator 在主 agent 侧据此记账，并在 gui-prefab **也落定后**统一进入 gui-review：
```bash
# ↓ 由 orchestrator（主 agent）执行，不在本 subagent 内跑
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-config done
```
