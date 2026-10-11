---
name: gui-review
description: >-
  Atom Game GUI pipeline 第 5 阶段（唯一验证门）。并行两车道：Type-B 独立 gui-reviewer subagent
  （Bias Guard，品味判断）+ Type-A orchestrator 机械门（编译/LSP/prefab/生成文件/配置）。汇合成
  合并 CRITICAL 集合，产出 GUI_REVIEW.md + 6 态裁决 GUI_VERDICT.json + HUMAN_REVIEW.md。也可单独
  用于审查已有 GUI 代码。控制逻辑质量漂移 + 确定性验证。
---

# Phase 5: gui-review — 验证门（并行两车道）

**职责**：一个阶段、两条**并行**车道，汇合成合并 CRITICAL 门。
**控制：逻辑质量漂移（Type-B）+ 机器可验证正确性（Type-A）。**

> 基准文档：`${CLAUDE_PLUGIN_ROOT}/shared-references/verification-gates.md` 与 `acceptance-gate.md`。
> 本阶段合并了原独立的 gui-verify——Type-B 与机械 Type-A 不再分两个阶段跑两遍 reviewer。
> **全程无中途 HUMAN_CHECKPOINT**：需人确认项统一收口到 `HUMAN_REVIEW.md`，管线继续。

## Bias Guard 规则（Type-B 车道最关键）

- 每次审查用 **全新 subagent**（agent type: `gui-reviewer`），**不传**之前的 thread/context。
- 审查 prompt 中**不包含**「我们改了什么」「上一轮提到」等实现细节。
- 只传递：**当前代码文件 + GUI_PLAN.md + 相关 shared-references**。
- 审查者只能从代码本身判断质量。

## 并发安全

两条车道都只**读**同一份 draft 后冻结的产出，谁都不写文件，无竞态。Type-A 由 orchestrator 就地跑
（确定性、低风险，`acceptance-gate.md` §1 认可执行者自跑 self-check）；Type-B 交独立 subagent。

## 流程

1. 收集 Phase 2-4 的产出文件路径（Panel.lua / View.cs / ViewModel / 改动的 prefab / Excel↔data）。

2. **Type-B 车道（后台 spawn，不阻塞）**：用 Agent 工具
   `subagent_type: "gui-reviewer"`、`run_in_background: true` spawn，传入：
   - 待审代码文件
   - `${CLAUDE_PROJECT_DIR}/.claude/dev-gui-runs/<panelId>/GUI_PLAN.md`
   - 相关 `${CLAUDE_PLUGIN_ROOT}/shared-references/*.md`（含 `patterns/` 涉及的进阶模式）
   - **不传**任何实现叙述。
   subagent 按 5 个品味维度审查（见 `agents/gui-reviewer.md`），产出 `GUI_REVIEW.md` 到 run 目录。

3. **Type-A 车道（等 subagent 期间 orchestrator 自跑，机器可验证）**：逐项判
   `passed | failed | skipped`，缺能力判 `BLOCKED`/`NOT_APPLICABLE` 记入清单：
   - **C# 编译**（按两路径规则：Editor 运行中 → unity-cli 读 Console / refresh；Editor 未运行 →
     Batch Mode 编译（`./unity/WindowsEditor/Unity.exe -projectPath ./client/ -batchmode -quit ...`）；
     两路径均不可用 → `BLOCKED`）
   - **Lua 语法**（Claude Code LSP 诊断 `.lua` 文件；LSP 不可用则 `BLOCKED`）
   - **Prefab 节点存在 / 绑定数量匹配**（有 Prefab 能力则核实，否则 `BLOCKED`）
   - **生成文件优先工具导出**（`*_viewmodel.lua` / `*ViewModel.cs` 的 diff；`*_data.lua` 例外）
     - 例外：diff 带 `TODO(模拟导出)` 标记 → 判 `BLOCKED`「待工具正式重新导出覆盖」记入清单，
       **不判 failed、不触发 improve**
     - 无标记的手改（本可用工具却未用）→ 仍判 `failed`
   - **配置 Excel↔data 同步**（无配置变更 → `NOT_APPLICABLE`）

4. **汇合两车道 → 合并 CRITICAL 集合**：
   - `{Type-A 编译失败}` ∪ `{Type-A Lua 语法错误}`（**编译/语法失败升为 CRITICAL**）
   - ∪ `{Type-B 报出的 CRITICAL}`
   - 机械门的 `BLOCKED` / `NOT_APPLICABLE`（缺能力/不适用）**不进** CRITICAL 集合——否则缺
     Unity/Prefab 能力会把管线拖进 improve 死循环，只记 `HUMAN_REVIEW.md`。

## 6 态裁决 → `GUI_VERDICT.json`

```json
{
  "panel_id": "xxx",
  "verdict": "PASS|WARN|FAIL|NOT_APPLICABLE|BLOCKED|ERROR",
  "type_a_gates": { "compile": "passed", "lua_syntax": "passed", "...": "..." },
  "type_b_gates": { "interaction": "passed", "perf": "passed", "layout": "passed" },
  "critical_count": 0,
  "summary": "...",
  "timestamp": "2026-06-16T..."
}
```

| Verdict | 含义 | 需人工签字 |
|---------|------|-----------|
| PASS | 全部通过、无 CRITICAL | 否 |
| WARN | 有 MAJOR/MINOR 无 CRITICAL | 否 |
| FAIL | 有未修复 CRITICAL（Type-A 编译/语法失败 或 Type-B CRITICAL） | 是 |
| NOT_APPLICABLE | 某项不适用（如无配置变更） | 否 |
| BLOCKED | 检查条件不满足（Unity 未开、缺 MCP、模拟导出待覆盖） | 是 |
| ERROR | 检查执行出错 | 是 |

> 「需人工签字」≠ 停顿。FAIL/BLOCKED/ERROR 写进 `HUMAN_REVIEW.md`，管线继续。

## 产出 `HUMAN_REVIEW.md`（最终统一人工检查清单）

```markdown
# Human Review: <panelId>
- [ ] Excel 配置正确性 + 正式 GDE 导表（覆盖模拟写入的 *_data.lua）
- [ ] 运行期效果：打开 panel 截图核对交互与布局
- [ ] 未解决 CRITICAL（如有）：<file:line + 原因>
- [ ] BLOCKED / 降级项：<因环境缺失未能自动验证的项>
```

## Gate（分支）

- **合并 CRITICAL == 0** → `accept` 本阶段，跳过 gui-improve，直接进入 **gui-learn**。
- **合并 CRITICAL > 0** → 进入 **gui-improve**（迭代修复，最多 2 轮）；每轮修完**重跑本阶段两车道**。

## 记录状态

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-review done
# 合并 CRITICAL == 0（独立 reviewer + 确定性 Type-A 均通过）→ accept：
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" accept "${CLAUDE_PROJECT_DIR}" <panelId> gui-review \
    --reviewer gui-reviewer+type-a --verdict-id <run>/GUI_VERDICT.json
# 无 CRITICAL 时同时把 gui-improve 显式跳过：
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-improve skipped
```

## 审查维度

**Type-B（gui-reviewer，品味）**：MVVM 一致性 / 生命周期正确性 / 空安全 / 性能反模式 / 代码规范。
**Type-A（orchestrator，机械）**：C# 编译 / Lua 语法 / Prefab 绑定 / 生成文件导出 / 配置同步。
（Type-B 详见 `${CLAUDE_PLUGIN_ROOT}/agents/gui-reviewer.md`。）
