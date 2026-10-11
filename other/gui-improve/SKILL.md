---
name: gui-improve
user-invocable: false
description: >-
  Atom Game GUI pipeline 第 6 阶段。对 gui-review 合并 CRITICAL 集合（Type-A 编译/语法失败 +
  Type-B CRITICAL）迭代修复（最多 2 轮）：修复 → 重跑 gui-review 两车道（Bias Guard）→ 记录
  GUI_IMPROVEMENT_LOG.md。仅当 gui-review 报出合并 CRITICAL 时使用。2 轮后仍有 CRITICAL 则记入
  HUMAN_REVIEW.md，不暂停。
---

# Phase 6: gui-improve — 迭代修复循环

**职责**：修复合并 CRITICAL → 重跑 gui-review 两车道，**最多 2 轮**。

## 流程

```
Round 1:
  1. 读合并 CRITICAL 集合来源：GUI_REVIEW.md（Type-B）+ GUI_VERDICT.json 的 type_a_gates
     （编译/Lua 语法失败）+ MAJOR 问题
  2. 按优先级修复（CRITICAL → MAJOR；含编译/语法错误）
  3. 重跑 gui-review 两车道：Type-B 全新 spawn gui-reviewer（Bias Guard）+ Type-A 机械门
  4. 对比新旧结果（新 GUI_REVIEW.md + GUI_VERDICT.json）
  5. 记录 GUI_IMPROVEMENT_LOG.md

Round 2（如仍有合并 CRITICAL）:
  重复 1-5，修复剩余 CRITICAL

2 轮后仍有合并 CRITICAL:
  → 把未解决项写入 HUMAN_REVIEW.md（逐条 file:line + 原因），不暂停
  → 继续跑 gui-learn，由最终人工清单统一收口
```

## Bias Guard 实现（每轮重跑 gui-review 的 Type-B 车道）

spawn 全新 `gui-reviewer` subagent，**不在 prompt 中包含**：
- 上一轮的审查结果
- 「我们已修复了 XXX」
- 之前 subagent 的 threadId

**只传递**：当前代码文件 + GUI_PLAN.md + 相关 shared-references。
（理由见 `${CLAUDE_PLUGIN_ROOT}/shared-references/acceptance-gate.md`：执行者不能为自己的修复辩护。）

## 输出 `GUI_IMPROVEMENT_LOG.md`

```markdown
# GUI Improvement Log: <panelId>

| Round | Score Before | Score After | Key Changes |
|-------|-------------|------------|-------------|
| 1 | 5/10 | 7/10 | 修复空指针、补充事件退订 |
| 2 | 7/10 | 8/10 | 优化列表滚动性能 |

## Round 1
### Issues Fixed
1. [CRITICAL] ...
### Review After Fix
[新审查结果摘要]
```

## 记录状态

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-improve done
```

→ 回到 **gui-review** 重跑两车道出最终裁决（更新 GUI_VERDICT.json），再进 **gui-learn**。
