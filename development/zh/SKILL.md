---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: 系统化 Bug 扫荡工作流，包含基于代码库规模的目标值计算、翻倍升级机制、区域追踪及最终验证。适用于执行 /bugsweep 或用户要求进行系统化 Bug 排查时。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="bugsweep banner">

> **中文** — `bugsweep` 官方中文版本。


# /bugsweep — 系统化 Bug 扫荡工作流 (中文)

具有收敛停止条件的迭代式 Bug 排查流程。根据代码库规模按比例调整目标，在搜索显得过于表面时触发升级，并通过区域追踪防止重复检查。

## 1. 计算基础搜索轮数 (base_rate)

```
LOC = productive source lines (src/, lib/ — excluding tests, configs, docs, generated)
x = max(1, ceil(LOC / 1500))
base_rate = x * 3
```

| LOC | x | 基础轮数 (Base rate) |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

向用户汇报: "代码库规模: {LOC} LOC → 基础轮数 = {base_rate} 次无 Bug 搜索轮次。"

## 2. 搜索循环

```
counter = 0
target = base_rate
any_bug_found = False
checked = []  # (area_name, type: code|task)

LOOP:
  area = pick_new_area()  # see area rules
  checked.append(area)

  Perform a thorough bug search

  IF bug found:
    any_bug_found = True
    Fix following bugfix-protocol (phases 4+5)
    Review: see model rule (newer model classes: no external review needed)
    Commit + push
    counter = 0  # RESET
  ELSE:
    counter += 1
    Report: "✓ Clean: {area} — {counter}/{target}"

  IF counter >= target:
    IF NOT any_bug_found:
      # Doubling escalation: not a single bug → search too shallow?
      target = base_rate * 2
      any_bug_found = True  # escalate only ONCE
      Report: "⚠ No bug in {base_rate} passes → target doubled to {target}."
      CONTINUE LOOP
    ELSE:
      GOTO final verification
```

### 搜索循环实践注意事项 (来自实际扫荡经验)

- **非 Git 仓库:** 在没有 `git` 的环境中（例如云端同步的项目文件夹），使用**版本化备份**代替 "commit + push"：在首次修复前创建 `file_<ts>.bak`。**注意 — 修复前的备份并非最终工作备份:** 完成最后一次修复后，务必再创建一个新的 `_FINAL_` 备份，否则同步波动可能会抹掉整个修复过程。
- **初始即已知多个 Bug:** 如果在开始前就已经已知 N 个 Bug（例如来自先前的运行），按 "每个 Bug: 修复 → 审查 → 提交 → 重置" 的方式操作是不切实际的。应将已知 Bug 作为单个修复块进行统一处理（在结尾统一审查），并从发现第一个**新发现的** Bug 开始计算基础轮数/搜索循环。重置逻辑依然适用于在扫荡过程中新发现的 Bug。
- **同一 Bug 存在于多处:** 发现的缺陷（例如错误的正则表达式、错误的格式假设）往往会在其他地方被复制。每次修复后，应在其他位置搜索相同模式 — 这本身就是一个非常有价值的独立“区域”。

## 3. 区域规则 (防止敷衍)

“区域”可以是一个**代码重点**，也可以是一个**任务**（代码的功能目的）。

### 代码重点
- 可以在轮次之间**扩展**（更多文件）或**转移**（不同部分）
- 绝不能与先前轮次的选择完全相同
- 合规: 第 1 轮 = `maintenance.py`，第 5 轮 = `maintenance.py + orchestrator.py`（扩展）
- 不合规: 第 1 轮 = `maintenance.py`，第 5 轮 = `maintenance.py`（完全相同）

