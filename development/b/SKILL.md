---
name: b
description: Implements the next pending task test-first, one slice at a time, committing each task separately and recording traps and debt as it goes. Use when a plan exists and implementation should start or continue, when the user says /b, or when asked to build, implement or code a task.
---

# /b —— 实现下一个任务

## 前置

- `SPEC.md` 必须存在（没有 → 让用户先跑 `/s`，不要臆造需求）
- `tasks/todo.md` 必须存在（没有 → 先跑 `/p`）
- 工作区干净：除规划产物外有未提交改动就停下来问。逐任务提交会把无关改动裹进去，
  破坏干净回滚。
- 已与主干同步：`git fetch origin && git pull --rebase origin <主干>`

## 循环（一次一个任务）

1. 读任务的验收标准，读相关代码、现有模式、类型
2. **写失败的测试**（RED）—— 描述期望行为
3. 写最小实现让它通过（GREEN）
4. 跑全量测试查回归
5. 跑构建
6. **记录 diff 显示不出来的东西** → `docs/intent/<主题>.md`：
   - 踩到的坑（为什么这里不能直接那样写）
   - 中途放弃的做法及原因
   - 明知留下的技术债和它的上限
7. 提交：只 stage 这个任务碰的文件 + todo 状态更新，**绝不 `git add -A`**
8. 勾掉任务，停下来

## 规则

- **一次一片。** 做完一个任务停，不要顺手做下一个。
- **本地验证，不要推上去试。** 能本地跑的必须本地跑通再提交；
  把 CI / 部署当迭代循环，一轮 10 分钟换本地 1 秒。
- **不越界。** SPEC 的「非目标」是硬边界，想加就先回去改 SPEC。
- 遇到下面情况**停下来问**，不要硬闯：
  - 测试改不通或构建坏了且没有明显修法 → 用 `/ct` 或直接问
  - SPEC 有歧义，或任务需要 SPEC 没覆盖的决策
  - 高风险不可逆：认证/权限、破坏性数据迁移、支付、删除、部署、密钥，
    以及任何 `git revert` 撤不回来的操作
- 一致性契约：改了行为就同步改测试、文档、`AGENTS.md` 里描述它的段落。

## 何时进下一步

`tasks/todo.md` 全部勾完、测试全绿。然后跑 `/t` 补验收与回归，再 `/rv`。

## Red Flags

- 一个 commit 里塞了多个任务
- `docs/intent/` 这一轮一个字没加，但你至少绕过了两个坑
- 测试是后补的（先写实现再补测试 = 测试在描述实现，不是描述行为）
- 顺手改了任务范围之外的文件
