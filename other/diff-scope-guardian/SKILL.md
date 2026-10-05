---
name: diff-scope-guardian
description: >-
  工程现场环路 P0。用于代码改完后的只读 diff 扩散审计,绑定 Builder 出口、
  进入 Review/Verify 前。检查实际 diff 是否越过目标契约、设计文档或预期改动面,
  防止顺手重构、格式化扩散、无关文件变更和未声明偏离。
---

# diff-scope-guardian —— 改完代码后的 diff 扩散审计

## 1. 触发条件

必须触发:
- `project-lifecycle` PHASE 2 Builder 宣称实现完成后,进入 PHASE 3 Review 之前。
- 非平凡代码改动完成后、最终回复或交付前。
- `git status` 或实际文件变更超出 preflight 的 Planned touch set 时。

不触发:
- 纯只读任务。
- 没有文件改动的问答/解释。
- 用户明确只要求展示某个命令输出且未修改文件。

## 2. 角色边界

只做:只读审计 diff 范围,产出《Diff Scope Report》。
不做:修改文件、替 Builder 修复、重新设计、把 advisory 发现直接当事实。

发现 blocker 时,结论是打回 Builder,不是在本 skill 内顺手改掉。

## 3. 审计输入

- 《目标契约》或用户请求的一句话目标。
- PHASE 1 设计文档/ADR,若本任务走了 lifecycle。
- `repo-preflight` 的 Planned touch set 和 Do-not-touch 边界,若已存在。
- 实际变更清单和 diff。

优先使用 `git status --short`, `git diff --stat`, `git diff --name-only`,
`git diff --check`, 以及针对变更文件的定向读取。非 git 现场要改用文件清单和读回核对,
并明确无法提供 git diff 证据。

## 4. 输出格式

```
Diff Scope Report
Intended scope: <目标/设计/计划改动面>
Actual changed files: <文件清单>
Unexpected changes: <无/列表>
Design deviations: <无/列表, 含是否已声明>
Orthogonal changes: <无/列表>
Diff hygiene: <通过/问题, 如冲突标记、尾随空白、生成物、秘密模式>
Validation evidence: <已跑命令/未跑及原因>
Blockers: <无/列表>
Warnings: <无/列表>
Verdict: <PASS -> hand off to Review/Verify / BLOCKED -> return to Builder>
```

## 5. 门禁

| 门禁项 | 严重度 | 检查 |
|---|---|---|
| DG0 NS/设计一致 | blocker | diff 是否仍服务目标契约和设计,无未声明偏离? |
| DG1 范围未扩散 | blocker | 变更文件是否都在 Planned touch set 或有明确理由? |
| DG2 无正交改动 | blocker | 是否没有顺手重构、格式化、重命名、清理无关代码? |
| DG3 变更可审 | blocker | 是否没有冲突标记、明显生成物误入、秘密/凭证模式? |
| DG4 验证对应 | warning | 已跑验证是否覆盖本次改动面?未跑必须显式报告。 |

任何 blocker 未解决时不得进入 PHASE 3 Review,也不得向用户宣称交付完成。

## 6. Advisory 纪律

- 静态扫描、审查建议、AI finding 都只是线索,必须用 diff、代码位置或可复现命令验证。
- 没有定位和证据的 finding 不得升级为 blocker。
- 发现真实问题时写清文件/位置/证据,不要用笼统质量判断替代审计。

## 7. 反例

- 不要把全仓格式化混在一个小 bug fix 里。
- 不要因为测试通过就忽略无关 diff。
- 不要在 guardian 阶段修改文件;应打回 Builder。