### 任务 (功能目的)
- 可以**细化**（检查子函数）或**扩大**（将相关函数组合在一起）
- 绝不能与先前轮次完全相同的任务
- 合规: 第 1 轮 = "watchdog 中的线程安全"，第 5 轮 = "整个托盘区中的线程安全"（扩大）
- 合规: 第 1 轮 = "进程检测"，第 5 轮 = "进程检测内部的存储标记匹配"（细化）
- 不合规: 第 1 轮 = "watchdog 中的线程安全"，第 5 轮 = "watchdog 中的线程安全"（完全相同）

### 命名规范
- 区域必须在搜索**开始前**完成命名（不得事后追溯分配）
- 格式: `"{name}" ({type}: code|task)`

## 4. 最终验证

当 counter >= target 且 any_bug_found 时:

**步骤 A — bugfix-protocol 第 5 阶段:**
- [ ] 完整测试套件通过 (`pytest`)
- [ ] **至少实际执行一次修改后的执行路径** — 而不仅仅是运行测试。对从未调用修改位置的代码运行单元测试并保持全绿属于假安全。运行实际修改后的路径（试运行 dry run、冒烟测试 smoke run、CLI 调用）并检查是否存在 traceback、签名或命名错误。`py_compile` 或单纯的 import 只能检查语法，无法验证路径是否正常运行。
- [ ] **每个修复都必须至少有一个触发它的测试** — 如果修复缺少能实际触发修改分支的测试，则视为未验证（对于编排/网络路径，必要时结合 mock + dry run）。
- [ ] 类型检查（若已配置）
- [ ] 代码检查 Lint（若已配置）
- [ ] 已检查本轮修复涉及的边缘情况

**步骤 B — 审查 (模型规则):**
- **较新的模型类别（例如 Claude 5 / Fable 级别）:** 无需外部顾问或第二模型审查。步骤 A（测试 + 实际冒烟运行）即为验证依据。若确实存在不确定性，可独立召唤新的审查子智能体 — 但必须先通过实证检验（在未修改的代码上测试其发现），再将其归为 Bug。背景（2026-06-11 扫荡经验）：当时第二审查员不可用，替代子智能体给出了 1 个发现（置信度 85%），但测试证明其并非 Bug — 外部审查未对结果产生改变。
- **较旧的模型:** 与顾问进行总结讨论（备选方案：第二模型作为审查员）；顾问予以确认或指出遗漏。

**如果在验证期间发现 Bug:**
→ 修复 + 测试 + 提交
→ 重置: counter = 0, target = base_rate（全新的基础轮数，不翻倍）
→ 返回搜索循环（已检查清单 checked 保留，any_bug_found = True）

**如果验证完全无误:**
→ 完成。Commit + push。输出协议总结。

## 5. 协议总结 (结尾处)

```markdown
## Bug Sweep Result

- **Codebase:** {LOC} LOC
- **Base rate:** {base_rate} (escalated: {target})
- **Areas checked:** {len(checked)}
- **Bugs found:** {count}
- **Resets:** {reset_count}
- **Doubling triggered:** yes/no
- **Fixes:**
  - {title} — {commit_hash}
  - ...
- **Final test suite:** {passed}/{total} green
- **Review verdict:** self-verification (newer model class) / advisor confirmed / gaps named
```

## 何时使用此工作流

- 特性开发完成后（质量保证）
- 版本发布前（验收扫荡）
- 定期作为代码卫生检查
- 当用户输入 `/bugsweep` 时

## 与其他 Skill 的交互

- **bugfix-protocol:** 针对每个发现的 Bug 的修复流程（第 4+5 阶段）
- **systematic-debugging:** 用于扫荡过程中难以复现的 Bug
- **code-review:** 可用作任务区域

---

## 更新日志

### 1.1.0 (2026-06-13)
- 移植了步骤 B 的模型规则（源自本地 Skill 安装，状态 2026-06-11）：较新的模型类别通过测试 + 实际冒烟运行进行自我验证，无需外部审查；协议字段 "Review verdict" 相应扩充

### 1.0.0 (2026-06-13)
- 在 Skill 库中首次发布（采纳自本地 Skill 安装，状态 2026-06-01）
