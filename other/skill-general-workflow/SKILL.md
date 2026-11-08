---
name: general-workflow
description: 通用开发工作流技能。覆盖头脑风暴与方案收敛、spec/计划写作、任务拆解与执行纪律、完成前验证、Git worktree 与分支收尾、合并冲突、pre-commit、CI/CD 质量门禁、陌生代码库摸底、代码简化、问题分诊、代码审查协作礼仪。触发词：头脑风暴、设计、写计划、拆任务、执行计划、验证、声称完成、worktree、合并冲突、分支、收尾、pre-commit、CI、质量门禁、摸代码库、理解代码、简化代码、重构、issue、triage、分诊、发起审查、回应审查、brainstorm, write plan, task breakdown, execute plan, verify, claim completion, git worktree, merge conflict, finish branch, codebase recon, simplify code, code review, issue triage。用于：开始新功能前设计、拆解复杂任务、严格验证"完成"、管理多分支并行开发、进入陌生代码库、整理技术债等场景。
metadata:
  agent_created: true
---

# General Workflow（通用开发工作流）

从想法到交付的开发流程纪律。核心立场：**没有设计不写码，没有验证不称完成，没有闭环不提修复**。

## 症状 → 加载哪个 reference

| 症状 / 任务 | 加载 |
|---|---|
| 需求模糊要先对齐；要收敛点子/评估方案；写 spec 或实现计划 | `references/plan-and-spec.md` |
| 执行计划中卡住；验证"是否真的完成了"；宣称通过/修好前 | `references/execution-verification.md` |
| 多分支并行；合并冲突；分支收尾；配 pre-commit/CI | `references/git-branch-ci.md` |
| 进陌生代码库；简化/重构代码；设计模块边界 | `references/codebase-understanding.md` |
| 处理 issue 队列；发起/回应代码审查 | `references/triage-collaboration.md` |

## 铁律

**MUST**
- 未先呈现设计并获批准前，禁止写实现代码或脚手架；简单项目允许几句话的设计但必须呈现批准。
- 每个实现计划以固定头开始：Goal 一句话 / Architecture 2-3 句 / Tech Stack / 依据的 spec 路径；假设执行者对代码库零上下文。
- 每个任务能在 2–5 分钟完成并自带测试循环：写失败测试→跑确认失败→最小实现→跑确认通过→commit；写不出失败测试的任务视为过大，继续拆。
- 任务描述必须含精确文件路径（含行号）、接口签名、预期输出；禁止"添加校验""修复 bug"这类无路径无预期输出的描述。
- 未经用户明确同意，绝不在 main/master 分支上开始实现。
- 每任务依次：标 in_progress→严格按步执行→跑计划内验证→标 completed，不跳验证。
- 声称"通过/完成/修好"前，必须在本轮已运行的验证命令输出中读到证据（0 failures / exit 0 / 逐条 checklist）。
- 合并前确认 base 分支（不确定就问）；合并冲突解决时尽可能保留双方意图，禁止发明新行为。
- 简化代码前先理解它为何存在（Chesterton's Fence）；一次只改一项，每项后跑测试套件。

**NOT**
- 禁止"先快速修，以后再查"“加个 try/catch 压住”“大概是 X，先试试"式修复——回到根因。
- 禁止多个修复同时上、混入"顺手改"、重构与功能同 PR、依赖批量 bump（一依赖一变更）。
- 禁止 `git merge --abort` 放弃冲突解决；禁止对远端已前进的分支擅自 force-push。
- 禁止在未忽略 `.worktrees/` 前创建 worktree（整树会被误提交）。
- 禁止只写"write tests"不给测试代码；禁止计划中出现 TBD/TODO/implement later。
- 计划被更新或根本方法需重想时，禁止闷头继续执行——回到 Review。

## 工作流（从想法到交付）

1. **头脑风暴**：澄清提问一次一个；给 2-3 个方案带取舍与推荐；设计分节呈现并逐节确认。
2. **写计划**：spec 自审（占位符/一致性/范围/歧义）→ 计划落盘 `docs/plans/YYYY-MM-DD-<topic>.md`。
3. **执行**：挑剔性审读计划 → 按任务循环推进；四种情况立即停下询问（阻塞/缺信息/指令不明/验证反复失败）。
4. **验证**：断言前门禁五步（识别命令→全新运行→读全部输出→核对断言→才可断言）。
5. **收尾**：全量测试绿 → 确认 base → 合并/PR → 清理 worktree。
6. **反思**：无价值的 pass-through 模块删除；僵尸代码（无引用/无测试）清除。

## 参考索引

5 个 reference 均按"第一步→判据→如何证明根因"组织；`plan-and-spec.md` 含 spec 模板与任务尺寸表。

