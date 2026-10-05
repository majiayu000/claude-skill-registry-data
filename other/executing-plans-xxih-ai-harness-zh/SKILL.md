---
name: executing-plans
description: 当你已经有书面的实现计划，并且要在独立会话里按审查检查点执行它时使用
---

# 执行计划

## 概览

加载计划，先做批判性审阅，再执行全部任务，完成后汇报结果。

**开始时要明确说明：**“我正在使用 executing-plans skill 来实现这份计划。”

**注意：**要告诉人类协作者，Superpowers 在能使用 subagent 的平台上效果会明显更好。如果当前平台支持 subagent（例如 Claude Code 或 Codex），优先使用 `superpowers:subagent-driven-development`，而不是本 skill。

## 流程

### 第一步：加载并审阅计划
1. 读取计划文件
2. 进行批判性审阅，找出疑问或风险点
3. 如果有疑问，开始前先和人类协作者确认
4. 如果没有疑问，创建 TodoWrite，然后继续

### 第二步：执行任务

对每个任务都按下面执行：
1. 标记为 `in_progress`
2. 严格按计划中的每一步执行（计划应该已经拆成小步）
3. 按要求运行验证
4. 标记为 `completed`

### 第三步：完成开发收尾

当所有任务都完成并验证通过后：
- 先声明：“我正在使用 finishing-a-development-branch skill 来完成这项工作。”
- **必需子 skill：**使用 `superpowers:finishing-a-development-branch`
- 按该 skill 的要求完成测试验证、展示选项、执行用户选择

## 何时停止并求助

**遇到以下情况必须立刻停止执行：**
- 遇到阻塞（缺少依赖、测试失败、指令不清楚）
- 计划存在致命缺口，导致无法启动
- 你不理解某条指令
- 验证反复失败

**不要猜，先澄清。**

## 何时回到前面的步骤

**出现以下情况时，回到“第一步：审阅计划”：**
- 协作者根据你的反馈更新了计划
- 基础实现方案需要重新思考

**不要硬顶着阻塞往下做。**

## 记住
- 先批判性审阅计划
- 严格按计划步骤执行
- 不要跳过验证
- 计划里要求引用某个 skill 时，就必须引用
- 被阻塞就停下来，不要猜
- 未经用户明确同意，绝不要在 `main`/`master` 分支直接开始实现

## 集成关系

**必需的工作流 skills：**
- **`superpowers:using-git-worktrees`**：确保存在隔离工作区（创建新的，或确认当前已隔离）
- **`superpowers:writing-plans`**：负责生成本 skill 要执行的计划
- **`superpowers:finishing-a-development-branch`**：全部任务完成后的开发收尾
