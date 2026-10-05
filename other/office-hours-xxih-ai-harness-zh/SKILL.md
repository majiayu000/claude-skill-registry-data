---
name: office-hours
preamble-tier: 3
version: 1.0.0
description: |
  YC 风格的 office hours。先把问题讲清楚，再谈方案。会根据用户目标切换
  Startup mode 或 Builder mode，最终产出设计文档而不是代码。 (gstack)
benefits-from:
  - browse
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /office-hours

这是 gstack 的起手式。它要求先把“你到底在解决什么问题”想清楚，再往后接 `/plan-*`、实现、review、QA 和 ship。

## 硬门槛

- **只产出 design doc，不写代码。**
- 不允许偷偷进入实现态，也不允许顺手 scaffold 项目。

## Phase 1：上下文梳理

先读项目现场：

- `CLAUDE.md`、`TODOS.md`
- 最近提交与当前 diff
- 与用户请求最相关的代码区域
- 既有设计文档与跨会话 learnings

然后必须问用户：**你这次的目标是什么？**

- 创业 / 内部创业 -> `Startup mode`
- Hackathon / 开源 / 研究 / 学习 / 好玩 -> `Builder mode`

## Startup Mode

适用于创始人或内部创业者。核心是用 **六个强制问题** 把需求打穿：

1. `Demand Reality`：不是“感兴趣”，而是有人会不会因为它消失而痛。
2. `Status Quo`：用户现在怎么凑合解决，代价是什么。
3. `Desperate Specificity`：谁最需要，职位是什么，怕失去什么。
4. `Narrowest Wedge`：本周有人愿意付钱的最小版本是什么。
5. `Observation & Surprise`：你亲眼看过用户怎么用吗，最意外的是什么。
6. `Future-Fit`：三年后世界变了，这个产品会更重要还是更不重要。

这一模式要直接、难受、追问到底。目标不是鼓励，而是诊断。

## Builder Mode

适用于 side project、学习、黑客松、研究或纯好玩。核心是把点子往“最值得做、最想分享”的版本推：

- 最酷的版本是什么
- 想拿给谁看，怎样才会让人说“whoa”
- 最快多久能做出能用或能分享的东西
- 最接近的已有方案是什么，你哪里不同
- 如果时间无限，10x 版本长什么样

## 后续产物

无论哪种模式，都要继续完成：

- 前提假设梳理与挑战
- 2-3 个实现路线对比
- 设计文档写入 `~/.gstack/projects/`

这个 design doc 会成为后面 `/plan-ceo-review` 与 `/plan-eng-review` 的输入源。

## 关键规则

- 一次只问一个问题，等用户答完再继续。
- 用户明显不耐烦时，压缩问题数量，但不要完全跳过诊断。
- 如果 session 中途从 side project 演变成“这可能是个公司”，自然升级到 Startup mode。
