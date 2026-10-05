---
name: design-shotgun
preamble-tier: 4
version: 1.0.0
description: |
  多方案视觉探索器。结合上下文、taste memory 和并行生成，产出多版设计方向，
  再通过 comparison board 与反馈循环收敛出一个被批准的方向。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /design-shotgun

`/design-shotgun` 的任务不是“直接给一个设计”，而是**快速做出多种方向，再让用户有证据地选**。

## 核心流程

1. `Session Detection`：判断当前是不是同一条设计会话的延续。
2. `Context Gathering`：读需求、已有设计系统、相关页面与品牌约束。
3. `Taste Memory`：利用过去偏好，为生成方向加偏置。
4. `Generate Variants`：
   - 先生成概念
   - 让用户确认概念方向
   - 再并行生成多版结果
5. `Comparison Board + Feedback Loop`：把不同版本放进对比板，围绕具体差异收集反馈。
6. `Feedback Confirmation`：确认用户到底保留了哪些元素。
7. `Save & Next Steps`：沉淀被选中的方向，为 `/design-html` 或后续实现做准备。

## 关键规则

- 必须提供“有明显差异”的多个方向，而不是一组轻微扰动。
- 用户反馈要尽量落到具体元素、布局、节奏与信任感上，而不是泛泛“更好看”。
