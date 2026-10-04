---
name: problem-to-solution
description: >
  问题到方案 Workflow：当用户显式调用 `$problem-to-solution`，或明确要求运行“问题到方案”完整流程时使用。
  把模糊产品问题经过校准、必要的研究/决策、方案生成和挑战，推进为一个可进入 PRD 的已确认方案；不负责 PRD 交付或外部发布。
---

# 问题到方案

这是 `workflow` 的 Codex Runtime 入口，不是新的原子 Skill。先读取同目录 `WORKFLOW.md`，再按当前状态调用现有 Skill 或 Loop。

## 输入

优先从对话和项目材料中发现以下信息，只询问会改变路线的缺口：

- 当前问题或模糊感受；
- 期望结果与判断标准；
- 用户、业务场景、约束和截止时间；
- 已有事实、候选方案和不可改变项。

## 工作流

1. 先判断输入状态：问题、目标或判断标准不稳定时使用 `ai-collaboration-calibration`；已经稳定时跳过校准。
2. 只有当事实缺口会改变选择时才进入研究：开放式领域理解使用 `research-topic-compiler`，具体选择缺证据时使用 `$decision-loop`。
3. 问题已稳定但没有候选方案时，直接使用 `brainstorming` 比较真实方案并形成推荐与 Design Spec。
4. 已有候选方案且只需挑战时，直接进入 `$solution-loop`；其他情况只在方案风险、依赖或失败模式需要多轮关闭时进入。
5. 按 `WORKFLOW.md` 的 Confirmed Solution Gate 判断结束、Human Gate 或阻塞，不用文档数量代替方案确认。

## 边界

- 不为了走流程而调用全部 Skill。
- 不把研究结论直接伪装成产品方案。
- 不让 Maker 自己声明挑战已经关闭。
- 不生成完整 PRD、UI 交付包、研发事项或外部发布结果。
- Skill/Loop handoff 不授权 DingTalk、Yunxiao、Runtime 或 Skillshare 写入。

## 输出

返回 `status`、稳定的问题定义、关键决策、已确认方案、保留项、剩余 gap、下一责任节点和恢复点。只有达到 `solution_confirmed` 才建议进入 `$solution-to-delivery`。

## 完成定义

只有 `WORKFLOW.md` 的 Confirmed Solution Gate 全部成立，且需要业务取舍时已经经过 Human Gate，才输出 `solution_confirmed`。否则必须返回唯一 `next_gap` 和可恢复的 `resume_point`。

## 资源与验证

- `WORKFLOW.md` 是阶段路由、完成门槛和输出状态的权威合同，每次执行前读取。
- `evals/evals.json` 覆盖完整路径、最短路径、相邻原子 Skill 和下游 Workflow 的触发回归；修改入口后运行这些评测并保留结果。
