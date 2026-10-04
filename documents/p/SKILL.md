---
name: p
description: Breaks a SPEC into small verifiable tasks, records the rationale for every design choice, and generates a technical design document for human review. Use when a spec exists and work needs slicing, when the user says /p, or when asked to plan, break down or sequence a change.
---

# /p —— SPEC → 技术设计 + 计划 + 任务 + 选型理由

## 输入

`SPEC.md`（没有就先跑 `/s`，不要替用户臆造需求）+ 相关代码 + `docs/intent/`。

**先进只读模式**：读代码、理清组件依赖，再动笔。

## 产出

四样东西，缺一不可：

### 1. `docs/design/<工作项ID>/technical-design.md` —— 给人 review 的技术说明

使用 `docs/templates/technical-design.md`，基于 SPEC、相关代码和本轮规划同步生成，写清现状、
方案、接口、数据、安全、依赖、测试、灰度与回滚，方便研发人员查看。

工作项 ID 从 Meegle 工作项、SPEC 或当前分支名读取；多个来源不一致时停下来确认，不得猜测。
项目模板不存在时停止并提示重新执行 `/init`，不得自行编造模板。

简单改动也生成，但保持简短；不涉及的关键章节明确写“无变更”，不要编造复杂方案，
也不要留下看似完整的空表格。

### 2. `tasks/plan.md` —— 分几个阶段实施

按阶段组织，每阶段写清改哪些模块、验收标准、验证方式。

### 3. `tasks/todo.md` —— 做什么

checklist，**纵向切分**：一个任务 = 一条完整路径（能独立验证、能独立提交），
不是「先写完所有 model 再写所有 controller」。

每个任务小到能在一次专注会话里完成实现 + 测试 + 验证。

```markdown
- [ ] Task 1: <一句话> — 验收：<怎么算完成>
```

### 4. `docs/intent/<主题>.md` —— 为什么这么选 ★

**只要某一步存在两个以上可行方案，就当场记下来：**

```markdown
## <决策点>
- 候选：A / B / C
- 选择：B
- 理由：<为什么>
- 否决 A 的原因：<为什么不>
- 否决 C 的原因：<为什么不>
```

**必须在决策当时写。** 只存在于本次会话里的理由，会话一结束就没了；
事后从代码里读不回来，从 diff 里更推不出来。这是后面 MR 的 Why 段唯一的原料来源。

## 规则

1. **规划期间不写代码。**
2. 技术设计是本轮规划的伴随产物，不增加新的审批或阻塞节点。
3. 阶段之间插检查点：跑到这里应该能验证什么。
4. 一个任务 = 一个人 = 一个 commit。多人并行时在 todo 里标认领人。
5. 计划要给人确认后再进 `/b`。**生成计划的人不批准计划。**

## 何时进下一步

`docs/design/<工作项ID>/technical-design.md` 已生成，`tasks/todo.md` 每条都可独立验证，
`docs/intent/` 里记下了这一轮所有的多选一。
然后跑 `/b`。

## Red Flags

- `docs/intent/` 是空的，但你在计划里做了 3 个技术选型
- 技术设计与 `tasks/plan.md` 复制同一段方案，后续必然漂移
- 简单改动生成十几页空表格，用文档体积冒充设计质量
- 任务是横向分层（「实现所有 API」），验证不了单条
- 任务大到一次会话做不完
- 计划里出现 SPEC 没要求的功能
