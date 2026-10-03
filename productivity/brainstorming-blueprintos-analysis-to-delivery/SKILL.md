---
name: brainstorming
description: 反复提问澄清需求,产出设计稿 — 来自 superpowers 体系(obra/superpowers)。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/brainstorming/。
version: 4.0.0

---

# Brainstorming(桥接到 superpowers)

## Contract

- Inputs: feature idea, user constraints, optional signed analysis-delivery docs
- Outputs: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- Gates: user agrees the design captures intent
- Required disciplines: `stage-gate`
- Next: `/design-an-interface` or `/writing-plans`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/brainstorming/SKILL.md`

## 何时调

- 拿到新需求/新功能,需要先与用户对齐
- 在 `analysis-delivery-workflow` 阶段 2(grill-task)之后
- 在 `dev-design` 阶段 7 之前

## 如何调

```bash
# 方式 1:直接调 superpowers 官方
/brainstorming
```

## 衔接点

- **产出**:`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- **下一步**:`/writing-plans`(拆任务)
- **门控**:`disciplines/stage-gate` 第 2 层

> 🚧 **桥接层不重复 superpowers 内容**,保持单一权威源。

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/brainstorming/` 不存在,按以下 4 步在本仓库独立完成脑暴:

### 1. 5 问澄清

逐一问用户以下 5 个问题,**一次一个问题,不堆叠**:

| # | 提问 | 目标 |
|---|------|------|
| 1 | 这个功能给谁用?(角色 / 使用场景) | 锁定用户 |
| 2 | 解决他们什么具体问题? | 锁定价值 |
| 3 | 不做会怎样?(现状如何) | 锁定紧迫性 |
| 4 | 成功长什么样?(可观测的产物) | 锁定验收标准 |
| 5 | 范围边界?哪些场景**不**做? | 锁定非目标 |

任何问题用户答"不知道" → 拆子问题再问,**禁止替用户编答案**。

### 2. 3 候选设计

基于澄清结果,**生成 3 个候选方案**,每个含:

- **核心思路**(1-2 句)
- **关键数据结构 / 接口**(粗略)
- **影响范围**(哪些文件/模块要改)
- **取舍**(选 A 牺牲了什么 / 得到了什么)

### 3. 用户选 1 + 反馈循环

把 3 个候选展示给用户 → 用户选 1 → 允许其修改细节 → 输出**设计稿**到 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`。

### 4. 签字闭环

设计稿末尾加 `## Sign-off`,等用户**白名单话术**(4 句之一)签字:

- "我已全部确认,可以进入下一步"
- "确认通过"
- "全部完成,继续"
- "approved, proceed to next stage"

❌ "OK/好/继续" 一律不视为签字。

### 最小纪律摘要(脑暴专用)

- **一次一问**:堆叠问题 = 用户答不全
- **3 候选而非 1**:多视角避免单点盲区
- **写下来不靠记忆**:产出 design.md 是脑暴的**唯一**交付物
- **签字才能进下一阶段**

### 安装提示

```bash
npx skills@latest add obra/superpowers-brainstorming
```
