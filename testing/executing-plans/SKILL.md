---
name: executing-plans
description: 逐步按计划执行 + 复盘 — 来自 superpowers 体系。本 skill 是桥接层,完整纪律见 <SUPERPOWERS_SKILL_ROOT>/executing-plans/。
version: 4.0.0

---

# Executing-Plans(桥接到 superpowers)

## Contract

- Inputs: writing plan, passing task tests, implementation diff
- Outputs: commit history and 5-question retrospective / knowledge updates
- Gates: tests pass; verification command recorded; commit or explicit handoff state exists
- Required disciplines: `stage-gate`
- Next: next `/tdd` task or `/verification-before-completion`

> **本仓库不维护此 skill 的内容**。完整纪律请读:
> `<SUPERPOWERS_SKILL_ROOT>/executing-plans/SKILL.md`

## 何时调

- tdd 通过后,逐步 commit
- 每个 writing-plans 子任务 GREEN 后

## 衔接点

- **产出**:commit history + 5 问复盘(沉淀到知识库)
- **下一步**:下一任务(回到 `/tdd`)或 `/verification-before-completion`
- **门控**:`disciplines/stage-gate` 第 3 层(commit + 复盘 + 沉淀三件套)

## 降级方案(superpowers 未装时)

如果 `<SUPERPOWERS_SKILL_ROOT>/executing-plans/` 不存在,按以下 4 步执行 + 复盘:

### 1. 一次一个任务

- 从 plan 第 1 个**未被 blocked** 的任务开始
- 走 `/tdd` 红绿循环直到 GREEN
- ❌ 跳任务 = 中间某个依赖没建,后面全崩

### 2. commit 前 3 件套

| 件 | 内容 | 标志 |
|---|---|---|
| Verify | 跑完整验证命令看到 0 失败 | "VERIFIED:" 在 commit msg |
| Test | RED→GREEN 转换记录在 commit msg | 让人能复现 |
| 复盘 | 5 问复盘填到 commit body 或 PR | 沉淀到知识库 |

### 3. 5 问复盘模板

每次 commit 后回答 5 问:

1. **实际用时 vs 估计**:偏差多少?为什么?
2. **遇到什么意外**:踩了什么坑?
3. **有什么可以做得更好**:下次的规则/工具变更?
4. **学到什么新知识**:要写入知识库哪一篇?
5. **下一步动作**:接哪个任务 / 是否需要回头改 plan?

### 4. 进入下一个任务或停

- 下一个任务 → 回到 `/tdd`
- 全部完成 → 走 `/verification-before-completion`
- 卡住 → 停下,把 5 问复盘写到 `RETRO_<topic>.md`,向用户汇报

### 最小纪律摘要

- **不跳任务**:plan 顺序有依赖,跳 = 后面崩
- **commit 前必 verify**:`verification-before-completion` 5 步铁律
- **5 问不复盘 = 知识不沉淀**:下次再踩同一个坑
- **卡住就停,不要硬刚**:停 > 撞墙

### 安装提示

```bash
npx skills@latest add obra/superpowers-executing-plans
```
