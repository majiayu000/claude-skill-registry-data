---
name: pr-lifecycle
description: 当你要创建 PR、查看 review 或 checks 状态、处理评审反馈，或在条件满足时推进合并时使用。
---

# PR Lifecycle

这个 skill 解决的是“当前这轮要在 PR 生命周期里推进哪一步”。它是远端 PR 动作的统一入口，但不是默认自动跑完整闭环；先识别当前意图，再只执行本轮需要的动作。

## 何时使用

- 你要创建 PR、补充 PR 文案，或同步已有 PR 的状态
- 你要查看 review、comments、checks 或 merge blocker
- 你要处理评审反馈、请求 review，或在条件满足时推进合并
- 用户给的是组合动作，例如“提 PR 并请人 review”或“看状态，没 blocker 就 merge”

不适用：

- 还没有形成可评审的 diff
- 当前只是在做本地分支收尾，尚未进入远端 PR 流程
- 当前问题只是本地 merge / rebase 冲突，且没有 PR 上下文需要同步

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 当前动作范围
   - 本轮明确要做哪些原子动作
   - 哪些动作本轮不做
2. PR 当前状态
   - PR 编号 / URL
   - base / head
   - draft / ready
   - blocker 摘要
3. 执行结果
   - 本轮完成了什么
   - 下一步等什么
   - 若未明确要求，不自动进入下一个阶段

默认要求：

- 所有远端动作都围绕一个明确的 PR，或明确的 head / base 组合展开
- 默认只执行用户明确表达或可直接推断的那几个原子动作
- 用户没有授权时，不把“创建 PR”自动扩展成“请求 review / 处理反馈 / merge”
- 若上下文不清，先补齐状态，再决定是否继续推进

## 原子动作

这个 skill 内部只维护少量稳定原子动作：

1. `create`
   - 创建或更新 PR / MR 文案与远端记录
2. `request-review`
   - 发起或同步 review 请求
3. `handle-feedback`
   - 拉取并处理 review comments，回复原线程
4. `check-status`
   - 查看 review / checks / blocker 状态
5. `merge`
   - 在条件满足时 merge 或开启 auto-merge

遇到冲突、权限缺失或执行面不可用时，先停在当前动作，明确 blocker，不把失败合理化为“已经推进完成”。

## 路由规则

使用这个 skill 时，不要求用户先说出内部动作名；按意图和关键词路由即可。

常见映射：

- “提 PR”“开 PR”“发 PR”“创建 PR”
  - 路由到 `create`
- “开个 review”“找 reviewer 看一下”
  - 路由到 `request-review`
- “处理 review comments”“回评审意见”“看看 reviewer 说了什么”
  - 路由到 `handle-feedback`
- “看看 PR 现在什么状态”“CI 过了没”“还有什么 blocker”
  - 路由到 `check-status`
- “review 完就 merge”“如果都过了就合并”
  - 路由到 `check-status + merge`

如果用户意图不清：

- 先做 `check-status`
- 明确当前 PR 状态和 blocker
- 不自动推进到 `merge`

## 执行流程

1. 识别本轮意图
   - 先判断本轮要触发哪些原子动作
   - 明确哪些动作本轮不要做
2. 确认 PR 上下文
   - 当前是待创建分支，还是已有 PR
   - 明确 base / head、远端 URL、review / checks 状态
3. 执行被路由到的原子动作
   - `create`
     - 整理标题、摘要、测试计划
     - 创建或更新 PR
   - `request-review`
     - 准备 review 上下文
     - 发起 reviewer 或 review 请求
   - `handle-feedback`
     - 拉取 comments
     - 核实每条反馈是否成立
     - 回复原线程并记录剩余 blocker
   - `check-status`
     - 读取 review、checks、merge blocker 状态
   - `merge`
     - 仅在 blocker 清空或用户明确接受当前条件时执行
     - 选择 merge / squash / rebase merge / auto-merge
4. 总结状态
   - 记录本轮完成项、未完成项和下一步建议
   - 不自动假设要继续执行下一个原子动作

## 决策约束

- 这是入口 skill，不是默认全自动 pipeline
- 不要把“提 PR”自动扩展成“提 PR -> review -> merge”
- 不要在未确认完整远端状态前宣称 ready to merge
- 不要把本地 worktree 清理、远端 PR 推进、冲突处理混成同一个步骤
- 当用户给的是组合动作时，可以一次执行多个原子动作；但组合应来自用户意图，而不是 skill 自作主张

## 失败信号

- 一个 PR 已经开出来，但没有持续记录 URL、状态和 blocker
- comments 处理和 CI 修复互相脱节，导致重复劳动
- checks 还没绿就开始谈 merge
- 评论还没清空就误判 ready
- 用户只说“提 PR”，skill 却默认一路做到 merge
- merge 完没有记录结果，也没同步本地收尾
