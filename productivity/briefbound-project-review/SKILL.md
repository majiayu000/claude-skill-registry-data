---
name: briefbound-project-review
description: Use when Briefbound workflow needs a Chinese-first review of an entire repository, codebase, architecture, technical debt, test coverage, risk modules, maintainability, or project health before planning, refactoring, takeover, or prioritization. Do not use when the user has listed several goals and has not chosen among them, such as speed, structure, and interface.
license: MIT
---

# Briefbound Project Review

## 目标

对整仓或明确子系统做只读、证据化审查，找出最影响完成率、误改率和用户价值的问题。以理解与学习为目的的项目拆解交 `briefbound-project-dissection`；风险优先的接手审查仍由本 skill 负责。PR/diff 使用 `briefbound-pr-review`，具体 bug 使用 `briefbound-bug-review`。用户列出多个目标且尚未选定，例如速度、结构、界面，停止审查并交回 `briefbound-router` 对齐，到此结束：不写下一步建议，也不推荐方向。

## Briefbound task contract

- Context Boundary: 审查范围、实际读取的入口/模块/测试/配置/git/运行证据和排除范围。
- Output Contract: 项目健康结论、风险排序 findings、可连续执行的修复顺序和 Route Out。
- Allowed Action: 默认只读；不编辑文件、移动分支或修改 index。用户要求修复时由 Briefbound Router 建立执行契约。
- Success Evidence: finding 绑定文件/命令/运行证据、影响、最小动作和验证条件。
- Stop Condition: 范围不明或用户列出多个目标尚未选定、对象变成 PR/具体 bug、关键证据缺失、需要写入或高风险决策。
- Route Out: `briefbound-simplification-audit`、`briefbound-planning`、`briefbound-bug-review`、`briefbound-performance-engineering`、`briefbound-pr-review`、`briefbound-router` 或 BLOCKED。
- Support 图解：完整审查报告结构复杂时，自动加载当前可用的 `briefbound-diagram-design` 配图（不夺内容所有权），无需另问；短状态回复不配图。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文；保留技术字面量；只报结论、证据、风险和产出；Route Out 仅以 Briefbound task contract 为准。目标尚未选定，或只读审查已停在报告且没有顺序、范围、高风险需要拍板时，到此结束，不写下一步建议。需要拍板时末行才写 `下一步建议: <一个具体动作>`，不把可自行完成的步骤交回。

## 深度与证据

- `QUICK`：目录、README、配置、测试入口和近期 git 信号。
- `STANDARD`：默认；增加关键链路、依赖、CI、测试质量和边界。
- `DEEP`：接手、重构或高风险发布前；增加热点历史、状态/数据/权限/迁移风险。

不要为了全面扫描全仓。先确认事实源和高信号入口，再沿用户目标钻取 owning modules；证据足以回答审查目标时停止。按需检查架构边界、修改热点、真实行为测试、配置/数据/权限、发布回滚和接续成本，不为未命中的通用清单继续扩读。

## Findings

严重度：`P0` 数据/安全/核心不可用；`P1` 高风险缺陷或关键契约/测试缺口；`P2` 明显增加误改和维护成本；`P3` 非阻塞改进。

每条必须包含：位置或命令证据、具体观察、影响、最小有效动作、验证条件。不得把“项目复杂”“测试不足”“TODO 很多”直接当 finding；孤立实现 bug 不升级为项目 finding，除非证据表明它代表重复模式、架构边界或系统性风险。

Telemetry Gap 与已确认问题分开；WATCHLIST 必须写明升级、降级或关闭所需的日志、指标、测试或时间窗口。

## 执行顺序

多个 finding 按依赖、用户价值、误改风险和验证成本排序，而不是只推荐一个：

- `SAFE_DIRECT`：已有修复许可时依次执行并验证，不逐项询问。
- `PLAN_THEN_EXECUTE`：存在设计分叉时先规划，再回到执行。
- `DEFERRED`：只记录触发条件。
- `BLOCKED`：停止并问一个不可约问题。

只有顺序会改变产品取舍、范围或高风险动作时才让用户选择。只读审查请求本轮停在报告；没有这类拍板就不写下一步建议。用户说“继续/开始修复/按顺序修”时从第一个非 Deferred/Blocked 项连续推进。

## 输出

```text
项目审查: HEALTHY / WATCHLIST / NEEDS_ATTENTION / HIGH_RISK / BLOCKED
范围与关键证据: ...
Findings:
- P0/P1/P2/P3 [位置] 问题；影响；最小动作；验证条件
执行顺序（仅多个后续动作时）:
1. <动作> [SAFE_DIRECT/PLAN_THEN_EXECUTE/DEFERRED/BLOCKED]
证据缺口与剩余风险: ...
下一步建议: <仅顺序、范围或高风险需要拍板时写；目标未选定或只读报告无需拍板则省略>
```

没有 finding 时明确说明未发现结构性问题，并用一句话说明最重要的未覆盖边界。不默认生成项目地图、矩阵、ledger、完整扫描清单或专项路由清单。
